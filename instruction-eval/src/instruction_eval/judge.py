"""Judging: the judge brief, verdict validation, and blinded packets."""

import dataclasses
import json
import re
from collections import deque
from collections.abc import Callable, Container, Iterable, Iterator, Mapping, Sequence
from collections.abc import Set as AbstractSet
from dataclasses import dataclass
from datetime import datetime
from itertools import islice
from pathlib import Path
from random import Random
from statistics import fmean
from typing import TYPE_CHECKING

import yaml

from instruction_eval.conditions import strip_frontmatter
from instruction_eval.coverage import split_sentences
from instruction_eval.records import (
    ANCHOR_KEY,
    ANCHORS_RECORD,
    CALIBRATION_RECORD,
    CONDITIONS_RECORD,
    FIRST_REVISION,
    GATE_RECORD,
    KEY_SEPARATOR,
    TASKS_RECORD,
    Demand,
    Demands,
    JudgeDemand,
    Record,
    RecordError,
    RecordKind,
    Refusal,
    SeriesFolder,
    OPEN_SPLIT,
    SeriesRecords,
    load_record,
    parse_record,
    _attempt_folder,
    sha256,
    write_file,
    write_record,
)
from instruction_eval.tasks import OMISSION_PREFIX, ExpectedReply, expected_replies, refuse_missing_replies

if TYPE_CHECKING:
    from instruction_eval.reader import Transcript, TranscriptReply

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
        packets[packet] = _packet_text(entries, origins, random)
    return BlindPackets(packets=packets, origins=origins)


def _packet_text(entries: list[_Entry], origins: dict[str, Record], random: Random) -> str:
    """Return the entries shuffled into a packet's markdown under fresh blind ids, recording each id's origin in `origins`."""
    random.shuffle(entries)
    sections = []
    for entry in entries:
        blind_id = _fresh_blind_id(origins, random)
        origins[blind_id] = entry.origin
        sections.append(_section(blind_id, entry.exchanges))
    return SECTION_SEPARATOR.join(sections) + "\n"


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


JUDGE_DEFINITION_PREFIX = "ie-judge-"
AGENTS_FOLDER = ".claude/agents"
FAILED_JUDGINGS_BEFORE_RECALIBRATION = 3
RECALIBRATE_REFUSAL = "recalibrate in a new series"


@dataclass(frozen=True)
class AnchorAgreement:
    """How closely a judging counted a packet's anchors: per judge demand the mean breach difference, and the share of anchor `done` values matched."""

    breach_difference: Mapping[str, float]
    done_agreement: float


@dataclass(frozen=True)
class AcceptedJudging:
    """The lowest judging of a packet that passed: its number, judge model, transcript with hash, and anchor agreement."""

    judging: int
    judge_model: str
    transcript: Path
    transcript_hash: str
    anchors: AnchorAgreement


@dataclass(frozen=True)
class PendingJudging:
    """A judging launched whose verdict is still to come."""

    judging: int


@dataclass(frozen=True)
class NeedsJudging:
    """A packet with no accepted or pending judging, the next judging to write being `judging`."""

    judging: int


JudgingState = AcceptedJudging | PendingJudging | NeedsJudging


@dataclass(frozen=True)
class _Judgings:
    """What every judging of one revision is read against: the series files, the revision, the judge transcripts with a way to read them, the origins, the judge model, the anchors' known counts, and the judge demands."""

    files: SeriesFolder
    revision: str
    transcripts: Sequence["Transcript"]
    read_transcript: Callable[[Path], bytes]
    origins: Record
    judge_model: str
    acceptance: Mapping[str, float]
    known_anchors: Mapping[str, Record]
    judge_demand_ids: AbstractSet[str]


