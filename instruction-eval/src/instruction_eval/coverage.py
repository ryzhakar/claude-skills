"""Coverage of an instruction's demands by its sentences."""

import re
from dataclasses import dataclass
from itertools import accumulate


@dataclass(frozen=True)
class Sentence:
    """One sentence of an instruction: its number from 1, its markdown unit's number from 1, and its byte span."""

    number: int
    unit: int
    start: int
    end: int


@dataclass(frozen=True)
class Unit:
    """A markdown unit's byte range and whether it splits into sentences rather than being one sentence."""

    start: int
    end: int
    splits: bool


def split_sentences(text: bytes) -> tuple[Sentence, ...]:
    """Number the sentences of an instruction from 1 over its markdown units."""
    unit_spans = [
        (unit_number, span)
        for unit_number, unit in enumerate(read_units(text), 1)
        for span in sentence_spans(text, unit)
    ]
    return tuple(
        Sentence(number, unit_number, start, end)
        for number, (unit_number, (start, end)) in enumerate(unit_spans, 1)
    )


SENTENCE_END = re.compile(rb"""[.!?]["')\]]*(?=\s|\Z)""")
WORD_BEFORE_END = re.compile(rb"[A-Za-z.]*\Z")
ABBREVIATIONS = {b"e.g", b"i.e", b"etc", b"vs", b"cf", b"Mr", b"Mrs", b"Dr", b"St", b"No"}
SINGLE_LETTER = re.compile(rb"[A-Za-z]")
WHOLE_LINE_UNIT = re.compile(rb"\s*(?:[#|>]|([-*_])(?:[ \t]*\1){2,}\s*\Z)")
FENCE_OPEN = re.compile(rb"\s*(`{3,}|~{3,})")
FRONTMATTER_DELIMITER = re.compile(rb"---\s*\Z")
LIST_MARKER = re.compile(rb"\s*(?:[-*+]|\d+[.)])(?:[ \t]+|\Z)")


def read_units(text: bytes) -> list[Unit]:
    """Read the markdown units of a text in order."""
    spans = line_spans(text)
    lines = [text[start:end] for start, end in spans]
    units = []
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        text_offset, last, splits = unit_extent(lines, index)
        units.append(Unit(spans[index][0] + text_offset, spans[last][1], splits))
        index = last + 1
    return units


def unit_extent(lines: list[bytes], first: int) -> tuple[int, int, bool]:
    """Return where the unit opening at a line starts its text within that line, its last line, and whether it splits."""
    if first == 0 and (closing := frontmatter_closing_line(lines)) is not None:
        return 0, closing, False
    fence = FENCE_OPEN.match(lines[first])
    if fence:
        return 0, fence_last_line(lines, first, fence.group(1)), False
    if WHOLE_LINE_UNIT.match(lines[first]):
        return 0, first, False
    marker = LIST_MARKER.match(lines[first])
    return marker.end() if marker else 0, paragraph_last_line(lines, first), True


def frontmatter_closing_line(lines: list[bytes]) -> int | None:
    """Return the line closing a frontmatter block that opens the text, or None when the text opens none."""
    if not FRONTMATTER_DELIMITER.match(lines[0]):
        return None
    return next((index for index in range(1, len(lines)) if FRONTMATTER_DELIMITER.match(lines[index])), None)


def fence_last_line(lines: list[bytes], first: int, fence: bytes) -> int:
    """Return the line closing a fenced code block, or the text's last non-blank line when none closes it."""
    closing = re.compile(rb"\s*%b{%d,}\s*\Z" % (re.escape(fence[:1]), len(fence)))
    for index in range(first + 1, len(lines)):
        if closing.match(lines[index]):
            return index
    return max(index for index, line in enumerate(lines) if line.strip())


def paragraph_last_line(lines: list[bytes], first: int) -> int:
    """Return the last line of the paragraph or list item opening at a line."""
    last = first
    while last + 1 < len(lines) and continues_paragraph(lines[last + 1]):
        last += 1
    return last


def continues_paragraph(line: bytes) -> bool:
    """Tell whether a line continues the paragraph or list item above it."""
    return bool(line.strip()) and not any(
        opening.match(line) for opening in (WHOLE_LINE_UNIT, FENCE_OPEN, LIST_MARKER)
    )


def line_spans(text: bytes) -> list[tuple[int, int]]:
    """Return each line's byte span, its newline excluded."""
    lines = text.split(b"\n")
    starts = accumulate((len(line) + len(b"\n") for line in lines), initial=0)
    return [(start, start + len(line)) for start, line in zip(starts, lines)]


def sentence_spans(text: bytes, unit: Unit) -> list[tuple[int, int]]:
    """Return the byte spans of a unit's sentences: the whole unit, or each sentence of a splitting unit."""
    if not unit.splits:
        return [(unit.start, unit.end)]
    spans = []
    sentence_start = unit.start
    for end in SENTENCE_END.finditer(text, unit.start, unit.end):
        if is_abbreviation(text[unit.start:end.start()]):
            continue
        spans.append((first_non_space(text, sentence_start), end.end()))
        sentence_start = end.end()
    if text[sentence_start:unit.end].strip():
        spans.append((first_non_space(text, sentence_start), last_non_space_end(text, unit)))
    return spans


def last_non_space_end(text: bytes, unit: Unit) -> int:
    """Return the position just past a unit's last non-whitespace byte."""
    return unit.start + len(text[unit.start:unit.end].rstrip())



def is_abbreviation(text_before_end: bytes) -> bool:
    """Tell whether the word ending a text is an abbreviation or a single letter, which ends no sentence."""
    word = WORD_BEFORE_END.search(text_before_end).group()
    return word in ABBREVIATIONS or bool(SINGLE_LETTER.fullmatch(word))


def first_non_space(text: bytes, position: int) -> int:
    """Return the position of the first non-whitespace byte at or after a position."""
    return position + len(text[position:]) - len(text[position:].lstrip())
