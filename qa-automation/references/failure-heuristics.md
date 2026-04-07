# Failure Classification and Healing Heuristics

Unified reference for both executor-agent (classification) and healer-agent (repair decisions). Covers failure taxonomy, regex patterns, decision trees, false positive detection, flaky test identification, and cross-browser analysis.

## Six-Category Failure Taxonomy

All Playwright test failures fall into one of six categories based on error message patterns. Apply these regex-based rules to the `error.message` field from the JSON reporter output.

### 1. Locator Failures (28% of all test failures)

Element could not be found or interacted with. Primary candidates for automated healing via the ten-tier locator algorithm.

**Regex pattern:**
```javascript
/locator\.|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden/i
```

**Common messages:**
| Pattern | Example |
|---------|---------|
| `locator.` | `locator.click: Target closed` |
| `selector` | `selector resolved to hidden element` |
| `element not found` | `element not found in the DOM` |
| `waiting for` | `Timeout 30000ms exceeded waiting for getByRole('button', { name: 'Submit' })` |
| `getBy` | `getByTestId('submit-btn') resolved to 0 elements` |
| `resolved to 0 elements` | `locator resolved to 0 elements` |
| `resolved to hidden` | `locator resolved to hidden element` |

**Typical causes:** UI refactoring changed attributes (class, id, data-testid), element moved in DOM, element relabeled, framework update changed rendered HTML.

**Healable:** YES - candidate for automated healing.

### 2. Timing Failures (30%)

Test timed out waiting for a condition. Often signals flaky tests needing wait strategy fixes, NOT locator changes.

**Regex pattern:**
```javascript
/timeout|timed out|race condition|navigation timeout|waitFor.*exceeded/i
```

**Common messages:**
| Pattern | Example |
|---------|---------|
| `timeout` | `Timeout 5000ms exceeded` |
| `timed out` | `Test timed out after 30000ms` |
| `race condition` | `race condition: element detached from DOM` |
| `navigation timeout` | `page.goto: Navigation timeout 30000ms exceeded` |
| `waitFor.*exceeded` | `page.waitForSelector: Timeout 30000ms exceeded` |

**Typical causes:** Missing or insufficient waits, slow backend, animation interference, resource contention in parallel execution, WASM hydration delay (Leptos, SvelteKit).

**Healable:** NO - fix waits, not locators.

**Recommended fixes:**
- Replace `page.waitForTimeout()` with web-first assertions (`expect(locator).toBeVisible()`)
- Increase action timeout in `playwright.config.ts`
- Add `await page.waitForLoadState('domcontentloaded')` before interactions
- For WASM apps: add 150ms buffer after `domcontentloaded`

### 3. Data/Assertion Failures (14%)

Element found but content or state did not match expectations. Almost always a real application bug.

**Regex pattern:**
```javascript
/expected.*to(Equal|Be|Have|Contain|Match)|AssertionError|toHaveText|toContain|toHaveURL/i
```

**Common messages:**
| Pattern | Example |
|---------|---------|
| `expected.*toEqual` | `expect(received).toEqual(expected): Expected "admin" to equal "user"` |
| `expected.*toBe` | `Expected "Revenue: $0" to equal "Revenue: $5,678"` |
| `AssertionError` | `AssertionError: expected true to be false` |
| `toHaveText` | `expect(locator).toHaveText: Expected "Welcome" but received "Error"` |
| `toContain` | `expect(received).toContain: "checkout" not found in "login"` |
| `toHaveURL` | `expect(page).toHaveURL: Expected "/dashboard" but received "/login"` |

**Healable:** NO - NEVER heal these automatically.

**Why these MUST NOT be healed:**
- Locator found the element correctly
- Application returned incorrect data or state
- Changing the locator would mask a real bug
- Core false positive risk: healing an assertion failure means shipping a bug

### 4. Visual Failures (10%)

Screenshot comparison failures and layout regressions. Require human visual review.

**Regex pattern:**
```javascript
/screenshot|visual.*regression|pixel.*diff|snapshot.*mismatch|toMatchSnapshot|toHaveScreenshot/i
```

