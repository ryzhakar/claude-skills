# Claude Code Hooks -- Complete Specification

Research date: 2026-04-13
Sources:
- [Hooks Reference](https://code.claude.com/docs/en/hooks.md) (primary technical reference)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md) (practical guide with examples)
- [Settings](https://code.claude.com/docs/en/settings.md) (configuration scopes and hook settings)
- [Environment Variables](https://code.claude.com/docs/en/env-vars.md) (env vars available in hooks)
- [Claude Code Docs Map](https://code.claude.com/docs/en/claude_code_docs_map.md) (page index)
- [TypeScript SDK Reference](https://code.claude.com/docs/en/typescript.md) (Hook Types section)

---

## 1. All Hook Event Types

Complete list of 26 hook events, with exact string names as used in settings JSON.

Source: [Hooks Reference -- Hook Lifecycle](https://code.claude.com/docs/en/hooks.md)

### Event Cadences

- **Once per session**: `SessionStart`, `SessionEnd`
- **Once per turn**: `UserPromptSubmit`, `Stop`, `StopFailure`
- **On every tool call**: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`
- **Conditional/async**: all others

### Complete Event Table

| Event | When it fires | Can block? |
|:---|:---|:---|
| `SessionStart` | When a session begins or resumes | No |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context | No |
| `UserPromptSubmit` | When user submits a prompt, before Claude processes it | Yes |
| `PreToolUse` | Before a tool call executes | Yes |
| `PermissionRequest` | When a permission dialog appears | Yes |
| `PermissionDenied` | When auto mode classifier denies a tool call | No (but can signal `retry: true`) |
| `PostToolUse` | After a tool call succeeds | No (feedback only) |
| `PostToolUseFailure` | After a tool call fails | No (feedback only) |
| `Notification` | When Claude Code sends a notification | No |
| `SubagentStart` | When a subagent is spawned | No |
| `SubagentStop` | When a subagent finishes | Yes |
| `TaskCreated` | When a task is being created via `TaskCreate` | Yes |
| `TaskCompleted` | When a task is being marked as completed | Yes |
| `Stop` | When Claude finishes responding | Yes |
| `StopFailure` | When the turn ends due to an API error | No (ignored) |
| `TeammateIdle` | When an agent team teammate is about to go idle | Yes |
| `ConfigChange` | When a configuration file changes during a session | Yes (except `policy_settings`) |
| `CwdChanged` | When the working directory changes (e.g., `cd`) | No |
| `FileChanged` | When a watched file changes on disk | No |
| `WorktreeCreate` | When a worktree is being created | Yes (non-zero exit aborts) |
| `WorktreeRemove` | When a worktree is being removed | No |
| `PreCompact` | Before context compaction | No |
| `PostCompact` | After context compaction completes | No |
| `Elicitation` | When an MCP server requests user input | Yes |
| `ElicitationResult` | After user responds to an MCP elicitation | Yes |
| `SessionEnd` | When a session terminates | No |

Source: [Hooks Reference -- Exit Code 2 Behavior Per Event](https://code.claude.com/docs/en/hooks.md)

---

## 2. Matcher Syntax

Source: [Hooks Reference -- Matcher Patterns](https://code.claude.com/docs/en/hooks.md)

### Evaluation Rules

| Matcher value | Evaluated as | Example |
|:---|:---|:---|
| `"*"`, `""`, or omitted | Match all | Fires on every occurrence of the event |
| Only letters, digits, `_`, and `\|` | Exact string, or `\|`-separated list of exact strings | `Bash` matches only Bash; `Edit\|Write` matches either |
| Contains any other character | JavaScript regular expression | `^Notebook` matches tools starting with Notebook; `mcp__memory__.*` matches every tool from `memory` server |

### What Each Event Matches On

| Event(s) | Matcher filters on |
|:---|:---|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | tool name |
| `SessionStart` | how session started: `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | why session ended: `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | notification type: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `SubagentStart`, `SubagentStop` | agent type: `Bash`, `Explore`, `Plan`, or custom agent names |
| `PreCompact`, `PostCompact` | trigger: `manual`, `auto` |
| `ConfigChange` | config source: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `StopFailure` | error type: `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded` | load reason: `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `Elicitation`, `ElicitationResult` | MCP server name |
| `FileChanged` | literal filenames (pipe-separated, NOT regex): `.envrc\|.env` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged` | **no matcher support** -- always fires |

### MCP Tool Naming

MCP tools follow the pattern `mcp__<server>__<tool>`:
- `mcp__memory__create_entities`
- `mcp__github__search_repositories`
- `mcp__memory__.*` matches all tools from the `memory` server
- `mcp__.*__write.*` matches any write tool from any server

### The `if` Field (v2.1.85+)

The `if` field uses permission rule syntax to filter by tool name AND arguments together. It goes beyond `matcher` (which filters at the group level by tool name only).

```json
{
  "type": "command",
  "if": "Bash(git *)",
  "command": ".claude/hooks/check-git-policy.sh"
}
```

Only works on tool events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`. Adding it to any other event prevents the hook from running.

Source: [Hooks Guide -- Filter by tool name and arguments with the `if` field](https://code.claude.com/docs/en/hooks-guide.md)

---

## 3. Hook Types

Source: [Hooks Reference -- Hook Handler Fields](https://code.claude.com/docs/en/hooks.md)

### 3a. Command Hooks (`type: "command"`)

Run a shell command. Script receives JSON input on stdin, communicates results through exit codes and stdout.

| Field | Required | Description |
|:---|:---|:---|
| `type` | yes | `"command"` |
| `command` | yes | Shell command to execute |
| `async` | no | If `true`, runs in background without blocking |
| `shell` | no | `"bash"` (default) or `"powershell"` |
| `if` | no | Permission rule syntax filter |
| `timeout` | no | Seconds before canceling (default: 600) |
| `statusMessage` | no | Custom spinner message |
| `once` | no | If `true`, runs only once per session then is removed (skills only) |

### 3b. HTTP Hooks (`type: "http"`)

POST event data to a URL. Endpoint communicates results through response body.

| Field | Required | Description |
|:---|:---|:---|
| `type` | yes | `"http"` |
| `url` | yes | URL to send POST request to |
| `headers` | no | Key-value pairs. Values support `$VAR_NAME` or `${VAR_NAME}` interpolation |
| `allowedEnvVars` | no | List of env var names allowed for header interpolation |
| `if` | no | Permission rule syntax filter |
| `timeout` | no | Seconds before canceling (default: 600) |
| `statusMessage` | no | Custom spinner message |

HTTP response handling:
- **2xx with empty body**: success (exit 0 equivalent)
- **2xx with plain text body**: success, text added as context
- **2xx with JSON body**: parsed using same JSON output schema as command hooks
- **Non-2xx status**: non-blocking error, execution continues
- **Connection failure/timeout**: non-blocking error, execution continues

To block a tool call via HTTP, return a 2xx response with JSON body containing the appropriate decision fields. HTTP status codes alone cannot block actions.

### 3c. Prompt Hooks (`type: "prompt"`)

Single-turn LLM evaluation. Model returns yes/no decision as JSON.

| Field | Required | Description |
|:---|:---|:---|
| `type` | yes | `"prompt"` |
| `prompt` | yes | Prompt text. Use `$ARGUMENTS` placeholder for hook input JSON |
| `model` | no | Model to use (default: fast model optimized for classification) |
| `timeout` | no | Seconds (default: 30) |
| `statusMessage` | no | Custom spinner message |

Model response format:
```json
{ "ok": true }
```
or
```json
{ "ok": false, "reason": "what remains to be done" }
```

If `"ok": true` (or truthy), action proceeds. If `"ok": false`, action is blocked and `reason` is fed back to Claude. Timeouts and errors are treated as allowing the action to proceed.

### 3d. Agent Hooks (`type: "agent"`)

Spawn a subagent that can use tools (Read, Grep, Glob, Bash, etc.) to verify conditions before returning a decision.

| Field | Required | Description |
|:---|:---|:---|
| `type` | yes | `"agent"` |
| `prompt` | yes | Verification task. Use `$ARGUMENTS` placeholder |
| `model` | no | Model to use (default: fast model) |
| `timeout` | no | Seconds (default: 60). Up to 50 tool-use turns |
| `statusMessage` | no | Custom spinner message |

Same `"ok"` / `"reason"` response format as prompt hooks.

Use prompt hooks when input data alone is enough to decide. Use agent hooks when you need to verify against actual codebase state.

Source: [Hooks Guide -- Prompt-based hooks / Agent-based hooks](https://code.claude.com/docs/en/hooks-guide.md)

---

## 4. Configuration Schema and File Locations

Source: [Hooks Reference -- Configuration](https://code.claude.com/docs/en/hooks.md), [Settings](https://code.claude.com/docs/en/settings.md)

### 4a. Where hooks.json / settings.json Live

| Location | Scope | Shareable |
|:---|:---|:---|
| `~/.claude/settings.json` | All your projects | No, local to your machine |
| `.claude/settings.json` | Single project | Yes, can be committed to repo |
| `.claude/settings.local.json` | Single project | No, gitignored |
| Managed policy settings | Organization-wide | Yes, admin-controlled |
| Plugin `hooks/hooks.json` | When plugin is enabled | Yes, bundled with plugin |
| Skill or agent frontmatter | While component is active | Yes, defined in component file |

### 4b. Complete JSON Schema

Three levels of nesting:
1. Choose a hook event (key name)
2. Add a matcher group to filter when it fires
3. Define one or more hook handlers

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<pattern|empty|omitted>",
        "hooks": [
          {
            "type": "command",
            "command": "script.sh",
            "if": "Bash(git *)",
            "timeout": 30,
            "async": true,
            "shell": "bash",
            "statusMessage": "Checking...",
            "once": true
          },
          {
            "type": "http",
            "url": "http://localhost:8080/hook",
            "headers": { "Authorization": "Bearer $TOKEN" },
            "allowedEnvVars": ["TOKEN"],
            "timeout": 30
          },
          {
            "type": "prompt",
            "prompt": "Is this safe? $ARGUMENTS",
            "model": "claude-haiku-4-6",
            "timeout": 30
          },
          {
            "type": "agent",
            "prompt": "Verify tests pass. $ARGUMENTS",
            "model": "claude-sonnet-4-6",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### 4c. Hook-Related Settings Keys

| Key | Description |
|:---|:---|
| `hooks` | The hooks configuration object itself |
| `disableAllHooks` | If `true`, disables all hooks and custom status line |
| `allowManagedHooksOnly` | (Managed only) Only managed hooks, SDK hooks, and force-enabled plugin hooks load |
| `allowedHttpHookUrls` | URL patterns HTTP hooks may target. `*` wildcard supported. Arrays merge across sources |
| `httpHookAllowedEnvVars` | Env var names HTTP hooks can interpolate into headers. Each hook's effective `allowedEnvVars` is the intersection of its own list and this setting |

Source: [Settings -- Hook configuration](https://code.claude.com/docs/en/settings.md)

### 4d. Settings Precedence

1. **Managed** (highest) -- cannot be overridden
2. **Command line arguments** -- temporary session overrides
3. **Local** -- overrides project and user
4. **Project** -- overrides user
5. **User** (lowest)

`disableAllHooks` respects managed hierarchy: if admin configured hooks through managed policy, user/project `disableAllHooks` cannot disable managed hooks.

### 4e. Plugin hooks.json Schema

Plugin hooks use a slightly different wrapper:

```json
{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 4f. Skill/Agent Frontmatter Hooks

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

For subagents, `Stop` hooks are automatically converted to `SubagentStop`.

---

## 5. Exit Codes

Source: [Hooks Reference -- Exit Code Output](https://code.claude.com/docs/en/hooks.md)

### Exit Code Semantics

| Exit code | Meaning | Behavior |
|:---|:---|:---|
| **0** | Success | Action proceeds. stdout parsed for JSON output. For `UserPromptSubmit` and `SessionStart`, stdout is added as context Claude can see |
| **2** | Blocking error | Action is blocked. stderr text fed back to Claude as error message. stdout/JSON ignored |
| **Any other** | Non-blocking error | Action proceeds. Transcript shows `<hook name> hook error` notice with first line of stderr |

### Exit 2 Behavior Per Event

| Hook event | What happens on exit 2 |
|:---|:---|
| `PreToolUse` | Blocks the tool call |
| `PermissionRequest` | Denies the permission |
| `UserPromptSubmit` | Blocks prompt processing and erases the prompt |
| `Stop` | Prevents Claude from stopping, continues conversation |
| `SubagentStop` | Prevents the subagent from stopping |
| `TeammateIdle` | Prevents teammate from going idle (continues working) |
| `TaskCreated` | Rolls back the task creation |
| `TaskCompleted` | Prevents task from being marked completed |
| `ConfigChange` | Blocks the configuration change (except `policy_settings`) |
| `Elicitation` | Denies the elicitation |
| `ElicitationResult` | Blocks the response (action becomes decline) |
| `WorktreeCreate` | Any non-zero exit causes worktree creation to fail |
| `StopFailure` | Output and exit code are ignored |
| `PostToolUse` | Shows stderr to Claude (tool already ran) |
| `PostToolUseFailure` | Shows stderr to Claude (tool already failed) |
| `PermissionDenied` | Exit code and stderr ignored (use JSON `retry: true` instead) |
| `Notification` | Shows stderr to user only |
| `SubagentStart` | Shows stderr to user only |
| `SessionStart` | Shows stderr to user only |
| `SessionEnd` | Shows stderr to user only |
| `CwdChanged` | Shows stderr to user only |
| `FileChanged` | Shows stderr to user only |
| `PreCompact` | Shows stderr to user only |
| `PostCompact` | Shows stderr to user only |
| `WorktreeRemove` | Failures logged in debug mode only |
| `InstructionsLoaded` | Exit code is ignored |

---

## 6. JSON Output Protocol

Source: [Hooks Reference -- JSON Output](https://code.claude.com/docs/en/hooks.md)

### Universal JSON Fields (all events)

| Field | Default | Description |
|:---|:---|:---|
| `continue` | `true` | If `false`, Claude stops processing entirely. Takes precedence over event-specific decision fields |
| `stopReason` | none | Message shown to user when `continue` is `false`. Not shown to Claude |
| `suppressOutput` | `false` | If `true`, omits stdout from debug log |
| `systemMessage` | none | Warning message shown to user |

Output injected into context (`additionalContext`, `systemMessage`, or plain stdout) is capped at **10,000 characters**. Exceeding this limit saves output to a file and replaces it with a preview and file path.

### Decision Control Summary Table

| Events | Decision pattern | Key fields |
|:---|:---|:---|
| `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop`, `ConfigChange` | Top-level `decision` | `decision: "block"`, `reason` |
| `TeammateIdle`, `TaskCreated`, `TaskCompleted` | Exit code or `continue: false` | Exit 2 blocks with stderr. JSON `{"continue": false, "stopReason": "..."}` stops teammate entirely |
| `PreToolUse` | `hookSpecificOutput` | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| `PermissionRequest` | `hookSpecificOutput` | `decision.behavior` (allow/deny), `decision.updatedInput`, `decision.updatedPermissions`, `decision.message`, `decision.interrupt` |
| `PermissionDenied` | `hookSpecificOutput` | `retry: true` tells model it may retry |
| `WorktreeCreate` | path return | Command hook prints path on stdout; HTTP hook returns `hookSpecificOutput.worktreePath` |
| `Elicitation` | `hookSpecificOutput` | `action` (accept/decline/cancel), `content` (form field values) |
| `ElicitationResult` | `hookSpecificOutput` | `action` (accept/decline/cancel), `content` (override values) |
| `WorktreeRemove`, `Notification`, `SessionEnd`, `PreCompact`, `PostCompact`, `InstructionsLoaded`, `StopFailure`, `CwdChanged`, `FileChanged` | None | No decision control; side effects only |

### PreToolUse JSON Output (detailed)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed",
    "updatedInput": { "command": "npm run lint" },
    "additionalContext": "Current environment: production"
  }
}
```

`permissionDecision` values:
- `"allow"`: skip interactive permission prompt. Deny and ask rules still apply
- `"deny"`: cancel tool call, send reason to Claude
- `"ask"`: show permission prompt to user
- `"defer"`: (non-interactive `-p` mode only) exit process with tool call preserved for later resumption

When multiple PreToolUse hooks return different decisions, precedence is: `deny` > `defer` > `ask` > `allow`.

### PermissionRequest JSON Output (detailed)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": { "command": "npm run lint" },
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

Permission update entry types: `addRules`, `replaceRules`, `removeRules`, `setMode`, `addDirectories`, `removeDirectories`.

Destinations: `session` (in-memory), `localSettings`, `projectSettings`, `userSettings`.

### Stop Hook JSON Output

```json
{
  "decision": "block",
  "reason": "Validation failed, please fix the errors"
}
```

`stop_hook_active` field is `true` on re-entry to prevent infinite loops.

---

## 7. Environment Variables Available Inside Hooks

Source: [Hooks Reference -- Reference Scripts by Path](https://code.claude.com/docs/en/hooks.md), [Environment Variables](https://code.claude.com/docs/en/env-vars.md)

### Variables Available in Hook Commands

| Variable | Description |
|:---|:---|
| `CLAUDE_PROJECT_DIR` | The project root. Wrap in quotes for paths with spaces |
| `CLAUDE_PLUGIN_ROOT` | Plugin's installation directory (for plugin hooks) |
| `CLAUDE_PLUGIN_DATA` | Plugin's persistent data directory (survives updates) |
| `CLAUDE_ENV_FILE` | File path to write `export` statements for persisting env vars. Available in `SessionStart`, `CwdChanged`, and `FileChanged` hooks ONLY |
| `CLAUDE_CODE_REMOTE` | Set to `"true"` in remote web environments; not set in local CLI |

### Variables NOT Available in Hooks

The `CLAUDECODE` environment variable (set to `1` in shell environments spawned by Claude Code) is **NOT** set in hooks or status line commands. It is only set in Bash tool and tmux sessions.

### Hook-Specific Environment Variables

| Variable | Description |
|:---|:---|
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | Timeout for SessionEnd hooks (default: 1500ms) |

### env Key in Settings

The `env` key in settings.json provides environment variables applied to every session:
```json
{ "env": { "FOO": "bar" } }
```

---

## 8. Hook Ordering and Precedence

Source: [Hooks Reference -- Hook Handler Fields](https://code.claude.com/docs/en/hooks.md), [Hooks Guide -- How hooks work](https://code.claude.com/docs/en/hooks-guide.md)

### Execution Model

- **All matching hooks run in parallel**
- **Identical handlers are deduplicated automatically** (command hooks by command string, HTTP hooks by URL)
- Handlers run in the current directory with Claude Code's environment

### Decision Precedence (when multiple hooks match)

For `PreToolUse`:
- **`deny` > `defer` > `ask` > `allow`**

For all blocking events:
- The **most restrictive** answer wins
- A `PreToolUse` hook returning `deny` cancels the tool call regardless of other hooks
- One hook returning `ask` forces the permission prompt even if the rest return `allow`
- Text from `additionalContext` is **kept from every hook** and passed to Claude together

### `updatedInput` Conflict

When multiple PreToolUse hooks return `updatedInput` to rewrite a tool's arguments, **the last one to finish wins**. Since hooks run in parallel, the order is non-deterministic. Avoid having more than one hook modify the same tool's input.

### Source Labels in /hooks Menu

Each hook is labeled with its source:
- `[User]`: from `~/.claude/settings.json`
- `[Project]`: from `.claude/settings.json`
- `[Local]`: from `.claude/settings.local.json`
- `[Plugin]`: from plugin's `hooks/hooks.json`
- `[Session]`: registered in memory for current session
- `[Built-in]`: registered internally by Claude Code

---

## 9. Common Input Fields (stdin JSON)

Source: [Hooks Reference -- Common Input Fields](https://code.claude.com/docs/en/hooks.md)

### Fields Present on Every Event

| Field | Description |
|:---|:---|
| `session_id` | Current session identifier |
| `transcript_path` | Path to conversation JSON |
| `cwd` | Current working directory when hook is invoked |
| `permission_mode` | Current permission mode: `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"`, or `"bypassPermissions"`. Not all events include this |
| `hook_event_name` | Name of the event that fired |

### Additional Fields (subagent context)

| Field | Description |
|:---|:---|
| `agent_id` | Unique identifier for the subagent (present only inside subagent calls) |
| `agent_type` | Agent name (e.g., `"Explore"`, `"security-reviewer"`) |

### Event-Specific Input Fields

**PreToolUse/PostToolUse/PostToolUseFailure**: `tool_name`, `tool_input`, `tool_use_id`, `tool_response` (PostToolUse only), `error` + `is_interrupt` (PostToolUseFailure only)

**UserPromptSubmit**: `prompt`

**SessionStart**: `source` (startup/resume/clear/compact), `model`, optional `agent_type`

**SessionEnd**: `exit_reason` (clear/resume/logout/prompt_input_exit/bypass_permissions_disabled/other)

**Stop**: `stop_reason` (end_turn/max_tokens/tool_use/stop_sequence/model_overloaded), `stop_hook_active`

**StopFailure**: `error_type` (rate_limit/authentication_failed/billing_error/invalid_request/server_error/max_output_tokens/unknown), `error_message`

**SubagentStart**: `agent_id`, `agent_type`

**SubagentStop**: `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message`

**Notification**: `message`, `title`, `notification_type`

**TaskCreated**: `task_id`, `task_subject`, `teammate_name`, `team_name`

**TaskCompleted**: `task_id`, `task_subject`, `completion_notes`, `teammate_name`, `team_name`

**TeammateIdle**: `teammate_name`, `team_name`

**ConfigChange**: `config_source`

**CwdChanged**: `new_cwd`

**FileChanged**: `file_path`, `change_type` (created/modified/deleted)

**InstructionsLoaded**: `file_path`, `memory_type` (User/Project/Local/Managed), `load_reason`, optional `globs`, `trigger_file_path`, `parent_file_path`

**PreCompact/PostCompact**: `trigger` (manual/auto)

**WorktreeCreate**: `worktree_path`, `branch`

**WorktreeRemove**: `worktree_path`

**Elicitation**: `mcp_server_name`, `request_id`, `elicitation_type` (form/confirmation/file_selection), `form_fields`

**ElicitationResult**: `mcp_server_name`, `request_id`, `elicitation_type`, `action`, `content`

**PermissionRequest**: `tool_name`, `tool_input`, `permission_suggestions`

**PermissionDenied**: `tool_name`, `tool_input`, `tool_use_id`, `reason`

### PreToolUse Tool Input Schemas

**Bash**: `command` (string), `description` (string?), `timeout` (number?), `run_in_background` (boolean?)

**Write**: `file_path` (string), `content` (string)

**Edit**: `file_path` (string), `old_string` (string), `new_string` (string), `replace_all` (boolean?)

**Read**: `file_path` (string), `offset` (number?), `limit` (number?)

**Glob**: `pattern` (string), `path` (string?)

**Grep**: `pattern` (string), `path` (string?), `glob` (string?), `output_mode` (string?), `-i` (boolean?), `multiline` (boolean?)

**WebFetch**: `url` (string), `prompt` (string)

**WebSearch**: `query` (string), `allowed_domains` (array?), `blocked_domains` (array?)

**Agent**: `prompt` (string), `description` (string), `subagent_type` (string), `model` (string?)

**AskUserQuestion**: `questions` (array of {question, header, options, multiSelect}), `answers` (object?)

---

## 10. Hooks and Permission Modes

Source: [Hooks Guide -- Hooks and permission modes](https://code.claude.com/docs/en/hooks-guide.md)

### Key Rules

1. **PreToolUse hooks fire BEFORE any permission-mode check.** A hook returning `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`. This lets you enforce policy that users cannot bypass.

2. **The reverse is NOT true.** A hook returning `"allow"` does NOT bypass deny rules from settings. Hooks can tighten restrictions but not loosen them past what permission rules allow.

3. **`PermissionRequest` hooks do NOT fire in non-interactive mode** (`-p`). Use `PreToolUse` hooks for automated permission decisions.

---

## 11. Async Hooks (Background Execution)

Source: [Hooks Reference -- Run hooks in the background](https://code.claude.com/docs/en/hooks.md)

Set `async: true` on a command hook to run it without blocking:

```json
{
  "type": "command",
  "command": "/path/to/lint-check.sh",
  "async": true
}
```

- Async hooks cannot control behavior (exit codes and JSON output are ignored)
- Run for side effects: logging, metrics, notifications
- Timeouts still apply; exceeding timeout kills the command
- `FileChanged`, `CwdChanged`, `InstructionsLoaded`, and `Notification` events run all their hooks **asynchronously by default**, so `async: true` has no effect for these events

---

## 12. Performance Implications

Source: [Hooks Guide -- Limitations](https://code.claude.com/docs/en/hooks-guide.md), [Hooks Reference](https://code.claude.com/docs/en/hooks.md)

### Latency

- **Command hooks ARE blocking** by default. They pause the agentic loop until they complete or timeout
- **Async hooks** (`async: true`) run in background without blocking
- **Default timeout**: 600 seconds (command), 30 seconds (prompt), 60 seconds (agent)
- **SessionEnd hooks timeout**: 1500ms by default (`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`)
- **SessionStart hooks run on every session**, including compaction -- keep these fast

### Execution Model

- All matching hooks for an event run **in parallel** (not sequentially)
- Identical hook commands are **deduplicated automatically**
- Hook output injected into context is **capped at 10,000 characters**

### Events That Are Always Async

`FileChanged`, `CwdChanged`, `InstructionsLoaded`, `Notification` -- these events run all hooks asynchronously by default.

---

## 13. Use Cases: When Hooks Serve Better Than Skill Instructions

Source: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md), [Settings -- costs](https://code.claude.com/docs/en/costs.md)

### Hooks vs Skills

| Aspect | Hooks | Skills |
|:---|:---|:---|
| Execution model | Deterministic, always runs | LLM decides whether to invoke |
| Latency cost | Adds wall-clock time but no tokens | Adds tokens to context window |
| Use case | Guardrails, formatting, notifications, validation | Domain knowledge, instructions, procedures |
| Can block actions | Yes (exit 2 or JSON) | No |
| Can modify tool input | Yes (`updatedInput`) | No |
| Runs without LLM | Yes (command/HTTP types) | No |

### When to Use Hooks

- **Pre-validation / guardrails**: Block dangerous commands, protect files, enforce policies
- **Post-validation**: Auto-format code after edits, run linters, validate output
- **Notifications**: Desktop alerts when Claude needs attention
- **Context injection**: Re-inject critical context after compaction
- **Environment management**: Reload env vars on directory change
- **Auto-approval**: Skip permission prompts for known-safe operations
- **Audit logging**: Track tool usage, config changes, session events
- **CI/CD integration**: POST events to external services

### When to Use Skills Instead

- When the decision requires LLM judgment (use prompt/agent hooks as a middle ground)
- When you need to provide extensive domain knowledge
- When the instructions are conditional on conversation context

---

## 14. Security Considerations

Source: [Hooks Guide -- Hooks and permission modes](https://code.claude.com/docs/en/hooks-guide.md), [Hooks Reference](https://code.claude.com/docs/en/hooks.md)

1. **Hooks can enforce policy that users cannot bypass** -- PreToolUse deny overrides even bypassPermissions mode
2. **Hooks cannot loosen restrictions** -- returning `"allow"` doesn't override deny rules from settings
3. **`allowManagedHooksOnly`** -- admin can restrict to only managed/SDK/force-enabled-plugin hooks
4. **`allowedHttpHookUrls`** -- restrict which URLs HTTP hooks can target
5. **`httpHookAllowedEnvVars`** -- restrict which env vars HTTP hooks can interpolate
6. **`disableAllHooks`** respects managed hierarchy -- users cannot disable managed hooks
7. **Shell profile interference** -- hooks spawn a shell that sources user profile. `echo` statements in `.bashrc`/`.zshrc` can corrupt JSON output. Wrap in `if [[ $- == *i* ]]; then` guard
8. **Policy settings cannot be blocked by ConfigChange hooks**

---

## 15. Troubleshooting Quick Reference

Source: [Hooks Guide -- Limitations and troubleshooting](https://code.claude.com/docs/en/hooks-guide.md)

| Problem | Solution |
|:---|:---|
| Hook not firing | Check `/hooks` menu, verify matcher is case-sensitive match, verify correct event type |
| JSON validation failed | Shell profile printing text on startup. Guard with `if [[ $- == *i* ]]; then` |
| Stop hook runs forever | Check `stop_hook_active` field in input; exit 0 if `true` |
| `/hooks` shows no hooks | Verify JSON validity (no trailing commas/comments), check file location |
| Hook error in output | Test manually: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' \| ./hook.sh` |
| Multiple hooks modifying same input | Last to finish wins (non-deterministic). Avoid multiple hooks modifying same tool's input |

### Debug Technique

Start with `claude --debug-file /tmp/claude.log` or run `/debug` mid-session. The debug log shows which hooks matched, exit codes, stdout, and stderr.

---

## 16. SDK Hook Types (TypeScript)

Source: [TypeScript SDK Reference -- Hook Types](https://code.claude.com/docs/en/typescript.md)

### HookEvent (string literal union)

All event names as TypeScript string literals:
`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `NotificationHookInput`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest`, `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`, `WorktreeCreate`, `WorktreeRemove`

### HookInput Types

| Type | Event | Key fields beyond base |
|:---|:---|:---|
| `PreToolUseHookInput` | PreToolUse | `tool_name`, `tool_input`, `tool_use_id` |
| `PostToolUseHookInput` | PostToolUse | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` |
| `PostToolUseFailureHookInput` | PostToolUseFailure | `tool_name`, `tool_input`, `error`, `is_interrupt` |
| `NotificationHookInput` | Notification | `message`, `title`, `notification_type` |
| `UserPromptSubmitHookInput` | UserPromptSubmit | `prompt` |
| `SessionStartHookInput` | SessionStart | `source`, `model` |
| `SessionEndHookInput` | SessionEnd | `exit_reason` |
| `StopHookInput` | Stop | `stop_reason`, `stop_hook_active` |
| `SubagentStartHookInput` | SubagentStart | `agent_id`, `agent_type` |
| `SubagentStopHookInput` | SubagentStop | `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message` |
| `PreCompactHookInput` | PreCompact | `trigger` |
| `PermissionRequestHookInput` | PermissionRequest | `tool_name`, `tool_input`, `permission_suggestions` |
| `SetupHookInput` | Setup | (base fields only) |
| `TeammateIdleHookInput` | TeammateIdle | `teammate_name`, `team_name` |
| `TaskCompletedHookInput` | TaskCompleted | `task_id`, `task_subject`, `completion_notes` |
| `ConfigChangeHookInput` | ConfigChange | `config_source` |
| `WorktreeCreateHookInput` | WorktreeCreate | `worktree_path`, `branch` |
| `WorktreeRemoveHookInput` | WorktreeRemove | `worktree_path` |

### HookJSONOutput Types

- `SyncHookJSONOutput`: `continue?`, `stopReason?`, `suppressOutput?`, `systemMessage?`, `hookSpecificOutput?`
- `AsyncHookJSONOutput`: `continue?`, `stopReason?`, `suppressOutput?`, `systemMessage?`, `watchPaths?`
- `HookSpecificOutput`: varies by `hookEventName`

---

## 17. Complete Worked Example: PreToolUse Resolution Flow

Source: [Hooks Reference -- How a Hook Resolves](https://code.claude.com/docs/en/hooks.md)

For `Bash "rm -rf /tmp/build"`:

1. **Event fires**: PreToolUse event fires. JSON sent to stdin:
   ```json
   { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" } }
   ```

2. **Matcher checks**: `"Bash"` matches the tool name, so this hook group activates.

3. **If condition checks**: `"Bash(rm *)"` matches because command starts with `rm`, so handler spawns.

4. **Hook handler runs**: Script inspects command, finds `rm -rf`, prints decision to stdout:
   ```json
   {
     "hookSpecificOutput": {
       "hookEventName": "PreToolUse",
       "permissionDecision": "deny",
       "permissionDecisionReason": "Destructive command blocked by hook"
     }
   }
   ```

5. **Claude Code acts on result**: Reads JSON decision, blocks tool call, feeds reason to Claude.
