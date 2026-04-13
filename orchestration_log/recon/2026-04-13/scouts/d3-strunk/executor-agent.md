# Strunk Analysis: executor-agent.md

## Critical & Severe

### R10 (Active Voice) - Severe
**Line 4:** "Use this agent to execute Playwright test suites via CLI, classify every failure into six categories, detect flaky tests, and produce .ai-failures.json."
- Good: All active verbs (execute, classify, detect, produce)
- No violation

**Line 30:** "Execute Playwright test suites, classify failures by type, detect flaky tests, and write structured reports."
- Good: All imperatives (active)
- No violation

**Line 60:** "CRITICAL: `healable_count` = locator failures ONLY. Timing failures are NOT healable."
- Good: Active construction with strong emphasis
- No violation

### R12 (Concrete Language) - Severe
**Line 52-59:** Failure classification regex patterns
```
- **locator** (28%): `/locator\.|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden/i`
- **timing** (30%): `/timeout|timed out|race condition|navigation timeout|waitFor.*exceeded/i`
```
- Excellent: Specific regex patterns, concrete percentages, actual error text
- No violation

**Line 66:** "Re-run failed tests: `npx playwright test --retries=2 --reporter=json tests/failing.spec.ts`"
- Excellent: Concrete command with specific flags
- No violation

### R11 (Positive Form) - Severe
**Line 60:** "Timing failures are NOT healable. Do not include timing in healable_count."
- Double negative construction
- Severity: Severe (critical operational instruction)
- Suggested revision: "Only locator failures are healable. Exclude timing failures from healable_count."

## Moderate

### R13 (Needless Words) - Moderate
**Line 4:** "CLI-exclusive — never uses MCP for test execution."
- "never uses" could be "excludes"
- Severity: Minor
- Suggested revision: "CLI-exclusive — excludes MCP for test execution."

**Line 36:** "Before running tests:"
- Concise
- No violation

**Line 39:** "Run seed health check: `npx playwright test tests/seed.spec.ts --reporter=json,line`"
- Concise and concrete
- No violation

**Line 41:** "If seed fails: write `.playwright/orchestrator-status.json` with `"status":"NEEDS_CONTEXT","blocker":"Seed file failing — environment broken"`"
- Clear conditional structure
- No violation

### R15 (Parallel Construction) - Moderate
**Lines 35-42:** Pre-Flight Checks list
```
1. Verify test files: `ls tests/*.spec.ts`
2. Verify Playwright: `npx playwright --version` (install if missing)
3. Install browsers: `npx playwright install --with-deps` (if needed)
4. Run seed health check: `npx playwright test tests/seed.spec.ts --reporter=json,line`
5. Check dev server if `playwright.config.ts` lacks `webServer` block: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`
```
- Inconsistent: Steps 1-4 start with imperative verbs; step 5 starts with conditional "Check dev server if..."
- Severity: Moderate
- Suggested revision: "5. Check dev server (if `playwright.config.ts` lacks `webServer`): `curl...`" to match imperative pattern

**Lines 78-83:** Outputs list
```
- `results.json` (Playwright JSON report)
- `.ai-failures.json` (classified failures)
- `playwright-report/` (HTML report)
- `test-results/**/trace.zip` (traces for manual debugging)
```
- Good: All items follow "filename (description)" pattern
- No violation

### R18 (Emphatic Position) - Moderate
**Line 30:** "You are CLI-exclusive — MCP has no test execution capability."
- Ends strongly with emphatic denial of MCP capability
- Good
- No violation

**Line 60:** "CRITICAL: `healable_count` = locator failures ONLY. Timing failures are NOT healable. Do not include timing in healable_count."
- Third sentence ends weakly with "healable_count" (technical term, not key concept)
- Severity: Minor
- Suggested revision: End with stronger point: "CRITICAL: Only locator failures count as healable. Timing failures are NOT healable. Exclude timing failures from healable_count."

## Minor & Stylistic

### R13 (Needless Words) - Minor
**Line 48:** "Read `results.json` and parse: total tests, passed, failed, skipped, duration, per-test error messages with file:line, browser project, attachment paths."
- "Read `results.json` and parse" → "Parse `results.json` for"
- Severity: Minor
- Suggested revision: "Parse `results.json` for: total tests, passed, failed, skipped, duration, per-test error messages with file:line, browser project, attachment paths."

**Line 98:** "If seed fails or environment broken: `"status":"NEEDS_CONTEXT","blocker":"<reason>"`"
- "seed fails or environment broken" could be tighter
- Severity: Minor
- Suggested revision: "If seed or environment fails: `"status":"NEEDS_CONTEXT","blocker":"<reason>"`"

### R11 (Positive Form) - Minor
**Line 36:** "Before running tests:"
- Positive temporal marker
- No violation

**Line 70:** "Flaky tests are NOT candidates for locator healing."
- Negative construction
- Severity: Minor
- Suggested revision: "Exclude flaky tests from locator healing."

### R10 (Active Voice) - Minor
**Line 41:** "If seed fails: write `.playwright/orchestrator-status.json`..."
- Good: Active imperative "write"
- No violation

**Line 98:** "Write `.playwright/orchestrator-status.json`:"
- Good: Active imperative
- No violation

## Summary

**Strengths:**
- Exceptionally concrete with specific regex patterns, percentages, and command examples
- Strong use of active voice throughout
- Technical precision in classification logic
- Clear imperative instructions

**Priority fixes:**
1. Line 60 (R11 Severe): Convert critical double-negative instruction to positive form
2. Lines 35-42 (R15 Moderate): Standardize pre-flight checklist parallel structure
3. Line 48 (R13 Minor): Reduce "read and parse" redundancy

**Total findings:**
- Critical/Severe: 1 (positive form in critical instruction)
- Moderate: 3 (1 parallel construction, 1 emphatic position, 1 needless words borderline)
- Minor/Stylistic: 4 (2 needless words, 2 positive form)
