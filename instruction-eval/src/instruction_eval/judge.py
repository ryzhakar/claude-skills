"""Judging: the judge brief, verdict validation, and blinded packets."""

import dataclasses
import re
from collections.abc import Container, Iterable, Mapping, Sequence
from collections.abc import Set as AbstractSet
from dataclasses import dataclass
from pathlib import Path
from random import Random

from instruction_eval.conditions import strip_frontmatter
from instruction_eval.records import (
    ANCHOR_KEY,
    Demand,
    Demands,
    JudgeDemand,
    Record,
    RecordError,
    RecordKind,
    Refusal,
    parse_record,
)
from instruction_eval.tasks import OMISSION_PREFIX, ExpectedReply

SOURCE_PLACEHOLDER = "{SOURCE}"
DEMANDS_PLACEHOLDER = "{DEMANDS}"
PACKET_PLACEHOLDER = "{PACKET}"
OUT_PLACEHOLDER = "{OUT}"
PLACEHOLDERS = (SOURCE_PLACEHOLDER, DEMANDS_PLACEHOLDER, PACKET_PLACEHOLDER, OUT_PLACEHOLDER)
PLACEHOLDER_PATTERN = re.compile("|".join(re.escape(placeholder) for placeholder in PLACEHOLDERS))
OATH_SKILL = "manifesto:manifesto-oath"
BRIEF_FORBIDDEN_WORDS = ("empty", "aim", "placebo", "instruction", "omit", "control", "condition", "revision", "reader", "digest")
SOURCE_FOLDER = "1-source"
SOURCE_SEPARATOR = "\n\n"
VERDICT_LABEL = RecordKind.VERDICT.value
OMISSIONS_PACKET_SUFFIX = "--omissions"
TURN_PACKET_INFIX = "-turn-"
BLIND_ID_BITS = 32
BLIND_ID_DRAWS = 100
SECTION_SEPARATOR = "\n\n"


def render_brief(
    brief: str,
    sources: Mapping[str, str],
    demands: Demands,
    gate_demand_ids: AbstractSet[str],
    packet: str,
    verdict_path: Path,
    reader_model: str,
    series_name: str,
) -> str:
    """Return the brief with its placeholders filled from the source files by basename in `sources` order, the demands, the packet text, and the verdict path, refusing a brief that breaks the brief rules."""
    _refuse_faulty_brief(brief, (*BRIEF_FORBIDDEN_WORDS, reader_model, series_name))
    fillings = {
        SOURCE_PLACEHOLDER: _binding_text(sources, demands, gate_demand_ids),
        DEMANDS_PLACEHOLDER: _demand_list(demand for demand in demands.demands if isinstance(demand, JudgeDemand)),
        PACKET_PLACEHOLDER: packet,
        OUT_PLACEHOLDER: str(verdict_path),
    }
    return PLACEHOLDER_PATTERN.sub(lambda match: fillings[match.group()], brief)


def _refuse_faulty_brief(brief: str, forbidden_words: Iterable[str]) -> None:
    """Refuse a brief lacking a placeholder once, lacking the oath skill, or naming a forbidden word outside its placeholders."""
    for placeholder in PLACEHOLDERS:
        count = brief.count(placeholder)
        if count != 1:
            raise Refusal(f"brief fault: {placeholder} appears {count} times, not once")
    if OATH_SKILL not in brief:
        raise Refusal(f"brief fault: no {OATH_SKILL}")
    text = PLACEHOLDER_PATTERN.sub("", brief)
    for word in forbidden_words:
        if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text, re.IGNORECASE):
            raise Refusal(f"brief fault: names {word.lower()}")


def _binding_text(sources: Mapping[str, str], demands: Demands, gate_demand_ids: AbstractSet[str]) -> str:
    """Return the text the judge binds to: each source file under its name, or with no source the gate demands."""
    if not sources:
        return _demand_list(demand for demand in demands.demands if demand.id in gate_demand_ids)
    return SOURCE_SEPARATOR.join(_source_file_text(basename, text) for basename, text in sources.items())


def _source_file_text(basename: str, text: str) -> str:
    """Return one source file's name line, a blank line, and its text without frontmatter."""
    return f"Source file: {basename}\n\n{strip_frontmatter(text, f'{SOURCE_FOLDER}/{basename}')}"


def _demand_list(demands: Iterable[Demand]) -> str:
    """Return one entry per demand holding its id, text, and boundary."""
    return "\n".join(f"- id: {demand.id}\n  text: {demand.text}\n  boundary: {demand.boundary}" for demand in demands)


def parse_verdict(document: object, blind_ids: AbstractSet[str], judge_demand_ids: AbstractSet[str]) -> Record:
    """Return the verdict document when it holds every blind id of its packet once, each counting every judge demand, values in range, and raise RecordError otherwise."""
    verdict = parse_record(RecordKind.VERDICT, document)
    _refuse_other_blind_ids(verdict, blind_ids)
    for index, entry in enumerate(verdict["verdicts"]):
        _refuse_other_demands(entry["breaches"], f"{VERDICT_LABEL}.verdicts[{index}].breaches", judge_demand_ids)
    return verdict


def _refuse_other_blind_ids(verdict: Record, blind_ids: AbstractSet[str]) -> None:
    """Raise RecordError when the verdict misses a blind id of the packet or judges one outside it."""
    judged = {entry["id"] for entry in verdict["verdicts"]}
    missing = sorted(blind_ids - judged)
    if missing:
        raise RecordError(f"{VERDICT_LABEL}: missing blind id {missing[0]}")
    foreign = sorted(judged - blind_ids)
    if foreign:
        raise RecordError(f"{VERDICT_LABEL}: blind id {foreign[0]} is not in the packet")


