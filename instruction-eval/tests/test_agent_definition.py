import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from instruction_eval.reader import (
    AgentKind,
    DefinitionEdited,
    refuse_edited_definition,
    render_agent_definition,
)

PINNED_MODEL = "claude-sonnet-5-5"
CONDITION_BYTES = b"Answer plainly.\r\n\nTrailing space \n"
LAUNCH_LIST_DESCRIPTION = "Generated agent; launch from the printed launch list only."
FENCE_LINE = b"---\n"
SLUGS =st.from_regex(r"[a-z][a-z0-9-]{0,40}", fullmatch=True)


def split_definition(definition: bytes) -> tuple[dict, bytes]:
    lines = definition.splitlines(keepends=True)
    assert lines[0] == FENCE_LINE
    closing = lines.index(FENCE_LINE, 1)
    return yaml.safe_load(b"".join(lines[1:closing])), b"".join(lines[closing + 1 :])


def test_reader_definition_carries_fixed_frontmatter_and_condition_bytes_as_body():
    definition = render_agent_definition(
        "ie-reader-r1-placebo", PINNED_MODEL, AgentKind.READER, CONDITION_BYTES
    )
    frontmatter, body = split_definition(definition)
    assert frontmatter["name"] == "ie-reader-r1-placebo"
    assert frontmatter["description"] == LAUNCH_LIST_DESCRIPTION
    assert frontmatter["model"] == PINNED_MODEL
    assert body == CONDITION_BYTES


def test_name_ending_in_dashes_keeps_the_body_unchanged():
    definition = render_agent_definition("a---", PINNED_MODEL, AgentKind.READER, b"")
    assert split_definition(definition) == (split_definition(definition)[0], b"")
    assert split_definition(definition)[0]["name"] == "a---"


@given(name=SLUGS, body=st.binary())
def test_any_condition_bytes_become_the_body_unchanged(name, body):
    definition = render_agent_definition(name, PINNED_MODEL, AgentKind.READER, body)
    assert split_definition(definition)[1] == body


@given(name=SLUGS)
def test_reader_definition_launches_with_zero_tools_by_emptying_the_allowlist(name):
    definition = render_agent_definition(name, PINNED_MODEL, AgentKind.READER, b"")
    frontmatter, _ = split_definition(definition)
    assert frontmatter["tools"] == "Read"
    assert frontmatter["disallowedTools"] == "Read"


@given(name=SLUGS)
def test_judge_definition_names_no_tool_besides_skill_and_write(name):
    definition = render_agent_definition(name, PINNED_MODEL, AgentKind.JUDGE, b"Rate it.\n")
    frontmatter, _ = split_definition(definition)
    assert {tool.strip() for tool in frontmatter["tools"].split(",")} == {"Skill", "Write"}
    assert "disallowedTools" not in frontmatter


@pytest.mark.parametrize("name", ["", "x\ntools: Read, Bash", "x\rtools: Bash", "a: b"])
def test_name_that_could_inject_frontmatter_is_refused(name):
    with pytest.raises(ValueError):
        render_agent_definition(name, PINNED_MODEL, AgentKind.READER, b"")


@pytest.mark.parametrize("model", ["", "m\ntools: Bash", "m: x"])
def test_model_that_could_inject_frontmatter_is_refused(model):
    with pytest.raises(ValueError):
        render_agent_definition("ie-reader-r1-a", model, AgentKind.READER, b"")


@given(on_disk=st.binary(), recomputed=st.binary())
def test_definition_is_refused_exactly_when_its_bytes_differ(on_disk, recomputed):
    if on_disk == recomputed:
        refuse_edited_definition("ie-reader-r1-a", on_disk, recomputed)
    else:
        with pytest.raises(DefinitionEdited, match="ie-reader-r1-a differs from its recomputation"):
            refuse_edited_definition("ie-reader-r1-a", on_disk, recomputed)
