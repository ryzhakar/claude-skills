# Claude Code Slash Commands -- Complete Specification

Research date: 2026-04-13
Sources: Official Claude Code documentation at code.claude.com/docs/en/

---

## 1. Terminology Clarification: Commands vs Skills (The Merger)

**Critical finding:** Custom commands have been merged into skills. The documentation states explicitly:

> "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to control whether you or Claude invokes them, and the ability for Claude to load them automatically when relevant."

**Source:** https://code.claude.com/docs/en/skills.md

There are now three categories of things invokable via `/`:

| Category | Mechanism | Who codes it | Model-invocable? |
|:--|:--|:--|:--|
| **Built-in commands** | Hard-coded CLI logic | Anthropic | No |
| **Bundled skills** | Prompt-based, shipped with CLI | Anthropic | Yes (Claude can invoke automatically) |
| **Custom skills/commands** | User-authored `.md` files | User/plugin | Configurable via frontmatter |

**Source:** https://code.claude.com/docs/en/commands.md

---

## 2. Command/Skill Definition Format -- Complete Frontmatter Reference

Skills are defined as `SKILL.md` files with YAML frontmatter. Commands in `.claude/commands/` are flat `.md` files that support the same frontmatter.

### All Frontmatter Fields

| Field | Required | Type | Default | Description |
|:--|:--|:--|:--|:--|
| `name` | No | string | Directory name | Display name. Lowercase letters, numbers, hyphens only. Max 64 chars. |
| `description` | Recommended | string | First paragraph of body | What the skill does and when to use it. Claude uses this for auto-invocation decisions. Truncated at 250 chars in listings. |
| `argument-hint` | No | string | (none) | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | No | boolean | `false` | When `true`, only the user can invoke (prevents Claude auto-loading). |
| `user-invocable` | No | boolean | `true` | When `false`, hidden from `/` menu. Only Claude can invoke. |
| `allowed-tools` | No | string or YAML list | (none) | Tools Claude can use without permission prompts when skill is active. Space-separated or YAML list. Does NOT restrict tools -- only grants additional permissions. |
| `model` | No | string | (session default) | Model to use when skill is active. |
| `effort` | No | string | (session default) | Effort level override. Options: `low`, `medium`, `high`, `max` (Opus 4.6 only). |
| `context` | No | string | (inline) | Set to `fork` to run in a forked subagent context. |
| `agent` | No | string | `general-purpose` | Which subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/`. |
| `hooks` | No | object | (none) | Hooks scoped to skill lifecycle. |
| `paths` | No | string or YAML list | (none) | Glob patterns limiting when skill auto-activates. Comma-separated or YAML list. |
| `shell` | No | string | `bash` | Shell for `!`command`` and ````!` blocks. Accepts `bash` or `powershell`. PowerShell requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. |

**Source:** https://code.claude.com/docs/en/skills.md -- "Frontmatter reference" section

---

## 3. File Locations -- Where Commands/Skills Live

### Skill Locations (priority order, highest first)

| Location | Path | Applies to |
|:--|:--|:--|
| Enterprise | Managed settings (server-managed) | All users in organization |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All user's projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

### Legacy Command Locations (still work, same frontmatter)

| Location | Path |
|:--|:--|
| Personal | `~/.claude/commands/<name>.md` |
| Project | `.claude/commands/<name>.md` |
| Plugin | `<plugin>/commands/<name>.md` |

### Precedence Rules

- When skills share the same name across levels: **enterprise > personal > project**.
- Plugin skills use `plugin-name:skill-name` namespace, so they cannot conflict.
- If a skill and a command share the same name, **the skill takes precedence**.

### Automatic Discovery from Nested Directories

Claude Code discovers skills from nested `.claude/skills/` directories. If editing files in `packages/frontend/`, it also looks in `packages/frontend/.claude/skills/`. This supports monorepos.

### Skills from `--add-dir` Directories

Skills are an exception to the `--add-dir` rule: `.claude/skills/` within an added directory IS loaded automatically and picked up by live change detection. Other `.claude/` configuration (subagents, commands, output styles) is NOT loaded from additional directories.

**Source:** https://code.claude.com/docs/en/skills.md -- "Where skills live" and "Skills from additional directories"

---

## 4. Argument Syntax -- Complete Reference

### Available String Substitutions

