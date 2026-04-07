# Locator Strategy Rules

Cross-browser locator decision framework for Playwright test generation. All rules derived from verified accessibility tree inconsistencies across Chrome, Firefox, and Safari (15-25% of Chrome-generated tests at risk of failing in other browsers).

Evidence: T4-03 cross-browser verification, Playwright issues #23377, #35720, #34483.

## Decision Tree

Follow this tree top-to-bottom for every element you need to locate in a test. Stop at the first match.

```
1. Does element have data-testid?
   YES -> Use getByTestId() [UNIVERSAL SAFE]
   NO  -> Continue to 2

2. Is element a form control with <label>?
   YES -> Use getByLabel() [UNIVERSAL SAFE]
   NO  -> Continue to 3

3. Is element plain text content (div, span, p)?
   YES -> Use getByText() with exact match [UNIVERSAL SAFE]
   NO  -> Continue to 4

4. Is element in the SAFE role list?
   (button, link, textbox, checkbox, radio, heading, img)
   YES -> Use getByRole(role) WITHOUT name filter [GENERALLY SAFE]
   NO  -> Continue to 5

5. Is element a list with list-style: none?
   YES -> Check if inside <nav>
         Inside <nav>: Use getByRole('list') [SAFE]
         Outside <nav>: FLAG for manual review. Add role="list" to HTML.
   NO  -> Continue to 6

6. Is element using caption, alert, form, or combobox roles?
   YES -> AVOID getByRole with name filter
         caption:  Use getByText() fallback
         alert:    Use getByRole('alert') without name OR getByText()
         form:     Use page.locator('form')
         combobox: Use getByRole('combobox') without name
   NO  -> Continue to 7

7. Element requires complex ARIA state checking (expanded, collapsed)?
   YES -> FLAG for browser-specific verification.
          Generate test-id-based fallback.
   NO  -> Continue to 8

8. DEFAULT: Generate BOTH getByRole() AND getByTestId() fallback
   Use .or() chaining: page.getByRole('...').or(page.getByTestId('...'))
```

## Ten-Tier Locator Discovery Hierarchy

Used by the self-healing algorithm. Deterministic, no LLM. Each tier is tried in order until one resolves.

| Tier | Strategy | Confidence | False Positive Rate |
|------|----------|------------|---------------------|
| 1 | `getByRole` + name (safe roles only) | HIGH | 2-5% |
| 2 | `getByRole` (role only, no name) | HIGH | 2-5% |
| 3 | `getByTestId` / `data-testid` / `data-qa` | HIGH | 2-5% |
| 4 | `getElementById` / `#id` | MEDIUM | 5-10% |
| 5 | `getByLabel` (exact match) | MEDIUM | 5-10% |
| 6 | `getByLabel` (contains match) | MEDIUM | 5-10% |
| 7 | `a[href*="..."]` (href fragment) | LOW | 10-15% |
| 8 | CSS class (exact) | LOW | 10-15% |
| 9 | CSS class (contains/partial) | LOW | 10-15% |
| 10 | `getByText` (visible text, last resort) | LOW | 10-15% |

Evidence: T3-01 verified ten-tier algorithm achieves 100% pass rate (31/31 tests) with <1s self-healing time per broken selector.

## Safe Locator Types (Universal across Chrome/Firefox/Safari)

### Tier 1: Universally Safe (Recommended)

1. `getByTestId()` -- Most resilient; immune to accessibility tree differences.
   Use for: components with unpredictable accessibility semantics.
   Trade-off: requires code modification; non-user-facing.

2. `getByText()` (exact matching) -- Stable across browsers when exact text is guaranteed.
   Use for: static content, headings, labels.
   Caution: avoid for dynamically generated text.

3. `getByLabel()` (for form controls) -- Relies on explicit label associations.
   Use for: input fields with proper `<label>` elements.
   Requirement: HTML must include label elements or aria-labelledby.

4. `getByPlaceholder()` -- Safe for inputs with placeholder attributes.
   Use for: form inputs lacking visible labels.
   Limitation: only applicable to input/textarea elements.

5. `getByAltText()` -- Reliable for images and area elements.
   Use for: image locators where alt text is guaranteed.
   Caution: fails if alt attribute is missing.

### Tier 2: Generally Safe (Role-Based, Restricted Set)

These `getByRole()` variants are safe **when used without the `name` option**:

- `getByRole('button')` -- Universal for native buttons
- `getByRole('link')` -- Stable for anchor tags
- `getByRole('textbox')` -- Consistent for input text fields
- `getByRole('checkbox')` -- Reliable for checkboxes
- `getByRole('radio')` -- Stable for radio buttons
- `getByRole('heading')` -- Consistent for h1-h6 elements
- `getByRole('img')` -- Reliable for image elements

## Shadow DOM Handling

Shadow DOM elements are invisible to Playwright's standard `getByRole`/`getByLabel` queries when the element lives inside a shadow root. The MCP `browser_snapshot` tool also cannot see elements inside shadow roots.

**Detection:** If `getByRole` returns 0 elements but the element is visually present on the page, suspect a shadow root boundary.

