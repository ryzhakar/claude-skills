import math
import re
from datetime import datetime, timedelta, timezone
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import TypeVar

import pytest
import yaml

from instruction_eval.records import (
    Acceptance,
    AgentRaters,
    AgentReader,
    Binding,
    Budget,
    CommandReader,
    Conditions,
    Conversation,
    Coverage,
    Demands,
    Dropped,
    Gate,
    GateCheck,
    Hypothesis,
    JudgeDemand,
    LongSentencesDemand,
    MoveChange,
    PatternDemand,
    Plan,
    PredictedMovement,
    Refusal,
    SentenceChange,
    Series,
    Task,
    Tasks,
    SeriesFolder,
    SeriesRecords,
    UserRaters,
    reply_path,
    write_file,
)
from series_fixtures import write_yaml

FIXTURES = Path(__file__).parent / "fixtures" / "user-record-schemas"


def fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text())


Loaded = TypeVar("Loaded")
HYPOTHESIS_REPLIES = {"b3f9a01c2": 1, "b00ffa917": 2}


def loaded(tmp_path: Path, load: Callable[[SeriesRecords], Loaded], documents: Mapping[str, object]) -> Loaded:
    """Write each document, YAML or raw bytes, at its series path and return what the series loader loads."""
    files = SeriesFolder(tmp_path / "series")
    for path, document in documents.items():
        if isinstance(document, bytes):
            write_file(files, path, document)
        else:
            write_yaml(files, path, document)
    return load(SeriesRecords(files))


def load_series(tmp_path: Path, document: object) -> Series:
    """Load `series.yaml` written as the document."""
    return loaded(tmp_path, SeriesRecords.series, {"series.yaml": document})


def load_demands(tmp_path: Path, document: object) -> Demands:
    """Load `2-demands.yaml` written as the document."""
    return loaded(tmp_path, SeriesRecords.demands, {"2-demands.yaml": document})


def load_tasks(tmp_path: Path, document: object) -> Tasks:
    """Load `3-tasks.yaml` written as the document beside the fixture demands it tempts."""
    return loaded(tmp_path, SeriesRecords.tasks, {"2-demands.yaml": fixture("2-demands.yaml"), "3-tasks.yaml": document})


def load_conditions(tmp_path: Path, document: object, series: object) -> Conditions:
    """Load `4-conditions.yaml` written as the document in the series written as `series`."""
    return loaded(tmp_path, SeriesRecords.conditions, {"series.yaml": series, "4-conditions.yaml": document})


def load_reader(tmp_path: Path, document: dict) -> object:
    """Load `5-reader.yaml` written as the document in a series of the reader kind it names."""
    reader_kind = document.get("kind") if document.get("kind") in ("agent", "command") else "agent"
    return loaded(tmp_path, SeriesRecords.reader, {"series.yaml": edited("series.yaml", reader_kind=reader_kind), "5-reader.yaml": document})


def load_gate(tmp_path: Path, document: object) -> Gate:
    """Load `7-gate.yaml` written as the document in an unfrozen series."""
    return loaded(tmp_path, SeriesRecords.gate, {"7-gate.yaml": document})


def load_plan(tmp_path: Path, document: object) -> Plan:
    """Load calibration attempt 1's `plan.yaml` written as the document."""
    return loaded(tmp_path, lambda records: records.plan(1), {"6-judge/calibration/attempt-1/plan.yaml": document})


def hypothesis_origins() -> dict:
    """Return r1's origins holding each blind id the fixture hypothesis reads as an open reply."""
    ids = {
        blind_id: {"packet": "explain-tides", "condition": "instruction", "task": "explain-tides", "split": "open", "repeat": repeat, "borrowed_from": None}
        for blind_id, repeat in HYPOTHESIS_REPLIES.items()
    }
    return {"ids": ids, "packets": {"explain-tides": "a" * 64}, "inputs": {}}


def load_hypothesis(tmp_path: Path, document: object) -> Hypothesis:
    """Load r2's `1-hypothesis.yaml` written as the document beside the demands, r1 coverage, and r1 origins it names."""
    replies = {reply_path("r1", "instruction", "explain-tides", repeat, None): b"reply" for repeat in HYPOTHESIS_REPLIES.values()}
    documents = {
        "2-demands.yaml": fixture("2-demands.yaml"),
        "r1/3-coverage.yaml": fixture("3-coverage.yaml"),
        "r1/6-origins.yaml": hypothesis_origins(),
        **replies,
        "r2/1-hypothesis.yaml": document,
    }
    return loaded(tmp_path, lambda records: records.hypothesis("r2"), documents)