**Common messages:**
| Pattern | Example |
|---------|---------|
| `screenshot` | `Screenshot comparison failed` |
| `toMatchSnapshot` | `expect(page).toMatchSnapshot() - snapshots don't match` |
| `toHaveScreenshot` | `expect(page).toHaveScreenshot() - max pixel diff exceeded` |
| `pixel.*diff` | `Pixel difference: 2.3% exceeds threshold 0.5%` |

**Healable:** NO - requires human visual review.

### 5. Interaction Failures (10%)

Element found but interaction was blocked by overlay, scroll position, or pointer events.

**Regex pattern:**
```javascript
/intercept|not scrollable|drag.*drop|click.*intercepted|obscured|pointer.*event/i
```

**Common messages:**
| Pattern | Example |
|---------|---------|
| `click.*intercepted` | `locator.click: Element is not visible or is intercepted by another element` |
| `intercept` | `click intercepted by overlay` |
| `not scrollable` | `Element not scrollable into view` |
| `drag.*drop` | `Drag and drop failed: target not droppable` |
| `pointer.*event` | `pointer-events: none prevents interaction` |

**Healable:** MAYBE - investigate case-by-case.

### 6. Other/Infrastructure Failures (8%)

Browser crashes, out-of-memory errors, network proxy errors, test framework errors. Require manual investigation.

**Healable:** NO - manual investigation required.

## Classification Algorithm

```javascript
function classifyFailure(error) {
  const msg = error || '';

  // 1. Locator failures (28% of all test failures)
  if (msg.match(/locator\.|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden/i)) {
    return 'locator';
  }

  // 2. Timing failures (30%)
  if (msg.match(/timeout|timed out|race condition|navigation timeout|waitFor.*exceeded/i)) {
    return 'timing';
  }

  // 3. Data/assertion failures (14%)
  if (msg.match(/expected.*to(Equal|Be|Have|Contain|Match)|AssertionError|toHaveText|toContain|toHaveURL/i)) {
    return 'data';
  }

  // 4. Visual failures (10%)
  if (msg.match(/screenshot|visual.*regression|pixel.*diff|snapshot.*mismatch|toMatchSnapshot|toHaveScreenshot/i)) {
    return 'visual';
  }

  // 5. Interaction failures (10%)
  if (msg.match(/intercept|not scrollable|drag.*drop|click.*intercepted|obscured|pointer.*event/i)) {
    return 'interaction';
  }

  // 6. Other/infrastructure (8%)
  return 'other';
}
```

## Decision Tree for Healing

Use this decision tree to classify test failures as locator (healable), timing (fixable but not locator), data/assertion (real bug, never heal), or other (manual investigation).

```
Test Fails
    |
    v
Step 1: Check error message pattern
    |
    +-- Matches /assertion|expected.*to|toEqual|toHaveText|toContain/i ?
    |   YES --> DATA/ASSERTION FAILURE (real bug)
    |           DO NOT HEAL. The locator found the element.
    |           The value is wrong. Application's fault.
    |
    +-- Matches /locator|selector|element not found|waiting for|getBy/i ?
    |   YES --> LOCATOR FAILURE (candidate for healing)
    |           Continue to Step 2.
    |
    +-- Matches /timeout|race condition|waitFor|timed out/i ?
    |   YES --> TIMING FAILURE (fix waits, not locators)
    |           Replace hardcoded waits with web-first assertions.
    |           DO NOT change locators for timing issues.
    |
    +-- None of the above ?
        YES --> OTHER FAILURE (manual investigation)
                Check visual regressions, interaction failures,
                infrastructure errors. Open HTML report or trace viewer.

Step 2: Verify it is truly a locator issue
    |
    +-- Did the element exist but assertion on it failed?
    |   YES --> RECLASSIFY as DATA failure. DO NOT HEAL.
    |
    +-- Are there console errors at ERROR or FATAL severity?
    |   YES --> RECLASSIFY as REAL BUG. DO NOT HEAL.
    |           Application is crashing, not just missing a locator.
    |
    +-- Are more than 10 tests failing simultaneously?
    |   YES --> RECLASSIFY as INFRASTRUCTURE failure. DO NOT HEAL.
    |           Mass failures indicate shared root cause.
    |
    +-- None of the above?
        YES --> CONFIRMED LOCATOR FAILURE. Proceed with healing.

Step 3: Determine locator failure subtype
    |
    +-- Element attributes changed (class, id, data-testid)?
    |   YES --> HIGH confidence healing candidate.
    |           UI refactor renamed attributes but element exists.
    |
    +-- Element relocated in DOM (same element, new position)?
    |   YES --> MEDIUM confidence healing candidate.
    |           Element moved (header to sidebar). Needs review.
    |
    +-- Element removed entirely from DOM?
    |   YES --> LOW confidence.
    |           Could be intentional removal or real bug.
    |           Flag for manual investigation.
    |
    +-- Element present but not visible (hidden by CSS/JS)?
        YES --> MEDIUM confidence.
                CSS-only change: healable. JS logic change: real bug.
```

