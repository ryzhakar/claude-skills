# Prompt Evaluation: generator-agent Agent

**Type:** Agent  
**File:** `/Users/ryzhakar/pp/claude-skills/qa-automation/agents/generator-agent.md`  
**Overall Score:** 85/100 (Good)

---

## Summary

The generator-agent is a comprehensive, technically sophisticated dual-mode agent (create/fix) with excellent constraint enforcement, strong workflow discipline (one test at a time), and exceptional anti-pattern awareness (no hollow tests, no fake findings). Approaching complexity threshold at 233 lines. Needs improvement in term precision, progressive disclosure, and example completeness.

---

## Critical Issues (Must Fix)

None.

---

## Warnings (Should Fix)

### W1: Length Approaching Threshold
**Criterion:** AGT-9 (MUST_NOT exceed 500 lines without progressive disclosure)  
**Location:** 233 lines  
**Evidence:** While under 500-line limit, this is the longest agent in the set. Heavy on inline guidance that could be extracted.

**Fix:** Extract to reference files:
- Lines 88-120 (few-shot + Given/When/Then pattern) → `@references/test-patterns.md`
- Lines 141-154 (risky locators) → `@references/locator-strategy.md` (merge with existing)
- Lines 156-162 (Shadow DOM, Page Objects) → `@references/test-patterns.md`

### W2: Vague Terms - Quality Descriptors
**Criterion:** CLR-2  
**Location:** Multiple  
**Evidence:**
- Line 52: "meaningful assertion" — what makes it meaningful?
- Line 66: "real assertion" — vs fake?
- Line 74: "similar patterns" — how to determine similarity?

**Fix:** Define:
- "meaningful assertion: verifies externally observable behavior (DOM state, URL, visibility) not internal state"
- "similar patterns: same page object usage, same describe/test structure, same assertion style"

### W3: Missing Output Examples
**Criterion:** EXM-3 (SHOULD show both input AND expected output)  
**Location:** Lines 9-25 frontmatter  
**Evidence:** Examples show dispatch triggers but not agent outputs (generated test code, status files).

**Fix:** Add example showing one complete generated .spec.ts file in frontmatter.

### W4: Contradictory Guidance - Seed vs Few-Shot
**Criterion:** CLR-3  
**Location:** Lines 62-64, 73-76  
**Evidence:**
- Line 62: "Read... `tests/seed.spec.ts` — import pattern, fixture usage, naming conventions"
- Line 74: "find 2-3 existing tests in `tests/*.spec.ts` covering similar patterns"
- Line 76: "This is distinct from the seed file — seed validates health, few-shot teaches style. If no reference tests exist, seed is your sole style reference."

**Issue:** Sequence unclear. Do you read seed first or few-shot first? What if seed and few-shot conflict on style?  
**Fix:** Numbered workflow:
```
1. Read seed.spec.ts — validate imports, fixtures
2. Find few-shot examples — learn assertion style, describe structure
3. If conflict: few-shot wins for style, seed wins for fixtures
```

### W5: Implicit Assumption - Playwright CLI Available
**Criterion:** CLR-6  
**Location:** Lines 91-98, 191-196  
**Evidence:** "Before writing a test, verify planned locators exist in the live DOM using playwright-cli"

**Issue:** Assumes playwright-cli is installed and accessible. What if it's not?  
**Fix:** Add to pre-flight checks: "Verify playwright-cli available: `playwright-cli --version`. If missing, write status NEEDS_CONTEXT."

### W6: Vague Edge Case - "Max 3 fix iterations"
**Criterion:** OUT-3  
**Location:** Line 130  
**Evidence:** "Max 3 fix iterations. If still failing after 3 attempts, write status file with blocker and STOP."

**Issue:** What counts as an iteration? Edit + run? Just run?  
**Fix:** "Max 3 edit-run cycles. One cycle = edit test + run test. After third failure, stop."

### W7: Mode Detection Logic Unclear
**Criterion:** CLR-1  
**Location:** Lines 33-39  
**Evidence:**
```
Detect mode from the dispatch prompt: if given a test plan reference, use create mode. If given specific test files and failure descriptions, use fix mode.
```
**Issue:** "Detect from dispatch prompt" is implicit. Agent must infer from context.  
**Fix:** Explicit mode parameter or clearer detection:
"If $ARGUMENTS contains 'fix' or paths to existing .spec.ts files: use fix mode. Otherwise: create mode."

---

## Anti-Patterns

### AP-CLR-02: Undefined Qualifiers
**Pattern:** "meaningful", "real", "similar" without definitions  
**Severity:** Medium

### AP-AGT-05: Bloated Skill (approaching)
**Pattern:** 233 lines with heavy inline guidance  
**Severity:** Low - under 500-line threshold but could benefit from extraction

---

## Strengths

### S1: Exceptional Anti-Pattern Awareness (Unique)
**Evidence:** Lines 51-54, 65-66  
```
No hollow tests. Every test must contain at least one real assertion... A test that navigates to a page and logs "needs implementation" is not a test — it's a placeholder that creates false confidence.
```
Prevents common failure mode. Excellent quality gate.

### S2: Strong Hard Rules Section (CON-2)
**Evidence:** Lines 41-66  
Seven numbered hard rules with rationale. Clear, enforceable, justified.

