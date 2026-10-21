"""Fixtures of a calibrated series whose r1 blinded the packets t1 and t1--omissions, and of its judgings."""

import json
from pathlib import Path

import yaml
from series_fixtures import DISK_LOGIN_FILES, SERIES_BINDING, NeutralLogin, write_yaml

import instruction_eval
from instruction_eval.judge import judge_prepare
from instruction_eval.reader import Transcript
from instruction_eval.records import SeriesFolder, sha256, write_file, write_record

TEMPLATE = Path(instruction_eval.__file__).parent / "templates" / "judge-brief.md"
JUDGE_MODEL = "claude-opus-4-1"
RATER_MODEL = "claude-sonnet-5-5"
READER_MODEL = "claude-haiku-4-5"
SOURCE_NAME = "policy.md"
SERIES = {"instruction": "/home/writer/terse.md", "sources": [f"/home/writer/{SOURCE_NAME}"], "reader_kind": "agent", "binding": SERIES_BINDING, "created": "2026-10-14T10:00:00+00:00"}
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
PLAN = {"judge_model": JUDGE_MODEL, "raters": ["agent", "agent"], "rater_model": RATER_MODEL, "sample_size": 4, "anchors_per_packet": 3, "acceptance": ACCEPTANCE}
ATTEMPT = "6-judge/calibration/attempt-1"
CALIBRATION = {
    "attempt": 1,
    "judge_model": JUDGE_MODEL,
    "raters": ["agent", "agent"],
    "sample_size": 4,
    "anchors_per_packet": 3,
    "acceptance": ACCEPTANCE,
    "brief_hash": sha256(TEMPLATE.read_bytes()),
    "agreement": {"inputs": {}, "demands": {"d-judge": {"breach_difference": 0.1, "self_difference": 0.1}}, "done_agreement": 1.0, "scale": None, "ratings": {}},
}
PACKETS = ("t1", "t1--omissions")
REPLY_IDS = {"t1": "b0000001a", "t1--omissions": "b0000002a"}
ANCHOR_IDS = {"t1": "b0000001b", "t1--omissions": "b0000002b"}
CONDITIONS = {"t1": "instruction", "t1--omissions": "omit-1"}


def packet_text(packet: str) -> str:
    """Return the packet's markdown: its reply entry and its anchor entry."""
    return f"## {REPLY_IDS[packet]}\n\n### User\n\nExplain tides.\n\n### Reply\n\n{packet} reply.\n\n## {ANCHOR_IDS[packet]}\n\n### User\n\nExplain snow.\n\n### Reply\n\nCold rain.\n"


def series_folder(tmp_path: Path, brief: str = TEMPLATE.read_text(), binding: dict = SERIES_BINDING) -> SeriesFolder:
    """Write a calibrated agent-reader series binding through `binding` in the folder `series`, its accepted attempt's brief `brief`, whose r1 blinded the packets `t1` and `t1--omissions`, each holding one reply and the anchor."""
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", {**SERIES, "binding": binding}, [])
    write_file(files, f"1-source/{SOURCE_NAME}", b"Be terse.\n")
    write_yaml(files, "2-demands.yaml", DEMANDS)
    write_yaml(files, "3-tasks.yaml", TASKS)
    write_yaml(files, "5-reader.yaml", {"kind": "agent", "model": READER_MODEL})
    write_yaml(files, f"{ATTEMPT}/plan.yaml", PLAN)
    write_file(files, f"{ATTEMPT}/brief.md", brief.encode())
    write_record(files, "6-judge/calibration.yaml", CALIBRATION, [f"{ATTEMPT}/brief.md", f"{ATTEMPT}/plan.yaml"])
    write_record(files, "6-judge/anchors.yaml", ANCHORS, [])
    ids = {}
    for packet in PACKETS:
        write_file(files, f"r1/5-replies/{CONDITIONS[packet]}/t1/repeat-1.yaml", b"reply")
        write_file(files, f"r1/6-packets/{packet}.md", packet_text(packet).encode())
        ids[REPLY_IDS[packet]] = {"packet": packet, "condition": CONDITIONS[packet], "task": "t1", "split": "open", "repeat": 1, "borrowed_from": None}
        ids[ANCHOR_IDS[packet]] = {"packet": packet, "anchor": "a-one"}
    packets = {packet: sha256(files.read_bytes(f"r1/6-packets/{packet}.md")) for packet in PACKETS}
    write_record(files, "r1/6-origins.yaml", {"ids": ids, "packets": packets}, [])
    return files


def prepare(tmp_path: Path, files: SeriesFolder, transcripts: list[Transcript] = (), binding_plugin: str = SERIES_BINDING["plugin"]) -> str:
    """Run `judge prepare r1` under the neutral login enabling the binding plugin and return what it prints."""
    login = NeutralLogin(tmp_path / "home", binding_plugin)
    return judge_prepare(files, "r1", login.environ(), login.home, files.root, list(transcripts), Path.read_bytes, DISK_LOGIN_FILES)


def definition(files: SeriesFolder, name: str) -> tuple[dict, str]:
    """Return the frontmatter and body of the generated definition."""
    header, _, body = files.read_bytes(f".claude/agents/{name}.md").decode().removeprefix("---\n").partition("---\n")
    return yaml.safe_load(header), body


def write_definition(files: SeriesFolder, packet: str, judging: int) -> None:
    write_file(files, f".claude/agents/ie-judge-r1-{packet}-k{judging}.md", b"definition")


def agents(files: SeriesFolder) -> list[str]:
    return sorted(path.name for path in (files.root / ".claude/agents").iterdir())


def judge_transcript(files: SeriesFolder, packet: str, judging: int, binding_skill: str = SERIES_BINDING["skill"]) -> Transcript:
    """Write the ended transcript of a judging that loaded the binding skill and wrote its verdict path, and return its location."""
    agent_type = f"ie-judge-r1-{packet}-k{judging}"
    verdict = files.root / f"r1/7-verdicts/{packet}/k{judging}.yaml"
    blocks = [
        {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": binding_skill}},
        {"type": "tool_use", "id": "toolu_2", "name": "Write", "input": {"file_path": str(verdict)}},
        {"type": "text", "text": "Done."},
    ]
    usage = {"input_tokens": 3, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 2}
    started = "2026-10-14T19:00:43.000Z"
    lines = [
        {"type": "user", "message": {"role": "user", "content": "Judge the packet."}, "timestamp": started},
        {"type": "assistant", "message": {"model": JUDGE_MODEL, "id": "msg_A", "role": "assistant", "content": blocks, "usage": usage}, "timestamp": started},
    ]
    path = files.root.parent / f"transcripts/{agent_type}/subagents/agent-{agent_type}.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines))
    return Transcript(path=path, session=path.parent.parent.name, agent_id=agent_type, agent_type=agent_type)


def write_verdict(files: SeriesFolder, packet: str, judging: int) -> None:
    """Write a verdict of the packet that counts its anchor as known."""
    reply = {"id": REPLY_IDS[packet], "breaches": {"d-judge": 2}, "done": True, "kind": "answer", "notes": ""}
    anchor = {"id": ANCHOR_IDS[packet], "breaches": {"d-judge": 1}, "done": True, "kind": "answer", "notes": ""}
    write_yaml(files, f"r1/7-verdicts/{packet}/k{judging}.yaml", {"verdicts": [reply, anchor]})
