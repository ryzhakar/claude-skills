"""Fixtures of a prepared r1 and of its reader transcripts and replies."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from series_fixtures import DISK_LOGIN_FILES, ONE_DEMAND, SERIES_BINDING, NeutralLogin, write_revision, write_yaml

from instruction_eval.reader import Transcript, reader_prepare, revision_collect
from instruction_eval.records import SeriesFolder, write_record

MODEL = "claude-sonnet-5-5"
SERIES = {"instruction": "/home/writer/terse.md", "sources": [], "reader_kind": "agent", "binding": SERIES_BINDING, "created": "2026-10-14T10:00:00+00:00"}
OPEN_MESSAGE = "Explain tides.\nBe brief.  \n"
SEALED_MESSAGE = "Explain rain."
TASKS = {
    "tasks": [
        {"id": "t-open", "tempts": "d-judge", "split": "open", "message": OPEN_MESSAGE, "answer_key": None},
        {"id": "t-sealed", "tempts": "d-judge", "split": "sealed", "message": SEALED_MESSAGE, "answer_key": None},
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


def prepared_series(tmp_path, tasks: dict = TASKS, reader: dict = READER, gate: dict = GATE) -> SeriesFolder:
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", {**SERIES, "reader_kind": reader["kind"]}, [])
    write_yaml(files, "2-demands.yaml", ONE_DEMAND)
    write_yaml(files, "3-tasks.yaml", tasks)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_yaml(files, "5-reader.yaml", reader)
    write_yaml(files, "7-gate.yaml", gate)
    write_revision(files, 1)
    home = tmp_path / "home"
    environ = NeutralLogin(home).environ() if reader["kind"] == "agent" else {}
    reader_prepare(files, "r1", {PLACEBO_PATH: b"Gardens bloom early\n"}.__getitem__, environ, home, files.root, DISK_LOGIN_FILES)
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


def prepare_reads() -> set[str]:
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


COMMAND_READER = {
    "kind": "command",
    "model": "gpt-5-mini",
    "command": ["llm-reply", "--system-file", "{condition}"],
    "fingerprint": ["llm-reply", "--version"],
    "sampling": {"temperature": 0.7},
}


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
