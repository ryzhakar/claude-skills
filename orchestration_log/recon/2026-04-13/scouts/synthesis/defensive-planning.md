# Synthesis Report: defensive-planning (Re-synthesis)

**Baseline:** 2178t (SKILL.md) + 850t (tdd-mode.md) + 832t (execution.md) + 661t (module-design.md) = 4521t total

**Previous synthesis:** Kept all three refs as lazy files. Models ignore references in practice. This re-synthesis inlines all reference content with compression.

---

## Core Points (Untouchable)

1. Implementer optimizes for "appears done" over "is done" -- plan must make appearing done harder than being done
2. Eliminate all decisions and options -- every alternative is an escape hatch
3. Verification gates with executable commands and exact expected output, not subjective checklists
4. Correction plans name observed failure modes and close the specific escape hatches exploited
5. Exhaustive enumeration of every file, field, and step -- no implicit behavior

---

## Inline from References

### INLINE: tdd-mode.md (850t)

Cite: D1 classifies as DEFERRABLE, but the directive overrides: all refs under 1400t must inline. Previous synthesis kept this as lazy reference. Models ignore references in practice -- content must be in the body.

**Content to inline (compressed ~500t):**

Insert after the "Writing Implementation Plans > Rules for Writing Plans" section, as a new subsection "TDD Micro-Task Structure":

```
### TDD Micro-Task Structure

For plans targeting TDD workflows, structure each task as a 2-5 minute red-green cycle with checkbox tracking:

- **Files:** List exact paths to create, modify, and test
- **Step 1:** Write failing test (include test code)
- **Step 2:** Run test, verify it fails (include command and expected failure)
- **Step 3:** Write minimal implementation (include code)
- **Step 4:** Run test, verify it passes (include command and expected output)
- **Step 5:** Commit (include exact git commands)

Never batch all tests then all implementation (horizontal slicing produces tests verifying imagined behavior).

**File decomposition before tasks:** Map which files will be created or modified. Each file has one responsibility. Files that change together live together. Each task produces self-contained changes.

**Plan self-review after writing:**
1. Spec coverage: point each requirement to the task implementing it. List gaps.
2. Placeholder scan -- all are plan failures: "TBD", "TODO", "implement later", "add appropriate error handling", "similar to Task N", steps without code blocks, references to undefined types/functions.
3. Type consistency: verify names and signatures in later tasks match what earlier tasks defined.
```

**Savings from deleting reference file:** 850t removed. Body grows ~500t. Net: -350t.

### INLINE: execution.md (832t)

Cite: D1 classifies as DEFERRABLE (post-planning phase). Directive overrides: all refs under 1400t must inline. Models skip lazy references.

**Content to inline (compressed ~480t):**

Replace the current reference link at line 369 with a new section "Plan Execution Protocol" before the "Remember" closing:

```
## Plan Execution Protocol

### Pre-Execution Review Gate

Before starting implementation: read the plan completely, identify questions or gaps, raise concerns with the user BEFORE starting. A plan that looked good during writing may reveal gaps from an executor's perspective.

### Task State Tracking

Track each task: `not_started -> in_progress -> completed | blocked`. Use markdown checkboxes. Mark completed only after all verification gates pass.

### Blocker Escalation

STOP executing when: hit a missing dependency, test failure contradicts plan, instruction is ambiguous, verification gate fails 2+ times. Ask for clarification rather than guessing. Report: which task, what is failing, what was attempted, what is needed.

### Two-Stage Review Ordering

After each task:
1. **Spec compliance first:** verify implementation matches specification line by line. Do not trust self-reports.
2. **Code quality second (only after Stage 1 passes):** verify quality, testing, architecture. Categorize: Critical / Important / Minor.

Reviewing quality before confirming spec compliance wastes effort -- polishing code that does not meet requirements is wasted work.

### Status-Driven Branching

| Status | Action |
|---|---|
| DONE | Proceed to spec compliance review |
| DONE_WITH_CONCERNS | Read concerns; address if about correctness, note if observations |
| NEEDS_CONTEXT | Provide missing context and re-dispatch |
| BLOCKED | Assess: context problem, reasoning problem, task too large, or plan wrong |
```

**Savings from deleting reference file:** 832t removed. Body grows ~480t. Net: -352t.

### INLINE: module-design.md (661t)

Cite: D1 classifies as DEFERRABLE (multi-module architecture). Directive overrides: all refs under 1400t must inline. Models skip lazy references.

**Content to inline (compressed ~380t):**

