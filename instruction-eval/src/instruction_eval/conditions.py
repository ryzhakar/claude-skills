from instruction_eval.coverage import Sentence, split_sentences
from instruction_eval.records import Omissions
from instruction_eval.tasks import EVERY_SENTENCE_OMISSIONS, INSTRUCTION_CONDITION, OMISSION_PREFIX

_FENCE = "---"


def revision_condition_texts(instruction: bytes, omissions: Omissions) -> dict[str, bytes]:
    """Return a revision's own condition texts by condition: its instruction, and one `omit-<n>` per sentence when omissions are every sentence."""
    return {INSTRUCTION_CONDITION: instruction, **omission_texts(instruction, omissions)}


def omission_texts(instruction: bytes, omissions: Omissions) -> dict[str, bytes]:
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
    if end < len(text) and _is_blank(text[end:_line_end(text, end)]):
        return start, _line_end(text, end)
    if start > 0 and _is_blank(text[_line_start(text, start - 1):start]):
        return _line_start(text, start - 1), end
    return start, end


def _line_start(text: bytes, position: int) -> int:
    """Return where the line holding a position starts."""
    return text.rfind(b"\n", 0, position) + 1


def _line_end(text: bytes, position: int) -> int:
    """Return where the line holding a position ends, past its newline when it has one."""
    newline = text.find(b"\n", position)
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