| Variable | Description |
|:--|:--|
| `$ARGUMENTS` | All arguments passed when invoking. If not present in content, appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | Access specific argument by 0-based index. E.g., `$ARGUMENTS[0]` for first. |
| `$N` | Shorthand for `$ARGUMENTS[N]`. E.g., `$0` for first, `$1` for second. |
| `${CLAUDE_SESSION_ID}` | Current session ID. Useful for logging, session-specific files. |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's `SKILL.md`. For plugin skills, the skill's subdirectory within the plugin (not plugin root). |

### Argument Parsing Rules

- Indexed arguments use **shell-style quoting**: wrap multi-word values in quotes to pass as single argument.
- Example: `/my-skill "hello world" second` makes `$0` = `hello world`, `$1` = `second`.
- `$ARGUMENTS` always expands to the full argument string as typed.
- If skill content lacks `$ARGUMENTS`, Claude Code auto-appends `ARGUMENTS: <value>` to the end.

### Plugin-specific Variables

| Variable | Description |
|:--|:--|
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to plugin's installation directory. Changes on update. |
| `${CLAUDE_PLUGIN_DATA}` | Persistent directory for plugin state, survives updates. Auto-created on first reference. |

**Source:** https://code.claude.com/docs/en/skills.md -- "Available string substitutions"

---

## 5. Command vs Skill -- Exact Behavioral Difference

### Built-in Commands vs Skills

| Aspect | Built-in Command | Skill (bundled or custom) |
|:--|:--|:--|
| Implementation | Hard-coded in CLI binary | Prompt-based `.md` file |
| Invocation | User only (type `/name`) | User AND/OR Claude (configurable) |
| Model-invocable | No | Yes (by default; configurable) |
| Arguments | Command-specific | `$ARGUMENTS` substitution |
| Context loading | Immediate execution | Description in context; body loads on invocation |
| Compaction | N/A | Re-attached after compaction (first 5,000 tokens, combined budget 25,000 tokens) |
| Available via Skill tool | No (`/compact`, `/init` etc. not available through Skill tool) | Yes |

### Invocation Control Matrix

| Frontmatter | User can invoke | Claude can invoke | Context behavior |
|:--|:--|:--|:--|
| (default) | Yes | Yes | Description always in context; full body loads on invocation |
| `disable-model-invocation: true` | Yes | No | Description NOT in context; full body loads when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full body loads when Claude invokes |

**Source:** https://code.claude.com/docs/en/skills.md -- "Control who invokes a skill"

---

## 6. Command/Skill Body -- What Goes in the Markdown

### Content Types

**Reference content** -- knowledge Claude applies to work (conventions, patterns, style guides). Runs inline alongside conversation context.

**Task content** -- step-by-step instructions for specific actions (deployments, commits). Often paired with `disable-model-invocation: true`.

### Dynamic Context Injection (Shell Preprocessing)

The `` !`<command>` `` syntax runs shell commands BEFORE the skill content is sent to Claude. Output replaces the placeholder.

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
---

## Pull request context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

For multi-line commands, use fenced code block with ` ```! `:

````markdown
```!
node --version
npm --version
git status --short
```
````

This is preprocessing -- Claude only sees the final rendered output.

**Disabling shell execution:** Set `"disableSkillShellExecution": true` in settings. Commands become `[shell command execution disabled by policy]`. Bundled and managed skills are unaffected.

### Extended Thinking Trigger

Include the word "ultrathink" anywhere in skill content to enable extended thinking.

### Supporting Files

Skills can include multiple files in their directory:

```
my-skill/
  SKILL.md           # Main instructions (required)
  reference.md       # Detailed API docs (loaded when needed)
  examples.md        # Usage examples (loaded when needed)
  scripts/
    helper.py        # Utility script (executed, not loaded)
