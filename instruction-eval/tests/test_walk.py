import fnmatch
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
CALIBRATION_ATTEMPT = "6-judge/calibration/attempt-1"
REFERENCE_USER_RATING = f"{CALIBRATION_ATTEMPT}/reference-user.yaml"
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
    sample = (series / f"{CALIBRATION_ATTEMPT}/sample.md").read_text()
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
class ExternalEdit:
    """An external file edited after the series took it in: the bytes taken in, and the file's bytes once edited."""

    external: Path
    taken_in: bytes
    edited: bytes


def edit_after_intake(external: Path, taken_in: bytes, addition: str) -> ExternalEdit:
    """Append the addition to the external file the series took in as `taken_in`, and return the edit."""
    external.write_bytes(external.read_bytes() + addition.encode())
    return ExternalEdit(external, taken_in, external.read_bytes())


@dataclass(frozen=True)
class Walk:
    """A finished walk: the session's runs, the series, the series stopped by hand after r4, the writer's files, the external edits, and the live instruction each keep wrote."""

    session: NeutralSession
    series: Path
    stopped_series: Path
    writer: Path
    external_edits: list[ExternalEdit]
    kept_at_cap: bytes
    kept_at_stop: bytes


def judge_revision(session: NeutralSession, series: Path, revision: str) -> list[Path]:
    """Blind, judge with scripted judges, collect, and detect the revision, returning the judges' transcripts."""
    session.run(series, "revision", "blind", revision)
    transcripts = run_scripted_agents(session, series, session.run(series, "judge", "prepare", revision))
    session.run(series, "judge", "collect", revision)
    session.run(series, "revision", "detect", revision)
    return transcripts


EDIT_LINE = "Edited after its snapshot.\n"
TRANSCRIPT_EDIT_LINE = json.dumps({"type": "user", "message": {"role": "user", "content": "Thanks."}, "timestamp": TRANSCRIPT_TIMESTAMP}) + "\n"


def walk_first_revision(session: NeutralSession, workspace: Path, writer: Path) -> tuple[Path, list[ExternalEdit]]:
    """Walk r1 from `series new` to `revision gate r1`, editing each external file after the series takes it in, and return the series folder and the edits."""
    live_instruction, source, placebo = writer / "instruction.md", writer / "policy.md", writer / "gardening.md"
    series = session.create(workspace, *SERIES_NEW)
    edits = [
        edit_after_intake(live_instruction, (series / "r1/2-instruction.md").read_bytes(), EDIT_LINE),
        edit_after_intake(source, (series / "1-source/policy.md").read_bytes(), EDIT_LINE),
    ]
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
    edits.append(edit_after_intake(placebo, (series / "4-placebo-source.md").read_bytes(), EDIT_LINE))
    session.run(series, "revision", "ask", "r1")
    session.run(series, "revision", "collect", "r1")
    working_brief = series / "6-judge/brief.md"
    working_brief.parent.mkdir()
    shutil.copyfile(PLUGIN_ROOT / "src/instruction_eval/templates/judge-brief.md", working_brief)
    copy_fixture("plan.yaml", series / f"{CALIBRATION_ATTEMPT}/plan.yaml")
    rating_launches = session.run(series, "judge", "calibrate")
    edits.append(edit_after_intake(working_brief, (series / f"{CALIBRATION_ATTEMPT}/brief.md").read_bytes(), EDIT_LINE))
    run_scripted_agents(session, series, rating_launches)
    write_user_rating(series)
    session.run(series, "judge", "calibrate")
    judge_transcript = judge_revision(session, series, "r1")[0]
    edits.append(edit_after_intake(judge_transcript, judge_transcript.read_bytes(), TRANSCRIPT_EDIT_LINE))
    session.run(series, "series", "status")
    copy_fixture("7-gate-completed.yaml", series / "7-gate.yaml")
    session.run(series, "series", "freeze")
    session.run(series, "revision", "score", "r1")
    session.run(series, "revision", "gate", "r1")
    return series, edits


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
    series, external_edits = walk_first_revision(session, workspace, writer)
    for number in range(2, LAST_REVISION):
        walk_later_revision(session, series, writer, number)
    stopped_series = series.parent / STOPPED_SERIES_NAME
    shutil.copytree(series, stopped_series)
    walk_later_revision(session, series, writer, LAST_REVISION)
    session.run(series, "series", "keep")
    kept_at_cap = (writer / "instruction.md").read_bytes()
    session.run(stopped_series, "series", "stop", "--reason", STOP_REASON)
    session.run(stopped_series, "series", "keep")
    return Walk(session, series, stopped_series, writer, external_edits, kept_at_cap, (writer / "instruction.md").read_bytes())


