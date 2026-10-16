import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field

import pytest
import yaml

from instruction_eval.records import (
    AgentReader,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    write_file,
    write_record,
)
from series_fixtures import write_yaml

CHECKS = [
    {"compares": "instruction-vs-empty", "gap": 0.5},
    {"compares": "instruction-vs-aim", "gap": 0.5},
    {"compares": "instruction-vs-placebo", "gap": 0.5},
    {"compares": "completion", "gap": 0.1},
]
GATE = {
    "repeats": 2,
    "level": 0.95,
    "done_by": "judge",
    "checks": CHECKS,
    "keep_rule": "best-estimate-shortest",
    "budget": "none",
}
HASH = "a" * 64
REPLY_PATH = "r1/5-replies/instruction/t-open/repeat-1.yaml"
REPLY_READS = ["series.yaml", "3-tasks.yaml", "7-gate.yaml#repeats", "r1/4-conditions/instruction.md"]
AGENT_COST = {
    "input_tokens": 10,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 5,
    "spent_input_tokens": 10,
}
REPLY = {
    "condition": "instruction",
    "task": "t-open",
    "split": "open",
    "repeat": 1,
    "message": "Explain tides.",
    "text": "The moon pulls.",
    "model": "claude-sonnet-4-5",
    "reader_kind": "agent",
    "started": "2026-10-14T10:00:00+00:00",
    "seconds": 1.5,
    "transcript": "/tmp/transcripts/t-open.jsonl",
    "transcript_hash": HASH,
    "cost": AGENT_COST,
}
REPLY_ORIGIN = {
    "packet": "t-open",
    "condition": "instruction",
    "task": "t-open",
    "split": "open",
    "repeat": 1,
    "borrowed_from": None,
}
ANCHOR_ORIGIN = {"packet": "t-open", "anchor": "a-one"}
ORIGINS = {"ids": {"b00000001": REPLY_ORIGIN, "b00000002": ANCHOR_ORIGIN}, "packets": {"t-open": HASH}}
ATTEMPT = "6-judge/calibration/attempt-1"
ATTEMPT_ORIGINS = {"ids": {"b0000000a": {**REPLY_ORIGIN, "packet": "sample"}}, "packets": {"sample": HASH}}
VERDICT_ENTRY = {"breaches": {"d-judge": 0}, "done": True, "kind": "answer", "notes": ""}
VERDICT = {"verdicts": [{"id": "b00000001", **VERDICT_ENTRY}, {"id": "b00000002", **VERDICT_ENTRY}]}
RATING = {"verdicts": [{"id": "b0000000a", **VERDICT_ENTRY}]}
AGREEMENT = {
    "demands": {"d-judge": {"breach_difference": 0.1, "self_difference": 0.1}},
    "done_agreement": 0.9,
    "scale": None,
    "ratings": {
        "candidate-1.yaml": {
            "model": "claude-opus-4-1",
            "transcript": "/tmp/transcripts/candidate-1.jsonl",
            "transcript_hash": HASH,
        }
    },
}
ACCEPTANCE = {"breach_difference": 0.5, "self_difference": 0.5, "done_agreement": 0.8}
CALIBRATION = {
    "attempt": 1,
    "judge_model": "claude-opus-4-1",
    "raters": ["user"],
    "sample_size": 1,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
    "brief_hash": HASH,
    "agreement": {"inputs": {}, **AGREEMENT},
}
ANCHORS = {
    "anchors": [
        {
            "id": "a-one",
            "task": "t-open",
            "message": "Explain tides.",
            "text": "The moon pulls.",
            "breaches": {"d-judge": 0},
            "done": True,
        }
    ]
}
COLLECTED = {
    "packets": {
        "t-open": {
            "accepted": 1,
            "judge_model": "claude-opus-4-1",
            "transcript": "/tmp/transcripts/judge.jsonl",
            "transcript_hash": HASH,
            "anchors": {"breach_difference": {"d-judge": 0.0}, "done_agreement": 1.0},
        }
    }
}
DETECTORS = {"verdicts": [{"id": "b00000001", "breaches": {"d-pattern": 0}, "done_by_answer_key": None}]}
SCORES = {
    "split": "open",
    "rows": [
        {
            "id": "b00000001",
            "condition": "instruction",
            "task": "t-open",
            "repeat": 1,
            "turn": None,
            "borrowed_from": None,
            "breaches": {"d-judge": 0, "d-pattern": 0},
            "kind": "answer",
            "done_by_answer_key": None,
            "done_by_judge": True,
            "done": True,
        }
    ],
    "by_condition": {
        "instruction": {"breaches_per_reply": 0.0, "demands": {"d-judge": 0.0}, "done_rate": 1.0, "kinds": {"answer": 1}}
    },
    "comparisons": {},
    "drift": {},
    "disagreements": ["b00000001"],
}
OUTCOME_COST = {"replies": 1, "input_tokens": 10, "output_tokens": 5, "seconds": 1.5}
OUTCOME = {
    "outcome": "fail",
    "checks": [],
    "instruction_breaches": 0.0,
    "completion_passed": True,
    "words": 2,
    "cost": OUTCOME_COST,
}
R2_OUTCOME = {
    **OUTCOME,
    "changed_from_parent": "unchanged",
    "parent_comparison": {"target": "d-judge", "mean_difference": 0.0, "interval": [-0.1, 0.1]},
}
SIGMA = {"breaches": {"instruction": 0.1}, "done": {"instruction": 0.1}, "drift": {}, "demands": {"d-judge": {"instruction": 0.1}}}
FROZEN = {
    "hashes": {},
    "noise": {
        "repeats": 2,
        "level": 0.95,
        "z": 1.96,
        "sigma": SIGMA,
        "checks": {"instruction-vs-empty": 0.1},
        "demands": {"d-judge": 0.1},
        "done_change": 0.1,
    },
    "tool_version": "0.1.0",
    "frozen_at": "2026-10-14T10:00:00+00:00",
}
HYPOTHESIS = {
    "failing_demand": "d-judge",
    "replies_read": ["b00000001"],
    "change": {"action": "rewrite", "sentence": 1},
    "predicted_movement": {"direction": "down", "size": 0.5},
}
TASKS = {
    "tasks": [
        {"id": "t-open", "tempts": "d-judge", "split": "open", "message": "Explain tides.", "answer_key": None},
        {"id": "t-sealed", "tempts": "d-pattern", "split": "sealed", "message": "Explain rain.", "answer_key": None},
        {"id": "t-over", "tempts": "overreach", "split": "open", "message": "Add two and two.", "answer_key": "4"},
    ],
    "conversations": [{"id": "c-open", "split": "open", "turns": ["Plan a trip.", "Which week?"]}],
}
COVERAGE = {"demands": {"d-judge": [1], "d-pattern": {"dropped": "Unmeasured here."}}, "sentences": {1: ["d-judge"]}}


