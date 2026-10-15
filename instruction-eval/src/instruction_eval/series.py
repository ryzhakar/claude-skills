"""Series commands: `series new` makes a series folder, and every other command is guarded against a folder that is no series, a stopped series, a changed frozen part, and a broken revision chain."""

import itertools
import os
from collections.abc import Iterator, Sequence
from datetime import datetime
from pathlib import Path

from instruction_eval.judge import SOURCE_FOLDER
from instruction_eval.records import (
    FIRST_REVISION,
    FIRST_REVISION_NUMBER,
    FROZEN_RECORD,
    SERIES_RECORD,
    STOP_RECORD,
    ReaderKind,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    revision_record_path,
    sha256,
    write_file,
    write_record,
)

SERIES_HOME_FOLDER = "instruction-series"
AGENTS_FOLDER = ".claude/agents"
PATH_SEPARATOR = "/"
FIRST_INSTRUCTION = f"{FIRST_REVISION}/2-instruction.md"

STOPPED_SERIES_COMMANDS = ("series status", "series keep")


def series_new(
    name: str,
    instruction: str,
    sources: Sequence[str],
    reader_kind: ReaderKind,
    working_dir: Path,
    home: Path,
    now: datetime,
) -> SeriesFolder:
    """Make the series folder `name` names, holding the snapshots of the live instruction and the sources, and return it."""
    instruction_path = _resolve_against(working_dir, instruction)
    source_paths = [_resolve_against(working_dir, source) for source in sources]
    files = SeriesFolder(_series_folder_path(name, working_dir, home))
    _refuse_non_empty_folder(files)
    instruction_bytes = instruction_path.read_bytes()
    write_record(files, SERIES_RECORD, _series_record(instruction_path, source_paths, reader_kind, now), [])
    _make_agents_folder(files)
    _snapshot_sources(files, source_paths)
    write_file(files, FIRST_INSTRUCTION, instruction_bytes)
    write_record(files, revision_record_path(FIRST_REVISION), _first_revision_record(instruction_bytes), [])
    return files


def _resolve_against(working_dir: Path, path: str) -> Path:
    """Return the absolute path `path` names, a relative one taken from the working directory."""
    return Path(os.path.normpath(working_dir / path))


def _series_folder_path(name: str, working_dir: Path, home: Path) -> Path:
    """Return the folder a bare name puts under the home series directory, and any value holding `/` as given."""
    if PATH_SEPARATOR in name:
        return _resolve_against(working_dir, name)
    return home / SERIES_HOME_FOLDER / name


def _refuse_non_empty_folder(files: SeriesFolder) -> None:
    """Refuse a series folder that exists as a file or holds anything."""
    root = files.root
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise Refusal(f"series folder not empty: {root}")


def _series_record(instruction: Path, sources: Sequence[Path], reader_kind: ReaderKind, now: datetime) -> dict[str, object]:
    """Return the `series.yaml` record of the live instruction and sources."""
    return {
        "instruction": str(instruction),
        "sources": [str(source) for source in sources],
        "reader_kind": reader_kind,
        "created": now.isoformat(),
    }


def _first_revision_record(instruction: bytes) -> dict[str, object]:
    """Return the `r1/2-revision.yaml` record of the first instruction snapshot."""
    return {"number": FIRST_REVISION_NUMBER, "parent": None, "hash": sha256(instruction), "parent_record": None, "change": None}


def _make_agents_folder(files: SeriesFolder) -> None:
    """Make the empty folder the neutral session's agent definitions go in."""
    (files.root / AGENTS_FOLDER).mkdir(parents=True, exist_ok=True)


def _snapshot_sources(files: SeriesFolder, sources: Sequence[Path]) -> None:
    """Copy each source's bytes to `1-source/<basename>`."""
    for source in sources:
        write_file(files, f"{SOURCE_FOLDER}/{source.name}", source.read_bytes())


def guard_series(files: SeriesFolder, command: str) -> None:
    """Refuse running `command` in a folder lacking `series.yaml`, in a stopped series, after a frozen part changed, or past a broken revision chain."""
    _refuse_missing_series(files)
    _refuse_stopped_series(files, command)
    records = SeriesRecords(files)
    _refuse_changed_frozen_parts(files, records)
    _refuse_broken_revision_chain(files, records)


def _refuse_missing_series(files: SeriesFolder) -> None:
    """Refuse a working directory lacking `series.yaml`."""
    if not files.holds(SERIES_RECORD):
        raise Refusal(f"not a series folder: no {SERIES_RECORD}")


def _refuse_stopped_series(files: SeriesFolder, command: str) -> None:
    """Refuse a stopped series to every command but `series status` and `series keep`."""
    if files.holds(STOP_RECORD) and command not in STOPPED_SERIES_COMMANDS:
        raise Refusal(f"series stopped: only {' and '.join(STOPPED_SERIES_COMMANDS)} run")


def _refuse_changed_frozen_parts(files: SeriesFolder, records: SeriesRecords) -> None:
    """Refuse a frozen series when a path `8-frozen.yaml` hashes no longer holds the hashed bytes."""
    if not files.holds(FROZEN_RECORD):
        return
    for path, frozen_hash in records.frozen()["hashes"].items():
        if not files.holds(path) or sha256(files.read_bytes(path)) != frozen_hash:
            raise Refusal(f"frozen part changed: {path}")


def _refuse_broken_revision_chain(files: SeriesFolder, records: SeriesRecords) -> None:
    """Refuse a series whose revision record names a parent record other than the parent's bytes."""
    for revision in _later_revisions(files):
        record = records.revision(revision)
        parent_path = revision_record_path(record["parent"])
        if record["parent_record"] != sha256(files.read_bytes(parent_path)):
            raise Refusal(f"broken revision chain: {revision_record_path(revision)} (parent record {parent_path} differs)")


def _later_revisions(files: SeriesFolder) -> Iterator[str]:
    """Return the ids of the revisions after the first, in order, up to the first without a record."""
    revisions = (f"r{number}" for number in itertools.count(FIRST_REVISION_NUMBER + 1))
    return itertools.takewhile(lambda revision: files.holds(revision_record_path(revision)), revisions)
