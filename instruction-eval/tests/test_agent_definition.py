import pytest
import yaml

from instruction_eval.reader import (
    AgentKind,
    DefinitionEdited,
    refuse_edited_definition,
    render_agent_definition,
)

PINNED_MODEL = "claude-sonnet-5-5"
CONDITION_BYTES = b"Answer plainly.\r\n\nTrailing space \n"
LAUNCH_LIST_DESCRIPTION = "Generated agent; launch from the printed launch list only."


def split_definition(definition: bytes) -> tuple[dict, bytes]:
    opening, frontmatter, body = definition.split(b"---\n", 2)
    assert opening == b""
    return yaml.safe_load(frontmatter), body


def test_reader_definition_carries_fixed_frontmatter_and_condition_bytes_as_body():
    definition = render_agent_definition(
        "ie-reader-r1-placebo", PINNED_MODEL, AgentKind.READER, CONDITION_BYTES
    )
    frontmatter, body = split_definition(definition)
    assert frontmatter["name"] == "ie-reader-r1-placebo"
    assert frontmatter["description"] == LAUNCH_LIST_DESCRIPTION
    assert frontmatter["model"] == PINNED_MODEL
    assert body == CONDITION_BYTES


def test_reader_definition_launches_with_zero_tools_by_emptying_the_allowlist():
    definition = render_agent_definition(
        "ie-reader-r1-placebo", PINNED_MODEL, AgentKind.READER, CONDITION_BYTES
    )
    frontmatter, _ = split_definition(definition)
    assert frontmatter["tools"] == "Read"
    assert frontmatter["disallowedTools"] == "Read"


def test_judge_definition_names_no_tool_besides_skill_and_write():
    definition = render_agent_definition(
        "ie-judge-r1-t1-k1", PINNED_MODEL, AgentKind.JUDGE, b"Rate it.\n"
    )
    frontmatter, _ = split_definition(definition)
    assert {name.strip() for name in frontmatter["tools"].split(",")} == {"Skill", "Write"}
    assert "disallowedTools" not in frontmatter


def test_edited_definition_is_refused_on_recompute():
    recomputed = render_agent_definition(
        "ie-reader-r1-placebo", PINNED_MODEL, AgentKind.READER, CONDITION_BYTES
    )
    refuse_edited_definition(recomputed, recomputed)
    with pytest.raises(DefinitionEdited):
        refuse_edited_definition(recomputed + b" ", recomputed)
