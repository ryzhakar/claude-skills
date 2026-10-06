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


def agent_launched(run_hook, subagent_type, agent_id="a1"):
    return run_hook("PostToolUse", tool_name="Agent", tool_input={"subagent_type": subagent_type, "prompt": "x"}, tool_response={"status": "async_launched", "agentId": agent_id})


def agent_messaged(run_hook, agent_id):
    return run_hook("PostToolUse", tool_name="SendMessage", tool_input={"to": agent_id, "message": "re-review"}, tool_response={"success": True})


def agent_completed(run_hook, subagent_type, message="Status: DONE"):
    return run_hook("PostToolUse", tool_name="Agent", tool_input={"subagent_type": subagent_type, "prompt": "x"}, tool_response={"status": "completed", "agentId": "a1", "content": [{"type": "text", "text": message}]})


def orchestrator_stops(run_hook):
    return run_hook("Stop", stop_hook_active=False, last_assistant_message="done")


def test_implementer_stop_makes_the_orchestrator_launch_the_spec_review(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer", "Status: DONE\nWorktree: /tmp/wt-auth")
    output = orchestrator_stops(run_hook)
    assert output["hookSpecificOutput"]["hookEventName"] == "Stop"
    assert "spec-reviewer" in context_of(output)
    assert "/tmp/wt-auth" in context_of(output)


def test_launching_the_spec_review_clears_the_mandate(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer")
    agent_launched(run_hook, "dev-cycle:spec-reviewer")
    assert orchestrator_stops(run_hook) is None


def test_spec_reviewer_stop_demands_the_quality_review_until_it_launches(run_hook):
    subagent_stopped(run_hook, "dev-cycle:spec-reviewer", "/tmp/reviews/spec-x.md")
    assert "code-quality-reviewer" in context_of(orchestrator_stops(run_hook))
    agent_launched(run_hook, "dev-cycle:code-quality-reviewer")
    assert orchestrator_stops(run_hook) is None


def test_quality_reviewer_stop_demands_the_merge_decision_once(run_hook):
    subagent_stopped(run_hook, "dev-cycle:code-quality-reviewer", "/tmp/reviews/quality-x.md")
    assert "merge" in context_of(orchestrator_stops(run_hook)).lower()
    assert orchestrator_stops(run_hook) is None


def test_a_pending_stage_continues_the_turn_three_times_then_clears(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer")
    assert all(orchestrator_stops(run_hook) is not None for _ in range(3))
    assert orchestrator_stops(run_hook) is None


def test_a_foreground_completion_injects_the_mandate_at_once(run_hook):
    output = agent_completed(run_hook, "dev-cycle:implementer")
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
    assert agent_launched(run_hook, "dev-cycle:spec-reviewer") is None
    assert orchestrator_stops(run_hook) is None


def test_sessions_do_not_share_pending_stages(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer")
    other = run_hook("Stop", stop_hook_active=False, session_id="another-session")
    assert other is None


def test_malformed_input_is_silent(tmp_path):
    completed = subprocess.run([sys.executable, str(SCRIPT)], input="not json", capture_output=True, text=True, env={"CLAUDE_PLUGIN_DATA": str(tmp_path), "PATH": "/usr/bin:/bin"})
    assert completed.returncode == 0
    assert completed.stdout == ""


def test_without_a_data_directory_nothing_is_claimed(tmp_path):
    payload = json.dumps({"session_id": SESSION, "hook_event_name": "SubagentStop", "agent_type": "dev-cycle:implementer", "agent_id": "a", "last_assistant_message": "m"})
    completed = subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    assert completed.returncode == 0
    assert completed.stdout == ""


def test_an_implementer_stop_without_done_opens_no_review(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer", "Status: NEEDS_CONTEXT\nWorktree: /tmp/wt")
    assert orchestrator_stops(run_hook) is None
    subagent_stopped(run_hook, "dev-cycle:implementer", "Status: DONE_WITH_CONCERNS\nWorktree: /tmp/wt")
    assert orchestrator_stops(run_hook) is None


def test_a_foreground_completion_without_done_injects_nothing(run_hook):
    assert agent_completed(run_hook, "dev-cycle:implementer", "Status: BLOCKED") is None
    assert orchestrator_stops(run_hook) is None


def test_foreground_reviewer_completions_inject_the_next_mandate(run_hook):
    assert "code-quality-reviewer" in context_of(agent_completed(run_hook, "dev-cycle:spec-reviewer", "/tmp/reviews/spec-x.md"))
    agent_launched(run_hook, "dev-cycle:code-quality-reviewer")
    assert "merge" in context_of(agent_completed(run_hook, "dev-cycle:code-quality-reviewer", "/tmp/reviews/quality-x.md")).lower()


def test_an_implementer_launch_retires_the_merge_decision(run_hook):
    subagent_stopped(run_hook, "dev-cycle:code-quality-reviewer", "/tmp/reviews/quality-x.md")
    agent_launched(run_hook, "dev-cycle:implementer")
    assert orchestrator_stops(run_hook) is None


def test_a_second_stop_of_the_same_agent_adds_no_stage(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer")
    subagent_stopped(run_hook, "dev-cycle:implementer")
    assert all(orchestrator_stops(run_hook) is not None for _ in range(3))
    assert orchestrator_stops(run_hook) is None


def test_continuing_a_known_reviewer_by_message_clears_the_mandate(run_hook):
    agent_launched(run_hook, "dev-cycle:spec-reviewer", "spec-1")
    subagent_stopped(run_hook, "dev-cycle:implementer", "Status: DONE\nWorktree: /tmp/wt")
    agent_messaged(run_hook, "spec-1")
    assert orchestrator_stops(run_hook) is None


def test_a_stopped_agent_is_known_for_later_messages(run_hook):
    run_hook("SubagentStop", agent_type="dev-cycle:code-quality-reviewer", agent_id="cq-1", last_assistant_message="/tmp/reviews/quality-x.md", stop_hook_active=False)
    orchestrator_stops(run_hook)
    subagent_stopped(run_hook, "dev-cycle:spec-reviewer", "/tmp/reviews/spec-y.md")
    agent_messaged(run_hook, "cq-1")
    assert orchestrator_stops(run_hook) is None


def test_messaging_an_unknown_agent_changes_nothing(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer")
    agent_messaged(run_hook, "someone-else")
    assert orchestrator_stops(run_hook) is not None


def test_a_malformed_reviewer_stop_opens_no_stage(run_hook):
    subagent_stopped(run_hook, "dev-cycle:implementer", "Status: DONE\nWorktree: /tmp/wt")
    agent_launched(run_hook, "dev-cycle:spec-reviewer", "r1")
    subagent_stopped(run_hook, "dev-cycle:spec-reviewer", "Dispatch malformed: base SHA, verdict path")
    assert orchestrator_stops(run_hook) is None
