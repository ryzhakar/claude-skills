import re
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from math import sqrt
from statistics import NormalDist, fmean, linear_regression, mean, variance
from typing import NamedTuple, TypedDict

import numpy

from instruction_eval.coverage import CODE_FENCE_OPENING, closing_code_fence, split_sentences
from instruction_eval.records import (
    CONDITION_KEY,
    REPEAT_KEY,
    SPLIT_KEY,
    TASK_KEY,
    TURN_KEY,
    REPLY_TEXT_KEY,
    DONE_BY_KEY,
    LEVEL_KEY,
    COVERAGE_KEYS,
    coverage_input,
    ANCHOR_KEY,
    COLLECTED_FILE,
    COMPLETION_COMPARES,
    DEMANDS_INPUT,
    DETECTOR_DEMANDS,
    DETECTORS_FILE,
    DRIFT_COMPARES,
    EMPTY_CONTROL,
    FIRST_REVISION,
    GATE_RECORD,
    KEY_SEPARATOR,
    NEAR_SOURCE_COMPARES,
    OPEN_SPLIT,
    ORIGINS_FILE,
    SCORES_FILE,
    SOURCE_CONTROL,
    TASKS_RECORD,
    VS_COMPARES,
    DoneBy,
    Gate,
    LongSentencesDemand,
    PatternDemand,
    Record,
    SeriesFolder,
    SeriesRecords,
    Split,
    accepted_verdict_paths,
    missing_gate_key,
    origin_reply_paths,
    write_record,
)
from instruction_eval.tasks import INSTRUCTION_CONDITION, words

_TWO_SIDED_TAILS = 2
_LEAST_VALUES_FOR_VARIANCE = 2
_LEAST_TURNS_FOR_SLOPE = 2
_ANSWER_KEY_DONE: DoneBy = "answer-key"


class ScoredReply(TypedDict):
    """One sealed r1 reply scored: its condition, task or conversation, repeat, turn or null, breaches, and done."""

    condition: str
    task: str
    repeat: int
    turn: int | None
    breaches: Mapping[str, int]
    done: bool | None


class ReplyRow(ScoredReply):
    """One reply of a revision joined from its origin, its accepted verdict, and its detector entry, as `8-scores.yaml` rows hold it."""

    id: str
    borrowed_from: str | None
    kind: str
    done_by_answer_key: bool | None
    done_by_judge: bool | None


def join_reply_rows(
    origins: Record, verdicts: Iterable[Record], detectors: Record, done_by: DoneBy, split: Split
) -> list[ReplyRow]:
    """Return a row per reply of the split in origin order, anchors left out, breaches of every demand, done chosen by `done_by`."""
    judged = _entries_by_id(entry for verdict in verdicts for entry in verdict["verdicts"])
    detected = _entries_by_id(detectors["verdicts"])
    return [
        _reply_row(blind_id, origin, judged[blind_id], detected[blind_id], done_by)
        for blind_id, origin in origins["ids"].items()
        if ANCHOR_KEY not in origin and origin[SPLIT_KEY] == split
    ]


def _entries_by_id(entries: Iterable[Record]) -> dict[str, Record]:
    """Map each verdict or detector entry's blind id to the entry."""
    return {entry["id"]: entry for entry in entries}


def _reply_row(blind_id: str, origin: Record, judged: Record, detected: Record, done_by: DoneBy) -> ReplyRow:
    """Return the row of one reply from its origin, its judge entry, and its detector entry."""
    return {
        "id": blind_id,
        CONDITION_KEY: origin[CONDITION_KEY],
        TASK_KEY: origin[TASK_KEY],
        REPEAT_KEY: origin[REPEAT_KEY],
        TURN_KEY: origin.get(TURN_KEY),
        "borrowed_from": origin["borrowed_from"],
        "breaches": {**judged["breaches"], **detected["breaches"]},
        "kind": judged["kind"],
        "done_by_answer_key": detected["done_by_answer_key"],
        "done_by_judge": judged["done"],
        "done": _reply_done(done_by, detected["done_by_answer_key"], judged["done"]),
    }


