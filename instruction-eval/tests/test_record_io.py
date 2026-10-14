import shutil
from pathlib import Path

import pytest

from instruction_eval.records import load_record, write_record

FIXTURE_SERIES = Path(__file__).parent / "fixtures" / "record-io"


@pytest.fixture
def series(tmp_path):
    return Path(shutil.copytree(FIXTURE_SERIES, tmp_path / "series"))


def test_written_record_loads_back_with_inputs_naming_every_read(series):
    write_record(series, "r1/9-outcome.yaml", {"passed": True}, ["series.yaml", "7-gate.yaml#repeats"])
    loaded = load_record(series, "r1/9-outcome.yaml")
    assert loaded["passed"] is True
    assert set(loaded["inputs"]) == {"series.yaml", "7-gate.yaml#repeats"}
