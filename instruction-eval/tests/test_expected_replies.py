from pathlib import Path

import pytest

from instruction_eval.records import Conditions, Conversation, Refusal, SeriesFolder, Task, Tasks, write_file
from instruction_eval.tasks import expected_replies, refuse_missing_replies

TASKS = Tasks(
    tasks=(
        Task(id="t-open", tempts="d-one", split="open", message="Explain tides.", answer_key=None),
        Task(id="t-sealed", tempts="d-one", split="sealed", message="Explain rain.", answer_key=None),
    ),
    conversations=(Conversation(id="c-open", split="open", turns=("Plan a trip.", "Which week?")),),
)


def conditions(omissions: str) -> Conditions:
    return Conditions(controls=("empty", "aim"), aim="Be terse.", placebo_source=Path("/tmp/placebo.md"), omissions=omissions)


def paths(revision: str, condition: str) -> list[str]:
    folder = f"{revision}/5-replies/{condition}"
    return [
        *(f"{folder}/t-open/repeat-{repeat}.yaml" for repeat in (1, 2)),
        *(f"{folder}/t-sealed/repeat-{repeat}.yaml" for repeat in (1, 2)),
        *(f"{folder}/c-open/repeat-{repeat}/turn-{turn}.yaml" for repeat in (1, 2) for turn in (1, 2)),
    ]


def test_r1_expects_every_task_and_conversation_turn_per_repeat_for_the_instruction_and_each_control():
    expected = expected_replies("r1", TASKS, conditions("none"), repeats=2, sentence_count=3)
    assert [reply.path for reply in expected] == sorted(paths("r1", "instruction") + paths("r1", "empty") + paths("r1", "aim"))


def open_task_paths(revision: str, condition: str) -> list[str]:
    return [f"{revision}/5-replies/{condition}/t-open/repeat-{repeat}.yaml" for repeat in (1, 2)]


def test_every_sentence_omissions_add_one_condition_per_sentence_asked_on_open_tasks_only():
    expected = expected_replies("r1", TASKS, conditions("every-sentence"), repeats=2, sentence_count=2)
    omissions = open_task_paths("r1", "omit-1") + open_task_paths("r1", "omit-2")
    assert [reply.path for reply in expected] == sorted(paths("r1", "instruction") + paths("r1", "empty") + paths("r1", "aim") + omissions)


def test_a_later_revision_expects_its_own_instruction_and_omissions_and_borrows_control_replies_from_r1():
    expected = expected_replies("r2", TASKS, conditions("every-sentence"), repeats=2, sentence_count=1)
    own = paths("r2", "instruction") + open_task_paths("r2", "omit-1")
    assert [reply.path for reply in expected] == sorted(own + paths("r1", "empty") + paths("r1", "aim"))


def write_replies(files: SeriesFolder, reply_paths: list[str]) -> None:
    for path in reply_paths:
        write_file(files, path, b"reply")


def test_a_revision_asked_for_a_subset_of_conditions_refuses_counting_the_gap_and_naming_its_first_path(tmp_path):
    files = SeriesFolder(tmp_path)
    write_replies(files, paths("r1", "instruction"))
    expected = expected_replies("r1", TASKS, conditions("none"), repeats=2, sentence_count=3)
    with pytest.raises(Refusal, match=r"^missing replies: 16, first r1/5-replies/aim/c-open/repeat-1/turn-1\.yaml$"):
        refuse_missing_replies(files, expected)


def test_a_revision_holding_every_expected_reply_passes_the_gap_check(tmp_path):
    files = SeriesFolder(tmp_path)
    write_replies(files, paths("r2", "instruction") + paths("r1", "empty") + paths("r1", "aim"))
    refuse_missing_replies(files, expected_replies("r2", TASKS, conditions("none"), repeats=2, sentence_count=3))
