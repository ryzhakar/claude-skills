import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

from instruction_eval.records import RecordRefused, Series, parse_series

FIXTURES = Path(__file__).parent / "fixtures" / "user-record-schemas"


def fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text())


def test_series_loads_as_typed_record():
    series = parse_series(fixture("series.yaml"))
    assert series == Series(
        instruction=Path("/home/writer/instructions/terse.md"),
        sources=(Path("/home/writer/sources/strunk.md"), Path("/home/writer/sources/orwell.md")),
        reader_kind="agent",
        created=datetime(2026, 10, 14, 10, tzinfo=timezone(timedelta(hours=3))),
        inputs={},
    )


def edited(name: str, **changes: object) -> dict:
    document = fixture(name)
    for key, value in changes.items():
        if value is ABSENT:
            del document[key]
        else:
            document[key] = value
    return document


ABSENT = object()


@pytest.mark.parametrize(
    ("changes", "named"),
    [
        ({"reader_kind": "human"}, "reader_kind"),
        ({"instruction": "instructions/terse.md"}, "instruction"),
        ({"sources": ["/a.md", "b.md"]}, "sources[1]"),
        ({"created": "2026-10-14T10:00:00"}, "created"),
        ({"inputs": {"2-demands.yaml": "ABC"}}, "inputs"),
        ({"created": ABSENT}, "created"),
        ({"cause": "too long"}, "cause"),
    ],
)
def test_series_refuses_a_malformed_key(changes, named):
    with pytest.raises(RecordRefused, match=re.escape(named)):
        parse_series(edited("series.yaml", **changes))
