"""Coverage of an instruction's demands by its sentences."""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import accumulate

from instruction_eval.records import (
    COVERAGE_FILE,
    FIRST_REVISION,
    INSTRUCTION_FILE,
    Coverage,
    Demands,
    Dropped,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    read_series_file,
)

_SENTENCE_END = re.compile(rb"""[.!?]["')\]]*(?=\s|\Z)""")
_WORD_RUN = re.compile(r"(?:[^\W\d_]|\.)*")
_ABBREVIATIONS = {"e.g", "i.e", "etc", "vs", "cf", "Mr", "Mrs", "Dr", "St", "No"}
_SINGLE_LETTER = re.compile(r"[^\W\d_]")
_WHOLE_LINE_UNIT = re.compile(rb"\s*(?:[#|>]|([-*_])(?:[ \t]*\1){2,}\s*\Z)")
CODE_FENCE_OPENING = r"\s*(`{3,}|~{3,})"
_FENCE_OPEN = re.compile(CODE_FENCE_OPENING.encode())
FRONTMATTER_FENCE = "---"
_FRONTMATTER_FENCE_BYTES = FRONTMATTER_FENCE.encode()
_LIST_MARKER = re.compile(rb"\s*(?:[-*+]|\d+[.)])(?:[ \t]+|\Z)")
_LEADING_SPACE = re.compile(rb"\s*")


@dataclass(frozen=True)
class Sentence:
    """One sentence of an instruction: its number from 1, its markdown unit's number from 1, and its byte span."""

    number: int
    unit: int
    start: int
    end: int


@dataclass(frozen=True)
class _Unit:
    """A markdown unit's byte range and whether it splits into sentences rather than being one sentence."""

    start: int
    end: int
    splits: bool


def split_sentences(text: bytes) -> tuple[Sentence, ...]:
    """Number the sentences of an instruction from 1 over its markdown units."""
    unit_spans = [
        (unit_number, span)
        for unit_number, unit in enumerate(_read_units(text), 1)
        for span in _sentence_spans(text, unit)
    ]
    return tuple(
        Sentence(number, unit_number, start, end)
        for number, (unit_number, (start, end)) in enumerate(unit_spans, 1)
    )


def _read_units(text: bytes) -> list[_Unit]:
    """Read the markdown units of a text in order."""
    spans = _line_spans(text)
    lines = [text[start:end] for start, end in spans]
    units = []
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        text_offset, last, splits = _unit_extent(lines, index)
        units.append(_Unit(spans[index][0] + text_offset, spans[last][1], splits))
        index = last + 1
    return units


def _unit_extent(lines: list[bytes], first: int) -> tuple[int, int, bool]:
    """Return where the unit opening at a line starts its text within that line, its last line, and whether it splits."""
    if first == 0 and (closing := _frontmatter_closing_line(lines)) is not None:
        return 0, closing, False
    for pattern, extent in _UNIT_OPENINGS:
        if opening := pattern.match(lines[first]):
            return extent(lines, first, opening)
    return 0, _paragraph_last_line(lines, first), True


def _fenced_code_extent(lines: list[bytes], first: int, opening: re.Match[bytes]) -> tuple[int, int, bool]:
    """Return the extent of a fenced code block, one sentence through its closing line."""
    return 0, _fence_last_line(lines, first, opening.group(1)), False


def _whole_line_extent(lines: list[bytes], first: int, opening: re.Match[bytes]) -> tuple[int, int, bool]:
    """Return the extent of a heading, table row, blockquote line, or horizontal rule, one sentence of one line."""
    return 0, first, False


def _list_item_extent(lines: list[bytes], first: int, opening: re.Match[bytes]) -> tuple[int, int, bool]:
    """Return the extent of a list item, its text after the marker splitting into sentences."""
    return opening.end(), _paragraph_last_line(lines, first), True


_UNIT_OPENINGS = (
    (_FENCE_OPEN, _fenced_code_extent),
    (_WHOLE_LINE_UNIT, _whole_line_extent),
    (_LIST_MARKER, _list_item_extent),
)


def _frontmatter_closing_line(lines: list[bytes]) -> int | None:
    """Return the line closing a frontmatter block that opens the text, or None when the text opens none."""
    if not opens_frontmatter(lines):
        return None
    return frontmatter_closing_line(lines)


def opens_frontmatter(lines: Sequence[bytes]) -> bool:
    """Tell whether the first line is exactly the frontmatter fence."""
    return lines[0] == _FRONTMATTER_FENCE_BYTES


def frontmatter_closing_line(lines: Sequence[bytes]) -> int | None:
    """Return the index of the first line after the first that is exactly the frontmatter fence, or None when no line is."""
    return next((index for index in range(1, len(lines)) if lines[index] == _FRONTMATTER_FENCE_BYTES), None)


def _fence_last_line(lines: list[bytes], first: int, fence: bytes) -> int:
    """Return the line closing a fenced code block, or the text's last non-blank line when none closes it."""
    closing = re.compile(closing_code_fence(fence.decode()).encode())
    for index in range(first + 1, len(lines)):
        if closing.match(lines[index]):
            return index
    return max(index for index, line in enumerate(lines) if line.strip())


def closing_code_fence(fence: str) -> str:
    """Return the pattern of a line closing the code fence: its character at least as many times, alone on the line."""
    return rf"\s*{re.escape(fence[0])}{{{len(fence)},}}\s*\Z"


def _paragraph_last_line(lines: list[bytes], first: int) -> int:
    """Return the last line of the paragraph or list item opening at a line."""
    last = first
    while last + 1 < len(lines) and _continues_paragraph(lines[last + 1]):
        last += 1
    return last


