# Synthesis: triage-issue (REVISED -- full inline)

**Baseline**: 1283 tokens (SKILL.md body only, no references)
**D4 Score**: 88/100
**References**: None. No inlining needed.

---

## Core Points (Untouchable)

1. **Autonomous depth over interactive breadth** -- one question, then autonomous investigation without user interruption. (D2 rank 1)
2. **Durable behavioral descriptions** -- describe contracts and behaviors, not implementation details or file paths. (D2 rank 2)
3. **WHERE/WHAT/WHY/WHAT ELSE investigation framework** with comprehensive checklist. (D2 rank 3)
4. **Public interface test discipline** -- tests survive refactoring, target module boundaries. (D2 rank 4)
5. **Document all investigations** -- even failed reproduction or multiple causes produce documented issues. (D2 rank 5)

---

## Proposed SKILL.md

```markdown
---
name: triage-issue
description: >
  Autonomously diagnoses bugs, traces root causes, designs TDD fix plans, and publishes
  GitHub issues. Triggers: bug reports, "this is broken", "triage an issue", "investigate
  a bug", "find the root cause", "create a GitHub issue", autonomous problem diagnosis.
---

# Triage Issue

With minimal user interaction, autonomously diagnose a reported bug, trace its root cause,
design a TDD fix plan, and publish a GitHub issue.

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

### Phase 5: Create GitHub Issue

Create the issue using `gh issue create` with this structure.
Publish directly and share the URL without asking for review.

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

After creating the issue, print the issue URL and a one-line summary of the root cause.

## Edge Cases

- **Cannot reproduce**: Document the investigation path, which hypotheses you tested,
  and why reproduction failed. Create the issue anyway -- partial diagnosis beats silence.

- **Multiple root causes**: If investigation reveals distinct independent causes,
  create separate issues for each. Cross-reference them in each issue body.

- **Fix requires design change**: If the root cause stems from flawed design requiring
  architectural rework, note this in the issue and suggest using the improve-architecture
  skill.
```

---

## Change Log vs Previous Synthesis

| Change | Citation | Rationale |
|--------|----------|-----------|
| Description rewritten: third-person active, compressed triggers, front-loaded within 250 chars | D3 R10 "passive obscures agent"; plugin-dev-ecosystem 1.2 "third person"; compression-strategies 7.2 "truncated at 250 chars" | Was passive "This skill should be used when..."; now active third-person. |
| "full autonomous exploration" -> "autonomous exploration" | D3 R13 "'full' is needless intensifier" | Drop intensifier. |
| "all the evidence" -> "the evidence" | D3 R13 "'all' overstates" | Drop. |
| "Launch a deep investigation" -> "Investigate the codebase" | D3 R13 "'deep' is vague intensifier" | Checklist defines depth. |
| "Based on investigation, determine:" -> "From your investigation, determine:" | D3 R10 active voice | Strengthens agency. |
| "Rules for the fix plan:" -> "Fix plan rules:" | D3 R13 | More direct. |
| "with the structure below" -> "with this structure" | D3 R13 "'below' is needless direction" | Direct reference. |
| "Describe the investigation findings:" -> "Describe your investigation:" | D3 R13 "'findings' redundant" | Cut. |
| Merged "Do NOT include file paths..." + standalone sentence | D3 R13 "adds no new information" | Single merged sentence. |
| "partial diagnosis is more valuable than no documentation" -> "partial diagnosis beats silence" | D3 R11 "negative construction" | Positive, concrete. |
| "for the design phase" -> dropped | D3 R13 "needless qualifier" | Obvious from context. |
| Attribution footer -> removed (to ATTRIBUTION file) | Context cost | No operational value in context. |
| AC checkboxes fixed to parallel active voice | D3 R15 "Mixed voice and form breaks parallel structure" | All active voice now. |
| Phase headers and constructions activated | D3 R10 severe passives | Multiple passive-to-active conversions. |
| "Why Autonomous" -> "Why Investigate Autonomously" | D3 R12 "Autonomous is abstract adjective used as noun" | Verb form more concrete. |
| Preserved: "Do NOT ask follow-up questions" | D2 core point 1 | Load-bearing binary prohibition. |
| Preserved: "Publish directly" constraint | D2 core point 5 | Load-bearing binary prohibition. |
| Preserved: "Never batch all tests..." | D2 core point 4 | Load-bearing TDD cycle constraint. |

---

## Projected Token Delta

| Category | Tokens |
|----------|--------|
| Baseline | 1283 |
| Strunk compression + restructure | -90 |
| D4 fixes (parallel AC, active voice) | net 0 |
| **Projected** | **~1193** |
| **Net reduction** | **~90 tokens (7.0%)** |

No references to inline. Unit is already lean. Gains from eliminating wordiness and fixing voice.
