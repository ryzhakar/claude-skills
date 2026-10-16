import copy
import re
from pathlib import Path

import pytest
import yaml
from hypothesis import given, strategies as st

from instruction_eval.records import Refusal, RecordKind, parse_record

FIXTURES = Path(__file__).parent / "fixtures" / "command-record-schemas"


def load_fixture(kind: RecordKind) -> dict:
    return yaml.safe_load((FIXTURES / f"{kind.value}.yaml").read_text())


def changed(document: dict, path: tuple, value) -> dict:
    result = copy.deepcopy(document)
    target = result
    for step in path[:-1]:
        target = target[step]
    target[path[-1]] = value
    return result


def without(document: dict, path: tuple) -> dict:
    result = copy.deepcopy(document)
    target = result
    for step in path[:-1]:
        target = target[step]
    del target[path[-1]]
    return result


def assert_refused(kind: RecordKind, document: dict, fragment: str) -> None:
    with pytest.raises(Refusal, match=re.escape(fragment)):
        parse_record(kind, document)


def test_stop_record_parses_as_written():
    document = load_fixture(RecordKind.STOP)
    assert parse_record(RecordKind.STOP, document) == document


STOP_REFUSALS = [
    (("stop",), "halted", "stop"),
    (("kept",), "2", "kept"),
    (("extra",), 1, "extra"),
]


@pytest.mark.parametrize("path,value,fragment", STOP_REFUSALS)
def test_stop_record_refuses_bad_value(path, value, fragment):
    assert_refused(RecordKind.STOP, changed(load_fixture(RecordKind.STOP), path, value), fragment)


def test_stop_record_refuses_missing_inputs():
    assert_refused(RecordKind.STOP, without(load_fixture(RecordKind.STOP), ("inputs",)), "inputs")


@pytest.mark.parametrize("stop,reason,accepted", [
    ("unresolvable", "user text", True),
    ("unresolvable", None, False),
    ("capped", "budget", True),
    ("capped", "rounds", False),
    ("capped", None, True),
    ("passed", "budget", False),
    ("no-effect", "x", False),
])
def test_stop_reason_is_present_only_for_unresolvable_and_budget_cap(stop, reason, accepted):
    document = changed(load_fixture(RecordKind.STOP), ("stop",), stop)
    if reason is not None:
        document["reason"] = reason
    if accepted:
        assert parse_record(RecordKind.STOP, document) == document
    else:
        assert_refused(RecordKind.STOP, document, "reason")


def first_revision() -> dict:
    document = load_fixture(RecordKind.REVISION)
    document.update(number=1, parent=None, parent_record=None, change=None)
    return document


def test_revision_record_parses_as_written():
    document = load_fixture(RecordKind.REVISION)
    assert parse_record(RecordKind.REVISION, document) == document


def test_first_revision_has_no_parent_and_no_change():
    document = first_revision()
    assert parse_record(RecordKind.REVISION, document) == document


@pytest.mark.parametrize("path,value", [
    (("number",), 0),
    (("number",), True),
    (("parent",), None),
    (("parent_record",), None),
    (("change",), None),
    (("hash",), "ABC"),
    (("change", "action"), "swap"),
    (("change", "sentence"), 0),
    (("change", "to"), 2),
    (("change", "old"), 5),
])
def test_revision_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.REVISION), path, value)
    assert_refused(RecordKind.REVISION, document, path[-1])


@pytest.mark.parametrize("path,value", [
    (("parent",), "r1"),
    (("parent_record",), "a" * 64),
    (("change",), {"action": "add", "sentence": 1, "old": "", "new": "x"}),
])
def test_first_revision_refuses_parent_fields(path, value):
    assert_refused(RecordKind.REVISION, changed(first_revision(), path, value), path[0])


@pytest.mark.parametrize("change", [
    {"action": "add", "sentence": 2, "old": "gone", "new": "x"},
    {"action": "delete", "sentence": 2, "old": "x", "new": "left"},
    {"action": "move", "sentence": 2, "old": "x", "new": "y", "to": 4},
    {"action": "move", "sentence": 2, "old": "x", "new": "x"},
])
def test_revision_change_text_follows_its_action(change):
    assert_refused(RecordKind.REVISION, changed(load_fixture(RecordKind.REVISION), ("change",), change), "change")


