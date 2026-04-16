# Hook Architecture Reference

Authoritative reference for building Claude Code plugin hooks. Consolidated from official documentation and field testing.

Sources:
- [Hooks Reference](https://code.claude.com/docs/en/hooks.md)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)
- [Settings](https://code.claude.com/docs/en/settings.md)
- [TypeScript SDK -- Hook Types](https://code.claude.com/docs/en/typescript.md)
- Field research: orchestration_log/recon/2026-04-13/scouts/bridge-research/hooks-full-spec.md

---

## Event Catalog

26 events. Grouped by cadence.

### Once Per Session

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `SessionStart` | Session begins or resumes | Source: `startup\|resume\|clear\|compact` | No |
| `SessionEnd` | Session terminates | Reason: `clear\|resume\|logout\|prompt_input_exit\|other` | No |

### Per Turn

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `UserPromptSubmit` | User submits prompt, before processing | None (always fires) | Yes |
| `Stop` | Claude finishes responding | None (always fires) | Yes |
| `StopFailure` | Turn ends due to API error | Error type: `rate_limit\|authentication_failed\|billing_error\|invalid_request\|server_error\|max_output_tokens\|unknown` | No |

### Per Tool Call

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `PreToolUse` | Before tool executes | Tool name: `Bash\|Edit\|Write\|Read\|Glob\|Grep\|Agent\|mcp__server__tool` | Yes |
| `PostToolUse` | After tool succeeds | Tool name | No |
| `PostToolUseFailure` | After tool fails | Tool name | No |
| `PermissionRequest` | Permission dialog appears | Tool name | Yes |
| `PermissionDenied` | Auto mode blocks tool | Tool name | No (`retry: true` only) |

### Per Agent

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `SubagentStart` | Subagent spawns | Agent type (custom name or `Bash\|Explore\|Plan`) | No |
| `SubagentStop` | Subagent finishes | Agent type | Yes |

### Compaction

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `PreCompact` | Before context compaction | Trigger: `manual\|auto` | Yes |
| `PostCompact` | After compaction completes | Trigger: `manual\|auto` | No |

### Tasks

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `TaskCreated` | Task created via TaskCreate | None (always fires) | Yes |
| `TaskCompleted` | Task marked completed | None (always fires) | Yes |
| `TeammateIdle` | Teammate about to go idle | None (always fires) | Yes |

### Configuration and Files

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `ConfigChange` | Config file changes | Source: `user_settings\|project_settings\|local_settings\|policy_settings\|skills` | Yes (except policy) |
| `CwdChanged` | Working directory changes | None (always fires) | No |
| `FileChanged` | Watched file changes | Literal filenames (pipe-separated, NOT regex) | No |
| `InstructionsLoaded` | CLAUDE.md or rules loaded | Reason: `session_start\|nested_traversal\|path_glob_match\|include\|compact` | No |

### Worktree

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `WorktreeCreate` | Worktree created | None (always fires) | Yes (any non-zero) |
| `WorktreeRemove` | Worktree removed | None (always fires) | No |

### MCP

| Event | Fires when | Matcher target | Blocks? |
|---|---|---|---|
| `Elicitation` | MCP server requests input | MCP server name | Yes |
| `ElicitationResult` | User responds to MCP elicitation | MCP server name | Yes |

### Always Async

These events run all hooks asynchronously by default: `FileChanged`, `CwdChanged`, `InstructionsLoaded`, `Notification`.

---

## Hook Types

### Command (`type: "command"`)

Run a shell script. JSON on stdin, exit code + stdout for output.

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/my-hook.sh",
  "timeout": 30,
  "async": false,
  "shell": "bash",
  "if": "Bash(git *)",
  "statusMessage": "Checking...",
  "once": true
}
```

| Field | Required | Default | Notes |
|---|---|---|---|
| `command` | Yes | -- | Shell command. `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths |
| `timeout` | No | 600s | Seconds before kill |
| `async` | No | false | Background execution (exit codes ignored) |
| `shell` | No | bash | `bash` or `powershell` |
| `if` | No | -- | Permission rule syntax filter (tool events only) |
| `statusMessage` | No | -- | Custom spinner text |
| `once` | No | false | Run once per session then remove (skills only) |

### HTTP (`type: "http"`)

POST event data to a URL.

```json
{
  "type": "http",
  "url": "http://localhost:8080/hook",
  "headers": {"Authorization": "Bearer $TOKEN"},
  "allowedEnvVars": ["TOKEN"],
  "timeout": 30
}
```

2xx with JSON body = parsed like command hook output. Non-2xx/timeout = non-blocking error.

### Prompt (`type: "prompt"`)

Single-turn LLM yes/no decision. Fast, no tool access.

```json
{
  "type": "prompt",
  "prompt": "Is this safe? $ARGUMENTS",
  "model": "claude-haiku-4-5",
  "timeout": 30
}
```

Returns `{"ok": true}` or `{"ok": false, "reason": "..."}`. Timeouts/errors default to allow.

### Agent (`type: "agent"`)

Multi-turn subagent with tool access (up to 50 turns). Slower, can inspect codebase.

```json
{
  "type": "agent",
  "prompt": "Verify tests pass. $ARGUMENTS",
  "model": "claude-sonnet-4-6",
  "timeout": 60
}
```

Same `ok`/`reason` response format as prompt hooks.

---

## Matcher Patterns

| Pattern | Evaluation | Example |
|---|---|---|
| `"*"`, `""`, or omitted | Match all | Every occurrence |
| Letters, digits, `_`, `\|` only | Exact or pipe-separated list | `Bash`, `Edit\|Write` |
| Other characters | JavaScript regex | `^mcp__.*__write`, `^Notebook` |

Matchers are **case-sensitive**. Tool names use PascalCase (`Bash`, `Edit`, `Write`). MCP tools: `mcp__<server>__<tool>`.

### The `if` Field (v2.1.85+)

Filters by tool name AND arguments. Permission rule syntax. Tool events only.

```json
{"if": "Bash(git *)"}
{"if": "Edit(*.ts)"}
{"if": "WebFetch(domain:example.com)"}
```

Adding `if` to non-tool events **prevents the hook from running**.

---

## Exit Codes

| Code | Meaning | Behavior |
|---|---|---|
| **0** | Success | Action proceeds. Parse stdout for JSON |
| **2** | Block | Action blocked. stderr fed to Claude |
| **Other** | Non-blocking error | Action proceeds. First line of stderr shown |

### What Exit 2 Does Per Event

**Blocks action:** `PreToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `ConfigChange`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `Elicitation`, `ElicitationResult`, `WorktreeCreate`.

**Cannot block (already happened or informational):** `PostToolUse`, `PostToolUseFailure`, `SessionStart`, `SessionEnd`, `SubagentStart`, `PostCompact`, `Notification`, `CwdChanged`, `FileChanged`, `InstructionsLoaded`, `WorktreeRemove`, `StopFailure`.

---

## JSON Protocol

### Universal Input (All Events)

```json
{
  "session_id": "abc123",
  "cwd": "/project/root",
  "hook_event_name": "PreToolUse",
  "hook_source_file": "/path/to/settings.json"
}
```

### Universal Output (All Events)

```json
{
  "continue": false,
  "stopReason": "Build failed",
  "suppressOutput": true,
  "systemMessage": "Warning shown to user"
}

```

Output injected into context is capped at **10,000 characters**. Exceeding saves to file with preview.

### Event-Specific Input Fields

**PreToolUse/PostToolUse/PostToolUseFailure:** `tool_name`, `tool_input`, `tool_use_id`, `tool_response` (Post only), `error` + `is_interrupt` (Failure only)

**Stop:** `stop_reason` (end_turn/max_tokens/tool_use/stop_sequence), `stop_hook_active` (true on re-entry)

**SubagentStop:** `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message`

**SubagentStart:** `agent_id`, `agent_type`

**SessionStart:** `source` (startup/resume/clear/compact), `model`

**SessionEnd:** `exit_reason` (clear/resume/logout/prompt_input_exit/other)

**UserPromptSubmit:** `prompt`

**ConfigChange:** `config_source`

**FileChanged:** `file_path`, `change_type` (created/modified/deleted)

**CwdChanged:** `new_cwd`

**TaskCreated:** `task_id`, `task_subject`, `teammate_name`, `team_name`

**TaskCompleted:** `task_id`, `task_subject`, `completion_notes`, `teammate_name`, `team_name`

**WorktreeCreate:** `worktree_path`, `branch`

**WorktreeRemove:** `worktree_path`

**PreCompact/PostCompact:** `trigger` (manual/auto)

**InstructionsLoaded:** `file_path`, `memory_type`, `load_reason`, optional `globs`, `trigger_file_path`, `parent_file_path`

**Elicitation:** `mcp_server_name`, `request_id`, `elicitation_type`, `form_fields`

**ElicitationResult:** `mcp_server_name`, `request_id`, `elicitation_type`, `action`, `content`

**PermissionRequest:** `tool_name`, `tool_input`, `permission_suggestions`

**PermissionDenied:** `tool_name`, `tool_input`, `tool_use_id`, `reason`

### Decision Patterns by Event

| Events | Pattern | Key fields |
|---|---|---|
| `UserPromptSubmit`, `PostToolUse`, `Stop`, `SubagentStop`, `ConfigChange` | Top-level decision | `decision: "block"`, `reason` |
| `PreToolUse` | hookSpecificOutput | `permissionDecision` (allow/deny/ask/defer), `updatedInput`, `additionalContext` |
| `PermissionRequest` | hookSpecificOutput | `decision.behavior` (allow/deny), `decision.updatedInput`, `decision.updatedPermissions` |
| `PermissionDenied` | hookSpecificOutput | `retry: true` |
| Prompt/Agent hooks | ok/reason | `ok: true` or `ok: false, reason: "..."` |

### PreToolUse Output (Full)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked",
    "updatedInput": {"command": "npm run lint"},
    "additionalContext": "Current environment: production"
  }
}
```

Decision precedence when multiple hooks match: **deny > defer > ask > allow**.

### Stop/SubagentStop Output

```json
{
  "decision": "block",
  "reason": "Validation failed, please fix errors"
}
```

Guard re-entry with `stop_hook_active`:

```bash
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0
fi
```

---

## Configuration Locations

| Location | Scope | Precedence | Shareable |
|---|---|---|---|
| Managed policy | Org-wide | 1 (highest) | Yes |
| Plugin `hooks/hooks.json` | When plugin enabled | 2 | Yes |
| `.claude/settings.local.json` | Project | 3 | No |
| `.claude/settings.json` | Project | 4 | Yes |
| `~/.claude/settings.json` | User | 5 (lowest) | No |
| Skill/agent frontmatter | While active | Varies | Yes |

### Plugin hooks.json Format

```json
{
  "description": "What these hooks do",
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "implementer",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/my-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Frontmatter Hooks

```yaml
---
name: my-skill
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
---
```

For subagents, `Stop` hooks in frontmatter auto-convert to `SubagentStop`.

### Settings Keys

| Key | Purpose |
|---|---|
| `disableAllHooks` | Disable all hooks (managed hooks survive if admin set) |
| `allowManagedHooksOnly` | (Managed) Block user/project hooks |
| `allowedHttpHookUrls` | Allowlist for HTTP hook targets |
| `httpHookAllowedEnvVars` | Allowlist for env vars in HTTP headers |

---

## Environment Variables

| Variable | Available in | Description |
|---|---|---|
| `CLAUDE_PROJECT_DIR` | All hooks | Project root |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin hooks | Plugin install directory |
| `${CLAUDE_PLUGIN_DATA}` | Plugin hooks | Plugin persistent data directory |
| `CLAUDE_ENV_FILE` | SessionStart, CwdChanged, FileChanged | Write `export` statements here to persist env vars |
| `CLAUDE_CODE_REMOTE` | All | `"true"` in remote web environments |

Shell profile is sourced for environment. Unconditional `echo` in `.bashrc`/`.zshrc` corrupts JSON output — guard with `if [[ $- == *i* ]]; then`.

---

## Execution Model

- All matching hooks run **in parallel**
- Identical commands are **deduplicated** (exact string match)
- Most restrictive decision wins across parallel hooks
- `updatedInput` conflict: last to finish wins (non-deterministic) — avoid multiple hooks modifying same tool's input
- `additionalContext` from all hooks is concatenated

---

## Hook Design Patterns

### Context Injection (One-Time)

SessionStart and PostCompact hooks inject context that persists until compaction. Keep these thorough — they run once, not per-call.

```json
{
  "SessionStart": [{
    "matcher": "startup|resume",
    "hooks": [{"type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/inject-context.sh"}]
  }],
  "PostCompact": [{
    "matcher": "*",
    "hooks": [{"type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/re-inject-context.sh"}]
  }]
}
```

### Gating on Config Existence

Invisible when unconfigured. Check for config file, exit 0 silently if absent.

```bash
CONFIG="${CLAUDE_PROJECT_DIR}/.config.yaml"
[ -f "$CONFIG" ] || exit 0
```

### Template-Based Output

Extract prompt text into template files for modularity. Use `envsubst` for variable substitution.

```bash
export AGENT_TYPE LAST_MESSAGE
envsubst '${AGENT_TYPE} ${LAST_MESSAGE}' < "$SCRIPT_DIR/templates/mandate.txt"
```

### Agent Lifecycle Chain

Chain SubagentStop hooks to enforce sequential agent dispatch. Each hook fires when a specific agent type stops and injects a mandate for the next agent.

```
implementer stops → hook injects spec-review mandate
spec-reviewer stops → hook injects quality-review mandate
```

### Re-Entry Guard

Stop and SubagentStop hooks can cause infinite loops. Guard with `stop_hook_active`.

```bash
INPUT=$(cat)
ACTIVE=$(echo "$INPUT" | python3 -c 'import sys,json; print(json.loads(sys.stdin.read()).get("stop_hook_active", False))' 2>/dev/null)
[ "$ACTIVE" = "True" ] && exit 0
```

---

## Troubleshooting

| Problem | Diagnosis |
|---|---|
| Hook not firing | Check `/hooks` menu. Verify matcher is case-sensitive exact match. Verify event type. |
| JSON parse error | Shell profile printing text. Guard `echo` with `if [[ $- == *i* ]]`. |
| Stop hook loops | Check `stop_hook_active` field. Exit 0 if true. |
| Hook times out | Increase `timeout`. Check script for hangs. Verify `jq`/`python3` installed. |
| Multiple hooks modify same input | Non-deterministic — last to finish wins. Avoid. |
| Hook in `-p` mode doesn't fire | `PermissionRequest` hooks skip non-interactive mode. Use `PreToolUse` instead. |

Debug: `claude --debug-file /tmp/claude.log` or `/debug` mid-session. Shows matched hooks, exit codes, stdout, stderr.

---

## PreToolUse Tool Input Schemas

Quick reference for writing PreToolUse hooks that inspect tool arguments.

| Tool | Key fields |
|---|---|
| `Bash` | `command` (string), `description` (string?), `timeout` (number?) |
| `Write` | `file_path` (string), `content` (string) |
| `Edit` | `file_path` (string), `old_string` (string), `new_string` (string) |
| `Read` | `file_path` (string), `offset` (number?), `limit` (number?) |
| `Glob` | `pattern` (string), `path` (string?) |
| `Grep` | `pattern` (string), `path` (string?), `glob` (string?) |
| `WebFetch` | `url` (string), `prompt` (string) |
| `Agent` | `prompt` (string), `description` (string), `subagent_type` (string) |

---

## Hooks vs Skills

| Aspect | Hooks | Skills |
|---|---|---|
| Execution | Deterministic, always runs | LLM decides whether to invoke |
| Cost | Wall-clock time, no tokens | Tokens in context window |
| Can block | Yes (exit 2 or JSON) | No |
| Can modify input | Yes (`updatedInput`) | No |
| Runs without LLM | Yes (command/HTTP) | No |
| Use for | Guardrails, formatting, validation, lifecycle enforcement | Domain knowledge, procedures, instructions |
