from collections.abc import Sequence
from pathlib import Path

import numpy
import pytest

from instruction_eval.gate import revision_gate
from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, write_file, write_record
from instruction_eval.scores import BOOTSTRAP_SEED
from series_fixtures import Reply, sha256, write_origins, write_yaml

FIRST_INSTRUCTION = b"Be terse. Avoid hedges.\n"
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
COVERAGE = {"demands": {"d-judge": [1], "d-hedge": [2]}, "sentences": {1: ["d-judge"], 2: ["d-hedge"]}}
TASKS = {
    "tasks": [
        {"id": "t1", "tempts": "d-judge", "split": "open", "message": "Explain the tides.", "answer_key": None},
        {"id": "t2", "tempts": "d-judge", "split": "sealed", "message": "Explain the snow.", "answer_key": None},
        {"id": "t3", "tempts": "d-hedge", "split": "sealed", "message": "Explain the rain.", "answer_key": None},
    ],
    "conversations": [],
}
CONDITIONS = {"controls": ["empty", "aim", "placebo"], "aim": "Answer in few words.", "placebo_source": "/tmp/placebo.md", "omissions": "none"}
CONTROLS = ("empty", "aim", "placebo")
ANCHORS = {"anchors": [{"id": "a-one", "task": "t1", "message": "Explain the tides.", "text": "The moon.", "breaches": {"d-judge": 0}, "done": True}]}
CHECKS = [{"compares": compares, "gap": 1.0} for compares in ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")]
GATE = {"repeats": 2, "level": 0.95, "done_by": "judge", "checks": CHECKS, "keep_rule": "best-estimate-shortest", "budget": "none"}
GATE_KEYS = ("repeats", "level", "done_by", "checks", "keep_rule", "budget")
SIGMA = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
NOISE = {"repeats": 2, "level": 0.95, "z": 1.96, "sigma": SIGMA, "checks": {}, "demands": {"d-judge": 0.1, "d-hedge": 0.1}, "done_change": 0.1}
COLLECTED_PACKET = {
    "accepted": 1,
    "judge_model": "claude-opus-4-1",
    "transcript": "/tmp/transcripts/judge.jsonl",
    "transcript_hash": "a" * 64,
    "anchors": {"breach_difference": {"d-judge": 0.0}, "done_agreement": 1.0},
}
REPLY_COST = {"input_tokens": 4, "cache_creation_input_tokens": 3, "cache_read_input_tokens": 3, "output_tokens": 5, "spent_input_tokens": 10}
HYPOTHESIS = {
    "failing_demand": "d-judge",
    "replies_read": ["b00000001"],
    "change": {"action": "rewrite", "sentence": 1},
    "predicted_movement": {"direction": "down", "size": 0.5},
}
HYPOTHESIS_KEYS = ("failing_demand", "replies_read", "change", "predicted_movement")


def sealed_replies(condition: str, judged: int, start: int, borrowed_from: str | None = None) -> list[Reply]:
    """Build both repeats of both sealed tasks under the condition, each breaching `d-judge` as given, blind ids counted from `start`."""
    return [
        Reply(f"b{start + index:08x}", condition, task, repeat=repeat, split="sealed", judged=judged, borrowed_from=borrowed_from)
        for index, (task, repeat) in enumerate((task, repeat) for task in ("t2", "t3") for repeat in (1, 2))
    ]


def first_replies(instruction_judged: int, aim_judged: int) -> list[Reply]:
    """Build r1's replies: one open instruction reply breaching `d-judge`, then the sealed replies of the instruction and every control."""
    return [
        Reply("b00000001", "instruction", "t1", judged=1),
        *sealed_replies("instruction", instruction_judged, 0x10),
        *sealed_replies("empty", 3, 0x20),
        *sealed_replies("aim", aim_judged, 0x30),
        *sealed_replies("placebo", 3, 0x40),
    ]


def reply_record(reply: Reply) -> dict:
    """Return the reply record of a fixture reply."""
    task = next(task for task in TASKS["tasks"] if task["id"] == reply.task)
    return {
        "condition": reply.condition,
        "task": reply.task,
        "split": reply.split,
        "repeat": reply.repeat,
        "message": task["message"],
        "text": "An answer.",
        "model": "claude-sonnet-4-5",
        "reader_kind": "agent",
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.5,
        "transcript": "/tmp/transcripts/reader.jsonl",
        "transcript_hash": "a" * 64,
        "cost": REPLY_COST,
    }


def write_revision_instruction(files: SeriesFolder, revision: str, number: int, instruction: bytes) -> None:
    """Write a revision's instruction snapshot and its record chained to the previous revision's."""
    write_file(files, f"{revision}/2-instruction.md", instruction)
    parent = None if number == 1 else f"r{number - 1}"
    record = {
        "number": number,
        "parent": parent,
        "hash": sha256(instruction),
        "parent_record": None if parent is None else sha256(files.read_bytes(f"{parent}/2-revision.yaml")),
        "change": None if parent is None else {"action": "rewrite", "sentence": 1, "old": "Be terse.", "new": "Be brief."},
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [])


def write_measured_revision(files: SeriesFolder, revision: str, replies: Sequence[Reply]) -> None:
    """Write the revision's own reply records, origins, accepted verdicts, collection, and detector counts, each packet carrying one anchor."""
    for condition in {reply.condition for reply in replies if reply.borrowed_from is None}:
        write_file(files, f"{revision}/4-conditions/{condition}.md", condition.encode())
    for reply in replies:
        if reply.borrowed_from is None:
            write_record(files, reply.path_in(revision), reply_record(reply), [])
    anchor_ids = write_origins(files, revision, replies, "a-one")
    for packet, anchor_id in anchor_ids.items():
        entries = [{"id": reply.id, "breaches": {"d-judge": reply.judged}, "done": reply.done, "kind": "answer", "notes": ""} for reply in replies if reply.packet == packet]
        anchor_entry = {"id": anchor_id, "breaches": {"d-judge": 0}, "done": True, "kind": "answer", "notes": ""}
        write_yaml(files, f"{revision}/7-verdicts/{packet}/k1.yaml", {"verdicts": [*entries, anchor_entry]})
    write_record(files, f"{revision}/7-collected.yaml", {"packets": dict.fromkeys(anchor_ids, COLLECTED_PACKET)}, [])
    detectors = [{"id": reply.id, "breaches": {"d-hedge": reply.hedges}, "done_by_answer_key": reply.key} for reply in replies]
    write_record(files, f"{revision}/7-detectors.yaml", {"verdicts": detectors}, [])


def frozen_series(tmp_path: Path, replies: Sequence[Reply], gate: dict = GATE) -> SeriesFolder:
    """Write a frozen series whose r1 holds the replies, judged and detected."""
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", {"instruction": "/tmp/terse.md", "sources": [], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_record(files, "6-judge/anchors.yaml", ANCHORS, [])
    write_yaml(files, "7-gate.yaml", gate)
    write_revision_instruction(files, "r1", 1, FIRST_INSTRUCTION)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    write_measured_revision(files, "r1", replies)
    write_record(files, "8-frozen.yaml", {"hashes": {}, "noise": NOISE, "tool_version": "0.1.0", "frozen_at": "2026-10-14T10:00:00+00:00"}, [])
    return files


def bootstrap_rng() -> numpy.random.Generator:
    """Return the fresh seeded random source the composition root hands each bootstrap."""
    return numpy.random.default_rng(BOOTSTRAP_SEED)


def measured_reads(revision: str, replies: Sequence[Reply]) -> set[str]:
    """Return a measured revision's reply files, origins, accepted verdicts, collection, and detector counts."""
    return {
        *(reply.path_in(revision) for reply in replies),
        f"{revision}/6-origins.yaml",
        *(f"{revision}/7-verdicts/{packet}/k1.yaml" for packet in {reply.packet for reply in replies}),
        f"{revision}/7-collected.yaml",
        f"{revision}/7-detectors.yaml",
    }


def gate_reads(revision: str, replies: Sequence[Reply], earlier_outcomes: Sequence[str] = ()) -> set[str]:
    """Return the Commands-table reads of `revision gate` expanded for a first revision."""
    return {
        "2-demands.yaml#demands",
        "3-tasks.yaml#tasks",
        "3-tasks.yaml#conversations",
        "r1/3-coverage.yaml#demands",
        "r1/3-coverage.yaml#sentences",
        *(f"7-gate.yaml#{key}" for key in GATE_KEYS),
        *measured_reads(revision, replies),
        "8-frozen.yaml",
        f"{revision}/2-instruction.md",
        *(f"{earlier}/9-outcome.yaml" for earlier in earlier_outcomes),
    }


def test_a_first_revision_beating_every_control_passes_storing_sealed_aggregates_its_keep_ranks_its_cost_and_a_passed_stop(tmp_path):
    replies = first_replies(instruction_judged=0, aim_judged=3)
    files = frozen_series(tmp_path, replies)

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    assert outcome["outcome"] == "pass"
    assert outcome["checks"] == [
        {"compares": "instruction-vs-empty", "gap": 1.0, "mean_difference": -3.0, "interval": [-3.0, -3.0], "pass": True},
        {"compares": "instruction-vs-aim", "gap": 1.0, "mean_difference": -3.0, "interval": [-3.0, -3.0], "pass": True},
        {"compares": "instruction-vs-placebo", "gap": 1.0, "mean_difference": -3.0, "interval": [-3.0, -3.0], "pass": True},
        {"compares": "completion", "gap": 1.0, "mean_difference": 0.0, "interval": [0.0, 0.0], "pass": True},
    ]
    assert (outcome["instruction_breaches"], outcome["completion_passed"], outcome["words"]) == (0.0, True, 4)
    assert outcome["cost"] == {"replies": 17, "input_tokens": 170, "output_tokens": 85, "seconds": 25.5}
    assert "changed_from_parent" not in outcome
    assert set(outcome["inputs"]) == gate_reads("r1", replies)
    stop = SeriesRecords(files).stop()
    assert (stop["stop"], stop["kept"]) == ("passed", "r1")
    outcome_text = files.read_bytes("r1/9-outcome.yaml").decode()
    assert not [reply.id for reply in replies if reply.split == "sealed" and reply.id in outcome_text]


def test_a_first_revision_missing_one_check_fails_without_a_stop(tmp_path):
    files = frozen_series(tmp_path, first_replies(instruction_judged=0, aim_judged=0))

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    assert outcome["outcome"] == "fail"
    assert [check["pass"] for check in outcome["checks"]] == [True, False, True, True]
    assert not files.holds("9-stop.yaml")


def test_a_later_revision_compares_its_instruction_with_the_parent_on_the_hypothesis_target_beside_borrowed_controls(tmp_path):
    first = first_replies(instruction_judged=3, aim_judged=3)
    files = frozen_series(tmp_path, first)
    revision_gate(files, "r1", bootstrap_rng)
    write_revision_instruction(files, "r2", 2, b"Be brief. Avoid hedges.\n")
    write_yaml(files, "r2/1-hypothesis.yaml", HYPOTHESIS)
    later = [
        Reply("b00000101", "instruction", "t1"),
        *sealed_replies("instruction", 0, 0x110),
        *(reply for start, control in enumerate(CONTROLS) for reply in sealed_replies(control, 3, 0x120 + 0x10 * start, borrowed_from="r1")),
    ]
    write_measured_revision(files, "r2", later)

    revision_gate(files, "r2", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r2")
    assert outcome["changed_from_parent"] == "changed"
    assert outcome["parent_comparison"] == {"target": "d-judge", "mean_difference": -3.0, "interval": [-3.0, -3.0]}
    assert outcome["outcome"] == "pass"
    assert outcome["cost"]["replies"] == 5
    hypothesis_reads = {f"r2/1-hypothesis.yaml#{key}" for key in HYPOTHESIS_KEYS}
    assert set(outcome["inputs"]) == gate_reads("r2", later, ["r1"]) | hypothesis_reads | measured_reads("r1", first)
    assert (SeriesRecords(files).stop()["stop"], SeriesRecords(files).stop()["kept"]) == ("passed", "r2")


def test_a_failing_revision_whose_asks_reach_the_budget_ceiling_stops_capped_for_budget(tmp_path):
    files = frozen_series(tmp_path, first_replies(instruction_judged=0, aim_judged=0), {**GATE, "budget": {"unit": "seconds", "ceiling": 10}})

    revision_gate(files, "r1", bootstrap_rng)

    stop = SeriesRecords(files).stop()
    assert {key: value for key, value in stop.items() if key != "inputs"} == {"stop": "capped", "reason": "budget", "kept": "r1"}
    assert set(stop["inputs"]) == {"7-gate.yaml#keep_rule", "7-gate.yaml#budget", "8-frozen.yaml", "r1/9-outcome.yaml"}


def test_a_completion_check_without_a_unit_holding_done_on_both_sides_stores_no_mean_no_interval_and_fails(tmp_path):
    replies = [reply if reply.condition != "instruction" else Reply(reply.id, reply.condition, reply.task, repeat=reply.repeat, split=reply.split, done=None) for reply in first_replies(0, 3)]
    files = frozen_series(tmp_path, replies)

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    completion = next(check for check in outcome["checks"] if check["compares"] == "completion")
    assert (completion["mean_difference"], completion["interval"], completion["pass"]) == (None, None, False)
    assert (outcome["outcome"], outcome["completion_passed"]) == ("fail", False)


def assert_refused_writing_nothing(files: SeriesFolder, message: str) -> None:
    """Assert `revision gate r1` refuses with the message and writes no outcome."""
    with pytest.raises(Refusal, match=message):
        revision_gate(files, "r1", bootstrap_rng)
    assert not files.holds("r1/9-outcome.yaml")


def test_a_revision_without_its_collection_is_refused(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 3))
    (files.root / "r1/7-collected.yaml").unlink()

    assert_refused_writing_nothing(files, r"^missing record: r1/7-collected\.yaml$")


def test_a_reply_origin_without_its_reply_file_is_refused(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 3))
    (files.root / "r1/5-replies/aim/t3/repeat-2.yaml").unlink()

    assert_refused_writing_nothing(files, r"^unresolved reply: r1/5-replies/aim/t3/repeat-2\.yaml \(r1/6-origins\.yaml\)$")


def test_an_unfrozen_series_is_refused(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 3))
    (files.root / "8-frozen.yaml").unlink()

    assert_refused_writing_nothing(files, r"^missing record: 8-frozen\.yaml$")


def test_a_gated_revision_refuses_a_second_gate(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 0))
    revision_gate(files, "r1", bootstrap_rng)

    with pytest.raises(Refusal, match=r"^already written: r1/9-outcome\.yaml$"):
        revision_gate(files, "r1", bootstrap_rng)
