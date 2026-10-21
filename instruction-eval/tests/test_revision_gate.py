import gate_fixtures
import pytest
from gate_fixtures import (
    CONDITIONS,
    CONTROLS,
    GATE,
    HYPOTHESIS,
    HYPOTHESIS_KEYS,
    REPLY_COST,
    assert_gate_refused_writing_nothing,
    first_replies,
    frozen_series,
    gate_reads,
    measured_reads,
    omission_replies,
    sealed_replies,
    write_measured_revision,
    write_revision_instruction,
)
from series_fixtures import Reply, bootstrap_rng, write_yaml

from instruction_eval.gate import revision_gate
from instruction_eval.records import Refusal, SeriesRecords


def test_a_first_revision_beating_every_control_passes_storing_sealed_aggregates_its_keep_ranks_its_cost_and_a_passed_stop(tmp_path):
    replies = first_replies(instruction_judged=0, aim_judged=3)
    files = frozen_series(tmp_path, replies)

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    assert outcome["outcome"] == "pass"
    assert outcome["checks"] == [
        {"compares": "instruction-vs-empty", "gap": 1.0, "mean_difference": -3.0, "interval": [-3.0, -3.0], "pass": True},
        {"compares": "instruction-vs-aim", "gap": 1.0, "mean_difference": -3.0, "interval": [-3.0, -3.0], "pass": True},
        {"compares": "instruction-vs-placebo", "gap": 1.0, "mean_difference": -3.0, "interval": [-3.0, -3.0], "pass": True},
        {"compares": "completion", "gap": 1.0, "mean_difference": 0.0, "interval": [0.0, 0.0], "pass": True},
    ]
    assert (outcome["instruction_breaches"], outcome["completion_passed"], outcome["words"]) == (0.0, True, 4)
    assert outcome["cost"] == {"replies": 17, "input_tokens": 170, "output_tokens": 85, "seconds": 25.5}
    assert "changed_from_parent" not in outcome
    assert set(outcome["inputs"]) == gate_reads("r1", replies)
    stop = SeriesRecords(files).stop()
    assert (stop["stop"], stop["kept"]) == ("passed", "r1")
    outcome_text = files.read_bytes("r1/9-outcome.yaml").decode()
    assert not [reply.id for reply in replies if reply.split == "sealed" and reply.id in outcome_text]


def test_a_first_revision_missing_one_check_fails_without_a_stop(tmp_path):
    files = frozen_series(tmp_path, first_replies(instruction_judged=0, aim_judged=0))

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    assert outcome["outcome"] == "fail"
    assert [check["pass"] for check in outcome["checks"]] == [True, False, True, True]
    assert not files.holds("9-stop.yaml")


def test_omission_replies_move_no_check_and_the_outcome_names_no_omission(tmp_path, monkeypatch):
    without = frozen_series(tmp_path / "without", first_replies(instruction_judged=0, aim_judged=3))
    revision_gate(without, "r1", bootstrap_rng)
    monkeypatch.setattr(gate_fixtures, "CONDITIONS", {**CONDITIONS, "omissions": "every-sentence"})
    files = frozen_series(tmp_path / "with", [*first_replies(instruction_judged=0, aim_judged=3), *omission_replies(0x50)])

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    assert outcome["checks"] == SeriesRecords(without).outcome("r1")["checks"]
    assert "omit-" not in repr({key: value for key, value in outcome.items() if key != "inputs"})


