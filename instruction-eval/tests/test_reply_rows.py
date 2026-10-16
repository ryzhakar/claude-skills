from instruction_eval.scores import join_reply_rows, measure_noise

HASH = "a" * 64


def origin(task: str, split: str, condition: str = "instruction", repeat: int = 1, turn: int | None = None, borrowed_from: str | None = None) -> dict:
    """Build a reply origin whose packet is its task's, or its turn's packet for a conversation turn."""
    packet = task if turn is None else f"{task}-turn-{turn}"
    reply_origin = {"packet": packet, "condition": condition, "task": task, "split": split, "repeat": repeat}
    if turn is not None:
        reply_origin["turn"] = turn
    return {**reply_origin, "borrowed_from": borrowed_from}


def judged(blind_id: str, breaches: dict[str, int], done: bool | None, kind: str = "answer") -> dict:
    """Build one judge verdict entry."""
    return {"id": blind_id, "breaches": breaches, "done": done, "kind": kind, "notes": ""}


def detected(blind_id: str, breaches: dict[str, int], done_by_answer_key: bool | None) -> dict:
    """Build one detector entry."""
    return {"id": blind_id, "breaches": breaches, "done_by_answer_key": done_by_answer_key}


def test_judge_mode_row_joins_origin_verdict_and_detector_with_the_judges_done():
    origins = {
        "ids": {"b00000001": origin("t1", "open", borrowed_from="r1"), "b00000002": {"packet": "t1", "anchor": "a1"}},
        "packets": {"t1": HASH},
    }
    verdicts = [{"verdicts": [judged("b00000001", {"d-judge": 2}, True), judged("b00000002", {"d-judge": 0}, False)]}]
    detectors = {"verdicts": [detected("b00000001", {"d-pattern": 1}, False)]}

    rows = join_reply_rows(origins, verdicts, detectors, done_by="judge", split="open")

    assert rows == [
        {
            "id": "b00000001",
            "condition": "instruction",
            "task": "t1",
            "repeat": 1,
            "turn": None,
            "borrowed_from": "r1",
            "breaches": {"d-judge": 2, "d-pattern": 1},
            "kind": "answer",
            "done_by_answer_key": False,
            "done_by_judge": True,
            "done": True,
        }
    ]


def test_answer_key_mode_takes_the_key_verdict_where_the_task_has_a_key_and_the_judges_elsewhere():
    origins = {
        "ids": {
            "b00000001": origin("t-keyed", "sealed"),
            "b00000002": origin("t-keyed", "sealed", repeat=2),
            "b00000003": origin("t-keyless", "sealed"),
        },
        "packets": {"t-keyed": HASH, "t-keyless": HASH},
    }
    verdicts = [
        {"verdicts": [judged("b00000001", {}, False, kind="probe"), judged("b00000002", {}, True)]},
        {"verdicts": [judged("b00000003", {}, False)]},
    ]
    detectors = {
        "verdicts": [detected("b00000001", {}, True), detected("b00000002", {}, False), detected("b00000003", {}, None)]
    }

    rows = join_reply_rows(origins, verdicts, detectors, done_by="answer-key", split="sealed")

    assert [(row["id"], row["done_by_answer_key"], row["done_by_judge"], row["done"]) for row in rows] == [
        ("b00000001", True, False, True),
        ("b00000002", False, True, False),
        ("b00000003", None, False, False),
    ]


def test_rows_of_a_split_carry_each_turn_reply_with_its_turn_beside_task_replies():
    origins = {
        "ids": {
            "b00000001": origin("t1", "sealed"),
            "b00000002": origin("c1", "sealed", turn=1),
            "b00000003": origin("c1", "sealed", turn=2),
            "b00000004": origin("t2", "open"),
        },
        "packets": {"t1": HASH, "c1-turn-1": HASH, "c1-turn-2": HASH, "t2": HASH},
    }
    verdicts = [
        {"verdicts": [judged("b00000001", {}, True)]},
        {"verdicts": [judged("b00000002", {}, True)]},
        {"verdicts": [judged("b00000003", {}, True)]},
        {"verdicts": [judged("b00000004", {}, True)]},
    ]
    detectors = {"verdicts": [detected(f"b0000000{index}", {}, None) for index in range(1, 5)]}

    rows = join_reply_rows(origins, verdicts, detectors, done_by="judge", split="sealed")

    assert [(row["task"], row["turn"]) for row in rows] == [("t1", None), ("c1", 1), ("c1", 2)]


def test_a_dropped_demand_stays_measured_in_the_row_while_noise_sums_gate_demands_alone():
    origins = {
        "ids": {
            "b00000001": origin("t1", "sealed", repeat=1),
            "b00000002": origin("t1", "sealed", repeat=2),
        },
        "packets": {"t1": HASH},
    }
    verdicts = [{"verdicts": [judged("b00000001", {"d-gate": 1, "d-dropped": 0}, True), judged("b00000002", {"d-gate": 1, "d-dropped": 9}, True)]}]
    detectors = {"verdicts": [detected("b00000001", {}, None), detected("b00000002", {}, None)]}

    rows = join_reply_rows(origins, verdicts, detectors, done_by="judge", split="sealed")

    assert [row["breaches"]["d-dropped"] for row in rows] == [0, 9]
    assert measure_noise(rows, ["d-gate"], ["empty", "aim", "placebo"], repeats=2, level=0.95)["sigma"]["breaches"]["instruction"] == 0
