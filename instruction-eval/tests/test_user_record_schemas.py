import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

from instruction_eval.records import (
    Conditions,
    Conversation,
    Demands,
    JudgeDemand,
    LongSentencesDemand,
    PatternDemand,
    RecordRefused,
    Series,
    Task,
    Tasks,
    parse_conditions,
    parse_demands,
    parse_series,
    parse_tasks,
)

FIXTURES = Path(__file__).parent / "fixtures" / "user-record-schemas"


def fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text())


def test_series_loads_as_typed_record():
    series = parse_series(fixture("series.yaml"))
    assert series == Series(
        instruction=Path("/home/writer/instructions/terse.md"),
        sources=(Path("/home/writer/sources/strunk.md"), Path("/home/writer/sources/orwell.md")),
        reader_kind="agent",
        created=datetime(2026, 10, 14, 10, tzinfo=timezone(timedelta(hours=3))),
        inputs={},
    )


def edited(name: str, **changes: object) -> dict:
    document = fixture(name)
    for key, value in changes.items():
        if value is ABSENT:
            del document[key]
        else:
            document[key] = value
    return document


ABSENT = object()


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"reader_kind": "human"}, "reader_kind"),
        ({"instruction": "instructions/terse.md"}, "instruction"),
        ({"sources": ["/a.md", "b.md"]}, "sources[1]"),
        ({"created": "2026-10-14T10:00:00"}, "created"),
        ({"inputs": {"2-demands.yaml": "ABC"}}, "inputs"),
        ({"created": ABSENT}, "created"),
        ({"cause": "too long"}, "cause"),
    ],
)
def test_series_refuses_a_malformed_key(changes, named):
    with pytest.raises(RecordRefused, match=re.escape(named)):
        parse_series(edited("series.yaml", **changes))


def test_demands_load_as_one_variant_per_counter():
    demands = parse_demands(fixture("2-demands.yaml"))
    assert demands == Demands(
        demands=(
            LongSentencesDemand(id="short-sentences", text="Keep sentences short.", boundary="Quoted material is exempt.", limit=25),
            PatternDemand(
                id="no-hedges",
                text="Never hedge.",
                boundary="Uncertainty stated as a number is not a hedge.",
                pattern=re.compile(r"\b(perhaps|maybe)\b"),
            ),
            JudgeDemand(id="active-voice", text="Prefer the active voice.", boundary="Passive is allowed when the actor is unknown."),
        )
    )


def edited_entry(name: str, list_key: str, index: int, **changes: object) -> dict:
    document = fixture(name)
    entry = document[list_key][index]
    for key, value in changes.items():
        if value is ABSENT:
            del entry[key]
        else:
            entry[key] = value
    return document


LONG_SENTENCES, PATTERN, JUDGE = 0, 1, 2


@pytest.mark.parametrize(
    ("index", "changes", "named"),
    [
        (PATTERN, {"limit": 25}, "limit"),
        (PATTERN, {"pattern": ABSENT}, "pattern"),
        (PATTERN, {"pattern": "(unclosed"}, "demands[1].pattern"),
        (LONG_SENTENCES, {"pattern": "x"}, "pattern"),
        (LONG_SENTENCES, {"limit": 0}, "demands[0].limit"),
        (LONG_SENTENCES, {"limit": True}, "demands[0].limit"),
        (JUDGE, {"pattern": "x"}, "pattern"),
        (JUDGE, {"limit": 3}, "limit"),
        (JUDGE, {"counted_by": "reader"}, "demands[2].counted_by"),
        (JUDGE, {"id": "overreach"}, "reserved"),
        (JUDGE, {"id": "completion"}, "reserved"),
        (JUDGE, {"id": "Active_Voice"}, "demands[2].id"),
        (JUDGE, {"boundary": ""}, "demands[2].boundary"),
    ],
)
def test_demands_refuse_a_malformed_demand(index, changes, named):
    with pytest.raises(RecordRefused, match=re.escape(named)):
        parse_demands(edited_entry("2-demands.yaml", "demands", index, **changes))


