import hashlib

import pytest
import yaml

from instruction_eval.records import Refusal, SeriesFolder, write_file, write_record
from instruction_eval.series import series_stop

SERIES = {
    "instruction": "/home/writer/terse.md",
    "sources": [],
    "reader_kind": "agent",
    "created": "2026-10-14T10:00:00+00:00",
}
DEMANDS = {"demands": [{"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
COVERAGE = {"demands": {"d-judge": [1]}, "sentences": {1: ["d-judge"]}}
GATE = {"keep_rule": "best-estimate-shortest"}
SIGMA = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
NOISE = {"repeats": 2, "level": 0.95, "z": 1.96, "sigma": SIGMA, "checks": {}, "demands": {}, "done_change": None}
COST = {"replies": 4, "input_tokens": None, "output_tokens": None, "seconds": 1.5}
FROZEN_PARTS = ("series.yaml", "2-demands.yaml", "r1/2-instruction.md", "r1/3-coverage.yaml")
REASON = "no hypothesis clears twice its noise"


def sha256(files: SeriesFolder, path: str) -> str:
    return hashlib.sha256((files.root / path).read_bytes()).hexdigest()


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    target = files.root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(document))


def write_revision(files: SeriesFolder, number: int) -> None:
    revision = f"r{number}"
    write_file(files, f"{revision}/2-instruction.md", f"Revision {number}.\n".encode())
    first = number == 1
    record = {
        "number": number,
        "parent": None if first else f"r{number - 1}",
        "hash": sha256(files, f"{revision}/2-instruction.md"),
        "parent_record": None if first else sha256(files, f"r{number - 1}/2-revision.yaml"),
        "change": None if first else {"action": "rewrite", "sentence": 1, "old": "Old.", "new": "New."},
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [] if first else [f"r{number - 1}/2-revision.yaml"])


def outcome(passed: bool, completion_passed: bool, instruction_breaches: float, words: int) -> dict:
    return {
        "outcome": "pass" if passed else "fail",
        "checks": [],
        "instruction_breaches": instruction_breaches,
        "completion_passed": completion_passed,
        "words": words,
        "cost": COST,
    }


def frozen_series(tmp_path, revisions: int, outcomes: dict[int, dict]) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", SERIES, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "7-gate.yaml", GATE)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    for number in range(1, revisions + 1):
        write_revision(files, number)
    frozen = {
        "hashes": {path: sha256(files, path) for path in FROZEN_PARTS},
        "noise": NOISE,
        "tool_version": "0.1.0",
        "frozen_at": "2026-10-14T10:00:00+00:00",
    }
    write_record(files, "8-frozen.yaml", frozen, [])
    for number, record in outcomes.items():
        write_record(files, f"r{number}/9-outcome.yaml", record, [])
    return files


def read_stop(files: SeriesFolder) -> dict:
    return yaml.safe_load((files.root / "9-stop.yaml").read_bytes())


def test_a_failed_latest_gated_revision_stops_the_series_keeping_the_best_estimate_of_every_gated_revision(tmp_path):
    files = frozen_series(tmp_path, 2, {1: outcome(False, True, 0.5, 40), 2: outcome(False, True, 0.25, 30)})

    series_stop(files, REASON)

    stop = read_stop(files)
    inputs = stop.pop("inputs")
    assert stop == {"stop": "unresolvable", "kept": "r2", "reason": REASON}
    assert set(inputs) == {"7-gate.yaml#keep_rule", "8-frozen.yaml", "r1/9-outcome.yaml", "r2/9-outcome.yaml"}
    assert inputs["8-frozen.yaml"] == sha256(files, "8-frozen.yaml")


def test_an_ungated_later_revision_is_no_candidate_and_leaves_the_latest_gated_revision_the_latest(tmp_path):
    files = frozen_series(tmp_path, 3, {1: outcome(False, True, 0.25, 30), 2: outcome(False, True, 0.5, 40)})

    series_stop(files, REASON)

    stop = read_stop(files)
    assert stop["kept"] == "r1"
    assert set(stop["inputs"]) == {"7-gate.yaml#keep_rule", "8-frozen.yaml", "r1/9-outcome.yaml", "r2/9-outcome.yaml"}


def test_a_series_with_no_revision_passing_completion_stops_keeping_nothing(tmp_path):
    files = frozen_series(tmp_path, 1, {1: outcome(False, False, 0.0, 10)})

    series_stop(files, REASON)

    assert read_stop(files)["kept"] is None


def test_a_series_with_no_gated_revision_refuses(tmp_path):
    files = frozen_series(tmp_path, 1, {})

    with pytest.raises(Refusal, match=r"^no gated revision to stop on$"):
        series_stop(files, REASON)


def test_a_passed_latest_gated_revision_refuses(tmp_path):
    files = frozen_series(tmp_path, 2, {1: outcome(False, True, 0.5, 40), 2: outcome(True, True, 0.0, 30)})

    with pytest.raises(Refusal, match=r"^latest gated revision r2 did not fail$"):
        series_stop(files, REASON)


def test_a_stopped_series_refuses_a_second_stop_leaving_the_first(tmp_path):
    files = frozen_series(tmp_path, 1, {1: outcome(False, True, 0.5, 40)})
    series_stop(files, REASON)
    first = read_stop(files)

    with pytest.raises(Refusal, match=r"^series stopped: only series status and series keep run$"):
        series_stop(files, "another reason")
    assert read_stop(files) == first


def test_a_folder_that_is_no_series_refuses(tmp_path):
    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        series_stop(SeriesFolder(tmp_path), REASON)
