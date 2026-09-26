#!/usr/bin/env python3
"""check-back hooks.

stop:   Stop hook. Records in-flight background tasks for this session and
        keeps the turn going while tasks run with no wake set.
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


def prune(directory):
    cutoff = time.time() - STATE_TTL_SECONDS
    for path in directory.glob("*"):
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink()
        except OSError:
            pass


def stop(data):
    tasks = data.get("background_tasks")
    crons = data.get("session_crons")
    # Registry unreachable: nothing is known, so nothing is claimed.
    if not isinstance(tasks, list) or not isinstance(crons, list):
        return

    path = state_file(data.get("session_id"))
    if path is not None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            prune(path.parent)
            if tasks:
                path.write_text("\n".join(describe(t) for t in tasks) + "\n")
            elif path.exists():
                path.unlink()
        except OSError:
            pass

    # Loop guard: a turn already continued by a Stop hook ends.
    if data.get("stop_hook_active"):
        return
    # A running Monitor watch is itself a wake.
    watches = [t for t in tasks if t.get("type") == "monitor"]
    pending = [t for t in tasks if t.get("type") != "monitor"]
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
        stop(data)
    elif mode == "resume":
        resume(data)


if __name__ == "__main__":
    main()
    sys.exit(0)
