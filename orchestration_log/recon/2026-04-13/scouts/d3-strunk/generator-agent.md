# Strunk Analysis: generator-agent.md

## Critical & Severe

### R10 (Active Voice) - Severe
**Line 36:** "Detect mode from the dispatch prompt: if given a test plan reference, use create mode. If given specific test files and failure descriptions, use fix mode."
- Passive: "if given" (twice)
- Severity: Severe
- Suggested revision: "Detect mode from the dispatch prompt: test plan reference triggers create mode; specific test files and failure descriptions trigger fix mode."

**Line 42:** "If `tests/seed.spec.ts` is missing or failing, STOP."
- Passive: "is missing or failing"
- Severity: Moderate
- Suggested revision: "If `tests/seed.spec.ts` does not exist or fails, STOP."

**Line 52:** "Every test must contain at least one real assertion"
- Good: Active construction
- No violation

### R12 (Concrete Language) - Severe
**Line 54:** "Never log implementation gaps, harness errors, or test infrastructure issues as business findings. Harness errors are test failures. Implementation gaps are blockers. Neither are findings."
- Good: Concrete categories with clear distinctions
- No violation

**Line 91:** "Before writing any test, find 2-3 existing tests in `tests/*.spec.ts` covering similar patterns."
- Excellent: Specific number (2-3), concrete file path
- No violation

**Line 93:** "Before writing a test, verify planned locators exist in the live DOM using playwright-cli."
- Good: Concrete action, specific tool
- No violation

### R11 (Positive Form) - Severe
**Line 42:** "If `tests/seed.spec.ts` is missing or failing, STOP. Write `.playwright/orchestrator-status.json` with status `NEEDS_CONTEXT` and blocker message. Do not proceed."
- Triple negative: "missing", "Do not proceed", plus blocker concept
- Severity: Severe
- Suggested revision: "If `tests/seed.spec.ts` is missing or failing, STOP. Write `.playwright/orchestrator-status.json` with status `NEEDS_CONTEXT` and blocker message, then exit."

**Line 52:** "No AI libraries, no MCP, no runtime LLM calls."
- Triple negative for emphasis
- Severity: Moderate (emphatic denial justified)
- Suggested revision: "Import only from `@playwright/test` or project fixtures." (already stated, so "No X, no Y, no Z" is redundant emphasis)

**Line 54:** "Never log implementation gaps, harness errors, or test infrastructure issues as business findings."
- Negative prohibition
- Severity: Moderate
- Suggested revision: "Log only actual business findings, excluding implementation gaps, harness errors, and test infrastructure issues."

## Moderate

### R13 (Needless Words) - Moderate
**Line 33:** "You transform test plans into executable Playwright .spec.ts files AND fix structural issues in existing tests."
- "AND" in caps adds emphasis but is redundant with "and"
- Severity: Minor
- Suggested revision: "You transform test plans into executable Playwright .spec.ts files and fix structural issues in existing tests."

**Line 38:** "Detect mode from the dispatch prompt: if given a test plan reference, use create mode. If given specific test files and failure descriptions, use fix mode."
- "if given" repeated
- Severity: Moderate
- Suggested revision: "Detect mode from the dispatch prompt: test plan reference → create mode; test files + failure descriptions → fix mode."

**Line 46:** "One test at a time. Write ONE test, run it, fix until green, THEN write the next."
- Repetition of concept (one test, ONE test, next)
- Severity: Minor (emphatic repetition justified)
- No violation (purposeful emphasis)

**Line 86:** "If no reference tests exist, seed is your sole style reference."
- Concise
- No violation

