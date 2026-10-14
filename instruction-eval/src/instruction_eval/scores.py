from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from math import sqrt
from statistics import NormalDist, linear_regression, mean, variance
from typing import NamedTuple, TypedDict

import numpy

_INSTRUCTION = "instruction"
_SOURCE = "source"
_EMPTY = "empty"
_VS_CONTROLS = (_EMPTY, "aim", "placebo")
_VS_PREFIX = "instruction-vs-"
_NEAR_SOURCE = "instruction-near-source"
_COMPLETION = "completion"
_DRIFT = "drift"
_TWO_SIDED_TAILS = 2
_LEAST_VALUES_FOR_VARIANCE = 2
_LEAST_TURNS_FOR_SLOPE = 2


class ScoredReply(TypedDict):
    """One sealed r1 reply scored: its condition, task or conversation, repeat, turn or null, breaches, and done."""

    condition: str
    task: str
    repeat: int
    turn: int | None
    breaches: Mapping[str, int]
    done: bool | None


class NoiseSigma(TypedDict):
    """Each condition's mean repeat variance per metric, null where no unit holds two non-null values."""

    breaches: dict[str, float | None]
    done: dict[str, float | None]
    drift: dict[str, float | None]
    demands: dict[str, dict[str, float | None]]


class Noise(TypedDict):
    """The `8-frozen.yaml` `noise` value: variances and half-widths only."""

    repeats: int
    level: float
    z: float
    sigma: NoiseSigma
    checks: dict[str, float | None]
    demands: dict[str, float | None]
    done_change: float | None


def measure_noise(
    sealed_rows: Sequence[ScoredReply],
    gate_demands: Sequence[str],
    controls: Sequence[str],
    repeats: int,
    level: float,
) -> Noise:
    """Return r1's noise: each condition's repeat variances and the half-width each check and change can resolve."""
    z = NormalDist().inv_cdf((1 + level) / _TWO_SIDED_TAILS)
    conditions = [_INSTRUCTION, *controls]
    task_replies = [row for row in sealed_rows if row["turn"] is None]
    turn_replies = [row for row in sealed_rows if row["turn"] is not None]
    task_repeat_units = repeats * _unit_count(task_replies)
    sigma: NoiseSigma = {
        "breaches": _repeat_variances(task_replies, conditions, partial(_breach_total, demands=gate_demands)),
        "done": _repeat_variances(task_replies, conditions, _done_value),
        "drift": {
            condition: _mean_repeat_variance(_drift_slopes_by_unit(turn_replies, condition, gate_demands))
            for condition in conditions
        },
        "demands": {
            demand: _repeat_variances(task_replies, conditions, partial(_breach_total, demands=[demand]))
            for demand in gate_demands
        },
    }
    return {
        "repeats": repeats,
        "level": level,
        "z": z,
        "sigma": sigma,
        "checks": _check_half_widths(
            z,
            sigma,
            controls,
            _best_done_control(task_replies, controls),
            task_repeat_units,
            repeats * _unit_count(turn_replies),
        ),
        "demands": {
            demand: _change_half_width(z, by_condition[_INSTRUCTION], task_repeat_units)
            for demand, by_condition in sigma["demands"].items()
        },
        "done_change": _change_half_width(z, sigma["done"][_INSTRUCTION], task_repeat_units),
    }


def _check_half_widths(
    z: float,
    sigma: NoiseSigma,
    controls: Sequence[str],
    completion_control: str | None,
    task_repeat_units: int,
    conversation_repeat_units: int,
) -> dict[str, float | None]:
    """Map each defined compares to the half-width of instruction minus its control, drift only with conversations."""
    breaches = sigma["breaches"]
    done_of_completion_control = sigma["done"][completion_control] if completion_control else None
    checks = {
        _VS_PREFIX + control: _half_width(z, [breaches[_INSTRUCTION], breaches[control]], task_repeat_units)
        for control in _VS_CONTROLS
    }
    checks[_COMPLETION] = _half_width(z, [sigma["done"][_INSTRUCTION], done_of_completion_control], task_repeat_units)
    if _SOURCE in controls:
        checks[_NEAR_SOURCE] = _half_width(z, [breaches[_INSTRUCTION], breaches[_SOURCE]], task_repeat_units)
    if conversation_repeat_units:
        drift = sigma["drift"]
        drift_control = _SOURCE if _SOURCE in controls else _EMPTY
        checks[_DRIFT] = _half_width(z, [drift[_INSTRUCTION], drift[drift_control]], conversation_repeat_units)
    return checks


def _unit_count(replies: Sequence[ScoredReply]) -> int:
    """Return how many distinct tasks or conversations the replies span."""
    return len({reply["task"] for reply in replies})


