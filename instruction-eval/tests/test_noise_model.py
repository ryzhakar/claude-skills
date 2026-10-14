from math import sqrt
from statistics import NormalDist

import pytest

from instruction_eval.scores import measure_noise

LEVEL = 0.95
Z = NormalDist().inv_cdf((1 + LEVEL) / 2)
CONTROLS = ["empty", "aim", "placebo"]


def reply(condition, task, repeat, breaches, done=None, turn=None):
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
        reply("instruction", "t1", 1, {"d1": 1}),
        reply("instruction", "t1", 2, {"d1": 3}),
        reply("instruction", "t2", 1, {"d1": 0}),
        reply("instruction", "t2", 2, {"d1": 0}),
        reply("empty", "t1", 1, {"d1": 2}),
        reply("empty", "t1", 2, {"d1": 6}),
        reply("empty", "t2", 1, {"d1": 4}),
        reply("empty", "t2", 2, {"d1": 4}),
    ]

    noise = measure_noise(rows, ["d1"], CONTROLS, repeats=2, level=LEVEL)

    assert noise["sigma"]["breaches"]["instruction"] == pytest.approx(1.0)
    assert noise["sigma"]["breaches"]["empty"] == pytest.approx(4.0)
    assert noise["checks"]["instruction-vs-empty"] == pytest.approx(Z * sqrt(5 / (2 * 2)))


def done_replies(condition, done_by_task):
    return [
        reply(condition, task, repeat, {"d1": 0}, done=done)
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
