---
name: qa-orchestration
description: >
  Extension of agentic-delegation for the Playwright test lifecycle.
  Adds the Plan->Generate->Execute->Heal->Report loop, four-agent orchestration,
  confidence-based PR routing, circuit breaker safety, and session persistence.

  Hard preference: orchestration plugin (agentic-delegation skill).
  Same-plugin agents: planner-agent, generator-agent, executor-agent, healer-agent.

  Triggers: "run QA", "automate testing", "create and run Playwright tests",
  "set up E2E testing", "generate and execute tests", "run the full test pipeline",
  "heal broken tests", or mentions running the full Playwright test lifecycle.
---

# QA Orchestration

Extends agentic-delegation with the Playwright test lifecycle. The parent skill establishes the economics (agents are cheap, orchestrator context is expensive), the model ladder (haiku-first with upgrade-on-failure), execution patterns (parallel fan-out, sequential pipeline), and quality governance (re-launch principle, contradiction resolution). This skill adds the Plan->Generate->Execute->Heal->Report loop that governs how those patterns apply to automated testing.

If the orchestration plugin is installed, read agentic-delegation's SKILL.md before proceeding. If not installed, recommend installing it. Core principles: delegate aggressively (agents are cheap), the orchestrator's context is for decisions and dispatch (never for grunt work), agents communicate through files on disk (the orchestrator routes, never relays).

## Verb Interpretation

Every user verb implies agent-delegated execution. The orchestrator decomposes, dispatches, and assembles. It never executes directly.

- "run tests" / "run QA" -- dispatch the full Plan->Generate->Execute->Heal->Report loop.
- "generate tests" / "create tests" -- dispatch generator-agent (Phase 2).
- "heal tests" / "fix selectors" / "fix locators" -- dispatch healer-agent (Phase 4).
- "plan tests" / "explore the app" -- dispatch planner-agent (Phase 1).
- "execute tests" / "run the suite" -- dispatch executor-agent (Phase 3).
- "fix timing" / "fix test architecture" -- dispatch generator-agent in fix mode.

No exceptions. The orchestrator coordinates; agents act.

## System Architecture

### Parent Framework: agentic-delegation (orchestration plugin)

Provides: model ladder, decomposition patterns, execution patterns, quality governance (re-launch principle, contradiction resolution, concurrent file write prevention, independent verification), session persistence (ARRIVE/WORK/LEAVE lifecycle). This skill uses the parent's parallel fan-out (healing dispatch), sequential pipeline (phase ordering), status-driven branching, and file-based communication.

For multi-session QA work, the parent's session persistence protocol applies -- `conventions.md` holds QA-specific rules (locator strategy decisions, confidence threshold tuning, browser-specific patterns), `codebase_state.md` holds the test inventory and healing history, `deferred_items.md` tracks unresolved test failures deferred from healing.

### Agents

| Agent | Model | Role |
|-------|-------|------|
| planner-agent | sonnet | Explores live app via browser, produces test plan, page inventory, selector strategy |
| generator-agent | sonnet | Writes tests one-at-a-time with verify loop, accessibility-first locators. Owns structural test fixes (fix mode). |
| executor-agent | haiku | Runs tests via CLI, classifies failures into 6 categories, identifies healable locator failures |
| healer-agent | sonnet | Applies ten-tier locator algorithm, scores confidence, fixes locator-only failures |

### Artifact Contract

Canonical inventory. The table is authoritative; body prose may reference rows by ID and MUST NOT contradict them. `${stem}` = test filename stem; `${test-name}` = sanitized test title.

