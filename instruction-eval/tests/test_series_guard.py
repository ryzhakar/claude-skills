import re

import pytest

from instruction_eval.records import Refusal, SeriesFolder, guard_series, write_file, write_record
from series_fixtures import ONE_DEMAND, ONE_DEMAND_COVERAGE, SERIES_BINDING, sha256, write_revision, write_yaml

SERIES = {
    "instruction": "/home/writer/terse.md",
    "sources": [],
    "reader_kind": "agent",
    "binding": SERIES_BINDING,
    "created": "2026-10-14T10:00:00+00:00",
}
SIGMA = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
NOISE = {"repeats": 2, "level": 0.95, "z": 1.96, "sigma": SIGMA, "checks": {}, "demands": {}, "done_change": None}
FROZEN_PARTS = ("series.yaml", "2-demands.yaml", "r1/2-instruction.md", "r1/3-coverage.yaml")


@pytest.fixture
def guarded_files(tmp_path):
    guarded_files = SeriesFolder(tmp_path)
    write_record(guarded_files, "series.yaml", SERIES, [])
    write_yaml(guarded_files, "2-demands.yaml", ONE_DEMAND)
    write_file(guarded_files, "r1/2-instruction.md", b"Be terse.\n")
    first = {"number": 1, "parent": None, "hash": sha256(guarded_files.read_bytes("r1/2-instruction.md")), "parent_record": None, "change": None}
    write_record(guarded_files, "r1/2-revision.yaml", first, [])
    write_yaml(guarded_files, "r1/3-coverage.yaml", ONE_DEMAND_COVERAGE)
    frozen = {
        "hashes": {path: sha256(guarded_files.read_bytes(path)) for path in FROZEN_PARTS},
        "noise": NOISE,
        "tool_version": "0.1.0",
        "frozen_at": "2026-10-14T10:00:00+00:00",
    }
    write_record(guarded_files, "8-frozen.yaml", frozen, [])
    write_revision(guarded_files, 2, sha256(guarded_files.read_bytes("r1/2-revision.yaml")))
    write_revision(guarded_files, 3, sha256(guarded_files.read_bytes("r2/2-revision.yaml")))
    return guarded_files


def test_a_frozen_series_with_unchanged_parts_and_an_unbroken_chain_runs_any_command(guarded_files):
    guard_series(guarded_files, "revision gate")


def test_a_folder_lacking_series_yaml_refuses_every_command(tmp_path):
    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        guard_series(SeriesFolder(tmp_path), "series status")


def stop(guarded_files: SeriesFolder) -> None:
    write_record(guarded_files, "9-stop.yaml", {"stop": "capped", "kept": "r1"}, [])


@pytest.mark.parametrize("command", ["revision ask", "revision new", "series stop", "judge prepare"])
def test_a_stopped_series_refuses_every_command_that_could_change_it(guarded_files, command):
    stop(guarded_files)
    with pytest.raises(Refusal, match=r"^series stopped: only series status and series keep run$"):
        guard_series(guarded_files, command)


@pytest.mark.parametrize("command", ["series status", "series keep"])
def test_a_stopped_series_still_runs_status_and_keep(guarded_files, command):
    stop(guarded_files)
    guard_series(guarded_files, command)


@pytest.mark.parametrize("part", FROZEN_PARTS)
def test_a_frozen_series_whose_part_changed_a_byte_refuses_naming_it(guarded_files, part):
    with (guarded_files.root / part).open("ab") as frozen_part:
        frozen_part.write(b" ")
    with pytest.raises(Refusal, match=rf"^frozen part changed: {re.escape(part)}$"):
        guard_series(guarded_files, "revision ask")


def test_a_frozen_series_whose_part_was_deleted_refuses_naming_it(guarded_files):
    (guarded_files.root / "r1/2-instruction.md").unlink()
    with pytest.raises(Refusal, match=r"^unresolved frozen part: r1/2-instruction\.md \(8-frozen\.yaml\)$"):
        guard_series(guarded_files, "revision ask")


def test_an_unfrozen_series_runs_after_its_parts_change(guarded_files):
    (guarded_files.root / "8-frozen.yaml").unlink()
    write_yaml(guarded_files, "2-demands.yaml", {"demands": [{**ONE_DEMAND["demands"][0], "text": "Be brief."}]})
    guard_series(guarded_files, "series freeze")


def test_a_revision_record_naming_another_parent_record_refuses_as_a_broken_chain(guarded_files):
    (guarded_files.root / "r3/2-revision.yaml").unlink()
    (guarded_files.root / "r3/2-instruction.md").unlink()
    write_revision(guarded_files, 3, "0" * 64)
    with pytest.raises(Refusal, match=r"^broken revision chain: r3/2-revision\.yaml \(parent record r2/2-revision\.yaml differs\)$"):
        guard_series(guarded_files, "revision gate")


def test_an_edited_parent_record_refuses_every_command_on_its_child(guarded_files):
    with (guarded_files.root / "r2/2-revision.yaml").open("a") as parent_record:
        parent_record.write("\n")
    with pytest.raises(Refusal, match=r"^stale: r3/2-revision\.yaml \(input r2/2-revision\.yaml changed\)$"):
        guard_series(guarded_files, "revision gate")
