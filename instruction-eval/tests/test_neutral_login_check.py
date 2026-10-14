import json
from pathlib import Path

import pytest

from instruction_eval.reader import NeutralLoginRefused, check_neutral_login

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
    with pytest.raises(NeutralLoginRefused):
        check_neutral_login({}, login.home, login.working_dir)


def test_refuses_a_claude_md_in_the_config_dir(login: Login):
    (login.config_dir / "CLAUDE.md").write_text("memory")
    with pytest.raises(NeutralLoginRefused):
        login.check()


@pytest.mark.parametrize("folder", ["agents", "skills"])
def test_refuses_a_non_empty_agents_or_skills_folder(login: Login, folder: str):
    (login.config_dir / folder).mkdir()
    (login.config_dir / folder / "entry.md").write_text("x")
    with pytest.raises(NeutralLoginRefused):
        login.check()


@pytest.mark.parametrize("folder", ["agents", "skills"])
def test_refuses_a_linked_agents_or_skills_folder(login: Login, folder: str):
    target = login.home / "elsewhere"
    target.mkdir()
    (login.config_dir / folder).symlink_to(target)
    with pytest.raises(NeutralLoginRefused):
        login.check()


@pytest.mark.parametrize("folder", ["agents", "skills"])
def test_accepts_an_empty_agents_or_skills_folder(login: Login, folder: str):
    (login.config_dir / folder).mkdir()
    login.check()


@pytest.mark.parametrize("outside", [".claude", ".claudes-bare", "elsewhere/readers"])
def test_refuses_a_config_dir_outside_the_bare_logins_folder(login: Login, outside: str):
    config_dir = login.home / outside
    config_dir.mkdir(parents=True, exist_ok=True)
    environ = {"CLAUDE_CONFIG_DIR": str(config_dir)}
    with pytest.raises(NeutralLoginRefused):
        check_neutral_login(environ, login.home, login.working_dir)
