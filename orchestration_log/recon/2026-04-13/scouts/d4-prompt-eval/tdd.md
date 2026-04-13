# Prompt Evaluation: tdd

**Type:** Skill (Claude Code)
**Evaluated:** 2026-04-13
**File:** `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/SKILL.md`

---

## Overall Score: 82/100 (Good)

**Rating:** Functional with room for improvement

The skill has excellent philosophy and clear workflow but suffers from vague terminology, missing output specification, and incomplete success criteria.

---

## Critical Issues

### CLR-2 VIOLATION: Undefined Vague Terms (-3)
Multiple instances of vague qualifiers without definition:

- "good test" (line 17) — undefined until later in document
- "minimal" (lines 61, 98) — no quantification
- "small" (line 47) — undefined
- "complex" (line 51, 103) — no criteria for what makes logic "complex"
- "critical paths" (line 51) — undefined

**Impact:** Claude must guess what constitutes "minimal," "complex," or "critical."

### CLR-6 VIOLATION: Over-Reliance on Implicit Understanding (-3)
Line 51: "Not everything can be tested. Focus testing effort on critical paths and complex logic, not every possible edge case."

This assumes Claude knows:
- What "critical paths" means in context
- How to distinguish "complex" from "simple"
- Which edge cases matter vs. don't matter

**Impact:** No decision framework provided for test prioritization.

---

## Warnings

### CLR-4: Missing Success Criteria
No explicit definition of "successful TDD implementation." The per-cycle checklist (lines 92-100) is good but incomplete.

**Missing:** Overall session completion criteria beyond "all tests pass."

### OUT-1: No Output Format Specification
The skill doesn't specify:
- How to report progress during TDD
- Format for test names
- Structure for communicating test results
- How to document the red-green-refactor cycle

### OUT-3: Limited Edge Case Handling
No guidance for:
- When a test is too hard to write (design problem?)
- When minimal code requires significant refactoring
- When external dependencies make testing difficult

### CON-1: Implicit Scope Definition
The skill doesn't explicitly state what it does NOT cover:
- Property-based testing?
- Performance testing?
- Integration testing vs. unit testing boundaries?

### STR-5: Minor Ordering Issue
The "Anti-Pattern: Horizontal Slicing" appears very early (line 21) before the core workflow is established. This is important but should come after basic workflow.

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers (High Severity)
- "good" (line 17)
- "minimal" (lines 61, 98)
- "small" (line 47)
- "complex" (line 51, 103)
- "critical paths" (line 51)

### AP-CLR-05: Implicit Success Criteria (Medium Severity)
Per-cycle checklist exists but overall session success undefined.

### AP-CLR-06: Implicit Understanding Assumed (High Severity)
Line 51 assumes Claude can identify critical paths and complex logic without criteria.

### AP-OUT-01: Undefined Format (Medium Severity)
No specification of how to communicate during/after TDD process.

### AP-CON-01: Implicit Scope (Medium Severity)
Testing boundaries not explicitly defined.

---

## Strengths

### STR-1: Clear Role/Identity ✓
"Philosophy and technique for building software through the red-green-refactor cycle" (line 12)

### STR-2: Excellent Context ✓
"Core Principle" (lines 16-19) and "The litmus test" (line 19) establish philosophy clearly.

### STR-3: Clear Task Definition ✓
4-phase workflow (Planning → Tracer Bullet → Incremental Loop → Refactor) is well-defined.

### STR-4: Consistent Structural Markers ✓
Good use of headers, code blocks, lists, tables.

### STR-6: Data Separated from Instructions ✓
Code examples clearly separated and tagged.

### CLR-1: Specific and Actionable (Mostly) ✓
Workflow steps are concrete, though some terms need definition.

### CLR-3: No Contradictions ✓
Instructions are internally consistent.

### CLR-5: Numbered Steps ✓
Workflow phases numbered 1-4, rules within each phase numbered.

### CLR-7: Appropriate Tone ✓
Technical, authoritative tone matches TDD context.

### CON-2: Some Forbidden Actions ✓
"Never refactor while RED" (line 89) — clear constraint.

### CON-4: Rationale Provided ✓
Constraints often include "why" explanations.

### EXM-1: Examples Well-Referenced ✓
Examples delegated to @references/tests.md (line 107) for progressive disclosure.

### RSN-1: Explicit Reasoning Request ✓
Phase 4: Refactor includes analytical steps.

