import json
import random
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

import instruction_eval
from instruction_eval.judge import calibrate_stage_one, calibrate_stage_two
from instruction_eval.reader import Transcript
from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, reply_path, write_file, write_record
from series_fixtures import sha256, tree, write_yaml

TEMPLATE = Path(instruction_eval.__file__).parent / "templates" / "judge-brief.md"
REQUIRED_PLUGINS = {"instruction-eval@my-claude-skills": True, "manifesto@my-claude-skills": True}
JUDGE_MODEL = "claude-opus-4-1"
RATER_MODEL = "claude-sonnet-5-5"
READER_MODEL = "claude-haiku-4-5"
SOURCE_NAME = "policy.md"
SERIES = {"instruction": "/home/writer/terse.md", "sources": [f"/home/writer/{SOURCE_NAME}"], "reader_kind": "agent", "created": "2026-10-14T10:00:00+00:00"}
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
CONDITIONS = ("empty", "instruction")
TASK_IDS = ("t1", "t2", "t3", "t4", "t5", "t6")
TASKS = {
    "tasks": [{"id": task, "tempts": "d-judge", "split": "open", "message": f"Explain {task}.", "answer_key": None} for task in TASK_IDS],
    "conversations": [],
}
ACCEPTANCE = {"breach_difference": 0.5, "self_difference": 0.5, "done_agreement": 0.8}
AGENT_PLAN = {"judge_model": JUDGE_MODEL, "raters": ["agent", "agent"], "rater_model": RATER_MODEL, "sample_size": 6, "anchors_per_packet": 3, "acceptance": ACCEPTANCE}
USER_PLAN = {"judge_model": JUDGE_MODEL, "raters": ["user"], "sample_size": 6, "anchors_per_packet": 3, "acceptance": ACCEPTANCE}
COST = {"input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 1, "spent_input_tokens": 1}
ATTEMPT = "6-judge/calibration/attempt-1"
AGENT_RATINGS = {"candidate-1": JUDGE_MODEL, "candidate-2": JUDGE_MODEL, "reference-rater-1": RATER_MODEL, "reference-rater-2": RATER_MODEL}


def write_reply(files: SeriesFolder, condition: str, task: str, repeat: int) -> None:
    """Write an r1 reply record of the condition to the task."""
    record = {
        "condition": condition,
        "task": task,
        "split": "open",
        "repeat": repeat,
        "message": f"Explain {task}.",
        "text": f"{condition} {task} {repeat}",
        "model": READER_MODEL,
        "reader_kind": "agent",
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.0,
        "transcript": "/tmp/transcripts/reader.jsonl",
        "transcript_hash": "a" * 64,
        "cost": COST,
    }
    write_record(files, reply_path("r1", condition, task, repeat, None), record, [])


class NeutralLogin:
    """A neutral login under a home folder, as stage one checks it."""

    def __init__(self, home: Path):
        self.home = home
        self.config_dir = home / ".claudes-bare" / "readers"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        (self.config_dir / "settings.json").write_text(json.dumps({"enabledPlugins": REQUIRED_PLUGINS}))

    def environ(self) -> dict[str, str]:
        return {"CLAUDE_CONFIG_DIR": str(self.config_dir)}


def stage_one(tmp_path: Path, files: SeriesFolder) -> None:
    """Run stage one under the neutral login."""
    login = NeutralLogin(tmp_path / "home")
    calibrate_stage_one(files, TEMPLATE, login.environ(), login.home, files.root, random.Random(7))


def calibrating_series(tmp_path: Path, plan: dict = AGENT_PLAN) -> SeriesFolder:
    """Write a series with a source, demands, tasks, one r1 reply per condition and open task, a brief, and the plan for attempt 1, then run stage one."""
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", SERIES, [])
    write_file(files, f"1-source/{SOURCE_NAME}", b"Be terse.\n")
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_file(files, "6-judge/brief.md", TEMPLATE.read_bytes())
    write_yaml(files, f"{ATTEMPT}/plan.yaml", plan)
    for condition in CONDITIONS:
        for task in TASK_IDS:
            write_reply(files, condition, task, 1)
    stage_one(tmp_path, files)
    return files


Origin = dict
Count = Callable[[Origin], tuple[int, bool | None]]


def sample_origins(files: SeriesFolder, attempt: int = 1) -> dict[str, Origin]:
    """Return the origin of every blind id the attempt's sample holds."""
    return SeriesRecords(files).attempt_origins(attempt)["ids"]


def write_rating(files: SeriesFolder, name: str, count: Count, attempt: int = 1) -> None:
    """Write the rating file `name` of the attempt, each entry's breaches of `d-judge` and done value given by `count` of its origin."""
    entries = []
    for blind_id, origin in sample_origins(files, attempt).items():
        breaches, done = count(origin)
        entries.append({"id": blind_id, "breaches": {"d-judge": breaches}, "done": done, "kind": "answer", "notes": ""})
    write_yaml(files, f"6-judge/calibration/attempt-{attempt}/{name}.yaml", {"verdicts": entries})


def rating_transcript(files: SeriesFolder, name: str, model: str, attempt: int = 1) -> Transcript:
    """Write the ended transcript of a rating agent that loaded the oath skill and wrote its rating file, and return its location."""
    agent_type = f"ie-calib-{attempt}-{name.removeprefix('reference-')}"
    rating = files.root / f"6-judge/calibration/attempt-{attempt}/{name}.yaml"
    blocks = [
        {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": "manifesto:manifesto-oath"}},
        {"type": "tool_use", "id": "toolu_2", "name": "Write", "input": {"file_path": str(rating)}},
        {"type": "text", "text": "Done."},
    ]
    usage = {"input_tokens": 3, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 2}
    started = "2026-10-14T19:00:43.000Z"
    lines = [
        {"type": "user", "message": {"role": "user", "content": "Rate the sample."}, "timestamp": started},
        {"type": "assistant", "message": {"model": model, "id": "msg_A", "role": "assistant", "content": blocks, "usage": usage}, "timestamp": started},
    ]
    path = files.root.parent / f"transcripts/{agent_type}/subagents/agent-{agent_type}.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines))
    return Transcript(path=path, session=path.parent.parent.name, agent_id=agent_type, agent_type=agent_type)


def rate(files: SeriesFolder, counts: dict[str, Count], attempt: int = 1) -> list[Transcript]:
    """Write each agent rating with its counts and its transcript, and return the transcripts."""
    transcripts = []
    for name, count in counts.items():
        write_rating(files, name, count, attempt)
        transcripts.append(rating_transcript(files, name, AGENT_RATINGS[name], attempt))
    return transcripts


def one_done(origin: Origin) -> tuple[int, bool | None]:
    return 1, True


def stage_two(files: SeriesFolder, transcripts: list[Transcript]) -> str:
    return calibrate_stage_two(files, transcripts, Path.read_bytes)


def test_an_attempt_every_rating_agrees_on_is_accepted_into_the_calibration_and_its_sample_becomes_the_anchors(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done))

    printed = stage_two(files, transcripts)

    assert printed == "accepted: attempt 1\n"
    records = SeriesRecords(files)
    agreement = records.agreement(1)
    assert agreement["demands"] == {"d-judge": {"breach_difference": 0.0, "self_difference": 0.0}}
    assert agreement["done_agreement"] == 1.0
    assert agreement["scale"] == 1.0
    assert agreement["ratings"] == {
        f"{name}.yaml": {"model": model, "transcript": str(transcript.path), "transcript_hash": sha256(transcript.path.read_bytes())}
        for (name, model), transcript in zip(AGENT_RATINGS.items(), transcripts)
    }
    calibration = records.calibration()
    assert {key: calibration[key] for key in ("attempt", "judge_model", "raters", "sample_size", "anchors_per_packet", "acceptance")} == {
        "attempt": 1,
        "judge_model": JUDGE_MODEL,
        "raters": ["agent", "agent"],
        "sample_size": 6,
        "anchors_per_packet": 3,
        "acceptance": ACCEPTANCE,
    }
    assert calibration["brief_hash"] == sha256(files.read_bytes(f"{ATTEMPT}/brief.md"))
    assert calibration["agreement"] == agreement
    anchors = records.anchors()["anchors"]
    sampled = sample_origins(files)
    assert {anchor["id"]: (anchor["task"], anchor["message"], anchor["text"], anchor["done"]) for anchor in anchors} == {
        blind_id: (origin["task"], f"Explain {origin['task']}.", f"{origin['condition']} {origin['task']} 1", True) for blind_id, origin in sampled.items()
    }
    assert all(anchor["breaches"] == {"d-judge": 1} for anchor in anchors)


def counting(breaches: int, done: bool | None) -> Count:
    return lambda origin: (breaches, done)


def done_unless_instruction_outside_t1(breaches: int) -> Count:
    return lambda origin: (breaches, origin["task"] == "t1" or origin["condition"] == "empty")


def test_a_candidate_whose_runs_disagree_is_rejected_its_agreement_measured_against_the_raters_median_and_common_done(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(
        files,
        {
            "candidate-1": counting(2, True),
            "candidate-2": counting(0, False),
            "reference-rater-1": counting(1, True),
            "reference-rater-2": done_unless_instruction_outside_t1(2),
        },
    )

    printed = stage_two(files, transcripts)

    assert printed == "rejected: attempt 1 (self_difference of d-judge 2.0 over 0.5)\n"
    agreement = SeriesRecords(files).agreement(1)
    assert agreement["demands"] == {"d-judge": {"breach_difference": 0.5, "self_difference": 2.0}}
    assert agreement["done_agreement"] == 0.5
    assert agreement["scale"] == pytest.approx(1 / 1.5)
    assert not files.holds("6-judge/calibration.yaml")
    assert not files.holds("6-judge/anchors.yaml")


def test_a_rejected_attempt_stays_as_it_is_and_the_next_attempt_is_accepted_on_its_own_sample_whatever_the_working_brief_and_earlier_brief_hold(tmp_path):
    files = calibrating_series(tmp_path)
    stage_two(files, rate(files, {**dict.fromkeys(AGENT_RATINGS, one_done), "candidate-2": counting(3, True)}))
    rejected_agreement = files.read_bytes("6-judge/calibration/attempt-1/agreement.yaml")
    write_yaml(files, "6-judge/calibration/attempt-2/plan.yaml", AGENT_PLAN)
    stage_one(tmp_path, files)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done), attempt=2)
    (files.root / "6-judge/brief.md").write_text("Edited working brief.\n")
    (files.root / "6-judge/calibration/attempt-1/brief.md").write_text("Edited earlier brief.\n")

    printed = stage_two(files, transcripts)

    assert printed == "accepted: attempt 2\n"
    calibration = SeriesRecords(files).calibration()
    assert calibration["attempt"] == 2
    assert calibration["brief_hash"] == sha256(files.read_bytes("6-judge/calibration/attempt-2/brief.md"))
    assert {anchor["id"] for anchor in SeriesRecords(files).anchors()["anchors"]} == set(sample_origins(files, 2))
    assert files.read_bytes("6-judge/calibration/attempt-1/agreement.yaml") == rejected_agreement


