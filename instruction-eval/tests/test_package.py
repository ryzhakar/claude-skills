import json
import tomllib
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAMES = {
    "series", "demands", "coverage", "tasks", "conditions", "reader",
    "judge", "revision", "scores", "gate", "records", "cli",
}


def test_manifest_declares_version_and_manifesto_dependency():
    manifest = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["version"] == "0.1.0"
    assert manifest["dependencies"] == ["manifesto"]


def test_package_holds_exactly_the_declared_modules():
    package_dir = PLUGIN_ROOT / "src" / "instruction_eval"
    present = {path.stem for path in package_dir.glob("*.py")}
    assert present == MODULE_NAMES | {"__init__"}


def test_lockfile_locks_yaml_parser_and_numpy():
    lock = tomllib.loads((PLUGIN_ROOT / "uv.lock").read_text())
    locked = {package["name"] for package in lock["package"]}
    assert {"pyyaml", "numpy"} <= locked


def test_plugin_ships_no_hooks():
    assert not (PLUGIN_ROOT / "hooks").exists()