## False Positive Scenarios

The most dangerous failure mode is healing a test that correctly detects a real bug. These are the key scenarios to watch for:

### Scenario 1: Element found, assertion fails

```typescript
// Locator works fine:
const price = page.getByTestId('product-price');
// Assertion fails because app returned wrong data:
await expect(price).toHaveText('$99.99');  // Actually shows "$0.00"
```

**Decision:** NEVER HEAL. The test is correct. Pricing bug in the application.

### Scenario 2: Feature intentionally removed

```typescript
// "Delete Account" button was intentionally removed from the UI:
await page.getByRole('button', { name: 'Delete Account' }).click();
```

**Decision:** DO NOT HEAL. The feature is gone. The test should be deleted, not healed. Flag with note: "Element removed from DOM. Verify if intentional feature removal."

### Scenario 3: Multiple failures on same page

Five tests on the checkout page all fail with locator errors. More likely a page restructuring (new checkout flow) than five independent locator breaks.

**Decision:** Reduce confidence by 0.1-0.2. If cluster size exceeds 10, do not heal.

### Scenario 4: Browser-specific failure

```
auth.spec.ts PASS on chromium
auth.spec.ts PASS on firefox
auth.spec.ts FAIL on webkit: getByRole('list') resolved to 0 elements
```

**Decision:** Browser-specific accessibility tree difference. Replace risky locator with cross-browser safe alternative (`getByTestId()`). HIGH confidence if fix uses universally safe locator.

### Scenario 5: Console errors accompany the failure

```
Console ERROR: Uncaught TypeError: Cannot read properties of undefined
Test FAIL: getByRole('button', { name: 'Submit' }) not found
```

**Decision:** Application crashed before rendering the button. Real bug. DO NOT HEAL.

## Classification Confidence by Error Pattern

| Pattern | Classification Confidence | Notes |
|---------|--------------------------|-------|
| Element not found + DOM changed + no errors | 95% locator issue | Safe to heal |
| Element not found + DOM unchanged + no errors | 60% locator issue | Suspicious, could be timing |
| Element not found + console errors | 20% locator issue | Likely real bug |
| Assertion failed (any context) | 0% locator issue | Always a real bug |
| Timeout + element eventually appears on retry | 90% timing issue | Fix waits, not locators |
| Multiple failures on same page | 70% shared cause | Investigate page-level change |

## Common Error Messages Classification

| Error Message | Category | Healable? |
|--------------|----------|-----------|
| `locator.click: Timeout 30000ms exceeded waiting for getByRole(...)` | Locator | YES |
| `expect(locator).toBeVisible: Timeout 5000ms exceeded` | Timing | NO - add proper wait |
| `expect(page).toHaveURL: Timeout 5000ms exceeded` | Timing | NO - navigation incomplete |
| `Expected "foo" to equal "bar"` | Data | NO - real bug |
| `locator.fill: Target closed` | Other | MAYBE - page navigated away |
| `page.goto: net::ERR_CONNECTION_REFUSED` | Other | NO - server not running |
| `browserType.launch: Executable doesn't exist` | Other | NO - browsers not installed |
| `getByTestId('x') resolved to 0 elements` | Locator | YES - test ID removed |
| `strict mode violation: getByRole('button') resolved to 3 elements` | Locator | YES - need name filter |

