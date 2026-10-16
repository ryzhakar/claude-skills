from instruction_eval.gate import stop_after
from instruction_eval.records import Budget

CEILING = 100.0
TOKEN_BUDGET = Budget("tokens", CEILING)


def outcome(passed: bool = False, changed: str | None = None, completion_passed: bool = True, breaches: float = 1.0, words: int = 10) -> dict:
    """Build one gated revision's outcome, `changed_from_parent` absent when null."""
    record = {"outcome": "pass" if passed else "fail", "instruction_breaches": breaches, "completion_passed": completion_passed, "words": words}
    if changed is not None:
        record["changed_from_parent"] = changed
    return record


def test_a_passing_revision_stops_the_series_as_passed_keeping_the_passing_one():
    outcomes = {"r1": outcome(breaches=0.0, words=1), "r2": outcome(passed=True, changed="changed")}

    assert stop_after("r2", outcomes, None, 0.0) == {"stop": "passed", "kept": "r2"}


def test_two_unchanged_revisions_in_a_row_stop_the_series_as_no_effect():
    outcomes = {"r2": outcome(changed="unchanged"), "r3": outcome(changed="unchanged", breaches=0.5)}

    assert stop_after("r3", outcomes, None, 0.0) == {"stop": "no-effect", "kept": "r3"}


def test_an_unchanged_revision_after_a_changed_parent_goes_on():
    outcomes = {"r2": outcome(changed="changed"), "r3": outcome(changed="unchanged")}

    assert stop_after("r3", outcomes, None, 0.0) is None


def test_an_unchanged_second_revision_goes_on_as_the_first_has_no_comparison():
    outcomes = {"r1": outcome(), "r2": outcome(changed="unchanged")}

    assert stop_after("r2", outcomes, None, 0.0) is None


def test_the_fifth_revision_failing_caps_the_series_without_a_reason_keeping_the_fewest_breaches():
    outcomes = {"r1": outcome(breaches=0.5), "r4": outcome(breaches=0.25), "r5": outcome(breaches=0.75)}

    assert stop_after("r5", outcomes, None, 0.0) == {"stop": "capped", "kept": "r4"}


def test_a_fourth_revision_failing_goes_on():
    assert stop_after("r4", {"r4": outcome()}, None, 0.0) is None


def test_cost_reaching_the_ceiling_caps_the_series_with_the_budget_reason():
    outcomes = {"r1": outcome(), "r2": outcome(changed="changed")}

    assert stop_after("r2", outcomes, TOKEN_BUDGET, CEILING) == {"stop": "capped", "reason": "budget", "kept": "r1"}


def test_cost_below_the_ceiling_goes_on():
    assert stop_after("r2", {"r2": outcome()}, TOKEN_BUDGET, CEILING - 1) is None


def test_cost_over_any_ceiling_goes_on_without_a_budget():
    assert stop_after("r2", {"r2": outcome()}, None, CEILING * 10) is None


def test_passing_wins_over_no_effect_and_a_cap():
    outcomes = {"r4": outcome(changed="unchanged"), "r5": outcome(passed=True, changed="unchanged")}

    assert stop_after("r5", outcomes, TOKEN_BUDGET, CEILING)["stop"] == "passed"


def test_no_effect_wins_over_a_cap():
    outcomes = {"r4": outcome(changed="unchanged"), "r5": outcome(changed="unchanged")}

    assert stop_after("r5", outcomes, TOKEN_BUDGET, CEILING)["stop"] == "no-effect"


def test_a_cap_at_the_fifth_revision_wins_over_the_budget_reason():
    assert stop_after("r5", {"r5": outcome()}, TOKEN_BUDGET, CEILING) == {"stop": "capped", "kept": "r5"}


def test_no_revision_passing_completion_keeps_nothing():
    assert stop_after("r5", {"r5": outcome(completion_passed=False)}, None, 0.0) == {"stop": "capped", "kept": None}