def _refuse_other_demands(breaches: Mapping[str, int], path: str, judge_demand_ids: AbstractSet[str]) -> None:
    """Raise RecordError when a breaches map misses a judge demand or counts another demand."""
    missing = sorted(judge_demand_ids - breaches.keys())
    if missing:
        raise RecordError(f"{path}: missing judge demand {missing[0]}")
    foreign = sorted(breaches.keys() - judge_demand_ids)
    if foreign:
        raise RecordError(f"{path}: {foreign[0]} is not a judge demand")


@dataclass(frozen=True)
class BlindPackets:
    """A revision's packets by id, each its markdown text, and the origin of every blind id they hold."""

    packets: Mapping[str, str]
    origins: Mapping[str, Record]


@dataclass(frozen=True)
class _Entry:
    """One packet entry before blinding: its origin and its exchanges of user message and reply text."""

    origin: Record
    exchanges: tuple[tuple[str, str], ...]


def blind_replies(revision: str, replies: Mapping[ExpectedReply, Record], anchors: Sequence[Record], anchors_per_packet: int, random: Random) -> BlindPackets:
    """Return the revision's packets of its replies, each with `anchors_per_packet` anchors of other tasks, shuffled under blind ids unique in the revision, refusing a packet with too few such anchors."""
    packets: dict[str, str] = {}
    origins: dict[str, Record] = {}
    for packet, (task, keys) in sorted(_replies_by_packet(replies).items()):
        entries = [
            *(_reply_entry(packet, revision, key, replies) for key in keys),
            *(_anchor_entry(packet, anchor) for anchor in _drawn_anchors(packet, task, anchors, anchors_per_packet, random)),
        ]
        random.shuffle(entries)
        sections = []
        for entry in entries:
            blind_id = _fresh_blind_id(origins, random)
            origins[blind_id] = entry.origin
            sections.append(_section(blind_id, entry.exchanges))
        packets[packet] = SECTION_SEPARATOR.join(sections) + "\n"
    return BlindPackets(packets=packets, origins=origins)


def _replies_by_packet(replies: Iterable[ExpectedReply]) -> dict[str, tuple[str, list[ExpectedReply]]]:
    """Group the replies by packet id, each packet paired with the task or conversation it judges."""
    groups: dict[str, tuple[str, list[ExpectedReply]]] = {}
    for key in replies:
        groups.setdefault(_packet_id(key), (key.task, []))[1].append(key)
    return groups


def _packet_id(key: ExpectedReply) -> str:
    """Return the packet a reply goes to: its task's omission packet, its conversation turn's packet, or its task's packet."""
    if key.condition.startswith(OMISSION_PREFIX):
        return f"{key.task}{OMISSIONS_PACKET_SUFFIX}"
    if key.turn is not None:
        return f"{key.task}{TURN_PACKET_INFIX}{key.turn}"
    return key.task


def _reply_entry(packet: str, revision: str, key: ExpectedReply, replies: Mapping[ExpectedReply, Record]) -> _Entry:
    """Return a reply's entry: its origin, and its exchange preceded by the earlier turns of its repeat."""
    record = replies[key]
    origin = {"packet": packet, "condition": key.condition, "task": key.task, "split": record["split"], "repeat": key.repeat}
    if key.turn is not None:
        origin["turn"] = key.turn
    origin["borrowed_from"] = None if key.revision == revision else key.revision
    earlier = [replies[dataclasses.replace(key, turn=turn)] for turn in range(1, key.turn or 1)]
    return _Entry(origin=origin, exchanges=tuple((reply["message"], reply["text"]) for reply in (*earlier, record)))


def _anchor_entry(packet: str, anchor: Record) -> _Entry:
    """Return an anchor's entry: its origin and its one exchange."""
    return _Entry(origin={"packet": packet, ANCHOR_KEY: anchor["id"]}, exchanges=((anchor["message"], anchor["text"]),))


def _drawn_anchors(packet: str, task: str, anchors: Sequence[Record], anchors_per_packet: int, random: Random) -> list[Record]:
    """Draw `anchors_per_packet` anchors of tasks other than `task` at random, refusing the packet when fewer exist."""
    others = [anchor for anchor in anchors if anchor["task"] != task]
    if len(others) < anchors_per_packet:
        raise Refusal(f"too few anchors for {packet}")
    return random.sample(others, anchors_per_packet)


def _fresh_blind_id(taken: Container[str], random: Random) -> str:
    """Return `b` and 8 random hex digits no taken id equals, refusing after `BLIND_ID_DRAWS` taken draws."""
    for _ in range(BLIND_ID_DRAWS):
        blind_id = f"b{random.getrandbits(BLIND_ID_BITS):08x}"
        if blind_id not in taken:
            return blind_id
    raise Refusal("no free blind id")


def _section(blind_id: str, exchanges: Iterable[tuple[str, str]]) -> str:
    """Return an entry's markdown section: its blind id heading, then each user message and reply text."""
    parts = [f"## {blind_id}", *(part for message, text in exchanges for part in (f"### User\n\n{message}", f"### Reply\n\n{text}"))]
    return SECTION_SEPARATOR.join(parts)