def sha256(files: SeriesFolder, path: str) -> str:
    return hashlib.sha256((files.root / path).read_bytes()).hexdigest()


def rewrite_record(files: SeriesFolder, path: str, record: dict, reads: list[str]) -> None:
    (files.root / path).unlink()
    write_record(files, path, record, reads)


@pytest.fixture
def files(tmp_path):
    files = SeriesFolder(tmp_path)
    series = {
        "instruction": "/home/writer/terse.md",
        "sources": [],
        "reader_kind": "agent",
        "created": "2026-10-14T10:00:00+00:00",
    }
    write_record(files, "series.yaml", series, [])
    write_yaml(files, "2-demands.yaml", {
        "demands": [
            {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
            {"id": "d-pattern", "text": "No hedges.", "boundary": "None.", "counted_by": "pattern", "pattern": "maybe"},
        ]
    })
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "4-conditions.yaml", {
        "controls": ["empty", "aim", "placebo"],
        "aim": "Make replies short.",
        "placebo_source": "/home/writer/placebo.md",
        "omissions": "none",
    })
    write_yaml(files, "5-reader.yaml", {"kind": "agent", "model": "claude-sonnet-4-5"})
    write_yaml(files, "7-gate.yaml", GATE)
    write_file(files, "r1/2-instruction.md", b"Be terse.\n")
    write_record(files, "r1/2-revision.yaml", {
        "number": 1, "parent": None, "hash": sha256(files, "r1/2-instruction.md"), "parent_record": None, "change": None,
    }, [])
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    for condition in ("instruction", "empty", "aim", "placebo"):
        write_file(files, f"r1/4-conditions/{condition}.md", condition.encode())
    write_record(files, REPLY_PATH, REPLY, REPLY_READS)
    write_yaml(files, f"{ATTEMPT}/plan.yaml", {
        "judge_model": "claude-opus-4-1",
        "raters": ["user"],
        "sample_size": 1,
        "anchors_per_packet": 3,
        "acceptance": ACCEPTANCE,
    })
    write_record(files, f"{ATTEMPT}/origins.yaml", ATTEMPT_ORIGINS, [f"{ATTEMPT}/plan.yaml", REPLY_PATH])
    write_yaml(files, f"{ATTEMPT}/candidate-1.yaml", RATING)
    write_record(files, f"{ATTEMPT}/agreement.yaml", AGREEMENT, [f"{ATTEMPT}/plan.yaml", f"{ATTEMPT}/candidate-1.yaml"])
    write_record(files, "6-judge/calibration.yaml", CALIBRATION, [f"{ATTEMPT}/plan.yaml"])
    write_record(files, "6-judge/anchors.yaml", ANCHORS, [f"{ATTEMPT}/plan.yaml"])
    write_record(files, "r1/6-origins.yaml", ORIGINS, ["3-tasks.yaml", "7-gate.yaml#repeats", REPLY_PATH])
    write_yaml(files, "r1/7-verdicts/t-open/k1.yaml", VERDICT)
    write_record(files, "r1/7-collected.yaml", COLLECTED, ["r1/6-origins.yaml", "r1/7-verdicts/t-open/k1.yaml"])
    write_record(files, "r1/7-detectors.yaml", DETECTORS, ["2-demands.yaml", "r1/6-origins.yaml"])
    write_record(files, "r1/8-scores.yaml", SCORES, ["7-gate.yaml#level", "r1/7-collected.yaml"])
    write_record(files, "r1/9-outcome.yaml", OUTCOME, ["7-gate.yaml", "r1/8-scores.yaml"])
    write_record(files, "8-frozen.yaml", FROZEN, ["7-gate.yaml"])
    write_yaml(files, "r2/1-hypothesis.yaml", HYPOTHESIS)
    write_file(files, "r2/2-instruction.md", b"Be brief.\n")
    write_record(files, "r2/2-revision.yaml", {
        "number": 2,
        "parent": "r1",
        "hash": sha256(files, "r2/2-instruction.md"),
        "parent_record": sha256(files, "r1/2-revision.yaml"),
        "change": {"action": "rewrite", "sentence": 1, "old": "Be terse.", "new": "Be brief."},
    }, ["r1/2-revision.yaml", "r2/1-hypothesis.yaml"])
    write_yaml(files, "r2/3-coverage.yaml", COVERAGE)
    write_record(files, "r2/9-outcome.yaml", R2_OUTCOME, ["7-gate.yaml"])
    write_record(files, "9-stop.yaml", {"stop": "capped", "kept": "r1"}, ["7-gate.yaml#keep_rule"])
    return files


