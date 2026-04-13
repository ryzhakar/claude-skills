# Prompt Evaluation: planner-agent Agent

**Type:** Agent  
**File:** `/Users/ryzhakar/pp/claude-skills/qa-automation/agents/planner-agent.md`  
**Overall Score:** 82/100 (Good)

---

## Summary

The planner-agent is a comprehensive, technically sophisticated agent for test planning via browser exploration. Strong workflow structure, excellent security awareness (CVE check), and multi-mode operation (CLI/MCP). Needs improvement in term precision, constraint clarity, and progressive disclosure. At 182 lines with heavy reference dependencies, it's approaching complexity threshold.

---

## Critical Issues (Must Fix)

None.

---

## Warnings (Should Fix)

### W1: Vague Constraint - "The Iron Law"
**Criterion:** CLR-2, CON-2  
**Location:** Lines 35-40  
**Evidence:**
```
NO PLAN WITHOUT LIVE EXPLORATION FIRST.
```
**Issue:** While dramatic, lacks operational precision. What constitutes "exploration"? How many pages? What if a page is inaccessible?  
**Fix:** "Every page listed in test-plan.md must have a corresponding entry in VERIFICATION.md showing browser state snapshot or MCP interaction log. Plans containing pages not in VERIFICATION.md are invalid and must not be written."

### W2: Vague Quality Terms
**Criterion:** CLR-2  
**Location:** Lines 121-133 (DOM quality score)  
**Evidence:**
- Line 122: "proper form elements" — what is "proper"?
- Line 123: "ARIA labels work" — work how?
- Line 130: "clickable divs" — how to detect?

**Fix:** Define each criterion measurably: "proper form elements: <input>, <select>, <textarea> (not contenteditable divs)", "ARIA labels work: getByLabel('Email') returns visible element"

### W3: Missing Tool Constraint Rationale (AGT-4)
**Criterion:** CON-4  
**Location:** Line 26 frontmatter  
**Evidence:** `tools: ["Read", "Write", "Bash", "Glob"]` — no Edit, no Grep

**Issue:** Why no Edit? Why no Grep? Rationale missing.  
**Fix:** Add comment: "No Edit (only creates new files), no Grep (uses Bash for package.json inspection)"

### W4: Contradictory Guidance - MCP vs CLI
**Criterion:** CLR-3  
**Location:** Lines 42-44, 65-69  
**Evidence:**
- Line 42: "Use @playwright/cli for live exploration. It writes snapshots to disk (not context), giving **unlimited session length**"
- Line 65: "Use MCP ONLY when the agent cannot access the Bash tool"
- Line 87: "**Use @playwright/cli (default)**"
- Line 92: "**MCP fallback (sandboxed environments only)**"

**Issue:** Three different phrasings for the same decision (default vs fallback vs only). Not contradictory but inconsistent emphasis.  
**Fix:** State once clearly at top: "Default: @playwright/cli. Fallback: MCP when Bash unavailable. Decision rule: if `playwright-cli open` fails, switch to MCP."

### W5: Implicit Scope Boundary
**Criterion:** CON-1  
**Location:** Missing explicit "You do NOT" section  
**Evidence:** Role defined (lines 31-32) but no forbidden actions listed.

**Fix:** Add:
```
You do NOT:
- Generate test code (that's generator-agent's job)
- Execute tests (that's executor-agent's job)
- Fix failing tests (that's healer-agent's job)
```

### W6: Length Approaching Threshold
**Criterion:** AGT-9  
**Location:** 182 lines  
**Evidence:** Under 500-line limit but heavy on reference dependencies (@references/ files).

**Fix:** Consider extracting DOM scoring algorithm and selector strategy details to reference files.

### W7: Vague Edge Case - "Cap at 10 interactions"
**Criterion:** CLR-2, OUT-3  
**Location:** Lines 67, 107  
**Evidence:** "Cap at 10 interactions" appears twice for MCP but no guidance on what to do when limit is hit.

**Fix:** "If 10-interaction MCP limit reached before full app explored, write status file: `NEEDS_CONTEXT`, blocker: 'Application too complex for MCP exploration. Use @playwright/cli or provide user-driven recording.'"

---

## Anti-Patterns

### AP-CLR-02: Undefined Qualifiers
**Pattern:** "proper", "correct", "obvious" used without definition  
**Severity:** Medium

### AP-STR-03: Format Not at End (Minor)
**Pattern:** Status file format appears mid-prompt (lines 154-169), not at end  
**Severity:** Low - mitigated by strong section markers

---

## Strengths

### S1: Exceptional Security Awareness (SAF-6)
**Evidence:** Lines 68-76  
MCP version check for CVE-2025-9611. Non-negotiable blocking on vulnerable version. Excellent.

