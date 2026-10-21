import hashlib
import shutil
from pathlib import Path

import pytest

from instruction_eval.records import Refusal, SeriesFolder, load_record, write_file, write_record
from series_fixtures import ReadCountingFolder

FIXTURE_SERIES = Path(__file__).parent / "fixtures" / "record-io"


@pytest.fixture
def record_series(tmp_path):
    return SeriesFolder(Path(shutil.copytree(FIXTURE_SERIES, tmp_path / "series")))


def test_written_record_loads_back_with_inputs_naming_every_read(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml", "7-gate.yaml#repeats"])
    loaded = load_record(record_series, "r1/9-outcome.yaml")
    assert loaded["passed"] is True
    assert set(loaded["inputs"]) == {"series.yaml", "7-gate.yaml#repeats"}


def test_inputs_hold_the_sha256_of_the_whole_file_and_of_the_key_value_as_canonical_yaml(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml", "7-gate.yaml#keep_rule"])
    inputs = load_record(record_series, "r1/9-outcome.yaml")["inputs"]
    canonical_keep_rule = "rank:\n- completion\n- overreach\ntie: earliest\n"
    assert inputs == {
        "series.yaml": hashlib.sha256((record_series.root / "series.yaml").read_bytes()).hexdigest(),
        "7-gate.yaml#keep_rule": hashlib.sha256(canonical_keep_rule.encode()).hexdigest(),
    }


def test_writing_a_record_that_carries_its_own_inputs_refuses_and_writes_nothing(record_series):
    with pytest.raises(Refusal, match=r"^record r1/9-outcome.yaml carries inputs; inputs come from its reads$"):
        write_record(record_series, "r1/9-outcome.yaml", {"inputs": {"x": "1"}}, [])
    assert not (record_series.root / "r1/9-outcome.yaml").exists()


def test_writing_an_existing_file_refuses_and_keeps_the_first_bytes_alone(record_series):
    write_file(record_series, "r1/2-instruction.md", b"first")
    with pytest.raises(Refusal, match=r"^already written: r1/2-instruction.md$"):
        write_file(record_series, "r1/2-instruction.md", b"second")
    assert (record_series.root / "r1/2-instruction.md").read_bytes() == b"first"
    assert [entry.name for entry in (record_series.root / "r1").iterdir()] == ["2-instruction.md"]


def test_loading_a_record_after_its_consumed_key_changed_refuses_as_stale(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats"])
    gate = record_series.root / "7-gate.yaml"
    gate.write_text(gate.read_text().replace("repeats: 3", "repeats: 4"))
    with pytest.raises(Refusal, match=r"^stale: r1/9-outcome.yaml \(input 7-gate.yaml#repeats changed\)$"):
        load_record(record_series, "r1/9-outcome.yaml")


def test_editing_an_unconsumed_key_or_restyling_a_consumed_one_keeps_the_record_loadable(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#keep_rule"])
    (record_series.root / "7-gate.yaml").write_text(
        "keep_rule: {tie: earliest, rank: [completion, overreach]}\nlevel: 0.95\nrepeats: 3\ndone_by: judge\n"
    )
    assert load_record(record_series, "r1/9-outcome.yaml")["passed"] is True


def test_loading_a_record_after_a_whole_file_input_changed_refuses_as_stale(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml"])
    with (record_series.root / "series.yaml").open("a") as series_file:
        series_file.write("\n")
    with pytest.raises(Refusal, match=r"^stale: r1/9-outcome.yaml \(input series.yaml changed\)$"):
        load_record(record_series, "r1/9-outcome.yaml")


@pytest.mark.parametrize("entry", ["series.yaml", "7-gate.yaml#repeats"])
def test_loading_a_record_after_its_input_was_deleted_refuses_naming_the_missing_input(record_series, entry):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, [entry])
    missing_path = entry.partition("#")[0]
    (record_series.root / missing_path).unlink()
    with pytest.raises(Refusal, match=rf"^missing input: {missing_path}$"):
        load_record(record_series, "r1/9-outcome.yaml")


def test_loading_a_record_after_its_consumed_key_was_removed_refuses_naming_the_missing_key(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats"])
    gate = record_series.root / "7-gate.yaml"
    gate.write_text(gate.read_text().replace("repeats: 3\n", ""))
    with pytest.raises(Refusal, match=r"^missing input: 7-gate.yaml#repeats$"):
        load_record(record_series, "r1/9-outcome.yaml")


def test_loading_an_absent_record_refuses_naming_it(record_series):
    with pytest.raises(Refusal, match=r"^missing record: r1/9-outcome.yaml$"):
        load_record(record_series, "r1/9-outcome.yaml")


@pytest.mark.parametrize(
    "content",
    [
        b"- passed\n",
        b"passed: true\n",
        b"passed: true\ninputs: [series.yaml]\n",
        b"inputs: {1: abc}\n",
        b"inputs: {series.yaml: 1}\n",
    ],
)
def test_loading_a_record_without_an_inputs_map_refuses_as_malformed(record_series, content):
    record_series.write_once("r1/9-outcome.yaml", content)
    with pytest.raises(Refusal, match=r"^malformed record: r1/9-outcome.yaml \(no inputs map\)$"):
        load_record(record_series, "r1/9-outcome.yaml")


def test_loading_a_record_that_is_not_yaml_refuses_as_malformed(record_series):
    record_series.write_once("r1/9-outcome.yaml", b"inputs: [unclosed\n")
    with pytest.raises(Refusal, match=r"^malformed record: r1/9-outcome.yaml \(not YAML\)$"):
        load_record(record_series, "r1/9-outcome.yaml")


def test_writing_a_record_from_a_keyed_input_that_is_not_yaml_refuses_naming_the_input(record_series):
    (record_series.root / "7-gate.yaml").write_text("repeats: [unclosed\n")
    with pytest.raises(Refusal, match=r"^malformed input: 7-gate.yaml \(not YAML\)$"):
        write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats"])


def test_loading_a_record_after_its_keyed_input_stopped_being_yaml_refuses_naming_the_input(record_series):
    write_record(record_series, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats"])
    (record_series.root / "7-gate.yaml").write_text("repeats: [unclosed\n")
    with pytest.raises(Refusal, match=r"^malformed input: 7-gate.yaml \(not YAML\)$"):
        load_record(record_series, "r1/9-outcome.yaml")


def test_a_file_consumed_under_several_keys_is_read_once_per_write_and_once_per_load(record_series):
    files = ReadCountingFolder(record_series.root)
    write_record(files, "r1/9-outcome.yaml", {"passed": True}, ["7-gate.yaml#repeats", "7-gate.yaml#level"])
    load_record(files, "r1/9-outcome.yaml")
    assert files.reads["7-gate.yaml"] == 2
