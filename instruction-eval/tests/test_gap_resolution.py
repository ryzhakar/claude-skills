import math

import numpy
import pytest
from hypothesis import given
from hypothesis import strategies as st

from instruction_eval.gate import least_repeats, refuse_unresolvable_gaps, series_least_repeats
from instruction_eval.records import GateCheck, Refusal
from instruction_eval.scores import Noise, ScoredReply

REQUIRED_HALF_WIDTHS = {"instruction-vs-empty": 0.1, "instruction-vs-aim": 0.1, "instruction-vs-placebo": 0.1, "completion": 0.1}
REQUIRED_GAPS = {"instruction-vs-empty": 1.0, "instruction-vs-aim": 1.0, "instruction-vs-placebo": 1.0, "completion": 1.0}


def noise(checks: dict[str, float | None], repeats: int = 2, demands: dict | None = None, done_change: float | None = 0.1) -> Noise:
    """Build r1's noise holding the given check half-widths."""
    sigma = {"breaches": {}, "done": {}, "drift": {}, "demands": {}}
    return {
        "repeats": repeats,
        "level": 0.95,
        "z": 1.96,
        "sigma": sigma,
        "checks": checks,
        "demands": {"d": 0.1} if demands is None else demands,
        "done_change": done_change,
    }


def gate_checks(gaps: dict[str, float]) -> list[GateCheck]:
    """Build the gate checks of the given gaps."""
    return [GateCheck(compares, gap) for compares, gap in gaps.items()]


def rng() -> numpy.random.Generator:
    """Return the seeded random source handed to the admission comparison."""
    return numpy.random.default_rng(20261012)


def refuse(gaps: dict[str, float], half_widths: dict[str, float | None], rows: list[ScoredReply] = (), sources: bool = False, **noise_keys) -> None:
    """Run the refusal over the gate checks and noise built from the given values."""
    refuse_unresolvable_gaps(gate_checks(gaps), noise(half_widths, **noise_keys), list(rows), ["d"], sources, rng())


def test_a_gap_narrower_than_twice_its_noise_refuses_naming_the_check_and_the_least_repeats():
    with pytest.raises(Refusal, match=r"^unresolvable gap: instruction-vs-aim \(noise 0\.6 > gap / 2 0\.5\); least repeats 3$"):
        refuse(REQUIRED_GAPS, {**REQUIRED_HALF_WIDTHS, "instruction-vs-aim": 0.6})


def test_several_unresolvable_gaps_refuse_naming_each_check_and_the_least_repeats_resolving_every_check():
    half_widths = {**REQUIRED_HALF_WIDTHS, "instruction-vs-aim": 0.6, "completion": 0.85}
    expected = r"^unresolvable gap: instruction-vs-aim \(noise 0\.6 > gap / 2 0\.5\), completion \(noise 0\.85 > gap / 2 0\.5\); least repeats 6$"
    with pytest.raises(Refusal, match=expected):
        refuse(REQUIRED_GAPS, half_widths)


def test_the_series_least_repeats_is_the_most_any_check_needs_and_null_when_a_check_has_no_noise():
    half_widths = {**REQUIRED_HALF_WIDTHS, "instruction-vs-aim": 0.6, "completion": 0.85}

    assert series_least_repeats(gate_checks(REQUIRED_GAPS), noise(half_widths)) == 6
    assert series_least_repeats(gate_checks({**REQUIRED_GAPS, "drift": 1.0}), noise(half_widths)) is None


def test_a_gap_exactly_twice_its_noise_resolves():
    refuse(REQUIRED_GAPS, {**REQUIRED_HALF_WIDTHS, "instruction-vs-aim": 0.5})


def test_a_check_whose_noise_is_null_refuses_naming_the_check():
    with pytest.raises(Refusal, match=r"^null noise: completion$"):
        refuse(REQUIRED_GAPS, {**REQUIRED_HALF_WIDTHS, "completion": None})


def test_a_drift_check_absent_from_the_noise_refuses_as_null():
    with pytest.raises(Refusal, match=r"^null noise: drift$"):
        refuse({**REQUIRED_GAPS, "drift": 1.0}, REQUIRED_HALF_WIDTHS)


