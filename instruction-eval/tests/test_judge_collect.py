from pathlib import Path

import pytest
from series_fixtures import tree, write_yaml
from test_judge_prepare import (
    JUDGE_MODEL,
    PACKETS,
    SERIES,
    SOURCE_NAME,
    judge_transcript,
    prepare,
    series_folder,
    write_verdict,
)

from instruction_eval.judge import judge_collect
from instruction_eval.reader import Transcript
from instruction_eval.records import Refusal, SeriesFolder, SeriesRecords, sha256, write_record


def collect(files: SeriesFolder, transcripts: list[Transcript]) -> str:
    """Run `judge collect r1` over the judge transcripts and return what it prints."""
    return judge_collect(files, "r1", transcripts, Path.read_bytes)


def judged_series(tmp_path: Path) -> tuple[SeriesFolder, dict[str, Transcript]]:
    """Return a series whose packets each hold a prepared first judging, and the transcript of each judge that ended, by packet."""
    files = series_folder(tmp_path)
    prepare(tmp_path, files)
    return files, {packet: judge_transcript(files, packet, 1) for packet in PACKETS}


def test_every_packet_accepted_writes_the_collection_of_each_accepted_judging_and_prints_nothing(tmp_path):
    files, transcripts = judged_series(tmp_path)
    for packet in PACKETS:
        write_verdict(files, packet, 1)

    printed = collect(files, list(transcripts.values()))

    assert printed == ""
    assert SeriesRecords(files).collected("r1")["packets"] == {
        packet: {
            "accepted": 1,
            "judge_model": JUDGE_MODEL,
            "transcript": str(transcripts[packet].path),
            "transcript_hash": sha256(transcripts[packet].path.read_bytes()),
            "anchors": {"breach_difference": {"d-judge": 0.0}, "done_agreement": 1.0},
        }
        for packet in PACKETS
    }


def test_a_pending_judging_refuses_naming_its_packet_and_writes_nothing(tmp_path):
    files, transcripts = judged_series(tmp_path)
    write_verdict(files, "t1", 1)
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^judging pending: t1--omissions$"):
        collect(files, [transcripts["t1"]])

    assert tree(files.root) == before


def test_a_returned_judging_without_a_verdict_prints_its_packet_to_re_judge_and_writes_nothing(tmp_path):
    files, transcripts = judged_series(tmp_path)
    write_verdict(files, "t1", 1)
    before = tree(files.root)

    printed = collect(files, list(transcripts.values()))

    assert printed == "re-judge: t1--omissions\n"
    assert tree(files.root) == before


def test_the_collection_names_as_inputs_exactly_what_it_reads_the_reader_model_included(tmp_path):
    files, transcripts = judged_series(tmp_path)
    for packet in PACKETS:
        write_verdict(files, packet, 1)

    collect(files, list(transcripts.values()))

    assert set(SeriesRecords(files).collected("r1")["inputs"]) == {
        "series.yaml",
        "1-source/policy.md",
        "2-demands.yaml#demands",
        "5-reader.yaml#model",
        "6-judge/calibration.yaml",
        "6-judge/calibration/attempt-1/brief.md",
        "6-judge/anchors.yaml",
        "r1/6-packets/t1.md",
        "r1/6-packets/t1--omissions.md",
        "r1/6-origins.yaml",
        "r1/7-verdicts/t1/k1.yaml",
        "r1/7-verdicts/t1--omissions/k1.yaml",
        ".claude/agents/ie-judge-r1-t1-k1.md",
        ".claude/agents/ie-judge-r1-t1--omissions-k1.md",
    }


def test_a_series_without_sources_names_as_inputs_the_first_coverage_demands_its_judges_bind_to(tmp_path):
    files = series_folder(tmp_path)
    (files.root / "series.yaml").unlink()
    write_record(files, "series.yaml", {**SERIES, "sources": []}, [])
    (files.root / f"1-source/{SOURCE_NAME}").unlink()
    write_yaml(files, "r1/3-coverage.yaml", {"demands": {"d-judge": [1], "d-hedge": [1]}, "sentences": {1: ["d-judge", "d-hedge"]}})
    prepare(tmp_path, files)
    transcripts = [judge_transcript(files, packet, 1) for packet in PACKETS]
    for packet in PACKETS:
        write_verdict(files, packet, 1)

    collect(files, transcripts)

    inputs = set(SeriesRecords(files).collected("r1")["inputs"])
    assert "r1/3-coverage.yaml#demands" in inputs
    assert not any(read.startswith("1-source/") for read in inputs)


def test_a_judge_definition_edited_since_judge_prepare_refuses_naming_it_and_writes_nothing(tmp_path):
    files, transcripts = judged_series(tmp_path)
    for packet in PACKETS:
        write_verdict(files, packet, 1)
    definition = files.root / ".claude/agents/ie-judge-r1-t1--omissions-k1.md"
    definition.write_bytes(definition.read_bytes() + b"Count gently.\n")
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^\.claude/agents/ie-judge-r1-t1--omissions-k1\.md differs from its recomputation$"):
        collect(files, list(transcripts.values()))

    assert tree(files.root) == before


def test_a_packet_holding_three_failed_judgings_refuses_to_recalibrate_in_a_new_series_and_writes_nothing(tmp_path):
    files, first_transcripts = judged_series(tmp_path)
    write_verdict(files, "t1--omissions", 1)
    transcripts = list(first_transcripts.values())
    for judging in (2, 3):
        prepare(tmp_path, files, transcripts)
        transcripts.append(judge_transcript(files, "t1", judging))
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^recalibrate in a new series$"):
        collect(files, transcripts)

    assert tree(files.root) == before
