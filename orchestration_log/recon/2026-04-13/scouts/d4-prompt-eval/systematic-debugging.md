# Prompt Evaluation: systematic-debugging

**Type:** Skill (Claude Code)
**Evaluated:** 2026-04-13
**File:** `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/systematic-debugging/SKILL.md`

---

## Overall Score: 85/100 (Good)

**Rating:** Functional with minor improvements needed

The skill is well-structured with clear workflow and strong constraints. Minor clarity issues and missing output specifications prevent an excellent rating.

---

## Critical Issues

None. No MUST or MUST_NOT violations detected.

---

## Warnings

### CLR-2: Borderline Vague Terms
Several terms approach vagueness but are contextually acceptable:

- "carefully" (line 43) — acceptable in "Read Error Messages Carefully" as it's followed by specific instructions
- "completely" (line 44) — acceptable when paired with "Read stack traces completely"
- "minimal" (line 107) — context-dependent but could be clearer

**Assessment:** Not violations (context provides clarity) but could be tightened.

### CLR-4: Implicit Success Criteria
No explicit definition of "successful debugging session" or completion criteria beyond "bug resolved, tests pass."

**Missing:** "A debugging session is complete when: [checklist]"

### OUT-1: No Output Format Specification
The skill doesn't specify HOW to report findings. Should the user expect:
- A written analysis document?
- Inline comments as work proceeds?
- A final summary?
- Just the fix with no explanation?

**Impact:** Inconsistent reporting across debugging sessions.

### STR-5: Minor Ordering Issue
"User Signals of Process Violation" (lines 179-187) appears late. This is meta-guidance that belongs earlier, near the workflow definition.

### SAF-6: Limited Error Handling for Edge Cases
No guidance for:
- What to do when reproduction is impossible (Heisenbug)
- How to proceed when no recent changes exist
- When to escalate vs. continue investigating

---

## Anti-Patterns Detected

### AP-CLR-04: Hedged Questions (Low Severity)
Line 65: "can the issue be triggered reliably?" — This is acceptable as diagnostic question, not a hedged instruction.

### AP-OUT-01: Undefined Format (Medium Severity)
No specification of how to communicate findings during/after debugging.

### AP-AGT-04: Workflow Present but Could Be Clearer (Low Severity)
The 4-phase structure is clear, but transitions between phases could be more explicit (when exactly to move from Phase 1 to Phase 2).

---

## Strengths

### STR-1: Clear Role/Identity ✓
"Mandatory root cause protocol for any bug, test failure, or unexpected behavior" (line 12)

### STR-2: Relevant Context ✓
"The Iron Law" (lines 16-20) establishes the philosophy before rules.

### STR-3: Clear Task Definition ✓
"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" (line 17) — unambiguous.

### STR-4: Consistent Structural Markers ✓
Excellent use of headers, numbered phases, code blocks, tables.

### STR-6: Data Separated from Instructions ✓
Code examples and patterns clearly separated with markdown blocks.

### CLR-1: Specific and Actionable ✓
Every phase has concrete, executable steps.

### CLR-3: No Contradictions ✓
All instructions are coherent and mutually reinforcing.

### CLR-5: Numbered Steps ✓
4 phases clearly numbered, sub-steps numbered within each phase.

### CLR-7: Appropriate Tone ✓
Authoritative technical tone matches the task.

### CON-1: Explicit Scope Definition ✓
"Apply for ANY technical issue: test failures, production bugs..." (line 25)
"Do not skip when:" section (lines 34-36) defines boundaries.

### CON-2: Forbidden Actions Explicit ✓
"Red Flags" section (lines 163-178) lists prohibited thought patterns.

### CON-4: Rationale Provided ✓
Constraints include "WHY:" explanations (e.g., lines 61-62).

### CON-6: Constraints Grouped ✓
"Red Flags," "Common Rationalizations," "User Signals" sections group related constraints.

### SAF-2: Input Validation ✓
Phase 1 step 2: "Reproduce Consistently" — validates that the bug is real.

### SAF-6: Error Handling for Fix Failures ✓
Phase 4 step 4: Clear escalation protocol after 3 failed fixes (lines 136-156).

### RSN-1: Explicit Reasoning Request ✓
Phase 2: "Pattern Analysis" — explicit investigation before action.

### RSN-3: Provides "Out" for Uncertainty ✓
Phase 3 step 4: "Say 'I do not understand X.' Do not pretend to know." (line 117)

### RSN-4: Evidence Before Conclusions ✓
Phase 1 requires evidence gathering before Phase 3 hypothesis formation.

### AGT-1: Has Name Field ✓
`name: systematic-debugging` (line 2)

### AGT-2: Description with Trigger Keywords ✓
Rich trigger list: "bug", "test failure", "unexpected behavior", "error", "crash", etc. (lines 4-6)

### AGT-3: Proactive Use Indicated ✓
"Apply BEFORE proposing any fix, especially under time pressure" (line 8)

### AGT-6: Clear Workflow ✓
Mandatory 4-phase structure: Root Cause → Pattern Analysis → Hypothesis → Implementation

