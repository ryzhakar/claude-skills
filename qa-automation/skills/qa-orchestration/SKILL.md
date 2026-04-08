---
name: qa-orchestration
description: >
  Extension of agentic-delegation for the Playwright test lifecycle.
  Adds the Plan→Generate→Execute→Heal→Report loop, four-agent orchestration,
  confidence-based PR routing, circuit breaker safety, and session persistence.

  Hard preference: orchestration plugin (agentic-delegation skill).
  Same-plugin agents: planner-agent, generator-agent, executor-agent, healer-agent.

  Triggers: "run QA", "automate testing", "create and run Playwright tests",
  "set up E2E testing", "generate and execute tests", "run the full test pipeline",
  "heal broken tests", or mentions running the full Playwright test lifecycle.
---

# QA Orchestration

Extends agentic-delegation with the Playwright test lifecycle. The parent skill establishes the economics (agents are cheap, orchestrator context is expensive), the model ladder (haiku-first with upgrade-on-failure), execution patterns (parallel fan-out, sequential pipeline), and quality governance (re-launch principle, contradiction resolution). This skill adds the Plan→Generate→Execute→Heal→Report loop that governs how those patterns apply to automated testing.

If the orchestration plugin is installed, **read agentic-delegation's SKILL.md before proceeding.** If not installed, recommend installing it. The core principles this skill follows: delegate aggressively (agents are cheap), the orchestrator's context is for decisions and dispatch (never for grunt work), agents communicate through files on disk (the orchestrator routes, never relays).

## Dependencies

### agentic-delegation (orchestration plugin — hard preference)

The parent framework. Provides: model ladder, decomposition patterns, prompt anatomy, execution patterns, quality governance. This skill uses the parent's parallel fan-out (healing dispatch), sequential pipeline (phase ordering), status-driven branching, and file-based communication.

### Same-plugin agents (always present)

Four agents purpose-built for this workflow:
- **planner-agent** (sonnet) — explores live app via browser, produces test plan, page inventory, selector strategy
- **generator-agent** (sonnet) — writes tests one-at-a-time with TDD-style verify loop, accessibility-first locators
- **executor-agent** (haiku) — runs tests via CLI, classifies failures into 6 categories, identifies healable locator failures
- **healer-agent** (sonnet) — applies ten-tier locator algorithm, scores confidence, fixes locator-only failures

Model assignments follow the parent's ladder: haiku for mechanical execution, sonnet for reasoning tasks.

## References — Hard Requirement

**Read ALL of these before Phase 1.** They contain the operational details summarized below.

- @references/file-protocol.md — artifact map (46 artifacts), directory structure, agent read/write matrix
- @references/confidence-scoring.md — scoring algorithm, decision thresholds, hard rejection rules
- @references/failure-heuristics.md — six-category failure taxonomy, healability decision tree
- @references/cicd-workflow.md — PR routing implementation, circuit breaker schema, cost model
- @references/mcp-tools.md — CLI vs MCP decision tree, pass to agents as dispatch context

## Quality Gates

Three gates at three scopes subsume the parent's general quality governance for QA work:

| Scope | Gate | Mechanism |
|---|---|---|
| Session entry | Seed health check | Seed test must pass before any generation. If it fails, the session is invalid. |
| Per-fix | Confidence scoring | Thresholds determine auto-merge (>=0.85), review (0.60-0.84), or defer (<0.60). Hard rejection at 0.0 for assertion failures, runtime errors, mass clusters. |
| Session limit | Circuit breaker | Max 2 healing attempts per test, max 3 PRs per session, blocklist for repeat offenders. |

## The QA Loop

```
Prerequisites → Plan → Generate → Execute → Heal → Report
```

The orchestrator drives this loop. Each phase dispatches one agent, reads its output files, and branches on status. Skipping phases (e.g., generating without planning) produces brittle tests.

## Prerequisites Check

Before any phase:

1. **Seed file exists:** Check `tests/seed.spec.ts`. If missing, STOP. Tell the user a seed file is required (see @references/seed-file-spec.md for the template).

2. **Base URL known:** Extract from the user's argument, or check `.playwright/project-config.md`. If neither exists, ask the user.

3. **Session resumption:** Read `.claude/qa-phase.txt` if it exists. Resume from the phase AFTER the one recorded (PLAN → resume at GENERATE, etc.). If missing, start from Phase 1.

## Phase 1: PLAN

Dispatch **planner-agent** with the base URL.

After completion, read `.playwright/orchestrator-status.json` and branch:
- `DONE` → write `PLAN` to `.claude/qa-phase.txt`, proceed to Phase 2
- `NEEDS_CONTEXT` → surface the `blocker` field to the user, re-dispatch once after input
- `BLOCKED` → surface blocker, stop

## Phase 2: GENERATE

Dispatch **generator-agent**.

After completion, read `.playwright/orchestrator-status.json` and branch:
- `DONE` → write `GENERATE` to `.claude/qa-phase.txt`, proceed to Phase 3
- `NEEDS_CONTEXT` → surface blocker, re-dispatch once
- `BLOCKED` → surface blocker, stop

## Phase 3: EXECUTE

Dispatch **executor-agent**.

After completion, read `.playwright/orchestrator-status.json` and `.ai-failures.json`:
- `DONE` with zero locator failures → skip to Phase 5 (Report)
- `DONE` with locator failures → proceed to Phase 4 (Heal)
- `NEEDS_CONTEXT` → surface blocker, re-dispatch once
- `BLOCKED` → surface blocker, stop

Write `EXECUTE` to `.claude/qa-phase.txt`.

## Phase 4: HEAL

Read `.ai-failures.json`. Count locator-category entries (N).

### Dispatch

- **N == 0:** Skip healing. Proceed to Phase 5.
- **N < 5:** Single **healer-agent** with the full `.ai-failures.json` path.
- **N >= 5:** Parallel fan-out — one **healer-agent** per failure. Write single-item input files to `.playwright/healed/{test-name}-input.json`, launch all N agents in a single message. Each writes output to `.playwright/healed/{test-name}.json`.

### Aggregate and Route

After all healer results are collected:

1. **Update circuit breaker** (`.github/healing-state.json`): increment attempts per test, blocklist tests failing twice, increment PR counter.

2. **Route by confidence:** HIGH (>=0.85) → consolidated auto-merge PR. MEDIUM (0.60-0.84) → review PR. LOW (<0.60) → no PR, record as deferred. See @references/cicd-workflow.md for PR creation implementation and @references/confidence-scoring.md for threshold details.

3. **PR budget:** Max 3 PRs per session.

Write `HEAL` to `.claude/qa-phase.txt`.

## Phase 5: Report

Write `.playwright/session-report.md` summarizing: tests generated/passing/failing, locator failures found, healing outcomes by confidence tier, and artifact locations.

Report the summary to the user. Clear `.claude/qa-phase.txt`.

## Error Handling

If any agent dispatch fails (no output file, agent error):
- Report the failure phase and error to the user
- Preserve `.claude/qa-phase.txt` for session resumption
- Do not retry a failed phase more than once
