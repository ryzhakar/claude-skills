import hashlib
import re

import pytest
import yaml

from instruction_eval.records import Refusal, SeriesFolder, guard_series, write_file, write_record

SERIES = {
    "instruction": "/home/writer/terse.md",
    "sources": [],
    "reader_kind": "agent",
    "created": "2026-10-14T10:00:00+00:00",
}
DEMANDS = {"demands": [{"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
COVERAGE = {"demands": {"d-judge": [1]}, "sentences": {1: ["d-judge"]}}
SIGMA = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
NOISE = {"repeats": 2, "level": 0.95, "z": 1.96, "sigma": SIGMA, "checks": {}, "demands": {}, "done_change": None}
FROZEN_PARTS = ("series.yaml", "2-demands.yaml", "r1/2-instruction.md", "r1/3-coverage.yaml")


def sha256(files: SeriesFolder, path: str) -> str:
    return hashlib.sha256((files.root / path).read_bytes()).hexdigest()


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    target = files.root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(document))


def write_revision(files: SeriesFolder, number: int, parent_record: str) -> None:
    revision = f"r{number}"
    write_file(files, f"{revision}/2-instruction.md", f"Revision {number}.\n".encode())
    change = {"action": "rewrite", "sentence": 1, "old": "Old.", "new": "New."}
    record = {
        "number": number,
        "parent": f"r{number - 1}",
        "hash": sha256(files, f"{revision}/2-instruction.md"),
        "parent_record": parent_record,
        "change": change,
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [f"r{number - 1}/2-revision.yaml"])


@pytest.fixture
def files(tmp_path):
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", SERIES, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_file(files, "r1/2-instruction.md", b"Be terse.\n")
    first = {"number": 1, "parent": None, "hash": sha256(files, "r1/2-instruction.md"), "parent_record": None, "change": None}
    write_record(files, "r1/2-revision.yaml", first, [])
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    frozen = {
        "hashes": {path: sha256(files, path) for path in FROZEN_PARTS},
        "noise": NOISE,
        "tool_version": "0.1.0",
        "frozen_at": "2026-10-14T10:00:00+00:00",
    }
    write_record(files, "8-frozen.yaml", frozen, [])
    write_revision(files, 2, sha256(files, "r1/2-revision.yaml"))
    write_revision(files, 3, sha256(files, "r2/2-revision.yaml"))
    return files


def test_a_frozen_series_with_unchanged_parts_and_an_unbroken_chain_runs_any_command(files):
    guard_series(files, "revision gate")


def test_a_folder_lacking_series_yaml_refuses_every_command(tmp_path):
    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        guard_series(SeriesFolder(tmp_path), "series status")


def stop(files: SeriesFolder) -> None:
    write_record(files, "9-stop.yaml", {"stop": "capped", "kept": "r1"}, [])


@pytest.mark.parametrize("command", ["revision ask", "revision new", "series stop", "judge prepare"])
def test_a_stopped_series_refuses_every_command_that_could_change_it(files, command):
    stop(files)
    with pytest.raises(Refusal, match=r"^series stopped: only series status and series keep run$"):
        guard_series(files, command)


@pytest.mark.parametrize("command", ["series status", "series keep"])
def test_a_stopped_series_still_runs_status_and_keep(files, command):
    stop(files)
    guard_series(files, command)


@pytest.mark.parametrize("part", FROZEN_PARTS)
def test_a_frozen_series_whose_part_changed_a_byte_refuses_naming_it(files, part):
    with (files.root / part).open("ab") as frozen_part:
        frozen_part.write(b" ")
    with pytest.raises(Refusal, match=rf"^frozen part changed: {re.escape(part)}$"):
        guard_series(files, "revision ask")


def test_a_frozen_series_whose_part_was_deleted_refuses_naming_it(files):
    (files.root / "r1/2-instruction.md").unlink()
    with pytest.raises(Refusal, match=r"^unresolved frozen part: r1/2-instruction\.md \(8-frozen\.yaml\)$"):
        guard_series(files, "revision ask")


def test_an_unfrozen_series_runs_after_its_parts_change(files):
    (files.root / "8-frozen.yaml").unlink()
    write_yaml(files, "2-demands.yaml", {"demands": [{**DEMANDS["demands"][0], "text": "Be brief."}]})
    guard_series(files, "series freeze")


def test_a_revision_record_naming_another_parent_record_refuses_as_a_broken_chain(files):
    (files.root / "r3/2-revision.yaml").unlink()
    (files.root / "r3/2-instruction.md").unlink()
    write_revision(files, 3, "0" * 64)
    with pytest.raises(Refusal, match=r"^broken revision chain: r3/2-revision\.yaml \(parent record r2/2-revision\.yaml differs\)$"):
        guard_series(files, "revision gate")


def test_an_edited_parent_record_refuses_every_command_on_its_child(files):
    with (files.root / "r2/2-revision.yaml").open("a") as parent_record:
        parent_record.write("\n")
    with pytest.raises(Refusal, match=r"^stale: r3/2-revision\.yaml \(input r2/2-revision\.yaml changed\)$"):
        guard_series(files, "revision gate")