## Flaky vs Broken vs Real Bug

Distinguishing between flaky tests, real bugs, and broken locators is critical to avoid false positives.

| Signal | Flaky Test | Real Bug | Broken Locator |
|--------|-----------|----------|----------------|
| Consistency | Intermittent (2-98% fail) | Consistent (100% fail) | Consistent (100% fail) |
| Code changes | None | Recent commit | None |
| DOM state | Timing-dependent | Normal or error state | Changed attributes |
| Console errors | None | Present | None |
| API responses | Variable | Failed or wrong data | Normal |
| Retry behavior | Passes on retry | Still fails | Still fails |
| Cluster size | 1-3 tests | 5+ tests | 1-2 tests |
| Correct action | FIX TEST (add waits) | DO NOT HEAL (file bug) | HEAL LOCATOR (update selector) |

## Flaky Test Taxonomy

A test is flaky when it fails intermittently (2-98% failure rate). Flaky tests are NOT candidates for locator healing.

| Category | Frequency | Detection | Fix |
|----------|-----------|-----------|-----|
| Async Wait | 45% | Uses `waitForTimeout` instead of web-first assertions | Replace with `expect(locator).toBeVisible()` |
| Race Conditions | 24% | Fails with `--workers>1`, passes with `--workers=1` | Fix test order dependency |
| Resource-Affected | 46.5% | Passes locally, fails on CI | Increase timeouts, optimize test data |
| Network Issues | 9% | API timeouts or backend unavailability | Mock APIs in tests |
| Environment Differences | 12% | Platform or browser-specific | Platform-specific locators |

## Cross-Browser Failure Flags

When a test fails in only one browser project, add a `browser_specific` flag to the failure entry.

### Known Browser-Specific Patterns

| Browser | Locator | Problem | Fix |
|---------|---------|---------|-----|
| WebKit | `getByRole('list')` on styled lists | Safari removes list role when `list-style: none` | `getByTestId()` or wrap in `<nav>` |
| Firefox | `getByRole('caption', { name })` | Returns empty string for caption accessible names | `getByText()` |
| Firefox | `getByRole('alert', { name })` | Cannot select alerts by name | `getByRole('alert')` without name |
| Firefox | `getByRole('combobox', { name })` | Selection fails when name specified | `getByRole('combobox')` without name |
| Firefox | `getByRole('form', { name })` | Fails to find form elements by name | `page.locator('form')` |

**Evidence:** T4-03 verified 15-25% of Chrome-generated tests at risk of failing in other browsers due to accessibility tree inconsistencies.

### Browser-Specific Failure Entry Example

```json
{
  "title": "displays product list",
  "file": "tests/products.spec.ts",
  "line": 8,
  "project": "webkit",
  "error": "getByRole('list') resolved to 0 elements",
  "browser_specific": true,
  "browser_note": "WebKit removes list role when list-style: none is applied"
}
```

## Output Schema

Write classified failures to `.ai-failures.json`:

```json
{
  "timestamp": "ISO 8601 timestamp",
  "summary": {
    "total_failures": 0,
    "locator": 0,
    "timing": 0,
    "data": 0,
    "visual": 0,
    "interaction": 0,
    "other": 0
  },
  "locator": [],
  "timing": [],
  "data": [],
  "visual": [],
  "interaction": [],
  "other": []
}
```

### Failure Entry Schema

Each failure entry in the category arrays:

```json
{
  "title": "test title from spec",
  "file": "tests/example.spec.ts",
  "line": 12,
  "project": "chromium|firefox|webkit",
  "error": "full error message",
  "attachments": {
    "screenshot": "path/to/screenshot.png",
    "trace": "path/to/trace.zip"
  }
}
```

For browser-specific failures, add:

```json
{
  "browser_specific": true,
  "browser_note": "Description of browser-specific behavior"
}
```
