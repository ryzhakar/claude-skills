from collections.abc import Mapping, Sequence
from math import sqrt
from statistics import NormalDist, linear_regression, mean, variance
from typing import TypedDict

INSTRUCTION = "instruction"
SOURCE = "source"
EMPTY = "empty"
VS_CONTROLS = (EMPTY, "aim", "placebo")


class ScoredReply(TypedDict):
    """One sealed r1 reply scored: its condition, task or conversation, repeat, turn or null, gate breaches, and done."""

    condition: str
    task: str
    repeat: int
    turn: int | None
    breaches: Mapping[str, int]
    done: bool | None


def measure_noise(
    sealed_rows: Sequence[ScoredReply],
    gate_demands: Sequence[str],
    controls: Sequence[str],
    repeats: int,
    level: float,
) -> dict:
    """Return r1's noise: each condition's repeat variances and the half-width each check and change can resolve."""
    z = NormalDist().inv_cdf((1 + level) / 2)
    task_replies = [row for row in sealed_rows if row["turn"] is None]
    task_count = len({row["task"] for row in task_replies})
    breaches_sigma = {
        condition: mean_repeat_variance(breach_totals_by_unit(task_replies, condition, gate_demands))
        for condition in (INSTRUCTION, *controls)
    }
    done_sigma = {
        condition: mean_repeat_variance(done_values_by_unit(task_replies, condition))
        for condition in (INSTRUCTION, *controls)
    }
    completion_control = best_done_control(task_replies, controls)
    checks = {
        f"instruction-vs-{control}": half_width(
            z, [breaches_sigma[INSTRUCTION], breaches_sigma[control]], repeats * task_count
        )
        for control in VS_CONTROLS
    }
    checks["completion"] = half_width(
        z, [done_sigma[INSTRUCTION], done_sigma.get(completion_control)], repeats * task_count
    )
    if SOURCE in controls:
        checks["instruction-near-source"] = half_width(
            z, [breaches_sigma[INSTRUCTION], breaches_sigma[SOURCE]], repeats * task_count
        )
    turn_replies = [row for row in sealed_rows if row["turn"] is not None]
    conversation_count = len({row["task"] for row in turn_replies})
    drift_sigma = {
        condition: mean_repeat_variance(drift_slopes_by_unit(turn_replies, condition, gate_demands))
        for condition in (INSTRUCTION, *controls)
    }
    if turn_replies:
        drift_control = SOURCE if SOURCE in controls else EMPTY
        checks["drift"] = half_width(
            z, [drift_sigma[INSTRUCTION], drift_sigma[drift_control]], repeats * conversation_count
        )
    demands_sigma = {
        demand: {
            condition: mean_repeat_variance(breach_totals_by_unit(task_replies, condition, [demand]))
            for condition in (INSTRUCTION, *controls)
        }
        for demand in gate_demands
    }
    demands_change = {
        demand: half_width(z, [by_condition[INSTRUCTION]] * 2, repeats * task_count)
        for demand, by_condition in demands_sigma.items()
    }
    return {
        "sigma": {"breaches": breaches_sigma, "done": done_sigma, "drift": drift_sigma, "demands": demands_sigma},
        "checks": checks,
        "demands": demands_change,
        "done_change": half_width(z, [done_sigma[INSTRUCTION]] * 2, repeats * task_count),
    }


def drift_slopes_by_unit(
    replies: Sequence[ScoredReply], condition: str, demands: Sequence[str]
) -> dict[str, list[float | None]]:
    """Map each conversation to its condition's least-squares slopes of breach totals over turns, one per repeat."""
    turn_totals: dict[tuple[str, int], tuple[list[int], list[int]]] = {}
    for reply in replies:
        if reply["condition"] == condition:
            turns, totals = turn_totals.setdefault((reply["task"], reply["repeat"]), ([], []))
            turns.append(reply["turn"])
            totals.append(breach_total(reply, demands))
    slopes: dict[str, list[float | None]] = {}
    for (conversation, _), (turns, totals) in turn_totals.items():
        slopes.setdefault(conversation, []).append(linear_regression(turns, totals).slope)
    return slopes


def breach_total(reply: ScoredReply, demands: Sequence[str]) -> int:
    """Return the reply's breaches summed over the demands."""
    return sum(reply["breaches"][demand] for demand in demands)


def done_values_by_unit(replies: Sequence[ScoredReply], condition: str) -> dict[str, list[float | None]]:
    """Map each unit to its condition's done values as 1, 0, or null, one per repeat."""
    values: dict[str, list[float | None]] = {}
    for reply in replies:
        if reply["condition"] == condition:
            values.setdefault(reply["task"], []).append(None if reply["done"] is None else float(reply["done"]))
    return values


def best_done_control(replies: Sequence[ScoredReply], controls: Sequence[str]) -> str | None:
    """Return the control with the highest done rate over non-null done values, or null when no control has one."""
    done_rates = {
        control: mean(present)
        for control in controls
        if (present := [reply["done"] for reply in replies if reply["condition"] == control and reply["done"] is not None])
    }
    return max(done_rates, key=done_rates.__getitem__, default=None)


def breach_totals_by_unit(
    replies: Sequence[ScoredReply], condition: str, demands: Sequence[str]
) -> dict[str, list[float | None]]:
    """Map each unit to its condition's breach totals over the demands, one per repeat."""
    totals: dict[str, list[float | None]] = {}
    for reply in replies:
        if reply["condition"] == condition:
            totals.setdefault(reply["task"], []).append(breach_total(reply, demands))
    return totals


def mean_repeat_variance(values_by_unit: Mapping[str, Sequence[float | None]]) -> float | None:
    """Return the mean sample variance over units holding at least two non-null values, or null when none does."""
    present_by_unit = [[value for value in values if value is not None] for values in values_by_unit.values()]
    variances = [variance(present) for present in present_by_unit if len(present) >= 2]
    return mean(variances) if variances else None


def half_width(z: float, variances: Sequence[float | None], repeat_units: int) -> float | None:
    """Return z times the root of the summed variances over the repeat-unit count, or null when any variance is null."""
    if None in variances:
        return None
    return z * sqrt(sum(variances) / repeat_units)