@pytest.mark.parametrize("change", [
    {"action": "add", "sentence": 2, "old": "", "new": "x"},
    {"action": "delete", "sentence": 2, "old": "x", "new": ""},
    {"action": "move", "sentence": 2, "old": "x", "new": "x", "to": 4},
])
def test_revision_change_accepts_each_action(change):
    document = changed(load_fixture(RecordKind.REVISION), ("change",), change)
    assert parse_record(RecordKind.REVISION, document) == document


def test_frozen_record_parses_as_written():
    document = load_fixture(RecordKind.FROZEN)
    assert parse_record(RecordKind.FROZEN, document) == document


def test_frozen_record_accepts_fingerprint_hash_of_command_readers():
    document = changed(load_fixture(RecordKind.FROZEN), ("fingerprint_hash",), "c" * 64)
    assert parse_record(RecordKind.FROZEN, document) == document


@pytest.mark.parametrize("path,value", [
    (("hashes", "series.yaml"), "xyz"),
    (("hashes",), ["series.yaml"]),
    (("noise", "repeats"), 1),
    (("noise", "level"), 1),
    (("noise", "level"), 0),
    (("noise", "z"), 0),
    (("noise", "sigma", "breaches", "empty"), -0.1),
    (("noise", "sigma", "demands", "brevity", "empty"), "high"),
    (("noise", "sigma", "total"), {}),
    (("noise", "checks", "instruction-vs-everything"), 0.1),
    (("noise", "checks", "drift"), -1),
    (("noise", "demands", "Bad Id"), 0.1),
    (("noise", "done_change"), "none"),
    (("fingerprint_hash",), "short"),
    (("tool_version",), ""),
    (("frozen_at",), "2026-10-14T10:00:00"),
    (("frozen_at",), "yesterday"),
])
def test_frozen_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.FROZEN), path, value)
    assert_refused(RecordKind.FROZEN, document, path[-1])


def test_frozen_record_refuses_missing_noise_key():
    document = without(load_fixture(RecordKind.FROZEN), ("noise", "done_change"))
    assert_refused(RecordKind.FROZEN, document, "done_change")


def command_reply() -> dict:
    document = load_fixture(RecordKind.REPLY)
    del document["transcript"], document["transcript_hash"]
    document.update(reader_kind="command", fingerprint_hash="c" * 64, cost=dict(NULL_COST))
    return document


def test_command_reply_refuses_integer_cost():
    document = command_reply()
    document["cost"] = load_fixture(RecordKind.REPLY)["cost"]
    assert_refused(RecordKind.REPLY, document, "cost")


def test_agent_reply_parses_as_written():
    document = load_fixture(RecordKind.REPLY)
    assert parse_record(RecordKind.REPLY, document) == document


def test_command_reply_carries_fingerprint_hash_and_no_transcript():
    document = command_reply()
    assert parse_record(RecordKind.REPLY, document) == document


NULL_COST = {
    "input_tokens": None,
    "cache_creation_input_tokens": None,
    "cache_read_input_tokens": None,
    "output_tokens": None,
    "spent_input_tokens": None,
}


def test_reply_cost_accepts_all_null_fields():
    document = changed(load_fixture(RecordKind.REPLY), ("cost",), dict(NULL_COST))
    assert parse_record(RecordKind.REPLY, document) == document


@pytest.mark.parametrize("nulled", list(NULL_COST))
def test_reply_cost_refuses_one_null_among_integers(nulled):
    document = changed(load_fixture(RecordKind.REPLY), ("cost", nulled), None)
    assert_refused(RecordKind.REPLY, document, "cost")


@pytest.mark.parametrize("filled", list(NULL_COST))
def test_reply_cost_refuses_one_integer_among_nulls(filled):
    cost = dict(NULL_COST, **{filled: 0})
    document = changed(load_fixture(RecordKind.REPLY), ("cost",), cost)
    assert_refused(RecordKind.REPLY, document, "cost")


@pytest.mark.parametrize("key", ["input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"])
def test_reply_spent_input_tokens_is_the_sum_of_the_three_input_fields(key):
    document = changed(load_fixture(RecordKind.REPLY), ("cost", key), 999)
    assert_refused(RecordKind.REPLY, document, "spent_input_tokens")


def test_turn_reply_carries_its_turn_number():
    document = changed(load_fixture(RecordKind.REPLY), ("turn",), 2)
    assert parse_record(RecordKind.REPLY, document) == document


