"""Series commands `series new`, `series stop`, and `series keep`, and the guard of every command but `series new` against a folder that is no series, a stopped series, a changed frozen part, and a broken revision chain."""

import itertools
import os
from collections.abc import Iterator, Mapping, Sequence
from datetime import datetime
from pathlib import Path

from instruction_eval.conditions import UnclosedFrontmatter, strip_frontmatter
from instruction_eval.gate import kept_revision
from instruction_eval.judge import SOURCE_FOLDER
from instruction_eval.records import (
    FAIL_OUTCOME,
    FIRST_REVISION,
    FIRST_REVISION_NUMBER,
    FROZEN_RECORD,
    GATE_RECORD,
    SERIES_RECORD,
    STOP_RECORD,
    UNRESOLVABLE_STOP,
    ReaderKind,
    Record,
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
STATUS_COMMAND = "series status"
STOP_COMMAND = "series stop"
KEEP_COMMAND = "series keep"
OUTCOME_FILE = "9-outcome.yaml"
KEEP_RULE_INPUT = f"{GATE_RECORD}#keep_rule"
GIT_ENTRY = ".git"
LOGIN_MEMORY_FILE = ".claude/CLAUDE.md"
MEMORY_FILES = ("CLAUDE.md", LOGIN_MEMORY_FILE, "CLAUDE.local.md", ".manifestos.yaml")
INSTRUCTION_FILE = "2-instruction.md"
FIRST_INSTRUCTION = f"{FIRST_REVISION}/{INSTRUCTION_FILE}"

STOPPED_SERIES_COMMANDS = (STATUS_COMMAND, KEEP_COMMAND)


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
    _refuse_folder_under_memory_file(files, home)
    _refuse_folder_inside_git_work_tree(files)
    _refuse_non_empty_folder(files)
    _refuse_duplicate_basenames(source_paths)
    texts = {path: _read_external_file(path) for path in (instruction_path, *source_paths)}
    refuse_unclosed_frontmatter(texts)
    write_record(files, SERIES_RECORD, _series_record(instruction_path, source_paths, reader_kind, now), [])
    _make_agents_folder(files)
    _snapshot_sources(files, source_paths, texts)
    write_file(files, FIRST_INSTRUCTION, texts[instruction_path])
    write_record(files, revision_record_path(FIRST_REVISION), _first_revision_record(texts[instruction_path]), [])
    return files


def _resolve_against(working_dir: Path, path: str) -> Path:
    """Return the absolute path `path` names, a relative one taken from the working directory."""
    return Path(os.path.normpath(working_dir / path))


def _series_folder_path(name: str, working_dir: Path, home: Path) -> Path:
    """Return the folder a bare name puts under the home series directory, and any value holding `/` as given."""
    if PATH_SEPARATOR in name:
        return _resolve_against(working_dir, name)
    return home / SERIES_HOME_FOLDER / name


def _refuse_folder_under_memory_file(files: SeriesFolder, home: Path) -> None:
    """Refuse a series folder that or whose ancestor up to `/` holds a memory file, except the home default login's."""
    login_memory_file = home / LOGIN_MEMORY_FILE
    for directory in _folder_and_ancestors(files):
        for memory_file in MEMORY_FILES:
            candidate = directory / memory_file
            if candidate.is_file() and candidate != login_memory_file:
                raise Refusal(f"series folder under a memory file: {candidate}")


def _refuse_folder_inside_git_work_tree(files: SeriesFolder) -> None:
    """Refuse a series folder that or whose ancestor up to `/` holds a `.git` entry."""
    for directory in _folder_and_ancestors(files):
        if (directory / GIT_ENTRY).exists():
            raise Refusal(f"series folder inside a git work tree: {directory}")


def _folder_and_ancestors(files: SeriesFolder) -> tuple[Path, ...]:
    """Return the series folder and each ancestor up to `/`, nearest first."""
    return (files.root, *files.root.parents)


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


def _snapshot_sources(files: SeriesFolder, sources: Sequence[Path], texts: Mapping[Path, bytes]) -> None:
    """Copy each source's bytes to `1-source/<basename>`."""
    for source in sources:
        write_file(files, f"{SOURCE_FOLDER}/{source.name}", texts[source])


def _refuse_duplicate_basenames(sources: Sequence[Path]) -> None:
    """Refuse two sources sharing a basename."""
    seen: set[str] = set()
    for source in sources:
        if source.name in seen:
            raise Refusal(f"duplicate source basename: {source.name}")
        seen.add(source.name)


def _read_external_file(path: Path) -> bytes:
    """Return the bytes of a file outside the series, refusing it when absent or unreadable."""
    try:
        return path.read_bytes()
    except FileNotFoundError:
        raise Refusal(f"missing file: {path}") from None
    except OSError:
        raise Refusal(f"unreadable file: {path}") from None


def refuse_unclosed_frontmatter(texts: Mapping[Path, bytes]) -> None:
    """Refuse a file whose first line is `---` with no later line exactly `---`."""
    for path, text in texts.items():
        try:
            strip_frontmatter(text.decode(), str(path))
        except UnicodeDecodeError:
            raise Refusal(f"not UTF-8: {path}") from None
        except UnclosedFrontmatter as unclosed:
            raise Refusal(str(unclosed)) from None


def series_stop(files: SeriesFolder, reason: str) -> None:
    """Write `9-stop.yaml` as `unresolvable` with the reason and the kept revision ranked from every gated revision's outcome."""
    guard_series(files, STOP_COMMAND)
    outcomes = _gated_outcomes(files, SeriesRecords(files))
    _refuse_unless_latest_gated_revision_failed(outcomes)
    reads = [KEEP_RULE_INPUT, FROZEN_RECORD, *(_outcome_path(revision) for revision in outcomes)]
    write_record(files, STOP_RECORD, {"stop": UNRESOLVABLE_STOP, "kept": kept_revision(outcomes), "reason": reason}, reads)


def series_keep(files: SeriesFolder) -> None:
    """Write the kept revision's instruction snapshot over the live instruction file, refusing a series not stopped or keeping nothing."""
    guard_series(files, KEEP_COMMAND)
    records = SeriesRecords(files)
    kept = _kept_revision(files, records)
    records.series().instruction.write_bytes(files.read_bytes(f"{kept}/{INSTRUCTION_FILE}"))


def _kept_revision(files: SeriesFolder, records: SeriesRecords) -> str:
    """Return the revision the stop keeps, refusing a series not stopped and a stop keeping nothing."""
    if not files.holds(STOP_RECORD):
        raise Refusal("series not stopped")
    kept = records.stop()["kept"]
    if kept is None:
        raise Refusal("no revision passed completion")
    return kept


def _refuse_unless_latest_gated_revision_failed(outcomes: Mapping[str, Record]) -> None:
    """Refuse a series with no gated revision or whose latest gated revision did not fail."""
    if not outcomes:
        raise Refusal("no gated revision to stop on")
    latest, latest_outcome = list(outcomes.items())[-1]
    if latest_outcome["outcome"] != FAIL_OUTCOME:
        raise Refusal(f"latest gated revision {latest} did not fail")


def _gated_outcomes(files: SeriesFolder, records: SeriesRecords) -> dict[str, Record]:
    """Return the outcome of each gated revision by id, in order."""
    return {revision: records.outcome(revision) for revision in revision_ids(files) if files.holds(_outcome_path(revision))}


def _outcome_path(revision: str) -> str:
    """Return the path of a revision's `9-outcome.yaml`."""
    return f"{revision}/{OUTCOME_FILE}"


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
    return itertools.islice(revision_ids(files), 1, None)


def revision_ids(files: SeriesFolder) -> Iterator[str]:
    """Return the ids of the revisions, in order, up to the first without a record."""
    revisions = (f"r{number}" for number in itertools.count(FIRST_REVISION_NUMBER))
    return itertools.takewhile(lambda revision: files.holds(revision_record_path(revision)), revisions)
