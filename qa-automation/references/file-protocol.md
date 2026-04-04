# File Communication Protocol

All QA automation skills communicate through durable file artifacts written to disk. Skills never relay test content through conversation context -- they write to a path and tell the next skill where to read.

## Core Rule

Skills do NOT summarize or relay content. They point to files.

```
CORRECT:
  Planner writes to .playwright/test-plan.md
  User tells Generator: "Generate tests from the plan"
  Generator reads .playwright/test-plan.md directly

WRONG:
  Planner writes plan
  Orchestrator reads plan, summarizes it, passes summary to Generator
  Generator works from summary (lossy, hallucination-prone)
```

## Artifact Map

| Artifact | Producer | Consumer | Format | Location |
|----------|----------|----------|--------|----------|
| Test Plan | test-planner | test-generator, human | Markdown | `.playwright/test-plan.md` |
| Page Inventory | test-planner | test-generator | Markdown with checkboxes | `.playwright/pages.md` |
| Selector Strategy | test-planner | test-generator | Markdown | `.playwright/selector-strategy.md` |
| Project Config | test-planner | test-generator | Markdown | `.playwright/project-config.md` |
| Verification Evidence | test-planner | human | Markdown | `.playwright/VERIFICATION.md` |
| Test Files | test-generator | test-executor, test-healer | TypeScript | `tests/*.spec.ts` |
| Page Objects | test-generator | test-executor | TypeScript | `tests/pages/*.page.ts` |
| Fixtures | test-generator | all test skills | TypeScript | `tests/fixtures.ts` |
| Test Data Helpers | test-generator | test files | TypeScript | `tests/helpers/test-data.ts` |
| Seed File | human or test-generator | all test skills | TypeScript | `tests/seed.spec.ts` |
| Test Results | test-executor | test-healer | JSON | `results.json` |
| Failure Classification | test-executor | test-healer | JSON | `.ai-failures.json` |
| Healing Results | test-healer | CI/CD | JSON | `.healing-results.json` |
| Traces | test-executor | test-healer, human | Playwright trace.zip | `test-results/**/trace.zip` |
| Screenshots | test-executor | test-healer, human | PNG | `test-results/**/*.png` |
| HTML Report | test-executor | human | HTML | `playwright-report/` |
| Circuit Breaker State | test-healer | test-healer (next run) | JSON | `.github/healing-state.json` |

## Directory Structure

```
project-root/
  .playwright/                    # Skill state files (planner output)
    test-plan.md
    pages.md
    selector-strategy.md
    project-config.md
    VERIFICATION.md
  tests/                          # Test code (generator output)
    seed.spec.ts                  # Mandatory seed file
    fixtures.ts                   # Worker-scoped fixtures
    helpers/
      test-data.ts                # TestDataFactory with workerId
    pages/                        # Page objects (if complex flows)
      login.page.ts
      dashboard.page.ts
    auth.spec.ts                  # Generated test files
    checkout.spec.ts
  results.json                    # Test results (executor output)
  .ai-failures.json               # Classified failures (executor output)
  .healing-results.json           # Healing results (healer output)
  test-results/                   # Playwright output directory
    **/trace.zip
    **/*.png
  playwright-report/              # HTML report (executor output)
  .github/
    healing-state.json            # Circuit breaker state (healer)
```

## Naming Conventions

- Test files: `<feature>.spec.ts` (e.g., `checkout.spec.ts`, `auth.spec.ts`)
- Page objects: `<page-name>.page.ts` (e.g., `login.page.ts`)
- Fixtures: `fixtures.ts` (single file, worker-scoped)
- Test data: `helpers/test-data.ts` (TestDataFactory with workerId for parallel isolation)
- Seed file: `seed.spec.ts` (or `seeds/<role>-seed.spec.ts` for multi-role)

## Skill Read/Write Summary

### test-planner

Reads:
- `package.json` -- detect framework, dependencies
- Existing `tests/*.spec.ts` -- learn project patterns
- `tests/seed.spec.ts` -- understand fixtures and imports

