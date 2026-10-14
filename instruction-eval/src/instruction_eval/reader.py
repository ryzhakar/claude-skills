import json
from dataclasses import dataclass
from pathlib import Path

PROJECTS_DIR_NAME = "projects"
SUBAGENTS_DIR_NAME = "subagents"
TRANSCRIPT_PATTERN = "agent-*.jsonl"
TRANSCRIPT_ID_PREFIX = "agent-"
META_SUFFIX = ".meta.json"
KEY_SEPARATOR_CHARS = "/."
KEY_REPLACEMENT = "-"


@dataclass(frozen=True)
class Transcript:
    path: Path
    session: str
    agent_id: str
    agent_type: str


def locate_transcripts(config_dir: Path, series_folder: Path) -> list[Transcript]:
    """Return the subagent transcripts of the series folder's sessions, ordered by path."""
    project_dir = config_dir / PROJECTS_DIR_NAME / project_key(series_folder)
    paths = sorted(project_dir.glob(f"*/{SUBAGENTS_DIR_NAME}/{TRANSCRIPT_PATTERN}"))
    return [read_transcript(path) for path in paths]


def project_key(series_folder: Path) -> str:
    """Return the series folder's absolute path with each slash and dot replaced by a dash."""
    return "".join(
        KEY_REPLACEMENT if char in KEY_SEPARATOR_CHARS else char
        for char in str(series_folder)
    )


def read_transcript(path: Path) -> Transcript:
    """Return the transcript at the path with the agent type its meta file holds."""
    meta_path = path.with_suffix(META_SUFFIX)
    agent_type = json.loads(meta_path.read_text())["agentType"]
    return Transcript(
        path=path,
        session=path.parent.parent.name,
        agent_id=path.stem.removeprefix(TRANSCRIPT_ID_PREFIX),
        agent_type=agent_type,
    )