def _continues_paragraph(line: bytes) -> bool:
    """Tell whether a line continues the paragraph or list item above it."""
    return bool(line.strip()) and not any(pattern.match(line) for pattern, _ in _UNIT_OPENINGS)


def _line_spans(text: bytes) -> list[tuple[int, int]]:
    """Return each line's byte span, its newline excluded."""
    lines = text.split(b"\n")
    starts = accumulate((len(line) + len(b"\n") for line in lines), initial=0)
    return [(start, start + len(line)) for start, line in zip(starts, lines)]


def _sentence_spans(text: bytes, unit: _Unit) -> list[tuple[int, int]]:
    """Return the byte spans of a unit's sentences: the whole unit, or each sentence of a splitting unit."""
    if not unit.splits:
        return [(unit.start, unit.end)]
    spans = []
    sentence_start = unit.start
    previous_end = unit.start
    for end in _SENTENCE_END.finditer(text, unit.start, unit.end):
        word_region_start, previous_end = previous_end, end.end()
        if _is_abbreviation(text[word_region_start:end.start()]):
            continue
        spans.append((_first_non_space(text, sentence_start, unit.end), end.end()))
        sentence_start = end.end()
    if text[sentence_start:unit.end].strip():
        spans.append((_first_non_space(text, sentence_start, unit.end), _last_non_space_end(text, unit)))
    return spans


def _last_non_space_end(text: bytes, unit: _Unit) -> int:
    """Return the position just past a unit's last non-whitespace byte."""
    return unit.start + len(text[unit.start:unit.end].rstrip())


def _is_abbreviation(text_before_end: bytes) -> bool:
    """Tell whether the word ending a text is an abbreviation or a single letter, which ends no sentence."""
    reversed_text = text_before_end.decode(errors="replace")[::-1]
    word = _WORD_RUN.match(reversed_text).group()[::-1]
    return word in _ABBREVIATIONS or bool(_SINGLE_LETTER.fullmatch(word))


def _first_non_space(text: bytes, position: int, end: int) -> int:
    """Return the position of the first non-whitespace byte between a position and an end."""
    return _LEADING_SPACE.match(text, position, end).end()


def coverage_check(files: SeriesFolder, revision: str) -> None:
    """Refuse a revision's coverage that leaves a demand or sentence unmapped, maps a number outside the text, disagrees between its two maps, or in a later revision drops other demands than the first."""
    records = SeriesRecords(files)
    coverage = records.coverage(revision)
    path = _coverage_path(revision)
    sentence_count = len(split_sentences(read_series_file(files, f"{revision}/{INSTRUCTION_FILE}")))
    _refuse_unmapped_demands(records.demands(), coverage, path)
    _refuse_numbers_outside_text(coverage, sentence_count, path)
    _refuse_sentences_without_demand(coverage, sentence_count)
    _refuse_disagreeing_maps(coverage, path)
    _refuse_dropped_set_other_than_first(records, coverage, revision, path)


def _coverage_path(revision: str) -> str:
    """Return the path of a revision's `3-coverage.yaml`."""
    return f"{revision}/{COVERAGE_FILE}"


def _refuse_unmapped_demands(demands: Demands, coverage: Coverage, path: str) -> None:
    """Refuse the first demand of the series, in file order, the coverage does not map."""
    unmapped = next((demand.id for demand in demands.demands if demand.id not in coverage.demands), None)
    if unmapped is not None:
        raise Refusal(f"unmapped demand: {unmapped} ({path})")


def _refuse_numbers_outside_text(coverage: Coverage, sentence_count: int, path: str) -> None:
    """Refuse a sentence number beyond the text's sentence count in either map."""
    numbers = {*(number for number, _ in _demand_side_pairs(coverage)), *coverage.sentences}
    outside = next((number for number in sorted(numbers) if number > sentence_count), None)
    if outside is not None:
        raise Refusal(f"sentence number outside the text: {outside} ({path})")


def _refuse_sentences_without_demand(coverage: Coverage, sentence_count: int) -> None:
    """Refuse the first sentence of the text the sentence map lacks."""
    bare = next((number for number in range(1, sentence_count + 1) if number not in coverage.sentences), None)
    if bare is not None:
        raise Refusal(f"sentence {bare} carries no demand (imported)")


def _refuse_disagreeing_maps(coverage: Coverage, path: str) -> None:
    """Refuse a demand and a sentence one map pairs and the other does not."""
    sentence_side = {(number, demand) for number, demands in coverage.sentences.items() for demand in demands}
    unpaired = sorted(_demand_side_pairs(coverage) ^ sentence_side)
    if unpaired:
        number, demand = unpaired[0]
        raise Refusal(f"coverage maps disagree: demand {demand} and sentence {number} ({path})")


def _refuse_dropped_set_other_than_first(records: SeriesRecords, coverage: Coverage, revision: str, path: str) -> None:
    """Refuse a later revision dropping other demands than the first revision's coverage drops."""
    if revision == FIRST_REVISION:
        return
    differing = _dropped_demands(coverage) ^ _dropped_demands(records.coverage(FIRST_REVISION))
    if differing:
        raise Refusal(f"dropped demands differ from {FIRST_REVISION}: {', '.join(sorted(differing))} ({path})")


def _demand_side_pairs(coverage: Coverage) -> set[tuple[int, str]]:
    """Return each (sentence number, demand id) pair the demand map holds, a dropped demand holding none."""
    return {(number, demand) for demand, sentences in coverage.demands.items() if not isinstance(sentences, Dropped) for number in sentences}


def _dropped_demands(coverage: Coverage) -> set[str]:
    """Return the ids of the demands a coverage drops."""
    return {demand for demand, sentences in coverage.demands.items() if isinstance(sentences, Dropped)}
