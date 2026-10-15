import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Final

from instruction_eval.records import FIRST_REVISION, OPEN_SPLIT, Conditions, Omissions, Refusal, SeriesFolder, Tasks, reply_path

WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
SEQUENCE_LENGTH = 3
INSTRUCTION_CONDITION = "instruction"
OMISSION_PREFIX = "omit-"
EVERY_SENTENCE_OMISSIONS: Final[Omissions] = "every-sentence"


@dataclass(frozen=True)
class ExpectedReply:
    """One reply a revision expects: the revision whose folder holds it, its condition, task or conversation, repeat, and turn."""

    revision: str
    condition: str
    task: str
    repeat: int
    turn: int | None

    @property
    def path(self) -> str:
        """Return the series path of the reply file."""
        return reply_path(self.revision, self.condition, self.task, self.repeat, self.turn)


def expected_replies(revision: str, tasks: Tasks, conditions: Conditions, repeats: int, sentence_count: int) -> tuple[ExpectedReply, ...]:
    """Return the expected reply set of a revision in path order: its own instruction and omission replies, and the controls' replies r1 holds."""
    replies = [
        *_every_task_and_turn(revision, INSTRUCTION_CONDITION, tasks, repeats),
        *(reply for omission in _omission_conditions(conditions, sentence_count) for reply in _open_tasks(revision, omission, tasks, repeats)),
        *(reply for control in conditions.controls for reply in _every_task_and_turn(FIRST_REVISION, control, tasks, repeats)),
    ]
    return tuple(sorted(replies, key=lambda reply: reply.path))


def refuse_missing_replies(files: SeriesFolder, expected: Iterable[ExpectedReply]) -> None:
    """Refuse a gap against the expected reply set, counting the missing replies and naming the first in path order."""
    missing = [reply.path for reply in expected if not files.holds(reply.path)]
    if missing:
        raise Refusal(f"missing replies: {len(missing)}, first {min(missing)}")


def _every_task_and_turn(revision: str, condition: str, tasks: Tasks, repeats: int) -> Iterator[ExpectedReply]:
    """Yield a reply per task and per conversation turn, each repeat."""
    for repeat in range(1, repeats + 1):
        yield from (ExpectedReply(revision, condition, task.id, repeat, None) for task in tasks.tasks)
        for conversation in tasks.conversations:
            yield from (ExpectedReply(revision, condition, conversation.id, repeat, turn) for turn in range(1, len(conversation.turns) + 1))


def _open_tasks(revision: str, condition: str, tasks: Tasks, repeats: int) -> Iterator[ExpectedReply]:
    """Yield a reply per open task, each repeat."""
    for repeat in range(1, repeats + 1):
        yield from (ExpectedReply(revision, condition, task.id, repeat, None) for task in tasks.tasks if task.split == OPEN_SPLIT)


def _omission_conditions(conditions: Conditions, sentence_count: int) -> tuple[str, ...]:
    """Return one `omit-<n>` condition per sentence when the conditions call for omissions, else none."""
    if conditions.omissions != EVERY_SENTENCE_OMISSIONS:
        return ()
    return tuple(f"{OMISSION_PREFIX}{sentence}" for sentence in range(1, sentence_count + 1))


def words(text: str) -> list[str]:
    """Return the lowercased matches of the word pattern in order, as the public word list other units count and join."""
    return [match.lower() for match in WORD_PATTERN.findall(text)]


def shared_phrases(text: str, other: str) -> list[str]:
    """Return each three-word sequence both texts hold, in order of first appearance in the first text."""
    other_sequences = set(_word_sequences(words(other)))
    return [
        sequence
        for sequence in dict.fromkeys(_word_sequences(words(text)))
        if sequence in other_sequences
    ]


def _word_sequences(word_list: list[str]) -> list[str]:
    """Return each run of three consecutive words joined by single spaces."""
    return [
        " ".join(word_list[start : start + SEQUENCE_LENGTH])
        for start in range(len(word_list) - SEQUENCE_LENGTH + 1)
    ]
