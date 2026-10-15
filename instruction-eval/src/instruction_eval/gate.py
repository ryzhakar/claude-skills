import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from statistics import mean
from typing import Literal, TypedDict

import numpy

from instruction_eval.records import (
    BUDGET_REASON,
    CAPPED_STOP,
    FEWEST_REPEATS,
    NO_EFFECT_STOP,
    PASS_OUTCOME,
    PASSED_STOP,
    Compares,
    Direction,
    GateCheck,
    Record,
    Refusal,
)
from instruction_eval.scores import Comparison, Noise, PairedUnit, ScoredReply, compare_paired

LATER_REVISION_COUNT = 4
LAST_REVISION_NUMBER = LATER_REVISION_COUNT + 1

PassRule = Callable[[float, tuple[float, float], float], bool]


def _undercuts_control_by_gap(mean_difference: float, interval: tuple[float, float], gap: float) -> bool:
    """Tell whether the instruction undercuts its control by the gap on average and the interval lies wholly below zero."""
    return mean_difference <= -gap and interval[1] < 0


def _upper_bound_within_gap(mean_difference: float, interval: tuple[float, float], gap: float) -> bool:
    """Tell whether the interval's upper bound stays at or below the gap."""
    return interval[1] <= gap


def _lower_bound_within_gap(mean_difference: float, interval: tuple[float, float], gap: float) -> bool:
    """Tell whether the interval's lower bound stays at or above minus the gap."""
    return interval[0] >= -gap


_PASS_RULES: Mapping[Compares, PassRule] = {
    "instruction-vs-empty": _undercuts_control_by_gap,
    "instruction-vs-aim": _undercuts_control_by_gap,
    "instruction-vs-placebo": _undercuts_control_by_gap,
    "instruction-near-source": _upper_bound_within_gap,
    "drift": _upper_bound_within_gap,
    "completion": _lower_bound_within_gap,
}


def check_passes(check: GateCheck, comparison: Comparison) -> bool:
    """Tell whether a sealed comparison passes the check's pass rule at its gap, a comparison without units failing."""
    if comparison.mean_difference is None or comparison.interval is None:
        return False
    return _PASS_RULES[check.compares](comparison.mean_difference, comparison.interval, check.gap)


GAP_RESOLUTION_SHARE = 2
SOURCE_CONDITION = "source"
EMPTY_CONDITION = "empty"
_NEAR_SOURCE_COMPARES: Compares = "instruction-near-source"
_VS_EMPTY_COMPARES: Compares = "instruction-vs-empty"


def refuse_unresolvable_gaps(
    checks: Sequence[GateCheck],
    noise: Noise,
    sealed_rows: Sequence[ScoredReply],
    gate_demands: Sequence[str],
    series_has_sources: bool,
    rng: numpy.random.Generator,
) -> None:
    """Raise Refusal on a null noise, a check whose noise exceeds half its gap, or an `instruction-near-source` check r1's sealed rows do not admit."""
    near_source = _NEAR_SOURCE_COMPARES in {check.compares for check in checks}
    if near_source:
        _refuse_near_source_without_sources(series_has_sources)
    _refuse_null_change_noise(noise)
    for check in checks:
        _refuse_unresolvable_gap(check, noise)
    if near_source:
        _refuse_unadmitted_near_source(_vs_empty_check(checks), sealed_rows, gate_demands, noise["level"], rng)


def _refuse_near_source_without_sources(series_has_sources: bool) -> None:
    """Raise Refusal when an `instruction-near-source` check stands in a series without sources."""
    if not series_has_sources:
        raise Refusal(f"{_NEAR_SOURCE_COMPARES} refused: the series has no sources")


def _vs_empty_check(checks: Sequence[GateCheck]) -> GateCheck:
    """Return the `instruction-vs-empty` check, which every gate holds."""
    return next(check for check in checks if check.compares == _VS_EMPTY_COMPARES)


