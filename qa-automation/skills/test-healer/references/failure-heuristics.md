# Failure Classification Heuristics

Decision tree for classifying test failures as locator (healable), timing (fixable but not locator), data/assertion (real bug, never heal), or other (manual investigation).

## Decision Tree

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

## Flaky vs Broken vs Real Bug

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

## Common Error Messages

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

## Classification Confidence by Error Pattern

| Pattern | Classification Confidence | Notes |
|---------|--------------------------|-------|
| Element not found + DOM changed + no errors | 95% locator issue | Safe to heal |
| Element not found + DOM unchanged + no errors | 60% locator issue | Suspicious, could be timing |
| Element not found + console errors | 20% locator issue | Likely real bug |
| Assertion failed (any context) | 0% locator issue | Always a real bug |
| Timeout + element eventually appears on retry | 90% timing issue | Fix waits, not locators |
| Multiple failures on same page | 70% shared cause | Investigate page-level change |
