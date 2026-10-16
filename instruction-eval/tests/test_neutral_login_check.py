import json
from pathlib import Path

import pytest

from instruction_eval.reader import check_neutral_login
from instruction_eval.records import Refusal

REQUIRED_PLUGINS = {
    "instruction-eval@my-claude-skills": True,
    "manifesto@my-claude-skills": True,
}


class Login:
    def __init__(self, home: Path):
        self.home = home
        self.config_dir = home / ".claudes-bare" / "readers"
        self.working_dir = home / "work" / "series"
        self.config_dir.mkdir(parents=True)
        self.working_dir.mkdir(parents=True)
        self.write_settings(REQUIRED_PLUGINS)

    def write_settings(self, enabled_plugins: dict) -> None:
        settings = {"enabledPlugins": enabled_plugins}
        (self.config_dir / "settings.json").write_text(json.dumps(settings))

    def environ(self) -> dict[str, str]:
        return {"CLAUDE_CONFIG_DIR": str(self.config_dir)}

    def check(self) -> None:
        check_neutral_login(self.environ(), self.home, self.working_dir)


@pytest.fixture
def login(tmp_path: Path) -> Login:
    return Login(tmp_path / "home")


def test_accepts_a_clean_neutral_login(login: Login):
    login.check()


def test_refuses_an_unset_config_dir(login: Login):
    with pytest.raises(Refusal):
        check_neutral_login({}, login.home, login.working_dir)


def test_refuses_a_broken_link_named_claude_md_in_the_config_dir(login: Login):
    (login.config_dir / "CLAUDE.md").symlink_to(login.home / "missing")
    with pytest.raises(Refusal):
        login.check()


def test_refuses_a_claude_md_in_the_config_dir(login: Login):
    (login.config_dir / "CLAUDE.md").write_text("memory")
    with pytest.raises(Refusal):
        login.check()


@pytest.mark.parametrize("folder", ["agents", "skills"])
def test_refuses_a_non_empty_agents_or_skills_folder(login: Login, folder: str):
    (login.config_dir / folder).mkdir()
    (login.config_dir / folder / "entry.md").write_text("x")
    with pytest.raises(Refusal):
        login.check()


@pytest.mark.parametrize("folder", ["agents", "skills"])
def test_refuses_a_linked_agents_or_skills_folder(login: Login, folder: str):
    target = login.home / "elsewhere"
    target.mkdir()
    (login.config_dir / folder).symlink_to(target)
    with pytest.raises(Refusal):
        login.check()


@pytest.mark.parametrize("folder", ["agents", "skills"])
def test_accepts_an_empty_agents_or_skills_folder(login: Login, folder: str):
    (login.config_dir / folder).mkdir()
    login.check()


@pytest.mark.parametrize(
    "enabled_plugins",
    [
        {},
        {"instruction-eval@my-claude-skills": True},
        {**REQUIRED_PLUGINS, "memento@my-claude-skills": True},
        {**REQUIRED_PLUGINS, "manifesto@my-claude-skills": False},
        {"instruction-eval@my-claude-skills": True, "manifesto@my-claude-skills": "true"},
    ],
)
def test_refuses_enabled_plugins_other_than_the_two_required(login: Login, enabled_plugins: dict):
    login.write_settings(enabled_plugins)
    with pytest.raises(Refusal):
        login.check()


def test_refuses_a_config_dir_without_settings(login: Login):
    (login.config_dir / "settings.json").unlink()
    with pytest.raises(Refusal):
        login.check()


@pytest.mark.parametrize("content", ["not json", "[]", '{"enabledPlugins": []}'])
def test_refuses_settings_that_are_not_a_plugin_mapping(login: Login, content: str):
    (login.config_dir / "settings.json").write_text(content)
    with pytest.raises(Refusal):
        login.check()


MEMORY_FILES = ["CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md", ".manifestos.yaml"]


REFUSED_PLACEMENTS = [
    (placement, memory_file)
    for placement in ["working_dir", "three_levels_up", "home"]
    for memory_file in MEMORY_FILES
    if (placement, memory_file) != ("home", ".claude/CLAUDE.md")
]


@pytest.mark.parametrize(("placement", "memory_file"), REFUSED_PLACEMENTS)
def test_refuses_a_memory_file_at_the_working_dir_or_an_ancestor(
    login: Login, placement: str, memory_file: str
):
    holders = {
        "working_dir": login.working_dir,
        "three_levels_up": login.working_dir.parents[2],
        "home": login.home,
    }
    planted = holders[placement] / memory_file
    planted.parent.mkdir(parents=True, exist_ok=True)
    planted.write_text("memory")
    with pytest.raises(Refusal):
        login.check()


@pytest.mark.parametrize("memory_file", MEMORY_FILES)
def test_refuses_a_memory_file_in_a_folder_outside_home(login: Login, memory_file: str):
    outside = login.home.parent / "outside"
    login.working_dir = outside / "series"
    login.working_dir.mkdir(parents=True)
    planted = outside / memory_file
    planted.parent.mkdir(parents=True, exist_ok=True)
    planted.write_text("memory")
    with pytest.raises(Refusal):
        login.check()


def test_accepts_the_home_user_memory(login: Login):
    user_memory = login.home / ".claude" / "CLAUDE.md"
    user_memory.parent.mkdir()
    user_memory.write_text("memory")
    login.check()


@pytest.mark.parametrize("outside", [".claude", ".claudes-bare", "elsewhere/readers"])
def test_refuses_a_config_dir_outside_the_bare_logins_folder(login: Login, outside: str):
    config_dir = login.home / outside
    config_dir.mkdir(parents=True, exist_ok=True)
    environ = {"CLAUDE_CONFIG_DIR": str(config_dir)}
    with pytest.raises(Refusal):
        check_neutral_login(environ, login.home, login.working_dir)
