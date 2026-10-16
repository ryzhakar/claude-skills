import hashlib
import json
import os
import re
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = PLUGIN_ROOT / "bin" / "instruction-eval"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "walk"
COMMAND_TIMEOUT_SECONDS = 120
SERIES_NAME = "walk"
STOPPED_SERIES_NAME = "walk-stopped"
LAST_REVISION = 5
STOP_REASON = "no hypothesis clears the noise"
NEUTRAL_LOGIN = Path(".claudes-bare") / "readers"
REQUIRED_PLUGINS = {"instruction-eval@my-claude-skills": True, "manifesto@my-claude-skills": True}
JUDGE_SESSION = "walk-session"
JUDGE_DEMAND = "terse"
FAILING_DEMAND = "no-apology"
OATH_SKILL = "manifesto:manifesto-oath"
TRANSCRIPT_TIMESTAMP = "2026-10-14T19:00:43.000Z"
BLIND_ID_HEADING = re.compile(r"^## (b[0-9a-f]{8})$", re.MULTILINE)
VERDICT_PATH_LINE = re.compile(r"Write one YAML file to (\S+) with the Write tool")
REFERENCE_USER_RATING = "6-judge/calibration/attempt-1/reference-user.yaml"
DELETED_SENTENCE = 2
PREDICTED_SIZE = 0.5
SERIES_NEW = ("series", "new", SERIES_NAME, "--instruction", "writer/instruction.md", "--source", "writer/policy.md", "--reader-kind", "command")


def tree_bytes(root: Path) -> dict[str, bytes]:
    """Return every file under the root by its root-relative path, with its bytes."""
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}


@dataclass(frozen=True)
class CommandRun:
    """One launcher run inside a series folder: the command, the series tree before and after, and what it printed."""

    series: Path
    command: tuple[str, ...]
    before: Mapping[str, bytes]
    after: Mapping[str, bytes]
    stdout: str

    @property
    def created(self) -> set[str]:
        """Return the series paths the run wrote."""
        return set(self.after) - set(self.before)


@dataclass
class NeutralSession:
    """The neutral session the walk runs in: the real launcher under a fake home and the neutral login, recording each run's effect on its series."""

    home: Path
    uv_cache: str
    runs: list[CommandRun] = field(default_factory=list)

    @property
    def config_dir(self) -> Path:
        """Return the neutral login's config dir."""
        return self.home / NEUTRAL_LOGIN

    def launch(self, working_dir: Path, *command: str) -> str:
        """Run the launcher in the working dir, refusing a nonzero exit, and return what it printed."""
        environment = {key: value for key, value in os.environ.items() if key != "CLAUDE_CONFIG_DIR"}
        environment.update({"HOME": str(self.home), "UV_CACHE_DIR": self.uv_cache, "CLAUDE_CONFIG_DIR": str(self.config_dir)})
        finished = subprocess.run([str(LAUNCHER), *command], cwd=working_dir, env=environment, capture_output=True, text=True, timeout=COMMAND_TIMEOUT_SECONDS)
        assert finished.returncode == 0, f"{' '.join(command)}: {finished.stderr}"
        return finished.stdout

    def run(self, series: Path, *command: str) -> str:
        """Run the command in the series folder, record its effect on the series tree, and return what it printed."""
        before = tree_bytes(series)
        stdout = self.launch(series, *command)
        self.runs.append(CommandRun(series, command, before, tree_bytes(series), stdout))
        return stdout

    def create(self, working_dir: Path, *command: str) -> Path:
        """Run `series new` in the working dir, record the series it writes, and return the series folder."""
        stdout = self.launch(working_dir, *command)
        series = Path(stdout.strip())
        self.runs.append(CommandRun(series, command, {}, tree_bytes(series), stdout))
        return series


def write_neutral_login(config_dir: Path) -> None:
    """Write the neutral login: its settings enabling exactly the two required plugins, and nothing else."""
    config_dir.mkdir(parents=True)
    (config_dir / "settings.json").write_text(json.dumps({"enabledPlugins": REQUIRED_PLUGINS}))


