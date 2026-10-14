import json
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol

CONFIG_DIR_VARIABLE = "CLAUDE_CONFIG_DIR"
BARE_LOGINS_DIRNAME = ".claudes-bare"
SETTINGS_FILENAME = "settings.json"
MEMORY_FILENAME = "CLAUDE.md"
EXTENSION_FOLDERNAMES = ("agents", "skills")
USER_MEMORY_RELATIVE_PATH = Path(".claude") / MEMORY_FILENAME
MEMORY_RELATIVE_PATHS = (
    Path(MEMORY_FILENAME),
    USER_MEMORY_RELATIVE_PATH,
    Path("CLAUDE.local.md"),
    Path(".manifestos.yaml"),
)
ENABLED_PLUGINS_KEY = "enabledPlugins"
REQUIRED_PLUGINS = {
    "instruction-eval@my-claude-skills": True,
    "manifesto@my-claude-skills": True,
}


class NeutralLoginRefused(Exception):
    """Raised when the session is not the neutral login."""


class FileSystem(Protocol):
    """The file-system reads the neutral login check needs."""

    def exists(self, path: Path) -> bool: ...

    def is_symlink(self, path: Path) -> bool: ...

    def is_dir(self, path: Path) -> bool: ...

    def listdir(self, path: Path) -> list[Path]: ...

    def read_text(self, path: Path) -> str: ...

    def resolve(self, path: Path) -> Path: ...


class LocalFileSystem:
    """The file system of the machine the process runs on."""

    def exists(self, path: Path) -> bool:
        return path.exists()

    def is_symlink(self, path: Path) -> bool:
        return path.is_symlink()

    def is_dir(self, path: Path) -> bool:
        return path.is_dir()

    def listdir(self, path: Path) -> list[Path]:
        return list(path.iterdir())

    def read_text(self, path: Path) -> str:
        return path.read_text()

    def resolve(self, path: Path) -> Path:
        return path.resolve()


def check_neutral_login(
    environ: Mapping[str, str],
    home: Path,
    working_dir: Path,
    file_system: FileSystem,
) -> None:
    """Refuse unless the session runs under the neutral login at a clean working directory."""
    config_dir = _neutral_config_dir(environ, home, file_system)
    _refuse_claude_md(config_dir, file_system)
    for folder_name in EXTENSION_FOLDERNAMES:
        _refuse_extension_folder(config_dir / folder_name, file_system)
    _refuse_other_plugins(config_dir, file_system)
    _refuse_memory_files_in_ancestry(working_dir, home, file_system)


def _neutral_config_dir(
    environ: Mapping[str, str], home: Path, file_system: FileSystem
) -> Path:
    """Return the config directory, refusing when it is unset or outside the bare logins folder."""
    configured = environ.get(CONFIG_DIR_VARIABLE)
    if not configured:
        raise NeutralLoginRefused(f"{CONFIG_DIR_VARIABLE} is unset")
    config_dir = file_system.resolve(Path(configured))
    bare_logins = file_system.resolve(home / BARE_LOGINS_DIRNAME)
    if bare_logins not in config_dir.parents:
        raise NeutralLoginRefused(f"{config_dir} is outside {bare_logins}")
    return config_dir


def _refuse_claude_md(config_dir: Path, file_system: FileSystem) -> None:
    """Refuse when the config directory holds a CLAUDE.md."""
    memory_file = config_dir / MEMORY_FILENAME
    if file_system.exists(memory_file) or file_system.is_symlink(memory_file):
        raise NeutralLoginRefused(f"{memory_file} exists")


def _refuse_extension_folder(folder: Path, file_system: FileSystem) -> None:
    """Refuse when the folder is linked or holds anything."""
    if file_system.is_symlink(folder):
        raise NeutralLoginRefused(f"{folder} is a link")
    if file_system.exists(folder) and not _is_empty_folder(folder, file_system):
        raise NeutralLoginRefused(f"{folder} is not an empty folder")


def _is_empty_folder(folder: Path, file_system: FileSystem) -> bool:
    """Report whether the path is a folder with no entries."""
    return file_system.is_dir(folder) and not file_system.listdir(folder)


def _refuse_other_plugins(config_dir: Path, file_system: FileSystem) -> None:
    """Refuse unless enabledPlugins is exactly the two required plugins, both true."""
    settings_file = config_dir / SETTINGS_FILENAME
    if not file_system.exists(settings_file):
        raise NeutralLoginRefused(f"{settings_file} is missing")
    try:
        settings = json.loads(file_system.read_text(settings_file))
    except json.JSONDecodeError as error:
        raise NeutralLoginRefused(f"{settings_file} is not JSON") from error
    enabled = settings.get(ENABLED_PLUGINS_KEY) if isinstance(settings, dict) else None
    if not isinstance(enabled, dict) or set(enabled) != set(REQUIRED_PLUGINS):
        raise NeutralLoginRefused(f"{ENABLED_PLUGINS_KEY} is not the two required plugins")
    if not all(value is True for value in enabled.values()):
        raise NeutralLoginRefused(f"{ENABLED_PLUGINS_KEY} holds a plugin not true")


def _refuse_memory_files_in_ancestry(
    working_dir: Path, home: Path, file_system: FileSystem
) -> None:
    """Refuse when the working directory or an ancestor holds a memory file, sparing the home user memory."""
    user_memory = file_system.resolve(home / USER_MEMORY_RELATIVE_PATH)
    resolved = file_system.resolve(working_dir)
    for folder in (resolved, *resolved.parents):
        for relative_path in MEMORY_RELATIVE_PATHS:
            memory_file = folder / relative_path
            if memory_file != user_memory and file_system.exists(memory_file):
                raise NeutralLoginRefused(f"{memory_file} exists")
