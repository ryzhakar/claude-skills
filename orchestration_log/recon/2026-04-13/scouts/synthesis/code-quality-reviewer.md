# Synthesis Report: code-quality-reviewer (Re-synthesis)

**Baseline:** 1225t (code-quality-reviewer.md) -- no references

**Previous synthesis:** Applied Strunk compression, example compression, concrete checklist items, parallel construction. This re-synthesis preserves those changes.

---

## Core Points (Untouchable)

1. Post-spec-compliance phase operating exclusively on git diff ranges, not the entire codebase
2. Three-tier severity categorization (Critical/Important/Minor) with distinct merge-blocking semantics
3. Balanced feedback mandate -- acknowledge strengths in the changes under review; strengths are structurally required
4. Specificity and actionability -- file:line references, WHY it matters, HOW to fix
5. Evidence-based merge verdict: Ready / With fixes / No, backed by technical reasoning

---

## Inline from References

No references to inline.

---

## Cut

### CUT-1: Description examples compression (~100t)
Cite: Three examples with `<commentary>` blocks consume ~320t.
**Action:** Compress to 2 examples (post-spec review + pre-PR review). Remove `<commentary>`.
**Savings:** ~100t

### CUT-2: Redundant scope restatement (line 145, ~10t)
Cite: D3 Strunk R13: Line 43 states scope; line 145 restates it.
**Action:** Remove "Focus on what THIS change contributed (not pre-existing issues)" from DO section since line 43 already covers scope.
**Savings:** ~10t

**Total cut savings:** ~110t

---

## Restructure

### RESTRUC-1: Active voice for scope directive and checklist questions
Cite: D3 Strunk R10 Moderate.
- Line 43: "Your review is scoped to a specific git range" -> "Scope your review to a specific git range"
- Line 77: "Are units decomposed so they can be understood and tested independently?" -> "Can you understand and test each unit independently?"
- Line 83: "Edge cases covered in tests?" -> "Do tests cover edge cases?"
- Line 89: "Backward compatibility considered?" -> "Does the implementation consider backward compatibility?"

### RESTRUC-2: Parallel construction in quality checklists (lines 65-90)
Cite: D3 Strunk R15 Moderate.
**Action:** Standardize all checklist items to interrogative form:
- "Clean separation of concerns?" -> "Does each module handle one concern?"
- "Proper error handling?" -> "Do errors propagate with specific messages?"
- "DRY principle followed?" -> "Is duplicated logic extracted to shared functions?"
- "Edge cases handled?" -> "Are edge cases handled (null values, empty collections, boundary conditions)?"
- "Names are clear and descriptive?" -> "Do names describe the public interface?"
- "Sound design decisions?" -> "Do design decisions match requirements without over-engineering?"
- "No obvious performance issues?" -> "Are there N+1 queries, unbounded loops, or unnecessary recomputations?"
- "No hardcoded secrets?" -> "Do secrets use environment variables, not hardcoded values?"

### RESTRUC-3: Parallel construction in issue templates (lines 113-130)
Cite: D3 Strunk R15 Moderate.
**Action:** Standardize all three severity templates to same field structure: File, Issue, Impact, Fix. Minor issues still get Impact (even if brief) and Fix (even if "optional improvement").

### RESTRUC-4: Emphatic position fixes
Cite: D3 Strunk R18 Moderate.
- Line 51: "balanced feedback is more useful than pure criticism" -> "pure criticism is less useful than balanced feedback"
- Line 154: "Note the ambiguity and request clarification rather than guessing" -> "Rather than guess, note the ambiguity and request clarification"

---

## Strengthen

### STR-1: Concrete checklist items replacing vague terms
Cite: D4 W1 and D3 Strunk R12.
- "Proper error handling (not swallowed, not generic)" -> "Errors caught with specific messages and propagated, not swallowed or caught generically"
- "Type safety (if applicable)" -> "Type annotations complete and preventing invalid data"
- "Edge cases handled" -> "Edge cases handled (null values, empty collections, boundary conditions)"
- "Sound design decisions" -> "Design decisions match requirements without over-engineering"
- "No obvious performance issues" -> "No N+1 queries, unbounded loops, or unnecessary recomputations"

### STR-2: Clarify "strengths in changes" (line 50)
Cite: D4 W2.
**Action:** "Acknowledge strengths" -> "Acknowledge strengths in the changes under review"

### STR-3: Add self-verification instruction
Cite: D4 R5.
**Action:** Add to DO section: "Spot-check 3 findings by re-reading file:line references before submitting the report."
**Cost:** ~12t added.

---

## Hook/Command Splits

No hook candidates. Code quality review requires reading code, applying judgment, and producing structured reports.

---

## Delete List

None (no reference files).

---

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| code-quality-reviewer.md body | 1225t | ~1137t | -88t |
| **Total** | **1225t** | **~1137t** | **-88t (-7.2%)** |

Primary savings from compressing frontmatter examples (-100t) and removing redundant scope restatement (-10t), offset by self-verification instruction (+12t) and expanded checklist specificity (+10t). D4 score rises from 90 toward 94+ through concrete checklist terms, parallel construction, active voice, and emphatic position fixes.
