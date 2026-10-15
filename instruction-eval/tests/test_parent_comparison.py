import numpy

from instruction_eval.gate import compare_with_parent
from instruction_eval.scores import ScoredReply

LEVEL = 0.95
SEED = 7
SIZE = 0.5


def reply(task: str, breaches: int, repeat: int = 1, done: bool | None = None, condition: str = "instruction") -> ScoredReply:
    """Build one sealed single-task reply holding the given breaches of demand `d`."""
    return {"condition": condition, "task": task, "repeat": repeat, "turn": None, "breaches": {"d": breaches}, "done": done}


def rng() -> numpy.random.Generator:
    """Return the seeded random source handed to the comparison."""
    return numpy.random.default_rng(SEED)


def test_a_demand_whose_breaches_fell_wholly_below_zero_changed_as_predicted_down():
    revision = [reply("t1", 0), reply("t2", 1)]
    parent = [reply("t1", 2), reply("t2", 3)]

    result = compare_with_parent(revision, parent, "d", "down", SIZE, LEVEL, rng())

    assert result.changed_from_parent == "changed"
    assert result.target == "d"
    assert result.comparison.mean_difference == -2.0
    assert result.comparison.interval == (-2.0, -2.0)


def test_a_demand_whose_breaches_rose_wholly_above_zero_reversed_against_a_predicted_down():
    revision = [reply("t1", 3), reply("t2", 4)]
    parent = [reply("t1", 1), reply("t2", 1)]

    result = compare_with_parent(revision, parent, "d", "down", SIZE, LEVEL, rng())

    assert result.changed_from_parent == "reversed"


def test_an_interval_holding_zero_inside_the_predicted_size_is_unchanged():
    revision = [reply("t1", 2), reply("t2", 2)]
    parent = [reply("t1", 2), reply("t2", 2)]

    result = compare_with_parent(revision, parent, "d", "down", SIZE, LEVEL, rng())

    assert result.changed_from_parent == "unchanged"


def test_an_interval_holding_zero_as_wide_as_the_predicted_size_is_unresolved():
    revision = [reply("t1", 3), reply("t2", 1)]
    parent = [reply("t1", 2), reply("t2", 2)]

    result = compare_with_parent(revision, parent, "d", "down", 1.0, LEVEL, rng())

    assert result.comparison.interval == (-1.0, 1.0)
    assert result.changed_from_parent == "unresolved"


def test_breaches_rising_wholly_above_zero_changed_as_predicted_up():
    revision = [reply("t1", 3), reply("t2", 4)]
    parent = [reply("t1", 1), reply("t2", 1)]

    assert compare_with_parent(revision, parent, "d", "up", SIZE, LEVEL, rng()).changed_from_parent == "changed"


def test_breaches_falling_wholly_below_zero_reversed_against_a_predicted_up():
    revision = [reply("t1", 0), reply("t2", 1)]
    parent = [reply("t1", 2), reply("t2", 3)]

    assert compare_with_parent(revision, parent, "d", "up", SIZE, LEVEL, rng()).changed_from_parent == "reversed"


def test_completion_compares_the_done_rate_per_task_over_repeats():
    revision = [reply("t1", 0, 1, True), reply("t1", 0, 2, True), reply("t2", 0, 1, True), reply("t2", 0, 2, False)]
    parent = [reply("t1", 0, 1, False), reply("t1", 0, 2, False), reply("t2", 0, 1, True), reply("t2", 0, 2, False)]

    result = compare_with_parent(revision, parent, "completion", "up", SIZE, LEVEL, rng())

    assert result.target == "completion"
    assert result.comparison.mean_difference == 0.5
    assert result.comparison.units == 2


def test_replies_of_other_conditions_and_conversation_turns_are_left_out():
    revision = [reply("t1", 0), reply("t1", 9, condition="empty"), {**reply("c1", 9), "turn": 1}]
    parent = [reply("t1", 2), reply("t1", 0, condition="empty"), {**reply("c1", 0), "turn": 1}]

    result = compare_with_parent(revision, parent, "d", "down", SIZE, LEVEL, rng())

    assert result.comparison.units == 1
    assert result.comparison.mean_difference == -2.0


def test_no_shared_task_leaves_the_comparison_unresolved():
    result = compare_with_parent([reply("t1", 0)], [reply("t2", 0)], "d", "down", SIZE, LEVEL, rng())

    assert result.comparison.interval is None
    assert result.changed_from_parent == "unresolved"