def test_raters_who_never_agree_on_done_refuse_as_no_reference_done_and_write_nothing(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, {**dict.fromkeys(AGENT_RATINGS, one_done), "reference-rater-2": counting(1, False)})
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^no reference done in the sample$"):
        stage_two(files, transcripts)

    assert tree(files.root) == before


def test_a_reference_counting_no_breach_leaves_the_scale_null(tmp_path):
    files = calibrating_series(tmp_path)

    stage_two(files, rate(files, dict.fromkeys(AGENT_RATINGS, counting(0, True))))

    assert SeriesRecords(files).agreement(1)["scale"] is None


def test_a_half_reference_count_becomes_an_anchor_count_rounded_away_from_zero(tmp_path):
    files = calibrating_series(tmp_path)
    counts = {"candidate-1": counting(2, True), "candidate-2": counting(2, True), "reference-rater-1": counting(1, True), "reference-rater-2": counting(2, True)}

    assert stage_two(files, rate(files, counts)) == "accepted: attempt 1\n"

    assert {anchor["breaches"]["d-judge"] for anchor in SeriesRecords(files).anchors()["anchors"]} == {2}


def done_on_t1_alone(origin: Origin) -> tuple[int, bool | None]:
    return 1, True if origin["task"] == "t1" else None


def test_too_few_anchors_of_other_tasks_reject_the_attempt_naming_the_first_task_short_of_them(tmp_path):
    files = calibrating_series(tmp_path)
    counts = {**dict.fromkeys(AGENT_RATINGS, one_done), "reference-rater-1": done_on_t1_alone}

    printed = stage_two(files, rate(files, counts))

    assert printed == "rejected: attempt 1 (too few anchors for t1)\n"
    assert files.holds("6-judge/calibration/attempt-1/agreement.yaml")
    assert not files.holds("6-judge/calibration.yaml")