def judging_states(
    files: SeriesFolder, revision: str, transcripts: Sequence["Transcript"], read_transcript: Callable[[Path], bytes]
) -> dict[str, JudgingState]:
    """Return each packet of the revision's origins with its judging state, refusing a packet holding three failed judgings."""
    records = SeriesRecords(files)
    origins = records.origins(revision)
    calibration = records.calibration()
    judgings = _Judgings(
        files=files,
        revision=revision,
        transcripts=transcripts,
        read_transcript=read_transcript,
        origins=origins,
        judge_model=calibration["judge_model"],
        acceptance=calibration["acceptance"],
        known_anchors={anchor["id"]: anchor for anchor in records.anchors()["anchors"]},
        judge_demand_ids={demand.id for demand in records.demands().demands if isinstance(demand, JudgeDemand)},
    )
    return {packet: _packet_state(judgings, packet) for packet in sorted(origins["packets"])}


def _packet_state(judgings: _Judgings, packet: str) -> JudgingState:
    """Return the judging state of one packet: its lowest passing judging, else its first pending one, else the next judging to write."""
    numbers = _judging_numbers(judgings.files, judgings.revision, packet)
    outcomes = [_judging_outcome(judgings, packet, number) for number in numbers]
    accepted = [outcome for outcome in outcomes if isinstance(outcome, AcceptedJudging)]
    if accepted:
        return accepted[0]
    pending = [outcome for outcome in outcomes if isinstance(outcome, PendingJudging)]
    if pending:
        return pending[0]
    if outcomes.count(None) >= FAILED_JUDGINGS_BEFORE_RECALIBRATION:
        raise Refusal(RECALIBRATE_REFUSAL)
    return NeedsJudging(len(numbers) + 1)


def _judging_outcome(judgings: _Judgings, packet: str, number: int) -> AcceptedJudging | PendingJudging | None:
    """Return the judging's acceptance, `PendingJudging` while its verdict is awaited, or None when it failed."""
    agent_type = _judging_agent_type(judgings.revision, packet, number)
    reply = _final_reply(judgings, agent_type)
    if not judgings.files.holds(_verdict_file(judgings.revision, packet, number)):
        return None if reply else PendingJudging(number)
    verdict = _valid_verdict(judgings, packet, number)
    if verdict is None or reply is None or reply.model != judgings.judge_model or _is_rejected(judgings, reply, packet, number):
        return None
    anchors = _anchor_agreement(judgings, packet, verdict)
    if not _within_acceptance(anchors, judgings.acceptance):
        return None
    return AcceptedJudging(
        judging=number,
        judge_model=reply.model,
        transcript=reply.transcript,
        transcript_hash=reply.transcript_hash,
        anchors=anchors,
    )


def _judging_agent_type(revision: str, packet: str, number: int) -> str:
    """Return the agent type of judging `number` of a revision's packet."""
    return f"{JUDGE_DEFINITION_PREFIX}{revision}-{packet}-k{number}"


def _verdict_file(revision: str, packet: str, number: int) -> str:
    """Return the series path of judging `number`'s verdict file."""
    return f"{revision}/7-verdicts/{packet}/k{number}.yaml"


def _final_reply(judgings: _Judgings, agent_type: str) -> "TranscriptReply | None":
    """Return the final reply of the agent type's latest transcript, or None when that transcript does not end in one."""
    from instruction_eval.reader import parse_transcript_replies

    transcripts = [transcript for transcript in judgings.transcripts if transcript.agent_type == agent_type]
    if not transcripts:
        return None
    latest = max(transcripts, key=lambda transcript: _start_time(judgings.read_transcript(transcript.path)))
    replies = parse_transcript_replies(latest.path, judgings.read_transcript(latest.path))
    return replies[-1] if replies else None


def _start_time(transcript: bytes) -> datetime:
    """Return the timestamp of the transcript's first line."""
    return datetime.fromisoformat(json.loads(transcript.splitlines()[0])["timestamp"])


def _is_rejected(judgings: _Judgings, reply: "TranscriptReply", packet: str, number: int) -> bool:
    """Tell whether the judge's transcript shows a memory file, SubagentStart text, or a tool use besides loading the oath skill and writing the verdict."""
    from instruction_eval.reader import judge_transcript_rejection

    verdict_path = judgings.files.root / _verdict_file(judgings.revision, packet, number)
    return judge_transcript_rejection(reply.transcript, judgings.read_transcript(reply.transcript), verdict_path) is not None


