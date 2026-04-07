# Ten-Tier Self-Healing Algorithm

Complete TypeScript implementation of the ten-tier deterministic locator discovery and self-healing algorithm. Ported from the Python original at renjithnj/zero-cost-self-healing-qa. Verified: 100% pass rate (31/31 tests), <1s healing time per broken selector, zero operational cost.

Source: T3-01 verification of https://github.com/renjithnj/zero-cost-self-healing-qa

## Architecture

Three-layer design:
1. **LocatorCache** -- JSON persistence for discovered selectors
2. **DOMExtractor** -- Ten-tier locator discovery algorithm
3. **SmartFind** -- Self-healing interaction wrapper with automatic cache invalidation

When a cached selector fails, SmartFind invalidates the cache entry, re-runs the ten-tier discovery against the live DOM, and retries the action. Typical healing time: 1-3 seconds.

## Tier Priority

| Tier | Strategy | Example | Confidence |
|------|----------|---------|------------|
| 1 | Role + accessible name | `getByRole('link', { name: 'Products' })` | HIGH |
| 2 | Role only | `getByRole('searchbox')` | HIGH |
| 3 | data-testid / data-qa | `[data-testid="search-input"]` | HIGH |
| 4 | HTML id | `#quantity` | MEDIUM |
| 5 | ARIA label (exact) | `[aria-label="cart"]` | MEDIUM |
| 6 | ARIA label (contains) | `[aria-label*="cart"]` | MEDIUM |
| 7 | href fragment | `a[href*="/products"]` | LOW |
| 8 | CSS class (exact) | `.cart` | LOW |
| 9 | CSS class (contains) | `[class*="cart"]` | LOW |
| 10 | Visible text | `getByText('Add to cart')` | LOW |

Each tier uses a 1500ms timeout before falling through to the next. Typical resolution at tiers 1-3 in under 100ms. Worst case: 15s (all 10 tiers time out).

## TypeScript Implementation

### Element Patterns

Each element is described by a pattern dictionary with fallback options for each tier. This structure is application-specific -- the healer generates patterns from the page under test, not from a hardcoded dictionary.

```typescript
export interface ElementPattern {
  role_name?: string[];   // Tier 1: "link::Products", "button::Submit"
  role_only?: string[];   // Tier 2: "searchbox", "navigation"
  testid?: string[];      // Tier 3: "search-input", "submit-btn"
  id?: string[];           // Tier 4: "quantity", "email"
  aria?: string[];         // Tier 5-6: "cart", "search products"
  href?: string[];         // Tier 7: "/products", "/checkout"
  css?: string[];          // Tier 8-9: "cart", "nav-link"
  text?: string[];         // Tier 10: "Add to cart", "Submit"
}
```

Example pattern for a login button:
```typescript
const loginButton: ElementPattern = {
  role_name: ['button::Login', 'button::Sign In'],
  testid: ['login-button', 'login-btn'],
  text: ['Login', 'Sign In', 'Log In'],
  css: ['btn-default', 'login-btn'],
};
```

### LocatorCache

Persistent JSON cache for discovered selectors. Stores selector strings keyed by element name.

```typescript
import * as fs from 'fs/promises';
import * as path from 'path';

export interface CacheData {
  selectors: Record<string, string>;
  updated_at?: string;
}

export class LocatorCache {
  private data: CacheData = { selectors: {} };

  constructor(private readonly cachePath: string) {}

  async load(): Promise<void> {
    try {
      const exists = await fs.access(this.cachePath).then(() => true).catch(() => false);
      if (exists) {
        const content = await fs.readFile(this.cachePath, 'utf-8');
        this.data = JSON.parse(content);
        const count = Object.keys(this.data.selectors || {}).length;
        console.log(`  Locator cache loaded: ${count} selectors`);
      }
    } catch (error) {
      this.data = { selectors: {} };
    }
  }

  private async save(): Promise<void> {
    const dir = path.dirname(this.cachePath);
    await fs.mkdir(dir, { recursive: true });
    this.data.updated_at = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
    await fs.writeFile(this.cachePath, JSON.stringify(this.data, null, 2), 'utf-8');
  }

  get(key: string): string | null {
    return this.data.selectors?.[key] ?? null;
  }

  async set(key: string, value: string): Promise<void> {
    if (!this.data.selectors) {
      this.data.selectors = {};
    }
    this.data.selectors[key] = value;
    await this.save();
  }

  async invalidate(key: string): Promise<void> {
    if (this.data.selectors?.[key]) {
      delete this.data.selectors[key];
      await this.save();
      console.log(`  Invalidated: ${key}`);
    }
  }

  count(): number {
    return Object.keys(this.data.selectors || {}).length;
  }

  updatedAt(): string {
    return this.data.updated_at || 'never';
  }
}
```

