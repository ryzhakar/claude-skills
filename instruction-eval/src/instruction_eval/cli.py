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

from instruction_eval.coverage import coverage_check, split_sentences
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
    ATTEMPT_ORIGINS_FILE,
    INSTRUCTION_FILE,
    ReaderKind,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    attempt_folder,
    dump_canonical_yaml,
    guard_series,
)
from instruction_eval.revision import revision_new
from instruction_eval.scores import BOOTSTRAP_SEED, BootstrapRng, revision_detect, revision_score
from instruction_eval.series import (
    series_freeze,
    series_keep,
    series_new,
    series_status,
    series_stop,
)
from instruction_eval.tasks import expected_replies, tasks_check

_READER_KINDS = get_args(ReaderKind)
_REVISION_ID_PATTERN = re.compile(r"r[0-9]+")

_ORDER_OF_WORK = """\
Order of work:
1. in any shell: `series new`; then start the neutral session there: `cd <series folder> && claudes run readers`; every later step runs in that session
2. user writes `2-demands.yaml`; `demands check`
3. user writes `r1/3-coverage.yaml`; `coverage check r1`
4. user writes `4-conditions.yaml`, `5-reader.yaml`, and `7-gate.yaml` `repeats`, `level`, `done_by`
5. user writes `3-tasks.yaml`; `tasks check`
6. `reader fingerprint` (command kind); `reader prepare r1`; `revision ask r1`; agents launched; `revision collect r1`
7. user writes `6-judge/brief.md` and `6-judge/calibration/attempt-1/plan.yaml`; `judge calibrate` (snapshots the brief); ratings; `judge calibrate`; on rejection, the user edits the brief, writes `attempt-<n+1>/plan.yaml`, and repeats
8. `revision blind r1`; `judge prepare r1`; judges; `judge collect r1`; `revision detect r1`
9. `series status` prints the noise; user completes `7-gate.yaml`; `series freeze`
10. `revision score r1`; `revision gate r1`. `series status` is available at any step
11. on `fail`: user writes `r2/1-hypothesis.yaml`; writer edits the instruction; `revision new`; user writes `r2/3-coverage.yaml`; `coverage check r2`; `reader prepare r2`; `revision ask r2 --conditions instruction …`; `revision collect r2`; `revision blind r2`; `judge prepare r2`; `judge collect r2`; `revision detect r2`; `revision score r2`; `revision gate r2`
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


_COMMANDS = {
    "series": {
        "new": _add_series_new_arguments,
        "status": _add_no_arguments,
        "freeze": _add_no_arguments,
        "stop": _add_series_stop_arguments,
        "keep": _add_no_arguments,
    },
    "demands": {"check": _add_no_arguments},
    "coverage": {"check": _add_revision_argument},
    "tasks": {"check": _add_no_arguments},
    "reader": {"fingerprint": _add_no_arguments, "prepare": _add_revision_argument},
    "revision": {
        "ask": _add_revision_ask_arguments,
        "collect": _add_revision_argument,
        "blind": _add_revision_argument,
        "detect": _add_revision_argument,
        "score": _add_revision_argument,
        "gate": _add_revision_argument,
        "new": _add_no_arguments,
    },
    "judge": {
        "calibrate": _add_no_arguments,
        "prepare": _add_revision_argument,
        "collect": _add_revision_argument,
    },
}


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser of every command, its help printing the order of work."""
    parser = argparse.ArgumentParser(
        prog="instruction-eval",
        epilog=_ORDER_OF_WORK,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    groups = parser.add_subparsers(dest="group", required=True)
    for group, verbs in _COMMANDS.items():
        verb_parsers = groups.add_parser(group).add_subparsers(dest="verb", required=True)
        for verb, add_arguments in verbs.items():
            add_arguments(verb_parsers.add_parser(verb))
    return parser


_READER_TIMEOUT_SECONDS = ASK_TIMEOUT_SECONDS
_REFUSAL_EXIT_CODE = 1
_PLUGIN_ROOT = Path(__file__).resolve().parents[2]
_PLUGIN_MANIFEST = _PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
_BRIEF_TEMPLATE = Path(__file__).resolve().parent / "templates" / "judge-brief.md"
_GUARDED_COMMANDS = frozenset(
    {
        ("demands", "check"),
        ("coverage", "check"),
        ("tasks", "check"),
        ("series", "freeze"),
        ("revision", "ask"),
        ("revision", "detect"),
        ("revision", "score"),
        ("judge", "calibrate"),
    }
)
_FINGERPRINT_KEY = "fingerprint"
_FINGERPRINT_HASH_KEY = "fingerprint_hash"


@dataclass(frozen=True)
class _Effects:
    """Every effect a command takes: the clock, the folders, the environment, the random sources, and the readers of files and processes."""

    now: Callable[[], datetime]
    home: Path
    working_dir: Path
    environ: Mapping[str, str]
    random: random.Random
    bootstrap_rng: BootstrapRng
    read_external: Callable[[Path], bytes]
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


def _refuse_unknown_conditions(files: SeriesFolder, revision: str, conditions: Sequence[str]) -> None:
    """Refuse the first named condition outside the revision's condition set."""
    if not conditions:
        return
    instruction_path = f"{revision}/{INSTRUCTION_FILE}"
    if not files.holds(instruction_path):
        raise Refusal(f"missing record: {instruction_path}")
    records = SeriesRecords(files)
    sentence_count = len(split_sentences(files.read_bytes(instruction_path)))
    replies = expected_replies(revision, records.tasks(), records.conditions(), 1, sentence_count)
    known = sorted({reply.condition for reply in replies if reply.revision == revision})
    for condition in conditions:
        if condition not in known:
            raise Refusal(f"unknown condition: {condition} (revision {revision} has {', '.join(known)})")


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
    series_keep(_series_folder(effects))
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
    return dump_canonical_yaml({_FINGERPRINT_KEY: fingerprint.output, _FINGERPRINT_HASH_KEY: fingerprint.fingerprint_hash}).decode()


def _prepare_reader(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Write the condition files and reader definitions of the revision."""
    reader_prepare(_series_folder(effects), arguments.revision, effects.read_external, effects.environ, effects.home, effects.working_dir)
    return ""


def _ask(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Ask the revision's missing replies and return an agent reader's launch list."""
    files = _series_folder(effects)
    _refuse_unknown_conditions(files, arguments.revision, arguments.conditions)
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


_HANDLERS: dict[tuple[str, str], _Handler] = {
    ("series", "new"): _new_series,
    ("series", "status"): _status,
    ("series", "freeze"): _freeze,
    ("series", "stop"): _stop,
    ("series", "keep"): _keep,
    ("demands", "check"): _check_demands,
    ("coverage", "check"): _check_coverage,
    ("tasks", "check"): _check_tasks,
    ("reader", "fingerprint"): _fingerprint,
    ("reader", "prepare"): _prepare_reader,
    ("revision", "ask"): _ask,
    ("revision", "collect"): _collect,
    ("revision", "blind"): _blind,
    ("revision", "detect"): _detect,
    ("revision", "score"): _score,
    ("revision", "gate"): _gate,
    ("revision", "new"): _new_revision,
    ("judge", "calibrate"): _calibrate,
    ("judge", "prepare"): _prepare_judge,
    ("judge", "collect"): _collect_judge,
}


def _run_command(arguments: argparse.Namespace, effects: _Effects) -> str:
    """Run the parsed command with its effects and return the text it prints."""
    if (arguments.group, arguments.verb) in _GUARDED_COMMANDS:
        guard_series(_series_folder(effects), _command_name(arguments))
    return _HANDLERS[(arguments.group, arguments.verb)](arguments, effects)


def _execute(argv: Sequence[str], effects: _Effects, stdout: TextIO, stderr: TextIO) -> int:
    """Run the command `argv` names, printing its text to `stdout` or its refusal to `stderr`, and return the exit code."""
    arguments = build_parser().parse_args(list(argv))
    try:
        stdout.write(_run_command(arguments, effects))
    except Refusal as refusal:
        stderr.write(f"{refusal}\n")
        return _REFUSAL_EXIT_CODE
    return 0


def main() -> None:
    """Run the command line of the process with the effects of the running process."""
    raise SystemExit(_execute(sys.argv[1:], _real_effects(), sys.stdout, sys.stderr))
