import pytest
import yaml

from instruction_eval.demands import demands_check
from instruction_eval.records import Refusal, SeriesFolder

JUDGE_DEMAND = {"id": "be-terse", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}
PATTERN_DEMAND = {"id": "no-hedges", "text": "Never hedge.", "boundary": "Numbers are exempt.", "counted_by": "pattern", "pattern": r"\bmaybe\b"}
LONG_SENTENCES_DEMAND = {"id": "short-sentences", "text": "Keep sentences short.", "boundary": "Quotes are exempt.", "counted_by": "long-sentences", "limit": 25}


def series_holding(tmp_path, demands: list[dict]) -> SeriesFolder:
    (tmp_path / "2-demands.yaml").write_text(yaml.safe_dump({"demands": demands}))
    return SeriesFolder(tmp_path)


def test_a_demand_record_of_every_counting_kind_passes(tmp_path):
    files = series_holding(tmp_path, [JUDGE_DEMAND, PATTERN_DEMAND, LONG_SENTENCES_DEMAND])

    assert demands_check(files) is None


def test_a_duplicate_demand_id_refuses_naming_the_id(tmp_path):
    files = series_holding(tmp_path, [JUDGE_DEMAND, {**PATTERN_DEMAND, "id": JUDGE_DEMAND["id"]}])

    with pytest.raises(Refusal, match=r"^duplicate demand id: be-terse \(2-demands\.yaml\)$"):
        demands_check(files)


@pytest.mark.parametrize(
    "demand, reason",
    [
        ({**JUDGE_DEMAND, "boundary": ""}, "boundary"),
        ({**JUDGE_DEMAND, "id": "overreach"}, "overreach"),
        ({**JUDGE_DEMAND, "id": "completion"}, "completion"),
        ({**PATTERN_DEMAND, "limit": 3}, "limit"),
        ({**LONG_SENTENCES_DEMAND, "pattern": "x"}, "pattern"),
        ({**JUDGE_DEMAND, "pattern": "x"}, "pattern"),
        ({**JUDGE_DEMAND, "limit": 3}, "limit"),
        ({**PATTERN_DEMAND, "pattern": "("}, "pattern"),
        ({**LONG_SENTENCES_DEMAND, "limit": 0}, "limit"),
    ],
    ids=["empty-boundary", "overreach-id", "completion-id", "pattern-with-limit", "long-sentences-with-pattern", "judge-with-pattern", "judge-with-limit", "uncompilable-pattern", "zero-limit"],
)
def test_an_invalid_demand_refuses_naming_the_offending_key(tmp_path, demand, reason):
    files = series_holding(tmp_path, [demand])

    with pytest.raises(Refusal, match=rf"^malformed record: 2-demands\.yaml \(.*{reason}"):
        demands_check(files)


def test_a_missing_demand_record_refuses(tmp_path):
    with pytest.raises(Refusal):
        demands_check(SeriesFolder(tmp_path))
