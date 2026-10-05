import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parent.parent
SCRIPT = HOOKS_DIR / "review-chain.py"
SESSION = "session-under-test"


@pytest.fixture
def run_hook(tmp_path):
    def run(event, **fields):
        payload = {"session_id": SESSION, "hook_event_name": event, **fields}
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env={"CLAUDE_PLUGIN_DATA": str(tmp_path), "CLAUDE_PLUGIN_ROOT": str(HOOKS_DIR), "PATH": "/usr/bin:/bin"},
        )
        assert completed.returncode == 0, completed.stderr
        return json.loads(completed.stdout) if completed.stdout.strip() else None

    return run


def context_of(output):
    return output["hookSpecificOutput"]["additionalContext"]


def subagent_stopped(run_hook, agent_type, message="Status: DONE\nWorktree: /tmp/wt"):
    return run_hook("SubagentStop", agent_type=agent_type, agent_id="agent-1", last_assistant_message=message, stop_hook_active=False)


def agent_launched(run_hook, subagent_type):
    return run_hook("PostToolUse", tool_name="Agent", tool_input={"subagent_type": subagent_type, "prompt": "x"}, tool_response={"status": "async_launched", "agentId": "a1"})


def agent_completed(run_hook, subagent_type):
    return run_hook("PostToolUse", tool_name="Agent", tool_input={"subagent_type": subagent_type, "prompt": "x"}, tool_response={"status": "completed", "agentId": "a1", "content": [{"type": "text", "text": "Status: DONE"}]})


def orchestrator_stops(run_hook):
    return run_hook("Stop", stop_hook_active=False, last_assistant_message="done")


def test_implementer_stop_makes_the_orchestrator_launch_the_spec_review(run_hook):
    subagent_stopped(run_hook, "dev-discipline:implementer", "Status: DONE\nWorktree: /tmp/wt-auth")
    output = orchestrator_stops(run_hook)
    assert output["hookSpecificOutput"]["hookEventName"] == "Stop"
    assert "spec-reviewer" in context_of(output)
    assert "/tmp/wt-auth" in context_of(output)


def test_launching_the_spec_review_clears_the_mandate(run_hook):
    subagent_stopped(run_hook, "dev-discipline:implementer")
    agent_launched(run_hook, "dev-discipline:spec-reviewer")
    assert orchestrator_stops(run_hook) is None


def test_spec_reviewer_stop_demands_the_quality_review_until_it_launches(run_hook):
    subagent_stopped(run_hook, "dev-discipline:spec-reviewer", "/tmp/reviews/spec-x.md")
    assert "code-quality-reviewer" in context_of(orchestrator_stops(run_hook))
    agent_launched(run_hook, "dev-discipline:code-quality-reviewer")
    assert orchestrator_stops(run_hook) is None


def test_quality_reviewer_stop_demands_the_merge_decision_once(run_hook):
    subagent_stopped(run_hook, "dev-discipline:code-quality-reviewer", "/tmp/reviews/quality-x.md")
    assert "merge" in context_of(orchestrator_stops(run_hook)).lower()
    assert orchestrator_stops(run_hook) is None


def test_a_pending_stage_continues_the_turn_three_times_then_clears(run_hook):
    subagent_stopped(run_hook, "dev-discipline:implementer")
    assert all(orchestrator_stops(run_hook) is not None for _ in range(3))
    assert orchestrator_stops(run_hook) is None


def test_a_foreground_completion_injects_the_mandate_at_once(run_hook):
    output = agent_completed(run_hook, "dev-discipline:implementer")
    assert output["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    assert "spec-reviewer" in context_of(output)
    assert orchestrator_stops(run_hook) is not None


def test_a_bare_agent_type_counts(run_hook):
    subagent_stopped(run_hook, "implementer")
    assert "spec-reviewer" in context_of(orchestrator_stops(run_hook))


def test_other_agents_are_ignored(run_hook):
    assert subagent_stopped(run_hook, "general-purpose") is None
    assert agent_launched(run_hook, "Explore") is None
    assert orchestrator_stops(run_hook) is None


def test_launching_a_stage_nothing_awaits_changes_nothing(run_hook):
    assert agent_launched(run_hook, "dev-discipline:spec-reviewer") is None
    assert orchestrator_stops(run_hook) is None


def test_sessions_do_not_share_pending_stages(run_hook):
    subagent_stopped(run_hook, "dev-discipline:implementer")
    other = run_hook("Stop", stop_hook_active=False, session_id="another-session")
    assert other is None


def test_malformed_input_is_silent(tmp_path):
    completed = subprocess.run([sys.executable, str(SCRIPT)], input="not json", capture_output=True, text=True, env={"CLAUDE_PLUGIN_DATA": str(tmp_path), "PATH": "/usr/bin:/bin"})
    assert completed.returncode == 0
    assert completed.stdout == ""


def test_without_a_data_directory_nothing_is_claimed(tmp_path):
    payload = json.dumps({"session_id": SESSION, "hook_event_name": "SubagentStop", "agent_type": "dev-discipline:implementer", "agent_id": "a", "last_assistant_message": "m"})
    completed = subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    assert completed.returncode == 0
    assert completed.stdout == ""
