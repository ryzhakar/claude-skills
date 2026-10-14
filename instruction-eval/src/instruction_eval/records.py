"""Typed records of a series, built from parsed YAML documents and refused when malformed."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, get_args

HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

ReaderKind = Literal["agent", "command"]


class RecordRefused(ValueError):
    """A record document that breaks its schema, its message naming the offending key."""


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
    keys = read_keys(document, "series.yaml", required={"instruction", "sources", "reader_kind", "created", "inputs"})
    return Series(
        instruction=read_absolute_path(keys["instruction"], "instruction"),
        sources=tuple(read_absolute_path(source, f"sources[{index}]") for index, source in enumerate(read_list(keys["sources"], "sources"))),
        reader_kind=read_choice(keys["reader_kind"], "reader_kind", get_args(ReaderKind)),
        created=read_timestamp(keys["created"], "created"),
        inputs=read_hashes(keys["inputs"], "inputs"),
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
    keys = read_keys(document, "2-demands.yaml", required={"demands"})
    entries = read_non_empty_list(keys["demands"], "demands")
    return Demands(demands=tuple(read_demand(entry, f"demands[{index}]") for index, entry in enumerate(entries)))


def read_demand(value: object, where: str) -> Demand:
    """Return the demand variant its `counted_by` names, refusing the other variants' keys."""
    shared = {"id", "text", "boundary", "counted_by"}
    counted_by = read_choice(read_keys(value, where, required={"counted_by"}, optional=shared | {"pattern", "limit"})["counted_by"], f"{where}.counted_by", DEMAND_COUNTERS)
    keys = read_keys(value, where, required=shared | DEMAND_COUNTER_KEYS[counted_by])
    demand_id = read_demand_id(keys["id"], f"{where}.id")
    text = read_string(keys["text"], f"{where}.text")
    boundary = read_string(keys["boundary"], f"{where}.boundary")
    if counted_by == "pattern":
        return PatternDemand(id=demand_id, text=text, boundary=boundary, pattern=read_regex(keys["pattern"], f"{where}.pattern"))
    if counted_by == "long-sentences":
        return LongSentencesDemand(id=demand_id, text=text, boundary=boundary, limit=read_integer(keys["limit"], f"{where}.limit", minimum=1))
    return JudgeDemand(id=demand_id, text=text, boundary=boundary)


DEMAND_COUNTERS = ("judge", "pattern", "long-sentences")
DEMAND_COUNTER_KEYS = {"judge": set(), "pattern": {"pattern"}, "long-sentences": {"limit"}}
RESERVED_DEMAND_IDS = ("overreach", "completion")


def read_demand_id(value: object, where: str) -> str:
    """Return a demand id, refusing the ids that name task and hypothesis targets."""
    demand_id = read_id(value, where)
    if demand_id in RESERVED_DEMAND_IDS:
        raise RecordRefused(f"{where}: {demand_id!r} is reserved")
    return demand_id


def read_id(value: object, where: str) -> str:
    """Return an id matching the series id pattern."""
    if not isinstance(value, str) or not ID_PATTERN.match(value):
        raise RecordRefused(f"{where}: expected an id matching {ID_PATTERN.pattern}, got {value!r}")
    return value


def read_non_empty_list(value: object, where: str) -> list[object]:
    """Return a YAML sequence holding at least one item."""
    items = read_list(value, where)
    if not items:
        raise RecordRefused(f"{where}: expected a non-empty list")
    return items


def read_regex(value: object, where: str) -> re.Pattern[str]:
    """Return a Python regex compiled with no flags."""
    try:
        return re.compile(read_string(value, where))
    except re.error as error:
        raise RecordRefused(f"{where}: {error}") from error


def read_integer(value: object, where: str, minimum: int) -> int:
    """Return an integer at or above `minimum`."""
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise RecordRefused(f"{where}: expected an integer >= {minimum}, got {value!r}")
    return value


def read_keys(value: object, where: str, required: set[str], optional: set[str] = frozenset()) -> Mapping[str, object]:
    """Return a mapping holding every required key and no key outside required and optional."""
    if not isinstance(value, Mapping):
        raise RecordRefused(f"{where}: expected a mapping, got {value!r}")
    missing = required - value.keys()
    if missing:
        raise RecordRefused(f"{where}: missing {', '.join(sorted(missing))}")
    unknown = value.keys() - required - optional
    if unknown:
        raise RecordRefused(f"{where}: unknown {', '.join(sorted(map(str, unknown)))}")
    return value


def read_list(value: object, where: str) -> list[object]:
    """Return a YAML sequence."""
    if not isinstance(value, list):
        raise RecordRefused(f"{where}: expected a list, got {value!r}")
    return value


def read_string(value: object, where: str) -> str:
    """Return a non-empty string."""
    if not isinstance(value, str) or not value:
        raise RecordRefused(f"{where}: expected a non-empty string, got {value!r}")
    return value


def read_absolute_path(value: object, where: str) -> Path:
    """Return an absolute path."""
    path = Path(read_string(value, where))
    if not path.is_absolute():
        raise RecordRefused(f"{where}: expected an absolute path, got {value!r}")
    return path


def read_choice(value: object, where: str, choices: tuple[str, ...]) -> str:
    """Return a value drawn from a closed enum."""
    if value not in choices:
        raise RecordRefused(f"{where}: {value!r} is not one of {', '.join(choices)}")
    return value


def read_timestamp(value: object, where: str) -> datetime:
    """Return an ISO 8601 timestamp carrying an offset."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            pass
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise RecordRefused(f"{where}: expected an ISO 8601 timestamp with offset, got {value!r}")
    return value


def read_hashes(value: object, where: str) -> Mapping[str, str]:
    """Return a map from a series path to its lowercase sha256 hex."""
    if not isinstance(value, Mapping):
        raise RecordRefused(f"{where}: expected a mapping, got {value!r}")
    for path, digest in value.items():
        read_string(path, f"{where} key")
        if not isinstance(digest, str) or not HASH_PATTERN.match(digest):
            raise RecordRefused(f"{where}[{path}]: expected a lowercase sha256 hex, got {digest!r}")
    return dict(value)