| ID | Path | Producer | Consumer | Format | Required |
|----|------|----------|----------|--------|----------|
| A1 | `.playwright/test-plan.md` | planner | generator | markdown | yes |
| A2 | `.playwright/pages.md` | planner | human (DOM quality review) | markdown | yes |
| A3 | `.playwright/selector-strategy.md` | planner | generator | markdown | yes |
| A4 | `.playwright/project-config.md` | planner | generator, human | markdown | yes |
| A5 | `.playwright/VERIFICATION.md` | planner | human | markdown | yes |
| A6 | `.playwright/snap-*.yaml` | planner | orchestrator (CLI Evidence Check) | yaml | yes |
| A7 | `.playwright/orchestrator-status.json` | every agent (overwritten per phase) | orchestrator | json | yes |
| A8 | `.claude/qa-phase.txt` | orchestrator | orchestrator | text | yes |
| A9 | `tests/seed.spec.ts` | human (initial); generator (regeneration) | every agent | typescript | yes |
| A10 | `tests/*.spec.ts` | generator | executor, healer | typescript | yes |
| A11 | `tests/pages/*.page.ts` | generator | tests (imported by `tests/*.spec.ts`) | typescript | conditional (when a flow has 5+ steps or repeats — see generator-agent.md "Page Objects") |
| A12 | `tests/fixtures.ts` | generator | tests, page objects | typescript | conditional (when page objects or worker fixtures exist) |
| A13 | `tests/helpers/test-data.ts` | generator | tests | typescript | conditional (when parallel tests conflict — see generator-agent.md "Test Data") |
| A14 | `.playwright/snap-gen-${stem}.yaml` | generator | orchestrator (Generator Live-Verification Check) | yaml | yes (one per new test) |
| A15 | `results.json` | executor | human (HTML report companion) | json | yes |
| A16 | `.ai-failures.json` | executor | orchestrator (Phase 4 routing), healer | json | yes |
| A17 | `playwright-report/` | executor | human | html dir | yes |
| A18 | `test-results/**/trace.zip` | executor | healer (debugging, optional) | zip | conditional (present when failures occur with tracing enabled) |
| A19 | `.healing-results.json` | healer (batch / N<5) | orchestrator (confidence routing) | json | conditional (batch mode: N<5) |
| A20 | `.playwright/healed/${test-name}.json` | healer (parallel / N>=5) | orchestrator (confidence routing) | json | conditional (parallel mode: N>=5) |
| A21 | `.github/healing-state.json` | orchestrator (post-aggregation write) | healer (pre-dispatch read) | json | yes after round 1 (healer treats absence as empty on first round) |
| A22 | `.playwright/lessons.md` | generator (fix mode), healer | generator, healer | markdown | conditional (absent on first run; agents skip-if-missing) |
| A23 | `.playwright/session-report.md` | orchestrator | human | markdown | yes |

Notes on producer/consumer accuracy:
- **A2 (pages.md):** planner-internal DOM quality output, NOT a generator input. Generator's Pre-Flight check and Reads list omit it; selector-strategy.md (A3) carries the actionable derivative.
- **A15 (results.json):** healer consumes the normalized form (`.ai-failures.json`, A16), not `results.json` directly.
- **A22 (lessons.md):** only generator-in-fix-mode and healer write it. Planner and executor do not.

### Status Protocol

Each agent writes `.playwright/orchestrator-status.json` on completion:

- **DONE** -- phase completed successfully
- **NEEDS_CONTEXT** -- agent needs user input
- **BLOCKED** -- unrecoverable error

Phase sequence: `PLAN` -> `GENERATE` -> `EXECUTE` -> `HEAL`. Written to `.claude/qa-phase.txt` after each phase completes. Read on session resumption to determine re-entry point.

### Multi-App Mode

Active when multiple base URLs are detected. Phase adaptations:

- **Plan:** Dispatch planner with all URLs. Produces per-app artifacts: `.playwright/pages-{app-name}.md`, `.playwright/selector-strategy-{app-name}.md`.
- **Generate:** Dual-context fixtures (one browser context per app). Comparison-as-findings pattern (log deltas, not absolute assertions).
- **Heal:** Per-app locator healing. `app_specific` field identifies which app's DOM changed.
- **Report:** Finding summary table replaces pass/fail for comparative tests.

Finding taxonomy:

| Status | Meaning |
|--------|---------|
| MATCH | Same value in both apps |
| MISMATCH | Different values -- flag for review |
| MISSING | Feature absent in one app |
| EXTRA | Feature present unexpectedly |

