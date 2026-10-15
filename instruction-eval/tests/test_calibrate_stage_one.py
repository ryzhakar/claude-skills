import json
import random
from pathlib import Path

import pytest
import yaml

import instruction_eval
from instruction_eval.judge import calibrate_stage_one
from instruction_eval.reader import NeutralLoginRefused
from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, reply_path, write_file, write_record
from series_fixtures import sha256, tree, write_yaml

TEMPLATE = Path(instruction_eval.__file__).parent / "templates" / "judge-brief.md"
REQUIRED_PLUGINS = {"instruction-eval@my-claude-skills": True, "manifesto@my-claude-skills": True}
JUDGE_MODEL = "claude-opus-4-1"
RATER_MODEL = "claude-sonnet-5-5"
READER_MODEL = "claude-haiku-4-5"
SOURCE_NAME = "policy.md"
SOURCE_TEXT = "Be terse.\n"
SERIES = {"instruction": "/home/writer/terse.md", "sources": [f"/home/writer/{SOURCE_NAME}"], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-plain", "text": "Use plain words.", "boundary": "Names are exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
COVERAGE = {"demands": {"d-judge": [1], "d-plain": [1], "d-hedge": {"dropped": "Unmeasured here."}}, "sentences": {1: ["d-judge", "d-plain"]}}
CONDITIONS = ("aim", "empty", "instruction", "placebo", "source")
OPEN_TASKS = ("t1", "t2")
SEALED_TASKS = ("t3",)
ACCEPTANCE = {"breach_difference": 0.5, "self_difference": 0.5, "done_agreement": 0.8}
AGENT_PLAN = {"judge_model": JUDGE_MODEL, "raters": ["agent", "agent"], "rater_model": RATER_MODEL, "sample_size": 6, "anchors_per_packet": 3, "acceptance": ACCEPTANCE}
USER_PLAN = {"judge_model": JUDGE_MODEL, "raters": ["user"], "sample_size": 6, "anchors_per_packet": 3, "acceptance": ACCEPTANCE}
COST = {"input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 1, "spent_input_tokens": 1}
CALIBRATION = {
    "attempt": 1,
    "judge_model": JUDGE_MODEL,
    "raters": ["agent", "agent"],
    "sample_size": 6,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
    "brief_hash": "c" * 64,
    "agreement": {"inputs": {}, "demands": {"d-judge": {"breach_difference": 0.1, "self_difference": 0.1}}, "done_agreement": 1.0, "scale": None, "ratings": {}},
}


def write_reply(files: SeriesFolder, condition: str, task: str, repeat: int, turn: int | None = None) -> None:
    """Write an r1 reply record of the condition to the task, or to a turn of the conversation."""
    record = {
        "condition": condition,
        "task": task,
        "split": "sealed" if task in SEALED_TASKS else "open",
        "repeat": repeat,
        "message": f"Explain {task}." if turn is None else f"Turn {turn}.",
        "text": f"{condition} {task} {repeat}",
        "model": READER_MODEL,
        "reader_kind": "agent",
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.0,
        "transcript": "/tmp/transcripts/reader.jsonl",
        "transcript_hash": "a" * 64,
        "cost": COST,
    }
    write_record(files, reply_path("r1", condition, task, repeat, turn), record if turn is None else {**record, "turn": turn}, [])


def stage_one_series(tmp_path: Path) -> SeriesFolder:
    """Write a series with sources, demands, a brief, a plan for attempt 1, and r1 replies of every condition to open, sealed, and conversation tasks, and omissions."""
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", SERIES, [])
    write_file(files, f"1-source/{SOURCE_NAME}", SOURCE_TEXT.encode())
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    write_file(files, "6-judge/brief.md", TEMPLATE.read_bytes())
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", AGENT_PLAN)
    for condition in CONDITIONS:
        write_file(files, f"r1/4-conditions/{condition}.md", condition.encode())
        for task in (*OPEN_TASKS, *SEALED_TASKS):
            for repeat in (1, 2):
                write_reply(files, condition, task, repeat)
        write_reply(files, condition, "c1", 1, turn=1)
    write_file(files, "r1/4-conditions/omit-1.md", b"")
    for repeat in (1, 2):
        write_reply(files, "omit-1", "t1", repeat)
    return files


class NeutralLogin:
    """A neutral login under a home folder, as the reader commands check it."""

    def __init__(self, home: Path):
        self.home = home
        self.config_dir = home / ".claudes-bare" / "readers"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        (self.config_dir / "settings.json").write_text(json.dumps({"enabledPlugins": REQUIRED_PLUGINS}))

    def environ(self) -> dict[str, str]:
        return {"CLAUDE_CONFIG_DIR": str(self.config_dir)}


def calibrate(tmp_path: Path, files: SeriesFolder, seed: int = 7) -> str:
    """Run stage one under the neutral login and return the printed launch list."""
    login = NeutralLogin(tmp_path / "home")
    return calibrate_stage_one(files, TEMPLATE, login.environ(), login.home, files.root, random.Random(seed))


def test_stage_one_refuses_once_calibration_exists_and_writes_nothing(tmp_path):
    files = stage_one_series(tmp_path)
    write_record(files, "6-judge/calibration.yaml", CALIBRATION, [])
    before = tree(files.root)

    with pytest.raises(Refusal, match="6-judge/calibration.yaml"):
        calibrate(tmp_path, files)

    assert tree(files.root) == before


def test_stage_one_without_any_attempt_plan_refuses_naming_the_first_plan_path(tmp_path):
    files = stage_one_series(tmp_path)
    (files.root / "6-judge/calibration/attempt-1/plan.yaml").unlink()

    with pytest.raises(Refusal, match=r"^missing record: 6-judge/calibration/attempt-1/plan\.yaml$"):
        calibrate(tmp_path, files)


def test_stage_one_without_the_working_brief_refuses_naming_the_template_it_starts_from_and_writes_nothing(tmp_path):
    files = stage_one_series(tmp_path)
    (files.root / "6-judge/brief.md").unlink()
    before = tree(files.root)

    with pytest.raises(Refusal, match=rf"^missing brief: 6-judge/brief\.md, start from {TEMPLATE}$"):
        calibrate(tmp_path, files)

    assert tree(files.root) == before
