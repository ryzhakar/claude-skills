import re
from importlib.resources import files
from pathlib import Path

import pytest

from instruction_eval.judge import render_brief
from instruction_eval.records import DEFAULT_BINDING, Demands, JudgeDemand, LongSentencesDemand, PatternDemand, Refusal
from series_fixtures import OTHER_BINDING

BRIEF = "Bind through {SKILL} to:\n{SOURCE}\nCount:\n{DEMANDS}\nEntries:\n{PACKET}\nWrite to {OUT}\n"
BINDING_SKILL = OTHER_BINDING["skill"]
TERSE = JudgeDemand(id="d-terse", text="Keep it short.", boundary="Under 100 words.")
PLAIN = JudgeDemand(id="d-plain", text="Use plain words.", boundary="No jargon.")
NO_EMOJI = PatternDemand(id="d-no-emoji", text="No emoji.", boundary="Any emoji.", pattern=re.compile("[\U0001F600-\U0001F64F]"))
SHORT_SENTENCES = LongSentencesDemand(id="d-short", text="Short sentences.", boundary="Over 20 words.", limit=20)
DEMANDS = Demands(demands=(TERSE, NO_EMOJI, PLAIN, SHORT_SENTENCES))
SOURCES = {"style.md": "---\nname: style\n---\nBe brief.\n", "voice.md": "Speak plainly.\n"}
PACKET = "## b0000000a\n\nHello.\n"
VERDICT_PATH = Path("/series/r1/7-verdicts/t-one/k1.yaml")


def render(
    brief: str = BRIEF, sources: dict[str, str] = SOURCES, gate_demand_ids: frozenset[str] = frozenset({"d-terse", "d-no-emoji"}), binding_skill: str = BINDING_SKILL
) -> str:
    return render_brief(
        brief,
        binding_skill=binding_skill,
        sources=sources,
        demands=DEMANDS,
        gate_demand_ids=gate_demand_ids,
        packet=PACKET,
        verdict_path=VERDICT_PATH,
        reader_model="claude-sonnet-4-5",
        series_name="stop-yapping",
    )


def demand_entry(demand: JudgeDemand | PatternDemand) -> str:
    return f"- id: {demand.id}\n  text: {demand.text}\n  boundary: {demand.boundary}"


def test_a_brief_renders_the_binding_skill_and_each_source_file_under_its_name_stripped_of_frontmatter_and_lists_judge_demands_only():
    assert render() == (
        "Bind through oath:bind to:\n"
        "Source file: style.md\n\nBe brief.\n\n\nSource file: voice.md\n\nSpeak plainly.\n"
        f"\nCount:\n{demand_entry(TERSE)}\n{demand_entry(PLAIN)}\n"
        f"Entries:\n{PACKET}\n"
        "Write to /series/r1/7-verdicts/t-one/k1.yaml\n"
    )


def test_a_brief_without_sources_binds_the_judge_to_the_gate_demands_of_every_counter():
    rendered = render(sources={}, gate_demand_ids=frozenset({"d-terse", "d-no-emoji"}))
    assert rendered.startswith(f"Bind through oath:bind to:\n{demand_entry(TERSE)}\n{demand_entry(NO_EMOJI)}\nCount:\n")


def test_placeholder_text_inside_a_filling_stays_as_written():
    rendered = render(sources={"loop.md": "Write {OUT} and {PACKET} literally.\n"})
    assert "Source file: loop.md\n\nWrite {OUT} and {PACKET} literally.\n" in rendered


@pytest.mark.parametrize("placeholder", ["{SKILL}", "{SOURCE}", "{DEMANDS}", "{PACKET}", "{OUT}"])
def test_a_brief_lacking_a_placeholder_is_refused_naming_it(placeholder):
    with pytest.raises(Refusal, match=rf"^brief fault: {re.escape(placeholder)} appears 0 times, not once$"):
        render(brief=BRIEF.replace(placeholder, "here"))


def test_a_brief_repeating_a_placeholder_is_refused_naming_it():
    with pytest.raises(Refusal, match=r"^brief fault: \{PACKET\} appears 2 times, not once$"):
        render(brief=BRIEF + "Again: {PACKET}\n")


@pytest.mark.parametrize(
    "word",
    ["empty", "Aim", "PLACEBO", "instruction", "omit", "control", "condition", "revision", "reader", "digest", "claude-sonnet-4-5", "stop-yapping"],
)
def test_a_brief_naming_a_condition_word_the_reader_model_or_the_series_is_refused_naming_it(word):
    with pytest.raises(Refusal, match=rf"^brief fault: names {re.escape(word.lower())}$"):
        render(brief=f"{BRIEF}Mind the {word}, as in {word}-3.\n")


def test_a_brief_may_say_source_and_hold_banned_words_inside_longer_words():
    render(brief=f"{BRIEF}Each Source, every aiming reviser, the readers and controls.\n")


SHIPPED_BRIEF = (files("instruction_eval") / "templates" / "judge-brief.md").read_text()


def test_the_shipped_brief_passes_the_brief_rules_with_and_without_sources():
    render(brief=SHIPPED_BRIEF)
    render(brief=SHIPPED_BRIEF, sources={})


@pytest.mark.parametrize("binding_skill", [DEFAULT_BINDING.skill, BINDING_SKILL])
def test_the_shipped_brief_names_the_binding_skill_before_the_entries(binding_skill):
    rendered = render(brief=SHIPPED_BRIEF, binding_skill=binding_skill)
    assert -1 < rendered.find(binding_skill) < rendered.find(PACKET)


@pytest.mark.parametrize(
    "asks",
    [
        "breach count per listed demand",
        "`done`",
        "`kind`",
        "`notes`",
        "`answer`: attempts the request with content",
        "`probe`: holds only a command, question, or request for input meant to precede an answer",
        "`refusal`: declines the request",
        "`blank`: holds no characters or only whitespace",
        "`true` for a correct answer however terse",
        "`false` for a wrong, evasive, probe, refusal, or blank reply",
        "`null` when the reply gives no ground to decide",
    ],
)
def test_the_shipped_brief_asks_per_entry_for_breaches_done_kind_and_notes_with_their_definitions(asks):
    assert asks in SHIPPED_BRIEF
