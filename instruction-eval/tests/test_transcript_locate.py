from pathlib import Path

import pytest

from instruction_eval.reader import locate_transcripts

CONFIG_DIR = Path(__file__).parent / "fixtures" / "transcript-locate" / "config"
WORKING_DIR = Path("/srv")
SERIES_FOLDER = Path("/srv/series.v1")


def test_series_transcripts_are_found_with_their_agent_types():
    found = locate_transcripts(CONFIG_DIR, SERIES_FOLDER, WORKING_DIR)
    assert [(t.agent_id, t.agent_type) for t in found] == [
        ("a1", "ie-reader-r1-empty"),
        ("b2", "ie-reader-r1-terse"),
    ]


def test_transcripts_of_other_series_folders_are_left_out():
    found = locate_transcripts(CONFIG_DIR, Path("/srv/other"), WORKING_DIR)
    assert [t.agent_id for t in found] == ["c3"]


def test_series_folder_without_sessions_has_no_transcripts():
    assert locate_transcripts(CONFIG_DIR, Path("/srv/unused"), WORKING_DIR) == []


def test_transcript_names_its_session_and_file():
    first = locate_transcripts(CONFIG_DIR, SERIES_FOLDER, WORKING_DIR)[0]
    assert first.session == "sess-a"
    assert first.path == (
        CONFIG_DIR / "projects" / "-srv-series-v1" / "sess-a" / "subagents" / "agent-a1.jsonl"
    )


def test_relative_series_folder_is_read_under_the_working_dir():
    found = locate_transcripts(CONFIG_DIR, Path("series.v1"), WORKING_DIR)
    assert [t.agent_id for t in found] == ["a1", "b2"]


def test_transcript_without_meta_file_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-e5.jsonl.*meta"):
        locate_transcripts(CONFIG_DIR, Path("/srv/nometa"), WORKING_DIR)


def test_meta_file_without_agent_type_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-f6.jsonl.*agentType"):
        locate_transcripts(CONFIG_DIR, Path("/srv/notype"), WORKING_DIR)


def test_meta_file_with_invalid_json_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-g7.jsonl.*not valid JSON"):
        locate_transcripts(CONFIG_DIR, Path("/srv/badjson"), WORKING_DIR)


def test_meta_file_holding_no_object_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-h8.jsonl.*not a JSON object"):
        locate_transcripts(CONFIG_DIR, Path("/srv/notobject"), WORKING_DIR)


def test_meta_file_with_non_string_agent_type_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-i9.jsonl.*agentType"):
        locate_transcripts(CONFIG_DIR, Path("/srv/badtype"), WORKING_DIR)