def _reply_done(done_by: DoneBy, done_by_answer_key: bool | None, done_by_judge: bool | None) -> bool | None:
    """Return the judge's done, unless answer-key mode holds a key verdict for the reply's task."""
    if done_by == _ANSWER_KEY_DONE and done_by_answer_key is not None:
        return done_by_answer_key
    return done_by_judge


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
    z = _z_for_level(level)
    conditions = [INSTRUCTION_CONDITION, *controls]
    task_replies = [row for row in sealed_rows if row[TURN_KEY] is None]
    turn_replies = [row for row in sealed_rows if row[TURN_KEY] is not None]
    task_repeat_units = repeats * _unit_count(task_replies)
    sigma: NoiseSigma = {
        "breaches": _repeat_variances(task_replies, conditions, partial(breach_total, demands=gate_demands)),
        "done": _repeat_variances(task_replies, conditions, done_value),
        "drift": {
            condition: _mean_repeat_variance(_drift_slopes_by_unit(turn_replies, condition, gate_demands))
            for condition in conditions
        },
        "demands": {
            demand: _repeat_variances(task_replies, conditions, partial(breach_total, demands=[demand]))
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
            demand: _change_half_width(z, by_condition[INSTRUCTION_CONDITION], task_repeat_units)
            for demand, by_condition in sigma["demands"].items()
        },
        "done_change": _change_half_width(z, sigma["done"][INSTRUCTION_CONDITION], task_repeat_units),
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
        compares: _half_width(z, [breaches[INSTRUCTION_CONDITION], breaches[control]], task_repeat_units)
        for control, compares in VS_COMPARES.items()
    }
    checks[COMPLETION_COMPARES] = _half_width(z, [sigma["done"][INSTRUCTION_CONDITION], done_of_completion_control], task_repeat_units)
    if SOURCE_CONTROL in controls:
        checks[NEAR_SOURCE_COMPARES] = _half_width(z, [breaches[INSTRUCTION_CONDITION], breaches[SOURCE_CONTROL]], task_repeat_units)
    if conversation_repeat_units:
        drift = sigma["drift"]
        checks[DRIFT_COMPARES] = _half_width(z, [drift[INSTRUCTION_CONDITION], drift[_drift_control(controls)]], conversation_repeat_units)
    return checks


def _drift_control(controls: Sequence[str]) -> str:
    """Return the control drift is compared with: `source` when the controls hold it, else `empty`."""
    return SOURCE_CONTROL if SOURCE_CONTROL in controls else EMPTY_CONTROL


def _unit_count(replies: Sequence[ScoredReply]) -> int:
    """Return how many distinct tasks or conversations the replies span."""
    return len({reply[TASK_KEY] for reply in replies})


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
        if reply[CONDITION_KEY] == condition:
            values.setdefault(reply[TASK_KEY], []).append(metric(reply))
    return values


def _drift_slopes_by_unit(
    replies: Sequence[ScoredReply], condition: str, demands: Sequence[str]
) -> dict[str, list[float | None]]:
    """Map each conversation to its condition's least-squares slopes of breach totals over turns, one per repeat."""
    turn_totals: dict[tuple[str, int], tuple[list[int], list[int]]] = {}
    for reply in replies:
        if reply[CONDITION_KEY] == condition and (turn := reply[TURN_KEY]) is not None:
            turns, totals = turn_totals.setdefault((reply[TASK_KEY], reply[REPEAT_KEY]), ([], []))
            turns.append(turn)
            totals.append(breach_total(reply, demands))
    slopes: dict[str, list[float | None]] = {}
    for (conversation, _), (turns, totals) in turn_totals.items():
        slopes.setdefault(conversation, []).append(_least_squares_slope(turns, totals))
    return slopes


def _least_squares_slope(turns: Sequence[int], totals: Sequence[int]) -> float | None:
    """Return the least-squares slope of totals over turns, or null when fewer than two distinct turns exist."""
    if len(set(turns)) < _LEAST_TURNS_FOR_SLOPE:
        return None
    return linear_regression(turns, totals).slope


def breach_total(reply: ScoredReply, demands: Sequence[str]) -> int:
    """Return the reply's breaches summed over the demands."""
    return sum(reply["breaches"][demand] for demand in demands)


def done_value(reply: ScoredReply) -> float | None:
    """Return the reply's done as 1 or 0, or null when done is null."""
    return None if reply["done"] is None else float(reply["done"])


