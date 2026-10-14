import hashlib
from datetime import datetime, timezone
from pathlib import Path

from instruction_eval.reader import TokenUsage, parse_transcript_replies

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "transcript-parse"


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
    assert reply.tokens == TokenUsage(input_tokens=3, output_tokens=12)


def test_reply_tokens_are_absent_when_the_transcript_records_no_usage():
    [reply] = replies_of("no-usage.jsonl")
    assert reply.tokens is None


def test_transcript_hash_covers_bytes_through_the_reply_line_only():
    transcript_bytes = (FIXTURES / "single-turn.jsonl").read_bytes()
    through_reply_line = b"".join(transcript_bytes.splitlines(keepends=True)[:4])
    [reply] = replies_of("single-turn.jsonl")
    assert reply.transcript_hash == hashlib.sha256(through_reply_line).hexdigest()


def test_conversation_pairs_kth_user_message_with_last_assistant_text_before_the_next():
    replies = replies_of("three-turn.jsonl")
    assert [(reply.turn, reply.text) for reply in replies] == [(1, "ONE"), (2, "TWO"), (3, "THREE")]
    assert replies[1].seconds == 3.25
    assert replies[1].tokens == TokenUsage(input_tokens=37, output_tokens=22)


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
