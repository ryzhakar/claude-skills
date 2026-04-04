---
name: test-generator
description: >
  Transform structured test plans into executable Playwright .spec.ts files with accessibility-first
  locators. Use when user asks to "generate tests from plan", "create Playwright tests", "write 
  .spec.ts files", "implement test scenarios", "convert plan to tests", or after test-planner 
  produces a plan. REQUIRES a seed file -- refuses without one. Generates one test at a time: 
  write, run, verify, then next. Output is pure Playwright + TypeScript with zero AI runtime 
  dependency.
---

# Test Generator

Transform test plans into executable Playwright .spec.ts files, one test at a time, with accessibility-first locators and zero AI runtime dependency in generated output.

## Core Rules

1. **Seed file is mandatory.** If `tests/seed.spec.ts` does not exist, STOP. Provide the template from @../../references/seed-file-spec.md and ask the user to create one.
2. **One test at a time.** Write ONE test -> run it -> fix until green -> THEN write the next. Never batch-generate.
3. **Verify selectors before writing.** Every locator in a test MUST be confirmed against the live DOM (via MCP snapshot or CLI exploration) before the test is written.
4. **Accessibility-first locators.** Follow @../../references/locator-strategy.md. No CSS class or ID selectors in generated tests.
5. **Pure output.** Generated .spec.ts files import only from `@playwright/test` or project fixtures. No AI libraries, no MCP references, no runtime LLM calls.

## Workflow

### Phase 1: Pre-Flight Checks

Before generating any test:

1. **Read test plan.** Open `.playwright/test-plan.md`. If missing, tell the user to run the test-planner skill first.

2. **Read selector strategy.** Open `.playwright/selector-strategy.md`. This defines which locator approach to use per page.

3. **Read seed file.** Open `tests/seed.spec.ts`.
   - Missing: STOP. Provide the seed template from @../../references/seed-file-spec.md. Ask the user to create one and verify it passes.
   - Present: Note the import pattern, fixture usage, naming conventions.

4. **Check existing tests.** Read any `tests/*.spec.ts` files to learn project patterns (describe block style, helper usage, assertion style).

5. **Verify dev server is running:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
   ```
   If not 200, ask the user to start the server.

### Phase 2: Choose Generation Strategy

Present the user with two options:

"I see {N} scenarios in the test plan. Two approaches available:

1. **CLI codegen** -- You record interactions with `npx playwright codegen {URL}`, I refine the output with accessibility-first locators. ~3,000 tokens per 5 tests.
2. **Direct generation** -- I navigate the app with MCP, verify every selector, and write the tests. ~30,000 tokens per 5 tests.

Which approach works for your workflow?"

### Phase 3a: CLI Codegen Mode

If the user chooses codegen:

1. Instruct:
   ```
   Run: npx playwright codegen {URL}
   Perform the scenario manually, then save the generated file and tell me the path.
   ```

2. Read the generated file. Codegen output uses raw CSS selectors.

3. Refine the test:
   - Replace ALL CSS selectors with accessibility-first locators per @../../references/locator-strategy.md
   - Replace `page.click('.btn-submit')` with `page.getByRole('button', { name: 'Submit' }).click()`
   - Replace `page.fill('#email')` with `page.getByLabel('Email').fill('...')`
   - Add web-first assertions (auto-retrying, not synchronous checks)
   - Add `test.step()` blocks if the test has 3+ interactions
   - Match import pattern from seed file

4. Run quality check (see Phase 4 quality checklist below).

5. Verify TypeScript compiles:
   ```bash
   npx tsc --noEmit
   ```

6. Run the test:
   ```bash
   npx playwright test tests/{file}.spec.ts
   ```

7. If failing, fix and re-run. Do not proceed to the next test until this one passes.

### Phase 3b: Direct Generation Mode

If generating tests directly:

**Step 1: Pre-Flight Selector Verification (MANDATORY)**

Navigate to every page involved in the test scenario. Take an accessibility snapshot. Confirm each planned locator exists in the live DOM.

Using MCP:
```
browser_navigate({ url: 'http://localhost:3000/login' })
browser_snapshot()
```

Read the accessibility tree. Compare `ref` values against the locator strategy from `.playwright/selector-strategy.md`.

If a planned locator does not exist:
- Check if the element uses a different label or role
- If no semantic locator works, use `getByTestId()`
- If no test ID exists, flag for dev team and use `.or()` fallback

**Step 2: Write ONE Test**

```typescript
import { test, expect } from '@playwright/test';

