from dataclasses import dataclass

ASK_REPEAT_FACTOR = 4


class BudgetRefusal(Exception):
    pass


@dataclass(frozen=True)
class ReplyCost:
    input_tokens: int | None
    output_tokens: int | None
    seconds: float


@dataclass(frozen=True)
class Budget:
    unit: str
    ceiling: float


@dataclass(frozen=True)
class SeriesShape:
    task_count: int
    open_task_count: int
    conversation_turns: int
    repeats: int
    omission_sentences: int


def _reply_cost_in_unit(reply: ReplyCost, unit: str) -> float:
    """Return the reply's cost in the budget unit."""
    if unit == "tokens":
        return reply.input_tokens + reply.output_tokens
    return reply.seconds


def _mean_reply_cost(r1_replies: list[ReplyCost], unit: str) -> float:
    """Return r1's mean cost per reply in the budget unit."""
    return _total_cost(r1_replies, unit) / len(r1_replies)


def _total_cost(replies: list[ReplyCost], unit: str) -> float:
    """Return the replies' summed cost in the budget unit."""
    return sum(_reply_cost_in_unit(reply, unit) for reply in replies)


def _predicted_cost(r1_replies: list[ReplyCost], shape: SeriesShape, unit: str) -> float:
    """Return r1's cost plus four times its mean reply cost over the later revisions' replies."""
    reads_per_revision = (shape.task_count + shape.conversation_turns) * shape.repeats
    omission_reads = shape.open_task_count * shape.repeats * shape.omission_sentences
    return _total_cost(r1_replies, unit) + ASK_REPEAT_FACTOR * _mean_reply_cost(
        r1_replies, unit
    ) * (reads_per_revision + omission_reads)


def _refuse_token_budget_over_null_tokens(r1_replies: list[ReplyCost], unit: str) -> None:
    """Raise BudgetRefusal when the unit is tokens and any r1 reply has null tokens."""
    has_null_tokens = any(
        reply.input_tokens is None or reply.output_tokens is None for reply in r1_replies
    )
    if unit == "tokens" and has_null_tokens:
        raise BudgetRefusal("tokens budget refused: an r1 reply has null tokens")


def refuse_unaffordable_freeze(
    budget: Budget | None, r1_replies: list[ReplyCost], shape: SeriesShape
) -> None:
    """Raise BudgetRefusal when the budget ceiling is below the series' predicted cost."""
    if budget is None:
        return
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
    _refuse_token_budget_over_null_tokens(r1_replies, budget.unit)
    projected = cost_so_far + ask_reply_count * _mean_reply_cost(r1_replies, budget.unit)
    if projected > budget.ceiling:
        raise BudgetRefusal(f"projected cost {projected:g} exceeds ceiling {budget.ceiling:g}")


def _sum_unless_null(values: list[int | None]) -> int | None:
    """Sum the values, or return null when any value is null."""
    return None if None in values else sum(values)


def sum_revision_cost(replies: list[ReplyCost]) -> dict:
    """Sum replies into the cost record of a revision's asks, token sums null when any reply's are."""
    return {
        "replies": len(replies),
        "input_tokens": _sum_unless_null([reply.input_tokens for reply in replies]),
        "output_tokens": _sum_unless_null([reply.output_tokens for reply in replies]),
        "seconds": sum(reply.seconds for reply in replies),
    }
