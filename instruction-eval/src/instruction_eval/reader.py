from enum import Enum

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
