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
