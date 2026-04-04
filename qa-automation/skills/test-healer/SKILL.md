---
name: test-healer
description: >
  Diagnose test failures, distinguish real bugs from test brittleness, and auto-fix broken locators.
  Use when "heal tests", "fix broken tests", "auto-fix test failures", "repair locators",
  "self-heal tests", "why are my tests failing", "fix flaky tests", "update broken selectors",
  or after test-executor classifies failures in .ai-failures.json. Applies deterministic ten-tier
  self-healing first (zero LLM cost, 2-5% false positive rate), falls back to LLM reasoning only
  when deterministic healing fails, computes confidence scores, and creates fix PRs with
  confidence-based routing. NEVER heals assertion failures or runtime errors.
---

# Test Healer

Diagnose and repair broken Playwright tests. Deterministic healing first, LLM fallback second. Never heal real bugs.

## The Iron Law

```
NEVER HEAL ASSERTION FAILURES.
NEVER HEAL RUNTIME ERRORS.
ELEMENT FOUND + WRONG VALUE = APPLICATION BUG. DO NOT TOUCH THE TEST.
```

Assertion failures mean the test correctly detected a real bug. Healing the test lets the bug ship.

## Workflow

### Phase 1: Read Failure Report

Read the classified failure report:

```bash
cat .ai-failures.json 2>/dev/null
```

Contains failures in categories: `locator`, `timing`, `data`, `visual`, `interaction`, `other`. Only `locator` failures are healing candidates.

If `.ai-failures.json` does not exist, parse `results.json` directly using patterns from @references/failure-heuristics.md:

```bash
cat results.json
```

Classify with:
- Locator: `/locator\.|selector|element not found|waiting for|getBy|resolved to 0 elements|resolved to hidden/i`
- Timing: `/timeout|timed out|race condition|navigation timeout|waitFor.*exceeded/i`
- Data: `/expected.*to(Equal|Be|Have|Contain|Match)|AssertionError|toHaveText|toContain|toHaveURL/i`
- Visual: `/screenshot|visual.*regression|pixel.*diff|snapshot.*mismatch|toMatchSnapshot|toHaveScreenshot/i`
- Interaction: `/intercept|not scrollable|drag.*drop|click.*intercepted|obscured|pointer.*event/i`

### Phase 2: Check Circuit Breaker

```bash
cat .github/healing-state.json 2>/dev/null || echo '{"healing_attempts":{}, "prs_created":0, "blocklist":[]}'
```

**Rules:**
- Max 2 healing attempts per test. After 2, skip it and mark for manual investigation.
- Max 3 PRs per CI run. After 3, stop healing.
- Tests failing healing twice within 24h are blocklisted.

If circuit breaker is tripped for all remaining failures, inform the user that manual intervention is required. Do not attempt further healing.

### Phase 3: Reject Non-Healable Failures

For each locator failure, apply hard rejection rules before scoring. See @references/confidence-scoring.md for the full algorithm.

**Hard rejection (score = 0.0, skip immediately):**

1. Element exists but assertion on its value failed -- REAL BUG (data failures)
2. Visual comparison failures -- REQUIRE HUMAN REVIEW (visual failures)
3. Interaction blocked by overlay or pointer events -- UI DESIGN ISSUE (interaction failures)
4. Console errors at ERROR or FATAL severity -- APPLICATION BROKEN
5. More than 10 concurrent test failures -- INFRASTRUCTURE ISSUE
6. No candidate element found by ten-tier algorithm -- CANNOT HEAL

**If none of the above match**, read the test file and identify the broken locator expression:

```bash
# Find the failing line and surrounding context
grep -n "getByRole\|getByTestId\|getByLabel\|getByText\|locator(" tests/auth.spec.ts
```

Classify the broken locator type:
- `getByRole('button', { name: 'Submit' })` -- role + name broke
- `getByTestId('submit-btn')` -- test-id removed or renamed
- `getByLabel('Email')` -- label text changed
- `page.locator('.submit-btn')` -- CSS class changed
- `getByText('Sign In')` -- visible text changed

See @references/failure-heuristics.md for the complete decision tree with false positive scenarios.