def test_every_record_of_a_consistent_series_loads_typed(files):
    records = SeriesRecords(files)
    assert records.series().reader_kind == "agent"
    assert [demand.id for demand in records.demands().demands] == ["d-judge", "d-pattern"]
    assert [task.id for task in records.tasks().tasks] == ["t-open", "t-sealed", "t-over"]
    assert records.conditions().controls == ("empty", "aim", "placebo")
    assert records.reader() == AgentReader(model="claude-sonnet-4-5")
    assert records.gate().keep_rule == GATE["keep_rule"]
    assert records.complete_gate().repeats == GATE["repeats"]
    assert records.plan(1).sample_size == 1
    assert records.hypothesis("r2").replies_read == ("b00000001",)
    assert records.coverage("r1").sentences == {1: ("d-judge",)}
    assert records.revision("r2")["parent"] == "r1"
    assert records.reply(REPLY_PATH)["text"] == REPLY["text"]
    assert records.origins("r1")["ids"] == ORIGINS["ids"]
    assert records.attempt_origins(1)["packets"] == ATTEMPT_ORIGINS["packets"]
    assert records.verdict("r1", "t-open", 1) == VERDICT
    assert records.rating(1, "candidate-1") == RATING
    assert records.agreement(1)["done_agreement"] == AGREEMENT["done_agreement"]
    assert records.calibration()["attempt"] == 1
    assert records.anchors()["anchors"] == ANCHORS["anchors"]
    assert records.collected("r1")["packets"] == COLLECTED["packets"]
    assert records.detectors("r1")["verdicts"] == DETECTORS["verdicts"]
    assert records.scores("r1")["rows"] == SCORES["rows"]
    assert records.outcome("r2")["parent_comparison"] == R2_OUTCOME["parent_comparison"]
    assert records.frozen()["noise"] == FROZEN["noise"]
    assert records.stop()["kept"] == "r1"