@pytest.mark.parametrize("path,value", [
    (("condition",), "Bad Id"),
    (("split",), "hidden"),
    (("repeat",), 0),
    (("turn",), 0),
    (("reader_kind",), "human"),
    (("started",), "2026-10-14T10:00:00"),
    (("seconds",), "fast"),
    (("transcript",), "relative/path.jsonl"),
    (("transcript_hash",), "nope"),
    (("cost", "input_tokens"), -1),
    (("cost", "output_tokens"), 1.5),
    (("cost", "total_tokens"), 3),
    (("model",), ""),
    (("message",), 7),
    (("text",), None),
])
def test_reply_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.REPLY), path, value)
    assert_refused(RecordKind.REPLY, document, path[-1])


@pytest.mark.parametrize("variant,drop,add", [
    ("agent", "transcript", None),
    ("agent", "transcript_hash", None),
    ("agent", None, ("fingerprint_hash", "c" * 64)),
    ("command", "fingerprint_hash", None),
    ("command", None, ("transcript", "/tmp/t.jsonl")),
    ("command", None, ("transcript_hash", "d" * 64)),
])
def test_reply_refuses_fields_of_the_other_reader_kind(variant, drop, add):
    document = load_fixture(RecordKind.REPLY) if variant == "agent" else command_reply()
    if drop:
        del document[drop]
    if add:
        document[add[0]] = add[1]
    assert_refused(RecordKind.REPLY, document, (drop or add[0]))


def test_origins_record_parses_reply_and_anchor_entries():
    document = load_fixture(RecordKind.ORIGINS)
    assert parse_record(RecordKind.ORIGINS, document) == document


@pytest.mark.parametrize("path,value", [
    (("ids", "x7k", "packet"), "Bad Packet"),
    (("ids", "x7k", "split"), "hidden"),
    (("ids", "x7k", "repeat"), 0),
    (("ids", "x7k", "borrowed_from"), "parent"),
    (("ids", "m2q", "turn"), 0),
    (("ids", "a9z", "anchor"), "Bad Anchor"),
    (("ids", "Bad Blind"), {"packet": "p1", "anchor": "anchor-1"}),
    (("packets", "p1"), "nothash"),
    (("packets",), []),
])
def test_origins_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.ORIGINS), path, value)
    assert_refused(RecordKind.ORIGINS, document, path[-1])


@pytest.mark.parametrize("path", [
    ("ids", "x7k", "borrowed_from"),
    ("ids", "x7k", "task"),
    ("ids", "a9z", "packet"),
])
def test_origins_record_refuses_missing_entry_key(path):
    assert_refused(RecordKind.ORIGINS, without(load_fixture(RecordKind.ORIGINS), path), path[-1])


def test_origins_anchor_entry_refuses_reply_keys():
    document = changed(load_fixture(RecordKind.ORIGINS), ("ids", "a9z", "task"), "greet")
    assert_refused(RecordKind.ORIGINS, document, "task")


def test_verdict_record_parses_as_written():
    document = load_fixture(RecordKind.VERDICT)
    assert parse_record(RecordKind.VERDICT, document) == document


@pytest.mark.parametrize("done", [True, False, None])
def test_verdict_done_accepts_true_false_and_null(done):
    document = changed(load_fixture(RecordKind.VERDICT), ("verdicts", 0, "done"), done)
    assert parse_record(RecordKind.VERDICT, document) == document


@pytest.mark.parametrize("path,value", [
    (("verdicts",), []),
    (("verdicts", 0, "id"), "Bad Id"),
    (("verdicts", 1, "id"), "x7k"),
    (("verdicts", 0, "breaches", "brevity"), -1),
    (("verdicts", 0, "breaches", "brevity"), 1.5),
    (("verdicts", 0, "breaches", "brevity"), True),
    (("verdicts", 0, "done"), "yes"),
    (("verdicts", 0, "done"), 1),
    (("verdicts", 0, "kind"), "essay"),
    (("verdicts", 0, "notes"), None),
])
def test_verdict_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.VERDICT), path, value)
    assert_refused(RecordKind.VERDICT, document, path[-1])


def test_verdict_record_carries_no_inputs():
    document = changed(load_fixture(RecordKind.VERDICT), ("inputs",), {})
    assert_refused(RecordKind.VERDICT, document, "inputs")


@pytest.mark.parametrize("path", [("verdicts", 0, "breaches", "total"), ("verdicts", 0, "total")])
def test_verdict_record_refuses_a_total_key(path):
    document = changed(load_fixture(RecordKind.VERDICT), path, 3)
    assert_refused(RecordKind.VERDICT, document, "total")


