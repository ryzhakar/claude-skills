from math import sqrt
from statistics import NormalDist

import pytest

from instruction_eval.scores import ScoredReply, measure_noise

LEVEL = 0.95
Z = NormalDist().inv_cdf((1 + LEVEL) / 2)
CONTROLS = ["empty", "aim", "placebo"]


def noise_reply(
    condition: str,
    task: str,
    repeat: int,
    breaches: dict[str, int],
    done: bool | None = None,
    turn: int | None = None,
) -> ScoredReply:
    """Build one sealed scored reply, a single-task reply when turn is null."""
    return {
        "condition": condition,
        "task": task,
        "repeat": repeat,
        "turn": turn,
        "breaches": breaches,
        "done": done,
    }


def test_vs_check_noise_at_two_repeats_pools_instruction_and_control_variances():
    rows = [
        noise_reply("instruction", "t1", 1, {"d1": 1}),
        noise_reply("instruction", "t1", 2, {"d1": 3}),
        noise_reply("instruction", "t2", 1, {"d1": 0}),
        noise_reply("instruction", "t2", 2, {"d1": 0}),
        noise_reply("empty", "t1", 1, {"d1": 2}),
        noise_reply("empty", "t1", 2, {"d1": 6}),
        noise_reply("empty", "t2", 1, {"d1": 4}),
        noise_reply("empty", "t2", 2, {"d1": 4}),
    ]

    noise = measure_noise(rows, ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["sigma"]["breaches"]["instruction"] == pytest.approx(1.0)
    assert noise["sigma"]["breaches"]["empty"] == pytest.approx(4.0)
    assert noise["checks"]["instruction-vs-empty"] == pytest.approx(Z * sqrt(5 / (2 * 2)))


def test_near_source_noise_compares_instruction_with_source():
    rows = [
        noise_reply("instruction", "t1", 1, {"d1": 1}),
        noise_reply("instruction", "t1", 2, {"d1": 3}),
        noise_reply("instruction", "t2", 1, {"d1": 0}),
        noise_reply("instruction", "t2", 2, {"d1": 0}),
        noise_reply("source", "t1", 1, {"d1": 0}),
        noise_reply("source", "t1", 2, {"d1": 2}),
        noise_reply("source", "t2", 1, {"d1": 1}),
        noise_reply("source", "t2", 2, {"d1": 1}),
    ]

    noise = measure_noise(rows, ["d1"], [*CONTROLS, "source"], repeats=2, level=LEVEL)

    assert noise["checks"]["instruction-near-source"] == pytest.approx(Z * sqrt(2 / (2 * 2)))


def test_near_source_noise_is_absent_without_a_source():
    noise = measure_noise(THREE_REPEAT_DONE_ROWS, ["d1"], CONTROLS, repeats=3, level=LEVEL)

    assert "instruction-near-source" not in noise["checks"]


def turn_replies(condition: str, totals_by_conversation: dict[str, list[list[int]]]) -> list[ScoredReply]:
    """Build turn replies from d1 breach totals nested by conversation, then repeat, then turn."""
    return [
        noise_reply(condition, conversation, repeat, {"d1": total}, turn=turn)
        for conversation, repeats in totals_by_conversation.items()
        for repeat, totals in enumerate(repeats, start=1)
        for turn, total in enumerate(totals, start=1)
    ]


def test_drift_noise_pools_slope_variances_over_conversations_against_empty():
    rows = [
        *turn_replies("instruction", {"c1": [[0, 1, 2], [0, 0, 0]], "c2": [[1, 1, 1], [1, 1, 1]]}),
        *turn_replies("empty", {"c1": [[0, 2, 4], [0, 0, 0]], "c2": [[3, 2, 1], [1, 2, 3]]}),
    ]

    noise = measure_noise(rows, ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["sigma"]["drift"]["instruction"] == pytest.approx(0.25)
    assert noise["sigma"]["drift"]["empty"] == pytest.approx(2.0)
    assert noise["checks"]["drift"] == pytest.approx(Z * sqrt(2.25 / (2 * 2)))


def test_drift_noise_compares_instruction_with_source_when_a_source_exists():
    rows = [
        *turn_replies("instruction", {"c1": [[0, 1, 2], [0, 0, 0]], "c2": [[1, 1, 1], [1, 1, 1]]}),
        *turn_replies("empty", {"c1": [[0, 2, 4], [0, 0, 0]], "c2": [[3, 2, 1], [1, 2, 3]]}),
        *turn_replies("source", {"c1": [[0, 1, 2], [0, 0, 0]], "c2": [[0, 0, 0], [0, 0, 0]]}),
    ]

    noise = measure_noise(rows, ["d1"], [*CONTROLS, "source"], repeats=2, level=LEVEL)

    assert noise["checks"]["drift"] == pytest.approx(Z * sqrt(0.5 / (2 * 2)))


def test_drift_noise_leaves_out_a_conversation_repeat_with_one_sealed_turn():
    rows = [
        *turn_replies("instruction", {"c1": [[0, 1, 2], [5]], "c2": [[0, 2], [0, 0]]}),
        *turn_replies("empty", {"c1": [[0, 0, 0], [0, 0, 0]], "c2": [[0, 0], [0, 0]]}),
    ]

    noise = measure_noise(rows, ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["sigma"]["drift"]["instruction"] == pytest.approx(2.0)
    assert noise["checks"]["drift"] == pytest.approx(Z * sqrt(2 / (2 * 2)))


def test_conversation_turns_leave_task_noise_unchanged():
    task_rows = [
        noise_reply("instruction", "t1", 1, {"d1": 1}),
        noise_reply("instruction", "t1", 2, {"d1": 3}),
        noise_reply("empty", "t1", 1, {"d1": 2}),
        noise_reply("empty", "t1", 2, {"d1": 6}),
    ]
    conversation_rows = [
        *turn_replies("instruction", {"c1": [[0, 9], [5, 0]]}),
        *turn_replies("empty", {"c1": [[7, 0], [0, 3]]}),
    ]

    noise = measure_noise([*task_rows, *conversation_rows], ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["checks"]["instruction-vs-empty"] == pytest.approx(Z * sqrt((2 + 8) / (2 * 1)))


def test_drift_noise_is_absent_without_conversations():
    noise = measure_noise(THREE_REPEAT_DONE_ROWS, ["d1"], CONTROLS, repeats=3, level=LEVEL)

    assert "drift" not in noise["checks"]


def done_replies(condition: str, done_by_task: dict[str, list[bool | None]]) -> list[ScoredReply]:
    """Build breach-free task replies from done values nested by task, then repeat."""
    return [
        noise_reply(condition, task, repeat, {"d1": 0}, done=done)
        for task, dones in done_by_task.items()
        for repeat, done in enumerate(dones, start=1)
    ]


THREE_REPEAT_DONE_ROWS = [
    *done_replies("instruction", {"t1": [True, False, None], "t2": [True, True, True]}),
    *done_replies("empty", {"t1": [False, False, False], "t2": [False, False, True]}),
    *done_replies("aim", {"t1": [True, False, None], "t2": [True, True, True]}),
    *done_replies("placebo", {"t1": [True, True, True], "t2": [True, False, True]}),
]


def test_completion_noise_at_three_repeats_compares_instruction_with_the_best_done_control():
    noise = measure_noise(THREE_REPEAT_DONE_ROWS, ["d1"], CONTROLS, repeats=3, level=LEVEL)

    assert noise["sigma"]["done"]["instruction"] == pytest.approx(0.25)
    assert noise["sigma"]["done"]["placebo"] == pytest.approx(1 / 6)
    assert noise["checks"]["completion"] == pytest.approx(Z * sqrt((0.25 + 1 / 6) / (3 * 2)))


def test_done_change_noise_at_three_repeats_doubles_the_instruction_done_variance():
    noise = measure_noise(THREE_REPEAT_DONE_ROWS, ["d1"], CONTROLS, repeats=3, level=LEVEL)

    assert noise["done_change"] == pytest.approx(Z * sqrt(2 * 0.25 / (3 * 2)))


def test_noise_is_null_where_no_unit_holds_two_non_null_values():
    rows = [
        *done_replies("instruction", {"t1": [True, None], "t2": [None, None]}),
        *done_replies("empty", {"t1": [True, False], "t2": [False, False]}),
    ]

    noise = measure_noise(rows, ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["sigma"]["done"]["instruction"] is None
    assert noise["checks"]["completion"] is None
    assert noise["done_change"] is None


def test_completion_noise_is_null_when_no_control_has_a_done_value():
    rows = [
        *done_replies("instruction", {"t1": [True, False], "t2": [True, True]}),
        *done_replies("empty", {"t1": [None, None], "t2": [None, None]}),
    ]

    noise = measure_noise(rows, ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["checks"]["completion"] is None


def test_noise_holds_variances_and_half_widths_only():
    noise = measure_noise(THREE_REPEAT_DONE_ROWS, ["d1"], CONTROLS, repeats=3, level=LEVEL)

    assert set(noise) == {"repeats", "level", "z", "sigma", "checks", "demands", "done_change"}
    assert set(noise["sigma"]) == {"breaches", "done", "drift", "demands"}
    assert (noise["repeats"], noise["level"], noise["z"]) == (3, LEVEL, pytest.approx(Z))


def test_demand_change_noise_doubles_the_instruction_variance_of_each_gate_demand():
    rows = [
        noise_reply("instruction", "t1", 1, {"d1": 1, "d2": 0, "dropped": 9}),
        noise_reply("instruction", "t1", 2, {"d1": 3, "d2": 2, "dropped": 0}),
        noise_reply("instruction", "t2", 1, {"d1": 0, "d2": 5, "dropped": 4}),
        noise_reply("instruction", "t2", 2, {"d1": 0, "d2": 8, "dropped": 1}),
    ]

    noise = measure_noise(rows, ["d1", "d2"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["sigma"]["demands"]["d2"]["instruction"] == pytest.approx(3.25)
    assert noise["demands"] == {
        "d1": pytest.approx(Z * sqrt(2 * 1.0 / (2 * 2))),
        "d2": pytest.approx(Z * sqrt(2 * 3.25 / (2 * 2))),
    }