@dataclass(frozen=True)
class ReadCountingFolder(SeriesFolder):
    reads: Counter = field(default_factory=Counter)

    def read_bytes(self, path):
        self.reads[path] += 1
        return super().read_bytes(path)


@pytest.mark.parametrize(
    "load",
    [lambda records: records.scores("r1"), lambda records: records.hypothesis("r2"), lambda records: records.reply(REPLY_PATH)],
)
def test_one_loader_reads_each_shared_record_once_however_many_records_reference_it(files, load):
    counting = ReadCountingFolder(files.root)
    load(SeriesRecords(counting))
    shared = {path: counting.reads[path] for path in ("2-demands.yaml", "r1/3-coverage.yaml") if counting.reads[path]}
    assert shared == dict.fromkeys(shared, 1)


def at(*keys: object, value: object):
    def change(document: dict) -> None:
        container = document
        for key in keys[:-1]:
            container = container[key]
        container[keys[-1]] = value

    return change


def edit(files: SeriesFolder, path: str, change) -> None:
    document = yaml.safe_load((files.root / path).read_text())
    reads = document.pop("inputs", None)
    change(document)
    if reads is None:
        write_yaml(files, path, document)
    else:
        rewrite_record(files, path, document, list(reads))


def refusal(path: str, kind: str, name: str) -> str:
    return rf"^unresolved {kind}: {re.escape(str(name))} \({re.escape(path)}\)$"


@pytest.mark.parametrize(
    ("path", "change", "load", "kind", "name"),
    [
        ("3-tasks.yaml", at("tasks", 0, "tempts", value="d-gone"), lambda records: records.tasks(), "demand", "d-gone"),
        ("r1/3-coverage.yaml", at("demands", "d-gone", value=[1]), lambda records: records.coverage("r1"), "demand", "d-gone"),
        ("r1/3-coverage.yaml", at("sentences", 1, value=["d-gone"]), lambda records: records.coverage("r1"), "demand", "d-gone"),
        ("r2/1-hypothesis.yaml", at("failing_demand", value="d-pattern"), lambda records: records.hypothesis("r2"), "gate demand", "d-pattern"),
        ("r2/9-outcome.yaml", at("parent_comparison", "target", value="d-pattern"), lambda records: records.outcome("r2"), "gate demand", "d-pattern"),
        ("8-frozen.yaml", at("noise", "demands", value={"d-pattern": 0.1}), lambda records: records.frozen(), "gate demand", "d-pattern"),
        ("8-frozen.yaml", at("noise", "sigma", "demands", value={"d-pattern": {}}), lambda records: records.frozen(), "gate demand", "d-pattern"),
        ("r1/7-verdicts/t-open/k1.yaml", at("verdicts", 0, "breaches", value={"d-pattern": 0}), lambda records: records.verdict("r1", "t-open", 1), "judge demand", "d-pattern"),
        (f"{ATTEMPT}/candidate-1.yaml", at("verdicts", 0, "breaches", value={"d-pattern": 0}), lambda records: records.rating(1, "candidate-1"), "judge demand", "d-pattern"),
        ("6-judge/anchors.yaml", at("anchors", 0, "breaches", value={"d-pattern": 0}), lambda records: records.anchors(), "judge demand", "d-pattern"),
        (f"{ATTEMPT}/agreement.yaml", at("demands", value={"d-pattern": {"breach_difference": 0, "self_difference": 0}}), lambda records: records.agreement(1), "judge demand", "d-pattern"),
        ("6-judge/calibration.yaml", at("agreement", "demands", value={"d-pattern": {"breach_difference": 0, "self_difference": 0}}), lambda records: records.calibration(), "judge demand", "d-pattern"),
        ("r1/7-collected.yaml", at("packets", "t-open", "anchors", "breach_difference", value={"d-pattern": 0}), lambda records: records.collected("r1"), "judge demand", "d-pattern"),
        ("r1/7-detectors.yaml", at("verdicts", 0, "breaches", value={"d-judge": 0}), lambda records: records.detectors("r1"), "detector demand", "d-judge"),
        ("r1/8-scores.yaml", at("rows", 0, "breaches", value={"d-gone": 0}), lambda records: records.scores("r1"), "demand", "d-gone"),
        ("r1/8-scores.yaml", at("by_condition", "instruction", "demands", value={"d-gone": 0}), lambda records: records.scores("r1"), "demand", "d-gone"),
    ],
)
def test_a_record_naming_a_demand_the_series_lacks_refuses_naming_it(files, path, change, load, kind, name):
    edit(files, path, change)
    with pytest.raises(Refusal, match=refusal(path, kind, name)):
        load(SeriesRecords(files))


