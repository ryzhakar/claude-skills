import json
from collections.abc import Mapping
from pathlib import Path

CONFIG_DIR_VARIABLE = "CLAUDE_CONFIG_DIR"
BARE_LOGINS_DIRNAME = ".claudes-bare"
SETTINGS_FILENAME = "settings.json"
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
    ...


def _refuse_claude_md(config_dir: Path) -> None:
    """Refuse when the config directory holds a CLAUDE.md."""
    ...


def _refuse_agents_and_skills(config_dir: Path) -> None:
    """Refuse when the config directory holds a non-empty or linked agents or skills folder."""
    ...


def _refuse_other_plugins(config_dir: Path) -> None:
    """Refuse unless enabledPlugins is exactly the two required plugins, both true."""
    ...


def _refuse_memory_files_in_ancestry(working_dir: Path, home: Path) -> None:
    """Refuse when the working directory or an ancestor holds a memory file, sparing the home user memory."""
    ...
