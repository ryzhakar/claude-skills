import hashlib
import tempfile
from pathlib import Path

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from instruction_eval.reader import reader_fingerprint
from instruction_eval.records import Refusal, SeriesFolder, write_record

FINGERPRINT_COMMAND = ["llm-reply", "--version"]
COMMAND_SERIES = {"instruction": "/home/writer/terse.md", "sources": [], "reader_kind": "command", "created": "2026-10-14T10:00:00+00:00"}
COMMAND_READER = {
    "kind": "command",
    "model": "gpt-5-mini",
    "command": ["llm-reply", "--system-file", "{condition}"],
    "fingerprint": FINGERPRINT_COMMAND,
    "sampling": {"temperature": 0.7, "seed": "fixed"},
}
FINGERPRINT_OUTPUT = "model: gpt-5-mini\nbuild: 1.2.3\ntemperature: 0.7\nseed: fixed\n"


def command_series(tmp_path) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", COMMAND_SERIES, [])
    (tmp_path / "5-reader.yaml").write_text(yaml.safe_dump(COMMAND_READER))
    return files


def canonical_hash(output: dict) -> str:
    dumped = yaml.safe_dump(output, sort_keys=True, default_flow_style=False, allow_unicode=True)
    return hashlib.sha256(dumped.encode()).hexdigest()


def test_fingerprint_is_the_parsed_output_with_the_sha256_of_its_canonical_yaml(tmp_path):
    files = command_series(tmp_path)
    asked = []

    def run_fingerprint(command):
        asked.append(list(command))
        return FINGERPRINT_OUTPUT

    fingerprint = reader_fingerprint(files, run_fingerprint)

    parsed = {"model": "gpt-5-mini", "build": "1.2.3", "temperature": 0.7, "seed": "fixed"}
    assert asked == [FINGERPRINT_COMMAND]
    assert fingerprint.output == parsed
    assert fingerprint.fingerprint_hash == canonical_hash(parsed)


def test_an_agent_reader_refuses_and_runs_nothing(tmp_path):
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", {**COMMAND_SERIES, "reader_kind": "agent"}, [])
    (tmp_path / "5-reader.yaml").write_text(yaml.safe_dump({"kind": "agent", "model": "claude-sonnet-5-5"}))
    asked = []

    with pytest.raises(Refusal, match=r"^reader fingerprint refuses an agent reader$"):
        reader_fingerprint(files, lambda command: asked.append(command) or FINGERPRINT_OUTPUT)

    assert asked == []


@pytest.mark.parametrize("missing", ["model", "build", "temperature", "seed"])
def test_output_lacking_model_build_or_a_sampling_key_refuses_naming_the_key(tmp_path, missing):
    files = command_series(tmp_path)
    without = "".join(line + "\n" for line in FINGERPRINT_OUTPUT.splitlines() if not line.startswith(f"{missing}:"))

    with pytest.raises(Refusal, match=rf"^fingerprint output lacks {missing}$"):
        reader_fingerprint(files, lambda command: without)


@pytest.mark.parametrize("output", ["", "- model\n- build\n", "plain text", "a: [unclosed"])
def test_output_that_is_no_yaml_mapping_refuses(tmp_path, output):
    files = command_series(tmp_path)

    with pytest.raises(Refusal, match=r"^fingerprint output is not a YAML mapping$"):
        reader_fingerprint(files, lambda command: output)


def test_a_folder_that_is_no_series_refuses_and_runs_nothing(tmp_path):
    asked = []

    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        reader_fingerprint(SeriesFolder(tmp_path), lambda command: asked.append(command) or FINGERPRINT_OUTPUT)

    assert asked == []


def fingerprint_hash_of(files, output: str) -> str:
    return reader_fingerprint(files, lambda command: output).fingerprint_hash


PARSED_OUTPUT = {"model": "gpt-5-mini", "build": "1.2.3", "temperature": 0.7, "seed": "fixed"}


def output_text(items) -> str:
    return yaml.safe_dump(dict(items), sort_keys=False)


def hash_in_fresh_series(output: str) -> str:
    with tempfile.TemporaryDirectory() as folder:
        return fingerprint_hash_of(command_series(Path(folder)), output)


@given(items=st.permutations(list(PARSED_OUTPUT.items())))
def test_output_with_its_keys_in_any_order_hashes_the_same(items):
    assert hash_in_fresh_series(output_text(items)) == canonical_hash(PARSED_OUTPUT)


@given(key=st.sampled_from(sorted(PARSED_OUTPUT)), value=st.integers())
def test_output_with_any_one_value_changed_hashes_differently(key, value):
    assert hash_in_fresh_series(output_text({**PARSED_OUTPUT, key: value}.items())) != canonical_hash(PARSED_OUTPUT)
