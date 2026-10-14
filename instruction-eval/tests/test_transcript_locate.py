from pathlib import Path

from instruction_eval.reader import locate_transcripts

CONFIG_DIR = Path(__file__).parent / "fixtures" / "transcript-locate" / "config"
SERIES_FOLDER = Path("/srv/series.v1")


def test_series_transcripts_are_found_with_their_agent_types():
    found = locate_transcripts(CONFIG_DIR, SERIES_FOLDER)
    assert [(t.agent_id, t.agent_type) for t in found] == [
        ("a1", "ie-reader-r1-empty"),
        ("b2", "ie-reader-r1-terse"),
    ]


def test_transcripts_of_other_series_folders_are_left_out():
    found = locate_transcripts(CONFIG_DIR, Path("/srv/other"))
    assert [t.agent_id for t in found] == ["c3"]


def test_series_folder_without_sessions_has_no_transcripts():
    assert locate_transcripts(CONFIG_DIR, Path("/srv/unused")) == []


def test_transcript_names_its_session_and_file():
    first = locate_transcripts(CONFIG_DIR, SERIES_FOLDER)[0]
    assert first.session == "sess-a"
    assert first.path == (
        CONFIG_DIR / "projects" / "-srv-series-v1" / "sess-a" / "subagents" / "agent-a1.jsonl"
    )


def test_relative_series_folder_is_read_as_its_absolute_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    key = str(tmp_path / "series.v1").replace("/", "-").replace(".", "-")
    subagents = tmp_path / "config" / "projects" / key / "sess-d" / "subagents"
    subagents.mkdir(parents=True)
    (subagents / "agent-d4.jsonl").write_text("{}\n")
    (subagents / "agent-d4.meta.json").write_text('{"agentType": "ie-reader-r1-empty"}\n')
    found = locate_transcripts(tmp_path / "config", Path("series.v1"))
    assert [t.agent_id for t in found] == ["d4"]
