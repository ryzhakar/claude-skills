# QA Automation v2: Implementation Plan

This document supersedes ARCHITECTURE.md and IMPLEMENTATION-BRIEF.md. Where they conflict with this plan, this plan wins.

---

## Final Structure (14 files)

```
qa-automation/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── planner-agent.md
│   ├── generator-agent.md
│   ├── executor-agent.md
│   └── healer-agent.md
├── skills/
│   └── qa-run/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
└── references/
    ├── file-protocol.md
    ├── locator-strategy.md
    ├── mcp-tools.md
    ├── seed-file-spec.md
    ├── ten-tier-algorithm.md
    ├── confidence-scoring.md
    ├── failure-heuristics.md
    └── cicd-workflow.md
```

---

## Dismissed Approaches (DO NOT implement)

### ❌ Sub-skills (qa-plan, qa-generate, qa-execute, qa-heal)

The ARCHITECTURE.md specifies 4 hidden sub-skills with `user-invocable: false` and `context: fork` as intermediaries between the orchestrator and agents. **Do not create these.** They are middlemen that:
- Duplicate agent instructions
- Duplicate orchestrator branching logic
- Introduce unresolved `context: fork` wiring ambiguity
- Create a subagent depth violation (qa-heal as subagent dispatching healer-agents)

The orchestrator dispatches agents directly via the Agent tool. 4 fewer files, 1 fewer layer, 0 ambiguities.

### ❌ PR creation in healer-agent

ARCHITECTURE.md Phase 6 of healer-agent creates git branches, pushes, opens PRs, auto-merges. **Do not implement this in the healer.** It braids healing with deployment and creates contradictory code paths (single healer creates PRs vs parallel fan-out creating one consolidated PR).

PR creation belongs in the orchestrator's Phase 4 post-processing. The healer writes fixes and results. The orchestrator reads results and creates PRs.

### ❌ Circuit breaker writing in healer-agent

ARCHITECTURE.md has the healer reading AND writing `.github/healing-state.json`. In parallel mode, N concurrent writers race on the same file. **Healers read the circuit breaker (blocklist check). Healers never write it.** The orchestrator updates circuit breaker state after aggregating all healer results.

### ❌ `.playwright/orchestrator-status.md` (JSON in .md)

ARCHITECTURE.md names the status file `.md` for `@` syntax compatibility. The file contains JSON. **Name it `orchestrator-status.json`.** Call things what they are.

### ❌ `allowed-tools` in skill frontmatter

ARCHITECTURE.md puts `allowed-tools: Read, Write, Bash, Glob` on skill frontmatter. This field is documented for commands, not skills. Skills load as instructions into Claude's main context where all tools are available. **Do not use `allowed-tools` in SKILL.md frontmatter.** Agent definitions have `tools:` which IS the correct restriction mechanism for agents.

---

## Responsibility Boundaries

| Concern | Owner | NOT owned by |
|---------|-------|-------------|
| Phase sequencing & branching | orchestrator (qa-run) | agents |
| Agent dispatch (including parallel fan-out) | orchestrator | hooks, sub-skills |
| Status file reading & branching | orchestrator | agents |
| PR creation (all confidence levels) | orchestrator | healer-agent |
| Circuit breaker state updates | orchestrator | healer-agent |
| Circuit breaker state reading (blocklist) | healer-agent | orchestrator |
| Phase persistence (.claude/qa-phase.txt) | orchestrator | hooks (hook only reads) |
| Compaction recovery message | SessionStart(compact) hook | orchestrator |
| Directory creation | SessionStart(startup) hook | agents |
| Ad-hoc healing suggestion | PostToolUseFailure hook | orchestrator |
| Test plan artifacts | planner-agent | — |
| Test file generation | generator-agent | — |
| Failure classification | executor-agent | — |
| Locator repair + results JSON | healer-agent | — |

---

## Build Order

Each tier depends only on tiers above it. Files within a tier can be built in parallel.

### Tier 0: Scaffold

**File:** `.claude-plugin/plugin.json`

