from pathlib import Path

import pytest

from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, write_file, write_record
from instruction_eval.revision import revision_new
from series_fixtures import Reply, sha256, write_origins, write_yaml

PARENT_INSTRUCTION = b"Be terse. Avoid hedges.\n"
LIVE_INSTRUCTION = b"Be brief. Avoid hedges.\n"
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
TASKS = {
    "tasks": [
        {"id": "t1", "tempts": "d-judge", "split": "open", "message": "Explain the tides.", "answer_key": None},
        {"id": "t2", "tempts": "d-judge", "split": "sealed", "message": "Explain the snow.", "answer_key": None},
    ],
    "conversations": [{"id": "c1", "split": "open", "turns": ["Plan a trip.", "Pick a quiet week."]}],
}
CONDITIONS = {"controls": ["empty", "aim", "placebo"], "aim": "Answer in few words.", "placebo_source": "/tmp/placebo.md", "omissions": "none"}
COVERAGE = {"demands": {"d-judge": [1], "d-hedge": [2]}, "sentences": {1: ["d-judge"], 2: ["d-hedge"]}}
PLACEBO = b"Lorem ipsum dolor sit amet.\n"
ANCHORS = {"anchors": [{"id": "a-one", "task": "t2", "message": "Explain the snow.", "text": "Cold rain.", "breaches": {"d-judge": 0}, "done": True}]}
REPLIES = [
    Reply("b00000001", "instruction", "t1", judged=1, hedges=0, done=False),
    Reply("b00000002", "instruction", "t1", repeat=2, judged=0, hedges=2),
    Reply("b00000003", "instruction", "t2", split="sealed", judged=4, hedges=4),
]
COLLECTED_PACKET = {
    "accepted": 1,
    "judge_model": "claude-opus-4-1",
    "transcript": "/tmp/transcripts/judge.jsonl",
    "transcript_hash": "a" * 64,
    "anchors": {"breach_difference": {"d-judge": 0.0}, "done_agreement": 1.0},
}
SIGMA = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
NOISE = {"repeats": 2, "level": 0.95, "z": 1.96, "sigma": SIGMA, "checks": {}, "demands": {"d-judge": 0.1, "d-hedge": 0.1}, "done_change": 0.1}
COST = {"replies": 3, "input_tokens": None, "output_tokens": None, "seconds": 1.5}
CHECKS = [{"compares": compares, "gap": 1.0} for compares in ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")]
GATE = {"repeats": 2, "level": 0.95, "done_by": "judge", "checks": CHECKS, "keep_rule": "best-estimate-shortest", "budget": "none"}
HYPOTHESIS = {
    "failing_demand": "d-judge",
    "replies_read": ["b00000001"],
    "change": {"action": "rewrite", "sentence": 1},
    "predicted_movement": {"direction": "down", "size": 0.5},
}
HYPOTHESIS_KEYS = ("failing_demand", "replies_read", "change", "predicted_movement")


def outcome(result: str) -> dict:
    """Return a gated revision's outcome record."""
    return {"outcome": result, "checks": [], "instruction_breaches": 1.0, "completion_passed": True, "words": 4, "cost": COST}


def gated_series(tmp_path: Path, result: str = "fail", hypothesis: dict | None = None) -> SeriesFolder:
    """Write a frozen series whose r1 is judged, detected, and gated with the result, and the r2 hypothesis."""
    live = tmp_path / "live" / "terse.md"
    live.parent.mkdir()
    live.write_bytes(LIVE_INSTRUCTION)
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", {"instruction": str(live), "sources": [], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_record(files, "6-judge/anchors.yaml", ANCHORS, [])
    write_file(files, "r1/2-instruction.md", PARENT_INSTRUCTION)
    write_record(files, "r1/2-revision.yaml", {"number": 1, "parent": None, "hash": sha256(PARENT_INSTRUCTION), "parent_record": None, "change": None}, [])
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    write_file(files, "r1/4-conditions/placebo.md", PLACEBO)
    for reply in REPLIES:
        write_file(files, reply.path_in("r1"), b"reply")
    anchor_ids = write_origins(files, "r1", REPLIES, "a-one")
    for packet, anchor_id in anchor_ids.items():
        entries = [{"id": reply.id, "breaches": {"d-judge": reply.judged}, "done": reply.done, "kind": "answer", "notes": ""} for reply in REPLIES if reply.packet == packet]
        anchor_entry = {"id": anchor_id, "breaches": {"d-judge": 0}, "done": True, "kind": "answer", "notes": ""}
        write_yaml(files, f"r1/7-verdicts/{packet}/k1.yaml", {"verdicts": [*entries, anchor_entry]})
    write_record(files, "r1/7-collected.yaml", {"packets": dict.fromkeys(anchor_ids, COLLECTED_PACKET)}, [])
    detectors = [{"id": reply.id, "breaches": {"d-hedge": reply.hedges}, "done_by_answer_key": None} for reply in REPLIES]
    write_record(files, "r1/7-detectors.yaml", {"verdicts": detectors}, [])
    write_yaml(files, "7-gate.yaml", GATE)
    write_record(files, "8-frozen.yaml", {"hashes": {}, "noise": NOISE, "tool_version": "0.1.0", "frozen_at": "2026-10-14T10:00:00+00:00"}, [])
    write_record(files, "r1/9-outcome.yaml", outcome(result), [])
    write_yaml(files, "r2/1-hypothesis.yaml", hypothesis or HYPOTHESIS)
    return files


def read_live(path: Path) -> bytes:
    """Read the live instruction as the composition root does."""
    return path.read_bytes()


def live_path(files: SeriesFolder) -> Path:
    """Return the live instruction path the fixture series names."""
    return files.root.parent / "live" / "terse.md"


def expected_reads() -> set[str]:
    """Return the Commands-table reads of `revision new` expanded for r2 over the fixture's packets."""
    return {
        "2-demands.yaml#demands",
        "3-tasks.yaml#tasks",
        "3-tasks.yaml#conversations",
        "4-conditions.yaml#aim",
        "7-gate.yaml#done_by",
        "r1/3-coverage.yaml#demands",
        "r1/3-coverage.yaml#sentences",
        "r1/4-conditions/placebo.md",
        "8-frozen.yaml",
        *(f"r2/1-hypothesis.yaml#{key}" for key in HYPOTHESIS_KEYS),
        "r1/2-instruction.md",
        "r1/2-revision.yaml",
        "r1/6-origins.yaml",
        "r1/7-verdicts/t1/k1.yaml",
        "r1/7-verdicts/t2/k1.yaml",
        "r1/7-collected.yaml",
        "r1/7-detectors.yaml",
        "r1/9-outcome.yaml",
    }


def test_a_new_revision_snapshots_the_live_instruction_and_records_its_change_chained_to_the_parent(tmp_path):
    files = gated_series(tmp_path)

    revision_new(files, read_live)

    assert files.read_bytes("r2/2-instruction.md") == LIVE_INSTRUCTION
    record = SeriesRecords(files).revision("r2")
    assert {key: value for key, value in record.items() if key != "inputs"} == {
        "number": 2,
        "parent": "r1",
        "hash": sha256(LIVE_INSTRUCTION),
        "parent_record": sha256(files.read_bytes("r1/2-revision.yaml")),
        "change": {"action": "rewrite", "sentence": 1, "old": "Be terse.", "new": "Be brief."},
    }
    assert set(record["inputs"]) == expected_reads()


def test_editing_the_live_instruction_after_the_snapshot_leaves_the_revision_loadable(tmp_path):
    files = gated_series(tmp_path)
    revision_new(files, read_live)

    live_path(files).write_bytes(b"Be curt. Avoid hedges.\n")

    assert SeriesRecords(files).revision("r2")["hash"] == sha256(LIVE_INSTRUCTION)


def test_a_moved_sentence_records_its_text_as_both_the_old_and_the_new(tmp_path):
    move = {**HYPOTHESIS, "change": {"action": "move", "sentence": 2, "to": 1}}
    files = gated_series(tmp_path, hypothesis=move)
    live_path(files).write_bytes(b"Avoid hedges. Be terse.\n")

    revision_new(files, read_live)

    change = SeriesRecords(files).revision("r2")["change"]
    assert change == {"action": "move", "sentence": 2, "to": 1, "old": "Avoid hedges.", "new": "Avoid hedges."}


def assert_refused_writing_nothing(files: SeriesFolder, message: str) -> None:
    """Assert `revision new` refuses with the message and writes no r2 snapshot or record."""
    with pytest.raises(Refusal, match=message):
        revision_new(files, read_live)
    assert not files.holds("r2/2-instruction.md")
    assert not files.holds("r2/2-revision.yaml")


def test_a_missing_hypothesis_is_refused(tmp_path):
    files = gated_series(tmp_path)
    (files.root / "r2/1-hypothesis.yaml").unlink()

    assert_refused_writing_nothing(files, r"^missing record: r2/1-hypothesis\.yaml$")


def test_a_latest_revision_that_passed_is_refused(tmp_path):
    assert_refused_writing_nothing(gated_series(tmp_path, result="pass"), r"^latest revision r1 did not fail$")


def test_an_ungated_latest_revision_is_refused(tmp_path):
    files = gated_series(tmp_path)
    (files.root / "r1/9-outcome.yaml").unlink()

    assert_refused_writing_nothing(files, r"^latest revision r1 is not gated$")


def test_a_stopped_series_is_refused(tmp_path):
    files = gated_series(tmp_path)
    write_record(files, "9-stop.yaml", {"stop": "unresolvable", "kept": None, "reason": "no hypothesis"}, [])

    assert_refused_writing_nothing(files, r"^series stopped")


def test_an_instruction_not_making_the_named_change_is_refused(tmp_path):
    files = gated_series(tmp_path, hypothesis={**HYPOTHESIS, "change": {"action": "rewrite", "sentence": 2}})

    assert_refused_writing_nothing(files, r"^the instruction does not make the named change: rewrite 2$")


def test_an_instruction_with_unclosed_frontmatter_is_refused(tmp_path):
    files = gated_series(tmp_path)
    live_path(files).write_bytes(b"---\nBe brief. Avoid hedges.\n")

    assert_refused_writing_nothing(files, r"^unclosed frontmatter: ")


@pytest.mark.parametrize(
    ("sentence", "source"),
    [
        (b"Explain the tides briefly.", "task t1: explain the tides"),
        (b"Pick a quiet word.", "conversation c1 turn 2: pick a quiet"),
        (b"Answer in few words.", "aim: answer in few"),
        (b"Lorem ipsum dolor here.", r"r1/4-conditions/placebo\.md: lorem ipsum dolor"),
    ],
)
def test_an_instruction_echoing_a_task_a_turn_the_aim_or_the_placebo_is_refused(tmp_path, sentence, source):
    files = gated_series(tmp_path)
    live_path(files).write_bytes(sentence + b" Avoid hedges.\n")

    assert_refused_writing_nothing(files, rf"^revision r2 echoes {source}$")


@pytest.mark.parametrize(
    ("hypothesis", "message"),
    [
        ({**HYPOTHESIS, "predicted_movement": {"direction": "down", "size": 0.2}}, r"^predicted size 0\.2 does not exceed twice"),
        ({**HYPOTHESIS, "replies_read": ["b00000003"]}, r"^replies_read holds no open reply: b00000003$"),
        ({**HYPOTHESIS, "replies_read": ["b00000002"]}, r"^replies_read shows no failure of d-judge$"),
        ({**HYPOTHESIS, "failing_demand": "d-hedge"}, r"^replies_read shows no failure of d-hedge$"),
        ({**HYPOTHESIS, "failing_demand": "completion", "replies_read": ["b00000002"]}, r"^replies_read shows no failure of completion$"),
        (
            {**HYPOTHESIS, "failing_demand": "completion", "predicted_movement": {"direction": "down", "size": 0.2}},
            r"^predicted size 0\.2 does not exceed twice the change noise of completion: 0\.2$",
        ),
    ],
)
def test_an_unfit_hypothesis_is_refused(tmp_path, hypothesis, message):
    assert_refused_writing_nothing(gated_series(tmp_path, hypothesis=hypothesis), message)


@pytest.mark.parametrize(("failing_demand", "replies_read"), [("d-hedge", ["b00000002"]), ("completion", ["b00000001"])])
def test_a_detector_demand_reads_the_detector_counts_and_completion_the_done_values(tmp_path, failing_demand, replies_read):
    files = gated_series(tmp_path, hypothesis={**HYPOTHESIS, "failing_demand": failing_demand, "replies_read": replies_read})

    revision_new(files, read_live)

    assert files.holds("r2/2-revision.yaml")
