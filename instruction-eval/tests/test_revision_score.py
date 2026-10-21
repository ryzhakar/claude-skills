from collections.abc import Sequence

import pytest

from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, write_file, write_record
from instruction_eval.scores import revision_score
from series_fixtures import Reply, bootstrap_rng, write_agent_series, write_origins, write_yaml

DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
        {"id": "d-dropped", "text": "Cite sources.", "boundary": "None.", "counted_by": "judge"},
    ]
}
COVERAGE = {
    "demands": {"d-judge": [1], "d-hedge": [1], "d-dropped": {"dropped": "Unmeasured here."}},
    "sentences": {1: ["d-judge", "d-hedge"]},
}
TASKS = {
    "tasks": [
        {"id": "t1", "tempts": "d-judge", "split": "open", "message": "Explain tides.", "answer_key": None},
        {"id": "t2", "tempts": "d-hedge", "split": "open", "message": "Explain rain.", "answer_key": "water"},
        {"id": "t3", "tempts": "d-judge", "split": "sealed", "message": "Explain snow.", "answer_key": None},
    ],
    "conversations": [
        {"id": "c1", "split": "open", "turns": ["Plan a trip.", "Which week?", "Which day?"]},
        {"id": "c2", "split": "open", "turns": ["Plan a meal.", "Which wine?", "Which cheese?"]},
    ],
}
CONDITIONS = ("instruction", "empty", "aim", "placebo", "source")
ANCHORS = {
    "anchors": [
        {"id": "a-one", "task": "t3", "message": "Explain snow.", "text": "Cold rain.", "breaches": {"d-judge": 0, "d-dropped": 0}, "done": True}
    ]
}
COLLECTED_PACKET = {
    "accepted": 1,
    "judge_model": "claude-opus-4-1",
    "transcript": "/tmp/transcripts/judge.jsonl",
    "transcript_hash": "a" * 64,
    "anchors": {"breach_difference": {"d-judge": 0.0}, "done_agreement": 1.0},
}


def write_scored_series(files: SeriesFolder, gate: dict) -> None:
    """Write the series records every revision of the fixture shares."""
    write_agent_series(files, DEMANDS, TASKS, ANCHORS)
    write_yaml(files, "7-gate.yaml", gate)
    write_yaml(files, "r1/3-coverage.yaml", COVERAGE)
    for condition in CONDITIONS:
        write_file(files, f"r1/4-conditions/{condition}.md", condition.encode())


def write_judged_revision(files: SeriesFolder, revision: str, replies: Sequence[Reply]) -> None:
    """Write the revision's reply files, origins, accepted verdicts, collection, and detector counts, each packet carrying one anchor."""
    for reply in replies:
        if reply.borrowed_from is None:
            write_file(files, reply.path_in(revision), f"reply {reply.id}".encode())
    anchor_ids = write_origins(files, revision, replies, "a-one")
    for packet, anchor_id in anchor_ids.items():
        entries = [
            {"id": reply.id, "breaches": {"d-judge": reply.judged, "d-dropped": reply.dropped}, "done": reply.done, "kind": reply.kind, "notes": ""}
            for reply in replies
            if reply.packet == packet
        ]
        anchor_entry = {"id": anchor_id, "breaches": {"d-judge": 0, "d-dropped": 0}, "done": True, "kind": "answer", "notes": ""}
        write_yaml(files, f"{revision}/7-verdicts/{packet}/k1.yaml", {"verdicts": [*entries, anchor_entry]})
    write_record(files, f"{revision}/7-collected.yaml", {"packets": dict.fromkeys(anchor_ids, COLLECTED_PACKET)}, [])
    detectors = [{"id": reply.id, "breaches": {"d-hedge": reply.hedges}, "done_by_answer_key": reply.key} for reply in replies]
    write_record(files, f"{revision}/7-detectors.yaml", {"verdicts": detectors}, [])


def scored_series(tmp_path, replies: Sequence[Reply], done_by: str = "judge") -> SeriesFolder:
    """Write a series whose r1 holds the replies, with the gate's level and done mode."""
    files = SeriesFolder(tmp_path)
    write_scored_series(files, {"repeats": 2, "level": 0.95, "done_by": done_by})
    write_judged_revision(files, "r1", replies)
    return files


def read_scores(files: SeriesFolder, revision: str = "r1") -> dict:
    """Read the scores record through the series loader."""
    return SeriesRecords(files).scores(revision)


