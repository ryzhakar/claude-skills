from dataclasses import dataclass
from typing import NamedTuple, Sequence

import numpy

BOOTSTRAP_SEED = 20261012
BOOTSTRAP_RESAMPLES = 2000


class PairedUnit(NamedTuple):
    """One resampled unit's value under the instruction and under the condition it is compared with."""

    instruction: float
    other: float


@dataclass(frozen=True)
class Comparison:
    """Mean instruction-minus-other difference over units, its percentile bootstrap interval, and the unit count."""

    mean_difference: float | None
    interval: tuple[float, float] | None
    units: int


def compare_paired(units: Sequence[PairedUnit], level: float, rng: numpy.random.Generator) -> Comparison:
    """Average instruction minus other per unit and bound it by a percentile bootstrap interval at `level`, null without units."""
    if not units:
        return Comparison(mean_difference=None, interval=None, units=0)
    differences = unit_differences(units)
    resample_means = bootstrap_resample_means(differences, rng)
    return Comparison(
        mean_difference=float(differences.mean()),
        interval=percentile_interval(resample_means, level),
        units=len(differences),
    )


def unit_differences(units: Sequence[PairedUnit]) -> numpy.ndarray:
    """Return each unit's instruction value minus its other value."""
    return numpy.array([unit.instruction - unit.other for unit in units], dtype=float)


def bootstrap_resample_means(differences: numpy.ndarray, rng: numpy.random.Generator) -> numpy.ndarray:
    """Return the mean difference of each of the resamples drawn from units with replacement."""
    return differences[rng.integers(0, len(differences), size=(BOOTSTRAP_RESAMPLES, len(differences)))].mean(axis=1)


def percentile_interval(resample_means: numpy.ndarray, level: float) -> tuple[float, float]:
    """Return the central `level` interval of the resample means by numpy's linear quantile."""
    low, high = numpy.quantile(resample_means, [(1 - level) / 2, (1 + level) / 2], method="linear")
    return float(low), float(high)
