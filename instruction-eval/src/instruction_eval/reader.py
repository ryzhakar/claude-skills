import hashlib
import json
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum
from itertools import accumulate
from pathlib import Path
from typing import Any, TypeVar

import yaml

from instruction_eval.conditions import control_texts, revision_condition_texts
from instruction_eval.coverage import coverage_check, split_sentences
from instruction_eval.gate import (
    BudgetRefusal,
    _cost_so_far,
    _earlier_outcomes,
    _reply_cost,
    _stop_budget,
    refuse_unaffordable_ask,
)
from instruction_eval.records import (
    AGENT_READER,
    AGENTS_FOLDER,
    COLLECTED_FILE,
    COMMAND_READER,
    CONDITION_KEYS,
    CONDITIONS_RECORD,
    COVERAGE_FILE,
    DEMANDS_RECORD,
    FIRST_REVISION,
    FROZEN_RECORD,
    GATE_RECORD,
    INSTRUCTION_FILE,
    KEY_SEPARATOR,
    PLACEBO_SNAPSHOT,
    READER_RECORD,
    REPLIES_FOLDER,
    REPLY_COST_KEYS,
    SERIES_RECORD,
    SPENT_INPUT_TOKENS_KEY,
    TASK_KEYS,
    TASKS_RECORD,
    TURN_PREFIX,
    AgentReader,
    CommandReader,
    Conversation,
    Reader,
    Refusal,
    SeriesFolder,
    SeriesRecords,
    Task,
    Tasks,
    _dump_canonical_yaml,
    condition_path,
    outcome_path,
    read_series_file,
    reply_path,
    revision_number,
    sha256,
    source_snapshot_path,
    utf8_text,
    write_file,
    write_record,
)
from instruction_eval.series import _refuse_other_reader_build, guard_series, revision_ids
from instruction_eval.tasks import ExpectedReply, expected_replies, refuse_missing_replies

FRONTMATTER_FENCE = "---\n"
LAUNCH_LIST_DESCRIPTION = "Generated agent; launch from the printed launch list only."
EMPTY_TOOLSET_LINES = ("tools: Read", "disallowedTools: Read")
JUDGE_TOOLSET_LINES = ("tools: Skill, Write",)
FRONTMATTER_BREAKERS = ("\n", "\r", ": ")
PREPARE_COMMAND = "reader prepare"
ASK_COMMAND = "revision ask"
READER_AGENT_PREFIX = "ie-reader-"
LAUNCHES_KEY = "launches"
AGENT_TYPE_KEY = "agent_type"
CONDITION_KEY = "condition"
TASK_KEY = "task"
CONVERSATION_KEY = "conversation"
REPEAT_KEY = "repeat"
LAUNCH_MESSAGE_KEY = "message"
SEND_MESSAGES_KEY = "send_messages"
FINGERPRINT_COMMAND = "reader fingerprint"
FINGERPRINT_KEYS = ("model", "build")
AGENT_READER_FINGERPRINT_REFUSAL = f"{FINGERPRINT_COMMAND} refuses an agent reader"


class AgentKind(Enum):
    READER = "reader"
    JUDGE = "judge"


class DefinitionEdited(Exception):
    """Raised when a definition on disk differs from its recomputation."""


def refuse_edited_definition(name: str, on_disk: bytes, recomputed: bytes) -> None:
    """Raise DefinitionEdited naming the definition when its bytes differ from the recomputed bytes."""
    if on_disk != recomputed:
        raise DefinitionEdited(f"{name} differs from its recomputation")


def render_agent_definition(name: str, model: str, kind: AgentKind, body: bytes) -> bytes:
    """Render an agent definition file whose body is the given bytes."""
    frontmatter = _frontmatter_text(name, model, kind)
    return frontmatter.encode("utf-8") + body


def _frontmatter_text(name: str, model: str, kind: AgentKind) -> str:
    """Return the fenced frontmatter block for one generated agent."""
    lines = (
        f"name: {_single_line_value(name)}",
        f"description: {LAUNCH_LIST_DESCRIPTION}",
        f"model: {_single_line_value(model)}",
        *_toolset_lines(kind),
    )
    return FRONTMATTER_FENCE + "".join(line + "\n" for line in lines) + FRONTMATTER_FENCE


def _single_line_value(value: str) -> str:
    """Return the value unchanged or raise ValueError when it is empty or could break frontmatter."""
    if not value or any(breaker in value for breaker in FRONTMATTER_BREAKERS):
        raise ValueError(f"frontmatter value must be non-empty, single-line, without ': ': {value!r}")
    return value


def _toolset_lines(kind: AgentKind) -> tuple[str, ...]:
    """Return the frontmatter lines that fix the tools of an agent kind."""
    return EMPTY_TOOLSET_LINES if kind is AgentKind.READER else JUDGE_TOOLSET_LINES


PROJECTS_DIR_NAME = "projects"
SUBAGENTS_DIR_NAME = "subagents"
TRANSCRIPT_PATTERN = "agent-*.jsonl"
TRANSCRIPT_ID_PREFIX = "agent-"
META_SUFFIX = ".meta.json"
AGENT_TYPE_FIELD = "agentType"
KEY_SEPARATOR_CHARS = "/."
KEY_REPLACEMENT = "-"


@dataclass(frozen=True)
class Transcript:
    """One subagent transcript with the session and agent that wrote it."""

    path: Path
    session: str
    agent_id: str
    agent_type: str


def locate_transcripts(
    config_dir: Path, series_folder: Path, working_dir: Path
) -> list[Transcript]:
    """Return the subagent transcripts of the series folder's sessions, ordered by path; an absolute series folder ignores the working dir."""
    project_dir = config_dir / PROJECTS_DIR_NAME / _project_key(working_dir / series_folder)
    paths = sorted(project_dir.glob(f"*/{SUBAGENTS_DIR_NAME}/{TRANSCRIPT_PATTERN}"))
    return [_read_transcript(path) for path in paths]


def _project_key(absolute_series_folder: Path) -> str:
    """Return the absolute path with each slash and dot replaced by a dash."""
    return "".join(
        KEY_REPLACEMENT if char in KEY_SEPARATOR_CHARS else char
        for char in str(absolute_series_folder)
    )


def _read_transcript(path: Path) -> Transcript:
    """Return the transcript at the path with the agent type its meta file holds."""
    meta_path = path.with_suffix(META_SUFFIX)
    if not meta_path.is_file():
        raise ValueError(f"{path}: meta file {meta_path.name} is missing")
    meta = _read_meta(path, meta_path)
    agent_type = meta.get(AGENT_TYPE_FIELD)
    if not isinstance(agent_type, str):
        raise ValueError(f"{path}: meta file lacks a string {AGENT_TYPE_FIELD}")
    return Transcript(
        path=path,
        session=path.parent.parent.name,
        agent_id=path.stem.removeprefix(TRANSCRIPT_ID_PREFIX),
        agent_type=agent_type,
    )


def _read_meta(path: Path, meta_path: Path) -> dict:
    """Return the JSON object the meta file holds, refusing any other content by transcript name."""
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        raise ValueError(f"{path}: meta file is not valid JSON") from None
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: meta file is not a JSON object")
    return meta


