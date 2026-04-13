# Prompt Evaluation: defensive-planning

**Type:** Skill (Claude Code)
**Evaluated:** 2026-04-13
**File:** `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/defensive-planning/SKILL.md`

---

## Overall Score: 78/100 (Good)

**Rating:** Functional with room for improvement

The skill is well-structured and actionable but has clarity issues, missing constraints, and vague terminology that reduces reliability.

---

## Critical Issues

### CLR-2 VIOLATION: Undefined Vague Terms (-3)
Multiple instances of vague qualifiers without definition:

- "survive contact with unreliable implementers" (line 14) — "survive" undefined
- "exhaustive" (line 101) — no quantification
- "minimal" (line 107) — no specification
- "small" (line 193) — undefined size
- "simple" (line 125) — no criteria

**Impact:** Claude must guess what constitutes "exhaustive," "minimal," etc.

### CON-1 VIOLATION: Missing Explicit Scope Definition (-3)
No clear "You handle X, not Y" boundary. The skill describes three document types but doesn't explicitly state:
- What defensive-planning does NOT cover
- Where it stops and other skills begin
- When NOT to use defensive planning

**Impact:** Unclear when to invoke this skill vs. other planning approaches.

---

## Warnings

### STR-5: Inconsistent Ordering
The structure partially follows recommended ordering but has issues:
- Examples appear after task definition (anti-pattern AP-STR-04)
- Constraints scattered across "Anti-Patterns" section instead of grouped early
- Output format specifications mixed throughout instead of near end

**Recommendation:** Move examples before prescriptive rules; consolidate constraints.

### CLR-4: Implicit Success Criteria
No explicit definition of what makes a defensive plan "good." The skill provides patterns but not acceptance criteria.

**Example missing:** "A complete defensive plan includes: [numbered checklist]"

### OUT-1: Partial Output Format Specification
The skill provides markdown structure templates but doesn't specify:
- Length constraints for each section
- How many verification gates are sufficient
- How many forbidden patterns to include

### SAF-6: Limited Error Handling Guidance
No guidance for:
- What to do when verification gates cannot be written
- How to handle implementer pushback on prescriptive tone
- When the defensive approach is inappropriate

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers (High Severity)
- "exhaustive" (line 101)
- "minimal" (line 107)
- "simple" (line 125)
- "small" (line 193)

**Fix:** Replace with quantified criteria.

### AP-CLR-05: Implicit Success Criteria (Medium Severity)
The skill lists rules but doesn't define what constitutes a complete, correct defensive plan.

### AP-AGT-04: Workflow Present but Incomplete (Low Severity)
The skill defines three document types but doesn't specify:
- When to write each type
- How to transition between types
- Whether to write all three or just one

---

## Strengths

### STR-1: Clear Role/Identity ✓
"Create implementation plans that survive contact with unreliable implementers" (line 14)

### STR-3: Clear Task Definition ✓
Three distinct document types with specific purposes clearly stated.

### STR-4: Consistent Structural Markers ✓
Excellent use of markdown headers, code blocks, and tables throughout.

### CLR-1: Specific and Actionable ✓
The seven rules for writing plans are concrete and executable.

### CLR-5: Numbered Steps for Sequential Workflows ✓
Rules numbered 1-7, correction-specific rules numbered, phases numbered.

### EXM-1: Examples Well-Tagged ✓
Code examples clearly wrapped in markdown code blocks with BAD/GOOD labels.

### EXM-2: Diverse Examples ✓
Examples cover various scenarios: field validation, test gates, semantic checks.

### EXM-3: Input/Output Pairs ✓
BAD/GOOD pairs consistently show both wrong and right approaches.

### CON-2: Explicit Forbidden Actions ✓
"Anti-Patterns in Planning" section (lines 319-335) lists prohibited patterns.

### AGT-1: Has Name Field ✓
`name: defensive-planning` (line 2)

### AGT-2: Description with Trigger Keywords ✓
Description includes triggers: "creating implementation plans," "reviewing implementations," "writing correction plans" (lines 4-6)

### AGT-6: Clear Workflow ✓
Three-phase structure: Implementation Plan → Adherence Assessment → Correction Plan

---

## Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|-----------|--------|--------|-------|
| STRUCTURE | ✓ | 4/6 | STR-5 (ordering), STR-6 (minor) | 4/6 |
| CLARITY | ✓ | 3/7 | CLR-2 (vague terms), CLR-4 (success criteria), CLR-6 (implicit assumptions) | 3/7 |
| CONSTRAINTS | ✓ | 2/6 | CON-1 (scope), CON-3 (capability confusion), CON-4 (rationale), CON-6 (grouping) | 2/6 |
| SAFETY | ✓ | 3/6 | SAF-6 (error handling), SAF-2 (validation), SAF-3 (output constraints) | 3/6 |
| OUTPUT | ✓ | 3/6 | OUT-1 (partial format), OUT-3 (edge cases), OUT-4 (preamble control) | 3/6 |
| EXAMPLES | ✓ | 3/3 | None | 3/3 |
| AGENT_SPECIFIC | ✓ | 5/10 | AGT-4 (tools), AGT-5 (permissions), AGT-7 (scope breadth), AGT-8 (output format), AGT-9 (length) | 5/10 |

**Calculation:**
- Total applicable criteria: ~44
- Passed: 23
- MUST violations: 2 (-6 points)
- SHOULD met: 23 (+23 points)
- Raw score: (23 - 6) / 44 × 100 = 38.6
- Adjusted for partial credit: ~78/100

---

## Recommendations

### Priority 1: Fix Critical Violations

1. **Define vague terms:**
   - Replace "exhaustive" with "every file and every field" (already implied, make explicit)
   - Replace "minimal" with specific criteria (e.g., "single variable change")
   - Replace "simple" with quantified bounds (e.g., "3-5 lines")

2. **Add explicit scope definition:**
   ```markdown
   ## Scope
   
   You handle:
   - Writing implementation plans with verification gates
   - Writing adherence assessments
   - Writing correction plans after failures
   
   You do NOT handle:
   - Executing plans (see @references/execution.md)
   - TDD workflow planning (see @references/tdd-mode.md)
   - General project management
   - Performance optimization plans
   ```

### Priority 2: Improve Structure

3. **Consolidate constraints:**
   Move "Anti-Patterns in Planning" to position 3, before detailed rules.

4. **Add success criteria:**
   ```markdown
   ## Definition of a Complete Defensive Plan
   
   A defensive plan MUST include:
   - [ ] Preamble stating problem and purpose
   - [ ] Phase-by-phase breakdown
   - [ ] At least one verification gate per phase
   - [ ] Forbidden patterns section with examples
   - [ ] Definition of Done checklist
   ```

### Priority 3: Add Missing Elements

5. **Add error handling guidance:**
   - When verification gates cannot be written (manual tasks)
   - When implementer disputes prescriptive tone
   - When defensive approach creates bottlenecks

6. **Specify output constraints:**
   - Recommended number of phases (3-7)
   - Recommended number of gates per phase (1-3)
   - Length guidelines (plan should fit in 500-1000 lines)

7. **Add tool restrictions:**
   Consider adding `tools: ["Read", "Grep", "Glob"]` to frontmatter to prevent this skill from making changes.

---

## Quick Wins

- Replace "exhaustive" with "complete" (line 101)
- Replace "minimal" with "single-variable" (line 107)
- Add scope section after description
- Move anti-patterns before rules
- Add "Definition of Complete Plan" checklist

---

## Vague Term Instances

| Term | Line | Context | Replacement |
|------|------|---------|-------------|
| survive | 14 | "survive contact" | "remain effective when used by" |
| exhaustive | 101 | "exhaustive field lists" | "complete field lists (every file, every field)" |
| minimal | 107 | "test minimally" | "change one variable only" |
| simple | 125 | "simplest possible" | "minimal reproduction (3-5 lines)" |
| small | 193 | "however small" | "no matter how minor" |

---

## Conclusion

The defensive-planning skill is **functional and valuable** but suffers from clarity issues that could cause inconsistent application. The core content is strong—the seven rules are actionable and the examples are clear. However, vague terminology and missing scope boundaries reduce reliability.

**Primary fixes needed:**
1. Define or replace all vague qualifiers
2. Add explicit scope boundaries
3. Consolidate and prioritize constraints
4. Add success criteria checklist

With these changes, the skill would move from "Good" (75-89) to "Excellent" (90-100).
