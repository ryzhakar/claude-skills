import pytest
import yaml

from instruction_eval.records import Refusal, SeriesFolder, write_record
from instruction_eval.tasks import tasks_check

DEMANDS = [{"id": "d-a", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]
INSTRUCTION = "Be terse. Never pad answers with filler.\n"
AIM = "Answer in few words."
PLACEBO = "Gardens need patient watering through summer.\n"
TASKS = [
    {"id": "tide-open", "tempts": "d-a", "split": "open", "message": "Why does the sea rise twice daily?", "answer_key": None},
    {"id": "tide-sealed", "tempts": "d-a", "split": "sealed", "message": "What pulls the ocean toward the moon?", "answer_key": None},
    {"id": "loop-open", "tempts": "overreach", "split": "open", "message": "My loop prints one number too many. Fix only that.", "answer_key": r"range\(n\)"},
    {"id": "loop-sealed", "tempts": "overreach", "split": "sealed", "message": "This counter starts at two. Make it start at one.", "answer_key": r"= 1"},
]
CONTROLS = ["empty", "aim", "placebo"]
CONVERSATIONS = [
    {"id": "trip-open", "split": "open", "turns": ["I want to visit Lisbon in spring.", "Which week has the fewest crowds?"]},
    {"id": "trip-open-two", "split": "open", "turns": ["Cheese or sausage tonight?", "Would a salad suit either?"]},
    {"id": "trip-sealed", "split": "sealed", "turns": ["My bicycle chain keeps slipping.", "Could the sprocket be worn?"]},
    {"id": "trip-sealed-two", "split": "sealed", "turns": ["Tomatoes split before ripening.", "Is uneven watering responsible?"]},
]


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    target = files.root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(document))


def tasks_series(
    tmp_path,
    tasks: list[dict] = TASKS,
    conversations: list[dict] | None = None,
    aim: str = AIM,
    instructions: tuple[str, ...] = (INSTRUCTION,),
    placebo: str | bytes | None = PLACEBO,
    placebo_snapshot: str | None = None,
    source_files: dict[str, str] | None = None,
) -> SeriesFolder:
    root = tmp_path / "series"
    root.mkdir()
    files = SeriesFolder(root)
    external_placebo = tmp_path / "placebo.md"
    if placebo is not None:
        external_placebo.write_bytes(placebo if isinstance(placebo, bytes) else placebo.encode())
    sources = source_files or {}
    series = {"instruction": "/home/writer/terse.md", "sources": [f"/home/writer/{name}" for name in sources], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}
    write_record(files, "series.yaml", series, [])
    write_yaml(files, "2-demands.yaml", {"demands": DEMANDS})
    write_yaml(files, "3-tasks.yaml", {"tasks": tasks, "conversations": conversations or []})
    controls = [*CONTROLS, "source"] if sources else CONTROLS
    write_yaml(files, "4-conditions.yaml", {"controls": controls, "aim": aim, "placebo_source": str(external_placebo), "omissions": "every-sentence"})
    for number, instruction in enumerate(instructions, 1):
        (root / f"r{number}").mkdir()
        (root / f"r{number}/2-instruction.md").write_text(instruction)
    for name, text in sources.items():
        (root / "1-source").mkdir(exist_ok=True)
        (root / f"1-source/{name}").write_text(text)
    if placebo_snapshot is not None:
        (root / "4-placebo-source.md").write_text(placebo_snapshot)
    return files


def test_a_task_set_covering_every_demand_and_overreach_in_both_halves_passes(tmp_path):
    files = tasks_series(tmp_path)

    assert tasks_check(files) is None


@pytest.mark.parametrize(
    "dropped_task, target, half",
    [("tide-sealed", "d-a", "sealed"), ("tide-open", "d-a", "open"), ("loop-open", "overreach", "open"), ("loop-sealed", "overreach", "sealed")],
)
def test_a_demand_or_overreach_absent_from_either_half_refuses_naming_the_target_and_half(tmp_path, dropped_task, target, half):
    files = tasks_series(tmp_path, tasks=[task for task in TASKS if task["id"] != dropped_task])

    with pytest.raises(Refusal, match=rf"^no {half} task tempts {target} \(3-tasks\.yaml\)$"):
        tasks_check(files)


def test_an_overreach_task_without_an_answer_key_refuses_naming_it(tmp_path):
    tasks = [{**task, "answer_key": None} if task["id"] == "loop-sealed" else task for task in TASKS]
    files = tasks_series(tmp_path, tasks=tasks)

    with pytest.raises(Refusal, match=r"^overreach task without answer_key: loop-sealed \(3-tasks\.yaml\)$"):
        tasks_check(files)