@pytest.mark.parametrize(
    ("path", "change", "load", "kind", "name"),
    [
        (REPLY_PATH, at("task", value="t-gone"), lambda records: records.reply(REPLY_PATH), "task", "t-gone"),
        ("6-judge/anchors.yaml", at("anchors", 0, "task", value="t-gone"), lambda records: records.anchors(), "task", "t-gone"),
        (REPLY_PATH, at("condition", value="omit-9"), lambda records: records.reply(REPLY_PATH), "condition", "omit-9"),
        ("r2/2-revision.yaml", at("parent", value="r7"), lambda records: records.revision("r2"), "revision", "r7"),
        ("9-stop.yaml", at("kept", value="r7"), lambda records: records.stop(), "revision", "r7"),
        ("r1/6-origins.yaml", at("ids", "b00000002", "anchor", value="a-gone"), lambda records: records.origins("r1"), "anchor", "a-gone"),
        ("r1/6-origins.yaml", at("ids", "b00000001", "packet", value="p-gone"), lambda records: records.origins("r1"), "packet", "p-gone"),
        ("r1/7-collected.yaml", at("packets", value={"p-gone": COLLECTED["packets"]["t-open"]}), lambda records: records.collected("r1"), "packet", "p-gone"),
        ("r1/6-origins.yaml", at("ids", "b00000001", "repeat", value=2), lambda records: records.origins("r1"), "reply", "r1/5-replies/instruction/t-open/repeat-2.yaml"),
        ("r1/6-origins.yaml", at("ids", "b00000001", "borrowed_from", value="r2"), lambda records: records.origins("r1"), "reply", "r2/5-replies/instruction/t-open/repeat-1.yaml"),
        ("r1/6-origins.yaml", at("ids", "b00000001", "turn", value=1), lambda records: records.origins("r1"), "reply", "r1/5-replies/instruction/t-open/repeat-1/turn-1.yaml"),
        (f"{ATTEMPT}/origins.yaml", at("ids", "b0000000a", "repeat", value=2), lambda records: records.attempt_origins(1), "reply", "r1/5-replies/instruction/t-open/repeat-2.yaml"),
        ("r1/7-verdicts/t-open/k1.yaml", at("verdicts", 0, "id", value="b00000009"), lambda records: records.verdict("r1", "t-open", 1), "blind id", "b00000009"),
        (f"{ATTEMPT}/candidate-1.yaml", at("verdicts", 0, "id", value="b00000001"), lambda records: records.rating(1, "candidate-1"), "blind id", "b00000001"),
        ("r1/7-detectors.yaml", at("verdicts", 0, "id", value="b00000009"), lambda records: records.detectors("r1"), "blind id", "b00000009"),
        ("r1/8-scores.yaml", at("rows", 0, "id", value="b00000009"), lambda records: records.scores("r1"), "blind id", "b00000009"),
        ("r1/8-scores.yaml", at("disagreements", value=["b00000009"]), lambda records: records.scores("r1"), "blind id", "b00000009"),
        ("r2/1-hypothesis.yaml", at("replies_read", value=["b00000009"]), lambda records: records.hypothesis("r2"), "blind id", "b00000009"),
        ("6-judge/calibration.yaml", at("attempt", value=2), lambda records: records.calibration(), "attempt", "2"),
        (f"{ATTEMPT}/agreement.yaml", at("ratings", value={"candidate-2.yaml": AGREEMENT["ratings"]["candidate-1.yaml"]}), lambda records: records.agreement(1), "rating", "candidate-2.yaml"),
        ("8-frozen.yaml", at("hashes", value={"r1/gone.md": HASH}), lambda records: records.frozen(), "frozen part", "r1/gone.md"),
        (REPLY_PATH, at("turn", value=1), lambda records: records.reply(REPLY_PATH), "turn", "1"),
        (REPLY_PATH, at("split", value="sealed"), lambda records: records.reply(REPLY_PATH), "split", "sealed"),
        ("r1/8-scores.yaml", at("rows", 0, "condition", value="omit-9"), lambda records: records.scores("r1"), "condition", "omit-9"),
        ("r1/8-scores.yaml", at("rows", 0, "task", value="t-gone"), lambda records: records.scores("r1"), "task", "t-gone"),
        ("r1/8-scores.yaml", at("by_condition", value={"omit-9": SCORES["by_condition"]["instruction"]}), lambda records: records.scores("r1"), "condition", "omit-9"),
    ],
)
def test_a_record_naming_an_entry_the_series_lacks_refuses_naming_it(files, path, change, load, kind, name):
    edit(files, path, change)
    with pytest.raises(Refusal, match=refusal(path, kind, name)):
        load(SeriesRecords(files))


