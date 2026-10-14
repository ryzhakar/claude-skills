from instruction_eval.gate import ReplyCost, sum_revision_cost


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