def load_coverage(tmp_path: Path, document: object) -> Coverage:
    """Load r1's `3-coverage.yaml` written as the document beside the demands it maps."""
    return loaded(tmp_path, lambda records: records.coverage("r1"), {"2-demands.yaml": fixture("2-demands.yaml"), "r1/3-coverage.yaml": document})


def test_series_loads_as_typed_record(tmp_path):
    series = load_series(tmp_path, fixture("series.yaml"))
    assert series == Series(
        instruction=Path("/home/writer/instructions/terse.md"),
        sources=(Path("/home/writer/sources/strunk.md"), Path("/home/writer/sources/orwell.md")),
        reader_kind="agent",
        binding=Binding(plugin="oath@elsewhere", skill="oath:bind"),
        created=datetime(2026, 10, 14, 10, tzinfo=timezone(timedelta(hours=3))),
        inputs={},
    )


ABSENT = object()


def edited(name: str, **changes: object) -> dict:
    document = fixture(name)
    for key, value in changes.items():
        if value is ABSENT:
            del document[key]
        else:
            document[key] = value
    return document


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"reader_kind": "human"}, "reader_kind"),
        ({"instruction": "instructions/terse.md"}, "instruction"),
        ({"sources": ["/a.md", "b.md"]}, "sources[1]"),
        ({"created": "2026-10-14T10:00:00"}, "created"),
        ({"inputs": {"2-demands.yaml": "ABC"}}, "2-demands.yaml"),
        ({"inputs": {"2-demands.yaml": "a" * 64 + "\n"}}, "2-demands.yaml"),
        ({"inputs": ["2-demands.yaml"]}, "inputs"),
        ({"created": ABSENT}, "created"),
        ({"cause": "too long"}, "cause"),
        ({"binding": ABSENT}, "binding"),
        ({"binding": {"plugin": "oath@elsewhere"}}, "binding: missing skill"),
        ({"binding": {"plugin": "oath@elsewhere", "skill": "oath:bind", "marketplace": "elsewhere"}}, "binding: unknown marketplace"),
        ({"binding": {"plugin": "", "skill": "oath:bind"}}, "binding.plugin"),
        ({"binding": {"plugin": "oath@elsewhere", "skill": "oath:\nbind"}}, "binding.skill"),
    ],
)
def test_series_refuses_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_series(tmp_path, edited("series.yaml", **changes))


def test_a_series_made_before_the_binding_setting_is_refused_naming_the_missing_binding(tmp_path):
    with pytest.raises(Refusal, match=r"^malformed record: series\.yaml \(record: missing binding\)$"):
        load_series(tmp_path, edited("series.yaml", binding=ABSENT))


