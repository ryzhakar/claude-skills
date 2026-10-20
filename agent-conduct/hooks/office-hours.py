#!/usr/bin/env python3
"""Deny AskUserQuestion while the silence marker exists."""
import json
import os
import sys
from pathlib import Path
from typing import TextIO

HERE = Path(__file__).resolve().parent
QUESTION_TOOL = "AskUserQuestion"
MARKER_PATH_PARTS = (".claude", "work-silently")
SILENCE_TEMPLATE = HERE / "templates" / "office-hours-silence.txt"


def marker(project_dir: Path) -> Path:
    """Return the silence marker's path under the project directory."""
    return project_dir.joinpath(*MARKER_PATH_PARTS)


def main(stdin: TextIO, stdout: TextIO, project_dir: Path, reason: str) -> None:
    """Write a deny decision for a question-tool payload while the marker is a file."""
    try:
        data = json.load(stdin)
    except (ValueError, OSError):
        return
    if not isinstance(data, dict) or data.get("tool_name") != QUESTION_TOOL:
        return
    if not marker(project_dir).is_file():
        return
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        stdout,
    )


if __name__ == "__main__":
    main(
        sys.stdin,
        sys.stdout,
        Path(os.environ.get("CLAUDE_PROJECT_DIR") or "."),
        SILENCE_TEMPLATE.read_text().strip(),
    )
    sys.exit(0)
