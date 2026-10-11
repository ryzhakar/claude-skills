# .manifestos.yaml Schema Reference

## Format variants

### Flat list (backwards compatible, orchestrator-only)

Root is a YAML list. All elements bind to the orchestrator. No subagent bindings.

```yaml
- only-fluff-die
- first-principles
- agentic-delegation
```

### Grouped mapping (full form)

Root is a YAML mapping with `you:` and/or `subagents:` keys. Supports optional top-level fields.

```yaml
manifesto_dir: /path/to/your/LLM_MANIFESTOS
you:
  - only-fluff-die
  - name: first-principles
    purpose: reasoning methodology
  - name: agentic-delegation
    purpose: orchestration operating model
    source: orchestration/skills/agentic-delegation/SKILL.md

subagents:
  instruction-writer:
    - name: first-principles
    - name: strunk-spr-v3
      purpose: writing compression standard
      source: https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml
  other:
    - first-principles
```

---

## Element forms

Each element in any list is one of:

**String** — name only, no metadata.

```yaml
- only-fluff-die
```

**Mapping** — name plus optional fields.

```yaml
- name: first-principles
  purpose: reasoning methodology
  source: .claude/manifesto-repo/LLM_MANIFESTOS/manifestos/first-principles.md
```

---

## Fields

### Top-level mapping fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `manifesto_dir` | string (path) | no | `<project_dir>/.claude/manifesto-repo/LLM_MANIFESTOS` | Override the default manifesto repository directory. All hooks use this path for Tier 1 resolution. Valid only in dict-form; ignored in flat list form. |

### Element fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Element identifier. Used for tiered resolution when no source is given. |
| `purpose` | no | Freeform text. Injected into hook output as natural language — tells the model why this element is in the stack. |
| `source` | no | Freeform. Path-shaped = file path. URL-shaped = fetch URL. Other text = location hint. |

---

## Scope keys

| Key | Meaning |
|-----|---------|
| `you:` | Orchestrator constitution. Injected by the SessionStart hook as natural language prose. |
| `subagents:` | Mapping of agent-type keys. Each key names a list of elements for that agent type. |
| `other:` (under `subagents:`) | Catch-all for agents not matching any specific key. |

---

## Hook behavior

### SessionStart

Matcher: `startup|resume|compact`. The host sends the firing source on stdin as `source`; the hook states it in one preamble line, `Session source: <source>.`

Parse `.manifestos.yaml`, render `you:` elements as natural language prose. Compose output from three parts: session preamble + shared binding core + inline footer. NEVER inject raw YAML. SessionStart and SubagentStart add `(voice: <register>, reader: <reader>)` after each element name from the matching manifesto's `register` and `reader` frontmatter fields, keep only the fields present, and omit the clause when neither exists.

Emit JSON: `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": <text>}}`. The text stays under 8,000 characters. The host persists hook output over 10,000 characters to a file and shows the model a 2KB preview.

The binding core never inlines `skills/manifesto-oath/SKILL.md`. It commands the model to invoke the Skill tool with skill `manifesto:manifesto-oath` (fallback: Read the skill file by absolute path), then lists five steps in at most 25 lines: resolve, read whole, interplay, commit, verify. Transitive depth: unbounded. Step two follows every reference until no unresolved reference remains, the rule the oath skill states; the hooks set no depth cap.

The footer includes a SUBAGENT BINDING REINFORCEMENT block instructing the orchestrator to use first-person user voice in dispatch prompts, so subagents receive binding directives as owner instructions rather than forwarded AI text.

The orchestrator is NOT responsible for supplying base subagent bindings — SubagentStart handles that automatically. The orchestrator MAY augment subagent bindings via dispatch prompts.

PostCompact is not an event in the host's `hookSpecificOutput` schema, so the plugin registers no PostCompact hook. Compaction fires SessionStart with source `compact`; that run re-binds.

### SubagentStart

Reads `agent_type` from stdin JSON. Matches against `subagents:` keys in `.manifestos.yaml` using this resolution order:

1. Exact key match
2. Prefix-strip match (`plugin:agent` matches the key `agent`)
3. Suffix match (the agent type ends with a key other than `other`; `my-instruction-writer` matches `instruction-writer`)
4. `other:` catch-all
5. Static fallback (no config, or no match and no `other:`): the injected text names no element

An absent `agent_type` skips to step 4.

Injects the same binding core as SessionStart: the load command for `manifesto:manifesto-oath` and the five steps, never the skill text. Output stays under 8,000 characters. This is a real binding injection, not a reminder.

The ceremony carries element names, purposes, and configured sources — never element content. Subagents read or fetch each element themselves; dispatch prompts carry sources for elements the config omits.

Tier 2 resolution injects the plugin cache path so subagents can resolve skills from the installed plugin location without knowing the absolute path at authoring time.

### UserPromptSubmit

Fires on every user message. Parses manifesto files listed under `you:` (using the same tiered resolution as other hooks) and extracts YAML frontmatter taglines. Injects the taglines as a brief drift-prevention reminder into the hook output.

Output accumulates in conversation history (platform behavior) — this is intentional. Each injection reinforces the active constitution without re-running the full binding ceremony.

### Template architecture

Composable parts live in `hooks/templates/parts/`:

| File | Used by |
|------|---------|
| `preamble-session.txt` | SessionStart |
| `preamble-subagent.txt` | SubagentStart |
| `binding-core.txt` | SessionStart and SubagentStart (shared) |

Placeholders: `ELEMENT_DESCRIPTION`, `MANIFESTO_DIR`, `PLUGINS_CACHE_DIR`, `SKILL_PATH`, `SOURCE`. Footers are inlined in the shell scripts, not extracted to files.

`hooks/test_hooks.sh` runs every hook against the live `.manifestos.yaml` and asserts the output contract.

---

## Repository management

SessionStart calls `ensure_repo()` from `hooks/ensure-repo.sh`, cloning the manifesto repo to `manifesto_dir` on first use and pulling on later sessions. SubagentStart and UserPromptSubmit read whatever `ensure_repo()` last left in place and never clone or pull themselves, keeping their tighter timeouts network-free. `ensure_repo()` drops a self-ignoring `.gitignore` (`*`) next to the clone so the project's own git history never picks it up.

---

## Parsing rules

1. Root is a list → treat as `you:` section; no subagent bindings.
2. Root is a mapping → expect `you:` and/or `subagents:` keys.
3. String node in any list → normalize to `{name: <string>}`.
4. Dict node → `{name:, purpose?:, source?:}`.
