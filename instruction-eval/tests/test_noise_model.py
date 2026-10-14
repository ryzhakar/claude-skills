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