def score_reads(revision: str, replies: Sequence[Reply]) -> set[str]:
    """Return the Commands-table reads of `revision score` expanded for the revision's replies."""
    packets = {reply.packet for reply in replies}
    return {
        "2-demands.yaml#demands",
        "3-tasks.yaml#tasks",
        "3-tasks.yaml#conversations",
        "r1/3-coverage.yaml#demands",
        "r1/3-coverage.yaml#sentences",
        "7-gate.yaml#level",
        "7-gate.yaml#done_by",
        *(reply.path_in(revision) for reply in replies),
        f"{revision}/6-origins.yaml",
        *(f"{revision}/7-verdicts/{packet}/k1.yaml" for packet in packets),
        f"{revision}/7-collected.yaml",
        f"{revision}/7-detectors.yaml",
    }


def test_the_scores_hold_open_rows_only_and_name_no_sealed_blind_id(tmp_path):
    replies = [
        Reply("b00000001", "instruction", "t1", judged=1, hedges=2, dropped=3),
        Reply("b00000002", "instruction", "t3", split="sealed"),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    scores = read_scores(files)
    assert scores["split"] == "open"
    assert scores["rows"] == [
        {
            "id": "b00000001",
            "condition": "instruction",
            "task": "t1",
            "repeat": 1,
            "turn": None,
            "borrowed_from": None,
            "breaches": {"d-judge": 1, "d-dropped": 3, "d-hedge": 2},
            "kind": "answer",
            "done_by_answer_key": None,
            "done_by_judge": True,
            "done": True,
        }
    ]
    assert b"b00000002" not in files.read_bytes("r1/8-scores.yaml")
    assert set(scores["inputs"]) == score_reads("r1", replies)


def test_each_condition_scores_its_single_task_replies_summing_gate_demands_and_reporting_a_dropped_demand_apart(tmp_path):
    replies = [
        Reply("b00000001", "instruction", "t1", repeat=1, judged=1, hedges=1, dropped=4),
        Reply("b00000002", "instruction", "t1", repeat=2, done=None, kind="probe"),
        Reply("b00000003", "instruction", "t2", judged=2, done=False),
        Reply("b00000004", "instruction", "c1", turn=1, judged=9, hedges=9, dropped=9, kind="blank"),
        Reply("b00000005", "empty", "t1"),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    by_condition = read_scores(files)["by_condition"]
    assert by_condition == {
        "instruction": {
            "breaches_per_reply": pytest.approx(4 / 3),
            "demands": {"d-judge": 1.0, "d-dropped": pytest.approx(4 / 3), "d-hedge": pytest.approx(1 / 3)},
            "done_rate": 0.5,
            "kinds": {"answer": 2, "probe": 1},
        },
        "empty": {"breaches_per_reply": 0.0, "demands": {"d-judge": 0.0, "d-dropped": 0.0, "d-hedge": 0.0}, "done_rate": 1.0, "kinds": {"answer": 1}},
    }


def per_task_replies(condition: str, judged: dict[str, tuple[int, int]], start: int, **reply_keys) -> list[Reply]:
    """Build two repeats per task under the condition, each repeat breaching `d-judge` as given, blind ids counted from `start`."""
    return [
        Reply(f"b{start + index:08x}", condition, task, repeat=repeat, judged=breaches, **reply_keys)
        for index, (task, repeat, breaches) in enumerate(
            (task, repeat, breaches) for task, pair in judged.items() for repeat, breaches in enumerate(pair, 1)
        )
    ]


def test_each_vs_comparison_averages_instruction_minus_its_control_per_task_with_a_bootstrap_interval_and_a_sign(tmp_path):
    replies = [
        *per_task_replies("instruction", {"t1": (0, 0), "t2": (1, 1)}, 0x10),
        *per_task_replies("empty", {"t1": (2, 2), "t2": (3, 3)}, 0x20),
        *per_task_replies("aim", {"t1": (0, 0), "t2": (1, 1)}, 0x30),
        *per_task_replies("placebo", {"t1": (1, 3), "t2": (1, 1)}, 0x40, dropped=7),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    comparisons = read_scores(files)["comparisons"]
    assert set(comparisons) == {"instruction-vs-empty", "instruction-vs-aim", "instruction-vs-placebo", "completion"}
    assert comparisons["instruction-vs-empty"] == {"mean_difference": -2.0, "interval": [-2.0, -2.0], "units": 2}
    assert comparisons["instruction-vs-aim"] == {"mean_difference": 0.0, "interval": [0.0, 0.0], "units": 2}
    assert comparisons["instruction-vs-placebo"] == {"mean_difference": -1.0, "interval": [-2.0, 0.0], "units": 2}


def per_task_done(condition: str, done: dict[str, tuple[bool | None, bool | None]], start: int) -> list[Reply]:
    """Build two repeats per task under the condition with the given done values, blind ids counted from `start`."""
    return [
        Reply(f"b{start + index:08x}", condition, task, repeat=repeat, done=value)
        for index, (task, repeat, value) in enumerate(
            (task, repeat, value) for task, pair in done.items() for repeat, value in enumerate(pair, 1)
        )
    ]


def test_completion_compares_done_rates_with_the_best_done_control_over_tasks_both_hold_a_done_for(tmp_path):
    replies = [
        *per_task_done("instruction", {"t1": (True, False), "t2": (None, None)}, 0x10),
        *per_task_done("empty", {"t1": (True, True), "t2": (True, True)}, 0x20),
        *per_task_done("aim", {"t1": (False, False), "t2": (False, False)}, 0x30),
        *per_task_done("placebo", {"t1": (None, None), "t2": (True, False)}, 0x40),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    assert read_scores(files)["comparisons"]["completion"] == {"mean_difference": -0.5, "interval": [-0.5, -0.5], "units": 1}


def test_completion_without_a_task_both_hold_a_done_for_has_no_mean_no_interval_and_a_null_done_rate(tmp_path):
    replies = [
        *per_task_done("instruction", {"t1": (None, None), "t2": (None, None)}, 0x10),
        *per_task_done("empty", {"t1": (True, True), "t2": (True, True)}, 0x20),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    scores = read_scores(files)
    assert scores["comparisons"]["completion"] == {"mean_difference": None, "interval": None, "units": 0}
    assert scores["by_condition"]["instruction"]["done_rate"] is None


def test_a_series_with_a_source_compares_instruction_near_source_and_no_vs_source(tmp_path):
    replies = [
        *per_task_replies("instruction", {"t1": (0, 0), "t2": (0, 0)}, 0x10),
        *per_task_replies("empty", {"t1": (2, 2), "t2": (2, 2)}, 0x20),
        *per_task_replies("source", {"t1": (1, 1), "t2": (1, 1)}, 0x30),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    comparisons = read_scores(files)["comparisons"]
    assert set(comparisons) == {"instruction-vs-empty", "instruction-near-source", "completion"}
    assert comparisons["instruction-near-source"] == {"mean_difference": -1.0, "interval": [-1.0, -1.0], "units": 2}


def per_turn_replies(condition: str, judged: dict[str, tuple[int, int, int]], start: int) -> list[Reply]:
    """Build two repeats of each three-turn conversation under the condition, each repeat breaching `d-judge` per turn as given."""
    return [
        Reply(f"b{start + index:08x}", condition, conversation, repeat=repeat, turn=turn, judged=breaches)
        for index, (conversation, repeat, turn, breaches) in enumerate(
            (conversation, repeat, turn, breaches)
            for conversation, per_turn in judged.items()
            for repeat in (1, 2)
            for turn, breaches in enumerate(per_turn, 1)
        )
    ]


def test_drift_is_each_conversations_breach_slope_over_turns_compared_with_empty_without_a_source_and_moves_nothing_else(tmp_path):
    replies = [
        *per_task_replies("instruction", {"t1": (1, 1)}, 0x10),
        *per_task_replies("empty", {"t1": (1, 1)}, 0x20),
        *per_turn_replies("instruction", {"c1": (0, 1, 2), "c2": (5, 5, 5)}, 0x100),
        *per_turn_replies("empty", {"c1": (0, 0, 0), "c2": (0, 0, 0)}, 0x200),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    scores = read_scores(files)
    assert scores["drift"] == {
        "instruction": {"slope": 0.5, "interval": [0.0, 1.0]},
        "empty": {"slope": 0.0, "interval": [0.0, 0.0]},
    }
    assert scores["comparisons"]["drift"] == {"mean_difference": 0.5, "interval": [0.0, 1.0], "units": 2}
    assert scores["comparisons"]["instruction-vs-empty"]["mean_difference"] == 0.0
    assert scores["by_condition"]["instruction"]["breaches_per_reply"] == 1.0


def test_drift_compares_instruction_with_source_when_the_series_has_one(tmp_path):
    replies = [
        *per_task_replies("instruction", {"t1": (1, 1)}, 0x10),
        *per_task_replies("empty", {"t1": (1, 1)}, 0x20),
        *per_task_replies("source", {"t1": (1, 1)}, 0x30),
        *per_turn_replies("instruction", {"c1": (0, 1, 2), "c2": (0, 1, 2)}, 0x100),
        *per_turn_replies("empty", {"c1": (0, 1, 2), "c2": (0, 1, 2)}, 0x200),
        *per_turn_replies("source", {"c1": (0, 0, 0), "c2": (0, 0, 0)}, 0x300),
    ]
    files = scored_series(tmp_path, replies)

    revision_score(files, "r1", bootstrap_rng)

    assert read_scores(files)["comparisons"]["drift"] == {"mean_difference": 1.0, "interval": [1.0, 1.0], "units": 2}


DONE_MODE_REPLIES = [
    Reply("b00000001", "instruction", "t1", done=True, key=None),
    Reply("b00000002", "instruction", "t2", done=True, key=False),
    Reply("b00000003", "instruction", "t2", repeat=2, done=False, key=False),
]


@pytest.mark.parametrize(("done_by", "dones"), [("answer-key", [True, False, False]), ("judge", [True, True, False])])
def test_done_follows_the_done_mode_with_key_and_judge_side_by_side_and_disagreements_listed(tmp_path, done_by, dones):
    files = scored_series(tmp_path, DONE_MODE_REPLIES, done_by=done_by)

    revision_score(files, "r1", bootstrap_rng)

    scores = read_scores(files)
    assert [row["done"] for row in scores["rows"]] == dones
    assert [(row["done_by_answer_key"], row["done_by_judge"]) for row in scores["rows"]] == [(None, True), (False, True), (False, False)]
    assert scores["disagreements"] == ["b00000002"]


def test_a_later_revision_scores_its_own_instruction_against_control_rows_borrowed_from_r1(tmp_path):
    files = SeriesFolder(tmp_path)
    write_scored_series(files, {"repeats": 2, "level": 0.95, "done_by": "judge"})
    first = [Reply("b00000001", "instruction", "t1", judged=3), Reply("b00000002", "empty", "t1", judged=2)]
    write_judged_revision(files, "r1", first)
    write_file(files, "r2/4-conditions/instruction.md", b"instruction")
    later = [Reply("b00000011", "instruction", "t1", judged=0), Reply("b00000012", "empty", "t1", judged=2, borrowed_from="r1")]
    write_judged_revision(files, "r2", later)

    revision_score(files, "r2", bootstrap_rng)

    scores = read_scores(files, "r2")
    assert [(row["condition"], row["borrowed_from"]) for row in scores["rows"]] == [("instruction", None), ("empty", "r1")]
    assert scores["comparisons"]["instruction-vs-empty"]["mean_difference"] == -2.0
    assert set(scores["inputs"]) == score_reads("r2", later)
    assert "r1/5-replies/empty/t1/repeat-1.yaml" in scores["inputs"]


@pytest.mark.parametrize("key", ["level", "done_by"])
def test_a_gate_without_the_level_or_done_mode_refuses_writing_nothing(tmp_path, key):
    files = SeriesFolder(tmp_path)
    gate = {"repeats": 2, "level": 0.95, "done_by": "judge"}
    del gate[key]
    write_scored_series(files, gate)
    write_judged_revision(files, "r1", [Reply("b00000001", "instruction", "t1")])

    with pytest.raises(Refusal, match=rf"^missing key: 7-gate\.yaml#{key}$"):
        revision_score(files, "r1", bootstrap_rng)
    assert not files.holds("r1/8-scores.yaml")


def test_a_revision_already_scored_refuses_a_second_score(tmp_path):
    files = scored_series(tmp_path, [Reply("b00000001", "instruction", "t1")])
    revision_score(files, "r1", bootstrap_rng)

    with pytest.raises(Refusal, match=r"^already written: r1/8-scores\.yaml$"):
        revision_score(files, "r1", bootstrap_rng)