def test_a_verdict_naming_a_blind_id_of_another_packet_refuses_naming_it(files):
    edit(files, "r1/6-origins.yaml", at("ids", "b00000002", "packet", value="t-other"))
    edit(files, "r1/6-origins.yaml", at("packets", "t-other", value=HASH))
    path = "r1/7-verdicts/t-open/k1.yaml"
    with pytest.raises(Refusal, match=refusal(path, "blind id", "b00000002")):
        SeriesRecords(files).verdict("r1", "t-open", 1)


TURN_PATH = "r1/5-replies/instruction/c-open/repeat-1/turn-2.yaml"
TURN_REPLY = {**REPLY, "task": "c-open", "turn": 2}


def test_a_conversation_turn_reply_within_its_turns_loads(files):
    write_record(files, TURN_PATH, TURN_REPLY, REPLY_READS)
    assert SeriesRecords(files).reply(TURN_PATH)["turn"] == 2


@pytest.mark.parametrize(("reply", "name"), [({**TURN_REPLY, "turn": 3}, "3"), ({k: v for k, v in TURN_REPLY.items() if k != "turn"}, "absent")])
def test_a_conversation_reply_naming_no_turn_or_a_turn_past_its_last_refuses_naming_it(files, reply, name):
    write_record(files, TURN_PATH, reply, REPLY_READS)
    with pytest.raises(Refusal, match=refusal(TURN_PATH, "turn", name)):
        SeriesRecords(files).reply(TURN_PATH)


def test_scores_holding_a_control_row_borrowed_from_r1_load(files):
    write_file(files, "r2/4-conditions/instruction.md", b"instruction")
    borrowed_row = {**SCORES["rows"][0], "condition": "empty", "borrowed_from": "r1"}
    write_record(files, "r2/6-origins.yaml", {"ids": {"b00000001": {**REPLY_ORIGIN, "borrowed_from": "r1"}}, "packets": {"t-open": HASH}}, [])
    by_condition = {"instruction": SCORES["by_condition"]["instruction"], "empty": SCORES["by_condition"]["instruction"]}
    write_record(files, "r2/8-scores.yaml", {**SCORES, "rows": [borrowed_row], "by_condition": by_condition}, [])
    assert SeriesRecords(files).scores("r2")["rows"] == [borrowed_row]