def test_detectors_record_parses_as_written():
    document = load_fixture(RecordKind.DETECTORS)
    assert parse_record(RecordKind.DETECTORS, document) == document


@pytest.mark.parametrize("path,value", [
    (("verdicts", 0, "id"), "Bad Id"),
    (("verdicts", 1, "id"), "x7k"),
    (("verdicts", 0, "breaches", "hedging"), -2),
    (("verdicts", 0, "done_by_answer_key"), "yes"),
    (("verdicts", 0, "breaches", "total"), 3),
    (("verdicts", 0, "breaches_total"), 3),
    (("verdicts", 0, "done"), True),
])
def test_detectors_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.DETECTORS), path, value)
    assert_refused(RecordKind.DETECTORS, document, path[-1])


def test_detectors_record_refuses_missing_answer_key_field():
    document = without(load_fixture(RecordKind.DETECTORS), ("verdicts", 0, "done_by_answer_key"))
    assert_refused(RecordKind.DETECTORS, document, "done_by_answer_key")


def test_collected_record_parses_as_written():
    document = load_fixture(RecordKind.COLLECTED)
    assert parse_record(RecordKind.COLLECTED, document) == document


@pytest.mark.parametrize("path,value", [
    (("packets", "Bad Packet"), {}),
    (("packets", "p1", "accepted"), 0),
    (("packets", "p1", "judge_model"), "opus"),
    (("packets", "p1", "transcript"), "judge.jsonl"),
    (("packets", "p1", "transcript_hash"), "nope"),
    (("packets", "p1", "anchors", "breach_difference", "brevity"), "high"),
    (("packets", "p1", "anchors", "breach_difference", "total"), 1),
    (("packets", "p1", "anchors", "done_agreement"), None),
])
def test_collected_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.COLLECTED), path, value)
    assert_refused(RecordKind.COLLECTED, document, path[-1])


def test_scores_record_parses_as_written():
    document = load_fixture(RecordKind.SCORES)
    assert parse_record(RecordKind.SCORES, document) == document


@pytest.mark.parametrize("path", [
    ("by_condition", "instruction", "done_rate"),
    ("comparisons", "drift", "mean_difference"),
])
def test_scores_record_accepts_null_where_no_value_is_defined(path):
    document = changed(load_fixture(RecordKind.SCORES), path, None)
    assert parse_record(RecordKind.SCORES, document) == document


@pytest.mark.parametrize("path,value", [
    (("split",), "sealed"),
    (("rows", 0, "kind"), "essay"),
    (("rows", 0, "repeat"), 0),
    (("rows", 0, "turn"), 0),
    (("rows", 0, "borrowed_from"), "parent"),
    (("rows", 0, "breaches", "brevity"), -1),
    (("rows", 0, "breaches", "total"), 2),
    (("rows", 0, "breaches_total"), 2),
    (("rows", 0, "done"), "maybe"),
    (("rows", 0, "done_by_judge"), 1),
    (("by_condition", "instruction", "breaches_per_reply"), -1),
    (("by_condition", "instruction", "kinds", "essay"), 1),
    (("by_condition", "instruction", "kinds", "answer"), -1),
    (("by_condition", "instruction", "done_rate"), 1.5),
    (("by_condition", "instruction", "total"), 3),
    (("comparisons", "instruction-vs-nothing"), {"mean_difference": 0, "interval": None, "units": 1}),
    (("comparisons", "drift", "units"), 1.5),
    (("comparisons", "drift", "interval"), [1, 0]),
    (("comparisons", "drift", "interval"), [1]),
    (("drift", "instruction", "interval"), None),
    (("drift", "instruction", "slope"), "up"),
    (("disagreements",), ["Bad Id"]),
])
def test_scores_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.SCORES), path, value)
    assert_refused(RecordKind.SCORES, document, path[-1])


def test_scores_record_refuses_missing_row_key():
    document = without(load_fixture(RecordKind.SCORES), ("rows", 0, "done_by_judge"))
    assert_refused(RecordKind.SCORES, document, "done_by_judge")


def test_outcome_record_parses_as_written():
    document = load_fixture(RecordKind.OUTCOME)
    assert parse_record(RecordKind.OUTCOME, document) == document


def first_revision_outcome() -> dict:
    document = load_fixture(RecordKind.OUTCOME)
    del document["changed_from_parent"], document["parent_comparison"]
    return document


def test_first_revision_outcome_omits_parent_fields():
    document = first_revision_outcome()
    assert parse_record(RecordKind.OUTCOME, document) == document


