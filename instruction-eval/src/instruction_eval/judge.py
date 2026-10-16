"""Judging: the judge brief, verdict validation, and blinded packets."""

import dataclasses
import json
import math
import re
from collections import deque
from collections.abc import Callable, Container, Iterable, Iterator, Mapping, Sequence
from collections.abc import Set as AbstractSet
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import islice
from pathlib import Path
from random import Random
from statistics import fmean, median
from typing import TYPE_CHECKING

import yaml

from instruction_eval.conditions import strip_frontmatter
from instruction_eval.coverage import split_sentences
from instruction_eval.records import (
    AGENTS_FOLDER,
    AGREEMENT_FILE,
    ANCHOR_KEY,
    ANCHORS_RECORD,
    ATTEMPT_FOLDER_PREFIX,
    ATTEMPT_ORIGINS_FILE,
    BRIEF_SNAPSHOT_FILE,
    CALIBRATION_FOLDER,
    CALIBRATION_RECORD,
    COLLECTED_FILE,
    CONDITIONS_RECORD,
    COVERAGE_FILE,
    DEMANDS_RECORD,
    FIRST_ATTEMPT,
    FIRST_REVISION,
    GATE_RECORD,
    INSTRUCTION_FILE,
    KEY_SEPARATOR,
    OPEN_SPLIT,
    ORIGINS_FILE,
    PACKETS_FOLDER,
    PLAN_FILE,
    READER_RECORD,
    REFERENCE_PREFIX,
    REFERENCE_USER_FILE,
    REPEAT_PREFIX,
    REPLIES_FOLDER,
    SAMPLE_FILE,
    SERIES_RECORD,
    SOURCE_FOLDER,
    TASKS_RECORD,
    VERDICTS_FOLDER,
    WORKING_BRIEF,
    Acceptance,
    AgentRaters,
    Demand,
    Demands,
    JudgeDemand,
    Plan,
    Record,
    RecordKind,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    Task,
    attempt_folder,
    load_record,
    parse_record,
    sha256,
    verdict_path,
    write_file,
    write_record,
)
from instruction_eval.tasks import (
    OMISSION_PREFIX,
    ExpectedReply,
    expected_replies,
    refuse_missing_replies,
)

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
    """Return the verdict document when it holds every blind id of its packet once, each counting every judge demand, values in range, and raise Refusal otherwise."""
    verdict = parse_record(RecordKind.VERDICT, document)
    _refuse_other_blind_ids(verdict, blind_ids)
    for index, entry in enumerate(verdict["verdicts"]):
        _refuse_other_demands(entry["breaches"], f"{VERDICT_LABEL}.verdicts[{index}].breaches", judge_demand_ids)
    return verdict


def _refuse_other_blind_ids(verdict: Record, blind_ids: AbstractSet[str]) -> None:
    """Raise Refusal when the verdict misses a blind id of the packet or judges one outside it."""
    judged = {entry["id"] for entry in verdict["verdicts"]}
    missing = sorted(blind_ids - judged)
    if missing:
        raise Refusal(f"{VERDICT_LABEL}: missing blind id {missing[0]}")
    foreign = sorted(judged - blind_ids)
    if foreign:
        raise Refusal(f"{VERDICT_LABEL}: blind id {foreign[0]} is not in the packet")


def _refuse_other_demands(breaches: Mapping[str, int], path: str, judge_demand_ids: AbstractSet[str]) -> None:
    """Raise Refusal when a breaches map misses a judge demand or counts another demand."""
    missing = sorted(judge_demand_ids - breaches.keys())
    if missing:
        raise Refusal(f"{path}: missing judge demand {missing[0]}")
    foreign = sorted(breaches.keys() - judge_demand_ids)
    if foreign:
        raise Refusal(f"{path}: {foreign[0]} is not a judge demand")


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
    return _judging_states(records, revision, records.origins(revision), records.calibration(), transcripts, read_transcript)


