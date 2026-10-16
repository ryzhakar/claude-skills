"""Series records: their shapes, files written once, CLI records whose inputs must still hash as written, and the guard of every command but `series new` against a folder that is no series, a stopped series, a changed frozen part, and a broken revision chain."""

import functools
import hashlib
import itertools
import math
import os
import re
import tempfile
from collections.abc import Callable, Container, Iterable, Iterator, Mapping
from collections.abc import Set as AbstractSet
from dataclasses import dataclass, fields
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, Literal, NoReturn, TypeVar, get_args

import yaml

KEY_SEPARATOR = "#"
STATUS_COMMAND = "series status"
KEEP_COMMAND = "series keep"
STOPPED_SERIES_COMMANDS = (STATUS_COMMAND, KEEP_COMMAND)
INPUTS_KEY = "inputs"

SERIES_RECORD = "series.yaml"
DEMANDS_RECORD = "2-demands.yaml"
DEMANDS_INPUT = f"{DEMANDS_RECORD}{KEY_SEPARATOR}demands"
TASKS_RECORD = "3-tasks.yaml"
CONDITIONS_RECORD = "4-conditions.yaml"
READER_RECORD = "5-reader.yaml"
GATE_RECORD = "7-gate.yaml"
FROZEN_RECORD = "8-frozen.yaml"
STOP_RECORD = "9-stop.yaml"
SOURCE_FOLDER = "1-source"
PLACEBO_SNAPSHOT = "4-placebo-source.md"
AGENTS_FOLDER = ".claude/agents"
JUDGE_FOLDER = "6-judge"
WORKING_BRIEF = f"{JUDGE_FOLDER}/brief.md"
CALIBRATION_RECORD = f"{JUDGE_FOLDER}/calibration.yaml"
ANCHORS_RECORD = f"{JUDGE_FOLDER}/anchors.yaml"
CALIBRATION_FOLDER = f"{JUDGE_FOLDER}/calibration"
ATTEMPT_FOLDER_PREFIX = "attempt-"
FIRST_ATTEMPT = 1
PLAN_FILE = "plan.yaml"
BRIEF_SNAPSHOT_FILE = "brief.md"
SAMPLE_FILE = "sample.md"
ATTEMPT_ORIGINS_FILE = "origins.yaml"
AGREEMENT_FILE = "agreement.yaml"
REFERENCE_PREFIX = "reference-"
REVISION_PREFIX = "r"
FIRST_REVISION_NUMBER = 1
FIRST_REVISION = f"{REVISION_PREFIX}{FIRST_REVISION_NUMBER}"
HYPOTHESIS_FILE = "1-hypothesis.yaml"
INSTRUCTION_FILE = "2-instruction.md"
REVISION_RECORD_FILE = "2-revision.yaml"
COVERAGE_FILE = "3-coverage.yaml"
CONDITIONS_FOLDER = "4-conditions"
REPLIES_FOLDER = "5-replies"
REPEAT_PREFIX = "repeat-"
TURN_PREFIX = "turn-"
PACKETS_FOLDER = "6-packets"
ORIGINS_FILE = "6-origins.yaml"
COLLECTED_FILE = "7-collected.yaml"
DETECTORS_FILE = "7-detectors.yaml"
VERDICTS_FOLDER = "7-verdicts"
SCORES_FILE = "8-scores.yaml"
OUTCOME_FILE = "9-outcome.yaml"


class Refusal(ValueError):
    """A refusal of a command or a record, carrying the one-line message the user reads."""


@dataclass(frozen=True)
class SeriesFolder:
    """The series folder on disk at `root`."""

    root: Path

    def read_bytes(self, path: str) -> bytes:
        """Return the bytes at `path`, raising FileNotFoundError when it is absent."""
        return (self.root / path).read_bytes()

    def holds(self, path: str) -> bool:
        """Tell whether a file exists at `path`."""
        return (self.root / path).is_file()

    def write_once(self, path: str, content: bytes) -> None:
        """Write `content` whole to `path`, raising FileExistsError when it exists."""
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = _stage_beside(target, content)
        try:
            os.link(staged, target)
        finally:
            staged.unlink()


def write_file(files: SeriesFolder, path: str, content: bytes) -> None:
    """Write the series file at `path` whole and once, refusing when it exists."""
    try:
        files.write_once(path, content)
    except FileExistsError:
        raise Refusal(f"already written: {path}") from None


def read_series_file(files: SeriesFolder, path: str) -> bytes:
    """Return the bytes of the series file at `path`, refusing it absent."""
    try:
        return files.read_bytes(path)
    except FileNotFoundError:
        raise Refusal(f"missing file: {path}") from None


def utf8_text(content: bytes, label: str) -> str:
    """Return the UTF-8 text of the bytes, refusing them as not UTF-8 under `label`."""
    try:
        return content.decode()
    except UnicodeDecodeError:
        raise Refusal(f"not UTF-8: {label}") from None


def series_paths(files: SeriesFolder, pattern: str) -> list[str]:
    """Return the series path of every file the glob pattern matches, in path order."""
    return sorted(path.relative_to(files.root).as_posix() for path in files.root.glob(pattern) if path.is_file())


def write_record(files: SeriesFolder, path: str, record: Mapping[str, Any], reads: Iterable[str]) -> None:
    """Write a YAML record whose `inputs` map each read, a series path or `<path>#<key>`, to its sha256, refusing a record carrying its own."""
    if INPUTS_KEY in record:
        raise Refusal(f"record {path} carries inputs; inputs come from its reads")
    write_file(files, path, dump_canonical_yaml({**record, INPUTS_KEY: _hash_inputs(files, reads)}))


def load_record(files: SeriesFolder, path: str) -> dict[str, Any]:
    """Load the CLI record at `path`, refusing when an input no longer hashes as written."""
    record = _parse_record(_read_record(files, path), path)
    written_hashes = record[INPUTS_KEY]
    current_hashes = _hash_inputs(files, written_hashes)
    for entry, written_hash in written_hashes.items():
        if current_hashes[entry] != written_hash:
            raise Refusal(f"stale: {path} (input {entry} changed)")
    return record


def _read_record(files: SeriesFolder, path: str) -> bytes:
    """Read the CLI record at `path`, refusing when it is absent."""
    try:
        return files.read_bytes(path)
    except FileNotFoundError:
        raise Refusal(f"missing record: {path}") from None


def _parse_record(content: bytes, path: str) -> dict[str, Any]:
    """Parse a CLI record, refusing it as malformed unless it is a YAML mapping holding an `inputs` mapping of strings to strings."""
    record = _parse_yaml(content, path)
    if not isinstance(record, dict) or not _is_text_map(record.get(INPUTS_KEY)):
        raise Refusal(f"malformed record: {path} (no inputs map)")
    return record


def _parse_yaml(content: bytes, path: str) -> Any:
    """Parse the YAML record at `path`, refusing it as malformed when it is not YAML."""
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError:
        raise Refusal(f"malformed record: {path} (not YAML)") from None


def _is_text_map(value: Any) -> bool:
    """Tell whether the value is a mapping from strings to strings."""
    return isinstance(value, dict) and all(isinstance(item, str) for pair in value.items() for item in pair)


def _hash_inputs(files: SeriesFolder, reads: Iterable[str]) -> dict[str, str]:
    """Map each read to the sha256 of what it names, reading and parsing each named file once."""
    read_file = functools.cache(lambda file_path: _read_input(files, file_path))
    parse_file = functools.cache(lambda file_path: _parse_input(read_file(file_path), file_path))
    return {entry: _hash_input(read_file, parse_file, entry) for entry in reads}


def _hash_input(read_file: Callable[[str], bytes], parse_file: Callable[[str], Any], entry: str) -> str:
    """Hash a whole series file, or for `<path>#<key>` that key's value dumped as canonical YAML."""
    file_path, separator, key = entry.partition(KEY_SEPARATOR)
    if not separator:
        return sha256(read_file(file_path))
    return sha256(dump_canonical_yaml(_read_top_level_value(parse_file(file_path), entry, key)))


def _read_top_level_value(document: Any, entry: str, key: str) -> Any:
    """Return the value of a top-level key of a parsed YAML document, refusing `entry` as missing when the key is absent."""
    if not isinstance(document, dict) or key not in document:
        raise Refusal(f"missing input: {entry}")
    return document[key]


def _parse_input(content: bytes, path: str) -> Any:
    """Parse the YAML series input at `path`, refusing it as malformed when it is not YAML."""
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError:
        raise Refusal(f"malformed input: {path}") from None


def _read_input(files: SeriesFolder, path: str) -> bytes:
    """Read the series input at `path`, refusing when it is absent."""
    try:
        return files.read_bytes(path)
    except FileNotFoundError:
        raise Refusal(f"missing input: {path}") from None


def _stage_beside(target: Path, content: bytes) -> Path:
    """Write the content to a fresh file in the target's folder and return its path."""
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as staged:
        staged.write(content)
    return Path(staged.name)


def dump_canonical_yaml(value: Any) -> bytes:
    """Dump a value as YAML with sorted keys in block style."""
    return yaml.safe_dump(value, sort_keys=True, default_flow_style=False, allow_unicode=True).encode()


def sha256(content: bytes) -> str:
    """Return the lowercase sha256 hex digest of the bytes."""
    return hashlib.sha256(content).hexdigest()


Record = Mapping[str, Any]
Check = Callable[[Any, str], None]

