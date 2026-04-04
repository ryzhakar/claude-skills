# Failure Classification Rules

Regex-based patterns for classifying Playwright test failures into six actionable categories. Apply to the `error.message` field from the JSON reporter output.

## Classification Algorithm

```javascript
function classifyFailure(error) {
  const msg = error || '';

  // 1. Locator failures (28% of all test failures)
  // Element could not be found or interacted with
  if (msg.match(/locator\.|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden/i)) {
    return 'locator';
  }

  // 2. Timing failures (30%)
  // Test timed out waiting for a condition
  if (msg.match(/timeout|timed out|race condition|navigation timeout|waitFor.*exceeded/i)) {
    return 'timing';
  }

  // 3. Data/assertion failures (14%)
  // Element found but assertion on content/state failed
  if (msg.match(/expected.*to(Equal|Be|Have|Contain|Match)|AssertionError|toHaveText|toContain|toHaveURL/i)) {
    return 'data';
  }

  // 4. Visual failures (10%)
  // Screenshot comparison or layout regression
  if (msg.match(/screenshot|visual.*regression|pixel.*diff|snapshot.*mismatch|toMatchSnapshot|toHaveScreenshot/i)) {
    return 'visual';
  }

  // 5. Interaction failures (10%)
  // Element found but interaction blocked
  if (msg.match(/intercept|not scrollable|drag.*drop|click.*intercepted|obscured|pointer.*event/i)) {
    return 'interaction';
  }

  // 6. Other/infrastructure (8%)
  return 'other';
}
```

## Pattern Details

### Locator Failures (28%)

Element could not be found or interacted with. Primary candidates for automated healing via the ten-tier locator algorithm.

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

### Timing Failures (30%)

Test timed out waiting for a condition. Often signals flaky tests needing wait strategy fixes, NOT locator changes. Do NOT heal with locator changes.

| Pattern | Example |
|---------|---------|
| `timeout` | `Timeout 5000ms exceeded` |
| `timed out` | `Test timed out after 30000ms` |
| `race condition` | `race condition: element detached from DOM` |
| `navigation timeout` | `page.goto: Navigation timeout 30000ms exceeded` |
| `waitFor.*exceeded` | `page.waitForSelector: Timeout 30000ms exceeded` |

**Typical causes:** Missing or insufficient waits, slow backend, animation interference, resource contention in parallel execution, WASM hydration delay (Leptos, SvelteKit).

**Recommended fixes (not locator healing):**
- Replace `page.waitForTimeout()` with web-first assertions (`expect(locator).toBeVisible()`)
- Increase action timeout in `playwright.config.ts`
- Add `await page.waitForLoadState('domcontentloaded')` before interactions
- For WASM apps: add 150ms buffer after `domcontentloaded`

### Data/Assertion Failures (14%)

Element found but content or state did not match expectations. Almost always a real application bug. NEVER heal these automatically.

| Pattern | Example |
|---------|---------|
| `expected.*toEqual` | `expect(received).toEqual(expected): Expected "admin" to equal "user"` |
| `expected.*toBe` | `Expected "Revenue: $0" to equal "Revenue: $5,678"` |
| `AssertionError` | `AssertionError: expected true to be false` |
| `toHaveText` | `expect(locator).toHaveText: Expected "Welcome" but received "Error"` |
| `toContain` | `expect(received).toContain: "checkout" not found in "login"` |
| `toHaveURL` | `expect(page).toHaveURL: Expected "/dashboard" but received "/login"` |

**Why these MUST NOT be healed:**
- Locator found the element correctly
- Application returned incorrect data or state
- Changing the locator would mask a real bug
- Core false positive risk: healing an assertion failure means shipping a bug

### Visual Failures (10%)

Screenshot comparison failures and layout regressions. Require human visual review.

| Pattern | Example |
|---------|---------|
| `screenshot` | `Screenshot comparison failed` |
| `toMatchSnapshot` | `expect(page).toMatchSnapshot() - snapshots don't match` |
| `toHaveScreenshot` | `expect(page).toHaveScreenshot() - max pixel diff exceeded` |
| `pixel.*diff` | `Pixel difference: 2.3% exceeds threshold 0.5%` |

### Interaction Failures (10%)

Element found but interaction was blocked by overlay, scroll position, or pointer events.

| Pattern | Example |
|---------|---------|
| `click.*intercepted` | `locator.click: Element is not visible or is intercepted by another element` |
| `intercept` | `click intercepted by overlay` |
| `not scrollable` | `Element not scrollable into view` |
| `drag.*drop` | `Drag and drop failed: target not droppable` |
| `pointer.*event` | `pointer-events: none prevents interaction` |

### Other/Infrastructure Failures (8%)

Browser crashes, out-of-memory errors, network proxy errors, test framework errors. Require manual investigation.

## Output Schema

Write to `.ai-failures.json`:

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

Each failure entry:
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

## Cross-Browser Failure Flags

When a test fails in only one browser project, add a `browser_specific` flag:

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

### Known Browser-Specific Patterns

| Browser | Locator | Problem | Fix |
|---------|---------|---------|-----|
| WebKit | `getByRole('list')` on styled lists | Safari removes list role when `list-style: none` | `getByTestId()` or wrap in `<nav>` |
| Firefox | `getByRole('caption', { name })` | Returns empty string for caption accessible names | `getByText()` |
| Firefox | `getByRole('alert', { name })` | Cannot select alerts by name | `getByRole('alert')` without name |
| Firefox | `getByRole('combobox', { name })` | Selection fails when name specified | `getByRole('combobox')` without name |
| Firefox | `getByRole('form', { name })` | Fails to find form elements by name | `page.locator('form')` |

Evidence: T4-03 verified 15-25% of Chrome-generated tests at risk of failing in other browsers due to accessibility tree inconsistencies.

## Flaky Test Taxonomy

A test is flaky when it fails intermittently (2-98% failure rate). Flaky tests are NOT candidates for locator healing.

| Category | Frequency | Detection | Fix |
|----------|-----------|-----------|-----|
| Async Wait | 45% | Uses `waitForTimeout` instead of web-first assertions | Replace with `expect(locator).toBeVisible()` |
| Race Conditions | 24% | Fails with `--workers>1`, passes with `--workers=1` | Fix test order dependency |
| Resource-Affected | 46.5% | Passes locally, fails on CI | Increase timeouts, optimize test data |
| Network Issues | 9% | API timeouts or backend unavailability | Mock APIs in tests |
| Environment Differences | 12% | Platform or browser-specific | Platform-specific locators |
