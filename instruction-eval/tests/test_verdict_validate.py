import copy

import pytest

from instruction_eval.judge import parse_verdict
from instruction_eval.records import RecordError

BLIND_IDS = frozenset({"b0000000a", "b0000000b"})
JUDGE_DEMAND_IDS = frozenset({"d-terse", "d-plain"})


def entry(blind_id: str) -> dict:
    return {"id": blind_id, "breaches": {"d-terse": 0, "d-plain": 2}, "done": True, "kind": "answer", "notes": "fine"}


VALID = {"verdicts": [entry("b0000000a"), entry("b0000000b")]}


def broken(edit) -> dict:
    document = copy.deepcopy(VALID)
    edit(document["verdicts"])
    return document


def test_a_verdict_holding_each_packet_id_once_with_every_judge_demand_counted_in_range_is_valid():
    assert parse_verdict(VALID, BLIND_IDS, JUDGE_DEMAND_IDS) == VALID


@pytest.mark.parametrize(
    ("edit", "fault"),
    [
        (lambda verdicts: verdicts.pop(), r"missing blind id b0000000b"),
        (lambda verdicts: verdicts.append(entry("b0000000c")), r"blind id b0000000c is not in the packet"),
        (lambda verdicts: verdicts.append(entry("b0000000a")), r"duplicate id"),
        (lambda verdicts: verdicts[0]["breaches"].pop("d-plain"), r"verdicts\[0\]\.breaches: missing judge demand d-plain"),
        (lambda verdicts: verdicts[1]["breaches"].update({"d-emoji": 0}), r"verdicts\[1\]\.breaches: d-emoji is not a judge demand"),
        (lambda verdicts: verdicts[0]["breaches"].update({"d-terse": -1}), r"d-terse"),
        (lambda verdicts: verdicts[0]["breaches"].update({"d-terse": 1.5}), r"d-terse"),
        (lambda verdicts: verdicts[0].update({"done": "yes"}), r"done"),
        (lambda verdicts: verdicts[0].update({"kind": "essay"}), r"kind"),
        (lambda verdicts: verdicts[0].pop("notes"), r"notes"),
        (lambda verdicts: verdicts.clear(), r"verdicts"),
    ],
    ids=["missing-id", "foreign-id", "repeated-id", "uncounted-demand", "non-judge-demand", "negative-count", "fractional-count", "done-out-of-range", "kind-out-of-range", "no-notes", "no-entries"],
)
def test_an_invalid_verdict_is_refused_naming_its_fault(edit, fault):
    with pytest.raises(RecordError, match=fault):
        parse_verdict(broken(edit), BLIND_IDS, JUDGE_DEMAND_IDS)