### DOMExtractor

The ten-tier locator discovery algorithm. Given an element key and its pattern, tries each tier in order until one succeeds.

```typescript
import { Page, Locator } from '@playwright/test';

export class DOMExtractor {
  constructor(private readonly page: Page) {}

  async find(key: string, pattern: ElementPattern): Promise<string | null> {
    if (!pattern) {
      return null;
    }

    // Tier 1: role + name
    for (const name of pattern.role_name || []) {
      const parts = name.split('::');
      if (parts.length === 2) {
        const [role, rname] = parts;
        const sel = await this.tryRole(role, rname);
        if (sel) return sel;
      }
    }

    // Tier 2: role only
    for (const role of pattern.role_only || []) {
      const sel = await this.tryRoleOnly(role);
      if (sel) return sel;
    }

    // Tier 3: data-testid
    for (const tid of pattern.testid || []) {
      let sel = await this.tryCss(`[data-testid="${tid}"]`);
      if (sel) return sel;
      sel = await this.tryCss(`[data-qa="${tid}"]`);
      if (sel) return sel;
    }

    // Tier 4: HTML id
    for (const id of pattern.id || []) {
      const sel = await this.tryCss(`#${id}`);
      if (sel) return sel;
    }

    // Tier 5: aria-label exact
    for (const aria of pattern.aria || []) {
      const sel = await this.tryCss(`[aria-label="${aria}"]`);
      if (sel) return sel;
    }

    // Tier 6: aria-label contains
    for (const aria of pattern.aria || []) {
      const sel = await this.tryCss(`[aria-label*="${aria}"]`);
      if (sel) return sel;
    }

    // Tier 7: href fragment
    for (const href of pattern.href || []) {
      const sel = await this.tryCss(`a[href*="${href}"]`);
      if (sel) return sel;
    }

    // Tier 8: CSS class exact
    for (const css of pattern.css || []) {
      const selector =
        !css.startsWith('[') && !css.includes(' ')
          ? `.${css.replace(/^\./, '')}`
          : css;
      const sel = await this.tryCss(selector);
      if (sel) return sel;
    }

    // Tier 9: CSS class contains (partial match on first segment)
    for (const css of pattern.css || []) {
      const base = css.replace(/^\./, '').split('-')[0];
      if (base.length > 3) {
        const sel = await this.tryCss(`[class*="${base}"]`);
        if (sel) return sel;
      }
    }

    // Tier 10: visible text (last resort)
    for (const text of pattern.text || []) {
      const sel = await this.tryText(text);
      if (sel) return sel;
    }

    return null;
  }

  private async tryCss(selector: string): Promise<string | null> {
    try {
      const loc = this.page.locator(selector).first();
      await loc.waitFor({ timeout: 1500, state: 'visible' });
      return selector;
    } catch {
      return null;
    }
  }

  private async tryRole(role: string, name: string): Promise<string | null> {
    try {
      let loc: Locator;
      if (name.startsWith('re:')) {
        const pattern = new RegExp(name.slice(3), 'i');
        loc = this.page.getByRole(role as any, { name: pattern }).first();
      } else {
        loc = this.page.getByRole(role as any, { name }).first();
      }
      await loc.waitFor({ timeout: 1500, state: 'visible' });
      return `role::${role}::${name}`;
    } catch {
      return null;
    }
  }

  private async tryRoleOnly(role: string): Promise<string | null> {
    try {
      const loc = this.page.getByRole(role as any).first();
      await loc.waitFor({ timeout: 1500, state: 'visible' });
      return `role::${role}::`;
    } catch {
      return null;
    }
  }

  private async tryText(text: string): Promise<string | null> {
    try {
      const loc = this.page.getByText(text, { exact: true }).first();
      await loc.waitFor({ timeout: 1500, state: 'visible' });
      return `text::${text}`;
    } catch {
      return null;
    }
  }
}
```

### SmartFind

Self-healing interaction layer. Wraps element discovery with automatic cache invalidation and re-discovery when a cached selector breaks.

```typescript
import { Page, Locator } from '@playwright/test';
import { LocatorCache } from './locatorCache';
import { DOMExtractor } from './domExtractor';

