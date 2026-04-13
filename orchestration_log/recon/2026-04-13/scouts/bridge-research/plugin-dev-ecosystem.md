# Plugin-Dev Ecosystem: Official Documentation Research

Research date: 2026-04-13
Sources: Claude Code docs (code.claude.com), Anthropic Platform docs (platform.claude.com), plugin-dev built-in skills

---

## 1. Skill Authoring Best Practices

### 1.1 Frontmatter Fields and Semantics

Source: https://code.claude.com/docs/en/skills.md

All frontmatter fields are optional. Only `description` is recommended.

| Field | Required | Semantics |
|---|---|---|
| `name` | No | Display name; directory name used if omitted. Lowercase letters, numbers, hyphens only. Max 64 chars. |
| `description` | Recommended | What skill does + when to use it. Claude uses this for auto-invocation. Truncated at 250 chars in listing. Front-load the key use case. |
| `argument-hint` | No | Hint shown during autocomplete (e.g., `[issue-number]`). |
| `disable-model-invocation` | No | `true` prevents Claude from auto-loading. Description removed from context entirely. |
| `user-invocable` | No | `false` hides from `/` menu. Only Claude can invoke. |
| `allowed-tools` | No | Tools permitted without asking while skill is active. Space-separated string or YAML list. Does NOT restrict available tools. |
| `model` | No | Model override while skill is active. |
| `effort` | No | Effort level override: `low`, `medium`, `high`, `max`. |
| `context` | No | Set to `fork` to run in isolated subagent context. |
| `agent` | No | Subagent type when `context: fork` (e.g., `Explore`, `Plan`, custom name). Defaults to `general-purpose`. |
| `hooks` | No | Hooks scoped to skill lifecycle. |
| `paths` | No | Glob patterns limiting auto-activation to matching files. |
| `shell` | No | Shell for inline commands: `bash` (default) or `powershell`. |

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

API-level skill constraints (stricter than Claude Code):
- `name`: Max 64 chars, lowercase letters/numbers/hyphens only, no XML tags, cannot contain "anthropic" or "claude"
- `description`: Max 1024 chars, non-empty, no XML tags

### 1.2 Description Effectiveness

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

**Critical rules:**
- **Always write in third person.** Description is injected into system prompt; inconsistent POV causes discovery problems.
  - Good: "Processes Excel files and generates reports"
  - Bad: "I can help you process Excel files" / "You can use this to process Excel files"
- **Be specific and include key terms.** Include both what it does AND triggers/contexts.
- Description is the primary mechanism for skill selection from potentially 100+ available skills.

Source: https://code.claude.com/docs/en/skills.md

- Descriptions longer than 250 characters are truncated in skill listing.
- All skill names are always included, but descriptions are shortened to fit a character budget.
- Budget scales at 1% of context window, fallback of 8,000 characters.
- Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` to raise the limit.

Source: plugin-dev:skill-development skill

- Use third-person format: "This skill should be used when the user asks to..."
- Include specific trigger phrases users would say (e.g., "create a hook", "add a PreToolUse hook")
- List concrete scenarios

### 1.3 Body Structure and Progressive Disclosure

Source: https://code.claude.com/docs/en/skills.md

- Keep SKILL.md under 500 lines (official tip).
- Move detailed reference material to separate files.
- Skill content enters conversation as a single message and stays for the session.
- After compaction: first 5,000 tokens of each skill re-attached; combined budget of 25,000 tokens across all re-attached skills.

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

- **Default assumption:** Claude is already very smart. Only add context Claude doesn't already have.
- Keep SKILL.md body under 500 lines for optimal performance.
- Three-level loading: metadata always loaded, SKILL.md body on trigger, bundled resources as needed.
- Keep references one level deep from SKILL.md (avoid deeply nested references).
- For reference files longer than 100 lines, include table of contents at top.
- Avoid time-sensitive information.
- Use consistent terminology throughout.
- Avoid offering too many options; provide a default with escape hatch.

Source: plugin-dev:skill-development skill

- Target 1,500-2,000 words for body (ideal), under 3,000 words, hard max 5,000 words.
- Write using imperative/infinitive form (verb-first), not second person.
- Move detailed content to `references/`, working code to `examples/`, utilities to `scripts/`.
- Always reference supporting files in SKILL.md so Claude knows they exist.

### 1.4 String Substitutions

Source: https://code.claude.com/docs/en/skills.md

| Variable | Description |
|---|---|
| `$ARGUMENTS` | All arguments passed to skill |
| `$ARGUMENTS[N]` / `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing SKILL.md |

