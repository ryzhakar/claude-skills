from pathlib import Path

import pytest

from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, reply_path, write_file, write_record
from instruction_eval.series import refuse_unready_freeze
from series_fixtures import ONE_DEMAND, ONE_DEMAND_COVERAGE, sha256, write_yaml

INSTRUCTION = b"Be terse.\n"
PLACEBO = b"Lorem ipsum dolor sit amet.\n"
TASKS = {
    "tasks": [
        {"id": "t-open", "tempts": "d-judge", "split": "open", "message": "Explain the tides.", "answer_key": None},
        {"id": "t-sealed", "tempts": "d-judge", "split": "sealed", "message": "Explain the snow.", "answer_key": None},
        {"id": "o-open", "tempts": "overreach", "split": "open", "message": "Name the moon.", "answer_key": "moon"},
        {"id": "o-sealed", "tempts": "overreach", "split": "sealed", "message": "Name the sun.", "answer_key": "sun"},
    ],
    "conversations": [],
}
CONDITIONS = {"controls": ["empty", "aim", "placebo"], "aim": "Answer in few words.", "placebo_source": "/tmp/placebo.md", "omissions": "none"}
CONDITION_NAMES = ("instruction", "empty", "aim", "placebo")
CHECKS = [{"compares": compares, "gap": 1.0} for compares in ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")]
GATE = {"repeats": 2, "level": 0.95, "done_by": "judge", "checks": CHECKS, "keep_rule": "best-estimate-shortest", "budget": "none"}
HASH = "a" * 64
FINGERPRINT_HASH = "f" * 64
AGENT_READER = {"kind": "agent", "model": "claude-sonnet-4-5"}
COMMAND_READER = {"kind": "command", "model": "local-7b", "command": ["run", "{condition}"], "fingerprint": ["fingerprint"], "sampling": {"temperature": 0}}
NULL_COST = dict.fromkeys(("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "spent_input_tokens"))
PROCESSED_RECORDS = ("r1/6-origins.yaml", "r1/7-collected.yaml", "r1/7-detectors.yaml")


def reply(condition: str, task: dict, repeat: int, reader_kind: str) -> dict:
    """Return the reply record of one r1 task repeat under the condition by a reader of the kind."""
    record = {
        "condition": condition,
        "task": task["id"],
        "split": task["split"],
        "repeat": repeat,
        "message": task["message"],
        "text": "An answer.",
        "model": "claude-sonnet-4-5",
        "reader_kind": reader_kind,
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.0,
        "cost": NULL_COST,
    }
    if reader_kind == "agent":
        return {**record, "transcript": "/tmp/transcripts/reader.jsonl", "transcript_hash": HASH}
    return {**record, "fingerprint_hash": FINGERPRINT_HASH}


def ready_series(tmp_path: Path, reader: dict = AGENT_READER) -> SeriesFolder:
    """Write a series whose r1 is asked, collected, blinded, judged, and detected, and whose gate is complete."""
    files = SeriesFolder(tmp_path / "series")
    reader_kind = reader["kind"]
    write_record(files, "series.yaml", {"instruction": "/tmp/terse.md", "sources": [], "reader_kind": reader_kind, "created": "2026-10-14T10:00:00+00:00"}, [])
    write_yaml(files, "2-demands.yaml", ONE_DEMAND)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_file(files, "4-placebo-source.md", PLACEBO)
    write_yaml(files, "5-reader.yaml", reader)
    write_record(files, "6-judge/calibration.yaml", {"attempt": 1}, [])
    write_yaml(files, "7-gate.yaml", GATE)
    write_file(files, "r1/2-instruction.md", INSTRUCTION)
    write_record(files, "r1/2-revision.yaml", {"number": 1, "parent": None, "hash": sha256(INSTRUCTION), "parent_record": None, "change": None}, [])
    write_yaml(files, "r1/3-coverage.yaml", ONE_DEMAND_COVERAGE)
    for condition in CONDITION_NAMES:
        write_file(files, f"r1/4-conditions/{condition}.md", condition.encode())
        for task in TASKS["tasks"]:
            for repeat in (1, 2):
                write_record(files, reply_path("r1", condition, task["id"], repeat, None), reply(condition, task, repeat, reader_kind), [f"r1/4-conditions/{condition}.md"])
    for path in PROCESSED_RECORDS:
        write_record(files, path, {}, ["4-placebo-source.md"])
    return files


def read_nothing(path: Path) -> bytes:
    """Stand in for the external file reader, which a series holding its placebo snapshot never calls."""
    raise AssertionError(f"read an external file: {path}")


def test_a_ready_series_freezes_without_refusal(tmp_path):
    files = ready_series(tmp_path)
    refuse_unready_freeze(files, SeriesRecords(files), None, read_nothing)


def test_a_missing_calibration_is_refused(tmp_path):
    files = ready_series(tmp_path)
    (files.root / "6-judge/calibration.yaml").unlink()

    with pytest.raises(Refusal, match=r"^no 6-judge/calibration\.yaml$"):
        refuse_unready_freeze(files, SeriesRecords(files), None, read_nothing)


def assert_refused(files: SeriesFolder, message: str, fingerprint_hash: str | None = None) -> None:
    """Assert the freeze readiness check refuses the series with the message."""
    with pytest.raises(Refusal, match=message):
        refuse_unready_freeze(files, SeriesRecords(files), fingerprint_hash, read_nothing)


@pytest.mark.parametrize("path", ["2-demands.yaml", "3-tasks.yaml", "4-conditions.yaml", "4-placebo-source.md", "5-reader.yaml"])
def test_a_missing_part_is_refused(tmp_path, path):
    files = ready_series(tmp_path)
    (files.root / path).unlink()

    assert_refused(files, rf"^missing record: {path}$")


@pytest.mark.parametrize("key", ["repeats", "level", "done_by", "checks", "keep_rule", "budget"])
def test_a_gate_missing_a_key_is_refused_the_keep_rule_included(tmp_path, key):
    files = ready_series(tmp_path)
    write_yaml(files, "7-gate.yaml", {name: value for name, value in GATE.items() if name != key})

    assert_refused(files, rf"^missing key: 7-gate\.yaml#{key}$")


def test_a_failing_demands_check_is_refused(tmp_path):
    files = ready_series(tmp_path)
    write_yaml(files, "2-demands.yaml", {"demands": ONE_DEMAND["demands"] * 2})

    assert_refused(files, r"^duplicate demand id: d-judge")


def test_a_failing_tasks_check_is_refused(tmp_path):
    files = ready_series(tmp_path)
    keyless = [{**task, "answer_key": None} for task in TASKS["tasks"]]
    write_yaml(files, "3-tasks.yaml", {**TASKS, "tasks": keyless})

    assert_refused(files, r"^overreach task without answer_key: o-open")


def test_a_first_coverage_failing_its_check_is_refused(tmp_path):
    files = ready_series(tmp_path)
    write_yaml(files, "r1/3-coverage.yaml", {"demands": {"d-judge": [1]}, "sentences": {}})

    assert_refused(files, r"^sentence 1 carries no demand \(imported\)$")


def test_a_gap_against_the_first_expected_replies_is_refused(tmp_path):
    files = ready_series(tmp_path)
    (files.root / "r1/5-replies/aim/o-open/repeat-2.yaml").unlink()

    assert_refused(files, r"^missing replies: 1, first r1/5-replies/aim/o-open/repeat-2\.yaml$")


@pytest.mark.parametrize(("step", "path"), [("blinded", "r1/6-origins.yaml"), ("judged", "r1/7-collected.yaml"), ("detected", "r1/7-detectors.yaml")])
def test_a_first_revision_not_blinded_judged_or_detected_is_refused(tmp_path, step, path):
    files = ready_series(tmp_path)
    (files.root / path).unlink()

    assert_refused(files, rf"^r1 not {step}: no {path}$")


def test_a_stale_first_revision_record_is_refused(tmp_path):
    files = ready_series(tmp_path)
    (files.root / "4-placebo-source.md").write_bytes(b"Lorem ipsum dolor sit amet again.\n")

    assert_refused(files, r"^stale: r1/6-origins\.yaml \(input 4-placebo-source\.md changed\)$")


def test_a_command_reader_whose_fresh_fingerprint_matches_every_first_reply_is_ready(tmp_path):
    files = ready_series(tmp_path, COMMAND_READER)
    refuse_unready_freeze(files, SeriesRecords(files), FINGERPRINT_HASH, read_nothing)


def test_a_command_reader_whose_fresh_fingerprint_differs_from_a_first_reply_is_refused(tmp_path):
    files = ready_series(tmp_path, COMMAND_READER)

    assert_refused(files, r"^reader fingerprint changed since r1/5-replies/aim/o-open/repeat-1\.yaml$", fingerprint_hash="0" * 64)


def test_a_drift_check_without_conversations_is_refused(tmp_path):
    files = ready_series(tmp_path)
    write_yaml(files, "7-gate.yaml", {**GATE, "checks": [*CHECKS, {"compares": "drift", "gap": 1.0}]})

    assert_refused(files, r"^drift check without conversations \(3-tasks\.yaml\)$")


def test_a_near_source_check_without_sources_is_refused(tmp_path):
    files = ready_series(tmp_path)
    write_yaml(files, "7-gate.yaml", {**GATE, "checks": [*CHECKS, {"compares": "instruction-near-source", "gap": 1.0}]})

    assert_refused(files, r"^instruction-near-source check without sources \(series\.yaml\)$")