def _refuse_unadmitted_near_source(
    vs_empty: GateCheck, sealed_rows: Sequence[ScoredReply], gate_demands: Sequence[str], level: float, rng: numpy.random.Generator
) -> None:
    """Raise Refusal unless `source` minus `empty` over r1's sealed tasks passes the `instruction-vs-empty` check."""
    gate_breaches = partial(_gate_breaches, gate_demands=gate_demands)
    units = _paired_units(_task_means(sealed_rows, SOURCE_CONDITION, gate_breaches), _task_means(sealed_rows, EMPTY_CONDITION, gate_breaches))
    if not check_passes(vs_empty, compare_paired(units, level, rng)):
        raise Refusal(f"{_NEAR_SOURCE_COMPARES} refused: source minus empty misses the {_VS_EMPTY_COMPARES} gap on r1's sealed rows")


def _gate_breaches(row: ScoredReply, gate_demands: Sequence[str]) -> float:
    """Return the reply's breaches summed over the gate demands."""
    return float(sum(row["breaches"][demand] for demand in gate_demands))


def least_repeats(check: GateCheck, noise: Noise) -> int | None:
    """Return the fewest repeats, at least two, at which the check's noise scaled from r1's repeats is at most half its gap, null without noise."""
    half_width = noise["checks"].get(check.compares)
    if half_width is None:
        return None
    return max(FEWEST_REPEATS, math.ceil(noise["repeats"] * (GAP_RESOLUTION_SHARE * half_width / check.gap) ** 2))


def _refuse_null_change_noise(noise: Noise) -> None:
    """Raise Refusal naming the first gate demand whose change noise is null, then a null done change noise."""
    null_demand = next((demand for demand, half_width in noise["demands"].items() if half_width is None), None)
    if null_demand is not None:
        raise Refusal(f"null noise: demands.{null_demand}")
    if noise["done_change"] is None:
        raise Refusal("null noise: done_change")


def _refuse_unresolvable_gap(check: GateCheck, noise: Noise) -> None:
    """Raise Refusal naming the check when its noise is null, or when it exceeds half its gap, with its least repeats."""
    half_width = noise["checks"].get(check.compares)
    if half_width is None:
        raise Refusal(f"null noise: {check.compares}")
    resolvable = check.gap / GAP_RESOLUTION_SHARE
    if half_width > resolvable:
        raise Refusal(
            f"unresolvable gap: {check.compares} (noise {half_width:g} > gap / 2 {resolvable:g}; least repeats {least_repeats(check, noise)})"
        )


BudgetUnit = Literal["tokens", "seconds"]
TOKENS_UNIT: BudgetUnit = "tokens"
SECONDS_UNIT: BudgetUnit = "seconds"


class BudgetRefusal(Exception):
    pass


class RevisionCost(TypedDict):
    replies: int
    input_tokens: int | None
    output_tokens: int | None
    seconds: float


@dataclass(frozen=True)
class ReplyCost:
    input_tokens: int | None
    output_tokens: int | None
    seconds: float


@dataclass(frozen=True)
class Budget:
    unit: BudgetUnit
    ceiling: float


@dataclass(frozen=True)
class SeriesShape:
    task_count: int
    open_task_count: int
    conversation_turns: int
    repeats: int
    omission_sentences: int


def _reply_cost_in_unit(reply: ReplyCost, unit: BudgetUnit) -> float:
    """Return the reply's cost in the budget unit."""
    if unit == TOKENS_UNIT:
        return reply.input_tokens + reply.output_tokens
    if unit == SECONDS_UNIT:
        return reply.seconds
    raise ValueError(f"unknown budget unit: {unit}")


def _mean_reply_cost(r1_replies: list[ReplyCost], unit: BudgetUnit) -> float:
    """Return r1's mean cost per reply in the budget unit."""
    return _total_cost(r1_replies, unit) / len(r1_replies)


def _total_cost(replies: list[ReplyCost], unit: BudgetUnit) -> float:
    """Return the replies' summed cost in the budget unit."""
    return sum(_reply_cost_in_unit(reply, unit) for reply in replies)


def _predicted_cost(r1_replies: list[ReplyCost], shape: SeriesShape, unit: BudgetUnit) -> float:
    """Return r1's cost plus the mean-priced replies of the later revisions."""
    reads_per_revision = (shape.task_count + shape.conversation_turns) * shape.repeats
    omission_reads = shape.open_task_count * shape.repeats * shape.omission_sentences
    return _total_cost(r1_replies, unit) + LATER_REVISION_COUNT * _mean_reply_cost(
        r1_replies, unit
    ) * (reads_per_revision + omission_reads)


