import json
from pathlib import Path

import pytest

from instruction_eval.judge import AcceptedJudging, NeedsJudging, PendingJudging, judging_states
from instruction_eval.reader import Transcript
from instruction_eval.records import Refusal, SeriesFolder, write_file, write_record
from series_fixtures import write_agent_series, write_yaml

JUDGE_MODEL = "claude-opus-4-1"
OTHER_MODEL = "claude-sonnet-5-5"
PACKETS = ("t1", "t1--omissions")
REPLY_IDS = {"t1": "b0000001a", "t1--omissions": "b0000002a"}
ANCHOR_IDS = {"t1": "b0000001b", "t1--omissions": "b0000002b"}
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
TASKS = {
    "tasks": [
        {"id": "t1", "tempts": "d-judge", "split": "open", "message": "Explain tides.", "answer_key": None},
        {"id": "t3", "tempts": "d-judge", "split": "sealed", "message": "Explain snow.", "answer_key": None},
    ],
    "conversations": [],
}
ANCHORS = {"anchors": [{"id": "a-one", "task": "t3", "message": "Explain snow.", "text": "Cold rain.", "breaches": {"d-judge": 1}, "done": True}]}
ACCEPTANCE = {"breach_difference": 0.5, "self_difference": 0.5, "done_agreement": 0.8}
CALIBRATION = {
    "attempt": 1,
    "judge_model": JUDGE_MODEL,
    "raters": ["agent", "agent"],
    "rater_model": OTHER_MODEL,
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
    "brief_hash": "c" * 64,
    "agreement": {"demands": {"d-judge": {"breach_difference": 0.1, "self_difference": 0.1}}, "done_agreement": 1.0, "scale": None, "ratings": {}},
}
PLAN = {
    "judge_model": JUDGE_MODEL,
    "raters": ["agent", "agent"],
    "rater_model": OTHER_MODEL,
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
}
HASH = "a" * 64


def series_folder(tmp_path: Path) -> SeriesFolder:
    """Write a series whose r1 blinded the packets `t1` and `t1--omissions`, each holding one reply and the anchor."""
    files = SeriesFolder(tmp_path / "series")
    write_agent_series(files, DEMANDS, TASKS, ANCHORS)
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", PLAN)
    write_record(files, "6-judge/calibration.yaml", CALIBRATION, [])
    write_file(files, "r1/5-replies/instruction/t1/repeat-1.yaml", b"reply")
    write_file(files, "r1/5-replies/omit-1/t1/repeat-1.yaml", b"reply")
    origin = {"split": "open", "repeat": 1, "task": "t1", "borrowed_from": None}
    ids = {
        REPLY_IDS["t1"]: {**origin, "packet": "t1", "condition": "instruction"},
        REPLY_IDS["t1--omissions"]: {**origin, "packet": "t1--omissions", "condition": "omit-1"},
        **{anchor_id: {"packet": packet, "anchor": "a-one"} for packet, anchor_id in ANCHOR_IDS.items()},
    }
    write_record(files, "r1/6-origins.yaml", {"ids": ids, "packets": dict.fromkeys(PACKETS, HASH)}, [])
    return files


def write_definition(files: SeriesFolder, packet: str, judging: int) -> None:
    write_file(files, f".claude/agents/ie-judge-r1-{packet}-k{judging}.md", b"definition")


def states(files: SeriesFolder, transcripts: list[Transcript] = ()) -> dict:
    return judging_states(files, "r1", list(transcripts), Path.read_bytes)


def test_a_packet_with_no_judging_needs_judging_one(tmp_path):
    files = series_folder(tmp_path)

    assert states(files) == {"t1": NeedsJudging(1), "t1--omissions": NeedsJudging(1)}
