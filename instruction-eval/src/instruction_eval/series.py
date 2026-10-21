"""Series commands `series new`, `series freeze`, `series stop`, `series keep`, and `series status`."""

import fnmatch
import itertools
import os
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import datetime
from pathlib import Path

import yaml

from instruction_eval.conditions import (
    UnclosedFrontmatter,
    strip_frontmatter,
)
from instruction_eval.coverage import coverage_check, split_sentences
from instruction_eval.demands import demands_check
from instruction_eval.gate import (
    BudgetRefusal,
    SeriesShape,
    kept_revision,
    least_repeats,
    measured_revision,
    near_source_without_sources,
    refuse_unaffordable_freeze,
    refuse_unresolvable_gaps,
    reply_cost,
    stop_budget,
    sum_unless_null,
)
from instruction_eval.reader import MEMORY_RELATIVE_PATHS, USER_MEMORY_RELATIVE_PATH, refuse_other_reader_build
from instruction_eval.records import (
    AGENTS_FOLDER,
    AGREEMENT_FILE,
    ANCHORS_RECORD,
    ATTEMPT_FOLDER_PREFIX,
    CALIBRATION_FOLDER,
    CALIBRATION_RECORD,
    COLLECTED_FILE,
    COMMAND_READER,
    CONDITIONS_RECORD,
    COVERAGE_FILE,
    DEMANDS_RECORD,
    DETECTORS_FILE,
    DRIFT_COMPARES,
    FAIL_OUTCOME,
    FIRST_ATTEMPT,
    FIRST_REVISION,
    FIRST_REVISION_NUMBER,
    FROZEN_RECORD,
    GATE_RECORD,
    INSTRUCTION_FILE,
    KEEP_COMMAND,
    KEY_SEPARATOR,
    NEAR_SOURCE_COMPARES,
    OPEN_SPLIT,
    ORIGINS_FILE,
    PLACEBO_SNAPSHOT,
    PLAN_FILE,
    READER_RECORD,
    REFERENCE_USER_FILE,
    SERIES_RECORD,
    SOURCE_FOLDER,
    STATUS_COMMAND,
    STOP_RECORD,
    TASKS_RECORD,
    UNRESOLVABLE_STOP,
    VERDICTS_FOLDER,
    WORKING_BRIEF,
    Binding,
    Budget,
    CompleteGate,
    GateCheck,
    ReaderKind,
    Record,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    attempt_folder,
    guard_series,
    load_record,
    outcome_path,
    revision_ids,
    revision_record_path,
    sha256,
    source_snapshot_path,
    utf8_text,
    write_file,
    write_record,
)
from instruction_eval.scores import (
    BootstrapRng,
    Noise,
    measure_noise,
)
from instruction_eval.tasks import (
    ExpectedReply,
    expected_replies,
    omission_conditions,
    refuse_missing_replies,
    tasks_check,
)

SERIES_HOME_FOLDER = "instruction-series"
PATH_SEPARATOR = "/"
STOP_COMMAND = "series stop"
KEEP_RULE_INPUT = f"{GATE_RECORD}{KEY_SEPARATOR}keep_rule"
GIT_ENTRY = ".git"
FIRST_INSTRUCTION = f"{FIRST_REVISION}/{INSTRUCTION_FILE}"


def series_new(
    name: str,
    instruction: str,
    sources: Sequence[str],
    reader_kind: ReaderKind,
    binding: Binding,
    working_dir: Path,
    home: Path,
    now: datetime,
) -> SeriesFolder:
    """Make the series folder `name` names, holding the snapshots of the live instruction and the sources and the judges' binding, and return it."""
    instruction_path = _resolve_against(working_dir, instruction)
    source_paths = [_resolve_against(working_dir, source) for source in sources]
    files = SeriesFolder(_series_folder_path(name, working_dir, home))
    _refuse_folder_under_memory_file(files, home)
    _refuse_folder_inside_git_work_tree(files)
    _refuse_non_empty_folder(files)
    _refuse_duplicate_basenames(source_paths)
    texts = {path: _read_external_file(path) for path in (instruction_path, *source_paths)}
    refuse_unclosed_frontmatter(texts)
    write_record(files, SERIES_RECORD, _series_record(instruction_path, source_paths, reader_kind, binding, now), [])
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
    login_memory_file = home / USER_MEMORY_RELATIVE_PATH
    for directory in _folder_lineage(files):
        for memory_file in MEMORY_RELATIVE_PATHS:
            candidate = directory / memory_file
            if candidate.is_file() and candidate != login_memory_file:
                raise Refusal(f"series folder under a memory file: {candidate}")


