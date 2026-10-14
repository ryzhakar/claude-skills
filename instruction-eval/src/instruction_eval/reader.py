import hashlib
import json
from dataclasses import dataclass, fields
from datetime import datetime
from itertools import accumulate
from pathlib import Path

_USER_ENTRY_TYPE = "user"
_ASSISTANT_ENTRY_TYPE = "assistant"
_TEXT_BLOCK_TYPE = "text"


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

    entry: dict
    end: int


def parse_transcript_replies(transcript: Path, content: bytes) -> tuple[TranscriptReply, ...]:
    """Pair the k-th user message of the transcript bytes with its reply as turn k, skipping unanswered turns."""
    turns = _group_lines_by_turn(_split_transcript_lines(content))
    replies = (
        _reply_to_turn(number, turn_lines, transcript, content)
        for number, turn_lines in enumerate(turns, 1)
    )
    return tuple(reply for reply in replies if reply is not None)


def _split_transcript_lines(content: bytes) -> tuple[_TranscriptLine, ...]:
    """Parse each JSONL line of the transcript, keeping where its bytes end."""
    raw_lines = content.splitlines(keepends=True)
    ends = accumulate(len(raw_line) for raw_line in raw_lines)
    return tuple(_TranscriptLine(json.loads(raw_line), end) for raw_line, end in zip(raw_lines, ends))


def _group_lines_by_turn(lines: tuple[_TranscriptLine, ...]) -> tuple[tuple[_TranscriptLine, ...], ...]:
    """Split the lines into turns, each opening with a user message and running to the next."""
    starts = [index for index, line in enumerate(lines) if _is_user_message(line.entry)]
    return tuple(lines[start:stop] for start, stop in zip(starts, [*starts[1:], len(lines)]))


def _is_user_message(entry: dict) -> bool:
    """Tell a user message, whose content is a string, from tool results and every other entry."""
    return entry["type"] == _USER_ENTRY_TYPE and isinstance(entry["message"]["content"], str)


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


def _text_blocks(entry: dict) -> tuple[str, ...]:
    """Return the text blocks of an assistant entry, empty for every other entry."""
    if entry["type"] != _ASSISTANT_ENTRY_TYPE:
        return ()
    return tuple(block["text"] for block in entry["message"]["content"] if block["type"] == _TEXT_BLOCK_TYPE)


def _timestamp_of(entry: dict) -> datetime:
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
