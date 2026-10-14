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
WHOLE_LINE_UNIT = re.compile(rb"\s*[#|>]")


def read_units(text: bytes) -> list[Unit]:
    """Read the markdown units of a text in order."""
    lines = [text[start:end] for start, end in line_spans(text)]
    spans = line_spans(text)
    units = []
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        if WHOLE_LINE_UNIT.match(lines[index]):
            units.append(Unit(*spans[index], splits=False))
            index += 1
            continue
        last = index
        while last + 1 < len(lines) and continues_paragraph(lines[last + 1]):
            last += 1
        units.append(Unit(spans[index][0], spans[last][1], splits=True))
        index = last + 1
    return units


def continues_paragraph(line: bytes) -> bool:
    """Tell whether a line continues the paragraph or list item above it."""
    return bool(line.strip()) and not WHOLE_LINE_UNIT.match(line)


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
