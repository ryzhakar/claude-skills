# Session 2026-05-01

## Checkpoint — 18:15

### Narrative

Single-plugin deep session: manifesto plugin v2.3.1 → v3.0.1.

**Phase 1 — Gap analysis (spec-chef).** Identified 5 problems: (1) Tier 2 skill resolution gives subagents no actionable path, (2) hardcoded manifesto directory, (3) plugin auto-clones repo, (4) no mid-session drift prevention, (5) subagent binding has low compliance without user-voice reinforcement. Extracted 6 decisions via constrained questioning.

**Phase 2 — Implementation (7-task plan, 3 phases).** Task 1 (ensure-repo.sh refactor) sequential, then Tasks 2-4 parallel (Tier 2 fix, drift hook, persona nudge), then Tasks 5-6 parallel (SCHEMA.md, version bump). All implemented via worktree-isolated implementer agents.

**Phase 3 — Critical bug discovery.** During adversarial testing setup, discovered `post-compact.sh` outputs plain text — platform routes it to debug log, not conversation context. PostCompact requires `hookSpecificOutput` JSON wrapping. This means **constitution bindings have never re-injected after compaction** in any version of the plugin. Fixed by adding `emit_json()` wrapper matching `subagent-start.sh` pattern.

**Phase 4 — Adversarial testing.** 6 test agents, ~50 tests total. Categories: ensure-repo + drift-reminder, subagent-start + session-start, hooks.json + backwards compatibility, reference-compliance output format, spec-test against all 6 decisions, edge case bombardment (shell injection, malformed YAML, large inputs, stdin edge cases). One additional bug found: non-string YAML scalars crash the renderer (fixed with scalar coercion in `normalize_item`).

**Phase 5 — Manifesto tagline sharpening.** 10 sonnet agents (1 per manifesto) extracted optimal drift-reminder taglines from full content. 6 changed, 4 kept. Applied to LLM_MANIFESTOS repo, README regenerated, committed + pushed.

### Decisions

| Decision | Context | Rationale |
|----------|---------|-----------|
| manifesto_dir in .manifestos.yaml only | Env var override considered but rejected | Single source of truth, project-scoped config |
| Default dir stays /tmp path | User wants backwards compat | Override is additive, not substitutive |
| Missing dir = silent skip | Exit 2 blocking considered | Non-blocking — hooks shouldn't prevent sessions |
| Tier 2: inject plugin cache path for subagents | Inline skill content and eliminate Tier 2 also considered | User chose "inject directory, they're smart enough" |
| UserPromptSubmit for drift prevention | PreToolUse(Agent) and Stop hook also considered | Only UPS and SessionStart inject visible context reliably; UPS fires every message |
| Taglines only for drift content | Taglines + tension pointers considered | Only taglines are parseable from frontmatter |
| Persona nudge via SessionStart footer | SubagentStart dual output and PreToolUse(Agent) hook also considered | SessionStart is the natural place for orchestrator instructions |
| Dual injection for subagent binding | Orchestrator-only considered | Hook provides ceremony, orchestrator provides authority (user voice) |
| ensure_repo() on-demand, not auto-clone | Clean break and deprecation also considered | User wants the script available but not auto-triggered |
| Major version bump to 3.0.0 | User approved explicitly | Breaking changes: auto-clone removed, PostCompact output format changed |

### Failures

| Failure | Root cause | Correction |
|---------|-----------|------------|
| PostCompact bindings going to debug log | Plain text stdout on PostCompact goes to debug log per platform contract; only UPS and SessionStart are exceptions | Wrapped output in hookSpecificOutput JSON with emit_json() |
| Non-string YAML scalars crash renderer | normalize_item only handled str and dict; int/bool/None passed through | Added scalar coercion (str()) and None filtering |
| PLUGINS_CACHE_DIR renders as "/" in dev context | Path derivation goes up 4 levels from hooks/ dir; in dev repo this is filesystem root | Fallback to ~/.claude/plugins/cache instead of empty string |
| ELEMENT_DESCRIPTION dead code in emit_static_fallback | Set in function but preamble-subagent.txt has no ${ELEMENT_DESCRIPTION} placeholder | Not fixed this session — pre-existing, cosmetic |

### Working State

Implementation and testing complete. All 7 tasks done. Version at 3.0.1 (user bumped from 3.0.0 during edge case fix). User applied a linter fix to normalize_item that handles None and coerces scalars to str. No commits made by orchestrator — user handles VCS.
