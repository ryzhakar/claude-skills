import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import partial
from statistics import fmean
from typing import Literal, TypedDict

import numpy

from instruction_eval.records import (
    BUDGET_REASON,
    CAPPED_STOP,
    COLLECTED_FILE,
    DETECTORS_FILE,
    FAIL_OUTCOME,
    FEWEST_REPEATS,
    FIRST_REVISION,
    FIRST_REVISION_NUMBER,
    FROZEN_RECORD,
    GATE_RECORD,
    HYPOTHESIS_FILE,
    INSTRUCTION_FILE,
    KEY_SEPARATOR,
    NO_EFFECT_STOP,
    ORIGINS_FILE,
    PASS_OUTCOME,
    PASSED_STOP,
    SEALED_SPLIT,
    SPENT_INPUT_TOKENS_KEY,
    STOP_RECORD,
    Compares,
    Direction,
    DoneBy,
    Dropped,
    GateCheck,
    Hypothesis,
    NoBudget,
    Record,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    accepted_verdict_paths,
    origin_reply_paths,
    outcome_path,
    parent_revision,
    revision_id,
    revision_number,
    write_record,
)
from instruction_eval.records import Budget as GateBudget
from instruction_eval.scores import (
    SCORE_USER_INPUTS,
    BootstrapRng,
    Comparison,
    Noise,
    ReplyRow,
    ScoredReply,
    breach_total,
    compare_paired,
    instruction_comparisons,
    join_reply_rows,
    paired_units,
    task_means,
)
from instruction_eval.tasks import words

LATER_REVISION_COUNT = 4
LAST_REVISION_NUMBER = LATER_REVISION_COUNT + 1

PassRule = Callable[[float, tuple[float, float], float], bool]


def _undercuts_control_by_gap(mean_difference: float, interval: tuple[float, float], gap: float) -> bool:
    """Tell whether the instruction undercuts its control by the gap on average and the interval lies wholly below zero."""
    return mean_difference <= -gap and interval[1] < 0


def _upper_bound_within_gap(mean_difference: float, interval: tuple[float, float], gap: float) -> bool:
    """Tell whether the interval's upper bound stays at or below the gap."""
    return interval[1] <= gap


def _lower_bound_within_gap(mean_difference: float, interval: tuple[float, float], gap: float) -> bool:
    """Tell whether the interval's lower bound stays at or above minus the gap."""
    return interval[0] >= -gap


_PASS_RULES: Mapping[Compares, PassRule] = {
    "instruction-vs-empty": _undercuts_control_by_gap,
    "instruction-vs-aim": _undercuts_control_by_gap,
    "instruction-vs-placebo": _undercuts_control_by_gap,
    "instruction-near-source": _upper_bound_within_gap,
    "drift": _upper_bound_within_gap,
    "completion": _lower_bound_within_gap,
}


def check_passes(check: GateCheck, comparison: Comparison) -> bool:
    """Tell whether a sealed comparison passes the check's pass rule at its gap, a comparison without units failing."""
    if comparison.mean_difference is None or comparison.interval is None:
        return False
    return _PASS_RULES[check.compares](comparison.mean_difference, comparison.interval, check.gap)


GAP_RESOLUTION_SHARE = 2
SOURCE_CONDITION = "source"
EMPTY_CONDITION = "empty"
_NEAR_SOURCE_COMPARES: Compares = "instruction-near-source"
_VS_EMPTY_COMPARES: Compares = "instruction-vs-empty"


def refuse_unresolvable_gaps(
    checks: Sequence[GateCheck],
    noise: Noise,
    sealed_rows: Sequence[ScoredReply],
    gate_demands: Sequence[str],
    series_has_sources: bool,
    rng: numpy.random.Generator,
) -> None:
    """Raise Refusal on a null noise, a check whose noise exceeds half its gap, or an `instruction-near-source` check r1's sealed rows do not admit."""
    near_source = _NEAR_SOURCE_COMPARES in {check.compares for check in checks}
    if near_source:
        _refuse_near_source_without_sources(series_has_sources)
    _refuse_null_change_noise(noise)
    _refuse_unresolvable_gaps(checks, noise)
    if near_source:
        _refuse_unadmitted_near_source(_vs_empty_check(checks), sealed_rows, gate_demands, noise["level"], rng)