def copy_fixture(name: str, target: Path) -> None:
    """Copy the walk fixture to the target path, making its folder."""
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(FIXTURES / name, target)


def write_yaml(path: Path, document: object) -> None:
    """Write the document as YAML at the path, making its folder."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(document, sort_keys=False))


def project_key(series: Path) -> str:
    """Return the config dir's project folder name of the series: its absolute path with each slash and dot a dash."""
    return re.sub(r"[/.]", "-", str(series))


def launched_agent_types(launch_list: str) -> list[str]:
    """Return the agent types the printed launch list names."""
    return [launch["agent_type"] for launch in yaml.safe_load(launch_list)["launches"]]


def scripted_verdict(blind_ids: Sequence[str]) -> dict:
    """Return the verdict a scripted judge gives: no breach of the judge demand and done, for every entry."""
    return {"verdicts": [{"id": blind_id, "breaches": {JUDGE_DEMAND: 0}, "done": True, "kind": "answer", "notes": "Plain answer."} for blind_id in blind_ids]}


def run_scripted_agent(session: NeutralSession, series: Path, agent_type: str, judge_model: str) -> Path:
    """Act as the launched judge or rater: read its definition, write the verdict it names, and leave its transcript in the neutral login; return the transcript."""
    body = (series / ".claude" / "agents" / f"{agent_type}.md").read_text()
    verdict_path = Path(VERDICT_PATH_LINE.search(body).group(1))
    write_yaml(verdict_path, scripted_verdict(BLIND_ID_HEADING.findall(body)))
    blocks = [
        {"type": "tool_use", "id": "toolu_1", "name": "Skill", "input": {"skill": OATH_SKILL}},
        {"type": "tool_use", "id": "toolu_2", "name": "Write", "input": {"file_path": str(verdict_path)}},
        {"type": "text", "text": "Done."},
    ]
    usage = {"input_tokens": 3, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 2}
    lines = [
        {"type": "user", "message": {"role": "user", "content": "Judge the packet."}, "timestamp": TRANSCRIPT_TIMESTAMP},
        {"type": "assistant", "message": {"model": judge_model, "id": "msg_A", "role": "assistant", "content": blocks, "usage": usage}, "timestamp": TRANSCRIPT_TIMESTAMP},
    ]
    transcript = session.config_dir / "projects" / project_key(series) / JUDGE_SESSION / "subagents" / f"agent-{agent_type}.jsonl"
    transcript.parent.mkdir(parents=True, exist_ok=True)
    transcript.write_text("".join(json.dumps(line) + "\n" for line in lines))
    transcript.with_suffix(".meta.json").write_text(json.dumps({"agentType": agent_type}))
    return transcript


def run_scripted_agents(session: NeutralSession, series: Path, launch_list: str) -> list[Path]:
    """Act as every agent the launch list names and return their transcripts."""
    judge_model = yaml.safe_load((FIXTURES / "plan.yaml").read_text())["judge_model"]
    return [run_scripted_agent(session, series, agent_type, judge_model) for agent_type in launched_agent_types(launch_list)]


def write_user_rating(series: Path) -> None:
    """Act as the user rater: rate every entry of the attempt's sample as the scripted judge does."""
    sample = (series / "6-judge/calibration/attempt-1/sample.md").read_text()
    write_yaml(series / REFERENCE_USER_RATING, scripted_verdict(BLIND_ID_HEADING.findall(sample)))


def hypothesis(series: Path, parent: str) -> dict:
    """Return the hypothesis that deleting the second sentence lowers the parent's apologies, reading the parent's open instruction replies."""
    origins = yaml.safe_load((series / parent / "6-origins.yaml").read_text())["ids"]
    read = sorted(blind_id for blind_id, origin in origins.items() if origin.get("condition") == "instruction" and origin["split"] == "open")
    return {
        "failing_demand": FAILING_DEMAND,
        "replies_read": read,
        "change": {"action": "delete", "sentence": DELETED_SENTENCE},
        "predicted_movement": {"direction": "down", "size": PREDICTED_SIZE},
    }


