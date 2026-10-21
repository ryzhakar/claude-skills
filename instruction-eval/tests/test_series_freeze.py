from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest
from series_fixtures import SERIES_BINDING, Reply, bootstrap_rng, read_nothing, sha256, tree, write_origins, write_yaml

from instruction_eval.records import (
    Refusal,
    SeriesFolder,
    SeriesRecords,
    reply_path,
    write_file,
    write_record,
)
from instruction_eval.series import series_freeze

INSTRUCTION = b"Be terse. Avoid hedges.\n"
PLACEBO = b"Lorem ipsum dolor sit amet.\n"
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
TASKS = {
    "tasks": [
        {"id": "j-open", "tempts": "d-judge", "split": "open", "message": "Explain the tides.", "answer_key": None},
        {"id": "j-sealed", "tempts": "d-judge", "split": "sealed", "message": "Explain the snow.", "answer_key": None},
        {"id": "h-open", "tempts": "d-hedge", "split": "open", "message": "Explain the rain.", "answer_key": None},
        {"id": "h-sealed", "tempts": "d-hedge", "split": "sealed", "message": "Explain the hail.", "answer_key": None},
        {"id": "o-open", "tempts": "overreach", "split": "open", "message": "Name the moon.", "answer_key": "moon"},
        {"id": "o-sealed", "tempts": "overreach", "split": "sealed", "message": "Name the sun.", "answer_key": "sun"},
    ],
    "conversations": [],
}
CONDITIONS = {"controls": ["empty", "aim", "placebo"], "aim": "Answer in few words.", "placebo_source": "/tmp/placebo.md", "omissions": "none"}
CONDITION_NAMES = ("instruction", "empty", "aim", "placebo")
COVERAGE = {"demands": {"d-judge": [1], "d-hedge": [2]}, "sentences": {1: ["d-judge"], 2: ["d-hedge"]}}
ANCHORS = {"anchors": [{"id": "a-one", "task": "j-open", "message": "Explain the tides.", "text": "The moon.", "breaches": {"d-judge": 0}, "done": True}]}
CHECKS = [{"compares": compares, "gap": 1.0} for compares in ("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion")]
GATE = {"repeats": 2, "level": 0.95, "done_by": "judge", "checks": CHECKS, "keep_rule": "best-estimate-shortest", "budget": "none"}
AGENT_READER = {"kind": "agent", "model": "claude-sonnet-4-5"}
COMMAND_READER = {"kind": "command", "model": "local-7b", "command": ["run", "{condition}"], "fingerprint": ["fingerprint"], "sampling": {"temperature": 0}}
FINGERPRINT_HASH = "f" * 64
NULL_COST = dict.fromkeys(("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "spent_input_tokens"))
ATTEMPT = "6-judge/calibration/attempt-1"
REPLY_COST = {"input_tokens": 4, "cache_creation_input_tokens": 3, "cache_read_input_tokens": 3, "output_tokens": 5, "spent_input_tokens": 10}
COLLECTED_PACKET = {
    "accepted": 1,
    "judge_model": "claude-opus-4-1",
    "transcript": "/tmp/transcripts/judge.jsonl",
    "transcript_hash": "a" * 64,
    "anchors": {"breach_difference": {"d-judge": 0.0}, "done_agreement": 1.0},
}
FROZEN_AT = datetime(2026, 10, 15, 9, 30, tzinfo=timezone.utc)
TOOL_VERSION = "0.1.0"


def unbreached_first_replies() -> list[Reply]:
    """Build r1's replies: every task at both repeats under every condition, none breaching."""
    pairs = [(condition, task, repeat) for condition in CONDITION_NAMES for task in TASKS["tasks"] for repeat in (1, 2)]
    return [Reply(f"b{index:08x}", condition, task["id"], repeat=repeat, split=task["split"]) for index, (condition, task, repeat) in enumerate(pairs, 1)]


def reader_reply_record(reply: Reply, reader_kind: str) -> dict:
    """Return the reply record of a fixture reply by a reader of the kind."""
    task = next(task for task in TASKS["tasks"] if task["id"] == reply.task)
    record = {
        "condition": reply.condition,
        "task": reply.task,
        "split": reply.split,
        "repeat": reply.repeat,
        "message": task["message"],
        "text": "An answer.",
        "model": "claude-sonnet-4-5",
        "reader_kind": reader_kind,
        "started": "2026-10-14T10:00:00+00:00",
        "seconds": 1.5,
    }
    if reader_kind == "agent":
        return {**record, "transcript": "/tmp/transcripts/reader.jsonl", "transcript_hash": "a" * 64, "cost": REPLY_COST}
    return {**record, "fingerprint_hash": FINGERPRINT_HASH, "cost": NULL_COST}


def write_measured_first_revision(files: SeriesFolder, replies: list[Reply], reader_kind: str) -> None:
    """Write r1's condition texts, replies, origins, accepted verdicts, collection, and detector counts, each packet carrying one anchor."""
    for condition in CONDITION_NAMES:
        write_file(files, f"r1/4-conditions/{condition}.md", condition.encode())
    for reply in replies:
        write_record(files, reply_path("r1", reply.condition, reply.task, reply.repeat, None), reader_reply_record(reply, reader_kind), [])
    anchor_ids = write_origins(files, "r1", replies, "a-one")
    for packet, anchor_id in anchor_ids.items():
        entries = [{"id": reply.id, "breaches": {"d-judge": reply.judged}, "done": reply.done, "kind": "answer", "notes": ""} for reply in replies if reply.packet == packet]
        anchor_entry = {"id": anchor_id, "breaches": {"d-judge": 0}, "done": True, "kind": "answer", "notes": ""}
        write_yaml(files, f"r1/7-verdicts/{packet}/k1.yaml", {"verdicts": [*entries, anchor_entry]})
    write_record(files, "r1/7-collected.yaml", {"packets": dict.fromkeys(anchor_ids, COLLECTED_PACKET)}, [])
    answer_keys = {task["id"]: task["answer_key"] for task in TASKS["tasks"]}
    detectors = [{"id": reply.id, "breaches": {"d-hedge": reply.hedges}, "done_by_answer_key": True if answer_keys[reply.task] else None} for reply in replies]
    write_record(files, "r1/7-detectors.yaml", {"verdicts": detectors}, [])


def ready_series(tmp_path: Path, replies: list[Reply] | None = None, gate: dict = GATE, reader: dict = AGENT_READER) -> SeriesFolder:
    """Write a series whose r1 is asked, collected, calibrated, blinded, judged, and detected, and whose gate is complete."""
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", {"instruction": "/tmp/terse.md", "sources": [], "reader_kind": reader["kind"], "binding": SERIES_BINDING, "created": "2026-10-14T10:00:00+00:00"}, [])
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_file(files, "4-placebo-source.md", PLACEBO)
    write_yaml(files, "5-reader.yaml", reader)
    write_file(files, "6-judge/brief.md", b"The working brief.\n")
    write_yaml(files, f"{ATTEMPT}/plan.yaml", {"sample_size": 4})
    write_yaml(files, f"{ATTEMPT}/reference-user.yaml", {"verdicts": []})
    write_file(files, f"{ATTEMPT}/brief.md", b"The brief snapshot.\n")
    write_record(files, "6-judge/calibration.yaml", {"attempt": 1}, [])
    write_record(files, "6-judge/anchors.yaml", ANCHORS, [])
    write_yaml(files, "7-gate.yaml", gate)
    write_file(files, "r1/2-instruction.md", INSTRUCTION)
    write_record(files, "r1/2-revision.yaml", {"number": 1, "parent": None, "hash": sha256(INSTRUCTION), "parent_record": None, "change": None}, [])
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    write_measured_first_revision(files, unbreached_first_replies() if replies is None else replies, reader["kind"])
    write_file(files, ".claude/agents/ie-reader-r1-instruction.md", b"definition")
    return files


def freeze(files: SeriesFolder, fingerprint_hash: str | None = None) -> None:
    """Run `series freeze` at the fixed time and tool version."""
    series_freeze(files, fingerprint_hash, read_nothing, bootstrap_rng, TOOL_VERSION, FROZEN_AT)


def series_files(files: SeriesFolder) -> list[str]:
    """Return the series path of every file in the folder."""
    return sorted(path.relative_to(files.root).as_posix() for path in files.root.rglob("*") if path.is_file())


def test_a_ready_series_freezes_hashing_every_series_file_but_the_working_brief_and_agent_definitions_with_its_noise_version_and_time(tmp_path):
    files = ready_series(tmp_path)
    present = series_files(files)

    freeze(files)

    frozen = SeriesRecords(files).frozen()
    hashed = [path for path in present if path != "6-judge/brief.md" and not path.startswith(".claude/")]
    assert frozen["hashes"] == {path: sha256(files.read_bytes(path)) for path in hashed}
    assert set(frozen["noise"]) == {"repeats", "level", "z", "sigma", "checks", "demands", "done_change"}
    assert frozen["noise"]["checks"] == dict.fromkeys(("instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion"), 0.0)
    assert frozen["tool_version"] == TOOL_VERSION
    assert frozen["frozen_at"] == "2026-10-15T09:30:00+00:00"
    assert "fingerprint_hash" not in frozen


def test_a_file_outside_the_series_parts_is_neither_hashed_nor_read(tmp_path):
    files = ready_series(tmp_path)
    write_file(files, "notes.md", b"Scratch notes.\n")

    freeze(files)

    frozen = SeriesRecords(files).frozen()
    assert "notes.md" not in frozen["hashes"]
    assert "notes.md" not in frozen["inputs"]


def test_a_command_reader_series_records_the_fresh_fingerprint_hash(tmp_path):
    files = ready_series(tmp_path, reader=COMMAND_READER)

    freeze(files, FINGERPRINT_HASH)

    assert SeriesRecords(files).frozen()["fingerprint_hash"] == FINGERPRINT_HASH


def noisy_instruction_replies() -> list[Reply]:
    """Build r1's replies with the instruction's second repeat of every sealed task breaching three times, so its repeats disagree."""
    return [replace(reply, judged=3) if reply.condition == "instruction" and reply.split == "sealed" and reply.repeat == 2 else reply for reply in unbreached_first_replies()]


def test_a_gap_the_noise_cannot_resolve_refuses_naming_the_checks_and_the_least_repeats_and_writes_nothing(tmp_path):
    files = ready_series(tmp_path, noisy_instruction_replies())
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^unresolvable gap: instruction-vs-empty \(noise 1\.69738 > gap / 2 0\.5\), .*; least repeats 24$"):
        freeze(files)

    assert tree(files.root) == before


def test_a_budget_ceiling_below_the_predicted_cost_refuses_and_writes_nothing(tmp_path):
    files = ready_series(tmp_path, gate={**GATE, "budget": {"unit": "tokens", "ceiling": 1000}})
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^predicted cost 1440 exceeds ceiling 1000$"):
        freeze(files)

    assert tree(files.root) == before


def test_a_budget_ceiling_at_the_predicted_cost_freezes(tmp_path):
    files = ready_series(tmp_path, gate={**GATE, "budget": {"unit": "tokens", "ceiling": 1440}})

    freeze(files)

    assert files.holds("8-frozen.yaml")


USER_RECORD_KEYS = {
    "2-demands.yaml": DEMANDS,
    "3-tasks.yaml": TASKS,
    "4-conditions.yaml": CONDITIONS,
    "5-reader.yaml": AGENT_READER,
    f"{ATTEMPT}/plan.yaml": {"sample_size": 4},
    f"{ATTEMPT}/reference-user.yaml": {"verdicts": []},
    "7-gate.yaml": GATE,
    "r1/3-coverage.yaml": COVERAGE,
}


def test_the_freeze_names_as_inputs_every_file_it_reads_each_user_record_by_key(tmp_path):
    files = ready_series(tmp_path)
    present = series_files(files)

    freeze(files)

    whole = {path for path in present if path not in USER_RECORD_KEYS and path != "6-judge/brief.md" and not path.startswith(".claude/")}
    by_key = {f"{path}#{key}" for path, document in USER_RECORD_KEYS.items() for key in document}
    assert set(SeriesRecords(files).frozen()["inputs"]) == whole | by_key


def test_tasks_freeze_with_the_series_so_a_task_edited_after_freeze_refuses_the_next_command(tmp_path):
    files = ready_series(tmp_path)
    freeze(files)
    write_yaml(files, "3-tasks.yaml", {**TASKS, "tasks": [{**TASKS["tasks"][0], "message": "Explain the waves."}, *TASKS["tasks"][1:]]})

    with pytest.raises(Refusal, match=r"^stale: 8-frozen\.yaml \(input 3-tasks\.yaml#tasks changed\)$"):
        freeze(files)


def test_a_task_file_changed_after_freeze_in_bytes_alone_refuses_the_next_command(tmp_path):
    files = ready_series(tmp_path)
    freeze(files)
    (files.root / "3-tasks.yaml").write_bytes(files.read_bytes("3-tasks.yaml") + b"# reworded\n")

    with pytest.raises(Refusal, match=r"^frozen part changed: 3-tasks\.yaml$"):
        freeze(files)


def test_a_series_not_ready_to_freeze_refuses_and_writes_nothing(tmp_path):
    files = ready_series(tmp_path)
    (files.root / "6-judge/calibration.yaml").unlink()
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^no 6-judge/calibration\.yaml$"):
        freeze(files)

    assert tree(files.root) == before


def test_a_first_revision_whose_sealed_instruction_replies_hold_no_done_refuses_its_null_done_change_noise(tmp_path):
    replies = [replace(reply, done=None) if reply.condition == "instruction" and reply.split == "sealed" else reply for reply in unbreached_first_replies()]
    files = ready_series(tmp_path, replies)

    with pytest.raises(Refusal, match=r"^null noise: done_change$"):
        freeze(files)

    assert not files.holds("8-frozen.yaml")