def test_missing_rating_files_refuse_listing_each_and_write_nothing(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, {"candidate-1": one_done, "reference-rater-1": one_done})
    before = tree(files.root)

    with pytest.raises(Refusal, match=rf"^missing rating: {ATTEMPT}/candidate-2\.yaml\nmissing rating: {ATTEMPT}/reference-rater-2\.yaml$"):
        stage_two(files, transcripts)

    assert tree(files.root) == before


def test_an_invalid_rating_file_refuses_naming_it_and_writes_nothing(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done))
    rating = files.root / ATTEMPT / "reference-rater-2.yaml"
    document = yaml.safe_load(rating.read_text())
    rating.write_text(yaml.safe_dump({"verdicts": document["verdicts"][1:]}))
    before = tree(files.root)

    with pytest.raises(Refusal, match=rf"^invalid rating: {ATTEMPT}/reference-rater-2\.yaml \(verdict: missing blind id b[0-9a-f]{{8}}\)$"):
        stage_two(files, transcripts)

    assert tree(files.root) == before


def retranscribed(files: SeriesFolder, transcripts: list[Transcript], name: str, model: str) -> list[Transcript]:
    """Return the transcripts with the one of rating `name` rewritten as served by `model`."""
    path = next(transcript.path for transcript in transcripts if transcript.agent_type.endswith(name.removeprefix("reference-")))
    path.write_text(path.read_text().replace(AGENT_RATINGS[name], model))
    return transcripts


