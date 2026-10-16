import os
import subprocess
from pathlib import Path

import pytest
import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = PLUGIN_ROOT / "bin" / "instruction-eval"
ENTRY_POINT_TIMEOUT_SECONDS = 120
INSTRUCTION = "Be terse. Never apologise.\n"


@pytest.fixture(scope="session")
def uv_cache() -> str:
    return subprocess.run(["uv", "cache", "dir"], capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def home(tmp_path) -> Path:
    (tmp_path / "home").mkdir()
    return tmp_path / "home"


@pytest.fixture
def run(home, uv_cache):
    def run_in(folder: Path, *args: str, extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
        environment = {key: value for key, value in os.environ.items() if key != "CLAUDE_CONFIG_DIR"}
        environment.update({"HOME": str(home), "UV_CACHE_DIR": uv_cache, **(extra_env or {})})
        return subprocess.run(
            [str(LAUNCHER), *args], cwd=folder, env=environment, capture_output=True, text=True, timeout=ENTRY_POINT_TIMEOUT_SECONDS
        )

    return run_in


@pytest.fixture
def series(tmp_path, run) -> Path:
    (tmp_path / "instruction.md").write_text(INSTRUCTION)
    created = run(tmp_path, "series", "new", "demo", "--instruction", "instruction.md", "--reader-kind", "command")
    assert created.returncode == 0, created.stderr
    return Path(created.stdout.strip())


def test_series_new_prints_the_folder_and_series_status_prints_its_standing(series, run, home):
    assert series == home / "instruction-series" / "demo"
    status = run(series, "series", "status")
    assert status.returncode == 0, status.stderr
    assert yaml.safe_load(status.stdout)["frozen"] is False


BARE_SERIES_REFUSALS = [
    (["demands", "check"], "missing record: 2-demands.yaml"),
    (["coverage", "check", "r1"], "missing record"),
    (["tasks", "check"], "missing record"),
    (["reader", "prepare", "r1"], "missing record"),
    (["revision", "collect", "r1"], "missing record"),
    (["revision", "blind", "r1"], "missing record"),
    (["revision", "detect", "r1"], "missing record"),
    (["revision", "score", "r1"], "missing record"),
    (["revision", "gate", "r1"], "missing record"),
    (["revision", "new"], "latest revision r1 is not gated"),
    (["series", "freeze"], "missing record"),
    (["series", "stop", "--reason", "done"], "no gated revision to stop on"),
    (["judge", "calibrate"], "missing record"),
    (["judge", "prepare", "r1"], "CLAUDE_CONFIG_DIR is unset"),
    (["judge", "collect", "r1"], "missing record"),
]


@pytest.mark.parametrize(("command", "refusal"), BARE_SERIES_REFUSALS, ids=[" ".join(command) for command, _ in BARE_SERIES_REFUSALS])
def test_a_command_the_series_cannot_yet_serve_prints_one_refusal_line_and_exits_one(series, run, command, refusal):
    result = run(series, *command)
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    assert len(result.stderr.strip().splitlines()) == 1
    assert refusal in result.stderr


def test_every_command_refuses_outside_a_series_folder(tmp_path, run):
    result = run(tmp_path, "series", "status")
    assert result.returncode == 1
    assert result.stderr == "not a series folder: no series.yaml\n"
