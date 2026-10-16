from pathlib import Path

import pytest
import yaml
from judging_fixtures import (
    JUDGE_MODEL,
    PACKETS,
    SOURCE_NAME,
    TEMPLATE,
    agents,
    definition,
    judge_transcript,
    packet_text,
    prepare,
    series_folder,
    write_definition,
    write_verdict,
)
from series_fixtures import tree

from instruction_eval.judge import judge_prepare
from instruction_eval.records import Refusal


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


def test_a_packet_whose_judging_is_pending_gets_no_new_judging_and_prints_the_pending_line(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    printed = prepare(tmp_path, files)

    pending, _, launch_list = printed.partition("\n")
    assert pending == "judging k1 pending: t1"
    assert yaml.safe_load(launch_list) == {"launches": [{"agent_type": "ie-judge-r1-t1--omissions-k1"}]}
    assert files.read_bytes(".claude/agents/ie-judge-r1-t1-k1.md") == b"definition"
    assert agents(files) == ["ie-judge-r1-t1--omissions-k1.md", "ie-judge-r1-t1-k1.md"]


def test_a_returned_judging_without_a_verdict_is_followed_by_the_next_judging_of_its_packet(tmp_path):
    files = series_folder(tmp_path)
    write_definition(files, "t1", 1)

    printed = prepare(tmp_path, files, [judge_transcript(files, "t1", 1)])

    assert yaml.safe_load(printed) == {"launches": [{"agent_type": "ie-judge-r1-t1-k2"}, {"agent_type": "ie-judge-r1-t1--omissions-k1"}]}
    frontmatter, body = definition(files, "ie-judge-r1-t1-k2")
    assert frontmatter["name"] == "ie-judge-r1-t1-k2"
    assert f"{files.root}/r1/7-verdicts/t1/k2.yaml" in body


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

    with pytest.raises(Refusal):
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