_USER_ENTRY_TYPE = "user"
_ASSISTANT_ENTRY_TYPE = "assistant"
_TEXT_BLOCK_TYPE = "text"
_SEND_MESSAGE_WRAPPER_OPENING = "The coordinator sent a message while you were working:\n"
_SEND_MESSAGE_WRAPPER_CLOSING = "\n\nAddress this before completing your current task."
_TYPE_KEY = "type"
_MESSAGE_KEY = "message"
_CONTENT_KEY = "content"
_TIMESTAMP_KEY = "timestamp"
_ID_KEY = "id"
_MODEL_KEY = "model"
_USAGE_KEY = "usage"
_META_KEY = "isMeta"
_TEXT_KEY = "text"

_FieldValue = TypeVar("_FieldValue")


@dataclass(frozen=True)
class TokenUsage:
    """Tokens one reply spent, each field named and counted as the transcript's `message.usage` key."""

    input_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    output_tokens: int

    @property
    def spent_input_tokens(self) -> int:
        """Return every input token the reply spent: uncached, cache creation, and cache read."""
        return self.input_tokens + self.cache_creation_input_tokens + self.cache_read_input_tokens


@dataclass(frozen=True)
class TranscriptReply:
    """One user turn of a subagent transcript paired with the last assistant text answering it."""

    turn: int
    message: str
    text: str
    model: str
    started: datetime
    seconds: float
    tokens: TokenUsage | None
    transcript: Path
    transcript_hash: str


@dataclass(frozen=True)
class _TurnOpening:
    """A user message that opens a turn, typed or delivered by SendMessage."""

    message: str
    timestamp: datetime


@dataclass(frozen=True)
class _AssistantChunk:
    """One assistant line, with the byte offset just past it."""

    message_id: str
    model: str
    texts: tuple[str, ...]
    usage: TokenUsage | None
    timestamp: datetime
    end: int


class _MalformedEntry(Exception):
    """A decoded transcript entry lacks a field the parser reads, or holds it in the wrong shape."""


def parse_transcript_replies(transcript: Path, content: bytes) -> tuple[TranscriptReply, ...]:
    """Pair the k-th user message of the transcript bytes with its reply as turn k, skipping unanswered turns."""
    turns = _group_entries_by_turn(_read_transcript_entries(transcript, content))
    replies = (
        _reply_to_turn(number, opening, chunks, transcript, content)
        for number, (opening, chunks) in enumerate(turns, 1)
    )
    return tuple(reply for reply in replies if reply is not None)


def _read_transcript_entries(transcript: Path, content: bytes) -> tuple[_TurnOpening | _AssistantChunk, ...]:
    """Read the turn openings and assistant chunks of each non-blank JSONL line, keeping where each chunk's bytes end."""
    raw_lines = content.splitlines(keepends=True)
    ends = accumulate(len(raw_line) for raw_line in raw_lines)
    entries = (
        _parse_transcript_line(transcript, number, raw_line, end)
        for number, (raw_line, end) in enumerate(zip(raw_lines, ends), 1)
        if raw_line.strip()
    )
    return tuple(entry for entry in entries if entry is not None)


def _parse_transcript_line(
    transcript: Path, number: int, raw_line: bytes, end: int
) -> _TurnOpening | _AssistantChunk | None:
    """Read one transcript line into what turn pairing uses, refusing with transcript, line, and fault when it cannot."""
    entry = _decode_object_line(transcript, number, raw_line)
    try:
        return _entry_from_json(entry, end)
    except _MalformedEntry as fault:
        raise ValueError(f"{transcript}: line {number} {fault}") from fault


def _decode_object_line(transcript: Path, number: int, raw_line: bytes) -> dict[str, Any]:
    """Decode one transcript line as a JSON object, refusing with the transcript and line number when it is not."""
    entry = _decode_transcript_line(transcript, number, raw_line)
    if not isinstance(entry, dict):
        raise ValueError(f"{transcript}: line {number} is not a JSON object")
    return entry


def _decode_transcript_line(transcript: Path, number: int, raw_line: bytes) -> object:
    """Decode one transcript line as JSON, refusing with the transcript and line number when it is not."""
    try:
        return json.loads(raw_line)
    except json.JSONDecodeError as error:
        raise ValueError(f"{transcript}: line {number} is not JSON") from error


def _entry_from_json(entry: dict[str, Any], end: int) -> _TurnOpening | _AssistantChunk | None:
    """Read a decoded entry as a turn opening or an assistant chunk, or None when it is neither."""
    entry_type = _field(entry, (_TYPE_KEY,), str)
    if entry_type == _USER_ENTRY_TYPE:
        return _turn_opening_from_json(entry)
    if entry_type == _ASSISTANT_ENTRY_TYPE:
        return _assistant_chunk_from_json(entry, end)
    return None


def _turn_opening_from_json(entry: dict[str, Any]) -> _TurnOpening | None:
    """Read a user entry as a turn opening, or None for tool results and harness injections."""
    content = _field(entry, (_MESSAGE_KEY, _CONTENT_KEY), object)
    if not isinstance(content, str):
        return None
    if entry.get(_META_KEY) and not content.startswith(_SEND_MESSAGE_WRAPPER_OPENING):
        return None
    return _TurnOpening(message=content, timestamp=_timestamp_field(entry))


def _assistant_chunk_from_json(entry: dict[str, Any], end: int) -> _AssistantChunk:
    """Read an assistant entry's message id, model, text blocks, usage, and timestamp."""
    blocks = _field(entry, (_MESSAGE_KEY, _CONTENT_KEY), list)
    return _AssistantChunk(
        message_id=_field(entry, (_MESSAGE_KEY, _ID_KEY), str),
        model=_field(entry, (_MESSAGE_KEY, _MODEL_KEY), str),
        texts=tuple(
            _field(block, (_TEXT_KEY,), str)
            for block in blocks
            if _field(block, (_TYPE_KEY,), str) == _TEXT_BLOCK_TYPE
        ),
        usage=_usage_field(entry),
        timestamp=_timestamp_field(entry),
        end=end,
    )


def _usage_field(entry: dict[str, Any]) -> TokenUsage | None:
    """Read the assistant entry's usage, or None when it records none."""
    if not _has_field(entry, (_MESSAGE_KEY, _USAGE_KEY)):
        return None
    return TokenUsage(
        **{field.name: _field(entry, (_MESSAGE_KEY, _USAGE_KEY, field.name), int) for field in fields(TokenUsage)}
    )


def _timestamp_field(entry: dict[str, Any]) -> datetime:
    """Read the entry's ISO 8601 timestamp as an aware datetime."""
    try:
        return datetime.fromisoformat(_field(entry, (_TIMESTAMP_KEY,), str))
    except ValueError as error:
        raise _MalformedEntry(f"has an unparseable {_TIMESTAMP_KEY}") from error


