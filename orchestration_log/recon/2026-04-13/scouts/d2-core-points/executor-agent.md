# Core Points: executor-agent

Source: /Users/ryzhakar/pp/claude-skills/qa-automation/agents/executor-agent.md

## Iteration 1

**Point:** The executor-agent is strictly CLI-exclusive for test execution and never uses MCP because MCP has no test execution capability.

**Evidence:**
- Line 4: "CLI-exclusive — never uses MCP for test execution."
- Line 30: "You are CLI-exclusive — MCP has no test execution capability."
- Lines 45-46: All execution commands are `npx playwright test` CLI commands

## Iteration 2

**Point:** Healable count must only include locator failures, never timing failures, despite timing being the most common failure type.

**Evidence:**
- Line 60: "**CRITICAL:** `healable_count` = locator failures ONLY. Timing failures are NOT healable. Do not include timing in healable_count."
- Line 94: Status file schema shows `"healable_count": <locator_failure_count>`
- Lines 53-54: Locator failures are 28% while timing failures are 30%, yet only locator failures count as healable

## Iteration 3

**Point:** Seed file health check is a mandatory gate that blocks execution if the environment is broken, not just a diagnostic step.

**Evidence:**
- Line 39: "Run seed health check: `npx playwright test tests/seed.spec.ts --reporter=json,line`"
- Line 40: "If seed fails: write `.playwright/orchestrator-status.json` with `"status":"NEEDS_CONTEXT","blocker":"Seed file failing — environment broken"`"
- Line 98: Environment broken triggers `"status":"NEEDS_CONTEXT","blocker":"<reason>"` instead of proceeding

## Iteration 4

**Point:** Flaky test detection through retries is essential because flaky tests must be excluded from locator healing candidacy.

**Evidence:**
- Line 66: "Re-run failed tests: `npx playwright test --retries=2 --reporter=json tests/failing.spec.ts`"
- Line 68: "If retry passes: flag `flaky: true`. Flaky tests are NOT candidates for locator healing."
- Line 104: References `@references/failure-heuristics.md — classification decision tree, regex patterns, flaky taxonomy`

## Iteration 5

**Point:** Cross-browser failure patterns distinguish browser-specific locator issues from real bugs, with different browsers having different accessibility capabilities.

**Evidence:**
- Line 72: "Single-browser failure: browser-specific locator issue (WebKit list role, Firefox caption/alert/combobox/form name filters, Chromium most permissive)"
- Line 73: "All-browser failure: real bug or universally broken locator"
- Line 75: "Flag with `browser_specific: true` when applicable."

## Rank Summary

1. **CLI-exclusive execution** — Architectural constraint that defines the agent's entire operational mode
2. **Healable count = locator only** — Critical business logic that directly impacts the healing phase workflow
3. **Seed health check gate** — Mandatory blocker that prevents wasted work in broken environments
4. **Flaky detection excludes healing** — Quality filter that prevents false-positive healing attempts
5. **Cross-browser pattern analysis** — Diagnostic capability that separates environmental issues from real defects
