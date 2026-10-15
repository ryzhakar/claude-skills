from pathlib import Path

import pytest

from instruction_eval.reader import refuse_exposed_reader_transcript
from instruction_eval.records import Refusal

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "transcript-screen"
PINNED_MODEL = "claude-sonnet-5-5"
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