def _refuse_folder_inside_git_work_tree(files: SeriesFolder) -> None:
    """Refuse a series folder that or whose ancestor up to `/` holds a `.git` entry."""
    for directory in _folder_lineage(files):
        if (directory / GIT_ENTRY).exists():
            raise Refusal(f"series folder inside a git work tree: {directory}")


def _folder_lineage(files: SeriesFolder) -> tuple[Path, ...]:
    """Return the series folder and each ancestor up to `/`, nearest first."""
    return (files.root, *files.root.parents)


def _refuse_non_empty_folder(files: SeriesFolder) -> None:
    """Refuse a series folder that exists as a file or holds anything."""
    root = files.root
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise Refusal(f"series folder not empty: {root}")


def _series_record(instruction: Path, sources: Sequence[Path], reader_kind: ReaderKind, binding: Binding, now: datetime) -> dict[str, object]:
    """Return the `series.yaml` record of the live instruction, the sources, and the judges' binding."""
    return {
        "instruction": str(instruction),
        "sources": [str(source) for source in sources],
        "reader_kind": reader_kind,
        "binding": {"plugin": binding.plugin, "skill": binding.skill},
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
        write_file(files, source_snapshot_path(source.name), texts[source])


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
            strip_frontmatter(utf8_text(text, str(path)), str(path))
        except UnclosedFrontmatter as unclosed:
            raise Refusal(str(unclosed)) from None


def series_stop(files: SeriesFolder, reason: str) -> None:
    """Write `9-stop.yaml` as `unresolvable` with the reason and the kept revision ranked from every gated revision's outcome."""
    guard_series(files, STOP_COMMAND)
    outcomes = _gated_outcomes(files, SeriesRecords(files))
    _refuse_unless_latest_gated_revision_failed(outcomes)
    reads = [KEEP_RULE_INPUT, FROZEN_RECORD, *(outcome_path(revision) for revision in outcomes)]
    write_record(files, STOP_RECORD, {"stop": UNRESOLVABLE_STOP, "kept": kept_revision(outcomes), "reason": reason}, reads)


def series_keep(files: SeriesFolder, replace_file: Callable[[Path, bytes], None]) -> None:
    """Replace the live instruction file with the kept revision's instruction snapshot through `replace_file`, refusing a series not stopped or keeping nothing."""
    guard_series(files, KEEP_COMMAND)
    records = SeriesRecords(files)
    kept = _kept_revision(files, records)
    replace_file(records.series().instruction, files.read_bytes(f"{kept}/{INSTRUCTION_FILE}"))


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
    return {revision: records.outcome(revision) for revision in revision_ids(files) if files.holds(outcome_path(revision))}


FREEZE_PARTS = (DEMANDS_RECORD, TASKS_RECORD, CONDITIONS_RECORD, PLACEBO_SNAPSHOT, READER_RECORD)
FIRST_REVISION_STEPS = {
    "blinded": f"{FIRST_REVISION}/{ORIGINS_FILE}",
    "judged": f"{FIRST_REVISION}/{COLLECTED_FILE}",
    "detected": f"{FIRST_REVISION}/{DETECTORS_FILE}",
}
RECORD_PATTERN = "*.yaml"


def _refuse_unready_freeze(
    files: SeriesFolder, records: SeriesRecords, fingerprint_hash: str | None, read_external: Callable[[Path], bytes]
) -> tuple[ExpectedReply, ...]:
    """Return r1's expected replies, refusing freezing a series lacking a part or a gate key, failing a check, with r1 unmeasured, stale, or read by another reader build than `fingerprint_hash` (a command reader's fresh hash, None for an agent reader), or with a check it cannot measure."""
    _refuse_missing_parts(files)
    gate = records.complete_gate()
    demands_check(files)
    tasks_check(files, read_external)
    coverage_check(files, FIRST_REVISION)
    _refuse_uncalibrated(files)
    expected = _first_revision_replies(files, records, gate.repeats)
    refuse_missing_replies(files, expected)
    _refuse_unmeasured_first_revision(files)
    _refuse_stale_first_revision_records(files)
    if records.series().reader_kind == COMMAND_READER:
        refuse_other_reader_build(records, [reply.path for reply in expected], fingerprint_hash)
    _refuse_unmeasurable_checks(gate.checks, records)
    return expected


def _refuse_missing_parts(files: SeriesFolder) -> None:
    """Refuse the first of the user's parts 2 to 5 and the placebo snapshot that is absent."""
    missing = next((path for path in FREEZE_PARTS if not files.holds(path)), None)
    if missing is not None:
        raise Refusal(f"missing record: {missing}")


def _refuse_uncalibrated(files: SeriesFolder) -> None:
    """Refuse a series without an accepted judge calibration."""
    if not files.holds(CALIBRATION_RECORD):
        raise Refusal(f"no {CALIBRATION_RECORD}")


def _first_revision_replies(files: SeriesFolder, records: SeriesRecords, repeats: int) -> tuple[ExpectedReply, ...]:
    """Return the replies r1 expects at the gate's repeats."""
    sentence_count = len(split_sentences(files.read_bytes(FIRST_INSTRUCTION)))
    return expected_replies(FIRST_REVISION, records.tasks(), records.conditions(), repeats, sentence_count)


def _refuse_unmeasured_first_revision(files: SeriesFolder) -> None:
    """Refuse an r1 not yet blinded, judged, or detected, naming the first step whose record is absent."""
    for step, path in FIRST_REVISION_STEPS.items():
        if not files.holds(path):
            raise Refusal(f"{FIRST_REVISION} not {step}: no {path}")


def _refuse_stale_first_revision_records(files: SeriesFolder) -> None:
    """Refuse the first CLI record under r1 whose inputs no longer hash as written."""
    for path in _first_revision_command_records(files):
        load_record(files, path)


def _first_revision_command_records(files: SeriesFolder) -> list[str]:
    """Return the series path of every YAML record under r1 a CLI command wrote, in path order."""
    paths = sorted(path.relative_to(files.root).as_posix() for path in (files.root / FIRST_REVISION).rglob(RECORD_PATTERN))
    user_and_judge_records = (f"{FIRST_REVISION}/{COVERAGE_FILE}", f"{FIRST_REVISION}/{VERDICTS_FOLDER}/")
    return [path for path in paths if not path.startswith(user_and_judge_records)]


def _refuse_unmeasurable_checks(checks: Sequence[GateCheck], records: SeriesRecords) -> None:
    """Refuse a `drift` check in a series without conversations and an `instruction-near-source` check in a series without sources."""
    compared = {check.compares for check in checks}
    if DRIFT_COMPARES in compared and not records.tasks().conversations:
        raise Refusal(f"{DRIFT_COMPARES} check without conversations ({TASKS_RECORD})")
    if near_source_without_sources(checks, bool(records.series().sources)):
        raise Refusal(f"{NEAR_SOURCE_COMPARES} check without sources ({SERIES_RECORD})")


FREEZE_COMMAND = "series freeze"
EVERY_FILE_PATTERN = "**/*"
ANY_ATTEMPT_FOLDER = f"{CALIBRATION_FOLDER}/{ATTEMPT_FOLDER_PREFIX}*"
FROZEN_PART_PATTERNS = (
    SERIES_RECORD,
    f"{SOURCE_FOLDER}/*",
    DEMANDS_RECORD,
    TASKS_RECORD,
    CONDITIONS_RECORD,
    PLACEBO_SNAPSHOT,
    READER_RECORD,
    CALIBRATION_RECORD,
    ANCHORS_RECORD,
    f"{CALIBRATION_FOLDER}/*",
    GATE_RECORD,
    f"{FIRST_REVISION}/*",
)
USER_RECORD_PATTERNS = (
    DEMANDS_RECORD,
    TASKS_RECORD,
    CONDITIONS_RECORD,
    READER_RECORD,
    GATE_RECORD,
    f"{ANY_ATTEMPT_FOLDER}/{PLAN_FILE}",
    f"{ANY_ATTEMPT_FOLDER}/{REFERENCE_USER_FILE}",
    f"{FIRST_REVISION}/{COVERAGE_FILE}",
)


def series_freeze(
    files: SeriesFolder,
    fingerprint_hash: str | None,
    read_external: Callable[[Path], bytes],
    bootstrap_rng: BootstrapRng,
    tool_version: str,
    now: datetime,
) -> None:
    """Write `8-frozen.yaml`: the hash of every series file, r1's noise, a command reader's fresh fingerprint hash, the tool version, and the time, refusing a series not ready to freeze."""
    guard_series(files, FREEZE_COMMAND)
    records = SeriesRecords(files)
    expected = _refuse_unready_freeze(files, records, fingerprint_hash, read_external)
    gate = records.complete_gate()
    sealed_rows = measured_revision(records, FIRST_REVISION, gate.done_by).sealed_rows
    gate_demands = records.gate_demands()
    noise = measure_noise(sealed_rows, gate_demands, records.conditions().controls, gate.repeats, gate.level)
    refuse_unresolvable_gaps(gate.checks, noise, sealed_rows, gate_demands, bool(records.series().sources), bootstrap_rng())
    _refuse_unaffordable_series(files, records, gate, expected)
    hashed = _frozen_parts(files)
    frozen = {**_frozen_record(files, hashed, noise, tool_version, now), **_reader_build(records, fingerprint_hash)}
    write_record(files, FROZEN_RECORD, frozen, _freeze_reads(files, hashed))


def _reader_build(records: SeriesRecords, fingerprint_hash: str | None) -> dict[str, str | None]:
    """Return the fresh fingerprint hash a command reader's series records, nothing for an agent reader."""
    if records.series().reader_kind != COMMAND_READER:
        return {}
    return {"fingerprint_hash": fingerprint_hash}


def _freeze_reads(files: SeriesFolder, hashed: Sequence[str]) -> list[str]:
    """Return what the freeze reads: every hashed file whole, a user-written record by each top-level key."""
    return [read for path in hashed for read in (_user_record_keys(files, path) if _matches_any(path, USER_RECORD_PATTERNS) else [path])]


def _user_record_keys(files: SeriesFolder, path: str) -> list[str]:
    """Return a user-written record's reads, one `<path>#<key>` per top-level key."""
    return [f"{path}{KEY_SEPARATOR}{key}" for key in yaml.safe_load(files.read_bytes(path))]


def _refuse_unaffordable_series(files: SeriesFolder, records: SeriesRecords, gate: CompleteGate, first_revision_replies: Sequence[ExpectedReply]) -> None:
    """Refuse a budget ceiling below the series' cost predicted from r1's replies."""
    first_replies = [reply_cost(records.reply(reply.path)) for reply in first_revision_replies]
    try:
        refuse_unaffordable_freeze(stop_budget(gate.budget), first_replies, _series_shape(files, records, gate.repeats))
    except BudgetRefusal as unaffordable:
        raise Refusal(str(unaffordable)) from None


def _series_shape(files: SeriesFolder, records: SeriesRecords, repeats: int) -> SeriesShape:
    """Return the counts the cost prediction scales by: tasks, open tasks, conversation turns, repeats, and r1's omitted sentences."""
    tasks = records.tasks()
    return SeriesShape(
        task_count=len(tasks.tasks),
        open_task_count=sum(task.split == OPEN_SPLIT for task in tasks.tasks),
        conversation_turns=sum(len(conversation.turns) for conversation in tasks.conversations),
        repeats=repeats,
        omission_sentences=len(omission_conditions(records.conditions().omissions, len(split_sentences(files.read_bytes(FIRST_INSTRUCTION))))),
    )


def _frozen_parts(files: SeriesFolder) -> list[str]:
    """Return the series path of every file the freeze hashes, each matching a part of the series, in path order."""
    paths = files.paths(EVERY_FILE_PATTERN)
    return [path for path in paths if _matches_any(path, FROZEN_PART_PATTERNS)]


def _matches_any(path: str, patterns: Sequence[str]) -> bool:
    """Tell whether the series path matches a pattern, `*` spanning folders."""
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def _frozen_record(files: SeriesFolder, hashed: Sequence[str], noise: Noise, tool_version: str, now: datetime) -> dict[str, object]:
    """Return `8-frozen.yaml`: each hashed path's hash, the noise, the tool version, and the time."""
    return {
        "hashes": {path: sha256(files.read_bytes(path)) for path in hashed},
        "noise": noise,
        "tool_version": tool_version,
        "frozen_at": now.isoformat(),
    }


STATUS_PARTS = (
    SERIES_RECORD,
    DEMANDS_RECORD,
    TASKS_RECORD,
    CONDITIONS_RECORD,
    PLACEBO_SNAPSHOT,
    READER_RECORD,
    WORKING_BRIEF,
    CALIBRATION_RECORD,
    ANCHORS_RECORD,
    GATE_RECORD,
    FROZEN_RECORD,
    STOP_RECORD,
)
PARTS_KEY = "parts"
FROZEN_KEY = "frozen"
REVISIONS_KEY = "revisions"
COST_KEY = "cost"
CALIBRATION_KEY = "calibration"
AWAITING_KEY = "packets_awaiting_judging"
NOISE_KEY = "noise"
LEAST_REPEATS_KEY = "least_repeats"
STOP_KEY = "stop"
SPENT_KEY = "spent"
BUDGET_KEY = "budget"
REPLIES_KEY = "replies"
INPUT_TOKENS_KEY = "input_tokens"
OUTPUT_TOKENS_KEY = "output_tokens"
SECONDS_KEY = "seconds"
ATTEMPTS_KEY = "attempts"
ATTEMPT_KEY = "attempt"
ACCEPTED_KEY = "accepted"
SCALE_KEY = "scale"
STOP_STANDING_KEYS = ("stop", "kept", "reason")
STATUS_DEFAULT_LEVEL = 0.95
UNGATED_STANDING = {"outcome": None, "changed_from_parent": None, "instruction_breaches": None, "completion_passed": None, "words": None}


def series_status(files: SeriesFolder) -> str:
    """Return the series' standing as YAML, writing nothing: parts present, frozen or not, revision outcomes, cost against budget, calibration, packets awaiting judging, r1's noise, least repeats, and the stop."""
    guard_series(files, STATUS_COMMAND)
    records = SeriesRecords(files)
    noise = _first_revision_noise(files, records)
    standing = {
        PARTS_KEY: [part for part in STATUS_PARTS if files.holds(part)],
        FROZEN_KEY: files.holds(FROZEN_RECORD),
        REVISIONS_KEY: {revision: _revision_standing(files, records, revision) for revision in revision_ids(files)},
        COST_KEY: _cost_standing(files, records),
        CALIBRATION_KEY: _calibration_standing(files, records),
        AWAITING_KEY: _packets_awaiting_judging(files, records),
        NOISE_KEY: noise,
        LEAST_REPEATS_KEY: _least_repeats_per_check(files, records, noise),
        STOP_KEY: _stop_standing(files, records),
    }
    return yaml.safe_dump(standing, sort_keys=False)


def _revision_standing(files: SeriesFolder, records: SeriesRecords, revision: str) -> dict[str, object]:
    """Return a revision's outcome, change from its parent, and keep ranks, each null while the revision is ungated."""
    if not files.holds(outcome_path(revision)):
        return dict(UNGATED_STANDING)
    outcome = records.outcome(revision)
    return {key: outcome.get(key) for key in UNGATED_STANDING}


def _cost_standing(files: SeriesFolder, records: SeriesRecords) -> dict[str, object]:
    """Return the cost every gated revision's asks spent and the gate's budget, null while the gate holds none."""
    costs = [outcome[COST_KEY] for outcome in _gated_outcomes(files, records).values()]
    spent = {
        REPLIES_KEY: sum(cost[REPLIES_KEY] for cost in costs),
        INPUT_TOKENS_KEY: sum_unless_null([cost[INPUT_TOKENS_KEY] for cost in costs]),
        OUTPUT_TOKENS_KEY: sum_unless_null([cost[OUTPUT_TOKENS_KEY] for cost in costs]),
        SECONDS_KEY: sum(cost[SECONDS_KEY] for cost in costs),
    }
    return {SPENT_KEY: spent, BUDGET_KEY: _written_budget(files, records)}


def _written_budget(files: SeriesFolder, records: SeriesRecords) -> str | dict[str, object] | None:
    """Return the gate's budget as written, `none` or its unit and ceiling, or None while the gate or its budget is unwritten."""
    budget = records.gate().budget if files.holds(GATE_RECORD) else None
    if isinstance(budget, Budget):
        return {"unit": budget.unit, "ceiling": budget.ceiling}
    return budget


def _calibration_standing(files: SeriesFolder, records: SeriesRecords) -> dict[str, object]:
    """Return each calibration attempt with its scale, null until rated, and the accepted attempt, null until one is accepted."""
    attempts = [{ATTEMPT_KEY: attempt, SCALE_KEY: _attempt_scale(files, records, attempt)} for attempt in _attempt_numbers(files)]
    accepted = records.calibration()[ATTEMPT_KEY] if files.holds(CALIBRATION_RECORD) else None
    return {ATTEMPTS_KEY: attempts, ACCEPTED_KEY: accepted}


def _attempt_numbers(files: SeriesFolder) -> Iterator[int]:
    """Return the numbers of the calibration attempts, in order, up to the first without a plan."""
    numbers = itertools.count(FIRST_ATTEMPT)
    return itertools.takewhile(lambda attempt: files.holds(f"{attempt_folder(attempt)}/{PLAN_FILE}"), numbers)


def _attempt_scale(files: SeriesFolder, records: SeriesRecords, attempt: int) -> float | None:
    """Return the scale an attempt's agreement reports, None while the attempt is unrated or its reference mean is zero."""
    if not files.holds(f"{attempt_folder(attempt)}/{AGREEMENT_FILE}"):
        return None
    return records.agreement(attempt)[SCALE_KEY]


def _packets_awaiting_judging(files: SeriesFolder, records: SeriesRecords) -> dict[str, list[str]]:
    """Return, per blinded revision without a collection, its packets in order, the collection existing once every packet is accepted."""
    blinded = [revision for revision in revision_ids(files) if files.holds(f"{revision}/{ORIGINS_FILE}")]
    return {revision: sorted(records.origins(revision)["packets"]) for revision in blinded if not files.holds(f"{revision}/{COLLECTED_FILE}")}


def _first_revision_noise(files: SeriesFolder, records: SeriesRecords) -> Noise | None:
    """Return r1's noise from its sealed rows, None until r1 is blinded, judged, and detected and the gate holds `repeats` and `done_by`."""
    measured = all(files.holds(f"{FIRST_REVISION}/{step}") for step in (ORIGINS_FILE, COLLECTED_FILE, DETECTORS_FILE))
    gate = records.gate() if measured and files.holds(GATE_RECORD) else None
    if gate is None or gate.repeats is None or gate.done_by is None:
        return None
    sealed_rows = measured_revision(records, FIRST_REVISION, gate.done_by).sealed_rows
    level = STATUS_DEFAULT_LEVEL if gate.level is None else gate.level
    return measure_noise(sealed_rows, records.gate_demands(), records.conditions().controls, gate.repeats, level)


def _least_repeats_per_check(files: SeriesFolder, records: SeriesRecords, noise: Noise | None) -> dict[str, int | None]:
    """Return, per gate check, the fewest repeats resolving its gap, empty until r1's noise and the gate's checks exist."""
    checks = records.gate().checks if files.holds(GATE_RECORD) else None
    if noise is None or checks is None:
        return {}
    return {check.compares: least_repeats(check, noise) for check in checks}


def _stop_standing(files: SeriesFolder, records: SeriesRecords) -> dict[str, object] | None:
    """Return the stop's kind, kept revision, and reason, or None while the series runs."""
    if not files.holds(STOP_RECORD):
        return None
    stop = records.stop()
    return {key: stop.get(key) for key in STOP_STANDING_KEYS}