def _field(entry: object, path: tuple[str, ...], expected_type: type[_FieldValue]) -> _FieldValue:
    """Return the value the nested keys of the path lead to, refusing a missing key or a value of another type."""
    if not _has_field(entry, path):
        raise _MalformedEntry(f"lacks {'.'.join(path)}")
    value: object = entry
    for key in path:
        value = value[key]
    if not isinstance(value, expected_type):
        raise _MalformedEntry(f"has a non-{expected_type.__name__} {'.'.join(path)}")
    return value


def _has_field(entry: object, path: tuple[str, ...]) -> bool:
    """Tell whether the nested keys of the path lead to a value in the entry."""
    value: object = entry
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return False
        value = value[key]
    return True


def _group_entries_by_turn(
    entries: tuple[_TurnOpening | _AssistantChunk, ...],
) -> tuple[tuple[_TurnOpening, tuple[_AssistantChunk, ...]], ...]:
    """Split the entries into turns, each a turn opening with the assistant chunks up to the next opening."""
    starts = [index for index, entry in enumerate(entries) if isinstance(entry, _TurnOpening)]
    return tuple(
        (entries[start], entries[start + 1 : stop])
        for start, stop in zip(starts, [*starts[1:], len(entries)])
    )


def _reply_to_turn(
    number: int,
    opening: _TurnOpening,
    chunks: tuple[_AssistantChunk, ...],
    transcript: Path,
    content: bytes,
) -> TranscriptReply | None:
    """Build the reply to one turn from its last assistant text, or None when no assistant text answers it."""
    answering_chunks = [chunk for chunk in chunks if chunk.texts]
    if not answering_chunks:
        return None
    reply_chunk = answering_chunks[-1]
    return TranscriptReply(
        turn=number,
        message=opening.message,
        text="".join(reply_chunk.texts),
        model=reply_chunk.model,
        started=opening.timestamp,
        seconds=(reply_chunk.timestamp - opening.timestamp).total_seconds(),
        tokens=_turn_token_usage(chunks),
        transcript=transcript,
        transcript_hash=hashlib.sha256(content[: reply_chunk.end]).hexdigest(),
    )


def _turn_token_usage(chunks: tuple[_AssistantChunk, ...]) -> TokenUsage | None:
    """Sum the final usage of each assistant message in the turn, or None when any message lacks usage."""
    final_usages = {chunk.message_id: chunk.usage for chunk in chunks}.values()
    if None in final_usages:
        return None
    return TokenUsage(
        **{field.name: sum(getattr(usage, field.name) for usage in final_usages) for field in fields(TokenUsage)}
    )


CONFIG_DIR_VARIABLE = "CLAUDE_CONFIG_DIR"
BARE_LOGINS_DIRNAME = ".claudes-bare"
SETTINGS_FILENAME = "settings.json"
MEMORY_FILENAME = "CLAUDE.md"
EXTENSION_FOLDERNAMES = ("agents", "skills")
USER_MEMORY_RELATIVE_PATH = Path(".claude") / MEMORY_FILENAME
MEMORY_RELATIVE_PATHS = (
    Path(MEMORY_FILENAME),
    USER_MEMORY_RELATIVE_PATH,
    Path("CLAUDE.local.md"),
    Path(".manifestos.yaml"),
)
ENABLED_PLUGINS_KEY = "enabledPlugins"
REQUIRED_PLUGINS = {
    "instruction-eval@my-claude-skills": True,
    "manifesto@my-claude-skills": True,
}


class NeutralLoginRefused(Exception):
    """Raised when the session is not the neutral login."""


def check_neutral_login(
    environ: Mapping[str, str], home: Path, working_dir: Path
) -> None:
    """Refuse unless the session runs under the neutral login at a clean working directory."""
    config_dir = _neutral_config_dir(environ, home)
    _refuse_claude_md(config_dir)
    for folder_name in EXTENSION_FOLDERNAMES:
        _refuse_extension_folder(config_dir / folder_name)
    _refuse_other_plugins(config_dir)
    _refuse_memory_files_in_ancestry(working_dir, home)


def _neutral_config_dir(
    environ: Mapping[str, str], home: Path
) -> Path:
    """Return the config directory, refusing when it is unset or outside the bare logins folder."""
    configured = environ.get(CONFIG_DIR_VARIABLE)
    if not configured:
        raise NeutralLoginRefused(f"{CONFIG_DIR_VARIABLE} is unset")
    config_dir = Path(configured).resolve()
    bare_logins = (home / BARE_LOGINS_DIRNAME).resolve()
    if bare_logins not in config_dir.parents:
        raise NeutralLoginRefused(f"{config_dir} is outside {bare_logins}")
    return config_dir


def _refuse_claude_md(config_dir: Path) -> None:
    """Refuse when the config directory holds a CLAUDE.md."""
    memory_file = config_dir / MEMORY_FILENAME
    if memory_file.exists() or memory_file.is_symlink():
        raise NeutralLoginRefused(f"{memory_file} exists")


def _refuse_extension_folder(folder: Path) -> None:
    """Refuse when the folder is linked or holds anything."""
    if folder.is_symlink():
        raise NeutralLoginRefused(f"{folder} is a link")
    if folder.exists() and not _is_empty_folder(folder):
        raise NeutralLoginRefused(f"{folder} is not an empty folder")


def _is_empty_folder(folder: Path) -> bool:
    """Report whether the path is a folder with no entries."""
    return folder.is_dir() and not any(folder.iterdir())


def _refuse_other_plugins(config_dir: Path) -> None:
    """Refuse unless enabledPlugins is exactly the two required plugins, both true."""
    settings_file = config_dir / SETTINGS_FILENAME
    if not settings_file.is_file():
        raise NeutralLoginRefused(f"{settings_file} is missing")
    try:
        settings = json.loads(settings_file.read_text())
    except json.JSONDecodeError as error:
        raise NeutralLoginRefused(f"{settings_file} is not JSON") from error
    enabled = settings.get(ENABLED_PLUGINS_KEY) if isinstance(settings, dict) else None
    if not isinstance(enabled, dict) or set(enabled) != set(REQUIRED_PLUGINS):
        raise NeutralLoginRefused(f"{ENABLED_PLUGINS_KEY} is not the two required plugins")
    if not all(value is True for value in enabled.values()):
        raise NeutralLoginRefused(f"{ENABLED_PLUGINS_KEY} holds a plugin not true")


def _refuse_memory_files_in_ancestry(
    working_dir: Path, home: Path
) -> None:
    """Refuse when the working directory or an ancestor holds a memory file, sparing the home user memory."""
    user_memory = (home / USER_MEMORY_RELATIVE_PATH).resolve()
    resolved = working_dir.resolve()
    for folder in (resolved, *resolved.parents):
        for relative_path in MEMORY_RELATIVE_PATHS:
            memory_file = folder / relative_path
            if memory_file != user_memory and memory_file.exists():
                raise NeutralLoginRefused(f"{memory_file} exists")


