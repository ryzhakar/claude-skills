import re

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, write_file, write_record
from instruction_eval.scores import revision_detect
from series_fixtures import Reply, write_agent_series, write_origins

DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-doubled", "text": "No doubled vowels.", "boundary": "Names are exempt.", "counted_by": "pattern", "pattern": "aa"},
        {"id": "d-long", "text": "Keep sentences short.", "boundary": "Quotes are exempt.", "counted_by": "long-sentences", "limit": 3},
    ]
}
TASKS = {
    "tasks": [
        {"id": "t1", "tempts": "d-doubled", "split": "open", "message": "Explain tides.", "answer_key": "answer-[0-9]+"},
        {"id": "t2", "tempts": "d-long", "split": "sealed", "message": "Explain rain.", "answer_key": None},
    ],
    "conversations": [{"id": "c1", "split": "open", "turns": ["Plan a trip.", "Which week?"]}],
}
ANCHORS = {
    "anchors": [
        {"id": "a-one", "task": "t2", "message": "Explain rain.", "text": "Water falls.", "breaches": {"d-judge": 0}, "done": True}
    ]
}
AGENT_COST = {"input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 1, "spent_input_tokens": 1}
FENCED_REPLY = "aaaa aaa. This sentence has many words. Short one.\n\n```\naa aa aa answer-42 This fenced sentence has many words.\n```\nDone now.\n"


def reply_record(reply: Reply) -> dict:
    """Return the reply record an agent reader's collection writes for the reply."""
    record = {
        "condition": reply.condition,
        "task": reply.task,
        "split": reply.split,
        "repeat": reply.repeat,
        "message": "Explain.",
        "text": reply.text,
        "model": "claude-sonnet-4-5",
        "reader_kind": "agent",
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.0,
        "transcript": "/tmp/transcripts/reader.jsonl",
        "transcript_hash": "a" * 64,
        "cost": AGENT_COST,
    }
    return record if reply.turn is None else {**record, "turn": reply.turn}


def write_series(files: SeriesFolder) -> None:
    """Write the series records every revision of the fixture shares."""
    write_agent_series(files, DEMANDS, TASKS, ANCHORS)


def write_revision(files: SeriesFolder, revision: str, replies: list[Reply]) -> None:
    """Write the revision's condition texts, its own reply records, and its origins, each packet carrying one anchor."""
    for condition in {reply.condition for reply in replies if reply.borrowed_from is None}:
        write_file(files, f"{revision}/4-conditions/{condition}.md", condition.encode())
    for reply in replies:
        if reply.borrowed_from is None:
            write_record(files, reply.path_in(revision), reply_record(reply), [])
    write_origins(files, revision, replies, "a-one")


def detected_series(tmp_path, replies: list[Reply]) -> SeriesFolder:
    """Write a series whose r1 holds the replies."""
    files = SeriesFolder(tmp_path)
    write_series(files)
    write_revision(files, "r1", replies)
    return files


def reads_of(revision: str, replies: list[Reply]) -> set[str]:
    """Return the Commands-table reads of `revision detect` expanded for the revision's replies."""
    return {
        "2-demands.yaml#demands",
        "3-tasks.yaml#tasks",
        "3-tasks.yaml#conversations",
        *(reply.path_in(revision) for reply in replies),
        f"{revision}/6-origins.yaml",
    }


def test_detectors_count_patterns_and_long_sentences_outside_fenced_code_and_match_the_answer_key_inside_it(tmp_path):
    replies = [Reply("b00000001", "instruction", "t1", FENCED_REPLY)]
    files = detected_series(tmp_path, replies)

    revision_detect(files, "r1")

    detectors = SeriesRecords(files).detectors("r1")
    assert detectors["verdicts"] == [{"id": "b00000001", "breaches": {"d-doubled": 3, "d-long": 1}, "done_by_answer_key": True}]
    assert set(detectors["inputs"]) == reads_of("r1", replies)


def test_a_reply_missing_its_key_is_not_done_by_it_and_a_keyless_task_or_conversation_turn_holds_no_key_verdict(tmp_path):
    replies = [
        Reply("b00000001", "instruction", "t1", "No number here."),
        Reply("b00000002", "instruction", "t2", "answer-42", split="sealed"),
        Reply("b00000003", "instruction", "c1", "answer-42", turn=1),
    ]
    files = detected_series(tmp_path, replies)

    revision_detect(files, "r1")

    verdicts = SeriesRecords(files).detectors("r1")["verdicts"]
    assert [(entry["id"], entry["done_by_answer_key"]) for entry in verdicts] == [("b00000001", False), ("b00000002", None), ("b00000003", None)]


def test_an_unclosed_fence_hides_the_rest_of_the_reply_from_the_detectors(tmp_path):
    text = "aa.\n~~~~\naa aa\n~~~\nThis line stays inside the fence too.\n"
    files = detected_series(tmp_path, [Reply("b00000001", "instruction", "t1", text)])

    revision_detect(files, "r1")

    assert SeriesRecords(files).detectors("r1")["verdicts"][0]["breaches"] == {"d-doubled": 1, "d-long": 0}


def test_a_later_revision_detects_control_replies_it_borrows_from_r1(tmp_path):
    files = SeriesFolder(tmp_path)
    write_series(files)
    write_revision(files, "r1", [Reply("b00000001", "empty", "t1", "aa aa")])
    later = [Reply("b00000011", "instruction", "t1", "aa"), Reply("b00000012", "empty", "t1", "aa aa", borrowed_from="r1")]
    write_revision(files, "r2", later)

    revision_detect(files, "r2")

    detectors = SeriesRecords(files).detectors("r2")
    assert [entry["breaches"]["d-doubled"] for entry in detectors["verdicts"]] == [1, 2]
    assert set(detectors["inputs"]) == reads_of("r2", later)
    assert "r1/5-replies/empty/t1/repeat-1.yaml" in detectors["inputs"]


def test_a_revision_already_detected_refuses_a_second_detection(tmp_path):
    files = detected_series(tmp_path, [Reply("b00000001", "instruction", "t1", "aa")])
    revision_detect(files, "r1")

    with pytest.raises(Refusal, match=r"^already written: r1/7-detectors\.yaml$"):
        revision_detect(files, "r1")


PROSE = st.lists(st.sampled_from(["aa", "a", "b.", "aaa", "word", "\n"]), max_size=12).map(" ".join)
FENCED_LINES = st.lists(st.text(alphabet="ab .", max_size=12), max_size=4)


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(before=PROSE, fenced=FENCED_LINES, after=PROSE, fence=st.sampled_from(["```", "~~~", "````"]))
def test_whatever_a_closed_fence_holds_leaves_the_pattern_count_of_the_prose_around_it(tmp_path_factory, before, fenced, after, fence):
    text = "\n".join([before, fence, *fenced, fence, after])
    files = detected_series(tmp_path_factory.mktemp("series"), [Reply("b00000001", "instruction", "t1", text)])

    revision_detect(files, "r1")

    expected = len(re.findall("aa", before)) + len(re.findall("aa", after))
    assert SeriesRecords(files).detectors("r1")["verdicts"][0]["breaches"]["d-doubled"] == expected
