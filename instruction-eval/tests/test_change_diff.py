import pytest
from hypothesis import given, strategies as st

from instruction_eval.revision import Change, change_holds

PARENT = ["a", "b", "c"]


def test_rewrite_holds_when_only_the_named_sentence_differs():
    assert change_holds(PARENT, ["a", "B", "c"], Change("rewrite", 2))


def test_rewrite_names_the_first_sentence_as_one():
    assert change_holds(PARENT, ["A", "b", "c"], Change("rewrite", 1))


def test_rewrite_names_the_last_sentence_by_its_count():
    assert change_holds(PARENT, ["a", "b", "C"], Change("rewrite", 3))


def test_rewrite_refuses_sentence_number_zero():
    assert not change_holds(PARENT, ["A", "b", "c"], Change("rewrite", 0))


def test_rewrite_refuses_another_sentence_changed():
    assert not change_holds(PARENT, ["A", "B", "c"], Change("rewrite", 2))


def test_rewrite_refuses_the_named_sentence_unchanged():
    assert not change_holds(PARENT, PARENT, Change("rewrite", 2))


def test_rewrite_refuses_a_different_length():
    assert not change_holds(PARENT, ["a", "B"], Change("rewrite", 2))


def test_add_holds_when_removing_the_named_child_sentence_leaves_the_parent():
    assert change_holds(PARENT, ["a", "x", "b", "c"], Change("add", 2))


def test_add_refuses_the_wrong_sentence_named():
    assert not change_holds(PARENT, ["a", "x", "b", "c"], Change("add", 3))


def test_add_refuses_sentence_number_zero():
    assert not change_holds(PARENT, ["x", "a", "b", "c"], Change("add", 0))


def test_add_refuses_a_number_outside_the_child():
    assert not change_holds(PARENT, ["a", "b", "c", "x"], Change("add", 5))


def test_delete_holds_when_removing_the_named_parent_sentence_leaves_the_child():
    assert change_holds(PARENT, ["a", "c"], Change("delete", 2))


def test_delete_refuses_the_wrong_sentence_named():
    assert not change_holds(PARENT, ["a", "c"], Change("delete", 1))


def test_delete_refuses_sentence_number_zero():
    assert not change_holds(PARENT, ["b", "c"], Change("delete", 0))


def test_delete_refuses_a_number_outside_the_parent():
    assert not change_holds(PARENT, ["a", "b"], Change("delete", 4))


def test_move_holds_when_the_sentence_lands_at_the_destination():
    assert change_holds(PARENT, ["b", "c", "a"], Change("move", 1, 3))


def test_move_refuses_the_same_source_and_destination():
    assert not change_holds(PARENT, PARENT, Change("move", 2, 2))


def test_move_refuses_a_wrong_destination():
    assert not change_holds(PARENT, ["b", "c", "a"], Change("move", 1, 2))


def test_move_refuses_destination_number_zero():
    assert not change_holds(PARENT, ["b", "c", "a"], Change("move", 1, 0))


def test_a_move_without_a_destination_cannot_be_constructed():
    with pytest.raises(ValueError, match="move needs a destination"):
        Change("move", 1)


@pytest.mark.parametrize("action", ["rewrite", "add", "delete"])
def test_a_non_move_with_a_destination_cannot_be_constructed(action):
    with pytest.raises(ValueError, match="only move takes a destination"):
        Change(action, 1, 5)


def test_adjacent_swap_holds_named_as_moving_the_first_sentence_later():
    assert change_holds(["a", "b"], ["b", "a"], Change("move", 1, 2))


def test_adjacent_swap_holds_named_as_moving_the_second_sentence_earlier():
    assert change_holds(["a", "b"], ["b", "a"], Change("move", 2, 1))


sentence_lists = st.lists(st.text(max_size=4), min_size=1, max_size=6)
sentences = st.text(max_size=4)


def numbers_in(items: list[str], extra: int = 0):
    return st.integers(min_value=1, max_value=len(items) + extra)


def with_removed(items: list[str], number: int) -> list[str]:
    return items[: number - 1] + items[number:]


def with_inserted(items: list[str], number: int, sentence: str) -> list[str]:
    return items[: number - 1] + [sentence] + items[number - 1 :]


@st.composite
def distinct_number_pairs(draw):
    parent = draw(st.lists(st.text(max_size=4), min_size=2, max_size=6))
    source = draw(numbers_in(parent))
    destination = draw(numbers_in(parent).filter(lambda n: n != source))
    return parent, source, destination


@given(st.data())
def test_rewriting_to_a_different_sentence_holds(data):
    parent = data.draw(sentence_lists)
    number = data.draw(numbers_in(parent))
    replacement = data.draw(sentences.filter(lambda text: text != parent[number - 1]))
    child = parent[: number - 1] + [replacement] + parent[number:]
    assert change_holds(parent, child, Change("rewrite", number))


@given(st.data())
def test_rewriting_to_an_equal_sentence_never_holds(data):
    parent = data.draw(sentence_lists)
    number = data.draw(numbers_in(parent))
    assert not change_holds(parent, list(parent), Change("rewrite", number))


@given(st.data())
def test_adding_a_sentence_holds(data):
    parent = data.draw(st.lists(sentences, max_size=6))
    number = data.draw(numbers_in(parent, extra=1))
    child = with_inserted(parent, number, data.draw(sentences))
    assert change_holds(parent, child, Change("add", number))


@given(st.data())
def test_deleting_a_sentence_holds(data):
    parent = data.draw(sentence_lists)
    number = data.draw(numbers_in(parent))
    assert change_holds(parent, with_removed(parent, number), Change("delete", number))


@given(st.data())
def test_a_delete_is_undone_by_an_add_at_the_same_number(data):
    parent = data.draw(sentence_lists)
    number = data.draw(numbers_in(parent))
    child = with_removed(parent, number)
    assert change_holds(child, parent, Change("add", number))


@given(distinct_number_pairs())
def test_a_move_holds_and_is_undone_by_the_reverse_move(case):
    parent, source, destination = case
    child = with_inserted(with_removed(parent, source), destination, parent[source - 1])
    assert change_holds(parent, child, Change("move", source, destination))
    assert change_holds(child, parent, Change("move", destination, source))
