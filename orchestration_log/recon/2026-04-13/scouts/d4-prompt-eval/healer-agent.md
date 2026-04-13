# Prompt Evaluation: healer-agent Agent

**Type:** Agent  
**File:** `/Users/ryzhakar/pp/claude-skills/qa-automation/agents/healer-agent.md`  
**Overall Score:** 89/100 (Good)

---

## Summary

The healer-agent is a highly focused, algorithmically precise agent for deterministic locator repair with exceptional constraint enforcement (THE IRON LAW). Strong confidence scoring, circuit breaker logic, and mandatory DOM verification. Excellent domain knowledge (ten-tier algorithm, Similo scoring). Minor improvements needed in term precision, output examples, and progressive disclosure.

---

## Critical Issues (Must Fix)

None.

---

## Warnings (Should Fix)

### W1: "The Iron Law" - Dramatic but Imprecise
**Criterion:** CLR-2, CON-2  
**Location:** Lines 32-38  
**Evidence:**
```
THE IRON LAW
NEVER HEAL ASSERTION FAILURES.
NEVER HEAL RUNTIME ERRORS.
ELEMENT FOUND + WRONG VALUE = APPLICATION BUG. DO NOT TOUCH THE TEST.
```
**Issue:** While dramatic and memorable, lacks operational precision. What constitutes an "assertion failure" vs a "locator failure"? How to detect programmatically?

**Fix:** Add detection criteria:
```
NEVER HEAL ASSERTION FAILURES.
Detection: error message contains "expect(", "toBe", "toHaveText", "toContain", "toEqual"
Action: write confidence: 0.0, category: "assertion", skip healing
```

### W2: Vague Term - "all tiers return null"
**Criterion:** CLR-2  
**Location:** Lines 77, 102-120  
**Evidence:** "When the ten-tier algorithm returns null for all tiers..."

**Issue:** What does "null" mean? No match? Empty array? undefined?  
**Fix:** "When the ten-tier algorithm returns no candidate locators at any tier (all tiers yield empty result sets)..."

### W3: Missing Output Example
**Criterion:** OUT-2  
**Location:** Lines 137-149, 151-162  
**Evidence:** Output schema defined but no concrete example.

**Fix:** Add example showing one healed failure:
```json
{
  "test": "Login flow - Submit button click",
  "file": "tests/auth.spec.ts:45",
  "status": "healed",
  "confidence": 0.92,
  "tier": 1,
  "original": "getByRole('button', { name: 'Sign In' })",
  "healed": "getByRole('button', { name: 'Log In' })",
  "verified": true
}
```

### W4: Implicit Circuit Breaker Logic
**Criterion:** CLR-1  
**Location:** Lines 52-61  
**Evidence:**
```
Read `.github/healing-state.json` (or treat as empty if missing).
Rules:
- Max 2 attempts per test (key: "file:line:title") — skip and mark deferred if exceeded
- Tests on blocklist — skip
```
**Issue:** How to check attempt count? What is the schema of healing-state.json?  
**Fix:** Show schema:
```json
{
  "tests/auth.spec.ts:45:Login flow": {"attempts": 2},
  "blocklist": ["tests/flaky.spec.ts:12:Unstable test"]
}
```

### W5: Vague Edge Case - "10+ concurrent test failures"
**Criterion:** OUT-3  
**Location:** Line 68  
**Evidence:** "10+ concurrent test failures — INFRASTRUCTURE ISSUE"

**Issue:** "Concurrent" is ambiguous. Same timestamp? Same test run? What's the detection rule?  
**Fix:** "10 or more failures in the same test run (same `results.json` batch) — likely infrastructure issue, not locator issue. Mark all deferred."

### W6: Confidence Band Overlap
**Criterion:** CLR-3  
**Location:** Lines 87-90  
**Evidence:**
```
Thresholds:
- >= 0.85: HIGH
- 0.60 - 0.84: MEDIUM
- 0.40 - 0.59: LOW
- < 0.40: REJECT
```
**Issue:** What happens at exactly 0.85? 0.60? 0.40? Boundary handling unclear.  
**Fix:** Use mathematical notation: `[0.85, 1.0]`, `[0.60, 0.85)`, `[0.40, 0.60)`, `[0.0, 0.40)`

### W7: "Recommended but not required" Weakens Discipline
**Criterion:** CON-2  
**Location:** Line 100  
**Evidence:** "For tiers 1-6, DOM verification is recommended but not required"

**Issue:** Creates ambiguity. Weakens "Mandatory for Tiers 7+" rule.  
**Fix:** "For tiers 1-6, DOM verification is optional (confidence scores account for verification absence). For tiers 7-10, DOM verification is MANDATORY."

---

## Anti-Patterns

### AP-CLR-02: Undefined Qualifiers (Minor)
**Pattern:** "meaningful", "all tiers return null" without precise definition  
**Severity:** Low - mitigated by strong algorithmic references

---

## Strengths

### S1: Exceptional Constraint - THE IRON LAW (CON-2)
**Evidence:** Lines 32-38  
```
NEVER HEAL ASSERTION FAILURES.
NEVER HEAL RUNTIME ERRORS.
```
Prevents catastrophic error class. Bold, memorable, repeated.

### S2: Strong Algorithmic Precision (CLR-1, RSN-1)
**Evidence:** Lines 72-78  
Ten-tier algorithm with confidence bands. Deterministic, not heuristic.