def _refuse_near_source_without_sources(series_has_sources: bool) -> None:
    """Raise Refusal when an `instruction-near-source` check stands in a series without sources."""
    if not series_has_sources:
        raise Refusal(f"{_NEAR_SOURCE_COMPARES} refused: the series has no sources")


def _vs_empty_check(checks: Sequence[GateCheck]) -> GateCheck:
    """Return the `instruction-vs-empty` check, which every gate holds."""
    return next(check for check in checks if check.compares == _VS_EMPTY_COMPARES)


def _refuse_unadmitted_near_source(
    vs_empty: GateCheck, sealed_rows: Sequence[ScoredReply], gate_demands: Sequence[str], level: float, rng: numpy.random.Generator
) -> None:
    """Raise Refusal unless `source` minus `empty` over r1's sealed tasks passes the `instruction-vs-empty` check."""
    gate_breaches = partial(breach_total, demands=gate_demands)
    units = paired_units(task_means(sealed_rows, SOURCE_CONDITION, gate_breaches), task_means(sealed_rows, EMPTY_CONDITION, gate_breaches))
    if not check_passes(vs_empty, compare_paired(units, level, rng)):
        raise Refusal(f"{_NEAR_SOURCE_COMPARES} refused: source minus empty misses the {_VS_EMPTY_COMPARES} gap on r1's sealed rows")


def least_repeats(check: GateCheck, noise: Noise) -> int | None:
    """Return the fewest repeats, at least two, at which the check's noise scaled from r1's repeats is at most half its gap, null without noise."""
    half_width = noise["checks"].get(check.compares)
    if half_width is None:
        return None
    exact_repeats = noise["repeats"] * (GAP_RESOLUTION_SHARE * Fraction(half_width) / Fraction(check.gap)) ** 2
    return max(FEWEST_REPEATS, math.ceil(exact_repeats))


def _refuse_null_change_noise(noise: Noise) -> None:
    """Raise Refusal naming the first gate demand whose change noise is null, then a null done change noise."""
    null_demand = next((demand for demand, half_width in noise["demands"].items() if half_width is None), None)
    if null_demand is not None:
        raise Refusal(f"null noise: demands.{null_demand}")
    if noise["done_change"] is None:
        raise Refusal("null noise: done_change")


def _refuse_unresolvable_gaps(checks: Sequence[GateCheck], noise: Noise) -> None:
    """Raise Refusal naming the first check with null noise, else every check whose noise exceeds half its gap with the least repeats resolving every check."""
    for check in checks:
        if noise["checks"].get(check.compares) is None:
            raise Refusal(f"null noise: {check.compares}")
    unresolvable = [check for check in checks if noise["checks"][check.compares] > check.gap / GAP_RESOLUTION_SHARE]
    if unresolvable:
        named = ", ".join(_unresolvable_gap_description(check, noise) for check in unresolvable)
        raise Refusal(f"unresolvable gap: {named}; least repeats {series_least_repeats(checks, noise)}")


def _unresolvable_gap_description(check: GateCheck, noise: Noise) -> str:
    """Return the check named with its noise against half its gap."""
    return f"{check.compares} (noise {noise['checks'][check.compares]:g} > gap / 2 {check.gap / GAP_RESOLUTION_SHARE:g})"


def series_least_repeats(checks: Sequence[GateCheck], noise: Noise) -> int | None:
    """Return the fewest repeats at which every check's noise is at most half its gap, null when a check has no noise."""
    per_check = [least_repeats(check, noise) for check in checks]
    return None if None in per_check else max(per_check, default=FEWEST_REPEATS)


BudgetUnit = Literal["tokens", "seconds"]
TOKENS_UNIT: BudgetUnit = "tokens"
SECONDS_UNIT: BudgetUnit = "seconds"


class BudgetRefusal(Exception):
    pass


class RevisionCost(TypedDict):
    replies: int
    input_tokens: int | None
    output_tokens: int | None
    seconds: float


@dataclass(frozen=True)
class ReplyCost:
    input_tokens: int | None
    output_tokens: int | None
    seconds: float


@dataclass(frozen=True)
class Budget:
    unit: BudgetUnit
    ceiling: float


@dataclass(frozen=True)
class SeriesShape:
    task_count: int
    open_task_count: int
    conversation_turns: int
    repeats: int
    omission_sentences: int


