from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Literal, TypedDict

from instruction_eval.records import Compares, GateCheck
from instruction_eval.scores import Comparison

LATER_REVISION_COUNT = 4

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
