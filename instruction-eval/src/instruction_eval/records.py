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


AGENT_MODEL_PATTERN = re.compile(r"^claude-[a-z0-9]+(-[a-z0-9]+)+$")
MODEL_ALIASES = ("sonnet", "opus", "haiku", "fable", "inherit")
CONDITION_PLACEHOLDER = "{condition}"
Scalar = str | int | float | bool


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
    kind = read_choice(read_keys(document, "5-reader.yaml", required={"kind"}, optional=COMMAND_READER_KEYS)["kind"], "kind", get_args(ReaderKind))
    if kind == "agent":
        keys = read_keys(document, "5-reader.yaml", required={"kind", "model"})
        return AgentReader(model=read_agent_model(keys["model"], "model"))
    keys = read_keys(document, "5-reader.yaml", required=COMMAND_READER_KEYS)
    return CommandReader(
        model=read_model(keys["model"], "model"),
        command=read_command(keys["command"], "command"),
        fingerprint=read_entries(keys["fingerprint"], "fingerprint", read_string),
        sampling=read_sampling(keys["sampling"], "sampling"),
    )


COMMAND_READER_KEYS = {"kind", "model", "command", "fingerprint", "sampling"}


def read_agent_model(value: object, where: str) -> str:
    """Return a full Claude model id."""
    model = read_model(value, where)
    if not AGENT_MODEL_PATTERN.match(model):
        raise RecordRefused(f"{where}: expected a model id matching {AGENT_MODEL_PATTERN.pattern}, got {model!r}")
    return model


def read_model(value: object, where: str) -> str:
    """Return a non-empty model name that is not a Claude alias."""
    model = read_string(value, where)
    if model in MODEL_ALIASES:
        raise RecordRefused(f"{where}: alias {model!r} is refused; name the full model id")
    return model


def read_command(value: object, where: str) -> tuple[str, ...]:
    """Return a command line holding the condition placeholder exactly once."""
    command = read_entries(value, where, read_string)
    if sum(part.count(CONDITION_PLACEHOLDER) for part in command) != 1:
        raise RecordRefused(f"{where}: expected {CONDITION_PLACEHOLDER} exactly once")
    return command


def read_sampling(value: object, where: str) -> Mapping[str, Scalar]:
    """Return a map from a sampling setting to its scalar value."""
    if not isinstance(value, Mapping):
        raise RecordRefused(f"{where}: expected a mapping, got {value!r}")
    for setting, setting_value in value.items():
        read_string(setting, f"{where} key")
        if not isinstance(setting_value, Scalar):
            raise RecordRefused(f"{where}[{setting}]: expected a scalar, got {setting_value!r}")
    return dict(value)