### S3: Circuit Breaker Pattern (SAF-6)
**Evidence:** Lines 52-61  
Max attempts, blocklist. Prevents infinite loops and known-bad patterns.

### S4: Mandatory DOM Verification (SAF-2)
**Evidence:** Lines 96-120  
Tier 7+ requires live DOM check. Grounded verification, not theoretical.

### S5: Hard Rejection Rules (CON-2)
**Evidence:** Lines 63-69  
Six explicit rejection scenarios with score = 0.0. No ambiguity.

### S6: Lessons Feedback Loop (Unique)
**Evidence:** Lines 92-95  
`.playwright/lessons.md` — agent learns from prior cycles. Appends discoveries.

### S7: DOM Re-Discovery Protocol (AGT-6)
**Evidence:** Lines 102-120  
Seven-step workflow for when all tiers fail. Uses playwright-cli for live inspection.

### S8: Confidence Score Thresholds (OUT-1)
**Evidence:** Lines 87-90  
Four tiers with numerical ranges. Machine-parseable, not subjective.

### S9: Apply-Only-If-Confident Rule (SAF-6)
**Evidence:** Line 122  
```
Apply Fixes (confidence >= 0.60 only)
```
Prevents low-confidence changes. Safety gate.

### S10: Structured Dual Output (OUT-1)
**Evidence:** Lines 137-162  
Single-failure (parallel) vs batch mode outputs. Supports both orchestration patterns.

### S11: Reference File Protocol (AGT-9)
**Evidence:** Lines 164-172  
Five reference files for algorithms and schemas. Good progressive disclosure.

### S12: Clear Tool Justification (AGT-4)
**Evidence:** Line 25 frontmatter  
Read, Write, Edit, Bash, Grep, Glob — needs Edit to apply fixes, Bash for playwright-cli.

### S13: Model Selection (AGT-5)
**Evidence:** Line 23 frontmatter  
`model: sonnet` — uses strong model for complex algorithmic reasoning (ten-tier, Similo). Justified.

### S14: Inline Code Examples (OUT-2)
**Evidence:** Lines 124-126  
Exact comment format for healed locators. Shows what to write.

---

## Recommendations

### R1: Operationalize THE IRON LAW
Add detection criteria for assertion failures vs locator failures (see W1). Make rule executable.

### R2: Define "null" Precisely
Replace "returns null" with "returns empty result set" or "yields no candidate locators" (see W2).

### R3: Add Concrete Output Example
Show complete `.playwright/healed/{test-name}.json` with real values (see W3).

### R4: Show Circuit Breaker Schema
Include `healing-state.json` schema in the prompt or extract to @references/file-protocol.md (see W4).

### R5: Define "Concurrent Failures"
Make "10+ concurrent test failures" measurable (see W5).

### R6: Use Mathematical Intervals
Replace range notation with mathematical intervals to clarify boundaries (see W6).

### R7: Strengthen DOM Verification Guidance
Remove "recommended but not required" ambiguity. Make tier 1-6 verification optional but document impact on confidence (see W7).

### R8: Add Flaky Test Handling
Line 68 mentions flaky detection but doesn't explain how healer handles tests already flagged flaky by executor. Add: "If test is flagged `flaky: true` in .ai-failures.json, skip healing (mark deferred)."

### R9: Add Progressive Disclosure Note
At 172 lines with five reference dependencies, acknowledge: "This agent implements complex algorithms. See @references/ten-tier-algorithm.md for decision tree diagram."

### R10: Clarify LLM Fallback
Lines 77-78 mention "LLM fallback when all tiers return null" but don't explain what LLM does. Add: "LLM fallback: analyze error message and DOM structure to propose locator. Max confidence: MEDIUM (0.60-0.84). Never auto-apply."

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| **STRUCTURE** | 6/6 | Excellent role, context, workflow, markers, ordering. |
| **CLARITY** | 5/7 | Clear task, strong algorithm. Vague terms ("null", "concurrent") reduce score. |
| **CONSTRAINTS** | 6/6 | Exceptional: IRON LAW, hard rejection rules, confidence thresholds, circuit breaker. |
| **SAFETY** | 5/5 | DOM verification, circuit breaker, confidence gates, error handling. |
| **OUTPUT** | 5/6 | Dual output formats, confidence thresholds. Missing concrete examples. |
| **EXAMPLES** | 2/3 | Tagged frontmatter examples. Missing output pairs. |
| **REASONING** | 2/2 | Ten-tier algorithm = explicit reasoning. Lessons feedback = learning. |
| **AGENT_SPECIFIC** | 9/10 | All criteria met. Progressive disclosure present but could be stronger. |
| **DATA_SEPARATION** | 2/2 | Reference files tagged. Circuit breaker reads external state. |

**Total Applicable:** 49 criteria  
**Total Met:** 42 criteria  
**Violations:** 0 MUST, 0 MUST_NOT  
**Final Score:** (42 + 6 MUST met) / 54 × 100 = **89/100**

---

## Evaluation Metadata

- **Evaluator:** Claude Sonnet 4.5
- **Date:** 2026-04-13
- **Criteria Version:** evaluation-criteria.md (prompt-engineering/references)
- **Anti-Pattern Scan:** anti-patterns.md (AP-CLR-02 minor detected)
- **Term Blacklist Scan:** term-blacklists.md (vague terms: "null", "concurrent", minor issues)