```

Reference supporting files from `SKILL.md` so Claude knows what they contain. Keep `SKILL.md` under 500 lines.

### Skill Content Lifecycle

- Rendered `SKILL.md` enters conversation as a single message and stays for the session.
- Claude Code does NOT re-read the file on later turns.
- Auto-compaction re-attaches invoked skills: first 5,000 tokens each, combined budget 25,000 tokens, most-recently-invoked first.

**Source:** https://code.claude.com/docs/en/skills.md -- "Inject dynamic context", "Skill content lifecycle", "Add supporting files"

---

## 7. Built-in Commands -- Complete Reference

All entries from https://code.claude.com/docs/en/commands.md. `<arg>` = required, `[arg]` = optional.

| Command | Purpose |
|:--|:--|
| `/add-dir <path>` | Add working directory for file access during session |
| `/agents` | Manage agent configurations |
| `/autofix-pr [prompt]` | Spawn web session watching current branch PR for CI/review fixes |
| `/batch <instruction>` | **[Skill]** Orchestrate large-scale parallel changes across codebase |
| `/btw <question>` | Side question without adding to conversation history |
| `/chrome` | Configure Chrome integration settings |
| `/claude-api` | **[Skill]** Load Claude API reference material for project language |
| `/clear` | Clear conversation history. Aliases: `/reset`, `/new` |
| `/color [color\|default]` | Set prompt bar color. Colors: red, blue, green, yellow, purple, orange, pink, cyan |
| `/compact [instructions]` | Compact conversation with optional focus |
| `/config` | Open Settings interface. Alias: `/settings` |
| `/context` | Visualize current context usage as colored grid |
| `/copy [N]` | Copy last assistant response to clipboard; interactive picker for code blocks |
| `/cost` | Show token usage statistics |
| `/debug [description]` | **[Skill]** Enable debug logging and troubleshoot issues |
| `/desktop` | Continue session in Desktop app. Alias: `/app` |
| `/diff` | Interactive diff viewer showing uncommitted changes and per-turn diffs |
| `/doctor` | Diagnose and verify installation and settings |
| `/effort [level]` | Set effort level: low, medium, high, max, auto |
| `/exit` | Exit CLI. Alias: `/quit` |
| `/export [filename]` | Export conversation as plain text |
| `/extra-usage` | Configure extra usage for rate limits |
| `/fast [on\|off]` | Toggle fast mode |
| `/feedback [report]` | Submit feedback. Alias: `/bug` |
| `/branch [name]` | Branch conversation at this point. Alias: `/fork` |
| `/help` | Show help and available commands |
| `/hooks` | View hook configurations |
| `/ide` | Manage IDE integrations |
| `/init` | Initialize project with CLAUDE.md |
| `/insights` | Generate session analysis report |
| `/install-github-app` | Set up Claude GitHub Actions app |
| `/install-slack-app` | Install Claude Slack app |
| `/keybindings` | Open keybindings configuration |
| `/login` | Sign in to Anthropic account |
| `/logout` | Sign out from Anthropic account |
| `/loop [interval] [prompt]` | **[Skill]** Run prompt repeatedly on interval |
| `/mcp` | Manage MCP server connections |
| `/memory` | Edit CLAUDE.md files and auto-memory |
| `/mobile` | Show QR code for mobile app. Aliases: `/ios`, `/android` |
| `/model [model]` | Select or change AI model |
| `/passes` | Share free week of Claude Code |
| `/permissions` | Manage tool permission rules. Alias: `/allowed-tools` |
| `/plan [description]` | Enter plan mode |
| `/plugin` | Manage plugins |
| `/powerup` | Interactive feature lessons with demos |
| `/pr-comments [PR]` | (Removed v2.1.91) Fetch PR comments |
| `/privacy-settings` | View/update privacy settings (Pro/Max only) |
| `/release-notes` | View changelog in interactive picker |
| `/reload-plugins` | Reload active plugins without restart |
| `/remote-control` | Enable remote control from claude.ai. Alias: `/rc` |
| `/remote-env` | Configure default remote environment |
| `/rename [name]` | Rename current session |
| `/resume [session]` | Resume conversation. Alias: `/continue` |
| `/review` | (Deprecated) Install code-review plugin instead |
| `/rewind` | Rewind conversation/code to previous point. Alias: `/checkpoint` |
| `/sandbox` | Toggle sandbox mode |
| `/schedule [description]` | Create/manage cloud scheduled tasks |
| `/security-review` | Analyze branch changes for security vulnerabilities |
| `/setup-bedrock` | Configure Amazon Bedrock |
| `/setup-vertex` | Configure Google Vertex AI |
| `/simplify [focus]` | **[Skill]** Review changed files for reuse/quality/efficiency issues |
| `/skills` | List available skills |
| `/stats` | Visualize usage, sessions, streaks |
| `/status` | Open Settings Status tab |
| `/statusline` | Configure status line |
| `/stickers` | Order Claude Code stickers |
| `/tasks` | List background tasks. Alias: `/bashes` |
| `/teleport` | Pull web session into terminal. Alias: `/tp` |
| `/terminal-setup` | Configure terminal keybindings |
| `/theme` | Change color theme |
| `/ultraplan <prompt>` | Draft plan in ultraplan session |
| `/upgrade` | Open upgrade page |
| `/usage` | Show plan usage/rate limits |
| `/vim` | (Removed v2.1.92) Use `/config` instead |
| `/voice` | Toggle voice dictation |
| `/web-setup` | Connect GitHub to Claude Code on web |

### MCP Prompts as Commands

MCP servers can expose prompts that appear as commands with format `/mcp__<server>__<prompt>`, dynamically discovered from connected servers.

**Source:** https://code.claude.com/docs/en/commands.md

---

## 8. Custom Command/Skill Examples -- Official Examples

### Example 1: Explain Code Skill (model-invocable + user-invocable)

```yaml
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:
1. Start with an analogy
2. Draw a diagram (ASCII art)
3. Walk through the code step-by-step
4. Highlight a gotcha
```

### Example 2: Deploy Skill (user-only, subagent)

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

### Example 3: Fix Issue (with arguments)

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

### Example 4: Migrate Component (indexed arguments)

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

### Example 5: PR Summary (dynamic context injection)

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

### Example 6: Commit (tool pre-approval)

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

### Example 7: Code Review (in plugin, from plugins reference)

```yaml
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

