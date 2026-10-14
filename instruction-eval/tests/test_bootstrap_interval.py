import math
from statistics import NormalDist

import numpy
import pytest

from instruction_eval.scores import BOOTSTRAP_RESAMPLES, BOOTSTRAP_SEED, PairedUnit, compare_paired, z_for_level

LEVEL = 0.9
PROPERTY_SEED = 7
PROPERTY_CASES = 200
MAX_PROPERTY_UNITS = 12
CONVENTIONAL_Z_AT_95 = 1.96
CONVENTIONAL_Z_TOLERANCE = 1e-3
FLOAT_TOLERANCE = 1e-12
UNITS = [
    PairedUnit(instruction=0.0, other=1.0),
    PairedUnit(instruction=0.5, other=0.5),
    PairedUnit(instruction=0.25, other=1.0),
    PairedUnit(instruction=1.0, other=0.0),
]


def property_rng() -> numpy.random.Generator:
    return numpy.random.default_rng(PROPERTY_SEED)


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
    assert math.isclose(comparison.interval[0], expected_low, abs_tol=FLOAT_TOLERANCE)
    assert math.isclose(comparison.interval[1], expected_high, abs_tol=FLOAT_TOLERANCE)


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


def test_z_at_level_095_is_the_conventional_two_sided_critical_value():
    assert math.isclose(z_for_level(0.95), CONVENTIONAL_Z_AT_95, abs_tol=CONVENTIONAL_Z_TOLERANCE)


def test_z_rises_with_level_and_mirrors_the_lower_tail_quantile():
    ascending_levels = sorted(property_rng().uniform(0, 1, PROPERTY_CASES))
    z_values = [z_for_level(level) for level in ascending_levels]

    assert all(lower < higher for lower, higher in zip(z_values, z_values[1:]))
    for level, z in zip(ascending_levels, z_values):
        assert math.isclose(z, -NormalDist().inv_cdf((1 - level) / 2), rel_tol=FLOAT_TOLERANCE)


def test_interval_lies_ordered_within_the_unit_differences_for_any_units():
    rng = property_rng()
    for _ in range(PROPERTY_CASES):
        unit_count = int(rng.integers(1, MAX_PROPERTY_UNITS + 1))
        units = [PairedUnit(instruction=float(a), other=float(b)) for a, b in rng.normal(size=(unit_count, 2))]
        differences = [unit.instruction - unit.other for unit in units]

        comparison = compare_paired(units, float(rng.uniform(0, 1)), numpy.random.default_rng(BOOTSTRAP_SEED))

        assert comparison.units == unit_count
        assert comparison.interval is not None
        low, high = comparison.interval
        assert min(differences) - FLOAT_TOLERANCE <= low <= high <= max(differences) + FLOAT_TOLERANCE
        assert math.isclose(comparison.mean_difference, sum(differences) / unit_count, abs_tol=FLOAT_TOLERANCE)


@pytest.mark.parametrize("level", [0.0, 1.0, -0.5, 1.5])
def test_comparison_refuses_level_outside_open_unit_interval(level):
    with pytest.raises(ValueError, match=f"level must lie strictly between 0 and 1, got {level}"):
        compare_paired(UNITS, level, numpy.random.default_rng(BOOTSTRAP_SEED))


@pytest.mark.parametrize("level", [0.0, 1.0, -0.5, 1.5])
def test_z_refuses_level_outside_open_unit_interval(level):
    with pytest.raises(ValueError, match=f"level must lie strictly between 0 and 1, got {level}"):
        z_for_level(level)
