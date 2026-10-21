import pytest

from instruction_eval.records import Refusal, SeriesFolder, replace_whole, write_record
from instruction_eval.series import series_keep
from series_fixtures import SERIES_BINDING, sha256, tree, write_revision


def kept_series(tmp_path, stop: dict | None) -> SeriesFolder:
    files = SeriesFolder(tmp_path / "series")
    live = tmp_path / "live.md"
    live.write_bytes(b"Edited while the series ran.\n")
    document = {"instruction": str(live), "sources": [], "reader_kind": "agent", "binding": SERIES_BINDING, "created": "2026-10-14T10:00:00+00:00"}
    write_record(files, "series.yaml", document, [])
    write_revision(files, 1)
    write_revision(files, 2)
    if stop is not None:
        write_record(files, "9-stop.yaml", stop, [])
    return files


def test_a_stopped_series_writes_the_kept_snapshot_to_the_live_instruction_path_leaving_the_series_folder_unchanged(tmp_path):
    files = kept_series(tmp_path, {"stop": "capped", "kept": "r1"})
    before = tree(files.root)
    series_hash = sha256(files.read_bytes("series.yaml"))

    series_keep(files, replace_whole)

    assert sha256((tmp_path / "live.md").read_bytes()) == sha256(files.read_bytes("r1/2-instruction.md"))
    assert tree(files.root) == before
    assert sha256(files.read_bytes("series.yaml")) == series_hash
    assert sorted(path.name for path in tmp_path.iterdir()) == ["live.md", "series"]


def test_the_kept_snapshot_reaches_the_live_instruction_only_through_the_replacement_it_is_handed(tmp_path):
    files = kept_series(tmp_path, {"stop": "capped", "kept": "r2"})
    replaced = []

    series_keep(files, lambda target, content: replaced.append((target, content)))

    assert replaced == [(tmp_path / "live.md", files.read_bytes("r2/2-instruction.md"))]
    assert (tmp_path / "live.md").read_bytes() == b"Edited while the series ran.\n"


def test_an_unstopped_series_refuses_and_leaves_the_live_instruction(tmp_path):
    files = kept_series(tmp_path, None)

    with pytest.raises(Refusal, match=r"^series not stopped$"):
        series_keep(files, replace_whole)
    assert (tmp_path / "live.md").read_bytes() == b"Edited while the series ran.\n"


def test_a_stop_keeping_nothing_refuses_and_leaves_the_live_instruction(tmp_path):
    files = kept_series(tmp_path, {"stop": "unresolvable", "kept": None, "reason": "none clears the noise"})

    with pytest.raises(Refusal, match=r"^no revision passed completion$"):
        series_keep(files, replace_whole)
    assert (tmp_path / "live.md").read_bytes() == b"Edited while the series ran.\n"


def test_a_folder_that_is_no_series_refuses(tmp_path):
    with pytest.raises(Refusal, match=r"^not a series folder: no series\.yaml$"):
        series_keep(SeriesFolder(tmp_path), replace_whole)