Replace the current reference link at line 71 with inline content within the "Writing Implementation Plans" section:

```
### Module Design Heuristics

**Deep modules:** Encapsulate complex functionality behind a simple interface. Ask: can I reduce the number of methods? Simplify parameters? Hide more complexity inside? Shallow modules (large interface, thin implementation) create overhead without encapsulation.

**Testability as decomposition criterion:** Module boundaries should coincide with testability boundaries. A module that accepts dependencies (not creates them), returns results (not side effects), and has a small surface area is testable through its public interface alone.

**Testing decisions section in plans:**

```markdown
## Testing Decisions
- Tests verify behavior through public interfaces, not implementation details
- Tests survive internal refactoring
- Modules tested: [Module A] -- [behaviors]; [Module B] -- [behaviors]; [Module C] -- not tested (justification)
- Test runner, naming convention, prior art paths
```

This runs before task decomposition: file structure identifies modules, deep-modules heuristic evaluates interfaces, testability confirms each module can be tested through its interface.
```

**Savings from deleting reference file:** 661t removed. Body grows ~380t. Net: -281t.

---

## Cut

### CUT-1: Redundant closing block (lines 372-384, ~60t)
Cite: D3 Strunk R13: "These two sentences say the same thing from different angles."
**Action:** Remove "The implementer optimizes for completion, not correctness." Keep the three parallel emphatic sentences and "Plan defensively." Cut attribution to single line.
**Savings:** ~60t

### CUT-2: Redundant preamble template (line 49, ~5t)
Cite: D3 Strunk R13.
**Action:** "Why this plan exists. What problem it solves." -> "What problem this solves."

### CUT-3: "Write it down" after "Pick one" (line 76, ~3t)
Cite: D3 Strunk R13.
**Action:** Remove.

### CUT-4: Reference link sentences now deleted (~25t)
Three @references/ link sentences removed since content is inlined.

### CUT-5: Description compression (lines 4-9, ~40t)
Cite: D3 Strunk R13: "Point (4) restates (1-3)."
**Action:** Compress to two sentences keeping all trigger phrases.

**Total cut savings:** ~133t

---

## Restructure

### RESTRUC-1: Active voice for document type definitions (lines 31, 34, 37)
Cite: D3 Strunk R10 Severe.
**Action:** "Written BEFORE work begins" -> "Write BEFORE work begins." Same for all three types.

### RESTRUC-2: Parallel construction in severity levels (lines 227-231)
Cite: D3 Strunk R15.
**Action:** Add second sentence to MODERATE and LOW:
- MODERATE: "Feature works but has issues. Creates inconsistency or maintainability debt."
- LOW: "Minor quality issues. Affects style or documentation."

---

## Strengthen

### STR-1: Replace "optimize for" corporate jargon (line 18)
Cite: D3 Strunk R12.
**Action:** "The implementer will optimize for 'appears done' over 'is done'" -> "The implementer will choose appearing done over being done."

### STR-2: Replace vague "actual behavior" (line 206)
Cite: D3 Strunk R12, D4 CLR-2.
**Action:** "Passing tests prove nothing about semantic correctness. Verify function output matches specification."

### STR-3: Tighten anti-pattern descriptions (lines 321-325)
Cite: D3 Strunk R13.
**Action:** "Every 'or' lets implementers choose the easier option." / "Conditional language ('if needed') invites omission."

### STR-4: Positive form for Rule 7 title (line 164)
Cite: D3 Strunk R11.
**Action:** "No Implicit Behavior" -> "Make All Behavior Explicit"

---

## Hook/Command Splits

No hook candidates. Defensive planning produces documents, not tool-use enforcement.

---

## Delete List

- `dev-discipline/skills/defensive-planning/references/tdd-mode.md`
- `dev-discipline/skills/defensive-planning/references/execution.md`
- `dev-discipline/skills/defensive-planning/references/module-design.md`

---

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| SKILL.md body | 2178t | ~2405t | +227t |
| tdd-mode.md | 850t | 0 (deleted) | -850t |
| execution.md | 832t | 0 (deleted) | -832t |
| module-design.md | 661t | 0 (deleted) | -661t |
| **Total** | **4521t** | **~2405t** | **-2116t (-46.8%)** |

Nearly 47% total reduction. The SKILL.md body grows by ~227t from inlined reference content (compressed from 2343t total refs to ~1360t inline). All reference files deleted. Models now see the full content every time the skill loads, instead of ignoring lazy references.
