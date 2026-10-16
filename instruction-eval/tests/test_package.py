import json
import re
import tomllib
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PLUGIN_ROOT.parent
NUMBER_WORDS = (
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
)
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


def test_lockfile_names_no_loopback_index():
    assert "127.0.0.1" not in (PLUGIN_ROOT / "uv.lock").read_text()


def test_plugin_ships_no_hooks():
    assert not (PLUGIN_ROOT / "hooks").exists()


def test_marketplace_lists_the_plugin_at_its_version_and_the_readmes_name_it_and_its_skills():
    manifest = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text())
    marketplace = json.loads((REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json").read_text())
    entry = next(plugin for plugin in marketplace["plugins"] if plugin["name"] == "instruction-eval")
    assert (entry["source"], entry["version"]) == ("./instruction-eval/", manifest["version"])
    assert "[instruction-eval](instruction-eval/)" in (REPOSITORY_ROOT / "README.md").read_text()
    plugin_readme = (PLUGIN_ROOT / "README.md").read_text()
    assert all(f"skills/{skill.name}/SKILL.md" in plugin_readme for skill in (PLUGIN_ROOT / "skills").iterdir())


def test_capabilities_counts_every_plugin_directory():
    capabilities = (REPOSITORY_ROOT / "orchestration_log" / "reference" / "capabilities.md").read_text()
    counted = re.search(r"^(\w+) plugins, each a top-level directory", capabilities, re.MULTILINE).group(1)
    plugin_directories = list(REPOSITORY_ROOT.glob("*/.claude-plugin/plugin.json"))
    assert NUMBER_WORDS.index(counted.lower()) == len(plugin_directories)