_ATTACHMENT_ENTRY_TYPE = "attachment"
_ATTACHMENT_KEY = "attachment"
_INSTRUCTIONS_ATTACHMENT_TYPE = "instructions"
_NESTED_MEMORY_ATTACHMENT_TYPE = "nested_memory"
_FILES_KEY = "files"
_PATH_KEY = "path"
_HOOK_EVENT_KEY = "hookEvent"
_SUBAGENT_START_EVENT = "SubagentStart"
_HOOK_TEXT_KEYS = ("stdout", "content")
_SUBAGENT_START_EXPOSURE = "shows SubagentStart text"
_TOOL_USE_BLOCK_SUFFIX = "tool_use"
_NAME_KEY = "name"
_INPUT_KEY = "input"
_SKILL_TOOL = "Skill"
_SKILL_INPUT_KEY = "skill"
OATH_SKILL = "manifesto:manifesto-oath"
_WRITE_TOOL = "Write"
_FILE_PATH_INPUT_KEY = "file_path"


def refuse_exposed_reader_transcript(transcript: Path, content: bytes, turns: Sequence[str], pinned_model: str) -> None:
    """Refuse a reader transcript showing a memory file, SubagentStart text, any tool use, a turn message other than the task's, or a model other than the pinned one."""
    exposures = (
        *_screen_entries(
            transcript,
            content,
            (
                _outside_context_exposures,
                lambda entry: _tool_use_exposures(entry, _no_tool_use_allowed),
                lambda entry: _model_exposures(entry, pinned_model),
            ),
        ),
        *_turn_message_exposures(transcript, content, turns),
    )
    if exposures:
        raise Refusal(f"{transcript}: {exposures[0]}")


def judge_transcript_rejection(transcript: Path, content: bytes, verdict_path: Path) -> str | None:
    """Return why a judge transcript rejects its verdict, a memory file, SubagentStart text, or a tool use besides loading the oath skill and writing the verdict path, or None when nothing does."""
    exposures = _screen_entries(
        transcript,
        content,
        (
            _outside_context_exposures,
            lambda entry: _tool_use_exposures(
                entry, lambda tool_use: _is_oath_skill_load(tool_use) or _is_verdict_write(tool_use, verdict_path)
            ),
        ),
    )
    return exposures[0] if exposures else None


def _is_oath_skill_load(tool_use: dict[str, Any]) -> bool:
    """Tell whether a tool use loads the manifesto oath skill."""
    return _field(tool_use, (_NAME_KEY,), str) == _SKILL_TOOL and _field(tool_use, (_INPUT_KEY,), dict).get(_SKILL_INPUT_KEY) == OATH_SKILL


def _is_verdict_write(tool_use: dict[str, Any], verdict_path: Path) -> bool:
    """Tell whether a tool use writes the verdict path."""
    return _field(tool_use, (_NAME_KEY,), str) == _WRITE_TOOL and _field(tool_use, (_INPUT_KEY,), dict).get(_FILE_PATH_INPUT_KEY) == str(verdict_path)


def _screen_entries(
    transcript: Path, content: bytes, screens: Iterable[Callable[[dict[str, Any]], tuple[str, ...]]]
) -> tuple[str, ...]:
    """Name what each screen finds in each non-blank transcript line, in line order, refusing with transcript, line, and fault a line it cannot read."""
    return tuple(
        exposure
        for number, raw_line in enumerate(content.splitlines(), 1)
        if raw_line.strip()
        for exposure in _screen_entry(transcript, number, _decode_object_line(transcript, number, raw_line), screens)
    )


def _screen_entry(
    transcript: Path, number: int, entry: dict[str, Any], screens: Iterable[Callable[[dict[str, Any]], tuple[str, ...]]]
) -> tuple[str, ...]:
    """Name what each screen finds in one entry, refusing with transcript, line, and fault an entry missing a field a screen reads."""
    try:
        return tuple(exposure for screen in screens for exposure in screen(entry))
    except _MalformedEntry as fault:
        raise ValueError(f"{transcript}: line {number} {fault}") from fault


def _outside_context_exposures(entry: dict[str, Any]) -> tuple[str, ...]:
    """Name each memory file and each SubagentStart text an attachment entry shows."""
    if _field(entry, (_TYPE_KEY,), str) != _ATTACHMENT_ENTRY_TYPE:
        return ()
    return _attachment_exposures(_field(entry, (_ATTACHMENT_KEY,), dict))


def _attachment_exposures(attachment: dict[str, Any]) -> tuple[str, ...]:
    """Name each memory file and each SubagentStart text one attachment shows."""
    memory_exposures = tuple(f"shows memory file {path}" for path in _memory_file_paths(attachment))
    return (*memory_exposures, *_subagent_start_exposures(attachment))


def _subagent_start_exposures(attachment: dict[str, Any]) -> tuple[str, ...]:
    """Name the SubagentStart text an attachment shows, when its hook output or added context is non-empty."""
    shows_text = attachment.get(_HOOK_EVENT_KEY) == _SUBAGENT_START_EVENT and any(
        attachment.get(key) for key in _HOOK_TEXT_KEYS
    )
    return (_SUBAGENT_START_EXPOSURE,) if shows_text else ()


def _memory_file_paths(attachment: dict[str, Any]) -> tuple[str, ...]:
    """Return the path of each memory file an attachment carries into the agent's context."""
    attachment_type = _field(attachment, (_TYPE_KEY,), str)
    if attachment_type == _INSTRUCTIONS_ATTACHMENT_TYPE:
        return tuple(_field(file, (_PATH_KEY,), str) for file in _field(attachment, (_FILES_KEY,), list))
    if attachment_type == _NESTED_MEMORY_ATTACHMENT_TYPE:
        return (_field(attachment, (_PATH_KEY,), str),)
    return ()


def _tool_use_exposures(entry: dict[str, Any], allowed: Callable[[dict[str, Any]], bool]) -> tuple[str, ...]:
    """Name each tool use of an assistant entry that the allowance refuses."""
    if _field(entry, (_TYPE_KEY,), str) != _ASSISTANT_ENTRY_TYPE:
        return ()
    return tuple(
        f"shows tool use {_field(block, (_NAME_KEY,), str)}"
        for block in _field(entry, (_MESSAGE_KEY, _CONTENT_KEY), list)
        if _field(block, (_TYPE_KEY,), str).endswith(_TOOL_USE_BLOCK_SUFFIX) and not allowed(block)
    )


def _no_tool_use_allowed(tool_use: dict[str, Any]) -> bool:
    """Allow no tool use."""
    return False


def _turn_message_exposures(transcript: Path, content: bytes, turns: Sequence[str]) -> tuple[str, ...]:
    """Name each turn whose message differs from the task's turn as the reader receives it, the SendMessage wrapper kept on later turns."""
    received = (*turns[:1], *(_SEND_MESSAGE_WRAPPER_OPENING + turn + _SEND_MESSAGE_WRAPPER_CLOSING for turn in turns[1:]))
    openings = [entry for entry in _read_transcript_entries(transcript, content) if isinstance(entry, _TurnOpening)]
    return tuple(
        f"turn {number} message differs from the task's"
        for number, opening in enumerate(openings, 1)
        if number > len(received) or opening.message != received[number - 1]
    )