### Phase 4: Apply Deterministic Ten-Tier Healing

For each locator failure that passed Phase 3, apply the ten-tier algorithm. This is deterministic, zero LLM cost, 2-5% false positive rate.

See @references/ten-tier-algorithm.md for the complete TypeScript implementation with `DOMExtractor`, `SmartFind`, and `LocatorCache` classes.

Tiers 1-3 = HIGH confidence. Tiers 4-6 = MEDIUM. Tiers 7-10 = LOW. See @references/ten-tier-algorithm.md for full definitions and TypeScript implementation.

**Healing process:**

1. Read the test file. Identify the broken locator expression.
2. Navigate to the page where the failure occurred (use `npx playwright test --debug` or read the trace).
3. Inspect the page to find the current state of the element.
4. Apply the ten-tier algorithm: which tier resolves this element now?
5. Choose the highest-confidence tier that matches.
6. Write the new locator into the test file.

**Tier-based confidence:**
- Tiers 1-3: HIGH (2-5% FP rate). Auto-apply.
- Tiers 4-6: MEDIUM (5-10% FP rate). Create review PR.
- Tiers 7-10: LOW (10-15% FP rate). Do not create PR. Require manual fix.

### Phase 5: LLM Fallback (When Deterministic Fails)

If the ten-tier algorithm cannot find the element (returns null for all tiers), fall back to LLM-based healing. This is more expensive (10K+ tokens per failure, 8-15% FP rate).

LLM fallback process:

1. Read the test file, the error message, and the page DOM (via trace or snapshot).
2. Reason about what the element should be based on test context and surrounding code.
3. Propose a new locator with justification.
4. Score the proposed fix using the confidence algorithm (same thresholds apply).
5. Apply only if score >= 0.60.

LLM healing is NEVER auto-applied at HIGH confidence. Maximum confidence for LLM fixes is MEDIUM (requires human review).

### Phase 6: Handle Timing Failures

Timing failures from the `timing` category are NOT healed with locator changes.

Replace anti-patterns with web-first assertions:

```typescript
// BEFORE (anti-pattern):
await page.waitForTimeout(2000);
expect(await page.textContent('.result')).toBe('Done');

// AFTER (web-first assertion):
await expect(page.locator('.result')).toHaveText('Done', { timeout: 10000 });
```

```typescript
// BEFORE (anti-pattern):
await page.goto('/products');
await page.waitForSelector('.product-tile');

// AFTER:
await page.goto('/products', { waitUntil: 'domcontentloaded' });
await expect(page.locator('.product-tile').first()).toBeVisible();
```

Warn user that timing fixes indicate test fragility needing deeper investigation.

### Phase 7: Compute Overall Confidence

Compute confidence per @references/confidence-scoring.md using primary signals (70%: error type, DOM changes, console errors) and secondary signals (30%: API health, element similarity, history, cluster analysis).

**Decision thresholds:**

| Score | Decision | Action |
|-------|----------|--------|
| 0.85 - 1.0 | HIGH | Auto-apply. In CI: auto-merge PR. |
| 0.60 - 0.84 | MEDIUM | Create PR requiring human review within 24h. |
| 0.40 - 0.59 | LOW | Fail the test. Require manual investigation. |
| 0.0 - 0.39 | REJECT | Never heal. Real bug. |

### Phase 8: Apply and Verify Fixes

For each fix with confidence >= 0.60:

1. Edit the test file. Replace the broken locator. Add a comment:
   ```typescript
   // Healer: replaced getByRole('button', { name: 'Sign In' }) -> 'Log In' (tier 1, HIGH)
   await page.getByRole('button', { name: 'Log In' }).click();
   ```

2. Re-run ONLY the fixed tests:
   ```bash
   npx playwright test tests/auth.spec.ts --reporter=json,line
   ```

3. If test still fails: increment circuit breaker counter. If second attempt, add to blocklist. Report failure and recommend manual investigation.

4. If test passes: fix is validated. Proceed to Phase 9.

### Phase 9: Create Fix Artifacts

**Interactive mode (local development):**
Present changes to user. Show what changed and why. Let user approve.

**CI/CD mode:**
Create branch and PR. See @references/cicd-workflow.md for the complete GitHub Actions workflow.

