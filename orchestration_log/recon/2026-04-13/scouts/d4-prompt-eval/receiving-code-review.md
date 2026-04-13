# Prompt Evaluation: receiving-code-review

**Type:** Skill (Claude Code)
**Evaluated:** 2026-04-13
**File:** `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/receiving-code-review/SKILL.md`

---

## Overall Score: 88/100 (Good)

**Rating:** Functional with minor improvements possible

The skill is exceptionally well-structured with clear behavioral constraints and excellent example patterns. Minor gaps in output specification and edge case handling prevent an excellent rating.

---

## Critical Issues

None. No MUST or MUST_NOT violations detected.

---

## Warnings

### OUT-1: Partial Output Format Specification
The skill specifies WHAT to say (technical acknowledgment vs. performative agreement) but not HOW to structure multi-item responses.

**Missing:**
- Format for multi-item feedback responses
- Whether to respond item-by-item or in aggregate
- How to structure clarifying questions

### OUT-3: Limited Edge Case Handling
No guidance for:
- How to respond when verification is impossible
- Format when feedback contains both correct and incorrect items
- Response structure when requesting user consultation

### CLR-4: Implicit Success Criteria
No explicit definition of "successful code review response." What constitutes complete adherence to this protocol?

### SAF-6: Limited Error Handling
No guidance for:
- What to do when implementer cannot verify reviewer suggestions
- How to handle conflicts between multiple reviewers
- When user is unavailable for architectural consultation

---

## Anti-Patterns Detected

### AP-OUT-01: Undefined Format (Medium Severity)
While response patterns are given (lines 42-48, 122-132), overall structure for complex feedback is not specified.

### AP-OUT-03: Missing Edge Cases (Medium Severity)
No handling for:
- Mixed correct/incorrect feedback
- Impossible-to-verify suggestions
- Conflicting reviewer opinions

---

## Strengths

### STR-1: Clear Role/Identity ✓
"Protocol for receiving and acting on code review feedback with technical rigor" (line 14)

### STR-2: Excellent Context ✓
"Core Principle" (lines 16-18) establishes philosophy before rules.

### STR-3: Clear Task Definition ✓
6-step response pattern (lines 22-30) is unambiguous.

### STR-4: Consistent Structural Markers ✓
Excellent use of headers, code blocks, tables, bullet lists.

### STR-5: Logical Ordering ✓
Follows recommended sequence: Role → Core Principle → Response Pattern → Constraints → Examples → Implementation

### STR-6: Data Separated from Instructions ✓
Example responses clearly tagged as GOOD/BAD.

### CLR-1: Specific and Actionable ✓
Every step in the response pattern is concrete.

### CLR-3: No Contradictions ✓
All instructions coherent and mutually reinforcing.

### CLR-5: Numbered Steps ✓
Response pattern has 6 numbered steps (lines 24-30).

### CLR-7: Appropriate Tone ✓
Professional, technical tone matches code review context.

### CON-1: Explicit Scope Definition ✓
"Source-Specific Handling" (lines 66-90) defines boundaries between user feedback and external reviewer feedback.

### CON-2: Forbidden Actions Explicit ✓
"Prohibited Response Patterns" (lines 33-50) — one of the clearest constraint sections encountered.

### CON-4: Rationale Provided ✓
"**Rationale:** The code itself demonstrates that feedback was received. Performative agreement adds no technical value and wastes time." (line 51)

### CON-6: Constraints Well-Grouped ✓
Prohibited patterns, required patterns, and rationale grouped together (lines 31-53).

### SAF-2: Input Validation ✓
"Clarity Gate" (lines 54-64) — validates understanding before proceeding.

### EXM-1: Examples Well-Tagged ✓
GOOD/BAD labels consistently used (lines 122-145).

### EXM-2: Diverse Examples ✓
Examples cover: acknowledgment, correction, pushback, mixed scenarios.

### EXM-3: Input/Output Pairs ✓
Every BAD pattern has a GOOD alternative.

### RSN-3: Provides "Out" for Uncertainty ✓
"When verification is not possible, state the limitation" (line 87)

### AGT-1: Has Name Field ✓
`name: receiving-code-review` (line 2)

### AGT-2: Description with Trigger Keywords ✓
Rich triggers: "receives code review feedback", "gets review comments", "has PR feedback", etc. (lines 6-8)

### AGT-6: Clear Workflow ✓
6-step response pattern provides mandatory workflow.

### AGT-7: Focused Scope ✓
Single purpose: anti-performative code review protocol.

### AGT-8: Output Format Specified (Partially) ✓
Response patterns specified at sentence level, though not at document level.

---

## Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|-----------|--------|--------|-------|
| STRUCTURE | ✓ | 6/6 | None | 6/6 |
| CLARITY | ✓ | 5/7 | CLR-2 (N/A), CLR-4 (success criteria) | 5/7 |
| CONSTRAINTS | ✓ | 6/6 | None | 6/6 |
| SAFETY | ✓ | 3/6 | SAF-1 (N/A), SAF-3 (N/A), SAF-6 (edge cases) | 3/6 |
| OUTPUT | ✓ | 3/6 | OUT-1 (partial format), OUT-3 (edge cases), OUT-4 (preamble) | 3/6 |
| EXAMPLES | ✓ | 3/3 | None | 3/3 |
| REASONING | ✓ | 2/4 | RSN-1 (N/A), RSN-4 (N/A) | 2/4 |
| AGENT_SPECIFIC | ✓ | 6/10 | AGT-3 (proactive use), AGT-4 (tools), AGT-5 (permissions), AGT-9 (length acceptable) | 6/10 |

