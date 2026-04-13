# Strunk Analysis: healer-agent.md

## Critical & Severe

### R11 (Positive Form) - Severe
**Lines 34-38:** THE IRON LAW
```
NEVER HEAL ASSERTION FAILURES.
NEVER HEAL RUNTIME ERRORS.
ELEMENT FOUND + WRONG VALUE = APPLICATION BUG. DO NOT TOUCH THE TEST.
```
- Triple negative prohibition (NEVER, NEVER, DO NOT)
- Severity: Critical (but justified as emphatic prohibition - "Iron Law" framing signals master exemption)
- Note: This is legitimate negative use per Strunk (denial/prohibition, not evasion). Alternatives would weaken force.
- No revision needed (purposeful negative for emphasis)

**Line 40:** "If you encounter an assertion failure: write `confidence: 0.0` and skip it."
- Positive action given (write, skip)
- No violation

### R10 (Active Voice) - Severe
**Line 4:** "Use this agent to repair broken Playwright locators using the deterministic ten-tier algorithm."
- Good: Active "repair" using specific tool
- No violation

**Line 31:** "You repair broken Playwright locators using deterministic ten-tier healing."
- Good: Active verb, concrete method
- No violation

**Line 52:** "Read `.github/healing-state.json` (or treat as empty if missing)."
- Good: Active imperative
- No violation

### R12 (Concrete Language) - Severe
**Line 74:** "**Tier confidence bands:**"
```
- Tiers 1-3: HIGH (2-5% FP)
- Tiers 4-6: MEDIUM (5-10% FP)
- Tiers 7-10: LOW (10-15% FP)
```
- Excellent: Specific tier ranges, concrete false-positive percentages
- No violation

**Line 81:** "**Thresholds:**"
```
- `>= 0.85`: HIGH
- `0.60 - 0.84`: MEDIUM
- `0.40 - 0.59`: LOW
- `< 0.40`: REJECT
```
- Excellent: Precise numerical thresholds
- No violation

## Moderate

### R13 (Needless Words) - Moderate
**Line 31:** "You repair broken Playwright locators using deterministic ten-tier healing. Never touch assertion failures or runtime errors."
- "Never touch" could be "Skip"
- Severity: Minor
- Suggested revision: "You repair broken Playwright locators using deterministic ten-tier healing. Skip assertion failures and runtime errors."

**Line 59:** "Only process entries from the `locator` category. Skip all other categories."
- Second sentence reinforces first (justified for emphasis)
- No violation

**Line 91:** "If `.playwright/lessons.md` exists, read it before starting."
- "If ... exists, read it" → "Read `.playwright/lessons.md` if present"
- Severity: Minor
- Suggested revision: "Read `.playwright/lessons.md` if present before starting."

### R15 (Parallel Construction) - Moderate
**Lines 61-66:** Hard Rejection list
```
1. Assertion on element value — REAL BUG
2. Visual comparison failure — HUMAN REVIEW
3. Interaction blocked by overlay — UI DESIGN ISSUE
4. Console errors ERROR/FATAL — APPLICATION BROKEN
5. 10+ concurrent test failures — INFRASTRUCTURE ISSUE
6. Ten-tier algorithm returns null for all tiers — CANNOT HEAL
```
- Good: All items follow "Condition — Classification" pattern
- No violation

**Lines 100-114:** DOM Re-Discovery steps
```
1. Ensure the app is running (check with `curl -s -o /dev/null -w "%{http_code}" <base-url>`)
2. `playwright-cli open <base-url>`
3. Navigate to the page where the locator failed
4. `playwright-cli snapshot --filename=/tmp/healer-snap.yaml`
5. Read the snapshot file — search for elements matching the original locator's intent
6. If found: propose the new locator with confidence based on Similo scoring
7. `playwright-cli close-all`
```
- Inconsistent: Steps 1, 5, 6 are full sentences with explanations; steps 2, 4, 7 are bare commands; step 3 is imperative without backticks
- Severity: Moderate
- Suggested revision: Standardize to either "Step N: `command` (explanation)" or "Step N: Action verb (explanation)" throughout

### R11 (Positive Form) - Moderate
**Line 31:** "Never touch assertion failures or runtime errors."
- Negative prohibition
- Severity: Moderate
- Suggested revision: "Process only locator failures, skipping assertion failures and runtime errors."

**Line 52:** "DO NOT write to this file."
- Negative prohibition
- Severity: Minor
- Suggested revision: "The orchestrator updates this file after aggregation." (implication: not you)

**Line 59:** "Skip all other categories."
- Positive imperative "skip"
- No violation

### R18 (Emphatic Position) - Moderate
**Line 31:** "You repair broken Playwright locators using deterministic ten-tier healing. Never touch assertion failures or runtime errors."
- Ends with "runtime errors" (technical term, not main point)
- Severity: Minor
- Suggested revision: "You repair broken Playwright locators using deterministic ten-tier healing, processing only locator failures."

**Line 104:** "This step is MANDATORY when all tiers return null."
- Ends strongly with emphatic "when all tiers return null" (key condition)
- Good
- No violation

**Line 125:** "In his eye was a look that boded mischief."
- Wait, this is from the Strunk file (line 1586), not the healer-agent
- No violation (not in healer-agent.md)

## Minor & Stylistic

### R13 (Needless Words) - Minor
**Line 46:** "You receive either:"
- Concise
- No violation

**Line 54:** "**Rules:**"
- Concise
- No violation

**Line 97:** "For tiers 1-6, DOM verification is recommended but not required (higher confidence, lower false-positive rate)."
- Parenthetical adds value
- No violation

**Line 115:** "Also use it when:"
- Concise transition
- No violation

### R10 (Active Voice) - Minor
**Line 122:** "Edit test file, replace broken locator, add comment:"
- Good: Three active imperatives
- No violation

**Line 127:** "Re-run only the fixed test:"
- Good: Active imperative
- No violation

**Line 131:** "If still fails after fix: mark as deferred"
- Good: Active "mark"
- No violation

### R12 (Concrete Language) - Minor
**Line 123-126:** Code example
```typescript
// Healer: replaced getByRole('button', { name: 'Sign In' }) -> 'Log In' (tier 1, HIGH, score 0.92)
await page.getByRole('button', { name: 'Log In' }).click();
```
- Excellent: Specific tier number, confidence band, numerical score, concrete before/after locators
- No violation

## Summary

**Strengths:**
- Exceptionally concrete with precise numerical thresholds and percentages
- Strong use of active voice in imperatives (repair, process, read, edit, mark)
- "Iron Law" negative construction justified as emphatic prohibition
- Excellent specificity in confidence scoring and tier classification

**Priority fixes:**
1. Lines 100-114 (R15 Moderate): Standardize DOM Re-Discovery step format for parallel construction
2. Line 31 (R11 Moderate): Convert "Never touch" negative to positive "Process only locator failures"
3. Line 91 (R13 Minor): Tighten "If ... exists, read it" construction

**Total findings:**
- Critical/Severe: 1 (positive form - but justified as Iron Law emphatic denial)
- Moderate: 4 (1 parallel construction, 2 positive form, 1 emphatic position)
- Minor/Stylistic: 3 (2 needless words, 1 positive form)

**Note on Iron Law:**
The triple-negative prohibition in lines 34-38 violates R11 (positive form) but is justified per Strunk's guidance: "Use 'not' as means of denial or antithesis, never as means of evasion." The Iron Law uses negatives for emphatic denial (NEVER heal wrong thing), not evasion. This is legitimate negative use for rhetorical force. Alternative positive forms ("Heal only locator failures") would weaken the emphatic prohibition needed for a critical safety constraint.