### AGT-7: Focused Scope ✓
Single clear purpose: systematic debugging with root cause analysis.

---

## Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|-----------|--------|--------|-------|
| STRUCTURE | ✓ | 5/6 | STR-5 (minor ordering) | 5/6 |
| CLARITY | ✓ | 5/7 | CLR-2 (borderline), CLR-4 (success criteria) | 5/7 |
| CONSTRAINTS | ✓ | 6/6 | None | 6/6 |
| SAFETY | ✓ | 4/6 | SAF-1 (N/A), SAF-6 (edge cases) | 4/6 |
| OUTPUT | ✓ | 2/6 | OUT-1 (format), OUT-3 (edge cases), OUT-4 (preamble), OUT-6 (exclusions) | 2/6 |
| REASONING | ✓ | 3/4 | RSN-2 (N/A) | 3/4 |
| AGENT_SPECIFIC | ✓ | 7/10 | AGT-4 (tools), AGT-5 (permissions), AGT-8 (output format) | 7/10 |

**Calculation:**
- Total applicable criteria: ~41
- Passed: 32
- MUST violations: 0
- SHOULD met: 32 (+32 points)
- Raw score: 32 / 41 × 100 = 78
- Adjusted for strong constraint adherence: ~85/100

---

## Recommendations

### Priority 1: Add Output Format Specification

```markdown
## Reporting Protocol

During debugging:
- State current phase and findings in real-time
- Quote exact error messages and line numbers
- Show command outputs when gathering evidence

After debugging:
- Summary: Root cause in 1-2 sentences
- Evidence: Quote key findings that led to diagnosis
- Fix: Code changes with brief explanation
- Verification: Test results confirming resolution
```

### Priority 2: Define Success Criteria

```markdown
## Debugging Session Completion Criteria

A debugging session is complete when ALL of these are true:
- [ ] Root cause identified and understood
- [ ] Hypothesis tested and confirmed
- [ ] Fix implemented
- [ ] Test case added reproducing the bug
- [ ] All existing tests still pass
- [ ] Fix verified in environment where bug occurred
```

### Priority 3: Add Edge Case Handling

```markdown
## Edge Cases

### Non-Reproducible Bugs (Heisenbugs)
If reproduction is impossible after 3 attempts:
1. Add instrumentation/logging
2. Monitor in production/staging
3. Gather crash dumps or telemetry
4. Document conditions when bug appears
5. Escalate to user with findings

### No Recent Changes
If git history shows no recent changes:
- Check environment changes (dependencies, config, infrastructure)
- Check data changes (database migrations, new data patterns)
- Check external dependencies (API changes, third-party services)
```

### Priority 4: Tighten Vague Terms

- Line 107: "Make the SMALLEST possible change" → "Change one variable only"
- Line 43: "Read Error Messages Carefully" → "Read Error Messages Completely" (already says "completely" for stack traces, use consistently)

### Priority 5: Improve Phase Transitions

Add explicit transition criteria:

```markdown
## Phase Transitions

**1 → 2:** When you can reliably reproduce the bug AND have traced data flow
**2 → 3:** When you have identified differences between working and broken code
**3 → 4:** When hypothesis is confirmed through minimal test
**Return to 1:** When hypothesis is disproven or fix fails
```

### Priority 6: Add Tool Restrictions (Optional)

Consider specifying minimal tools needed:
```yaml
tools: ["Read", "Grep", "Glob", "Bash"]
disallowedTools: ["Write", "Edit"]  # During investigation phase
```

---

## Quick Wins

1. Add "## Reporting Protocol" section specifying output format
2. Add "Debugging Session Completion Criteria" checklist
3. Move "User Signals of Process Violation" earlier (after Phase 4)
4. Replace "smallest" with "single-variable" (line 107)
5. Add "Phase Transitions" subsection to workflow

---

## Vague Term Instances (Borderline)

| Term | Line | Context | Assessment |
|------|------|---------|------------|
| carefully | 43 | "Read Error Messages Carefully" | Acceptable (followed by specifics) |
| completely | 44 | "Read stack traces completely" | Acceptable (unambiguous) |
| minimal/smallest | 107 | "SMALLEST possible change" | Borderline (could use "single-variable") |

---

## Contradictions: None Detected

The skill maintains internal consistency throughout. The 4-phase structure is mutually reinforcing.

---

## Conclusion

The systematic-debugging skill is **strong and well-designed**. It has:
- Clear mandatory workflow
- Excellent constraint specification
- Strong reasoning guidance
- Good error handling for fix failures

The primary weakness is **lack of output format specification**—the skill doesn't tell Claude HOW to report findings. This is a common gap in process-oriented skills that focus on methodology but not deliverables.

**Primary improvements needed:**
1. Add reporting protocol (output format specification)
2. Add completion criteria checklist
3. Add edge case handling (non-reproducible bugs, etc.)
4. Tighten "smallest" to "single-variable"

With these changes, the skill would move from "Good" (85) to "Excellent" (92-95).

**Current strengths to preserve:**
- The Iron Law framing
- Red flags section
- Common rationalizations table
- User signals detection
- Architectural questioning threshold
- Progressive disclosure via @references