@pytest.mark.parametrize("path,value", [
    (("outcome",), "draw"),
    (("checks", 0, "compares"), "instruction-vs-all"),
    (("checks", 0, "gap"), 0),
    (("checks", 0, "pass"), "yes"),
    (("checks", 0, "interval"), [1, 0]),
    (("changed_from_parent",), "improved"),
    (("parent_comparison", "target"), "Bad Target"),
    (("parent_comparison", "interval"), [1, 0]),
    (("instruction_breaches"), "none"),
    (("completion_passed",), None),
    (("words",), -1),
    (("cost", "replies"), 1.5),
    (("cost", "input_tokens"), -1),
    (("cost", "seconds"), "slow"),
    (("cost", "breaches_total"), 1),
])
def test_outcome_record_refuses_bad_value(path, value):
    path = (path,) if isinstance(path, str) else path
    document = changed(load_fixture(RecordKind.OUTCOME), path, value)
    assert_refused(RecordKind.OUTCOME, document, path[-1])


def test_outcome_target_accepts_completion():
    document = changed(load_fixture(RecordKind.OUTCOME), ("parent_comparison", "target"), "completion")
    assert parse_record(RecordKind.OUTCOME, document) == document


def test_outcome_without_paired_units_accepts_null_means_and_intervals():
    document = load_fixture(RecordKind.OUTCOME)
    for path in (("checks", 0, "mean_difference"), ("checks", 0, "interval"), ("parent_comparison", "mean_difference"), ("parent_comparison", "interval")):
        document = changed(document, path, None)
    assert parse_record(RecordKind.OUTCOME, document) == document


@pytest.mark.parametrize("dropped", ["changed_from_parent", "parent_comparison"])
def test_outcome_parent_fields_come_together(dropped):
    document = without(load_fixture(RecordKind.OUTCOME), (dropped,))
    assert_refused(RecordKind.OUTCOME, document, dropped)


def test_agreement_record_parses_as_written():
    document = load_fixture(RecordKind.AGREEMENT)
    assert parse_record(RecordKind.AGREEMENT, document) == document


def test_agreement_scale_accepts_a_number():
    document = changed(load_fixture(RecordKind.AGREEMENT), ("scale",), 1.5)
    assert parse_record(RecordKind.AGREEMENT, document) == document


@pytest.mark.parametrize("path,value", [
    (("demands", "Bad Id"), {"breach_difference": 0, "self_difference": 0}),
    (("demands", "brevity", "breach_difference"), "high"),
    (("demands", "brevity", "total"), 1),
    (("done_agreement"), None),
    (("scale",), "big"),
    (("ratings", "candidate-1.yaml", "model"), "opus"),
    (("ratings", "candidate-1.yaml", "transcript"), "relative.jsonl"),
    (("ratings", "candidate-1.yaml", "transcript_hash"), "nope"),
    (("accepted",), True),
])
def test_agreement_record_refuses_bad_value(path, value):
    path = (path,) if isinstance(path, str) else path
    document = changed(load_fixture(RecordKind.AGREEMENT), path, value)
    assert_refused(RecordKind.AGREEMENT, document, path[-1])


def test_calibration_record_parses_as_written():
    document = load_fixture(RecordKind.CALIBRATION)
    assert parse_record(RecordKind.CALIBRATION, document) == document


@pytest.mark.parametrize("raters", [["user"], ["agent", "agent"]])
def test_calibration_accepts_user_or_two_agent_raters(raters):
    document = changed(load_fixture(RecordKind.CALIBRATION), ("raters",), raters)
    assert parse_record(RecordKind.CALIBRATION, document) == document


@pytest.mark.parametrize("path,value", [
    (("raters",), ["agent"]),
    (("raters",), ["user", "user"]),
    (("raters",), ["agent", "user"]),
    (("attempt",), 0),
    (("judge_model",), "sonnet"),
    (("sample_size",), 0),
    (("anchors_per_packet",), 2),
    (("acceptance", "breach_difference"), -1),
    (("acceptance", "self_difference"), "tight"),
    (("acceptance", "done_agreement"), 1.5),
    (("brief_hash",), "nope"),
    (("agreement", "done_agreement"), None),
    (("accepted",), True),
    (("rater_model",), "claude-opus-4-1"),
])
def test_calibration_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.CALIBRATION), path, value)
    assert_refused(RecordKind.CALIBRATION, document, path[-1])


def test_anchors_record_parses_as_written():
    document = load_fixture(RecordKind.ANCHORS)
    assert parse_record(RecordKind.ANCHORS, document) == document


