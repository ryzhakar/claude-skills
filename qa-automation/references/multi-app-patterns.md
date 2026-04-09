# Multi-App Testing Patterns

Patterns for comparing two or more applications in a single QA session. The default plugin workflow assumes a single base URL — this reference documents the adaptations needed when testing multiple apps (v1 vs v2, competitor A vs B, staging vs production).

Extracted from field testing (2026-04-09, 14 tests across 2 apps, every phase required workarounds).

## When This Applies

Multi-app mode is active when the user provides multiple base URLs, or when the test plan involves comparing behavior across different deployments. The orchestrator detects this and includes this reference in agent dispatch prompts.

## Phase Adaptations

### Plan (planner-agent)

Dispatch the planner with ALL base URLs. The planner explores each app independently and produces per-app artifacts:

- `.playwright/pages-{app-name}.md` — per-app page inventory
- `.playwright/selector-strategy-{app-name}.md` — per-app selector decisions
- `.playwright/project-config.md` — lists all apps with their URLs and tech stacks

The test plan organizes scenarios by comparison concern (what to compare), not by app (where to look). Example: "Compare product listing count between v1 and v2" — not "Test v1 products" + "Test v2 products" separately.

### Generate (generator-agent)

**Dual-context fixtures.** Tests need simultaneous access to both apps:

```typescript
import { test as base } from '@playwright/test';

type MultiAppFixtures = {
  appA: { page: Page; baseURL: string };
  appB: { page: Page; baseURL: string };
};

export const test = base.extend<MultiAppFixtures>({
  appA: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await use({ page, baseURL: 'https://app-a.example.com' });
    await context.close();
  },
  appB: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await use({ page, baseURL: 'https://app-b.example.com' });
    await context.close();
  },
});
```

**Comparison-as-findings, not absolute assertions.** Multi-app tests do not assert fixed values. They compare values between apps and log the delta:

```typescript
test('product count matches between apps', async ({ appA, appB }) => {
  await appA.page.goto(`${appA.baseURL}/products`);
  await appB.page.goto(`${appB.baseURL}/products`);

  const countA = await appA.page.locator('.product-card').count();
  const countB = await appB.page.locator('.product-card').count();

  // Log as finding, not assertion
  const finding: ComparisonFinding = {
    feature: 'product-listing',
    metric: 'product_count',
    appA_value: countA,
    appB_value: countB,
    status: countA === countB ? 'match' : 'mismatch',
    delta: Math.abs(countA - countB),
  };

  test.info().annotations.push({
    type: 'finding',
    description: JSON.stringify(finding),
  });

  // Optionally assert on critical mismatches
  if (finding.status === 'mismatch') {
    console.warn(`MISMATCH: ${finding.metric} — ${countA} vs ${countB}`);
  }
});
```

**When to use `expect()` vs findings:**
- Use `expect()` for structural requirements (page loads, element exists, navigation works)
- Use findings for comparative data (counts, text content, prices, feature presence)

### Execute (executor-agent)

No changes to executor behavior. Failure classification works the same way. The executor reports findings from test annotations alongside pass/fail status.

### Heal (healer-agent)

Locator healing works per-app — the healer identifies which app's DOM changed. The `browser_specific` field in `.ai-failures.json` extends naturally to `app_specific`:

```json
{
  "title": "product count matches between apps",
  "file": "tests/comparison.spec.ts",
  "line": 12,
  "error": "locator('.product-card') resolved to 0 elements",
  "app_specific": "appB",
  "app_note": "Selector valid in appA, broken in appB — appB uses '.product-item' instead"
}
```

### Report

The session report includes a finding summary:

```markdown
## Comparison Findings

| Feature | Metric | App A | App B | Status |
|---------|--------|-------|-------|--------|
| Product listing | product_count | 24 | 22 | MISMATCH |
| Search | result_count for "shoes" | 8 | 8 | MATCH |
| Cart | add_to_cart_button | present | present | MATCH |
| Checkout | tax_calculation | $4.99 | $5.49 | MISMATCH |
```

## Finding Taxonomy

Multi-app findings replace the single-app pass/fail model:

| Status | Meaning | Action |
|--------|---------|--------|
| MATCH | Same value in both apps | No action |
| MISMATCH | Different values | Flag for review — may be intentional (feature difference) or a bug |
| MISSING | Feature present in one app, absent in the other | Flag as potential regression or feature gap |
| EXTRA | Feature present in one app that shouldn't be | Flag as potential scope creep or unintended behavior |

Findings are NOT test failures. A mismatch is data for a human to interpret, not a bug for the healer to fix.

## Auth in Multi-App Mode

If apps require authentication, each app gets its own browser profile:

```bash
# Create persistent profiles per app
playwright-cli open --profile=app-a-profile https://app-a.example.com
# Log in manually, close browser — profile persists
playwright-cli open --profile=app-b-profile https://app-b.example.com
# Log in manually, close browser — profile persists
```

Use `--profile` for persistent auth state, NOT `--storage-state` (which requires re-export after token refresh).