def _refuse_empty_r1(r1_replies: list[ReplyCost]) -> None:
    """Raise BudgetRefusal when r1 has no replies to price from."""
    if not r1_replies:
        raise BudgetRefusal("budget refused: r1 has no replies")


def _refuse_token_budget_over_null_tokens(r1_replies: list[ReplyCost], unit: BudgetUnit) -> None:
    """Raise BudgetRefusal when the unit is tokens and any r1 reply has null tokens."""
    has_null_tokens = any(
        reply.input_tokens is None or reply.output_tokens is None for reply in r1_replies
    )
    if unit == TOKENS_UNIT and has_null_tokens:
        raise BudgetRefusal("tokens budget refused: an r1 reply has null tokens")


def refuse_unaffordable_freeze(
    budget: Budget | None, r1_replies: list[ReplyCost], shape: SeriesShape
) -> None:
    """Raise BudgetRefusal when the budget ceiling is below the series' predicted cost."""
    if budget is None:
        return
    _refuse_empty_r1(r1_replies)
    _refuse_token_budget_over_null_tokens(r1_replies, budget.unit)
    predicted = _predicted_cost(r1_replies, shape, budget.unit)
    if predicted > budget.ceiling:
        raise BudgetRefusal(f"predicted cost {predicted:g} exceeds ceiling {budget.ceiling:g}")


def refuse_unaffordable_ask(
    budget: Budget | None, r1_replies: list[ReplyCost], cost_so_far: float, ask_reply_count: int
) -> None:
    """Raise BudgetRefusal when the cost so far plus the ask's replies at r1's mean cost exceeds the ceiling."""
    if budget is None:
        return
    _refuse_empty_r1(r1_replies)
    _refuse_token_budget_over_null_tokens(r1_replies, budget.unit)
    projected = cost_so_far + ask_reply_count * _mean_reply_cost(r1_replies, budget.unit)
    if projected > budget.ceiling:
        raise BudgetRefusal(f"projected cost {projected:g} exceeds ceiling {budget.ceiling:g}")


def _sum_unless_null(values: list[int | None]) -> int | None:
    """Sum the values, or return null when any value is null."""
    return None if None in values else sum(values)


def sum_revision_cost(replies: list[ReplyCost]) -> RevisionCost:
    """Sum replies into the cost record of a revision's asks, token sums null when any reply's are."""
    return {
        "replies": len(replies),
        "input_tokens": _sum_unless_null([reply.input_tokens for reply in replies]),
        "output_tokens": _sum_unless_null([reply.output_tokens for reply in replies]),
        "seconds": sum(reply.seconds for reply in replies),
    }


REVISION_PREFIX = "r"


def kept_revision(outcomes: Mapping[str, Record]) -> str | None:
    """Return the revision `best-estimate-shortest` keeps from each gated revision's outcome by id, null when none passed completion."""
    candidates = [revision for revision, outcome in outcomes.items() if outcome["completion_passed"]]
    return min(candidates, key=lambda revision: _keep_rank(revision, outcomes[revision]), default=None)


def _keep_rank(revision: str, outcome: Record) -> tuple[bool, float, int, int]:
    """Return a candidate's rank, lowest first: a pass, then fewer instruction breaches, then fewer words, then the lower number."""
    return (outcome["outcome"] != PASS_OUTCOME, outcome["instruction_breaches"], outcome["words"], _revision_number(revision))


def _revision_number(revision: str) -> int:
    """Return the number a revision id carries."""
    return int(revision.removeprefix(REVISION_PREFIX))


COMPLETION_TARGET = "completion"
INSTRUCTION_CONDITION = "instruction"
DOWN: Direction = "down"
UP: Direction = "up"
ChangedFromParent = Literal["changed", "reversed", "unchanged", "unresolved"]
CHANGED: ChangedFromParent = "changed"
REVERSED: ChangedFromParent = "reversed"
UNCHANGED: ChangedFromParent = "unchanged"
UNRESOLVED: ChangedFromParent = "unresolved"


@dataclass(frozen=True)
class ParentComparison:
    """A revision's instruction minus its parent's on the hypothesis target, and what that says about the predicted change."""

    target: str
    comparison: Comparison
    changed_from_parent: ChangedFromParent


