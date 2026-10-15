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


def verdict_path(files: SeriesFolder, packet: str, judging: int) -> Path:
    return files.root / f"r1/7-verdicts/{packet}/k{judging}.yaml"


def judge_transcript(
    files: SeriesFolder,
    packet: str,
    judging: int,
    model: str = JUDGE_MODEL,
    final: bool = True,
    started: str = "2026-10-14T19:00:43.000Z",
    tools: tuple[dict, ...] = (),
) -> Transcript:
    """Write the transcript of a judging that loaded the oath skill and wrote its verdict path, and return its location."""
    agent_type = f"ie-judge-r1-{packet}-k{judging}"
    uses = tools or (
        {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": "manifesto:manifesto-oath"}},
        {"type": "tool_use", "id": "toolu_2", "name": "Write", "input": {"file_path": str(verdict_path(files, packet, judging))}},
    )
    blocks = [*uses, *([{"type": "text", "text": "Done."}] if final else [])]
    usage = {"input_tokens": 3, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 2}
    lines = [
        {"type": "user", "message": {"role": "user", "content": "Judge the packet."}, "timestamp": started},
        {"type": "assistant", "message": {"model": model, "id": "msg_A", "role": "assistant", "content": blocks, "usage": usage}, "timestamp": started},
    ]
    path = files.root.parent / f"transcripts/{agent_type}-{started}/subagents/agent-{agent_type}.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines))
    return Transcript(path=path, session=path.parent.parent.name, agent_id=agent_type, agent_type=agent_type)


def test_a_packet_with_no_judging_needs_judging_one(tmp_path):
    files = series_folder(tmp_path)

    assert states(files) == {"t1": NeedsJudging(1), "t1--omissions": NeedsJudging(1)}


def test_a_judging_without_verdict_or_transcript_is_pending_and_blocks_a_new_one_for_its_packet_alone(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    assert states(files) == {"t1": PendingJudging(1), "t1--omissions": NeedsJudging(1)}


def test_a_returned_judging_without_a_verdict_file_failed_and_the_next_judging_follows_it(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    assert states(files, [judge_transcript(files, "t1", 1)]) == {"t1": NeedsJudging(2), "t1--omissions": NeedsJudging(1)}
