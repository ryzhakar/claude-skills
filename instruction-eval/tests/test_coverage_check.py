import pytest
import yaml

from instruction_eval.coverage import coverage_check
from instruction_eval.records import Refusal, SeriesFolder

DEMANDS = [
    {"id": "d-a", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"},
    {"id": "d-b", "text": "Never hedge.", "boundary": "Numbers are exempt.", "counted_by": "judge"},
]
INSTRUCTION = "Be terse. Never hedge. Be terse again.\n"
COVERAGE = {
    "demands": {"d-a": [1, 3], "d-b": [2]},
    "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a"]},
}
COVERAGE_PATH = "r1/3-coverage.yaml"


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    target = files.root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(document))


def covered_series(tmp_path, coverage: dict = COVERAGE, instruction: str = INSTRUCTION, demands: list[dict] = DEMANDS) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_yaml(files, "2-demands.yaml", {"demands": demands})
    (tmp_path / "r1").mkdir()
    (tmp_path / "r1/2-instruction.md").write_text(instruction)
    write_yaml(files, COVERAGE_PATH, coverage)
    return files


def test_a_coverage_mapping_every_demand_and_sentence_both_ways_passes(tmp_path):
    files = covered_series(tmp_path)

    assert coverage_check(files, "r1") is None


def test_a_demand_the_coverage_leaves_unmapped_refuses_naming_it(tmp_path):
    coverage = {"demands": {"d-a": [1, 3]}, "sentences": {1: ["d-a"], 2: ["d-a"], 3: ["d-a"]}}
    files = covered_series(tmp_path, coverage=coverage)

    with pytest.raises(Refusal, match=r"^unmapped demand: d-b \(r1/3-coverage\.yaml\)$"):
        coverage_check(files, "r1")


@pytest.mark.parametrize(
    "coverage",
    [
        {"demands": {"d-a": [1, 4], "d-b": [2]}, "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a"]}},
        {"demands": {"d-a": [1, 3], "d-b": [2]}, "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a"], 4: ["d-b"]}},
    ],
    ids=["demand-map", "sentence-map"],
)
def test_a_sentence_number_outside_the_text_refuses_naming_it(tmp_path, coverage):
    files = covered_series(tmp_path, coverage=coverage)

    with pytest.raises(Refusal, match=r"^sentence number outside the text: 4 \(r1/3-coverage\.yaml\)$"):
        coverage_check(files, "r1")


def test_a_sentence_the_sentence_map_lacks_refuses_as_carrying_no_demand_imported(tmp_path):
    coverage = {"demands": {"d-a": [1], "d-b": [2]}, "sentences": {1: ["d-a"], 2: ["d-b"]}}
    files = covered_series(tmp_path, coverage=coverage)

    with pytest.raises(Refusal, match=r"^sentence 3 carries no demand \(imported\)$"):
        coverage_check(files, "r1")


@pytest.mark.parametrize(
    "coverage",
    [
        {"demands": {"d-a": [1, 3], "d-b": []}, "sentences": {1: ["d-a"], 3: ["d-a"]}},
        {"demands": {"d-a": [1, 3], "d-b": [2]}, "sentences": {1: ["d-a"], 2: [], 3: ["d-a"]}},
        {"demands": {"d-a": [0, 3], "d-b": [2]}, "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a"]}},
    ],
    ids=["empty-demand-list", "empty-sentence-list", "number-below-one"],
)
def test_a_coverage_breaking_its_schema_refuses_as_a_malformed_record(tmp_path, coverage):
    files = covered_series(tmp_path, coverage=coverage)

    with pytest.raises(Refusal, match=r"^malformed record: r1/3-coverage\.yaml "):
        coverage_check(files, "r1")


def test_a_revision_without_an_instruction_refuses(tmp_path):
    files = covered_series(tmp_path)
    (tmp_path / "r1/2-instruction.md").unlink()

    with pytest.raises(Refusal, match=r"^missing file: r1/2-instruction\.md$"):
        coverage_check(files, "r1")


def test_a_coverage_naming_a_demand_outside_the_series_refuses(tmp_path):
    coverage = {"demands": {"d-a": [1, 3], "d-b": [2], "d-c": [1]}, "sentences": {1: ["d-a", "d-c"], 2: ["d-b"], 3: ["d-a"]}}
    files = covered_series(tmp_path, coverage=coverage)

    with pytest.raises(Refusal, match=r"^unresolved demand: d-c \(r1/3-coverage\.yaml\)$"):
        coverage_check(files, "r1")


@pytest.mark.parametrize(
    "coverage",
    [
        {"demands": {"d-a": [1, 3], "d-b": [2, 3]}, "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a"]}},
        {"demands": {"d-a": [1, 3], "d-b": [2]}, "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a", "d-b"]}},
        {"demands": {"d-a": [1, 3], "d-b": {"dropped": "unmeasurable"}}, "sentences": {1: ["d-a"], 2: ["d-b"], 3: ["d-a"]}},
    ],
    ids=["demand-lists-a-sentence-lacking-it", "sentence-lists-a-demand-lacking-it", "sentence-lists-a-dropped-demand"],
)
def test_two_maps_that_disagree_refuse_naming_the_pair(tmp_path, coverage):
    files = covered_series(tmp_path, coverage=coverage)

    with pytest.raises(Refusal, match=r"^coverage maps disagree: demand d-b and sentence [23] \(r1/3-coverage\.yaml\)$"):
        coverage_check(files, "r1")


FIRST_DROPPING_D_B = {"demands": {"d-a": [1, 2, 3], "d-b": {"dropped": "unmeasurable"}}, "sentences": {1: ["d-a"], 2: ["d-a"], 3: ["d-a"]}}
SECOND_DROPPING_D_A = {"demands": {"d-a": {"dropped": "unmeasurable"}, "d-b": [1, 2, 3]}, "sentences": {1: ["d-b"], 2: ["d-b"], 3: ["d-b"]}}


def with_second_revision(files: SeriesFolder, coverage: dict) -> None:
    (files.root / "r2").mkdir()
    (files.root / "r2/2-instruction.md").write_text(INSTRUCTION)
    write_yaml(files, "r2/3-coverage.yaml", coverage)


def test_a_later_revision_dropping_the_demands_the_first_drops_passes(tmp_path):
    files = covered_series(tmp_path, coverage=FIRST_DROPPING_D_B)
    with_second_revision(files, FIRST_DROPPING_D_B)

    assert coverage_check(files, "r2") is None


def test_a_later_revision_dropping_other_demands_than_the_first_refuses_naming_them(tmp_path):
    files = covered_series(tmp_path, coverage=FIRST_DROPPING_D_B)
    with_second_revision(files, SECOND_DROPPING_D_A)

    with pytest.raises(Refusal, match=r"^dropped demands differ from r1: d-a, d-b \(r2/3-coverage\.yaml\)$"):
        coverage_check(files, "r2")
