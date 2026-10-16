import itertools
import re
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from instruction_eval.records import (
    FIRST_REVISION,
    FIRST_REVISION_NUMBER,
    INSTRUCTION_FILE,
    OPEN_SPLIT,
    OVERREACH_TARGET,
    PLACEBO_SNAPSHOT,
    SEALED_SPLIT,
    SOURCE_FOLDER,
    TASKS_RECORD,
    Conditions,
    Omissions,
    Refusal,
    Series,
    SeriesFolder,
    SeriesRecords,
    Tasks,
    read_series_file,
    reply_path,
    revision_id,
    utf8_text,
)

LabelledText = tuple[str, str]
WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
SEQUENCE_LENGTH = 3
INSTRUCTION_CONDITION = "instruction"
OMISSION_PREFIX = "omit-"
EVERY_SENTENCE_OMISSIONS: Final[Omissions] = "every-sentence"
HALVES = (OPEN_SPLIT, SEALED_SPLIT)
FEWEST_CONVERSATIONS_PER_HALF = 2
FEWEST_TURNS = 2
ID_SEPARATOR_CLASH = "--"
AIM_LABEL = "aim"
PLACEBO_LABEL = "placebo source"
TURN_SUFFIX = re.compile(r"-turn-[0-9]+\Z")


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


def tasks_check(files: SeriesFolder, read_external: Callable[[Path], bytes]) -> None:
    """Refuse a task set that leaves a demand or `overreach` untempted in a half, lacks an answer key, holds unfit conversations or ids, repeats a message, or echoes an instruction, the aim, or the placebo source."""
    records = SeriesRecords(files)
    tasks = records.tasks()
    _refuse_untempted_halves(tasks, [demand.id for demand in records.demands().demands])
    _refuse_overreach_without_answer_key(tasks)
    _refuse_unfit_conversations(tasks)
    _refuse_unfit_ids(tasks)
    _refuse_shared_messages(tasks)
    _refuse_echoes(files, records, tasks, read_external)


def _refuse_untempted_halves(tasks: Tasks, demand_ids: list[str]) -> None:
    """Refuse the first demand, then `overreach`, that no task of the open half or no task of the sealed half tempts."""
    tempted = {(task.tempts, task.split) for task in tasks.tasks}
    for target in (*demand_ids, OVERREACH_TARGET):
        for half in HALVES:
            if (target, half) not in tempted:
                raise Refusal(f"no {half} task tempts {target} ({TASKS_RECORD})")


def _refuse_overreach_without_answer_key(tasks: Tasks) -> None:
    """Refuse the first task tempting `overreach` that carries no answer key."""
    keyless = next((task.id for task in tasks.tasks if task.tempts == OVERREACH_TARGET and task.answer_key is None), None)
    if keyless is not None:
        raise Refusal(f"overreach task without answer_key: {keyless} ({TASKS_RECORD})")


def _refuse_unfit_conversations(tasks: Tasks) -> None:
    """Refuse conversations unless there are none or each half holds at least two of at least two turns."""
    if not tasks.conversations:
        return
    for half in HALVES:
        held = sum(1 for conversation in tasks.conversations if conversation.split == half)
        if held < FEWEST_CONVERSATIONS_PER_HALF:
            raise Refusal(f"{half} half holds fewer than two conversations: {held} ({TASKS_RECORD})")
    short = next((conversation.id for conversation in tasks.conversations if len(conversation.turns) < FEWEST_TURNS), None)
    if short is not None:
        raise Refusal(f"conversation {short} holds fewer than two turns ({TASKS_RECORD})")


def _refuse_unfit_ids(tasks: Tasks) -> None:
    """Refuse a task or conversation id that another holds, that holds `--`, or that ends in `-turn-<digits>`."""
    ids = [entry.id for entry in (*tasks.tasks, *tasks.conversations)]
    for entry_id in ids:
        if ids.count(entry_id) > 1:
            raise Refusal(f"duplicate id: {entry_id} ({TASKS_RECORD})")
        if ID_SEPARATOR_CLASH in entry_id:
            raise Refusal(f'id holds "{ID_SEPARATOR_CLASH}": {entry_id} ({TASKS_RECORD})')
        if TURN_SUFFIX.search(entry_id):
            raise Refusal(f"id ends in -turn-<digits>: {entry_id} ({TASKS_RECORD})")