def test_series_keep_writes_the_kept_revision_over_the_live_instruction(walk):
    assert walk.kept_at_cap == (walk.series / f"r{LAST_REVISION}/2-instruction.md").read_bytes()
    assert walk.kept_at_stop == (walk.stopped_series / f"r{LAST_REVISION - 1}/2-instruction.md").read_bytes()


TASKS = [task["id"] for task in yaml.safe_load((FIXTURES / "3-tasks.yaml").read_text())["tasks"]]
REPEATS = yaml.safe_load((FIXTURES / "7-gate-started.yaml").read_text())["repeats"]
FIRST_CONDITIONS = ("aim", "empty", "instruction", "placebo", "source")
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


def test_external_files_edited_after_the_series_takes_them_in_refuse_no_later_command(walk):
    collected = yaml.safe_load((walk.series / "r1/7-collected.yaml").read_text())["packets"][TASKS[0]]

    assert [edit.external.name for edit in walk.external_edits] == ["instruction.md", "policy.md", "gardening.md", "brief.md", f"agent-ie-judge-r1-{TASKS[0]}-k1.jsonl"]
    assert all(edit.edited != edit.taken_in and edit.edited.startswith(edit.taken_in) for edit in walk.external_edits)
    assert collected["transcript_hash"] == hashlib.sha256(walk.external_edits[-1].taken_in).hexdigest()
    assert walk.session.runs[-1].command == ("series", "keep")


REPORT_NAME = re.compile(r"^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$", re.IGNORECASE)


def told_paths(series: Path) -> set[Path]:
    """Return every path a generated definition of the series tells its agent to write."""
    return {Path(match) for definition in (series / ".claude/agents").iterdir() for match in VERDICT_PATH_LINE.findall(definition.read_text())}


def test_no_path_written_or_told_to_an_agent_is_named_as_a_report(walk):
    written = {run.series / path for run in walk.session.runs for path in run.created} | {walk.writer / "instruction.md"}
    told = told_paths(walk.series) | told_paths(walk.stopped_series)

    assert told and written
    assert [path for path in written | told if REPORT_NAME.match(path.name)] == []


STAGE_ONE_READS_THE_TABLE_OMITS = (f"{CALIBRATION_ATTEMPT}/sample.md",)
BLIND_READS_THE_TABLE_OMITS = ("{revision}/2-instruction.md",)
COLLECT_READS_THE_TABLE_OMITS = ("5-reader.yaml#model",)
REVISION_NEW_READS_THE_TABLE_OMITS = ("7-gate.yaml#done_by",)
REVISION_RECORD = re.compile(r"r([0-9]+)/.*")
BORROWED_REPLIES = [f"r1/5-replies/{control}/**" for control in FIRST_CONDITIONS if control != "instruction"]


def revision_number(record: str) -> int:
    """Return the number of the revision a record sits in."""
    return int(REVISION_RECORD.fullmatch(record).group(1))


def earlier_outcomes(number: int) -> list[str]:
    """Return the outcome records of every revision before `number`."""
    return [f"r{earlier}/9-outcome.yaml" for earlier in range(1, number)]


def sampled_replies(origins: Mapping) -> list[str]:
    """Return the r1 reply files a calibration attempt's origins name."""
    return [f"r1/5-replies/{origin['condition']}/{origin['task']}/repeat-{origin['repeat']}.yaml" for origin in origins["ids"].values()]


