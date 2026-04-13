# Synthesis Report: implementer (Re-synthesis)

**Baseline:** 1321t (implementer.md) -- no references

**Previous synthesis:** Applied Strunk compression, example compression, concrete term replacement. This re-synthesis preserves those changes and adds minor precision improvements.

---

## Core Points (Untouchable)

1. Escalate immediately when uncertain rather than producing questionable work -- no work is better than bad work
2. Implement exactly what the task specifies -- nothing more, nothing less (strict scope adherence)
3. Self-review is mandatory before reporting: completeness, quality, discipline, testing -- fix before submitting
4. Clarify before starting -- raise concerns before work, not during
5. TDD adherence is conditional and task-driven: red-green-refactor when specified, test-after otherwise

---

## Inline from References

No references to inline.

---

## Cut

### CUT-1: Description examples compression (~120t)
Cite: Frontmatter examples at lines 6-40 consume ~400t. Three examples with verbose `<commentary>` blocks.
**Action:** Compress 3 examples. Remove `<commentary>` inner dialogue. Keep dispatch pattern but tighten.
**Savings:** ~120t

### CUT-2: "nothing more, nothing less" after "exactly" (line 49)
Cite: D3 Strunk R13.
**Action:** Retain. Emphatic marker reinforcing Core Point #2. Per directive, emphatic markers preserved.

**Total cut savings:** ~120t

---

## Restructure

### RESTRUC-1: Active voice for critical directives
Cite: D3 Strunk R10 Severe.
- Line 46: "Your job is to produce working, tested, committed code" -> "Produce working, tested, committed code that matches the task specification"
- Line 56: "It is always acceptable to pause and clarify" -> "Always pause and clarify rather than guess"
- Line 109: "If issues are found during self-review, fix them" -> "If you find issues during self-review, fix them"

### RESTRUC-2: Positive form conversions
Cite: D3 Strunk R11 Moderate.
- Line 72: "do not restructure things outside the task scope" -> "Restructure only what the task scope covers"
- Line 127: "Never silently produce work that is uncertain" -> "Always surface doubts through the status system"

### RESTRUC-3: Parallel structure in status definitions (lines 122-125)
Cite: D3 Strunk R15.
- "DONE: Work complete, tested, committed, self-reviewed."
- "DONE_WITH_CONCERNS: Work complete but doubts exist about correctness or approach."
- "NEEDS_CONTEXT: Cannot proceed -- information not provided."
- "BLOCKED: Cannot complete the task. Describe the blocker."

---

## Strengthen

### STR-1: Replace vague "clear" with specific criteria
Cite: D4 W1 (3 instances).
- Line 66: "clear commit message" -> "commit message following `<type>: <what changed>` format"
- Line 73: "one clear responsibility" -> "one responsibility" (drop vague qualifier)
- Line 96: "Names are clear and accurate" -> "Names describe what things do, not how they work"

### STR-2: Concrete escalation triggers (line 81)
Cite: D3 Strunk R12 Severe.
**Action:** "Understanding code beyond what was provided is necessary" -> "You cannot determine dependencies or context from the provided files"

### STR-3: Concrete stalled progress (line 84)
Cite: D3 Strunk R12 Moderate.
**Action:** "Progress has stalled after reading file after file without gaining understanding" -> "You have read multiple files but still cannot locate the relevant logic"

### STR-4: Resolve "minimally" ambiguity (line 63)
Cite: D4 W2.
**Action:** "implement minimally" -> "implement only the code required to make the test pass"

### STR-5: Emphatic position (line 77)
Cite: D3 Strunk R18.
**Action:** "Bad work is worse than no work" -> "No work is better than bad work"

---

## Hook/Command Splits

No hook candidates. The implementer agent operates within a delegation context. Its status system IS the enforcement mechanism.

---

## Delete List

None (no reference files).

---

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| implementer.md body | 1321t | ~1210t | -111t |
| **Total** | **1321t** | **~1210t** | **-111t (-8.4%)** |

Primary savings from compressing verbose frontmatter examples (-120t), partially offset by strengthened language (+9t). D4 score rises from 88 toward 92+ through vague-term resolution ("clear", "minimally"), active voice, and concrete escalation triggers.