Findings are data for humans to interpret, not bugs for the healer to fix.

## Constraints

- Retry a failed phase once, then stop.
- Max 3 PRs per session.
- Preserve `.claude/qa-phase.txt` across failures for session resumption.
- The orchestrator never edits test files directly. Agents own all file mutations.

### Conflict Resolution

When a QA spec contradicts a project principle, the project principle wins. Flag the spec for correction. Document the conflict in `.playwright/lessons.md` with: the spec recommendation, the principle it violated, and the resolution applied. Specs serve projects, not the reverse.

### Generator-Agent Dispatch Modes

The generator-agent operates in three modes:

| Mode | Trigger | Input | Behavior |
|------|---------|-------|----------|
| **Create** | Phase 2 initial generation | Test plan + page inventory | Full plan-driven generation with verify loop |
| **Fix** | Timing/structural failures from Phase 3 | Failing test paths + error descriptions | Structural repair (waits, fixtures, architecture) |
| **Modify** | Targeted change to existing test | File path + modification prompt | The modification prompt IS the spec. Skip test-plan reading, skip verify loop. Direct surgical edit. |

Modify mode exists because the generator's create/fix protocol adds overhead (plan reading, verify loop) that provides no value for targeted edits like "add 20 lines to this test block." The modification prompt contains all context needed.

## Quality Gates

Three gates at three scopes:

| Scope | Gate | Mechanism |
|-------|------|-----------|
| Session entry | Seed health check | `tests/seed.spec.ts` must pass before any generation. Failing seed = invalid session. |
| Per-fix | Confidence scoring | Thresholds determine auto-merge ([0.85, 1.0]), review ([0.60, 0.85)), or defer ([0.0, 0.60)). Hard rejection at 0.0 for assertion failures, runtime errors, console fatal, mass clusters (10+ in same test run), zero-candidate. |
| Session limit | Circuit breaker | Max 2 healing attempts per test, max 3 PRs per session, blocklist for repeat offenders. |

## The QA Loop

```
Prerequisites -> Plan -> (Generate -> Execute -> Heal)* -> Report
```

The orchestrator drives this loop. The outer sequence is linear (Plan then inner loop then Report). The inner loop (Generate->Execute->Heal) repeats until an exit condition is met. Each phase dispatches one agent, reads its output files, and branches on status.

### Inner Loop Exit Conditions

Exit the Generate->Execute->Heal cycle when any of these is true:
- **All tests pass.** Zero failures of any category.
- **Only structural failures remain.** All locator failures healed; remaining failures are timing, assertion, or infrastructure issues requiring human intervention.
- **Circuit breaker trips.** Max healing attempts per test exceeded, or max PRs per session reached.
- **No progress.** A healing round produced zero successful fixes (same failures persist). Stop to prevent infinite looping.

## Prerequisites Check

Before any phase:

1. **Check `tests/seed.spec.ts` exists.** If missing, STOP. Tell the user a seed file is required. Seed must contain 5 components: import statement, navigation, interaction, assertion, accessibility-first locators.

2. **Check the base URL.** Extract from the user's argument, or check `.playwright/project-config.md`. If neither exists, ask the user.

3. **Session resumption.** Read `.claude/qa-phase.txt` if it exists. Resume from the phase after the one recorded (PLAN -> resume at GENERATE, etc.). If missing, start from Phase 1.

## Phase 1: PLAN

Record the dispatch start time: `T0=$(date +%s)`. Dispatch **planner-agent** with the base URL.

After completion, read `.playwright/orchestrator-status.json` and branch:
- `DONE` -> run Planner Completeness Check AND CLI Evidence Check, then write `PLAN` to `.claude/qa-phase.txt`, proceed to Phase 2
- `NEEDS_CONTEXT` -> surface the `blocker` field to the user, re-dispatch once after input
- `BLOCKED` -> surface blocker, stop

### Planner Completeness Check

Verify all 5 required artifacts exist:
1. `.playwright/test-plan.md`
2. `.playwright/pages.md`
3. `.playwright/selector-strategy.md`
4. `.playwright/project-config.md`
5. `.playwright/VERIFICATION.md`

