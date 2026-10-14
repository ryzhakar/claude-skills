from dataclasses import dataclass
from enum import StrEnum


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