def compare_with_parent(
    revision_rows: Sequence[ScoredReply],
    parent_rows: Sequence[ScoredReply],
    target: str,
    direction: Direction,
    predicted_size: float,
    level: float,
    rng: numpy.random.Generator,
) -> ParentComparison:
    """Compare the revision's sealed instruction replies with its parent's on the target, a demand id or `completion`."""
    target_value = partial(_reply_value, target=target)
    units = _paired_units(_task_means(revision_rows, INSTRUCTION_CONDITION, target_value), _task_means(parent_rows, INSTRUCTION_CONDITION, target_value))
    comparison = compare_paired(units, level, rng)
    return ParentComparison(target, comparison, _movement_verdict(comparison.interval, direction, predicted_size))


def _paired_units(instruction_values: Mapping[str, float], other_values: Mapping[str, float]) -> list[PairedUnit]:
    """Pair each task's instruction-side mean with its other-side mean, tasks one side lacks left out."""
    return [PairedUnit(instruction_values[task], other_values[task]) for task in sorted(instruction_values.keys() & other_values.keys())]


def _task_means(rows: Sequence[ScoredReply], condition: str, reply_value: Callable[[ScoredReply], float | None]) -> dict[str, float]:
    """Map each task to the mean value of the condition's single-task replies over repeats, tasks without a value left out."""
    values_by_task: dict[str, list[float]] = {}
    for row in rows:
        value = reply_value(row)
        if row["condition"] == condition and row["turn"] is None and value is not None:
            values_by_task.setdefault(row["task"], []).append(value)
    return {task: mean(values) for task, values in values_by_task.items()}


def _reply_value(row: ScoredReply, target: str) -> float | None:
    """Return the reply's breaches of the target demand, or its done as 1 or 0 for `completion`, null when done is null."""
    if target == COMPLETION_TARGET:
        return None if row["done"] is None else float(row["done"])
    return float(row["breaches"][target])


def _movement_verdict(
    interval: tuple[float, float] | None, direction: Direction, predicted_size: float
) -> ChangedFromParent:
    """Return `changed` or `reversed` when the interval excludes zero, `unchanged` when it holds zero narrower than the predicted size, else `unresolved`."""
    if interval is None:
        return UNRESOLVED
    low, high = interval
    if high < 0:
        return CHANGED if direction == DOWN else REVERSED
    if low > 0:
        return CHANGED if direction == UP else REVERSED
    return UNCHANGED if (high - low) / 2 < predicted_size else UNRESOLVED


def stop_after(revision: str, outcomes: Mapping[str, Record], budget: Budget | None, cost_so_far: float) -> Record | None:
    """Return the `9-stop.yaml` content the gated revision's stop earns, first match winning, null when the series goes on."""
    stop = _first_matching_stop(revision, outcomes, budget, cost_so_far)
    return None if stop is None else {**stop, "kept": kept_revision(outcomes)}


def _first_matching_stop(
    revision: str, outcomes: Mapping[str, Record], budget: Budget | None, cost_so_far: float
) -> Record | None:
    """Return the stop and its reason of the first rule the revision meets, null when it meets none."""
    if outcomes[revision]["outcome"] == PASS_OUTCOME:
        return {"stop": PASSED_STOP}
    if _unchanged_from_parent(revision, outcomes) and _unchanged_from_parent(_parent_revision(revision), outcomes):
        return {"stop": NO_EFFECT_STOP}
    if _revision_number(revision) >= LAST_REVISION_NUMBER:
        return {"stop": CAPPED_STOP}
    if budget is not None and cost_so_far >= budget.ceiling:
        return {"stop": CAPPED_STOP, "reason": BUDGET_REASON}
    return None


def _unchanged_from_parent(revision: str, outcomes: Mapping[str, Record]) -> bool:
    """Tell whether the revision's outcome holds `unchanged` as its `changed_from_parent`, a missing outcome or value being no."""
    return outcomes.get(revision, {}).get("changed_from_parent") == UNCHANGED


def _parent_revision(revision: str) -> str:
    """Return the id of the revision before the given one."""
    return f"{REVISION_PREFIX}{_revision_number(revision) - 1}"
