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


FINGERPRINT_OUTPUT = "model: gpt-5-mini\nbuild: b1\ntemperature: 0.7\n"
DEMANDS = {"demands": [{"id": "d-one", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
OPEN_MESSAGE = "Explain tides.\n"
TASKS = {
    "tasks": [
        {"id": "t-open", "tempts": "d-one", "split": "open", "message": OPEN_MESSAGE, "answer_key": None},
        {"id": "t-sealed", "tempts": "d-one", "split": "sealed", "message": "Explain rain.", "answer_key": None},
    ],
    "conversations": [],
}
COVERAGE = {"demands": {"d-one": [1]}, "sentences": {1: ["d-one"]}}
CONDITIONS_BY_NAME = ["aim", "empty", "instruction", "placebo"]


def write_script(path: Path, body: str) -> Path:
    path.write_text(f"#!/bin/sh\n{body}\n")
    path.chmod(0o755)
    return path


def write_yaml(path: Path, document: object) -> None:
    path.write_text(yaml.safe_dump(document))


@pytest.fixture
def command_series(tmp_path, run) -> Path:
    (tmp_path / "instruction.md").write_text("Be terse.\n")
    created = run(tmp_path, "series", "new", "demo", "--instruction", "instruction.md", "--reader-kind", "command")
    folder = Path(created.stdout.strip())
    fakes = tmp_path / "fakes"
    fakes.mkdir()
    reader = write_script(fakes / "reader", "cat >/dev/null; echo terse-reply")
    fingerprint = write_script(fakes / "fingerprint", f"printf '{FINGERPRINT_OUTPUT}'")
    placebo = tmp_path / "gardening.md"
    placebo.write_text("Gardens bloom early.\n")
    write_yaml(folder / "2-demands.yaml", DEMANDS)
    write_yaml(folder / "3-tasks.yaml", TASKS)
    write_yaml(folder / "4-conditions.yaml", {"controls": ["empty", "aim", "placebo"], "aim": "Be terse.", "placebo_source": str(placebo), "omissions": "none"})
    write_yaml(
        folder / "5-reader.yaml",
        {"kind": "command", "model": "gpt-5-mini", "command": [str(reader), "{condition}"], "fingerprint": [str(fingerprint)], "sampling": {"temperature": 0.7}},
    )
    write_yaml(folder / "7-gate.yaml", {"repeats": 2})
    write_yaml(folder / "r1/3-coverage.yaml", COVERAGE)
    return folder


def test_demands_check_passes_in_silence_and_refuses_a_repeated_demand_in_one_line(command_series, run):
    passed = run(command_series, "demands", "check")
    assert (passed.returncode, passed.stdout, passed.stderr) == (0, "", "")
    write_yaml(command_series / "2-demands.yaml", {"demands": [*DEMANDS["demands"], *DEMANDS["demands"]]})
    refused = run(command_series, "demands", "check")
    assert refused.returncode == 1
    assert refused.stderr == "duplicate demand id: d-one (2-demands.yaml)\n"


def test_reader_fingerprint_prints_the_parsed_output_with_its_hash(command_series, run):
    result = run(command_series, "reader", "fingerprint")
    assert result.returncode == 0, result.stderr
    printed = yaml.safe_load(result.stdout)
    assert printed["fingerprint"] == {"model": "gpt-5-mini", "build": "b1", "temperature": 0.7}
    assert len(printed["fingerprint_hash"]) == 64


def test_revision_ask_refuses_a_condition_outside_the_revisions_set(command_series, run):
    result = run(command_series, "revision", "ask", "r1", "--conditions", "omit-3")
    assert result.returncode == 1
    assert result.stderr == f"unknown condition: omit-3 (revision r1 has {', '.join(CONDITIONS_BY_NAME)})\n"
    assert not (command_series / "r1/5-replies").exists()


def test_revision_ask_through_a_command_reader_answers_only_the_named_conditions(command_series, run):
    prepared = run(command_series, "reader", "prepare", "r1")
    assert prepared.returncode == 0, prepared.stderr
    asked = run(command_series, "revision", "ask", "r1", "--conditions", "instruction")
    assert asked.returncode == 0, asked.stderr
    assert asked.stdout == ""
    replies = sorted(path.relative_to(command_series).as_posix() for path in (command_series / "r1/5-replies").rglob("*.yaml"))
    assert replies == [
        f"r1/5-replies/instruction/{task}/repeat-{repeat}.yaml" for task in ("t-open", "t-sealed") for repeat in (1, 2)
    ]
    collected = run(command_series, "revision", "collect", "r1")
    assert collected.returncode == 1
    assert collected.stderr == "missing replies: 12, first r1/5-replies/aim/t-open/repeat-1.yaml\n"


def test_judge_calibrate_runs_stage_one_until_the_latest_attempt_holds_origins_then_stage_two(command_series, run):
    attempt = command_series / "6-judge/calibration/attempt-1"
    attempt.mkdir(parents=True)
    (attempt / "plan.yaml").write_text("{}\n")
    stage_one = run(command_series, "judge", "calibrate")
    assert stage_one.returncode == 1
    assert stage_one.stderr.startswith("missing brief: 6-judge/brief.md, start from ")
    assert stage_one.stderr.strip().endswith("templates/judge-brief.md")
    (attempt / "origins.yaml").write_text("{}\n")
    stage_two = run(command_series, "judge", "calibrate")
    assert stage_two.returncode == 1
    assert stage_two.stderr.startswith("malformed record: 6-judge/calibration/attempt-1/plan.yaml")


def test_series_freeze_refuses_a_series_whose_command_reader_cannot_fingerprint(command_series, run):
    write_script(Path(yaml.safe_load((command_series / "5-reader.yaml").read_text())["fingerprint"][0]), "exit 3")
    result = run(command_series, "series", "freeze")
    assert result.returncode == 1
    assert result.stderr == "fingerprint exited 3\n"