def _model_exposures(entry: dict[str, Any], pinned_model: str) -> tuple[str, ...]:
    """Name an assistant entry's model when it is other than the pinned one."""
    if _field(entry, (_TYPE_KEY,), str) != _ASSISTANT_ENTRY_TYPE:
        return ()
    model = _field(entry, (_MESSAGE_KEY, _MODEL_KEY), str)
    return () if model == pinned_model else (f"model {model} is not the pinned {pinned_model}",)


@dataclass(frozen=True)
class Fingerprint:
    """The parsed output of a command reader's fingerprint with the sha256 of its canonical YAML."""

    output: Mapping[str, Any]
    fingerprint_hash: str


def reader_fingerprint(files: SeriesFolder, run_fingerprint: Callable[[Sequence[str]], str]) -> Fingerprint:
    """Run the command reader's fingerprint and return its parsed output with the hash of that output as canonical YAML."""
    guard_series(files, FINGERPRINT_COMMAND)
    reader = _command_reader(SeriesRecords(files).reader())
    output = _parse_fingerprint_output(run_fingerprint(reader.fingerprint))
    _refuse_missing_key(output, (*FINGERPRINT_KEYS, *reader.sampling))
    return Fingerprint(output=output, fingerprint_hash=sha256(_dump_canonical_yaml(output)))


def _command_reader(reader: Reader) -> CommandReader:
    """Return the reader when it is a command reader, refusing an agent reader."""
    if isinstance(reader, AgentReader):
        raise Refusal(AGENT_READER_FINGERPRINT_REFUSAL)
    return reader


def _parse_fingerprint_output(text: str) -> dict[str, Any]:
    """Parse the fingerprint output as a YAML mapping, refusing any other content."""
    try:
        output = yaml.safe_load(text)
    except yaml.YAMLError:
        output = None
    if not isinstance(output, dict):
        raise Refusal("fingerprint output is not a YAML mapping")
    return output


def _refuse_missing_key(output: Mapping[str, Any], required: Iterable[str]) -> None:
    """Refuse the first required key the output lacks."""
    for key in required:
        if key not in output:
            raise Refusal(f"fingerprint output lacks {key}")


def reader_prepare(
    files: SeriesFolder,
    revision: str,
    read_external: Callable[[Path], bytes],
    environ: Mapping[str, str],
    home: Path,
    working_dir: Path,
) -> None:
    """Write the condition files of the revision, the placebo snapshot first for r1."""
    guard_series(files, PREPARE_COMMAND)
    records = SeriesRecords(files)
    reader = records.reader()
    if isinstance(reader, AgentReader):
        check_neutral_login(environ, home, working_dir)
    placebo_source = _external_placebo_source(revision, records, read_external)
    texts = _condition_texts(files, revision, records, placebo_source)
    if placebo_source is not None:
        write_file(files, PLACEBO_SNAPSHOT, placebo_source)
    for condition, text in texts.items():
        write_file(files, condition_path(revision, condition), text)
    if isinstance(reader, AgentReader):
        _write_reader_definitions(files, revision, reader.model, texts)


def _external_placebo_source(revision: str, records: SeriesRecords, read_external: Callable[[Path], bytes]) -> bytes | None:
    """Return the bytes of the external placebo source for r1, or None for a later revision, refusing a missing file."""
    if revision != FIRST_REVISION:
        return None
    path = records.conditions().placebo_source
    try:
        return read_external(path)
    except FileNotFoundError:
        raise Refusal(f"missing placebo source: {path}") from None


def _condition_texts(files: SeriesFolder, revision: str, records: SeriesRecords, placebo_source: bytes | None) -> dict[str, bytes]:
    """Return the text of each condition the revision prepares, by condition."""
    instruction = _revision_instruction(files, revision)
    own_texts = revision_condition_texts(instruction, records.conditions().omissions)
    if placebo_source is None:
        return own_texts
    sources = {path: utf8_text(files.read_bytes(path), path) for path in _source_paths(records)}
    try:
        controls = control_texts(records.conditions(), instruction, sources, utf8_text(placebo_source, PLACEBO_SNAPSHOT))
    except ValueError as refused:
        raise Refusal(str(refused)) from None
    return {**own_texts, **controls}


def _revision_instruction(files: SeriesFolder, revision: str) -> bytes:
    """Return the bytes of a revision's instruction snapshot, refusing it absent."""
    return read_series_file(files, f"{revision}/{INSTRUCTION_FILE}")


def _source_paths(records: SeriesRecords) -> list[str]:
    """Return the series path of each source snapshot, in `sources` order."""
    return [source_snapshot_path(source.name) for source in records.series().sources]


def _write_reader_definitions(files: SeriesFolder, revision: str, model: str, texts: Mapping[str, bytes]) -> None:
    """Write one reader definition per condition, its body the condition's text."""
    for condition, text in texts.items():
        agent_type = _reader_agent_type(revision, condition)
        definition = render_agent_definition(agent_type, model, AgentKind.READER, text)
        write_file(files, f"{AGENTS_FOLDER}/{agent_type}.md", definition)


def _reader_agent_type(revision: str, condition: str) -> str:
    """Return the agent type of the reader that runs a condition of a revision."""
    return f"{READER_AGENT_PREFIX}{revision}-{condition}"


def agent_launch_list(files: SeriesFolder, revision: str, conditions: Sequence[str]) -> str:
    """Return the launch list as YAML: per task and per conversation, condition, and repeat, the agent type and the exact messages."""
    guard_series(files, ASK_COMMAND)
    records = SeriesRecords(files)
    return _launch_list(_asked_replies(files, revision, records, conditions), records)


def _launch_list(replies: Sequence[ExpectedReply], records: SeriesRecords) -> str:
    """Return the launch list of the replies as YAML."""
    return yaml.safe_dump({LAUNCHES_KEY: _launches(replies, records.tasks())}, sort_keys=False, allow_unicode=True)


def _asked_replies(files: SeriesFolder, revision: str, records: SeriesRecords, conditions: Sequence[str]) -> tuple[ExpectedReply, ...]:
    """Return the expected replies of the revision no file holds yet, those of the named conditions when any are named."""
    expected = _expected_reply_set(files, revision, records)
    return tuple(reply for reply in expected if (not conditions or reply.condition in conditions) and not files.holds(reply.path))


def _expected_reply_set(files: SeriesFolder, revision: str, records: SeriesRecords) -> tuple[ExpectedReply, ...]:
    """Return the replies the revision expects at the gate's repeats, in path order."""
    sentence_count = len(split_sentences(_revision_instruction(files, revision)))
    return expected_replies(revision, records.tasks(), records.conditions(), _gate_repeats(records), sentence_count)


def _gate_repeats(records: SeriesRecords) -> int:
    """Return the repeats the gate holds, refusing them unwritten."""
    repeats = records.gate().repeats
    if repeats is None:
        raise Refusal(f"missing key: {GATE_RECORD}{KEY_SEPARATOR}{REPEATS_KEY}")
    return repeats