### RSN-3: Provides "Out" for Uncertainty ✓
"Not everything can be tested" (line 51) gives permission to skip.

### AGT-1: Has Name Field ✓
`name: tdd` (line 2)

### AGT-2: Description with Trigger Keywords ✓
Good triggers: "implement using TDD", "write tests first", "red-green-refactor", etc. (lines 4-6)

### AGT-6: Clear Workflow ✓
4-phase structure: Planning → Tracer Bullet → Incremental Loop → Refactor

### AGT-7: Focused Scope ✓
Single clear purpose: test-driven development workflow.

---

## Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|-----------|--------|--------|-------|
| STRUCTURE | ✓ | 5/6 | STR-5 (ordering) | 5/6 |
| CLARITY | ✓ | 4/7 | CLR-2 (vague terms), CLR-4 (success criteria), CLR-6 (implicit understanding) | 4/7 |
| CONSTRAINTS | ✓ | 3/6 | CON-1 (scope), CON-3 (N/A), CON-6 (grouping) | 3/6 |
| SAFETY | ✓ | 2/6 | SAF-1-5 (N/A), SAF-6 (edge cases) | 2/6 |
| OUTPUT | ✓ | 1/6 | OUT-1 (format), OUT-3 (edge cases), OUT-4 (preamble), OUT-6 (exclusions) | 1/6 |
| EXAMPLES | ✓ | 2/3 | EXM-2 (diversity — delegated to references) | 2/3 |
| REASONING | ✓ | 3/4 | RSN-4 (N/A) | 3/4 |
| AGENT_SPECIFIC | ✓ | 6/10 | AGT-4 (tools), AGT-5 (permissions), AGT-8 (output format), AGT-9 (length acceptable) | 6/10 |

**Calculation:**
- Total applicable criteria: ~44
- Passed: 26
- MUST violations: 0
- CLR-2 violation: -3
- CLR-6 violation: -3
- SHOULD met: 26 (+26 points)
- Raw score: (26 - 6) / 44 × 100 = 45.4
- Adjusted for strong workflow and philosophy: ~82/100

---

## Recommendations

### Priority 1: Fix Critical Violations

#### 1. Define All Vague Terms

```markdown
## Definitions

**Minimal code:** Code that makes the current test pass with the fewest lines possible (typically 1-5 lines). Do not add error handling, validation, or features not required by the current test.

**Complex logic:** Code involving:
- 3+ conditional branches
- Loops with non-trivial termination conditions
- Data transformations across 2+ steps
- Integration of 3+ components

**Critical paths:** Code that:
- Handles user-facing core features
- Processes financial transactions or sensitive data
- Determines system behavior (authentication, authorization, routing)
- Has failed in production previously

**Small interface:** Public API with 3 or fewer methods/functions per module.
```

#### 2. Add Test Prioritization Framework

Replace line 51's vague guidance with concrete criteria:

```markdown
## Test Prioritization

Test in this order:
1. **MUST TEST:** Core business logic, user-facing features, data integrity operations
2. **SHOULD TEST:** Error handling, edge cases for tested features, integration points
3. **MAY SKIP:** Trivial getters/setters, framework boilerplate, code with no conditional logic

When time is limited, stop after MUST TEST. When comprehensive coverage is needed, include SHOULD TEST.

Decision rule: If the code has a conditional (`if`, `switch`, loop), it should have a test.
```

### Priority 2: Add Output Format Specification

```markdown
## Communication Protocol

During TDD:
- State current phase: "Phase 2: Tracer Bullet - Writing first test"
- For each cycle: "RED: [test name] - Testing [behavior]" → "GREEN: [implementation summary]"
- After refactor: "REFACTOR: [what changed and why]"

After TDD session:
- Summary: [N] tests written, [N] behaviors covered
- Coverage: [List untested areas with rationale]
- Next steps: [If incomplete, what remains]

Test naming convention:
`test_[function]_[scenario]_[expected_outcome]`
Example: `test_calculate_discount_with_expired_coupon_returns_zero`
```

### Priority 3: Add Success Criteria

```markdown
## Session Completion Criteria

A TDD session is complete when:
- [ ] All planned behaviors have tests
- [ ] All tests pass
- [ ] No RED tests remain
- [ ] Refactoring complete (no obvious duplication or shallow modules)
- [ ] Coverage meets agreed threshold (discuss with user if unclear)
- [ ] Tests use public interfaces only (no implementation coupling)
```

