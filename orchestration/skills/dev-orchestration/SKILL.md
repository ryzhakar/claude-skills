---
name: dev-orchestration
version: 1.0.0
description: |
  This skill should be used when the user asks to "implement a feature end-to-end",
  "execute an implementation plan", "build this with agents", "orchestrate development",
  "run the dev loop", "implement using subagents", "dispatch implementers",
  "coordinate implementation and review", or when a multi-step development task
  requires planning, implementation, review, and iteration as a coordinated workflow.

  Governs the full plan-implement-review-fix development lifecycle by orchestrating
  dev-discipline agents (implementer, spec-reviewer, code-quality-reviewer) and skills
  (defensive-planning, tdd, systematic-debugging, receiving-code-review) into a
  coherent execution workflow with quality gates and status-driven branching.
---

# Dev Orchestration

Govern the full development lifecycle as a coordinated agent workflow. The orchestrator decomposes work, dispatches implementers, triggers reviewers, interprets status, and decides when to loop back versus declare done. Implementation happens in agents. The orchestrator's context is for decisions, dispatch, and detection -- not for writing code.

## Core Loop

Every development task follows one loop:

```
Plan --> Implement --> Review --> Fix (if needed) --> Done
```

The orchestrator drives this loop. Each phase has specific entry/exit criteria, agent dispatch patterns, and escalation protocols. Skipping phases produces spec drift, quality regression, or wasted effort.

### When the Loop Applies

Apply the full loop for any task touching behavior-carrying code: new features, bug fixes, refactors, migrations. Scale the loop to task size -- a one-function change uses a lightweight pass through each phase; a multi-file feature uses the full machinery with decomposition and parallel dispatch.

For tasks under ~10 lines of trivially obvious changes, execute directly without agent dispatch. Everything else goes through the loop.

## Phase 1: Plan

Decompose the work into implementation units before touching code.

If the defensive-planning skill is available, use it to produce the implementation plan with verification gates, forbidden patterns, and exhaustive field lists. Otherwise, create a plan that specifies: (1) exact files to create or modify, (2) exact behavior each unit must produce, (3) verification commands with expected output, (4) explicit ordering and dependencies between units.

### Decomposition Heuristic

Break features into units where each unit:
- Touches 1-3 files
- Produces independently testable behavior
- Can be described in a self-contained brief (no "see previous task" references)
- Takes an implementer agent 2-10 minutes

Units that touch 5+ files or require cross-cutting coordination signal insufficient decomposition. Split further.

### Ordering

Identify dependencies between units. Build foundational units first (data models, interfaces), then dependent units (logic, integration), then verification units (integration tests, end-to-end checks).

If the agentic-delegation skill is available, apply its decomposition patterns (by entity, by aspect, by concern) and its sequential pipeline pattern for dependent units. Otherwise, map dependencies manually: list each unit's inputs and outputs, topologically sort, and group independent units for parallel dispatch.

## Phase 2: Implement

Dispatch one agent per implementation unit. Never implement in orchestrator context -- agents get fresh context and produce focused work.

### Dispatch

For each unit, construct a brief containing: (1) the task specification with exact code expectations, (2) file paths to read for context, (3) TDD requirements if applicable, (4) scope boundaries (what to build, what NOT to build).

If the dev-discipline implementer agent is available, dispatch it with the task brief. It follows TDD when specified, self-reviews, and reports structured status. Otherwise, launch a sonnet agent with the implementation brief directly, instructing it to: implement the specified behavior, write tests, commit, and report status as DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.

### TDD Gate

If the tdd skill is available, require TDD mode for all behavior-carrying code: each unit follows the red-green-refactor cycle with vertical slicing (one test at a time, not all tests first). Otherwise, require that tests exist for every unit and that tests verify behavior through public interfaces, not implementation details.

TDD checkpoints map to the orchestration loop:
- RED: test written and failing (unit is in-progress)
- GREEN: minimal implementation passes (unit ready for review)
- REFACTOR: cleanup after review passes (unit complete)

### Sequencing

Dispatch independent units in parallel when possible. Sequential dispatch only when a unit requires another's output (interface definitions, shared types, generated code).

For multi-unit features, the pattern is:

```
Dispatch units A, B, C in parallel (independent)
   --> all report DONE
Dispatch unit D (depends on A and B)
   --> reports DONE
Dispatch integration verification agent
   --> reports PASS or issues
```

For detailed dispatch mechanics including prompt templates and context requirements, see @references/agent-dispatch.md -- it covers implementer, spec-reviewer, and code-quality-reviewer dispatch patterns with fallbacks.

## Phase 3: Review

Apply two-stage review after each unit implementation. The order is mandatory: spec compliance first, code quality second. Reviewing quality before confirming spec compliance wastes effort on code that may not meet requirements.

### Stage 1: Spec Compliance