REVISION_ID_PATTERN = r"r[1-9][0-9]*"
IDENTIFIER_PATTERN = r"[a-z0-9][a-z0-9-]*"
AGENT_MODEL_ID_PATTERN = r"claude-[a-z0-9]+(-[a-z0-9]+)+"
Control = Literal["empty", "aim", "placebo", "source"]
EMPTY_CONTROL, AIM_CONTROL, PLACEBO_CONTROL, SOURCE_CONTROL = get_args(Control)
CONTROLS_WITHOUT_SOURCES = (EMPTY_CONTROL, AIM_CONTROL, PLACEBO_CONTROL)
Compares = Literal["instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "instruction-near-source", "completion", "drift"]
COMPARES = get_args(Compares)
VS_EMPTY_COMPARES, VS_AIM_COMPARES, VS_PLACEBO_COMPARES, NEAR_SOURCE_COMPARES, COMPLETION_COMPARES, DRIFT_COMPARES = COMPARES
VS_COMPARES = {EMPTY_CONTROL: VS_EMPTY_COMPARES, AIM_CONTROL: VS_AIM_COMPARES, PLACEBO_CONTROL: VS_PLACEBO_COMPARES}
REQUIRED_COMPARES = (*VS_COMPARES.values(), COMPLETION_COMPARES)
OVERREACH_TARGET = "overreach"
HASH_PATTERN = r"[0-9a-f]{64}"
TOTAL_KEY = "total"
INTERVAL_LENGTH = 2
FEWEST_ANCHORS_PER_PACKET = 3
TOTAL_REFUSAL = "breach totals derive from breaches maps and are never stored"

ReaderKind = Literal["agent", "command"]
AGENT_READER, COMMAND_READER = get_args(ReaderKind)
USER_RATER = "user"
AGENT_RATER = "agent"
USER_RATERS = [USER_RATER]
AGENT_RATERS = [AGENT_RATER, AGENT_RATER]
REFERENCE_USER_FILE = f"{REFERENCE_PREFIX}{USER_RATER}.yaml"
PERMITTED_RATER_SETS = (tuple(USER_RATERS), tuple(AGENT_RATERS))
OPEN_SPLIT = "open"
SEALED_SPLIT = "sealed"

REWRITE_ACTION = "rewrite"
ADD_ACTION = "add"
DELETE_ACTION = "delete"
MOVE_ACTION = "move"
MOVE_TARGET_KEY = "to"

PASSED_STOP = "passed"
NO_EFFECT_STOP = "no-effect"
CAPPED_STOP = "capped"
UNRESOLVABLE_STOP = "unresolvable"
BUDGET_REASON = "budget"

ANSWER_KIND = "answer"
PROBE_KIND = "probe"
REFUSAL_KIND = "refusal"
BLANK_KIND = "blank"

PASS_OUTCOME = "pass"
FAIL_OUTCOME = "fail"

ANCHOR_KEY = "anchor"
SPENT_INPUT_TOKENS_KEY = "spent_input_tokens"
REPLY_INPUT_TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
REPLY_COST_KEYS = (*REPLY_INPUT_TOKEN_KEYS, "output_tokens", SPENT_INPUT_TOKENS_KEY)
PARENT_OUTCOME_KEYS = ("changed_from_parent", "parent_comparison")
LINEAGE_KEYS = ("parent", "parent_record", "change")
AGENT_ONLY_REPLY_KEYS = ("transcript", "transcript_hash")
COMMAND_ONLY_REPLY_KEYS = ("fingerprint_hash",)


class RecordKind(StrEnum):
    """Names each record shape that parse_record accepts."""

    STOP = "stop"
    REVISION = "revision"
    FROZEN = "frozen"
    REPLY = "reply"
    ORIGINS = "origins"
    VERDICT = "verdict"
    DETECTORS = "detectors"
    COLLECTED = "collected"
    SCORES = "scores"
    OUTCOME = "outcome"
    AGREEMENT = "agreement"
    CALIBRATION = "calibration"
    ANCHORS = "anchors"


def _refuse(path: str, reason: str) -> NoReturn:
    """Raise a Refusal naming the path and the reason."""
    raise Refusal(f"{path}: {reason}")


def _matching(pattern: str, description: str) -> Check:
    """Return a check that accepts strings fully matching the pattern."""

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not a string fully matching the pattern."""
        if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
            _refuse(path, f"expected {description}, got {value!r}")

    return check


def _enum(*allowed: str) -> Check:
    """Return a check that accepts only the allowed strings."""

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not one of the allowed strings."""
        if not isinstance(value, str) or value not in allowed:
            _refuse(path, f"expected one of {list(allowed)}, got {value!r}")

    return check


def _nullable(inner: Check) -> Check:
    """Return a check that accepts null or whatever the inner check accepts."""

    def check(value: Any, path: str) -> None:
        """Pass null and hand any other value to the inner check."""
        if value is not None:
            inner(value, path)

    return check


def _text(value: Any, path: str) -> None:
    """Refuse a value that is not a non-empty string."""
    if not isinstance(value, str) or not value:
        _refuse(path, f"expected non-empty string, got {value!r}")


def _map_of(key_check: Check, value_check: Check) -> Check:
    """Return a check that accepts a map whose keys and values pass the given checks."""

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not a map of checked keys and values."""
        if not isinstance(value, Mapping):
            _refuse(path, f"expected a map, got {value!r}")
        for key, item in value.items():
            key_check(key, f"{path}.{key}")
            value_check(item, f"{path}.{key}")

    return check


def _mapping(
    required: Mapping[str, Check],
    optional: Mapping[str, Check] | None = None,
    rule: Check | None = None,
) -> Check:
    """Return a check that accepts a closed map with the given keys and a final cross-key rule."""
    optional = optional or {}

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not a closed map of checked keys obeying the rule."""
        if not isinstance(value, Mapping):
            _refuse(path, f"expected a map, got {value!r}")
        for key in value:
            if key not in required and key not in optional:
                _refuse(f"{path}.{key}", TOTAL_REFUSAL if TOTAL_KEY in str(key) else "unknown key")
        for key, key_check in required.items():
            if key not in value:
                _refuse(f"{path}.{key}", "missing key")
            key_check(value[key], f"{path}.{key}")
        for key, key_check in optional.items():
            if key in value:
                key_check(value[key], f"{path}.{key}")
        if rule is not None:
            rule(value, path)

    return check


def _string(value: Any, path: str) -> None:
    """Refuse a value that is not a string."""
    if not isinstance(value, str):
        _refuse(path, f"expected string, got {value!r}")


def _integer(minimum: int) -> Check:
    """Return a check that accepts integers at or above the minimum."""

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not an integer at or above the minimum."""
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            _refuse(path, f"expected integer >= {minimum}, got {value!r}")

    return check


def _number(description: str, accepts: Callable[[float], bool]) -> Check:
    """Return a check that accepts numbers the predicate accepts."""

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not a number the predicate accepts."""
        is_number = isinstance(value, int | float) and not isinstance(value, bool)
        if not is_number or not accepts(value):
            _refuse(path, f"expected number {description}, got {value!r}")

    return check


def _timestamp(value: Any, path: str) -> None:
    """Refuse a value that is not an ISO 8601 timestamp with an offset."""
    if isinstance(value, datetime):
        parsed = value
    else:
        try:
            parsed = datetime.fromisoformat(value)
        except (TypeError, ValueError):
            _refuse(path, f"expected ISO 8601 timestamp with offset, got {value!r}")
    if parsed.tzinfo is None:
        _refuse(path, f"expected ISO 8601 timestamp with offset, got {value!r}")


_ANY_NUMBER = _number("", lambda value: True)
_NON_NEGATIVE = _number(">= 0", lambda value: value >= 0)
_POSITIVE = _number("> 0", lambda value: value > 0)
_LEVEL = _number("in (0, 1)", lambda value: 0 < value < 1)
_IDENTIFIER = _matching(IDENTIFIER_PATTERN, "an id")
_HASH = _matching(HASH_PATTERN, "lowercase sha256 hex")
_REVISION_ID = _matching(REVISION_ID_PATTERN, "a revision id")
_INPUTS = _map_of(_text, _HASH)
_POSITION = _integer(1)
_COMPARES = _enum(*COMPARES)
_BY_CONDITION = _map_of(_IDENTIFIER, _nullable(_NON_NEGATIVE))
_NULLABLE_COUNT = _nullable(_integer(0))
_SPLIT = _enum(OPEN_SPLIT, SEALED_SPLIT)
_READER_KIND = _enum(AGENT_READER, COMMAND_READER)
_VERDICT_KIND = _enum(ANSWER_KIND, PROBE_KIND, REFUSAL_KIND, BLANK_KIND)
_ABSOLUTE_PATH = _matching(r"/.+", "an absolute path")


def _reply_cost_rule(cost: Record, path: str) -> None:
    """Refuse a cost whose fields mix null and integers or whose spent total is not the input sum."""
    if len({value is None for value in cost.values()}) != 1:
        _refuse(path, "all five fields are integers or all are null")
    if cost[SPENT_INPUT_TOKENS_KEY] is None:
        return
    if cost[SPENT_INPUT_TOKENS_KEY] != sum(cost[key] for key in REPLY_INPUT_TOKEN_KEYS):
        _refuse(f"{path}.{SPENT_INPUT_TOKENS_KEY}", "the sum of the three input fields")


_REPLY_COST = _mapping({key: _NULLABLE_COUNT for key in REPLY_COST_KEYS}, rule=_reply_cost_rule)


def _reply_reader_kind_rule(reply: Record, path: str) -> None:
    """Refuse a reply whose transcript, fingerprint, or cost fields disagree with its reader kind."""
    is_agent = reply["reader_kind"] == AGENT_READER
    for key in AGENT_ONLY_REPLY_KEYS:
        if (key in reply) != is_agent:
            _refuse(f"{path}.{key}", f"present iff reader_kind is {AGENT_READER}")
    for key in COMMAND_ONLY_REPLY_KEYS:
        if (key in reply) == is_agent:
            _refuse(f"{path}.{key}", f"present iff reader_kind is {COMMAND_READER}")
    if not is_agent and reply["cost"][SPENT_INPUT_TOKENS_KEY] is not None:
        _refuse(f"{path}.cost", f"null for {COMMAND_READER} readers")


_NOISE = _mapping(
    {
        "repeats": _integer(2),
        "level": _LEVEL,
        "z": _POSITIVE,
        "sigma": _mapping(
            {
                "breaches": _BY_CONDITION,
                "done": _BY_CONDITION,
                "drift": _BY_CONDITION,
                "demands": _map_of(_IDENTIFIER, _BY_CONDITION),
            }
        ),
        "checks": _map_of(_COMPARES, _nullable(_NON_NEGATIVE)),
        "demands": _map_of(_IDENTIFIER, _nullable(_NON_NEGATIVE)),
        "done_change": _nullable(_NON_NEGATIVE),
    }
)


def _change_rule(change: Record, path: str) -> None:
    """Refuse a change whose target and texts disagree with its action."""
    action = change["action"]
    if (action == MOVE_ACTION) != (MOVE_TARGET_KEY in change):
        _refuse(f"{path}.{MOVE_TARGET_KEY}", f"present iff action is {MOVE_ACTION}")
    if action == ADD_ACTION and change["old"] != "":
        _refuse(f"{path}.old", f"empty on {ADD_ACTION}")
    if action == DELETE_ACTION and change["new"] != "":
        _refuse(f"{path}.new", f"empty on {DELETE_ACTION}")
    if action == MOVE_ACTION and change["old"] != change["new"]:
        _refuse(f"{path}.new", f"the moved text on {MOVE_ACTION}, equal to old")


_CHANGE = _mapping(
    {
        "action": _enum(REWRITE_ACTION, ADD_ACTION, DELETE_ACTION, MOVE_ACTION),
        "sentence": _POSITION,
        "old": _string,
        "new": _string,
    },
    {MOVE_TARGET_KEY: _POSITION},
    _change_rule,
)


def _revision_lineage_rule(record: Record, path: str) -> None:
    """Refuse a revision whose lineage fields are null unless it is the first."""
    for key in LINEAGE_KEYS:
        if (record[key] is None) != (record["number"] == FIRST_REVISION_NUMBER):
            _refuse(f"{path}.{key}", f"null iff number is {FIRST_REVISION_NUMBER}")


def _stop_reason_rule(record: Record, path: str) -> None:
    """Refuse a stop whose reason is absent, present, or worded against its stop kind."""
    stop = record["stop"]
    reason = record.get("reason")
    if stop == UNRESOLVABLE_STOP:
        if reason is None:
            _refuse(f"{path}.reason", f"required for {UNRESOLVABLE_STOP}")
    elif stop == CAPPED_STOP:
        if reason is not None and reason != BUDGET_REASON:
            _refuse(f"{path}.reason", f"only {BUDGET_REASON!r} allowed for {CAPPED_STOP}")
    elif reason is not None:
        _refuse(f"{path}.reason", f"not allowed for {stop}")


_NULLABLE_REVISION_ID = _nullable(_REVISION_ID)
_REPLY_ORIGIN = _mapping(
    {
        "packet": _IDENTIFIER,
        "condition": _IDENTIFIER,
        "task": _IDENTIFIER,
        "split": _SPLIT,
        "repeat": _POSITION,
        "borrowed_from": _NULLABLE_REVISION_ID,
    },
    {"turn": _POSITION},
)
_ANCHOR_ORIGIN = _mapping({"packet": _IDENTIFIER, ANCHOR_KEY: _IDENTIFIER})


def _origin(value: Any, path: str) -> None:
    """Refuse an origin that is neither a reply origin nor an anchor origin."""
    is_anchor = isinstance(value, Mapping) and ANCHOR_KEY in value
    (_ANCHOR_ORIGIN if is_anchor else _REPLY_ORIGIN)(value, path)


def _list_of(item_check: Check, unique_by: str | None = None, non_empty: bool = False) -> Check:
    """Return a check that accepts a list of checked items, optionally non-empty and unique by a key."""

    def check(value: Any, path: str) -> None:
        """Refuse a value that is not a list of checked items meeting the size and uniqueness rules."""
        if not isinstance(value, list) or (non_empty and not value):
            _refuse(path, f"expected {'a non-empty' if non_empty else 'a'} list, got {value!r}")
        for index, item in enumerate(value):
            item_check(item, f"{path}[{index}]")
        if unique_by is not None:
            seen = [item[unique_by] for item in value]
            if len(set(seen)) != len(seen):
                _refuse(path, f"duplicate {unique_by}")

    return check


def _boolean_or_null(value: Any, path: str) -> None:
    """Refuse a value that is neither a boolean nor null."""
    if value is not None and not isinstance(value, bool):
        _refuse(path, f"expected true, false, or null, got {value!r}")


def _breach_demand_id(value: Any, path: str) -> None:
    """Refuse a breach map key that is a stored total or not an id."""
    if value == TOTAL_KEY:
        _refuse(path, TOTAL_REFUSAL)
    _IDENTIFIER(value, path)


_BREACHES = _map_of(_breach_demand_id, _integer(0))
_VERDICT_ENTRY = _mapping(
    {
        "id": _IDENTIFIER,
        "breaches": _BREACHES,
        "done": _boolean_or_null,
        "kind": _VERDICT_KIND,
        "notes": _string,
    }
)
_DETECTOR_ENTRY = _mapping(
    {"id": _IDENTIFIER, "breaches": _BREACHES, "done_by_answer_key": _boolean_or_null}
)
_AGENT_MODEL = _matching(AGENT_MODEL_ID_PATTERN, "a full claude model id")
_COLLECTED_PACKET = _mapping(
    {
        "accepted": _POSITION,
        "judge_model": _AGENT_MODEL,
        "transcript": _ABSOLUTE_PATH,
        "transcript_hash": _HASH,
        "anchors": _mapping(
            {
                "breach_difference": _map_of(_breach_demand_id, _ANY_NUMBER),
                "done_agreement": _ANY_NUMBER,
            }
        ),
    }
)


def _boolean(value: Any, path: str) -> None:
    """Refuse a value that is not a boolean."""
    if not isinstance(value, bool):
        _refuse(path, f"expected true or false, got {value!r}")


def _interval(value: Any, path: str) -> None:
    """Refuse a value that is not a two-number list with low at most high."""
    _list_of(_ANY_NUMBER)(value, path)
    if len(value) != INTERVAL_LENGTH or value[0] > value[1]:
        _refuse(path, f"expected [low, high] with low <= high, got {value!r}")


def _outcome_parent_fields_rule(outcome: Record, path: str) -> None:
    """Refuse an outcome carrying only one of the two parent fields."""
    present = [key for key in PARENT_OUTCOME_KEYS if key in outcome]
    if present and len(present) != len(PARENT_OUTCOME_KEYS):
        missing = next(key for key in PARENT_OUTCOME_KEYS if key not in outcome)
        _refuse(f"{path}.{missing}", "present together with its pair")


_UNIT_CLOSED = _number("in [0, 1]", lambda value: 0 <= value <= 1)
_ROW = _mapping(
    {
        "id": _IDENTIFIER,
        "condition": _IDENTIFIER,
        "task": _IDENTIFIER,
        "repeat": _POSITION,
        "turn": _nullable(_POSITION),
        "borrowed_from": _NULLABLE_REVISION_ID,
        "breaches": _BREACHES,
        "kind": _VERDICT_KIND,
        "done_by_answer_key": _boolean_or_null,
        "done_by_judge": _boolean_or_null,
        "done": _boolean_or_null,
    }
)
_CONDITION_SCORES = _mapping(
    {
        "breaches_per_reply": _NON_NEGATIVE,
        "demands": _map_of(_IDENTIFIER, _NON_NEGATIVE),
        "done_rate": _nullable(_UNIT_CLOSED),
        "kinds": _map_of(_VERDICT_KIND, _integer(0)),
    }
)
_COMPARISON = _mapping(
    {"mean_difference": _nullable(_ANY_NUMBER), "interval": _nullable(_interval), "units": _integer(0)}
)
_DRIFT = _mapping({"slope": _ANY_NUMBER, "interval": _interval})
_OUTCOME_CHECK = _mapping(
    {
        "compares": _COMPARES,
        "gap": _POSITIVE,
        "mean_difference": _nullable(_ANY_NUMBER),
        "interval": _nullable(_interval),
        "pass": _boolean,
    }
)
_PARENT_COMPARISON = _mapping(
    {"target": _IDENTIFIER, "mean_difference": _nullable(_ANY_NUMBER), "interval": _nullable(_interval)}
)
_OUTCOME_COST = _mapping(
    {
        "replies": _integer(0),
        "input_tokens": _NULLABLE_COUNT,
        "output_tokens": _NULLABLE_COUNT,
        "seconds": _NON_NEGATIVE,
    }
)


def _raters(value: Any, path: str) -> None:
    """Refuse a rater list that is neither the user alone nor two agents."""
    if not isinstance(value, list) or tuple(value) not in PERMITTED_RATER_SETS:
        _refuse(path, f"expected one of {PERMITTED_RATER_SETS}, got {value!r}")


_AGREEMENT = _mapping(
    {
        "inputs": _INPUTS,
        "demands": _map_of(
            _IDENTIFIER,
            _mapping({"breach_difference": _ANY_NUMBER, "self_difference": _ANY_NUMBER}),
        ),
        "done_agreement": _ANY_NUMBER,
        "scale": _nullable(_ANY_NUMBER),
        "ratings": _map_of(
            _text,
            _mapping(
                {"model": _AGENT_MODEL, "transcript": _ABSOLUTE_PATH, "transcript_hash": _HASH}
            ),
        ),
    }
)
_ACCEPTANCE = _mapping(
    {
        "breach_difference": _NON_NEGATIVE,
        "self_difference": _NON_NEGATIVE,
        "done_agreement": _UNIT_CLOSED,
    }
)
_ANCHOR = _mapping(
    {
        "id": _IDENTIFIER,
        "task": _IDENTIFIER,
        "message": _string,
        "text": _string,
        "breaches": _BREACHES,
        "done": _boolean_or_null,
    }
)


_SCHEMAS: Mapping[RecordKind, Check] = {
    RecordKind.AGREEMENT: _AGREEMENT,
    RecordKind.CALIBRATION: _mapping(
        {
            "inputs": _INPUTS,
            "attempt": _POSITION,
            "judge_model": _AGENT_MODEL,
            "raters": _raters,
            "sample_size": _integer(1),
            "anchors_per_packet": _integer(FEWEST_ANCHORS_PER_PACKET),
            "acceptance": _ACCEPTANCE,
            "brief_hash": _HASH,
            "agreement": _AGREEMENT,
        }
    ),
    RecordKind.ANCHORS: _mapping(
        {"inputs": _INPUTS, "anchors": _list_of(_ANCHOR, "id", non_empty=True)}
    ),
    RecordKind.SCORES: _mapping(
        {
            "inputs": _INPUTS,
            "split": _enum(OPEN_SPLIT),
            "rows": _list_of(_ROW),
            "by_condition": _map_of(_IDENTIFIER, _CONDITION_SCORES),
            "comparisons": _map_of(_COMPARES, _COMPARISON),
            "drift": _map_of(_IDENTIFIER, _DRIFT),
            "disagreements": _list_of(_IDENTIFIER),
        }
    ),
    RecordKind.OUTCOME: _mapping(
        {
            "inputs": _INPUTS,
            "outcome": _enum(PASS_OUTCOME, FAIL_OUTCOME),
            "checks": _list_of(_OUTCOME_CHECK),
            "instruction_breaches": _NON_NEGATIVE,
            "completion_passed": _boolean,
            "words": _integer(0),
            "cost": _OUTCOME_COST,
        },
        {
            "changed_from_parent": _enum("changed", "reversed", "unchanged", "unresolved"),
            "parent_comparison": _PARENT_COMPARISON,
        },
        _outcome_parent_fields_rule,
    ),
    RecordKind.DETECTORS: _mapping(
        {"inputs": _INPUTS, "verdicts": _list_of(_DETECTOR_ENTRY, "id", non_empty=True)}
    ),
    RecordKind.COLLECTED: _mapping(
        {"inputs": _INPUTS, "packets": _map_of(_IDENTIFIER, _COLLECTED_PACKET)}
    ),
    RecordKind.VERDICT: _mapping({"verdicts": _list_of(_VERDICT_ENTRY, "id", non_empty=True)}),
    RecordKind.ORIGINS: _mapping(
        {
            "inputs": _INPUTS,
            "ids": _map_of(_IDENTIFIER, _origin),
            "packets": _map_of(_IDENTIFIER, _HASH),
        }
    ),
    RecordKind.STOP: _mapping(
        {
            "inputs": _INPUTS,
            "stop": _enum(PASSED_STOP, NO_EFFECT_STOP, CAPPED_STOP, UNRESOLVABLE_STOP),
            "kept": _nullable(_REVISION_ID),
        },
        {"reason": _text},
        _stop_reason_rule,
    ),
    RecordKind.REVISION: _mapping(
        {
            "inputs": _INPUTS,
            "number": _POSITION,
            "parent": _nullable(_REVISION_ID),
            "hash": _HASH,
            "parent_record": _nullable(_HASH),
            "change": _nullable(_CHANGE),
        },
        rule=_revision_lineage_rule,
    ),
    RecordKind.FROZEN: _mapping(
        {
            "inputs": _INPUTS,
            "hashes": _map_of(_text, _HASH),
            "noise": _NOISE,
            "tool_version": _text,
            "frozen_at": _timestamp,
        },
        {"fingerprint_hash": _HASH},
    ),
    RecordKind.REPLY: _mapping(
        {
            "inputs": _INPUTS,
            "condition": _IDENTIFIER,
            "task": _IDENTIFIER,
            "split": _SPLIT,
            "repeat": _POSITION,
            "message": _string,
            "text": _string,
            "model": _text,
            "reader_kind": _READER_KIND,
            "started": _timestamp,
            "seconds": _NON_NEGATIVE,
            "cost": _REPLY_COST,
        },
        {
            "turn": _POSITION,
            "transcript": _ABSOLUTE_PATH,
            "transcript_hash": _HASH,
            "fingerprint_hash": _HASH,
        },
        _reply_reader_kind_rule,
    ),
}


def parse_record(kind: RecordKind, document: Any) -> Record:
    """Return the document when it matches the kind's schema and raise Refusal otherwise."""
    _SCHEMAS[kind](document, kind.value)
    return document


Entry = TypeVar("Entry")
Key = TypeVar("Key")
Choice = TypeVar("Choice", bound=str)

DOCUMENT = ""
DOCUMENT_LABEL = "record"
FEWEST_REPEATS = 2
HASH_DIGEST_PATTERN = re.compile(rf"^{HASH_PATTERN}\Z")
ID_PATTERN = re.compile(rf"^{IDENTIFIER_PATTERN}\Z")
BLIND_ID_PATTERN = re.compile(r"^b[0-9a-f]{8}\Z")
AGENT_MODEL_PATTERN = re.compile(rf"^{AGENT_MODEL_ID_PATTERN}\Z")
MODEL_ALIASES = ("sonnet", "opus", "haiku", "fable", "inherit")
RESERVED_DEMAND_IDS = (OVERREACH_TARGET, COMPLETION_COMPARES)
CONDITION_PLACEHOLDER = "{condition}"

Counter = Literal["judge", "pattern", "long-sentences"]
JUDGE_COUNTER: Final[Counter] = "judge"
PATTERN_COUNTER: Final[Counter] = "pattern"
LONG_SENTENCES_COUNTER: Final[Counter] = "long-sentences"
Split = Literal["open", "sealed"]
Omissions = Literal["every-sentence", "none"]
DoneBy = Literal["answer-key", "judge"]
KeepRule = Literal["best-estimate-shortest"]
BudgetUnit = Literal["tokens", "seconds"]
TOKENS_UNIT, SECONDS_UNIT = get_args(BudgetUnit)
NoBudget = Literal["none"]
(NO_BUDGET,) = get_args(NoBudget)
InPlaceAction = Literal["rewrite", "add", "delete"]
ChangeAction = InPlaceAction | Literal["move"]
Direction = Literal["down", "up"]
Scalar = str | int | float | bool

DEMAND_KEYS = {"id", "text", "boundary", "counted_by"}
DEMAND_KEYS_BY_COUNTER: Mapping[Counter, AbstractSet[str]] = {
    JUDGE_COUNTER: DEMAND_KEYS,
    PATTERN_COUNTER: DEMAND_KEYS | {"pattern"},
    LONG_SENTENCES_COUNTER: DEMAND_KEYS | {"limit"},
}
READER_KEYS_BY_KIND: Mapping[ReaderKind, AbstractSet[str]] = {
    AGENT_READER: {"kind", "model"},
    COMMAND_READER: {"kind", "model", "command", "fingerprint", "sampling"},
}
CHANGE_KEYS_BY_ACTION: Mapping[ChangeAction, AbstractSet[str]] = {
    **{action: {"action", "sentence"} for action in get_args(InPlaceAction)},
    MOVE_ACTION: {"action", "sentence", "to"},
}


@dataclass(frozen=True)
class Series:
    """The `series.yaml` record."""

    instruction: Path
    sources: tuple[Path, ...]
    reader_kind: ReaderKind
    created: datetime
    inputs: Mapping[str, str]


def parse_series(document: object) -> Series:
    """Build the `series.yaml` record from its parsed document."""
    keys = read_keys(document, DOCUMENT, required={"instruction", "sources", "reader_kind", "created", "inputs"})
    return Series(
        instruction=read_absolute_path(keys["instruction"], "instruction"),
        sources=read_entries(keys["sources"], "sources", read_absolute_path),
        reader_kind=read_choice(keys["reader_kind"], "reader_kind", get_args(ReaderKind)),
        created=read_timestamp(keys["created"], "created"),
        inputs=read_map(keys["inputs"], "inputs", read_string, read_hash),
    )


@dataclass(frozen=True)
class JudgeDemand:
    """A demand whose breaches a judge counts."""

    id: str
    text: str
    boundary: str


@dataclass(frozen=True)
class PatternDemand:
    """A demand whose breaches are the matches of `pattern`."""

    id: str
    text: str
    boundary: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class LongSentencesDemand:
    """A demand whose breaches are the sentences longer than `limit` words."""

    id: str
    text: str
    boundary: str
    limit: int


Demand = JudgeDemand | PatternDemand | LongSentencesDemand


@dataclass(frozen=True)
class Demands:
    """The `2-demands.yaml` record."""

    demands: tuple[Demand, ...]


def parse_demands(document: object) -> Demands:
    """Build the `2-demands.yaml` record from its parsed document."""
    keys = read_keys(document, DOCUMENT, required={"demands"})
    return Demands(demands=read_non_empty_entries(keys["demands"], "demands", read_demand))


def read_demand(value: object, where: str) -> Demand:
    """Return the demand variant its `counted_by` names, refusing the other variants' keys."""
    counted_by, keys = read_variant(value, where, "counted_by", DEMAND_KEYS_BY_COUNTER)
    demand_id = read_demand_id(keys["id"], child(where, "id"))
    text = read_string(keys["text"], child(where, "text"))
    boundary = read_string(keys["boundary"], child(where, "boundary"))
    if counted_by == PATTERN_COUNTER:
        return PatternDemand(id=demand_id, text=text, boundary=boundary, pattern=read_regex(keys["pattern"], child(where, "pattern")))
    if counted_by == LONG_SENTENCES_COUNTER:
        return LongSentencesDemand(id=demand_id, text=text, boundary=boundary, limit=read_integer(keys["limit"], child(where, "limit"), minimum=1))
    return JudgeDemand(id=demand_id, text=text, boundary=boundary)


def read_demand_id(value: object, where: str) -> str:
    """Return a demand id, refusing the ids that name task and hypothesis targets."""
    demand_id = read_id(value, where)
    if demand_id in RESERVED_DEMAND_IDS:
        raise Refusal(f"{where}: {demand_id!r} is reserved")
    return demand_id


@dataclass(frozen=True)
class Task:
    """One single-message task of `3-tasks.yaml`."""

    id: str
    tempts: str
    split: Split
    message: str
    answer_key: re.Pattern[str] | None


@dataclass(frozen=True)
class Conversation:
    """One multi-turn conversation of `3-tasks.yaml`."""

    id: str
    split: Split
    turns: tuple[str, ...]


@dataclass(frozen=True)
class Tasks:
    """The `3-tasks.yaml` record."""

    tasks: tuple[Task, ...]
    conversations: tuple[Conversation, ...]


TASK_KEYS = ("tasks", "conversations")


def task_entries(tasks: Tasks) -> dict[str, Task | Conversation]:
    """Return every task and conversation by id."""
    return {entry.id: entry for entry in (*tasks.tasks, *tasks.conversations)}


def parse_tasks(document: object) -> Tasks:
    """Build the `3-tasks.yaml` record from its parsed document."""
    keys = read_keys(document, DOCUMENT, required=set(TASK_KEYS))
    return Tasks(
        tasks=read_entries(keys["tasks"], "tasks", read_task),
        conversations=read_entries(keys["conversations"], "conversations", read_conversation),
    )


def read_task(value: object, where: str) -> Task:
    """Return one task entry."""
    keys = read_keys(value, where, required={"id", "tempts", "split", "message", "answer_key"})
    return Task(
        id=read_id(keys["id"], child(where, "id")),
        tempts=read_id(keys["tempts"], child(where, "tempts")),
        split=read_choice(keys["split"], child(where, "split"), get_args(Split)),
        message=read_string(keys["message"], child(where, "message")),
        answer_key=read_nullable(keys["answer_key"], child(where, "answer_key"), read_regex),
    )


def read_conversation(value: object, where: str) -> Conversation:
    """Return one conversation entry."""
    keys = read_keys(value, where, required={"id", "split", "turns"})
    return Conversation(
        id=read_id(keys["id"], child(where, "id")),
        split=read_choice(keys["split"], child(where, "split"), get_args(Split)),
        turns=read_entries(keys["turns"], child(where, "turns"), read_string),
    )


@dataclass(frozen=True)
class Conditions:
    """The `4-conditions.yaml` record."""

    controls: tuple[Control, ...]
    aim: str
    placebo_source: Path
    omissions: Omissions


CONDITION_KEYS = ("controls", "aim", "placebo_source", "omissions")


def parse_conditions(document: object, series: Series) -> Conditions:
    """Build the `4-conditions.yaml` record, refusing controls other than the set the series sources call for."""
    keys = read_keys(document, DOCUMENT, required=set(CONDITION_KEYS))
    return Conditions(
        controls=read_controls(keys["controls"], "controls", series.sources),
        aim=read_line(keys["aim"], "aim"),
        placebo_source=read_absolute_path(keys["placebo_source"], "placebo_source"),
        omissions=read_choice(keys["omissions"], "omissions", get_args(Omissions)),
    )


def read_controls(value: object, where: str, sources: tuple[Path, ...]) -> tuple[Control, ...]:
    """Return the controls, which hold `source` exactly when the series has sources."""
    controls = read_entries(value, where, lambda item, item_where: read_choice(item, item_where, get_args(Control)))
    expected = get_args(Control) if sources else CONTROLS_WITHOUT_SOURCES
    if sorted(controls) != sorted(expected):
        raise Refusal(f"{where}: expected exactly {', '.join(expected)}, got {', '.join(controls)}")
    return controls


@dataclass(frozen=True)
class AgentReader:
    """The `5-reader.yaml` variant for a Claude subagent reader."""

    model: str


@dataclass(frozen=True)
class CommandReader:
    """The `5-reader.yaml` variant for a reader run as an external command."""

    model: str
    command: tuple[str, ...]
    fingerprint: tuple[str, ...]
    sampling: Mapping[str, Scalar]


Reader = AgentReader | CommandReader


def parse_reader(document: object) -> Reader:
    """Build the `5-reader.yaml` record as the variant its `kind` names, refusing the other variant's keys."""
    kind, keys = read_variant(document, DOCUMENT, "kind", READER_KEYS_BY_KIND)
    if kind == AGENT_READER:
        return AgentReader(model=read_agent_model(keys["model"], "model"))
    return CommandReader(
        model=read_model(keys["model"], "model"),
        command=read_command(keys["command"], "command"),
        fingerprint=read_entries(keys["fingerprint"], "fingerprint", read_string),
        sampling=read_map(keys["sampling"], "sampling", read_string, read_scalar),
    )


def read_agent_model(value: object, where: str) -> str:
    """Return a full Claude model id."""
    model = read_model(value, where)
    if not AGENT_MODEL_PATTERN.match(model):
        raise Refusal(f"{where}: expected a model id matching {AGENT_MODEL_PATTERN.pattern}, got {model!r}")
    return model


def read_model(value: object, where: str) -> str:
    """Return a non-empty model name that is not a Claude alias."""
    model = read_string(value, where)
    if model in MODEL_ALIASES:
        raise Refusal(f"{where}: alias {model!r} is refused; name the full model id")
    return model


def read_command(value: object, where: str) -> tuple[str, ...]:
    """Return a command line holding the condition placeholder exactly once."""
    command = read_entries(value, where, read_string)
    if sum(part.count(CONDITION_PLACEHOLDER) for part in command) != 1:
        raise Refusal(f"{where}: expected {CONDITION_PLACEHOLDER} exactly once")
    return command


def read_scalar(value: object, where: str) -> Scalar:
    """Return a string, number, or boolean."""
    if not isinstance(value, Scalar):
        raise Refusal(f"{where}: expected a scalar, got {value!r}")
    return value


@dataclass(frozen=True)
class GateCheck:
    """One gate check: a comparison and the gap it must clear."""

    compares: Compares
    gap: float


@dataclass(frozen=True)
class Budget:
    """A ceiling on the series cost in one unit."""

    unit: BudgetUnit
    ceiling: float


@dataclass(frozen=True)
class Gate:
    """The `7-gate.yaml` record, each key None until the user writes it."""

    repeats: int | None
    level: float | None
    done_by: DoneBy | None
    checks: tuple[GateCheck, ...] | None
    keep_rule: KeepRule | None
    budget: Budget | NoBudget | None


def parse_gate(document: object) -> Gate:
    """Build the `7-gate.yaml` record from its parsed document, any key absent."""
    keys = read_keys(document, DOCUMENT, required=set(), optional={"repeats", "level", "done_by", "checks", "keep_rule", "budget"})
    return Gate(
        repeats=read_present(keys, "repeats", lambda value, where: read_integer(value, where, minimum=FEWEST_REPEATS)),
        level=read_present(keys, "level", read_level),
        done_by=read_present(keys, "done_by", lambda value, where: read_choice(value, where, get_args(DoneBy))),
        checks=read_present(keys, "checks", read_checks),
        keep_rule=read_present(keys, "keep_rule", lambda value, where: read_choice(value, where, get_args(KeepRule))),
        budget=read_present(keys, "budget", read_budget),
    )


def read_level(value: object, where: str) -> float:
    """Return a confidence level strictly between 0 and 1."""
    level = read_number(value, where)
    if not 0 < level < 1:
        raise Refusal(f"{where}: expected a number in (0, 1), got {value!r}")
    return level


def read_checks(value: object, where: str) -> tuple[GateCheck, ...]:
    """Return the gate checks, each comparison once and every required comparison present."""
    checks = read_entries(value, where, read_check)
    compared = [check.compares for check in checks]
    repeated = sorted({compares for compares in compared if compared.count(compares) > 1})
    if repeated:
        raise Refusal(f"{where}: repeated {', '.join(repeated)}")
    missing = [compares for compares in REQUIRED_COMPARES if compares not in compared]
    if missing:
        raise Refusal(f"{where}: missing {', '.join(missing)}")
    return checks


def read_check(value: object, where: str) -> GateCheck:
    """Return one gate check."""
    keys = read_keys(value, where, required={"compares", "gap"})
    return GateCheck(
        compares=read_choice(keys["compares"], child(where, "compares"), get_args(Compares)),
        gap=read_positive_number(keys["gap"], child(where, "gap")),
    )


def read_budget(value: object, where: str) -> Budget | NoBudget:
    """Return a cost ceiling, or `none` for an unbounded series."""
    if value in get_args(NoBudget):
        return value
    keys = read_keys(value, where, required={"unit", "ceiling"})
    return Budget(
        unit=read_choice(keys["unit"], child(where, "unit"), get_args(BudgetUnit)),
        ceiling=read_positive_number(keys["ceiling"], child(where, "ceiling")),
    )


@dataclass(frozen=True)
class UserRaters:
    """The user rates the calibration sample alone."""


@dataclass(frozen=True)
class AgentRaters:
    """Two agents running `rater_model` rate the calibration sample, each alone."""

    rater_model: str


@dataclass(frozen=True)
class Acceptance:
    """The thresholds a calibration attempt's agreement must meet."""

    breach_difference: float
    self_difference: float
    done_agreement: float


@dataclass(frozen=True)
class Plan:
    """The `6-judge/calibration/attempt-<n>/plan.yaml` record."""

    judge_model: str
    raters: UserRaters | AgentRaters
    sample_size: int
    anchors_per_packet: int
    acceptance: Acceptance


def parse_plan(document: object) -> Plan:
    """Build the `6-judge/calibration/attempt-<n>/plan.yaml` record from its parsed document."""
    keys = read_keys(
        document,
        DOCUMENT,
        required={"judge_model", "raters", "sample_size", "anchors_per_packet", "acceptance"},
        optional={"rater_model"},
    )
    judge_model = read_agent_model(keys["judge_model"], "judge_model")
    return Plan(
        judge_model=judge_model,
        raters=read_raters(keys, judge_model),
        sample_size=read_integer(keys["sample_size"], "sample_size", minimum=1),
        anchors_per_packet=read_integer(keys["anchors_per_packet"], "anchors_per_packet", minimum=FEWEST_ANCHORS_PER_PACKET),
        acceptance=read_acceptance(keys["acceptance"], "acceptance"),
    )


def read_raters(keys: Mapping[str, object], judge_model: str) -> UserRaters | AgentRaters:
    """Return the rater set, `[user]` or `[agent, agent]`, carrying `rater_model` exactly when agents rate."""
    if keys["raters"] == USER_RATERS:
        if "rater_model" in keys:
            raise Refusal("rater_model: only [agent, agent] raters carry it")
        return UserRaters()
    if keys["raters"] == AGENT_RATERS:
        if "rater_model" not in keys:
            raise Refusal("rater_model: missing for [agent, agent] raters")
        return AgentRaters(rater_model=read_rater_model(keys["rater_model"], "rater_model", judge_model))
    raise Refusal(f"raters: expected [user] or [agent, agent], got {keys['raters']!r}")


def read_rater_model(value: object, where: str, judge_model: str) -> str:
    """Return an agent rater's model, which differs from the judge's."""
    rater_model = read_agent_model(value, where)
    if rater_model == judge_model:
        raise Refusal(f"{where}: must differ from judge_model {judge_model!r}")
    return rater_model


def read_acceptance(value: object, where: str) -> Acceptance:
    """Return the acceptance thresholds of a calibration plan."""
    keys = read_keys(value, where, required={"breach_difference", "self_difference", "done_agreement"})
    return Acceptance(
        breach_difference=read_bounded_number(keys["breach_difference"], child(where, "breach_difference"), 0, float("inf")),
        self_difference=read_bounded_number(keys["self_difference"], child(where, "self_difference"), 0, float("inf")),
        done_agreement=read_bounded_number(keys["done_agreement"], child(where, "done_agreement"), 0, 1),
    )


@dataclass(frozen=True)
class SentenceChange:
    """A rewrite, addition, or deletion at one sentence position."""

    action: InPlaceAction
    sentence: int


@dataclass(frozen=True)
class MoveChange:
    """A move of the parent's sentence `sentence` to position `to` in the child."""

    sentence: int
    to: int


@dataclass(frozen=True)
class PredictedMovement:
    """The direction and size a hypothesis predicts for its failing demand."""

    direction: Direction
    size: float


@dataclass(frozen=True)
class Hypothesis:
    """The `r<n>/1-hypothesis.yaml` record."""

    failing_demand: str
    replies_read: tuple[str, ...]
    change: SentenceChange | MoveChange
    predicted_movement: PredictedMovement


def parse_hypothesis(document: object) -> Hypothesis:
    """Build the `r<n>/1-hypothesis.yaml` record, which holds no cause."""
    keys = read_keys(document, DOCUMENT, required={"failing_demand", "replies_read", "change", "predicted_movement"})
    return Hypothesis(
        failing_demand=read_id(keys["failing_demand"], "failing_demand"),
        replies_read=read_entries(keys["replies_read"], "replies_read", read_blind_id),
        change=read_change(keys["change"], "change"),
        predicted_movement=read_predicted_movement(keys["predicted_movement"], "predicted_movement"),
    )


def read_blind_id(value: object, where: str) -> str:
    """Return a blind id: `b` and eight lowercase hex digits."""
    if not isinstance(value, str) or not BLIND_ID_PATTERN.match(value):
        raise Refusal(f"{where}: expected a blind id matching {BLIND_ID_PATTERN.pattern}, got {value!r}")
    return value


def read_change(value: object, where: str) -> SentenceChange | MoveChange:
    """Return the one change a hypothesis makes, carrying `to` exactly when it moves a sentence."""
    action, keys = read_variant(value, where, "action", CHANGE_KEYS_BY_ACTION)
    sentence = read_integer(keys["sentence"], child(where, "sentence"), minimum=1)
    if action == MOVE_ACTION:
        return MoveChange(sentence=sentence, to=read_integer(keys["to"], child(where, "to"), minimum=1))
    return SentenceChange(action=action, sentence=sentence)


def read_predicted_movement(value: object, where: str) -> PredictedMovement:
    """Return a hypothesis's predicted movement."""
    keys = read_keys(value, where, required={"direction", "size"})
    return PredictedMovement(
        direction=read_choice(keys["direction"], child(where, "direction"), get_args(Direction)),
        size=read_positive_number(keys["size"], child(where, "size")),
    )


@dataclass(frozen=True)
class Dropped:
    """A demand the coverage drops from the gate, with the user's reason."""

    reason: str


@dataclass(frozen=True)
class Coverage:
    """The `r<n>/3-coverage.yaml` record."""

    demands: Mapping[str, tuple[int, ...] | Dropped]
    sentences: Mapping[int, tuple[str, ...]]


def parse_coverage(document: object) -> Coverage:
    """Build the `r<n>/3-coverage.yaml` record from its parsed document."""
    keys = read_keys(document, DOCUMENT, required={"demands", "sentences"})
    return Coverage(
        demands=read_map(keys["demands"], "demands", read_id, read_demand_coverage),
        sentences=read_map(keys["sentences"], "sentences", read_sentence_number, read_sentence_coverage),
    )


def read_demand_coverage(value: object, where: str) -> tuple[int, ...] | Dropped:
    """Return the sentences covering a demand, or its drop with a reason."""
    if isinstance(value, list):
        return read_non_empty_entries(value, where, read_sentence_number)
    keys = read_keys(value, where, required={"dropped"})
    return Dropped(reason=read_string(keys["dropped"], child(where, "dropped")))


def read_sentence_coverage(value: object, where: str) -> tuple[str, ...]:
    """Return the demand ids a sentence carries."""
    return read_non_empty_entries(value, where, read_id)


def read_sentence_number(value: object, where: str) -> int:
    """Return a sentence number, counted from 1."""
    return read_integer(value, where, minimum=1)


def child(where: str, key: str) -> str:
    """Return the location of `key` inside the mapping at `where`."""
    return f"{where}.{key}" if where else key


def read_keys(value: object, where: str, required: AbstractSet[str], optional: AbstractSet[str] = frozenset()) -> Mapping[str, object]:
    """Return a mapping holding every required key and no key outside required and optional."""
    location = where or DOCUMENT_LABEL
    if not isinstance(value, Mapping):
        raise Refusal(f"{location}: expected a mapping, got {value!r}")
    missing = required - value.keys()
    if missing:
        raise Refusal(f"{location}: missing {', '.join(sorted(missing))}")
    unknown = value.keys() - required - optional
    if unknown:
        raise Refusal(f"{location}: unknown {', '.join(sorted(map(str, unknown)))}")
    return value


def read_variant(value: object, where: str, tag: str, keys_by_variant: Mapping[Choice, AbstractSet[str]]) -> tuple[Choice, Mapping[str, object]]:
    """Return the variant a mapping's `tag` key names and the mapping, which holds exactly that variant's keys."""
    every_key = set().union(*keys_by_variant.values())
    variant = read_choice(read_keys(value, where, required={tag}, optional=every_key)[tag], child(where, tag), tuple(keys_by_variant))
    return variant, read_keys(value, where, required=keys_by_variant[variant])


def read_present(keys: Mapping[str, object], key: str, read_value: Callable[[object, str], Entry]) -> Entry | None:
    """Return the key's value read by `read_value`, or None when the key is absent."""
    return read_value(keys[key], key) if key in keys else None


def read_nullable(value: object, where: str, read_value: Callable[[object, str], Entry]) -> Entry | None:
    """Return None for a YAML null, else the value read by `read_value`."""
    return None if value is None else read_value(value, where)


def read_entries(value: object, where: str, read_entry: Callable[[object, str], Entry]) -> tuple[Entry, ...]:
    """Return every item of a YAML sequence read by `read_entry`, each refused under its index."""
    if not isinstance(value, list):
        raise Refusal(f"{where}: expected a list, got {value!r}")
    return tuple(read_entry(item, f"{where}[{index}]") for index, item in enumerate(value))


def read_non_empty_entries(value: object, where: str, read_entry: Callable[[object, str], Entry]) -> tuple[Entry, ...]:
    """Return every item of a non-empty YAML sequence read by `read_entry`."""
    entries = read_entries(value, where, read_entry)
    if not entries:
        raise Refusal(f"{where}: expected a non-empty list")
    return entries


def read_map(
    value: object,
    where: str,
    read_key: Callable[[object, str], Key],
    read_value: Callable[[object, str], Entry],
) -> Mapping[Key, Entry]:
    """Return a YAML mapping with every key read by `read_key` and every value by `read_value`."""
    if not isinstance(value, Mapping):
        raise Refusal(f"{where}: expected a mapping, got {value!r}")
    return {read_key(key, f"{where} key"): read_value(item, f"{where}[{key}]") for key, item in value.items()}


def read_string(value: object, where: str) -> str:
    """Return a non-empty string."""
    if not isinstance(value, str) or not value:
        raise Refusal(f"{where}: expected a non-empty string, got {value!r}")
    return value


def read_line(value: object, where: str) -> str:
    """Return a non-empty string holding no line break."""
    line = read_string(value, where)
    if line != line.splitlines()[0]:
        raise Refusal(f"{where}: expected one line, got {value!r}")
    return line


def read_id(value: object, where: str) -> str:
    """Return an id matching the series id pattern."""
    if not isinstance(value, str) or not ID_PATTERN.match(value):
        raise Refusal(f"{where}: expected an id matching {ID_PATTERN.pattern}, got {value!r}")
    return value


def read_hash(value: object, where: str) -> str:
    """Return a lowercase sha256 hex digest."""
    if not isinstance(value, str) or not HASH_DIGEST_PATTERN.match(value):
        raise Refusal(f"{where}: expected a lowercase sha256 hex, got {value!r}")
    return value


def read_absolute_path(value: object, where: str) -> Path:
    """Return an absolute path."""
    path = Path(read_string(value, where))
    if not path.is_absolute():
        raise Refusal(f"{where}: expected an absolute path, got {value!r}")
    return path


def read_choice(value: object, where: str, choices: tuple[Choice, ...]) -> Choice:
    """Return a value drawn from a closed enum."""
    if value not in choices:
        raise Refusal(f"{where}: {value!r} is not one of {', '.join(choices)}")
    return value


def read_timestamp(value: object, where: str) -> datetime:
    """Return an ISO 8601 timestamp carrying an offset."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            pass
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise Refusal(f"{where}: expected an ISO 8601 timestamp with offset, got {value!r}")
    return value


def read_regex(value: object, where: str) -> re.Pattern[str]:
    """Return a Python regex compiled with no flags."""
    try:
        return re.compile(read_string(value, where))
    except re.error as error:
        raise Refusal(f"{where}: {error}") from error


def read_integer(value: object, where: str, minimum: int) -> int:
    """Return an integer at or above `minimum`."""
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise Refusal(f"{where}: expected an integer >= {minimum}, got {value!r}")
    return value


def read_number(value: object, where: str) -> float:
    """Return an integer or float, never a boolean."""
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise Refusal(f"{where}: expected a number, got {value!r}")
    return value


def read_positive_number(value: object, where: str) -> float:
    """Return a finite number above 0."""
    number = read_number(value, where)
    if not 0 < number < math.inf:
        raise Refusal(f"{where}: expected a finite number > 0, got {value!r}")
    return number


def read_bounded_number(value: object, where: str, lowest: float, highest: float) -> float:
    """Return a number in the closed interval from `lowest` to `highest`."""
    number = read_number(value, where)
    if not lowest <= number <= highest:
        raise Refusal(f"{where}: expected a number in [{lowest}, {highest}], got {value!r}")
    return number


Parsed = TypeVar("Parsed")

DEMAND_REFERENCE = "demand"
GATE_DEMAND_REFERENCE = "gate demand"
JUDGE_DEMAND_REFERENCE = "judge demand"
DETECTOR_DEMAND_REFERENCE = "detector demand"
DETECTOR_DEMANDS = (PatternDemand, LongSentencesDemand)
TASK_REFERENCE = "task"
CONDITION_REFERENCE = "condition"
REVISION_REFERENCE = "revision"
BLIND_ID_REFERENCE = "blind id"
ANCHOR_REFERENCE = "anchor"
PACKET_REFERENCE = "packet"
REPLY_REFERENCE = "reply"
ATTEMPT_REFERENCE = "attempt"
RATING_REFERENCE = "rating"
FROZEN_PART_REFERENCE = "frozen part"
SPLIT_REFERENCE = "split"
TURN_REFERENCE = "turn"
ABSENT_TURN = "absent"


@dataclass(frozen=True)
class CompleteGate:
    """The `7-gate.yaml` record with every key written, as `series freeze` and every later command read it."""

    repeats: int
    level: float
    done_by: DoneBy
    checks: tuple[GateCheck, ...]
    keep_rule: KeepRule
    budget: Budget | NoBudget


@dataclass(frozen=True)
class SeriesRecords:
    """The one typed loader of every series record, refusing a record whose schema, inputs, or references break."""

    files: SeriesFolder

    def series(self) -> Series:
        """Load `series.yaml`, once per loader."""
        return self._series

    def demands(self) -> Demands:
        """Load `2-demands.yaml`, once per loader."""
        return self._demands

    def tasks(self) -> Tasks:
        """Load `3-tasks.yaml`, once per loader, each task tempting a demand of the series or `overreach`."""
        return self._tasks

    @functools.cached_property
    def _series(self) -> Series:
        """Load `series.yaml`."""
        return _parsed(SERIES_RECORD, parse_series, load_record(self.files, SERIES_RECORD))

    @functools.cached_property
    def _demands(self) -> Demands:
        """Load `2-demands.yaml`."""
        return _parsed(DEMANDS_RECORD, parse_demands, _read_document(self.files, DEMANDS_RECORD))

    @functools.cached_property
    def _tasks(self) -> Tasks:
        """Load `3-tasks.yaml`, each task tempting a demand of the series or `overreach`."""
        tasks = _parsed(TASKS_RECORD, parse_tasks, _read_document(self.files, TASKS_RECORD))
        _resolve(TASKS_RECORD, DEMAND_REFERENCE, [task.tempts for task in tasks.tasks], {*self._demand_ids(), OVERREACH_TARGET})
        return tasks

    def conditions(self) -> Conditions:
        """Load `4-conditions.yaml`, its controls checked against the series sources."""
        series = self.series()
        return _parsed(CONDITIONS_RECORD, lambda document: parse_conditions(document, series), _read_document(self.files, CONDITIONS_RECORD))

    def reader(self) -> Reader:
        """Load `5-reader.yaml`, its kind the series reader kind."""
        reader = _parsed(READER_RECORD, parse_reader, _read_document(self.files, READER_RECORD))
        self._refuse_other_reader_kind(READER_RECORD, AGENT_READER if isinstance(reader, AgentReader) else COMMAND_READER)
        return reader

    def gate(self) -> Gate:
        """Load `7-gate.yaml`, any key still unwritten before freeze and every key written once the series is frozen."""
        gate = self._written_gate()
        if self.files.holds(FROZEN_RECORD):
            _completed(gate)
        return gate

    def complete_gate(self) -> CompleteGate:
        """Load `7-gate.yaml`, refusing an absent key."""
        return _completed(self._written_gate())

    def plan(self, attempt: int) -> Plan:
        """Load a calibration attempt's `plan.yaml`."""
        path = f"{attempt_folder(attempt)}/{PLAN_FILE}"
        return _parsed(path, parse_plan, _read_document(self.files, path))

    def hypothesis(self, revision: str) -> Hypothesis:
        """Load a revision's `1-hypothesis.yaml`, its failing demand a gate demand or `completion`."""
        path = f"{revision}/{HYPOTHESIS_FILE}"
        hypothesis = _parsed(path, parse_hypothesis, _read_document(self.files, path))
        _resolve(path, GATE_DEMAND_REFERENCE, [hypothesis.failing_demand], {*self.gate_demands(), COMPLETION_COMPARES})
        _resolve(path, BLIND_ID_REFERENCE, hypothesis.replies_read, self.origins(parent_revision(revision))["ids"])
        return hypothesis

    def coverage(self, revision: str) -> Coverage:
        """Load a revision's `3-coverage.yaml`, every demand it maps one of the series."""
        path = f"{revision}/{COVERAGE_FILE}"
        coverage = _parsed(path, parse_coverage, _read_document(self.files, path))
        sentence_demands = [demand for demands in coverage.sentences.values() for demand in demands]
        _resolve(path, DEMAND_REFERENCE, [*coverage.demands, *sentence_demands], self._demand_ids())
        return coverage

    def revision(self, revision: str) -> Record:
        """Load a revision's `2-revision.yaml`, its parent a revision of the series."""
        path = revision_record_path(revision)
        record = self._command_record(path, RecordKind.REVISION)
        parents = [] if record["parent"] is None else [record["parent"]]
        self._resolve_files(path, REVISION_REFERENCE, parents, revision_record_path)
        return record

    def reply(self, path: str) -> Record:
        """Load the reply record at `path`, its task or conversation one of the series with its split and turns, its condition one its revision prepared, its reader kind the series'."""
        reply = self._command_record(path, RecordKind.REPLY)
        self._refuse_other_reader_kind(path, reply["reader_kind"])
        entries = self._task_entries()
        _resolve(path, TASK_REFERENCE, [reply["task"]], entries)
        entry = entries[reply["task"]]
        _resolve(path, SPLIT_REFERENCE, [reply["split"]], {entry.split})
        _resolve(path, TURN_REFERENCE, [reply.get("turn", ABSENT_TURN)], _turns(entry))
        revision = path.partition("/")[0]
        self._resolve_files(path, CONDITION_REFERENCE, [reply["condition"]], functools.partial(condition_path, revision))
        return reply

    def origins(self, revision: str) -> Record:
        """Load a revision's `6-origins.yaml`, each reply origin naming a reply file and each anchor origin an anchor."""
        return self._origins(f"{revision}/{ORIGINS_FILE}", revision)

    def attempt_origins(self, attempt: int) -> Record:
        """Load a calibration attempt's `origins.yaml`, each origin naming an r1 reply file."""
        return self._origins(f"{attempt_folder(attempt)}/{ATTEMPT_ORIGINS_FILE}", FIRST_REVISION)

    def verdict(self, revision: str, packet: str, judging: int) -> Record:
        """Load the verdict of judging `judging` of a revision's packet, judging that packet's blind ids on judge demands only."""
        packet_ids = {blind_id for blind_id, origin in self.origins(revision)["ids"].items() if origin["packet"] == packet}
        return self._verdict_shaped(verdict_path(revision, packet, judging), packet_ids)

    def accepted_verdicts(self, revision: str, collected: Record) -> list[Record]:
        """Load the accepted verdict of each packet the revision's loaded collection names, in collection order."""
        return [self.verdict(revision, packet, judging["accepted"]) for packet, judging in collected["packets"].items()]

    def rating(self, attempt: int, rating: str) -> Record:
        """Load a calibration attempt's rating file named `rating`, rating the attempt's blind ids on judge demands only."""
        return self._verdict_shaped(f"{attempt_folder(attempt)}/{rating}.yaml", self.attempt_origins(attempt)["ids"])

    def agreement(self, attempt: int) -> Record:
        """Load a calibration attempt's `agreement.yaml`, measuring judge demands only over the attempt's rating files."""
        path = f"{attempt_folder(attempt)}/{AGREEMENT_FILE}"
        agreement = self._command_record(path, RecordKind.AGREEMENT)
        _resolve(path, JUDGE_DEMAND_REFERENCE, agreement["demands"], self._demand_ids(JudgeDemand))
        self._resolve_files(path, RATING_REFERENCE, agreement["ratings"], lambda rating: f"{attempt_folder(attempt)}/{rating}")
        return agreement

    def calibration(self) -> Record:
        """Load `6-judge/calibration.yaml`, naming an attempt with a plan and measuring judge demands only."""
        calibration = self._command_record(CALIBRATION_RECORD, RecordKind.CALIBRATION)
        _resolve(CALIBRATION_RECORD, JUDGE_DEMAND_REFERENCE, calibration["agreement"]["demands"], self._demand_ids(JudgeDemand))
        self._resolve_files(CALIBRATION_RECORD, ATTEMPT_REFERENCE, [calibration["attempt"]], lambda attempt: f"{attempt_folder(attempt)}/{PLAN_FILE}")
        return calibration

    def anchors(self) -> Record:
        """Load `6-judge/anchors.yaml`, each anchor a task of the series counted on judge demands only."""
        anchors = self._command_record(ANCHORS_RECORD, RecordKind.ANCHORS)
        _resolve(ANCHORS_RECORD, JUDGE_DEMAND_REFERENCE, _breach_demands(anchors["anchors"]), self._demand_ids(JudgeDemand))
        _resolve(ANCHORS_RECORD, TASK_REFERENCE, [anchor["task"] for anchor in anchors["anchors"]], {task.id for task in self.tasks().tasks})
        return anchors

    def collected(self, revision: str) -> Record:
        """Load a revision's `7-collected.yaml`, each packet one the revision blinded, its anchor agreement over judge demands only."""
        path = f"{revision}/{COLLECTED_FILE}"
        collected = self._command_record(path, RecordKind.COLLECTED)
        anchor_demands = [demand for packet in collected["packets"].values() for demand in packet["anchors"]["breach_difference"]]
        _resolve(path, JUDGE_DEMAND_REFERENCE, anchor_demands, self._demand_ids(JudgeDemand))
        _resolve(path, PACKET_REFERENCE, collected["packets"], self.origins(revision)["packets"])
        return collected

    def detectors(self, revision: str) -> Record:
        """Load a revision's `7-detectors.yaml`, counting the revision's blind ids on detector demands only."""
        path = f"{revision}/{DETECTORS_FILE}"
        detectors = self._command_record(path, RecordKind.DETECTORS)
        _resolve(path, DETECTOR_DEMAND_REFERENCE, _breach_demands(detectors["verdicts"]), self._demand_ids(*DETECTOR_DEMANDS))
        _resolve(path, BLIND_ID_REFERENCE, [entry["id"] for entry in detectors["verdicts"]], self.origins(revision)["ids"])
        return detectors

    def scores(self, revision: str) -> Record:
        """Load a revision's `8-scores.yaml`, scoring the revision's blind ids on demands, tasks, and prepared conditions of the series."""
        path = f"{revision}/{SCORES_FILE}"
        scores = self._command_record(path, RecordKind.SCORES)
        condition_demands = [demand for condition in scores["by_condition"].values() for demand in condition["demands"]]
        _resolve(path, DEMAND_REFERENCE, [*_breach_demands(scores["rows"]), *condition_demands], self._demand_ids())
        row_ids = [row["id"] for row in scores["rows"]]
        _resolve(path, BLIND_ID_REFERENCE, [*row_ids, *scores["disagreements"]], self.origins(revision)["ids"])
        _resolve(path, TASK_REFERENCE, [row["task"] for row in scores["rows"]], self._task_entries())
        for row in scores["rows"]:
            self._resolve_files(path, CONDITION_REFERENCE, [row["condition"]], functools.partial(condition_path, row["borrowed_from"] or revision))
        self._resolve_files(path, CONDITION_REFERENCE, scores["by_condition"], functools.partial(self._prepared_condition_path, revision))
        return scores

    def outcome(self, revision: str) -> Record:
        """Load a revision's `9-outcome.yaml`, its parent comparison targeting a gate demand or `completion`."""
        path = outcome_path(revision)
        outcome = self._command_record(path, RecordKind.OUTCOME)
        targets = [outcome["parent_comparison"]["target"]] if "parent_comparison" in outcome else []
        _resolve(path, GATE_DEMAND_REFERENCE, targets, {*self.gate_demands(), COMPLETION_COMPARES})
        return outcome

    def frozen(self) -> Record:
        """Load `8-frozen.yaml`, each hashed path a series file and its noise over gate demands only."""
        frozen = self._command_record(FROZEN_RECORD, RecordKind.FROZEN)
        self._resolve_files(FROZEN_RECORD, FROZEN_PART_REFERENCE, frozen["hashes"], str)
        noise = frozen["noise"]
        _resolve(FROZEN_RECORD, GATE_DEMAND_REFERENCE, [*noise["demands"], *noise["sigma"]["demands"]], set(self.gate_demands()))
        return frozen

    def stop(self) -> Record:
        """Load `9-stop.yaml`, its kept revision one of the series."""
        stop = self._command_record(STOP_RECORD, RecordKind.STOP)
        kept = [] if stop["kept"] is None else [stop["kept"]]
        self._resolve_files(STOP_RECORD, REVISION_REFERENCE, kept, revision_record_path)
        return stop

    def _written_gate(self) -> Gate:
        """Load `7-gate.yaml` as the user has written it so far."""
        return _parsed(GATE_RECORD, parse_gate, _read_document(self.files, GATE_RECORD))

    def _command_record(self, path: str, kind: RecordKind) -> Record:
        """Load the CLI record at `path`, its inputs re-hashed and its schema checked."""
        return _parsed(path, functools.partial(parse_record, kind), load_record(self.files, path))

    def _verdict_shaped(self, path: str, blind_ids: Container[str]) -> Record:
        """Load a verdict-shaped file written by a judge or rater, judging the given blind ids on judge demands only."""
        verdict = _parsed(path, functools.partial(parse_record, RecordKind.VERDICT), _read_document(self.files, path))
        _resolve(path, JUDGE_DEMAND_REFERENCE, _breach_demands(verdict["verdicts"]), self._demand_ids(JudgeDemand))
        _resolve(path, BLIND_ID_REFERENCE, [entry["id"] for entry in verdict["verdicts"]], blind_ids)
        return verdict

    def _origins(self, path: str, revision: str) -> Record:
        """Load an origins record whose unborrowed replies live in `revision`, each origin resolved to its packet and its reply or anchor."""
        origins = self._command_record(path, RecordKind.ORIGINS)
        entries = origins["ids"].values()
        _resolve(path, PACKET_REFERENCE, [origin["packet"] for origin in entries], origins["packets"])
        anchors = [origin[ANCHOR_KEY] for origin in entries if ANCHOR_KEY in origin]
        if anchors:
            _resolve(path, ANCHOR_REFERENCE, anchors, {anchor["id"] for anchor in self.anchors()["anchors"]})
        self._resolve_files(path, REPLY_REFERENCE, origin_reply_paths(origins, revision).values(), str)
        return origins

    def _refuse_other_reader_kind(self, path: str, reader_kind: ReaderKind) -> None:
        """Refuse the record at `path` when its reader kind differs from the one `series.yaml` holds."""
        series_kind = self.series().reader_kind
        if reader_kind != series_kind:
            raise Refusal(f"reader kind mismatch: {path} ({reader_kind}, {SERIES_RECORD} {series_kind})")

    def _resolve_files(self, path: str, kind: str, names: Iterable[Any], file_of: Callable[[Any], str]) -> None:
        """Refuse the record at `path` when a `kind` it names has no file at `file_of(name)`."""
        for name in names:
            if not self.files.holds(file_of(name)):
                raise _unresolved(path, kind, name)

    def _task_entries(self) -> dict[str, Task | Conversation]:
        """Return every task and conversation of the series by id."""
        return task_entries(self.tasks())

    def _prepared_condition_path(self, revision: str, condition: str) -> str:
        """Return the condition text `revision` prepared, or else the r1 text a later revision borrows."""
        own = condition_path(revision, condition)
        return own if self.files.holds(own) else condition_path(FIRST_REVISION, condition)

    def _demand_ids(self, *variants: type[Demand]) -> set[str]:
        """Return the ids of the series demands of the given variants, every variant when none is given."""
        return {demand.id for demand in self.demands().demands if not variants or isinstance(demand, variants)}

    def gate_demands(self) -> list[str]:
        """Return the ids of the gate demands: those r1's coverage does not drop, in coverage order."""
        return [demand for demand, coverage in self.coverage(FIRST_REVISION).demands.items() if not isinstance(coverage, Dropped)]


def _completed(gate: Gate) -> CompleteGate:
    """Return the gate with every key written, refusing the first absent key."""
    keys = {field.name: getattr(gate, field.name) for field in fields(gate)}
    absent = next((key for key, value in keys.items() if value is None), None)
    if absent is not None:
        raise missing_gate_key(absent)
    return CompleteGate(**keys)


def missing_gate_key(key: str) -> Refusal:
    """Return the refusal of a `7-gate.yaml` key still unwritten."""
    return Refusal(f"missing key: {GATE_RECORD}{KEY_SEPARATOR}{key}")


def _resolve(path: str, kind: str, names: Iterable[str], known: Container[str]) -> None:
    """Refuse the record at `path` when it names a `kind` outside the known names."""
    for name in names:
        if name not in known:
            raise _unresolved(path, kind, name)


def _unresolved(path: str, kind: str, name: object) -> Refusal:
    """Return the refusal of the record at `path` naming a `kind` the series lacks."""
    return Refusal(f"unresolved {kind}: {name} ({path})")


def _turns(entry: Task | Conversation) -> set[int | str]:
    """Return the turns a reply to the entry may name: a conversation's turn numbers, or for a task no turn."""
    if isinstance(entry, Conversation):
        return set(range(1, len(entry.turns) + 1))
    return {ABSENT_TURN}


def _breach_demands(entries: Iterable[Record]) -> list[str]:
    """Return every demand id the entries' breach maps name."""
    return [demand for entry in entries for demand in entry["breaches"]]


def revision_id(number: int) -> str:
    """Return the id of the revision with the given number."""
    return f"{REVISION_PREFIX}{number}"


def revision_number(revision: str) -> int:
    """Return the number a revision id carries."""
    return int(revision.removeprefix(REVISION_PREFIX))


def parent_revision(revision: str) -> str:
    """Return the id of the revision before the given one."""
    return revision_id(revision_number(revision) - 1)


def source_snapshot_path(basename: str) -> str:
    """Return the path of the series snapshot of the source file with the given basename."""
    return f"{SOURCE_FOLDER}/{basename}"


def agent_definition_path(agent_type: str) -> str:
    """Return the path of the definition of the agent with the given agent type."""
    return f"{AGENTS_FOLDER}/{agent_type}.md"


def revision_record_path(revision: str) -> str:
    """Return the path of a revision's `2-revision.yaml`."""
    return f"{revision}/{REVISION_RECORD_FILE}"


def condition_path(revision: str, condition: str) -> str:
    """Return the path of the condition text a revision prepared."""
    return f"{revision}/{CONDITIONS_FOLDER}/{condition}.md"


def reply_path(revision: str, condition: str, task: str, repeat: int, turn: int | None) -> str:
    """Return the path of one reply: a task's repeat, or with a turn a conversation turn within a repeat."""
    path = repeat_path(revision, condition, task, repeat)
    return f"{path}.yaml" if turn is None else f"{path}/{TURN_PREFIX}{turn}.yaml"


def repeat_path(revision: str, condition: str, task: str, repeat: int) -> str:
    """Return the path a repeat's reply file or turn folder is named by, without its suffix."""
    return f"{revision}/{REPLIES_FOLDER}/{condition}/{task}/{REPEAT_PREFIX}{repeat}"


def outcome_path(revision: str) -> str:
    """Return the path of a revision's `9-outcome.yaml`."""
    return f"{revision}/{OUTCOME_FILE}"


def packet_path(revision: str, packet: str) -> str:
    """Return the path of a revision's blinded packet."""
    return f"{revision}/{PACKETS_FOLDER}/{packet}.md"


def verdict_path(revision: str, packet: str, judging: int) -> str:
    """Return the path of the verdict judging `judging` of a revision's packet writes."""
    return f"{revision}/{VERDICTS_FOLDER}/{packet}/k{judging}.yaml"


def origin_reply_paths(origins: Record, revision: str) -> dict[str, str]:
    """Map each reply origin's blind id to the reply file it names, in its borrowed revision or else in `revision`."""
    return {
        blind_id: reply_path(origin["borrowed_from"] or revision, origin["condition"], origin["task"], origin["repeat"], origin.get("turn"))
        for blind_id, origin in origins["ids"].items()
        if ANCHOR_KEY not in origin
    }


def accepted_verdict_paths(revision: str, collected: Record) -> list[str]:
    """Return the path of each packet's accepted verdict the revision's collection names."""
    return [verdict_path(revision, packet, judging["accepted"]) for packet, judging in collected["packets"].items()]


def attempt_folder(attempt: int) -> str:
    """Return the folder of a calibration attempt."""
    return f"{CALIBRATION_FOLDER}/{ATTEMPT_FOLDER_PREFIX}{attempt}"


def _read_document(files: SeriesFolder, path: str) -> Any:
    """Read and parse the YAML record at `path`, refusing it absent or not YAML."""
    return _parse_yaml(_read_record(files, path), path)


def _parsed(path: str, parse: Callable[[Any], Parsed], document: Any) -> Parsed:
    """Return the document parsed by its schema, refusing a schema break as a malformed record at `path`."""
    try:
        return parse(document)
    except Refusal as error:
        raise Refusal(f"malformed record: {path} ({error})") from None


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
    revisions = (revision_id(number) for number in itertools.count(FIRST_REVISION_NUMBER))
    return itertools.takewhile(lambda revision: files.holds(revision_record_path(revision)), revisions)