export class SmartFind {
  private readonly extractor: DOMExtractor;

  constructor(
    private readonly page: Page,
    private readonly cache: LocatorCache
  ) {
    this.extractor = new DOMExtractor(page);
  }

  /**
   * Get a visible locator for key.
   * Self-heals automatically if selector is broken.
   */
  async get(
    key: string,
    pattern: ElementPattern,
    timeout: number = 6000
  ): Promise<Locator | null> {
    let selector = this.cache.get(key);

    if (!selector) {
      console.log(`  [${key}] not in cache - running DOM extraction`);
      selector = await this.rediscover(key, pattern);
    }

    if (!selector) {
      return null;
    }

    let loc = await this.resolve(selector, timeout);
    if (loc) {
      return loc;
    }

    // Self-healing triggered
    console.log(`  [${key}] selector broke: ${selector}`);
    console.log(`  Self-healing - re-extracting from DOM...`);
    await this.cache.invalidate(key);
    const newSelector = await this.rediscover(key, pattern);
    if (!newSelector) {
      console.log(`  Self-heal failed for [${key}] - element not found in DOM`);
      return null;
    }
    return await this.resolve(newSelector, timeout);
  }

  private async resolve(
    selector: string,
    timeout: number = 6000
  ): Promise<Locator | null> {
    try {
      if (selector.startsWith('role::')) {
        const parts = selector.split('::');
        const role = parts[1] || '';
        const name = parts[2] || '';
        if (!role) return null;

        let loc: Locator;
        if (!name) {
          loc = this.page.getByRole(role as any).first();
        } else if (name.startsWith('re:')) {
          const pattern = new RegExp(name.slice(3), 'i');
          loc = this.page.getByRole(role as any, { name: pattern }).first();
        } else {
          loc = this.page.getByRole(role as any, { name }).first();
        }
        await loc.waitFor({ timeout, state: 'visible' });
        return loc;
      } else if (selector.startsWith('text::')) {
        const text = selector.slice(6);
        const loc = this.page.getByText(text, { exact: true }).first();
        await loc.waitFor({ timeout, state: 'visible' });
        return loc;
      } else {
        const loc = this.page.locator(selector).first();
        await loc.waitFor({ timeout, state: 'visible' });
        return loc;
      }
    } catch {
      return null;
    }
  }

  private async rediscover(
    key: string,
    pattern: ElementPattern
  ): Promise<string | null> {
    const selector = await this.extractor.find(key, pattern);
    if (selector) {
      await this.cache.set(key, selector);
      console.log(`  Re-discovered [${key}]: ${selector}`);
    }
    return selector;
  }