@pytest.mark.parametrize(
    ("damage", "reason"),
    [
        (lambda files, transcripts: retranscribed(files, transcripts, "candidate-2", RATER_MODEL), rf"model {RATER_MODEL}, not {JUDGE_MODEL}"),
        (lambda files, transcripts: retranscribed(files, transcripts, "reference-rater-1", JUDGE_MODEL), rf"model {JUDGE_MODEL}, not {RATER_MODEL}"),
        (lambda files, transcripts: [transcript for transcript in transcripts if not transcript.agent_type.endswith("candidate-2")], "no ended transcript of ie-calib-1-candidate-2"),
    ],
    ids=["candidate-from-rater-model", "rater-from-judge-model", "no-transcript"],
)
def test_a_rating_whose_agent_ran_another_model_or_left_no_transcript_refuses_naming_it(tmp_path, damage, reason):
    files = calibrating_series(tmp_path)
    transcripts = damage(files, rate(files, dict.fromkeys(AGENT_RATINGS, one_done)))

    with pytest.raises(Refusal, match=rf"^invalid rating: {ATTEMPT}/[a-z-]+[0-9]\.yaml \({reason}\)$"):
        stage_two(files, transcripts)


def test_a_rating_whose_transcript_shows_a_tool_use_besides_the_oath_and_its_write_refuses_naming_it(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done))
    path = next(transcript.path for transcript in transcripts if transcript.agent_type == "ie-calib-1-candidate-1")
    path.write_text(path.read_text().replace('"name": "Skill"', '"name": "Read"'))

    with pytest.raises(Refusal, match=rf"^invalid rating: {ATTEMPT}/candidate-1\.yaml \(.+\)$"):
        stage_two(files, transcripts)


