from dataclasses import dataclass
from typing import Literal

Action = Literal["rewrite", "add", "delete", "move"]


@dataclass(frozen=True)
class Change:
    action: Action
    sentence: int
    destination: int | None = None


def change_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether the child sentence list is the parent with exactly the named change applied."""
    return _CHECKS[change.action](parent, child, change)


def _without(sentences: list[str], index: int) -> list[str]:
    """Return the sentences with the one at the index removed."""
    return sentences[:index] + sentences[index + 1:]


def _is_index(sentences: list[str], index: int | None) -> bool:
    """Say whether the index names a sentence in the list."""
    return index is not None and 0 <= index < len(sentences)


def _rewrite_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether only the named sentence differs between equal-length lists."""
    return (
        len(parent) == len(child)
        and _is_index(parent, change.sentence)
        and _without(parent, change.sentence) == _without(child, change.sentence)
        and child[change.sentence] != parent[change.sentence]
    )


def _add_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether removing the named child sentence leaves the parent."""
    return _is_index(child, change.sentence) and _without(child, change.sentence) == parent


def _delete_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether removing the named parent sentence leaves the child."""
    return _is_index(parent, change.sentence) and _without(parent, change.sentence) == child


def _move_holds(parent: list[str], child: list[str], change: Change) -> bool:
    """Say whether the named parent sentence reappears at the destination with the rest in order."""
    return (
        _is_index(parent, change.sentence)
        and _is_index(child, change.destination)
        and change.sentence != change.destination
        and parent[change.sentence] == child[change.destination]
        and _without(parent, change.sentence) == _without(child, change.destination)
    )


_CHECKS = {
    "rewrite": _rewrite_holds,
    "add": _add_holds,
    "delete": _delete_holds,
    "move": _move_holds,
}
