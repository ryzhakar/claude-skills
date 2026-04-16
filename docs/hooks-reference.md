# Claude Code Hooks Reference

Sources: official docs (code.claude.com/docs/en/hooks, hooks-guide), GitHub issues (anthropics/claude-code), ~15 real implementations, RustyClawd source analysis. Fetched 2026-04-16. Where docs and reality diverge, reality leads.

---

## Overview

Hooks are shell commands (or HTTP/LLM calls) invoked by Claude Code at named lifecycle events. They receive JSON on stdin and respond via exit code and stdout. Four types exist: **command**, **prompt**, **HTTP**, and **agent**. Only command hooks are viable for any use case where correctness matters. Prompt hooks fail silently on Stop and PreToolUse — the two most important blocking events. See [Prompt Hook Status](#prompt-hook-status) for the full failure analysis.

---

## Command Hook Reference

### Configuration Schema

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/validate.sh",
  "async": false,
  "asyncRewake": false,
  "shell": "bash",
  "if": "Bash(git *)",
  "timeout": 600,
  "statusMessage": "Validating...",
  "once": false
}
```

| Field | Required | Default | Notes |
|---|---|---|---|
| `type` | YES | — | Must be `"command"` |
| `command` | YES | — | Shell command; env vars expanded at spawn time |
| `async` | no | `false` | Background run — Claude does not wait; output ignored |
| `asyncRewake` | no | `false` | Background + wakes Claude on exit 2; implies `async: true` |
| `shell` | no | `"bash"` | `"bash"` or `"powershell"` (Windows) |
| `if` | no | — | Permission rule syntax filter; tool events only; v2.1.85+ |
| `timeout` | no | `600` | Seconds before kill; set lower for hot-path hooks |
| `statusMessage` | no | — | Spinner text while hook runs |
| `once` | no | `false` | Skills only: runs once per session then removed |

### Configuration Locations

| File | Scope | Shareable |
|---|---|---|
| `~/.claude/settings.json` | All projects | No |
| `.claude/settings.json` | Single project | Yes |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| `hooks/hooks.json` (plugin) | Plugin scope | With plugin |
| Skill/agent frontmatter YAML | Component lifetime | With component |

**settings.json format:**
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "..." }] }
    ]
  }
}
```

**Plugin hooks/hooks.json format** — requires outer `hooks` wrapper key:
```json
{
  "description": "Optional explanation",
  "hooks": {
    "PreToolUse": [
      { "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh" }] }
    ]
  }
}
```

**Skill/agent frontmatter YAML:**
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

`Stop` hooks in skill frontmatter auto-convert to `SubagentStop` for subagents.

**Settings keys:**

| Key | Purpose |
|---|---|
| `disableAllHooks` | Disable all hooks (managed hooks survive if admin-set) |
| `allowManagedHooksOnly` | (Managed) Block user/project hooks |
| `allowedHttpHookUrls` | Allowlist for HTTP hook targets |
| `httpHookAllowedEnvVars` | Allowlist for env vars in HTTP headers |

---

### Exit Code Semantics

| Exit code | Stdout parsed? | Effect |
|---|---|---|
| `0` | YES | Normal — stdout parsed for JSON; action proceeds |
| `2` | NO | Blocking — stdout ignored; stderr fed to Claude or user |
| Any other (incl. 1) | NO | Non-blocking error — action proceeds; first stderr line shown |

Exit code 1 is non-blocking. Use exit code 2 to enforce any policy.

### Per-Event Exit 2 Behavior

| Event | Effect of exit 2 |
|---|---|
| `PreToolUse` | Tool call canceled; stderr shown to Claude |
| `PostToolUse` | Error fed to Claude as feedback (tool already ran) |
| `Stop` / `SubagentStop` | Claude continues instead of stopping; stderr is Claude's reason |
| `UserPromptSubmit` | Prompt blocked; stderr displayed to user |
| `ConfigChange` | Config change blocked |
| `WorktreeCreate` | Any non-zero (not just 2) aborts worktree creation |
| `StopFailure` | Exit code ignored entirely |

### Known Exit 2 Bypass Bugs

