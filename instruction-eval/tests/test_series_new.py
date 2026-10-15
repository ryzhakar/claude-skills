import hashlib
import re
from datetime import datetime, timezone

import pytest
import yaml

from instruction_eval.records import Refusal
from instruction_eval.series import series_new

NOW = datetime(2026, 10, 14, 10, 0, tzinfo=timezone.utc)
INSTRUCTION = b"Be terse. Skip greetings.\n"


def tree(root):
    return sorted(f"{path.relative_to(root).as_posix()}{'/' if path.is_dir() else ''}" for path in root.rglob("*"))


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def new_series(tmp_path, name="terse", instruction="live.md", sources=(), reader_kind="agent"):
    (tmp_path / "home").mkdir(exist_ok=True)
    (tmp_path / "work").mkdir(exist_ok=True)
    return series_new(name, instruction, list(sources), reader_kind, tmp_path / "work", tmp_path / "home", NOW)


def test_a_bare_name_makes_the_series_folder_under_the_home_series_directory_holding_exactly_the_first_snapshots(tmp_path):
    (tmp_path / "work").mkdir()
    (tmp_path / "work/live.md").write_bytes(INSTRUCTION)
    (tmp_path / "work/facts.md").write_bytes(b"Tides.\n")

    files = new_series(tmp_path, sources=["facts.md"])

    root = tmp_path / "home/instruction-series/terse"
    assert files.root == root
    assert tree(root) == [
        ".claude/",
        ".claude/agents/",
        "1-source/",
        "1-source/facts.md",
        "r1/",
        "r1/2-instruction.md",
        "r1/2-revision.yaml",
        "series.yaml",
    ]
    assert (root / "1-source/facts.md").read_bytes() == b"Tides.\n"
    assert (root / "r1/2-instruction.md").read_bytes() == INSTRUCTION
    assert yaml.safe_load((root / "series.yaml").read_bytes()) == {
        "instruction": str(tmp_path / "work/live.md"),
        "sources": [str(tmp_path / "work/facts.md")],
        "reader_kind": "agent",
        "created": NOW.isoformat(),
        "inputs": {},
    }
    assert yaml.safe_load((root / "r1/2-revision.yaml").read_bytes()) == {
        "number": 1,
        "parent": None,
        "hash": sha256(INSTRUCTION),
        "parent_record": None,
        "change": None,
        "inputs": {},
    }


def test_a_value_holding_a_slash_is_the_folder_as_given_and_a_relative_one_resolves_against_the_working_directory(tmp_path):
    (tmp_path / "work").mkdir()
    (tmp_path / "work/live.md").write_bytes(INSTRUCTION)

    relative = new_series(tmp_path, name="runs/terse")
    absolute = new_series(tmp_path, name=str(tmp_path / "elsewhere/terse"))

    assert relative.root == tmp_path / "work/runs/terse"
    assert absolute.root == tmp_path / "elsewhere/terse"
    assert not (tmp_path / "home/instruction-series").exists()


def test_a_non_empty_folder_is_refused_and_an_empty_one_is_used(tmp_path):
    (tmp_path / "work").mkdir()
    (tmp_path / "work/live.md").write_bytes(INSTRUCTION)
    folder = tmp_path / "home/instruction-series/terse"
    (folder / ".claude").mkdir(parents=True)
    (folder / ".claude").rmdir()

    new_series(tmp_path)
    with pytest.raises(Refusal, match=rf"^series folder not empty: {re.escape(str(folder))}$"):
        new_series(tmp_path)


MEMORY_FILES = ["CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md", ".manifestos.yaml"]
PLACES = [
    ("work/terse", "work/terse"),
    ("work/a/b/c/terse", "work/a"),
    ("home/instruction-series/terse", "home"),
    ("elsewhere/terse", "elsewhere"),
    ("home/instruction-series/terse", ""),
]
REFUSED_CASES = [
    (memory_file, folder, holder)
    for memory_file in MEMORY_FILES
    for folder, holder in PLACES
    if (holder, memory_file) != ("home", ".claude/CLAUDE.md")
]


def plant(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"memory\n")


@pytest.mark.parametrize(("memory_file", "folder", "holder"), REFUSED_CASES)
def test_a_folder_that_or_whose_ancestor_holds_a_memory_file_is_refused_naming_it(tmp_path, memory_file, folder, holder):
    (tmp_path / "work").mkdir()
    (tmp_path / "work/live.md").write_bytes(INSTRUCTION)
    planted = tmp_path / holder / memory_file
    plant(planted)
    name = str(tmp_path / folder)

    with pytest.raises(Refusal, match=rf"^series folder under a memory file: {re.escape(str(planted))}$"):
        new_series(tmp_path, name=name)


def test_the_home_default_login_memory_file_is_no_reason_to_refuse(tmp_path):
    (tmp_path / "work").mkdir()
    (tmp_path / "work/live.md").write_bytes(INSTRUCTION)
    plant(tmp_path / "home/.claude/CLAUDE.md")

    new_series(tmp_path)
