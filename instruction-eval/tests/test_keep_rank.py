from instruction_eval.gate import kept_revision
from series_fixtures import outcome




def test_a_breach_tie_keeps_the_fewer_words_then_the_lower_number():
    outcomes = {
        "r1": outcome(False, True, 0.5, 40),
        "r2": outcome(False, True, 0.25, 30),
        "r3": outcome(False, True, 0.25, 20),
        "r4": outcome(False, True, 0.25, 20),
    }

    assert kept_revision(outcomes) == "r3"


def test_a_passing_revision_is_kept_over_fewer_breaches():
    outcomes = {"r1": outcome(False, True, 0.0, 10), "r2": outcome(True, True, 0.5, 40)}

    assert kept_revision(outcomes) == "r2"


def test_a_revision_failing_completion_is_no_candidate():
    outcomes = {"r1": outcome(False, True, 0.5, 40), "r2": outcome(False, False, 0.0, 10)}

    assert kept_revision(outcomes) == "r1"


def test_no_candidate_keeps_nothing():
    outcomes = {"r1": outcome(False, False, 0.5, 40), "r2": outcome(False, False, 0.0, 10)}

    assert kept_revision(outcomes) is None
