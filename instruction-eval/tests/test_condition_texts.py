from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from instruction_eval.conditions import UnclosedFrontmatter, control_texts, revision_condition_texts
from instruction_eval.records import Conditions
from instruction_eval.tasks import words

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


def conditions_with(controls):
    """Return a conditions record holding the given controls."""
    return Conditions(controls=controls, aim="Answers stay short.", placebo_source=Path("/placebo.md"), omissions="none")


def test_empty_control_is_zero_bytes():
    texts = control_texts(conditions_with(("empty",)), b"Write briefly.\n", {}, "Filler words.")
    assert texts == {"empty": b""}


def test_placebo_repeats_the_source_words_with_case_kept_to_r1_word_count():
    first_instruction = b"Write one short answer, then stop: no lists ever.\n"
    texts = control_texts(conditions_with(("placebo",)), first_instruction, {}, "The Harbor's tide -- rolls in.\n")
    assert texts == {"placebo": b"The Harbor's tide rolls in The Harbor's tide rolls"}


@given(st.text(), st.text().filter(words))
def test_placebo_word_count_equals_r1_word_count_on_every_recompute(first_instruction, placebo_source):
    conditions = conditions_with(("placebo",))
    first_bytes = first_instruction.encode()
    placebo = control_texts(conditions, first_bytes, {}, placebo_source)["placebo"]
    assert len(words(placebo.decode())) == len(words(first_instruction))
    assert control_texts(conditions, first_bytes, {}, placebo_source)["placebo"] == placebo


def test_aim_control_is_the_aim_line():
    texts = control_texts(conditions_with(("aim",)), b"Write briefly.\n", {}, "Filler words.")
    assert texts == {"aim": b"Answers stay short."}


def test_controls_texts_are_given_for_exactly_the_controls_held():
    texts = control_texts(conditions_with(("placebo", "empty", "aim")), b"Write briefly.\n", {}, "Filler words.")
    assert list(texts) == ["placebo", "empty", "aim"]


def test_source_joins_the_sources_in_order_without_frontmatter_by_two_newlines():
    sources = {"1-source/b.md": "---\nname: b\n---\nSecond file.\n", "1-source/a.md": "First file.\n"}
    texts = control_texts(conditions_with(("source",)), b"", sources, "")
    assert texts == {"source": b"Second file.\n\n\nFirst file.\n"}


def test_source_with_unclosed_frontmatter_is_refused_by_its_series_path():
    sources = {"1-source/a.md": "---\nname: a\nBody.\n"}
    with pytest.raises(UnclosedFrontmatter, match="^unclosed frontmatter: 1-source/a.md$"):
        control_texts(conditions_with(("source",)), b"", sources, "")
