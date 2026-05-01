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

Root is a YAML mapping with `you:` and/or `subagents:` keys.

```yaml
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
  source: /tmp/claude-manifesto-repo/LLM_MANIFESTOS/manifestos/first-principles.md
```

---

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Element identifier. Used for tiered resolution when no source is given. |
| `purpose` | no | Freeform text. Injected into hook output as natural language — tells the model why this element is in the stack. |
| `source` | no | Freeform. Path-shaped = file path. URL-shaped = fetch URL. Other text = location hint. |

---

## Scope keys

| Key | Meaning |
|-----|---------|
| `you:` | Orchestrator constitution. Injected by SessionStart and PostCompact hooks as natural language prose. |
| `subagents:` | Mapping of agent-type keys. Each key names a list of elements for that agent type. |
| `other:` (under `subagents:`) | Catch-all for agents not matching any specific key. |

---

## Hook behavior

### SessionStart / PostCompact

Parse `.manifestos.yaml`, render `you:` elements as natural language prose. Compose output from three parts: hook-specific preamble + shared binding core + inline footer. NEVER inject raw YAML.

The orchestrator is NOT responsible for supplying base subagent bindings — SubagentStart handles that automatically. The orchestrator MAY augment subagent bindings via dispatch prompts.

### SubagentStart

Reads `agent_type` from stdin JSON. Matches against `subagents:` keys in `.manifestos.yaml` using this resolution order:

1. Exact key match
2. Prefix-strip match
3. `other:` catch-all
4. Static fallback (no config)

Injects the FULL binding ceremony — same resolution protocol, transitive reading, interplay analysis, and manifesto-oath mandate as the orchestrator hooks. This is a real binding injection, not a reminder.

### Template architecture

Composable parts live in `hooks/templates/parts/`:

| File | Used by |
|------|---------|
| `preamble-session.txt` | SessionStart |
| `preamble-compact.txt` | PostCompact |
| `preamble-subagent.txt` | SubagentStart |
| `binding-core.txt` | All three hooks (shared) |

Footers are inlined in the shell scripts, not extracted to files.

---

## Parsing rules

1. Root is a list → treat as `you:` section; no subagent bindings.
2. Root is a mapping → expect `you:` and/or `subagents:` keys.
3. String node in any list → normalize to `{name: <string>}`.
4. Dict node → `{name:, purpose?:, source?:}`.
