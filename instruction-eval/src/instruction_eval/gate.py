from dataclasses import dataclass


@dataclass(frozen=True)
class ReplyCost:
    input_tokens: int | None
    output_tokens: int | None
    seconds: float


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
