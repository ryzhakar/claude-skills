#!/usr/bin/env python3
"""check-back hooks.

stop:   Stop hook. Records in-flight background tasks for this session and
        keeps the turn going while a command or an agent producing output runs with no wake set.
resume: SessionStart hook (resume). Names what the old session left running.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE_TTL_SECONDS = 7 * 24 * 3600
OBSERVED_STATES_FILE = "observed-task-states"
OBSERVED_STATES_LINE_CAP = 200
FINISHED_STATUSES = frozenset({"completed", "finished", "done", "stopped", "failed", "killed", "cancelled"})
AGENT_TYPES = frozenset({"subagent", "teammate"})
TEAMMATE_TASK_KIND = "in_process_teammate"
META_SUFFIX = ".meta.json"
TRANSCRIPT_SUFFIX = ".jsonl"
PRODUCING_WINDOW_SECONDS = 120
OUTPUT_SIZES_SUFFIX = ".output-sizes"
DEFAULT_TASKS_ROOT_PARENT = "/tmp"
WAKE_TASK_TYPE = "monitor"
LABELS = {"shell": "the background command", "subagent": "the background agent", "monitor": "the Monitor watch"}


def template(name):
    return (HERE / "templates" / name).read_text().strip()


def state_file(session_id):
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
    if not data_dir or not session_id:
        return None
    safe = re.sub(r"[^A-Za-z0-9_-]", "-", session_id)
    return Path(data_dir) / "check-back" / safe


def describe(task):
    label = LABELS.get(task.get("type"), f"the {task.get('type') or 'background'} task")
    what = task.get("description") or task.get("command") or task.get("name") or ""
    what = " ".join(what.split())[:200]
    ident = task.get("id") or "unknown"
    return f"{label} \"{what}\" (task {ident})" if what else f"{label} (task {ident})"


def task_status(task):
    """Return the task's status lower-cased and stripped, empty when absent."""
    return str(task.get("status") or "").strip().lower()


def output_path(tasks_root, data, task):
    """Return where the harness links the task's output transcript, None when the payload lacks the parts."""
    slug = Path(data.get("transcript_path") or "").parent.name
    session_id, task_id = data.get("session_id"), task.get("id")
    if not (slug and session_id and task_id):
        return None
    return tasks_root / slug / session_id / "tasks" / f"{task_id}.output"


def transcript_stat(path):
    """Return the stat of the file the path resolves to, None when absent or unreadable."""
    if path is None:
        return None
    try:
        return path.stat()
    except OSError:
        return None