def test_demands_load_as_one_variant_per_counter(tmp_path):
    demands = load_demands(tmp_path, fixture("2-demands.yaml"))
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
        (JUDGE, {"id": "active-voice\n"}, "demands[2].id"),
        (JUDGE, {"boundary": ""}, "demands[2].boundary"),
    ],
)
def test_demands_refuse_a_malformed_demand(tmp_path, index, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_demands(tmp_path, edited_entry("2-demands.yaml", "demands", index, **changes))


def test_demands_refuse_an_empty_list(tmp_path):
    with pytest.raises(Refusal, match="non-empty"):
        load_demands(tmp_path, {"demands": []})


def test_tasks_load_with_compiled_answer_keys(tmp_path):
    tasks = load_tasks(tmp_path, fixture("3-tasks.yaml"))
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
def test_tasks_refuse_a_malformed_entry(tmp_path, list_key, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_tasks(tmp_path, edited_entry("3-tasks.yaml", list_key, 0, **changes))


def series_with_sources() -> dict:
    return fixture("series.yaml")


def series_without_sources() -> dict:
    return edited("series.yaml", sources=[])


def test_conditions_load_with_every_control_when_the_series_has_sources(tmp_path):
    conditions = load_conditions(tmp_path, fixture("4-conditions.yaml"), series_with_sources())
    assert conditions == Conditions(
        controls=("empty", "aim", "placebo", "source"),
        aim="Make every reply terse.",
        placebo_source=Path("/home/writer/placebo/gardening.md"),
        omissions="every-sentence",
    )


def test_conditions_load_without_source_control_when_the_series_has_no_sources(tmp_path):
    conditions = load_conditions(tmp_path, edited("4-conditions.yaml", controls=["placebo", "empty", "aim"]), series_without_sources())
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
def test_conditions_refuse_a_control_set_the_sources_do_not_call_for(tmp_path, controls, series):
    with pytest.raises(Refusal, match="controls"):
        load_conditions(tmp_path, edited("4-conditions.yaml", controls=controls), series())


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
def test_conditions_refuse_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_conditions(tmp_path, edited("4-conditions.yaml", **changes), series_with_sources())


def test_agent_reader_loads_as_its_variant(tmp_path):
    assert load_reader(tmp_path, fixture("5-reader-agent.yaml")) == AgentReader(model="claude-sonnet-4-5")


def test_command_reader_loads_as_its_variant(tmp_path):
    assert load_reader(tmp_path, fixture("5-reader-command.yaml")) == CommandReader(
        model="gpt-5-mini",
        command=("llm-reply", "--system-file", "{condition}"),
        fingerprint=("llm-reply", "--version"),
        sampling={"temperature": 0.7, "max_tokens": 1024, "seed": "fixed"},
    )


@pytest.mark.parametrize("key", ["command", "fingerprint", "sampling"])
def test_agent_reader_refuses_a_command_reader_key(tmp_path, key):
    command_reader = fixture("5-reader-command.yaml")
    with pytest.raises(Refusal, match=key):
        load_reader(tmp_path, edited("5-reader-agent.yaml", **{key: command_reader[key]}))


@pytest.mark.parametrize("key", ["command", "fingerprint", "sampling"])
def test_command_reader_refuses_a_missing_variant_key(tmp_path, key):
    with pytest.raises(Refusal, match=key):
        load_reader(tmp_path, edited("5-reader-command.yaml", **{key: ABSENT}))


@pytest.mark.parametrize("alias", ["sonnet", "opus", "haiku", "fable", "inherit"])
@pytest.mark.parametrize("variant", ["5-reader-agent.yaml", "5-reader-command.yaml"])
def test_reader_refuses_a_model_alias(tmp_path, variant, alias):
    with pytest.raises(Refusal, match="model"):
        load_reader(tmp_path, edited(variant, model=alias))


@pytest.mark.parametrize("model", ["gpt-5-mini", "claude", "claude-", "Claude-sonnet-4-5", "claude-sonnet-4-5 ", "claude-sonnet-4-5\n"])
def test_agent_reader_refuses_a_model_outside_the_claude_pattern(tmp_path, model):
    with pytest.raises(Refusal, match="model"):
        load_reader(tmp_path, edited("5-reader-agent.yaml", model=model))


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"kind": "script"}, "kind"),
        ({"model": ""}, "model"),
        ({"command": ["llm-reply", "--system-file"]}, "command"),
        ({"command": ["llm-reply", "{condition}", "{condition}"]}, "command"),
        ({"command": ["llm-reply", 7, "{condition}"]}, "command[1]"),
        ({"fingerprint": "llm-reply --version"}, "fingerprint"),
        ({"sampling": {"temperature": [0.7]}}, "sampling"),
        ({"sampling": {"stop": None}}, "sampling"),
    ],
)
def test_command_reader_refuses_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_reader(tmp_path, edited("5-reader-command.yaml", **changes))


def test_gate_loads_every_key(tmp_path):
    assert load_gate(tmp_path, fixture("7-gate.yaml")) == Gate(
        repeats=5,
        level=0.95,
        done_by="answer-key",
        checks=(
            GateCheck(compares="instruction-vs-empty", gap=0.5),
            GateCheck(compares="instruction-vs-aim", gap=0.5),
            GateCheck(compares="instruction-vs-placebo", gap=0.25),
            GateCheck(compares="completion", gap=0.1),
            GateCheck(compares="drift", gap=1),
        ),
        keep_rule="best-estimate-shortest",
        budget=Budget(unit="tokens", ceiling=2000000),
    )