def test_a_rating_definition_edited_since_stage_one_refuses_naming_it_and_writes_nothing(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done))
    definition = files.root / ".claude/agents/ie-calib-1-rater-2.md"
    definition.write_text(definition.read_text() + "Count leniently.\n")
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^\.claude/agents/ie-calib-1-rater-2\.md differs from its recomputation$"):
        stage_two(files, transcripts)

    assert tree(files.root) == before


def sampled_reply_path(files: SeriesFolder) -> str:
    origin = next(iter(sample_origins(files).values()))
    return reply_path("r1", origin["condition"], origin["task"], origin["repeat"], None)


@pytest.mark.parametrize(
    "edited",
    [lambda files: f"{ATTEMPT}/plan.yaml", lambda files: f"{ATTEMPT}/brief.md", sampled_reply_path],
    ids=["plan", "brief-snapshot", "sampled-reply"],
)
def test_an_input_of_stage_one_edited_before_stage_two_refuses_as_stale_and_writes_nothing(tmp_path, edited):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done))
    path = edited(files)
    target = files.root / path
    target.write_text(target.read_text().replace(RATER_MODEL, "claude-sonnet-5-6") + "\n")
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^stale: "):
        stage_two(files, transcripts)

    assert tree(files.root) == before


def test_stage_two_refuses_once_the_calibration_exists(tmp_path):
    files = calibrating_series(tmp_path)
    transcripts = rate(files, dict.fromkeys(AGENT_RATINGS, one_done))
    stage_two(files, transcripts)
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^already calibrated: 6-judge/calibration\.yaml$"):
        stage_two(files, transcripts)

    assert tree(files.root) == before


def test_a_user_rater_is_the_reference_alone_and_only_the_candidate_ratings_carry_runs(tmp_path):
    files = calibrating_series(tmp_path, USER_PLAN)
    transcripts = rate(files, {"candidate-1": one_done, "candidate-2": one_done})
    write_rating(files, "reference-user", counting(3, True))

    printed = stage_two(files, transcripts)

    assert printed == "rejected: attempt 1 (breach_difference of d-judge 2.0 over 0.5)\n"
    agreement = SeriesRecords(files).agreement(1)
    assert sorted(agreement["ratings"]) == ["candidate-1.yaml", "candidate-2.yaml"]
    assert agreement["scale"] == pytest.approx(1 / 3)


PLAN_KEYS = ("judge_model", "raters", "rater_model", "sample_size", "anchors_per_packet", "acceptance")


def test_every_record_stage_two_writes_names_as_inputs_exactly_what_it_reads(tmp_path):
    files = calibrating_series(tmp_path)
    stage_two(files, rate(files, dict.fromkeys(AGENT_RATINGS, one_done)))

    sampled = {reply_path("r1", origin["condition"], origin["task"], origin["repeat"], None) for origin in sample_origins(files).values()}
    reads = {
        "series.yaml",
        f"1-source/{SOURCE_NAME}",
        "2-demands.yaml#demands",
        "3-tasks.yaml#tasks",
        *(f"{ATTEMPT}/plan.yaml#{key}" for key in PLAN_KEYS),
        f"{ATTEMPT}/brief.md",
        f"{ATTEMPT}/sample.md",
        f"{ATTEMPT}/origins.yaml",
        *(f"{ATTEMPT}/{name}.yaml" for name in AGENT_RATINGS),
        *(f".claude/agents/ie-calib-1-{name.removeprefix('reference-')}.md" for name in AGENT_RATINGS),
        *sampled,
    }
    records = SeriesRecords(files)
    assert set(records.agreement(1)["inputs"]) == reads
    assert set(records.calibration()["inputs"]) == reads
    assert set(records.anchors()["inputs"]) == reads
