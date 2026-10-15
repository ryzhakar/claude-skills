import hashlib
from pathlib import Path

import yaml

from instruction_eval.records import SeriesFolder, write_record
from instruction_eval.series import series_status
from series_fixtures import AGENT_SERIES, write_revision, write_yaml


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(path.relative_to(root).as_posix().encode())
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def status_of(files: SeriesFolder) -> dict:
    return yaml.safe_load(series_status(files))


def bare_series(tmp_path) -> SeriesFolder:
    files = SeriesFolder(tmp_path)
    write_record(files, "series.yaml", AGENT_SERIES, [])
    write_revision(files, 1)
    return files


def test_a_fresh_series_reports_its_parts_unfrozen_with_an_ungated_first_revision_and_changes_nothing(tmp_path):
    files = bare_series(tmp_path)
    write_yaml(files, "2-demands.yaml", {"demands": []})
    before = tree_hash(tmp_path)

    status = status_of(files)

    assert tree_hash(tmp_path) == before
    assert status["parts"] == ["series.yaml", "2-demands.yaml"]
    assert status["frozen"] is False
    assert status["revisions"] == {"r1": {"outcome": None, "changed_from_parent": None, "instruction_breaches": None, "completion_passed": None, "words": None}}
    assert status["stop"] is None