def _best_done_control(replies: Sequence[ScoredReply], controls: Sequence[str]) -> str | None:
    """Return the control with the highest done rate over non-null done values, or null when no control has one."""
    done_rates = {
        control: done_rate
        for control in controls
        if (done_rate := _done_rate([reply for reply in replies if reply[CONDITION_KEY] == control])) is not None
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
    _require_valid_level(level)
    if not units:
        return Comparison(mean_difference=None, interval=None, units=0)
    differences = _unit_differences(units)
    resample_means = _bootstrap_resample_means(differences, rng)
    return Comparison(
        mean_difference=float(differences.mean()),
        interval=_percentile_interval(resample_means, level),
        units=len(differences),
    )


def paired_units(instruction_values: Mapping[str, float], other_values: Mapping[str, float]) -> list[PairedUnit]:
    """Pair each unit's instruction-side mean with its other-side mean, units one side lacks left out."""
    return [PairedUnit(instruction_values[unit], other_values[unit]) for unit in sorted(instruction_values.keys() & other_values.keys())]


def task_means(rows: Sequence[ScoredReply], condition: str, reply_value: Callable[[ScoredReply], float | None]) -> dict[str, float]:
    """Map each task to the mean value of the condition's single-task replies over repeats, tasks without a value left out."""
    values_by_task: dict[str, list[float]] = {}
    for row in rows:
        value = reply_value(row)
        if row[CONDITION_KEY] == condition and row[TURN_KEY] is None and value is not None:
            values_by_task.setdefault(row[TASK_KEY], []).append(value)
    return {task: mean(values) for task, values in values_by_task.items()}


def _unit_differences(units: Sequence[PairedUnit]) -> numpy.ndarray:
    """Return each unit's instruction value minus its other value."""
    return numpy.array([unit.instruction - unit.other for unit in units], dtype=float)


def _bootstrap_resample_means(differences: numpy.ndarray, rng: numpy.random.Generator) -> numpy.ndarray:
    """Return the mean difference of each of the resamples drawn from units with replacement."""
    resampled_indices = rng.integers(0, len(differences), size=(BOOTSTRAP_RESAMPLES, len(differences)))
    return differences[resampled_indices].mean(axis=1)


def _percentile_interval(resample_means: numpy.ndarray, level: float) -> tuple[float, float]:
    """Return the central `level` interval of the resample means by numpy's linear quantile."""
    upper_probability = _upper_tail_probability(level)
    low, high = numpy.quantile(resample_means, [1 - upper_probability, upper_probability], method="linear")
    return float(low), float(high)


def _z_for_level(level: float) -> float:
    """Return the standard normal quantile at (1 + `level`) / 2."""
    _require_valid_level(level)
    return NormalDist().inv_cdf(_upper_tail_probability(level))


def _upper_tail_probability(level: float) -> float:
    """Return the probability (1 + `level`) / 2 bounding a central `level` interval from above."""
    return (1 + level) / _TWO_SIDED_TAILS


def _require_valid_level(level: float) -> None:
    """Raise ValueError naming `level` unless it lies strictly between 0 and 1."""
    if not 0 < level < 1:
        raise ValueError(f"level must lie strictly between 0 and 1, got {level}")


BootstrapRng = Callable[[], numpy.random.Generator]
LEVEL_INPUT = f"{GATE_RECORD}{KEY_SEPARATOR}{LEVEL_KEY}"
DONE_BY_INPUT = f"{GATE_RECORD}{KEY_SEPARATOR}{DONE_BY_KEY}"
DEMANDS_AND_TASKS_INPUTS = (DEMANDS_INPUT, f"{TASKS_RECORD}{KEY_SEPARATOR}tasks", f"{TASKS_RECORD}{KEY_SEPARATOR}conversations")
SCORE_USER_INPUTS = (
    *DEMANDS_AND_TASKS_INPUTS,
    *(coverage_input(FIRST_REVISION, key) for key in COVERAGE_KEYS),
    LEVEL_INPUT,
    DONE_BY_INPUT,
)
FENCE_OPENING = re.compile(CODE_FENCE_OPENING)
LINE_BREAK = "\n"


def revision_detect(files: SeriesFolder, revision: str) -> None:
    """Write the revision's `7-detectors.yaml`: per reply, its `pattern` and `long-sentences` breaches outside fenced code and its answer-key match."""
    records = SeriesRecords(files)
    detector_demands = [demand for demand in records.demands().demands if isinstance(demand, DETECTOR_DEMANDS)]
    answer_keys = {task.id: task.answer_key for task in records.tasks().tasks}
    origins = records.origins(revision)
    reply_paths = origin_reply_paths(origins, revision)
    replies = {blind_id: records.reply(path) for blind_id, path in reply_paths.items()}
    verdicts = [
        _detector_entry(blind_id, reply[REPLY_TEXT_KEY], detector_demands, answer_keys.get(reply[TASK_KEY])) for blind_id, reply in replies.items()
    ]
    write_record(files, f"{revision}/{DETECTORS_FILE}", {"verdicts": verdicts}, [*DEMANDS_AND_TASKS_INPUTS, *reply_paths.values(), f"{revision}/{ORIGINS_FILE}"])


def _detector_entry(
    blind_id: str, text: str, detector_demands: Sequence[PatternDemand | LongSentencesDemand], answer_key: re.Pattern[str] | None
) -> dict[str, object]:
    """Return one reply's detector entry: breaches of each detector demand outside fenced code, and the answer key's match on the full text, null without a key."""
    prose = _without_fenced_code(text)
    return {
        "id": blind_id,
        "breaches": {demand.id: _detected_breaches(demand, prose) for demand in detector_demands},
        "done_by_answer_key": None if answer_key is None else answer_key.search(text) is not None,
    }


def _detected_breaches(demand: PatternDemand | LongSentencesDemand, prose: str) -> int:
    """Return the non-overlapping pattern matches, or the sentences holding more words than the limit."""
    if isinstance(demand, PatternDemand):
        return sum(1 for _ in demand.pattern.finditer(prose))
    encoded = prose.encode()
    return sum(1 for sentence in split_sentences(encoded) if len(words(encoded[sentence.start : sentence.end].decode())) > demand.limit)


def _without_fenced_code(text: str) -> str:
    """Return the text with each fenced code block, through its closing fence or the text's end, replaced by one empty line."""
    kept: list[str] = []
    closing: re.Pattern[str] | None = None
    for line in text.split(LINE_BREAK):
        if closing is not None:
            closing = None if closing.match(line) else closing
        elif opening := FENCE_OPENING.match(line):
            closing = re.compile(closing_code_fence(opening.group(1)))
            kept.append("")
        else:
            kept.append(line)
    return LINE_BREAK.join(kept)


def revision_score(files: SeriesFolder, revision: str, bootstrap_rng: BootstrapRng) -> None:
    """Write the revision's `8-scores.yaml` from its open replies, each bootstrap drawing on a fresh `bootstrap_rng()`: rows, per-condition means, comparisons, drift, and done disagreements."""
    records = SeriesRecords(files)
    level, done_by = _scoring_keys(records.gate())
    origins = records.origins(revision)
    collected = records.collected(revision)
    verdicts = records.accepted_verdicts(revision, collected)
    rows = join_reply_rows(origins, verdicts, records.detectors(revision), done_by, OPEN_SPLIT)
    scores = _open_scores(rows, records.gate_demands(), level, bootstrap_rng)
    write_record(files, f"{revision}/{SCORES_FILE}", scores, _score_reads(revision, origins, collected))


def _scoring_keys(gate: Gate) -> tuple[float, DoneBy]:
    """Return the gate's level and done mode, refusing either key unwritten."""
    if gate.level is None:
        raise missing_gate_key(LEVEL_KEY)
    if gate.done_by is None:
        raise missing_gate_key(DONE_BY_KEY)
    return gate.level, gate.done_by


def _score_reads(revision: str, origins: Record, collected: Record) -> list[str]:
    """Return what `revision score` reads: the user keys and the revision's measured records."""
    return [*SCORE_USER_INPUTS, *measured_reads(revision, origins, collected)]


def measured_reads(revision: str, origins: Record, collected: Record) -> list[str]:
    """Return a measured revision's records: every reply file the origins name, the origins, the accepted verdicts, the collection, and the detector counts."""
    return [
        *origin_reply_paths(origins, revision).values(),
        f"{revision}/{ORIGINS_FILE}",
        *accepted_verdict_paths(revision, collected),
        f"{revision}/{COLLECTED_FILE}",
        f"{revision}/{DETECTORS_FILE}",
    ]


def _open_scores(rows: Sequence[ReplyRow], gate_demands: Sequence[str], level: float, bootstrap_rng: BootstrapRng) -> dict[str, object]:
    """Return the scores record of the open rows: the rows, per-condition means, comparisons, drift, and done disagreements."""
    task_rows = [row for row in rows if row[TURN_KEY] is None]
    turn_rows = [row for row in rows if row[TURN_KEY] is not None]
    return {
        SPLIT_KEY: OPEN_SPLIT,
        "rows": list(rows),
        "by_condition": {
            condition: _condition_scores([row for row in task_rows if row[CONDITION_KEY] == condition], gate_demands)
            for condition in _conditions_of(task_rows)
        },
        "comparisons": instruction_comparisons(task_rows, turn_rows, gate_demands, level, bootstrap_rng),
        "drift": {
            condition: _drift(slopes, level, bootstrap_rng)
            for condition in _conditions_of(turn_rows)
            if (slopes := _conversation_slopes(turn_rows, gate_demands, condition))
        },
        "disagreements": [row["id"] for row in rows if _key_and_judge_disagree(row)],
    }


def _key_and_judge_disagree(row: ReplyRow) -> bool:
    """Tell whether the reply holds both a key verdict and a judge verdict on done and they differ."""
    return None not in (row["done_by_answer_key"], row["done_by_judge"]) and row["done_by_answer_key"] != row["done_by_judge"]


def instruction_comparisons(
    task_rows: Sequence[ScoredReply], turn_rows: Sequence[ScoredReply], gate_demands: Sequence[str], level: float, bootstrap_rng: BootstrapRng
) -> dict[str, dict[str, object]]:
    """Map each compares the rows define to instruction minus its control: per task for breaches over gate demands and done rate, per conversation for drift."""
    controls = [condition for condition in (*VS_COMPARES, SOURCE_CONTROL) if condition in _conditions_of(task_rows)]
    task_breaches = partial(_task_means_of, task_rows, partial(breach_total, demands=gate_demands))
    comparisons = {VS_COMPARES[control]: _instruction_minus(task_breaches, control, level, bootstrap_rng) for control in controls if control != SOURCE_CONTROL}
    if SOURCE_CONTROL in controls:
        comparisons[NEAR_SOURCE_COMPARES] = _instruction_minus(task_breaches, SOURCE_CONTROL, level, bootstrap_rng)
    comparisons[COMPLETION_COMPARES] = _instruction_minus(partial(_task_means_of, task_rows, done_value), _best_done_control(task_rows, controls), level, bootstrap_rng)
    if turn_rows:
        comparisons[DRIFT_COMPARES] = _instruction_minus(partial(_conversation_slopes, turn_rows, gate_demands), _drift_control(controls), level, bootstrap_rng)
    return comparisons


def _task_means_of(task_rows: Sequence[ScoredReply], reply_value: Callable[[ScoredReply], float | None], condition: str | None) -> dict[str, float]:
    """Map each task to the condition's mean reply value, no task without a condition."""
    return task_means(task_rows, condition, reply_value) if condition else {}


def _conversation_slopes(turn_rows: Sequence[ScoredReply], gate_demands: Sequence[str], condition: str) -> dict[str, float]:
    """Map each conversation to the condition's drift slope averaged over repeats, conversations without a slope left out."""
    return {
        conversation: fmean(present)
        for conversation, slopes in _drift_slopes_by_unit(turn_rows, condition, gate_demands).items()
        if (present := [slope for slope in slopes if slope is not None])
    }


def _instruction_minus(unit_means: Callable[[str | None], Mapping[str, float]], other: str | None, level: float, bootstrap_rng: BootstrapRng) -> dict[str, object]:
    """Return the comparison record of instruction minus the other condition over the units both hold a mean for."""
    units = paired_units(unit_means(INSTRUCTION_CONDITION), unit_means(other))
    return _comparison_record(compare_paired(units, level, bootstrap_rng()))


def _drift(conversation_slopes: Mapping[str, float], level: float, bootstrap_rng: BootstrapRng) -> dict[str, object]:
    """Return a condition's mean drift slope over conversations and its percentile bootstrap interval."""
    slopes = numpy.array(list(conversation_slopes.values()))
    resample_means = _bootstrap_resample_means(slopes, bootstrap_rng())
    return {"slope": float(slopes.mean()), "interval": list(_percentile_interval(resample_means, level))}


def _comparison_record(comparison: Comparison) -> dict[str, object]:
    """Return a comparison as `8-scores.yaml` stores it: mean difference, interval as a list or null, and unit count."""
    interval = None if comparison.interval is None else list(comparison.interval)
    return {"mean_difference": comparison.mean_difference, "interval": interval, "units": comparison.units}


def _conditions_of(rows: Sequence[ScoredReply]) -> list[str]:
    """Return the conditions the rows hold, in order of first appearance."""
    return list(dict.fromkeys(row[CONDITION_KEY] for row in rows))


def _condition_scores(rows: Sequence[ReplyRow], gate_demands: Sequence[str]) -> dict[str, object]:
    """Return one condition's mean breaches per reply over gate demands, mean breaches per demand, done rate, and kind counts."""
    return {
        "breaches_per_reply": fmean(breach_total(row, gate_demands) for row in rows),
        "demands": {demand: fmean(row["breaches"][demand] for row in rows) for demand in rows[0]["breaches"]},
        "done_rate": _done_rate(rows),
        "kinds": dict(Counter(row["kind"] for row in rows)),
    }


def _done_rate(rows: Sequence[ScoredReply]) -> float | None:
    """Return the share of rows done among those whose done is not null, null when every done is null."""
    present = [row["done"] for row in rows if row["done"] is not None]
    return fmean(present) if present else None