@dataclass(frozen=True)
class Walk:
    """A finished walk: the session's runs, the series, the series stopped by hand after r4, the writer's files, and the live instruction each keep wrote."""

    session: NeutralSession
    series: Path
    stopped_series: Path
    writer: Path
    kept_at_cap: bytes
    kept_at_stop: bytes


def judge_revision(session: NeutralSession, series: Path, revision: str) -> None:
    """Blind, judge with scripted judges, collect, and detect the revision."""
    session.run(series, "revision", "blind", revision)
    run_scripted_agents(session, series, session.run(series, "judge", "prepare", revision))
    session.run(series, "judge", "collect", revision)
    session.run(series, "revision", "detect", revision)


def walk_first_revision(session: NeutralSession, workspace: Path, writer: Path) -> Path:
    """Walk r1 from `series new` to `revision gate r1` and return the series folder."""
    live_instruction, source, placebo = writer / "instruction.md", writer / "policy.md", writer / "gardening.md"
    series = session.create(workspace, *SERIES_NEW)
    live_instruction.write_text(live_instruction.read_text() + "Draft.\n")
    source.write_text(source.read_text() + "Edited after its snapshot.\n")
    copy_fixture("2-demands.yaml", series / "2-demands.yaml")
    session.run(series, "demands", "check")
    copy_fixture("coverage-r1.yaml", series / "r1/3-coverage.yaml")
    session.run(series, "coverage", "check", "r1")
    write_yaml(series / "4-conditions.yaml", {"controls": ["empty", "aim", "placebo", "source"], "aim": "Answers stay plain and brief.", "placebo_source": str(placebo), "omissions": "none"})
    write_yaml(
        series / "5-reader.yaml",
        {
            "kind": "command",
            "model": "scripted-reader",
            "command": ["sh", str(FIXTURES / "reader.sh"), "{condition}"],
            "fingerprint": ["sh", str(FIXTURES / "fingerprint.sh")],
            "sampling": {"temperature": 0},
        },
    )
    copy_fixture("7-gate-started.yaml", series / "7-gate.yaml")
    copy_fixture("3-tasks.yaml", series / "3-tasks.yaml")
    session.run(series, "tasks", "check")
    session.run(series, "reader", "fingerprint")
    session.run(series, "reader", "prepare", "r1")
    placebo.write_text(placebo.read_text() + "Edited after its snapshot.\n")
    session.run(series, "revision", "ask", "r1")
    session.run(series, "revision", "collect", "r1")
    (series / "6-judge").mkdir(exist_ok=True)
    shutil.copyfile(PLUGIN_ROOT / "src/instruction_eval/templates/judge-brief.md", series / "6-judge/brief.md")
    copy_fixture("plan.yaml", series / "6-judge/calibration/attempt-1/plan.yaml")
    rating_launches = session.run(series, "judge", "calibrate")
    (series / "6-judge/brief.md").write_text((series / "6-judge/brief.md").read_text() + "\nEdited after its snapshot.\n")
    run_scripted_agents(session, series, rating_launches)
    write_user_rating(series)
    session.run(series, "judge", "calibrate")
    judge_revision(session, series, "r1")
    session.run(series, "series", "status")
    copy_fixture("7-gate-completed.yaml", series / "7-gate.yaml")
    session.run(series, "series", "freeze")
    session.run(series, "revision", "score", "r1")
    session.run(series, "revision", "gate", "r1")
    return series


def walk_later_revision(session: NeutralSession, series: Path, writer: Path, number: int) -> None:
    """Walk revision `number` from its hypothesis to its gate, the writer deleting the second sentence of the parent."""
    revision, parent = f"r{number}", f"r{number - 1}"
    write_yaml(series / revision / "1-hypothesis.yaml", hypothesis(series, parent))
    copy_fixture(f"instruction-{revision}.md", writer / "instruction.md")
    session.run(series, "revision", "new")
    copy_fixture(f"coverage-{revision}.yaml", series / revision / "3-coverage.yaml")
    session.run(series, "coverage", "check", revision)
    session.run(series, "reader", "prepare", revision)
    session.run(series, "revision", "ask", revision, "--conditions", "instruction")
    session.run(series, "revision", "collect", revision)
    judge_revision(session, series, revision)
    session.run(series, "revision", "score", revision)
    session.run(series, "revision", "gate", revision)