def _reply_cost_in_unit(reply: ReplyCost, unit: BudgetUnit) -> float:
    """Return the reply's cost in the budget unit."""
    if unit == TOKENS_UNIT:
        return reply.input_tokens + reply.output_tokens
    if unit == SECONDS_UNIT:
        return reply.seconds
    raise ValueError(f"unknown budget unit: {unit}")


def _mean_reply_cost(r1_replies: list[ReplyCost], unit: BudgetUnit) -> float:
    """Return r1's mean cost per reply in the budget unit."""
    return _total_cost(r1_replies, unit) / len(r1_replies)


def _total_cost(replies: list[ReplyCost], unit: BudgetUnit) -> float:
    """Return the replies' summed cost in the budget unit."""
    return sum(_reply_cost_in_unit(reply, unit) for reply in replies)


def _predicted_cost(r1_replies: list[ReplyCost], shape: SeriesShape, unit: BudgetUnit) -> float:
    """Return r1's cost plus the mean-priced replies of the later revisions."""
    reads_per_revision = (shape.task_count + shape.conversation_turns) * shape.repeats
    omission_reads = shape.open_task_count * shape.repeats * shape.omission_sentences
    return _total_cost(r1_replies, unit) + LATER_REVISION_COUNT * _mean_reply_cost(
        r1_replies, unit
    ) * (reads_per_revision + omission_reads)


def _refuse_empty_r1(r1_replies: list[ReplyCost]) -> None:
    """Raise BudgetRefusal when r1 has no replies to price from."""
    if not r1_replies:
        raise BudgetRefusal("budget refused: r1 has no replies")


def _refuse_token_budget_over_null_tokens(r1_replies: list[ReplyCost], unit: BudgetUnit) -> None:
    """Raise BudgetRefusal when the unit is tokens and any r1 reply has null tokens."""
    has_null_tokens = any(
        reply.input_tokens is None or reply.output_tokens is None for reply in r1_replies
    )
    if unit == TOKENS_UNIT and has_null_tokens:
        raise BudgetRefusal("tokens budget refused: an r1 reply has null tokens")


def refuse_unaffordable_freeze(
    budget: Budget | None, r1_replies: list[ReplyCost], shape: SeriesShape
) -> None:
    """Raise BudgetRefusal when the budget ceiling is below the series' predicted cost."""
    if budget is None:
        return
    _refuse_empty_r1(r1_replies)
    _refuse_token_budget_over_null_tokens(r1_replies, budget.unit)
    predicted = _predicted_cost(r1_replies, shape, budget.unit)
    if predicted > budget.ceiling:
        raise BudgetRefusal(f"predicted cost {predicted:g} exceeds ceiling {budget.ceiling:g}")


def refuse_unaffordable_ask(
    budget: Budget | None, r1_replies: list[ReplyCost], cost_so_far: float, ask_reply_count: int
) -> None:
    """Raise BudgetRefusal when the cost so far plus the ask's replies at r1's mean cost exceeds the ceiling."""
    if budget is None:
        return
    _refuse_empty_r1(r1_replies)
    _refuse_token_budget_over_null_tokens(r1_replies, budget.unit)
    projected = cost_so_far + ask_reply_count * _mean_reply_cost(r1_replies, budget.unit)
    if projected > budget.ceiling:
        raise BudgetRefusal(f"projected cost {projected:g} exceeds ceiling {budget.ceiling:g}")


def _sum_unless_null(values: list[int | None]) -> int | None:
    """Sum the values, or return null when any value is null."""
    return None if None in values else sum(values)


def sum_revision_cost(replies: list[ReplyCost]) -> RevisionCost:
    """Sum replies into the cost record of a revision's asks, token sums null when any reply's are."""
    return {
        "replies": len(replies),
        "input_tokens": _sum_unless_null([reply.input_tokens for reply in replies]),
        "output_tokens": _sum_unless_null([reply.output_tokens for reply in replies]),
        "seconds": sum(reply.seconds for reply in replies),
    }


def kept_revision(outcomes: Mapping[str, Record]) -> str | None:
    """Return the revision `best-estimate-shortest` keeps from each gated revision's outcome by id, null when none passed completion."""
    candidates = [revision for revision, outcome in outcomes.items() if outcome["completion_passed"]]
    return min(candidates, key=lambda revision: _keep_rank(revision, outcomes[revision]), default=None)


