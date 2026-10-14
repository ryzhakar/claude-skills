"""Typed records of a series, built from parsed YAML documents and refused when malformed."""

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, TypeVar, get_args

HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

Entry = TypeVar("Entry")

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


Split = Literal["open", "sealed"]


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


def parse_tasks(document: object) -> Tasks:
    """Build the `3-tasks.yaml` record from its parsed document."""
    keys = read_keys(document, "3-tasks.yaml", required={"tasks", "conversations"})
    return Tasks(
        tasks=read_entries(keys["tasks"], "tasks", read_task),
        conversations=read_entries(keys["conversations"], "conversations", read_conversation),
    )


def read_task(value: object, where: str) -> Task:
    """Return one task entry."""
    keys = read_keys(value, where, required={"id", "tempts", "split", "message", "answer_key"})
    return Task(
        id=read_id(keys["id"], f"{where}.id"),
        tempts=read_id(keys["tempts"], f"{where}.tempts"),
        split=read_choice(keys["split"], f"{where}.split", get_args(Split)),
        message=read_string(keys["message"], f"{where}.message"),
        answer_key=None if keys["answer_key"] is None else read_regex(keys["answer_key"], f"{where}.answer_key"),
    )


def read_conversation(value: object, where: str) -> Conversation:
    """Return one conversation entry."""
    keys = read_keys(value, where, required={"id", "split", "turns"})
    return Conversation(
        id=read_id(keys["id"], f"{where}.id"),
        split=read_choice(keys["split"], f"{where}.split", get_args(Split)),
        turns=read_entries(keys["turns"], f"{where}.turns", read_string),
    )


Control = Literal["empty", "aim", "placebo", "source"]
Omissions = Literal["every-sentence", "none"]
CONTROLS_WITHOUT_SOURCES = ("empty", "aim", "placebo")


@dataclass(frozen=True)
class Conditions:
    """The `4-conditions.yaml` record."""

    controls: tuple[Control, ...]
    aim: str
    placebo_source: Path
    omissions: Omissions


def parse_conditions(document: object, series: Series) -> Conditions:
    """Build the `4-conditions.yaml` record, refusing controls other than the set the series sources call for."""
    keys = read_keys(document, "4-conditions.yaml", required={"controls", "aim", "placebo_source", "omissions"})
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
        raise RecordRefused(f"{where}: expected exactly {', '.join(expected)}, got {', '.join(controls)}")
    return controls


def read_line(value: object, where: str) -> str:
    """Return a non-empty string holding no line break."""
    line = read_string(value, where)
    if line != line.splitlines()[0]:
        raise RecordRefused(f"{where}: expected one line, got {value!r}")
    return line


def read_entries(value: object, where: str, read_entry: Callable[[object, str], Entry]) -> tuple[Entry, ...]:
    """Return every item of a YAML sequence read by `read_entry`, each refused under its index."""
    return tuple(read_entry(item, f"{where}[{index}]") for index, item in enumerate(read_list(value, where)))


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
