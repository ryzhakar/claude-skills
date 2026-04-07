---
name: qa-run
description: >
  This skill should be used when the user asks to "run QA", "automate testing",
  "create and run Playwright tests", "set up E2E testing", "generate and execute tests",
  "run the full test pipeline", "heal broken tests", or mentions running the full
  Playwright test lifecycle. Requires a base URL and a seed file (tests/seed.spec.ts).
  Sequences plan, generate, execute, and heal autonomously. Surfaces to the user only
  when blocked on missing input.
version: 2.0.0
---

# QA Automation Orchestrator

Coordinate the full Playwright test lifecycle by dispatching four agents in sequence.
Do not execute phase work directly — dispatch agents, read their output files, and branch.

## Prerequisites Check

Before any phase, verify:

1. **Seed file exists:** `ls tests/seed.spec.ts`
   If missing: STOP. Tell the user: "A seed file is required at tests/seed.spec.ts.
   See @references/seed-file-spec.md for the template. Create one and re-invoke /qa-run."

2. **Base URL known:** Extract from the user's argument (`$ARGUMENTS`), or check
   .playwright/project-config.md. If neither exists: ask the user for the base URL.

3. **Existing session:** Read `.claude/qa-phase.txt` if it exists.
   Resume from the phase AFTER the one recorded:
   - File says PLAN: resume from Phase 2 (GENERATE)
   - File says GENERATE: resume from Phase 3 (EXECUTE)
   - File says EXECUTE: resume from Phase 4 (HEAL)
   - File says HEAL: session already complete — report and clear
   - File missing or empty: start from Phase 1 (PLAN)
   Tell the user: "Resuming QA session from [phase] phase."

## Phase 1: PLAN

Dispatch the **planner-agent** via the Agent tool. Pass the base URL in the prompt.

After the agent completes, read `.playwright/orchestrator-status.json`.

Branch on `status`:
- `DONE`: proceed to Phase 2. Write `PLAN` to `.claude/qa-phase.txt`.
- `NEEDS_CONTEXT`: surface the `blocker` field to the user. Wait for input.
  After user responds, re-dispatch planner-agent once. If still NEEDS_CONTEXT, stop.
- `BLOCKED`: surface `blocker` to the user. Stop.

## Phase 2: GENERATE

Dispatch the **generator-agent** via the Agent tool.

After completion, read `.playwright/orchestrator-status.json`.

Branch on `status`:
- `DONE`: proceed to Phase 3. Write `GENERATE` to `.claude/qa-phase.txt`.
- `NEEDS_CONTEXT`: surface blocker. Wait for input. Retry once.
- `BLOCKED`: surface blocker. Stop.

## Phase 3: EXECUTE

Dispatch the **executor-agent** via the Agent tool.

After completion, read `.playwright/orchestrator-status.json` and `.ai-failures.json`.

Branch:
- `DONE` and `.ai-failures.json` has zero locator entries: skip to Phase 5 (Report).
- `DONE` and locator entries present: proceed to Phase 4 (HEAL).
- `NEEDS_CONTEXT`: surface blocker. Wait. Retry once.
- `BLOCKED`: surface blocker. Stop.

Write `EXECUTE` to `.claude/qa-phase.txt`.

## Phase 4: HEAL

Read `.ai-failures.json`. Count entries in the `locator` array (N).

### Dispatch

**If N == 0:** Skip healing entirely. Proceed to Phase 5.

**If N < 5:** Dispatch a single **healer-agent** with the full `.ai-failures.json` path.
Wait for completion. Read `.healing-results.json`.

**If N >= 5:** Dispatch N **healer-agents** in parallel (one per failure):
1. For each locator failure, write a single-item input file to
   `.playwright/healed/{test-name}-input.json` containing that failure's entry.
2. Launch all N agents in a single message, each pointing to its input file.
   Each writes output to `.playwright/healed/{test-name}.json`.
3. Wait for all completions. Read all output files:
   `ls .playwright/healed/*.json | grep -v '\-input\.json'`

### Aggregate and Route

After all healer results are collected (from `.healing-results.json` or individual files):

**Update circuit breaker** (`.github/healing-state.json`):
- Increment `healing_attempts` for each attempted test (key: "file:line:title")
- Tests failing healing twice: add to `blocklist`
- Increment `prs_created` for each PR created below

**Create PRs by confidence score:**

- **>= 0.85 (HIGH):** Collect all HIGH fixes. Create ONE consolidated branch and PR:
  ```
  git checkout -b healer/auto-fix-$(date +%s)
  git add tests/
  git commit -m "fix(tests): auto-heal locator failures (HIGH confidence)"
  git push origin HEAD
  gh pr create --title "fix(tests): Auto-heal locator failures" \
    --body "Deterministic healing. Tests re-validated. All fixes >= 0.85 confidence."
  gh pr merge --auto --squash
  ```

- **0.60-0.84 (MEDIUM):** Collect MEDIUM fixes. Create ONE review PR:
  ```
  git checkout -b healer/review-fix-$(date +%s)
  git add tests/
  git commit -m "fix(tests): heal locator failures (MEDIUM confidence, review required)"
  git push origin HEAD
  gh pr create --title "fix(tests): Heal locators (REVIEW REQUIRED)" \
    --body "Medium confidence healing. Review changes before merging."
  ```

- **< 0.60 (LOW/REJECT):** No PR. Record as deferred in results.

- **PR budget:** Max 3 PRs per session. After 3, stop creating PRs but still apply HIGH fixes inline.

Write `HEAL` to `.claude/qa-phase.txt`.

## Phase 5: Report

Write `.playwright/session-report.md`:

```markdown
# QA Session Report
Date: [ISO timestamp]
Base URL: [url]

## Results
Tests generated: N
Tests passing: N
Tests failing: N

## Healing
Locator failures found: N
Auto-healed (HIGH): N
Review PRs opened (MEDIUM): N
Deferred to manual (LOW): N

## Artifacts
- Test plan: .playwright/test-plan.md
- Generated tests: tests/*.spec.ts
- Execution report: playwright-report/index.html
- Failure classification: .ai-failures.json
- Healing results: .healing-results.json
```

Report the summary to the user. Clear `.claude/qa-phase.txt`.

## Error Handling

If any agent dispatch fails (no output file written, agent error):
- Report the failure phase and error to the user
- Preserve `.claude/qa-phase.txt` so the session can be resumed
- Do not retry a failed phase more than once

## References

Read these files from disk for artifact schemas and directory conventions:
- @references/file-protocol.md — artifact map and directory structure
- @references/mcp-tools.md — CLI-vs-MCP guidance for agent dispatch context
