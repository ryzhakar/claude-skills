import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

from instruction_eval.reader import Transcript, reader_prepare, revision_collect
from instruction_eval.records import Refusal, SeriesFolder, write_file, write_record
from series_fixtures import write_revision
from test_reader_prepare import NeutralLogin

MODEL = "claude-sonnet-5-5"
SERIES = {"instruction": "/home/writer/terse.md", "sources": [], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}
DEMANDS = {"demands": [{"id": "d-one", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
OPEN_MESSAGE = "Explain tides.\nBe brief.  \n"
SEALED_MESSAGE = "Explain rain."
TASKS = {
    "tasks": [
        {"id": "t-open", "tempts": "d-one", "split": "open", "message": OPEN_MESSAGE, "answer_key": None},
        {"id": "t-sealed", "tempts": "d-one", "split": "sealed", "message": SEALED_MESSAGE, "answer_key": None},
    ],
    "conversations": [],
}
MESSAGES = {"t-open": OPEN_MESSAGE, "t-sealed": SEALED_MESSAGE}
PLACEBO_PATH = Path("/home/writer/gardening.md")
CONDITIONS = {"controls": ["empty", "aim", "placebo"], "aim": "Be terse.", "placebo_source": str(PLACEBO_PATH), "omissions": "none"}
CONDITION_NAMES = ("aim", "empty", "instruction", "placebo")
READER = {"kind": "agent", "model": MODEL}
GATE = {"repeats": 2}
USAGE = {"input_tokens": 5, "cache_creation_input_tokens": 2, "cache_read_input_tokens": 1, "output_tokens": 4}
START = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    write_file(files, path, yaml.safe_dump(document).encode())


def prepared_series(tmp_path, tasks: dict = TASKS, reader: dict = READER, gate: dict = GATE) -> SeriesFolder:
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", {**SERIES, "reader_kind": reader["kind"]}, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", tasks)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_yaml(files, "5-reader.yaml", reader)
    write_yaml(files, "7-gate.yaml", gate)
    write_revision(files, 1)
    home = tmp_path / "home"
    environ = NeutralLogin(home).environ() if reader["kind"] == "agent" else {}
    reader_prepare(files, "r1", {PLACEBO_PATH: b"Gardens bloom early\n"}.__getitem__, environ, home, files.root)
    return files


def stamp(moment: datetime) -> str:
    return moment.isoformat()


def transcript_text(turns: list[str], answers: list[str], start: datetime, model: str = MODEL) -> bytes:
    lines = []
    for number, (turn, answer) in enumerate(zip(turns, answers)):
        opened = start + timedelta(seconds=10 * number)
        wrapped = turn if number == 0 else f"The coordinator sent a message while you were working:\n{turn}\n\nAddress this before completing your current task."
        user = {"type": "user", "message": {"role": "user", "content": wrapped}, "timestamp": stamp(opened), **({"isMeta": True} if number else {})}
        assistant = {
            "type": "assistant",
            "message": {"model": model, "id": f"msg-{number}", "role": "assistant", "content": [{"type": "text", "text": answer}], "usage": USAGE},
            "timestamp": stamp(opened + timedelta(seconds=1)),
        }
        lines += [json.dumps(user), json.dumps(assistant)]
    return ("\n".join(lines) + "\n").encode()


def reader_transcript(tmp_path, name: str, condition: str, turns: list[str], answers: list[str], start: datetime, model: str = MODEL) -> Transcript:
    path = tmp_path / "transcripts" / f"{name}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(transcript_text(turns, answers, start, model))
    return Transcript(path=path, session="s", agent_id=name, agent_type=f"ie-reader-r1-{condition}")


def answer_of(condition: str, task: str, repeat: int) -> str:
    return f"answer {condition} {task} {repeat}"


def task_transcripts(tmp_path, conditions=CONDITION_NAMES, repeats=(1, 2)) -> list[Transcript]:
    """Build a transcript per condition, task, and repeat, repeat p starting p minutes after the hour."""
    return [
        reader_transcript(tmp_path, f"{condition}-{task}-{repeat}", condition, [MESSAGES[task]], [answer_of(condition, task, repeat)], START + timedelta(minutes=repeat))
        for condition in conditions
        for task in MESSAGES
        for repeat in repeats
    ]


def collect(files: SeriesFolder, transcripts: list[Transcript]) -> str:
    return revision_collect(files, "r1", transcripts, Path.read_bytes)


def load(files: SeriesFolder, path: str) -> dict:
    return yaml.safe_load(files.read_bytes(path))


def expected_reads() -> set[str]:
    return {
        "series.yaml",
        "3-tasks.yaml#tasks",
        "3-tasks.yaml#conversations",
        *(f"4-conditions.yaml#{key}" for key in ("controls", "aim", "placebo_source", "omissions")),
        "4-placebo-source.md",
        "5-reader.yaml#kind",
        "5-reader.yaml#model",
        "7-gate.yaml#repeats",
        "r1/2-instruction.md",
        *(f"r1/4-conditions/{condition}.md" for condition in CONDITION_NAMES),
        *(f".claude/agents/ie-reader-r1-{condition}.md" for condition in CONDITION_NAMES),
    }


def test_the_earliest_transcripts_of_each_condition_and_task_become_its_repeats_each_reply_recording_its_transcript(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)

    surplus = collect(files, list(reversed(transcripts)))

    assert surplus == ""
    first = next(transcript for transcript in transcripts if transcript.agent_id == "instruction-t-open-1")
    record = load(files, "r1/5-replies/instruction/t-open/repeat-1.yaml")
    inputs = record.pop("inputs")
    assert set(inputs) == expected_reads()
    assert record == {
        "condition": "instruction",
        "task": "t-open",
        "split": "open",
        "repeat": 1,
        "message": OPEN_MESSAGE,
        "text": "answer instruction t-open 1",
        "model": MODEL,
        "reader_kind": "agent",
        "started": stamp(START + timedelta(minutes=1)),
        "seconds": 1.0,
        "transcript": str(first.path),
        "transcript_hash": hashlib.sha256(first.path.read_bytes()).hexdigest(),
        "cost": {**USAGE, "spent_input_tokens": 8},
    }
    assert load(files, "r1/5-replies/placebo/t-sealed/repeat-2.yaml")["text"] == "answer placebo t-sealed 2"


def test_transcripts_beyond_the_repeats_are_listed_and_ignored(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    late = reader_transcript(tmp_path, "late", "instruction", [OPEN_MESSAGE], ["a late answer"], START + timedelta(minutes=3))

    surplus = collect(files, [*transcripts, late])

    assert surplus == f"ignored surplus transcript: {late.path}\n"
    assert not files.holds("r1/5-replies/instruction/t-open/repeat-3.yaml")
    assert load(files, "r1/5-replies/instruction/t-open/repeat-2.yaml")["text"] == "answer instruction t-open 2"


def test_a_gap_refuses_after_writing_the_replies_it_could_match_and_a_rerun_fills_only_the_gap(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    withheld = [transcript for transcript in transcripts if transcript.agent_id in ("aim-t-open-2", "aim-t-sealed-1", "aim-t-sealed-2")]
    present = [transcript for transcript in transcripts if transcript not in withheld]
    late = reader_transcript(tmp_path, "late", "instruction", [OPEN_MESSAGE], ["a late answer"], START + timedelta(minutes=3))

    with pytest.raises(Refusal) as refused:
        collect(files, [*present, late])

    assert str(refused.value) == f"missing replies: 3, first r1/5-replies/aim/t-open/repeat-2.yaml\nignored surplus transcript: {late.path}"

    assert load(files, "r1/5-replies/aim/t-open/repeat-1.yaml")["text"] == "answer aim t-open 1"
    written = files.read_bytes("r1/5-replies/aim/t-open/repeat-1.yaml")
    assert collect(files, transcripts) == ""
    assert files.read_bytes("r1/5-replies/aim/t-open/repeat-1.yaml") == written
    assert load(files, "r1/5-replies/aim/t-sealed/repeat-2.yaml")["text"] == "answer aim t-sealed 2"


TRIP_TURNS = ["Plan a trip.", "Which week?"]
CONVERSATION_TASKS = {**TASKS, "conversations": [{"id": "c-open", "split": "open", "turns": TRIP_TURNS}]}


def conversation_transcripts(tmp_path) -> list[Transcript]:
    return [
        reader_transcript(
            tmp_path, f"{condition}-c-open-{repeat}", condition, TRIP_TURNS, [f"first {condition} {repeat}", f"second {condition} {repeat}"], START + timedelta(minutes=repeat)
        )
        for condition in CONDITION_NAMES
        for repeat in (1, 2)
    ]


def test_each_turn_of_a_conversation_transcript_becomes_a_reply_of_its_repeat(tmp_path):
    files = prepared_series(tmp_path, CONVERSATION_TASKS)

    collect(files, [*task_transcripts(tmp_path), *conversation_transcripts(tmp_path)])

    second = load(files, "r1/5-replies/placebo/c-open/repeat-2/turn-2.yaml")
    second.pop("inputs")
    assert second["text"] == "second placebo 2"
    assert second["turn"] == 2
    assert second["message"] == "Which week?"
    assert second["split"] == "open"
    assert second["started"] == stamp(START + timedelta(minutes=2, seconds=10))
    assert load(files, "r1/5-replies/instruction/c-open/repeat-1/turn-1.yaml")["message"] == "Plan a trip."


def test_a_transcript_served_by_another_model_refuses_before_any_reply_is_written(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    served_elsewhere = reader_transcript(tmp_path, "other", "aim", [OPEN_MESSAGE], ["x"], START + timedelta(minutes=9), model="claude-other-1")
    transcripts = [served_elsewhere if transcript.agent_id == "aim-t-open-1" else transcript for transcript in transcripts]

    with pytest.raises(Refusal, match=r"claude-other-1 is not the pinned claude-sonnet-5-5"):
        collect(files, transcripts)

    assert not (files.root / "r1/5-replies").exists()


def test_a_transcript_of_another_agent_type_or_opening_with_another_message_is_no_reply(tmp_path):
    files = prepared_series(tmp_path)
    transcripts = task_transcripts(tmp_path)
    judge = Transcript(path=tmp_path / "transcripts/judge.jsonl", session="s", agent_id="judge", agent_type="ie-judge-r1-t-open-k1")
    stray = reader_transcript(tmp_path, "stray", "aim", ["Explain snow."], ["x"], START)

    assert collect(files, [judge, stray, *transcripts]) == ""


COMMAND_READER = {
    "kind": "command",
    "model": "gpt-5-mini",
    "command": ["llm-reply", "--system-file", "{condition}"],
    "fingerprint": ["llm-reply", "--version"],
    "sampling": {"temperature": 0.7},
}


def tree(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))


def write_command_replies(files: SeriesFolder, conditions=CONDITION_NAMES) -> None:
    for condition in conditions:
        for task, message in MESSAGES.items():
            for repeat in (1, 2):
                reply = {
                    "condition": condition,
                    "task": task,
                    "split": "open" if task == "t-open" else "sealed",
                    "repeat": repeat,
                    "message": message,
                    "text": "a reply",
                    "model": "gpt-5-mini",
                    "reader_kind": "command",
                    "started": stamp(START),
                    "seconds": 1.0,
                    "fingerprint_hash": "a" * 64,
                    "cost": dict.fromkeys(("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "spent_input_tokens")),
                }
                write_record(files, f"r1/5-replies/{condition}/{task}/repeat-{repeat}.yaml", reply, [])


def test_a_command_reader_collects_nothing_and_refuses_a_gap_whatever_transcripts_exist(tmp_path):
    files = prepared_series(tmp_path, reader=COMMAND_READER)
    write_command_replies(files, conditions=("empty", "instruction", "placebo"))
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^missing replies: 4, first r1/5-replies/aim/t-open/repeat-1\.yaml$"):
        collect(files, task_transcripts(tmp_path))

    assert tree(files.root) == before


def test_a_command_reader_with_every_reply_written_collects_cleanly_without_writing(tmp_path):
    files = prepared_series(tmp_path, reader=COMMAND_READER)
    write_command_replies(files)
    before = tree(files.root)

    assert collect(files, []) == ""
    assert tree(files.root) == before


@pytest.mark.parametrize("edited", ["r1/4-conditions/aim.md", ".claude/agents/ie-reader-r1-aim.md"])
def test_an_edited_condition_text_or_reader_definition_refuses_before_any_reply_is_written(tmp_path, edited):
    files = prepared_series(tmp_path)
    (files.root / edited).write_bytes(b"edited")

    with pytest.raises(Refusal, match=rf"^{edited.replace('.', r'[.]')} differs from its recomputation$"):
        collect(files, task_transcripts(tmp_path))

    assert not (files.root / "r1/5-replies").exists()