  /**
   * Click an element. Dismisses overlays and retries once on failure.
   */
  async click(
    key: string,
    pattern: ElementPattern,
    timeout: number = 6000
  ): Promise<boolean> {
    const loc = await this.get(key, pattern, timeout);
    if (!loc) return false;

    try {
      await loc.scrollIntoViewIfNeeded();
      await this.page.waitForTimeout(100 + Math.random() * 200);
      await loc.click();
      return true;
    } catch {
      // Retry after dismissing overlays
      console.log(
        `  Click intercepted for [${key}] - dismissing overlays and retrying...`
      );
      await this.dismissOverlays();
      await this.page.waitForTimeout(1000);

      try {
        const loc2 = await this.get(key, pattern, 5000);
        if (loc2) {
          await loc2.scrollIntoViewIfNeeded();
          await loc2.click();
          console.log(`  Click succeeded after overlay dismissal [${key}]`);
          return true;
        }
      } catch (e2) {
        console.log(`  Click still failed for [${key}] after heal:`, e2);
      }

      // Final fallback: JS click
      try {
        const sel = this.cache.get(key);
        if (sel && !sel.startsWith('role::')) {
          await this.page.evaluate((selector) => {
            document
              .querySelector(selector)
              ?.dispatchEvent(
                new MouseEvent('click', { bubbles: true })
              );
          }, sel);
          console.log(`  Used JS click fallback for ${key}`);
          return true;
        }
      } catch {
        // Ignore JS click failure
      }
      return false;
    }
  }

  /**
   * Find input and type into it.
   */
  async fill(
    key: string,
    text: string,
    pattern: ElementPattern,
    timeout: number = 6000
  ): Promise<boolean> {
    const loc = await this.get(key, pattern, timeout);
    if (!loc) return false;

    try {
      await loc.click();
      await this.page.waitForTimeout(200);
      await loc.fill(text);
      return true;
    } catch (e) {
      console.log(`  Fill failed for [${key}]:`, e);
      return false;
    }
  }

  /**
   * Check if element exists and is visible.
   */
  async isVisible(
    key: string,
    pattern: ElementPattern,
    timeout: number = 3000
  ): Promise<boolean> {
    const loc = await this.get(key, pattern, timeout);
    return loc !== null;
  }

  /**
   * Get the text content of an element.
   */
  async text(key: string, pattern: ElementPattern): Promise<string | null> {
    const loc = await this.get(key, pattern);
    if (!loc) return null;

    try {
      const text = await loc.innerText();
      return text.trim();
    } catch {
      return null;
    }
  }

  /**
   * Dismiss any overlays (modals, banners, cookie notices).
   */
  async dismissOverlays(): Promise<void> {
    try {
      await this.page.evaluate(() => {
        // Remove any modal backdrops
        document
          .querySelectorAll('.modal-backdrop')
          .forEach((e) => e.remove());
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        // Close any open Bootstrap modals
        document.querySelectorAll('.modal.show').forEach((m) => {
          m.classList.remove('show');
          (m as HTMLElement).style.display = 'none';
        });
      });
      await this.page.waitForTimeout(200);
    } catch {
      // Ignore dismissal errors
    }

    // Try clicking close buttons on any visible modals
    for (const sel of [
      '.close',
      "[data-dismiss='modal']",
      '#dismiss-button',
    ]) {
      try {
        const loc = this.page.locator(sel).first();
        if (await loc.isVisible()) {
          await loc.click();
          await this.page.waitForTimeout(300);
        }
      } catch {
        // Ignore close button failures
      }
    }
  }
}
```

## Selector Encoding Format

The algorithm uses a string encoding to represent discovered selectors:

- **Role-based:** `"role::link::Products"` or `"role::searchbox::"` (empty name = role-only)
- **Text-based:** `"text::Add to cart"`
- **CSS-based:** Raw CSS selector string (e.g., `"#quantity"`, `".cart"`, `"[data-testid=\"search\"]"`)

The `resolve()` method reconstructs the appropriate Playwright locator from a cached string.

## How the Healer Uses This Algorithm

When a test fails with a locator error:

1. Identify the broken locator in the test file.
2. Construct an `ElementPattern` describing what the element should be (based on the original locator, element context, and page structure).
3. Run the ten-tier algorithm against the live page to find which tier resolves the element.
4. Rewrite the test file with the new locator, using the highest-confidence Playwright API that matches the discovered tier.

The algorithm is deterministic -- given the same page state, it always produces the same result. No LLM calls. Cost per healing operation: $0.

Performance: 1.5s timeout per tier, 10 tiers maximum = 15s worst case. Typical resolution at tiers 1-3 in under 100ms.