If any are missing, re-dispatch planner-agent with explicit instructions to produce the missing artifacts.

### CLI Evidence Check

The planner explores via `@playwright/cli`, which writes accessibility snapshots to `.playwright/snap-*.yaml`. Snapshot absence proves non-CLI exploration (MCP-only, scripted, or fabricated from memory). Verify:

```bash
find .playwright -maxdepth 1 -name 'snap-*.yaml' -newermt "@$T0" | head -1
```

- **One or more matches** -> CLI evidence present, proceed.
- **Zero matches (first miss)** -> re-dispatch planner-agent with this added directive: `"MANDATORY: explore via @playwright/cli only. Each visited page MUST produce a .playwright/snap-<page>.yaml snapshot. Scripts that launch browsers are prohibited."` Reset `T0` before re-dispatch.
- **Zero matches (second miss)** -> escalate: write `NEEDS_CONTEXT` to `.playwright/orchestrator-status.json` with blocker `"planner produced no CLI snapshots across two dispatches; manual investigation required"` and stop.

NEVER mark Phase 1 complete on agent self-report alone. NEVER skip the CLI Evidence Check. NEVER accept a missing snapshot set with the rationale "the agent had a reason" — silent skip is the failure mode this check exists to catch.

## Phase 2: GENERATE

Snapshot the pre-dispatch test set: `BEFORE=$(ls tests/*.spec.ts 2>/dev/null | sort)`. Record `T0=$(date +%s)`. Dispatch **generator-agent**. Include `.playwright/lessons.md` path in the dispatch if it exists (agents read it before starting -- it contains discoveries from prior cycles).

After completion, read `.playwright/orchestrator-status.json` and branch:
- `DONE` -> run Generator Live-Verification Check, then write `GENERATE` to `.claude/qa-phase.txt`, proceed to Phase 3
- `NEEDS_CONTEXT` -> surface blocker, re-dispatch once
- `BLOCKED` -> surface blocker, stop

### Generator Live-Verification Check

The generator writes one snapshot per test to `.playwright/snap-gen-${stem}.yaml` (artifact A14). The `snap-gen-` prefix disambiguates from planner snapshots (A6). For each new test in `tests/${stem}.spec.ts`, a matching `snap-gen-${stem}*.yaml` MUST exist with mtime after `T0`:

```bash
AFTER=$(ls tests/*.spec.ts 2>/dev/null | sort)
NEW=$(comm -13 <(echo "$BEFORE") <(echo "$AFTER"))
for t in $NEW; do
  stem=$(basename "$t" .spec.ts)
  find .playwright -maxdepth 1 -name "snap-gen-${stem}*.yaml" -newermt "@$T0" | head -1
done
```

- **Every new test has a matching snapshot** -> verification evidence present, proceed.
- **Any new test lacks a snapshot (first miss)** -> re-dispatch generator-agent with this added directive: `"MANDATORY: for each test in tests/<name>.spec.ts, run the locator-verification step and persist the snapshot to .playwright/snap-gen-<name>.yaml. Tests written without a corresponding snapshot will be rejected."` Reset `T0` and `BEFORE` before re-dispatch.
- **Any new test still lacks a snapshot (second miss)** -> escalate: write `NEEDS_CONTEXT` to `.playwright/orchestrator-status.json` with blocker `"generator skipped live verification across two dispatches for tests: <list>; manual review required"` and stop.

### Generator Conditional-Artifact Check

The generator's status file (A7) lists produced artifacts in its `artifacts` field. For every conditional path it claims (A11 `tests/pages/*.page.ts`, A12 `tests/fixtures.ts`, A13 `tests/helpers/test-data.ts`), confirm the file exists on disk:

```bash
for path in $(jq -r '.artifacts[]?' .playwright/orchestrator-status.json); do
  case "$path" in tests/pages/*|tests/fixtures.ts|tests/helpers/*) test -s "$path" || echo "MISSING: $path";; esac
done
```