def _keep_rank(revision: str, outcome: Record) -> tuple[bool, float, int, int]:
    """Return a candidate's rank, lowest first: a pass, then fewer instruction breaches, then fewer words, then the lower number."""
    return (outcome["outcome"] != PASS_OUTCOME, outcome["instruction_breaches"], outcome["words"], revision_number(revision))


COMPLETION_TARGET = "completion"
INSTRUCTION_CONDITION = "instruction"
DOWN: Direction = "down"
UP: Direction = "up"
ChangedFromParent = Literal["changed", "reversed", "unchanged", "unresolved"]
CHANGED: ChangedFromParent = "changed"
REVERSED: ChangedFromParent = "reversed"
UNCHANGED: ChangedFromParent = "unchanged"
UNRESOLVED: ChangedFromParent = "unresolved"


@dataclass(frozen=True)
class ParentComparison:
    """A revision's instruction minus its parent's on the hypothesis target, and what that says about the predicted change."""

    target: str
    comparison: Comparison
    changed_from_parent: ChangedFromParent


def compare_with_parent(
    revision_rows: Sequence[ScoredReply],
    parent_rows: Sequence[ScoredReply],
    target: str,
    direction: Direction,
    predicted_size: float,
    level: float,
    rng: numpy.random.Generator,
) -> ParentComparison:
    """Compare the revision's sealed instruction replies with its parent's on the target, a demand id or `completion`."""
    target_value = partial(_reply_value, target=target)
    units = paired_units(task_means(revision_rows, INSTRUCTION_CONDITION, target_value), task_means(parent_rows, INSTRUCTION_CONDITION, target_value))
    comparison = compare_paired(units, level, rng)
    return ParentComparison(target, comparison, _movement_verdict(comparison.interval, direction, predicted_size))


def _reply_value(row: ScoredReply, target: str) -> float | None:
    """Return the reply's breaches of the target demand, or its done as 1 or 0 for `completion`, null when done is null."""
    if target == COMPLETION_TARGET:
        return None if row["done"] is None else float(row["done"])
    return float(row["breaches"][target])


def _movement_verdict(
    interval: tuple[float, float] | None, direction: Direction, predicted_size: float
) -> ChangedFromParent:
    """Return `changed` or `reversed` when the interval excludes zero, `unchanged` when it holds zero narrower than the predicted size, else `unresolved`."""
    if interval is None:
        return UNRESOLVED
    low, high = interval
    if high < 0:
        return CHANGED if direction == DOWN else REVERSED
    if low > 0:
        return CHANGED if direction == UP else REVERSED
    return UNCHANGED if (high - low) / 2 < predicted_size else UNRESOLVED


def stop_after(revision: str, outcomes: Mapping[str, Record], budget: Budget | None, cost_so_far: float) -> Record | None:
    """Return the `9-stop.yaml` content the gated revision's stop earns, first match winning, null when the series goes on."""
    stop = _first_matching_stop(revision, outcomes, budget, cost_so_far)
    return None if stop is None else {**stop, "kept": kept_revision(outcomes)}


def _first_matching_stop(
    revision: str, outcomes: Mapping[str, Record], budget: Budget | None, cost_so_far: float
) -> Record | None:
    """Return the stop and its reason of the first rule the revision meets, null when it meets none."""
    if outcomes[revision]["outcome"] == PASS_OUTCOME:
        return {"stop": PASSED_STOP}
    if _unchanged_from_parent(revision, outcomes) and _unchanged_from_parent(parent_revision(revision), outcomes):
        return {"stop": NO_EFFECT_STOP}
    if revision_number(revision) >= LAST_REVISION_NUMBER:
        return {"stop": CAPPED_STOP}
    if budget is not None and cost_so_far >= budget.ceiling:
        return {"stop": CAPPED_STOP, "reason": BUDGET_REASON}
    return None


def _unchanged_from_parent(revision: str, outcomes: Mapping[str, Record]) -> bool:
    """Tell whether the revision's outcome holds `unchanged` as its `changed_from_parent`, a missing outcome or value being no."""
    return outcomes.get(revision, {}).get("changed_from_parent") == UNCHANGED


GATE_COMMAND = "revision gate"
GATE_KEYS = ("repeats", "level", "done_by", "checks", "keep_rule", "budget")
STOP_GATE_KEYS = ("keep_rule", "budget")
HYPOTHESIS_KEYS = ("failing_demand", "replies_read", "change", "predicted_movement")
NO_BUDGET: NoBudget = "none"