def _repeat_variances(
    replies: Sequence[ScoredReply], conditions: Sequence[str], metric: Callable[[ScoredReply], float | None]
) -> dict[str, float | None]:
    """Map each condition to the mean repeat variance of the per-reply metric over its units."""
    return {
        condition: _mean_repeat_variance(_metric_values_by_unit(replies, condition, metric)) for condition in conditions
    }


def _metric_values_by_unit(
    replies: Sequence[ScoredReply], condition: str, metric: Callable[[ScoredReply], float | None]
) -> dict[str, list[float | None]]:
    """Map each unit to its condition's metric values, one per repeat."""
    values: dict[str, list[float | None]] = {}
    for reply in replies:
        if reply["condition"] == condition:
            values.setdefault(reply["task"], []).append(metric(reply))
    return values


def _drift_slopes_by_unit(
    replies: Sequence[ScoredReply], condition: str, demands: Sequence[str]
) -> dict[str, list[float | None]]:
    """Map each conversation to its condition's least-squares slopes of breach totals over turns, one per repeat."""
    turn_totals: dict[tuple[str, int], tuple[list[int], list[int]]] = {}
    for reply in replies:
        if reply["condition"] == condition and (turn := reply["turn"]) is not None:
            turns, totals = turn_totals.setdefault((reply["task"], reply["repeat"]), ([], []))
            turns.append(turn)
            totals.append(_breach_total(reply, demands))
    slopes: dict[str, list[float | None]] = {}
    for (conversation, _), (turns, totals) in turn_totals.items():
        slopes.setdefault(conversation, []).append(_least_squares_slope(turns, totals))
    return slopes


def _least_squares_slope(turns: Sequence[int], totals: Sequence[int]) -> float | None:
    """Return the least-squares slope of totals over turns, or null when fewer than two distinct turns exist."""
    if len(set(turns)) < _LEAST_TURNS_FOR_SLOPE:
        return None
    return linear_regression(turns, totals).slope


def _breach_total(reply: ScoredReply, demands: Sequence[str]) -> int:
    """Return the reply's breaches summed over the demands."""
    return sum(reply["breaches"][demand] for demand in demands)


def _done_value(reply: ScoredReply) -> float | None:
    """Return the reply's done as 1 or 0, or null when done is null."""
    return None if reply["done"] is None else float(reply["done"])


def _best_done_control(replies: Sequence[ScoredReply], controls: Sequence[str]) -> str | None:
    """Return the control with the highest done rate over non-null done values, or null when no control has one."""
    done_rates = {
        control: mean(present)
        for control in controls
        if (present := [reply["done"] for reply in replies if reply["condition"] == control and reply["done"] is not None])
    }
    return max(done_rates, key=done_rates.__getitem__, default=None)


def _mean_repeat_variance(values_by_unit: Mapping[str, Sequence[float | None]]) -> float | None:
    """Return the mean sample variance over units holding at least two non-null values, or null when none does."""
    present_by_unit = [[value for value in values if value is not None] for values in values_by_unit.values()]
    variances = [variance(present) for present in present_by_unit if len(present) >= _LEAST_VALUES_FOR_VARIANCE]
    return mean(variances) if variances else None


def _change_half_width(z: float, instruction_variance: float | None, repeat_units: int) -> float | None:
    """Return the half-width of one instruction run minus another, each carrying the instruction variance."""
    return _half_width(z, [instruction_variance, instruction_variance], repeat_units)


def _half_width(z: float, variances: Sequence[float | None], repeat_units: int) -> float | None:
    """Return z times the root of the summed variances over the repeat-unit count, or null when any variance is null."""
    if None in variances:
        return None
    return z * sqrt(sum(variances) / repeat_units)


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
    require_valid_level(level)
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
    resampled_indices = rng.integers(0, len(differences), size=(BOOTSTRAP_RESAMPLES, len(differences)))
    return differences[resampled_indices].mean(axis=1)


def percentile_interval(resample_means: numpy.ndarray, level: float) -> tuple[float, float]:
    """Return the central `level` interval of the resample means by numpy's linear quantile."""
    upper_probability = upper_tail_probability(level)
    low, high = numpy.quantile(resample_means, [1 - upper_probability, upper_probability], method="linear")
    return float(low), float(high)


def z_for_level(level: float) -> float:
    """Return the standard normal quantile at (1 + `level`) / 2."""
    require_valid_level(level)
    return NormalDist().inv_cdf(upper_tail_probability(level))


def upper_tail_probability(level: float) -> float:
    """Return the probability (1 + `level`) / 2 bounding a central `level` interval from above."""
    return (1 + level) / 2


def require_valid_level(level: float) -> None:
    """Raise ValueError naming `level` unless it lies strictly between 0 and 1."""
    if not 0 < level < 1:
        raise ValueError(f"level must lie strictly between 0 and 1, got {level}")