- **All claimed artifacts present** -> proceed.
- **Any missing (first miss)** -> re-dispatch generator-agent with the missing list as a NEEDS_CONTEXT correction directive.
- **Any missing (second miss)** -> escalate: write `NEEDS_CONTEXT` with blocker `"generator claimed artifacts not on disk across two dispatches: <list>"` and stop.

Orchestrator MUST run both checks before advancing to Phase 3. Orchestrator MUST NOT mark Phase 2 complete on agent self-report alone. NEVER accept a missing snapshot or a missing claimed artifact — the snapshot is the audit trail; the claimed-artifact list is the contract.

## Phase 3: EXECUTE

Record `T0=$(date +%s)`. Dispatch **executor-agent**. Include `.playwright/lessons.md` path if it exists.

After completion, read `.playwright/orchestrator-status.json` and run the Executor Output Check before reading `.ai-failures.json`.

### Executor Output Check

The executor's load-bearing artifact is `.ai-failures.json` (A16) — Phase 4 routing reads it. Verify:

```bash
test -s .ai-failures.json && jq -e '.summary and (.locator | type == "array")' .ai-failures.json >/dev/null
find . -maxdepth 1 -name results.json -newermt "@$T0" | head -1
```

- **Both checks pass** -> proceed to Failure Routing.
- **`.ai-failures.json` missing or schema-invalid (first miss)** -> re-dispatch executor-agent with directive: `"MANDATORY: write .ai-failures.json with the full schema (summary + per-category arrays). Status DONE without this file is invalid."` Reset `T0` before re-dispatch.
- **Still missing or invalid (second miss)** -> escalate: write `NEEDS_CONTEXT` to `.playwright/orchestrator-status.json` with blocker `"executor produced no valid .ai-failures.json across two dispatches"` and stop.

Orchestrator MUST NOT advance to Phase 4 without a valid `.ai-failures.json`. NEVER infer failures from `orchestrator-status.json` alone — its `healable_count` field is a summary, not the routing source of truth.

### Failure Taxonomy

Six categories by regex on error messages. Only locator failures are healable.

| Category | % | Regex | Healable? |
|----------|---|-------|-----------|
| locator | 28 | `/locator\.\|selector\|element not found\|waiting for\|getBy\|resolved to 0 elements\|resolved to hidden/i` | YES |
| timing | 30 | `/timeout\|timed out\|race condition\|navigation timeout\|waitFor.*exceeded/i` | NO |
| data | 14 | `/expected.*to(Equal\|Be\|Have\|Contain\|Match)\|AssertionError\|toHaveText\|toContain\|toHaveURL/i` | NO |
| visual | 10 | `/screenshot\|visual.*regression\|pixel.*diff\|snapshot.*mismatch\|toMatchSnapshot\|toHaveScreenshot/i` | NO |
| interaction | 10 | `/intercept\|not scrollable\|drag.*drop\|click.*intercepted\|obscured\|pointer.*event/i` | NO |
| other | 8 | everything else | NO |

### Failure Routing Decision Tree

```
Test fails ->
  Assertion/data match? -> DO NOT HEAL (real bug)
  Locator match? -> Verify: element found but assertion failed? Reclassify as DATA.
                    Console ERROR/FATAL? Reclassify as REAL BUG.
                    10+ concurrent failures? Reclassify as INFRASTRUCTURE.
                    Confirmed locator -> proceed to Phase 4
  Timing match? -> Re-dispatch generator-agent in fix mode (fix waits, not locators)
  Other? -> Manual investigation
```

### Test Completeness Gate

Before routing failures, check that passing tests are substantive. A test that navigates and logs "needs implementation" without asserting is a hollow pass. If passing tests lack real assertions (no `expect()`, no comparison logic), re-dispatch generator-agent to complete the hollow tests before proceeding.

### Failure Routing

- `DONE` with zero failures -> check exit conditions, proceed to Report or re-enter inner loop
- `DONE` with locator failures -> proceed to Phase 4 (Heal)
- `DONE` with timing failures where locators are correct but test structure is wrong (serial execution of independent tests, missing waits, fixture teardown races) -> re-dispatch **generator-agent** in fix mode with failing test paths and error descriptions
- `NEEDS_CONTEXT` -> surface blocker, re-dispatch once
- `BLOCKED` -> surface blocker, stop