def _judging_states(
    records: SeriesRecords,
    revision: str,
    origins: Record,
    calibration: Record,
    transcripts: Sequence["Transcript"],
    read_transcript: Callable[[Path], bytes],
) -> dict[str, JudgingState]:
    """Return each packet of the loaded origins with its judging state under the loaded calibration, refusing a packet holding three failed judgings."""
    judgings = _Judgings(
        files=records.files,
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
    packet_origins = _packet_origins(judgings, packet)
    outcomes = [_judging_outcome(judgings, packet, packet_origins, number) for number in numbers]
    accepted = [outcome for outcome in outcomes if isinstance(outcome, AcceptedJudging)]
    if accepted:
        return accepted[0]
    pending = [outcome for outcome in outcomes if isinstance(outcome, PendingJudging)]
    if pending:
        return pending[0]
    if outcomes.count(None) >= FAILED_JUDGINGS_BEFORE_RECALIBRATION:
        raise Refusal(RECALIBRATE_REFUSAL)
    return NeedsJudging(len(numbers) + 1)


def _judging_outcome(
    judgings: _Judgings, packet: str, packet_origins: Mapping[str, Record], number: int
) -> AcceptedJudging | PendingJudging | None:
    """Return the judging's acceptance, `PendingJudging` while its verdict file is absent and its transcript has not ended, or None when it failed."""
    run = _latest_run(judgings.transcripts, judgings.read_transcript, _judging_agent_type(judgings.revision, packet, number))
    reply = run.reply if run else None
    if not judgings.files.holds(verdict_path(judgings.revision, packet, number)):
        return None if reply else PendingJudging(number)
    verdict = _valid_verdict(judgings, packet_origins, packet, number)
    if verdict is None or run is None or reply is None or reply.model != judgings.judge_model or _is_rejected(judgings, run, packet, number):
        return None
    anchors = _anchor_agreement(judgings, packet, packet_origins, verdict)
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


@dataclass(frozen=True)
class _Run:
    """The latest transcript of a judging: its path, its bytes, and its final reply when it has ended in one."""

    path: Path
    content: bytes
    reply: "TranscriptReply | None"


def _latest_run(transcripts: Sequence["Transcript"], read_transcript: Callable[[Path], bytes], agent_type: str) -> _Run | None:
    """Return the agent type's latest transcript read once, or None when it has no transcript."""
    from instruction_eval.reader import parse_transcript_replies

    contents = {transcript.path: read_transcript(transcript.path) for transcript in transcripts if transcript.agent_type == agent_type}
    if not contents:
        return None
    latest = max(contents, key=lambda path: _start_time(contents[path]))
    replies = parse_transcript_replies(latest, contents[latest])
    return _Run(path=latest, content=contents[latest], reply=replies[-1] if replies else None)


def _start_time(transcript: bytes) -> datetime:
    """Return the timestamp of the transcript's first line, the earliest time for an empty transcript."""
    lines = transcript.splitlines()
    if not lines:
        return datetime.min.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(json.loads(lines[0])["timestamp"])


def _is_rejected(judgings: _Judgings, run: _Run, packet: str, number: int) -> bool:
    """Tell whether the judge's transcript shows a memory file, SubagentStart text, or a tool use besides loading the oath skill and writing the verdict."""
    from instruction_eval.reader import judge_transcript_rejection

    verdict_file = judgings.files.root / verdict_path(judgings.revision, packet, number)
    return judge_transcript_rejection(run.path, run.content, verdict_file) is not None


def _valid_verdict(judgings: _Judgings, packet_origins: Mapping[str, Record], packet: str, number: int) -> Record | None:
    """Return the judging's verdict file parsed against the packet's blind ids and the judge demands, or None when it is not valid."""
    try:
        document = yaml.safe_load(judgings.files.read_bytes(verdict_path(judgings.revision, packet, number)))
        return parse_verdict(document, set(packet_origins), judgings.judge_demand_ids)
    except (yaml.YAMLError, Refusal):
        return None


def _packet_origins(judgings: _Judgings, packet: str) -> dict[str, Record]:
    """Return the origins of the blind ids the packet holds, by blind id."""
    return {blind_id: origin for blind_id, origin in judgings.origins["ids"].items() if origin["packet"] == packet}


def _anchor_agreement(judgings: _Judgings, packet: str, packet_origins: Mapping[str, Record], verdict: Record) -> AnchorAgreement:
    """Return how closely the verdict counted the packet's anchors against their known counts, refusing a packet with no anchor or none of known done value."""
    counted = {entry["id"]: entry for entry in verdict["verdicts"]}
    pairs = [
        (counted[blind_id], judgings.known_anchors[origin[ANCHOR_KEY]])
        for blind_id, origin in packet_origins.items()
        if ANCHOR_KEY in origin
    ]
    if not pairs:
        raise Refusal(f"no anchor in {packet}")
    decided = [(entry, known) for entry, known in pairs if known["done"] is not None]
    if not decided:
        raise Refusal(f"no anchor with a known done value in {packet}")
    breach_difference = {
        demand: fmean(abs(entry["breaches"][demand] - known["breaches"][demand]) for entry, known in pairs)
        for demand in sorted(judgings.judge_demand_ids)
    }
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
    write_record(files, f"{revision}/{ORIGINS_FILE}", _origins_record(blinded.origins, blinded.packets), _blind_reads(revision, expected))


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


def _origins_record(origins: Mapping[str, Record], packets: Mapping[str, str]) -> dict[str, object]:
    """Return the origins record: every blind id's origin and each packet's hash."""
    return {"ids": origins, "packets": {packet: sha256(text.encode()) for packet, text in packets.items()}}


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
ATTEMPT_PATTERN = re.compile(rf"{ATTEMPT_FOLDER_PREFIX}([0-9]+)")
CALIBRATION_AGENT_PREFIX = "ie-calib-"
CANDIDATE_NAME = "candidate"
RATER_NAME = "rater"
CANDIDATE_RUNS = (1, 2)
RATER_RUNS = (1, 2)
LAUNCHES_KEY = "launches"
AGENT_TYPE_KEY = "agent_type"
SAMPLE_PACKET = "sample"
POOL_EXHAUSTED_REFUSAL = "calibration pool exhausted: lower sample_size or start a new series with more repeats"
OPEN_TASK_REPLY_PATTERN = f"{FIRST_REVISION}/{REPLIES_FOLDER}/*/*/{REPEAT_PREFIX}*.yaml"
REPEAT_FILE_PATTERN = re.compile(rf"{REPEAT_PREFIX}([0-9]+)\.yaml")


def calibrate_stage_one(
    files: SeriesFolder, brief_template: Path, environ: Mapping[str, str], home: Path, working_dir: Path, random: Random
) -> str:
    """Run stage one of `judge calibrate` on the latest attempt: snapshot the brief, blind a sample of r1's open replies, write the rating definitions, and return their launch list."""
    _refuse_unusable_series(files, CALIBRATE_COMMAND)
    _refuse_calibrated_series(files)
    attempt = _latest_attempt(files)
    brief = _working_brief(files, brief_template)
    _refuse_outside_neutral_login(environ, home, working_dir)
    records = SeriesRecords(files)
    plan = records.plan(attempt)
    earlier = _earlier_attempts_with_origins(files, attempt)
    sample = _blind_sample(files, _sampled_by(records, earlier), attempt, plan.sample_size, random)
    ratings = _ratings(attempt, plan)
    folder = attempt_folder(attempt)
    definitions = {rating.agent_type: _rating_definition(files, records, folder, brief.decode(), sample.text, sample.reader_model, rating) for rating in ratings}
    write_file(files, f"{folder}/{BRIEF_SNAPSHOT_FILE}", brief)
    write_file(files, f"{folder}/{SAMPLE_FILE}", sample.text.encode())
    write_record(files, f"{folder}/{ATTEMPT_ORIGINS_FILE}", _origins_record(sample.origins, {SAMPLE_PACKET: sample.text}), _stage_one_reads(files, records, attempt, sample.replies, earlier))
    for name, definition in definitions.items():
        write_file(files, f"{AGENTS_FOLDER}/{name}.md", definition)
    return _launch_list(definitions)


@dataclass(frozen=True)
class _BlindSample:
    """An attempt's sample: the replies drawn, the model that served them, the packet text, and the origin of every blind id."""

    replies: tuple[ExpectedReply, ...]
    reader_model: str
    text: str
    origins: Mapping[str, Record]


def _blind_sample(files: SeriesFolder, taken: AbstractSet[ExpectedReply], attempt: int, sample_size: int, random: Random) -> _BlindSample:
    """Draw the attempt's sample of r1's open task replies and blind it into one packet."""
    drawn = _draw_sample(_open_task_replies(files), taken, attempt, sample_size)
    records = {key: _load_reply(files, key.path) for key in drawn}
    origins: dict[str, Record] = {}
    text = _packet_text([_reply_entry(SAMPLE_PACKET, FIRST_REVISION, key, records) for key in drawn], origins, random)
    return _BlindSample(replies=tuple(drawn), reader_model=_serving_model(records.values()), text=text, origins=origins)


def _serving_model(replies: Iterable[Record]) -> str:
    """Return the model that served the sampled replies, the one every r1 reply of the series shares."""
    return next(iter(replies))["model"]


@dataclass(frozen=True)
class _Rating:
    """One rating an attempt asks of an agent: its agent type, its model, and the file it writes."""

    agent_type: str
    model: str
    file: str


def _ratings(attempt: int, plan: Plan) -> list[_Rating]:
    """Return the ratings the plan asks of agents: the candidate judge twice, and with agent raters each rater once."""
    return [*_candidate_ratings(attempt, plan), *_agent_rater_ratings(attempt, plan)]


def _candidate_ratings(attempt: int, plan: Plan) -> list[_Rating]:
    """Return the candidate judge's two ratings."""
    return [_Rating(f"{CALIBRATION_AGENT_PREFIX}{attempt}-{CANDIDATE_NAME}-{run}", plan.judge_model, f"{CANDIDATE_NAME}-{run}.yaml") for run in CANDIDATE_RUNS]


def _agent_rater_ratings(attempt: int, plan: Plan) -> list[_Rating]:
    """Return each agent rater's rating, none when the user rates."""
    if not isinstance(plan.raters, AgentRaters):
        return []
    return [_Rating(f"{CALIBRATION_AGENT_PREFIX}{attempt}-{RATER_NAME}-{run}", plan.raters.rater_model, f"{REFERENCE_PREFIX}{RATER_NAME}-{run}.yaml") for run in RATER_RUNS]


def _rating_definition(files: SeriesFolder, records: SeriesRecords, folder: str, brief: str, sample: str, reader_model: str, rating: _Rating) -> bytes:
    """Return the rating's agent definition, its body the attempt's brief rendered for the sample and the rating's file."""
    return _judging_definition(files, records, brief, sample, Path(f"{files.root}/{folder}/{rating.file}"), reader_model, rating.agent_type, rating.model)


def _judging_definition(
    files: SeriesFolder, records: SeriesRecords, brief: str, packet: str, verdict_path: Path, reader_model: str, agent_type: str, model: str
) -> bytes:
    """Return the definition of a judge or rater agent running `model`, its body the brief rendered for the packet text and the verdict path."""
    sources = {source.name: files.read_bytes(f"{SOURCE_FOLDER}/{source.name}").decode() for source in records.series().sources}
    body = render_brief(brief, sources, records.demands(), _gate_demand_ids_without_sources(records), packet, verdict_path, reader_model, files.root.name)
    from instruction_eval.reader import AgentKind, render_agent_definition

    return render_agent_definition(agent_type, model, AgentKind.JUDGE, body.encode())


def _refuse_outside_neutral_login(environ: Mapping[str, str], home: Path, working_dir: Path) -> None:
    """Refuse a session outside the neutral login or a working directory under a memory file."""
    from instruction_eval.reader import check_neutral_login

    check_neutral_login(environ, home, working_dir)


def _refuse_calibrated_series(files: SeriesFolder) -> None:
    """Refuse a series whose judge is already calibrated."""
    if files.holds(CALIBRATION_RECORD):
        raise Refusal(f"already calibrated: {CALIBRATION_RECORD}")


def _latest_attempt(files: SeriesFolder) -> int:
    """Return the highest attempt number holding a plan, refusing a series without one."""
    folders = (files.root / CALIBRATION_FOLDER).glob(f"{ATTEMPT_FOLDER_PREFIX}*/{PLAN_FILE}")
    numbers = [int(match.group(1)) for folder in folders if (match := ATTEMPT_PATTERN.fullmatch(folder.parent.name))]
    if not numbers:
        raise Refusal(f"missing record: {attempt_folder(FIRST_ATTEMPT)}/{PLAN_FILE}")
    return max(numbers)


def _working_brief(files: SeriesFolder, brief_template: Path) -> bytes:
    """Return the bytes of the user's working brief, refusing it absent and naming the template to start from."""
    if not files.holds(WORKING_BRIEF):
        raise Refusal(f"missing brief: {WORKING_BRIEF}, start from {brief_template}")
    return files.read_bytes(WORKING_BRIEF)


def _earlier_attempts_with_origins(files: SeriesFolder, attempt: int) -> list[int]:
    """Return the numbers of the attempts before `attempt` that wrote origins."""
    return [earlier for earlier in range(FIRST_ATTEMPT, attempt) if files.holds(f"{attempt_folder(earlier)}/{ATTEMPT_ORIGINS_FILE}")]


def _sampled_by(records: SeriesRecords, attempts: Iterable[int]) -> set[ExpectedReply]:
    """Return the r1 replies the given attempts sampled, read from their origins."""
    return {reply for attempt in attempts for reply in _sampled_replies(records.attempt_origins(attempt)).values()}


def _sampled_replies(origins: Record) -> dict[str, ExpectedReply]:
    """Return the r1 reply each blind id of an attempt's origins names."""
    return {blind_id: ExpectedReply(FIRST_REVISION, origin["condition"], origin["task"], origin["repeat"], None) for blind_id, origin in origins["ids"].items()}


def _gate_demand_ids_without_sources(records: SeriesRecords) -> frozenset[str]:
    """Return the ids of the demands r1's coverage keeps when the series has no source, none when it has one."""
    if records.series().sources:
        return frozenset()
    return frozenset(records.gate_demands())


def _stage_one_reads(files: SeriesFolder, records: SeriesRecords, attempt: int, sample: Sequence[ExpectedReply], earlier: Iterable[int]) -> list[str]:
    """Return what stage one reads: the series records, the plan's keys, the brief snapshot, the sample, the sampled replies, and the earlier origins."""
    folder = attempt_folder(attempt)
    sources = records.series().sources
    plan_keys = yaml.safe_load(files.read_bytes(f"{folder}/{PLAN_FILE}"))
    return [
        SERIES_RECORD,
        *(f"{SOURCE_FOLDER}/{source.name}" for source in sources),
        *([] if sources else [f"{FIRST_REVISION}/{COVERAGE_FILE}{KEY_SEPARATOR}demands"]),
        f"{DEMANDS_RECORD}{KEY_SEPARATOR}demands",
        *(f"{folder}/{PLAN_FILE}{KEY_SEPARATOR}{key}" for key in plan_keys),
        f"{folder}/{BRIEF_SNAPSHOT_FILE}",
        f"{folder}/{SAMPLE_FILE}",
        *(reply.path for reply in sample),
        *(f"{attempt_folder(number)}/{ATTEMPT_ORIGINS_FILE}" for number in earlier),
    ]


def _open_task_replies(files: SeriesFolder) -> list[ExpectedReply]:
    """Return every open task reply of r1 other than an omission's, conversation turns excluded."""
    replies = (_reply_of_file(path.relative_to(files.root)) for path in sorted(files.root.glob(OPEN_TASK_REPLY_PATTERN)))
    return [reply for reply in replies if not reply.condition.startswith(OMISSION_PREFIX) and _load_reply(files, reply.path)["split"] == OPEN_SPLIT]


def _reply_of_file(path: Path) -> ExpectedReply:
    """Return the r1 reply a task reply file at the series path holds, refusing a repeat that is no number."""
    _, _, condition, task, name = path.parts
    repeat = REPEAT_FILE_PATTERN.fullmatch(name)
    if repeat is None:
        raise Refusal(f"malformed reply file: {path}")
    return ExpectedReply(FIRST_REVISION, condition, task, int(repeat.group(1)), None)


def _load_reply(files: SeriesFolder, path: str) -> Record:
    """Return the reply record at the path, refusing it stale or malformed."""
    document = load_record(files, path)
    try:
        return parse_record(RecordKind.REPLY, document)
    except Refusal as error:
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


JUDGE_PREPARE_COMMAND = "judge prepare"


def judge_prepare(
    files: SeriesFolder,
    revision: str,
    environ: Mapping[str, str],
    home: Path,
    working_dir: Path,
    transcripts: Sequence["Transcript"],
    read_transcript: Callable[[Path], bytes],
) -> str:
    """Write the next judging of each packet with no accepted or pending judging and return a pending line per packet awaiting its judge, then the launch list of the judgings written."""
    _refuse_unusable_series(files, JUDGE_PREPARE_COMMAND)
    _refuse_outside_neutral_login(environ, home, working_dir)
    records = SeriesRecords(files)
    origins = records.origins(revision)
    calibration = records.calibration()
    states = _judging_states(records, revision, origins, calibration, transcripts, read_transcript)
    needed = [(packet, state.judging) for packet, state in states.items() if isinstance(state, NeedsJudging)]
    definitions = _judge_definitions(files, records, revision, origins, calibration, needed)
    for agent_type, definition in definitions.items():
        write_file(files, f"{AGENTS_FOLDER}/{agent_type}.md", definition)
    pending = "".join(f"judging k{state.judging} pending: {packet}\n" for packet, state in states.items() if isinstance(state, PendingJudging))
    return pending + _launch_list(definitions)


def _judge_definitions(
    files: SeriesFolder, records: SeriesRecords, revision: str, origins: Record, calibration: Record, judgings: Iterable[tuple[str, int]]
) -> dict[str, bytes]:
    """Return by agent type the definition of each given judging of a packet, its body the accepted brief rendered for the packet and the judging's verdict path."""
    brief = _accepted_brief(files, calibration)
    packets = _blinded_packets(files, revision, origins)
    reader_model = records.reader().model
    definitions = {}
    for packet, judging in judgings:
        agent_type = _judging_agent_type(revision, packet, judging)
        verdict_file = files.root / verdict_path(revision, packet, judging)
        definitions[agent_type] = _judging_definition(files, records, brief, packets[packet], verdict_file, reader_model, agent_type, calibration["judge_model"])
    return definitions


def _blinded_packets(files: SeriesFolder, revision: str, origins: Record) -> dict[str, str]:
    """Return the text of each packet the revision's origins hash, by packet id, refusing a packet whose bytes no longer hash as blinded."""
    return {packet: _blinded_packet(files, revision, packet, packet_hash) for packet, packet_hash in origins["packets"].items()}


def _blinded_packet(files: SeriesFolder, revision: str, packet: str, packet_hash: str) -> str:
    """Return the packet's text, refusing it missing, or edited when its bytes differ from the hash its origins hold."""
    path = f"{revision}/{PACKETS_FOLDER}/{packet}.md"
    if not files.holds(path):
        raise Refusal(f"missing packet: {path}")
    content = files.read_bytes(path)
    if sha256(content) != packet_hash:
        raise Refusal(f"edited packet: {path} (hash differs from {revision}/{ORIGINS_FILE})")
    return content.decode()


def _accepted_brief(files: SeriesFolder, calibration: Record) -> str:
    """Return the brief snapshot of the attempt the calibration accepted."""
    return files.read_bytes(f"{attempt_folder(calibration['attempt'])}/{BRIEF_SNAPSHOT_FILE}").decode()


JUDGE_COLLECT_COMMAND = "judge collect"


def judge_collect(files: SeriesFolder, revision: str, transcripts: Sequence["Transcript"], read_transcript: Callable[[Path], bytes]) -> str:
    """Write the revision's collection of every packet's accepted judging and return nothing, or return the packets to re-judge, refusing a pending judging."""
    _refuse_unusable_series(files, JUDGE_COLLECT_COMMAND)
    records = SeriesRecords(files)
    origins = records.origins(revision)
    calibration = records.calibration()
    _refuse_edited_judge_definitions(files, records, revision, origins, calibration)
    states = _judging_states(records, revision, origins, calibration, transcripts, read_transcript)
    _refuse_pending_judgings(states)
    unjudged = [packet for packet, state in states.items() if isinstance(state, NeedsJudging)]
    if unjudged:
        return "".join(f"re-judge: {packet}\n" for packet in unjudged)
    accepted = {packet: state for packet, state in states.items() if isinstance(state, AcceptedJudging)}
    write_record(files, f"{revision}/{COLLECTED_FILE}", _collected_record(accepted), _collect_reads(files, records, revision, origins, calibration))
    return ""


def _refuse_edited_judge_definitions(files: SeriesFolder, records: SeriesRecords, revision: str, origins: Record, calibration: Record) -> None:
    """Refuse a judge definition of the revision whose bytes differ from its recomputation from the accepted brief and its packet."""
    from instruction_eval.reader import _refuse_edited_file

    written = [(packet, judging) for packet in origins["packets"] for judging in _judging_numbers(files, revision, packet)]
    for agent_type, recomputed in _judge_definitions(files, records, revision, origins, calibration, written).items():
        _refuse_edited_file(files, f"{AGENTS_FOLDER}/{agent_type}.md", recomputed)


def _refuse_pending_judgings(states: Mapping[str, JudgingState]) -> None:
    """Refuse naming the first packet whose judging is pending."""
    pending = next((packet for packet, state in states.items() if isinstance(state, PendingJudging)), None)
    if pending is not None:
        raise Refusal(f"judging pending: {pending}")


def _collected_record(accepted: Mapping[str, AcceptedJudging]) -> dict[str, object]:
    """Return the collection: per packet its accepted judging's number, judge model, transcript with hash, and anchor agreement."""
    return {
        "packets": {
            packet: {
                "accepted": judging.judging,
                "judge_model": judging.judge_model,
                "transcript": str(judging.transcript),
                "transcript_hash": judging.transcript_hash,
                "anchors": dataclasses.asdict(judging.anchors),
            }
            for packet, judging in accepted.items()
        }
    }


def _collect_reads(files: SeriesFolder, records: SeriesRecords, revision: str, origins: Record, calibration: Record) -> list[str]:
    """Return what `judge collect` reads: the series, its sources or without one r1's coverage demands, the demands, the reader model, the calibration with its accepted brief, the anchors, the revision's packets, origins, and verdicts, and its judge definitions."""
    sources = records.series().sources
    return [
        SERIES_RECORD,
        *(f"{SOURCE_FOLDER}/{source.name}" for source in sources),
        *([] if sources else [f"{FIRST_REVISION}/{COVERAGE_FILE}{KEY_SEPARATOR}demands"]),
        f"{DEMANDS_RECORD}{KEY_SEPARATOR}demands",
        f"{READER_RECORD}{KEY_SEPARATOR}model",
        CALIBRATION_RECORD,
        f"{attempt_folder(calibration['attempt'])}/{BRIEF_SNAPSHOT_FILE}",
        ANCHORS_RECORD,
        *(f"{revision}/{PACKETS_FOLDER}/{packet}.md" for packet in origins["packets"]),
        f"{revision}/{ORIGINS_FILE}",
        *series_paths(files, f"{revision}/{VERDICTS_FOLDER}/**/*.yaml"),
        *series_paths(files, f"{AGENTS_FOLDER}/{JUDGE_DEFINITION_PREFIX}{revision}-*.md"),
    ]


def series_paths(files: SeriesFolder, pattern: str) -> list[str]:
    """Return the series path of every file the glob pattern matches, in path order."""
    return sorted(path.relative_to(files.root).as_posix() for path in files.root.glob(pattern) if path.is_file())


def _launch_list(agent_types: Iterable[str]) -> str:
    """Return the launch list naming each agent type in order."""
    return yaml.safe_dump({LAUNCHES_KEY: [{AGENT_TYPE_KEY: agent_type} for agent_type in agent_types]}, sort_keys=False)


NO_REFERENCE_DONE_REFUSAL = "no reference done in the sample"
HALF = 0.5
PLAN_COPIED_KEYS = ("judge_model", "raters", "sample_size", "anchors_per_packet", "acceptance")


@dataclass(frozen=True)
class _Reference:
    """The raters' reference for one sampled reply: its breach count per judge demand and its done value, null when the raters differ."""

    breaches: Mapping[str, float]
    done: bool | None


@dataclass(frozen=True)
class _Differences:
    """How far one judge demand's candidate counts lie from the reference and from each other, named as the acceptance names its limits."""

    breach_difference: float
    self_difference: float


@dataclass(frozen=True)
class _Measures:
    """An attempt's agreement: the differences per judge demand, the done agreement, and the scale, null when the reference counts no breach."""

    demands: Mapping[str, _Differences]
    done_agreement: float
    scale: float | None


def calibrate_stage_two(files: SeriesFolder, transcripts: Sequence["Transcript"], read_transcript: Callable[[Path], bytes]) -> str:
    """Run stage two of `judge calibrate` on the latest attempt: score its candidate ratings against the raters' reference, write its agreement, and on acceptance the calibration and the anchors, returning the attempt's acceptance or rejection."""
    _refuse_unusable_series(files, CALIBRATE_COMMAND)
    _refuse_calibrated_series(files)
    attempt = _latest_attempt(files)
    folder = attempt_folder(attempt)
    records = SeriesRecords(files)
    plan = records.plan(attempt)
    sampled = _sampled_replies(records.attempt_origins(attempt))
    candidates, raters = _candidate_ratings(attempt, plan), _agent_rater_ratings(attempt, plan)
    agent_ratings = [*candidates, *raters]
    reference_files = [rating.file for rating in raters] if raters else [REFERENCE_USER_FILE]
    _refuse_missing_ratings(files, folder, [*(rating.file for rating in candidates), *reference_files])
    replies = {blind_id: _load_reply(files, reply.path) for blind_id, reply in sampled.items()}
    _refuse_edited_rating_definitions(files, records, folder, agent_ratings, _serving_model(replies.values()))
    runs = {rating.file: _rating_run(files, folder, rating, transcripts, read_transcript) for rating in agent_ratings}
    judge_demand_ids = sorted(demand.id for demand in records.demands().demands if isinstance(demand, JudgeDemand))
    entries = {name: _rating_entries(files, folder, name, sampled.keys(), set(judge_demand_ids)) for name in [*runs, *reference_files]}
    reference = _reference([entries[name] for name in reference_files], judge_demand_ids)
    measures = _agreement([entries[rating.file] for rating in candidates], reference, judge_demand_ids)
    anchors = _anchors(reference, replies)
    reads = _stage_two_reads(files, records, attempt, list(sampled.values()), agent_ratings, reference_files)
    write_record(files, f"{folder}/{AGREEMENT_FILE}", {**dataclasses.asdict(measures), "ratings": runs}, reads)
    rejection = _threshold_miss(measures, plan.acceptance) or _anchor_shortfall(anchors, records.tasks().tasks, plan.anchors_per_packet)
    if rejection:
        return f"rejected: attempt {attempt} ({rejection})\n"
    write_record(files, ANCHORS_RECORD, {"anchors": anchors}, reads)
    write_record(files, CALIBRATION_RECORD, _calibration_record(files, records, attempt, plan), reads)
    return f"accepted: attempt {attempt}\n"


def _refuse_missing_ratings(files: SeriesFolder, folder: str, names: Iterable[str]) -> None:
    """Refuse an attempt lacking a rating file, listing each one missing."""
    missing = [f"{folder}/{name}" for name in names if not files.holds(f"{folder}/{name}")]
    if missing:
        raise Refusal("\n".join(f"missing rating: {path}" for path in missing))


def _refuse_edited_rating_definitions(files: SeriesFolder, records: SeriesRecords, folder: str, ratings: Iterable[_Rating], reader_model: str) -> None:
    """Refuse a rating definition whose bytes differ from its recomputation from the attempt's brief snapshot and sample."""
    from instruction_eval.reader import _refuse_edited_file

    brief = files.read_bytes(f"{folder}/{BRIEF_SNAPSHOT_FILE}").decode()
    sample = files.read_bytes(f"{folder}/{SAMPLE_FILE}").decode()
    for rating in ratings:
        _refuse_edited_file(files, f"{AGENTS_FOLDER}/{rating.agent_type}.md", _rating_definition(files, records, folder, brief, sample, reader_model, rating))


def _rating_run(
    files: SeriesFolder, folder: str, rating: _Rating, transcripts: Sequence["Transcript"], read_transcript: Callable[[Path], bytes]
) -> dict[str, str]:
    """Return the model, transcript, and transcript hash of the agent that wrote the rating, refusing a rating without an ended transcript, from another model, or whose transcript rejects it."""
    from instruction_eval.reader import judge_transcript_rejection

    path = f"{folder}/{rating.file}"
    run = _latest_run(transcripts, read_transcript, rating.agent_type)
    if run is None or run.reply is None:
        raise Refusal(f"invalid rating: {path} (no ended transcript of {rating.agent_type})")
    if run.reply.model != rating.model:
        raise Refusal(f"invalid rating: {path} (model {run.reply.model}, not {rating.model})")
    rejection = judge_transcript_rejection(run.path, run.content, files.root / path)
    if rejection is not None:
        raise Refusal(f"invalid rating: {path} ({rejection})")
    return {"model": run.reply.model, "transcript": str(run.reply.transcript), "transcript_hash": run.reply.transcript_hash}


def _rating_entries(files: SeriesFolder, folder: str, name: str, blind_ids: AbstractSet[str], judge_demand_ids: AbstractSet[str]) -> dict[str, Record]:
    """Return the rating file's entries by blind id, refusing a rating that is not a valid verdict of the sample."""
    path = f"{folder}/{name}"
    try:
        verdict = parse_verdict(yaml.safe_load(files.read_bytes(path)), blind_ids, judge_demand_ids)
    except (yaml.YAMLError, Refusal) as error:
        raise Refusal(f"invalid rating: {path} ({error})") from None
    return {entry["id"]: entry for entry in verdict["verdicts"]}


def _reference(ratings: Sequence[Mapping[str, Record]], judge_demand_ids: Sequence[str]) -> dict[str, _Reference]:
    """Return each sampled reply's reference: per judge demand the raters' median count, and their common done value or null."""
    return {
        blind_id: _Reference(
            breaches={demand: median(rating[blind_id]["breaches"][demand] for rating in ratings) for demand in judge_demand_ids},
            done=_common_value([rating[blind_id]["done"] for rating in ratings]),
        )
        for blind_id in sorted(ratings[0])
    }


def _common_value(values: Sequence[bool | None]) -> bool | None:
    """Return the value every rater gave, or None when they differ."""
    return values[0] if len(set(values)) == 1 else None


def _agreement(candidates: Sequence[Mapping[str, Record]], reference: Mapping[str, _Reference], judge_demand_ids: Sequence[str]) -> _Measures:
    """Return how closely the candidate's two runs match the reference and each other per judge demand, their done agreement, and their scale, refusing a sample without a reference done value."""
    decided = [blind_id for blind_id, known in reference.items() if known.done is not None]
    if not decided:
        raise Refusal(NO_REFERENCE_DONE_REFUSAL)
    first, second = candidates
    demands = {
        demand: _Differences(
            breach_difference=fmean(abs(fmean(run[blind_id]["breaches"][demand] for run in candidates) - known.breaches[demand]) for blind_id, known in reference.items()),
            self_difference=fmean(abs(first[blind_id]["breaches"][demand] - second[blind_id]["breaches"][demand]) for blind_id in reference),
        )
        for demand in judge_demand_ids
    }
    done_agreement = fmean(fmean(run[blind_id]["done"] == reference[blind_id].done for blind_id in decided) for run in candidates)
    return _Measures(demands=demands, done_agreement=done_agreement, scale=_scale(candidates, reference, judge_demand_ids))


def _scale(candidates: Sequence[Mapping[str, Record]], reference: Mapping[str, _Reference], judge_demand_ids: Sequence[str]) -> float | None:
    """Return the candidate's mean count over the reference mean count, or None when the reference mean is zero."""
    reference_mean = fmean(known.breaches[demand] for known in reference.values() for demand in judge_demand_ids)
    if reference_mean == 0:
        return None
    return fmean(run[blind_id]["breaches"][demand] for run in candidates for blind_id in reference for demand in judge_demand_ids) / reference_mean


def _anchors(reference: Mapping[str, _Reference], replies: Mapping[str, Record]) -> list[dict[str, object]]:
    """Return an anchor of each sampled reply with a reference done value, its known counts the reference counts rounded half away from zero."""
    return [
        {
            "id": blind_id,
            "task": replies[blind_id]["task"],
            "message": replies[blind_id]["message"],
            "text": replies[blind_id]["text"],
            "breaches": {demand: _rounded_half_away_from_zero(count) for demand, count in known.breaches.items()},
            "done": known.done,
        }
        for blind_id, known in reference.items()
        if known.done is not None
    ]


def _rounded_half_away_from_zero(value: float) -> int:
    """Return the value rounded to the nearest integer, a half rounded away from zero."""
    return int(math.copysign(math.floor(abs(value) + HALF), value))


def _threshold_miss(measures: _Measures, acceptance: Acceptance) -> str | None:
    """Return the first measure that misses the acceptance, or None when every one meets it."""
    for demand, differences in measures.demands.items():
        for measure in dataclasses.fields(_Differences):
            value, limit = getattr(differences, measure.name), getattr(acceptance, measure.name)
            if value > limit:
                return f"{measure.name} of {demand} {value} over {limit}"
    if measures.done_agreement < acceptance.done_agreement:
        return f"done_agreement {measures.done_agreement} under {acceptance.done_agreement}"
    return None


def _anchor_shortfall(anchors: Sequence[Record], tasks: Iterable[Task], anchors_per_packet: int) -> str | None:
    """Return the first task with fewer than `anchors_per_packet` anchors of other tasks, or None when none has."""
    for task in tasks:
        if sum(anchor["task"] != task.id for anchor in anchors) < anchors_per_packet:
            return f"too few anchors for {task.id}"
    return None


def _calibration_record(files: SeriesFolder, records: SeriesRecords, attempt: int, plan: Plan) -> dict[str, object]:
    """Return the calibration of the accepted attempt: its plan, its brief snapshot's hash, and its agreement."""
    folder = attempt_folder(attempt)
    plan_keys = yaml.safe_load(files.read_bytes(f"{folder}/{PLAN_FILE}"))
    return {
        "attempt": attempt,
        **{key: plan_keys[key] for key in PLAN_COPIED_KEYS},
        "brief_hash": sha256(files.read_bytes(f"{folder}/{BRIEF_SNAPSHOT_FILE}")),
        "agreement": records.agreement(attempt),
    }


def _stage_two_reads(
    files: SeriesFolder, records: SeriesRecords, attempt: int, sampled: Sequence[ExpectedReply], ratings: Sequence[_Rating], reference_files: Iterable[str]
) -> list[str]:
    """Return what stage two reads: what stage one read, the attempt's origins, the rating files, the rating definitions, and the tasks."""
    folder = attempt_folder(attempt)
    rating_files = {rating.file for rating in ratings} | set(reference_files)
    return [
        *_stage_one_reads(files, records, attempt, sampled, _earlier_attempts_with_origins(files, attempt)),
        f"{folder}/{ATTEMPT_ORIGINS_FILE}",
        *(f"{folder}/{name}" for name in sorted(rating_files)),
        *(f"{AGENTS_FOLDER}/{rating.agent_type}.md" for rating in ratings),
        f"{TASKS_RECORD}{KEY_SEPARATOR}tasks",
    ]
