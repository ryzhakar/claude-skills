import pytest
import yaml

from instruction_eval.reader import agent_launch_list
from instruction_eval.records import Refusal, SeriesFolder, write_file, write_record
from series_fixtures import write_revision

TIDES_MESSAGE = "Explain tides.\nBe brief.  \n"
TRIP_TURNS = ["Plan a trip.", "Which week?", "Thanks."]
SERIES = {"instruction": "/home/writer/terse.md", "sources": [], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}
DEMANDS = {"demands": [{"id": "d-one", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
TASKS = {
    "tasks": [
        {"id": "t-open", "tempts": "d-one", "split": "open", "message": TIDES_MESSAGE, "answer_key": None},
        {"id": "t-sealed", "tempts": "d-one", "split": "sealed", "message": "Explain rain.", "answer_key": None},
    ],
    "conversations": [{"id": "c-open", "split": "open", "turns": TRIP_TURNS}],
}
CONDITIONS = {"controls": ["empty", "aim", "placebo"], "aim": "Be terse.", "placebo_source": "/home/writer/gardening.md", "omissions": "none"}
READER = {"kind": "agent", "model": "claude-sonnet-5-5"}
GATE = {"repeats": 2}


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    write_file(files, path, yaml.safe_dump(document).encode())


def agent_series(tmp_path, gate: dict = GATE, conditions: dict = CONDITIONS) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", SERIES, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "4-conditions.yaml", conditions)
    write_yaml(files, "5-reader.yaml", READER)
    write_yaml(files, "7-gate.yaml", gate)
    write_revision(files, 1)
    return files


def conversation_launch(condition: str, repeat: int, revision: str = "r1") -> dict:
    return {
        "agent_type": f"ie-reader-{revision}-{condition}",
        "condition": condition,
        "conversation": "c-open",
        "repeat": repeat,
        "message": TRIP_TURNS[0],
        "send_messages": TRIP_TURNS[1:],
    }


def task_launch(condition: str, task: str, message: str, repeat: int, revision: str = "r1") -> dict:
    return {
        "agent_type": f"ie-reader-{revision}-{condition}",
        "condition": condition,
        "task": task,
        "repeat": repeat,
        "message": message,
    }


def launches(files: SeriesFolder, revision: str, conditions: list[str]) -> list[dict]:
    return yaml.safe_load(agent_launch_list(files, revision, conditions))["launches"]


def test_each_task_and_conversation_repeat_lists_its_agent_type_and_exact_messages_in_path_order(tmp_path):
    files = agent_series(tmp_path)

    assert launches(files, "r1", ["instruction"]) == [
        conversation_launch("instruction", 1),
        conversation_launch("instruction", 2),
        task_launch("instruction", "t-open", TIDES_MESSAGE, 1),
        task_launch("instruction", "t-open", TIDES_MESSAGE, 2),
        task_launch("instruction", "t-sealed", "Explain rain.", 1),
        task_launch("instruction", "t-sealed", "Explain rain.", 2),
    ]


def write_reply(files: SeriesFolder, path: str) -> None:
    write_file(files, path, b"reply")


def test_no_named_condition_lists_every_condition_of_the_revision(tmp_path):
    files = agent_series(tmp_path)

    agent_types = [launch["agent_type"] for launch in launches(files, "r1", [])]

    assert sorted(set(agent_types)) == [f"ie-reader-r1-{name}" for name in ("aim", "empty", "instruction", "placebo")]
    assert len(agent_types) == 4 * 2 * 3


def test_a_later_revision_launches_its_own_instruction_and_any_control_reply_r1_lacks_under_the_r1_agent(tmp_path):
    files = agent_series(tmp_path)
    write_revision(files, 2)
    for control in ("aim", "empty"):
        for task in ("t-open", "t-sealed"):
            for repeat in (1, 2):
                write_reply(files, f"r1/5-replies/{control}/{task}/repeat-{repeat}.yaml")
        for repeat in (1, 2):
            for turn in (1, 2, 3):
                write_reply(files, f"r1/5-replies/{control}/c-open/repeat-{repeat}/turn-{turn}.yaml")
    for task in ("t-open", "t-sealed"):
        for repeat in (1, 2):
            write_reply(files, f"r1/5-replies/placebo/{task}/repeat-{repeat}.yaml")
    write_reply(files, "r1/5-replies/placebo/c-open/repeat-1/turn-1.yaml")
    write_reply(files, "r1/5-replies/placebo/c-open/repeat-1/turn-2.yaml")
    write_reply(files, "r1/5-replies/placebo/c-open/repeat-1/turn-3.yaml")

    assert [(launch["agent_type"], launch["repeat"]) for launch in launches(files, "r2", [])] == [
        ("ie-reader-r1-placebo", 2),
        ("ie-reader-r2-instruction", 1),
        ("ie-reader-r2-instruction", 2),
        ("ie-reader-r2-instruction", 1),
        ("ie-reader-r2-instruction", 2),
        ("ie-reader-r2-instruction", 1),
        ("ie-reader-r2-instruction", 2),
    ]


def test_omission_conditions_launch_open_tasks_only(tmp_path):
    files = agent_series(tmp_path, conditions={**CONDITIONS, "omissions": "every-sentence"})

    assert launches(files, "r1", ["omit-1"]) == [
        task_launch("omit-1", "t-open", TIDES_MESSAGE, 1),
        task_launch("omit-1", "t-open", TIDES_MESSAGE, 2),
    ]


def test_repeats_the_gate_has_not_written_refuse(tmp_path):
    files = agent_series(tmp_path, gate={})

    with pytest.raises(Refusal, match=r"^missing key: 7-gate\.yaml#repeats$"):
        agent_launch_list(files, "r1", [])


def test_a_folder_that_is_no_series_refuses(tmp_path):
    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        agent_launch_list(SeriesFolder(tmp_path), "r1", [])


def test_a_reply_already_collected_leaves_its_launch_out_and_a_conversation_missing_a_turn_stays_whole(tmp_path):
    files = agent_series(tmp_path)
    write_reply(files, "r1/5-replies/instruction/t-open/repeat-1.yaml")
    write_reply(files, "r1/5-replies/instruction/c-open/repeat-1/turn-1.yaml")
    write_reply(files, "r1/5-replies/instruction/c-open/repeat-2/turn-1.yaml")
    write_reply(files, "r1/5-replies/instruction/c-open/repeat-2/turn-2.yaml")
    write_reply(files, "r1/5-replies/instruction/c-open/repeat-2/turn-3.yaml")

    assert launches(files, "r1", ["instruction"]) == [
        conversation_launch("instruction", 1),
        task_launch("instruction", "t-open", TIDES_MESSAGE, 2),
        task_launch("instruction", "t-sealed", "Explain rain.", 1),
        task_launch("instruction", "t-sealed", "Explain rain.", 2),
    ]