def revision_gate(files: SeriesFolder, revision: str, bootstrap_rng: BootstrapRng) -> None:
    """Write the revision's `9-outcome.yaml` from its sealed rows, each bootstrap drawing on a fresh `bootstrap_rng()`, and `9-stop.yaml` when a stop applies."""
    _refuse_unusable_series(files)
    records = SeriesRecords(files)
    gate = records.complete_gate()
    records.frozen()
    gate_demands = _gate_demands(records)
    measured = _measured_revision(records, revision, gate.done_by)
    outcome = _outcome(files, records, revision, measured, gate_demands, gate.checks, gate.level, bootstrap_rng)
    earlier = _earlier_outcomes(files, records, revision)
    reads = _gate_reads(revision, measured, earlier)
    if revision != FIRST_REVISION:
        parent = _measured_revision(records, parent_revision(revision), gate.done_by)
        outcome = {**outcome, **_parent_fields(records.hypothesis(revision), measured.sealed_rows, parent.sealed_rows, gate.level, bootstrap_rng)}
        reads = [*reads, *hypothesis_reads(revision), *parent.reads]
    outcomes = {**earlier, revision: outcome}
    budget = _stop_budget(gate.budget)
    stop = stop_after(revision, outcomes, budget, _cost_so_far(outcomes, budget))
    write_record(files, outcome_path(revision), outcome, reads)
    if stop is not None:
        write_record(files, STOP_RECORD, stop, _stop_reads(outcomes))


@dataclass(frozen=True)
class _MeasuredRevision:
    """A revision's sealed reply rows, the cost of its own replies, and the files they were read from."""

    sealed_rows: list[ReplyRow]
    own_replies: list[ReplyCost]
    reads: list[str]


def _refuse_unusable_series(files: SeriesFolder) -> None:
    """Refuse a folder that is no series, a stopped series, a changed frozen part, or a broken revision chain."""
    from instruction_eval.series import guard_series

    guard_series(files, GATE_COMMAND)


def _gate_demands(records: SeriesRecords) -> list[str]:
    """Return the demands r1's coverage does not drop, in coverage order."""
    return [demand for demand, sentences in records.coverage(FIRST_REVISION).demands.items() if not isinstance(sentences, Dropped)]


def _measured_revision(records: SeriesRecords, revision: str, done_by: DoneBy) -> _MeasuredRevision:
    """Load a revision's sealed rows and own reply costs, refusing a missing collection or a reply origin without its reply file."""
    collected = records.collected(revision)
    origins = records.origins(revision)
    verdicts = records.accepted_verdicts(revision, collected)
    reply_paths = origin_reply_paths(origins, revision)
    own_paths = [path for path in reply_paths.values() if path.startswith(f"{revision}/")]
    return _MeasuredRevision(
        sealed_rows=join_reply_rows(origins, verdicts, records.detectors(revision), done_by, SEALED_SPLIT),
        own_replies=[_reply_cost(records.reply(path)) for path in own_paths],
        reads=[*reply_paths.values(), f"{revision}/{ORIGINS_FILE}", *accepted_verdict_paths(revision, collected), f"{revision}/{COLLECTED_FILE}", f"{revision}/{DETECTORS_FILE}"],
    )


def _reply_cost(reply: Record) -> ReplyCost:
    """Return a reply's spent input tokens, output tokens, and seconds."""
    return ReplyCost(reply["cost"][SPENT_INPUT_TOKENS_KEY], reply["cost"]["output_tokens"], reply["seconds"])


def _outcome(
    files: SeriesFolder,
    records: SeriesRecords,
    revision: str,
    measured: _MeasuredRevision,
    gate_demands: Sequence[str],
    checks: Sequence[GateCheck],
    level: float,
    bootstrap_rng: BootstrapRng,
) -> dict[str, object]:
    """Return the outcome of the revision's sealed rows: every check, the keep ranks, and the cost of its asks."""
    task_rows = [row for row in measured.sealed_rows if row["turn"] is None]
    turn_rows = [row for row in measured.sealed_rows if row["turn"] is not None]
    comparisons = instruction_comparisons(task_rows, turn_rows, gate_demands, level, bootstrap_rng)
    gated = [_gated_check(check, comparisons[check.compares]) for check in checks]
    return {
        "outcome": PASS_OUTCOME if all(check["pass"] for check in gated) else FAIL_OUTCOME,
        "checks": gated,
        "instruction_breaches": fmean(breach_total(row, gate_demands) for row in task_rows if row["condition"] == INSTRUCTION_CONDITION),
        "completion_passed": next(check["pass"] for check in gated if check["compares"] == COMPLETION_TARGET),
        "words": len(words(files.read_bytes(f"{revision}/{INSTRUCTION_FILE}").decode())),
        "cost": sum_revision_cost(measured.own_replies),
    }


