import json
from pathlib import Path

import pytest
import yaml

from instruction_eval.reader import NeutralLoginRefused, reader_prepare
from instruction_eval.records import Refusal, SeriesFolder, write_file, write_record
from series_fixtures import sha256

REQUIRED_PLUGINS = {"instruction-eval@my-claude-skills": True, "manifesto@my-claude-skills": True}

SOURCE_PATH = Path("/home/writer/policy.md")
PLACEBO_PATH = Path("/home/writer/gardening.md")
PLACEBO_BYTES = b"Gardens bloom early\r\n"
SOURCE_BYTES = b"Policy text.\n"
FIRST_INSTRUCTION = b"Write briefly. Cite sources.\n"
AGENT_MODEL = "claude-sonnet-5-5"
CONDITIONS = {
    "controls": ["empty", "aim", "placebo", "source"],
    "aim": "Answers stay short.",
    "placebo_source": str(PLACEBO_PATH),
    "omissions": "every-sentence",
}
COMMAND_READER = {
    "kind": "command",
    "model": "gpt-5-mini",
    "command": ["llm-reply", "--system-file", "{condition}"],
    "fingerprint": ["llm-reply", "--version"],
    "sampling": {"temperature": 0.7},
}
AGENT_READER = {"kind": "agent", "model": AGENT_MODEL}
EXTERNAL_FILES = {PLACEBO_PATH: PLACEBO_BYTES}


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    write_file(files, path, yaml.safe_dump(document).encode())


def write_revision_text(files: SeriesFolder, number: int, text: bytes) -> None:
    revision = f"r{number}"
    first = number == 1
    write_file(files, f"{revision}/2-instruction.md", text)
    record = {
        "number": number,
        "parent": None if first else f"r{number - 1}",
        "hash": sha256(text),
        "parent_record": None if first else sha256(files.read_bytes(f"r{number - 1}/2-revision.yaml")),
        "change": None if first else {"action": "rewrite", "sentence": 1, "old": "Old.", "new": "New."},
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [] if first else [f"r{number - 1}/2-revision.yaml"])


def series_folder(tmp_path: Path, reader: dict) -> SeriesFolder:
    files = SeriesFolder(tmp_path / "series")
    series = {
        "instruction": "/home/writer/terse.md",
        "sources": [str(SOURCE_PATH)],
        "reader_kind": reader["kind"],
        "created": "2026-10-14T10:00:00+00:00",
    }
    write_record(files, "series.yaml", series, [])
    write_file(files, f"1-source/{SOURCE_PATH.name}", SOURCE_BYTES)
    write_yaml(files, "4-conditions.yaml", CONDITIONS)
    write_yaml(files, "5-reader.yaml", reader)
    write_revision_text(files, 1, FIRST_INSTRUCTION)
    return files


def prepare(files: SeriesFolder, revision: str) -> None:
    reader_prepare(files, revision, EXTERNAL_FILES.__getitem__, {}, files.root, files.root)


def written(files: SeriesFolder, folder: str) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in sorted((files.root / folder).iterdir())}


def test_first_revision_writes_its_instruction_every_control_and_every_omission_from_the_placebo_snapshot(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)

    prepare(files, "r1")

    assert files.read_bytes("4-placebo-source.md") == PLACEBO_BYTES
    assert written(files, "r1/4-conditions") == {
        "instruction.md": FIRST_INSTRUCTION,
        "empty.md": b"",
        "aim.md": b"Answers stay short.",
        "placebo.md": b"Gardens bloom early Gardens",
        "source.md": SOURCE_BYTES,
        "omit-1.md": b"Cite sources.\n",
        "omit-2.md": b"Write briefly.\n",
    }


def forbidden_read(path: Path) -> bytes:
    raise AssertionError(f"read external file {path}")


class NeutralLogin:
    def __init__(self, home: Path):
        self.home = home
        self.config_dir = home / ".claudes-bare" / "readers"
        self.config_dir.mkdir(parents=True)
        (self.config_dir / "settings.json").write_text(json.dumps({"enabledPlugins": REQUIRED_PLUGINS}))

    def environ(self) -> dict[str, str]:
        return {"CLAUDE_CONFIG_DIR": str(self.config_dir)}


def split_definition(definition: bytes) -> tuple[dict, bytes]:
    header, _, body = definition.removeprefix(b"---\n").partition(b"---\n")
    return yaml.safe_load(header), body


