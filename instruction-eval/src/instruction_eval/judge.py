"""Judging: the judge brief, verdict validation, and blinded packets."""

import re
from collections.abc import Iterable, Mapping
from collections.abc import Set as AbstractSet
from pathlib import Path

from instruction_eval.conditions import strip_frontmatter
from instruction_eval.records import Demand, Demands, JudgeDemand, Record, RecordError, RecordKind, Refusal, parse_record

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
