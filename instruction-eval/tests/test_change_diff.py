import pytest

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