def test_a_later_revision_compares_its_instruction_with_the_parent_on_the_hypothesis_target_beside_borrowed_controls(tmp_path):
    first = first_replies(instruction_judged=3, aim_judged=3)
    files = frozen_series(tmp_path, first)
    revision_gate(files, "r1", bootstrap_rng)
    write_revision_instruction(files, "r2", 2, b"Be brief. Avoid hedges.\n")
    write_yaml(files, "r2/1-hypothesis.yaml", HYPOTHESIS)
    later = [
        Reply("b00000101", "instruction", "t1"),
        *sealed_replies("instruction", 0, 0x110),
        *(reply for start, control in enumerate(CONTROLS) for reply in sealed_replies(control, 3, 0x120 + 0x10 * start, borrowed_from="r1")),
    ]
    write_measured_revision(files, "r2", later)

    revision_gate(files, "r2", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r2")
    assert outcome["changed_from_parent"] == "changed"
    assert outcome["parent_comparison"] == {"target": "d-judge", "mean_difference": -3.0, "interval": [-3.0, -3.0]}
    assert outcome["outcome"] == "pass"
    assert outcome["cost"]["replies"] == 5
    hypothesis_reads = {f"r2/1-hypothesis.yaml#{key}" for key in HYPOTHESIS_KEYS}
    assert set(outcome["inputs"]) == gate_reads("r2", later, ["r1"]) | hypothesis_reads | measured_reads("r1", first)
    assert (SeriesRecords(files).stop()["stop"], SeriesRecords(files).stop()["kept"]) == ("passed", "r2")


def test_a_failing_revision_whose_asks_reach_the_budget_ceiling_stops_capped_for_budget(tmp_path):
    files = frozen_series(tmp_path, first_replies(instruction_judged=0, aim_judged=0), {**GATE, "budget": {"unit": "seconds", "ceiling": 10}})

    revision_gate(files, "r1", bootstrap_rng)

    stop = SeriesRecords(files).stop()
    assert {key: value for key, value in stop.items() if key != "inputs"} == {"stop": "capped", "reason": "budget", "kept": "r1"}
    assert set(stop["inputs"]) == {"7-gate.yaml#keep_rule", "7-gate.yaml#budget", "8-frozen.yaml", "r1/9-outcome.yaml"}


def test_a_completion_check_without_a_unit_holding_done_on_both_sides_stores_no_mean_no_interval_and_fails(tmp_path):
    replies = [reply if reply.condition != "instruction" else Reply(reply.id, reply.condition, reply.task, repeat=reply.repeat, split=reply.split, done=None) for reply in first_replies(0, 3)]
    files = frozen_series(tmp_path, replies)

    revision_gate(files, "r1", bootstrap_rng)

    outcome = SeriesRecords(files).outcome("r1")
    completion = next(check for check in outcome["checks"] if check["compares"] == "completion")
    assert (completion["mean_difference"], completion["interval"], completion["pass"]) == (None, None, False)
    assert (outcome["outcome"], outcome["completion_passed"]) == ("fail", False)


def test_a_revision_whose_replies_lack_token_counts_stores_null_token_sums_beside_its_replies_and_seconds(tmp_path, monkeypatch):
    monkeypatch.setattr(gate_fixtures, "REPLY_COST", dict.fromkeys(REPLY_COST))
    files = frozen_series(tmp_path, first_replies(0, 0))

    revision_gate(files, "r1", bootstrap_rng)

    assert SeriesRecords(files).outcome("r1")["cost"] == {"replies": 17, "input_tokens": None, "output_tokens": None, "seconds": 25.5}


def test_a_tokens_budget_over_asks_without_token_counts_is_refused_writing_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(gate_fixtures, "REPLY_COST", dict.fromkeys(REPLY_COST))
    files = frozen_series(tmp_path, first_replies(0, 0), {**GATE, "budget": {"unit": "tokens", "ceiling": 1000}})

    assert_gate_refused_writing_nothing(files, r"^tokens budget refused: r1 asked replies without token counts$")
    assert not files.holds("9-stop.yaml")


def test_a_revision_without_its_collection_is_refused(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 3))
    (files.root / "r1/7-collected.yaml").unlink()

    assert_gate_refused_writing_nothing(files, r"^missing record: r1/7-collected\.yaml$")


def test_a_reply_origin_without_its_reply_file_is_refused(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 3))
    (files.root / "r1/5-replies/aim/t3/repeat-2.yaml").unlink()

    assert_gate_refused_writing_nothing(files, r"^unresolved reply: r1/5-replies/aim/t3/repeat-2\.yaml \(r1/6-origins\.yaml\)$")


def test_an_unfrozen_series_is_refused(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 3))
    (files.root / "8-frozen.yaml").unlink()

    assert_gate_refused_writing_nothing(files, r"^missing record: 8-frozen\.yaml$")


def test_a_gated_revision_refuses_a_second_gate(tmp_path):
    files = frozen_series(tmp_path, first_replies(0, 0))
    revision_gate(files, "r1", bootstrap_rng)

    with pytest.raises(Refusal, match=r"^already written: r1/9-outcome\.yaml$"):
        revision_gate(files, "r1", bootstrap_rng)
