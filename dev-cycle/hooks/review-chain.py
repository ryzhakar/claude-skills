#!/usr/bin/env python3
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE_TTL_SECONDS = 7 * 24 * 3600
CONTINUATIONS_PER_STAGE = 3
MESSAGE_HEAD_CHARS = 300
PLUGIN_PREFIX = "dev-cycle:"
STAGE_OPENED_BY_STOP = {
    "implementer": "spec-review",
    "spec-reviewer": "quality-review",
    "code-quality-reviewer": "merge-decision",
}
STAGE_SATISFIED_BY_LAUNCH = {
    "spec-reviewer": "spec-review",
    "code-quality-reviewer": "quality-review",
    "implementer": "merge-decision",
}
MANDATE_TEMPLATE = {
    "spec-review": "review-mandate.txt",
    "quality-review": "quality-review-mandate.txt",
    "merge-decision": "merge-mandate.txt",
}
STAGES_INJECTED_ONCE = {"merge-decision"}
DONE_STATUS = re.compile(r"Status:\s*DONE\b")
EMPTY_STATE = {"pending": [], "agents": {}}


def agent_kind(agent_type):
    kind = agent_type[len(PLUGIN_PREFIX):] if agent_type.startswith(PLUGIN_PREFIX) else agent_type
    return kind if kind in STAGE_OPENED_BY_STOP else None


def state_path(session_id):
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
    if not data_dir or not session_id:
        return None
    safe_session = re.sub(r"[^A-Za-z0-9_-]", "-", session_id)
    return Path(data_dir) / "review-chain" / f"{safe_session}.json"


def load_state(path):
    try:
        state = json.loads(path.read_text())
    except (OSError, ValueError):
        return json.loads(json.dumps(EMPTY_STATE))
    if not isinstance(state, dict) or not isinstance(state.get("pending"), list) or not isinstance(state.get("agents"), dict):
        return json.loads(json.dumps(EMPTY_STATE))
    return state


def prune_expired(directory):
    cutoff = time.time() - STATE_TTL_SECONDS
    for sibling in directory.glob("*.json"):
        try:
            if sibling.stat().st_mtime < cutoff:
                sibling.unlink()
        except OSError:
            pass


def save_state(path, state):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        prune_expired(path.parent)
        if state["pending"] or state["agents"]:
            path.write_text(json.dumps(state))
        elif path.exists():
            path.unlink()
    except OSError:
        pass


def mandate_for(stage, record):
    text = (HERE / "templates" / MANDATE_TEMPLATE[stage]).read_text().strip()
    head = record.get("head", "")
    return f"{text} The stopped agent's report began: {head}" if head else text


def hook_output(event, text):
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def open_stage(pending, stage, agent_id, message):
    if any(record["stage"] == stage and record["agent_id"] == agent_id for record in pending):
        return
    pending.append({
        "stage": stage,
        "agent_id": agent_id,
        "since": time.time(),
        "head": " ".join(message.split())[:MESSAGE_HEAD_CHARS],
        "continuations": 0,
    })


def retire_stage(pending, stage):
    for index, record in enumerate(pending):
        if record["stage"] == stage:
            del pending[index]
            return


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(block.get("text", "") for block in content if isinstance(block, dict))
    return ""


MALFORMED = re.compile(r"^\s*Dispatch malformed:")


def stop_opens_a_stage(kind, message):
    if MALFORMED.search(message):
        return False
    return kind != "implementer" or DONE_STATUS.search(message) is not None


def on_subagent_stop(data, state):
    kind = agent_kind(data.get("agent_type") or "")
    if kind is None:
        return None
    agent_id = data.get("agent_id") or "unknown"
    message = data.get("last_assistant_message") or ""
    state["agents"][agent_id] = kind
    if stop_opens_a_stage(kind, message):
        open_stage(state["pending"], STAGE_OPENED_BY_STOP[kind], agent_id, message)
    return None


def on_agent_tool(tool_input, tool_response, state):
    kind = agent_kind(tool_input.get("subagent_type") or "")
    if kind is None:
        return None
    agent_id = tool_response.get("agentId") or "unknown"
    status = tool_response.get("status")
    state["agents"][agent_id] = kind
    if status == "async_launched":
        retire_stage(state["pending"], STAGE_SATISFIED_BY_LAUNCH[kind])
        return None
    if status == "completed":
        message = text_of(tool_response.get("content"))
        if not stop_opens_a_stage(kind, message):
            return None
        stage = STAGE_OPENED_BY_STOP[kind]
        open_stage(state["pending"], stage, agent_id, message)
        return hook_output("PostToolUse", mandate_for(stage, state["pending"][-1]))
    return None


def on_send_message(tool_input, state):
    kind = state["agents"].get(tool_input.get("to") or "")
    if kind is not None:
        retire_stage(state["pending"], STAGE_SATISFIED_BY_LAUNCH[kind])
    return None


def on_post_tool_use(data, state):
    tool_input = data.get("tool_input") or {}
    tool_response = data.get("tool_response") or {}
    if data.get("tool_name") == "Agent":
        return on_agent_tool(tool_input, tool_response, state)
    if data.get("tool_name") == "SendMessage":
        return on_send_message(tool_input, state)
    return None


def on_stop(data, state):
    pending = state["pending"]
    if not pending:
        return None
    record = pending[0]
    stage = record["stage"]
    if stage in STAGES_INJECTED_ONCE:
        del pending[0]
        return hook_output("Stop", mandate_for(stage, record))
    if record["continuations"] >= CONTINUATIONS_PER_STAGE:
        del pending[0]
        return None
    record["continuations"] += 1
    return hook_output("Stop", mandate_for(stage, record))


HANDLERS = {
    "SubagentStop": on_subagent_stop,
    "PostToolUse": on_post_tool_use,
    "Stop": on_stop,
}


def main():
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    if not isinstance(data, dict):
        return
    handler = HANDLERS.get(data.get("hook_event_name"))
    path = state_path(data.get("session_id"))
    if handler is None or path is None:
        return
    state = load_state(path)
    output = handler(data, state)
    save_state(path, state)
    if output is not None:
        json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
    sys.exit(0)