Write `EXECUTE` to `.claude/qa-phase.txt`.

## Phase 4: HEAL

Read `.ai-failures.json`. Count locator-category entries (N). Record `T0=$(date +%s)`.

### Pre-Dispatch Circuit-Breaker Gate

Healers read `.github/healing-state.json` (A21) for blocklist + attempt counts. The orchestrator tracks the inner-loop round in its own context (round 1 = first entry into Phase 4 this session; round 2+ = re-entries after a prior heal cycle).

- **Round 1:** file may be absent — healers treat absence as empty. Proceed to Dispatch.
- **Round 2+:** the prior round's Aggregate and Route step MUST have persisted this file. Verify before dispatch:

  ```bash
  test -s .github/healing-state.json && jq -e '.healing_attempts' .github/healing-state.json >/dev/null
  ```

  If the file is absent or malformed in round 2+, abort the inner loop and surface to the user: the aggregation step failed to persist circuit-breaker state. Orchestrator MUST NOT dispatch healers in round 2+ without an authoritative state file.

### Dispatch

- **N == 0:** Skip healing. Check exit conditions.
- **N < 5:** Single **healer-agent** (batch mode) with the full `.ai-failures.json` path and `.playwright/lessons.md`. Expected output: `.healing-results.json` (A19).
- **N >= 5:** Parallel fan-out -- one **healer-agent** per failure (parallel mode). Write single-item input files to `.playwright/healed/{test-name}-input.json`, launch all N agents in a single message. Expected output: `.playwright/healed/${test-name}.json` per agent (A20).

### Confidence Scoring

Seven-signal weighted algorithm:

**Primary signals (70% weight):**
1. Error type analysis (max +0.30): ELEMENT_NOT_FOUND +0.30, ELEMENT_NOT_VISIBLE +0.25, ASSERTION -> 0.0
2. DOM change detection (max +0.20): attribute changes +0.20, relocated +0.15, removed +0.05, unchanged -0.15
3. Console/runtime errors (max +0.20): none +0.20, WARNING +0.10, ERROR/FATAL -> 0.0

**Secondary signals (30% weight):**
4. Network/API health (max +0.10): OK +0.10, errors -0.10
5. Element match quality (max +0.10): similarity * 0.10, no candidate -> 0.0
6. Historical pattern (max +0.05): stable +0.05, flaky -0.10
7. Cluster analysis (max +0.05): isolated +0.05, small cluster +0.03, large (10+) -0.15

**Tier adjustment:** tiers 1-3 +0.05, tiers 7-10 -0.05

### Hard Rejection (score = 0.0)

1. Assertion on element value -- real bug
2. Runtime errors / crashes -- application broken
3. Console errors ERROR/FATAL -- application broken
4. No candidate element found -- cannot heal
5. 10+ failures in the same test run -- infrastructure issue

### Decision Thresholds

| Score | Category | Action |
|-------|----------|--------|
| [0.85, 1.0] | HIGH | Auto-merge PR |
| [0.60, 0.85) | MEDIUM | Review PR (24h SLA) |
| [0.40, 0.60) | LOW | No PR, defer |
| [0.0, 0.40) | REJECT | Skip |

### Circuit Breaker

Schema (`.github/healing-state.json`):
```json
{"healing_attempts":{"file:line:title":1},"prs_created":0,"blocklist":[],"last_updated":"ISO-8601"}
```

Rules:
- Max 2 healing attempts per test (key: `"file:line:title"`)
- Max 3 PRs per session
- Tests failing healing twice added to blocklist
- Blocklisted tests skipped until manually removed

### Cost Model

| Method | Token Cost | Time | FP Rate |
|--------|-----------|------|---------|
| Deterministic (ten-tier) | 0 tokens | 1-3s per failure | 2-5% |
| LLM fallback | ~10K tokens per failure | 30-60s per failure | 8-15% |

