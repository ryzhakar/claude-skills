import time
from pathlib import Path

import pytest
import yaml
from hypothesis import given, strategies as st

from instruction_eval.coverage import split_sentences

MARKDOWN_ALPHABET = "ab. !?-*#>|`~\n\t1)e.g"

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "sentence-split"
FIXTURE_NAMES = sorted(path.stem for path in FIXTURE_DIR.glob("*.md"))
ABBREVIATION_RUN_LENGTH = 20_000
SPLIT_SECONDS_LIMIT = 2
SENTENCE_PROBE_SIZE = 20_000
WORD_PROBE_SIZE = 5_000
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


def test_long_word_before_terminator_splits_in_linear_time():
    assert split_time_growth(lambda size: b"a" * size + b" b.", WORD_PROBE_SIZE) < LINEAR_GROWTH_LIMIT


@given(st.text(alphabet=MARKDOWN_ALPHABET).map(str.encode))
def test_sentences_are_numbered_from_one_in_order_without_overlap_each_a_non_blank_span_inside_the_text(text):
    sentences = split_sentences(text)
    assert [sentence.number for sentence in sentences] == list(range(1, len(sentences) + 1))
    assert all(0 <= sentence.start < sentence.end <= len(text) for sentence in sentences)
    assert all(earlier.end <= later.start and earlier.unit <= later.unit for earlier, later in zip(sentences, sentences[1:]))
    assert all(text[sentence.start:sentence.end].strip() for sentence in sentences)


def sentence_texts(text: bytes) -> list[bytes]:
    """Return the bytes of each sentence the text splits into."""
    return [text[sentence.start : sentence.end] for sentence in split_sentences(text)]


def test_an_exact_fence_line_opens_a_frontmatter_block_counted_as_one_sentence():
    assert sentence_texts(b"---\ntitle: x\n---\nBe terse.\n") == [b"---\ntitle: x\n---", b"Be terse."]


@pytest.mark.parametrize(
    ("text", "sentences"),
    [
        (b"--- \ntitle: x\n---\nBe terse.\n", [b"--- ", b"title: x", b"---", b"Be terse."]),
        (b"---\t\ntitle: x\n---\nBe terse.\n", [b"---\t", b"title: x", b"---", b"Be terse."]),
        (b"---\r\ntitle: x\r\n---\r\nBe terse.\r\n", [b"---\r", b"title: x", b"---\r", b"Be terse."]),
    ],
)
def test_a_fence_line_with_trailing_whitespace_or_a_carriage_return_opens_no_frontmatter_block(text, sentences):
    assert sentence_texts(text) == sentences
