import hashlib
import json
from dataclasses import dataclass, fields
from datetime import datetime
from itertools import accumulate
from pathlib import Path
from typing import Any

_USER_ENTRY_TYPE = "user"
_ASSISTANT_ENTRY_TYPE = "assistant"
_TEXT_BLOCK_TYPE = "text"
_SEND_MESSAGE_WRAPPER_OPENING = "The coordinator sent a message while you were working:\n"
_TYPE_KEY = "type"
_MESSAGE_KEY = "message"
_CONTENT_KEY = "content"
_TIMESTAMP_KEY = "timestamp"
_ID_KEY = "id"
_MODEL_KEY = "model"
_USAGE_KEY = "usage"
_META_KEY = "isMeta"
_TEXT_KEY = "text"
_FIELDS_READ_BY_ENTRY_TYPE = {
    _USER_ENTRY_TYPE: ((_TIMESTAMP_KEY,), (_MESSAGE_KEY, _CONTENT_KEY)),
    _ASSISTANT_ENTRY_TYPE: (
        (_TIMESTAMP_KEY,),
        (_MESSAGE_KEY, _ID_KEY),
        (_MESSAGE_KEY, _MODEL_KEY),
        (_MESSAGE_KEY, _CONTENT_KEY),
    ),
}


@dataclass(frozen=True)
class TokenUsage:
    """Tokens one reply spent, each field named and counted as the transcript's `message.usage` key."""

    input_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    output_tokens: int

    @property
    def spent_input_tokens(self) -> int:
        """Return every input token the reply spent: uncached, cache creation, and cache read."""
        return self.input_tokens + self.cache_creation_input_tokens + self.cache_read_input_tokens


@dataclass(frozen=True)
class TranscriptReply:
    """One user turn of a subagent transcript paired with the last assistant text answering it."""

    turn: int
    message: str
    text: str
    model: str
    started: datetime
    seconds: float
    tokens: TokenUsage | None
    transcript: Path
    transcript_hash: str


@dataclass(frozen=True)
class _TranscriptLine:
    """One parsed transcript entry with the byte offset just past its line."""

    entry: dict[str, Any]
    end: int


def parse_transcript_replies(transcript: Path, content: bytes) -> tuple[TranscriptReply, ...]:
    """Pair the k-th user message of the transcript bytes with its reply as turn k, skipping unanswered turns."""
    turns = _group_lines_by_turn(_split_transcript_lines(transcript, content))
    replies = (
        _reply_to_turn(number, turn_lines, transcript, content)
        for number, turn_lines in enumerate(turns, 1)
    )
    return tuple(reply for reply in replies if reply is not None)


def _split_transcript_lines(transcript: Path, content: bytes) -> tuple[_TranscriptLine, ...]:
    """Parse each JSONL line of the transcript, keeping where its bytes end."""
    raw_lines = content.splitlines(keepends=True)
    ends = accumulate(len(raw_line) for raw_line in raw_lines)
    return tuple(
        _TranscriptLine(_parse_transcript_line(transcript, number, raw_line), end)
        for number, (raw_line, end) in enumerate(zip(raw_lines, ends), 1)
    )


def _parse_transcript_line(transcript: Path, number: int, raw_line: bytes) -> dict[str, Any]:
    """Parse one transcript line into an entry holding every field the parser reads, refusing with transcript and line otherwise."""
    entry = _decode_transcript_line(transcript, number, raw_line)
    fault = _structural_fault(entry)
    if fault is not None:
        raise ValueError(f"{transcript}: line {number} {fault}")
    return entry


def _decode_transcript_line(transcript: Path, number: int, raw_line: bytes) -> object:
    """Decode one transcript line as JSON, refusing with the transcript and line number when it is not."""
    try:
        return json.loads(raw_line)
    except json.JSONDecodeError as error:
        raise ValueError(f"{transcript}: line {number} is not JSON") from error


def _structural_fault(entry: object) -> str | None:
    """Name the first field the parser reads that the decoded entry lacks, or None when it holds them all."""
    if not isinstance(entry, dict):
        return "is not a JSON object"
    if _TYPE_KEY not in entry:
        return f"lacks {_TYPE_KEY}"
    missing = [path for path in _FIELDS_READ_BY_ENTRY_TYPE.get(entry[_TYPE_KEY], ()) if not _has_field(entry, path)]
    return f"lacks {'.'.join(missing[0])}" if missing else None


def _has_field(entry: dict[str, Any], path: tuple[str, ...]) -> bool:
    """Tell whether the nested keys of the path lead to a value in the entry."""
    value: object = entry
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return False
        value = value[key]
    return True


def _group_lines_by_turn(lines: tuple[_TranscriptLine, ...]) -> tuple[tuple[_TranscriptLine, ...], ...]:
    """Split the lines into turns, each opening with a user message and running to the next."""
    starts = [index for index, line in enumerate(lines) if _is_user_message(line.entry)]
    return tuple(lines[start:stop] for start, stop in zip(starts, [*starts[1:], len(lines)]))


def _is_user_message(entry: dict[str, Any]) -> bool:
    """Tell a turn-opening user string, typed or delivered by SendMessage, from harness injections, tool results, and other entries."""
    if entry["type"] != _USER_ENTRY_TYPE or not isinstance(entry["message"]["content"], str):
        return False
    return not entry.get("isMeta") or entry["message"]["content"].startswith(_SEND_MESSAGE_WRAPPER_OPENING)


def _reply_to_turn(
    number: int, turn_lines: tuple[_TranscriptLine, ...], transcript: Path, content: bytes
) -> TranscriptReply | None:
    """Build the reply to one turn from its last assistant text, or None when no assistant text answers it."""
    answering_lines = [line for line in turn_lines if _text_blocks(line.entry)]
    if not answering_lines:
        return None
    user_entry, reply_line = turn_lines[0].entry, answering_lines[-1]
    started = _timestamp_of(user_entry)
    return TranscriptReply(
        turn=number,
        message=user_entry["message"]["content"],
        text="".join(_text_blocks(reply_line.entry)),
        model=reply_line.entry["message"]["model"],
        started=started,
        seconds=(_timestamp_of(reply_line.entry) - started).total_seconds(),
        tokens=_turn_token_usage(turn_lines),
        transcript=transcript,
        transcript_hash=hashlib.sha256(content[: reply_line.end]).hexdigest(),
    )


def _text_blocks(entry: dict[str, Any]) -> tuple[str, ...]:
    """Return the text blocks of an assistant entry, empty for every other entry."""
    if entry["type"] != _ASSISTANT_ENTRY_TYPE:
        return ()
    return tuple(block["text"] for block in entry["message"]["content"] if block["type"] == _TEXT_BLOCK_TYPE)


def _timestamp_of(entry: dict[str, Any]) -> datetime:
    """Return the entry's ISO 8601 timestamp as an aware datetime."""
    return datetime.fromisoformat(entry["timestamp"])


def _turn_token_usage(turn_lines: tuple[_TranscriptLine, ...]) -> TokenUsage | None:
    """Sum the final usage of each assistant message in the turn, or None when any message lacks usage."""
    final_usages = {
        line.entry["message"]["id"]: line.entry["message"].get("usage")
        for line in turn_lines
        if line.entry["type"] == _ASSISTANT_ENTRY_TYPE
    }.values()
    if None in final_usages:
        return None
    return TokenUsage(
        **{field.name: sum(usage[field.name] for usage in final_usages) for field in fields(TokenUsage)}
    )