def test_an_answer_key_that_fails_to_compile_refuses_as_a_malformed_record(tmp_path):
    tasks = [{**task, "answer_key": "range("} if task["id"] == "tide-open" else task for task in TASKS]
    files = tasks_series(tmp_path, tasks=tasks)

    with pytest.raises(Refusal, match=r"^malformed record: 3-tasks\.yaml \(tasks\[0\]\.answer_key"):
        tasks_check(files)


def test_conversations_two_per_half_of_two_turns_each_pass(tmp_path):
    files = tasks_series(tmp_path, conversations=CONVERSATIONS)

    assert tasks_check(files) is None


@pytest.mark.parametrize(
    "dropped_conversation, half, count",
    [("trip-sealed-two", "sealed", 1), ("trip-open-two", "open", 1)],
)
def test_a_half_holding_one_conversation_refuses_naming_the_half(tmp_path, dropped_conversation, half, count):
    conversations = [conversation for conversation in CONVERSATIONS if conversation["id"] != dropped_conversation]
    files = tasks_series(tmp_path, conversations=conversations)

    with pytest.raises(Refusal, match=rf"^{half} half holds fewer than two conversations: {count} \(3-tasks\.yaml\)$"):
        tasks_check(files)


def test_a_half_holding_no_conversation_while_the_other_holds_some_refuses(tmp_path):
    conversations = [conversation for conversation in CONVERSATIONS if conversation["split"] == "open"]
    files = tasks_series(tmp_path, conversations=conversations)

    with pytest.raises(Refusal, match=r"^sealed half holds fewer than two conversations: 0 \(3-tasks\.yaml\)$"):
        tasks_check(files)


def test_a_one_turn_conversation_refuses_naming_it(tmp_path):
    conversations = [{**conversation, "turns": conversation["turns"][:1]} if conversation["id"] == "trip-sealed" else conversation for conversation in CONVERSATIONS]
    files = tasks_series(tmp_path, conversations=conversations)

    with pytest.raises(Refusal, match=r"^conversation trip-sealed holds fewer than two turns \(3-tasks\.yaml\)$"):
        tasks_check(files)


def renamed(task_id: str, new_id: str) -> list[dict]:
    return [{**task, "id": new_id} if task["id"] == task_id else task for task in TASKS]


@pytest.mark.parametrize(
    "tasks, conversations",
    [
        (renamed("tide-sealed", "tide-open"), None),
        (renamed("tide-sealed", "trip-open"), CONVERSATIONS),
    ],
    ids=["two-tasks", "task-and-conversation"],
)
def test_an_id_two_entries_hold_refuses_naming_it(tmp_path, tasks, conversations):
    files = tasks_series(tmp_path, tasks=tasks, conversations=conversations)

    with pytest.raises(Refusal, match=r"^duplicate id: (tide-open|trip-open) \(3-tasks\.yaml\)$"):
        tasks_check(files)


@pytest.mark.parametrize(
    "new_id, message",
    [("tide--open", r'^id holds "--": tide--open \(3-tasks\.yaml\)$'), ("tide-open-turn-2", r"^id ends in -turn-<digits>: tide-open-turn-2 \(3-tasks\.yaml\)$")],
)
def test_an_id_the_reply_paths_cannot_carry_refuses_naming_it(tmp_path, new_id, message):
    files = tasks_series(tmp_path, tasks=renamed("tide-open", new_id))

    with pytest.raises(Refusal, match=message):
        tasks_check(files)


def test_two_tasks_sharing_a_message_refuse_naming_both(tmp_path):
    tasks = [{**task, "message": TASKS[0]["message"]} if task["id"] == "tide-sealed" else task for task in TASKS]
    files = tasks_series(tmp_path, tasks=tasks)

    with pytest.raises(Refusal, match=r"^shared message: tide-open and tide-sealed \(3-tasks\.yaml\)$"):
        tasks_check(files)


def test_a_task_sharing_a_message_with_a_conversations_first_turn_refuses_naming_both(tmp_path):
    tasks = [{**task, "message": CONVERSATIONS[0]["turns"][0]} if task["id"] == "tide-open" else task for task in TASKS]
    files = tasks_series(tmp_path, tasks=tasks, conversations=CONVERSATIONS)

    with pytest.raises(Refusal, match=r"^shared message: tide-open and trip-open \(3-tasks\.yaml\)$"):
        tasks_check(files)


def test_a_task_sharing_a_message_with_a_later_turn_passes(tmp_path):
    tasks = [{**task, "message": CONVERSATIONS[0]["turns"][1]} if task["id"] == "tide-open" else task for task in TASKS]
    files = tasks_series(tmp_path, tasks=tasks, conversations=CONVERSATIONS)

    assert tasks_check(files) is None