def test_gate_loads_with_only_the_step_four_keys(tmp_path):
    assert load_gate(tmp_path, {"repeats": 3, "level": 0.9, "done_by": "judge"}) == Gate(
        repeats=3, level=0.9, done_by="judge", checks=None, keep_rule=None, budget=None
    )


def test_gate_loads_an_unbounded_budget(tmp_path):
    assert load_gate(tmp_path, edited("7-gate.yaml", budget="none")).budget == "none"


@pytest.mark.parametrize("compares", ["instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion"])
def test_gate_refuses_checks_lacking_a_required_comparison(tmp_path, compares):
    checks = [check for check in fixture("7-gate.yaml")["checks"] if check["compares"] != compares]
    with pytest.raises(Refusal, match=re.escape(compares)):
        load_gate(tmp_path, edited("7-gate.yaml", checks=checks))


def test_gate_refuses_a_repeated_comparison(tmp_path):
    checks = fixture("7-gate.yaml")["checks"] + [{"compares": "drift", "gap": 2}]
    with pytest.raises(Refusal, match="drift"):
        load_gate(tmp_path, edited("7-gate.yaml", checks=checks))


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"repeats": 1}, "repeats"),
        ({"level": 1}, "level"),
        ({"level": 0}, "level"),
        ({"level": True}, "level"),
        ({"done_by": "reader"}, "done_by"),
        ({"keep_rule": "shortest"}, "keep_rule"),
        ({"budget": "unlimited"}, "budget"),
        ({"budget": {"unit": "dollars", "ceiling": 5}}, "budget.unit"),
        ({"budget": {"unit": "seconds", "ceiling": 0}}, "budget.ceiling"),
        ({"budget": {"unit": "seconds", "ceiling": math.inf}}, "budget.ceiling"),
        ({"checks": [{"compares": "instruction-vs-empty", "gap": 0}]}, "checks[0].gap"),
        ({"checks": [{"compares": "instruction-vs-empty", "gap": math.nan}]}, "checks[0].gap"),
        ({"checks": [{"compares": "instruction-vs-empty", "gap": math.inf}]}, "checks[0].gap"),
        ({"checks": [{"compares": "instruction-vs-source", "gap": 1}]}, "checks[0].compares"),
    ],
)
def test_gate_refuses_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_gate(tmp_path, edited("7-gate.yaml", **changes))


def test_plan_loads_with_agent_raters(tmp_path):
    assert load_plan(tmp_path, fixture("plan.yaml")) == Plan(
        judge_model="claude-opus-4-1",
        raters=AgentRaters(rater_model="claude-sonnet-4-5"),
        sample_size=12,
        anchors_per_packet=3,
        acceptance=Acceptance(breach_difference=0.5, self_difference=0.25, done_agreement=0.8),
    )


def test_plan_loads_with_the_user_as_rater(tmp_path):
    assert load_plan(tmp_path, edited("plan.yaml", raters=["user"], rater_model=ABSENT)).raters == UserRaters()


@pytest.mark.parametrize("raters", [["agent"], ["user", "user"], ["user", "agent"], ["agent", "agent", "agent"], [], "user"])
def test_plan_refuses_another_rater_set(tmp_path, raters):
    with pytest.raises(Refusal, match="raters"):
        load_plan(tmp_path, edited("plan.yaml", raters=raters))


def test_plan_refuses_a_rater_model_equal_to_the_judge_model(tmp_path):
    with pytest.raises(Refusal, match="rater_model"):
        load_plan(tmp_path, edited("plan.yaml", rater_model="claude-opus-4-1"))


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"rater_model": ABSENT}, "rater_model"),
        ({"raters": ["user"]}, "rater_model"),
        ({"judge_model": "opus"}, "judge_model"),
        ({"rater_model": "sonnet"}, "rater_model"),
        ({"judge_model": "gpt-5"}, "judge_model"),
        ({"sample_size": 0}, "sample_size"),
        ({"anchors_per_packet": 2}, "anchors_per_packet"),
        ({"acceptance": {"breach_difference": -0.1, "self_difference": 0, "done_agreement": 0.5}}, "acceptance.breach_difference"),
        ({"acceptance": {"breach_difference": 0, "self_difference": -1, "done_agreement": 0.5}}, "acceptance.self_difference"),
        ({"acceptance": {"breach_difference": 0, "self_difference": 0, "done_agreement": 1.5}}, "acceptance.done_agreement"),
        ({"acceptance": {"breach_difference": 0, "self_difference": 0}}, "done_agreement"),
    ],
)
def test_plan_refuses_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_plan(tmp_path, edited("plan.yaml", **changes))


