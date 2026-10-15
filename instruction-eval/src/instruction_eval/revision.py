from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from instruction_eval.coverage import split_sentences
from instruction_eval.gate import COMPLETION_TARGET, OUTCOME_FILE, REVISION_PREFIX, hypothesis_reads
from instruction_eval.records import (
    CONDITIONS_RECORD,
    FAIL_OUTCOME,
    FIRST_REVISION,
    FROZEN_RECORD,
    KEY_SEPARATOR,
    OPEN_SPLIT,
    Hypothesis,
    MoveChange,
    Record,
    Refusal,
    SentenceChange,
    SeriesFolder,
    SeriesRecords,
    Tasks,
    revision_record_path,
    sha256,
    write_file,
    write_record,
)
from instruction_eval.scores import COLLECTED_FILE, DEMANDS_AND_TASKS_INPUTS, DETECTORS_FILE, DONE_BY_INPUT, ORIGINS_FILE, Noise, ReplyRow, join_reply_rows
from instruction_eval.series import INSTRUCTION_FILE, guard_series, refuse_unclosed_frontmatter, revision_ids
from instruction_eval.tasks import shared_phrases

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


NEW_COMMAND = "revision new"
COVERAGE_INPUTS = (f"{FIRST_REVISION}/3-coverage.yaml{KEY_SEPARATOR}demands", f"{FIRST_REVISION}/3-coverage.yaml{KEY_SEPARATOR}sentences")
AIM_INPUT = f"{CONDITIONS_RECORD}{KEY_SEPARATOR}aim"
AIM_LABEL = "aim"
PLACEBO_CONDITION = f"{FIRST_REVISION}/4-conditions/placebo.md"
LabelledText = tuple[str, str]


def revision_new(files: SeriesFolder, read_external: Callable[[Path], bytes]) -> None:
    """Record the revision after the failed latest one: snapshot the live instruction once, check it makes the hypothesis' change without echoing a task, the aim, or the placebo, and chain its `2-revision.yaml` to the parent's."""
    guard_series(files, NEW_COMMAND)
    records = SeriesRecords(files)
    parent = _latest_revision(files)
    _refuse_ungated_or_passed(files, records, parent)
    revision = _next_revision(parent)
    hypothesis = records.hypothesis(revision)
    instruction = _live_instruction(records.series().instruction, read_external)
    parent_sentences = _sentence_texts(files.read_bytes(f"{parent}/{INSTRUCTION_FILE}"))
    sentences = _sentence_texts(instruction)
    change = _named_change(hypothesis.change)
    _refuse_unmade_change(parent_sentences, sentences, change)
    _refuse_echoes(revision, instruction.decode(), _echo_sources(files, records.tasks(), records.conditions().aim))
    refuse_unfit_hypothesis(hypothesis, _open_rows(records, parent), records.frozen()["noise"])
    accepted_verdicts = _accepted_verdict_paths(parent, records.collected(parent))
    write_file(files, f"{revision}/{INSTRUCTION_FILE}", instruction)
    record = _revision_record(files, revision, parent, instruction, _change_record(parent_sentences, sentences, change))
    write_record(files, revision_record_path(revision), record, _new_reads(revision, parent, accepted_verdicts))


def _latest_revision(files: SeriesFolder) -> str:
    """Return the id of the series' latest revision."""
    return list(revision_ids(files))[-1]


def _refuse_ungated_or_passed(files: SeriesFolder, records: SeriesRecords, revision: str) -> None:
    """Refuse a new revision unless the latest revision's outcome is `fail`."""
    if not files.holds(f"{revision}/{OUTCOME_FILE}"):
        raise Refusal(f"latest revision {revision} is not gated")
    if records.outcome(revision)["outcome"] != FAIL_OUTCOME:
        raise Refusal(f"latest revision {revision} did not fail")


def _revision_number(revision: str) -> int:
    """Return the number a revision id carries."""
    return int(revision.removeprefix(REVISION_PREFIX))


def _next_revision(revision: str) -> str:
    """Return the id of the revision after the given one."""
    return f"{REVISION_PREFIX}{_revision_number(revision) + 1}"


def _live_instruction(path: Path, read_external: Callable[[Path], bytes]) -> bytes:
    """Read the live instruction's bytes once, refusing it missing, not UTF-8, or opening a frontmatter it never closes."""
    try:
        instruction = read_external(path)
    except FileNotFoundError:
        raise Refusal(f"missing file: {path}") from None
    refuse_unclosed_frontmatter({path: instruction})
    return instruction


