import argparse
import json
import os
import random
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import TextIO, get_args

import numpy

from instruction_eval.coverage import coverage_check
from instruction_eval.demands import demands_check
from instruction_eval.gate import GATE_COMMAND, revision_gate
from instruction_eval.judge import (
    BLIND_COMMAND,
    CALIBRATE_COMMAND,
    JUDGE_COLLECT_COMMAND,
    JUDGE_PREPARE_COMMAND,
    calibrate_stage_one,
    calibrate_stage_two,
    judge_collect,
    judge_prepare,
    latest_attempt_number,
    revision_blind,
)
from instruction_eval.reader import (
    ASK_COMMAND,
    ASK_TIMEOUT_SECONDS,
    COLLECT_COMMAND,
    CONFIG_DIR_VARIABLE,
    FINGERPRINT_COMMAND,
    LoginFiles,
    PREPARE_COMMAND,
    AgentReader,
    ReaderRun,
    RunReader,
    Transcript,
    locate_transcripts,
    reader_fingerprint,
    reader_prepare,
    revision_ask,
    revision_collect,
)
from instruction_eval.records import (
    KEEP_COMMAND,
    STATUS_COMMAND,
    DONE_BY_KEY,
    LEVEL_KEY,
    REPEATS_KEY,
    FINGERPRINT_HASH_KEY,
    ATTEMPT_FOLDER_PREFIX,
    ATTEMPT_ORIGINS_FILE,
    CONDITIONS_RECORD,
    COVERAGE_FILE,
    DEFAULT_BINDING,
    DEMANDS_RECORD,
    FIRST_ATTEMPT,
    FIRST_REVISION,
    FIRST_REVISION_NUMBER,
    GATE_RECORD,
    HYPOTHESIS_FILE,
    PLAN_FILE,
    READER_RECORD,
    REVISION_PREFIX,
    TASKS_RECORD,
    WORKING_BRIEF,
    Binding,
    ReaderKind,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    attempt_folder,
    dump_canonical_yaml,
    guard_series,
    replace_whole,
)
from instruction_eval.revision import NEW_COMMAND, revision_new
from instruction_eval.scores import BOOTSTRAP_SEED, BootstrapRng, revision_detect, revision_score
from instruction_eval.series import (
    FREEZE_COMMAND,
    STOP_COMMAND,
    series_freeze,
    series_keep,
    series_new,
    series_status,
    series_stop,
)
from instruction_eval.tasks import tasks_check

_READER_KINDS = get_args(ReaderKind)
_REVISION_ID_PATTERN = re.compile(r"r[0-9]+")

