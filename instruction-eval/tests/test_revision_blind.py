import random
from collections.abc import Sequence

import pytest
import yaml

from instruction_eval.judge import revision_blind
from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, reply_path, sha256, write_file, write_record
from series_fixtures import ONE_DEMAND, write_agent_series, write_yaml

TASK_IDS = ("t1", "t2", "t3", "t4")
TASKS = {
    "tasks": [
        {"id": task, "tempts": "d-judge", "split": "open" if task == "t1" else "sealed", "message": f"Explain {task}.", "answer_key": None}
        for task in TASK_IDS
    ],
    "conversations": [],
}
ANCHORS = {
    "anchors": [
        {"id": f"a-{task}", "task": task, "message": f"Explain {task}.", "text": f"Known {task}.", "breaches": {"d-judge": 0}, "done": True}
        for task in TASK_IDS
    ]
}
CONTROLS = ("empty", "aim", "placebo")
CONDITIONS = {"controls": list(CONTROLS), "aim": "Answers stay short.", "placebo_source": "/home/writer/gardening.md", "omissions": "none"}
GATE = {"repeats": 2, "level": 0.95, "done_by": "judge"}
ACCEPTANCE = {"breach_difference": 0.5, "self_difference": 0.5, "done_agreement": 0.8}
PLAN = {
    "judge_model": "claude-opus-4-1",
    "raters": ["agent", "agent"],
    "rater_model": "claude-sonnet-5-5",
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
}
CALIBRATION = {
    "attempt": 1,
    "judge_model": "claude-opus-4-1",
    "raters": ["agent", "agent"],
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
    "brief_hash": "c" * 64,
    "agreement": {"inputs": {}, "demands": {"d-judge": {"breach_difference": 0.1, "self_difference": 0.1}}, "done_agreement": 1.0, "scale": None, "ratings": {}},
}
COST = {"input_tokens": 1, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 1, "spent_input_tokens": 1}
FIRST_REVISION_TEXT = b"Be terse.\n"
READS_OF_ALL_REVISIONS = {
    "3-tasks.yaml#tasks",
    "3-tasks.yaml#conversations",
    "4-conditions.yaml#controls",
    "4-conditions.yaml#aim",
    "4-conditions.yaml#placebo_source",
    "4-conditions.yaml#omissions",
    "7-gate.yaml#repeats",
    "6-judge/calibration.yaml",
    "6-judge/anchors.yaml",
}


def write_blinded_revision(files: SeriesFolder, number: int) -> None:
    """Write the revision's instruction snapshot and its revision record."""
    revision = f"r{number}"
    text = FIRST_REVISION_TEXT
    write_file(files, f"{revision}/2-instruction.md", text)
    first = number == 1
    record = {
        "number": number,
        "parent": None if first else f"r{number - 1}",
        "hash": sha256(text),
        "parent_record": None if first else sha256(files.read_bytes(f"r{number - 1}/2-revision.yaml")),
        "change": None if first else {"action": "rewrite", "sentence": 1, "old": "Old.", "new": "New."},
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [] if first else [f"r{number - 1}/2-revision.yaml"])


def write_blind_reply(files: SeriesFolder, path: str, condition: str, task: str, repeat: int) -> None:
    """Write the reply record at the path."""
    record = {
        "condition": condition,
        "task": task,
        "split": "open" if task == "t1" else "sealed",
        "repeat": repeat,
        "message": f"Explain {task}.",
        "text": f"{condition} {task} {repeat}",
        "model": "claude-sonnet-5-5",
        "reader_kind": "agent",
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.0,
        "transcript": "/tmp/transcripts/reader.jsonl",
        "transcript_hash": "a" * 64,
        "cost": COST,
    }
    write_record(files, path, record, [])


def write_condition_replies(files: SeriesFolder, revision: str, conditions: Sequence[str]) -> None:
    """Write the revision's reply of each condition to each task and repeat, its condition text first."""
    for condition in conditions:
        write_file(files, f"{revision}/4-conditions/{condition}.md", condition.encode())
        for task in TASK_IDS:
            for repeat in (1, 2):
                write_blind_reply(files, reply_path(revision, condition, task, repeat, None), condition, task, repeat)


def blindable_series(tmp_path, revisions: int = 1) -> SeriesFolder:
    """Write a series with calibration, anchors, and the replies of revision r1, and of later revisions the instruction's alone."""
    files = SeriesFolder(tmp_path)
    write_agent_series(files, ONE_DEMAND, TASKS, ANCHORS)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_yaml(files, "7-gate.yaml", GATE)
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", PLAN)
    write_record(files, "6-judge/calibration.yaml", CALIBRATION, [])
    for number in range(1, revisions + 1):
        write_blinded_revision(files, number)
    write_condition_replies(files, "r1", ("instruction", *CONTROLS))
    for number in range(2, revisions + 1):
        write_condition_replies(files, f"r{number}", ("instruction",))
    return files


def blind(files: SeriesFolder, revision: str = "r1", seed: int = 7) -> None:
    revision_blind(files, revision, random.Random(seed))


def blind_reads(revision: str, reply_paths: Sequence[str]) -> set[str]:
    """Return the Commands-table reads of `revision blind` expanded for the revision."""
    return {*READS_OF_ALL_REVISIONS, f"{revision}/2-instruction.md", *reply_paths}


