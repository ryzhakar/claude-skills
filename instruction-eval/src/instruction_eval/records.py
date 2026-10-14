"""Series records: their shapes, files written once, and CLI records whose inputs must still hash as written."""

import functools
import hashlib
import os
import re
import tempfile
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, NoReturn

import yaml

KEY_SEPARATOR = "#"
INPUTS_KEY = "inputs"


class Refusal(Exception):
    """A command's refusal, carrying the one-line message the user reads."""


@dataclass(frozen=True)
class SeriesFolder:
    """The series folder on disk at `root`."""

    root: Path

    def read_bytes(self, path: str) -> bytes:
        """Return the bytes at `path`, raising FileNotFoundError when it is absent."""
        return (self.root / path).read_bytes()

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


def write_record(files: SeriesFolder, path: str, record: Mapping[str, Any], reads: Iterable[str]) -> None:
    """Write a YAML record whose `inputs` map each read, a series path or `<path>#<key>`, to its sha256, refusing a record carrying its own."""
    if INPUTS_KEY in record:
        raise Refusal(f"record {path} carries inputs; inputs come from its reads")
    write_file(files, path, _dump_canonical_yaml({**record, INPUTS_KEY: _hash_inputs(files, reads)}))


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
    try:
        record = yaml.safe_load(content)
    except yaml.YAMLError:
        raise Refusal(f"malformed record: {path} (not YAML)") from None
    if not isinstance(record, dict) or not _is_text_map(record.get(INPUTS_KEY)):
        raise Refusal(f"malformed record: {path} (no inputs map)")
    return record


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
        return _sha256(read_file(file_path))
    return _sha256(_dump_canonical_yaml(_read_top_level_value(parse_file(file_path), entry, key)))


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


def _dump_canonical_yaml(value: Any) -> bytes:
    """Dump a value as YAML with sorted keys in block style."""
    return yaml.safe_dump(value, sort_keys=True, default_flow_style=False, allow_unicode=True).encode()


def _sha256(content: bytes) -> str:
    """Return the lowercase sha256 hex digest of the bytes."""
    return hashlib.sha256(content).hexdigest()


Record = Mapping[str, Any]
Check = Callable[[Any, str], None]

REVISION_ID_PATTERN = r"r[1-9][0-9]*"
IDENTIFIER_PATTERN = r"[a-z0-9][a-z0-9-]*"
COMPARES = (
    "instruction-vs-empty",
    "instruction-vs-aim",
    "instruction-vs-placebo",
    "instruction-near-source",
    "completion",
    "drift",
)
HASH_PATTERN = r"[0-9a-f]{64}"
TOTAL_KEY = "total"
INTERVAL_LENGTH = 2
MINIMUM_ANCHORS_PER_PACKET = 3
TOTAL_REFUSAL = "breach totals derive from breaches maps and are never stored"

AGENT_READER = "agent"
COMMAND_READER = "command"
USER_RATER = "user"
PERMITTED_RATER_SETS = ((USER_RATER,), (AGENT_READER, AGENT_READER))
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
FIRST_REVISION_NUMBER = 1
AGENT_ONLY_REPLY_KEYS = ("transcript", "transcript_hash")
COMMAND_ONLY_REPLY_KEYS = ("fingerprint_hash",)


class RecordError(ValueError):
    """Raised when a record breaks its schema."""


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
    """Raise a RecordError naming the path and the reason."""
    raise RecordError(f"{path}: {reason}")


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
_AGENT_MODEL = _matching(r"claude-[a-z0-9]+(-[a-z0-9]+)+", "a full claude model id")
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
        "done_rate": _UNIT_CLOSED,
        "kinds": _map_of(_VERDICT_KIND, _integer(0)),
    }
)
_COMPARISON = _mapping(
    {"mean_difference": _ANY_NUMBER, "interval": _nullable(_interval), "units": _integer(0)}
)
_DRIFT = _mapping({"slope": _ANY_NUMBER, "interval": _interval})
_OUTCOME_CHECK = _mapping(
    {
        "compares": _COMPARES,
        "gap": _POSITIVE,
        "mean_difference": _ANY_NUMBER,
        "interval": _nullable(_interval),
        "pass": _boolean,
    }
)
_PARENT_COMPARISON = _mapping(
    {"target": _IDENTIFIER, "mean_difference": _ANY_NUMBER, "interval": _interval}
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
            "anchors_per_packet": _integer(MINIMUM_ANCHORS_PER_PACKET),
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
    """Return the document when it matches the kind's schema and raise RecordError otherwise."""
    _SCHEMAS[kind](document, kind.value)
    return document
