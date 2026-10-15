import hashlib
import hashlib
import json
from pathlib import Path

import pytest
import yaml

from instruction_eval.judge import AcceptedJudging, AnchorAgreement, AnchorAgreement, NeedsJudging, PendingJudging, judging_states
from instruction_eval.reader import Transcript
from instruction_eval.records import Refusal, SeriesFolder, write_file, write_record
from series_fixtures import write_agent_series, write_yaml

JUDGE_MODEL = "claude-opus-4-1"
OTHER_MODEL = "claude-sonnet-5-5"
PACKETS = ("t1", "t1--omissions")
REPLY_IDS = {"t1": "b0000001a", "t1--omissions": "b0000002a"}
ANCHOR_IDS = {"t1": "b0000001b", "t1--omissions": "b0000002b"}
DEMANDS = {
    "demands": [
        {"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
        {"id": "d-hedge", "text": "No hedges.", "boundary": "Quotes are exempt.", "counted_by": "pattern", "pattern": "maybe"},
    ]
}
TASKS = {
    "tasks": [
        {"id": "t1", "tempts": "d-judge", "split": "open", "message": "Explain tides.", "answer_key": None},
        {"id": "t3", "tempts": "d-judge", "split": "sealed", "message": "Explain snow.", "answer_key": None},
    ],
    "conversations": [],
}
ANCHORS = {"anchors": [{"id": "a-one", "task": "t3", "message": "Explain snow.", "text": "Cold rain.", "breaches": {"d-judge": 1}, "done": True}]}
ACCEPTANCE = {"breach_difference": 0.5, "self_difference": 0.5, "done_agreement": 0.8}
CALIBRATION = {
    "attempt": 1,
    "judge_model": JUDGE_MODEL,
    "raters": ["agent", "agent"],
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
    "brief_hash": "c" * 64,
    "agreement": {"inputs": {}, "demands": {"d-judge": {"breach_difference": 0.1, "self_difference": 0.1}}, "done_agreement": 1.0, "scale": None, "ratings": {}},
}
PLAN = {
    "judge_model": JUDGE_MODEL,
    "raters": ["agent", "agent"],
    "rater_model": OTHER_MODEL,
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
}
HASH = "a" * 64


def series_folder(tmp_path: Path) -> SeriesFolder:
    """Write a series whose r1 blinded the packets `t1` and `t1--omissions`, each holding one reply and the anchor."""
    files = SeriesFolder(tmp_path / "series")
    write_agent_series(files, DEMANDS, TASKS, ANCHORS)
    write_yaml(files, "6-judge/calibration/attempt-1/plan.yaml", PLAN)
    write_record(files, "6-judge/calibration.yaml", CALIBRATION, [])
    write_file(files, "r1/5-replies/instruction/t1/repeat-1.yaml", b"reply")
    write_file(files, "r1/5-replies/omit-1/t1/repeat-1.yaml", b"reply")
    origin = {"split": "open", "repeat": 1, "task": "t1", "borrowed_from": None}
    ids = {
        REPLY_IDS["t1"]: {**origin, "packet": "t1", "condition": "instruction"},
        REPLY_IDS["t1--omissions"]: {**origin, "packet": "t1--omissions", "condition": "omit-1"},
        **{anchor_id: {"packet": packet, "anchor": "a-one"} for packet, anchor_id in ANCHOR_IDS.items()},
    }
    write_record(files, "r1/6-origins.yaml", {"ids": ids, "packets": dict.fromkeys(PACKETS, HASH)}, [])
    return files


def write_definition(files: SeriesFolder, packet: str, judging: int) -> None:
    write_file(files, f".claude/agents/ie-judge-r1-{packet}-k{judging}.md", b"definition")


def states(files: SeriesFolder, transcripts: list[Transcript] = ()) -> dict:
    return judging_states(files, "r1", list(transcripts), Path.read_bytes)


def verdict_path(files: SeriesFolder, packet: str, judging: int) -> Path:
    return files.root / f"r1/7-verdicts/{packet}/k{judging}.yaml"


def write_verdict(files: SeriesFolder, packet: str, judging: int, anchor_breaches: int = 1, anchor_done: bool | None = True) -> None:
    """Write judging `judging`'s verdict of the packet: its reply counted at 2 breaches, its anchor counted as given."""
    reply = {"id": REPLY_IDS[packet], "breaches": {"d-judge": 2}, "done": True, "kind": "answer", "notes": ""}
    anchor = {"id": ANCHOR_IDS[packet], "breaches": {"d-judge": anchor_breaches}, "done": anchor_done, "kind": "answer", "notes": ""}
    write_yaml(files, f"r1/7-verdicts/{packet}/k{judging}.yaml", {"verdicts": [reply, anchor]})


def judge_transcript(
    files: SeriesFolder,
    packet: str,
    judging: int,
    model: str = JUDGE_MODEL,
    final: bool = True,
    started: str = "2026-10-14T19:00:43.000Z",
    tools: tuple[dict, ...] = (),
) -> Transcript:
    """Write the transcript of a judging that loaded the oath skill and wrote its verdict path, and return its location."""
    agent_type = f"ie-judge-r1-{packet}-k{judging}"
    uses = tools or (
        {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": "manifesto:manifesto-oath"}},
        {"type": "tool_use", "id": "toolu_2", "name": "Write", "input": {"file_path": str(verdict_path(files, packet, judging))}},
    )
    blocks = [*uses, *([{"type": "text", "text": "Done."}] if final else [])]
    usage = {"input_tokens": 3, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 2}
    lines = [
        {"type": "user", "message": {"role": "user", "content": "Judge the packet."}, "timestamp": started},
        {"type": "assistant", "message": {"model": model, "id": "msg_A", "role": "assistant", "content": blocks, "usage": usage}, "timestamp": started},
    ]
    path = files.root.parent / f"transcripts/{agent_type}-{started}/subagents/agent-{agent_type}.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines))
    return Transcript(path=path, session=path.parent.parent.name, agent_id=agent_type, agent_type=agent_type)


def test_a_packet_with_no_judging_needs_judging_one(tmp_path):
    files = series_folder(tmp_path)

    assert states(files) == {"t1": NeedsJudging(1), "t1--omissions": NeedsJudging(1)}


def test_a_judging_without_verdict_or_transcript_is_pending_and_blocks_a_new_one_for_its_packet_alone(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    assert states(files) == {"t1": PendingJudging(1), "t1--omissions": NeedsJudging(1)}


def test_a_returned_judging_without_a_verdict_file_failed_and_the_next_judging_follows_it(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    assert states(files, [judge_transcript(files, "t1", 1)]) == {"t1": NeedsJudging(2), "t1--omissions": NeedsJudging(1)}


def test_a_judging_whose_transcript_has_not_ended_in_a_final_message_stays_pending(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    assert states(files, [judge_transcript(files, "t1", 1, final=False)])["t1"] == PendingJudging(1)


def test_a_returned_judging_whose_verdict_matches_the_anchors_is_accepted_with_its_transcript_and_anchor_agreement(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    write_verdict(files, "t1", 1)
    transcript = judge_transcript(files, "t1", 1)

    assert states(files, [transcript])["t1"] == AcceptedJudging(
        judging=1,
        judge_model=JUDGE_MODEL,
        transcript=transcript.path,
        transcript_hash=hashlib.sha256(transcript.path.read_bytes()).hexdigest(),
        anchors=AnchorAgreement(breach_difference={"d-judge": 0.0}, done_agreement=1.0),
    )


def reply_entry(blind_id: str, breaches: dict) -> dict:
    return {"id": blind_id, "breaches": breaches, "done": True, "kind": "answer", "notes": ""}


@pytest.mark.parametrize(
    "document",
    [
        "verdicts: [unclosed",
        {"verdicts": [reply_entry(REPLY_IDS["t1"], {"d-judge": 2})]},
        {"verdicts": [reply_entry(REPLY_IDS["t1"], {"d-judge": 2}), reply_entry(ANCHOR_IDS["t1"], {"d-judge": 1}), reply_entry("b0000009f", {"d-judge": 0})]},
        {"verdicts": [reply_entry(REPLY_IDS["t1"], {"d-judge": 2}), reply_entry(ANCHOR_IDS["t1"], {"d-hedge": 1})]},
        {"verdicts": [reply_entry(REPLY_IDS["t1"], {"d-judge": 2}), reply_entry(ANCHOR_IDS["t1"], {})]},
        {"verdicts": [reply_entry(REPLY_IDS["t1"], {"d-judge": 2}), reply_entry(ANCHOR_IDS["t1"], {"d-judge": -1})]},
    ],
    ids=["not-yaml", "missing-blind-id", "foreign-blind-id", "not-a-judge-demand", "uncounted-demand", "out-of-range"],
)
def test_a_returned_judging_whose_verdict_file_is_invalid_failed(tmp_path, document):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    target = verdict_path(files, "t1", 1)
    target.parent.mkdir(parents=True)
    target.write_text(document if isinstance(document, str) else yaml.safe_dump(document))

    assert states(files, [judge_transcript(files, "t1", 1)])["t1"] == NeedsJudging(2)


READ_TOOL = ({"type": "tool_use", "id": "toolu_3", "name": "Read", "input": {"file_path": "/series/r1/5-replies"}},)


@pytest.mark.parametrize(
    "transcript_options",
    [{"model": OTHER_MODEL}, {"tools": READ_TOOL}, None],
    ids=["wrong-model", "rejected-tool-use", "no-transcript"],
)
def test_a_returned_judging_fails_when_its_judge_ran_another_model_was_rejected_or_left_no_transcript(tmp_path, transcript_options):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    write_verdict(files, "t1", 1)
    transcripts = [] if transcript_options is None else [judge_transcript(files, "t1", 1, **transcript_options)]

    assert states(files, transcripts)["t1"] == NeedsJudging(2)


@pytest.mark.parametrize(
    "verdict_options",
    [{"anchor_breaches": 2}, {"anchor_breaches": 0}, {"anchor_done": False}, {"anchor_done": None}],
    ids=["breaches-over", "breaches-under", "done-contradicted", "done-undecided"],
)
def test_a_returned_judging_fails_when_it_misses_an_anchor_count_or_done_value_by_more_than_the_acceptance(tmp_path, verdict_options):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    write_verdict(files, "t1", 1, **verdict_options)

    assert states(files, [judge_transcript(files, "t1", 1)])["t1"] == NeedsJudging(2)


def returned_without_verdict(files: SeriesFolder, packet: str, judging: int) -> Transcript:
    write_definition(files, packet, judging)
    return judge_transcript(files, packet, judging)


def test_a_packet_holding_two_failed_judgings_needs_a_third(tmp_path):
    files = series_folder(tmp_path)
    transcripts = [returned_without_verdict(files, "t1", judging) for judging in (1, 2)]

    assert states(files, transcripts)["t1"] == NeedsJudging(3)


def test_a_packet_holding_three_failed_judgings_refuses_to_recalibrate_in_a_new_series(tmp_path):
    files = series_folder(tmp_path)
    transcripts = [returned_without_verdict(files, "t1", judging) for judging in (1, 2, 3)]

    with pytest.raises(Refusal, match="recalibrate in a new series"):
        states(files, transcripts)


def test_a_pending_judging_after_two_failures_blocks_a_new_one(tmp_path):
    files = series_folder(tmp_path)
    transcripts = [returned_without_verdict(files, "t1", judging) for judging in (1, 2)]
    write_definition(files, "t1", 3)

    assert states(files, transcripts)["t1"] == PendingJudging(3)


def test_the_lowest_judging_that_passes_is_accepted_though_a_later_one_passes_too(tmp_path):
    files = series_folder(tmp_path)
    transcripts = [returned_without_verdict(files, "t1", 1)]
    for judging in (2, 3):
        write_definition(files, "t1", judging)
        write_verdict(files, "t1", judging)
        transcripts.append(judge_transcript(files, "t1", judging))

    accepted = states(files, transcripts)["t1"]

    assert accepted.judging == 2
    assert accepted.transcript == transcripts[1].path


OLDER = "2026-10-14T19:00:43.000Z"
NEWER = "2026-10-14T20:00:43.000Z"


def test_a_relaunched_judging_whose_latest_transcript_has_not_ended_is_pending_whatever_an_earlier_transcript_did(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    transcripts = [judge_transcript(files, "t1", 1, started=NEWER, final=False), judge_transcript(files, "t1", 1, started=OLDER)]

    assert states(files, transcripts)["t1"] == PendingJudging(1)


def test_the_judge_of_a_judging_is_its_latest_transcript_whatever_the_order_the_transcripts_are_listed_in(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    write_verdict(files, "t1", 1)
    wrong_model = judge_transcript(files, "t1", 1, started=OLDER, model=OTHER_MODEL)
    right_model = judge_transcript(files, "t1", 1, started=NEWER)

    assert states(files, [right_model, wrong_model])["t1"].transcript == right_model.path
    assert states(files, [wrong_model, right_model])["t1"].transcript == right_model.path


def test_a_definition_of_the_omissions_packet_is_not_counted_for_the_task_packet_whose_name_it_begins_with(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1--omissions", 1)

    assert states(files) == {"t1": NeedsJudging(1), "t1--omissions": PendingJudging(1)}