def _launches(replies: Sequence[ExpectedReply], tasks: Tasks) -> list[dict[str, Any]]:
    """Return one launch per task or conversation repeat the replies name, in reply order."""
    task_by_id = {task.id: task for task in tasks.tasks}
    turns_by_conversation = {conversation.id: conversation.turns for conversation in tasks.conversations}
    repeats = dict.fromkeys((reply.revision, reply.condition, reply.task, reply.repeat) for reply in replies)
    return [
        _launch(revision, condition, task, repeat, task_by_id, turns_by_conversation)
        for revision, condition, task, repeat in repeats
    ]


def _launch(
    revision: str,
    condition: str,
    task: str,
    repeat: int,
    task_by_id: Mapping[str, Task],
    turns_by_conversation: Mapping[str, tuple[str, ...]],
) -> dict[str, Any]:
    """Return the launch of one task or conversation repeat."""
    launch = {AGENT_TYPE_KEY: _reader_agent_type(revision, condition), CONDITION_KEY: condition}
    if task in task_by_id:
        return {**launch, TASK_KEY: task, REPEAT_KEY: repeat, LAUNCH_MESSAGE_KEY: task_by_id[task].message}
    first_turn, *later_turns = turns_by_conversation[task]
    return {**launch, CONVERSATION_KEY: task, REPEAT_KEY: repeat, LAUNCH_MESSAGE_KEY: first_turn, SEND_MESSAGES_KEY: later_turns}


COLLECT_COMMAND = "revision collect"
SURPLUS_NOTICE = "ignored surplus transcript: "
READER_RECORD_KIND_KEY = "kind"
REPEATS_KEY = "repeats"
BUDGET_KEY = "budget"
SPLIT_KEY = "split"
TURN_KEY = "turn"
REPLY_MESSAGE_KEY = "message"
REPLY_MODEL_KEY = "model"
READER_KIND_KEY = "reader_kind"
STARTED_KEY = "started"
SECONDS_KEY = "seconds"
TRANSCRIPT_KEY = "transcript"
TRANSCRIPT_HASH_KEY = "transcript_hash"
FINGERPRINT_HASH_KEY = "fingerprint_hash"
COST_KEY = "cost"


def revision_collect(
    files: SeriesFolder, revision: str, transcripts: Sequence[Transcript], read_transcript: Callable[[Path], bytes]
) -> str:
    """Write the replies the revision's reader transcripts hold and return a line per surplus transcript, a command reader's collect writing nothing, refusing a gap against the expected replies with the surplus lines after the gap."""
    guard_series(files, COLLECT_COMMAND)
    records = SeriesRecords(files)
    reader = records.reader()
    texts = _verified_condition_texts(files, revision, records, reader)
    expected = _expected_reply_set(files, revision, records)
    surplus: tuple[Transcript, ...] = ()
    if isinstance(reader, AgentReader):
        reads = [*_reader_reads(revision, records, reader, texts), *(_definition_path(revision, condition) for condition in texts)]
        surplus = _write_agent_replies(files, records, reader.model, reads, expected, transcripts, read_transcript)
    listing = "".join(f"{SURPLUS_NOTICE}{transcript.path}\n" for transcript in surplus)
    try:
        refuse_missing_replies(files, expected)
    except Refusal as gap:
        raise Refusal(f"{gap}\n{listing}".rstrip("\n")) from None
    return listing


def _verified_condition_texts(files: SeriesFolder, revision: str, records: SeriesRecords, reader: Reader) -> dict[str, bytes]:
    """Return the text of each condition the revision prepares, recomputed from the series files, refusing a condition file or an agent reader's definition that differs from its recomputation."""
    placebo_source = read_series_file(files, PLACEBO_SNAPSHOT) if revision == FIRST_REVISION else None
    texts = _condition_texts(files, revision, records, placebo_source)
    for condition, text in texts.items():
        _refuse_edited_file(files, condition_path(revision, condition), text)
        if isinstance(reader, AgentReader):
            definition = render_agent_definition(_reader_agent_type(revision, condition), reader.model, AgentKind.READER, text)
            _refuse_edited_file(files, _definition_path(revision, condition), definition)
    return texts


def _refuse_edited_file(files: SeriesFolder, path: str, recomputed: bytes) -> None:
    """Refuse the series file at `path` when its bytes differ from the recomputed bytes."""
    try:
        refuse_edited_definition(path, read_series_file(files, path), recomputed)
    except DefinitionEdited as edited:
        raise Refusal(str(edited)) from None


def _definition_path(revision: str, condition: str) -> str:
    """Return the series path of the reader definition of a condition of a revision."""
    return f"{AGENTS_FOLDER}/{_reader_agent_type(revision, condition)}.md"


def _reader_reads(revision: str, records: SeriesRecords, reader: Reader, texts: Mapping[str, bytes]) -> list[str]:
    """Return what the reader commands read of every revision: the series, sources, task, condition, and reader keys, the placebo snapshot, the repeats, the instruction, and the condition files."""
    return [
        SERIES_RECORD,
        *_source_paths(records),
        *(f"{TASKS_RECORD}{KEY_SEPARATOR}{key}" for key in TASK_KEYS),
        *(f"{CONDITIONS_RECORD}{KEY_SEPARATOR}{key}" for key in CONDITION_KEYS),
        PLACEBO_SNAPSHOT,
        *(f"{READER_RECORD}{KEY_SEPARATOR}{key}" for key in (READER_RECORD_KIND_KEY, *(field.name for field in fields(reader)))),
        f"{GATE_RECORD}{KEY_SEPARATOR}{REPEATS_KEY}",
        f"{revision}/{INSTRUCTION_FILE}",
        *(condition_path(revision, condition) for condition in texts),
    ]


@dataclass(frozen=True)
class _ReaderTranscript:
    """A reader transcript matched to the task or conversation its first message opened, with its replies."""

    revision: str
    condition: str
    entry: Task | Conversation
    transcript: Transcript
    content: bytes
    replies: tuple[TranscriptReply, ...]

    @property
    def started(self) -> datetime:
        """Return when the transcript's first reply began."""
        return self.replies[0].started


def _write_agent_replies(
    files: SeriesFolder,
    records: SeriesRecords,
    pinned_model: str,
    reads: Sequence[str],
    expected: Sequence[ExpectedReply],
    transcripts: Sequence[Transcript],
    read_transcript: Callable[[Path], bytes],
) -> tuple[Transcript, ...]:
    """Write each expected reply no file holds from the earliest matching transcripts and return the surplus transcripts, refusing an exposed transcript before writing any reply."""
    matched = _reader_transcripts(expected, records.tasks(), transcripts, read_transcript)
    numbered, surplus = _numbered_by_start(matched, _gate_repeats(records))
    expected_paths = {reply.path for reply in expected}
    writes: list[tuple[str, dict[str, Any]]] = []
    for repeat, match in numbered:
        missing = {path: reply for path, reply in _transcript_reply_paths(match, repeat).items() if path in expected_paths and not files.holds(path)}
        if missing:
            refuse_exposed_reader_transcript(match.transcript.path, match.content, _turn_messages(match.entry), pinned_model)
        writes.extend((path, _agent_reply_record(match, repeat, reply)) for path, reply in missing.items())
    for path, record in writes:
        write_record(files, path, record, reads)
    return tuple(match.transcript for match in surplus)


