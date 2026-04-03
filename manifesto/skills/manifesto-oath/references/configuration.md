# Manifesto Configuration

How to declare which manifestos a project operates under. The manifesto plugin's hooks read this configuration at session start, after context compaction, and when subagents spawn.

## Configuration Sources

Two formats, checked in priority order:

### 1. `.manifestos.yaml` (preferred)

A YAML list at the project root. Each entry is a string — the hook auto-detects the type by shape.

```yaml
# By name — matched against files in the LLM_MANIFESTOS repo
- correct-by-construction
- decomplect
- first-principles

# By URL — fetched at initialization
- https://raw.githubusercontent.com/someone/repo/main/manifesto.md

# By local path — read from the project directory
- ./docs/team-principles.md
```

**Resolution rules (applied by Claude, not the hook):**

| Entry shape | Type | Resolution |
|-------------|------|------------|
| Plain text (no `/`, no `://`) | Name | Fuzzy-matched against manifesto filenames in the cloned repo |
| Starts with `http://` or `https://` | URL | Fetched via WebFetch tool |
| Starts with `./` or `/` | Local path | Read relative to the project root |

Names are matched by keyword against the repo's `manifestos/` directory. For example, `correct-by-construction` matches `Manifesto, rust - "correct by construction".md`. Claude handles the fuzzy matching.

### 2. `## Active Manifestos` section in CLAUDE.md

Fallback when `.manifestos.yaml` doesn't exist. The hook extracts everything between `## Active Manifestos` and the next `##` heading.

```markdown
## Active Manifestos

Bind to all three on session start:
1. **Correct By Construction**
2. **Simple Made Easy**
3. **First Principles — Break the Mold**
```

This format is freeform markdown — the hook passes the raw text to Claude, which interprets the names and resolves them against the repo.

### 3. No configuration

When neither source exists, the hook instructs Claude to delegate a subagent that explores the project (language, domain, conventions), reads the available manifesto files, and recommends which are relevant. Claude then asks the user before binding.

## Hook Lifecycle

The configuration is read at three points:

| Hook | Trigger | Behavior |
|------|---------|----------|
| **SessionStart** | Session begins | Clone repo (lazy), detect config, initialize bindings or explore |
| **PostCompact** | After context compaction | Re-detect config, re-bind (previous bindings don't survive compaction) |
| **SubagentStart** | Subagent spawned | Inject manifesto awareness (lightweight, no full oath ceremony) |

All hooks share a lazy clone mechanism — the LLM_MANIFESTOS repo is cloned once to `/tmp/claude-manifesto-repo/LLM_MANIFESTOS` on first access and reused across the session.

## Examples

### Rust project

```yaml
# .manifestos.yaml
- correct-by-construction
- decomplect
```

### Python project with team standards

```yaml
# .manifestos.yaml
- zen-of-python
- decomplect
- code-speaks
- ./docs/engineering-standards.md
```

### Project using external manifesto

```yaml
# .manifestos.yaml
- first-principles
- https://raw.githubusercontent.com/org/repo/main/OUR_MANIFESTO.md
```