HIGH confidence:
```bash
git checkout -b healer/auto-fix-$(date +%s)
git add tests/
git commit -m "fix(tests): auto-heal locator failures (HIGH confidence)"
git push origin HEAD
gh pr create --title "fix(tests): Auto-heal test failures (HIGH confidence)" \
  --body "Deterministic healing applied. Tests re-validated."
gh pr merge --auto --squash
```

MEDIUM confidence:
```bash
git checkout -b healer/review-fix-$(date +%s)
git add tests/
git commit -m "fix(tests): heal locator failures (MEDIUM confidence, review required)"
git push origin HEAD
gh pr create --title "fix(tests): Heal test failures (REVIEW REQUIRED)" \
  --body "Medium confidence healing. Review locator changes before merging."
```

LOW confidence: No PR. Report failure, recommend manual investigation.

### Phase 10: Update State

Update `.github/healing-state.json`:
```json
{
  "healing_attempts": {
    "auth.spec.ts:12:user can log in": 1,
    "checkout.spec.ts:45:checkout flow completes": 2
  },
  "prs_created": 1,
  "blocklist": [],
  "last_updated": "2026-04-03T12:00:00Z"
}
```

Write `.healing-results.json`:
```json
{
  "timestamp": "2026-04-03T12:00:00Z",
  "method": "deterministic",
  "healed": 2,
  "skipped": 1,
  "failed": 0,
  "confidence": "HIGH",
  "fixes": [
    {
      "test": "user can log in",
      "file": "tests/auth.spec.ts",
      "line": 12,
      "tier": 1,
      "tier_name": "role + accessible name",
      "original_locator": "getByRole('button', { name: 'Sign In' })",
      "healed_locator": "getByRole('button', { name: 'Log In' })",
      "confidence": 0.92,
      "verified": true
    }
  ],
  "skipped_reasons": [
    {
      "test": "displays KPI cards",
      "file": "tests/dashboard.spec.ts",
      "reason": "Assertion failure - real bug, not locator issue"
    }
  ]
}
```

## Composability

If the test-executor skill is available:
  Executor produces `.ai-failures.json` with pre-classified failures.
  Read that file directly instead of parsing raw `results.json`.
Otherwise:
  Parse `results.json` manually using the classification patterns
  from @references/failure-heuristics.md.

If the systematic-debugging skill is available:
  For data/assertion failures indicating real bugs, invoke systematic-debugging
  to apply the 4-phase root cause protocol (investigate, hypothesize, test, fix).
Otherwise:
  Flag real bugs for manual investigation. Present the error message, test file,
  and line number. Recommend checking recent code changes and console errors.

If the tdd skill is available:
  After healing, follow refactor discipline: get to GREEN first, then refactor
  the test for clarity and robustness. Do not refactor a failing test.
Otherwise:
  Apply the fix directly. Keep changes minimal and focused on the broken locator.

If the agentic-delegation skill is available:
  For multiple locator failures (5+), fan out healing agents -- one per failure.
  Each agent reads the test file, applies the ten-tier algorithm, and reports results.
  Orchestrator collects results and creates a single PR.
Otherwise:
  Heal failures sequentially, one at a time.

## References

- @references/ten-tier-algorithm.md -- Complete TypeScript implementation of the ten-tier locator discovery and self-healing algorithm (ported from renjithnj/zero-cost-self-healing-qa). Read when applying deterministic healing in Phase 4.
- @references/confidence-scoring.md -- Confidence scoring algorithm with signal weights, element similarity, flaky test detection, and decision thresholds. Read when computing scores in Phase 7 or applying hard rejection rules in Phase 3.
- @references/cicd-workflow.md -- GitHub Actions workflow for automated healing with circuit breaker, artifact collection, and confidence-based PR routing. Read when setting up CI/CD integration.
- @references/failure-heuristics.md -- Decision tree for classifying failures as locator vs timing vs data vs real bug, with false positive scenarios. Read when classifying failures in Phase 3 without executor output.
- @../../references/locator-strategy.md -- Cross-browser locator decision framework shared with other skills. Read when selecting replacement locators.
