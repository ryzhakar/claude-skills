import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

from instruction_eval.reader import TokenUsage, parse_transcript_replies

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "transcript-parse"
SINGLE_TURN_REPLY_LINE_COUNT = 4
THREE_TURN_REPLY_LINE_COUNTS = (2, 7, 9)


def replies_of(fixture_name):
    transcript = FIXTURES / fixture_name
    return parse_transcript_replies(transcript, transcript.read_bytes())


def test_single_turn_reply_records_text_model_message_and_timing():
    [reply] = replies_of("single-turn.jsonl")
    assert reply.turn == 1
    assert reply.message == "Hello."
    assert reply.text == "OK"
    assert reply.model == "claude-sonnet-5-5"
    assert reply.started == datetime(2026, 10, 14, 19, 47, 23, 988000, tzinfo=timezone.utc)
    assert reply.seconds == 1.5
    assert reply.transcript == FIXTURES / "single-turn.jsonl"


def test_reply_tokens_take_each_assistant_message_final_usage():
    [reply] = replies_of("single-turn.jsonl")
    assert reply.tokens == TokenUsage(
        input_tokens=3, cache_creation_input_tokens=13903, cache_read_input_tokens=100, output_tokens=12
    )


def test_spent_input_tokens_sum_uncached_cache_creation_and_cache_read_input():
    [reply] = replies_of("single-turn.jsonl")
    assert reply.tokens.spent_input_tokens == 14006


def test_reply_tokens_are_absent_when_the_transcript_records_no_usage():
    [reply] = replies_of("no-usage.jsonl")
    assert reply.tokens is None


def test_reply_tokens_are_absent_when_any_assistant_message_of_the_turn_lacks_usage():
    [reply] = replies_of("partial-usage.jsonl")
    assert reply.tokens is None


def test_transcript_hash_covers_bytes_through_the_reply_line_only():
    transcript_bytes = (FIXTURES / "single-turn.jsonl").read_bytes()
    through_reply_line = b"".join(transcript_bytes.splitlines(keepends=True)[:SINGLE_TURN_REPLY_LINE_COUNT])
    [reply] = replies_of("single-turn.jsonl")
    assert reply.transcript_hash == hashlib.sha256(through_reply_line).hexdigest()


def test_each_conversation_reply_hashes_bytes_through_its_own_reply_line():
    transcript_lines = (FIXTURES / "three-turn.jsonl").read_bytes().splitlines(keepends=True)
    expected = [
        hashlib.sha256(b"".join(transcript_lines[:line_count])).hexdigest()
        for line_count in THREE_TURN_REPLY_LINE_COUNTS
    ]
    assert [reply.transcript_hash for reply in replies_of("three-turn.jsonl")] == expected


def test_conversation_pairs_kth_user_message_with_last_assistant_text_before_the_next():
    replies = replies_of("three-turn.jsonl")
    assert [(reply.turn, reply.text) for reply in replies] == [(1, "ONE"), (2, "TWO"), (3, "THREE")]
    assert replies[1].seconds == 3.25
    assert replies[1].tokens == TokenUsage(
        input_tokens=37, cache_creation_input_tokens=10, cache_read_input_tokens=110, output_tokens=22
    )


def test_conversation_turn_message_keeps_the_send_message_wrapper():
    replies = replies_of("three-turn.jsonl")
    assert replies[2].message == (
        "The coordinator sent a message while you were working:\n"
        "TURN-3: reply with the single word THREE.\n\n"
        "Address this before completing your current task."
    )


def test_unanswered_turns_yield_no_reply_and_keep_later_turn_numbers():
    replies = replies_of("unanswered-turns.jsonl")
    assert [(reply.turn, reply.text) for reply in replies] == [(2, "TWO")]


def test_harness_injected_meta_messages_open_no_turn_while_send_message_turns_do():
    replies = replies_of("harness-injections.jsonl")
    assert [(reply.turn, reply.text) for reply in replies] == [(1, "ONE"), (2, "TWO")]
    assert replies[0].message == "TURN-1: reply with the single word ONE."
    assert replies[1].message.startswith("The coordinator sent a message while you were working:\n")


def test_a_line_that_is_not_json_is_refused_naming_transcript_and_line():
    transcript = FIXTURES / "single-turn.jsonl"
    truncated = transcript.read_bytes() + b'{"type":"assist'
    with pytest.raises(ValueError, match=rf"^{re.escape(str(transcript))}: line 6 is not JSON$"):
        parse_transcript_replies(transcript, truncated)


@pytest.mark.parametrize(
    ("malformed_line", "fault"),
    [
        (b"[]", "is not a JSON object"),
        (b"{}", "lacks type"),
        (b'{"type":"user","timestamp":"2026-10-14T19:47:30.000Z"}', "lacks message.content"),
        (
            b'{"type":"assistant","timestamp":"2026-10-14T19:47:31.000Z",'
            b'"message":{"model":"claude-sonnet-5-5","content":[{"type":"text","text":"OK"}]}}',
            "lacks message.id",
        ),
    ],
)
def test_a_parseable_line_missing_a_read_field_is_refused_naming_transcript_line_and_field(malformed_line, fault):
    transcript = FIXTURES / "single-turn.jsonl"
    with pytest.raises(ValueError, match=rf"^{re.escape(str(transcript))}: line 6 {fault}$"):
        parse_transcript_replies(transcript, transcript.read_bytes() + malformed_line)


def test_blank_lines_are_skipped_and_still_counted_in_the_hashed_bytes():
    transcript = FIXTURES / "single-turn.jsonl"
    transcript_lines = transcript.read_bytes().splitlines(keepends=True)
    [reply] = parse_transcript_replies(transcript, b"\n" + b"".join(transcript_lines) + b"\n")
    through_reply_line = b"\n" + b"".join(transcript_lines[:SINGLE_TURN_REPLY_LINE_COUNT])
    assert (reply.text, reply.transcript_hash) == ("OK", hashlib.sha256(through_reply_line).hexdigest())