_SECOND_REVISION = f"{REVISION_PREFIX}{FIRST_REVISION_NUMBER + 1}"
_SERIES_NEW_COMMAND = "series new"
_DEMANDS_CHECK_COMMAND = "demands check"
_COVERAGE_CHECK_COMMAND = "coverage check"
_TASKS_CHECK_COMMAND = "tasks check"
_DETECT_COMMAND = "revision detect"
_SCORE_COMMAND = "revision score"
_ORDER_OF_WORK = f"""\
Order of work:
1. in any shell: `{_SERIES_NEW_COMMAND}`; then start the neutral session there: `cd <series folder> && claudes run readers`; every later step runs in that session
2. user writes `{DEMANDS_RECORD}`; `{_DEMANDS_CHECK_COMMAND}`
3. user writes `{FIRST_REVISION}/{COVERAGE_FILE}`; `{_COVERAGE_CHECK_COMMAND} {FIRST_REVISION}`
4. user writes `{CONDITIONS_RECORD}`, `{READER_RECORD}`, and `{GATE_RECORD}` `{REPEATS_KEY}`, `{LEVEL_KEY}`, `{DONE_BY_KEY}`
5. user writes `{TASKS_RECORD}`; `{_TASKS_CHECK_COMMAND}`
6. `{FINGERPRINT_COMMAND}` (command kind); `{PREPARE_COMMAND} {FIRST_REVISION}`; `{ASK_COMMAND} {FIRST_REVISION}`; agents launched; `{COLLECT_COMMAND} {FIRST_REVISION}`
7. user writes `{WORKING_BRIEF}` and `{attempt_folder(FIRST_ATTEMPT)}/{PLAN_FILE}`; `{CALIBRATE_COMMAND}` (snapshots the brief); ratings; `{CALIBRATE_COMMAND}`; on rejection, the user edits the brief, writes `{ATTEMPT_FOLDER_PREFIX}<n+1>/{PLAN_FILE}`, and repeats
8. `{BLIND_COMMAND} {FIRST_REVISION}`; `{JUDGE_PREPARE_COMMAND} {FIRST_REVISION}`; judges; `{JUDGE_COLLECT_COMMAND} {FIRST_REVISION}`; `{_DETECT_COMMAND} {FIRST_REVISION}`
9. `{STATUS_COMMAND}` prints the noise; user completes `{GATE_RECORD}`; `{FREEZE_COMMAND}`
10. `{_SCORE_COMMAND} {FIRST_REVISION}`; `{GATE_COMMAND} {FIRST_REVISION}`. `{STATUS_COMMAND}` is available at any step
11. on `fail`: user writes `{_SECOND_REVISION}/{HYPOTHESIS_FILE}`; writer edits the instruction; `{NEW_COMMAND}`; user writes `{_SECOND_REVISION}/{COVERAGE_FILE}`; `{_COVERAGE_CHECK_COMMAND} {_SECOND_REVISION}`; `{PREPARE_COMMAND} {_SECOND_REVISION}`; `{ASK_COMMAND} {_SECOND_REVISION} --conditions instruction …`; `{COLLECT_COMMAND} {_SECOND_REVISION}`; `{BLIND_COMMAND} {_SECOND_REVISION}`; `{JUDGE_PREPARE_COMMAND} {_SECOND_REVISION}`; `{JUDGE_COLLECT_COMMAND} {_SECOND_REVISION}`; `{_DETECT_COMMAND} {_SECOND_REVISION}`; `{_SCORE_COMMAND} {_SECOND_REVISION}`; `{GATE_COMMAND} {_SECOND_REVISION}`
12. at a stop: `{KEEP_COMMAND}` writes the kept snapshot to the live instruction path
"""


def _revision_id(text: str) -> str:
    """Return the text when it is a revision id `r<n>`, else refuse it."""
    if not _REVISION_ID_PATTERN.fullmatch(text):
        raise argparse.ArgumentTypeError(f"not a revision id r<n>: {text}")
    return text


def _add_series_new_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the folder name, instruction, repeatable source, reader kind, and binding plugin and skill of `series new`."""
    parser.add_argument("name")
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--source", action="append", default=[], dest="sources")
    parser.add_argument("--reader-kind", required=True, choices=_READER_KINDS)
    parser.add_argument("--binding-plugin", default=DEFAULT_BINDING.plugin)
    parser.add_argument("--binding-skill", default=DEFAULT_BINDING.skill)


def _add_series_stop_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the required reason of `series stop`."""
    parser.add_argument("--reason", required=True)


def _add_revision_argument(parser: argparse.ArgumentParser) -> None:
    """Add the positional revision id."""
    parser.add_argument("revision", type=_revision_id)


