from collections.abc import Callable, Mapping
from itertools import cycle, islice

from instruction_eval.coverage import Sentence, split_sentences
from instruction_eval.records import PLACEBO_SNAPSHOT, Conditions, Control, Omissions
from instruction_eval.tasks import EVERY_SENTENCE_OMISSIONS, INSTRUCTION_CONDITION, OMISSION_PREFIX, WORD_PATTERN, words

_FENCE = "---"
_NEWLINE = b"\n"
SOURCE_SEPARATOR = "\n\n"
PLACEBO_WORD_SEPARATOR = " "
EMPTY_CONTROL: Control = "empty"
AIM_CONTROL: Control = "aim"
PLACEBO_CONTROL: Control = "placebo"
SOURCE_CONTROL: Control = "source"


def revision_condition_texts(instruction: bytes, omissions: Omissions) -> dict[str, bytes]:
    """Return a revision's own condition texts by condition: its instruction, and one `omit-<n>` per sentence when omissions are every sentence."""
    return {INSTRUCTION_CONDITION: instruction, **_omission_texts(instruction, omissions)}


def control_texts(conditions: Conditions, first_instruction: bytes, sources: Mapping[str, str], placebo_source: str) -> dict[str, bytes]:
    """Return the text of each control the conditions hold, from r1's instruction, the source texts by series path in `sources` order, and the placebo source snapshot."""
    texts: Mapping[Control, Callable[[], bytes]] = {
        EMPTY_CONTROL: bytes,
        AIM_CONTROL: conditions.aim.encode,
        PLACEBO_CONTROL: lambda: _placebo_text(placebo_source, first_instruction),
        SOURCE_CONTROL: lambda: _source_text(sources),
    }
    return {control: texts[control]() for control in conditions.controls}


def _placebo_text(placebo_source: str, first_instruction: bytes) -> bytes:
    """Return the placebo source's words, case kept, repeated from its start to r1's word count and joined by single spaces, refusing a wordless source while r1 has words."""
    word_count = len(words(first_instruction.decode()))
    placebo_words = WORD_PATTERN.findall(placebo_source)
    if word_count and not placebo_words:
        raise ValueError(f"placebo source holds no word: {PLACEBO_SNAPSHOT}")
    repeated = islice(cycle(placebo_words), word_count)
    return PLACEBO_WORD_SEPARATOR.join(repeated).encode()


def _source_text(sources: Mapping[str, str]) -> bytes:
    """Return the source texts without frontmatter joined by two newlines, refusing an unclosed frontmatter by its series path."""
    return SOURCE_SEPARATOR.join(strip_frontmatter(text, path) for path, text in sources.items()).encode()


def _omission_texts(instruction: bytes, omissions: Omissions) -> dict[str, bytes]:
    """Return the instruction without sentence n as `omit-<n>` for each sentence when omissions are every sentence, else nothing."""
    if omissions != EVERY_SENTENCE_OMISSIONS:
        return {}
    sentences = split_sentences(instruction)
    return {
        f"{OMISSION_PREFIX}{sentence.number}": _without(instruction, _omitted_span(instruction, sentence, sentences))
        for sentence in sentences
    }


def _omitted_span(text: bytes, sentence: Sentence, sentences: tuple[Sentence, ...]) -> tuple[int, int]:
    """Return the bytes omitting a sentence removes: its whole lines when it is its unit's only sentence, else its span with the whitespace after it, or before it when it ends its unit."""
    unit_sentences = [other for other in sentences if other.unit == sentence.unit]
    if len(unit_sentences) == 1:
        return _lone_sentence_lines(text, sentence)
    if sentence != unit_sentences[-1]:
        return sentence.start, _whitespace_end(text, sentence.end)
    return _whitespace_start(text, sentence.start), sentence.end


def _lone_sentence_lines(text: bytes, sentence: Sentence) -> tuple[int, int]:
    """Return a sentence's whole lines with one following blank line, else one preceding blank line, else no further line."""
    start = _line_start(text, sentence.start)
    end = _line_end(text, sentence.end)
    following_end = _line_end(text, end)
    preceding_start = _line_start(text, max(start - 1, 0))
    if end < len(text) and _is_blank(text[end:following_end]):
        return start, following_end
    if start > 0 and _is_blank(text[preceding_start:start]):
        return preceding_start, end
    return start, end


def _line_start(text: bytes, position: int) -> int:
    """Return where the line holding a position starts."""
    return text.rfind(_NEWLINE, 0, position) + 1


def _line_end(text: bytes, position: int) -> int:
    """Return where the line holding a position ends, past its newline when it has one."""
    newline = text.find(_NEWLINE, position)
    return len(text) if newline < 0 else newline + 1


def _is_blank(line: bytes) -> bool:
    """Tell whether a line holds only whitespace."""
    return not line.strip()


def _whitespace_end(text: bytes, position: int) -> int:
    """Return the position past the whitespace run starting at a position."""
    return len(text) - len(text[position:].lstrip())


def _whitespace_start(text: bytes, position: int) -> int:
    """Return where the whitespace run ending at a position starts."""
    return len(text[:position].rstrip())


def _without(text: bytes, span: tuple[int, int]) -> bytes:
    """Return the text with a byte span removed."""
    start, end = span
    return text[:start] + text[end:]


class UnclosedFrontmatter(ValueError):
    """Raised when a text opens a frontmatter block it never closes."""


def strip_frontmatter(text: str, path: str) -> str:
    """Return the text without its leading frontmatter block, refusing an unclosed block."""
    lines = text.split("\n")
    if lines[0] != _FENCE:
        return text
    closing_index = next((i for i, line in enumerate(lines[1:], 1) if line == _FENCE), None)
    if closing_index is None:
        raise UnclosedFrontmatter(f"unclosed frontmatter: {path}")
    return "\n".join(lines[closing_index + 1:])