def _valid_verdict(judgings: _Judgings, packet: str, number: int) -> Record | None:
    """Return the judging's verdict file parsed against the packet's blind ids and the judge demands, or None when it is not valid."""
    try:
        document = yaml.safe_load(judgings.files.read_bytes(_verdict_file(judgings.revision, packet, number)))
        return parse_verdict(document, set(_packet_origins(judgings, packet)), judgings.judge_demand_ids)
    except (yaml.YAMLError, RecordError):
        return None


def _packet_origins(judgings: _Judgings, packet: str) -> dict[str, Record]:
    """Return the origins of the blind ids the packet holds, by blind id."""
    return {blind_id: origin for blind_id, origin in judgings.origins["ids"].items() if origin["packet"] == packet}


def _anchor_agreement(judgings: _Judgings, packet: str, verdict: Record) -> AnchorAgreement:
    """Return how closely the verdict counted the packet's anchors against their known counts."""
    counted = {entry["id"]: entry for entry in verdict["verdicts"]}
    pairs = [
        (counted[blind_id], judgings.known_anchors[origin[ANCHOR_KEY]])
        for blind_id, origin in _packet_origins(judgings, packet).items()
        if ANCHOR_KEY in origin
    ]
    breach_difference = {
        demand: fmean(abs(entry["breaches"][demand] - known["breaches"][demand]) for entry, known in pairs)
        for demand in sorted(judgings.judge_demand_ids)
    }
    decided = [(entry, known) for entry, known in pairs if known["done"] is not None]
    return AnchorAgreement(breach_difference, fmean(entry["done"] == known["done"] for entry, known in decided))


def _within_acceptance(anchors: AnchorAgreement, acceptance: Mapping[str, float]) -> bool:
    """Tell whether every judge demand's breach difference stays within the accepted one and the done agreement reaches the accepted one."""
    return (
        all(difference <= acceptance["breach_difference"] for difference in anchors.breach_difference.values())
        and anchors.done_agreement >= acceptance["done_agreement"]
    )


def _judging_numbers(files: SeriesFolder, revision: str, packet: str) -> list[int]:
    """Return the numbers of the packet's judgings, counted from the definition files whose names match its pattern, ascending."""
    pattern = re.compile(rf"^{JUDGE_DEFINITION_PREFIX}{re.escape(revision)}-{re.escape(packet)}-k([0-9]+)\.md$")
    matches = (pattern.match(path.name) for path in (files.root / AGENTS_FOLDER).glob("*.md"))
    return sorted(int(match.group(1)) for match in matches if match)


BLIND_COMMAND = "revision blind"
INSTRUCTION_FILE = "2-instruction.md"
PACKETS_FOLDER = "6-packets"
ORIGINS_FILE = "6-origins.yaml"
TASK_KEYS = ("tasks", "conversations")
CONDITION_KEYS = ("controls", "aim", "placebo_source", "omissions")


def revision_blind(files: SeriesFolder, revision: str, random: Random) -> None:
    """Write the revision's blinded packets and their origins, a later revision borrowing every control reply from r1, refusing without calibration, a gap in the expected replies, or too few anchors."""
    _refuse_unusable_series(files, BLIND_COMMAND)
    records = SeriesRecords(files)
    calibration = records.calibration()
    expected = _expected_replies(files, revision, records)
    refuse_missing_replies(files, expected)
    replies = {reply: records.reply(reply.path) for reply in expected}
    blinded = blind_replies(revision, replies, records.anchors()["anchors"], calibration["anchors_per_packet"], random)
    _write_packets(files, revision, blinded.packets)
    write_record(files, f"{revision}/{ORIGINS_FILE}", _origins_record(blinded), _blind_reads(revision, expected))


def _refuse_unusable_series(files: SeriesFolder, command: str) -> None:
    """Refuse a folder that is no series, a stopped series, a changed frozen part, or a broken revision chain."""
    from instruction_eval.series import guard_series

    guard_series(files, command)