def agent_prepare(tmp_path: Path, files: SeriesFolder, revision: str) -> None:
    reader_prepare(files, revision, EXTERNAL_FILES.__getitem__, NeutralLogin(tmp_path / "home").environ(), tmp_path / "home", files.root)


def test_agent_reader_gets_one_definition_per_condition_with_the_condition_file_as_body(tmp_path):
    files = series_folder(tmp_path, AGENT_READER)

    agent_prepare(tmp_path, files, "r1")

    conditions = written(files, "r1/4-conditions")
    definitions = {Path(name).stem: split_definition(definition) for name, definition in written(files, ".claude/agents").items()}
    assert set(definitions) == {f"ie-reader-r1-{Path(name).stem}" for name in conditions}
    for name, (frontmatter, body) in definitions.items():
        condition = name.removeprefix("ie-reader-r1-")
        assert frontmatter["name"] == name
        assert frontmatter["description"] == "Generated agent; launch from the printed launch list only."
        assert frontmatter["model"] == AGENT_MODEL
        assert body == conditions[f"{condition}.md"]


def tree(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))


def test_a_folder_that_is_no_series_refuses(tmp_path):
    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        reader_prepare(SeriesFolder(tmp_path), "r1", forbidden_read, {}, tmp_path, tmp_path)


def test_revision_without_an_instruction_refuses_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^missing file: r2/2-instruction\.md$"):
        reader_prepare(files, "r2", forbidden_read, {}, files.root, files.root)

    assert tree(files.root) == before


def test_preparing_a_revision_twice_refuses_naming_the_first_file_already_written(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)
    prepare(files, "r1")

    with pytest.raises(Refusal, match=r"^already written: 4-placebo-source\.md$"):
        prepare(files, "r1")


def test_placebo_source_holding_no_word_refuses_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^placebo source holds no word: 4-placebo-source\.md$"):
        reader_prepare(files, "r1", {PLACEBO_PATH: b"-- ... --\n"}.__getitem__, {}, files.root, files.root)

    assert tree(files.root) == before


def missing_read(path: Path) -> bytes:
    raise FileNotFoundError(path)


def test_missing_placebo_source_refuses_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)
    before = tree(files.root)

    with pytest.raises(Refusal, match=rf"^missing placebo source: {PLACEBO_PATH}$"):
        reader_prepare(files, "r1", missing_read, {}, files.root, files.root)

    assert tree(files.root) == before


def test_placebo_source_that_is_not_utf8_refuses_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)
    before = tree(files.root)

    with pytest.raises(Refusal, match=r"^not UTF-8: 4-placebo-source\.md$"):
        reader_prepare(files, "r1", {PLACEBO_PATH: b"\xff\xfe"}.__getitem__, {}, files.root, files.root)

    assert tree(files.root) == before


def test_agent_reader_outside_the_neutral_login_refuses_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, AGENT_READER)
    before = tree(files.root)

    with pytest.raises(NeutralLoginRefused):
        reader_prepare(files, "r1", EXTERNAL_FILES.__getitem__, {}, tmp_path / "home", files.root)

    assert tree(files.root) == before


def test_agent_reader_below_a_claude_md_refuses_and_writes_nothing(tmp_path):
    files = series_folder(tmp_path, AGENT_READER)
    (tmp_path / "CLAUDE.md").write_text("memory")
    before = tree(files.root)

    with pytest.raises(NeutralLoginRefused):
        agent_prepare(tmp_path, files, "r1")

    assert tree(files.root) == before


def test_later_revision_writes_only_its_instruction_and_omissions_and_reads_no_external_file(tmp_path):
    files = series_folder(tmp_path, COMMAND_READER)
    prepare(files, "r1")
    write_revision_text(files, 2, b"Write briefly.\n\nCite sources. Name them.\n")

    reader_prepare(files, "r2", forbidden_read, {}, files.root, files.root)

    assert written(files, "r2/4-conditions") == {
        "instruction.md": b"Write briefly.\n\nCite sources. Name them.\n",
        "omit-1.md": b"Cite sources. Name them.\n",
        "omit-2.md": b"Write briefly.\n\nName them.\n",
        "omit-3.md": b"Write briefly.\n\nCite sources.\n",
    }
    assert files.read_bytes("4-placebo-source.md") == PLACEBO_BYTES