Writes:
- `.playwright/test-plan.md`
- `.playwright/pages.md`
- `.playwright/selector-strategy.md`
- `.playwright/project-config.md`
- `.playwright/VERIFICATION.md`

### test-generator

Reads:
- `.playwright/test-plan.md` -- scenarios to implement
- `.playwright/selector-strategy.md` -- locator decisions per page
- `tests/seed.spec.ts` -- quality reference and pattern template
- `package.json` -- framework detection

Writes:
- `tests/*.spec.ts` -- generated test files
- `tests/pages/*.page.ts` -- page objects (if complex flows)
- `tests/fixtures.ts` -- worker-scoped fixtures
- `tests/helpers/test-data.ts` -- TestDataFactory
- Updates `.playwright/test-plan.md` checkboxes (mark scenarios complete)

### test-executor

Reads:
- `tests/*.spec.ts` -- test files to run
- `playwright.config.ts` -- test configuration
- `tests/seed.spec.ts` -- run first to verify environment health

Writes:
- `results.json` -- Playwright JSON reporter output
- `.ai-failures.json` -- classified failures (locator, timing, data, other)
- `test-results/**/trace.zip` -- Playwright traces (on failure)
- `test-results/**/*.png` -- screenshots (on failure)
- `playwright-report/` -- HTML report

### test-healer

Reads:
- `.ai-failures.json` -- failure classification from executor
- `test-results/**/trace.zip` -- traces for debugging
- `tests/*.spec.ts` -- test files to repair
- `tests/seed.spec.ts` -- quality reference for healed tests
- `.github/healing-state.json` -- circuit breaker state

Writes:
- Updated `tests/*.spec.ts` -- fixed test files
- `.healing-results.json` -- healing results with confidence scores
- `.github/healing-state.json` -- updated circuit breaker state
- Git branch + commits + PR (for CI/CD integration)

## Progress Tracking

The test plan uses markdown checkboxes for progress tracking:

```markdown
| Feature | Suite | Tests | Priority | Status |
|---------|-------|-------|----------|--------|
| Authentication | auth.spec.ts | 8 | P0 | [x] |
| Checkout | checkout.spec.ts | 12 | P0 | [ ] |
| Search | search.spec.ts | 6 | P1 | [ ] |
```

The page inventory tracks exploration progress:

```markdown
## Pages

- [x] /login (Score: 95) -- explored, selectors verified
- [x] /dashboard (Score: 65) -- explored, needs test IDs
- [ ] /settings -- not yet explored
```

Skills update these checkboxes as they complete work.

## Failure Classification Format

The `.ai-failures.json` file classifies test failures for the healer:

```json
{
  "timestamp": "2026-04-03T12:00:00Z",
  "summary": {
    "total": 50,
    "passed": 35,
    "failed": 15,
    "flaky": 2,
    "timestamp": "2026-04-03T12:00:00Z"
  },
  "locator": [
    {
      "title": "user can log in with valid credentials",
      "file": "tests/auth.spec.ts",
      "line": 12,
      "project": "chromium",
      "error": "locator.click: Timeout 30000ms exceeded.\nwaiting for getByRole('button', { name: 'Sign In' })",
      "attachments": {
        "screenshot": "test-results/auth-login-chromium/screenshot.png",
        "trace": "test-results/auth-login-chromium/trace.zip"
      }
    }
  ],
  "timing": [],
  "data": [],
  "visual": [],
  "interaction": [],
  "other": []
}
```

Classification patterns:
- **locator** (28% of failures): error matches `locator|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden`
- **timing** (30%): error matches `timeout|timed out|race condition|navigation timeout|waitFor.*exceeded`
- **data** (14%): error matches `expected.*to(Equal|Be|Have|Contain|Match)|AssertionError|toHaveText|toContain|toHaveURL`
- **visual** (10%): error matches `screenshot|visual.*regression|pixel.*diff|snapshot.*mismatch|toMatchSnapshot|toHaveScreenshot`
- **interaction** (10%): error matches `intercept|not scrollable|drag.*drop|click.*intercepted|obscured|pointer.*event`
- **other** (8%): infrastructure failures, browser crashes, network errors
