import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "peers-facts"
SID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture
def home(tmp_path):
    path = tmp_path / "home"
    path.mkdir()
    return path


@pytest.fixture
def workdir(tmp_path):
    path = tmp_path / "work"
    path.mkdir()
    return path


def run(home, cwd, **env_extra):
    env = {
        "PATH": os.environ["PATH"],
        "HOME": str(home),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_SYSTEM": "/dev/null",
    }
    env.update(env_extra)
    result = subprocess.run(
        [str(SCRIPT)], cwd=cwd, env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    facts = {}
    for line in result.stdout.splitlines():
        key, _, value = line.partition(": ")
        facts[key] = value
    return facts


def git(cwd, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=cwd, check=True, capture_output=True,
        env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null"},
    )


def make_repo(path):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "-b", "main")
    git(path, "commit", "-q", "--allow-empty", "-m", "init")
    return path


def write_transcript(home, entries, sid=SID):
    d = home / ".claude" / "projects" / "proj"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{sid}.jsonl"
    path.write_text("".join(json.dumps(e) + "\n" for e in entries))
    return path


def assistant(model, content=()):
    return {"type": "assistant", "message": {"model": model, "content": list(content)}}


def test_model_is_last_real_assistant_model(home, workdir):
    agent_call = {
        "type": "tool_use", "name": "Agent",
        "input": {"model": "sonnet", "prompt": "x"},
    }
    write_transcript(home, [
        {"type": "user", "message": {"content": "hi"}},
        assistant("claude-opus-4-1"),
        assistant("claude-real-model", [agent_call]),
        assistant("<synthetic>"),
    ])
    facts = run(home, workdir, CLAUDE_CODE_SESSION_ID=SID)
    assert facts["model"] == "claude-real-model"
    assert facts["session_id"] == SID
    assert facts["login"] == str(home / ".claude")


def test_newest_transcript_wins(home, workdir):
    old = write_transcript(home, [assistant("old-model")])
    d = home / ".claude" / "projects" / "other"
    d.mkdir()
    new = d / f"{SID}.jsonl"
    new.write_text(json.dumps(assistant("new-model")) + "\n")
    os.utime(old, (1, 1))
    facts = run(home, workdir, CLAUDE_CODE_SESSION_ID=SID)
    assert facts["model"] == "new-model"


def test_missing_session_id_omits_model_and_id(home, workdir):
    write_transcript(home, [assistant("claude-real-model")])
    facts = run(home, workdir)
    assert "model" not in facts
    assert "session_id" not in facts


def test_missing_transcript_omits_model(home, workdir):
    facts = run(home, workdir, CLAUDE_CODE_SESSION_ID=SID)
    assert "model" not in facts


def test_config_dir_override(home, workdir, tmp_path):
    cfg = tmp_path / "cfg"
    d = cfg / "projects" / "p"
    d.mkdir(parents=True)
    (d / f"{SID}.jsonl").write_text(json.dumps(assistant("cfg-model")) + "\n")
    facts = run(home, workdir, CLAUDE_CODE_SESSION_ID=SID, CLAUDE_CONFIG_DIR=str(cfg))
    assert facts["model"] == "cfg-model"
    assert facts["login"] == str(cfg)


def test_git_repo_facts(home, tmp_path):
    repo = make_repo(tmp_path / "repo")
    facts = run(home, repo)
    assert Path(facts["checkout"]).resolve() == repo.resolve()
    assert facts["branch"] == "main"
    assert Path(facts["project"]).resolve() == repo.resolve()


def test_worktree_project_is_main_repo(home, tmp_path):
    repo = make_repo(tmp_path / "repo")
    wt = tmp_path / "wt"
    git(repo, "worktree", "add", "-q", "-b", "feat", str(wt))
    facts = run(home, wt)
    assert Path(facts["checkout"]).resolve() == wt.resolve()
    assert facts["branch"] == "feat"
    assert Path(facts["project"]).resolve() == repo.resolve()


def test_outside_git_project_is_cwd(home, workdir):
    facts = run(home, workdir)
    assert "checkout" not in facts
    assert "branch" not in facts
    assert facts["project"] == facts["cwd"]


def test_manifestos_from_checkout(home, tmp_path):
    repo = make_repo(tmp_path / "repo")
    (repo / ".manifestos.yaml").write_text(
        "me:\n  - name: ignored\nyou:\n  - name: alpha\n    path: a\n  - name: beta\n"
    )
    facts = run(home, repo)
    assert facts["manifestos_declared"] == "[alpha, beta]"


def test_manifestos_prefer_project_dir(home, tmp_path):
    repo = make_repo(tmp_path / "repo")
    (repo / ".manifestos.yaml").write_text("you:\n  - name: checkout-one\n")
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / ".manifestos.yaml").write_text("you:\n  - name: proj-one\n")
    facts = run(home, repo, CLAUDE_PROJECT_DIR=str(proj))
    assert facts["manifestos_declared"] == "[proj-one]"


def test_no_manifestos_file_omits_key(home, workdir):
    assert "manifestos_declared" not in run(home, workdir)


def test_root_default_and_override(home, workdir, tmp_path):
    assert run(home, workdir)["root"] == str(home / ".local/share/claude-peers")
    xdg = tmp_path / "xdg"
    assert run(home, workdir, XDG_DATA_HOME=str(xdg))["root"] == str(xdg / "claude-peers")
    assert run(home, workdir, CLAUDE_PEERS_ROOT="/custom/root")["root"] == "/custom/root"


def test_stamps_present(home, workdir):
    facts = run(home, workdir)
    assert facts["stamp_utc"].endswith("Z")
    assert "T" in facts["stamp"]
