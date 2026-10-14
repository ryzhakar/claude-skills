import pytest

from instruction_eval.gate import (
    Budget,
    BudgetRefusal,
    ReplyCost,
    SeriesShape,
    refuse_unaffordable_freeze,
    sum_revision_cost,
)

SHAPE = SeriesShape(
    task_count=3, open_task_count=1, conversation_turns=2, repeats=2, omission_sentences=3,
)
TWO_SECOND_R1_REPLIES = [ReplyCost(None, None, 2.0)] * 10
PREDICTED_SECONDS = 148.0


def test_freeze_accepts_a_ceiling_at_the_predicted_cost():
    refuse_unaffordable_freeze(Budget("seconds", PREDICTED_SECONDS), TWO_SECOND_R1_REPLIES, SHAPE)


def test_freeze_refuses_a_ceiling_below_the_predicted_cost():
    with pytest.raises(BudgetRefusal, match="predicted cost 148"):
        refuse_unaffordable_freeze(
            Budget("seconds", PREDICTED_SECONDS - 1), TWO_SECOND_R1_REPLIES, SHAPE,
        )


def test_revision_cost_sums_replies_tokens_and_seconds():
    replies = [ReplyCost(10, 5, 2.0), ReplyCost(20, 15, 3.0)]
    assert sum_revision_cost(replies) == {
        "replies": 2, "input_tokens": 30, "output_tokens": 20, "seconds": 5.0,
    }


def test_revision_cost_token_sums_are_null_when_any_reply_has_null_tokens():
    replies = [ReplyCost(10, 5, 2.0), ReplyCost(None, None, 3.0)]
    assert sum_revision_cost(replies) == {
        "replies": 2, "input_tokens": None, "output_tokens": None, "seconds": 5.0,
    }
