import pytest

from instruction_eval.gate import (
    BudgetRefusal,
    ReplyCost,
    SeriesShape,
    refuse_unaffordable_ask,
    refuse_unaffordable_freeze,
)
from instruction_eval.records import Budget

SHAPE = SeriesShape(
    task_count=3, open_task_count=1, conversation_turns=2, repeats=2, omission_sentences=3,
)
TWO_SECOND_R1_REPLIES = [ReplyCost(None, None, 2.0)] * 10
PREDICTED_COST = 148.0
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


def test_freeze_refuses_a_budget_when_r1_has_no_replies():
    with pytest.raises(BudgetRefusal, match="r1 has no replies"):
        refuse_unaffordable_freeze(Budget("seconds", 100.0), [], SHAPE)


def test_ask_refuses_a_budget_when_r1_has_no_replies():
    with pytest.raises(BudgetRefusal, match="r1 has no replies"):
        refuse_unaffordable_ask(Budget("seconds", 100.0), [], 0.0, 5)


def test_ask_accepts_a_series_with_no_budget():
    refuse_unaffordable_ask(None, TWO_SECOND_R1_REPLIES, 20.0, 5)


def test_ask_refuses_a_token_budget_when_any_r1_reply_has_null_tokens():
    r1_replies = [ReplyCost(10, 5, 2.0), ReplyCost(None, None, 2.0)]
    with pytest.raises(BudgetRefusal, match="null tokens"):
        refuse_unaffordable_ask(Budget("tokens", 1_000_000), r1_replies, 0.0, 5)


def test_freeze_accepts_a_ceiling_at_the_predicted_cost():
    refuse_unaffordable_freeze(Budget("seconds", PREDICTED_COST), TWO_SECOND_R1_REPLIES, SHAPE)


def test_freeze_accepts_a_series_with_no_budget():
    refuse_unaffordable_freeze(None, TWO_SECOND_R1_REPLIES, SHAPE)


def test_freeze_refuses_a_token_budget_when_any_r1_reply_has_null_tokens():
    r1_replies = [ReplyCost(10, 5, 2.0), ReplyCost(None, None, 2.0)]
    with pytest.raises(BudgetRefusal, match="null tokens"):
        refuse_unaffordable_freeze(Budget("tokens", 1_000_000), r1_replies, SHAPE)


def test_freeze_predicts_a_token_budget_from_input_plus_output_tokens():
    r1_replies = [ReplyCost(1, 1, 0.0)] * 10
    refuse_unaffordable_freeze(Budget("tokens", PREDICTED_COST), r1_replies, SHAPE)
    with pytest.raises(BudgetRefusal):
        refuse_unaffordable_freeze(Budget("tokens", PREDICTED_COST - 1), r1_replies, SHAPE)


def test_freeze_refuses_a_ceiling_below_the_predicted_cost():
    with pytest.raises(BudgetRefusal, match="predicted cost 148"):
        refuse_unaffordable_freeze(
            Budget("seconds", PREDICTED_COST - 1), TWO_SECOND_R1_REPLIES, SHAPE,
        )
