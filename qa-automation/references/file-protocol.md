# File Communication Protocol

All QA automation agents communicate through durable file artifacts written to disk. Agents never relay test content through conversation context -- they write to a path and tell the next agent where to read.

## Core Rule

Agents do NOT summarize or relay content. They point to files.

```
CORRECT:
  Planner agent writes to .playwright/test-plan.md
  User tells Generator: "Generate tests from the plan"
  Generator agent reads .playwright/test-plan.md directly

WRONG:
  Planner agent writes plan
  Orchestrator reads plan, summarizes it, passes summary to Generator
  Generator agent works from summary (lossy, hallucination-prone)
```

## Artifact Map

| Artifact | Producer | Consumer | Format | Location |
|----------|----------|----------|--------|----------|
| Test Plan | planner-agent | generator-agent, human | Markdown | `.playwright/test-plan.md` |
| Page Inventory | planner-agent | generator-agent | Markdown with checkboxes | `.playwright/pages.md` |
| Selector Strategy | planner-agent | generator-agent | Markdown | `.playwright/selector-strategy.md` |
| Project Config | planner-agent | generator-agent | Markdown | `.playwright/project-config.md` |
| Verification Evidence | planner-agent | human | Markdown | `.playwright/VERIFICATION.md` |
| Orchestrator Status | all agents | orchestrator | JSON | `.playwright/orchestrator-status.json` |
| QA Phase Marker | orchestrator | SessionStart hook | Text | `.claude/qa-phase.txt` |
| Healed Test Output | healer-agent | orchestrator | JSON | `.playwright/healed/{test-name}.json` |
| Session Report | orchestrator | human | Markdown | `.playwright/session-report.md` |
| Lessons | orchestrator, all agents | all agents | Markdown | `.playwright/lessons.md` |
| Test Files | generator-agent | executor-agent, healer-agent | TypeScript | `tests/*.spec.ts` |
| Page Objects | generator-agent | executor-agent | TypeScript | `tests/pages/*.page.ts` |
| Fixtures | generator-agent | all agents | TypeScript | `tests/fixtures.ts` |
| Test Data Helpers | generator-agent | test files | TypeScript | `tests/helpers/test-data.ts` |
| Seed File | human or generator-agent | all agents | TypeScript | `tests/seed.spec.ts` |
| Test Results | executor-agent | healer-agent | JSON | `results.json` |
| Failure Classification | executor-agent | healer-agent | JSON | `.ai-failures.json` |
| Healing Results | healer-agent | CI/CD | JSON | `.healing-results.json` |
| Traces | executor-agent | healer-agent, human | Playwright trace.zip | `test-results/**/trace.zip` |
| Screenshots | executor-agent | healer-agent, human | PNG | `test-results/**/*.png` |
| HTML Report | executor-agent | human | HTML | `playwright-report/` |
| Circuit Breaker State | healer-agent | healer-agent (next run) | JSON | `.github/healing-state.json` |

## Directory Structure