### R15 (Parallel Construction) - Moderate
**Lines 41-56:** Hard Rules list
```
1. **Seed file is mandatory.** If `tests/seed.spec.ts` is missing or failing, STOP. Write `.playwright/orchestrator-status.json` with status `NEEDS_CONTEXT` and blocker message. Do not proceed.

2. **Test plan is mandatory.** If `.playwright/test-plan.md` is missing, STOP. Write status file with `NEEDS_CONTEXT`.

3. **One test at a time.** Write ONE test, run it, fix until green, THEN write the next. Never batch-generate. Never proceed past a failing test.

4. **Accessibility-first locators only.** No CSS class or ID selectors. Use getByRole, getByLabel, getByText. Follow @references/locator-strategy.md.

5. **Pure output.** Generated .spec.ts files import only from `@playwright/test` or project fixtures. No AI libraries, no MCP, no runtime LLM calls.

6. **No hollow tests.** Every test must contain at least one real assertion (`expect()`) or comparison. A test that navigates to a page and logs "needs implementation" is not a test — it's a placeholder that creates false confidence. If you cannot write a meaningful assertion, write the test as `test.skip` with a reason, not as a passing hollow test.

7. **No fake findings.** Never log implementation gaps, harness errors, or test infrastructure issues as business findings. Harness errors are test failures. Implementation gaps are blockers. Neither are findings.
```
- Inconsistent length: Rules 1-2 have multi-sentence explanations with specific actions; Rule 3 has imperatives; Rules 4-5 are terse; Rules 6-7 are long explanatory paragraphs
- Inconsistent structure: Some start with bold title then stop action; some start with prohibition; some explain rationale
- Severity: Moderate
- Suggested revision: Standardize to "**Title.** Directive. [Action on violation if applicable.]" format

**Lines 187-196:** Fix Mode diagnosis list
```
   - Serial execution of independent tests (should be parallel-safe with isolated fixtures)
   - Fixture teardown race conditions (missing `await`, shared state between tests)
   - Missing or incorrect wait strategies (using `networkidle` instead of targeted waits, missing explicit `waitFor`)
   - Missing per-test timeout budgets (`test.setTimeout()`)
   - Shared mutable state between test blocks
```
- Inconsistent: Some items have parenthetical explanations; some don't
- Severity: Minor
- Suggested revision: Either add explanations to all or remove from all

### R18 (Emphatic Position) - Moderate
**Line 33:** "You transform test plans into executable Playwright .spec.ts files AND fix structural issues in existing tests. Two modes:"
- Ends weakly with "Two modes:" (transition phrase)
- Severity: Minor
- Suggested revision: Move mode explanation to opening: "Two modes: transform test plans into executable Playwright .spec.ts files (create) or fix structural issues in existing tests (fix)."

**Line 52:** "A test that navigates to a page and logs 'needs implementation' is not a test — it's a placeholder that creates false confidence."
- Ends strongly with "false confidence" (key problem)
- Good
- No violation

**Line 130:** "Do NOT move to next test until current test passes."
- Ends strongly with emphatic prohibition
- Good
- No violation

## Minor & Stylistic

### R13 (Needless Words) - Minor
**Line 60:** "Read these files before starting:"
- Concise
- No violation

**Line 70:** "Run the seed test:"
- Concise
- No violation

**Line 85:** "Before writing any test, find 2-3 existing tests in `tests/*.spec.ts` covering similar patterns. Read them. Match their assertion style, naming conventions, describe block structure."
- Three short sentences for emphasis
- Justified
- No violation

### R11 (Positive Form) - Minor
**Line 130:** "Do NOT move to next test until current test passes."
- Negative prohibition
- Severity: Minor
- Suggested revision: "Write the next test only after the current test passes."

**Line 135:** "Risky Locators (Avoid or Use .or() Fallback)"
- Negative framing in title
- Severity: Minor
- Suggested revision: "Fallback-Required Locators (Use .or())"

### R10 (Active Voice) - Minor
**Line 200:** "What Fix Mode Does NOT Do"
- List of negatives (what it doesn't do)
- Severity: Minor
- Suggested revision: "Fix Mode Scope" with positive list of what it does

**Line 207:** "Write `.playwright/orchestrator-status.json`:"
- Good: Active imperative
- No violation

## Summary

**Strengths:**
- Generally concrete with specific numbers (2-3 tests, 3 fix iterations)
- Strong use of imperatives and active voice in workflow sections
- Good emphatic endings in key prohibition statements
- Clear mode distinction and workflow steps

**Priority fixes:**
1. Line 36 (R10 Severe): Convert passive "if given" constructions to active triggers
2. Lines 41-56 (R15 Moderate): Standardize Hard Rules parallel structure (length and format consistency)
3. Line 42 (R11 Severe): Convert triple-negative blocker instruction to positive form
4. Line 38 (R13 Moderate): Reduce repeated "if given" phrasing

**Total findings:**
- Critical/Severe: 5 (2 active voice, 3 positive form)
- Moderate: 6 (2 needless words, 2 parallel construction, 1 positive form borderline, 1 emphatic position)
- Minor/Stylistic: 5 (1 needless words, 3 positive form, 1 active voice)