### 1.5 Skill Content Lifecycle

Source: https://code.claude.com/docs/en/skills.md

- Rendered SKILL.md content enters conversation as a single message and stays for the session.
- Claude Code does NOT re-read the skill file on later turns.
- Auto-compaction carries invoked skills forward: re-attaches first 5,000 tokens of each skill after summary.
- Combined budget of 25,000 tokens for re-attached skills, filled starting from most recently invoked.
- Older skills may be dropped entirely after compaction if many invoked in one session.

---

## 2. Agent Definition Best Practices

### 2.1 Frontmatter Fields

Source: https://code.claude.com/docs/en/sub-agents.md

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique identifier, lowercase letters and hyphens |
| `description` | Yes | When Claude should delegate; drives automatic delegation |
| `tools` | No | Allowlist of tools. Inherits all if omitted |
| `disallowedTools` | No | Denylist. Removed from inherited/specified list |
| `model` | No | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Maximum agentic turns before stop |
| `skills` | No | Skills preloaded at startup (full content injected, not just available) |
| `mcpServers` | No | MCP servers scoped to this agent |
| `hooks` | No | Lifecycle hooks scoped to agent |
| `memory` | No | Persistent memory scope: `user`, `project`, `local` |
| `background` | No | `true` to always run as background task |
| `effort` | No | `low`, `medium`, `high`, `max` |
| `isolation` | No | `worktree` for isolated git worktree |
| `color` | No | Display color: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | No | Auto-submitted as first user turn when agent runs as main session agent |

**Plugin agents additional restrictions:** `hooks`, `mcpServers`, and `permissionMode` are NOT supported for plugin-shipped agents (security).

### 2.2 Description Triggering Behavior

Source: https://code.claude.com/docs/en/sub-agents.md

- Claude uses description to decide when to delegate tasks automatically.
- To encourage proactive delegation, include "use proactively" in description.
- Example: "Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."

### 2.3 System Prompt Best Practices

Source: https://code.claude.com/docs/en/sub-agents.md

- Markdown body becomes the system prompt.
- Subagents receive ONLY this system prompt plus basic environment details (working directory), NOT the full Claude Code system prompt.
- CLAUDE.md files still load through normal message flow.
- Design focused subagents: each should excel at one specific task.
- Write detailed descriptions for delegation accuracy.
- Limit tool access for security and focus.
- Check into version control for team sharing.

### 2.4 Scope and Priority

Source: https://code.claude.com/docs/en/sub-agents.md

Priority (highest first):
1. Managed settings (organization-wide)
2. `--agents` CLI flag (current session)
3. `.claude/agents/` (current project)
4. `~/.claude/agents/` (all projects)
5. Plugin `agents/` directory (lowest)

---

## 3. Plugin Structure

### 3.1 plugin.json Format

Source: https://code.claude.com/docs/en/plugins-reference.md

Manifest is optional. If omitted, Claude Code auto-discovers components in default locations and derives name from directory name.

**Required fields (if manifest present):**

| Field | Type | Description |
|---|---|---|
| `name` | string | Unique identifier, kebab-case, no spaces |

**Metadata fields:**

| Field | Type | Description |
|---|---|---|
| `version` | string | Semantic version (MAJOR.MINOR.PATCH) |
| `description` | string | Brief explanation |
| `author` | object | `{name, email, url}` |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |

**Component path fields:**

| Field | Type | Description |
|---|---|---|
| `skills` | string or array | Custom skill directories (replaces default `skills/`) |
| `commands` | string or array | Custom command files/directories (replaces default `commands/`) |
| `agents` | string or array | Custom agent files (replaces default `agents/`) |
| `hooks` | string, array, or object | Hook config paths or inline config |
| `mcpServers` | string, array, or object | MCP config paths or inline config |
| `outputStyles` | string or array | Custom output style files/directories |
| `lspServers` | string, array, or object | LSP server configurations |
| `userConfig` | object | User-configurable values prompted at enable time |
| `channels` | array | Channel declarations for message injection |