def test_a_null_change_noise_of_a_gate_demand_refuses_naming_the_demand():
    with pytest.raises(Refusal, match=r"^null noise: demands\.d$"):
        refuse(REQUIRED_GAPS, REQUIRED_HALF_WIDTHS, demands={"d": None})


def test_a_null_done_change_noise_refuses():
    with pytest.raises(Refusal, match=r"^null noise: done_change$"):
        refuse(REQUIRED_GAPS, REQUIRED_HALF_WIDTHS, done_change=None)


def resolves_at(repeats: int, half_width: float, measured_repeats: int, gap: float) -> bool:
    """Tell whether the half-width measured at some repeats, scaled to other repeats, is at most half the gap."""
    return half_width * math.sqrt(measured_repeats / repeats) <= gap / 2


@given(
    measured_repeats=st.integers(min_value=2, max_value=20),
    half_width=st.floats(min_value=0, max_value=50, allow_nan=False),
    gap=st.floats(min_value=0.01, max_value=50, allow_nan=False),
)
def test_the_least_repeats_is_the_fewest_at_least_two_resolving_the_gap_and_exceeds_the_measured_repeats_exactly_when_the_gap_refuses(
    measured_repeats, half_width, gap
):
    check = GateCheck("instruction-vs-empty", gap)
    measured = noise({**REQUIRED_HALF_WIDTHS, "instruction-vs-empty": half_width}, repeats=measured_repeats)

    least = least_repeats(check, measured)

    assert least >= 2
    assert resolves_at(least, half_width, measured_repeats, gap)
    assert least == 2 or not resolves_at(least - 1, half_width, measured_repeats, gap)
    refused = not resolves_at(measured_repeats, half_width, measured_repeats, gap)
    assert (least > measured_repeats) == refused


def test_the_least_repeats_of_a_check_without_noise_is_null():
    assert least_repeats(GateCheck("drift", 1.0), noise(REQUIRED_HALF_WIDTHS)) is None


NEAR_SOURCE_GAPS = {**REQUIRED_GAPS, "instruction-near-source": 1.0}
NEAR_SOURCE_HALF_WIDTHS = {**REQUIRED_HALF_WIDTHS, "instruction-near-source": 0.1}


def sealed_reply(condition: str, task: str, repeat: int, gate_breaches: int, dropped_breaches: int = 0) -> ScoredReply:
    """Build one sealed r1 single-task reply breaching gate demand `d` and dropped demand `x`."""
    return {"condition": condition, "task": task, "repeat": repeat, "turn": None, "breaches": {"d": gate_breaches, "x": dropped_breaches}, "done": True}


def source_and_empty_rows(source_breaches: int, empty_breaches: int, dropped_source_breaches: int = 0) -> list[ScoredReply]:
    """Build two tasks of two repeats each under `source` and `empty`, every reply of a condition breaching alike."""
    return [
        reply
        for task in ("t1", "t2")
        for repeat in (1, 2)
        for reply in (
            sealed_reply("source", task, repeat, source_breaches, dropped_source_breaches),
            sealed_reply("empty", task, repeat, empty_breaches),
        )
    ]


def test_an_instruction_near_source_check_in_a_series_without_sources_refuses():
    with pytest.raises(Refusal, match=r"^instruction-near-source refused: the series has no sources$"):
        refuse(NEAR_SOURCE_GAPS, NEAR_SOURCE_HALF_WIDTHS, source_and_empty_rows(0, 2), sources=False)


def test_an_instruction_near_source_check_is_admitted_when_source_undercuts_empty_by_the_instruction_vs_empty_gap():
    refuse(NEAR_SOURCE_GAPS, NEAR_SOURCE_HALF_WIDTHS, source_and_empty_rows(1, 2, dropped_source_breaches=5), sources=True)


def test_an_instruction_near_source_check_refuses_when_source_undercuts_empty_by_less_than_the_instruction_vs_empty_gap():
    gaps = {**NEAR_SOURCE_GAPS, "instruction-vs-empty": 1.5}
    with pytest.raises(Refusal, match=r"^instruction-near-source refused: source minus empty misses the instruction-vs-empty gap on r1's sealed rows$"):
        refuse(gaps, NEAR_SOURCE_HALF_WIDTHS, source_and_empty_rows(1, 2), sources=True)
