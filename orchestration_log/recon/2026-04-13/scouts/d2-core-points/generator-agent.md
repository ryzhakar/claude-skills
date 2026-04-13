# Core Points Extraction: generator-agent

## Iteration 1

**Point**: The agent operates in two distinct modes (create and fix) where create mode generates new tests from plans one at a time, and fix mode repairs structural test architecture problems that the healer cannot handle.

**Evidence**:
1. Lines 33-38: "You transform test plans into executable Playwright .spec.ts files AND fix structural issues in existing tests. Two modes: **Create mode** (default): generate new tests from `.playwright/test-plan.md`, one at a time **Fix mode**: repair existing tests with structural problems (timing, fixture races, test architecture). Dispatched when the executor classifies failures as non-locator issues that the healer cannot handle."
2. Lines 176-184: "When dispatched with specific test files and failure descriptions (not a test plan): ### Input You receive: - Path(s) to failing test file(s) - Failure descriptions from the executor (error messages, category: timing/interaction/other) - `.playwright/lessons.md` if it exists"
3. Lines 19-25: Example shows "Timing failures are structural, not locator issues. Re-dispatching generator-agent in fix mode." with commentary "Timing failures where locators are correct route to generator (fix mode), not healer."

## Iteration 2

**Point**: The generator must verify every locator against the live DOM using playwright-cli before writing any test, because documentation-based selectors without verification caused 5 field failures.

**Evidence**:
1. Lines 91-98: "**Step 1: Verify Locators Before Writing (MANDATORY)** Before writing a test, verify planned locators exist in the live DOM using playwright-cli. Do not write selectors from documentation alone — 5 locator failures in field testing traced to selectors that were never verified against the live page: 1. `playwright-cli goto <page-url>` 2. `playwright-cli snapshot --filename=/tmp/gen-snap.yaml` 3. Read snapshot — confirm element refs match planned locators 4. If locator doesn't exist: update the test plan, don't write a broken test"
2. Lines 193-194 in Fix Mode: "3. **Verify locators are correct.** If the locator is also broken, fix the locator too — but the dispatch came here because the primary issue is structural. Use playwright-cli to verify."
3. Line 91 marks this as "(MANDATORY)" reinforcing its critical importance.

## Iteration 3

**Point**: Tests must never be hollow placeholders without real assertions because they create false confidence; unimplementable tests must be marked as test.skip with a reason rather than passing without meaningful expectations.

**Evidence**:
1. Lines 51-53: "**No hollow tests.** Every test must contain at least one real assertion (`expect()`) or comparison. A test that navigates to a page and logs 'needs implementation' is not a test — it's a placeholder that creates false confidence. If you cannot write a meaningful assertion, write the test as `test.skip` with a reason, not as a passing hollow test."
2. Lines 54-55: "**No fake findings.** Never log implementation gaps, harness errors, or test infrastructure issues as business findings. Harness errors are test failures. Implementation gaps are blockers. Neither are findings."
3. The bundling of these two rules (51-55) under "Hard Rules" emphasizes their emphatic importance in preventing false signals.

## Iteration 4

**Point**: The generator enforces strict one-at-a-time test creation with mandatory green status before proceeding, stopping completely after 3 failed fix attempts rather than continuing with broken tests.

**Evidence**:
1. Lines 46-47 (Hard Rule 3): "**One test at a time.** Write ONE test, run it, fix until green, THEN write the next. Never batch-generate. Never proceed past a failing test."
2. Lines 128-130: "If failing, diagnose (locator not found, timeout, assertion mismatch), fix, re-run. Max 3 fix iterations. If still failing after 3 attempts, write status file with blocker and STOP. Do NOT move to next test until current test passes."
3. Lines 100-101 (Step 2 heading): "**Step 2: Write ONE Test**" and the all-caps emphasis in "ONE" throughout the workflow section reinforces the pervasive nature of this constraint.

## Iteration 5

**Point**: The seed file at tests/seed.spec.ts is a mandatory prerequisite that must exist and pass before any generation work begins, with failure requiring immediate stop and NEEDS_CONTEXT status.

**Evidence**:
1. Lines 42-43 (Hard Rule 1): "**Seed file is mandatory.** If `tests/seed.spec.ts` is missing or failing, STOP. Write `.playwright/orchestrator-status.json` with status `NEEDS_CONTEXT` and blocker message. Do not proceed."
2. Lines 70-81: "Run the seed test: ```bash npx playwright test tests/seed.spec.ts ``` If it fails, STOP. Write `.playwright/orchestrator-status.json`: ```json { \"status\": \"NEEDS_CONTEXT\", \"blocker\": \"Seed test failing: [error message]. Fix seed.spec.ts before generating tests.\" }```"
3. Lines 4-7 in the description frontmatter: "Requires tests/seed.spec.ts" is called out as a fundamental dependency in the agent's description itself.

## Rank Summary

1. **Two-mode operation (create/fix)** — defines the agent's core identity and dispatch routing from other agents (executor → generator fix mode vs. planner → generator create mode)
2. **Mandatory live DOM verification before writing** — prevents the most common failure mode (5 documented field failures), requires playwright-cli snapshot workflow
3. **Strict one-at-a-time with green gate** — architectural constraint that prevents cascading failures and ensures quality (3-attempt limit, STOP on failure)
4. **No hollow tests** — quality gate preventing false confidence from placeholder assertions or mislabeled infrastructure failures
5. **Seed file prerequisite** — operational gate that blocks all work until the baseline test passes