### Example 8: Session Logger (session ID substitution)

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

**Source:** https://code.claude.com/docs/en/skills.md -- various sections; https://code.claude.com/docs/en/plugins.md

---

## 9. Command Discovery and Registration

### Auto-discovery Mechanism

- Claude Code scans known directories at session start for `.md` files (commands) and `SKILL.md` files (skills).
- Scan locations: `~/.claude/skills/`, `~/.claude/commands/`, `.claude/skills/`, `.claude/commands/`, plugin directories, managed settings.
- Nested `.claude/skills/` directories discovered when working in subdirectories (monorepo support).
- `--add-dir` directories: only `.claude/skills/` is auto-discovered (exception to the general rule).

### Registration at Runtime

- Typing `/` shows all available commands: built-in commands, bundled skills, user-authored skills, plugin skills, and MCP prompts.
- Typing `/` followed by letters filters the list.
- Plugin skills are namespaced: `/plugin-name:skill-name`.
- `/skills` command lists all available skills.

### Context Budget for Skill Descriptions

- Skill descriptions are loaded into context so Claude knows what's available.
- Budget scales dynamically at **1% of context window**, fallback **8,000 characters**.
- Each description capped at **250 characters** regardless of budget.
- Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.
- All skill names are always included even if descriptions are truncated.

### Live Change Detection

Skills support live change detection. Editing a skill file during a session (in project, personal, or `--add-dir` directories) is picked up without restarting. For plugins, use `/reload-plugins`.

**Source:** https://code.claude.com/docs/en/skills.md -- "Skill descriptions are cut short"; https://code.claude.com/docs/en/interactive-mode.md -- "Commands" section

---

## 10. Interaction Between Skills and Commands (and Subagents)

### Skills Invoking via the Skill Tool

Claude invokes skills through the **Skill tool**. This is a model-callable tool.

- Built-in commands (`/compact`, `/init`, etc.) are NOT available through the Skill tool.
- Permission rules can control skill access: `Skill(name)` for exact match, `Skill(name *)` for prefix.
- Denying `Skill` in `/permissions` disables all skill invocation by Claude.

### Skills Running in Subagents (`context: fork`)

When `context: fork` is set, the skill body becomes the prompt for an isolated subagent:

| Approach | System prompt | Task | Also loads |
|:--|:--|:--|:--|
| Skill with `context: fork` | From agent type (Explore, Plan, etc.) | SKILL.md content | CLAUDE.md |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

### Skills Can Reference Other Files

Skills can reference supporting files (templates, scripts, reference docs) by linking to them from `SKILL.md`. Claude reads these files using its tools when needed.

### Skills Cannot Directly Invoke Other Skills

There is no documented mechanism for one skill to invoke another skill. Skills are prompt-injected content. However, since Claude has the Skill tool, a skill's instructions could direct Claude to invoke another skill during execution.

### Subagents Can Preload Skills

Subagents defined in `.claude/agents/` can list skills in their `skills` frontmatter field. These skills are fully injected at startup (not lazily loaded).