DoneBy = Literal["answer-key", "judge"]
Compares = Literal["instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "instruction-near-source", "completion", "drift"]
REQUIRED_COMPARES = ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")
KeepRule = Literal["best-estimate-shortest"]
BudgetUnit = Literal["tokens", "seconds"]
NoBudget = Literal["none"]


@dataclass(frozen=True)
class Check:
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
    checks: tuple[Check, ...] | None
    keep_rule: KeepRule | None
    budget: Budget | NoBudget | None


def parse_gate(document: object) -> Gate:
    """Build the `7-gate.yaml` record from its parsed document, any key absent."""
    keys = read_keys(document, "7-gate.yaml", required=set(), optional={"repeats", "level", "done_by", "checks", "keep_rule", "budget"})
    return Gate(
        repeats=read_present(keys, "repeats", lambda value, where: read_integer(value, where, minimum=2)),
        level=read_present(keys, "level", read_level),
        done_by=read_present(keys, "done_by", lambda value, where: read_choice(value, where, get_args(DoneBy))),
        checks=read_present(keys, "checks", read_checks),
        keep_rule=read_present(keys, "keep_rule", lambda value, where: read_choice(value, where, get_args(KeepRule))),
        budget=read_present(keys, "budget", read_budget),
    )


def read_present(keys: Mapping[str, object], key: str, read_value: Callable[[object, str], Entry]) -> Entry | None:
    """Return the key's value read by `read_value`, or None when the key is absent."""
    return read_value(keys[key], key) if key in keys else None


def read_level(value: object, where: str) -> float:
    """Return a confidence level strictly between 0 and 1."""
    level = read_number(value, where)
    if not 0 < level < 1:
        raise RecordRefused(f"{where}: expected a number in (0, 1), got {value!r}")
    return level


def read_checks(value: object, where: str) -> tuple[Check, ...]:
    """Return the gate checks, each comparison once and every required comparison present."""
    checks = read_entries(value, where, read_check)
    compared = [check.compares for check in checks]
    repeated = sorted({compares for compares in compared if compared.count(compares) > 1})
    if repeated:
        raise RecordRefused(f"{where}: repeated {', '.join(repeated)}")
    missing = [compares for compares in REQUIRED_COMPARES if compares not in compared]
    if missing:
        raise RecordRefused(f"{where}: missing {', '.join(missing)}")
    return checks


def read_check(value: object, where: str) -> Check:
    """Return one gate check."""
    keys = read_keys(value, where, required={"compares", "gap"})
    return Check(
        compares=read_choice(keys["compares"], f"{where}.compares", get_args(Compares)),
        gap=read_positive_number(keys["gap"], f"{where}.gap"),
    )


def read_budget(value: object, where: str) -> Budget | NoBudget:
    """Return a cost ceiling, or `none` for an unbounded series."""
    if value in get_args(NoBudget):
        return value
    keys = read_keys(value, where, required={"unit", "ceiling"})
    return Budget(
        unit=read_choice(keys["unit"], f"{where}.unit", get_args(BudgetUnit)),
        ceiling=read_positive_number(keys["ceiling"], f"{where}.ceiling"),
    )


def read_number(value: object, where: str) -> float:
    """Return an integer or float, never a boolean."""
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise RecordRefused(f"{where}: expected a number, got {value!r}")
    return value


def read_positive_number(value: object, where: str) -> float:
    """Return a number above 0."""
    number = read_number(value, where)
    if number <= 0:
        raise RecordRefused(f"{where}: expected a number > 0, got {value!r}")
    return number


USER_RATERS = ["user"]
AGENT_RATERS = ["agent", "agent"]
PLAN_KEYS = {"judge_model", "raters", "sample_size", "anchors_per_packet", "acceptance"}


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
    keys = read_keys(document, "plan.yaml", required=PLAN_KEYS, optional={"rater_model"})
    judge_model = read_agent_model(keys["judge_model"], "judge_model")
    return Plan(
        judge_model=judge_model,
        raters=read_raters(keys, judge_model),
        sample_size=read_integer(keys["sample_size"], "sample_size", minimum=1),
        anchors_per_packet=read_integer(keys["anchors_per_packet"], "anchors_per_packet", minimum=3),
        acceptance=read_acceptance(keys["acceptance"], "acceptance"),
    )


def read_raters(keys: Mapping[str, object], judge_model: str) -> UserRaters | AgentRaters:
    """Return the rater set, `[user]` or `[agent, agent]`, carrying `rater_model` exactly when agents rate."""
    if keys["raters"] == USER_RATERS:
        if "rater_model" in keys:
            raise RecordRefused("rater_model: only [agent, agent] raters carry it")
        return UserRaters()
    if keys["raters"] == AGENT_RATERS:
        if "rater_model" not in keys:
            raise RecordRefused("rater_model: missing for [agent, agent] raters")
        return AgentRaters(rater_model=read_rater_model(keys["rater_model"], "rater_model", judge_model))
    raise RecordRefused(f"raters: expected [user] or [agent, agent], got {keys['raters']!r}")


def read_rater_model(value: object, where: str, judge_model: str) -> str:
    """Return an agent rater's model, which differs from the judge's."""
    rater_model = read_agent_model(value, where)
    if rater_model == judge_model:
        raise RecordRefused(f"{where}: must differ from judge_model {judge_model!r}")
    return rater_model


def read_acceptance(value: object, where: str) -> Acceptance:
    """Return the acceptance thresholds of a calibration plan."""
    keys = read_keys(value, where, required={"breach_difference", "self_difference", "done_agreement"})
    return Acceptance(
        breach_difference=read_bounded_number(keys["breach_difference"], f"{where}.breach_difference", 0, float("inf")),
        self_difference=read_bounded_number(keys["self_difference"], f"{where}.self_difference", 0, float("inf")),
        done_agreement=read_bounded_number(keys["done_agreement"], f"{where}.done_agreement", 0, 1),
    )


def read_bounded_number(value: object, where: str, lowest: float, highest: float) -> float:
    """Return a number in the closed interval from `lowest` to `highest`."""
    number = read_number(value, where)
    if not lowest <= number <= highest:
        raise RecordRefused(f"{where}: expected a number in [{lowest}, {highest}], got {value!r}")
    return number


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
