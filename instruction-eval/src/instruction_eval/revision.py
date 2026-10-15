from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from instruction_eval.gate import COMPLETION_TARGET
from instruction_eval.records import Hypothesis, Refusal
from instruction_eval.scores import Noise, ReplyRow

NOISE_MULTIPLE = 2


def refuse_unfit_hypothesis(hypothesis: Hypothesis, open_rows: Sequence[ReplyRow], noise: Noise) -> None:
    """Raise Refusal when the hypothesis reads a reply outside the parent's open replies or none that shows its failing demand, or predicts no more than twice its target's change noise."""
    _refuse_unopen_replies(hypothesis.replies_read, open_rows)
    _refuse_unshown_failure(hypothesis.failing_demand, _rows_read(hypothesis.replies_read, open_rows))
    _refuse_size_within_noise(hypothesis.failing_demand, hypothesis.predicted_movement.size, noise)


def _refuse_size_within_noise(failing_demand: str, predicted_size: float, noise: Noise) -> None:
    """Raise Refusal when the predicted size is at most twice the target's change noise."""
    limit = NOISE_MULTIPLE * _change_noise(failing_demand, noise)
    if predicted_size <= limit:
        raise Refusal(f"predicted size {predicted_size:g} does not exceed twice the change noise of {failing_demand}: {limit:g}")


def _change_noise(failing_demand: str, noise: Noise) -> float:
    """Return the change noise of the demand, or the done change noise for `completion`."""
    if failing_demand == COMPLETION_TARGET:
        return noise["done_change"]
    return noise["demands"][failing_demand]


def _rows_read(replies_read: Sequence[str], open_rows: Sequence[ReplyRow]) -> list[ReplyRow]:
    """Return the open rows whose ids the hypothesis read."""
    return [row for row in open_rows if row["id"] in replies_read]


def _refuse_unshown_failure(failing_demand: str, rows_read: Sequence[ReplyRow]) -> None:
    """Raise Refusal when no row read breaches the demand, or for `completion` when none has done false."""
    if not any(_shows_failure(row, failing_demand) for row in rows_read):
        raise Refusal(f"replies_read shows no failure of {failing_demand}")


def _shows_failure(row: ReplyRow, failing_demand: str) -> bool:
    """Tell whether the row breaches the demand, or for `completion` holds done false."""
    if failing_demand == COMPLETION_TARGET:
        return row["done"] is False
    return row["breaches"][failing_demand] > 0


def _refuse_unopen_replies(replies_read: Sequence[str], open_rows: Sequence[ReplyRow]) -> None:
    """Raise Refusal naming each read reply that is no open reply, a sealed one, an anchor, or an unknown id."""
    open_ids = {row["id"] for row in open_rows}
    unopen = [blind_id for blind_id in replies_read if blind_id not in open_ids]
    if unopen:
        raise Refusal(f"replies_read holds no open reply: {', '.join(unopen)}")


class Action(StrEnum):
    REWRITE = "rewrite"
    ADD = "add"
    DELETE = "delete"
    MOVE = "move"


@dataclass(frozen=True)
class Change:
    action: Action
    sentence: int
    destination: int | None = None

    def __post_init__(self) -> None:
        """Refuse a move without a destination and any other action with one."""
        if self.action == Action.MOVE and self.destination is None:
            raise ValueError("move needs a destination")
        if self.action != Action.MOVE and self.destination is not None:
            raise ValueError("only move takes a destination")


def change_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether the child sentence list is the parent with exactly the named change applied."""
    return _CHECKS[change.action](parent, child, change)


def _sentence(sentences: list[str], number: int) -> str:
    """Return the sentence with the given number, numbered from 1."""
    return sentences[number - 1]


def _without(sentences: list[str], number: int) -> list[str]:
    """Return the sentences with the numbered one removed."""
    return sentences[:number - 1] + sentences[number:]


def _is_number(sentences: list[str], number: int | None) -> bool:
    """Say whether the number names a sentence in the list, numbered from 1."""
    return number is not None and 1 <= number <= len(sentences)


def _rewrite_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether only the named sentence differs between equal-length lists."""
    return (
        len(parent) == len(child)
        and _is_number(parent, change.sentence)
        and _without(parent, change.sentence) == _without(child, change.sentence)
        and _sentence(child, change.sentence) != _sentence(parent, change.sentence)
    )


def _add_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether removing the named child sentence leaves the parent."""
    return _is_number(child, change.sentence) and _without(child, change.sentence) == parent


def _delete_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether removing the named parent sentence leaves the child."""
    return _is_number(parent, change.sentence) and _without(parent, change.sentence) == child


def _move_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether the named parent sentence reappears at the destination with the rest in order."""
    return (
        _is_number(parent, change.sentence)
        and _is_number(child, change.destination)
        and change.sentence != change.destination
        and _sentence(parent, change.sentence) == _sentence(child, change.destination)
        and _without(parent, change.sentence) == _without(child, change.destination)
    )


_CHECKS = {
    Action.REWRITE: _rewrite_holds,
    Action.ADD: _add_holds,
    Action.DELETE: _delete_holds,
    Action.MOVE: _move_holds,
}
