# Synthesis Report: spec-reviewer (Re-synthesis)

**Baseline:** 974t (spec-reviewer.md) -- no references

**Previous synthesis:** Applied Strunk compression, example compression, concrete terms. This re-synthesis preserves those changes.

---

## Core Points (Untouchable)

1. Adversarial posture -- never trust the implementer's report; verify claims against actual code
2. Line-by-line code verification: read specification, then read actual implementation code for each requirement
3. Four-category failure taxonomy: missing, partial, extra (scope creep), misinterpreted
4. File:line evidence for every finding -- verify by reading code, not trusting reports
5. Scope creep detection: unauthorized additions are failures equivalent to missing requirements

---

## Inline from References

No references to inline.

---

## Cut

### CUT-1: Description examples compression (~80t)
Cite: Three examples with `<commentary>` blocks consume ~300t.
**Action:** Compress to 2 examples (post-implementation check + pre-merge verification). Remove `<commentary>`.
**Savings:** ~80t

**Total cut savings:** ~80t

---

## Restructure

### RESTRUC-1: Convert passive checklist questions to active
Cite: D3 Strunk R10 Severe/Moderate.
- Line 84: "Claims of implementation that are not actually present in code?" -> "Does the code contain what the implementer claimed to have built?"
- Line 88: "Features built that were not requested?" -> "Did the implementer build features the spec did not request?"
- Line 92: "Requirements interpreted differently than intended?" -> "Did the implementer interpret any requirement differently than the spec intended?"
- Line 100: "All [N] requirements verified in code" -> "Verified all [N] requirements in code"

### RESTRUC-2: Parallel construction in "What to Check" (lines 83-94)
Cite: D3 Strunk R15 Minor.
**Action:** Standardize question format within each subsection to consistent interrogative sentences.

### RESTRUC-3: Emphatic position fix (line 120)
Cite: D3 Strunk R18 Moderate.
**Action:** "Verify by reading code, not by trusting reports" -> "Do not trust reports; verify by reading code"

---

## Strengthen

### STR-1: Active adversarial posture (line 45)
Cite: D3 Strunk R10 Moderate.
**Action:** "Your posture is adversarial" -> "Adopt an adversarial posture"

### STR-2: Concrete "missing pieces" (line 82)
Cite: D3 Strunk R12 Moderate.
**Action:** "missing pieces the implementer claimed to have built" -> "missing functions, classes, or features the implementer claimed to have built"

### STR-3: Concrete "over-engineering" (line 89)
Cite: D3 Strunk R12 Moderate.
**Action:** "Over-engineering or unnecessary abstractions?" -> "Extra base classes, middleware, or abstraction layers the spec did not require?"

### STR-4: Emphatic ordering in findings template (line 75)
Cite: D3 Strunk R18 Minor.
**Action:** "missing, partial, or misinterpreted" -> "misinterpreted, partially met, or missing entirely" (reorder by ascending severity).

---

## Hook/Command Splits

No hook candidates. Spec review is an analytical process requiring judgment.

---

## Delete List

None (no reference files).

---

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| spec-reviewer.md body | 974t | ~900t | -74t |
| **Total** | **974t** | **~900t** | **-74t (-7.6%)** |

Primary savings from compressing frontmatter examples (-80t), partially offset by concrete language additions (+6t). The agent already scored 92/100 on D4 -- highest in this unit set. Changes focus on prose precision: active voice in checklists, concrete terms replacing abstractions, emphatic position fixes.
