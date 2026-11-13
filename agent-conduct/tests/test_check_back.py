import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "check-back.py"
HOOK_SPEC = importlib.util.spec_from_file_location("check_back", HOOK)
HOOK_MODULE = importlib.util.module_from_spec(HOOK_SPEC)
HOOK_SPEC.loader.exec_module(HOOK_MODULE)
OBSERVED_LINE_CAP = HOOK_MODULE.OBSERVED_STATES_LINE_CAP
PRODUCING_WINDOW_SECONDS = HOOK_MODULE.PRODUCING_WINDOW_SECONDS
FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "stop-payload.json").read_text())
SESSION_ID = FIXTURE["session_id"]
PROJECT_SLUG = Path(FIXTURE["transcript_path"]).parent.name
STALE_AGE_SECONDS = 3600
FUTURE_AGE_SECONDS = -STALE_AGE_SECONDS
TEAMMATE_COUNT_AT_REAL_SCALE = 500
SCALE_TIME_BUDGET_SECONDS = 2.0


def tasks_dir(tmp_path):
    return tmp_path / "tmp" / PROJECT_SLUG / SESSION_ID / "tasks"


def write_transcript(tmp_path, task_id, size, age_seconds=STALE_AGE_SECONDS):
    transcript = tmp_path / "transcripts" / f"{task_id}.jsonl"
    transcript.parent.mkdir(parents=True, exist_ok=True)
    transcript.write_bytes(b"x" * size)
    moment = time.time() - age_seconds
    os.utime(transcript, (moment, moment))
    link = tasks_dir(tmp_path) / f"{task_id}.output"
    link.parent.mkdir(parents=True, exist_ok=True)
    if not link.is_symlink():
        link.symlink_to(transcript)


def project_transcript_path(tmp_path):
    return str(tmp_path / "projects" / PROJECT_SLUG / f"{SESSION_ID}.jsonl")


def write_teammate_transcript(tmp_path, task_id, size, age_seconds=STALE_AGE_SECONDS, description=None, file_stem=None):
    directory = tmp_path / "projects" / PROJECT_SLUG / SESSION_ID / "subagents"
    directory.mkdir(parents=True, exist_ok=True)
    stem = file_stem or f"agent-a{task_id}-0123456789abcdef"
    meta = {"taskKind": "in_process_teammate", "description": description or f"work {task_id}", "name": task_id}
    (directory / f"{stem}.meta.json").write_text(json.dumps(meta))
    transcript = directory / f"{stem}.jsonl"
    transcript.write_bytes(b"x" * size)
    moment = time.time() - age_seconds
    os.utime(transcript, (moment, moment))


def run_stop(tmp_path, tasks, crons=None, stop_hook_active=False, data_dir_set=True, transcript_path=None):
    payload = {
        **FIXTURE,
        "background_tasks": tasks,
        "session_crons": crons or [],
        "stop_hook_active": stop_hook_active,
        "transcript_path": project_transcript_path(tmp_path) if transcript_path is None else transcript_path,
    }
    env = {key: value for key, value in os.environ.items() if key != "CLAUDE_PLUGIN_DATA"}
    env["CHECK_BACK_TASKS_ROOT"] = str(tmp_path / "tmp")
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


def test_running_shell_is_pending(tmp_path):
    reason = run_stop(tmp_path, [task("s1", "shell", "running")])
    assert 'Still running with no wake set: the background command "work s1" (task s1).' in reason
    assert "task s1" in state_text(tmp_path)


def test_idle_agent_with_flat_transcript_is_not_pending(tmp_path):
    write_transcript(tmp_path, "a1", size=500)
    reason = run_stop(tmp_path, [task("a1", "subagent", "running")])
    assert reason == ""
    assert state_text(tmp_path) == ""


