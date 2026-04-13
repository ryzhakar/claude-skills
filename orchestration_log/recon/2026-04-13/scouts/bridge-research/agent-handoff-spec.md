# Claude Code Subagent Configuration & Dispatch — Precise Specification

Research date: 2026-04-13
Source: Claude Code documentation, SDK docs, GitHub issues, local codebase analysis

---

## 1. Agent Definition Format (Markdown Frontmatter)

### Location
- **Filesystem path**: `.claude/agents/AGENT_NAME.md` (Claude Code CLI and SDK)
- **Plugin path**: `PLUGIN_ROOT/agents/AGENT_NAME.md` (auto-discovered, no explicit registration needed)
- **Programmatic** (SDK only): Pass `agents` dict to `ClaudeAgentOptions` or `query()` options

### Exact YAML Frontmatter Fields

| Field | Type | Required | Default | Semantics |
|-------|------|----------|---------|-----------|
| `name` | string | YES | — | Unique identifier for agent; used in `/agents` list and as `subagent_type` in Agent tool |
| `description` | string (multiline) | YES | — | Natural language instruction for **when Claude should use this agent**. Directly controls automatic delegation. Write specific conditions, not generic descriptions. |
| `model` | string \| `"inherit"` | NO | `"inherit"` | Model override: `"sonnet"`, `"opus"`, `"haiku"`, or `"inherit"` (uses parent session model). Overridable by Agent tool's `model` parameter. |
| `color` | string (CSS hex or name) | NO | — | UI display color for agent in `/agents` list. No functional effect. |
| `tools` | `["Tool1", "Tool2", ...]` | NO | (inherit all) | **Tool allowlist**: agent can only use listed tools. If omitted, agent inherits all tools from parent. Subagents cannot include `"Agent"` (no nesting). |
| `isolation` | `"worktree"` | NO | (none) | Enables git worktree isolation for this agent. |
| `skills` | `[skill1, skill2]` | NO | (none) | List of skill names available to this agent (SDK: Python only). |
| `memory` | `"user"` \| `"project"` \| `"local"` | NO | — | Memory persistence tier (SDK: Python only). |
| `mcpServers` | `(string \| object)[]` | NO | (none) | MCP servers available to agent, by name or inline config (SDK only). |

### Critical Notes
- `description` drives automatic delegation — Claude matches task language to it
- Tool restriction is explicit allowlist; omit = inherit all parent tools
- Agent cannot have tools parent doesn't have
- No version field in agent frontmatter (only `plugin.json` carries versions)
- Filesystem agents load at startup only; changes require session restart

---

## 2. Agent Tool Invocation

### Tool Name
- **Current name**: `"Agent"` (as of Claude Code v2.1.63)
- **Legacy name**: `"Task"` (still accepted in older SDK versions)

### Required Parameters

