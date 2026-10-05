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
PLUGIN_PREFIX = "dev-discipline:"
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


def agent_kind(agent_type):
    kind = agent_type[len(PLUGIN_PREFIX):] if agent_type.startswith(PLUGIN_PREFIX) else agent_type
    return kind if kind in STAGE_OPENED_BY_STOP else None


def state_path(session_id):
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
    if not data_dir or not session_id:
        return None
    safe_session = re.sub(r"[^A-Za-z0-9_-]", "-", session_id)
    return Path(data_dir) / "review-chain" / f"{safe_session}.json"


def load_pending(path):
    try:
        pending = json.loads(path.read_text())
    except (OSError, ValueError):
        return []
    return pending if isinstance(pending, list) else []


def prune_expired(directory):
    cutoff = time.time() - STATE_TTL_SECONDS
    for sibling in directory.glob("*.json"):
        try:
            if sibling.stat().st_mtime < cutoff:
                sibling.unlink()
        except OSError:
            pass


def save_pending(path, pending):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        prune_expired(path.parent)
        if pending:
            path.write_text(json.dumps(pending))
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


def on_subagent_stop(data, pending):
    kind = agent_kind(data.get("agent_type") or "")
    if kind is None:
        return None
    open_stage(pending, STAGE_OPENED_BY_STOP[kind], data.get("agent_id") or "unknown", data.get("last_assistant_message") or "")
    return None


def on_post_tool_use(data, pending):
    if data.get("tool_name") != "Agent":
        return None
    tool_input = data.get("tool_input") or {}
    tool_response = data.get("tool_response") or {}
    kind = agent_kind(tool_input.get("subagent_type") or "")
    if kind is None:
        return None
    status = tool_response.get("status")
    if status == "async_launched":
        retire_stage(pending, STAGE_SATISFIED_BY_LAUNCH[kind])
        return None
    if status == "completed":
        stage = STAGE_OPENED_BY_STOP[kind]
        open_stage(pending, stage, tool_response.get("agentId") or "unknown", text_of(tool_response.get("content")))
        return hook_output("PostToolUse", mandate_for(stage, pending[-1]))
    return None


def on_stop(data, pending):
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
    pending = load_pending(path)
    output = handler(data, pending)
    save_pending(path, pending)
    if output is not None:
        json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
    sys.exit(0)
