# Core Points: implementer.md

## Iteration 1

**Point:** The implementer must escalate immediately when uncertain rather than producing questionable work, using explicit status codes to surface doubts.

**Evidence:**
1. Lines 76-86: "It is always acceptable to stop and escalate. Bad work is worse than no work... Report BLOCKED or NEEDS_CONTEXT with specifics"
2. Line 127: "Never silently produce work that is uncertain. Surface doubts through the status system"
3. Lines 122-125: Four-state status system (DONE, DONE_WITH_CONCERNS, BLOCKED, NEEDS_CONTEXT) forces explicit acknowledgment of uncertainty

## Iteration 2

**Point:** Implementation scope must be strictly bounded to the task specification with no additions, deletions, or architectural freelancing.

**Evidence:**
1. Line 49: "Implement exactly what the task specifies -- nothing more, nothing less"
2. Lines 100-102 (Discipline checklist): "No overbuilding (YAGNI)? Only what was requested was built?"
3. Lines 71-72: "If a file is growing beyond the plan's intent, stop and report DONE_WITH_CONCERNS rather than splitting files without plan guidance"

## Iteration 3

**Point:** Self-review is mandatory before reporting completion, covering completeness, quality, discipline, and testing with required fixes before status submission.

**Evidence:**
1. Lines 51, 66: "Self-review your work before reporting" and "Self-review (see checklist below)" appear in both core responsibilities and process
2. Lines 88-109: Comprehensive checklist covering Completeness, Quality, Discipline, and Testing dimensions
3. Line 109: "If issues are found during self-review, fix them before reporting" makes it a gate, not just a suggestion

## Iteration 4

**Point:** TDD adherence is conditional and task-driven, following red-green-refactor when specified but allowing test-after-implementation otherwise.

**Evidence:**
1. Lines 50, 62: "Follow TDD when the task requires it" and "If the task specifies TDD: write the failing test first, verify it fails, then implement minimally"
2. Line 63: "If the task does not specify TDD: implement the functionality, then write tests" provides alternative path
3. Lines 105-106: Self-review asks "TDD followed if required?" (not "TDD always followed")

## Iteration 5

**Point:** The agent must seek clarification before starting work rather than making assumptions about unclear requirements, dependencies, or approaches.

**Evidence:**
1. Lines 54-56: "If anything about the requirements, approach, dependencies, or assumptions is unclear: ask now. Raise concerns before starting work. It is always acceptable to pause and clarify rather than guess"
2. Lines 33-38 (Example 3): Shows NEEDS_CONTEXT workflow where agent returns for missing schema, then gets re-dispatched with complete information
3. Line 123-124: NEEDS_CONTEXT status exists specifically for "Cannot proceed without information that was not provided"

## Rank Summary

1. **Escalation over guessing** (Iteration 1) — The most emphatic and repeated directive; appears in responsibilities, throughout workflow, and as final warning
2. **Strict scope adherence** (Iteration 2) — Central constraint on all work; prevents both gold-plating and scope creep
3. **Mandatory self-review** (Iteration 3) — Gated requirement before status reporting; comprehensive checklist with fix-before-submit rule
4. **Clarify before starting** (Iteration 5) — Preventive measure that appears early in process and in examples
5. **Conditional TDD** (Iteration 4) — Important methodology guidance but pragmatic rather than dogmatic; follows task specification