def test_hypothesis_loads_a_move(tmp_path):
    assert load_hypothesis(tmp_path, fixture("1-hypothesis.yaml")) == Hypothesis(
        failing_demand="short-sentences",
        replies_read=("b3f9a01c2", "b00ffa917"),
        change=MoveChange(sentence=4, to=1),
        predicted_movement=PredictedMovement(direction="down", size=0.6),
    )


@pytest.mark.parametrize("action", ["rewrite", "add", "delete"])
def test_hypothesis_loads_a_change_in_place(tmp_path, action):
    hypothesis = load_hypothesis(tmp_path, edited("1-hypothesis.yaml", change={"action": action, "sentence": 2}, failing_demand="completion"))
    assert (hypothesis.change, hypothesis.failing_demand) == (SentenceChange(action=action, sentence=2), "completion")


def test_hypothesis_refuses_a_cause(tmp_path):
    with pytest.raises(Refusal, match="cause"):
        load_hypothesis(tmp_path, edited("1-hypothesis.yaml", cause="the rule sits too late"))


def test_hypothesis_refuses_a_cause_inside_the_change(tmp_path):
    with pytest.raises(Refusal, match="cause"):
        load_hypothesis(tmp_path, edited("1-hypothesis.yaml", change={"action": "move", "sentence": 4, "to": 1, "cause": "buried"}))


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"failing_demand": "Short"}, "failing_demand"),
        ({"replies_read": ["b3f9a01c"]}, "replies_read[0]"),
        ({"replies_read": ["b3f9a01c2\n"]}, "replies_read[0]"),
        ({"replies_read": ["short-sentences"]}, "replies_read[0]"),
        ({"change": {"action": "move", "sentence": 4}}, "change"),
        ({"change": {"action": "rewrite", "sentence": 4, "to": 1}}, "change"),
        ({"change": {"action": "swap", "sentence": 4}}, "change.action"),
        ({"change": {"action": "delete", "sentence": 0}}, "change.sentence"),
        ({"change": {"action": "move", "sentence": 4, "to": 0}}, "change.to"),
        ({"predicted_movement": {"direction": "sideways", "size": 1}}, "predicted_movement.direction"),
        ({"predicted_movement": {"direction": "up", "size": 0}}, "predicted_movement.size"),
        ({"predicted_movement": {"direction": "up", "size": math.nan}}, "predicted_movement.size"),
    ],
)
def test_hypothesis_refuses_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_hypothesis(tmp_path, edited("1-hypothesis.yaml", **changes))


def test_coverage_loads_both_maps(tmp_path):
    assert load_coverage(tmp_path, fixture("3-coverage.yaml")) == Coverage(
        demands={
            "short-sentences": (1, 3),
            "no-hedges": (2,),
            "active-voice": Dropped(reason="The writer judged it unmeasurable here."),
        },
        sentences={1: ("short-sentences",), 2: ("no-hedges",), 3: ("short-sentences",)},
    )


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"demands": {"short-sentences": []}}, "demands[short-sentences]"),
        ({"demands": {"short-sentences": [0]}}, "demands[short-sentences][0]"),
        ({"demands": {"short-sentences": {"dropped": ""}}}, "demands[short-sentences].dropped"),
        ({"demands": {"short-sentences": {"dropped": "x", "cause": "y"}}}, "cause"),
        ({"demands": {"Short": [1]}}, "demands key"),
        ({"sentences": {1: []}}, "sentences[1]"),
        ({"sentences": {"one": ["short-sentences"]}}, "sentences key"),
        ({"sentences": {0: ["short-sentences"]}}, "sentences key"),
        ({"sentences": {1: ["Short"]}}, "sentences[1][0]"),
        ({"imported": [4]}, "imported"),
    ],
)
def test_coverage_refuses_a_malformed_key(tmp_path, changes, named):
    with pytest.raises(Refusal, match=re.escape(named)):
        load_coverage(tmp_path, edited("3-coverage.yaml", **changes))
