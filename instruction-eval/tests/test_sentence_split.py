from pathlib import Path

import pytest
import yaml

from instruction_eval.coverage import split_sentences

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "sentence-split"
FIXTURE_NAMES = sorted(path.stem for path in FIXTURE_DIR.glob("*.md"))


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