def _reader_transcripts(
    expected: Sequence[ExpectedReply], tasks: Tasks, transcripts: Sequence[Transcript], read_transcript: Callable[[Path], bytes]
) -> list[_ReaderTranscript]:
    """Return the transcripts whose agent type is an expected reader's and whose first user message is the first message of an expected task or conversation."""
    readers = {_reader_agent_type(reply.revision, reply.condition): (reply.revision, reply.condition) for reply in expected}
    entries = {_turn_messages(entry)[0]: entry for entry in (*tasks.tasks, *tasks.conversations)}
    wanted = {(reply.revision, reply.condition, reply.task) for reply in expected}
    matches = []
    for transcript in transcripts:
        if transcript.agent_type not in readers:
            continue
        content = read_transcript(transcript.path)
        replies = parse_transcript_replies(transcript.path, content)
        revision, condition = readers[transcript.agent_type]
        entry = entries.get(replies[0].message) if replies and replies[0].turn == 1 else None
        if entry is not None and (revision, condition, entry.id) in wanted:
            matches.append(_ReaderTranscript(revision, condition, entry, transcript, content, replies))
    return matches


def _turn_messages(entry: Task | Conversation) -> tuple[str, ...]:
    """Return the messages the reader receives for a task or conversation, one per turn."""
    return entry.turns if isinstance(entry, Conversation) else (entry.message,)


def _numbered_by_start(matches: Sequence[_ReaderTranscript], repeats: int) -> tuple[list[tuple[int, _ReaderTranscript]], list[_ReaderTranscript]]:
    """Number the earliest `repeats` transcripts of each condition and task 1.. by start time and return the later ones as surplus."""
    groups: dict[tuple[str, str, str], list[_ReaderTranscript]] = {}
    for match in matches:
        groups.setdefault((match.revision, match.condition, match.entry.id), []).append(match)
    numbered: list[tuple[int, _ReaderTranscript]] = []
    surplus: list[_ReaderTranscript] = []
    for group in groups.values():
        by_start = sorted(group, key=lambda match: match.started)
        numbered.extend(enumerate(by_start[:repeats], 1))
        surplus.extend(by_start[repeats:])
    return numbered, surplus


def _transcript_reply_paths(match: _ReaderTranscript, repeat: int) -> dict[str, TranscriptReply]:
    """Map the reply file of each turn the entry has, at the repeat, to the transcript's reply to that turn."""
    turns = len(_turn_messages(match.entry))
    single = isinstance(match.entry, Task)
    return {
        reply_path(match.revision, match.condition, match.entry.id, repeat, None if single else reply.turn): reply
        for reply in match.replies
        if reply.turn <= turns
    }


def _reply_identity(entry: Task | Conversation, condition: str, repeat: int, turn: int | None) -> dict[str, Any]:
    """Return the keys naming one reply and the message it answers: condition, task, split, repeat, message, and for a conversation the turn."""
    identity = {
        CONDITION_KEY: condition,
        TASK_KEY: entry.id,
        SPLIT_KEY: entry.split,
        REPEAT_KEY: repeat,
        REPLY_MESSAGE_KEY: _turn_messages(entry)[(turn or 1) - 1],
    }
    return identity if turn is None else {**identity, TURN_KEY: turn}


def _agent_reply_record(match: _ReaderTranscript, repeat: int, reply: TranscriptReply) -> dict[str, Any]:
    """Return the reply record of one transcript reply: its text, served model, timing, tokens, and transcript."""
    turn = reply.turn if isinstance(match.entry, Conversation) else None
    return {
        **_reply_identity(match.entry, match.condition, repeat, turn),
        _TEXT_KEY: reply.text,
        REPLY_MODEL_KEY: reply.model,
        READER_KIND_KEY: AGENT_READER,
        STARTED_KEY: reply.started.isoformat(),
        SECONDS_KEY: reply.seconds,
        TRANSCRIPT_KEY: str(reply.transcript),
        TRANSCRIPT_HASH_KEY: reply.transcript_hash,
        COST_KEY: _reply_cost_record(reply.tokens),
    }


def _reply_cost_record(tokens: TokenUsage | None) -> dict[str, int | None]:
    """Return the reply's cost fields from its token usage, every field null without usage."""
    if tokens is None:
        return dict.fromkeys(REPLY_COST_KEYS)
    return {**{field.name: getattr(tokens, field.name) for field in fields(tokens)}, SPENT_INPUT_TOKENS_KEY: tokens.spent_input_tokens}


ASK_TIMEOUT_SECONDS = 600
MESSAGES_KEY = "messages"
ROLE_KEY = "role"
USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"
CONDITION_PLACEHOLDER = "{condition}"
TURN_FILE_PREFIX = f"/{TURN_PREFIX}"
COVERAGE_KEYS = ("demands", "sentences")
FIRST_REVISION_REPLIES_FOLDER = f"{FIRST_REVISION}/{REPLIES_FOLDER}"
REPLY_PATTERN = "*.yaml"
ANY_CONDITION = "*"


@dataclass(frozen=True)
class ReaderRun:
    """One run of a command reader: when it started, how long it ran, its exit code, None when it exceeded the timeout, and what it wrote to stdout."""

    started: datetime
    seconds: float
    exit_code: int | None
    stdout: str


RunReader = Callable[[Sequence[str], str, int], ReaderRun]


def revision_ask(
    files: SeriesFolder, revision: str, conditions: Sequence[str], run_reader: RunReader, run_fingerprint: Callable[[Sequence[str]], str]
) -> str:
    """Return an agent reader's launch list, or answer every missing reply serially through a command reader and return an empty text, refusing a failing coverage, an edited condition or definition, a changed reader build, or a failed reader run."""
    guard_series(files, ASK_COMMAND)
    _refuse_collected_revision(files, revision)
    records = SeriesRecords(files)
    reader = records.reader()
    coverage_check(files, revision)
    texts = _verified_condition_texts(files, revision, records, reader)
    asked = _asked_replies(files, revision, records, conditions)
    _refuse_unaffordable_later_ask(files, records, revision, len(asked))
    if isinstance(reader, AgentReader):
        return _launch_list(asked, records)
    _answer_replies(files, revision, records, reader, texts, asked, run_reader, run_fingerprint)
    return ""


def _refuse_unaffordable_later_ask(files: SeriesFolder, records: SeriesRecords, revision: str, ask_reply_count: int) -> None:
    """Refuse an ask of a later revision whose replies, each at r1's mean cost, take the cost so far past the gate's ceiling."""
    budget = None if revision == FIRST_REVISION else _stop_budget(records.complete_gate().budget)
    if budget is None:
        return
    first_replies = [_reply_cost(records.reply(reply.path)) for reply in _expected_reply_set(files, FIRST_REVISION, records)]
    cost_so_far = _cost_so_far(_earlier_outcomes(files, records, revision), budget)
    try:
        refuse_unaffordable_ask(budget, first_replies, cost_so_far, ask_reply_count)
    except BudgetRefusal as unaffordable:
        raise Refusal(str(unaffordable)) from None


