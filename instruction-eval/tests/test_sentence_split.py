import time
from pathlib import Path

import pytest
import yaml

from instruction_eval.coverage import split_sentences

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "sentence-split"
FIXTURE_NAMES = sorted(path.stem for path in FIXTURE_DIR.glob("*.md"))
ABBREVIATION_RUN_LENGTH = 20_000
SPLIT_SECONDS_LIMIT = 2
SENTENCE_PROBE_SIZE = 20_000
GROWTH_FACTOR = 4
LINEAR_GROWTH_LIMIT = 8
TIMING_RUNS = 3


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_sentences_are_numbered_spans_within_their_units(name):
    text = (FIXTURE_DIR / f"{name}.md").read_bytes()
    expected = yaml.safe_load((FIXTURE_DIR / f"{name}.yaml").read_text())
    sentences = split_sentences(text)
    assert [sentence.number for sentence in sentences] == list(range(1, len(expected) + 1))
    assert [
        {"unit": sentence.unit, "text": text[sentence.start:sentence.end].decode()}
        for sentence in sentences
    ] == expected


def test_abbreviation_heavy_paragraph_splits_in_linear_time():
    text = b"Mr. " * ABBREVIATION_RUN_LENGTH + b"End."
    started = time.perf_counter()
    sentences = split_sentences(text)
    assert time.perf_counter() - started < SPLIT_SECONDS_LIMIT
    assert [(sentence.start, sentence.end) for sentence in sentences] == [(0, len(text))]


def fastest_split_seconds(text):
    """Return the fastest of several timed splits of a text."""
    timings = []
    for _ in range(TIMING_RUNS):
        started = time.perf_counter()
        split_sentences(text)
        timings.append(time.perf_counter() - started)
    return min(timings)


def split_time_growth(make_text, size):
    """Return how many times longer splitting takes when the text grows by the growth factor."""
    return fastest_split_seconds(make_text(size * GROWTH_FACTOR)) / fastest_split_seconds(make_text(size))


def test_many_sentence_paragraph_splits_in_linear_time():
    assert split_time_growth(lambda size: b"Go. " * size, SENTENCE_PROBE_SIZE) < LINEAR_GROWTH_LIMIT