def _expected_replies(files: SeriesFolder, revision: str, records: SeriesRecords) -> tuple[ExpectedReply, ...]:
    """Return the replies the revision expects, refusing a gate whose repeats are unwritten."""
    repeats = records.gate().repeats
    if repeats is None:
        raise Refusal(f"missing key: {GATE_RECORD}{KEY_SEPARATOR}repeats")
    sentence_count = len(split_sentences(files.read_bytes(f"{revision}/{INSTRUCTION_FILE}")))
    return expected_replies(revision, records.tasks(), records.conditions(), repeats, sentence_count)


def _write_packets(files: SeriesFolder, revision: str, packets: Mapping[str, str]) -> None:
    """Write each packet's text to the revision's packets folder."""
    for packet, text in packets.items():
        write_file(files, f"{revision}/{PACKETS_FOLDER}/{packet}.md", text.encode())


def _origins_record(blinded: BlindPackets) -> dict[str, object]:
    """Return the origins record: every blind id's origin and each packet's hash."""
    return {"ids": blinded.origins, "packets": {packet: sha256(text.encode()) for packet, text in blinded.packets.items()}}


def _blind_reads(revision: str, expected: Iterable[ExpectedReply]) -> list[str]:
    """Return what `revision blind` reads: the task and condition keys, the repeats, the revision's instruction, every expected reply, the calibration, and the anchors."""
    return [
        *(f"{TASKS_RECORD}{KEY_SEPARATOR}{key}" for key in TASK_KEYS),
        *(f"{CONDITIONS_RECORD}{KEY_SEPARATOR}{key}" for key in CONDITION_KEYS),
        f"{GATE_RECORD}{KEY_SEPARATOR}repeats",
        f"{revision}/{INSTRUCTION_FILE}",
        *(reply.path for reply in expected),
        CALIBRATION_RECORD,
        ANCHORS_RECORD,
    ]


CALIBRATE_COMMAND = "judge calibrate"
WORKING_BRIEF = "6-judge/brief.md"
PLAN_FILE = "plan.yaml"
BRIEF_SNAPSHOT_FILE = "brief.md"
ATTEMPT_PATTERN = re.compile(r"attempt-([0-9]+)")
FIRST_ATTEMPT = 1
SAMPLE_PACKET = "sample"
SAMPLE_FILE = "sample.md"
ATTEMPT_ORIGINS_FILE = "origins.yaml"
POOL_EXHAUSTED_REFUSAL = "calibration pool exhausted: lower sample_size or start a new series with more repeats"
OPEN_TASK_REPLY_PATTERN = f"{FIRST_REVISION}/5-replies/*/*/repeat-*.yaml"
REPEAT_FILE_PATTERN = re.compile(r"repeat-([0-9]+)\.yaml")


def calibrate_stage_one(
    files: SeriesFolder, brief_template: Path, environ: Mapping[str, str], home: Path, working_dir: Path, random: Random
) -> str:
    """Run stage one of `judge calibrate` on the latest attempt: snapshot the brief, blind a sample of r1's open replies, write the rating definitions, and return their launch list."""
    _refuse_unusable_series(files, CALIBRATE_COMMAND)
    _refuse_calibrated_series(files)
    attempt = _latest_attempt(files)
    brief = _working_brief(files, brief_template)
    records = SeriesRecords(files)
    plan = records.plan(attempt)
    sample = _draw_sample(_open_task_replies(files), _sampled_earlier(records, attempt), attempt, plan.sample_size)
    replies = {key: _load_reply(files, key.path) for key in sample}
    origins: dict[str, Record] = {}
    sample_text = _packet_text([_reply_entry(SAMPLE_PACKET, FIRST_REVISION, key, replies) for key in sample], origins, random)
    folder = _attempt_folder(attempt)
    write_file(files, f"{folder}/{BRIEF_SNAPSHOT_FILE}", brief)
    write_file(files, f"{folder}/{SAMPLE_FILE}", sample_text.encode())
    write_record(
        files,
        f"{folder}/{ATTEMPT_ORIGINS_FILE}",
        {"ids": origins, "packets": {SAMPLE_PACKET: sha256(sample_text.encode())}},
        [],
    )
    return ""