def _add_revision_ask_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the revision id and the repeatable conditions flag of `revision ask`."""
    _add_revision_argument(parser)
    parser.add_argument("--conditions", action="append", default=[])


def _add_no_arguments(parser: argparse.ArgumentParser) -> None:
    """Add nothing to a command that takes no argument."""


_READER_TIMEOUT_SECONDS = ASK_TIMEOUT_SECONDS
_REFUSAL_EXIT_CODE = 1
_PLUGIN_ROOT = Path(__file__).resolve().parents[2]
_PLUGIN_MANIFEST = _PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
_BRIEF_TEMPLATE = Path(__file__).resolve().parent / "templates" / "judge-brief.md"
_FINGERPRINT_KEY = "fingerprint"


@dataclass(frozen=True)
class _Effects:
    """Every effect a command takes: the clock, the folders, the environment, the random sources, the readers of files and processes, and the replacer of the live instruction."""

    now: Callable[[], datetime]
    home: Path
    working_dir: Path
    environ: Mapping[str, str]
    random: random.Random
    bootstrap_rng: BootstrapRng
    read_external: Callable[[Path], bytes]
    replace_file: Callable[[Path, bytes], None]
    read_transcript: Callable[[Path], bytes]
    list_files: Callable[[Path, str], Iterable[Path]]
    login_files: LoginFiles
    run_reader: RunReader
    run_fingerprint: Callable[[Sequence[str]], str]
    tool_version: str
    brief_template: Path


def _run_process(command: Sequence[str], stdin: str | None, timeout_seconds: int) -> subprocess.CompletedProcess[str] | None:
    """Run the command to its end, returning None when it exceeds the time limit and refusing a command that cannot start."""
    try:
        return subprocess.run(list(command), input=stdin, capture_output=True, text=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        return None
    except OSError as error:
        raise Refusal(f"cannot run {command[0]}: {error.strerror}") from None


def _run_reader(now: Callable[[], datetime], command: Sequence[str], stdin: str, timeout_seconds: int) -> ReaderRun:
    """Run a command reader on the messages and return when it started, how long it ran, its exit code, and its stdout."""
    started = now()
    finished = _run_process(command, stdin, timeout_seconds)
    seconds = (now() - started).total_seconds()
    return ReaderRun(started, seconds, None, "") if finished is None else ReaderRun(started, seconds, finished.returncode, finished.stdout)


def _run_fingerprint(command: Sequence[str]) -> str:
    """Run a command reader's fingerprint and return its stdout, refusing a failed or overlong run."""
    finished = _run_process(command, None, _READER_TIMEOUT_SECONDS)
    if finished is None:
        raise Refusal(f"fingerprint exceeded {_READER_TIMEOUT_SECONDS} seconds")
    if finished.returncode != 0:
        raise Refusal(f"fingerprint exited {finished.returncode}")
    return finished.stdout


def _real_effects() -> _Effects:
    """Build the effects of the running process: the system clock, home, working directory, environment, and OS randomness."""
    now = lambda: datetime.now().astimezone()
    return _Effects(
        now=now,
        home=Path.home(),
        working_dir=Path.cwd(),
        environ=dict(os.environ),
        random=random.SystemRandom(),
        bootstrap_rng=lambda: numpy.random.default_rng(BOOTSTRAP_SEED),
        read_external=Path.read_bytes,
        replace_file=replace_whole,
        read_transcript=Path.read_bytes,
        list_files=Path.glob,
        login_files=LoginFiles(
            resolve=Path.resolve,
            exists=Path.exists,
            is_link=Path.is_symlink,
            is_folder=Path.is_dir,
            is_file=Path.is_file,
            entries=Path.iterdir,
            read_bytes=Path.read_bytes,
        ),
        run_reader=partial(_run_reader, now),
        run_fingerprint=_run_fingerprint,
        tool_version=json.loads(_PLUGIN_MANIFEST.read_text())["version"],
        brief_template=_BRIEF_TEMPLATE,
    )


_Handler = Callable[[argparse.Namespace, _Effects], str]


def _series_folder(effects: _Effects) -> SeriesFolder:
    """Return the series folder the command runs in."""
    return SeriesFolder(effects.working_dir)


def _command_name(arguments: argparse.Namespace) -> str:
    """Return the command's group and verb as the guard names it."""
    return f"{arguments.group} {arguments.verb}"


def _transcripts(effects: _Effects) -> list[Transcript]:
    """Return the subagent transcripts of the series folder's sessions, none when the session names no config dir."""
    config_dir = effects.environ.get(CONFIG_DIR_VARIABLE)
    if not config_dir:
        return []
    try:
        return locate_transcripts(Path(config_dir), effects.working_dir, effects.working_dir, effects.list_files, effects.read_transcript)
    except ValueError as unreadable:
        raise Refusal(str(unreadable)) from None