def test_agent_written_within_the_window_is_pending(tmp_path):
    write_transcript(tmp_path, "a1", size=500, age_seconds=PRODUCING_WINDOW_SECONDS // 2)
    reason = run_stop(tmp_path, [task("a1", "subagent", "running")])
    assert 'the background agent "work a1" (task a1)' in reason
    assert "task a1" in state_text(tmp_path)


def test_agent_whose_transcript_grew_since_the_previous_stop_is_pending(tmp_path):
    write_transcript(tmp_path, "a1", size=500)
    assert run_stop(tmp_path, [task("a1", "subagent", "running")]) == ""
    write_transcript(tmp_path, "a1", size=900)
    reason = run_stop(tmp_path, [task("a1", "subagent", "running")])
    assert "task a1" in reason


def test_agent_whose_transcript_stayed_flat_between_stops_is_not_pending(tmp_path):
    write_transcript(tmp_path, "a1", size=500)
    run_stop(tmp_path, [task("a1", "subagent", "running")])
    assert run_stop(tmp_path, [task("a1", "subagent", "running")]) == ""


def test_busy_teammate_is_pending(tmp_path):
    write_teammate_transcript(tmp_path, "t1", size=500, age_seconds=PRODUCING_WINDOW_SECONDS // 2)
    reason = run_stop(tmp_path, [task("t1", "teammate", "running")])
    assert 'the teammate task "work t1" (task t1)' in reason
    assert "task t1" in state_text(tmp_path)


def test_idle_teammate_is_not_pending(tmp_path):
    write_teammate_transcript(tmp_path, "t1", size=500)
    assert run_stop(tmp_path, [task("t1", "teammate", "running")]) == ""
    assert state_text(tmp_path) == ""


def test_many_idle_teammates_do_not_block(tmp_path):
    ids = [f"t{n}" for n in range(125)]
    for task_id in ids:
        write_teammate_transcript(tmp_path, task_id, size=500)
    assert run_stop(tmp_path, [task(i, "teammate", "running") for i in ids]) == ""
    assert state_text(tmp_path) == ""


def test_teammate_whose_transcript_grew_since_the_previous_stop_is_pending(tmp_path):
    write_teammate_transcript(tmp_path, "t1", size=500)
    assert run_stop(tmp_path, [task("t1", "teammate", "running")]) == ""
    write_teammate_transcript(tmp_path, "t1", size=900)
    assert "task t1" in run_stop(tmp_path, [task("t1", "teammate", "running")])


def test_only_the_busy_teammate_is_named(tmp_path):
    write_teammate_transcript(tmp_path, "t1", size=500, age_seconds=0)
    write_teammate_transcript(tmp_path, "t2", size=500)
    reason = run_stop(tmp_path, [task("t1", "teammate", "running"), task("t2", "teammate", "running")])
    assert "task t1" in reason and "task t2" not in reason


def test_five_hundred_idle_teammates_are_checked_within_the_time_budget(tmp_path):
    ids = [f"t{n}" for n in range(TEAMMATE_COUNT_AT_REAL_SCALE)]
    for task_id in ids:
        write_teammate_transcript(tmp_path, task_id, size=500)
    started = time.monotonic()
    reason = run_stop(tmp_path, [task(i, "teammate", "running") for i in ids])
    assert reason == ""
    assert time.monotonic() - started < SCALE_TIME_BUDGET_SECONDS


def test_teammate_with_a_future_dated_transcript_is_not_pending(tmp_path):
    write_teammate_transcript(tmp_path, "t1", size=500, age_seconds=FUTURE_AGE_SECONDS)
    assert run_stop(tmp_path, [task("t1", "teammate", "running")]) == ""


def test_subagent_with_a_future_dated_transcript_is_not_pending(tmp_path):
    write_transcript(tmp_path, "a1", size=500, age_seconds=FUTURE_AGE_SECONDS)
    assert run_stop(tmp_path, [task("a1", "subagent", "running")]) == ""


def test_teammates_sharing_a_description_follow_the_newest_transcript(tmp_path):
    write_teammate_transcript(tmp_path, "t1", size=500, description="shared work", file_stem="agent-aold")
    write_teammate_transcript(tmp_path, "t2", size=500, age_seconds=0, description="shared work", file_stem="agent-anew")
    reason = run_stop(tmp_path, [{"id": "t9", "type": "teammate", "status": "running", "description": "shared work"}])
    assert "task t9" in reason


def test_fixture_teammate_is_joined_to_its_meta_by_the_real_description(tmp_path):
    entry = next(t for t in FIXTURE["background_tasks"] if t["type"] == "teammate")
    write_teammate_transcript(
        tmp_path, entry["id"], size=500, age_seconds=0, description=entry["description"], file_stem="agent-aretire-just-231d0af3b6cf8a06"
    )
    assert f"task {entry['id']}" in run_stop(tmp_path, [entry])


def test_agent_without_a_transcript_is_not_pending(tmp_path):
    assert run_stop(tmp_path, [task("t1", "teammate", "running")]) == ""
    assert state_text(tmp_path) == ""


@pytest.mark.parametrize("status", ["completed", "DONE ", "failed", "killed", "cancelled", "stopped", "finished"])
def test_finished_agent_is_not_pending_even_while_its_transcript_is_fresh(tmp_path, status):
    write_transcript(tmp_path, "a1", size=500, age_seconds=0)
    assert run_stop(tmp_path, [task("a1", "subagent", status)]) == ""


def test_payload_without_a_transcript_path_leaves_agents_not_pending(tmp_path):
    write_transcript(tmp_path, "a1", size=500, age_seconds=0)
    assert run_stop(tmp_path, [task("a1", "subagent", "running")], transcript_path="") == ""


def test_skipped_tasks_leave_reason_and_state_of_pending_ones_alone(tmp_path):
    tasks = [
        task("s1", "shell", "running"),
        task("t1", "teammate", "running"),
        task("t2", "teammate", "completed"),
    ]
    write_teammate_transcript(tmp_path, "t1", size=500)
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