def _refuse_calibrated_series(files: SeriesFolder) -> None:
    """Refuse a series whose judge is already calibrated."""
    if files.holds(CALIBRATION_RECORD):
        raise Refusal(f"already calibrated: {CALIBRATION_RECORD}")


def _latest_attempt(files: SeriesFolder) -> int:
    """Return the highest attempt number holding a plan, refusing a series without one."""
    folders = (files.root / _attempt_folder(FIRST_ATTEMPT)).parent.glob(f"attempt-*/{PLAN_FILE}")
    numbers = [int(match.group(1)) for folder in folders if (match := ATTEMPT_PATTERN.fullmatch(folder.parent.name))]
    if not numbers:
        raise Refusal(f"missing record: {_attempt_folder(FIRST_ATTEMPT)}/{PLAN_FILE}")
    return max(numbers)


def _working_brief(files: SeriesFolder, brief_template: Path) -> bytes:
    """Return the bytes of the user's working brief, refusing it absent and naming the template to start from."""
    if not files.holds(WORKING_BRIEF):
        raise Refusal(f"missing brief: {WORKING_BRIEF}, start from {brief_template}")
    return files.read_bytes(WORKING_BRIEF)


def _sampled_earlier(records: SeriesRecords, attempt: int) -> set[ExpectedReply]:
    """Return the r1 replies the attempts before `attempt` sampled, read from their origins."""
    return {
        ExpectedReply(FIRST_REVISION, origin["condition"], origin["task"], origin["repeat"], None)
        for earlier in range(FIRST_ATTEMPT, attempt)
        if records.files.holds(f"{_attempt_folder(earlier)}/{ATTEMPT_ORIGINS_FILE}")
        for origin in records.attempt_origins(earlier)["ids"].values()
    }


def _open_task_replies(files: SeriesFolder) -> list[ExpectedReply]:
    """Return every open task reply of r1 other than an omission's, conversation turns excluded."""
    replies = (_reply_of_file(path.relative_to(files.root)) for path in sorted(files.root.glob(OPEN_TASK_REPLY_PATTERN)))
    return [reply for reply in replies if not reply.condition.startswith(OMISSION_PREFIX) and _load_reply(files, reply.path)["split"] == OPEN_SPLIT]


def _reply_of_file(path: Path) -> ExpectedReply:
    """Return the r1 reply a task reply file at the series path holds."""
    _, _, condition, task, name = path.parts
    return ExpectedReply(FIRST_REVISION, condition, task, int(REPEAT_FILE_PATTERN.fullmatch(name).group(1)), None)


def _load_reply(files: SeriesFolder, path: str) -> Record:
    """Return the reply record at the path, refusing it stale or malformed."""
    try:
        return parse_record(RecordKind.REPLY, load_record(files, path))
    except RecordError as error:
        raise Refusal(f"malformed record: {path} ({error})") from None


def _draw_sample(candidates: Sequence[ExpectedReply], taken: AbstractSet[ExpectedReply], attempt: int, sample_size: int) -> list[ExpectedReply]:
    """Draw `sample_size` unsampled candidates round-robin over their conditions in alphabetical order from index `attempt - 1` modulo the condition count, each condition in task then repeat order, refusing a pool too small."""
    unused = [reply for reply in candidates if reply not in taken]
    if len(unused) < sample_size:
        raise Refusal(POOL_EXHAUSTED_REFUSAL)
    conditions = sorted({reply.condition for reply in candidates})
    start = (attempt - 1) % len(conditions)
    queues = [
        deque(sorted((reply for reply in unused if reply.condition == condition), key=lambda reply: (reply.task, reply.repeat)))
        for condition in (*conditions[start:], *conditions[:start])
    ]
    return list(islice(_round_robin(queues), sample_size))


def _round_robin(queues: Sequence[deque[ExpectedReply]]) -> Iterator[ExpectedReply]:
    """Yield one reply from each queue in turn, skipping an emptied queue, until every queue is empty."""
    while any(queues):
        for queue in queues:
            if queue:
                yield queue.popleft()