def _latest_attempt_holds_origins(files: SeriesFolder) -> bool:
    """Tell whether the latest attempt has written its origins."""
    return files.holds(f"{attempt_folder(latest_attempt_number(files))}/{ATTEMPT_ORIGINS_FILE}")


def _fresh_fingerprint_hash(files: SeriesFolder, effects: _Effects) -> str | None:
    """Return a command reader's fresh fingerprint hash, None for an agent reader."""
    if isinstance(SeriesRecords(files).reader(), AgentReader):
        return None
    return reader_fingerprint(files, effects.run_fingerprint).fingerprint_hash


def _new_series(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Make the series folder and return its path."""
    binding = Binding(plugin=arguments.binding_plugin, skill=arguments.binding_skill)
    files = series_new(arguments.name, arguments.instruction, arguments.sources, arguments.reader_kind, binding, effects.working_dir, effects.home, effects.now())
    return f"{files.root}\n"


def _status(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Return the series' standing."""
    return series_status(_series_folder(effects))


def _freeze(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Freeze the series with a command reader's fresh fingerprint hash."""
    files = _series_folder(effects)
    series_freeze(files, _fresh_fingerprint_hash(files, effects), effects.read_external, effects.bootstrap_rng, effects.tool_version, effects.now())
    return ""


def _stop(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Stop the series for the reason given."""
    series_stop(_series_folder(effects), arguments.reason)
    return ""


def _keep(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Write the kept revision over the live instruction."""
    series_keep(_series_folder(effects), effects.replace_file)
    return ""


def _check_demands(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Check the demands record."""
    demands_check(_series_folder(effects))
    return ""


def _check_coverage(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Check the coverage record of the revision."""
    coverage_check(_series_folder(effects), arguments.revision)
    return ""


def _check_tasks(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Check the task record."""
    tasks_check(_series_folder(effects), effects.read_external)
    return ""


def _fingerprint(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Return the command reader's parsed fingerprint and its hash."""
    fingerprint = reader_fingerprint(_series_folder(effects), effects.run_fingerprint)
    return dump_canonical_yaml({_FINGERPRINT_KEY: fingerprint.output, FINGERPRINT_HASH_KEY: fingerprint.fingerprint_hash}).decode()


def _prepare_reader(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Write the condition files and reader definitions of the revision."""
    reader_prepare(_series_folder(effects), arguments.revision, effects.read_external, effects.environ, effects.home, effects.working_dir, effects.login_files)
    return ""


def _ask(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Ask the revision's missing replies and return an agent reader's launch list."""
    files = _series_folder(effects)
    return revision_ask(files, arguments.revision, arguments.conditions, effects.run_reader, effects.run_fingerprint)


def _collect(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Collect the revision's replies and return the surplus transcripts."""
    return revision_collect(_series_folder(effects), arguments.revision, _transcripts(effects), effects.read_transcript)


def _blind(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Blind the revision's replies into packets."""
    revision_blind(_series_folder(effects), arguments.revision, effects.random)
    return ""


def _detect(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Run the detectors over the revision's replies."""
    revision_detect(_series_folder(effects), arguments.revision)
    return ""


def _score(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Score the revision."""
    revision_score(_series_folder(effects), arguments.revision, effects.bootstrap_rng)
    return ""


def _gate(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Write the revision's outcome."""
    revision_gate(_series_folder(effects), arguments.revision, effects.bootstrap_rng)
    return ""


def _new_revision(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Record the next revision from the live instruction."""
    revision_new(_series_folder(effects), effects.read_external)
    return ""


def _calibrate(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Run stage two of calibration when the latest attempt holds origins, else stage one."""
    files = _series_folder(effects)
    if _latest_attempt_holds_origins(files):
        return calibrate_stage_two(files, _transcripts(effects), effects.read_transcript)
    return calibrate_stage_one(files, effects.brief_template, effects.environ, effects.home, effects.working_dir, effects.random, effects.login_files)


def _prepare_judge(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Write the judgings of the revision and return their launch list."""
    return judge_prepare(_series_folder(effects), arguments.revision, effects.environ, effects.home, effects.working_dir, _transcripts(effects), effects.read_transcript, effects.login_files)


def _collect_judge(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Collect the revision's verdicts."""
    return judge_collect(_series_folder(effects), arguments.revision, _transcripts(effects), effects.read_transcript)


@dataclass(frozen=True)
class _Command:
    """One command: what adds its arguments, what runs it, and whether the CLI guards the series first because the command does not."""

    add_arguments: Callable[[argparse.ArgumentParser], None]
    handle: _Handler
    guarded: bool = False


_COMMANDS: dict[str, _Command] = {
    _SERIES_NEW_COMMAND: _Command(_add_series_new_arguments, _new_series),
    STATUS_COMMAND: _Command(_add_no_arguments, _status),
    FREEZE_COMMAND: _Command(_add_no_arguments, _freeze),
    STOP_COMMAND: _Command(_add_series_stop_arguments, _stop),
    KEEP_COMMAND: _Command(_add_no_arguments, _keep),
    _DEMANDS_CHECK_COMMAND: _Command(_add_no_arguments, _check_demands, guarded=True),
    _COVERAGE_CHECK_COMMAND: _Command(_add_revision_argument, _check_coverage, guarded=True),
    _TASKS_CHECK_COMMAND: _Command(_add_no_arguments, _check_tasks, guarded=True),
    FINGERPRINT_COMMAND: _Command(_add_no_arguments, _fingerprint),
    PREPARE_COMMAND: _Command(_add_revision_argument, _prepare_reader),
    ASK_COMMAND: _Command(_add_revision_ask_arguments, _ask),
    COLLECT_COMMAND: _Command(_add_revision_argument, _collect),
    BLIND_COMMAND: _Command(_add_revision_argument, _blind),
    _DETECT_COMMAND: _Command(_add_revision_argument, _detect, guarded=True),
    _SCORE_COMMAND: _Command(_add_revision_argument, _score, guarded=True),
    GATE_COMMAND: _Command(_add_revision_argument, _gate),
    NEW_COMMAND: _Command(_add_no_arguments, _new_revision),
    CALIBRATE_COMMAND: _Command(_add_no_arguments, _calibrate, guarded=True),
    JUDGE_PREPARE_COMMAND: _Command(_add_revision_argument, _prepare_judge),
    JUDGE_COLLECT_COMMAND: _Command(_add_revision_argument, _collect_judge),
}


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser of every command, its help printing the order of work."""
    parser = argparse.ArgumentParser(
        prog="instruction-eval",
        epilog=_ORDER_OF_WORK,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    groups = parser.add_subparsers(dest="group", required=True)
    verb_parsers = {}
    for name, command in _COMMANDS.items():
        group, verb = name.split()
        if group not in verb_parsers:
            verb_parsers[group] = groups.add_parser(group).add_subparsers(dest="verb", required=True)
        command.add_arguments(verb_parsers[group].add_parser(verb))
    return parser


def _run_command(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Run the parsed command with its effects and return the text it prints."""
    command = _COMMANDS[_command_name(arguments)]
    if command.guarded:
        guard_series(_series_folder(effects), _command_name(arguments))
    return command.handle(arguments, effects)


def _execute(argv: Sequence[str], effects: _Effects, stdout: TextIO, stderr: TextIO) -> int:
    """Run the command `argv` names, printing its text to `stdout` or its refusal to `stderr`, and return the exit code."""
    arguments = _build_parser().parse_args(list(argv))
    try:
        stdout.write(_run_command(arguments, effects))
    except Refusal as refusal:
        stderr.write(f"{refusal}\n")
        return _REFUSAL_EXIT_CODE
    return 0


def main() -> None:
    """Run the command line of the process with the effects of the running process."""
    raise SystemExit(_execute(sys.argv[1:], _real_effects(), sys.stdout, sys.stderr))
