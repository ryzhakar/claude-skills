import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "check-back.py"
SESSION_ID = "session-1"
OBSERVED_LINE_CAP = 200


def run_stop(tmp_path, tasks, crons=None, stop_hook_active=False, data_dir_set=True):
    payload = {
        "session_id": SESSION_ID,
        "background_tasks": tasks,
        "session_crons": crons or [],
        "stop_hook_active": stop_hook_active,
    }
    env = {key: value for key, value in os.environ.items() if key != "CLAUDE_PLUGIN_DATA"}
    if data_dir_set:
        env["CLAUDE_PLUGIN_DATA"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, str(HOOK), "stop"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    if not result.stdout:
        return ""
    return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]


def state_text(tmp_path):
    path = tmp_path / "check-back" / SESSION_ID
    return path.read_text() if path.exists() else ""


def observed_lines(tmp_path):
    path = tmp_path / "check-back" / "observed-task-states"
    return path.read_text().splitlines() if path.exists() else []


def task(task_id, task_type, status=None):
    entry = {"id": task_id, "type": task_type, "description": f"work {task_id}"}
    if status is not None:
        entry["status"] = status
    return entry


def test_idle_teammate_is_not_nagged_about(tmp_path):
    reason = run_stop(tmp_path, [task("t1", "teammate", "idle")])
    assert reason == ""
    assert state_text(tmp_path) == ""


def test_running_shell_is_pending(tmp_path):
    reason = run_stop(tmp_path, [task("s1", "shell", "running")])
    assert 'Still running with no wake set: the background command "work s1" (task s1).' in reason
    assert "task s1" in state_text(tmp_path)


def test_running_subagent_is_pending(tmp_path):
    reason = run_stop(tmp_path, [task("a1", "subagent", "running")])
    assert 'the background agent "work a1" (task a1)' in reason
    assert "task a1" in state_text(tmp_path)


@pytest.mark.parametrize(
    "status",
    ["completed", "Idle ", "DONE", "failed", "killed", "cancelled", "stopped", "finished"],
)
def test_finished_or_idle_teammate_is_skipped(tmp_path, status):
    reason = run_stop(tmp_path, [task("t1", "teammate", status)])
    assert reason == ""
    assert state_text(tmp_path) == ""


@pytest.mark.parametrize("status", [None, "mystery", ""])
def test_missing_or_unknown_status_stays_pending(tmp_path, status):
    reason = run_stop(tmp_path, [task("t1", "teammate", status)])
    assert "task t1" in reason
    assert "task t1" in state_text(tmp_path)


def test_skipped_tasks_leave_reason_and_state_of_pending_ones_alone(tmp_path):
    tasks = [
        task("s1", "shell", "running"),
        task("t1", "teammate", "idle"),
        task("t2", "teammate", "completed"),
    ]
    reason = run_stop(tmp_path, tasks)
    assert "task s1" in reason
    assert "t1" not in reason and "t2" not in reason
    assert state_text(tmp_path) == 'the background command "work s1" (task s1)\n'


def test_monitor_is_a_wake(tmp_path):
    reason = run_stop(tmp_path, [task("m1", "monitor", "running"), task("s1", "shell", "running")])
    assert reason == ""
    assert "task s1" in state_text(tmp_path)


def test_cron_is_a_wake(tmp_path):
    assert run_stop(tmp_path, [task("s1", "shell", "running")], crons=[{"id": "c1"}]) == ""


def test_stop_hook_active_ends_the_loop(tmp_path):
    assert run_stop(tmp_path, [task("s1", "shell", "running")], stop_hook_active=True) == ""
    assert "task s1" in state_text(tmp_path)


def test_unreachable_registry_claims_nothing(tmp_path):
    assert run_stop(tmp_path, None) == ""


def test_new_type_status_pairs_are_recorded_once(tmp_path):
    tasks = [
        task("t1", "teammate", "idle"),
        task("s1", "shell", "running"),
        task("t2", "teammate", "idle"),
        task("x", "workflow"),
    ]
    run_stop(tmp_path, tasks)
    run_stop(tmp_path, tasks)
    assert observed_lines(tmp_path) == ["teammate\tidle", "shell\trunning", "workflow\t"]


def test_observed_states_are_capped(tmp_path):
    tasks = [task(f"t{n}", "teammate", f"state-{n}") for n in range(OBSERVED_LINE_CAP + 50)]
    run_stop(tmp_path, tasks)
    assert len(observed_lines(tmp_path)) == OBSERVED_LINE_CAP


def test_corrupt_observed_states_file_does_not_break_the_hook_or_state_write(tmp_path):
    directory = tmp_path / "check-back"
    directory.mkdir()
    (directory / "observed-task-states").write_bytes(b"\xff\xfe\x80\x81\n")
    reason = run_stop(tmp_path, [task("s1", "shell", "running")])
    assert "task s1" in reason
    assert "task s1" in state_text(tmp_path)


def test_unset_data_dir_writes_nothing(tmp_path):
    reason = run_stop(tmp_path, [task("s1", "shell", "running")], data_dir_set=False)
    assert "task s1" in reason
    assert list(tmp_path.iterdir()) == []
