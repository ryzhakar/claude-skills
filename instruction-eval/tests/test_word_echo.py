from instruction_eval.tasks import shared_phrases, words


def test_words_are_lowercased_alphanumeric_and_apostrophe_runs():
    assert words("Don't STOP-now, 42 times!") == ["don't", "stop", "now", "42", "times"]


def test_shared_phrases_names_each_shared_three_word_sequence_ignoring_case_and_punctuation():
    text = "Always, ALWAYS cite the source first."
    other = "You must always cite the source."
    assert shared_phrases(text, other) == ["always cite the", "cite the source"]


def test_shared_phrases_is_empty_when_two_words_only_are_shared():
    assert shared_phrases("cite the source", "cite the record") == []


def test_shared_phrases_is_empty_for_texts_under_three_words():
    assert shared_phrases("cite the", "cite the") == []


def test_shared_phrases_lists_a_repeated_sequence_once():
    assert shared_phrases("a b c a b c", "x a b c") == ["a b c"]
