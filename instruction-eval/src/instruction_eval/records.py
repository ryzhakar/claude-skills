"""Series records: files written once, and CLI records whose inputs must still hash as written."""

import hashlib
import os
import tempfile
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import yaml

KEY_SEPARATOR = "#"


class Refusal(Exception):
    """A command's refusal, carrying the one-line message the user reads."""


def write_file(series: Path, path: str, content: bytes) -> None:
    """Write the series file at `path` whole and once, refusing when it exists."""
    target = series / path
    target.parent.mkdir(parents=True, exist_ok=True)
    staged = _stage_beside(target, content)
    try:
        os.link(staged, target)
    except FileExistsError:
        raise Refusal(f"already written: {path}") from None
    finally:
        staged.unlink()


def write_record(series: Path, path: str, record: Mapping[str, Any], reads: Iterable[str]) -> None:
    """Write a YAML record whose `inputs` map each read, a series path or `<path>#<key>`, to its sha256."""
    write_file(series, path, _dump_yaml({**record, "inputs": _hash_inputs(series, reads)}))


def load_record(series: Path, path: str) -> dict[str, Any]:
    """Load the CLI record at `path`."""
    return yaml.safe_load((series / path).read_bytes())


def _hash_inputs(series: Path, reads: Iterable[str]) -> dict[str, str]:
    """Map each read to the sha256 of what it names."""
    return {entry: _hash_input(series, entry) for entry in reads}


def _hash_input(series: Path, entry: str) -> str:
    """Hash a whole series file, or for `<path>#<key>` that key's value dumped as canonical YAML."""
    file_path, separator, key = entry.partition(KEY_SEPARATOR)
    content = (series / file_path).read_bytes()
    if not separator:
        return _sha256(content)
    return _sha256(_dump_yaml(yaml.safe_load(content)[key]))


def _stage_beside(target: Path, content: bytes) -> Path:
    """Write the content to a fresh file in the target's folder and return its path."""
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as staged:
        staged.write(content)
    return Path(staged.name)


def _dump_yaml(value: Any) -> bytes:
    """Dump a value as YAML with sorted keys in block style."""
    return yaml.safe_dump(value, sort_keys=True, default_flow_style=False, allow_unicode=True).encode()


def _sha256(content: bytes) -> str:
    """Return the lowercase sha256 hex digest of the bytes."""
    return hashlib.sha256(content).hexdigest()
