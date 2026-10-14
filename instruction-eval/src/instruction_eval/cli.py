import argparse
import re

_READER_KINDS = ("agent", "command")
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