@pytest.mark.parametrize("path,value", [
    (("anchors",), []),
    (("anchors", 0, "id"), "Bad Id"),
    (("anchors", 1, "id"), "anchor-1"),
    (("anchors", 0, "task"), "Bad Task"),
    (("anchors", 0, "message"), 3),
    (("anchors", 0, "text"), None),
    (("anchors", 0, "breaches", "brevity"), -1),
    (("anchors", 0, "breaches", "total"), 1),
    (("anchors", 0, "done"), "yes"),
])
def test_anchors_record_refuses_bad_value(path, value):
    document = changed(load_fixture(RecordKind.ANCHORS), path, value)
    assert_refused(RecordKind.ANCHORS, document, path[-1])


JSON_SCALARS = (
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=True) | st.text(max_size=8)
)
JSON_VALUES = st.recursive(
    JSON_SCALARS,
    lambda children: st.lists(children, max_size=3)
    | st.dictionaries(st.text(max_size=8), children, max_size=3),
    max_leaves=12,
)
ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*")
BREACH_PATH = ("verdicts", 0, "breaches", "brevity")
INTERVAL_PATH = ("comparisons", "drift", "interval")


@given(document=JSON_VALUES, kind=st.sampled_from(list(RecordKind)))
def test_arbitrary_documents_are_refused_with_record_error_alone(document, kind):
    try:
        parse_record(kind, document)
    except Refusal:
        pass


@given(identifier=st.text().filter(lambda text: ID_PATTERN.fullmatch(text) is None))
def test_ids_outside_the_id_pattern_are_refused(identifier):
    document = changed(load_fixture(RecordKind.REPLY), ("task",), identifier)
    assert_refused(RecordKind.REPLY, document, "task")


@given(identifier=st.from_regex(ID_PATTERN, fullmatch=True))
def test_ids_inside_the_id_pattern_are_accepted(identifier):
    document = changed(load_fixture(RecordKind.REPLY), ("task",), identifier)
    assert parse_record(RecordKind.REPLY, document) == document


@given(count=st.integers(max_value=-1) | st.floats() | st.text() | st.booleans())
def test_breach_counts_other_than_non_negative_integers_are_refused(count):
    document = changed(load_fixture(RecordKind.VERDICT), BREACH_PATH, count)
    assert_refused(RecordKind.VERDICT, document, "brevity")


@given(count=st.integers(min_value=0))
def test_non_negative_integer_breach_counts_are_accepted(count):
    document = changed(load_fixture(RecordKind.VERDICT), BREACH_PATH, count)
    assert parse_record(RecordKind.VERDICT, document) == document


@given(moment=st.datetimes())
def test_timestamps_without_offset_are_refused(moment):
    document = changed(load_fixture(RecordKind.FROZEN), ("frozen_at",), moment.isoformat())
    assert_refused(RecordKind.FROZEN, document, "frozen_at")


@given(moment=st.datetimes(timezones=st.timezones()))
def test_timestamps_with_offset_are_accepted(moment):
    document = changed(load_fixture(RecordKind.FROZEN), ("frozen_at",), moment.isoformat())
    assert parse_record(RecordKind.FROZEN, document) == document


@given(low=st.integers(-1000, 1000), high=st.integers(-1000, 1000))
def test_intervals_are_accepted_exactly_when_low_does_not_exceed_high(low, high):
    document = changed(load_fixture(RecordKind.SCORES), INTERVAL_PATH, [low, high])
    if low <= high:
        assert parse_record(RecordKind.SCORES, document) == document
    else:
        assert_refused(RecordKind.SCORES, document, "interval")


@given(bounds=st.lists(st.integers(-1000, 1000), max_size=5).filter(lambda bounds: len(bounds) != 2))
def test_intervals_of_other_lengths_are_refused(bounds):
    document = changed(load_fixture(RecordKind.SCORES), INTERVAL_PATH, bounds)
    assert_refused(RecordKind.SCORES, document, "interval")


@given(ids=st.lists(st.from_regex(ID_PATTERN, fullmatch=True), min_size=1, max_size=4))
def test_repeated_blind_ids_in_a_verdict_are_refused(ids):
    entry = load_fixture(RecordKind.VERDICT)["verdicts"][0]
    verdicts = [dict(entry, id=identifier) for identifier in ids + ids[:1]]
    assert_refused(RecordKind.VERDICT, {"verdicts": verdicts}, "duplicate")