### S3: One-Test-at-a-Time Discipline (AGT-6)
**Evidence:** Line 45, 87-134  
```
One test at a time. Write ONE test, run it, fix until green, THEN write the next. Never batch-generate.
```
Prevents cascading failures. Excellent workflow control.

### S4: Mandatory Locator Verification (SAF-2)
**Evidence:** Lines 91-98  
Pre-flight locator check before writing test. Grounded in field data: "5 locator failures in field testing traced to selectors that were never verified."

### S5: Dual-Mode Operation (STR-2)
**Evidence:** Lines 33-39, 176-198  
Create mode + Fix mode in single agent. Clear mode detection and separate workflows.

### S6: Excellent Pre-Flight Protocol (RSN-1)
**Evidence:** Lines 58-80  
Nine required readings before starting. No guessing allowed.

### S7: Strong Constraint on Pure Output (CON-2)
**Evidence:** Lines 49-50
```
Pure output. Generated .spec.ts files import only from @playwright/test or project fixtures. No AI libraries, no MCP, no runtime LLM calls.
```
Prevents AI creep. Tests remain maintainable.

### S8: Lessons Feedback Loop (Unique)
**Evidence:** Lines 68, 197  
`.playwright/lessons.md` — agent learns from prior cycles. Prevents repeating failed approaches.

### S9: Risky Locators Catalog (STR-2)
**Evidence:** Lines 141-154  
Domain-specific knowledge about cross-browser issues (Playwright #35720, Safari list role). Grounded in real bugs.

### S10: Fix Mode Workflow (AGT-6)
**Evidence:** Lines 183-198  
Separate workflow for structural fixes. Doesn't conflate with create mode.

### S11: Given/When/Then Pattern (OUT-1)
**Evidence:** Lines 103-120  
Explicit test structure template with concrete example.

### S12: Clear Tool Usage (AGT-4)
**Evidence:** Line 28 frontmatter  
Read, Write, Edit, Bash, Glob — needs Edit to modify failing tests in fix mode. Justified.

---

## Recommendations

### R1: Extract to Reference Files
Move inline guidance to @references/ (see W1). Reduces prompt from 233 → ~150 lines.

### R2: Define Quality Terms
Add definitions section:
```markdown
## Definitions
- **Meaningful assertion:** Verifies externally observable behavior (DOM state, URL, response) not internal state or mocks
- **Similar patterns:** Matching page object style, assertion approach, or describe/test structure
```

### R3: Add Output Examples
Include one complete generated .spec.ts file showing Given/When/Then structure, imports, and assertions.

### R4: Clarify Seed vs Few-Shot Precedence
Add numbered workflow showing when to consult each source and how to resolve conflicts (see W4).

### R5: Add Explicit Mode Parameter
Frontmatter could include `mode: create|fix` or agent could check for explicit mode flag in $ARGUMENTS.

### R6: Strengthen Pre-Flight
Add playwright-cli availability check to pre-flight section.

### R7: Define "Iteration"
Make "max 3 fix iterations" measurable (see W6).

### R8: Add Status File Examples
Show concrete examples for all status codes:
```json
// DONE (create mode)
{"status":"DONE","artifacts":["tests/auth.spec.ts","tests/dashboard.spec.ts"]}

// NEEDS_CONTEXT
{"status":"NEEDS_CONTEXT","blocker":"Locator getByRole('button', {name: 'Submit'}) not found after 3 retries"}
```

### R9: Add Progressive Disclosure Note
Acknowledge in frontmatter: "This agent's guidance is comprehensive. For quick reference, see @references/test-patterns.md workflow diagram."

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| **STRUCTURE** | 5/6 | Strong role, dual modes, workflow. Length approaching threshold. |
| **CLARITY** | 5/7 | Clear tasks, strong rules. Vague terms and sequence ambiguity reduce score. |
| **CONSTRAINTS** | 6/6 | Excellent hard rules, rationale, grouping, pure output constraint. |
| **SAFETY** | 5/5 | Pre-flight checks, locator verification, error handling, lessons feedback. |
| **OUTPUT** | 4/6 | Given/When/Then template strong. Missing concrete examples, some edge cases undefined. |
| **EXAMPLES** | 2/3 | Tagged, diverse frontmatter. Missing output pairs. |
| **REASONING** | 2/2 | Pre-flight reading list = reasoning protocol. Uncertainty handling via status codes. |
| **AGENT_SPECIFIC** | 9/10 | All criteria met. Progressive disclosure present but could be stronger. |
| **DATA_SEPARATION** | 2/2 | Reference files tagged. Mode detection from arguments. |

**Total Applicable:** 49 criteria  
**Total Met:** 40 criteria  
**Violations:** 0 MUST, 0 MUST_NOT  
**Final Score:** (40 + 6 MUST met) / 54 × 100 = **85/100**

---

## Evaluation Metadata

- **Evaluator:** Claude Sonnet 4.5
- **Date:** 2026-04-13
- **Criteria Version:** evaluation-criteria.md (prompt-engineering/references)
- **Anti-Pattern Scan:** anti-patterns.md (AP-CLR-02, AP-AGT-05 approaching detected)
- **Term Blacklist Scan:** term-blacklists.md (vague terms: "meaningful", "real", "similar", "clear")