@pytest.fixture(scope="module")
def walk(tmp_path_factory) -> Walk:
    """Walk one series from `series new` through r5's cap to `series keep`, and a copy stopped by hand after r4 to its own keep, a script reading for the model and scripted stand-ins writing every rating, verdict, and transcript a model would."""
    workspace = tmp_path_factory.mktemp("walk")
    home = workspace / "home"
    writer = workspace / "writer"
    for name, fixture in (("instruction.md", "instruction-r1.md"), ("policy.md", "policy.md"), ("gardening.md", "gardening.md")):
        copy_fixture(fixture, writer / name)
    uv_cache = subprocess.run(["uv", "cache", "dir"], capture_output=True, text=True, check=True).stdout.strip()
    session = NeutralSession(home, uv_cache)
    write_neutral_login(session.config_dir)
    series = walk_first_revision(session, workspace, writer)
    for number in range(2, LAST_REVISION):
        walk_later_revision(session, series, writer, number)
    stopped_series = series.parent / STOPPED_SERIES_NAME
    shutil.copytree(series, stopped_series)
    walk_later_revision(session, series, writer, LAST_REVISION)
    session.run(series, "series", "keep")
    kept_at_cap = (writer / "instruction.md").read_bytes()
    session.run(stopped_series, "series", "stop", "--reason", STOP_REASON)
    session.run(stopped_series, "series", "keep")
    return Walk(session, series, stopped_series, writer, kept_at_cap, (writer / "instruction.md").read_bytes())


def test_series_keep_writes_the_kept_revision_over_the_live_instruction(walk):
    assert walk.kept_at_cap == (walk.series / f"r{LAST_REVISION}/2-instruction.md").read_bytes()
    assert walk.kept_at_stop == (walk.stopped_series / f"r{LAST_REVISION - 1}/2-instruction.md").read_bytes()


TASKS = [task["id"] for task in yaml.safe_load((FIXTURES / "3-tasks.yaml").read_text())["tasks"]]
REPEATS = yaml.safe_load((FIXTURES / "7-gate-started.yaml").read_text())["repeats"]
FIRST_CONDITIONS = ("aim", "empty", "instruction", "placebo", "source")
CALIBRATION_ATTEMPT = "6-judge/calibration/attempt-1"
SILENT_CHECKS = (("demands", "check"), ("coverage", "check", "r1"), ("tasks", "check"), ("reader", "fingerprint"))


def replies(revision: str, conditions: Sequence[str]) -> set[str]:
    """Return the reply files of every task and repeat of the conditions in the revision."""
    return {f"{revision}/5-replies/{condition}/{task}/repeat-{repeat}.yaml" for condition in conditions for task in TASKS for repeat in range(1, REPEATS + 1)}


def judged_revision_writes(revision: str) -> list[tuple[tuple[str, ...], set[str]]]:
    """Return the runs that judge and detect the revision, each with the files it writes."""
    return [
        (("revision", "blind", revision), {f"{revision}/6-origins.yaml", *(f"{revision}/6-packets/{task}.md" for task in TASKS)}),
        (("judge", "prepare", revision), {f".claude/agents/ie-judge-{revision}-{task}-k1.md" for task in TASKS}),
        (("judge", "collect", revision), {f"{revision}/7-collected.yaml"}),
        (("revision", "detect", revision), {f"{revision}/7-detectors.yaml"}),
    ]