test.describe('{Feature Name}', () => {
  test('{user-visible behavior description}', async ({ page }) => {
    // Given: precondition
    await page.goto('/login');

    // When: user action
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('SecurePass123');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Then: expected outcome
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
  });
});
```

**Step 3: Run That ONE Test**

```bash
npx playwright test tests/{file}.spec.ts --grep "{test name}"
```

**Step 4: Fix Until Green**

If failing, diagnose:
- Locator not found: take fresh `browser_snapshot()`, compare, fix the locator
- Timeout: check if element appears after navigation. Use web-first assertion, NOT `waitForTimeout`
- Assertion mismatch: verify expected value against actual page state

Do NOT move to the next test until this one passes.

**Step 5: Repeat** steps 2-4 for each remaining scenario.

### Phase 4: Quality Check

After writing each test, verify against seed file quality attributes:

- [ ] Uses getByRole / getByLabel / getByText (not CSS classes or IDs)
- [ ] Assertions verify state change (URL, text, visibility) -- not just element presence
- [ ] No `waitForTimeout` calls (exception: 150ms WASM hydration buffer)
- [ ] Readable structure (Given-When-Then comments or `test.step()` blocks)
- [ ] Cross-browser safe locators (no risky roles with name filters -- see below)
- [ ] Test name describes user behavior ("user can log in"), not implementation ("click login button")

**Risky locators to avoid** (from @../../references/locator-strategy.md):
- `getByRole('caption', { name })` -- Chromium/Firefox/WebKit inconsistency
- `getByRole('list')` on styled lists -- Safari removes list role with `list-style: none`
- `getByRole('form', { name })` -- Playwright issue #35720
- `getByRole('alert', { name })` -- cannot select with name parameter
- `getByRole('combobox', { name })` -- selection fails with name

When uncertain about cross-browser safety, use the `.or()` fallback:
```typescript
const submitButton = page
  .getByRole('button', { name: 'Submit' })
  .or(page.getByTestId('submit-button'));
```

### Phase 5: Page Objects (if needed)

Extract page objects when a flow has 5+ steps or actions are reused across multiple tests.

Create `tests/pages/{PageName}.page.ts`:

```typescript
import { type Page, type Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

Register in `tests/fixtures.ts`:

```typescript
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/login.page';

export const test = base.extend<{
  loginPage: LoginPage;
}>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
});

export { expect } from '@playwright/test';
```

Then update test imports:

```typescript
import { test, expect } from './fixtures';

test('user can log in', async ({ loginPage, page }) => {
  await loginPage.goto();
  await loginPage.login('user@example.com', 'SecurePass123');
  await expect(page).toHaveURL('/dashboard');
});
```

### Phase 6: Verify Full Suite

After all tests for a scenario pass individually:

1. Run serial (catches order-dependent tests):
   ```bash
   npx playwright test --workers=1
   ```

2. Run parallel (catches test isolation issues):
   ```bash
   npx playwright test --workers=4
   ```

3. If failures appear in parallel but not serial, tests share state. Fix with worker-scoped fixtures or unique test data:
   ```typescript
   // tests/helpers/test-data.ts
   export function createTestData(workerId: number) {
     return {
       email: `test-user-${workerId}-${Date.now()}@example.com`,
       username: `testuser_${workerId}_${Date.now()}`,
     };
   }
   ```

### Phase 7: Mark Scenario Complete

Update `.playwright/test-plan.md` checkboxes:

```markdown
| Feature | Suite | Tests | Priority | Status |
|---------|-------|-------|----------|--------|
| Authentication | auth.spec.ts | 8 | P0 | [x] |
```

Report to the user which scenarios are complete and which remain.

## Locator Priority

For the complete locator priority hierarchy and code patterns, see @../../references/locator-strategy.md

## WASM/Leptos Applications

For navigation patterns and hydration handling in WASM frameworks (Leptos, Yew, etc.), see @../../references/locator-strategy.md

## Composability

If tdd skill is available:
  Follow red-green-refactor. Write a failing test first, implement minimal feature code to pass, then refactor. Natural fit with one-test-at-a-time workflow.
Otherwise:
  Generate tests for existing features.

If systematic-debugging skill is available:
  Use root-cause tracing when generated tests fail unexpectedly (4-phase: investigate, hypothesize, test, fix).
Otherwise:
  Use Playwright trace viewer:
  ```bash
  npx playwright test --trace on
  npx playwright show-trace test-results/**/trace.zip
  ```

If agentic-delegation skill is available:
  Fan out test generation across agents -- one agent per test suite. Each agent reads the plan, generates tests for its assigned suite, reports completion.
Otherwise:
  Generate tests sequentially, one suite at a time.

## References

- @../../references/locator-strategy.md -- Locator decision tree, cross-browser safety rules, risky roles
- @../../references/seed-file-spec.md -- Seed file structure, template, quality attributes, anti-patterns
- @../../references/file-protocol.md -- File protocol specifications
- @../../references/mcp-tools.md -- MCP tool usage guidelines