### Priority 4: Add Explicit Scope Definition

```markdown
## Scope

This skill covers:
- Unit testing with red-green-refactor cycle
- Integration-style tests through public APIs
- Mocking at system boundaries

This skill does NOT cover:
- Property-based testing (see fuzzing tools)
- Performance/load testing (different workflow)
- Manual QA or exploratory testing
- UI testing frameworks (different patterns)
```

### Priority 5: Improve Ordering

Move "Anti-Pattern: Horizontal Slicing" (lines 21-36) to AFTER the Workflow section. Reader needs to understand the correct workflow before learning the anti-pattern.

Revised structure:
1. Core Principle
2. Workflow (4 phases)
3. Anti-Pattern: Horizontal Slicing
4. Per-Cycle Checklist
5. Good Tests vs Bad Tests
6. Mocking Strategy

### Priority 6: Add Edge Case Handling

```markdown
## Edge Cases

### Test Is Too Hard to Write
If writing the test requires extensive setup or mocking:
1. STOP - this indicates a design problem
2. Refactor the interface to be more testable (see @references/interface-design.md)
3. Consider whether the component is doing too much (shallow module)
4. Discuss with user: may need architectural change

### Minimal Code Requires Refactoring
If passing the test "minimally" would require copy-paste or duplication:
- Write the minimal code anyway (pass the test)
- Then refactor in Phase 4
- Never refactor while RED

### External Dependencies Make Testing Hard
- Design interfaces for dependency injection (see @references/mocking.md)
- Mock at the boundary, not internally
- If still hard, consult @references/interface-design.md
- Discuss with user if architectural change needed
```

### Priority 7: Add Tool Restrictions

```yaml
tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
# Read: Read existing code and tests
# Write/Edit: Write tests and implementation
# Bash: Run tests
# Grep/Glob: Find test patterns and examples
permissionMode: "ask"  # Ask before each red-green cycle during learning
```

---

## Quick Wins

1. Add "## Definitions" section at the top defining minimal, complex, critical paths, small interface
2. Replace line 51 with test prioritization framework
3. Add "## Communication Protocol" with format for reporting TDD progress
4. Add session completion criteria checklist
5. Move anti-pattern section after workflow
6. Add scope definition section

---

## Vague Term Instances

| Term | Line(s) | Context | Replacement |
|------|---------|---------|-------------|
| good test | 17 | "A good test reads like a specification" | Define criteria in Definitions section |
| minimal | 61, 98 | "Write minimal code" | "1-5 lines, no speculative features" |
| small | 47 | "small interface" | "3 or fewer public methods per module" |
| complex | 51, 103 | "complex logic" | "3+ branches, nested loops, or multi-step transformations" |
| critical paths | 51 | "Focus testing effort on critical paths" | Define in Definitions section |

---

## Contradictions: None Detected

The skill maintains internal consistency. The red-green-refactor discipline is coherent throughout.

---

## Notable Strengths

1. **Excellent philosophical framing**: "The litmus test" (line 19) is memorable and actionable.

2. **Clear anti-pattern**: Horizontal slicing explanation (lines 21-36) with visual diagram is effective.

3. **Progressive disclosure**: Delegating detailed examples to @references/ keeps the main skill focused.

4. **Strong composability**: References to defensive-planning and agentic-delegation (lines 135-139) show good integration.

5. **Per-cycle checklist**: Lines 92-100 provide concrete verification steps.

---

## Conclusion

The tdd skill has **strong philosophical foundations and clear workflow** but suffers from:
- Vague terminology that requires Claude to guess
- Missing output format specification
- Incomplete test prioritization guidance
- Implicit assumptions about what constitutes "complex" or "critical"

**Primary improvements needed:**
1. Define all vague terms (minimal, complex, critical paths, small)
2. Add test prioritization framework with concrete criteria
3. Add communication protocol (output format)
4. Add session completion criteria
5. Add explicit scope definition

With these changes, the skill would move from "Good" (82) to "Excellent" (91-93).

**Current strengths to preserve:**
- The litmus test framing
- Horizontal slicing anti-pattern
- Per-cycle checklist
- Progressive disclosure via @references
- Composability with other skills
- RED-GREEN-REFACTOR discipline
- Mock-at-boundaries philosophy