def _refuse_collected_revision(files: SeriesFolder, revision: str) -> None:
    """Refuse asking a revision whose replies are judged and collected, so no ask adds a reply to it."""
    if files.holds(f"{revision}/{COLLECTED_FILE}"):
        raise Refusal(f"{revision} already collected: no reply is added")


def _answer_replies(
    files: SeriesFolder,
    revision: str,
    records: SeriesRecords,
    reader: CommandReader,
    texts: Mapping[str, bytes],
    asked: Sequence[ExpectedReply],
    run_reader: RunReader,
    run_fingerprint: Callable[[Sequence[str]], str],
) -> None:
    """Run the command reader on each asked reply in turn, writing each reply as soon as its run succeeds."""
    fingerprint = reader_fingerprint(files, run_fingerprint)
    _refuse_changed_fingerprint(files, records, fingerprint.fingerprint_hash)
    reads = _ask_reads(files, revision, records, reader, texts)
    for reply in sorted(asked, key=_serial_order):
        run = run_reader(_reader_command(files, reader, reply), _reader_stdin(records, reply), ASK_TIMEOUT_SECONDS)
        _refuse_failed_run(reply, run)
        write_record(files, reply.path, _command_reply_record(records.tasks(), reply, run, fingerprint), [*reads, *_state_reads(files)])


def _ask_reads(files: SeriesFolder, revision: str, records: SeriesRecords, reader: Reader, texts: Mapping[str, bytes]) -> list[str]:
    """Return what `revision ask` reads: the reader commands' reads, the demands, the coverage of the revision and of r1, and from r2 on the budget, r1's condition files, and every earlier outcome."""
    coverage = (f"{coverage_revision}/{COVERAGE_FILE}{KEY_SEPARATOR}{key}" for coverage_revision in (revision, FIRST_REVISION) for key in COVERAGE_KEYS)
    reads = [*_reader_reads(revision, records, reader, texts), f"{DEMANDS_RECORD}{KEY_SEPARATOR}demands", *coverage]
    return reads if revision == FIRST_REVISION else [*reads, *_later_revision_reads(files, revision)]


def _later_revision_reads(files: SeriesFolder, revision: str) -> list[str]:
    """Return what an ask of a later revision reads besides an ask of r1: the budget, r1's condition files, and each earlier gated revision's outcome."""
    first_conditions = sorted(path.relative_to(files.root).as_posix() for path in files.root.glob(condition_path(FIRST_REVISION, ANY_CONDITION)))
    earlier = (earlier for earlier in revision_ids(files) if revision_number(earlier) < revision_number(revision))
    return [f"{GATE_RECORD}{KEY_SEPARATOR}{BUDGET_KEY}", *first_conditions, *(outcome_path(other) for other in earlier if files.holds(outcome_path(other)))]


def _state_reads(files: SeriesFolder) -> list[str]:
    """Return the freeze once the series is frozen, else the r1 replies written so far."""
    return [FROZEN_RECORD] if files.holds(FROZEN_RECORD) else _first_revision_reply_paths(files)


def _first_revision_reply_paths(files: SeriesFolder) -> list[str]:
    """Return the series path of every r1 reply file written so far, in path order."""
    replies = (files.root / FIRST_REVISION_REPLIES_FOLDER).rglob(REPLY_PATTERN)
    return sorted(reply.relative_to(files.root).as_posix() for reply in replies)


def _refuse_changed_fingerprint(files: SeriesFolder, records: SeriesRecords, fingerprint_hash: str) -> None:
    """Refuse a fingerprint hash differing from the freeze's once frozen, else from any r1 reply written so far."""
    if not files.holds(FROZEN_RECORD):
        _refuse_other_reader_build(records, _first_revision_reply_paths(files), fingerprint_hash)
    elif records.frozen().get(FINGERPRINT_HASH_KEY) != fingerprint_hash:
        raise Refusal(f"reader fingerprint changed since {FROZEN_RECORD}")


def _serial_order(reply: ExpectedReply) -> tuple[str, int]:
    """Return the sort key that orders replies by path, a conversation's turns in numeric order."""
    return (reply.path.rpartition(TURN_FILE_PREFIX)[0] or reply.path, reply.turn or 0)


def _reader_command(files: SeriesFolder, reader: CommandReader, reply: ExpectedReply) -> list[str]:
    """Return the reader's command with each `{condition}` replaced by the path of the reply's condition file."""
    condition_file = str(files.root / condition_path(reply.revision, reply.condition))
    return [part.replace(CONDITION_PLACEHOLDER, condition_file) for part in reader.command]


def _reader_stdin(records: SeriesRecords, reply: ExpectedReply) -> str:
    """Return the YAML `messages` the reader receives: the turns up to the reply's, with the repeat's earlier replies between them."""
    turns = _turn_messages(_entries_by_id(records.tasks())[reply.task])
    last_turn = reply.turn or 1
    messages: list[dict[str, str]] = []
    for turn in range(1, last_turn + 1):
        messages.append({ROLE_KEY: USER_ROLE, _TEXT_KEY: turns[turn - 1]})
        if turn < last_turn:
            earlier = reply_path(reply.revision, reply.condition, reply.task, reply.repeat, turn)
            messages.append({ROLE_KEY: ASSISTANT_ROLE, _TEXT_KEY: records.reply(earlier)[_TEXT_KEY]})
    return yaml.safe_dump({MESSAGES_KEY: messages}, allow_unicode=True)


def _entries_by_id(tasks: Tasks) -> dict[str, Task | Conversation]:
    """Return every task and conversation by id."""
    return {entry.id: entry for entry in (*tasks.tasks, *tasks.conversations)}


def _refuse_failed_run(reply: ExpectedReply, run: ReaderRun) -> None:
    """Refuse a run with a nonzero exit, no output, or more than the timeout, naming the reply and the cause."""
    if run.exit_code is None or run.seconds > ASK_TIMEOUT_SECONDS:
        cause = f"over {ASK_TIMEOUT_SECONDS} seconds"
    elif run.exit_code != 0:
        cause = f"exit {run.exit_code}"
    elif not run.stdout:
        cause = "empty output"
    else:
        return
    raise Refusal(f"reader failed: {reply.path} ({cause})")


def _command_reply_record(tasks: Tasks, reply: ExpectedReply, run: ReaderRun, fingerprint: Fingerprint) -> dict[str, Any]:
    """Return the reply record of one command reader run: its output, the fingerprint's model and hash, and null token counts."""
    entry = _entries_by_id(tasks)[reply.task]
    return {
        **_reply_identity(entry, reply.condition, reply.repeat, reply.turn),
        _TEXT_KEY: run.stdout,
        REPLY_MODEL_KEY: fingerprint.output[REPLY_MODEL_KEY],
        READER_KIND_KEY: COMMAND_READER,
        STARTED_KEY: run.started.isoformat(),
        SECONDS_KEY: run.seconds,
        FINGERPRINT_HASH_KEY: fingerprint.fingerprint_hash,
        COST_KEY: _reply_cost_record(None),
    }