| Bug | Issue | Status |
|---|---|---|
| Exit 2 does not block Task/Agent tool calls | [#26923](https://github.com/anthropics/claude-code/issues/26923), [#44534](https://github.com/anthropics/claude-code/issues/44534) | Open |
| Exit 2 does not block in headless (`-p`) mode | [#36071](https://github.com/anthropics/claude-code/issues/36071) | Open |
| Exit 2 bypassed when `allowedTools: ["*"]` is set | [#36071](https://github.com/anthropics/claude-code/issues/36071) | Open |
| All hooks silently disabled in subagents (`CLAUDE_CODE_SIMPLE=1`) | [#43612](https://github.com/anthropics/claude-code/issues/43612) | Open |
| Exit 2 display shows "hook error" prefix — looks like malfunction | [#34600](https://github.com/anthropics/claude-code/issues/34600), [#48015](https://github.com/anthropics/claude-code/issues/48015) | Open |

**Root cause of subagent bypass** (confirmed in source, issue #43612): The hook runner contains `if (U6(process.env.CLAUDE_CODE_SIMPLE)) return;`. Subagents run with `CLAUDE_CODE_SIMPLE=1`, causing all hooks to short-circuit before matching or execution. Security-critical PreToolUse hooks are completely bypassed by any subagent. No warning emitted.

**Workaround for Task/Agent blocking:** Block at the Bash level inside the subagent rather than at the Task/Agent PreToolUse level.

---

### Stdin JSON Format

Read all stdin before writing any output.

**Common fields (all events):**
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "hook_event_name": "PreToolUse",
  "agent_id": "(present when inside a subagent)",
  "agent_type": "(present when inside a subagent)"
}
```

**Per-event additions:**

| Event | Extra fields |
|---|---|
| `PreToolUse` | `tool_name`, `tool_input` (object), `tool_use_id` |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response` (object), `tool_use_id` |
| `PostToolUseFailure` | `tool_name`, `tool_input`, `tool_error`, `tool_use_id` |
| `PermissionRequest` | `tool_name`, `tool_input`, `tool_use_id` |
| `PermissionDenied` | `tool_name`, `tool_input`, `tool_use_id` |
| `UserPromptSubmit` | `prompt` (the user's prompt text) |
| `Stop` | `stop_reason`, `stop_hook_active` (boolean) |
| `SubagentStop` | `stop_reason`, `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message` |
| `SessionStart` | `source` (`startup`, `resume`, `clear`, `compact`), `model` |
| `SessionEnd` | `reason` |
| `ConfigChange` | `source`, `file_path` |
| `PreCompact` / `PostCompact` | `trigger` (`manual`, `auto`) |
| `CwdChanged` | new `cwd` |
| `FileChanged` | `file_path` |

**tool_input schema by tool:**

| Tool | Key fields in `tool_input` |
|---|---|
| `Bash` | `command`, `description`, `timeout`, `run_in_background` |
| `Edit` | `file_path`, `old_string`, `new_string` |
| `Write` | `file_path`, `content` |
| `Read` | `file_path` |
| `Agent` / `Task` | `prompt`, `subagent_type` |
| `Glob` | `pattern`, `path` |
| `Grep` | `pattern`, `path`, `glob` |
| `WebFetch` | `url`, `prompt` |

**tool_response.stderr bug** (issue [#44601](https://github.com/anthropics/claude-code/issues/44601)): `tool_response.stderr` is always empty for Bash commands even when the command produced stderr. `tool_response.stdout` is correct. Hooks cannot detect Bash command errors via stderr.

---

### Stdout Parsing Rules

- Stdout parsed only on exit code 0. Exit 2 causes stdout to be completely ignored.
- Stdout must contain only valid JSON. Extraneous text breaks parsing silently.
- For most events, plain non-JSON stdout goes to the debug log only.
- **Exceptions where plain stdout becomes visible context:** `UserPromptSubmit` and `SessionStart`.

**Output size caps:**

| Threshold | Behavior |
|---|---|
| < 50,000 chars | Injected into context (docs say 10K; v2.1.89+ extended to 50K per issue [#41799](https://github.com/anthropics/claude-code/issues/41799)) |
| > 50,000 chars | Written to disk; Claude receives file path + preview |

**Shell profile interference:** Claude Code spawns a non-interactive shell that still sources `~/.bashrc` / `~/.zshrc`. Unconditional `echo` in those files prepends text and breaks JSON parsing silently.

Fix:
```bash
if [[ $- == *i* ]]; then echo "Shell ready"; fi
```

Diagnose: `path/to/hook.sh < sample-input.json | jq .` — if jq fails, profile is contaminating stdout.

**Async hook JSON parsing bug** (issue [#24794](https://github.com/anthropics/claude-code/issues/24794)): Async hooks use a line-by-line parser. Multi-line JSON fails silently. Async hooks must produce single-line compact JSON:
```bash
output_json | jq -c .
```

---

### Stderr Handling

| Exit code | Stderr behavior |
|---|---|
| `0` | Written to debug log only; Claude does not see it |
| `2` | Fed to Claude as error/feedback; blocks action per event |
| Other non-zero | First line shown as `<hook name> hook error`; full stderr to debug log |

Use stdout (JSON) to communicate with Claude on success paths.

---

### Full JSON Output Schema

Return on stdout with exit code 0.

**Universal fields (all events):**

| Field | Type | Default | Behavior |
|---|---|---|---|
| `continue` | boolean | `true` | `false` halts all processing; overrides event-specific decisions |
| `stopReason` | string | none | Shown to user when `continue: false`; Claude does not see it |
| `suppressOutput` | boolean | `false` | Omits stdout from debug log |
| `systemMessage` | string | none | Warning shown to user (unreliable — see bugs below) |

**systemMessage bug** (issues [#40380](https://github.com/anthropics/claude-code/issues/40380), [#41285](https://github.com/anthropics/claude-code/issues/41285), [#47828](https://github.com/anthropics/claude-code/issues/47828)): Silently dropped for PreToolUse/PostToolUse unless `hookSpecificOutput` is also present. Stopped displaying in SessionStart hooks in current versions. Use `additionalContext` inside `hookSpecificOutput` for reliable delivery.

**Top-level `decision` field** — used by: `UserPromptSubmit`, `PostToolUse`, `Stop`, `SubagentStop`, `ConfigChange`, `PreCompact`:
```json
{ "decision": "block", "reason": "explanation shown to Claude" }
```
Omit to allow. `"block"` prevents the action. `reason` goes to Claude, not the user.

**Stop hook note:** Decision values are `"approve"` and `"block"` — NOT `"allow"` and `"block"` (confirmed via debug logs, issue [#34600](https://github.com/anthropics/claude-code/issues/34600)).

### hookSpecificOutput Per Event

Always requires `hookEventName` inside the object.

#### PreToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "explanation",
    "updatedInput": { "command": "modified command" },
    "additionalContext": "context added before tool execution"
  }
}
```

`permissionDecision` values:

| Value | Effect |
|---|---|
| `"allow"` | Skip interactive permission prompt; deny rules in settings still apply |
| `"deny"` | Cancel tool call; `permissionDecisionReason` shown to Claude |
| `"ask"` | Show permission prompt to user |
| `"defer"` | Non-interactive (`-p`) only; exits process with tool call preserved for Agent SDK |

Precedence when multiple hooks conflict: `deny` > `defer` > `ask` > `allow`.

`updatedInput`: modifies tool input before execution. Multiple hooks returning `updatedInput` for the same tool — last to finish wins (non-deterministic). Never have more than one hook modify the same tool's input.

**Known bugs:**

| Bug | Issue |
|---|---|
| `allow` no longer overrides `ask` permission rules (regressed ~v2.1.78-79) | [#36059](https://github.com/anthropics/claude-code/issues/36059) |
| `deny` silently ignored for MCP server tool calls | [#33106](https://github.com/anthropics/claude-code/issues/33106) |
| `deny` silently ignored for Agent/Task tool calls | [#44534](https://github.com/anthropics/claude-code/issues/44534) |
| `ask` silently overrides `deny` rules — security hole | [#39344](https://github.com/anthropics/claude-code/issues/39344) |
| `updatedInput` silently ignored for Agent/Task tool | [#39814](https://github.com/anthropics/claude-code/issues/39814) |

#### PostToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "context for Claude",
    "updatedMCPToolOutput": "replacement MCP tool output (MCP tools only)"
  }
}
```

Cannot retroactively block built-in tool execution. `updatedMCPToolOutput` replaces MCP tool output before Claude sees it; no equivalent exists for built-in tools (issue [#36843](https://github.com/anthropics/claude-code/issues/36843)).

**additionalContext for MCP PostToolUse bug** (issue [#24788](https://github.com/anthropics/claude-code/issues/24788)): `additionalContext` is silently dropped for MCP tool calls. Exit-2 blocking path works. No advisory injection available for MCP tools.

#### SessionStart

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "context added at session start"
  }
}
```

#### SubagentStart

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "context injected into subagent before it starts"
  }
}
```

No blocking decision — context injection only. Plain `{"additionalContext": "..."}` without the wrapper is silently ignored here; wrapper required.

#### Stop / SubagentStop

```json
{
  "decision": "block",
  "reason": "fed to Claude as system message — triggers re-entry",
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "additional context alongside reason"
  }
}
```

`decision: "block"` prevents stopping. `reason` injects a system message Claude acts on.

Every Stop/SubagentStop hook must include a re-entry guard:
```bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then exit 0; fi
```

Without this, a blocking Stop hook creates an infinite loop.

#### PermissionRequest

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ],
      "message": "explanation"
    }
  }
}
```

Does not fire in non-interactive (`-p`) mode. Use PreToolUse for automated decisions in headless contexts.

#### PermissionDenied

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

`retry: true` tells the model it may retry the denied tool call.

#### PostCompact

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostCompact",
    "additionalContext": "context re-injected after compaction"
  }
}
```

**Unresolved:** Issue [#46191](https://github.com/anthropics/claude-code/issues/46191) requests `additionalContext` support for PostCompact, conflicting with docs showing it working. Verify empirically before relying on it.

#### WorktreeCreate

Print worktree path to stdout as plain text.

#### Elicitation / ElicitationResult

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept|decline|cancel",
    "content": { "field_name": "value" }
  }
}
```

---

### Per-Event Behavior Table

| Event | Blocking (exit 2) | additionalContext | Known bugs |
|---|---|---|---|
| `UserPromptSubmit` | YES | YES | VS Code extension broken (#49063); subdirectory launch skips (#48179); Windows stdin broken (#48009); no prompt rewriting (#48554) |
| `Stop` | YES — Claude continues | YES (in hookSpecificOutput) | Display labeled "error" (#34600); re-entry guard required |
| `SubagentStop` | YES | YES | Team agent shutdown bypasses (#44971); not dispatched in VS Code (#39030) |
| `PreToolUse` | YES | YES | Bypass for Task/Agent (#26923, #44534); bypass in `-p` (#36071); bypass with `allowedTools: *` (#36071); `allow` regression (#36059); `deny` ignored for MCP (#33106); `ask` overrides deny (#39344); `updatedInput` ignored for Agent (#39814); all hooks disabled in subagents (#43612) |
| `PostToolUse` | NO (feedback only) | YES | `tool_response.stderr` always empty (#44601); additionalContext dropped for MCP (#24788); does not fire for Skill tool (#43630) |
| `SessionStart` | NO | YES | `systemMessage` regression (#41285, #47828); `compact` matcher additionalContext not injected (#28305); Desktop re-fires on tab switch (#39958); HTTP hooks not supported (#30170) |
| `PostCompact` | NO | Uncertain (#46191) | No context size/content in payload (#44308) |
| `SubagentStart` | NO | YES | `agent_type` may be missing (#44307); silent skip for background agents (#44075); no task prompt in payload (#32016) |
| `StopFailure` | N/A (ignored) | N/A | Output and exit code both ignored |
| `SessionEnd` | — | — | Agent-type hooks silently ignored; command hooks work (#40010) |

---

### Environment Variables

**Available in all command hooks:**

| Variable | Description |
|---|---|
| `CLAUDE_PROJECT_DIR` | Project root directory. Always quote: `"$CLAUDE_PROJECT_DIR"` |
| `CLAUDE_CODE_REMOTE` | `"true"` in remote web environments; unset in local CLI |

**SessionStart, CwdChanged, FileChanged only:**

| Variable | Description |
|---|---|
| `CLAUDE_ENV_FILE` | Write `export VAR=value` lines here; applied before each Bash command for the session |

**Plugin-specific (hook runs from a plugin):**

| Variable | Description |
|---|---|
| `CLAUDE_PLUGIN_ROOT` | Plugin installation directory (but see injection bug below) |
| `CLAUDE_PLUGIN_DATA` | Plugin persistent data directory; survives plugin updates |

**CLAUDE_PLUGIN_ROOT injection bug** (issue [#43380](https://github.com/anthropics/claude-code/issues/43380)): `CLAUDE_PLUGIN_ROOT` is not set at hook execution time. Resolves to empty, producing paths like `/hooks/session-start.mjs`. Affects all plugin hooks using `${CLAUDE_PLUGIN_ROOT}`. Status: **open bug**. Workaround: absolute paths computed at install time, or scripts copied to `CLAUDE_PLUGIN_DATA` during install.

---

### All Hook Events Reference

| Event | When it fires | Matcher filters on | Blocks? |
|---|---|---|---|
| `SessionStart` | Session begins or resumes | `startup`, `resume`, `clear`, `compact` | No |
| `SessionEnd` | Session terminates | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` | No |
| `UserPromptSubmit` | User submits prompt | (none) | Yes |
| `PreToolUse` | Before tool executes | Tool name (PascalCase) | Yes |
| `PermissionRequest` | Permission dialog about to appear | Tool name | Yes |
| `PermissionDenied` | Tool denied by auto-mode | Tool name | No (`retry: true` only) |
| `PostToolUse` | After tool succeeds | Tool name | No |
| `PostToolUseFailure` | After tool fails | Tool name | No |
| `Stop` | Claude finishes responding | (none) | Yes |
| `StopFailure` | Turn ends due to API error | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` | No |
| `SubagentStart` | Subagent spawned | Agent type (`Bash`, `Explore`, `Plan`, custom) | No |
| `SubagentStop` | Subagent finishes | Agent type | Yes |
| `TaskCreated` | Task created via TaskCreate | (none) | Yes |
| `TaskCompleted` | Task marked completed | (none) | Yes |
| `TeammateIdle` | Agent teammate about to idle | (none) | Yes |
| `Notification` | Claude sends notification | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` | No |
| `InstructionsLoaded` | CLAUDE.md or rules file loaded | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` | No |
| `ConfigChange` | Config file changes | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` | Yes |
| `CwdChanged` | Working directory changes | (none) | No |
| `FileChanged` | Watched file changes | Literal filenames (pipe-separated, NOT regex) | No |
| `WorktreeCreate` | Worktree being created | (none) | Yes (any non-zero) |
| `WorktreeRemove` | Worktree being removed | (none) | No |
| `PreCompact` | Before context compaction | `manual`, `auto` | Yes |
| `PostCompact` | After compaction completes | `manual`, `auto` | No |
| `Elicitation` | MCP server requests user input | MCP server name | Yes |
| `ElicitationResult` | User responds to MCP elicitation | MCP server name | Yes |

**Always-async events** (all hooks run async regardless of `async` field): `FileChanged`, `CwdChanged`, `InstructionsLoaded`, `Notification`.

---

### Matcher Patterns

| Pattern | Evaluation |
|---|---|
| `"*"`, `""`, or omitted | Match all |
| Letters, digits, `_`, `\|` only | Exact or pipe-separated: `Bash`, `Edit\|Write` |
| Other characters | JavaScript regex: `^mcp__.*__write` |

Matchers are case-sensitive. Tool names use PascalCase. MCP tools: `mcp__<server>__<tool>`.

### The `if` Field (v2.1.85+)

```json
{ "if": "Bash(git *)" }
{ "if": "Edit(*.ts)" }
{ "if": "WebFetch(domain:example.com)" }
```

- Filters on tool name AND arguments. Permission rule syntax.
- Tool events only: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`.
- Adding `if` to any other event prevents the hook from running.
- Both `matcher` and `if` must match for the process to spawn. They compose.

---

### Execution Model

- All matching hooks for an event run in **parallel**.
- Identical command strings are deduplicated — same string runs once.
- Most restrictive decision wins across parallel hooks.
- `additionalContext` from all hooks is concatenated, not winner-takes-all.
- `updatedInput` conflicts: last to finish wins (non-deterministic). Avoid multiple hooks modifying the same tool's input.
- Hooks do not see each other's output — design each to be independent.

### Async Mechanisms

**`async: true`:** Command runs in background; Claude continues immediately. Output ignored unless `asyncRewake` set. Use for fire-and-forget: logging, notifications, analytics.

**Known async bugs:**
- Stdin missing trailing newline in async mode; `bash read` silently discards data (issue [#30509](https://github.com/anthropics/claude-code/issues/30509)). Workaround: `read -t 1 -r line || true`.
- On macOS: async hooks may receive zero bytes on stdin (issue [#38162](https://github.com/anthropics/claude-code/issues/38162)). Remove `async: true` to restore.

**`asyncRewake: true`:** Implies `async: true`. If command exits with code 2, Claude is woken; stderr (or stdout if stderr empty) shown as system reminder. For long-running background monitors.

---

### additionalContext Accumulation Warning

`additionalContext` is not ephemeral. Each UserPromptSubmit injection adds a `<system-reminder>` block to conversation history; prior blocks are never removed (issue [#40216](https://github.com/anthropics/claude-code/issues/40216)). Across 20+ messages, all prior injections remain visible. Limit to conditional triggers or small content.

---

### Permissions and Hook Interaction

- PreToolUse hooks fire before any permission-mode check.
- `permissionDecision: "deny"` blocks even in `bypassPermissions` mode. Hooks enforce policy users cannot bypass by changing permission mode.
- `"allow"` does not override deny rules from settings. Hooks tighten; they cannot loosen.
- **Regression** (~v2.1.78-79): `allow` no longer overrides `ask` permission rules (issue [#36059](https://github.com/anthropics/claude-code/issues/36059)). Migrate to `PermissionRequest` hook for this use case.

---

### Canonical Script Template

```bash
#!/bin/bash
set -euo pipefail

# Read ALL stdin before writing anything
INPUT=$(cat)

# For Stop/SubagentStop: prevent infinite loops
# [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ] && exit 0

# Parse fields
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Policy check — block with exit 2; reason to stderr
if [[ "$FILE_PATH" == *".env"* ]]; then
  echo "Blocked: .env files are protected" >&2
  exit 2
fi

# Structured output — compact JSON; multi-line breaks async hooks
echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","additionalContext":"Validation passed"}}'
exit 0
```

Rules:
- Read all stdin before writing anything to stdout.
- Stdout must be JSON-only or empty.
- Human-readable messages go to stderr.
- Exit 2 blocks; exit 0 allows.
- Quote all variables.
- Always `--max-time` on network calls; hanging hooks block the entire turn.

---

### Real-World Patterns

**Reading stdin — reliability ranking:**

| Approach | Risk |
|---|---|
| `jq -r '.field'` (pipe directly) | Cleanest; preferred for simple reads |
| `json.load(sys.stdin)` (Python) | Safe for complex parsing |
| `JSON.parse(input)` (Node, buffer all chunks) | Safe |
| `INPUT=$(cat); echo "$INPUT" \| jq -r '.field'` | Shell var corruption on control chars in JSON |
| Env vars (`$CLAUDE_TOOL_NAME`) | Old API; avoid |

Anti-pattern: storing hook JSON in shell vars loses control characters common in command strings. Pipe directly for complex fields:
```bash
# Prefer this for complex command strings
jq -r '.tool_input.command' | your-validator
```

**PostToolUse auto-lint:**
```json
{
  "PostToolUse": [{
    "matcher": "Edit|Write",
    "hooks": [{ "type": "command", "command": "FILE_PATH=$(jq -r '.tool_input.file_path'); if [[ \"$FILE_PATH\" =~ \\.(ts|tsx)$ ]]; then npx eslint --fix \"$FILE_PATH\" >/dev/null || true; fi" }]
  }]
}
```
Key: `|| true` throughout — never blocks.

**PreToolUse security gate:**
```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
if echo "$CMD" | grep -qiE 'rm\s+-[a-zA-Z]*r[a-zA-Z]*f'; then
  echo "BLOCKED: Use trash instead of rm -rf" >&2
  exit 2
fi
exit 0
```

**Stop hook with flag file (avoids lint on every stop):**
```bash
#!/bin/bash
[ ! -e ".claude/hooks/.edited" ] && exit 0
INPUT=$(cat)
[ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ] && exit 0
if ! output=$(npx tsc --noEmit 2>&1); then
  echo "$output" >&2
  exit 2
fi
rm .claude/hooks/.edited
```

**Stop hook task injection:**
```bash
#!/bin/bash
INPUT=$(cat)
[ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ] && exit 0
RESPONSE=$(curl --silent --max-time 4 --fail "$EVENTS_URL") || true
[ -z "$RESPONSE" ] && exit 0
python3 -c "import json,sys; print(json.dumps({'decision':'block','reason':sys.argv[1]}))" "$RESPONSE"
```

Use `python3` for JSON serialization — avoids shell quoting issues with multi-line strings.

**Per-session budget enforcer:**
```bash
#!/bin/bash
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
COUNTER_FILE="/tmp/claude-budgets/$SESSION_ID"
mkdir -p /tmp/claude-budgets
COUNT=$([ -f "$COUNTER_FILE" ] && cat "$COUNTER_FILE" || echo 0)
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"
MAX="${CLAUDE_MAX_TOOL_CALLS:-500}"
if [ "$COUNT" -gt "$MAX" ]; then
  echo "Budget exceeded: $COUNT/$MAX tool calls" >&2
  exit 2
fi
exit 0
```

**Gating on config existence (invisible when unconfigured):**
```bash
CONFIG="${CLAUDE_PROJECT_DIR}/.config.yaml"
[ -f "$CONFIG" ] || exit 0
```

**Template-based context output:**
```bash
export AGENT_TYPE LAST_MESSAGE
envsubst '${AGENT_TYPE} ${LAST_MESSAGE}' < "$SCRIPT_DIR/templates/mandate.txt"
```

**Daemon architecture (complex rule systems):**
```bash
#!/bin/bash
jq -c '{event: "PreToolUse", hook_input: .}' | send_to_daemon_socket
```
Never store hook JSON in shell vars — pipe directly to preserve control characters. If daemon fails, errors to stdout as valid JSON so Claude sees them.

**Async fire-and-forget:**
```bash
curl -s -X POST "$API_URL/status" -H "Content-Type: application/json" \
  -d '{"status":"waiting"}' > /dev/null 2>&1 &
disown $! 2>/dev/null || true
echo '{"continue":true,"suppressOutput":true}'
exit 0
```

---

### Troubleshooting

| Problem | Diagnosis |
|---|---|
| Hook not firing | Check `/hooks` menu. Verify matcher is case-sensitive exact match. Verify event type. |
| JSON parse error | Shell profile printing text. Guard `echo` with `if [[ $- == *i* ]]`. |
| Stop hook loops | Check `stop_hook_active` field. Exit 0 if true. |
| Hook times out | Increase `timeout`. Check for hanging network calls without `--max-time`. |
| Multiple hooks modify same input | Non-deterministic — last to finish wins. Redesign to single hook. |
| Hook in `-p` mode doesn't fire | `PermissionRequest` skips non-interactive mode. Use `PreToolUse` instead. Also: exit-2 blocking bug #36071. |
| Subagent hooks not firing | `CLAUDE_CODE_SIMPLE=1` bypass bug #43612. No known workaround. |

Debug: `claude --debug-file /tmp/claude.log` or `/debug` mid-session. Shows matched hooks, exit codes, stdout, stderr.

---

## Prompt Hook Status

### What They Are

`type: "prompt"` hooks send hook input JSON to a Claude model and expect a yes/no decision in return. Intended as an LLM-based evaluation gate without shell scripting.

Configuration:
```json
{
  "type": "prompt",
  "prompt": "Is this safe? $ARGUMENTS",
  "model": "haiku",
  "timeout": 30
}
```

`$ARGUMENTS` is replaced with the complete JSON input the hook receives (same payload as command hook stdin). Only substitution placeholder available.

### Why They Don't Work

| Bug | Events | Issue(s) | Status |
|---|---|---|---|
| `ok: false` silently ignored — stop proceeds | Stop, SubagentStop | [#32608](https://github.com/anthropics/claude-code/issues/32608), [#41393](https://github.com/anthropics/claude-code/issues/41393), [#20221](https://github.com/anthropics/claude-code/issues/20221) | Open |
| Tool runs without waiting for hook — `ok: false` ignored | PreToolUse | [#33125](https://github.com/anthropics/claude-code/issues/33125) | Closed inactive; no fix |
| Stop hooks fail JSON schema validation always ("JSON validation failed") | Stop | [#41393](https://github.com/anthropics/claude-code/issues/41393) | Open; safety incident documented |
| Exponential payload + infinite retry loop | UserPromptSubmit | [#17249](https://github.com/anthropics/claude-code/issues/17249) | Autoclosed stale; no fix |
| SessionStart crashes ("ToolUseContext required. This is a bug.") | SessionStart | [#48508](https://github.com/anthropics/claude-code/issues/48508), [#45987](https://github.com/anthropics/claude-code/issues/45987) | Open |
| Agent hooks: "Messages are required. This is a bug." | UserPromptSubmit, PreToolUse, PostToolUse, PermissionRequest | [#26474](https://github.com/anthropics/claude-code/issues/26474), [#39184](https://github.com/anthropics/claude-code/issues/39184) | Open |
| Hooks don't fire from subdirectory | UserPromptSubmit | [#48179](https://github.com/anthropics/claude-code/issues/48179) | Duplicate of #36793 |
| Fail on Vertex AI (`output_config`) | All events | [#37746](https://github.com/anthropics/claude-code/issues/37746) | Open; command hooks unaffected |
| Timeout behavior contradicts docs (docs say blocks; likely allows) | All events | CHANGELOG fix + invariants doc | — |
| `additionalContext` accumulates (not ephemeral) | UserPromptSubmit | [#40216](https://github.com/anthropics/claude-code/issues/40216) | Open |
| `additionalContext` not injected in VS Code extension | UserPromptSubmit | [#49063](https://github.com/anthropics/claude-code/issues/49063) | Open |
| Prompt caching cost overrun | All events | [#48240](https://github.com/anthropics/claude-code/issues/48240), [#38165](https://github.com/anthropics/claude-code/issues/38165) | Open |

Debug log from issue #32608 showing silent ignore on Stop:
```
2026-03-09T21:40:02.599Z [DEBUG] Hooks: Prompt hook condition was not met: Do not ask...
2026-03-09T21:40:02.605Z [DEBUG] Stopped caffeinate, allowing sleep
```
The stop proceeded. The hook ran and parsed correctly — the result was discarded.

**Safety incident** (issue #41393): A broken Stop prompt hook left no safe path. A Claude session suggested spawning unbounded `claude -p` background processes as workaround, resulting in $300 unexpected charges, load average above 1000, and machine instability.

No maintainer responses found on any of these issues. All analyses and workarounds are community-sourced. Most were autoclosed by bots.

### Zero Adoption Finding

GitHub code search for `"type": "prompt"` in `.claude/settings.json` and hook config files returned no results. All 13 real-world implementations surveyed use `type: "command"` exclusively. Every implementation uses shell scripts or TypeScript/Python executed as commands — none uses the LLM evaluation mechanism.

### Verdict

`ok: false` is silently ignored on Stop and PreToolUse — the two most important blocking events. `UserPromptSubmit` blocking works but carries the exponential payload bug. Not supported on Vertex AI. Zero adoption in the ecosystem.

Use `type: "command"` for everything where correctness matters. If you need LLM-based evaluation, spawn `claude -p` or call the API directly from a command hook.

---

## HTTP and Agent Hook Types

Neither type was deeply researched. Both exist in the schema; command hooks cover all practical use cases.

### HTTP (`type: "http"`)

POST event data to a URL. Response parsed like command hook stdout on 2xx. Non-2xx or timeout is a non-blocking error.

```json
{
  "type": "http",
  "url": "http://localhost:8080/hook",
  "headers": {"Authorization": "Bearer $TOKEN"},
  "allowedEnvVars": ["TOKEN"],
  "timeout": 30
}
```

Known limitation: HTTP hooks not supported in SessionStart (issue #30170).

### Agent (`type: "agent"`)

Multi-turn subagent with tool access (up to 50 turns). Same `ok`/`reason` response format as prompt hooks.

```json
{
  "type": "agent",
  "prompt": "Verify tests pass. $ARGUMENTS",
  "model": "claude-sonnet-4-6",
  "timeout": 60
}
```

Same class of bugs as prompt hooks for blocking events (issues #26474, #39184: "Messages are required. This is a bug."). Not recommended for blocking use cases.

---

## Design Patterns

### Context Injection (One-Time)

SessionStart and PostCompact hooks inject context that persists until compaction. These run once per session — make them thorough.

```json
{
  "SessionStart": [{ "matcher": "startup|resume", "hooks": [{ "type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/inject-context.sh" }] }],
  "PostCompact": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/re-inject-context.sh" }] }]
}
```

### Gating on Config Existence

Exit 0 silently if config absent. Hook is invisible when unconfigured.

```bash
CONFIG="${CLAUDE_PROJECT_DIR}/.config.yaml"
[ -f "$CONFIG" ] || exit 0
```

### Template Output

Extract prompt text to `hooks/templates/*.txt` for modularity. Use `envsubst` for variable substitution.

```bash
export AGENT_TYPE LAST_MESSAGE
envsubst '${AGENT_TYPE} ${LAST_MESSAGE}' < "$SCRIPT_DIR/templates/mandate.txt"
```

### Agent Lifecycle Chain

Chain SubagentStop hooks to enforce sequential agent dispatch. Each fires when a specific agent type stops and injects a mandate for the next agent.

```
implementer stops → hook injects spec-review mandate
spec-reviewer stops → hook injects quality-review mandate
```

Implemented via `hookSpecificOutput.additionalContext` in SubagentStop, or via `decision: "block"` with `reason` to force the next task.

### Re-Entry Guard

Stop and SubagentStop hooks must guard against infinite loops. Check `stop_hook_active` at the top of every such hook:

```bash
INPUT=$(cat)
[ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ] && exit 0
```

Apply even to non-blocking hooks (sound players, status senders) — belt-and-suspenders.

### Anti-Patterns

| Anti-pattern | Consequence | Fix |
|---|---|---|
| Exit code 1 for blocking | Action proceeds; non-blocking error | Use exit code 2 |
| `systemMessage` as primary channel | Silently dropped for most events | Use `additionalContext` in `hookSpecificOutput` |
| Multiple hooks modifying same tool's `updatedInput` | Non-deterministic — last wins | Single hook per tool modification |
| Unconditional echo in shell profile | Contaminates stdout; breaks JSON parsing | Guard with `if [[ $- == *i* ]]` |
| Multi-line JSON from async hook | Silent parse failure; empty attachment | Pipe through `jq -c .` |
| Network calls without timeout | Hook hangs; blocks entire turn | Always `--max-time` on curl, etc. |
| Storing hook JSON in shell vars | Loses control characters in command strings | Pipe directly to `jq` or Python |
| Stop hook without re-entry guard | Infinite loop | Check `stop_hook_active` at top |
| `type: "prompt"` on blocking events | Silent no-op on Stop and PreToolUse | Use `type: "command"` |
| `${CLAUDE_PLUGIN_ROOT}` in plugin hooks (current builds) | Resolves to empty; broken paths | Absolute paths or scripts in `CLAUDE_PLUGIN_DATA` |
