import argparse
import json
import os
import random
import re
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import TextIO, get_args

import numpy

from instruction_eval.coverage import coverage_check
from instruction_eval.demands import demands_check
from instruction_eval.gate import revision_gate
from instruction_eval.judge import (
    calibrate_stage_one,
    calibrate_stage_two,
    judge_collect,
    judge_prepare,
    latest_attempt_number,
    revision_blind,
)
from instruction_eval.reader import (
    ASK_TIMEOUT_SECONDS,
    CONFIG_DIR_VARIABLE,
    FINGERPRINT_HASH_KEY,
    REPEATS_KEY,
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
    ATTEMPT_FOLDER_PREFIX,
    ATTEMPT_ORIGINS_FILE,
    CONDITIONS_RECORD,
    COVERAGE_FILE,
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
    ReaderKind,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    attempt_folder,
    dump_canonical_yaml,
    guard_series,
    replace_whole,
)
from instruction_eval.revision import revision_new
from instruction_eval.scores import BOOTSTRAP_SEED, DONE_BY_KEY, LEVEL_KEY, BootstrapRng, revision_detect, revision_score
from instruction_eval.series import (
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
_ORDER_OF_WORK = f"""\
Order of work:
1. in any shell: `series new`; then start the neutral session there: `cd <series folder> && claudes run readers`; every later step runs in that session
2. user writes `{DEMANDS_RECORD}`; `demands check`
3. user writes `{FIRST_REVISION}/{COVERAGE_FILE}`; `coverage check {FIRST_REVISION}`
4. user writes `{CONDITIONS_RECORD}`, `{READER_RECORD}`, and `{GATE_RECORD}` `{REPEATS_KEY}`, `{LEVEL_KEY}`, `{DONE_BY_KEY}`
5. user writes `{TASKS_RECORD}`; `tasks check`
6. `reader fingerprint` (command kind); `reader prepare {FIRST_REVISION}`; `revision ask {FIRST_REVISION}`; agents launched; `revision collect {FIRST_REVISION}`
7. user writes `{WORKING_BRIEF}` and `{attempt_folder(FIRST_ATTEMPT)}/{PLAN_FILE}`; `judge calibrate` (snapshots the brief); ratings; `judge calibrate`; on rejection, the user edits the brief, writes `{ATTEMPT_FOLDER_PREFIX}<n+1>/{PLAN_FILE}`, and repeats
8. `revision blind {FIRST_REVISION}`; `judge prepare {FIRST_REVISION}`; judges; `judge collect {FIRST_REVISION}`; `revision detect {FIRST_REVISION}`
9. `series status` prints the noise; user completes `{GATE_RECORD}`; `series freeze`
10. `revision score {FIRST_REVISION}`; `revision gate {FIRST_REVISION}`. `series status` is available at any step
11. on `fail`: user writes `{_SECOND_REVISION}/{HYPOTHESIS_FILE}`; writer edits the instruction; `revision new`; user writes `{_SECOND_REVISION}/{COVERAGE_FILE}`; `coverage check {_SECOND_REVISION}`; `reader prepare {_SECOND_REVISION}`; `revision ask {_SECOND_REVISION} --conditions instruction …`; `revision collect {_SECOND_REVISION}`; `revision blind {_SECOND_REVISION}`; `judge prepare {_SECOND_REVISION}`; `judge collect {_SECOND_REVISION}`; `revision detect {_SECOND_REVISION}`; `revision score {_SECOND_REVISION}`; `revision gate {_SECOND_REVISION}`
12. at a stop: `series keep` writes the kept snapshot to the live instruction path
"""


def _revision_id(text: str) -> str:
    """Return the text when it is a revision id `r<n>`, else refuse it."""
    if not _REVISION_ID_PATTERN.fullmatch(text):
        raise argparse.ArgumentTypeError(f"not a revision id r<n>: {text}")
    return text


def _add_series_new_arguments(parser: argparse.ArgumentParser) -> None:
    """Add the folder name, instruction, repeatable source, and reader kind of `series new`."""
    parser.add_argument("name")
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--source", action="append", default=[], dest="sources")
    parser.add_argument("--reader-kind", required=True, choices=_READER_KINDS)


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
        return locate_transcripts(Path(config_dir), effects.working_dir, effects.working_dir)
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
    files = series_new(arguments.name, arguments.instruction, arguments.sources, arguments.reader_kind, effects.working_dir, effects.home, effects.now())
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
    reader_prepare(_series_folder(effects), arguments.revision, effects.read_external, effects.environ, effects.home, effects.working_dir)
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
    return calibrate_stage_one(files, effects.brief_template, effects.environ, effects.home, effects.working_dir, effects.random)


def _prepare_judge(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Write the judgings of the revision and return their launch list."""
    return judge_prepare(_series_folder(effects), arguments.revision, effects.environ, effects.home, effects.working_dir, _transcripts(effects), effects.read_transcript)


def _collect_judge(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Collect the revision's verdicts."""
    return judge_collect(_series_folder(effects), arguments.revision, _transcripts(effects), effects.read_transcript)


@dataclass(frozen=True)
class _Command:
    """One command: what adds its arguments, what runs it, and whether the CLI guards the series first because the command does not."""

    add_arguments: Callable[[argparse.ArgumentParser], None]
    handle: _Handler
    guarded: bool = False


_COMMANDS: dict[tuple[str, str], _Command] = {
    ("series", "new"): _Command(_add_series_new_arguments, _new_series),
    ("series", "status"): _Command(_add_no_arguments, _status),
    ("series", "freeze"): _Command(_add_no_arguments, _freeze),
    ("series", "stop"): _Command(_add_series_stop_arguments, _stop),
    ("series", "keep"): _Command(_add_no_arguments, _keep),
    ("demands", "check"): _Command(_add_no_arguments, _check_demands, guarded=True),
    ("coverage", "check"): _Command(_add_revision_argument, _check_coverage, guarded=True),
    ("tasks", "check"): _Command(_add_no_arguments, _check_tasks, guarded=True),
    ("reader", "fingerprint"): _Command(_add_no_arguments, _fingerprint),
    ("reader", "prepare"): _Command(_add_revision_argument, _prepare_reader),
    ("revision", "ask"): _Command(_add_revision_ask_arguments, _ask),
    ("revision", "collect"): _Command(_add_revision_argument, _collect),
    ("revision", "blind"): _Command(_add_revision_argument, _blind),
    ("revision", "detect"): _Command(_add_revision_argument, _detect, guarded=True),
    ("revision", "score"): _Command(_add_revision_argument, _score, guarded=True),
    ("revision", "gate"): _Command(_add_revision_argument, _gate),
    ("revision", "new"): _Command(_add_no_arguments, _new_revision),
    ("judge", "calibrate"): _Command(_add_no_arguments, _calibrate, guarded=True),
    ("judge", "prepare"): _Command(_add_revision_argument, _prepare_judge),
    ("judge", "collect"): _Command(_add_revision_argument, _collect_judge),
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
    for (group, verb), command in _COMMANDS.items():
        if group not in verb_parsers:
            verb_parsers[group] = groups.add_parser(group).add_subparsers(dest="verb", required=True)
        command.add_arguments(verb_parsers[group].add_parser(verb))
    return parser


def _run_command(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Run the parsed command with its effects and return the text it prints."""
    command = _COMMANDS[(arguments.group, arguments.verb)]
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