def _refuse_shared_messages(tasks: Tasks) -> None:
    """Refuse two tasks, or a task and a conversation's first turn, sharing a message."""
    task_by_message: dict[str, str] = {}
    for task in tasks.tasks:
        _refuse_message_held_by(task_by_message, task.message, task.id)
        task_by_message[task.message] = task.id
    for conversation in tasks.conversations:
        _refuse_message_held_by(task_by_message, conversation.turns[0], conversation.id)


def _refuse_message_held_by(task_by_message: dict[str, str], message: str, owner: str) -> None:
    """Refuse a message a task already holds, naming that task and the owner."""
    if message in task_by_message:
        raise Refusal(f"shared message: {task_by_message[message]} and {owner} ({TASKS_RECORD})")


def _refuse_echoes(files: SeriesFolder, records: SeriesRecords, tasks: Tasks, read_external: Callable[[Path], bytes]) -> None:
    """Refuse a task message or turn sharing a three-word sequence with an instruction, the aim, or the placebo source, and the aim sharing one with an instruction."""
    conditions = records.conditions()
    instructions = _revision_instructions(files)
    aim = (AIM_LABEL, conditions.aim)
    placebo = _placebo_source(files, conditions, read_external)
    _, placebo_text = placebo
    _refuse_shared_phrases(_task_messages(tasks), [*instructions, aim, placebo])
    _refuse_shared_phrases([aim], instructions)
    _refuse_shared_phrases([(PLACEBO_LABEL, placebo_text)], _source_files(files, records.series()))


def _revision_instructions(files: SeriesFolder) -> list[LabelledText]:
    """Return the path and text of each revision's instruction, in revision order, up to the first revision without one."""
    paths = itertools.takewhile(files.holds, (f"{revision_id(number)}/{INSTRUCTION_FILE}" for number in itertools.count(FIRST_REVISION_NUMBER)))
    return [(path, utf8_text(read_series_file(files, path), path)) for path in paths]


def _placebo_source(files: SeriesFolder, conditions: Conditions, read_external: Callable[[Path], bytes]) -> LabelledText:
    """Return the label and text of the placebo source, the series snapshot when it exists, else the external file, refusing one missing, not UTF-8, or holding no word."""
    label, content = _placebo_source_bytes(files, conditions, read_external)
    text = utf8_text(content, label)
    if not words(text):
        raise Refusal(f"placebo source holds no word: {label}")
    return label, text


def _placebo_source_bytes(files: SeriesFolder, conditions: Conditions, read_external: Callable[[Path], bytes]) -> tuple[str, bytes]:
    """Return the label and bytes of the series snapshot of the placebo source when it exists, else of the external file, refusing the external file missing."""
    if files.holds(PLACEBO_SNAPSHOT):
        return PLACEBO_SNAPSHOT, files.read_bytes(PLACEBO_SNAPSHOT)
    path = conditions.placebo_source
    try:
        return str(path), read_external(path)
    except FileNotFoundError:
        raise Refusal(f"missing placebo source: {path}") from None


def _source_files(files: SeriesFolder, series: Series) -> list[LabelledText]:
    """Return the path and text of each series source file, in `sources` order."""
    paths = [f"{SOURCE_FOLDER}/{source.name}" for source in series.sources]
    return [(path, utf8_text(read_series_file(files, path), path)) for path in paths]


def _task_messages(tasks: Tasks) -> list[LabelledText]:
    """Return the label and text of every task message and every conversation turn."""
    turns = [(f"conversation {conversation.id} turn {number}", turn) for conversation in tasks.conversations for number, turn in enumerate(conversation.turns, 1)]
    return [*((f"task {task.id}", task.message) for task in tasks.tasks), *turns]


def _refuse_shared_phrases(owners: list[LabelledText], others: list[LabelledText]) -> None:
    """Refuse the first owner text sharing a three-word sequence with an other text, naming both and the first shared phrase."""
    for owner, text in owners:
        for other, other_text in others:
            phrases = shared_phrases(text, other_text)
            if phrases:
                raise Refusal(f"{owner} echoes {other}: {phrases[0]}")
