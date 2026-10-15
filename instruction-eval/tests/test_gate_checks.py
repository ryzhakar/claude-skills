from instruction_eval.gate import check_passes
from instruction_eval.records import GateCheck
from instruction_eval.scores import Comparison

GAP = 0.5
UNITS = 4


def compared(mean_difference: float, low: float, high: float) -> Comparison:
    """Build a comparison over a few units with the given mean and interval."""
    return Comparison(mean_difference=mean_difference, interval=(low, high), units=UNITS)


def test_vs_check_passes_at_a_mean_of_minus_gap_with_the_interval_below_zero():
    check = GateCheck(compares="instruction-vs-empty", gap=GAP)

    assert check_passes(check, compared(-0.5, -0.75, -0.25))
    assert not check_passes(check, compared(-0.25, -0.75, -0.125))
    assert not check_passes(check, compared(-0.5, -1.0, 0.0))


def test_near_source_check_passes_while_the_upper_bound_stays_within_the_gap():
    check = GateCheck(compares="instruction-near-source", gap=GAP)

    assert check_passes(check, compared(0.25, 0.0, 0.5))
    assert not check_passes(check, compared(0.25, 0.0, 0.625))


def test_drift_check_passes_while_the_upper_bound_stays_within_the_gap():
    check = GateCheck(compares="drift", gap=GAP)

    assert check_passes(check, compared(0.25, 0.0, 0.5))
    assert not check_passes(check, compared(0.25, 0.0, 0.625))


def test_completion_check_passes_while_the_lower_bound_stays_at_or_above_minus_gap():
    check = GateCheck(compares="completion", gap=GAP)

    assert check_passes(check, compared(-0.25, -0.5, 0.0))
    assert not check_passes(check, compared(-0.25, -0.625, 0.0))


def test_a_check_over_no_units_fails():
    check = GateCheck(compares="completion", gap=GAP)

    assert not check_passes(check, Comparison(mean_difference=None, interval=None, units=0))
