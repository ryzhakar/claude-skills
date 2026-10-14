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


class RecordError(ValueError):
    """Raised when a record breaks its schema."""


class RecordKind(StrEnum):
    STOP = "stop"
    REVISION = "revision"
    FROZEN = "frozen"


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
                _refuse(f"{path}.{key}", "unknown key")
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


_SCHEMAS: Mapping[RecordKind, Check] = {
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
}


def parse_record(kind: RecordKind, document: Any) -> Record:
    """Return the document when it matches the kind's schema and raise RecordError otherwise."""
    _SCHEMAS[kind](document, kind.value)
    return document
