import json
from collections.abc import Mapping
from pathlib import Path

CONFIG_DIR_VARIABLE = "CLAUDE_CONFIG_DIR"
BARE_LOGINS_DIRNAME = ".claudes-bare"
SETTINGS_FILENAME = "settings.json"
MEMORY_FILENAME = "CLAUDE.md"
EXTENSION_FOLDERNAMES = ("agents", "skills")
ENABLED_PLUGINS_KEY = "enabledPlugins"
REQUIRED_PLUGINS = {
    "instruction-eval@my-claude-skills": True,
    "manifesto@my-claude-skills": True,
}


class NeutralLoginRefused(Exception):
    """Raised when the session is not the neutral login."""


def check_neutral_login(
    environ: Mapping[str, str], home: Path, working_dir: Path
) -> None:
    """Refuse unless the session runs under the neutral login at a clean working directory."""
    config_dir = _neutral_config_dir(environ, home)
    _refuse_claude_md(config_dir)
    _refuse_agents_and_skills(config_dir)
    _refuse_other_plugins(config_dir)
    _refuse_memory_files_in_ancestry(working_dir, home)


def _neutral_config_dir(environ: Mapping[str, str], home: Path) -> Path:
    """Return the config directory, refusing when it is unset or outside the bare logins folder."""
    configured = environ.get(CONFIG_DIR_VARIABLE)
    if not configured:
        raise NeutralLoginRefused(f"{CONFIG_DIR_VARIABLE} is unset")
    config_dir = Path(configured).resolve()
    bare_logins = (home / BARE_LOGINS_DIRNAME).resolve()
    if bare_logins not in config_dir.parents:
        raise NeutralLoginRefused(f"{config_dir} is outside {bare_logins}")
    return config_dir


def _refuse_claude_md(config_dir: Path) -> None:
    """Refuse when the config directory holds a CLAUDE.md."""
    memory_file = config_dir / MEMORY_FILENAME
    if memory_file.exists() or memory_file.is_symlink():
        raise NeutralLoginRefused(f"{memory_file} exists")


def _refuse_agents_and_skills(config_dir: Path) -> None:
    """Refuse when the config directory holds a non-empty or linked agents or skills folder."""
    for folder_name in EXTENSION_FOLDERNAMES:
        folder = config_dir / folder_name
        if folder.is_symlink():
            raise NeutralLoginRefused(f"{folder} is a link")
        if folder.exists() and not (folder.is_dir() and not any(folder.iterdir())):
            raise NeutralLoginRefused(f"{folder} is not an empty folder")


def _refuse_other_plugins(config_dir: Path) -> None:
    """Refuse unless enabledPlugins is exactly the two required plugins, both true."""
    settings_file = config_dir / SETTINGS_FILENAME
    if not settings_file.is_file():
        raise NeutralLoginRefused(f"{settings_file} is missing")
    try:
        settings = json.loads(settings_file.read_text())
    except json.JSONDecodeError as error:
        raise NeutralLoginRefused(f"{settings_file} is not JSON") from error
    enabled = settings.get(ENABLED_PLUGINS_KEY) if isinstance(settings, dict) else None
    if not isinstance(enabled, dict) or set(enabled) != set(REQUIRED_PLUGINS):
        raise NeutralLoginRefused(f"{ENABLED_PLUGINS_KEY} is not the two required plugins")
    if not all(value is True for value in enabled.values()):
        raise NeutralLoginRefused(f"{ENABLED_PLUGINS_KEY} holds a plugin not true")


def _refuse_memory_files_in_ancestry(working_dir: Path, home: Path) -> None:
    """Refuse when the working directory or an ancestor holds a memory file, sparing the home user memory."""
    ...
