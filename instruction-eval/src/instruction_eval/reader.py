import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from itertools import accumulate
from pathlib import Path


@dataclass(frozen=True)
class TokenUsage:
    """Input and output tokens one reply spent, as the transcript's `message.usage` reports them."""

    input_tokens: int
    output_tokens: int


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
class TranscriptLine:
    """One parsed transcript entry with the byte offset just past its line."""

    entry: dict
    end: int


def parse_transcript_replies(transcript: Path, content: bytes) -> tuple[TranscriptReply, ...]:
    """Pair the k-th user message of the transcript bytes with its reply as turn k, skipping unanswered turns."""
    turns = group_lines_by_turn(split_transcript_lines(content))
    replies = (
        reply_to_turn(number, turn_lines, transcript, content)
        for number, turn_lines in enumerate(turns, 1)
    )
    return tuple(reply for reply in replies if reply is not None)


def split_transcript_lines(content: bytes) -> tuple[TranscriptLine, ...]:
    """Parse each JSONL line of the transcript, keeping where its bytes end."""
    raw_lines = content.splitlines(keepends=True)
    ends = accumulate(len(raw_line) for raw_line in raw_lines)
    return tuple(TranscriptLine(json.loads(raw_line), end) for raw_line, end in zip(raw_lines, ends))


def group_lines_by_turn(lines: tuple[TranscriptLine, ...]) -> tuple[tuple[TranscriptLine, ...], ...]:
    """Split the lines into turns, each opening with a user message and running to the next."""
    starts = [index for index, line in enumerate(lines) if is_user_message(line.entry)]
    return tuple(lines[start:stop] for start, stop in zip(starts, [*starts[1:], len(lines)]))


def is_user_message(entry: dict) -> bool:
    """Tell a user message, whose content is a string, from tool results and every other entry."""
    return entry["type"] == "user" and isinstance(entry["message"]["content"], str)


def reply_to_turn(
    number: int, turn_lines: tuple[TranscriptLine, ...], transcript: Path, content: bytes
) -> TranscriptReply | None:
    """Build the reply to one turn from its last assistant text, or None when no assistant text answers it."""
    answering_lines = [line for line in turn_lines if text_blocks(line.entry)]
    if not answering_lines:
        return None
    user_entry, reply_line = turn_lines[0].entry, answering_lines[-1]
    started = timestamp_of(user_entry)
    return TranscriptReply(
        turn=number,
        message=user_entry["message"]["content"],
        text="".join(text_blocks(reply_line.entry)),
        model=reply_line.entry["message"]["model"],
        started=started,
        seconds=(timestamp_of(reply_line.entry) - started).total_seconds(),
        tokens=turn_token_usage(turn_lines),
        transcript=transcript,
        transcript_hash=hashlib.sha256(content[: reply_line.end]).hexdigest(),
    )


def text_blocks(entry: dict) -> tuple[str, ...]:
    """Return the text blocks of an assistant entry, empty for every other entry."""
    if entry["type"] != "assistant":
        return ()
    return tuple(block["text"] for block in entry["message"]["content"] if block["type"] == "text")


def timestamp_of(entry: dict) -> datetime:
    """Return the entry's ISO 8601 timestamp as an aware datetime."""
    return datetime.fromisoformat(entry["timestamp"])


def turn_token_usage(turn_lines: tuple[TranscriptLine, ...]) -> TokenUsage | None:
    """Sum the final usage of each assistant message in the turn, or None when any message lacks usage."""
    final_usages = {
        line.entry["message"]["id"]: line.entry["message"]["usage"]
        for line in turn_lines
        if line.entry["type"] == "assistant"
    }.values()
    return TokenUsage(
        input_tokens=sum(usage["input_tokens"] for usage in final_usages),
        output_tokens=sum(usage["output_tokens"] for usage in final_usages),
    )