### S2: Strong Workflow Structure (AGT-6)
**Evidence:** Lines 78-155  
Six-step workflow with prerequisites, exploration, analysis, strategy, planning, status. Clear, numbered, complete.

### S3: Multi-Mode Operation (Unique)
**Evidence:** Lines 42-110  
Handles both CLI (default) and MCP (fallback) with explicit decision rules and security checks.

### S4: Evidence-Based Planning (RSN-4)
**Evidence:** Lines 35-40, 116  
"Every scenario must trace to a browser observation." No speculation allowed.

### S5: Status-Driven Error Handling (SAF-6)
**Evidence:** Lines 154-169  
Three status codes (DONE, NEEDS_CONTEXT, BLOCKED) with artifact tracking.

### S6: Domain-Specific Knowledge (STR-2)
**Evidence:** Lines 171-174  
WASM framework handling (Leptos, Yew, Dioxus) with wait strategy guidance.

### S7: Reference File Protocol (AGT-9, partial)
**Evidence:** Lines 176-182  
External references reduce prompt bloat. Good progressive disclosure pattern.

### S8: Quantified Quality Scoring (OUT-1)
**Evidence:** Lines 121-133  
DOM quality score with explicit point values. Measurable output.

### S9: Clear Tool Usage Context (TLS-7)
**Evidence:** Lines 42-44, 87-110  
When to use CLI vs MCP with technical reasoning (token efficiency, security).

### S10: Edge Case Coverage (OUT-3)
**Evidence:** Lines 161-169  
Three edge cases defined (success, app not accessible, blocked) with exact JSON output.

### S11: Good Description Triggers (AGT-2)
**Evidence:** Lines 3-23 frontmatter  
Clear trigger phrases: "explore a live web application to plan Playwright tests", "produce structured test planning artifacts"

---

## Recommendations

### R1: Clarify "The Iron Law"
Make the rule operationally precise with measurable compliance criteria (see W1).

### R2: Define All Quality Terms
Add definitions section after line 120:
```markdown
## Quality Criteria Definitions
- **Proper form elements:** Native HTML <input>, <select>, <textarea> (not contenteditable)
- **ARIA labels work:** getByLabel('Field Name') resolves to visible, enabled element
- **Clickable divs:** Elements with onClick handlers that are not <button>, <a>, or <input>
```

### R3: Consolidate Mode Selection
Replace three mentions of CLI/MCP decision with single decision tree at lines 42-44.

### R4: Add Explicit Scope Boundaries
Add "You do NOT" section listing agent responsibilities outside this agent's scope (see W5).

### R5: Extract DOM Scoring to Reference
Move lines 121-133 to `@references/dom-quality-scoring.md` and replace with:
"Compute DOM quality score per @references/dom-quality-scoring.md. Write scores to .playwright/pages.md."

### R6: Handle MCP Limit Edge Case
Add guidance for what to do when 10-interaction MCP limit is exhausted (see W7).

### R7: Add Output Example
Include one complete `.playwright/test-plan.md` example showing scenario structure and VERIFICATION.md traceability.

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| **STRUCTURE** | 5/6 | Strong role, context, workflow. Minor ordering issue (format mid-prompt). |
| **CLARITY** | 4/7 | Clear task. Multiple vague terms reduce score. |
| **CONSTRAINTS** | 4/6 | Good scope definition. Missing "do NOT" list and rationale for some rules. |
| **SAFETY** | 5/5 | Exceptional security check (CVE). Error handling. Input validation (MCP version). |
| **OUTPUT** | 5/6 | Explicit format with templates. Missing example, some edge cases undefined. |
| **EXAMPLES** | 2/3 | Tagged, diverse examples in frontmatter. Missing output pairs. |
| **REASONING** | 2/2 | Evidence-before-conclusions (browser snapshots). Uncertainty handling (edge cases). |
| **AGENT_SPECIFIC** | 9/10 | All criteria met. Progressive disclosure present but could be stronger. |
| **DATA_SEPARATION** | 2/2 | Reference files clearly tagged (@references/). |

**Total Applicable:** 49 criteria  
**Total Met:** 38 criteria  
**Violations:** 0 MUST, 0 MUST_NOT  
**Final Score:** (38 + 6 MUST met) / 54 × 100 = **82/100**

---

## Evaluation Metadata

- **Evaluator:** Claude Sonnet 4.5
- **Date:** 2026-04-13
- **Criteria Version:** evaluation-criteria.md (prompt-engineering/references)
- **Anti-Pattern Scan:** anti-patterns.md (AP-CLR-02, AP-STR-03 detected)
- **Term Blacklist Scan:** term-blacklists.md (vague terms: "proper", "correct", "work", "obvious")