| Parameter | Type | Required | Semantics |
|-----------|------|----------|-----------|
| `subagent_type` | string | YES | Agent name to invoke (must match agent's `name` field). Built-in `"general-purpose"` always available. |
| `prompt` | string | YES | Complete task instruction. **Only channel** for parent-to-agent context. Agent does not inherit parent conversation history. |
| `description` | string | YES | User-facing summary of what this invocation does. Not used by agent. |

### Optional Parameters

| Parameter | Type | Default | Semantics |
|-----------|------|---------|-----------|
| `model` | `"sonnet"` \| `"opus"` \| `"haiku"` | Agent's `model` field, or parent model if `"inherit"` | Override model for this invocation. Takes precedence over frontmatter. |
| `run_in_background` | boolean | false | If true, agent runs asynchronously; parent receives agentId immediately, gets notified on completion. |
| `isolation` | `"worktree"` | (none) | Creates fresh git worktree for this invocation, overriding frontmatter. |

---

## 3. Orchestration Harness — What the Platform Handles

### Automatic
- Context isolation (each agent starts fresh)
- Tool enforcement via allowlist
- Background execution with completion notification
- Worktree creation/cleanup
- Model override resolution
- CLAUDE.md auto-loaded into every agent's context

### Manual (Orchestrator Responsibility)
- Agent selection and dispatch decisions
- Prompt construction (all context must be inline)
- Parallel coordination and file conflict prevention
- Re-dispatch logic on NEEDS_CONTEXT / BLOCKED / DONE_WITH_CONCERNS
- Result aggregation
- Permission handling (each agent has independent permission context)

### Not Available
- Inter-agent messaging (agents are one-shot)
- Continuation context within agent sessions (CLI)
- Agent-to-agent delegation (Agent tool forbidden in subagents)
- Automatic result summarization
- Background task polling (use notification system instead)

---

## 4. Context Inheritance

| Item | Inherited | Notes |
|------|-----------|-------|
| Agent's system prompt | YES | Defines agent behavior |
| Agent tool's `prompt` parameter | YES | Task-specific instruction |
| `CLAUDE.md` from project | YES | Loaded via settingSources |
| Tool definitions | YES | Subset per agent's `tools` field |
| Parent session history | NO | Fresh context |
| Parent's system prompt | NO | Agent has only its own prompt |
| Skills (unless in `skills` field) | NO | Must be explicitly included |
| Parent's permissions | NO | Independent permission context |

**Critical rule**: The only channel from parent to agent is the Agent tool's `prompt` string.

---

## 5. Worktree Isolation

| Phase | Behavior |
|-------|----------|
| Creation | Git worktree created at `.claude/worktrees/WORKTREE_NAME/` |
| Execution | Agent runs entirely within worktree; modifications isolated |
| Cleanup (no changes) | Worktree and branch deleted automatically |
| Cleanup (changes exist) | User prompted to keep or discard |
| Orphan cleanup | Removed at startup if > `cleanupPeriodDays` and no unpushed commits |

### Provides
- Parallel execution without file conflicts
- Independent filesystem state per agent
- Same git history shared (new branches per worktree)

### Does NOT Provide
- Database, environment variable, network, or process isolation

---

## 6. Tool Restrictions

- `tools` field is an **allowlist**
- Omit field = inherit all parent tools
- Specify array = agent can only use listed tools
- Agent tools always a subset of parent tools
- Agent tool forbidden in subagents (no nesting)

### Common Combinations

| Use Case | Tools |
|----------|-------|
| Read-only analysis | `["Read", "Grep", "Glob"]` |
| Test execution | `["Bash", "Read", "Grep"]` |
| Implementation | `["Read", "Write", "Edit", "Bash", "Grep", "Glob"]` |

---

## 7. Plugin Agent Registration

- Place agent files at `PLUGIN_ROOT/agents/AGENT_NAME.md`
- Auto-discovered at plugin load time — no manifest entry in `plugin.json`
- Available as `subagent_type: "AGENT_NAME"` in Agent tool

### Precedence (if name collision)
1. Programmatically defined (highest)
2. Plugin agents
3. Built-in agents

---

## 8. Agent Status Codes (Convention from dev-discipline agents)

| Status | Meaning |
|--------|---------|
| `DONE` | Complete, tested, committed, self-reviewed |
| `DONE_WITH_CONCERNS` | Complete but concerns exist — must be addressed or escalated |
| `NEEDS_CONTEXT` | Cannot proceed without missing information — resubmit with context |
| `BLOCKED` | Cannot complete — specific blocker documented |

---

## 9. File Conflict Rule

Two parallel agents writing the same file = **silent data loss**. The later agent's version wins with no error, no warning, no conflict marker.

Prevention:
1. List which files each agent will modify before dispatch
2. If any file appears in two agents' write sets, make those agents sequential
3. Include isolation context in each agent's brief

---

## 10. SDK-Specific Features (Not Available in CLI)

| Feature | SDK | CLI |
|---------|-----|-----|
| `AgentDefinition` programmatic config | YES | NO |
| `skills` field | YES (Python) | NO |
| `memory` field | YES (Python) | NO |
| `mcpServers` field | YES | NO |
| Resume with `sessionId` | YES | NO |
| SendMessage continuation | NO (not documented) | NO |
