import hashlib
from pathlib import Path

from instruction_eval.records import SeriesFolder, write_file, write_record


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def tree(root: Path) -> list[str]:
    return sorted(f"{path.relative_to(root).as_posix()}{'/' if path.is_dir() else ''}" for path in root.rglob("*"))


def write_revision(files: SeriesFolder, number: int) -> None:
    revision = f"r{number}"
    write_file(files, f"{revision}/2-instruction.md", f"Revision {number}.\n".encode())
    first = number == 1
    record = {
        "number": number,
        "parent": None if first else f"r{number - 1}",
        "hash": sha256(files.read_bytes(f"{revision}/2-instruction.md")),
        "parent_record": None if first else sha256(files.read_bytes(f"r{number - 1}/2-revision.yaml")),
        "change": None if first else {"action": "rewrite", "sentence": 1, "old": "Old.", "new": "New."},
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [] if first else [f"r{number - 1}/2-revision.yaml"])
