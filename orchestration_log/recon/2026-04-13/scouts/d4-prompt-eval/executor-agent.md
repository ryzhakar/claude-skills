# Prompt Evaluation: executor-agent Agent

**Type:** Agent  
**File:** `/Users/ryzhakar/pp/claude-skills/qa-automation/agents/executor-agent.md`  
**Overall Score:** 87/100 (Good)

---

## Summary

The executor-agent is a well-focused, technically precise agent for test execution and failure classification. Excellent constraint clarity (CLI-exclusive), strong classification algorithm with regex patterns, and good error handling. Minor improvements needed in term precision, output format examples, and scope boundary definition.

---

## Critical Issues (Must Fix)

None.

---

## Warnings (Should Fix)

### W1: Missing Explicit Scope Boundary
**Criterion:** CON-1 (MUST have explicit scope definition)  
**Location:** Lines 30-31  
**Evidence:**
```
Execute Playwright test suites, classify failures by type, detect flaky tests, and write structured reports.
```
**Issue:** Role defined but no "You do NOT" section. What is out of scope?

**Fix:** Add after line 31:
```markdown
You do NOT:
- Generate tests (that's generator-agent)
- Fix failing tests or locators (that's healer-agent)
- Plan test scenarios (that's planner-agent)
- Modify test code (read-only except for reports)
```

### W2: Vague Term - "if needed"
**Criterion:** CLR-2  
**Location:** Line 39  
**Evidence:** "Install browsers: `npx playwright install --with-deps` **(if needed)**"

**Issue:** When is it needed? How to detect?  
**Fix:** "Install browsers if `npx playwright --version` succeeds but `ls ~/.cache/ms-playwright/chromium-*/` is empty"

### W3: Missing Output Example
**Criterion:** OUT-2 (SHOULD provide template or example)  
**Location:** Lines 50-52 (failure classification), 88-96 (status file)  
**Evidence:** Schema referenced but no concrete example.

**Fix:** Add example `.ai-failures.json` after line 52 showing one failure of each type with real error messages.

### W4: Implicit Assumption - "results.json"
**Criterion:** CLR-6 (MUST_NOT over-rely on implicit understanding)  
**Location:** Line 48  
**Evidence:** "Read `results.json` and parse..."

**Issue:** Assumes reader knows Playwright writes results.json. Where does it write it?  
**Fix:** "Playwright writes `results.json` to project root when `--reporter=json` is used. Read this file and parse..."

### W5: Edge Case Undefined - "browser-specific"
**Criterion:** OUT-3 (SHOULD specify handling of edge cases)  
**Location:** Lines 76-78  
**Evidence:**
```
Flag with `browser_specific: true` when applicable.
```
**Issue:** What does "applicable" mean? When exactly?  
**Fix:** "Flag `browser_specific: true` when failure occurs in exactly one browser project (Chromium, Firefox, or WebKit) but passes in others."

### W6: Contradictory Guidance on Flaky Tests
**Criterion:** CLR-3  
**Location:** Lines 65, 68  
**Evidence:**
- Line 65: "Re-run failed tests: `npx playwright test --retries=2 --reporter=json tests/failing.spec.ts`"
- Line 68: "If retry passes: flag `flaky: true`. Flaky tests are NOT candidates for locator healing."

**Issue:** How to know which tests to re-run before writing .ai-failures.json (which is the output)? Sequence unclear.  
**Severity:** Medium  
**Fix:** Clarify workflow: "1. Run full suite, 2. Classify failures, 3. Re-run failed tests with retries, 4. Update .ai-failures.json with flaky flags"

---

## Anti-Patterns

### AP-CLR-02: Undefined Qualifiers (Minor)
**Pattern:** "if needed" without criteria  
**Severity:** Low

---

## Strengths

### S1: Exceptional Constraint Clarity (CON-1)
**Evidence:** Line 30
```
You are CLI-exclusive — MCP has no test execution capability.
```
Crystal-clear technical boundary. No ambiguity.

### S2: Precise Classification Algorithm (CLR-1)
**Evidence:** Lines 50-58  
Six failure categories with exact regex patterns and percentages. Completely actionable.

### S3: Critical Distinction - Healable Count (Unique)
**Evidence:** Lines 60-61
```
**CRITICAL:** `healable_count` = locator failures ONLY. Timing failures are NOT healable. Do not include timing in healable_count.
```
Prevents common mistake. Bold, explicit, with examples.