**Source:** https://code.claude.com/docs/en/skills.md -- "Restrict Claude's skill access", "Run skills in a subagent"

---

## 11. Plugin Commands/Skills -- Structure and Discovery

### Plugin Directory Structure

```
my-plugin/
  .claude-plugin/
    plugin.json           # Manifest (optional)
  skills/                 # Skills as directories with SKILL.md
    code-reviewer/
      SKILL.md
    pdf-processor/
      SKILL.md
      scripts/
  commands/               # Legacy flat .md skill files
    status.md
    logs.md
  agents/                 # Subagent definitions
  hooks/
    hooks.json
  bin/                    # Executables added to PATH
  .mcp.json              # MCP servers
  .lsp.json              # LSP servers
  settings.json          # Default settings
  output-styles/          # Output style definitions
```

### Plugin Manifest Component Paths

```json
{
  "name": "my-plugin",
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/"
}
```

- Custom paths REPLACE default directories (not additive).
- To keep defaults AND add more: `"skills": ["./skills/", "./extras/"]`.
- All paths must be relative and start with `./`.

### Plugin Skill Namespacing

- Plugin skills are always namespaced: `/plugin-name:skill-name`.
- This prevents conflicts between plugins.
- The `name` field in `plugin.json` determines the namespace prefix.

### Plugin Skill Discovery

- Skills and commands auto-discovered when plugin is installed.
- Claude can invoke them automatically based on task context.
- `/reload-plugins` reloads without restarting.
- `--plugin-dir` flag for development/testing loads plugin directly.

### Plugin Caching

Marketplace plugins are copied to `~/.claude/plugins/cache/`. Orphaned versions removed after 7 days. Plugins cannot reference files outside their directory (path traversal blocked).

**Source:** https://code.claude.com/docs/en/plugins-reference.md; https://code.claude.com/docs/en/plugins.md

---

## 12. SDK Slash Commands (Agent SDK)

The SDK page at https://code.claude.com/docs/en/slash-commands.md redirects to the skills page. The SDK documentation uses the same unified skill/command system. Key SDK-specific notes:

- The SDK `SlashCommand` type is listed in the TypeScript reference.
- SDK skills follow the same `SKILL.md` format.
- The SDK supports both `skills/` and `commands/` directories.
- File locations: personal (`~/.claude/skills/`), project (`.claude/skills/`).
- Commands from `.claude/commands/` work identically with the same frontmatter.

**Source:** https://code.claude.com/docs/en/slash-commands.md (redirects to skills.md); https://code.claude.com/docs/en/typescript.md -- `SlashCommand` type

---

## 13. When to Use Skills vs CLAUDE.md vs Hooks

| Need | Use |
|:--|:--|
| Facts, conventions, always-on rules | CLAUDE.md |
| Procedures, workflows, checklists | Skills |
| User-triggered actions with side effects | Skills with `disable-model-invocation: true` |
| Background knowledge Claude should find when relevant | Skills with `user-invocable: false` |
| Deterministic enforcement (format on save, block edits) | Hooks |
| Long reference material (cost-free until used) | Skills with supporting files |
| Organization-wide standards | Managed skills or managed CLAUDE.md |

**Key insight from docs:** "Create a skill when you keep pasting the same playbook, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact."

**Source:** https://code.claude.com/docs/en/skills.md -- opening paragraph

---

## 14. Configuration and Settings Interaction

### Relevant Settings

| Setting | Effect |
|:--|:--|
| `disableSkillShellExecution` | Disables `!`command`` preprocessing in non-bundled skills |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Environment variable controlling description context budget |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | Required for `shell: powershell` in skill frontmatter |

### Permission Integration

- `allowed-tools` in frontmatter GRANTS permissions; does not restrict.
- Deny rules in `/permissions` override skill permissions.
- Permission syntax for skills: `Skill(name)` exact, `Skill(name *)` prefix.
- Denying `Skill` blocks all model skill invocation.

**Source:** https://code.claude.com/docs/en/skills.md -- "Pre-approve tools for a skill", "Restrict Claude's skill access"

---

## 15. Agent Skills Open Standard

Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with:

- **Invocation control** (`disable-model-invocation`, `user-invocable`)
- **Subagent execution** (`context: fork`, `agent`)
- **Dynamic context injection** (`` !`command` ``)

**Source:** https://code.claude.com/docs/en/skills.md -- opening section