def teammate_description(meta_path):
    """Return the description in a teammate meta file, None for any other or unreadable file."""
    try:
        meta = json.loads(meta_path.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(meta, dict) or meta.get("taskKind") != TEAMMATE_TASK_KIND:
        return None
    return meta.get("description")


def newest_by_description(entries):
    """Return the entry with the latest mtime for each description."""
    newest = {}
    for description, transcript in entries:
        known = newest.get(description)
        if known is None or transcript.st_mtime > known.st_mtime:
            newest[description] = transcript
    return newest


def teammate_transcripts(data):
    """Return the session's teammate transcript stats by description, the newest where descriptions repeat."""
    session_id = data.get("session_id")
    project_dir = Path(data.get("transcript_path") or "").parent
    if not (session_id and project_dir.name):
        return {}
    entries = []
    for meta_path in (project_dir / session_id / "subagents").glob("*" + META_SUFFIX):
        description = teammate_description(meta_path)
        transcript = transcript_stat(meta_path.with_name(meta_path.name[: -len(META_SUFFIX)] + TRANSCRIPT_SUFFIX))
        if description is not None and transcript is not None:
            entries.append((description, transcript))
    return newest_by_description(entries)


def agent_transcripts(tasks_root, data, tasks):
    """Return each agent task's transcript stat by task id."""
    agents = [t for t in tasks if t.get("type") in AGENT_TYPES]
    by_description = teammate_transcripts(data) if any(t.get("type") == "teammate" for t in agents) else {}
    return {
        t.get("id"): by_description.get(t.get("description"))
        if t.get("type") == "teammate"
        else transcript_stat(output_path(tasks_root, data, t))
        for t in agents
    }


def is_producing_output(transcript, previous_size, now):
    """Tell whether the transcript grew since the previous stop or was written within the producing window."""
    if transcript is None:
        return False
    grew = previous_size is not None and transcript.st_size > previous_size
    return grew or 0 <= now - transcript.st_mtime <= PRODUCING_WINDOW_SECONDS


def is_awaited(task, transcripts, previous_sizes, now):
    """Tell whether the task is unfinished and, for an agent, producing output."""
    if task_status(task) in FINISHED_STATUSES:
        return False
    if task.get("type") not in AGENT_TYPES:
        return True
    return is_producing_output(transcripts.get(task.get("id")), previous_sizes.get(task.get("id")), now)


def load_output_sizes(path):
    """Return the transcript sizes recorded at the previous stop, empty when unreadable."""
    try:
        sizes = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    return sizes if isinstance(sizes, dict) else {}


def save_output_sizes(path, transcripts):
    """Record the present transcript sizes by task id, never raising."""
    sizes = {task_id: t.st_size for task_id, t in transcripts.items() if t is not None}
    try:
        path.write_text(json.dumps(sizes))
    except OSError:
        pass


def observed_state_line(task):
    """Return the task's type and status as one tab-separated line."""
    return f"{task.get('type') or ''}\t{task_status(task)}"


def fresh_observed_lines(known, tasks):
    """Return the unrecorded type-status lines that still fit under the line cap."""
    fresh = []
    for line in map(observed_state_line, tasks):
        if line not in known and line not in fresh:
            fresh.append(line)
    return fresh[: max(OBSERVED_STATES_LINE_CAP - len(known), 0)]


def record_observed_states(directory, tasks):
    """Append the tasks' unrecorded type-status lines to the observed-states file, never raising."""
    path = directory / OBSERVED_STATES_FILE
    try:
        known = path.read_text().splitlines() if path.exists() else []
        fresh = fresh_observed_lines(known, tasks)
        if fresh:
            with path.open("a") as handle:
                handle.write("\n".join(fresh) + "\n")
    except (OSError, ValueError):
        pass


def registry_reachable(tasks, crons):
    """Tell whether the payload carries the task and cron registries."""
    return isinstance(tasks, list) and isinstance(crons, list)


def is_continued_turn(data):
    """Tell whether a Stop hook already continued this turn."""
    return bool(data.get("stop_hook_active"))


def is_wake(task):
    """Tell whether the task is itself a wake."""
    return task.get("type") == WAKE_TASK_TYPE


def prune(directory):
    cutoff = time.time() - STATE_TTL_SECONDS
    for path in directory.glob("*"):
        if path.name == OBSERVED_STATES_FILE:
            continue
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink()
        except OSError:
            pass


def stop(data, tasks_root, now):
    tasks = data.get("background_tasks")
    crons = data.get("session_crons")
    if not registry_reachable(tasks, crons):
        return

    path = state_file(data.get("session_id"))
    sizes_path = path.with_name(path.name + OUTPUT_SIZES_SUFFIX) if path is not None else None
    previous_sizes = load_output_sizes(sizes_path) if sizes_path is not None else {}
    transcripts = agent_transcripts(tasks_root, data, tasks)
    awaited = [t for t in tasks if is_awaited(t, transcripts, previous_sizes, now)]
    if path is not None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            prune(path.parent)
            save_output_sizes(sizes_path, transcripts)
            if awaited:
                path.write_text("\n".join(describe(t) for t in awaited) + "\n")
            elif path.exists():
                path.unlink()
        except OSError:
            pass
        record_observed_states(path.parent, tasks)

    if is_continued_turn(data):
        return
    watches = [t for t in awaited if is_wake(t)]
    pending = [t for t in awaited if not is_wake(t)]
    if not pending or crons or watches:
        return

    reason = (
        template("check-back-stop.txt")
        + " Still running with no wake set: "
        + "; ".join(describe(t) for t in pending)
        + "."
    )
    json.dump(
        {"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": reason}},
        sys.stdout,
    )


def resume(data):
    if data.get("source") != "resume":
        return
    path = state_file(data.get("session_id"))
    if path is None or not path.is_file():
        return
    try:
        items = [line for line in path.read_text().splitlines() if line.strip()]
        path.unlink()
    except OSError:
        return
    if not items:
        return
    sys.stdout.write(
        template("check-back-resume.txt")
        + " Running when that session ended: "
        + "; ".join(items)
        + ".\n"
    )


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    if not isinstance(data, dict):
        return
    if mode == "stop":
        tasks_root = Path(os.environ.get("CHECK_BACK_TASKS_ROOT") or f"{DEFAULT_TASKS_ROOT_PARENT}/claude-{os.getuid()}")
        stop(data, tasks_root, time.time())
    elif mode == "resume":
        resume(data)


if __name__ == "__main__":
    main()
    sys.exit(0)