### S4: Strong Pre-Flight Protocol (SAF-6)
**Evidence:** Lines 34-42  
Five-step validation before test execution. Includes seed health check and dev server verification.

### S5: Flaky Test Detection (SAF-6)
**Evidence:** Lines 65-68  
Retry logic with clear flagging criteria. Prevents false positives in healing.

### S6: Cross-Browser Analysis (STR-2)
**Evidence:** Lines 71-78  
Distinguishes browser-specific failures from universal failures. Domain knowledge.

### S7: Structured Status File (OUT-1)
**Evidence:** Lines 88-99  
JSON schema with phase, status, blocker, artifacts, healable_count. Machine-parseable orchestration.

### S8: Reference File Protocol (AGT-9)
**Evidence:** Lines 101-105  
External references for detailed schemas. Good progressive disclosure.

### S9: Clear Tool Justification (AGT-4)
**Evidence:** Line 25 frontmatter  
Read, Write, Bash, Glob — no Edit (creates reports, doesn't modify tests), no Grep (uses Bash for JSON parsing).

### S10: Good Description Triggers (AGT-2)
**Evidence:** Lines 3-22 frontmatter  
Clear triggers: "execute Playwright test suites via CLI", "classify every failure", "detect flaky tests"

### S11: Minimal Model (AGT-5, permission mode)
**Evidence:** Line 23 frontmatter  
`model: haiku` — uses fast, cheap model for straightforward execution task. Good resource allocation.

---

## Recommendations

### R1: Add Explicit Scope Boundary
Add "You do NOT" section to make out-of-scope actions explicit (see W1).

### R2: Clarify "if needed" Criteria
Replace conditional phrases with detection logic (see W2).

### R3: Add .ai-failures.json Example
Include one complete example after line 52:
```json
{
  "total": 3,
  "locator": [{"test": "Login test", "error": "locator.click: Target closed", "file": "tests/auth.spec.ts:12", "category": "locator", "healable": true, "flaky": false}],
  "timing": [...],
  "healable_count": 1
}
```

### R4: Clarify Workflow Sequence
Add numbered workflow section:
```
1. Run full suite
2. Read results.json
3. Classify failures by category
4. Re-run failures with --retries=2
5. Update classifications with flaky flags
6. Write .ai-failures.json
7. Write status file
```

### R5: Define "browser_specific" Precisely
Add explicit criteria for when to set the flag (see W5).

### R6: Add Pre-Flight Failure Example
Show what status file looks like when seed fails:
```json
{"phase":"EXECUTE","status":"NEEDS_CONTEXT","blocker":"Seed file failing: TimeoutError at tests/seed.spec.ts:8","artifacts":[],"healable_count":0}
```

### R7: Specify Artifact Paths
Line 82 lists artifacts but not their paths. Add:
- `results.json` (project root)
- `.ai-failures.json` (project root)
- `playwright-report/` (directory)
- `test-results/` (directory)

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| **STRUCTURE** | 5/6 | Strong role, workflow. Missing explicit scope boundary. |
| **CLARITY** | 5/7 | Clear task, precise regex. Vague terms ("if needed") and sequence ambiguity reduce score. |
| **CONSTRAINTS** | 5/6 | Excellent CLI-exclusive rule. Missing "do NOT" list. |
| **SAFETY** | 5/5 | Pre-flight checks, seed health, error handling, flaky detection. |
| **OUTPUT** | 4/6 | Format defined, edge cases present. Missing concrete examples. |
| **EXAMPLES** | 2/3 | Tagged, diverse frontmatter examples. Missing output pairs. |
| **REASONING** | 2/2 | Classification algorithm is explicit reasoning. Uncertainty handling (status codes). |
| **AGENT_SPECIFIC** | 10/10 | Name, description, workflow, tools, model all optimal. |
| **DATA_SEPARATION** | 2/2 | Reference files clearly tagged. |

**Total Applicable:** 47 criteria  
**Total Met:** 40 criteria  
**Violations:** 0 MUST, 0 MUST_NOT  
**Final Score:** (40 + 5 MUST met) / 52 × 100 = **87/100**

---

## Evaluation Metadata

- **Evaluator:** Claude Sonnet 4.5
- **Date:** 2026-04-13
- **Criteria Version:** evaluation-criteria.md (prompt-engineering/references)
- **Anti-Pattern Scan:** anti-patterns.md (AP-CLR-02 detected)
- **Term Blacklist Scan:** term-blacklists.md (vague terms: "if needed")
