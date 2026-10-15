from pathlib import Path

import pytest

from instruction_eval.conditions import revision_condition_texts

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "condition-texts"
OMISSION_CASES = sorted(
    (case.name, expected.stem)
    for case in FIXTURE_DIR.iterdir()
    for expected in case.glob("omit-*.md")
)


def test_instruction_condition_is_the_instruction_bytes():
    instruction = "# Rules\n\nWrite briefly. Cite sources.\n".encode()
    assert revision_condition_texts(instruction, "none") == {"instruction": instruction}


def test_every_sentence_omissions_give_one_omission_per_sentence():
    instruction = b"# Rules\n\nWrite briefly. Cite sources.\n"
    texts = revision_condition_texts(instruction, "every-sentence")
    assert list(texts) == ["instruction", "omit-1", "omit-2", "omit-3"]


@pytest.mark.parametrize(("case", "condition"), OMISSION_CASES)
def test_omission_removes_its_sentence_and_the_whitespace_that_held_it(case, condition):
    instruction = (FIXTURE_DIR / case / "instruction.md").read_bytes()
    texts = revision_condition_texts(instruction, "every-sentence")
    assert texts[condition] == (FIXTURE_DIR / case / f"{condition}.md").read_bytes()
