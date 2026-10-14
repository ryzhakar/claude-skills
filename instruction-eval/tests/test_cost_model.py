import pytest

from instruction_eval.gate import (
    Budget,
    BudgetRefusal,
    ReplyCost,
    SeriesShape,
    refuse_unaffordable_ask,
    refuse_unaffordable_freeze,
    sum_revision_cost,
)

SHAPE = SeriesShape(
    task_count=3, open_task_count=1, conversation_turns=2, repeats=2, omission_sentences=3,
)
TWO_SECOND_R1_REPLIES = [ReplyCost(None, None, 2.0)] * 10
PREDICTED_SECONDS = 148.0
COST_SO_FAR_PLUS_FIVE_REPLIES = 30.0


def test_ask_accepts_cost_so_far_plus_its_replies_at_the_ceiling():
    refuse_unaffordable_ask(
        Budget("seconds", COST_SO_FAR_PLUS_FIVE_REPLIES), TWO_SECOND_R1_REPLIES, 20.0, 5,
    )


def test_ask_refuses_cost_so_far_plus_its_replies_above_the_ceiling():
    with pytest.raises(BudgetRefusal, match="30"):
        refuse_unaffordable_ask(
            Budget("seconds", COST_SO_FAR_PLUS_FIVE_REPLIES - 1), TWO_SECOND_R1_REPLIES, 20.0, 5,
        )


def test_ask_accepts_a_series_with_no_budget():
    refuse_unaffordable_ask(None, TWO_SECOND_R1_REPLIES, 20.0, 5)


def test_ask_refuses_a_token_budget_when_any_r1_reply_has_null_tokens():
    r1_replies = [ReplyCost(10, 5, 2.0), ReplyCost(None, None, 2.0)]
    with pytest.raises(BudgetRefusal, match="null tokens"):
        refuse_unaffordable_ask(Budget("tokens", 1_000_000), r1_replies, 0.0, 5)


def test_freeze_accepts_a_ceiling_at_the_predicted_cost():
    refuse_unaffordable_freeze(Budget("seconds", PREDICTED_SECONDS), TWO_SECOND_R1_REPLIES, SHAPE)


def test_freeze_accepts_a_series_with_no_budget():
    refuse_unaffordable_freeze(None, TWO_SECOND_R1_REPLIES, SHAPE)


def test_freeze_refuses_a_token_budget_when_any_r1_reply_has_null_tokens():
    r1_replies = [ReplyCost(10, 5, 2.0), ReplyCost(None, None, 2.0)]
    with pytest.raises(BudgetRefusal, match="null tokens"):
        refuse_unaffordable_freeze(Budget("tokens", 1_000_000), r1_replies, SHAPE)


def test_freeze_predicts_a_token_budget_from_input_plus_output_tokens():
    r1_replies = [ReplyCost(1, 1, 0.0)] * 10
    refuse_unaffordable_freeze(Budget("tokens", PREDICTED_SECONDS), r1_replies, SHAPE)
    with pytest.raises(BudgetRefusal):
        refuse_unaffordable_freeze(Budget("tokens", PREDICTED_SECONDS - 1), r1_replies, SHAPE)


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