**Path behavior rules:**
- Custom paths for skills/commands/agents/outputStyles REPLACE defaults (not supplement)
- All paths must be relative and start with `./`
- Multiple paths can be specified as arrays
- To keep defaults AND add more: include default in array (e.g., `"skills": ["./skills/", "./extras/"]`)

### 3.2 Standard Directory Layout

Source: https://code.claude.com/docs/en/plugins-reference.md

```
plugin/
  .claude-plugin/plugin.json     # Manifest (optional)
  skills/                        # Skill directories with SKILL.md
  commands/                      # Flat .md skill files
  agents/                        # Subagent .md files
  output-styles/                 # Output style definitions
  hooks/hooks.json               # Hook configuration
  .mcp.json                      # MCP server definitions
  .lsp.json                      # LSP server configurations
  bin/                           # Executables added to PATH
  settings.json                  # Default settings (agent settings only)
  scripts/                       # Hook and utility scripts
```

**Critical:** `.claude-plugin/` contains ONLY `plugin.json`. All component directories must be at plugin root, NOT inside `.claude-plugin/`.

### 3.3 Environment Variables

Source: https://code.claude.com/docs/en/plugins-reference.md

| Variable | Description |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin installation directory. Changes on update. |
| `${CLAUDE_PLUGIN_DATA}` | Persistent directory for plugin state. Survives updates. Auto-created on first reference. |

Both are substituted inline in skill content, agent content, hook commands, and MCP/LSP configs. Also exported as env vars to hook processes and server subprocesses.

### 3.4 Version Management

Source: https://code.claude.com/docs/en/plugins-reference.md

- Follow semantic versioning.
- Claude Code uses version to determine whether to update; unchanged version means cached version used.
- Version can be managed in `plugin.json` or `marketplace.json` (plugin.json takes priority if both set).

### 3.5 Plugin Caching

Source: https://code.claude.com/docs/en/plugins-reference.md

- Marketplace plugins are copied to local cache (`~/.claude/plugins/cache`).
- Installed plugins cannot reference files outside their directory (path traversal blocked).
- Symlinks are preserved in cache and resolve at runtime.

---

## 4. Hook Development

### 4.1 Event Types

Source: https://code.claude.com/docs/en/hooks.md + https://code.claude.com/docs/en/hooks-guide.md

Complete event list (28 events):

| Event | Cadence | Can Block? |
|---|---|---|
| `SessionStart` | Once per session | No |
| `UserPromptSubmit` | Once per turn | Yes |
| `PreToolUse` | Per tool call | Yes |
| `PermissionRequest` | Per permission dialog | Yes |
| `PermissionDenied` | Per auto-mode denial | No (but retry) |
| `PostToolUse` | Per tool call | No (advisory) |
| `PostToolUseFailure` | Per tool failure | No |
| `Notification` | Per notification | No |
| `SubagentStart` | Per subagent spawn | No |
| `SubagentStop` | Per subagent finish | Yes |
| `TaskCreated` | Per task creation | Yes |
| `TaskCompleted` | Per task completion | Yes |
| `Stop` | Once per turn | Yes |
| `StopFailure` | Per API error | No (ignored) |
| `TeammateIdle` | Per idle teammate | Yes |
| `InstructionsLoaded` | Per instruction file | No |
| `ConfigChange` | Per config change | Yes |
| `CwdChanged` | Per directory change | No |
| `FileChanged` | Per watched file | No |
| `WorktreeCreate` | Per worktree creation | Yes |
| `WorktreeRemove` | Per worktree removal | No |
| `PreCompact` | Before compaction | No |
| `PostCompact` | After compaction | No |
| `Elicitation` | Per MCP input request | Yes |
| `ElicitationResult` | Per MCP input response | Yes |
| `SessionEnd` | Once per session | No |

### 4.2 Hook Types

Source: https://code.claude.com/docs/en/hooks-guide.md

| Type | Description |
|---|---|
| `command` | Run shell command. stdin=JSON, stdout/stderr=output, exit code=decision. |
| `http` | POST event JSON to URL. Response body parsed same as command. |
| `prompt` | Single-turn LLM evaluation. Returns `{ok: true/false, reason: "..."}`. |
| `agent` | Multi-turn verification with tool access. Same response format as prompt. |

### 4.3 Configuration Format

