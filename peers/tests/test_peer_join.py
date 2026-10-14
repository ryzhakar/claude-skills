import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parent.parent / "hooks"
HOOKS_JSON = HOOKS_DIR / "hooks.json"
SCRIPT = HOOKS_DIR / "peer-join.sh"
JOIN_TEXT = "JOIN-FIXTURE: join the peer protocol.\n"
COMPACT_TEXT = "COMPACT-FIXTURE: rejoin the peer protocol.\n"


@pytest.fixture
def home(tmp_path):
    path = tmp_path / "home"
    path.mkdir()
    return path


@pytest.fixture
def plugin_root(tmp_path):
    root = tmp_path / "plugin"
    (root / "hooks" / "templates").mkdir(parents=True)
    shutil.copy(SCRIPT, root / "hooks" / "peer-join.sh")
    return root


def write_templates(plugin_root, join=JOIN_TEXT, compact=COMPACT_TEXT):
    templates = plugin_root / "hooks" / "templates"
    if join is not None:
        (templates / "peer-join.txt").write_text(join)
    if compact is not None:
        (templates / "peer-compact.txt").write_text(compact)


def peer_commands(source):
    """Commands the platform runs on a SessionStart of this source, from hooks.json."""
    entries = json.loads(HOOKS_JSON.read_text())["hooks"]["SessionStart"]
    return [
        hook["command"]
        for entry in entries
        if re.fullmatch(entry.get("matcher", ".*"), source)
        for hook in entry["hooks"]
        if "peer-join.sh" in hook["command"]
    ]


@pytest.fixture
def session_start(home, plugin_root):
    def run(source):
        (command,) = peer_commands(source)
        completed = subprocess.run(
            ["bash", "-c", command],
            input=json.dumps({"hook_event_name": "SessionStart", "source": source}),
            capture_output=True,
            text=True,
            env={"HOME": str(home), "CLAUDE_PLUGIN_ROOT": str(plugin_root), "PATH": "/usr/bin:/bin"},
        )
        assert completed.returncode == 0, completed.stderr
        return completed.stdout

    return run


def open_gate(home):
    (home / ".local" / "share" / "claude-peers").mkdir(parents=True)


def test_absent_gate_prints_nothing_for_every_source(home, plugin_root, session_start):
    write_templates(plugin_root)
    for source in ("startup", "resume", "clear", "fork", "compact"):
        assert session_start(source) == ""


def test_absent_gate_leaves_the_peers_directory_uncreated(home, plugin_root, session_start):
    write_templates(plugin_root)
    session_start("startup")
    session_start("compact")
    assert not (home / ".local" / "share" / "claude-peers").exists()


def test_startup_prints_the_join_text(home, plugin_root, session_start):
    write_templates(plugin_root)
    open_gate(home)
    assert session_start("startup") == JOIN_TEXT


@pytest.mark.parametrize("source", ["resume", "clear", "fork"])
def test_resume_clear_fork_print_the_join_text(home, plugin_root, session_start, source):
    write_templates(plugin_root)
    open_gate(home)
    assert session_start(source) == JOIN_TEXT


def test_compact_prints_the_compact_text(home, plugin_root, session_start):
    write_templates(plugin_root)
    open_gate(home)
    assert session_start("compact") == COMPACT_TEXT


@pytest.mark.parametrize("source", ["startup", "resume", "clear", "fork", "compact"])
def test_exactly_one_peer_hook_fires_per_source(source):
    assert len(peer_commands(source)) == 1


@pytest.mark.parametrize("source", ["startup", "resume", "clear", "fork"])
def test_missing_join_template_prints_nothing(home, plugin_root, session_start, source):
    write_templates(plugin_root, join=None)
    open_gate(home)
    assert session_start(source) == ""


def test_missing_compact_template_prints_nothing(home, plugin_root, session_start):
    write_templates(plugin_root, compact=None)
    open_gate(home)
    assert session_start("compact") == ""


def test_missing_template_leaves_the_other_source_working(home, plugin_root, session_start):
    write_templates(plugin_root, compact=None)
    open_gate(home)
    assert session_start("startup") == JOIN_TEXT


def run_script(home, plugin_root, **extra):
    return subprocess.run(
        ["bash", "-c", peer_commands("startup")[0]],
        capture_output=True,
        text=True,
        env={"HOME": str(home), "CLAUDE_PLUGIN_ROOT": str(plugin_root), "PATH": "/usr/bin:/bin", **extra},
    )


def test_xdg_data_home_opens_the_gate(home, plugin_root, tmp_path):
    write_templates(plugin_root)
    xdg = tmp_path / "xdg"
    (xdg / "claude-peers").mkdir(parents=True)
    assert run_script(home, plugin_root, XDG_DATA_HOME=str(xdg)).stdout == JOIN_TEXT


def test_peers_root_override_opens_the_gate(home, plugin_root, tmp_path):
    write_templates(plugin_root)
    root = tmp_path / "custom-root"
    root.mkdir()
    assert run_script(home, plugin_root, CLAUDE_PEERS_ROOT=str(root)).stdout == JOIN_TEXT


def test_home_dot_claude_peers_alone_does_not_open_the_gate(home, plugin_root):
    write_templates(plugin_root)
    (home / ".claude-peers").mkdir()
    assert run_script(home, plugin_root).stdout == ""


def test_unset_home_prints_nothing_and_exits_zero(plugin_root):
    write_templates(plugin_root)
    completed = subprocess.run(
        ["bash", str(plugin_root / "hooks" / "peer-join.sh"), "join"],
        capture_output=True,
        text=True,
        env={"CLAUDE_PLUGIN_ROOT": str(plugin_root), "PATH": "/usr/bin:/bin"},
    )
    assert (completed.returncode, completed.stdout) == (0, "")


def test_unknown_argument_prints_nothing_and_exits_zero(home, plugin_root):
    write_templates(plugin_root)
    open_gate(home)
    completed = subprocess.run(
        ["bash", str(plugin_root / "hooks" / "peer-join.sh"), "bogus"],
        capture_output=True,
        text=True,
        env={"HOME": str(home), "CLAUDE_PLUGIN_ROOT": str(plugin_root), "PATH": "/usr/bin:/bin"},
    )
    assert (completed.returncode, completed.stdout) == (0, "")


def test_root_placeholder_prints_the_default_root(home, plugin_root, session_start):
    write_templates(plugin_root, join="root=<root> again=<root>\n")
    open_gate(home)
    expected = f"{home}/.local/share/claude-peers"
    assert session_start("startup") == f"root={expected} again={expected}\n"


def test_root_placeholder_prints_the_override_root(home, plugin_root, tmp_path):
    root = tmp_path / "custom&root"
    root.mkdir()
    write_templates(plugin_root, join="root=<root>\n")
    assert run_script(home, plugin_root, CLAUDE_PEERS_ROOT=str(root)).stdout == f"root={root}\n"