def _sentence_texts(text: bytes) -> list[str]:
    """Return the text of each sentence of an instruction, numbered from 1 by position."""
    return [text[sentence.start : sentence.end].decode() for sentence in split_sentences(text)]


def _named_change(change: SentenceChange | MoveChange) -> Change:
    """Return the change a hypothesis names as the sentence-list check takes it."""
    if isinstance(change, MoveChange):
        return Change(Action.MOVE, change.sentence, change.to)
    return Change(Action(change.action), change.sentence)


def _refuse_unmade_change(parent: list[str], child: list[str], change: Change) -> None:
    """Refuse an instruction whose sentences differ from the parent's by anything but the named change."""
    if not change_holds(parent, child, change):
        destination = "" if change.destination is None else f" to {change.destination}"
        raise Refusal(f"the instruction does not make the named change: {change.action} {change.sentence}{destination}")


def _echo_sources(files: SeriesFolder, tasks: Tasks, aim: str) -> list[LabelledText]:
    """Return the label and text of every task message and conversation turn, the aim, and r1's placebo condition."""
    turns = [(f"conversation {conversation.id} turn {number}", turn) for conversation in tasks.conversations for number, turn in enumerate(conversation.turns, 1)]
    return [
        *((f"task {task.id}", task.message) for task in tasks.tasks),
        *turns,
        (AIM_LABEL, aim),
        (PLACEBO_CONDITION, files.read_bytes(PLACEBO_CONDITION).decode()),
    ]


def _refuse_echoes(revision: str, instruction: str, sources: Sequence[LabelledText]) -> None:
    """Refuse an instruction sharing a three-word sequence with a source, naming the first source and phrase."""
    for label, text in sources:
        phrases = shared_phrases(instruction, text)
        if phrases:
            raise Refusal(f"revision {revision} echoes {label}: {phrases[0]}")


def _open_rows(records: SeriesRecords, revision: str) -> list[ReplyRow]:
    """Return the revision's open reply rows from its origins, accepted verdicts, and detector counts."""
    collected = records.collected(revision)
    verdicts = [records.verdict(revision, packet, judging["accepted"]) for packet, judging in collected["packets"].items()]
    return join_reply_rows(records.origins(revision), verdicts, records.detectors(revision), records.complete_gate().done_by, OPEN_SPLIT)


def _accepted_verdict_paths(revision: str, collected: Record) -> list[str]:
    """Return the path of each packet's accepted verdict."""
    return [f"{revision}/7-verdicts/{packet}/k{judging['accepted']}.yaml" for packet, judging in collected["packets"].items()]


def _change_record(parent: list[str], child: list[str], change: Change) -> dict[str, object]:
    """Return the change as `2-revision.yaml` holds it: action, sentence, `to` on a move, the removed text, and the added text."""
    record: dict[str, object] = {
        "action": str(change.action),
        "sentence": change.sentence,
        "old": "" if change.action == Action.ADD else _sentence(parent, change.sentence),
        "new": "" if change.action == Action.DELETE else _sentence(child, change.destination or change.sentence),
    }
    return record if change.destination is None else {**record, "to": change.destination}


def _revision_record(files: SeriesFolder, revision: str, parent: str, instruction: bytes, change: dict[str, object]) -> dict[str, object]:
    """Return the `2-revision.yaml` record of the instruction snapshot, chained to the parent's record."""
    return {
        "number": _revision_number(revision),
        "parent": parent,
        "hash": sha256(instruction),
        "parent_record": sha256(files.read_bytes(revision_record_path(parent))),
        "change": change,
    }


def _new_reads(revision: str, parent: str, accepted_verdicts: Sequence[str]) -> list[str]:
    """Return what `revision new` reads: the demand, task, aim, and coverage keys, r1's placebo, the freeze, the hypothesis keys, and the parent's instruction, record, origins, accepted verdicts, collection, detectors, and outcome."""
    return [
        *DEMANDS_AND_TASKS_INPUTS,
        AIM_INPUT,
        DONE_BY_INPUT,
        *COVERAGE_INPUTS,
        PLACEBO_CONDITION,
        FROZEN_RECORD,
        *hypothesis_reads(revision),
        f"{parent}/{INSTRUCTION_FILE}",
        revision_record_path(parent),
        f"{parent}/{ORIGINS_FILE}",
        *accepted_verdicts,
        f"{parent}/{COLLECTED_FILE}",
        f"{parent}/{DETECTORS_FILE}",
        f"{parent}/{OUTCOME_FILE}",
    ]
