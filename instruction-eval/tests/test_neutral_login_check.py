import json
from pathlib import Path

import pytest

from instruction_eval.reader import ACCOUNT_SYNCED_ENTRIES_BY_EXTENSION_FOLDERNAME, LoginFiles, check_neutral_login
from instruction_eval.records import DEFAULT_BINDING, Refusal
from series_fixtures import DISK_LOGIN_FILES, INSTRUCTION_EVAL_PLUGIN, OTHER_BINDING

REQUIRED_PLUGINS = {INSTRUCTION_EVAL_PLUGIN: True, DEFAULT_BINDING.plugin: True}


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

    def check(self, binding_plugin: str = DEFAULT_BINDING.plugin) -> None:
        check_neutral_login(self.environ(), self.home, self.working_dir, DISK_LOGIN_FILES, binding_plugin)


@pytest.fixture
def login(tmp_path: Path) -> Login:
    return Login(tmp_path / "home")


def test_accepts_a_clean_neutral_login(login: Login):
    login.check()


def test_refuses_an_unset_config_dir(login: Login):
    with pytest.raises(Refusal):
        check_neutral_login({}, login.home, login.working_dir, DISK_LOGIN_FILES, DEFAULT_BINDING.plugin)


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


SYNCED_BUCKET = "8340b9b5-4d3a-4099-958d-7dcb0a0aed42_8d6d5cd5-db00-47f0-898f-d48cbd3ed2b1"


def plant_account_synced_skills(config_dir: Path) -> None:
    """Lay out skills/synced as the account sync wrote it at /login: a bucket folder of skills, its manifest, and its marker file."""
    synced = config_dir / "skills" / "synced"
    (synced / SYNCED_BUCKET / "docx").mkdir(parents=True)
    (synced / SYNCED_BUCKET / "docx" / "SKILL.md").write_text("docx")
    (synced / SYNCED_BUCKET / "manifest.json").write_text("{}")
    (synced / f".bucket-{SYNCED_BUCKET}").write_text("")


def test_accepts_skills_the_account_synced_at_login(login: Login):
    plant_account_synced_skills(login.config_dir)
    login.check()


def test_refuses_a_skill_beside_the_account_synced_skills(login: Login):
    plant_account_synced_skills(login.config_dir)
    (login.config_dir / "skills" / "own-skill").mkdir()
    with pytest.raises(Refusal):
        login.check()


def test_refuses_a_linked_account_synced_skills_folder(login: Login):
    target = login.home / "elsewhere"
    target.mkdir()
    (login.config_dir / "skills").mkdir()
    (login.config_dir / "skills" / "synced").symlink_to(target)
    with pytest.raises(Refusal):
        login.check()


def test_the_account_synced_entries_table_cannot_be_widened():
    with pytest.raises(TypeError):
        ACCOUNT_SYNCED_ENTRIES_BY_EXTENSION_FOLDERNAME["agents"] = frozenset({"synced"})


def test_refuses_a_synced_folder_in_agents(login: Login):
    (login.config_dir / "agents" / "synced").mkdir(parents=True)
    with pytest.raises(Refusal):
        login.check()


@pytest.mark.parametrize(
    "enabled_plugins",
    [
        {},
        {INSTRUCTION_EVAL_PLUGIN: True},
        {**REQUIRED_PLUGINS, "memento@my-claude-skills": True},
        {**REQUIRED_PLUGINS, DEFAULT_BINDING.plugin: False},
        {INSTRUCTION_EVAL_PLUGIN: True, DEFAULT_BINDING.plugin: "true"},
    ],
)
def test_refuses_enabled_plugins_other_than_the_two_required(login: Login, enabled_plugins: dict):
    login.write_settings(enabled_plugins)
    with pytest.raises(Refusal):
        login.check()


def test_accepts_a_login_enabling_the_binding_plugin_the_series_names(login: Login):
    login.write_settings({INSTRUCTION_EVAL_PLUGIN: True, OTHER_BINDING["plugin"]: True})
    login.check(OTHER_BINDING["plugin"])


@pytest.mark.parametrize("enabled_plugins", [{INSTRUCTION_EVAL_PLUGIN: True}, REQUIRED_PLUGINS])
def test_refuses_a_login_lacking_the_binding_plugin_naming_binding_plugin(login: Login, enabled_plugins: dict):
    login.write_settings(enabled_plugins)
    with pytest.raises(Refusal, match=r"^enabledPlugins lacks binding\.plugin oath@elsewhere$"):
        login.check(OTHER_BINDING["plugin"])


def test_accepts_settings_allowing_the_judge_verdict_writes(login: Login):
    settings = {
        "enabledPlugins": REQUIRED_PLUGINS,
        "permissions": {"allow": ["Write(~/instruction-series/**/7-verdicts/**)", "Write(~/instruction-series/**/6-judge/calibration/**)"]},
    }
    (login.config_dir / "settings.json").write_text(json.dumps(settings))
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
        check_neutral_login(environ, login.home, login.working_dir, DISK_LOGIN_FILES, DEFAULT_BINDING.plugin)


def test_a_login_on_no_disk_is_probed_only_through_the_files_handed_in():
    home = Path("/nowhere/home")
    config_dir = home / ".claudes-bare" / "readers"
    contents = {config_dir / "settings.json": json.dumps({"enabledPlugins": REQUIRED_PLUGINS}).encode()}
    probed = []

    def probe(answer):
        def answered(path):
            probed.append(path)
            return answer(path)
        return answered

    login_files = LoginFiles(
        resolve=probe(lambda path: path),
        exists=probe(lambda path: path in contents),
        is_link=probe(lambda path: False),
        is_folder=probe(lambda path: False),
        is_file=probe(lambda path: path in contents),
        entries=probe(lambda path: []),
        read_bytes=probe(contents.__getitem__),
    )

    check_neutral_login({"CLAUDE_CONFIG_DIR": str(config_dir)}, home, home / "work" / "series", login_files, DEFAULT_BINDING.plugin)

    assert config_dir / "settings.json" in probed
    assert not Path("/nowhere").exists()
