import argparse
import re

import pytest
from hypothesis import given, strategies as st

from instruction_eval.cli import _build_parser

SERIES_NEW = ["series", "new", "demo", "--instruction", "i.md", "--reader-kind", "agent"]
EVERY_COMMAND = [
    ["series", "status"], ["series", "freeze"], ["series", "keep"],
    ["demands", "check"], ["coverage", "check", "r1"], ["tasks", "check"],
    ["reader", "fingerprint"], ["reader", "prepare", "r1"],
    ["revision", "ask", "r1"], ["revision", "collect", "r1"], ["revision", "blind", "r1"],
    ["revision", "detect", "r1"], ["revision", "score", "r1"], ["revision", "gate", "r1"],
    ["revision", "new"], ["judge", "calibrate"], ["judge", "prepare", "r1"],
    ["judge", "collect", "r1"],
]


def parse(*argv):
    return _build_parser().parse_args(list(argv))


def test_help_prints_the_twelve_steps_of_the_order_of_work(capsys):
    with pytest.raises(SystemExit):
        parse("--help")
    help_text = capsys.readouterr().out
    assert "Order of work" in help_text
    for step in range(1, 13):
        assert f"\n{step}. " in help_text
    assert "claudes run readers" in help_text
    assert "series keep" in help_text.split("\n12. ")[1]


def test_series_new_collects_two_source_flags_in_order():
    parsed = parse(*SERIES_NEW, "--source", "a.md", "--source", "b.md")
    assert parsed.sources == ["a.md", "b.md"]
    assert parsed.name == "demo"
    assert parsed.instruction == "i.md"
    assert parsed.reader_kind == "agent"


def test_series_new_without_source_has_an_empty_source_list():
    assert parse(*SERIES_NEW).sources == []


def test_reader_kind_is_a_closed_enum(capsys):
    with pytest.raises(SystemExit):
        parse("series", "new", "demo", "--instruction", "i.md", "--reader-kind", "human")
    assert "invalid choice" in capsys.readouterr().err


def test_reader_kind_is_required():
    with pytest.raises(SystemExit):
        parse("series", "new", "demo", "--instruction", "i.md")


CONDITION_NAMES = st.text(
    alphabet=st.characters(blacklist_characters="-", blacklist_categories=("Cs",)),
    min_size=1,
)


@given(names=st.lists(CONDITION_NAMES))
def test_revision_ask_returns_repeated_conditions_in_order(names):
    flags = [part for name in names for part in ("--conditions", name)]
    assert parse("revision", "ask", "r2", *flags).conditions == names


def test_revision_ask_without_conditions_leaves_the_list_empty():
    assert parse("revision", "ask", "r1").conditions == []


@given(number=st.integers(min_value=0).map(str))
def test_revision_id_of_r_then_digits_is_accepted(number):
    assert parse("revision", "ask", f"r{number}").revision == f"r{number}"


@given(text=st.text(alphabet=st.characters(blacklist_categories=("Cs",))).filter(
    lambda text: not re.fullmatch(r"r[0-9]+", text) and not text.startswith("-")
))
def test_revision_id_not_r_then_digits_is_refused(text):
    with pytest.raises(SystemExit):
        parse("revision", "ask", text)


def test_series_stop_takes_a_reason_value():
    assert parse("series", "stop", "--reason", "gate passed").reason == "gate passed"


def test_series_stop_refuses_a_reason_flag_without_value():
    with pytest.raises(SystemExit):
        parse("series", "stop", "--reason")


@pytest.mark.parametrize("command", EVERY_COMMAND)
def test_every_command_in_the_table_parses(command):
    parsed = parse(*command)
    assert (parsed.group, parsed.verb) == (command[0], command[1])


def all_parsers(parser):
    yield parser
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for child in action.choices.values():
                yield from all_parsers(child)


def test_no_flag_takes_no_value():
    valueless = [
        option
        for parser in all_parsers(_build_parser())
        for action in parser._actions
        if action.option_strings and action.nargs == 0 and action.dest != "help"
        for option in action.option_strings
    ]
    assert valueless == []
