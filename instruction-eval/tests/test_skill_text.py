"""R107-R111: the eleven SKILL.md files hold their names, keys, tags, commands, rules, and token ceiling."""

import re
import subprocess
from pathlib import Path

import pytest
import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PLUGIN_ROOT.parent
SKILLS_DIR = PLUGIN_ROOT / "skills"

SKILL_NAMES = [
    "start-series",
    "list-demands",
    "check-coverage",
    "write-tasks",
    "calibrate-judge",
    "freeze-series",
    "measure-revision",
    "judge-replies",
    "diagnose",
    "revise",
    "keep-revision",
]

COMMANDS_BY_SKILL = {
    "start-series": ["series new"],
    "list-demands": ["demands check"],
    "check-coverage": ["coverage check"],
    "write-tasks": ["tasks check"],
    "calibrate-judge": ["judge calibrate"],
    "freeze-series": [
        "series status",
        "series freeze",
        "reader fingerprint",
        "reader prepare",
        "revision ask",
        "revision collect",
        "revision blind",
        "revision detect",
    ],
    "measure-revision": [
        "series status",
        "reader prepare",
        "revision ask",
        "revision collect",
        "revision blind",
        "revision detect",
        "revision score",
        "revision gate",
    ],
    "judge-replies": ["judge prepare", "judge collect"],
    "diagnose": ["series stop"],
    "revise": ["coverage check", "revision new"],
    "keep-revision": ["series keep"],
}

WAVE_CAP_SKILLS = ["judge-replies", "freeze-series", "calibrate-judge", "measure-revision"]
WAVE_CAP_TEXT = "at most twenty agents"
TRANSCRIPT_RULE_TEXT = "last assistant message"
STATUS_SKILLS = ["freeze-series", "measure-revision"]
START_SERIES_TEXTS = [
    "claudes new --bare readers instruction-eval@my-claude-skills manifesto@my-claude-skills",
    "in any working directory",
    "claudes run readers",
]
FORBIDDEN_PATTERNS = [r"\$\{CLAUDE_PLUGIN_ROOT\}", r"\bgh\b", r"\bversion\b"]
FRONTMATTER_KEYS = {"name", "description"}
TOKEN_CEILING = 1500
OPENING_TAG = re.compile(r"^<([a-z][a-z0-9-]*)>$")
CLOSING_TAG = re.compile(r"^</([a-z][a-z0-9-]*)>$")
FRONTMATTER_FENCE = "---"


def skill_text(name: str) -> str:
    return (SKILLS_DIR / name / "SKILL.md").read_text()


def split_frontmatter(text: str) -> tuple[dict, str]:
    _, frontmatter, body = text.split(FRONTMATTER_FENCE + "\n", 2)
    return yaml.safe_load(frontmatter), body


def tag_structure_defects(body: str) -> list[str]:
    defects = []
    open_tag = None
    blocks = 0
    for line in body.splitlines():
        stripped = line.strip()
        opening = OPENING_TAG.match(stripped)
        closing = CLOSING_TAG.match(stripped)
        if opening and open_tag is None:
            open_tag = opening.group(1)
            blocks += 1
        elif closing and closing.group(1) == open_tag:
            open_tag = None
        elif opening or closing:
            defects.append(f"misplaced tag: {stripped}")
        elif stripped and open_tag is None:
            defects.append(f"text outside a tag: {stripped}")
    if open_tag is not None:
        defects.append(f"unclosed tag: {open_tag}")
    if blocks == 0:
        defects.append("no tag block")
    return defects


def count_tokens_by_skill() -> dict[str, int]:
    paths = [f"instruction-eval/skills/{name}/SKILL.md" for name in SKILL_NAMES]
    output = subprocess.run(
        ["just", "tokens", *paths],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    counts = {}
    for line in output.splitlines():
        match = re.match(r"\s*(\d+)\s+instruction-eval/skills/([^/]+)/SKILL\.md$", line)
        if match:
            counts[match.group(2)] = int(match.group(1))
    return counts


@pytest.fixture(scope="module")
def token_counts() -> dict[str, int]:
    return count_tokens_by_skill()


def test_skills_directory_holds_exactly_the_eleven_skills():
    assert sorted(path.name for path in SKILLS_DIR.iterdir()) == sorted(SKILL_NAMES)


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_each_skill_is_one_file_named_skill_md(name):
    assert [path.name for path in (SKILLS_DIR / name).iterdir()] == ["SKILL.md"]


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_frontmatter_holds_the_name_and_description_keys_only(name):
    frontmatter, _ = split_frontmatter(skill_text(name))
    assert set(frontmatter) == FRONTMATTER_KEYS
    assert frontmatter["name"] == name
    assert frontmatter["description"].strip()


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_body_is_xml_tag_blocks_alone(name):
    _, body = split_frontmatter(skill_text(name))
    assert tag_structure_defects(body) == []


def test_tag_check_names_text_outside_tags_and_unclosed_tags():
    assert tag_structure_defects("loose\n<a>\nx\n") == [
        "text outside a tag: loose",
        "unclosed tag: a",
    ]


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_skill_names_every_command_the_table_maps_to_it(name):
    text = skill_text(name)
    missing = [
        command
        for command in COMMANDS_BY_SKILL[name]
        if command not in text
    ]
    assert missing == []


@pytest.mark.parametrize("name", WAVE_CAP_SKILLS)
def test_launching_skill_states_the_wave_cap_and_the_transcript_rule(name):
    text = skill_text(name)
    assert WAVE_CAP_TEXT in text or "first twenty" in text
    assert TRANSCRIPT_RULE_TEXT in text


@pytest.mark.parametrize("name", STATUS_SKILLS)
def test_freeze_and_measure_skills_carry_series_status(name):
    assert "series status" in skill_text(name)


@pytest.mark.parametrize("required", START_SERIES_TEXTS)
def test_start_series_states_the_neutral_login_and_launch(required):
    assert required in skill_text("start-series")


@pytest.mark.parametrize("name", SKILL_NAMES)
@pytest.mark.parametrize("pattern", FORBIDDEN_PATTERNS)
def test_skill_carries_no_forbidden_string(name, pattern):
    assert re.search(pattern, skill_text(name)) is None


@pytest.mark.parametrize("name", SKILL_NAMES)
def test_skill_counts_under_the_token_ceiling(name, token_counts):
    assert token_counts[name] < TOKEN_CEILING