Source: ARCHITECTURE.md plugin.json section (use verbatim, it's correct).

Note: plugin.json goes inside `.claude-plugin/` per plugin-structure skill. The ARCHITECTURE.md shows it at root — adjust path.

### Tier 1: Reference Files (parallel, all 8)

All 8 reference files are edits/copies from v1 sources. Source mapping:

| v2 file | Primary source | Edits needed |
|---------|---------------|-------------|
| file-protocol.md | `plugin/references/file-protocol.md` | Add orchestrator-status.json, qa-phase.txt, healed/ dir, session-report.md to artifact map. Merge artifact-templates.md content from `plugin/skills/test-planner/references/artifact-templates.md`. Update skill names → agent names. |
| locator-strategy.md | `plugin/references/locator-strategy.md` | Add shadow DOM section (parent-component-first chaining). Source: T4-01, ARCHITECTURE.md shadow DOM guidance. Add note about MCP snapshot not seeing shadow root elements. |
| mcp-tools.md | `plugin/references/mcp-tools.md` | Add MCP version pin section: `@playwright/mcp >= v0.0.40`, CVE-2025-9611. Add version check command. Optionally add `@playwright/cli` reference from T3-12. |
| seed-file-spec.md | `plugin/references/seed-file-spec.md` | Add few-shot reference test section (distinct from seed). Seed = environment health check. Few-shot = 2-3 existing tests that teach assertion style. Source: ARCHITECTURE.md generator-agent "Few-Shot Reference Tests" section, T2-B05. Update "How Skills Use" → "How Agents Use". |
| ten-tier-algorithm.md | `plugin/skills/test-healer/references/ten-tier-algorithm.md` | Copy with minimal edits. Content is complete and verified. |
| confidence-scoring.md | `plugin/skills/test-healer/references/confidence-scoring.md` | Copy with minimal edits. |
| failure-heuristics.md | `plugin/skills/test-healer/references/failure-heuristics.md` | Merge with `plugin/skills/test-executor/references/failure-classification.md` (regex patterns, output schema, cross-browser flags, flaky taxonomy). Deduplicate overlapping content. |
| cicd-workflow.md | `plugin/skills/test-healer/references/cicd-workflow.md` | Fix healing stub: replace `echo` with `claude -p "invoke healer-agent on .ai-failures.json"`. Fix healable_count bug: `classifications.locator.length` only (remove timing). |

All v1 sources are at: `/Users/ryzhakar/ai-driven-research/qa-automation/plugin/`

### Tier 2: Hooks

**File:** `hooks/hooks.json`

Source: ARCHITECTURE.md hooks section. Use the plugin hooks.json wrapper format:
```json
{
  "hooks": {
    "SessionStart": [...],
    "PostToolUse": [...]
  }
}
```

Three hooks:
1. **SessionStart(compact):** Read `.claude/qa-phase.txt`, output checkpoint message. Use ARCHITECTURE.md command verbatim.
2. **SessionStart(startup):** `mkdir -p .playwright .claude`. Use verbatim.
3. **PostToolUse (failure detection):** Adapt from ARCHITECTURE.md's PostToolUseFailure. Verify the correct event name and matcher pattern — ARCHITECTURE.md uses `PostToolUseFailure` which may not be a real hook event. The documented events are: PreToolUse, PostToolUse, Stop, SubagentStop, UserPromptSubmit, SessionStart, SessionEnd, PreCompact, Notification. **If PostToolUseFailure doesn't exist, use PostToolUse with a prompt that checks for failure in the tool result.**

### Tier 3: Agent Definitions (parallel, all 4)

Each agent uses the ARCHITECTURE.md agent body as the starting point, with these adjustments:

**All agents:**
- Add `<example>` blocks to description (required by agent-development skill, missing from ARCHITECTURE.md)
- Use `@references/filename.md` syntax for reference file pointers (marketplace convention) AND add explicit instruction "Read these files from disk before proceeding"
- Remove any PR creation or circuit breaker writing instructions

**planner-agent.md** (model: sonnet, maxTurns: 40, color: blue, tools: Read, Write, Bash, Glob)
- Source: ARCHITECTURE.md planner-agent + v1 test-planner SKILL.md
- Preserve: Iron Law (no plan without exploration), DOM quality scoring formula, WASM hydration, edge case checklist
- Add: artifact template formats (from artifact-templates.md, if not fully covered by file-protocol.md reference)

**generator-agent.md** (model: sonnet, maxTurns: 80, color: green, tools: Read, Write, Edit, Bash, Glob)
- Source: ARCHITECTURE.md generator-agent + v1 test-generator SKILL.md
- Preserve: one-test-at-a-time discipline, quality checklist, risky locators list, .or() fallback, page object extraction threshold, worker-scoped fixtures
- Keep: few-shot reference test section (already in ARCHITECTURE.md)

**executor-agent.md** (model: haiku, maxTurns: 30, color: yellow, tools: Read, Write, Bash, Glob)
- Source: ARCHITECTURE.md executor-agent + v1 test-executor SKILL.md
- Preserve: CLI-exclusive rule, seed health check, 6-category regex classification, flaky detection, cross-browser analysis
- Enforce: healable_count = locator array length ONLY

**healer-agent.md** (model: sonnet, maxTurns: 40, color: red, tools: Read, Write, Edit, Bash, Grep, Glob)
- Source: ARCHITECTURE.md healer-agent + v1 test-healer SKILL.md
- Preserve: Iron Law, hard rejection rules, ten-tier algorithm reference, LLM fallback cap at MEDIUM, confidence scoring, healer comment format
- **Remove:** Phase 6 (PR creation) — orchestrator handles this
- **Change:** Circuit breaker to READ-ONLY — check blocklist, report skip reasons, do NOT update healing-state.json
- **Change:** color from orange to red (agent-development skill says red = critical/security, which fits healing better; orange is not a valid color option)
- Output: per-failure JSON in `.playwright/healed/{test-name}.json` (parallel mode) or `.healing-results.json` (single mode). In both cases, just write results. No git operations.

### Tier 4: Orchestrator Skill

**File:** `skills/qa-run/SKILL.md`

Source: ARCHITECTURE.md qa-run skill, heavily modified.

The orchestrator is the coordinator. It:

1. **Prerequisites:** Check seed file, base URL, existing session (.claude/qa-phase.txt for resume)
2. **Phase 1 PLAN:** Dispatch planner-agent via Agent tool. Read orchestrator-status.json. Branch on DONE/NEEDS_CONTEXT/BLOCKED. Write PLAN to qa-phase.txt.
3. **Phase 2 GENERATE:** Dispatch generator-agent. Read status. Branch. Write GENERATE.
4. **Phase 3 EXECUTE:** Dispatch executor-agent. Read status + .ai-failures.json. Branch. Write EXECUTE.
5. **Phase 4 HEAL:** Count locator failures in .ai-failures.json.
   - N == 0: skip healing
   - N < 5: dispatch 1 healer-agent with full failure list
   - N >= 5: dispatch N healer-agents in parallel (one per failure), each writing to `.playwright/healed/{test-name}.json`
   - After healing completes: aggregate results, update circuit breaker (.github/healing-state.json), create PRs by confidence:
     - >= 0.85 HIGH: single consolidated PR, auto-merge
     - 0.60-0.84 MEDIUM: review PR
     - < 0.60: record as deferred
   - Write HEAL to qa-phase.txt
6. **Phase 5 REPORT:** Write session-report.md. Clear qa-phase.txt.

Frontmatter:
```yaml
---
name: qa-run
description: >
  This skill should be used when the user asks to "run QA", "automate testing",
  "create and run Playwright tests", "set up E2E testing", "generate and execute tests",
  "run the full test pipeline", "run qa-run", or mentions running the full Playwright
  test lifecycle. Requires a base URL and seed file.
version: 2.0.0
---
```

No `user-invocable`, no `allowed-tools`, no `context` — just name, description, version.

---

## Validation Checklist

After building all files:

- [ ] `plugin.json` is in `.claude-plugin/` (not at root)
- [ ] All 4 agents have `<example>` blocks in descriptions
- [ ] All agents reference files with `@references/` AND explicit read instructions
- [ ] Healer-agent has NO git/PR operations
- [ ] Healer-agent circuit breaker is READ-ONLY
- [ ] orchestrator-status file is `.json` not `.md` everywhere
- [ ] qa-run SKILL.md has NO sub-skill invocations — dispatches agents directly
- [ ] qa-run SKILL.md owns PR creation and circuit breaker updates
- [ ] hooks.json uses correct plugin wrapper format (`{"hooks": {...}}`)
- [ ] PostToolUse hook event name is valid (not PostToolUseFailure)
- [ ] No `allowed-tools` in skill frontmatter
- [ ] Reference files have v2 edits applied (shadow DOM, MCP pin, few-shot, healable_count fix, artifact templates merged)
- [ ] Run plugin-validator agent on completed plugin
- [ ] Run skill-reviewer agent on qa-run skill
