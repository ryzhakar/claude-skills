import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = PLUGIN_ROOT / "bin" / "instruction-eval"
SHELL = "/bin/sh"
MISSING_UV_EXIT_CODE = 127
FAKE_UV = '#!/bin/sh\nprintf "%s\\n" "$@"\n'


def install_fake_uv(directory: Path) -> Path:
    directory.mkdir()
    fake = directory / "uv"
    fake.write_text(FAKE_UV)
    fake.chmod(0o755)
    return directory


def run_launcher(path_to_launcher: Path, search_path: str, *args: str):
    return subprocess.run(
        [SHELL, str(path_to_launcher), *args],
        capture_output=True,
        text=True,
        env={"PATH": search_path},
    )


def test_symlinked_launcher_runs_uv_against_the_plugin_root(tmp_path):
    fake_bin = install_fake_uv(tmp_path / "fakebin")
    link = tmp_path / "linked-instruction-eval"
    link.symlink_to(LAUNCHER)
    result = run_launcher(link, f"{fake_bin}:/usr/bin:/bin", "series", "--x")
    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "run", "--project", str(PLUGIN_ROOT), "--locked", "--quiet",
        "instruction-eval", "series", "--x",
    ]


def test_missing_uv_reports_one_line_and_exits_127(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    result = run_launcher(LAUNCHER, str(empty))
    assert result.returncode == MISSING_UV_EXIT_CODE
    assert len(result.stderr.strip().splitlines()) == 1
    assert "uv" in result.stderr
