# Prompt Evaluation: code-quality-reviewer Agent

**Type:** Agent  
**File:** `/Users/ryzhakar/pp/claude-skills/dev-discipline/agents/code-quality-reviewer.md`  
**Overall Score:** 90/100 (Excellent)

---

## Summary

The code-quality-reviewer agent is a production-ready, comprehensive quality audit agent with excellent tiered severity system, balanced feedback requirements, and strong scope control. Exceptional output format structure and constraint clarity. Minor improvements in term precision and example completeness.

---

## Critical Issues (Must Fix)

None.

---

## Warnings (Should Fix)

### W1: Vague Terms Without Definition
**Criterion:** CLR-2 (MUST_NOT contain undefined vague terms)  
**Location:** Multiple  
**Evidence:**
- Line 66: "Clean separation of concerns" — what is "clean"?
- Line 67: "Proper error handling" — "proper" is subjective
- Line 70: "Edge cases handled" — which edge cases?
- Line 71: "Names are clear and descriptive" — "clear" is subjective

**Fix:** Provide examples or criteria:
- "Separation of concerns: each class/module has single responsibility"
- "Error handling: errors are caught, logged, and propagated (not swallowed)"
- "Names describe public interface, not implementation details"

### W2: Contradictory Instruction Pair
**Criterion:** CLR-3 (MUST_NOT contain contradictory instructions)  
**Location:** Lines 50, 145  
**Evidence:**
- Line 50: "Acknowledge strengths -- balanced feedback is more useful than pure criticism"
- Line 145: "Focus on what THIS change contributed (not pre-existing issues)"

**Issue:** While contextually compatible, "acknowledge strengths" could be interpreted as requiring praise for pre-existing code, which contradicts "focus on this change."  
**Severity:** Low - context makes intent clear.  
**Fix:** "Acknowledge strengths **in the changes under review**"

### W3: Examples Missing Output
**Criterion:** EXM-3 (SHOULD show both input AND expected output)  
**Location:** Lines 6-36 frontmatter  
**Evidence:** Examples show dispatch context but not sample review output.

**Fix:** Add one complete review example showing the markdown output structure.

### W4: Vague Severity Criteria
**Criterion:** CLR-2  
**Location:** Lines 99-101  
**Evidence:**
- "obvious performance issues" — what threshold defines "obvious"?
- "Backward compatibility considered" — how to verify?

**Fix:** Make measurable: "Performance: no O(n²) algorithms on unbounded collections", "Breaking changes flagged in public APIs"

---

## Anti-Patterns

### AP-CLR-02: Undefined Qualifiers
**Pattern:** Uses "clean", "proper", "clear", "obvious" without definition  
**Severity:** Medium - reduced by strong structural guidance elsewhere

---

## Strengths

### S1: Exceptional Severity Tiering (CLR-4, OUT-1)
**Evidence:** Lines 93-101  
Three explicit tiers (Critical, Important, Minor) with clear definitions and merge-blocking criteria.

### S2: Comprehensive Output Template (OUT-2)
**Evidence:** Lines 103-136  
Complete markdown template with all sections, placeholders, and structure. Exactly what evaluator needs to produce.

### S3: Strong Constraint Grouping (CON-6)
**Evidence:** Lines 138-153  
DO/DO NOT sections with six positive rules and six forbidden actions. Clear, scannable, grouped.

### S4: Balanced Feedback Requirement (Unique Strength)
**Evidence:** Line 50
```
Acknowledge strengths -- balanced feedback is more useful than pure criticism
```
Prevents purely negative reviews. Forces objectivity.

### S5: Scope Control via Git Range (CON-1)
**Evidence:** Lines 43, 56-58, 145
```
Your review is scoped to a specific git range -- review only what changed, not the entire codebase.
```
Prevents scope creep. Reinforced three times.

### S6: Workflow with Technical Commands (AGT-6)
**Evidence:** Lines 55-61  
Five-step process starting with concrete git command. No ambiguity.

### S7: Edge Case Handling (SAF-6)
**Evidence:** Lines 155-159  
Three edge cases defined: no issues found, too many issues, unclear code intent. Each has guidance.

### S8: Clear Merge Verdict Requirement (CLR-4)
**Evidence:** Line 144, 152  
Forces explicit "Ready to merge: Yes/With fixes/No" decision. No hedging allowed.

### S9: Quality Checklist (CLR-4)
**Evidence:** Lines 64-91  
Four categories (Code Quality, Architecture, Testing, Production Readiness) with specific questions.

### S10: Tool Justification (AGT-4)
**Evidence:** Line 40 frontmatter  
Read, Write, Grep, Glob, Bash — needs Bash for git diff, but no Edit (read-only review).

### S11: Strong Role Definition (STR-1)
**Evidence:** Line 43
```
You are reviewing code changes for production readiness.
```
Clear, specific, measurable identity.

---

## Recommendations

### R1: Define Quality Terms
Replace subjective terms with objective criteria (see W1). Add examples to Quality Checklist.

### R2: Add Example Review
Include one complete review output in frontmatter or at end of prompt showing all sections filled in.

### R3: Quantify Severity Thresholds
Add to severity definitions:
- Critical: "Breaks functionality, security vulnerability, data loss"
- Important: "Missing error handling, test coverage <80%, architectural violation"
- Minor: "Code style (linter flags), optimization opportunities, missing comments"

### R4: Strengthen Length Constraint
Line 157 mentions ">20 issues" but could be more explicit about normal case:
"Limit findings to 15 items total (prioritize by severity). Group similar issues under one heading."

### R5: Add Self-Review Gate
Consider adding: "Before reporting, verify you read actual code (not just git stat output). Spot-check 3 findings by re-reading file:line references."

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| **STRUCTURE** | 6/6 | Role, context, constraints, workflow, format all excellent. |
| **CLARITY** | 5/7 | Clear task and structure. Vague terms reduce score. |
| **CONSTRAINTS** | 6/6 | Explicit scope (git range), forbidden actions, rationale, grouping. |
| **SAFETY** | 4/4 | Error handling (edge cases), no sensitive access. |
| **OUTPUT** | 6/6 | Explicit format, comprehensive template, edge cases, length guidance. |
| **EXAMPLES** | 2/3 | Tagged, diverse examples. Missing output pairs. |
| **REASONING** | 2/2 | Checklist-driven reasoning. Uncertainty handling (edge case 3). |
| **AGENT_SPECIFIC** | 10/10 | All agent criteria met optimally. |

**Total Applicable:** 44 criteria  
**Total Met:** 41 criteria  
**Violations:** 0 MUST, 0 MUST_NOT  
**Final Score:** (41 + 5 MUST met) / 51 × 100 = **90/100**

---

## Evaluation Metadata

- **Evaluator:** Claude Sonnet 4.5
- **Date:** 2026-04-13
- **Criteria Version:** evaluation-criteria.md (prompt-engineering/references)
- **Anti-Pattern Scan:** anti-patterns.md (AP-CLR-02 detected)
- **Term Blacklist Scan:** term-blacklists.md (vague terms: "clean", "proper", "clear", "obvious")
