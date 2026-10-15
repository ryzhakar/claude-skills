import hashlib
from pathlib import Path

import yaml

from instruction_eval.records import SeriesFolder, write_record
from instruction_eval.series import series_status
from series_fixtures import AGENT_SERIES, sha256, write_revision, write_yaml


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(path.relative_to(root).as_posix().encode())
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def status_of(files: SeriesFolder) -> dict:
    return yaml.safe_load(series_status(files))


def bare_series(tmp_path) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", AGENT_SERIES, [])
    write_revision(files, 1)
    return files


def test_a_fresh_series_reports_its_parts_unfrozen_with_an_ungated_first_revision_and_changes_nothing(tmp_path):
    files = bare_series(tmp_path)
    write_yaml(files, "2-demands.yaml", {"demands": []})
    before = tree_hash(tmp_path)

    status = status_of(files)

    assert tree_hash(tmp_path) == before
    assert status["parts"] == ["series.yaml", "2-demands.yaml"]
    assert status["frozen"] is False
    assert status["revisions"] == {"r1": {"outcome": None, "changed_from_parent": None, "instruction_breaches": None, "completion_passed": None, "words": None}}
    assert status["stop"] is None


DEMANDS = {"demands": [{"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
COVERAGE = {"demands": {"d-judge": [1]}, "sentences": {1: ["d-judge"]}}
SIGMA = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
NOISE = {"repeats": 2, "level": 0.95, "z": 1.96, "sigma": SIGMA, "checks": {}, "demands": {}, "done_change": None}
FROZEN_PARTS = ("series.yaml", "2-demands.yaml", "r1/2-instruction.md", "r1/3-coverage.yaml")
CHECKS = [{"compares": compares, "gap": 1.0} for compares in ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")]
GATE = {"repeats": 2, "level": 0.95, "done_by": "judge", "checks": CHECKS, "keep_rule": "best-estimate-shortest", "budget": "none"}


def outcome(passed: bool, instruction_breaches: float, words: int, cost: dict, changed_from_parent: str | None = None) -> dict:
    record = {
        "outcome": "pass" if passed else "fail",
        "checks": [],
        "instruction_breaches": instruction_breaches,
        "completion_passed": True,
        "words": words,
        "cost": cost,
    }
    if changed_from_parent is None:
        return record
    return {**record, "changed_from_parent": changed_from_parent, "parent_comparison": {"target": "d-judge", "mean_difference": -0.4, "interval": [-0.8, 0.0]}}


def gated_series(tmp_path, gate: dict, outcomes: dict[int, dict]) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", AGENT_SERIES, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "7-gate.yaml", gate)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    for number in outcomes:
        write_revision(files, number)
    hashes = {path: sha256(files.read_bytes(path)) for path in FROZEN_PARTS}
    write_record(files, "8-frozen.yaml", {"hashes": hashes, "noise": NOISE, "tool_version": "0.1.0", "frozen_at": "2026-10-14T10:00:00+00:00"}, [])
    for number, record in outcomes.items():
        write_record(files, f"r{number}/9-outcome.yaml", record, [])
    return files


FIRST_COST = {"replies": 4, "input_tokens": 100, "output_tokens": 20, "seconds": 1.5}
SECOND_COST = {"replies": 2, "input_tokens": 50, "output_tokens": 10, "seconds": 0.5}


def test_a_frozen_series_reports_each_gated_revisions_ranks_and_the_cost_so_far_against_the_budget(tmp_path):
    budget = {"unit": "tokens", "ceiling": 500}
    files = gated_series(
        tmp_path,
        {**GATE, "budget": budget},
        {1: outcome(False, 1.5, 40, FIRST_COST), 2: outcome(True, 0.5, 30, SECOND_COST, "changed")},
    )

    status = status_of(files)

    assert status["frozen"] is True
    assert status["revisions"] == {
        "r1": {"outcome": "fail", "changed_from_parent": None, "instruction_breaches": 1.5, "completion_passed": True, "words": 40},
        "r2": {"outcome": "pass", "changed_from_parent": "changed", "instruction_breaches": 0.5, "completion_passed": True, "words": 30},
    }
    assert status["cost"] == {"spent": {"replies": 6, "input_tokens": 150, "output_tokens": 30, "seconds": 2.0}, "budget": budget}


PLAN = {
    "judge_model": "claude-opus-4-1",
    "raters": ["agent", "agent"],
    "rater_model": "claude-sonnet-4-5",
    "sample_size": 12,
    "anchors_per_packet": 3,
    "acceptance": {"breach_difference": 0.5, "self_difference": 0.25, "done_agreement": 0.8},
}
UNRATED = "unrated"


def agreement(scale: float | None) -> dict:
    return {"demands": {"d-judge": {"breach_difference": 0.25, "self_difference": 0.5}}, "done_agreement": 0.9, "scale": scale, "ratings": {}}


def write_attempt(files: SeriesFolder, number: int, scale: float | None | str) -> None:
    folder = f"6-judge/calibration/attempt-{number}"
    write_yaml(files, f"{folder}/plan.yaml", PLAN)
    if scale != UNRATED:
        write_record(files, f"{folder}/agreement.yaml", agreement(scale), [])


def test_a_stopped_series_reports_each_calibration_attempt_with_its_scale_and_the_accepted_one_and_the_stop(tmp_path):
    files = gated_series(tmp_path, GATE, {1: outcome(False, 1.5, 40, FIRST_COST)})
    write_attempt(files, 1, 1.2)
    write_attempt(files, 2, None)
    write_attempt(files, 3, UNRATED)
    accepted = {**{key: value for key, value in PLAN.items() if key != "rater_model"}, "attempt": 2, "brief_hash": "c" * 64, "agreement": {**agreement(None), "inputs": {}}}
    write_record(files, "6-judge/calibration.yaml", accepted, ["6-judge/calibration/attempt-2/plan.yaml"])
    write_record(files, "9-stop.yaml", {"stop": "capped", "kept": "r1", "reason": "budget"}, [])

    status = status_of(files)

    assert status["calibration"] == {
        "attempts": [{"attempt": 1, "scale": 1.2}, {"attempt": 2, "scale": None}, {"attempt": 3, "scale": None}],
        "accepted": 2,
    }
    assert status["stop"] == {"stop": "capped", "kept": "r1", "reason": "budget"}
