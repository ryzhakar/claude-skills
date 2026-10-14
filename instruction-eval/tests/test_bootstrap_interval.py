import math

import numpy
import pytest

from instruction_eval.scores import BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED, PairedUnit, compare_paired, z_for_level

LEVEL = 0.9
UNITS = [
    PairedUnit(instruction=0.0, other=1.0),
    PairedUnit(instruction=0.5, other=0.5),
    PairedUnit(instruction=0.25, other=1.0),
    PairedUnit(instruction=1.0, other=0.0),
]


def linear_quantile_by_hand(ascending: list[float], probability: float) -> float:
    position = (len(ascending) - 1) * probability
    below = math.floor(position)
    above = min(below + 1, len(ascending) - 1)
    return ascending[below] + (position - below) * (ascending[above] - ascending[below])


def test_interval_matches_hand_computed_percentile_bootstrap():
    differences = [unit.instruction - unit.other for unit in UNITS]
    draws = numpy.random.default_rng(BOOTSTRAP_SEED).integers(0, len(UNITS), size=(BOOTSTRAP_RESAMPLES, len(UNITS)))
    resample_means = sorted(sum(differences[index] for index in row) / len(UNITS) for row in draws.tolist())
    expected_low = linear_quantile_by_hand(resample_means, (1 - LEVEL) / 2)
    expected_high = linear_quantile_by_hand(resample_means, (1 + LEVEL) / 2)

    comparison = compare_paired(UNITS, LEVEL, numpy.random.default_rng(BOOTSTRAP_SEED))

    assert comparison.mean_difference == -0.1875
    assert comparison.units == 4
    assert comparison.interval is not None
    assert math.isclose(comparison.interval[0], expected_low, abs_tol=1e-12)
    assert math.isclose(comparison.interval[1], expected_high, abs_tol=1e-12)


def test_instruction_below_other_on_every_unit_gives_interval_wholly_below_zero():
    units = [PairedUnit(instruction=0.0, other=value) for value in (1.0, 2.0, 1.5)]

    comparison = compare_paired(units, LEVEL, numpy.random.default_rng(BOOTSTRAP_SEED))

    assert comparison.mean_difference == -1.5
    assert comparison.interval is not None
    assert comparison.interval[1] < 0


def test_instruction_above_other_on_every_unit_gives_interval_wholly_above_zero():
    units = [PairedUnit(instruction=value, other=0.0) for value in (1.0, 2.0, 1.5)]

    comparison = compare_paired(units, LEVEL, numpy.random.default_rng(BOOTSTRAP_SEED))

    assert comparison.mean_difference == 1.5
    assert comparison.interval is not None
    assert comparison.interval[0] > 0


def test_no_units_gives_null_interval():
    comparison = compare_paired([], LEVEL, numpy.random.default_rng(BOOTSTRAP_SEED))

    assert comparison.mean_difference is None
    assert comparison.interval is None
    assert comparison.units == 0


def test_z_at_level_095_is_the_two_sided_normal_critical_value():
    assert math.isclose(z_for_level(0.95), 1.959963984540054, rel_tol=1e-12)


def test_z_at_level_090_is_the_normal_quantile_at_095():
    assert math.isclose(z_for_level(0.9), 1.6448536269514722, rel_tol=1e-12)


@pytest.mark.parametrize("level", [0.0, 1.0, -0.5, 1.5])
def test_comparison_refuses_level_outside_open_unit_interval(level):
    with pytest.raises(ValueError, match=f"level must lie strictly between 0 and 1, got {level}"):
        compare_paired(UNITS, level, numpy.random.default_rng(BOOTSTRAP_SEED))


@pytest.mark.parametrize("level", [0.0, 1.0, -0.5, 1.5])
def test_z_refuses_level_outside_open_unit_interval(level):
    with pytest.raises(ValueError, match=f"level must lie strictly between 0 and 1, got {level}"):
        z_for_level(level)
