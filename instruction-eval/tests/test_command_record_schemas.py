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
