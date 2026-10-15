import pytest

from instruction_eval.records import Hypothesis, MoveChange, PredictedMovement, Refusal
from instruction_eval.revision import refuse_unfit_hypothesis
from instruction_eval.scores import ReplyRow

NOISE = {"demands": {"d-judge": 0.25, "d-pattern": 0.25}, "done_change": 0.25}
CLEARING_SIZE = 0.6


def row(blind_id: str, breaches: dict[str, int] | None = None, done: bool | None = True) -> ReplyRow:
    """Build one open reply row of the parent."""
    return {
        "id": blind_id,
        "condition": "instruction",
        "task": "t1",
        "repeat": 1,
        "turn": None,
        "borrowed_from": None,
        "breaches": breaches or {"d-judge": 1, "d-pattern": 1},
        "kind": "answer",
        "done_by_answer_key": None,
        "done_by_judge": done,
        "done": done,
    }


def hypothesis(failing_demand: str = "d-judge", replies_read: tuple[str, ...] = ("b00000001",), size: float = CLEARING_SIZE) -> Hypothesis:
    """Build a hypothesis moving a sentence and predicting a drop of `size`."""
    return Hypothesis(failing_demand, replies_read, MoveChange(sentence=2, to=1), PredictedMovement("down", size))


def test_a_reply_that_is_no_open_reply_of_the_parent_is_refused():
    open_rows = [row("b00000001")]

    with pytest.raises(Refusal, match="b00000002"):
        refuse_unfit_hypothesis(hypothesis(replies_read=("b00000001", "b00000002")), open_rows, NOISE)


def test_a_demand_with_zero_breaches_across_the_replies_read_is_refused():
    open_rows = [row("b00000001", {"d-judge": 0, "d-pattern": 3}), row("b00000002", {"d-judge": 4, "d-pattern": 0})]

    with pytest.raises(Refusal, match="d-judge"):
        refuse_unfit_hypothesis(hypothesis(), open_rows, NOISE)


def test_a_demand_breached_by_any_reply_read_is_accepted():
    open_rows = [row("b00000001", {"d-judge": 0, "d-pattern": 0}), row("b00000002", {"d-judge": 1, "d-pattern": 0})]

    refuse_unfit_hypothesis(hypothesis(replies_read=("b00000001", "b00000002")), open_rows, NOISE)


def test_a_detector_demand_is_read_from_the_row_breaches_like_a_judge_demand():
    open_rows = [row("b00000001", {"d-judge": 5, "d-pattern": 0})]

    with pytest.raises(Refusal, match="d-pattern"):
        refuse_unfit_hypothesis(hypothesis(failing_demand="d-pattern"), open_rows, NOISE)


def test_completion_with_no_reply_read_holding_done_false_is_refused():
    open_rows = [row("b00000001", done=True), row("b00000002", done=None)]

    with pytest.raises(Refusal, match="completion"):
        refuse_unfit_hypothesis(hypothesis("completion", ("b00000001", "b00000002")), open_rows, NOISE)


def test_completion_with_a_reply_read_holding_done_false_is_accepted():
    open_rows = [row("b00000001", done=True), row("b00000002", done=False)]

    refuse_unfit_hypothesis(hypothesis("completion", ("b00000001", "b00000002")), open_rows, NOISE)


def test_a_predicted_size_of_twice_the_demands_change_noise_is_refused():
    open_rows = [row("b00000001")]

    with pytest.raises(Refusal, match="0.5"):
        refuse_unfit_hypothesis(hypothesis(size=0.5), open_rows, NOISE)


def test_a_predicted_size_above_twice_the_demands_change_noise_is_accepted():
    refuse_unfit_hypothesis(hypothesis(size=0.51), [row("b00000001")], NOISE)


def test_completion_is_held_to_twice_the_done_change_noise():
    open_rows = [row("b00000001", done=False)]
    noise = {"demands": {}, "done_change": 0.4}

    with pytest.raises(Refusal, match="0.8"):
        refuse_unfit_hypothesis(hypothesis("completion", size=0.8), open_rows, noise)
    refuse_unfit_hypothesis(hypothesis("completion", size=0.81), open_rows, noise)