```
project-root/
  .playwright/                    # Agent state files
    test-plan.md                  # Planner output
    pages.md
    selector-strategy.md
    project-config.md
    VERIFICATION.md
    orchestrator-status.json      # Per-agent completion status
    session-report.md             # Final orchestrator report
    lessons.md                    # Cross-cycle feedback (selectors that failed, patterns that worked)
    healed/                       # Healer agent outputs (parallel mode)
      {test-name}.json
  .claude/
    qa-phase.txt                  # Last completed phase (for recovery)
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
  .healing-results.json           # Aggregated healing results (orchestrator output)
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

## Agent Read/Write Summary

### planner-agent

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
- `.playwright/orchestrator-status.json` -- completion status

### generator-agent

Reads:
- `.playwright/test-plan.md` -- scenarios to implement
- `.playwright/selector-strategy.md` -- locator decisions per page
- `tests/seed.spec.ts` -- quality reference and pattern template
- `package.json` -- framework detection

Writes:
- `tests/*.spec.ts` -- generated test files (create mode) or patched test files (fix mode)
- `tests/pages/*.page.ts` -- page objects (if complex flows)
- `tests/fixtures.ts` -- worker-scoped fixtures
- `tests/helpers/test-data.ts` -- TestDataFactory
- Updates `.playwright/test-plan.md` checkboxes (mark scenarios complete)
- Appends to `.playwright/lessons.md` -- structural issues found and fixed (fix mode)
- `.playwright/orchestrator-status.json` -- completion status

### executor-agent

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
- `.playwright/orchestrator-status.json` -- completion status

### healer-agent

Reads:
- `.ai-failures.json` -- failure classification from executor
- `test-results/**/trace.zip` -- traces for debugging
- `tests/*.spec.ts` -- test files to repair
- `tests/seed.spec.ts` -- quality reference for healed tests
- `.github/healing-state.json` -- circuit breaker state

Writes:
- Updated `tests/*.spec.ts` -- fixed test files (direct mode)
- `.playwright/healed/{test-name}.json` -- per-failure output (parallel mode)
- `.github/healing-state.json` -- updated circuit breaker state
- Git branch + commits + PR (for CI/CD integration)

### orchestrator

Reads:
- `.playwright/orchestrator-status.json` -- agent completion status
- `.playwright/healed/*.json` -- individual healer outputs (parallel mode)

Writes:
- `.claude/qa-phase.txt` -- last completed phase for recovery
- `.healing-results.json` -- aggregated healing results
- `.playwright/session-report.md` -- final report with test counts, healing summary, artifact links

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

Agents update these checkboxes as they complete work.

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

## V2 Orchestrator Artifacts

### Orchestrator Status File

Each agent writes `.playwright/orchestrator-status.json` on completion:

```json
{
  "phase": "PLAN",
  "status": "DONE",
  "blocker": null,
  "artifacts": [
    ".playwright/test-plan.md",
    ".playwright/pages.md",
    ".playwright/selector-strategy.md",
    ".playwright/project-config.md",
    ".playwright/VERIFICATION.md"
  ]
}
```

Status values:
- **DONE**: phase completed successfully
- **NEEDS_CONTEXT**: agent needs user input or clarification
- **BLOCKED**: unrecoverable error (e.g., missing dependencies, invalid config)

### QA Phase Marker

`.claude/qa-phase.txt` contains a single line with the last completed phase name:

```
PLAN
```

Phase sequence: `PLAN` -> `GENERATE` -> `EXECUTE` -> `HEAL`

Written by orchestrator after each phase completes. Read by SessionStart hook to resume from correct phase after context compaction.

### Healed Test Output (Parallel Mode)

`.playwright/healed/{test-name}.json` contains per-failure healing results:

```json
{
  "test": "user can log in with valid credentials",
  "file": "tests/auth.spec.ts",
  "status": "healed",
  "confidence": 0.92,
  "tier": 1,
  "original": "await page.getByRole('button', { name: 'Sign In' }).click();",
  "healed": "await page.getByRole('button', { name: /sign in/i }).click();",
  "verified": true
}
```

Status values:
- **healed**: fix applied and verified
- **deferred**: low confidence, needs human review
- **rejected**: cannot fix automatically

### Session Report

`.playwright/session-report.md` contains the final orchestrator summary:

```markdown
# QA Automation Session Report

**Date:** 2026-04-07
**Duration:** 45 minutes
**Phases Completed:** PLAN, GENERATE, EXECUTE, HEAL

## Test Results

- **Total Tests:** 50
- **Passed:** 35
- **Failed:** 15
- **Healed:** 12 (80% healing rate)
- **Deferred:** 3 (needs human review)

## Healing Summary

### Tier 1 (Locator Fixes)
- 8 tests healed (confidence: 0.90+)
- Pattern: case-insensitive text matching

### Tier 2 (Timing Adjustments)
- 4 tests healed (confidence: 0.75+)
- Pattern: explicit wait conditions added

### Deferred
- `tests/checkout.spec.ts:45` -- ambiguous selector (confidence: 0.62)
- `tests/cart.spec.ts:78` -- data isolation issue (confidence: 0.58)
- `tests/search.spec.ts:120` -- visual regression (confidence: 0.45)

## Artifacts

- Test Plan: `.playwright/test-plan.md`
- Healing Results: `.healing-results.json`
- HTML Report: `playwright-report/index.html`
- Healed Outputs: `.playwright/healed/*.json`
```

### Aggregated Healing Results

`.healing-results.json` contains orchestrator-aggregated healing data:

```json
{
  "timestamp": "2026-04-07T10:30:00Z",
  "summary": {
    "total_failures": 15,
    "healed": 12,
    "deferred": 3,
    "rejected": 0,
    "healing_rate": 0.80
  },
  "by_tier": {
    "tier1": {
      "count": 8,
      "avg_confidence": 0.92,
      "pattern": "locator fixes (case-insensitive matching)"
    },
    "tier2": {
      "count": 4,
      "avg_confidence": 0.78,
      "pattern": "timing adjustments (explicit waits)"
    }
  },
  "deferred_tests": [
    {
      "test": "checkout calculates tax correctly",
      "file": "tests/checkout.spec.ts",
      "line": 45,
      "reason": "ambiguous selector",
      "confidence": 0.62
    }
  ]
}
```

## Artifact Templates

Output format templates for planner-agent artifacts.

### Project Configuration Template

```markdown
# Project Configuration

**Framework:** React 18 / Next.js 14
**State Management:** Zustand
**Auth:** NextAuth.js (session-based)
**Build Tool:** Vite
**Base URL:** http://localhost:3000
**Detected:** {YYYY-MM-DD}
```

For Leptos, Yew, or other WASM frameworks, add:

```markdown
**Wait Strategy:** domcontentloaded + 150ms hydration buffer (WASM)
```

### Verification Evidence Template

```markdown
# Verification Evidence

## Pages Visited
- /login -- form with 2 labeled inputs (Email, Password), 1 submit button
- /dashboard -- 3 KPI widgets (dynamic), navigation sidebar, user avatar
- /products -- product grid with 12 items, search input, pagination

## Interactions Tested
- Login form: fill Email + Password -> click Sign In -> redirects to /dashboard
- Product search: type in search input -> grid filters in real time
- Cart: click "Add to Cart" -> cart badge increments from 0 to 1

## Issues Found
- /dashboard KPI widgets lack ARIA labels (need data-testid)
- /products list uses list-style: none (Safari list role issue per locator-strategy.md)

## Screenshots
- /tmp/login-page.png
- /tmp/dashboard-loaded.png
```

### Page Inventory Template

```markdown
# Page Inventory

- [x] /login (Score: 95)
  - Email input: labeled, getByLabel works
  - Password input: labeled, getByLabel works
  - Submit button: native button, getByRole works
  - Verdict: semantic locators sufficient

- [x] /dashboard (Score: 65)
  - User widget: div-based, no ARIA label (needs data-testid)
  - Navigation: semantic <nav>, getByRole works
  - KPI cards: dynamic content, no test IDs (needs data-testid)
  - Verdict: mixed quality, flag elements needing test IDs

- [ ] /settings -- not yet explored
```

### Selector Strategy Template

```markdown
# Selector Strategy

## Page: /login (Score: 95)
**Approach:** Semantic locators only
- Email input: getByLabel('Email')
- Password input: getByLabel('Password')
- Submit button: getByRole('button', { name: 'Sign In' })

## Page: /dashboard (Score: 65)
**Approach:** Mixed -- semantic where available, test IDs for dynamic elements
- User widget: getByTestId('user-widget') -- no ARIA label
- Navigation menu: getByRole('navigation') -- semantic landmark present
- KPI cards: getByTestId('kpi-card-revenue') -- dynamic content, no stable text

**Needed Test IDs (flag for dev team):**
- User widget wrapper
- Individual KPI cards
- Notification bell icon
```

### Test Plan Template

```markdown
# Test Plan: {Feature Name}

**Date:** {YYYY-MM-DD}
**Feature:** {Description from user request}
**Coverage Goal:** {Critical paths / Full coverage / Smoke tests}
**Base URL:** {URL from Phase 1}

---

## Scenario 1: {Name}

**Priority:** P0 (Critical)
**Preconditions:** Logged in as standard user
**Steps:**
1. Navigate to /products
2. Click "Add to Cart" on first product
3. Open cart overlay
4. Click "Checkout"

**Expected Outcomes:**
- Cart overlay shows product name, price, quantity matching the product clicked
- Checkout page loads with cart summary
- Product quantity persists across page navigation

**Edge Cases:**
- Cart is empty -> empty state message visible
- Product out of stock -> "Add to Cart" button disabled

**Test Suite:** checkout.spec.ts
**Dependencies:** Auth fixture, product catalog data

---

## Test Coverage Summary

| Feature | Suite | Tests | Priority | Status |
|---------|-------|-------|----------|--------|
| Authentication | auth.spec.ts | 8 | P0 | [ ] |
| Product Browsing | product.spec.ts | 10 | P1 | [ ] |
| Checkout | checkout.spec.ts | 12 | P0 | [ ] |
```
