---
name: triage-issue
description: >
  This skill should be used when the user reports a bug, says "this is broken",
  asks to "triage an issue", "investigate a bug", "find the root cause", "file an issue
  for this bug", "create a GitHub issue", or wants autonomous diagnosis of a problem
  in the codebase. Produces root cause analysis, TDD fix plan, and a GitHub issue.
---

# Triage Issue

Autonomously diagnose a reported bug, trace its root cause, design a TDD fix plan,
and publish a GitHub issue -- all with minimal user interaction.

## Why Autonomous

Bug triage benefits from depth of investigation, not breadth of questioning.
One question to the user ("What's the problem?") then full autonomous exploration.
Follow-up questions waste the user's time when the codebase contains all the evidence.

## The Protocol

### Phase 1: Capture the Problem

Get a brief description of the issue from the user. If they have not provided one,
ask ONE question: "What problem are you seeing?"

Do NOT ask follow-up questions. Start investigating immediately.

### Phase 2: Explore and Diagnose

Launch a deep investigation of the codebase. Find four things:

| Question | Method |
|----------|--------|
| **WHERE** does the bug manifest? | Trace entry points: UI components, API handlers, CLI commands |
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

If the agentic-delegation skill is available, apply its Speculative Parallel pattern
for hypothesis testing -- launch parallel agents each investigating a different causal
hypothesis simultaneously. Otherwise, launch background agents for each hypothesis
independently, then read their summaries to determine which has supporting evidence.

### Phase 3: Classify the Issue

Based on investigation, determine:

- **Type**: regression (worked before), missing feature (never implemented), or design flaw (works as coded but coded wrong)
- **Scope**: single module, cross-module integration, or systemic pattern
- **Minimal fix**: the smallest change that addresses the root cause
- **Affected interfaces**: which module boundaries the fix touches

### Phase 4: Design TDD Fix Plan

Create an ordered sequence of RED-GREEN cycles. Each cycle is one vertical slice:

- **RED**: Describe a specific test capturing the broken or missing behavior
- **GREEN**: Describe the minimal code change to make that test pass

Rules for the fix plan:

1. **Vertical slices only.** Each cycle writes one test then one implementation change.
   Never batch all tests first then all implementation.

2. **Public interface tests.** Tests verify behavior through module boundaries
   (API responses, function return values, observable state changes), not through
   implementation internals (private methods, internal data structures).

3. **Durable descriptions.** Describe behaviors and contracts, not file paths or
   line numbers. A good test description reads like a spec; a bad one reads like
   a diff. The plan must remain useful after major refactors.

4. **Survival criterion.** Each test must survive internal refactoring of the
   module under test. If renaming a private function would break the test,
   the test targets the wrong abstraction level.

5. **Refactor step.** Include a final REFACTOR step after all RED-GREEN cycles
   if cleanup is needed (extract shared logic, rename for clarity, remove duplication).

### Phase 5: Create GitHub Issue

Create the issue using `gh issue create` with the structure below. Do NOT ask
the user to review before creating -- publish directly and share the URL.

```
## Problem

- **Actual behavior**: what happens now
- **Expected behavior**: what should happen
- **Reproduction**: steps or conditions (if applicable)

## Root Cause Analysis

Describe the investigation findings:
- The code path and module boundaries involved
- Why the current code produces incorrect behavior
- Contributing factors (missing validation, incorrect assumption, race condition, etc.)

Do NOT include specific file paths, line numbers, or implementation details
that couple to the current code layout. Describe modules, behaviors, and
contracts. The issue must remain useful after major refactors.

## TDD Fix Plan

1. **RED**: Write a test that [expected behavior description]
   **GREEN**: [Minimal change to make it pass]

2. **RED**: Write a test that [next behavior description]
   **GREEN**: [Minimal change to make it pass]

...

**REFACTOR**: [Cleanup needed after all tests pass, if any]

## Acceptance Criteria

- [ ] Root cause is addressed, not just the symptom
- [ ] All new tests pass
- [ ] Existing tests still pass
- [ ] No regression in adjacent functionality
```

After creating the issue, print the issue URL and a one-line summary of the root cause.

## Edge Cases

- **Cannot reproduce**: Document the investigation path, hypotheses tested,
  and why reproduction failed. Create the issue anyway with findings --
  partial diagnosis is more valuable than no documentation.

- **Multiple root causes**: If investigation reveals distinct independent causes,
  create separate issues for each. Cross-reference them in each issue body.

- **Fix requires design change**: If the root cause is a design flaw that needs
  architectural rework (not a simple fix), note this in the issue and suggest
  using the improve-architecture skill for the design phase.

---

*Originally based on triage-issue from https://github.com/mattpocock/skills, MIT licensed. Adapted and enhanced for this plugin.*