COMMAND_READER = {
    "kind": "command",
    "model": "gpt-5-mini",
    "command": ["reply", "{condition}"],
    "fingerprint": ["reply", "--version"],
    "sampling": {"temperature": 0.7},
}
NULL_COST = dict.fromkeys(AGENT_COST)


def test_a_reader_of_another_kind_than_the_series_refuses_naming_both(files):
    write_yaml(files, "5-reader.yaml", COMMAND_READER)
    with pytest.raises(Refusal, match=r"^reader kind mismatch: 5-reader\.yaml \(command, series\.yaml agent\)$"):
        SeriesRecords(files).reader()


def test_a_reply_of_another_reader_kind_than_the_series_refuses_naming_both(files):
    command_reply = {key: value for key, value in REPLY.items() if key not in ("transcript", "transcript_hash")}
    rewrite_record(files, REPLY_PATH, {**command_reply, "reader_kind": "command", "fingerprint_hash": HASH, "cost": NULL_COST}, REPLY_READS)
    with pytest.raises(Refusal, match=rf"^reader kind mismatch: {re.escape(REPLY_PATH)} \(command, series\.yaml agent\)$"):
        SeriesRecords(files).reply(REPLY_PATH)


def test_a_reply_whose_consumed_gate_key_changed_refuses_as_stale(files):
    write_yaml(files, "7-gate.yaml", {**GATE, "repeats": 3})
    with pytest.raises(Refusal, match=rf"^stale: {re.escape(REPLY_PATH)} \(input 7-gate\.yaml#repeats changed\)$"):
        SeriesRecords(files).reply(REPLY_PATH)


def test_a_reply_loads_after_the_user_edits_gate_checks_it_never_read(files):
    write_yaml(files, "7-gate.yaml", {**GATE, "checks": [*CHECKS, {"compares": "drift", "gap": 1}]})
    assert SeriesRecords(files).reply(REPLY_PATH)["text"] == REPLY["text"]


def test_a_reply_whose_input_was_deleted_refuses_naming_the_input(files):
    (files.root / "r1/4-conditions/instruction.md").unlink()
    with pytest.raises(Refusal, match=r"^missing input: r1/4-conditions/instruction\.md$"):
        SeriesRecords(files).reply(REPLY_PATH)


def test_a_complete_gate_refuses_an_unwritten_key_naming_it(files):
    write_yaml(files, "7-gate.yaml", {key: value for key, value in GATE.items() if key != "keep_rule"})
    with pytest.raises(Refusal, match=r"^missing key: 7-gate\.yaml#keep_rule$"):
        SeriesRecords(files).complete_gate()


def test_a_frozen_series_refuses_a_gate_with_an_unwritten_key(files):
    write_yaml(files, "7-gate.yaml", {key: value for key, value in GATE.items() if key != "budget"})
    with pytest.raises(Refusal, match=r"^missing key: 7-gate\.yaml#budget$"):
        SeriesRecords(files).gate()


def test_an_unfrozen_series_loads_a_gate_holding_only_the_step_four_keys(files):
    (files.root / "8-frozen.yaml").unlink()
    write_yaml(files, "7-gate.yaml", {"repeats": 2, "level": 0.9, "done_by": "judge"})
    gate = SeriesRecords(files).gate()
    assert (gate.repeats, gate.checks, gate.keep_rule, gate.budget) == (2, None, None, None)


def test_a_record_breaking_its_schema_refuses_as_malformed_naming_the_file(files):
    edit(files, "2-demands.yaml", at("demands", 0, "counted_by", value="eyeball"))
    with pytest.raises(Refusal, match=r"^malformed record: 2-demands\.yaml \(demands\[0\]\.counted_by: 'eyeball' is not one of"):
        SeriesRecords(files).demands()


def test_an_absent_user_record_refuses_naming_it(files):
    (files.root / "3-tasks.yaml").unlink()
    with pytest.raises(Refusal, match=r"^missing record: 3-tasks\.yaml$"):
        SeriesRecords(files).tasks()
