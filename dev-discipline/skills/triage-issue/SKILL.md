---
name: triage-issue
description: >
  Autonomously diagnoses bugs, traces root causes, designs TDD fix plans, and writes
  issue documents. Triggers: bug reports, "this is broken", "triage an issue", "investigate
  a bug", "find the root cause", "file an issue for this bug", autonomous problem diagnosis.
---

# Triage Issue

With minimal user interaction, autonomously diagnose a reported bug, trace its root cause,
design a TDD fix plan, and write an issue document to disk.

## Why Investigate Autonomously

Thorough investigation improves bug triage more than broad questioning.
One question to the user ("What's the problem?") then autonomous exploration.
Follow-up questions waste the user's time when the codebase contains the evidence.

## The Protocol

### Phase 1: Capture the Problem

Get a brief description of the issue from the user. If they haven't yet described it,
ask ONE question: "What problem are you seeing?"

Do NOT ask follow-up questions. Start investigating immediately.

### Phase 2: Explore and Diagnose

Investigate the codebase. Find four things:

| Question | Method |
|----------|--------|
| **WHERE** does the bug manifest? | Locate entry points: UI components, API handlers, CLI commands |
| **WHAT** code path is involved? | Follow the call chain from entry to failure |
| **WHY** does it fail? | Identify root cause, not symptom |
| **WHAT ELSE** shares this pattern? | Search for similar code that works or fails the same way |

Investigation checklist:
- Read related source files and their imports/dependencies
- Check existing tests (what is tested, what is missing)
- Run `git log` on affected files to find recent changes
- Examine error handling in the code path
- Search for similar patterns elsewhere that work correctly
- Look at type definitions and interface contracts at module boundaries

If you have access to the agentic-delegation skill, apply its Speculative Parallel pattern
for hypothesis testing -- launch parallel agents each investigating a different causal
hypothesis simultaneously. Otherwise, launch background agents for each hypothesis
independently, then read their summaries to determine which has supporting evidence.

### Phase 3: Classify the Issue

From your investigation, determine:

- **Classification**: regression (worked before), missing feature (never implemented), or design flaw (works as coded but coded wrong)
- **Scope**: single module, cross-module integration, or systemic pattern
- **Minimal fix**: the smallest change that fixes the root cause
- **Affected interfaces**: which module boundaries the fix touches

### Phase 4: Design TDD Fix Plan

Create an ordered sequence of RED-GREEN cycles. Each cycle is one vertical slice:

- **RED**: Describe a specific test capturing the broken or missing behavior
- **GREEN**: Describe the minimal code change to make that test pass

Fix plan rules:

1. **Vertical slices only.** Each cycle writes one test, then one implementation change.
   Never batch all tests first then all implementation.

2. **Test through public boundaries.** Tests verify behavior through module boundaries
   (API responses, function returns, state changes), not through implementation internals
   (private methods, internal structures).

3. **Refactor-proof descriptions.** Describe behaviors and contracts, not file paths or
   line numbers. A good test description reads like a spec; a bad one reads like
   a diff. The plan survives major refactors.

4. **Refactoring resilience test.** Each test must survive internal refactoring of the
   module under test. If renaming a private function would break the test,
   the test targets the wrong abstraction level.

5. **Refactor step.** Include a final REFACTOR step after all RED-GREEN cycles
   if cleanup is needed (extract shared logic, clarify names, remove duplication).

### Phase 5: Write Issue Document

Write the issue document to a file in the project's issue tracking directory (e.g., `issues/`, `docs/issues/`, or the project's convention) with this structure.
Write the file directly and share the file path without asking for review.

```
## Problem

- **Actual behavior**: what the code does now
- **Expected behavior**: what should happen
- **Reproduction**: how to trigger it (if applicable)

## Root Cause Analysis

Describe your investigation:
- The code path and module boundaries involved
- Why the current code produces incorrect behavior
- Contributors (missing validation, incorrect assumption, race condition, etc.)

Describe modules, behaviors, and contracts instead of file paths, line numbers,
or layout-specific implementation details. Write the issue so major refactors
won't invalidate it.

## TDD Fix Plan

1. **RED**: Write a test that [expected behavior description]
   **GREEN**: [Minimal change to make it pass]

2. **RED**: Write a test that [next behavior description]
   **GREEN**: [Minimal change to make it pass]

...

**REFACTOR**: [Cleanup needed after all tests pass, if any]

## Acceptance Criteria

- [ ] Fix addresses root cause, not just symptom
- [ ] All new tests pass
- [ ] All existing tests pass
- [ ] Adjacent functionality remains intact
```

After writing the issue document, print the file path and a one-line summary of the root cause.

## Edge Cases

- **Cannot reproduce**: Document the investigation path, which hypotheses you tested,
  and why reproduction failed. Write the issue document anyway -- partial diagnosis beats silence.

- **Multiple root causes**: If investigation reveals distinct independent causes,
  write separate issue documents for each. Cross-reference them in each document.

- **Fix requires design change**: If the root cause stems from flawed design requiring
  architectural rework, note this in the issue and suggest using the improve-architecture
  skill.