If the dev-discipline spec-reviewer agent is available, dispatch it with the task specification and the list of changed files. It reads actual code and compares to requirements line by line, with adversarial posture. Otherwise, launch a sonnet agent instructed to: read the spec, read every changed file, verify each requirement has corresponding implementation, identify missing/extra/misinterpreted requirements, and report PASS or FAIL with file:line references.

### Stage 2: Code Quality

Only after spec compliance passes. If the dev-discipline code-quality-reviewer agent is available, dispatch it with the git diff range. Otherwise, launch a sonnet agent instructed to: read changed files, evaluate code quality / testing adequacy / architecture soundness, categorize findings as Critical / Important / Minor, and give a merge verdict.

### Review Failure

When either reviewer reports issues:
1. Dispatch the implementer agent (or a fix agent) with the specific findings.
2. After fixes, re-dispatch the same reviewer.
3. Repeat until approved.
4. Never skip re-review. Never accept "close enough."

If the receiving-code-review skill is available, apply its verify-before-implement discipline and YAGNI enforcement when processing review findings. Otherwise, process findings individually: blocking issues first, then simple fixes, then complex fixes, testing each fix independently.

## Phase 4: Status-Driven Branching

Interpret implementer status reports and branch accordingly:

| Status | Action |
|---|---|
| DONE | Proceed to spec review |
| DONE_WITH_CONCERNS | Read concerns. Correctness/scope concerns: address before review. Observational concerns: note and proceed. |
| NEEDS_CONTEXT | Identify missing information. Provide it. Re-dispatch. |
| BLOCKED | Assess root cause (see below). |

### BLOCKED Escalation

When an implementer reports BLOCKED, determine the cause:

1. **Missing context** -- provide the missing information, re-dispatch same agent.
2. **Insufficient reasoning** -- re-dispatch with a more capable model.
3. **Task too large** -- decompose the unit further, dispatch sub-units.
4. **Plan defect** -- the plan's assumptions are wrong. Stop. Escalate to the user.

Never force retry without changing inputs. If the agent is stuck, something about the brief, context, or decomposition must change.

For the full lifecycle state machine with entry/exit criteria and loop limits, see @references/lifecycle-loops.md -- it covers the outer development loop, inner review loop, debugging escalation, and multi-unit coordination.

## Debugging Escalation

When implementation produces unexpected failures (tests fail for unclear reasons, behavior deviates from spec without obvious cause):

If the systematic-debugging skill is available, apply its 4-phase root cause protocol: investigate before fixing, trace data flow, form hypotheses, test minimally. Otherwise, follow this sequence: (1) read error messages completely, (2) check recent changes, (3) form one specific hypothesis, (4) test with the smallest possible change.

For multi-hypothesis investigation, dispatch parallel agents each investigating one hypothesis independently. Compare their evidence. This is faster than sequential investigation and catches the root cause more reliably.

### When to Escalate to Debugging

- Implementer reports BLOCKED due to test failures unrelated to its changes
- Review reveals behavior that contradicts the spec but the implementation looks correct
- A fix creates new failures elsewhere (symptom of architectural coupling)
- 3+ fix attempts on the same issue without resolution (triggers the systematic-debugging architectural questioning threshold)

## Multi-Unit Integration

After all units pass individual review, verify they work together:

1. Run the full test suite (not just unit-level tests).
2. Check interface compatibility between units (types, method signatures, data contracts).
3. Verify end-to-end behavior matches the original feature specification.

Dispatch an integration verification agent for step 2-3. If issues arise, determine which unit's implementation is at fault and re-enter the implement-review loop for that unit only.

## Anti-Patterns

**Code in orchestrator context.** The orchestrator dispatches and decides. It does not write code, read implementation files, or debug test failures. All of that happens in agents.

**Skipping spec review.** "The implementer self-reviewed" is not spec compliance. Self-review catches obvious errors; adversarial spec review catches spec drift, missing requirements, and scope creep.

**Reviewing quality before spec compliance.** Polishing code that does not meet requirements is wasted work. Always spec first, quality second.

**Batch-fixing review findings.** Applying all fixes at once without individual testing creates compound failures. Fix one issue, test, commit, repeat.

**Ignoring DONE_WITH_CONCERNS.** Concerns about correctness or scope must be addressed before review. Ignoring them and hoping the reviewer catches problems wastes a review cycle.

## References

- @references/lifecycle-loops.md -- Full state machine for the development loop, review loop, debugging escalation, multi-unit coordination, entry/exit criteria, and loop limits
- @references/agent-dispatch.md -- Prompt templates for dispatching implementer, spec-reviewer, and code-quality-reviewer agents, context requirements, status interpretation, and fallback patterns
- @references/software-engineering-examples.md -- Concrete delegation archetypes for code implementation, code review/audit, debugging, testing, and documentation workflows