def test_a_first_revision_is_blinded_into_one_packet_per_task_hashed_in_its_origins_which_read_exactly_what_the_command_reads(tmp_path):
    files = blindable_series(tmp_path)

    blind(files)

    origins = SeriesRecords(files).origins("r1")
    assert sorted(origins["packets"]) == list(TASK_IDS)
    for task in TASK_IDS:
        assert origins["packets"][task] == sha256(files.read_bytes(f"r1/6-packets/{task}.md"))
    reply_paths = [reply_path("r1", condition, task, repeat, None) for condition in ("instruction", *CONTROLS) for task in TASK_IDS for repeat in (1, 2)]
    assert set(origins["inputs"]) == blind_reads("r1", reply_paths)


def test_a_series_without_calibration_refuses_to_blind_and_writes_nothing(tmp_path):
    files = blindable_series(tmp_path)
    (files.root / "6-judge/calibration.yaml").unlink()

    with pytest.raises(Refusal, match="6-judge/calibration.yaml"):
        blind(files)

    assert not (files.root / "r1/6-packets").exists()
    assert not files.holds("r1/6-origins.yaml")


def test_a_later_revision_borrows_every_control_reply_from_r1_and_keeps_its_own_instruction_replies(tmp_path):
    files = blindable_series(tmp_path, revisions=2)

    blind(files, "r2")

    origins = SeriesRecords(files).origins("r2")
    replies = [origin for origin in origins["ids"].values() if "anchor" not in origin]
    assert {origin["borrowed_from"] for origin in replies if origin["condition"] == "instruction"} == {None}
    assert {origin["borrowed_from"] for origin in replies if origin["condition"] in CONTROLS} == {"r1"}
    assert len(replies) == len(TASK_IDS) * 2 * (1 + len(CONTROLS))
    reply_paths = [
        reply_path(revision, condition, task, repeat, None)
        for revision, conditions in (("r2", ("instruction",)), ("r1", CONTROLS))
        for condition in conditions
        for task in TASK_IDS
        for repeat in (1, 2)
    ]
    assert set(origins["inputs"]) == blind_reads("r2", reply_paths)


def test_a_gap_against_the_expected_replies_refuses_naming_the_count_and_the_first_path_and_writes_nothing(tmp_path):
    files = blindable_series(tmp_path)
    (files.root / reply_path("r1", "aim", "t2", 1, None)).unlink()
    (files.root / reply_path("r1", "aim", "t3", 2, None)).unlink()

    with pytest.raises(Refusal, match=r"^missing replies: 2, first r1/5-replies/aim/t2/repeat-1\.yaml$"):
        blind(files)

    assert not (files.root / "r1/6-packets").exists()


def test_a_packet_with_fewer_anchors_from_other_tasks_than_the_calibration_sets_refuses(tmp_path):
    files = blindable_series(tmp_path)
    (files.root / "6-judge/anchors.yaml").unlink()
    write_record(files, "6-judge/anchors.yaml", {"anchors": ANCHORS["anchors"][:3]}, [])

    with pytest.raises(Refusal, match="too few anchors for t"):
        blind(files)

    assert not files.holds("r1/6-origins.yaml")


def test_every_packet_of_the_revision_holds_its_replies_and_the_set_number_of_anchors_from_other_tasks(tmp_path):
    files = blindable_series(tmp_path)

    blind(files)

    origins = SeriesRecords(files).origins("r1")
    for task in TASK_IDS:
        entries = [origin for origin in origins["ids"].values() if origin["packet"] == task]
        anchors = [origin["anchor"] for origin in entries if "anchor" in origin]
        assert len([origin for origin in entries if "anchor" not in origin]) == 2 * (1 + len(CONTROLS))
        assert len(anchors) == 3
        assert f"a-{task}" not in anchors


def test_blinding_an_already_blinded_revision_refuses_and_keeps_the_written_packets(tmp_path):
    files = blindable_series(tmp_path)
    blind(files)
    written = files.read_bytes("r1/6-packets/t1.md")

    with pytest.raises(Refusal, match="already written"):
        blind(files, seed=8)

    assert files.read_bytes("r1/6-packets/t1.md") == written


def test_with_omissions_asked_each_open_task_gets_one_omissions_packet_of_its_omission_replies(tmp_path):
    files = blindable_series(tmp_path)
    (files.root / "4-conditions.yaml").write_text(yaml.safe_dump({**CONDITIONS, "omissions": "every-sentence"}))
    write_file(files, "r1/4-conditions/omit-1.md", b"")
    for repeat in (1, 2):
        write_blind_reply(files, reply_path("r1", "omit-1", "t1", repeat, None), "omit-1", "t1", repeat)

    blind(files)

    origins = SeriesRecords(files).origins("r1")
    omissions = [origin for origin in origins["ids"].values() if origin["packet"] == "t1--omissions" and "anchor" not in origin]
    assert sorted(origin["repeat"] for origin in omissions) == [1, 2]
    assert {origin["condition"] for origin in omissions} == {"omit-1"}
    assert "t1--omissions" in origins["packets"]
    assert files.holds("r1/6-packets/t1--omissions.md")