def first_revision_writes() -> list[tuple[tuple[str, ...], set[str]]]:
    """Return the runs of r1 from `series new` to its gate, each with the files it writes."""
    return [
        (SERIES_NEW, {"series.yaml", "1-source/policy.md", "r1/2-instruction.md", "r1/2-revision.yaml"}),
        *((command, set()) for command in SILENT_CHECKS),
        (("reader", "prepare", "r1"), {"4-placebo-source.md", *(f"r1/4-conditions/{condition}.md" for condition in FIRST_CONDITIONS)}),
        (("revision", "ask", "r1"), replies("r1", FIRST_CONDITIONS)),
        (("revision", "collect", "r1"), set()),
        (
            ("judge", "calibrate"),
            {
                *(f".claude/agents/ie-calib-1-candidate-{run}.md" for run in (1, 2)),
                *(f"{CALIBRATION_ATTEMPT}/{name}" for name in ("brief.md", "sample.md", "origins.yaml")),
            },
        ),
        (("judge", "calibrate"), {f"{CALIBRATION_ATTEMPT}/agreement.yaml", "6-judge/calibration.yaml", "6-judge/anchors.yaml"}),
        *judged_revision_writes("r1"),
        (("series", "status"), set()),
        (("series", "freeze"), {"8-frozen.yaml"}),
        (("revision", "score", "r1"), {"r1/8-scores.yaml"}),
        (("revision", "gate", "r1"), {"r1/9-outcome.yaml"}),
    ]


def later_revision_writes(number: int) -> list[tuple[tuple[str, ...], set[str]]]:
    """Return the runs of a later revision from `revision new` to its gate, each with the files it writes, the last revision's gate stopping the series."""
    revision = f"r{number}"
    stop = {"9-stop.yaml"} if number == LAST_REVISION else set()
    return [
        (("revision", "new"), {f"{revision}/2-instruction.md", f"{revision}/2-revision.yaml"}),
        (("coverage", "check", revision), set()),
        (("reader", "prepare", revision), {f"{revision}/4-conditions/instruction.md"}),
        (("revision", "ask", revision, "--conditions", "instruction"), replies(revision, ["instruction"])),
        (("revision", "collect", revision), set()),
        *judged_revision_writes(revision),
        (("revision", "score", revision), {f"{revision}/8-scores.yaml"}),
        (("revision", "gate", revision), {f"{revision}/9-outcome.yaml", *stop}),
    ]


def test_each_command_writes_exactly_the_files_its_writes_cell_names(walk):
    expected = [
        *first_revision_writes(),
        *(run for number in range(2, LAST_REVISION + 1) for run in later_revision_writes(number)),
        (("series", "keep"), set()),
        (("series", "stop", "--reason", STOP_REASON), {"9-stop.yaml"}),
        (("series", "keep"), set()),
    ]

    assert [(run.command, run.created) for run in walk.session.runs] == expected


def test_no_command_rewrites_or_removes_a_series_file(walk):
    for run in walk.session.runs:
        assert {path: run.after.get(path) for path in run.before} == run.before, run.command


def current_hash(series: Path, entry: str) -> str:
    """Return the sha256 an input entry names now: of the whole series file, or of a `<path>#<key>` value dumped as canonical YAML."""
    path, _, key = entry.partition("#")
    content = (series / path).read_bytes()
    if key:
        content = yaml.safe_dump(yaml.safe_load(content)[key], sort_keys=True, default_flow_style=False).encode()
    return hashlib.sha256(content).hexdigest()


def recorded_hashes(series: Path) -> dict[str, dict[str, str]]:
    """Return by record every hash the series stores: each CLI record's `inputs` and `8-frozen.yaml`'s `hashes`."""
    records = {path: yaml.safe_load(content) for path, content in tree_bytes(series).items() if path.endswith(".yaml")}
    hashes = {path: record["inputs"] for path, record in records.items() if isinstance(record, dict) and "inputs" in record}
    return {**hashes, "8-frozen.yaml#hashes": records["8-frozen.yaml"]["hashes"]}


def test_after_series_keep_every_stored_hash_still_names_its_series_file_unchanged(walk):
    for series in (walk.series, walk.stopped_series):
        for record, hashes in recorded_hashes(series).items():
            assert all((series / entry.partition("#")[0]).resolve().is_relative_to(series) for entry in hashes), record
            assert {entry: current_hash(series, entry) for entry in hashes} == hashes, record
