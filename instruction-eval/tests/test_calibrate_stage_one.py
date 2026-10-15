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
UNSOURCED_CONDITIONS = tuple(condition for condition in CONDITIONS if condition != "source")
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


def stage_one_series(tmp_path: Path, sourced: bool = True) -> SeriesFolder:
    """Write a series with demands, a brief, a plan for attempt 1, and r1 replies of every condition to open, sealed, and conversation tasks, and omissions; with sources unless `sourced` is false."""
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", SERIES if sourced else {**SERIES, "sources": []}, [])
    if sourced:
        write_file(files, f"1-source/{SOURCE_NAME}", SOURCE_TEXT.encode())
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    write_file(files, "6-judge/brief.md", TEMPLATE.read_bytes())
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", AGENT_PLAN)
    for condition in CONDITIONS if sourced else UNSOURCED_CONDITIONS:
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


ATTEMPT_ONE = "6-judge/calibration/attempt-1"


def test_stage_one_snapshots_the_working_brief_into_the_attempt_byte_for_byte(tmp_path):
    files = stage_one_series(tmp_path)

    calibrate(tmp_path, files)

    assert files.read_bytes(f"{ATTEMPT_ONE}/brief.md") == TEMPLATE.read_bytes()


FIRST_DRAW = {("aim", "t1", 1), ("empty", "t1", 1), ("instruction", "t1", 1), ("placebo", "t1", 1), ("source", "t1", 1), ("aim", "t1", 2)}


def sampled(files: SeriesFolder, attempt: int) -> set[tuple[str, str, int]]:
    """Return the condition, task, and repeat of each reply the attempt's origins name."""
    origins = SeriesRecords(files).attempt_origins(attempt)["ids"].values()
    return {(origin["condition"], origin["task"], origin["repeat"]) for origin in origins}


def test_the_first_attempt_draws_round_robin_from_the_alphabetical_first_condition_over_open_task_replies_alone(tmp_path):
    files = stage_one_series(tmp_path)

    calibrate(tmp_path, files)

    assert sampled(files, 1) == FIRST_DRAW
    origins = SeriesRecords(files).attempt_origins(1)
    assert sorted(origins["packets"]) == ["sample"]
    assert origins["packets"]["sample"] == sha256(files.read_bytes(f"{ATTEMPT_ONE}/sample.md"))


SECOND_DRAW = {("empty", "t1", 2), ("instruction", "t1", 2), ("placebo", "t1", 2), ("source", "t1", 2), ("aim", "t2", 1), ("empty", "t2", 1)}


def test_the_next_attempt_starts_one_condition_later_acts_on_its_own_plan_and_skips_what_earlier_attempts_sampled(tmp_path):
    files = stage_one_series(tmp_path)
    calibrate(tmp_path, files)
    write_yaml(files, "6-judge/calibration/attempt-2/plan.yaml", AGENT_PLAN)

    calibrate(tmp_path, files)

    assert sampled(files, 2) == SECOND_DRAW
    assert files.read_bytes("6-judge/calibration/attempt-2/brief.md") == TEMPLATE.read_bytes()


def test_the_start_condition_wraps_around_the_condition_count(tmp_path):
    files = stage_one_series(tmp_path)
    first_conditions = []
    for attempt in range(1, 7):
        write_yaml(files, f"6-judge/calibration/attempt-{attempt}/plan.yaml", {**AGENT_PLAN, "sample_size": 1})
        calibrate(tmp_path, files)
        ((condition, _, _),) = sampled(files, attempt)
        first_conditions.append(condition)

    assert first_conditions == ["aim", "empty", "instruction", "placebo", "source", "aim"]


EXHAUSTED = r"^calibration pool exhausted: lower sample_size or start a new series with more repeats$"


def test_a_sample_larger_than_the_open_task_replies_refuses_as_exhausted_and_writes_nothing(tmp_path):
    files = stage_one_series(tmp_path)
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", {**AGENT_PLAN, "sample_size": 21})
    before = tree(files.root)

    with pytest.raises(Refusal, match=EXHAUSTED):
        calibrate(tmp_path, files)

    assert tree(files.root) == before


def test_a_later_attempt_refuses_as_exhausted_when_earlier_attempts_left_too_few_unsampled_replies(tmp_path):
    files = stage_one_series(tmp_path)
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", {**AGENT_PLAN, "sample_size": 12})
    calibrate(tmp_path, files)
    write_yaml(files, "6-judge/calibration/attempt-2/plan.yaml", {**AGENT_PLAN, "sample_size": 9})
    before = tree(files.root)

    with pytest.raises(Refusal, match=EXHAUSTED):
        calibrate(tmp_path, files)

    assert tree(files.root) == before


def definition(files: SeriesFolder, name: str) -> tuple[dict, str]:
    """Return the frontmatter and body of the generated definition."""
    header, _, body = files.read_bytes(f".claude/agents/{name}.md").decode().removeprefix("---\n").partition("---\n")
    return yaml.safe_load(header), body


