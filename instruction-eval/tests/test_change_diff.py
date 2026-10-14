from instruction_eval.revision import Change, change_holds

PARENT = ["a", "b", "c"]


def test_rewrite_holds_when_only_the_named_sentence_differs():
    assert change_holds(PARENT, ["a", "B", "c"], Change("rewrite", 1))


def test_rewrite_refuses_another_sentence_changed():
    assert not change_holds(PARENT, ["A", "B", "c"], Change("rewrite", 1))


def test_rewrite_refuses_the_named_sentence_unchanged():
    assert not change_holds(PARENT, PARENT, Change("rewrite", 1))


def test_rewrite_refuses_a_different_length():
    assert not change_holds(PARENT, ["a", "B"], Change("rewrite", 1))


def test_add_holds_when_removing_the_named_child_sentence_leaves_the_parent():
    assert change_holds(PARENT, ["a", "x", "b", "c"], Change("add", 1))


def test_add_refuses_the_wrong_sentence_named():
    assert not change_holds(PARENT, ["a", "x", "b", "c"], Change("add", 2))


def test_add_refuses_an_index_outside_the_child():
    assert not change_holds(PARENT, ["a", "b", "c", "x"], Change("add", 4))


def test_delete_holds_when_removing_the_named_parent_sentence_leaves_the_child():
    assert change_holds(PARENT, ["a", "c"], Change("delete", 1))


def test_delete_refuses_the_wrong_sentence_named():
    assert not change_holds(PARENT, ["a", "c"], Change("delete", 0))


def test_delete_refuses_an_index_outside_the_parent():
    assert not change_holds(PARENT, ["a", "b"], Change("delete", 3))


def test_move_holds_when_the_sentence_lands_at_the_destination():
    assert change_holds(PARENT, ["b", "c", "a"], Change("move", 0, 2))


def test_move_refuses_the_same_source_and_destination():
    assert not change_holds(PARENT, PARENT, Change("move", 1, 1))


def test_move_refuses_a_wrong_destination():
    assert not change_holds(PARENT, ["b", "c", "a"], Change("move", 0, 1))


def test_move_refuses_a_missing_destination():
    assert not change_holds(PARENT, ["b", "c", "a"], Change("move", 0))


def test_adjacent_swap_holds_named_as_moving_the_first_sentence_later():
    assert change_holds(["a", "b"], ["b", "a"], Change("move", 0, 1))


def test_adjacent_swap_holds_named_as_moving_the_second_sentence_earlier():
    assert change_holds(["a", "b"], ["b", "a"], Change("move", 1, 0))
