import yaml

from instruction_eval.reader import AgentKind, render_agent_definition

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
