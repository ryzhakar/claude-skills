import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "office-hours.py"
QUESTION_TOOL = "AskUserQuestion"

_spec = importlib.util.spec_from_file_location("office_hours", HOOK)
office_hours = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(office_hours)


def run_hook(project_dir, stdin_text, env=None, cwd=None):
    """Run the hook script as Claude Code does, returning its stdout."""
    if env is None:
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir))
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )
    assert result.returncode == 0
    return result.stdout


def run_main(project_dir, stdin_text):
    """Call the hook's main with in-memory streams, returning its output."""
    stdout = io.StringIO()
    office_hours.main(io.StringIO(stdin_text), stdout, Path(project_dir), "denied")
    return stdout.getvalue()


def payload(tool_name=QUESTION_TOOL):
    return json.dumps(
        {
            "session_id": "session-1",
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "tool_input": {"questions": []},
        }
    )


def mark_silent(project_dir):
    (project_dir / ".claude").mkdir(exist_ok=True)
    (project_dir / ".claude" / "work-silently").touch()


def test_marker_present_denies_question(tmp_path):
    mark_silent(tmp_path)
    output = json.loads(run_hook(tmp_path, payload()))["hookSpecificOutput"]
    assert output["hookEventName"] == "PreToolUse"
    assert output["permissionDecision"] == "deny"
    reason = output["permissionDecisionReason"]
    assert isinstance(reason, str) and reason


def test_main_denies_with_the_reason_handed_in(tmp_path):
    mark_silent(tmp_path)
    output = json.loads(run_main(tmp_path, payload()))["hookSpecificOutput"]
    assert output["permissionDecisionReason"] == "denied"


def test_marker_absent_allows_question(tmp_path):
    assert run_hook(tmp_path, payload()) == ""


def test_other_tool_untouched_under_marker(tmp_path):
    mark_silent(tmp_path)
    assert run_hook(tmp_path, payload("Bash")) == ""


def test_malformed_payload_allows(tmp_path):
    mark_silent(tmp_path)
    assert run_hook(tmp_path, "{not json") == ""


def test_non_object_payload_allows(tmp_path):
    mark_silent(tmp_path)
    assert run_hook(tmp_path, "[]") == ""


def test_missing_tool_name_allows(tmp_path):
    mark_silent(tmp_path)
    assert run_hook(tmp_path, json.dumps({"session_id": "session-1"})) == ""


def test_marker_directory_allows(tmp_path):
    (tmp_path / ".claude" / "work-silently").mkdir(parents=True)
    assert run_hook(tmp_path, payload()) == ""


def test_unset_project_dir_falls_back_to_working_directory(tmp_path):
    mark_silent(tmp_path)
    env = {key: value for key, value in os.environ.items() if key != "CLAUDE_PROJECT_DIR"}
    output = run_hook(tmp_path, payload(), env=env, cwd=tmp_path)
    assert json.loads(output)["hookSpecificOutput"]["permissionDecision"] == "deny"


OTHER_TOOLS = ["Bash", "Edit", "Read", "Agent", "askuserquestion", "AskUserQuestion ", "", None, 0, ["AskUserQuestion"]]
NON_JSON_INPUTS = ["", " ", "{not json", "AskUserQuestion", "{'tool_name': 'AskUserQuestion'}", "[1,", "\x00", "nan?"]


@pytest.mark.parametrize("tool_name", OTHER_TOOLS)
def test_any_other_tool_allowed_under_marker(tmp_path, tool_name):
    mark_silent(tmp_path)
    assert run_main(tmp_path, payload(tool_name)) == ""


@pytest.mark.parametrize("stdin_text", NON_JSON_INPUTS)
def test_any_non_json_stdin_allowed_under_marker(tmp_path, stdin_text):
    mark_silent(tmp_path)
    assert run_main(tmp_path, stdin_text) == ""
