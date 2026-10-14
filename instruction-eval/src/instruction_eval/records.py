import re
from collections.abc import Callable, Mapping
from datetime import datetime
from enum import StrEnum
from typing import Any, NoReturn

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
BUDGET_REASON = "budget"
TOTAL_KEY = "total"
INTERVAL_LENGTH = 2
REPLY_INPUT_TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
MINIMUM_ANCHORS_PER_PACKET = 3
PERMITTED_RATER_SETS = (["user"], ["agent", "agent"])
PARENT_OUTCOME_KEYS = ("changed_from_parent", "parent_comparison")
TOTAL_REFUSAL = "breach totals derive from breaches maps and are never stored"


class RecordError(ValueError):
    """Raised when a record breaks its schema."""


class RecordKind(StrEnum):
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
    raise RecordError(f"{path}: {reason}")


def _matching(pattern: str, description: str) -> Check:
    def check(value: Any, path: str) -> None:
        if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
            _refuse(path, f"expected {description}, got {value!r}")

    return check


def _enum(*allowed: str) -> Check:
    def check(value: Any, path: str) -> None:
        if not isinstance(value, str) or value not in allowed:
            _refuse(path, f"expected one of {list(allowed)}, got {value!r}")

    return check


def _nullable(inner: Check) -> Check:
    def check(value: Any, path: str) -> None:
        if value is not None:
            inner(value, path)

    return check


def _text(value: Any, path: str) -> None:
    if not isinstance(value, str) or not value:
        _refuse(path, f"expected non-empty string, got {value!r}")


def _map_of(key_check: Check, value_check: Check) -> Check:
    def check(value: Any, path: str) -> None:
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
    optional = optional or {}

    def check(value: Any, path: str) -> None:
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
    if not isinstance(value, str):
        _refuse(path, f"expected string, got {value!r}")


def _integer(minimum: int) -> Check:
    def check(value: Any, path: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            _refuse(path, f"expected integer >= {minimum}, got {value!r}")

    return check


def _number(description: str, accepts: Callable[[float], bool]) -> Check:
    def check(value: Any, path: str) -> None:
        is_number = isinstance(value, int | float) and not isinstance(value, bool)
        if not is_number or not accepts(value):
            _refuse(path, f"expected number {description}, got {value!r}")

    return check


def _timestamp(value: Any, path: str) -> None:
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
_SPLIT = _enum("open", "sealed")
_READER_KIND = _enum("agent", "command")
_VERDICT_KIND = _enum("answer", "probe", "refusal", "blank")
_ABSOLUTE_PATH = _matching(r"/.+", "an absolute path")
def _reply_cost_rule(cost: Record, path: str) -> None:
    if len({value is None for value in cost.values()}) != 1:
        _refuse(path, "all five fields are integers or all are null")
    if cost["spent_input_tokens"] is None:
        return
    if cost["spent_input_tokens"] != sum(cost[key] for key in REPLY_INPUT_TOKEN_KEYS):
        _refuse(f"{path}.spent_input_tokens", "the sum of the three input fields")


_REPLY_COST = _mapping(
    {
        key: _NULLABLE_COUNT
        for key in (*REPLY_INPUT_TOKEN_KEYS, "output_tokens", "spent_input_tokens")
    },
    rule=_reply_cost_rule,
)
_AGENT_ONLY_REPLY_KEYS = ("transcript", "transcript_hash")
_COMMAND_ONLY_REPLY_KEYS = ("fingerprint_hash",)


def _reply_reader_kind_rule(reply: Record, path: str) -> None:
    is_agent = reply["reader_kind"] == "agent"
    for key in _AGENT_ONLY_REPLY_KEYS:
        if (key in reply) != is_agent:
            _refuse(f"{path}.{key}", "present iff reader_kind is agent")
    for key in _COMMAND_ONLY_REPLY_KEYS:
        if (key in reply) == is_agent:
            _refuse(f"{path}.{key}", "present iff reader_kind is command")
    if not is_agent and reply["cost"]["spent_input_tokens"] is not None:
        _refuse(f"{path}.cost", "null for command readers")


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
    action = change["action"]
    if (action == "move") != ("to" in change):
        _refuse(f"{path}.to", "present iff action is move")
    if action == "add" and change["old"] != "":
        _refuse(f"{path}.old", "empty on add")
    if action == "delete" and change["new"] != "":
        _refuse(f"{path}.new", "empty on delete")
    if action == "move" and change["old"] != change["new"]:
        _refuse(f"{path}.new", "the moved text on move, equal to old")


_CHANGE = _mapping(
    {
        "action": _enum("rewrite", "add", "delete", "move"),
        "sentence": _POSITION,
        "old": _string,
        "new": _string,
    },
    {"to": _POSITION},
    _change_rule,
)


def _revision_lineage_rule(record: Record, path: str) -> None:
    for key in ("parent", "parent_record", "change"):
        if (record[key] is None) != (record["number"] == 1):
            _refuse(f"{path}.{key}", "null iff number is 1")


def _stop_reason_rule(record: Record, path: str) -> None:
    stop = record["stop"]
    reason = record.get("reason")
    if stop == "unresolvable":
        if reason is None:
            _refuse(f"{path}.reason", "required for unresolvable")
    elif stop == "capped":
        if reason is not None and reason != BUDGET_REASON:
            _refuse(f"{path}.reason", f"only {BUDGET_REASON!r} allowed for capped")
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
_ANCHOR_ORIGIN = _mapping({"packet": _IDENTIFIER, "anchor": _IDENTIFIER})


def _origin(value: Any, path: str) -> None:
    is_anchor = isinstance(value, Mapping) and "anchor" in value
    (_ANCHOR_ORIGIN if is_anchor else _REPLY_ORIGIN)(value, path)


def _list_of(item_check: Check, unique_by: str | None = None, non_empty: bool = False) -> Check:
    def check(value: Any, path: str) -> None:
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
    if value is not None and not isinstance(value, bool):
        _refuse(path, f"expected true, false, or null, got {value!r}")


def _breach_demand_id(value: Any, path: str) -> None:
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
    if not isinstance(value, bool):
        _refuse(path, f"expected true or false, got {value!r}")


def _interval(value: Any, path: str) -> None:
    _list_of(_ANY_NUMBER)(value, path)
    if len(value) != INTERVAL_LENGTH or value[0] > value[1]:
        _refuse(path, f"expected [low, high] with low <= high, got {value!r}")


def _outcome_parent_fields_rule(outcome: Record, path: str) -> None:
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
    if value not in PERMITTED_RATER_SETS:
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
            "split": _enum("open"),
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
            "outcome": _enum("pass", "fail"),
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
            "stop": _enum("passed", "no-effect", "capped", "unresolvable"),
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