def ask_reads(record: str, present: set[str]) -> list[str]:
    """Return the Reads cell of `revision ask` for a command reader, expanded for the reply record."""
    number = revision_number(record)
    revision = f"r{number}"
    frozen = "8-frozen.yaml" in present
    return [
        "series.yaml", "1-source/*", "2-demands.yaml", "3-tasks.yaml", "4-conditions.yaml", "4-placebo-source.md", "5-reader.yaml", "7-gate.yaml#repeats",
        f"{revision}/2-instruction.md", f"{revision}/3-coverage.yaml", "r1/3-coverage.yaml", f"{revision}/4-conditions/*.md",
        *(["8-frozen.yaml"] if frozen else [path for path in present if path.startswith("r1/5-replies/") and path < record]),
        *(["7-gate.yaml#budget", "r1/4-conditions/*.md", *earlier_outcomes(number)] if number > 1 else []),
    ]


def calibration_reads(record: str, series: Path) -> list[str]:
    """Return the Reads cell of `judge calibrate` for the stage that writes the record."""
    stage_one = [
        "series.yaml", "1-source/*", "2-demands.yaml", f"{CALIBRATION_ATTEMPT}/plan.yaml", f"{CALIBRATION_ATTEMPT}/brief.md",
        *sampled_replies(yaml.safe_load((series / f"{CALIBRATION_ATTEMPT}/origins.yaml").read_text())),
    ]
    if record.endswith("origins.yaml"):
        return [*stage_one, *STAGE_ONE_READS_THE_TABLE_OMITS]
    return [*stage_one, f"{CALIBRATION_ATTEMPT}/sample.md", f"{CALIBRATION_ATTEMPT}/origins.yaml", f"{CALIBRATION_ATTEMPT}/candidate-*.yaml", f"{CALIBRATION_ATTEMPT}/reference-*.yaml", ".claude/agents/ie-calib-1-*.md", "3-tasks.yaml"]


def score_reads(revision: str) -> list[str]:
    """Return the Reads cell of `revision score` expanded for the revision."""
    later = [] if revision == "r1" else BORROWED_REPLIES
    return [
        "2-demands.yaml", "3-tasks.yaml", "r1/3-coverage.yaml", "7-gate.yaml#level", "7-gate.yaml#done_by",
        f"{revision}/5-replies/**", f"{revision}/6-origins.yaml", f"{revision}/7-verdicts/**", f"{revision}/7-collected.yaml", f"{revision}/7-detectors.yaml", *later,
    ]


def gate_reads(number: int) -> list[str]:
    """Return the Reads cell of `revision gate` expanded for the revision, `7-gate.yaml` read whole."""
    revision, parent = f"r{number}", f"r{number - 1}"
    later = [f"{revision}/1-hypothesis.yaml", *(f"{parent}/{part}" for part in ("5-replies/**", "6-origins.yaml", "7-verdicts/**", "7-collected.yaml", "7-detectors.yaml"))]
    score = [read for read in score_reads(revision) if not read.startswith("7-gate.yaml")]
    return [*score, "7-gate.yaml", "8-frozen.yaml", f"{revision}/2-instruction.md", *earlier_outcomes(number), *(later if number > 1 else [])]


STOP_READS = ("7-gate.yaml#keep_rule", "8-frozen.yaml", "r*/9-outcome.yaml")
GATE_STOP_READS = (*STOP_READS, "7-gate.yaml#budget")


def revision_new_reads(number: int) -> list[str]:
    """Return the Reads cell of `revision new` writing revision `number` from its parent."""
    parent = f"r{number - 1}"
    return [
        "2-demands.yaml", "3-tasks.yaml", "4-conditions.yaml", "r1/3-coverage.yaml", "r1/4-conditions/placebo.md", "8-frozen.yaml", f"r{number}/1-hypothesis.yaml",
        *(f"{parent}/{part}" for part in ("2-instruction.md", "2-revision.yaml", "6-origins.yaml", "7-verdicts/**", "7-collected.yaml", "7-detectors.yaml", "9-outcome.yaml")),
        *REVISION_NEW_READS_THE_TABLE_OMITS,
    ]