Run deterministic healing first. LLM fallback only when deterministic fails. Max confidence for LLM fixes: MEDIUM. Never auto-apply LLM fixes.

### Healer Output Check

Confidence routing depends on the healer's per-failure records (confidence, tier, original/healed locator). The status file (A7) carries summary counts only — it is NOT the routing source of truth.

```bash
case "$MODE" in
  batch)    test -s .healing-results.json && jq -e '.results | type == "array"' .healing-results.json >/dev/null ;;
  parallel) ls .playwright/healed/*.json 2>/dev/null | grep -v -- '-input\.json$' | head -1 ;;
esac
```

- **Expected file(s) present and well-formed** -> proceed to Aggregate and Route.
- **Missing or malformed (first miss)** -> re-dispatch the failed healer(s) with directive: `"MANDATORY: write per-failure output to <expected path>. Status DONE without this file is invalid."`
- **Missing or malformed (second miss)** -> escalate: write `NEEDS_CONTEXT` with blocker `"healer produced no valid output across two dispatches in <mode> mode"` and stop.

Orchestrator MUST NOT enter confidence routing without verified healer output. NEVER infer fix decisions from `orchestrator-status.json` counts alone.

### Aggregate and Route

After the Healer Output Check passes:

1. **Read healer output:** `.healing-results.json` (batch) or `.playwright/healed/${test-name}.json` files (parallel).

2. **Update circuit breaker** (`.github/healing-state.json`, A21): increment attempts per test, blocklist tests failing twice, increment PR counter. Confirm the write succeeded before exiting the round:

   ```bash
   test -s .github/healing-state.json && jq -e '.healing_attempts' .github/healing-state.json >/dev/null \
     || { echo "ABORT: failed to persist healing-state.json"; exit 1; }
   ```

   Orchestrator MUST persist this file before re-entering the inner loop. The next round's Pre-Dispatch Circuit-Breaker Gate enforces the read side.

3. **Route by confidence:** HIGH -> consolidated auto-merge PR. MEDIUM -> review PR. LOW -> no PR, record as deferred.

4. **PR budget:** Max 3 PRs per session.

### Update Lessons

After aggregating healer results, append discoveries to `.playwright/lessons.md`:
- Selectors that failed and why (prevents repeating same guesses)
- Patterns that worked (successful tier/locator combinations)
- Structural issues found (timing, fixture, architecture problems)

Write `HEAL` to `.claude/qa-phase.txt`. Check exit conditions -- proceed to Report or re-enter inner loop at GENERATE.

## Phase 5: Report

Validate findings before reporting. Generator must not log implementation gaps (harness errors, placeholder logic) as business findings. If findings exist, verify each has non-placeholder values (not 'TODO', 'needs implementation', empty strings). Strip or flag invalid findings.

Write `.playwright/session-report.md`:

```
# QA Automation Session Report
Date | Duration | Phases Completed
## Test Results
Total | Passed | Failed | Healed | Deferred
## Healing Summary
Per-tier breakdown with confidence averages
## Deferred
Test file:line -- reason -- confidence
## Artifacts
Links to test-plan, healing-results, HTML report, healed outputs
```

Report summary to user. Clear `.claude/qa-phase.txt`.

Exclude from user-facing summary: raw JSON artifacts, trace file paths, internal status file contents.

## Error Handling

If any agent dispatch fails (no output file, agent error):
- Report the failure phase and error to the user
- Preserve `.claude/qa-phase.txt` for session resumption
- Retry a failed phase once, then stop

If exit condition is ambiguous (hollow passes mixed with real passes): re-enter at GENERATE to complete hollow tests.

If status contradicts (phase.txt says EXECUTE but orchestrator-status.json says PLAN): surface the contradiction to the user and ask for direction.

If `.playwright/orchestrator-status.json` is missing after agent dispatch: treat as agent failure, report to user.

If `.github/healing-state.json` is corrupt or unparseable: reset to empty state `{"healing_attempts":{},"prs_created":0,"blocklist":[]}` and continue.
