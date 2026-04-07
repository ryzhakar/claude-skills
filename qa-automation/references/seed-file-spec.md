# Seed File Specification

A seed file is a mandatory reference test that establishes the quality bar, environment setup, and patterns for all generated tests. The test-generator skill MUST refuse to generate tests without a seed file.

## Purpose

1. **Quality reference** -- generated tests are compared against the seed for locator quality, assertion strength, and readability.
2. **Environment bootstrap** -- the seed proves the test harness works (Playwright installed, dev server accessible, auth functioning).
3. **Pattern template** -- the seed demonstrates imports, fixtures, naming conventions, and project-specific patterns.

Evidence: T2-B05 research verified seed file + 2-3 examples achieves 80-85% first-run pass rate.

## Location

The seed file lives in the project's test directory:

```
tests/
  seed.spec.ts         <-- primary seed (required)
  seeds/               <-- optional: role-specific seeds
    admin-seed.spec.ts
    guest-seed.spec.ts
```

## Required Components

Every seed file MUST include all five components:

| Component | Purpose | Example |
|-----------|---------|---------|
| Import statement | Establish test framework import pattern | `import { test, expect } from '@playwright/test'` or custom fixtures |
| Navigation | Prove base URL works | `await page.goto('/')` |
| At least one interaction | Prove browser interaction works | `await page.getByRole('button').click()` |
| At least one assertion | Prove assertions work | `await expect(page).toHaveURL('/dashboard')` |
| Accessibility-first locators | Establish locator quality standard | `getByRole`, `getByLabel`, not CSS selectors |

## Seed File Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('seed', () => {
  test('application loads and basic interaction works', async ({ page }) => {
    // Navigate to application
    await page.goto('/');

    // Verify initial page loaded
    await expect(page).toHaveTitle(/Your App/);

    // Perform a basic interaction
    await page.getByRole('link', { name: 'Products' }).click();

    // Verify navigation worked
    await expect(page).toHaveURL(/.*products/);
    await expect(page.getByRole('heading', { name: 'Products' })).toBeVisible();
  });
});
```

## Seed File with Authentication

For apps requiring login:

```typescript
import { test, expect } from '@playwright/test';

test.describe('seed - authenticated', () => {
  test('user can log in and reach dashboard', async ({ page }) => {
    // Given: User is on login page
    await page.goto('/login');

    // When: User submits valid credentials
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('SecurePass123');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Then: User reaches dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
  });
});
```

## Quality Attributes Checklist

When comparing generated tests against the seed, check:

- [ ] Uses accessibility-first locators (getByRole, getByLabel, getByText) -- not CSS classes or IDs
- [ ] Assertions verify state change (URL changed, element appeared) -- not just element presence
- [ ] No `waitForTimeout` calls (use web-first assertions instead)
- [ ] Test structure is readable (implicit Given-When-Then)
- [ ] Locators are cross-browser safe (no risky roles with name filters -- see @references/locator-strategy.md)
- [ ] Test name describes the user-visible behavior ("user can log in"), not the implementation ("click login button")

## Anti-Pattern Seed (DO NOT GENERATE)

```typescript
// EVERYTHING BELOW IS WRONG -- never generate tests like this

test('login test', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#email', 'user@example.com');          // CSS ID selector
  await page.fill('input[type="password"]', 'pass');       // Generic CSS
  await page.click('button.submit-btn');                   // Class selector
  await page.waitForTimeout(2000);                         // Hardcoded wait
  expect(page.url()).toContain('dashboard');                // Weak assertion
});
```

Problems: CSS selectors break on refactor, hardcoded waits are flaky, synchronous assertions race.

## Multi-Seed Strategy

For complex apps with multiple user roles, create role-specific seeds:

```
tests/seeds/
  admin-seed.spec.ts    -- seeds admin session, verifies admin dashboard
  member-seed.spec.ts   -- seeds member session, verifies member view
  guest-seed.spec.ts    -- seeds unauthenticated state, verifies public pages
  checkout-seed.spec.ts -- seeds cart with items, verifies checkout flow
```

Each seed initializes the specific state needed for its test domain.

## Required Seed Coverage

At minimum, the seed collection should cover these scenario types:

- **Authentication** -- login, logout, signup
- **Form submission** -- happy path, validation errors
- **CRUD operations** -- create, read, update, delete
- **Navigation** -- multi-step flows, back button, deep links
- **Edge cases** -- empty states, unauthorized access, error pages

## Few-Shot Reference Tests (Distinct from Seed)

The seed file and few-shot reference tests serve DIFFERENT purposes. Do not conflate them.

| Concern | Seed File | Few-Shot Reference Tests |
|---------|-----------|-------------------------|
| Purpose | Environment health check | Style teaching |
| Count | Exactly 1 (tests/seed.spec.ts) | 2-3 existing tests |
| When used | Before any generation — if seed fails, environment is broken | Before writing each test — to learn project conventions |
| What it teaches | Nothing about style | Assertion patterns, locator choices, naming conventions |
| Required? | Yes — generation refuses without it | No — if none exist, seed is the sole style reference |

### How to select few-shot reference tests:

1. Look for existing tests in `tests/*.spec.ts` (excluding seed)
2. Pick 2-3 that cover different patterns: one happy-path, one edge-case, one complex multi-step interaction
3. Read them before writing any generated test
4. Match their assertion style, naming conventions, and structural patterns

### If no reference tests exist:

Treat the seed file as the sole style reference. The first generated test becomes the reference for subsequent tests.

## How Agents Use the Seed File

| Agent | Usage |
|-------|-------|
| **test-planner** | Reads seed to understand existing fixtures, imports, and patterns before writing the test plan. |
| **test-generator** | Reads seed BEFORE generating any test. Compares generated output against seed quality attributes. Refuses to proceed without a seed file. |
| **test-executor** | Runs seed first to verify environment health before running the full suite. If seed fails, the environment is broken -- do not proceed. |
| **test-healer** | Uses seed patterns as reference when healing broken locators. Healed tests must match seed quality standards. |