def with_message(task_id: str, message: str) -> list[dict]:
    return [{**task, "message": message} if task["id"] == task_id else task for task in TASKS]


@pytest.mark.parametrize(
    "tasks, conversations, aim, instructions, refusal",
    [
        (with_message("tide-open", "Explain tides but never pad answers please."), None, AIM, (INSTRUCTION,), r"^task tide-open echoes r1/2-instruction\.md: never pad answers$"),
        (with_message("tide-open", "Why cut every wasted morsel of text?"), None, AIM, (INSTRUCTION, "Cut every wasted word.\n"), r"^task tide-open echoes r2/2-instruction\.md: cut every wasted$"),
        (TASKS, [{**CONVERSATIONS[0], "turns": ["I want to visit Lisbon.", "Will you answer in few days?"]}, *CONVERSATIONS[1:]], AIM, (INSTRUCTION,), r"^conversation trip-open turn 2 echoes aim: answer in few$"),
        (with_message("tide-sealed", "Do gardens need patient care?"), None, AIM, (INSTRUCTION,), r"^task tide-sealed echoes .*placebo\.md: gardens need patient$"),
        (TASKS, None, "Never pad answers, always.", (INSTRUCTION,), r"^aim echoes r1/2-instruction\.md: never pad answers$"),
    ],
    ids=["task-echoes-instruction", "task-echoes-later-revision", "turn-echoes-aim", "task-echoes-placebo", "aim-echoes-instruction"],
)
def test_an_echo_of_a_three_word_sequence_refuses_naming_the_text_and_the_phrase(tmp_path, tasks, conversations, aim, instructions, refusal):
    files = tasks_series(tmp_path, tasks=tasks, conversations=conversations, aim=aim, instructions=instructions)

    with pytest.raises(Refusal, match=refusal):
        tasks_check(files)


def test_a_placebo_source_sharing_a_three_word_sequence_with_a_source_file_refuses_naming_the_file_and_the_phrase(tmp_path):
    files = tasks_series(tmp_path, source_files={"guide.md": "Gardens need patient hands always.\n"})

    with pytest.raises(Refusal, match=r"^placebo source echoes 1-source/guide\.md: gardens need patient$"):
        tasks_check(files)


def test_a_source_file_sharing_no_sequence_with_the_placebo_source_passes(tmp_path):
    files = tasks_series(tmp_path, source_files={"guide.md": "Cite every claim.\n"})

    assert tasks_check(files) is None


def test_a_missing_placebo_source_refuses_naming_the_path(tmp_path):
    files = tasks_series(tmp_path, placebo=None)

    with pytest.raises(Refusal, match=rf"^missing placebo source: {tmp_path}/placebo\.md$"):
        tasks_check(files)


@pytest.mark.parametrize("placebo", ["", "-- !! ..\n"], ids=["empty", "punctuation-only"])
def test_a_placebo_source_holding_no_word_refuses_naming_the_path(tmp_path, placebo):
    files = tasks_series(tmp_path, placebo=placebo)

    with pytest.raises(Refusal, match=rf"^placebo source holds no word: {tmp_path}/placebo\.md$"):
        tasks_check(files)


def test_a_placebo_source_that_is_not_utf_8_refuses_naming_the_path(tmp_path):
    files = tasks_series(tmp_path, placebo=b"\xff\xfe")

    with pytest.raises(Refusal, match=rf"^not UTF-8: {tmp_path}/placebo\.md$"):
        tasks_check(files)


def test_the_series_snapshot_of_the_placebo_source_stands_in_for_the_external_file(tmp_path):
    files = tasks_series(tmp_path, placebo=None, placebo_snapshot=PLACEBO)

    assert tasks_check(files) is None


def test_an_echo_of_the_snapshot_refuses_naming_the_snapshot(tmp_path):
    files = tasks_series(tmp_path, tasks=with_message("tide-sealed", "Do gardens need patient care?"), placebo=None, placebo_snapshot=PLACEBO)

    with pytest.raises(Refusal, match=r"^task tide-sealed echoes 4-placebo-source\.md: gardens need patient$"):
        tasks_check(files)


def test_two_conversations_sharing_a_first_turn_pass(tmp_path):
    conversations = [{**conversation, "turns": [CONVERSATIONS[0]["turns"][0], *conversation["turns"][1:]]} if conversation["id"] == "trip-open-two" else conversation for conversation in CONVERSATIONS]
    files = tasks_series(tmp_path, conversations=conversations)

    assert tasks_check(files) is None
