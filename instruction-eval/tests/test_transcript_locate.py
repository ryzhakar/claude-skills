import json
import tempfile
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from instruction_eval.reader import locate_transcripts

CONFIG_DIR = Path(__file__).parent / "fixtures" / "transcript-locate" / "config"
WORKING_DIR = Path("/srv")
SERIES_FOLDER = Path("/srv/series.v1")


def test_transcripts_are_listed_and_read_only_through_the_effects_handed_in():
    project = Path("/config/projects/-srv-series-v1")
    transcript = project / "sess-a" / "subagents" / "agent-a1.jsonl"
    files = {transcript.with_suffix(".meta.json"): json.dumps({"agentType": "ie-reader-r1-empty"}).encode()}
    listed = []

    def list_files(folder: Path, pattern: str) -> list[Path]:
        listed.append((folder, pattern))
        return [transcript]

    found = locate_transcripts(Path("/config"), SERIES_FOLDER, WORKING_DIR, list_files, files.__getitem__)

    assert [(t.path, t.agent_type) for t in found] == [(transcript, "ie-reader-r1-empty")]
    assert listed == [(project, "*/subagents/agent-*.jsonl")]


def test_series_transcripts_are_found_with_their_agent_types():
    found = locate_transcripts(CONFIG_DIR, SERIES_FOLDER, WORKING_DIR, Path.glob, Path.read_bytes)
    assert [(t.agent_id, t.agent_type) for t in found] == [
        ("a1", "ie-reader-r1-empty"),
        ("b2", "ie-reader-r1-terse"),
    ]


def test_transcripts_of_other_series_folders_are_left_out():
    found = locate_transcripts(CONFIG_DIR, Path("/srv/other"), WORKING_DIR, Path.glob, Path.read_bytes)
    assert [t.agent_id for t in found] == ["c3"]


def test_series_folder_without_sessions_has_no_transcripts():
    assert locate_transcripts(CONFIG_DIR, Path("/srv/unused"), WORKING_DIR, Path.glob, Path.read_bytes) == []


def test_transcript_names_its_session_and_file():
    first = locate_transcripts(CONFIG_DIR, SERIES_FOLDER, WORKING_DIR, Path.glob, Path.read_bytes)[0]
    assert first.session == "sess-a"
    assert first.path == (
        CONFIG_DIR / "projects" / "-srv-series-v1" / "sess-a" / "subagents" / "agent-a1.jsonl"
    )


def test_relative_series_folder_is_read_under_the_working_dir():
    found = locate_transcripts(CONFIG_DIR, Path("series.v1"), WORKING_DIR, Path.glob, Path.read_bytes)
    assert [t.agent_id for t in found] == ["a1", "b2"]


def test_transcript_without_meta_file_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-e5.jsonl.*meta"):
        locate_transcripts(CONFIG_DIR, Path("/srv/nometa"), WORKING_DIR, Path.glob, Path.read_bytes)


def test_meta_file_without_agent_type_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-f6.jsonl.*agentType"):
        locate_transcripts(CONFIG_DIR, Path("/srv/notype"), WORKING_DIR, Path.glob, Path.read_bytes)


def test_meta_file_with_invalid_json_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-g7.jsonl.*not valid JSON"):
        locate_transcripts(CONFIG_DIR, Path("/srv/badjson"), WORKING_DIR, Path.glob, Path.read_bytes)


def test_meta_file_holding_no_object_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-h8.jsonl.*not a JSON object"):
        locate_transcripts(CONFIG_DIR, Path("/srv/notobject"), WORKING_DIR, Path.glob, Path.read_bytes)


def test_meta_file_with_non_string_agent_type_is_refused_by_name():
    with pytest.raises(ValueError, match="agent-i9.jsonl.*agentType"):
        locate_transcripts(CONFIG_DIR, Path("/srv/badtype"), WORKING_DIR, Path.glob, Path.read_bytes)


FOLDER_NAMES = st.text(alphabet="ab.", min_size=1, max_size=4).filter(lambda name: name.strip("."))
SESSION_NAMES = st.text(alphabet="s01", min_size=1, max_size=3)
AGENT_IDS = st.text(alphabet="a01", min_size=1, max_size=3)
AGENT_TYPES = st.text(alphabet="ie-rd", min_size=1, max_size=6)
SESSIONS = st.dictionaries(SESSION_NAMES, st.dictionaries(AGENT_IDS, AGENT_TYPES, max_size=3), max_size=3)
WORKING_DIR_NAMES = ("work", "elsewhere")


def _write_session_transcripts(config_dir: Path, absolute_folder: Path, sessions: dict[str, dict[str, str]]) -> dict[Path, str]:
    """Write the transcripts and meta files Claude Code keeps for the folder's sessions and return each transcript's agent type by path."""
    project = config_dir / "projects" / str(absolute_folder).replace("/", "-").replace(".", "-")
    written = {}
    for session, agents in sessions.items():
        subagents = project / session / "subagents"
        subagents.mkdir(parents=True, exist_ok=True)
        for agent_id, agent_type in agents.items():
            transcript = subagents / f"agent-{agent_id}.jsonl"
            transcript.write_text("")
            (subagents / f"agent-{agent_id}.meta.json").write_text(json.dumps({"agentType": agent_type}))
            written[transcript] = agent_type
    return written


@given(trees=st.fixed_dictionaries({name: st.dictionaries(FOLDER_NAMES, SESSIONS, min_size=1, max_size=3) for name in WORKING_DIR_NAMES}), data=st.data())
def test_transcripts_found_are_exactly_those_of_the_series_folder_under_the_working_dir(trees, data):
    series_folder = data.draw(st.sampled_from(sorted(trees[WORKING_DIR_NAMES[0]])))
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        config_dir = root / "config"
        written = {
            (working_dir_name, folder): _write_session_transcripts(config_dir, root / working_dir_name / folder, sessions)
            for working_dir_name, folders in trees.items()
            for folder, sessions in folders.items()
        }
        found = locate_transcripts(config_dir, Path(series_folder), root / WORKING_DIR_NAMES[0], Path.glob, Path.read_bytes)
        assert [(transcript.path, transcript.agent_type) for transcript in found] == sorted(written[(WORKING_DIR_NAMES[0], series_folder)].items())
