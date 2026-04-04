# Playwright Configuration

Recommended `playwright.config.ts` for use with the QA automation skill suite. Includes cross-browser projects, JSON reporter for machine-readable output, trace collection on failure, and WASM hydration timing.

## Full Configuration

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,

  // Fail on CI if test.only left in source
  forbidOnly: !!process.env.CI,

  // Retry on CI only
  retries: process.env.CI ? 2 : 0,

  // Serial on CI (stability), parallel locally (speed)
  workers: process.env.CI ? 1 : undefined,

  // JSON for machine parsing, HTML for human review, line for console
  reporter: [
    ['json', { outputFile: 'results.json' }],
    ['html', { open: 'never' }],
    ['line'],
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    navigationTimeout: 30_000,
    actionTimeout: 15_000,
  },

  // Cross-browser projects
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  // Uncomment and configure for your application
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120_000,
  // },
});
```

## WASM/Hydration Navigation

For Leptos, SvelteKit, Yew, or other WASM-hydrated frameworks. The `networkidle` event is officially discouraged by the Playwright team (GitHub #22897):

1. Leptos makes NO network calls during hydration -- loads WASM bundle first, hydrates synchronously
2. Browser background processes (analytics, service workers) keep network busy indefinitely
3. Tests become flaky with random pass/fail cycles

### Option A: Simple Buffer (Recommended)

```typescript
// In test helper or fixture
async function gotoWithHydration(page: Page, url: string) {
  await page.goto(url);
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(150); // Hydration buffer for WASM
}
```

### Option B: Explicit Hydration Signal (More Robust)

Requires a one-line setup in the app root:

```typescript
// In Playwright test
async function gotoLeptos(page: Page, url: string) {
  await page.goto(url);
  await page.waitForSelector('[data-hydrated="true"]', { timeout: 5000 });
}
```

App-side setup (Leptos example):
```rust
create_effect(|| {
  document
    .document_element()
    .unwrap()
    .set_attribute("data-hydrated", "true")
    .ok();
});
```

Evidence: T4-02 verified `networkidle` is unreliable for WASM; `domcontentloaded` + 150ms buffer is the industry standard pattern.

## Reporter Details

### JSON Reporter

Primary input for failure classification and test-healer. Key fields:

| Path | Value |
|------|-------|
| `suites[].specs[].tests[].results[].status` | `passed`, `failed`, `skipped` |
| `suites[].specs[].tests[].results[].error.message` | Error message for classification |
| `suites[].specs[].tests[].results[].attachments` | Screenshot and trace paths |
| `suites[].specs[].tests[].results[].duration` | Duration in milliseconds |

### Traces

Traces captured on failure contain screenshots at each action, network logs, console output, and DOM snapshots. They are for human debugging only -- Playwright's internal trace format is not a public API.

Open with: `npx playwright show-trace test-results/path/to/trace.zip`

### HTML Reporter

Interactive visual report. Open with: `npx playwright show-report`

## Execution Flags Reference

| Flag | Purpose |
|------|---------|
| `--reporter=json,html,line` | Multiple reporters simultaneously |
| `--project=chromium` | Single browser execution |
| `--grep "login"` | Filter by test name |
| `--shard=1/4` | CI parallelization (first quarter) |
| `--retries=2` | Retry failed tests twice |
| `--trace=on` | Always collect traces (verbose) |
| `--trace=on-first-retry` | Traces only for retried tests |
| `--workers=1` | Serial execution (disable parallelism) |
| `--workers=auto` | Playwright auto-selects worker count |
| `--headed` | Visible browser window |
| `--debug` | Step-through debug mode |

Evidence: T3-10 verified CLI consumes 27K tokens vs MCP 114K tokens on comparable workflows (4x reduction). Always prefer CLI execution.