def test_demands_refuse_an_empty_list():
    with pytest.raises(RecordRefused, match="non-empty"):
        parse_demands({"demands": []})


def test_tasks_load_with_compiled_answer_keys():
    tasks = parse_tasks(fixture("3-tasks.yaml"))
    assert tasks == Tasks(
        tasks=(
            Task(id="explain-tides", tempts="short-sentences", split="open", message="Why does the sea rise twice a day?", answer_key=None),
            Task(
                id="fix-loop",
                tempts="overreach",
                split="sealed",
                message="My loop prints one number too many. Fix only that.",
                answer_key=re.compile(r"range\(n\)"),
            ),
        ),
        conversations=(
            Conversation(id="plan-trip", split="open", turns=("I want to visit Lisbon in spring.", "Which week has the fewest crowds?")),
        ),
    )


@pytest.mark.parametrize(
    ("list_key", "changes", "named"),
    [
        ("tasks", {"split": "closed"}, "tasks[0].split"),
        ("tasks", {"answer_key": "[unclosed"}, "tasks[0].answer_key"),
        ("tasks", {"answer_key": ABSENT}, "answer_key"),
        ("tasks", {"tempts": "Short Sentences"}, "tasks[0].tempts"),
        ("tasks", {"message": ""}, "tasks[0].message"),
        ("conversations", {"split": "both"}, "conversations[0].split"),
        ("conversations", {"turns": ["fine", 3]}, "conversations[0].turns[1]"),
        ("conversations", {"id": "-plan"}, "conversations[0].id"),
    ],
)
def test_tasks_refuse_a_malformed_entry(list_key, changes, named):
    with pytest.raises(RecordRefused, match=re.escape(named)):
        parse_tasks(edited_entry("3-tasks.yaml", list_key, 0, **changes))


def series_with_sources() -> Series:
    return parse_series(fixture("series.yaml"))


def series_without_sources() -> Series:
    return parse_series(edited("series.yaml", sources=[]))


def test_conditions_load_with_every_control_when_the_series_has_sources():
    conditions = parse_conditions(fixture("4-conditions.yaml"), series_with_sources())
    assert conditions == Conditions(
        controls=("empty", "aim", "placebo", "source"),
        aim="Make every reply terse.",
        placebo_source=Path("/home/writer/placebo/gardening.md"),
        omissions="every-sentence",
    )


def test_conditions_load_without_source_control_when_the_series_has_no_sources():
    conditions = parse_conditions(edited("4-conditions.yaml", controls=["placebo", "empty", "aim"]), series_without_sources())
    assert conditions.controls == ("placebo", "empty", "aim")


@pytest.mark.parametrize(
    ("controls", "series"),
    [
        (["empty", "aim", "placebo"], series_with_sources),
        (["empty", "aim", "placebo", "source"], series_without_sources),
        (["empty", "aim", "placebo", "source", "source"], series_with_sources),
        (["empty", "aim", "source"], series_with_sources),
    ],
)
def test_conditions_refuse_a_control_set_the_sources_do_not_call_for(controls, series):
    with pytest.raises(RecordRefused, match="controls"):
        parse_conditions(edited("4-conditions.yaml", controls=controls), series())


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"controls": ["empty", "aim", "placebo", "source", "silence"]}, "controls[4]"),
        ({"aim": "Make every reply terse.\nAnd kind."}, "aim"),
        ({"aim": "Make every reply terse.\n"}, "aim"),
        ({"aim": ""}, "aim"),
        ({"placebo_source": "placebo/gardening.md"}, "placebo_source"),
        ({"omissions": "some"}, "omissions"),
        ({"omissions": ABSENT}, "omissions"),
    ],
)
def test_conditions_refuse_a_malformed_key(changes, named):
    with pytest.raises(RecordRefused, match=re.escape(named)):
        parse_conditions(edited("4-conditions.yaml", **changes), series_with_sources())