**Calculation:**
- Total applicable criteria: ~41
- Passed: 34
- MUST violations: 0
- SHOULD met: 34 (+34 points)
- Raw score: 34 / 41 × 100 = 82.9
- Adjusted for exceptional constraint clarity: ~88/100

---

## Recommendations

### Priority 1: Add Complete Output Format Specification

```markdown
## Response Format

### For Single-Item Feedback
[Technical restatement or action, 1 sentence]

### For Multi-Item Feedback
Before implementation:
1. List unclear items
2. Ask clarifying questions
3. Wait for all clarifications

After clarification:
For each item:
- Item [N]: [Technical restatement]
- Action: [Specific fix or pushback with reasoning]
- Status: [Implemented | Will implement after X | Needs discussion]

### For Mixed Correct/Incorrect Feedback
- Correct items: [List with brief acknowledgment]
- Items requiring discussion: [List with technical reasoning]
```

### Priority 2: Add Success Criteria

```markdown
## Completion Criteria

A code review response is complete when:
- [ ] All feedback items understood (no ambiguity remains)
- [ ] Performative language removed from response
- [ ] Each item has technical acknowledgment or reasoned pushback
- [ ] Fixes tested individually
- [ ] No regressions introduced
- [ ] All tests pass
```

### Priority 3: Add Edge Case Handling

```markdown
## Edge Cases

### Impossible to Verify
When verification is impossible:
"Cannot verify [X] without [Y]. Options:
1. Proceed with implementation assuming reviewer is correct
2. Request [Y] from user
3. Ask reviewer for evidence/reproduction

Preferred approach?"

### Conflicting Reviewers
When reviewers disagree:
"Reviewers have conflicting opinions on [X]:
- Reviewer A: [position]
- Reviewer B: [position]

Technical analysis: [reasoning]
Recommendation: [choice with justification]

User: Please confirm approach."

### User Unavailable
When architectural decision needed but user unavailable:
"This feedback conflicts with [prior architectural decision X].
Cannot proceed without user confirmation.
Marking as blocked: needs architectural review."
```

### Priority 4: Clarify Proactive Use

Add to description:
```yaml
description: >
  ...
  INVOKE IMMEDIATELY when code review feedback is received, BEFORE responding.
  This skill prevents performative responses that waste reviewer time.
```

### Priority 5: Specify Tool Restrictions

```yaml
tools: ["Read", "Grep", "Bash"]
# Read: verify codebase reality
# Grep: check actual usage (YAGNI enforcement)
# Bash: run verification commands
# NO Write/Edit until verification complete
```

### Priority 6: Add Preamble Control

```markdown
## Communication Style

Responses to code review feedback must:
- Skip introductory phrases
- Skip closing pleasantries
- State action or reasoning directly
- Use technical language only

Example:
❌ "Thank you for the feedback! I'll get started on these right away."
✅ [Direct implementation or technical questions]
```

---

## Quick Wins

1. Add "## Response Format" section with templates for 1-item, multi-item, and mixed feedback
2. Add "Completion Criteria" checklist
3. Add edge case handling for impossible-to-verify and conflicting reviewers
4. Add preamble control to "Communication Style"
5. Add tool restrictions to frontmatter

---

## Vague Term Instances

None detected. This skill has excellent specificity.

---

## Contradictions: None Detected

The skill maintains perfect internal consistency. The anti-performative protocol is coherent throughout.

---

## Notable Excellence

This skill demonstrates several exemplary patterns:

1. **Best-in-class constraint specification**: The "Prohibited Response Patterns" section (lines 33-50) is a model for other skills. It lists exact phrases to avoid with clear rationale.

2. **Excellent GOOD/BAD pairing**: Every prohibited pattern has a concrete alternative.

3. **Strong rationale**: Explains WHY anti-performative matters ("adds no technical value and wastes time").

4. **Clear decision logic**: The Clarity Gate (lines 54-64) is a perfect example of conditional workflow.

5. **Practical composability**: References defensive-planning skill appropriately (lines 171-173).

---

## Conclusion

The receiving-code-review skill is **exceptionally well-designed** in terms of:
- Constraint clarity
- Behavioral specification
- Example quality
- Internal consistency

The primary weakness is **incomplete output format specification**—while it tells Claude WHAT to say, it doesn't fully specify HOW to structure complex responses.

**Primary improvements needed:**
1. Add response format templates (single-item, multi-item, mixed)
2. Add completion criteria checklist
3. Add edge case handling (impossible verification, conflicting reviewers)
4. Add preamble control guidance

With these additions, the skill would reach "Excellent" (92-95).

**Current strengths to preserve:**
- Prohibited/Required response patterns with rationale
- Clarity Gate
- Source-specific handling
- YAGNI enforcement protocol
- Graceful correction patterns
- Implementation order specification
- Common mistakes table

This skill is already production-ready and highly effective. The recommended improvements would make it even more robust.
