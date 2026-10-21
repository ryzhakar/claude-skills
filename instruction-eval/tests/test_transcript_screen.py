import json
import re
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

from instruction_eval.reader import judge_transcript_rejection, refuse_exposed_reader_transcript
from instruction_eval.records import DEFAULT_BINDING, Refusal
from series_fixtures import OTHER_BINDING

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "transcript-screen"
PINNED_MODEL = "claude-sonnet-5-5"
VERDICT_PATH = Path("/series/r1/7-verdicts/t1/k1.yaml")
TASK = "Summarize the release notes in two lines."
TURN_TWO = "Now list the risks."


def screen_reader(fixture_name, turns=(TASK,)):
    transcript = FIXTURES / f"{fixture_name}.jsonl"
    refuse_exposed_reader_transcript(transcript, transcript.read_bytes(), turns, PINNED_MODEL)


def test_reader_transcript_showing_a_claude_md_is_refused():
    with pytest.raises(Refusal, match="reader-claude-md.jsonl: shows memory file /Users/u/CLAUDE.md$"):
        screen_reader("reader-claude-md")


def test_reader_transcript_showing_an_ancestor_claude_md_is_refused():
    with pytest.raises(Refusal, match="shows memory file /Users/u/project/CLAUDE.md$"):
        screen_reader("reader-nested-claude-md")


@pytest.mark.parametrize("fixture_name", ["reader-subagent-start-hook", "reader-subagent-start-context"])
def test_reader_transcript_showing_subagent_start_text_is_refused(fixture_name):
    with pytest.raises(Refusal, match="shows SubagentStart text$"):
        screen_reader(fixture_name)


def test_reader_transcript_showing_any_tool_use_is_refused():
    with pytest.raises(Refusal, match="shows tool use Read$"):
        screen_reader("reader-tool-use")


def test_reader_transcript_handing_its_reply_back_through_subagent_handback_passes():
    screen_reader("reader-subagent-handback", ("Explain tides.",))


def test_reader_transcript_served_by_another_model_is_refused():
    with pytest.raises(Refusal, match="model claude-opus-5-5 is not the pinned claude-sonnet-5-5$"):
        screen_reader("reader-other-model")


def test_reader_transcript_whose_task_message_is_not_byte_equal_is_refused():
    with pytest.raises(Refusal, match="turn 1 message differs from the task's$"):
        screen_reader("reader-other-message")


@pytest.mark.parametrize("fixture_name", ["reader-clean", "reader-empty-subagent-start-hook"])
def test_reader_transcript_with_session_context_and_silent_hooks_passes(fixture_name):
    screen_reader(fixture_name)


def test_conversation_turn_passes_inside_the_send_message_wrapper():
    screen_reader("reader-conversation", (TASK, TURN_TWO))


def test_conversation_turn_without_the_send_message_wrapper_is_refused():
    with pytest.raises(Refusal, match="turn 2 message differs from the task's$"):
        screen_reader("reader-conversation-unwrapped-turn", (TASK, TURN_TWO))


def test_turn_beyond_the_task_turns_is_refused():
    with pytest.raises(Refusal, match="turn 2 message differs from the task's$"):
        screen_reader("reader-conversation")


MALFORMED_CASES = [
    ("malformed-attachment-entry", "line 2 lacks attachment"),
    ("malformed-instructions-attachment", "line 2 lacks files"),
    ("malformed-assistant-entry", "line 3 lacks message.content"),
]


@pytest.mark.parametrize(("fixture_name", "fault"), MALFORMED_CASES)
def test_reader_screen_of_a_malformed_entry_is_refused_by_transcript_and_line(fixture_name, fault):
    with pytest.raises(ValueError, match=f"{fixture_name}.jsonl: {re.escape(fault)}$"):
        screen_reader(fixture_name)


@pytest.mark.parametrize(("fixture_name", "fault"), MALFORMED_CASES)
def test_judge_screen_of_a_malformed_entry_is_refused_by_transcript_and_line(fixture_name, fault):
    with pytest.raises(ValueError, match=f"{fixture_name}.jsonl: {re.escape(fault)}$"):
        judge_rejection(fixture_name)


def judge_rejection(fixture_name, binding_skill=OTHER_BINDING["skill"]):
    transcript = FIXTURES / f"{fixture_name}.jsonl"
    return judge_transcript_rejection(transcript, transcript.read_bytes(), VERDICT_PATH, binding_skill)


def skill_load(skill: str) -> dict:
    return {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": skill}}


VERDICT_WRITE = {"type": "tool_use", "id": "toolu_2", "name": "Write", "input": {"file_path": str(VERDICT_PATH)}}


def tool_use_rejection(tool_uses: list[dict], binding_skill: str) -> str | None:
    """Screen a judge transcript of one assistant entry per tool use, in order, against the binding skill."""
    lines = [{"type": "user", "message": {"role": "user", "content": "Judge the packet."}}]
    lines += [{"type": "assistant", "message": {"role": "assistant", "content": [tool_use]}} for tool_use in tool_uses]
    content = "".join(json.dumps(line) + "\n" for line in lines).encode()
    return judge_transcript_rejection(Path("judge.jsonl"), content, VERDICT_PATH, binding_skill)


def test_judge_transcript_loading_a_skill_besides_the_series_binding_skill_is_rejected():
    assert judge_rejection("judge-clean", DEFAULT_BINDING.skill) == "shows tool use Skill"


@pytest.mark.parametrize(
    "tool_uses",
    [[VERDICT_WRITE], [VERDICT_WRITE, skill_load(OTHER_BINDING["skill"])], []],
    ids=["never-loads", "loads-after-writing", "no-act"],
)
def test_judge_transcript_whose_first_act_is_not_loading_the_binding_skill_is_rejected(tool_uses):
    assert tool_use_rejection(tool_uses, OTHER_BINDING["skill"]) == "does not load oath:bind first"


@given(st.lists(st.sampled_from([skill_load(OTHER_BINDING["skill"]), VERDICT_WRITE])))
def test_judge_transcript_of_allowed_tool_uses_is_rejected_exactly_when_its_first_is_not_the_binding_skill_load(tool_uses):
    loads_first = bool(tool_uses) and tool_uses[0] != VERDICT_WRITE
    assert tool_use_rejection(tool_uses, OTHER_BINDING["skill"]) == (None if loads_first else "does not load oath:bind first")


def test_judge_transcript_showing_a_read_is_rejected():
    assert judge_rejection("judge-read") == "shows tool use Read"


def test_judge_transcript_loading_only_the_series_binding_skill_and_writing_its_verdict_is_kept():
    assert judge_rejection("judge-clean") is None


@pytest.mark.parametrize(
    ("fixture_name", "rejection"),
    [
        ("judge-other-skill", "shows tool use Skill"),
        ("judge-write-elsewhere", "shows tool use Write"),
        ("judge-claude-md", "shows memory file /Users/u/CLAUDE.md"),
        ("judge-subagent-start", "shows SubagentStart text"),
    ],
)
def test_judge_transcript_exposed_beyond_its_binding_skill_and_verdict_is_rejected(fixture_name, rejection):
    assert judge_rejection(fixture_name) == rejection