def reads_cell(run: CommandRun, record: str, present: set[str]) -> list[str]:
    """Return the Commands-table Reads cell of the run's command, expanded for the record it wrote, as series paths, globs, and `<path>#<key>` reads."""
    revision = record.partition("/")[0]
    if record in ("series.yaml", "r1/2-revision.yaml"):
        return []
    if record.startswith(CALIBRATION_ATTEMPT) or record in ("6-judge/calibration.yaml", "6-judge/anchors.yaml"):
        return calibration_reads(record, run.series)
    if "/5-replies/" in record:
        return ask_reads(record, present)
    if record == "8-frozen.yaml":
        return ["series.yaml", "1-source/*", "2-demands.yaml", "3-tasks.yaml", "4-conditions.yaml", "4-placebo-source.md", "5-reader.yaml", "6-judge/calibration.yaml", "6-judge/anchors.yaml", "6-judge/calibration/**", "7-gate.yaml", "r1/**"]
    if record == "9-stop.yaml":
        return list(GATE_STOP_READS if run.command[:2] == ("revision", "gate") else STOP_READS)
    if record.endswith("/2-revision.yaml"):
        return revision_new_reads(revision_number(record))
    if record.endswith("/6-origins.yaml"):
        later = [] if revision == "r1" else BORROWED_REPLIES
        return ["3-tasks.yaml", "4-conditions.yaml", "7-gate.yaml#repeats", f"{revision}/5-replies/**", "6-judge/calibration.yaml", "6-judge/anchors.yaml", *later, *(read.format(revision=revision) for read in BLIND_READS_THE_TABLE_OMITS)]
    if record.endswith("/7-collected.yaml"):
        return [
            "series.yaml", "1-source/*", "2-demands.yaml", "6-judge/calibration.yaml", f"{CALIBRATION_ATTEMPT}/brief.md", "6-judge/anchors.yaml",
            f"{revision}/6-packets/*.md", f"{revision}/6-origins.yaml", f"{revision}/7-verdicts/**", f".claude/agents/ie-judge-{revision}-*.md", *COLLECT_READS_THE_TABLE_OMITS,
        ]
    if record.endswith("/7-detectors.yaml"):
        return ["2-demands.yaml", "3-tasks.yaml", f"{revision}/5-replies/**", f"{revision}/6-origins.yaml", *([] if revision == "r1" else BORROWED_REPLIES)]
    if record.endswith("/8-scores.yaml"):
        return score_reads(revision)
    if record.endswith("/9-outcome.yaml"):
        return gate_reads(revision_number(record))
    raise AssertionError(f"no Reads cell for {record}")


def expand_reads(cell: Sequence[str], present: set[str]) -> set[str]:
    """Return the reads the cell names among the present series files, a `<glob>#<key>` read once per matching file."""
    expanded = set()
    for read in cell:
        pattern, _, key = read.partition("#")
        expanded |= {f"{path}#{key}" if key else path for path in present if fnmatch.fnmatchcase(path, pattern)}
    return expanded


def read_keys(reads: set[str]) -> dict[str, set[str]]:
    """Return by file the top-level keys the `<path>#<key>` reads name."""
    keys: dict[str, set[str]] = {}
    for read in reads:
        path, _, key = read.partition("#")
        if key:
            keys.setdefault(path, set()).add(key)
    return keys


def written_records(run: CommandRun) -> list[tuple[str, dict[str, str]]]:
    """Return each YAML record the run wrote with its `inputs`."""
    documents = {path: yaml.safe_load(run.after[path]) for path in sorted(run.created) if path.endswith(".yaml")}
    return [(path, document["inputs"]) for path, document in documents.items() if isinstance(document, dict) and "inputs" in document]


def present_at_write(run: CommandRun, record: str) -> set[str]:
    """Return the series files present when the run wrote the record: a reply sees the replies its ask wrote before it in path order."""
    written_before = {path for path in run.created if path < record} if "/5-replies/" in record else run.created - {record}
    return set(run.before) | written_before


def test_each_record_names_as_inputs_exactly_the_files_its_reads_cell_names(walk):
    for run in walk.session.runs:
        for record, inputs in written_records(run):
            present = present_at_write(run, record)
            expected = expand_reads(reads_cell(run, record, present), present)
            assert {read.partition("#")[0] for read in inputs} == {read.partition("#")[0] for read in expected}, (run.command, record)
            assert {path: keys for path, keys in read_keys(set(inputs)).items() if path in read_keys(expected)} == read_keys(expected), (run.command, record)
