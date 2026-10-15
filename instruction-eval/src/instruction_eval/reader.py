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

from instruction_eval.judge import OATH_SKILL
from instruction_eval.records import AgentReader, CommandReader, Reader, Refusal, SeriesFolder, SeriesRecords, _dump_canonical_yaml, sha256
from instruction_eval.series import guard_series

FRONTMATTER_FENCE = "---\n"
LAUNCH_LIST_DESCRIPTION = "Generated agent; launch from the printed launch list only."
EMPTY_TOOLSET_LINES = ("tools: Read", "disallowedTools: Read")
JUDGE_TOOLSET_LINES = ("tools: Skill, Write",)
FRONTMATTER_BREAKERS = ("\n", "\r", ": ")
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