def test_stage_one_writes_candidate_and_rater_definitions_from_the_snapshot_and_prints_their_launch_list(tmp_path):
    files = stage_one_series(tmp_path)

    launch_list = calibrate(tmp_path, files)

    names = ["ie-calib-1-candidate-1", "ie-calib-1-candidate-2", "ie-calib-1-rater-1", "ie-calib-1-rater-2"]
    assert yaml.safe_load(launch_list) == {"launches": [{"agent_type": name} for name in names]}
    models = [JUDGE_MODEL, JUDGE_MODEL, RATER_MODEL, RATER_MODEL]
    verdicts = ["candidate-1", "candidate-2", "reference-rater-1", "reference-rater-2"]
    sample = files.read_bytes(f"{ATTEMPT_ONE}/sample.md").decode()
    for name, model, verdict in zip(names, models, verdicts):
        frontmatter, body = definition(files, name)
        assert frontmatter == {"name": name, "description": "Generated agent; launch from the printed launch list only.", "model": model, "tools": "Skill, Write"}
        assert f"Source file: {SOURCE_NAME}\n\nBe terse." in body
        assert sample in body
        assert f"{files.root}/{ATTEMPT_ONE}/{verdict}.yaml" in body
        assert "d-judge" in body and "d-hedge" not in body


def test_user_raters_leave_only_the_two_candidate_definitions(tmp_path):
    files = stage_one_series(tmp_path)
    write_yaml(files, f"{ATTEMPT_ONE}/plan.yaml", USER_PLAN)

    launch_list = calibrate(tmp_path, files)

    assert yaml.safe_load(launch_list) == {"launches": [{"agent_type": "ie-calib-1-candidate-1"}, {"agent_type": "ie-calib-1-candidate-2"}]}
    assert sorted(path.name for path in (files.root / ".claude/agents").iterdir()) == ["ie-calib-1-candidate-1.md", "ie-calib-1-candidate-2.md"]


def test_stage_one_outside_the_neutral_login_refuses_and_writes_nothing(tmp_path):
    files = stage_one_series(tmp_path)
    before = tree(files.root)

    with pytest.raises(NeutralLoginRefused):
        calibrate_stage_one(files, TEMPLATE, {}, tmp_path / "home", files.root, random.Random(7))

    assert tree(files.root) == before


@pytest.mark.parametrize(
    ("brief", "fault"),
    [
        (TEMPLATE.read_text().replace("{OUT}", ""), r"brief fault: \{OUT\} appears 0 times, not once"),
        (TEMPLATE.read_text() + "\nCompare the control group.\n", r"brief fault: names control"),
        (TEMPLATE.read_text() + f"\nServed by {READER_MODEL}.\n", f"brief fault: names {READER_MODEL}"),
    ],
    ids=["lacks-placeholder", "forbidden-word", "reader-model"],
)
def test_a_faulty_brief_refuses_naming_the_fault_and_writes_nothing(tmp_path, brief, fault):
    files = stage_one_series(tmp_path)
    (files.root / "6-judge/brief.md").write_text(brief)
    before = tree(files.root)

    with pytest.raises(Refusal, match=fault):
        calibrate(tmp_path, files)

    assert tree(files.root) == before


PLAN_KEYS = ("judge_model", "raters", "rater_model", "sample_size", "anchors_per_packet", "acceptance")


def reads_of(files: SeriesFolder, attempt: int, earlier: int, sourced: bool = True) -> set[str]:
    """Return the Commands-table reads of stage one expanded for the attempt: the series records, its plan keys, brief, sample, sampled replies, and earlier origins."""
    folder = f"6-judge/calibration/attempt-{attempt}"
    sampled_replies = {reply_path("r1", condition, task, repeat, None) for condition, task, repeat in sampled(files, attempt)}
    return {
        "series.yaml",
        *([f"1-source/{SOURCE_NAME}"] if sourced else ["r1/3-coverage.yaml#demands"]),
        "2-demands.yaml#demands",
        *(f"{folder}/plan.yaml#{key}" for key in PLAN_KEYS),
        f"{folder}/brief.md",
        f"{folder}/sample.md",
        *sampled_replies,
        *(f"6-judge/calibration/attempt-{number}/origins.yaml" for number in range(1, earlier + 1)),
    }


def test_stage_one_records_the_inputs_it_reads_and_the_next_attempt_adds_every_earlier_origins_file(tmp_path):
    files = stage_one_series(tmp_path)
    calibrate(tmp_path, files)
    write_yaml(files, "6-judge/calibration/attempt-2/plan.yaml", AGENT_PLAN)
    calibrate(tmp_path, files)

    records = SeriesRecords(files)
    assert set(records.attempt_origins(1)["inputs"]) == reads_of(files, 1, earlier=0)
    assert set(records.attempt_origins(2)["inputs"]) == reads_of(files, 2, earlier=1)


def test_without_sources_the_judge_binds_to_the_gate_demands_of_the_coverage_and_the_inputs_name_the_coverage(tmp_path):
    files = stage_one_series(tmp_path, sourced=False)

    calibrate(tmp_path, files)

    _, body = definition(files, "ie-calib-1-candidate-1")
    assert "Source file:" not in body
    assert "- id: d-judge\n  text: Be terse." in body
    assert "- id: d-plain\n  text: Use plain words." in body
    assert "d-hedge" not in body
    assert set(SeriesRecords(files).attempt_origins(1)["inputs"]) == reads_of(files, 1, earlier=0, sourced=False)