Source: https://code.claude.com/docs/en/hooks.md

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<pattern>",
        "hooks": [
          {
            "type": "command",
            "command": "...",
            "if": "Bash(git *)",
            "timeout": 600,
            "statusMessage": "...",
            "once": false,
            "async": false,
            "shell": "bash"
          }
        ]
      }
    ]
  }
}
```

### 4.4 Matcher Syntax

Source: https://code.claude.com/docs/en/hooks.md

| Value | Evaluation |
|---|---|
| `"*"`, `""`, or omitted | Match all |
| Only letters/digits/`_`/`\|` | Exact string or `\|`-separated list |
| Contains other characters | JavaScript regular expression |

### 4.5 Exit Code Semantics

Source: https://code.claude.com/docs/en/hooks.md

- **Exit 0**: Success. Parse stdout for JSON.
- **Exit 2**: Blocking error. stderr fed to Claude as error message.
- **Other**: Non-blocking error for most events.

### 4.6 Hook Locations

Source: https://code.claude.com/docs/en/hooks-guide.md

| Location | Scope |
|---|---|
| `~/.claude/settings.json` | All projects |
| `.claude/settings.json` | Single project (committable) |
| `.claude/settings.local.json` | Single project (gitignored) |
| Managed policy | Organization-wide |
| Plugin `hooks/hooks.json` | When plugin enabled |
| Skill/agent frontmatter | While component active |

---

## 5. Quality Criteria from plugin-dev Built-in Tools

### 5.1 plugin-dev:skill-development Validation Checklist

Source: plugin-dev:skill-development skill (loaded from official plugin-dev plugin)

**Structure:**
- SKILL.md file exists with valid YAML frontmatter
- Frontmatter has `name` and `description` fields
- Markdown body is present and substantial
- Referenced files actually exist

**Description Quality:**
- Uses third person ("This skill should be used when...")
- Includes specific trigger phrases users would say
- Lists concrete scenarios ("create X", "configure Y")
- Not vague or generic

**Content Quality:**
- SKILL.md body uses imperative/infinitive form
- Body is focused and lean (1,500-2,000 words ideal, <5k max)
- Detailed content moved to `references/`
- Examples are complete and working
- Scripts are executable and documented

**Progressive Disclosure:**
- Core concepts in SKILL.md
- Detailed docs in `references/`
- Working code in `examples/`
- Utilities in `scripts/`
- SKILL.md references these resources

**Testing:**
- Skill triggers on expected user queries
- Content is helpful for intended tasks
- No duplicated information across files
- References load when needed

### 5.2 plugin-dev:plugin-structure Validation

Source: plugin-dev:plugin-structure skill

**Manifest validation:**
- `plugin.json` in `.claude-plugin/` directory (not at root)
- Name field present and kebab-case
- Version follows semver
- Paths relative and starting with `./`

**Directory structure:**
- Components at plugin root, NOT inside `.claude-plugin/`
- Only create directories for components actually used
- Kebab-case for all directory and file names

**Path portability:**
- All intra-plugin paths use `${CLAUDE_PLUGIN_ROOT}`
- No hardcoded absolute paths
- No home directory shortcuts
- No relative paths from working directory

### 5.3 Plugin Agent Restrictions

Source: https://code.claude.com/docs/en/plugins-reference.md

Per the plugins-reference:
- Plugin agents support: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `isolation`
- Only valid `isolation` value: `"worktree"`
- Plugin agents do NOT support: `hooks`, `mcpServers`, `permissionMode` (security restriction)

### 5.4 Official Anthropic API Skill Checklist

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

**Core quality:**
- Description is specific and includes key terms
- Description includes both what the skill does and when to use it
- SKILL.md body under 500 lines
- Additional details in separate files (if needed)
- No time-sensitive information (or in "old patterns" section)
- Consistent terminology throughout
- Examples are concrete, not abstract
- File references one level deep
- Progressive disclosure used appropriately
- Workflows have clear steps

**Code and scripts:**
- Scripts solve problems rather than punt to Claude
- Error handling is explicit and helpful
- No "voodoo constants" (all values justified)
- Required packages listed and verified as available
- Scripts have clear documentation
- No Windows-style paths (all forward slashes)
- Validation/verification steps for critical operations
- Feedback loops included for quality-critical tasks

**Testing:**
- At least three evaluations created
- Tested with Haiku, Sonnet, and Opus
- Tested with real usage scenarios
- Team feedback incorporated (if applicable)

---

## 6. CLAUDE.md Best Practices

### 6.1 Official Sizing Guidance

Source: https://code.claude.com/docs/en/memory.md

- **Target under 200 lines per CLAUDE.md file.**
- Longer files consume more context and reduce adherence.
- If growing large, split using `@imports` or `.claude/rules/` files.
- Auto memory MEMORY.md: first 200 lines or 25KB loaded at session start.

Source: https://code.claude.com/docs/en/costs.md

- "Aim to keep CLAUDE.md under 200 lines by including only essentials."
- "Move instructions from CLAUDE.md to skills": specialized instructions should become skills that load on-demand.

### 6.2 What Belongs in CLAUDE.md vs Skills

Source: https://code.claude.com/docs/en/skills.md

- "Create a skill when you keep pasting the same playbook, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact."
- "Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it."

Source: https://code.claude.com/docs/en/memory.md

CLAUDE.md is for:
- Build commands, conventions, project layout
- "Always do X" rules
- Facts Claude should hold in every session

Skills are for:
- Multi-step procedures
- Instructions that only matter for one part of the codebase
- Task-specific workflows

Source: https://code.claude.com/docs/en/costs.md

- "If it contains detailed instructions for specific workflows (like PR reviews or database migrations), those tokens are present even when you're doing unrelated work."

### 6.3 Writing Effective Instructions

Source: https://code.claude.com/docs/en/memory.md

**Specificity:** Write concrete, verifiable instructions.
- Good: "Use 2-space indentation"
- Bad: "Format code properly"
- Good: "Run `npm test` before committing"
- Bad: "Test your changes"
- Good: "API handlers live in `src/api/handlers/`"
- Bad: "Keep files organized"

**Structure:** Use markdown headers and bullets. Organized sections are easier to follow.

**Consistency:** If two rules contradict, Claude may pick arbitrarily. Review periodically.

**Block comments:** HTML comments (`<!-- -->`) are stripped before injection. Use for human-only notes.

### 6.4 How CLAUDE.md Loads

Source: https://code.claude.com/docs/en/memory.md

- Walks UP directory tree from CWD, loading CLAUDE.md + CLAUDE.local.md at each level.
- All discovered files concatenated (not overriding).
- CLAUDE.local.md appended after CLAUDE.md within each directory.
- Subdirectory CLAUDE.md files load on-demand when Claude reads files there.
- Project-root CLAUDE.md survives compaction (re-read from disk).
- Nested CLAUDE.md files NOT re-injected after compaction automatically.

### 6.5 Rules Organization

Source: https://code.claude.com/docs/en/memory.md

- `.claude/rules/` directory for modular topic files.
- Rules without `paths` frontmatter loaded at launch (same priority as `.claude/CLAUDE.md`).
- Path-specific rules use glob patterns in `paths` YAML frontmatter.
- User-level rules in `~/.claude/rules/` apply to every project.
- User rules loaded before project rules (project has higher priority).
- Symlinks supported for sharing rules across projects.

### 6.6 Import Syntax

Source: https://code.claude.com/docs/en/memory.md

- `@path/to/import` syntax for importing files.
- Both relative and absolute paths allowed.
- Relative paths resolve from containing file, not CWD.
- Recursive imports supported, max depth 5.
- First encounter of external imports shows approval dialog.

---

## 7. Cross-Reference: Local Criteria vs Official Documentation

### 7.1 What Official Documentation Requires That Local Criteria Miss

Local criteria file: `/Users/ryzhakar/pp/claude-skills/prompt-engineering/references/evaluation-criteria.md`

**Gaps in local criteria (items official docs emphasize that local criteria omit or underweight):**

1. **Skill description third-person requirement** -- Official docs are emphatic: "Always write in third person." Local AGT-2 checks for trigger keywords but does not enforce person/voice.
   - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

2. **Skill description 250-char truncation** -- Official docs warn that descriptions are truncated at 250 characters in the skill listing. Local criteria have no length constraint on descriptions.
   - Source: code.claude.com/docs/en/skills.md

3. **SKILL.md body under 500 lines** -- Official docs state this as a firm tip. Local AGT-9 checks 500 lines but only mentions "progressive disclosure" as the remedy. The official remedy is specific: move to separate files, keep references one level deep.
   - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

4. **Imperative/infinitive writing form** -- plugin-dev skills are explicit: "Write using verb-first instructions, not second person." Local criteria do not check writing voice/form of skill content.
   - Source: plugin-dev:skill-development built-in skill

5. **Progressive disclosure three-level model** -- Official docs define the metadata/body/resources loading hierarchy. Local criteria treat this as a single line count check (AGT-9), not as a structural pattern.
   - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

6. **Plugin agent security restrictions** -- Plugin agents cannot use `hooks`, `mcpServers`, or `permissionMode`. Local criteria have no awareness of plugin vs project agent distinctions.
   - Source: code.claude.com/docs/en/plugins-reference.md

7. **CLAUDE.md sizing at 200 lines** -- Official docs say "target under 200 lines." Local criteria have no CLAUDE.md sizing criterion.
   - Source: code.claude.com/docs/en/memory.md

8. **Skill content lifecycle (compaction budget)** -- Skills get 5,000 tokens per skill and 25,000 combined budget after compaction. Local criteria have no awareness of compaction behavior.
   - Source: code.claude.com/docs/en/skills.md

9. **`disable-model-invocation` vs `user-invocable`** -- Official docs detail invocation control matrix. Local criteria check only whether description has trigger keywords, not invocation control semantics.
   - Source: code.claude.com/docs/en/skills.md

10. **Agent `name` + `description` both required** -- Official subagent docs mark both as required fields. Local AGT-1 checks name, AGT-2 checks description, but they are SHOULDs; official docs make them MUST for agents.
    - Source: code.claude.com/docs/en/sub-agents.md

11. **Plugin manifest path rules** -- Custom paths for skills/commands/agents REPLACE defaults (not supplement). All paths must start with `./`. Local criteria have no plugin path validation.
    - Source: code.claude.com/docs/en/plugins-reference.md

12. **Hook `if` field for argument-level filtering** -- Official docs describe the `if` field using permission rule syntax for fine-grained hook matching. Not in local criteria.
    - Source: code.claude.com/docs/en/hooks-guide.md

13. **No time-sensitive information in skills** -- Official API best practices explicitly warn against this. Local criteria do not check for temporal references.
    - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

14. **Script error handling: "Solve, don't punt"** -- Official API best practices require scripts to handle errors explicitly rather than failing and leaving Claude to figure it out. Local criteria do not check script quality.
    - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

15. **Consistent terminology** -- Official API docs stress using one term consistently throughout. Local CLR-2 checks for vague terms but not for inconsistent synonyms.
    - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

16. **Evaluation-driven development** -- Official API docs recommend building evaluations BEFORE writing skills, with at least 3 test scenarios. Local criteria have no evaluation requirement.
    - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

17. **Testing across model tiers** -- Official API docs require testing with Haiku, Sonnet, and Opus. Local criteria do not mention multi-model testing.
    - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

18. **Naming conventions (gerund form)** -- API best practices suggest gerund form for skill names (e.g., `processing-pdfs`). No naming convention in local criteria beyond "lowercase hyphenated."
    - Source: platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

19. **`${CLAUDE_PLUGIN_ROOT}` portability requirement** -- All plugin scripts and configs must use this variable, never hardcoded paths. Not in local criteria.
    - Source: code.claude.com/docs/en/plugins-reference.md

20. **Skill `context: fork` requires explicit task instructions** -- Official docs warn: "If your skill contains guidelines without a task, the subagent receives the guidelines but no actionable prompt, and returns without meaningful output." Not in local criteria.
    - Source: code.claude.com/docs/en/skills.md

### 7.2 What Local Criteria Check That Official Docs Do Not Explicitly Mention

1. **Scoring formula with weighted violations** -- Local criteria define `MUST (-3)`, `SHOULD (+1)`, `MUST_NOT (-3)` scoring. Official docs use qualitative language but no scoring model.

2. **Category applicability rules** -- Local criteria define when each category applies (e.g., TOOLS only if tools defined). Official docs do not have applicability gating.

3. **Vague term blacklist (CLR-2)** -- Local criteria reference a term blacklist file. Official docs say "be specific" but do not maintain a blacklist.

4. **Contradiction detection (CLR-3)** -- Local criteria explicitly check for contradictory instructions. Official docs mention consistency but not contradiction scanning.

5. **Data separation / injection defense (DAT-1 through DAT-4)** -- Local criteria have a dedicated category for data/instruction separation with tagged boundaries. Official docs mention this only briefly in security context.

6. **Reasoning category (RSN-1 through RSN-4)** -- Local criteria check for explicit reasoning requests, uncertainty outs, and evidence-before-conclusions patterns. Official docs do not address reasoning patterns for skills.

7. **Output format undefined flexibility (OUT-5)** -- Local criteria flag "structure however you prefer" as a MUST_NOT. Official docs recommend templates but don't explicitly flag open-ended format as an error.

8. **Example diversity and count (EXM-2 through EXM-5)** -- Local criteria specify 3-5 examples for complex tasks, max 10 for simple tasks. Official API docs recommend examples but do not specify counts.

9. **Scope definition as MUST (CON-1)** -- Local criteria require explicit scope ("You handle X, not Y"). Official docs mention focused purpose for agents but do not formalize scope boundaries as a universal requirement.

10. **Tool parameter validation (TLS-1 through TLS-7)** -- Local criteria have detailed checks for tool parameter descriptions, types, and enum values. These apply to API tool definitions, not to Claude Code skills/agents which don't define tool parameters themselves.

---

## 8. Summary of Key Findings

### Critical Official Requirements (MUST-level)

1. Skills: `description` should be present, specific, and front-loaded within 250 chars
2. Skills: SKILL.md body under 500 lines; use progressive disclosure
3. Skills: Write in third person (description) and imperative form (body)
4. Agents: Both `name` and `description` are required fields
5. Agents: Focused single purpose per agent
6. Plugins: `name` is only required manifest field (kebab-case)
7. Plugins: Components at root, not inside `.claude-plugin/`
8. Plugins: All paths relative, starting with `./`
9. Plugins: Use `${CLAUDE_PLUGIN_ROOT}` for all internal paths
10. CLAUDE.md: Target under 200 lines
11. CLAUDE.md: Move procedures/workflows to skills
12. Hooks: Scripts must be executable (`chmod +x`)
13. Hooks: Event names are case-sensitive

### Key Architectural Insights

1. **Skills are on-demand; CLAUDE.md is always-on.** This fundamental cost difference should drive what goes where.
2. **Descriptions are the discovery mechanism.** Poor descriptions mean skills never trigger. Budget is 1% of context window.
3. **Compaction budget is limited.** 25,000 tokens shared across all re-attached skills after compaction. Design skills to be valuable within first 5,000 tokens.
4. **Plugin agents are sandboxed.** No hooks, no MCP servers, no permission mode changes for security.
5. **Hook precedence: deny wins.** When multiple PreToolUse hooks return different decisions, `deny > defer > ask > allow`.
6. **Path replacement, not supplementation.** Custom paths in plugin.json replace defaults for skills/commands/agents/outputStyles.

### Recommended Additions to Local Evaluation Criteria

Priority additions based on gap analysis:

1. **AGT-DESC-VOICE**: MUST -- Skill descriptions use third person
2. **AGT-DESC-LENGTH**: SHOULD -- Skill descriptions front-load key use case within 250 chars
3. **AGT-BODY-VOICE**: SHOULD -- Skill body uses imperative/infinitive form
4. **AGT-BODY-SIZE**: SHOULD -- SKILL.md body 1,500-2,000 words (hard limit 500 lines)
5. **AGT-PROGRESSIVE**: SHOULD -- Skills >500 lines use progressive disclosure to separate files
6. **AGT-AGENT-REQUIRED**: MUST -- Agent definitions have both `name` and `description`
7. **PLG-PATHS**: MUST -- All plugin paths relative, starting with `./`
8. **PLG-ROOT-VAR**: MUST -- Plugin scripts use `${CLAUDE_PLUGIN_ROOT}`, no hardcoded paths
9. **PLG-STRUCTURE**: MUST -- Components at plugin root, not inside `.claude-plugin/`
10. **MEM-SIZE**: SHOULD -- CLAUDE.md under 200 lines
11. **MEM-SCOPE**: SHOULD -- Procedures/workflows in skills, not CLAUDE.md
12. **SKL-NO-TEMPORAL**: SHOULD -- No time-sensitive information in skills
13. **SKL-TERMINOLOGY**: SHOULD -- Consistent terminology throughout skill
14. **SKL-REFERENCES-DEPTH**: SHOULD -- File references one level deep from SKILL.md