def _gated_check(check: GateCheck, comparison: Mapping[str, object]) -> dict[str, object]:
    """Return a check as `9-outcome.yaml` stores it: its compares and gap, the sealed mean difference and interval, and whether it passes."""
    interval = comparison["interval"]
    sealed = Comparison(comparison["mean_difference"], None if interval is None else tuple(interval), comparison["units"])
    return {"compares": check.compares, "gap": check.gap, "mean_difference": sealed.mean_difference, "interval": interval, "pass": check_passes(check, sealed)}


def _parent_fields(hypothesis: Hypothesis, rows: Sequence[ScoredReply], parent_rows: Sequence[ScoredReply], level: float, bootstrap_rng: BootstrapRng) -> dict[str, object]:
    """Return `changed_from_parent` and `parent_comparison`: the revision's sealed instruction minus its parent's on the hypothesis target."""
    movement = hypothesis.predicted_movement
    compared = compare_with_parent(rows, parent_rows, hypothesis.failing_demand, movement.direction, movement.size, level, bootstrap_rng())
    interval = None if compared.comparison.interval is None else list(compared.comparison.interval)
    return {
        "changed_from_parent": compared.changed_from_parent,
        "parent_comparison": {"target": compared.target, "mean_difference": compared.comparison.mean_difference, "interval": interval},
    }


def _earlier_outcomes(files: SeriesFolder, records: SeriesRecords, revision: str) -> dict[str, Record]:
    """Return the outcome of each gated revision before the given one, by id in order."""
    earlier = (revision_id(number) for number in range(FIRST_REVISION_NUMBER, revision_number(revision)))
    return {other: records.outcome(other) for other in earlier if files.holds(outcome_path(other))}


def _gate_reads(revision: str, measured: _MeasuredRevision, earlier: Mapping[str, Record]) -> list[str]:
    """Return what `revision gate` reads of every revision: `revision score`'s reads, every gate key, the freeze, the instruction, and every earlier outcome."""
    return [
        *SCORE_USER_INPUTS,
        *measured.reads,
        *(f"{GATE_RECORD}{KEY_SEPARATOR}{key}" for key in GATE_KEYS),
        FROZEN_RECORD,
        f"{revision}/{INSTRUCTION_FILE}",
        *(outcome_path(other) for other in earlier),
    ]


def hypothesis_reads(revision: str) -> list[str]:
    """Return each key of the revision's hypothesis as a read."""
    return [f"{revision}/{HYPOTHESIS_FILE}{KEY_SEPARATOR}{key}" for key in HYPOTHESIS_KEYS]


def _stop_budget(budget: GateBudget | NoBudget) -> Budget | None:
    """Return the gate's budget as the stop rules take it, null without a ceiling."""
    return None if budget == NO_BUDGET else Budget(budget.unit, budget.ceiling)


def _cost_so_far(outcomes: Mapping[str, Record], budget: Budget | None) -> float:
    """Return every gated revision's ask cost summed in the budget unit, zero without a budget, refusing a tokens budget over a revision without token counts."""
    if budget is None:
        return 0
    costs = {revision: ReplyCost(outcome["cost"]["input_tokens"], outcome["cost"]["output_tokens"], outcome["cost"]["seconds"]) for revision, outcome in outcomes.items()}
    uncounted = next((revision for revision, cost in costs.items() if None in (cost.input_tokens, cost.output_tokens)), None)
    if budget.unit == TOKENS_UNIT and uncounted is not None:
        raise Refusal(f"tokens budget refused: {uncounted} asked replies without token counts")
    return _total_cost(list(costs.values()), budget.unit)


def _stop_reads(outcomes: Mapping[str, Record]) -> list[str]:
    """Return what the stop reads: the keep rule and budget, the freeze, and every gated revision's outcome."""
    return [*(f"{GATE_RECORD}{KEY_SEPARATOR}{key}" for key in STOP_GATE_KEYS), FROZEN_RECORD, *(outcome_path(revision) for revision in outcomes)]
