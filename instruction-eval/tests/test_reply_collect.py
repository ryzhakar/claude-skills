import hashlib
import re
from datetime import timedelta

import pytest
from reader_fixtures import (
    COMMAND_READER,
    CONVERSATION_TASKS,
    MODEL,
    OPEN_MESSAGE,
    START,
    USAGE,
    collect,
    conversation_transcripts,
    expected_reads,
    load,
    prepared_series,
    reader_transcript,
    stamp,
    task_transcripts,
    write_command_replies,
)
from series_fixtures import tree

from instruction_eval.reader import Transcript
from instruction_eval.records import Refusal


def test_the_earliest_transcripts_of_each_condition_and_task_become_its_repeats_each_reply_recording_its_transcript(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)

    surplus = collect(files, list(reversed(transcripts)))

    assert surplus == ""
    first = next(transcript for transcript in transcripts if transcript.agent_id == "instruction-t-open-1")
    record = load(files, "r1/5-replies/instruction/t-open/repeat-1.yaml")
    inputs = record.pop("inputs")
    assert set(inputs) == expected_reads()
    assert record == {
        "condition": "instruction",
        "task": "t-open",
        "split": "open",
        "repeat": 1,
        "message": OPEN_MESSAGE,
        "text": "answer instruction t-open 1",
        "model": MODEL,
        "reader_kind": "agent",
        "started": stamp(START + timedelta(minutes=1)),
        "seconds": 1.0,
        "transcript": str(first.path),
        "transcript_hash": hashlib.sha256(first.path.read_bytes()).hexdigest(),
        "cost": {**USAGE, "spent_input_tokens": 8},
    }
    assert load(files, "r1/5-replies/placebo/t-sealed/repeat-2.yaml")["text"] == "answer placebo t-sealed 2"


def test_transcripts_beyond_the_repeats_are_listed_and_ignored(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    late = reader_transcript(tmp_path, "late", "instruction", [OPEN_MESSAGE], ["a late answer"], START + timedelta(minutes=3))

    surplus = collect(files, [*transcripts, late])

    assert surplus == f"ignored surplus transcript: {late.path}\n"
    assert not files.holds("r1/5-replies/instruction/t-open/repeat-3.yaml")
    assert load(files, "r1/5-replies/instruction/t-open/repeat-2.yaml")["text"] == "answer instruction t-open 2"


def test_a_gap_refuses_after_writing_the_replies_it_could_match_and_a_rerun_fills_only_the_gap(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    withheld = [transcript for transcript in transcripts if transcript.agent_id in ("aim-t-open-2", "aim-t-sealed-1", "aim-t-sealed-2")]
    present = [transcript for transcript in transcripts if transcript not in withheld]
    late = reader_transcript(tmp_path, "late", "instruction", [OPEN_MESSAGE], ["a late answer"], START + timedelta(minutes=3))

    with pytest.raises(Refusal) as refused:
        collect(files, [*present, late])

    assert str(refused.value) == f"missing replies: 3, first r1/5-replies/aim/t-open/repeat-2.yaml\nignored surplus transcript: {late.path}"

    assert load(files, "r1/5-replies/aim/t-open/repeat-1.yaml")["text"] == "answer aim t-open 1"
    written = files.read_bytes("r1/5-replies/aim/t-open/repeat-1.yaml")
    assert collect(files, transcripts) == ""
    assert files.read_bytes("r1/5-replies/aim/t-open/repeat-1.yaml") == written
    assert load(files, "r1/5-replies/aim/t-sealed/repeat-2.yaml")["text"] == "answer aim t-sealed 2"


def test_each_turn_of_a_conversation_transcript_becomes_a_reply_of_its_repeat(tmp_path):
    files = prepared_series(tmp_path, CONVERSATION_TASKS)

    collect(files, [*task_transcripts(tmp_path), *conversation_transcripts(tmp_path)])

    second = load(files, "r1/5-replies/placebo/c-open/repeat-2/turn-2.yaml")
    second.pop("inputs")
    assert second["text"] == "second placebo 2"
    assert second["turn"] == 2
    assert second["message"] == "Which week?"
    assert second["split"] == "open"
    assert second["started"] == stamp(START + timedelta(minutes=2, seconds=10))
    assert load(files, "r1/5-replies/instruction/c-open/repeat-1/turn-1.yaml")["message"] == "Plan a trip."


def test_a_transcript_served_by_another_model_refuses_before_any_reply_is_written(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    served_elsewhere = reader_transcript(tmp_path, "other", "aim", [OPEN_MESSAGE], ["x"], START + timedelta(minutes=9), model="claude-other-1")
    transcripts = [served_elsewhere if transcript.agent_id == "aim-t-open-1" else transcript for transcript in transcripts]

    with pytest.raises(Refusal, match=r"claude-other-1 is not the pinned claude-sonnet-5-5"):
        collect(files, transcripts)

    assert not (files.root / "r1/5-replies").exists()


def test_a_transcript_of_another_agent_type_or_opening_with_another_message_is_no_reply(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    judge = Transcript(path=tmp_path / "transcripts/judge.jsonl", session="s", agent_id="judge", agent_type="ie-judge-r1-t-open-k1")
    stray = reader_transcript(tmp_path, "stray", "aim", ["Explain snow."], ["x"], START)

    assert collect(files, [judge, stray, *transcripts]) == ""


def test_a_command_reader_collects_nothing_and_refuses_a_gap_whatever_transcripts_exist(tmp_path):
    files = prepared_series(tmp_path, reader=COMMAND_READER)
    write_command_replies(files, conditions=("empty", "instruction", "placebo"))
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^missing replies: 4, first r1/5-replies/aim/t-open/repeat-1\.yaml$"):
        collect(files, task_transcripts(tmp_path))

    assert tree(files.root) == before


def test_a_command_reader_with_every_reply_written_collects_cleanly_without_writing(tmp_path):
    files = prepared_series(tmp_path, reader=COMMAND_READER)
    write_command_replies(files)
    before = tree(files.root)

    assert collect(files, []) == ""
    assert tree(files.root) == before


@pytest.mark.parametrize("edited", ["r1/4-conditions/aim.md", ".claude/agents/ie-reader-r1-aim.md"])
def test_an_edited_condition_text_or_reader_definition_refuses_before_any_reply_is_written(tmp_path, edited):
    files = prepared_series(tmp_path)
    (files.root / edited).write_bytes(b"edited")

    with pytest.raises(Refusal, match=rf"^{edited.replace('.', r'[.]')} differs from its recomputation$"):
        collect(files, task_transcripts(tmp_path))

    assert not (files.root / "r1/5-replies").exists()


@pytest.mark.parametrize("bad_line", [b"not json", b"[1, 2]", b'{"type": "user"}'], ids=["not-json", "not-object", "malformed-entry"])
def test_a_transcript_line_that_cannot_be_read_refuses_in_one_line_before_any_reply_is_written(tmp_path, bad_line):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    transcripts[0].path.write_bytes(transcripts[0].path.read_bytes() + bad_line + b"\n")

    with pytest.raises(Refusal, match=rf"^{re.escape(str(transcripts[0].path))}: line 3 "):
        collect(files, transcripts)

    assert not (files.root / "r1/5-replies").exists()
