"""Guards every command but `series new` against a folder that is no series, a stopped series, a changed frozen part, and a broken revision chain."""

import itertools
from collections.abc import Iterator

from instruction_eval.records import (
    FIRST_REVISION_NUMBER,
    FROZEN_RECORD,
    SERIES_RECORD,
    STOP_RECORD,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    revision_record_path,
    sha256,
)

STOPPED_SERIES_COMMANDS = ("series status", "series keep")


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
