"""Typed records of a series, built from parsed YAML documents and refused when malformed."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, get_args

HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")

ReaderKind = Literal["agent", "command"]


class RecordRefused(ValueError):
    """A record document that breaks its schema, its message naming the offending key."""


@dataclass(frozen=True)
class Series:
    """The `series.yaml` record."""

    instruction: Path
    sources: tuple[Path, ...]
    reader_kind: ReaderKind
    created: datetime
    inputs: Mapping[str, str]


def parse_series(document: object) -> Series:
    """Build the `series.yaml` record from its parsed document."""
    keys = read_keys(document, "series.yaml", required={"instruction", "sources", "reader_kind", "created", "inputs"})
    return Series(
        instruction=read_absolute_path(keys["instruction"], "instruction"),
        sources=tuple(read_absolute_path(source, f"sources[{index}]") for index, source in enumerate(read_list(keys["sources"], "sources"))),
        reader_kind=read_choice(keys["reader_kind"], "reader_kind", get_args(ReaderKind)),
        created=read_timestamp(keys["created"], "created"),
        inputs=read_hashes(keys["inputs"], "inputs"),
    )


def read_keys(value: object, where: str, required: set[str], optional: set[str] = frozenset()) -> Mapping[str, object]:
    """Return a mapping holding every required key and no key outside required and optional."""
    if not isinstance(value, Mapping):
        raise RecordRefused(f"{where}: expected a mapping, got {value!r}")
    missing = required - value.keys()
    if missing:
        raise RecordRefused(f"{where}: missing {', '.join(sorted(missing))}")
    unknown = value.keys() - required - optional
    if unknown:
        raise RecordRefused(f"{where}: unknown {', '.join(sorted(map(str, unknown)))}")
    return value


def read_list(value: object, where: str) -> list[object]:
    """Return a YAML sequence."""
    if not isinstance(value, list):
        raise RecordRefused(f"{where}: expected a list, got {value!r}")
    return value


def read_string(value: object, where: str) -> str:
    """Return a non-empty string."""
    if not isinstance(value, str) or not value:
        raise RecordRefused(f"{where}: expected a non-empty string, got {value!r}")
    return value


def read_absolute_path(value: object, where: str) -> Path:
    """Return an absolute path."""
    path = Path(read_string(value, where))
    if not path.is_absolute():
        raise RecordRefused(f"{where}: expected an absolute path, got {value!r}")
    return path


def read_choice(value: object, where: str, choices: tuple[str, ...]) -> str:
    """Return a value drawn from a closed enum."""
    if value not in choices:
        raise RecordRefused(f"{where}: {value!r} is not one of {', '.join(choices)}")
    return value


def read_timestamp(value: object, where: str) -> datetime:
    """Return an ISO 8601 timestamp carrying an offset."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            pass
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise RecordRefused(f"{where}: expected an ISO 8601 timestamp with offset, got {value!r}")
    return value


def read_hashes(value: object, where: str) -> Mapping[str, str]:
    """Return a map from a series path to its lowercase sha256 hex."""
    if not isinstance(value, Mapping):
        raise RecordRefused(f"{where}: expected a mapping, got {value!r}")
    for path, digest in value.items():
        read_string(path, f"{where} key")
        if not isinstance(digest, str) or not HASH_PATTERN.match(digest):
            raise RecordRefused(f"{where}[{path}]: expected a lowercase sha256 hex, got {digest!r}")
    return dict(value)
