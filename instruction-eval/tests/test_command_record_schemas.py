import copy
import re
from pathlib import Path

import pytest
import yaml

from instruction_eval.records import RecordError, RecordKind, parse_record

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
    with pytest.raises(RecordError, match=re.escape(fragment)):
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
