from instruction_eval.tasks import shared_phrases, words


def test_words_are_lowercased_alphanumeric_and_apostrophe_runs():
    assert words("Don't STOP-now, 42 times!") == ["don't", "stop", "now", "42", "times"]
