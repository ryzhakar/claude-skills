import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

FRONTMATTER_FENCE = "---\n"
LAUNCH_LIST_DESCRIPTION = "Generated agent; launch from the printed launch list only."
EMPTY_TOOLSET_LINES = ("tools: Read", "disallowedTools: Read")
JUDGE_TOOLSET_LINES = ("tools: Skill, Write",)
FRONTMATTER_BREAKERS = ("\n", "\r", ": ")


class AgentKind(Enum):
    READER = "reader"
    JUDGE = "judge"


class DefinitionEdited(Exception):
    """Raised when a definition on disk differs from its recomputation."""


def refuse_edited_definition(name: str, on_disk: bytes, recomputed: bytes) -> None:
    """Raise DefinitionEdited naming the definition when its bytes differ from the recomputed bytes."""
    if on_disk != recomputed:
        raise DefinitionEdited(f"{name} differs from its recomputation")


def render_agent_definition(name: str, model: str, kind: AgentKind, body: bytes) -> bytes:
    """Render an agent definition file whose body is the given bytes."""
    frontmatter = _frontmatter_text(name, model, kind)
    return frontmatter.encode("utf-8") + body


def _frontmatter_text(name: str, model: str, kind: AgentKind) -> str:
    """Return the fenced frontmatter block for one generated agent."""
    lines = (
        f"name: {_single_line_value(name)}",
        f"description: {LAUNCH_LIST_DESCRIPTION}",
        f"model: {_single_line_value(model)}",
        *_toolset_lines(kind),
    )
    return FRONTMATTER_FENCE + "".join(line + "\n" for line in lines) + FRONTMATTER_FENCE


def _single_line_value(value: str) -> str:
    """Return the value unchanged or raise ValueError when it is empty or could break frontmatter."""
    if not value or any(breaker in value for breaker in FRONTMATTER_BREAKERS):
        raise ValueError(f"frontmatter value must be non-empty, single-line, without ': ': {value!r}")
    return value


def _toolset_lines(kind: AgentKind) -> tuple[str, ...]:
    """Return the frontmatter lines that fix the tools of an agent kind."""
    return EMPTY_TOOLSET_LINES if kind is AgentKind.READER else JUDGE_TOOLSET_LINES


PROJECTS_DIR_NAME = "projects"
SUBAGENTS_DIR_NAME = "subagents"
TRANSCRIPT_PATTERN = "agent-*.jsonl"
TRANSCRIPT_ID_PREFIX = "agent-"
META_SUFFIX = ".meta.json"
AGENT_TYPE_FIELD = "agentType"
KEY_SEPARATOR_CHARS = "/."
KEY_REPLACEMENT = "-"


@dataclass(frozen=True)
class Transcript:
    """One subagent transcript with the session and agent that wrote it."""

    path: Path
    session: str
    agent_id: str
    agent_type: str


def locate_transcripts(
    config_dir: Path, series_folder: Path, working_dir: Path
) -> list[Transcript]:
    """Return the subagent transcripts of the series folder's sessions, ordered by path; an absolute series folder ignores the working dir."""
    project_dir = config_dir / PROJECTS_DIR_NAME / _project_key(working_dir / series_folder)
    paths = sorted(project_dir.glob(f"*/{SUBAGENTS_DIR_NAME}/{TRANSCRIPT_PATTERN}"))
    return [_read_transcript(path) for path in paths]


def _project_key(absolute_series_folder: Path) -> str:
    """Return the absolute path with each slash and dot replaced by a dash."""
    return "".join(
        KEY_REPLACEMENT if char in KEY_SEPARATOR_CHARS else char
        for char in str(absolute_series_folder)
    )


def _read_transcript(path: Path) -> Transcript:
    """Return the transcript at the path with the agent type its meta file holds."""
    meta_path = path.with_suffix(META_SUFFIX)
    if not meta_path.is_file():
        raise ValueError(f"{path}: meta file {meta_path.name} is missing")
    meta = _read_meta(path, meta_path)
    agent_type = meta.get(AGENT_TYPE_FIELD)
    if not isinstance(agent_type, str):
        raise ValueError(f"{path}: meta file lacks a string {AGENT_TYPE_FIELD}")
    return Transcript(
        path=path,
        session=path.parent.parent.name,
        agent_id=path.stem.removeprefix(TRANSCRIPT_ID_PREFIX),
        agent_type=agent_type,
    )


def _read_meta(path: Path, meta_path: Path) -> dict:
    """Return the JSON object the meta file holds, refusing any other content by transcript name."""
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        raise ValueError(f"{path}: meta file is not valid JSON") from None
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: meta file is not a JSON object")
    return meta
