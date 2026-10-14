"""Series records: files written once, and CLI records whose inputs must still hash as written."""

import functools
import hashlib
import os
import tempfile
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

KEY_SEPARATOR = "#"
INPUTS_KEY = "inputs"


class Refusal(Exception):
    """A command's refusal, carrying the one-line message the user reads."""


@dataclass(frozen=True)
class SeriesFolder:
    """The series folder on disk at `root`."""

    root: Path

    def read_bytes(self, path: str) -> bytes:
        """Return the bytes at `path`, raising FileNotFoundError when it is absent."""
        return (self.root / path).read_bytes()

    def write_once(self, path: str, content: bytes) -> None:
        """Write `content` whole to `path`, raising FileExistsError when it exists."""
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = _stage_beside(target, content)
        try:
            os.link(staged, target)
        finally:
            staged.unlink()


def write_file(files: SeriesFolder, path: str, content: bytes) -> None:
    """Write the series file at `path` whole and once, refusing when it exists."""
    try:
        files.write_once(path, content)
    except FileExistsError:
        raise Refusal(f"already written: {path}") from None


def write_record(files: SeriesFolder, path: str, record: Mapping[str, Any], reads: Iterable[str]) -> None:
    """Write a YAML record whose `inputs` map each read, a series path or `<path>#<key>`, to its sha256."""
    write_file(files, path, _dump_canonical_yaml({**record, INPUTS_KEY: _hash_inputs(files, reads)}))


def load_record(files: SeriesFolder, path: str) -> dict[str, Any]:
    """Load the CLI record at `path`, refusing when an input no longer hashes as written."""
    record = _parse_record(_read_record(files, path), path)
    written_hashes = record[INPUTS_KEY]
    current_hashes = _hash_inputs(files, written_hashes)
    for entry, written_hash in written_hashes.items():
        if current_hashes[entry] != written_hash:
            raise Refusal(f"stale: {path} (input {entry} changed)")
    return record


def _read_record(files: SeriesFolder, path: str) -> bytes:
    """Read the CLI record at `path`, refusing when it is absent."""
    try:
        return files.read_bytes(path)
    except FileNotFoundError:
        raise Refusal(f"missing record: {path}") from None


def _parse_record(content: bytes, path: str) -> dict[str, Any]:
    """Parse a CLI record, refusing it as malformed unless it is a YAML mapping holding an `inputs` mapping."""
    try:
        record = yaml.safe_load(content)
    except yaml.YAMLError:
        raise Refusal(f"malformed record: {path} (not YAML)") from None
    if not isinstance(record, dict) or not isinstance(record.get(INPUTS_KEY), dict):
        raise Refusal(f"malformed record: {path} (no inputs map)")
    return record


def _hash_inputs(files: SeriesFolder, reads: Iterable[str]) -> dict[str, str]:
    """Map each read to the sha256 of what it names, reading and parsing each named file once."""
    read_file = functools.cache(lambda file_path: _read_input(files, file_path))
    parse_file = functools.cache(lambda file_path: yaml.safe_load(read_file(file_path)))
    return {entry: _hash_input(read_file, parse_file, entry) for entry in reads}


def _hash_input(read_file: Callable[[str], bytes], parse_file: Callable[[str], Any], entry: str) -> str:
    """Hash a whole series file, or for `<path>#<key>` that key's value dumped as canonical YAML."""
    file_path, separator, key = entry.partition(KEY_SEPARATOR)
    if not separator:
        return _sha256(read_file(file_path))
    return _sha256(_dump_canonical_yaml(_read_top_level_value(parse_file(file_path), entry, key)))


def _read_top_level_value(document: Any, entry: str, key: str) -> Any:
    """Return the value of a top-level key of a parsed YAML document, refusing `entry` as missing when the key is absent."""
    if not isinstance(document, dict) or key not in document:
        raise Refusal(f"missing input: {entry}")
    return document[key]


def _read_input(files: SeriesFolder, path: str) -> bytes:
    """Read the series input at `path`, refusing when it is absent."""
    try:
        return files.read_bytes(path)
    except FileNotFoundError:
        raise Refusal(f"missing input: {path}") from None


def _stage_beside(target: Path, content: bytes) -> Path:
    """Write the content to a fresh file in the target's folder and return its path."""
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as staged:
        staged.write(content)
    return Path(staged.name)


def _dump_canonical_yaml(value: Any) -> bytes:
    """Dump a value as YAML with sorted keys in block style."""
    return yaml.safe_dump(value, sort_keys=True, default_flow_style=False, allow_unicode=True).encode()


def _sha256(content: bytes) -> str:
    """Return the lowercase sha256 hex digest of the bytes."""
    return hashlib.sha256(content).hexdigest()
