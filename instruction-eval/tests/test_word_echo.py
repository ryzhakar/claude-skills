from hypothesis import given, strategies as st

from instruction_eval.tasks import SEQUENCE_LENGTH, shared_phrases, words

ASCII_LAST_CODEPOINT = 127
PHRASE_VOCABULARY = ["cite", "the", "source", "always", "first"]
MOST_PHRASE_WORDS = 12


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


@given(st.text(alphabet=st.characters(max_codepoint=ASCII_LAST_CODEPOINT)))
def test_words_are_lowercase_and_unchanged_by_lowercasing_the_text(text):
    found = words(text)
    assert all(word == word.lower() for word in found)
    assert words(text.lower()) == found


@given(st.lists(st.sampled_from(PHRASE_VOCABULARY), min_size=SEQUENCE_LENGTH, max_size=MOST_PHRASE_WORDS))
def test_a_text_shares_each_of_its_own_three_word_runs_with_itself_once_in_order(word_list):
    runs = dict.fromkeys(" ".join(word_list[start:start + SEQUENCE_LENGTH]) for start in range(len(word_list) - SEQUENCE_LENGTH + 1))
    assert shared_phrases(" ".join(word_list), " ".join(word_list)) == list(runs)
