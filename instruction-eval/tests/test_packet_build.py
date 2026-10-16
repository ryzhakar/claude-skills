import random
import re
from collections import Counter

import pytest

from instruction_eval.judge import blind_replies
from instruction_eval.records import Refusal
from instruction_eval.tasks import ExpectedReply

ANCHORS = [
    {"id": f"a-{task}", "task": task, "message": f"Ask {task}.", "text": f"Known reply to {task}.", "breaches": {"d-terse": 0}, "done": True}
    for task in ("t-one", "t-two", "t-three", "t-four")
]
TURNS = ("Plan a trip.", "Which week?")


def reply(revision: str, condition: str, task: str, repeat: int, turn: int | None = None) -> tuple[ExpectedReply, dict]:
    message = TURNS[turn - 1] if turn else f"Explain {task}."
    record = {"condition": condition, "task": task, "split": "open", "repeat": repeat, "message": message, "text": f"{condition} {task} {repeat} {turn} reply."}
    if turn:
        record["turn"] = turn
    return ExpectedReply(revision, condition, task, repeat, turn), record


REPLIES = dict(
    [
        *(reply("r2", "instruction", "t-one", repeat) for repeat in (1, 2)),
        *(reply("r1", "empty", "t-one", repeat) for repeat in (1, 2)),
        *(reply("r2", "omit-1", "t-one", repeat) for repeat in (1, 2)),
        *(reply("r2", "instruction", "c-trip", repeat, turn) for repeat in (1, 2) for turn in (1, 2)),
    ]
)


def blind(anchors: list[dict] = ANCHORS, anchors_per_packet: int = 3):
    return blind_replies("r2", REPLIES, anchors, anchors_per_packet, random.Random(7))


def sections(packet: str) -> dict[str, str]:
    parts = re.split(r"^## (b[0-9a-f]{8})\n", packet, flags=re.MULTILINE)
    assert parts[0] == ""
    return {blind_id: body.strip() for blind_id, body in zip(parts[1::2], parts[2::2])}


def test_replies_go_to_one_gate_packet_per_task_and_per_conversation_turn_and_omissions_to_one_packet_per_task():
    packets = blind()
    assert sorted(packets.packets) == ["c-trip-turn-1", "c-trip-turn-2", "t-one", "t-one--omissions"]
    held = Counter(origin["packet"] for origin in packets.origins.values() if "anchor" not in origin)
    assert held == {"t-one": 4, "t-one--omissions": 2, "c-trip-turn-1": 2, "c-trip-turn-2": 2}


def test_each_packet_holds_one_section_per_blind_id_it_owns_and_every_blind_id_is_unique_in_the_revision():
    packets = blind()
    for packet_id, packet in packets.packets.items():
        assert sorted(sections(packet)) == sorted(blind_id for blind_id, origin in packets.origins.items() if origin["packet"] == packet_id)
    assert all(re.fullmatch(r"b[0-9a-f]{8}", blind_id) for blind_id in packets.origins)


def test_every_packet_adds_the_set_number_of_anchors_from_other_tasks_only():
    packets = blind()
    for packet_id in packets.packets:
        anchors = [origin["anchor"] for origin in packets.origins.values() if origin["packet"] == packet_id and "anchor" in origin]
        assert len(anchors) == 3
        assert len(set(anchors)) == 3
        if packet_id.startswith("t-one"):
            assert "a-t-one" not in anchors


def test_an_origin_records_the_reply_and_names_the_revision_it_borrows_from():
    origins = blind().origins.values()
    assert {"packet": "t-one", "condition": "empty", "task": "t-one", "split": "open", "repeat": 2, "borrowed_from": "r1"} in origins
    assert {"packet": "t-one", "condition": "instruction", "task": "t-one", "split": "open", "repeat": 1, "borrowed_from": None} in origins
    assert {"packet": "c-trip-turn-2", "condition": "instruction", "task": "c-trip", "split": "open", "repeat": 1, "turn": 2, "borrowed_from": None} in origins


def test_a_turn_entry_carries_the_earlier_turns_and_replies_of_its_repeat_before_its_own_message_and_reply():
    packets = blind()
    blind_id = next(blind_id for blind_id, origin in packets.origins.items() if origin.get("turn") == 2 and origin["repeat"] == 1)
    assert sections(packets.packets["c-trip-turn-2"])[blind_id] == (
        "### User\n\nPlan a trip.\n\n### Reply\n\ninstruction c-trip 1 1 reply.\n\n"
        "### User\n\nWhich week?\n\n### Reply\n\ninstruction c-trip 1 2 reply."
    )


def test_an_anchor_entry_carries_the_anchor_message_and_text():
    packets = blind()
    blind_id, origin = next((blind_id, origin) for blind_id, origin in packets.origins.items() if origin.get("anchor") == "a-t-two")
    assert sections(packets.packets[origin["packet"]])[blind_id] == "### User\n\nAsk t-two.\n\n### Reply\n\nKnown reply to t-two."


def test_a_packet_with_fewer_anchors_of_other_tasks_than_the_set_number_is_refused():
    with pytest.raises(Refusal, match="^too few anchors for t-one$"):
        blind(anchors=ANCHORS[:3])


class RepeatingRandom(random.Random):
    def getrandbits(self, bits: int) -> int:
        return 0


def test_a_random_source_that_keeps_drawing_taken_blind_ids_is_refused_rather_than_drawn_forever():
    with pytest.raises(Refusal, match="^no free blind id$"):
        blind_replies("r2", REPLIES, ANCHORS, 3, RepeatingRandom(7))
