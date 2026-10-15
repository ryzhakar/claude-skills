import json
from pathlib import Path

import pytest
import yaml

import instruction_eval
from instruction_eval.judge import judge_prepare
from instruction_eval.reader import NeutralLoginRefused, Transcript
from instruction_eval.records import Refusal, SeriesFolder, sha256, write_file, write_record
from series_fixtures import tree, write_yaml

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


def series_folder(tmp_path: Path, brief: str = TEMPLATE.read_text()) -> SeriesFolder:
    """Write a calibrated agent-reader series in the folder `series`, its accepted attempt's brief `brief`, whose r1 blinded the packets `t1` and `t1--omissions`, each holding one reply and the anchor."""
    files = SeriesFolder(tmp_path / "series")
    write_record(files, "series.yaml", SERIES, [])
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


class NeutralLogin:
    """A neutral login under a home folder, as the judge commands check it."""

    def __init__(self, home: Path):
        self.home = home
        self.config_dir = home / ".claudes-bare" / "readers"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        (self.config_dir / "settings.json").write_text(json.dumps({"enabledPlugins": REQUIRED_PLUGINS}))

    def environ(self) -> dict[str, str]:
        return {"CLAUDE_CONFIG_DIR": str(self.config_dir)}


def prepare(tmp_path: Path, files: SeriesFolder, transcripts: list[Transcript] = ()) -> str:
    """Run `judge prepare r1` under the neutral login and return what it prints."""
    login = NeutralLogin(tmp_path / "home")
    return judge_prepare(files, "r1", login.environ(), login.home, files.root, list(transcripts), Path.read_bytes)


def definition(files: SeriesFolder, name: str) -> tuple[dict, str]:
    """Return the frontmatter and body of the generated definition."""
    header, _, body = files.read_bytes(f".claude/agents/{name}.md").decode().removeprefix("---\n").partition("---\n")
    return yaml.safe_load(header), body


def test_each_unjudged_packet_gets_judging_one_rendered_from_the_accepted_brief_and_the_launch_list_names_them(tmp_path):
    files = series_folder(tmp_path)

    printed = prepare(tmp_path, files)

    names = ["ie-judge-r1-t1-k1", "ie-judge-r1-t1--omissions-k1"]
    assert yaml.safe_load(printed) == {"launches": [{"agent_type": name} for name in names]}
    for name, packet in zip(names, PACKETS):
        frontmatter, body = definition(files, name)
        assert frontmatter == {"name": name, "description": "Generated agent; launch from the printed launch list only.", "model": JUDGE_MODEL, "tools": "Skill, Write"}
        assert f"Source file: {SOURCE_NAME}\n\nBe terse." in body
        assert "- id: d-judge" in body and "d-hedge" not in body
        assert packet_text(packet) in body
        assert f"{files.root}/r1/7-verdicts/{packet}/k1.yaml" in body


def write_definition(files: SeriesFolder, packet: str, judging: int) -> None:
    write_file(files, f".claude/agents/ie-judge-r1-{packet}-k{judging}.md", b"definition")


def agents(files: SeriesFolder) -> list[str]:
    return sorted(path.name for path in (files.root / ".claude/agents").iterdir())


def test_a_packet_whose_judging_is_pending_gets_no_new_judging_and_prints_the_pending_line(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    printed = prepare(tmp_path, files)

    pending, _, launch_list = printed.partition("\n")
    assert pending == "judging k1 pending: t1"
    assert yaml.safe_load(launch_list) == {"launches": [{"agent_type": "ie-judge-r1-t1--omissions-k1"}]}
    assert files.read_bytes(".claude/agents/ie-judge-r1-t1-k1.md") == b"definition"
    assert agents(files) == ["ie-judge-r1-t1--omissions-k1.md", "ie-judge-r1-t1-k1.md"]


def judge_transcript(files: SeriesFolder, packet: str, judging: int) -> Transcript:
    """Write the ended transcript of a judging that loaded the oath skill and wrote its verdict path, and return its location."""
    agent_type = f"ie-judge-r1-{packet}-k{judging}"
    verdict = files.root / f"r1/7-verdicts/{packet}/k{judging}.yaml"
    blocks = [
        {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": "manifesto:manifesto-oath"}},
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


def test_a_returned_judging_without_a_verdict_is_followed_by_the_next_judging_of_its_packet(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    printed = prepare(tmp_path, files, [judge_transcript(files, "t1", 1)])

    assert yaml.safe_load(printed) == {"launches": [{"agent_type": "ie-judge-r1-t1-k2"}, {"agent_type": "ie-judge-r1-t1--omissions-k1"}]}
    frontmatter, body = definition(files, "ie-judge-r1-t1-k2")
    assert frontmatter["name"] == "ie-judge-r1-t1-k2"
    assert f"{files.root}/r1/7-verdicts/t1/k2.yaml" in body


def write_verdict(files: SeriesFolder, packet: str, judging: int) -> None:
    """Write a verdict of the packet that counts its anchor as known."""
    reply = {"id": REPLY_IDS[packet], "breaches": {"d-judge": 2}, "done": True, "kind": "answer", "notes": ""}
    anchor = {"id": ANCHOR_IDS[packet], "breaches": {"d-judge": 1}, "done": True, "kind": "answer", "notes": ""}
    write_yaml(files, f"r1/7-verdicts/{packet}/k{judging}.yaml", {"verdicts": [reply, anchor]})


def test_a_packet_with_an_accepted_judging_gets_nothing(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)
    write_verdict(files, "t1", 1)

    printed = prepare(tmp_path, files, [judge_transcript(files, "t1", 1)])

    assert printed == "launches:\n- agent_type: ie-judge-r1-t1--omissions-k1\n"
    assert agents(files) == ["ie-judge-r1-t1--omissions-k1.md", "ie-judge-r1-t1-k1.md"]


def test_a_packet_edited_after_blinding_refuses_naming_it_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path)
    (files.root / "r1/6-packets/t1--omissions.md").write_text("## b0000002a\n\nEdited.\n")
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^edited packet: r1/6-packets/t1--omissions\.md \(hash differs from r1/6-origins\.yaml\)$"):
        prepare(tmp_path, files)

    assert tree(files.root) == before


def test_a_packet_deleted_after_blinding_refuses_naming_it(tmp_path):
    files = series_folder(tmp_path)
    (files.root / "r1/6-packets/t1.md").unlink()

    with pytest.raises(Refusal, match=r"^missing packet: r1/6-packets/t1\.md$"):
        prepare(tmp_path, files)


def test_outside_the_neutral_login_it_refuses_for_every_reader_kind_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path)
    before = tree(files.root)

    with pytest.raises(NeutralLoginRefused):
        judge_prepare(files, "r1", {}, tmp_path / "home", files.root, [], Path.read_bytes)

    assert tree(files.root) == before


def test_a_packet_holding_three_failed_judgings_refuses_to_recalibrate_in_a_new_series_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path)
    transcripts = []
    for judging in (1, 2, 3):
        write_definition(files, "t1", judging)
        transcripts.append(judge_transcript(files, "t1", judging))
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^recalibrate in a new series$"):
        prepare(tmp_path, files, transcripts)

    assert tree(files.root) == before


def test_an_accepted_brief_naming_the_series_folder_refuses_naming_the_fault_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, brief=TEMPLATE.read_text() + "\nJudge for the series folder.\n")
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^brief fault: names series$"):
        prepare(tmp_path, files)

    assert tree(files.root) == before
