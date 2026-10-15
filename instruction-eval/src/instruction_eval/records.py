"""Typed records of a series, built from parsed YAML documents and refused when malformed."""

import math
import re
from collections.abc import Callable, Mapping
from collections.abc import Set as AbstractSet
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final, Literal, TypeVar, get_args

Entry = TypeVar("Entry")
Key = TypeVar("Key")
Choice = TypeVar("Choice", bound=str)

DOCUMENT = ""
DOCUMENT_LABEL = "record"
FEWEST_REPEATS = 2
FEWEST_ANCHORS_PER_PACKET = 3
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}\Z")
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*\Z")
BLIND_ID_PATTERN = re.compile(r"^b[0-9a-f]{8}\Z")
AGENT_MODEL_PATTERN = re.compile(r"^claude-[a-z0-9]+(-[a-z0-9]+)+\Z")
MODEL_ALIASES = ("sonnet", "opus", "haiku", "fable", "inherit")
RESERVED_DEMAND_IDS = ("overreach", "completion")
CONDITION_PLACEHOLDER = "{condition}"
USER_RATERS = ["user"]
AGENT_RATERS = ["agent", "agent"]

ReaderKind = Literal["agent", "command"]
AGENT_KIND: Final[ReaderKind] = "agent"
COMMAND_KIND: Final[ReaderKind] = "command"
Counter = Literal["judge", "pattern", "long-sentences"]
JUDGE_COUNTER: Final[Counter] = "judge"
PATTERN_COUNTER: Final[Counter] = "pattern"
LONG_SENTENCES_COUNTER: Final[Counter] = "long-sentences"
Split = Literal["open", "sealed"]
Control = Literal["empty", "aim", "placebo", "source"]
CONTROLS_WITHOUT_SOURCES = ("empty", "aim", "placebo")
Omissions = Literal["every-sentence", "none"]
DoneBy = Literal["answer-key", "judge"]
Compares = Literal["instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "instruction-near-source", "completion", "drift"]
REQUIRED_COMPARES = ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")
KeepRule = Literal["best-estimate-shortest"]
BudgetUnit = Literal["tokens", "seconds"]
NoBudget = Literal["none"]
InPlaceAction = Literal["rewrite", "add", "delete"]
ChangeAction = InPlaceAction | Literal["move"]
MOVE_ACTION: Final[ChangeAction] = "move"
Direction = Literal["down", "up"]
Scalar = str | int | float | bool

DEMAND_KEYS = {"id", "text", "boundary", "counted_by"}
DEMAND_KEYS_BY_COUNTER: Mapping[Counter, AbstractSet[str]] = {
    JUDGE_COUNTER: DEMAND_KEYS,
    PATTERN_COUNTER: DEMAND_KEYS | {"pattern"},
    LONG_SENTENCES_COUNTER: DEMAND_KEYS | {"limit"},
}
READER_KEYS_BY_KIND: Mapping[ReaderKind, AbstractSet[str]] = {
    AGENT_KIND: {"kind", "model"},
    COMMAND_KIND: {"kind", "model", "command", "fingerprint", "sampling"},
}
CHANGE_KEYS_BY_ACTION: Mapping[ChangeAction, AbstractSet[str]] = {
    **{action: {"action", "sentence"} for action in get_args(InPlaceAction)},
    MOVE_ACTION: {"action", "sentence", "to"},
}


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
        raise RecordRefused(f"{where}: {demand_id!r} is reserved")
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


def parse_tasks(document: object) -> Tasks:
    """Build the `3-tasks.yaml` record from its parsed document."""
    keys = read_keys(document, DOCUMENT, required={"tasks", "conversations"})
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


def parse_conditions(document: object, series: Series) -> Conditions:
    """Build the `4-conditions.yaml` record, refusing controls other than the set the series sources call for."""
    keys = read_keys(document, DOCUMENT, required={"controls", "aim", "placebo_source", "omissions"})
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
    if kind == AGENT_KIND:
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


def read_scalar(value: object, where: str) -> Scalar:
    """Return a string, number, or boolean."""
    if not isinstance(value, Scalar):
        raise RecordRefused(f"{where}: expected a scalar, got {value!r}")
    return value


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
        raise RecordRefused(f"{where}: expected a blind id matching {BLIND_ID_PATTERN.pattern}, got {value!r}")
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
        raise RecordRefused(f"{location}: expected a mapping, got {value!r}")
    missing = required - value.keys()
    if missing:
        raise RecordRefused(f"{location}: missing {', '.join(sorted(missing))}")
    unknown = value.keys() - required - optional
    if unknown:
        raise RecordRefused(f"{location}: unknown {', '.join(sorted(map(str, unknown)))}")
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
        raise RecordRefused(f"{where}: expected a list, got {value!r}")
    return tuple(read_entry(item, f"{where}[{index}]") for index, item in enumerate(value))


def read_non_empty_entries(value: object, where: str, read_entry: Callable[[object, str], Entry]) -> tuple[Entry, ...]:
    """Return every item of a non-empty YAML sequence read by `read_entry`."""
    entries = read_entries(value, where, read_entry)
    if not entries:
        raise RecordRefused(f"{where}: expected a non-empty list")
    return entries


def read_map(
    value: object,
    where: str,
    read_key: Callable[[object, str], Key],
    read_value: Callable[[object, str], Entry],
) -> Mapping[Key, Entry]:
    """Return a YAML mapping with every key read by `read_key` and every value by `read_value`."""
    if not isinstance(value, Mapping):
        raise RecordRefused(f"{where}: expected a mapping, got {value!r}")
    return {read_key(key, f"{where} key"): read_value(item, f"{where}[{key}]") for key, item in value.items()}


def read_string(value: object, where: str) -> str:
    """Return a non-empty string."""
    if not isinstance(value, str) or not value:
        raise RecordRefused(f"{where}: expected a non-empty string, got {value!r}")
    return value


def read_line(value: object, where: str) -> str:
    """Return a non-empty string holding no line break."""
    line = read_string(value, where)
    if line != line.splitlines()[0]:
        raise RecordRefused(f"{where}: expected one line, got {value!r}")
    return line


def read_id(value: object, where: str) -> str:
    """Return an id matching the series id pattern."""
    if not isinstance(value, str) or not ID_PATTERN.match(value):
        raise RecordRefused(f"{where}: expected an id matching {ID_PATTERN.pattern}, got {value!r}")
    return value


def read_hash(value: object, where: str) -> str:
    """Return a lowercase sha256 hex digest."""
    if not isinstance(value, str) or not HASH_PATTERN.match(value):
        raise RecordRefused(f"{where}: expected a lowercase sha256 hex, got {value!r}")
    return value


def read_absolute_path(value: object, where: str) -> Path:
    """Return an absolute path."""
    path = Path(read_string(value, where))
    if not path.is_absolute():
        raise RecordRefused(f"{where}: expected an absolute path, got {value!r}")
    return path


def read_choice(value: object, where: str, choices: tuple[Choice, ...]) -> Choice:
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


def read_number(value: object, where: str) -> float:
    """Return an integer or float, never a boolean."""
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise RecordRefused(f"{where}: expected a number, got {value!r}")
    return value


def read_positive_number(value: object, where: str) -> float:
    """Return a finite number above 0."""
    number = read_number(value, where)
    if not 0 < number < math.inf:
        raise RecordRefused(f"{where}: expected a finite number > 0, got {value!r}")
    return number


def read_bounded_number(value: object, where: str, lowest: float, highest: float) -> float:
    """Return a number in the closed interval from `lowest` to `highest`."""
    number = read_number(value, where)
    if not lowest <= number <= highest:
        raise RecordRefused(f"{where}: expected a number in [{lowest}, {highest}], got {value!r}")
    return number