**Resolution — Parent-Component-First Chaining:**
```typescript
// Correct: chain into shadow root via the host component tag
await page.locator('my-dialog').getByRole('button', { name: 'Confirm' }).click();

// Wrong: getByRole cannot traverse slot projections from page root
await page.getByRole('dialog').getByRole('button', { name: 'Confirm' }).click();
```

**Pattern:** `page.locator('component-tag-name').getByRole(...)` — use the custom element tag as the entry point, then query within it.

**When to use `.or()` fallback with shadow DOM:**
```typescript
const btn = page.locator('my-dialog').getByRole('button', { name: 'Confirm' })
  .or(page.getByTestId('confirm-btn'));
```

**Frameworks with heavy shadow DOM usage:** Lit, Shoelace, Material Web Components, Ionic, Vaadin. For these frameworks, default to parent-component-first chaining for all interactive elements.

## Cross-Browser Safety Matrix

Risky locators that WILL break in cross-browser testing. Avoid them or use fallbacks.

**Note:** MCP `browser_snapshot` does not report elements inside shadow roots — verify with `page.locator('component-tag').evaluate()` if snapshot returns empty for expected elements.

| Locator | Risk | Browser Affected | Problem | Workaround |
|---------|------|------------------|---------|------------|
| `getByRole('caption', { name: '...' })` | HIGH | Firefox, WebKit | Chromium returns name; Firefox/WebKit return empty string | Use `getByText()` |
| `getByRole('list')` on styled lists | HIGH | Safari/WebKit | Safari removes list role when `list-style: none` | Add `role="list"` to HTML or use `getByTestId()` |
| `getByRole('form', { name: '...' })` | MEDIUM-HIGH | All (Playwright #35720) | Fails to find form elements | Use `page.locator('form')` |
| `getByRole('alert', { name: '...' })` | MEDIUM | All (Playwright #23377) | Cannot select with name parameter | Use `getByRole('alert')` without name |
| `getByRole('combobox', { name: '...' })` | MEDIUM | All (Playwright #23377) | Selection fails when name specified | Use `getByRole('combobox')` without name |
| `getByRole('treeitem')` with ARIA states | MEDIUM | Chromium | May omit expanded/collapsed states | Use `getByTestId()` |
| Any `getByRole()` with `{ name }` on non-safe roles | MEDIUM | Varies | Inconsistent accessibility tree behavior | Use `.or()` dual-locator pattern |

## Fallback Patterns

### Dual-Locator with .or() (recommended for generated tests)

```typescript
// Primary: semantic locator (user-facing, accessible)
// Fallback: test-id (guaranteed cross-browser)
const submitButton = page
  .getByRole('button', { name: 'Submit' })
  .or(page.getByTestId('submit-button'));
```

### Test-ID Only (for high-risk components)

```typescript
// Bypass accessibility tree entirely for:
// - caption elements
// - styled lists outside <nav>
// - form elements with complex ARIA
const tableCaption = page.getByTestId('table-caption');  // Not getByRole('caption')
```

## Locator Priority for Generated Tests

When writing a test locator, try in this order. Stop at the first that works:

1. `getByRole()` with name -- but ONLY for safe roles (button, link, textbox, checkbox, radio, heading)
2. `getByLabel()` -- for form controls with labels
3. `getByText()` -- for plain text content
4. `getByTestId()` -- when semantic options are unavailable
5. `.or()` dual-locator -- when cross-browser safety is uncertain
6. `page.locator()` with CSS -- absolute last resort, flag for review

## Assertions: Web-First Only

Always use auto-retrying web-first assertions. Never use synchronous checks.

```typescript
// CORRECT: web-first assertions (auto-retry)
await expect(page).toHaveURL('/dashboard');
await expect(page.getByRole('heading')).toHaveText('Welcome');
await expect(page.getByRole('button')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();

// WRONG: synchronous checks (race conditions)
expect(page.url()).toContain('dashboard');        // no auto-retry
expect(await locator.isVisible()).toBe(true);     // snapshot, not retry
await page.waitForTimeout(2000);                  // hardcoded wait
```

## Leptos/WASM Applications

For Leptos, Yew, or other WASM-based frameworks:

- Use `domcontentloaded` wait state, NOT `networkidle` (unreliable for WASM).
- Add a 150ms buffer after navigation for hydration to complete.
- Verify elements are interactive, not just present.

```typescript
// Leptos/WASM navigation pattern
await page.goto('/app', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(150);  // hydration buffer -- acceptable ONLY for WASM
await expect(page.getByRole('button', { name: 'Submit' })).toBeEnabled();
```

Evidence: T4-02 verified networkidle is unreliable for WASM; domcontentloaded + 150ms buffer recommended.

## Cross-Browser Testing Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } }
  ],
  // Single test suite runs across all browsers
  // Tests use universal locators with fallbacks
});
```

When executor detects browser-specific failures:
1. Check if failure involves risky locators (caption, list with list-style: none, etc.)
2. Replace with test-id fallback or safer alternative
3. Re-run across all browsers
4. If still failing, escalate to manual review
