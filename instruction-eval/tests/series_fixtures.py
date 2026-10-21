import hashlib
import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

import numpy
import yaml

from instruction_eval.reader import LoginFiles
from instruction_eval.records import DEFAULT_BINDING, SeriesFolder, reply_path, write_file, write_record
from instruction_eval.scores import BOOTSTRAP_SEED

SERIES_BINDING = {"plugin": DEFAULT_BINDING.plugin, "skill": DEFAULT_BINDING.skill}
OTHER_BINDING = {"plugin": "oath@elsewhere", "skill": "oath:bind"}
INSTRUCTION_EVAL_PLUGIN = "instruction-eval@my-claude-skills"


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def bootstrap_rng() -> numpy.random.Generator:
    """Return the fresh seeded random source the composition root hands each bootstrap."""
    return numpy.random.default_rng(BOOTSTRAP_SEED)


def tree(root: Path) -> list[str]:
    return sorted(f"{path.relative_to(root).as_posix()}{'/' if path.is_dir() else ''}" for path in root.rglob("*"))


def write_revision(files: SeriesFolder, number: int, parent_record: str | None = None) -> None:
    """Write revision `number`'s instruction and record, chained to the parent's record bytes unless `parent_record` names another hash."""
    revision = f"r{number}"
    write_file(files, f"{revision}/2-instruction.md", f"Revision {number}.\n".encode())
    first = number == 1
    record = {
        "number": number,
        "parent": None if first else f"r{number - 1}",
        "hash": sha256(files.read_bytes(f"{revision}/2-instruction.md")),
        "parent_record": None if first else parent_record or sha256(files.read_bytes(f"r{number - 1}/2-revision.yaml")),
        "change": None if first else {"action": "rewrite", "sentence": 1, "old": "Old.", "new": "New."},
    }
    write_record(files, f"{revision}/2-revision.yaml", record, [] if first else [f"r{number - 1}/2-revision.yaml"])


PACKET_HASH = "a" * 64
AGENT_SERIES = {"instruction": "/home/writer/terse.md", "sources": [], "reader_kind": "agent", "binding": SERIES_BINDING, "created": "2026-10-14T10:00:00+00:00"}


@dataclass(frozen=True)
class Reply:
    """One reply of a fixture revision: its origin, its text, its judge verdict, and its detector count."""

    id: str
    condition: str
    task: str
    text: str = ""
    repeat: int = 1
    turn: int | None = None
    split: str = "open"
    judged: int = 0
    hedges: int = 0
    dropped: int = 0
    done: bool | None = True
    key: bool | None = None
    kind: str = "answer"
    borrowed_from: str | None = None

    @property
    def packet(self) -> str:
        """Return the packet the reply sits in: its task, or its conversation turn."""
        return self.task if self.turn is None else f"{self.task}-turn-{self.turn}"

    def path_in(self, revision: str) -> str:
        """Return the reply file the origin names, a borrowed reply's in the revision it names."""
        return reply_path(self.borrowed_from or revision, self.condition, self.task, self.repeat, self.turn)

    def origin(self) -> dict:
        """Return the reply's origin entry."""
        entry = {"packet": self.packet, "condition": self.condition, "task": self.task, "split": self.split, "repeat": self.repeat, "borrowed_from": self.borrowed_from}
        return entry if self.turn is None else {**entry, "turn": self.turn}


def read_nothing(path: Path) -> bytes:
    """Stand in for the external file reader, which a series holding its placebo snapshot never calls."""
    raise AssertionError(f"read an external file: {path}")


def write_yaml_at(target: Path, document: object) -> None:
    """Write the document as YAML at the path, making its folder."""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(document, sort_keys=False))


def write_yaml(files: SeriesFolder, path: str, document: object) -> None:
    """Write the document as YAML at the path under the series root."""
    write_yaml_at(files.root / path, document)


@dataclass(frozen=True)
class ReadCountingFolder(SeriesFolder):
    """A series folder counting the reads of each path."""

    reads: Counter = field(default_factory=Counter)

    def read_bytes(self, path):
        self.reads[path] += 1
        return super().read_bytes(path)


OUTCOME_COST = {"replies": 4, "input_tokens": None, "output_tokens": None, "seconds": 1.5}
PARENT_COMPARISON = {"target": "d-judge", "mean_difference": -0.4, "interval": [-0.8, 0.0]}


def outcome(
    passed: bool,
    completion_passed: bool = True,
    instruction_breaches: float = 1.0,
    words: int = 10,
    cost: dict = OUTCOME_COST,
    changed_from_parent: str | None = None,
) -> dict:
    """Return a gated revision's outcome record with its keep ranks and cost, and its parent fields when it names a change from its parent."""
    record = {
        "outcome": "pass" if passed else "fail",
        "checks": [],
        "instruction_breaches": instruction_breaches,
        "completion_passed": completion_passed,
        "words": words,
        "cost": cost,
    }
    if changed_from_parent is None:
        return record
    return {**record, "changed_from_parent": changed_from_parent, "parent_comparison": PARENT_COMPARISON}


DISK_LOGIN_FILES = LoginFiles(
    resolve=Path.resolve,
    exists=Path.exists,
    is_link=Path.is_symlink,
    is_folder=Path.is_dir,
    is_file=Path.is_file,
    entries=Path.iterdir,
    read_bytes=Path.read_bytes,
)
ONE_DEMAND = {"demands": [{"id": "d-judge", "text": "Be terse.", "boundary": "Code is exempt.", "counted_by": "judge"}]}
ONE_DEMAND_COVERAGE = {"demands": {"d-judge": [1]}, "sentences": {1: ["d-judge"]}}


class NeutralLogin:
    """A neutral login under a home folder enabling instruction-eval and the binding plugin, as the commands launching agents check it."""

    def __init__(self, home: Path, binding_plugin: str = DEFAULT_BINDING.plugin):
        self.home = home
        self.config_dir = home / ".claudes-bare" / "readers"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        enabled_plugins = {INSTRUCTION_EVAL_PLUGIN: True, binding_plugin: True}
        (self.config_dir / "settings.json").write_text(json.dumps({"enabledPlugins": enabled_plugins}))

    def environ(self) -> dict[str, str]:
        """Return the environment naming the login's config folder."""
        return {"CLAUDE_CONFIG_DIR": str(self.config_dir)}


def write_agent_series(files: SeriesFolder, demands: dict, tasks: dict, anchors: dict, binding: dict = SERIES_BINDING) -> None:
    """Write an agent-reader series record binding through `binding` with its demands, tasks, and anchors."""
    write_record(files, "series.yaml", {**AGENT_SERIES, "binding": binding}, [])
    write_yaml(files, "2-demands.yaml", demands)
    write_yaml(files, "3-tasks.yaml", tasks)
    write_record(files, "6-judge/anchors.yaml", anchors, [])


def write_origins(files: SeriesFolder, revision: str, replies: Sequence[Reply], anchor: str) -> dict[str, str]:
    """Write the revision's origins of the replies, each packet carrying one origin of the anchor, and return each packet's anchor blind id."""
    packets = sorted({reply.packet for reply in replies})
    anchor_ids = {packet: f"b{index:04x}a0a0" for index, packet in enumerate(packets)}
    ids = {reply.id: reply.origin() for reply in replies}
    ids.update({anchor_id: {"packet": packet, "anchor": anchor} for packet, anchor_id in anchor_ids.items()})
    write_record(files, f"{revision}/6-origins.yaml", {"ids": ids, "packets": dict.fromkeys(packets, PACKET_HASH)}, [])
    return anchor_ids
