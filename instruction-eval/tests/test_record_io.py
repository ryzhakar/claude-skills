import hashlib
import shutil
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from instruction_eval.records import Refusal, SeriesFolder, load_record, write_file, write_record

FIXTURE_SERIES = Path(__file__).parent / "fixtures" / "record-io"


@pytest.fixture
def series(tmp_path):
    return SeriesFolder(Path(shutil.copytree(FIXTURE_SERIES, tmp_path / "series")))


def test_written_record_loads_back_with_inputs_naming_every_read(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml", "7-gate.yaml#repeats"])
    loaded = load_record(series, "r1/9-outcome.yaml")
    assert loaded["passed"] is True
    assert set(loaded["inputs"]) == {"series.yaml", "7-gate.yaml#repeats"}


def test_inputs_hold_the_sha256_of_the_whole_file_and_of_the_key_value_as_canonical_yaml(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml", "7-gate.yaml#keep_rule"])
    inputs = load_record(series, "r1/9-outcome.yaml")["inputs"]
    canonical_keep_rule = "rank:\n- completion\n- overreach\ntie: earliest\n"
    assert inputs == {
        "series.yaml": hashlib.sha256((series.root / "series.yaml").read_bytes()).hexdigest(),
        "7-gate.yaml#keep_rule": hashlib.sha256(canonical_keep_rule.encode()).hexdigest(),
    }


def test_writing_an_existing_file_refuses_and_keeps_the_first_bytes_alone(series):
    write_file(series, "r1/2-instruction.md", b"first")
    with pytest.raises(Refusal, match=r"^already written: r1/2-instruction.md$"):
        write_file(series, "r1/2-instruction.md", b"second")
    assert (series.root / "r1/2-instruction.md").read_bytes() == b"first"
    assert [entry.name for entry in (series.root / "r1").iterdir()] == ["2-instruction.md"]


def test_loading_a_record_after_its_consumed_key_changed_refuses_as_stale(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats"])
    gate = series.root / "7-gate.yaml"
    gate.write_text(gate.read_text().replace("repeats: 3", "repeats: 4"))
    with pytest.raises(Refusal, match=r"^stale: r1/9-outcome.yaml \(input 7-gate.yaml#repeats changed\)$"):
        load_record(series, "r1/9-outcome.yaml")


def test_editing_an_unconsumed_key_or_restyling_a_consumed_one_keeps_the_record_loadable(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#keep_rule"])
    (series.root / "7-gate.yaml").write_text(
        "keep_rule: {tie: earliest, rank: [completion, overreach]}\nlevel: 0.95\nrepeats: 3\ndone_by: judge\n"
    )
    assert load_record(series, "r1/9-outcome.yaml")["passed"] is True


def test_loading_a_record_after_a_whole_file_input_changed_refuses_as_stale(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml"])
    with (series.root / "series.yaml").open("a") as series_file:
        series_file.write("\n")
    with pytest.raises(Refusal, match=r"^stale: r1/9-outcome.yaml \(input series.yaml changed\)$"):
        load_record(series, "r1/9-outcome.yaml")


@pytest.mark.parametrize("entry", ["series.yaml", "7-gate.yaml#repeats"])
def test_loading_a_record_after_its_input_was_deleted_refuses_naming_the_missing_input(series, entry):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, [entry])
    missing_path = entry.partition("#")[0]
    (series.root / missing_path).unlink()
    with pytest.raises(Refusal, match=rf"^missing input: {missing_path}$"):
        load_record(series, "r1/9-outcome.yaml")


def test_loading_a_record_after_its_consumed_key_was_removed_refuses_naming_the_missing_key(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats"])
    gate = series.root / "7-gate.yaml"
    gate.write_text(gate.read_text().replace("repeats: 3\n", ""))
    with pytest.raises(Refusal, match=r"^missing input: 7-gate.yaml#repeats$"):
        load_record(series, "r1/9-outcome.yaml")


def test_loading_an_absent_record_refuses_naming_it(series):
    with pytest.raises(Refusal, match=r"^missing record: r1/9-outcome.yaml$"):
        load_record(series, "r1/9-outcome.yaml")


@pytest.mark.parametrize("content", [b"- passed\n", b"passed: true\n", b"passed: true\ninputs: [series.yaml]\n"])
def test_loading_a_record_without_an_inputs_map_refuses_as_malformed(series, content):
    series.write_once("r1/9-outcome.yaml", content)
    with pytest.raises(Refusal, match=r"^malformed record: r1/9-outcome.yaml \(no inputs map\)$"):
        load_record(series, "r1/9-outcome.yaml")


@dataclass
class ReadCountingFiles:
    folder: SeriesFolder
    reads: Counter = field(default_factory=Counter)

    def read_bytes(self, path):
        self.reads[path] += 1
        return self.folder.read_bytes(path)

    def write_once(self, path, content):
        self.folder.write_once(path, content)


def test_a_file_consumed_under_several_keys_is_read_once_per_write_and_once_per_load(series):
    files = ReadCountingFiles(series)
    write_record(files, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats", "7-gate.yaml#level"])
    load_record(files, "r1/9-outcome.yaml")
    assert files.reads["7-gate.yaml"] == 2
