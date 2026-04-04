---
name: test-executor
description: >
  Execute Playwright test suites, classify failures by type, and produce structured reports.
  Use when "run tests", "execute Playwright tests", "run E2E tests", "check test results",
  "run cross-browser tests", "why did tests fail", "classify test failures", "detect flaky tests",
  or after test-generator produces .spec.ts files. CLI-exclusive (not MCP). Outputs JSON reports
  with failure classification (locator, timing, data, visual, interaction, other) for test-healer.
---

# Test Executor

Execute Playwright tests, parse JSON results, classify failures into six healable categories, and produce structured failure reports. CLI-exclusive -- test execution cannot run through MCP.

## Core Principle

Every failure must be classified so downstream healing can act on it. The JSON reporter is the single source of truth for failure data. Traces are binary artifacts for human debugging only -- never attempt to parse them programmatically.

## Workflow

### Phase 1: Verify Prerequisites

Before running tests:

1. Verify test files exist: `ls tests/*.spec.ts`
2. Verify Playwright installed: `npx playwright --version`
3. Install browsers if needed: `npx playwright install --with-deps`
4. Run seed file first: `npx playwright test tests/seed.spec.ts --reporter=json,line`. If seed fails, environment is broken -- report error and stop.
5. Check dev server running (if required):
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
   ```
   If server not running and `playwright.config.ts` lacks a `webServer` block, instruct user to start server.
6. Verify `playwright.config.ts` has JSON reporter configured. If missing, reference @references/playwright-config.md for the recommended configuration.

### Phase 2: Execute Tests

**Full suite:**
```bash
npx playwright test --reporter=json,html,line
```

JSON reporter writes `results.json` (configurable in config). Line reporter provides console output. HTML reporter generates `playwright-report/`.

**Targeted execution:**

| Scope | Command |
|-------|---------|
| Specific file | `npx playwright test tests/auth.spec.ts --reporter=json,html,line` |
| Pattern match | `npx playwright test --grep "login" --reporter=json,html,line` |
| Single browser | `npx playwright test --project=chromium --reporter=json,html,line` |
| CI shard | `npx playwright test --shard=1/4 --reporter=json,html,line` |

**Trace collection:** Configure `trace: 'on-first-retry'` in `playwright.config.ts`. Captures traces only when tests fail and retry -- small output, full diagnostics.

**WASM/Leptos timing:** For Leptos, SvelteKit, or WASM-hydrated frameworks, use `domcontentloaded` with 150ms buffer -- NOT `networkidle`. The Playwright team officially discourages `networkidle` (GitHub #22897). WASM hydration makes no network calls -- it loads the bundle and hydrates synchronously -- so `networkidle` is completely unreliable. See @references/playwright-config.md for navigation helpers.

### Phase 3: Parse Results

Read `results.json` and extract: total tests, passed, failed, skipped, duration, per-test error messages with file paths and line numbers, attachment paths (screenshots, traces).

Present a summary to the user showing counts and listing each failure with its file:line, test title, browser project, and error message.

### Phase 4: Classify Failures

Apply regex-based classification to each failure. See @references/failure-classification.md for the complete pattern set and output format.

**Six categories:**

| Category | Share | Healable? | Signal |
|----------|-------|-----------|--------|
| Locator | 28% | YES | Element not found or not interactable |
| Timing | 30% | NO (fix waits) | Timeout waiting for condition |
| Data/assertion | 14% | NEVER | Element found, value wrong -- real bug |
| Visual | 10% | NO (manual) | Screenshot diff or layout shift |
| Interaction | 10% | NO (manual) | Click intercepted, not scrollable |
| Other | 8% | NO (manual) | Browser crash, OOM, infra error |

Write the classified failures to `.ai-failures.json` following the schema in @references/failure-classification.md.

### Phase 5: Detect Flaky Tests

A test is flaky if it fails intermittently (2-98% failure rate). Flaky tests are NOT candidates for locator healing.

Quick check -- re-run failed tests with retries:
```bash
npx playwright test --retries=2 --reporter=json tests/checkout.spec.ts
```

If first attempt fails but retry passes, flag as flaky. Categories (from @references/failure-classification.md):
- Async Wait (45%) -- missing waits or `waitForTimeout` instead of web-first assertions
- Race Conditions (24%) -- fails with `--workers>1`, passes with `--workers=1`
- Resource-Affected (46.5%) -- passes locally, fails on CI
- Network Issues (9%) -- API timeouts
- Environment Differences (12%) -- platform or browser-specific

(Categories overlap -- a single flaky test may match multiple categories.)

### Phase 6: Cross-Browser Analysis

Analyze per-browser failures:

- **Single-browser failure:** Likely browser-specific locator issue. Known patterns:
  - WebKit: `getByRole('list')` fails on styled lists with `list-style: none`
  - Firefox: caption/alert/combobox/form roles with name filters return empty strings
  - Chromium: most permissive accessibility tree

- **All-browser failure:** Likely real bug or universally broken locator.

Flag browser-specific failures with `browser_specific: true` so healer applies targeted fixes. See @references/failure-classification.md for known browser patterns.

### Phase 7: Present Results and Next Steps

1. **All pass:** Report success.
2. **Locator failures:** Inform user that test-healer can attempt automated repair. Present count, ask to proceed.
3. **Timing failures:** Recommend proper waits. Do NOT recommend locator healing. Suggest `--retries=2` to confirm flakiness.
4. **Data/assertion failures:** Flag as potential real bugs. Investigate application behavior, not test code.
5. **Visual/interaction/other:** Recommend manual investigation via `npx playwright show-report` or `npx playwright show-trace test-results/path/to/trace.zip`.

## Composability

If test-healer skill available:
  After classifying failures, suggest invoking test-healer for locator failures.
  Healer reads `.ai-failures.json` directly -- do not relay failure content through context.
Otherwise:
  Present failures with enough detail for manual debugging.

If systematic-debugging skill available:
  For data/assertion failures indicating real bugs, suggest systematic-debugging
  for root-cause investigation before attempting fixes.
Otherwise:
  Recommend checking recent code changes, console errors, API responses.

If agentic-delegation skill available:
  For large test suites (50+ tests), suggest fan-out execution across agents,
  one per shard. Each agent runs shard and writes results to numbered JSON file.
Otherwise:
  Run sequentially or with Playwright parallelism (`--workers=auto`).

## References

- @references/failure-classification.md -- Six-category classification patterns, regex rules, output schema, browser-specific flags, flaky test taxonomy
- @references/playwright-config.md -- Recommended Playwright configuration: cross-browser projects, reporters, trace settings, WASM navigation helpers
- @../../references/file-protocol.md -- File protocol specifications
- @../../references/mcp-tools.md -- MCP tool usage guidelines
