---
name: dev-orchestration
description: |
  Extension of agentic-delegation for the software development lifecycle.
  Adds the Plan→Implement→Review→Fix loop, dev-discipline agent orchestration,
  TDD gates, status-driven branching, and debugging escalation.

  Prerequisite: agentic-delegation (same plugin — must be read first).
  Hard preference: dev-discipline plugin (implementer, spec-reviewer, code-quality-reviewer agents).

  Triggers: "implement a feature end-to-end", "execute an implementation plan",
  "build this with agents", "orchestrate development", "run the dev loop",
  "implement using subagents", "dispatch implementers", "coordinate implementation and review".
---

# Dev Orchestration

Extends agentic-delegation with the development lifecycle. The parent skill establishes the economics, model ladder, decomposition patterns, prompt anatomy, execution patterns, and quality governance. This skill adds the Plan→Implement→Review→Fix loop that governs how those patterns apply to writing software.

**Read agentic-delegation's SKILL.md before proceeding.** This is a hard gate, not a suggestion. The instructions below assume the parent's framework is fully internalized.

## Dependencies

### agentic-delegation (same plugin — always present)

The parent skill. Provides: model ladder (haiku-first with upgrade-on-failure), decomposition patterns (by entity, by aspect, by concern), prompt anatomy (9-section template), execution patterns (parallel fan-out, sequential pipeline, map-reduce), quality governance (re-launch principle, contradiction resolution, concurrent file write prevention, independent verification), and session persistence (ARRIVE/WORK/LEAVE lifecycle for multi-session work).

This skill uses all of the above. None are restated here. For multi-session dev projects, the parent's session persistence protocol applies directly — the `conventions.md` document holds dev-specific rules (forbidden patterns, test philosophy, review protocol), `codebase_state.md` holds the module inventory, and `deferred_items.md` tracks unresolved review findings.

### dev-discipline (separate plugin — hard preference)

Provides three agents purpose-built for this workflow:
- **implementer** — executes tasks from plans, follows TDD, self-reviews, reports structured status (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED)
- **spec-reviewer** — adversarially verifies implementation matches spec, reports PASS / FAIL with file:line references
- **code-quality-reviewer** — audits code quality after spec compliance passes, gives merge verdict (Yes / With fixes / No)

If dev-discipline is not installed, recommend installing it. If that isn't happening immediately, construct equivalent agent prompts — @references/agent-dispatch.md describes the context each agent type needs.

dev-discipline also provides skills referenced below: **defensive-planning**, **tdd**, **systematic-debugging**, **receiving-code-review**. Same preference pattern applies.

## The Development Loop

```
Plan → Implement → Review → Fix (if needed) → Done
```

The orchestrator drives this loop. Each phase has entry/exit criteria and agent dispatch patterns. Skipping phases produces spec drift, quality regression, or wasted effort.

Apply the full loop for any task touching behavior-carrying code: new features, bug fixes, refactors, migrations. Scale to task size — a one-function change uses a lightweight pass; a multi-file feature uses full decomposition and parallel dispatch.

For tasks under ~10 lines of trivially obvious changes, execute directly without agent dispatch.

For the complete state machine with entry/exit criteria and loop limits, see @references/lifecycle-loops.md.

## Phase 1: Plan

Decompose the work into implementation units before touching code.

Use defensive-planning to produce the implementation plan with verification gates, forbidden patterns, and exhaustive field lists.

### Dev-Specific Decomposition

The parent's decomposition patterns (by entity, by aspect, by concern) apply. For dev tasks, the natural unit is measured in files and testable behaviors:

- Touches 1-3 files
- Produces independently testable behavior
- Can be described in a self-contained brief (no "see previous task" references)
- Takes an implementer agent 2-10 minutes

Units touching 5+ files signal insufficient decomposition. Split further.

### Ordering

Build foundational units first (data models, interfaces), then dependent units (logic, integration), then verification units (integration tests, end-to-end checks). Use the parent's sequential pipeline pattern for dependent units.

## Phase 2: Implement

Dispatch one agent per implementation unit. Never implement in orchestrator context.

### Dispatch

For each unit, construct a brief containing:
1. The task specification with exact code expectations
2. File paths to read for context
3. TDD requirements (if applicable)
4. Scope boundaries (what to build, what NOT to build)

Dispatch the **implementer** agent with this brief. Default model: sonnet — the parent's Implementation archetype already derives this ("requires reasoning about system constraints"). Upgrade only if an agent reports BLOCKED citing reasoning limitations.

For dispatch details, context requirements, and re-dispatch patterns, see @references/agent-dispatch.md.

### TDD Gate

Require TDD for all behavior-carrying code. Each unit follows the red-green-refactor cycle with vertical slicing (one test at a time, not all tests first). Use tdd for discipline.

TDD checkpoints map to the loop:
- RED: test written and failing (unit in-progress)
- GREEN: minimal implementation passes (unit ready for review)
- REFACTOR: cleanup after review passes (unit complete)

### Sequencing

Dispatch independent units in parallel — the default per the parent. Sequential only when a unit requires another's output.

```
Dispatch units A, B, C in parallel (independent)
  → all report DONE
Dispatch unit D (depends on A and B)
  → reports DONE
Dispatch integration verification agent
  → reports PASS or issues
```

### Commit Discipline

Agents commit their own work with descriptive messages. If fixes are needed, dispatch a fix agent — the orchestrator does not edit code, does not commit code, does not debug code.

One logical change per commit. Fix commits reference what they fix. No history rewriting (no rebase, no amend, no force push).

### Verification After Each Agent

Run the test suite and type checker after every implementer reports DONE. Agent self-reports are unreliable for cross-module integration — an agent may report DONE while its changes break tests in modules it didn't touch.

This is the dev-specific application of the parent's governing principle #12: verify independently, trust artifacts not claims.

## Phase 3: Review

Two-stage review after each unit. Order is mandatory: spec compliance first, code quality second. Reviewing quality before confirming spec compliance wastes effort on code that may not meet requirements.

The two-stage review with loop limits is the quality governance for dev work. It subsumes the parent's general quality patterns (re-launch, spot-checking) in this context.

### Stage 1: Spec Compliance

Dispatch the **spec-reviewer** with the task specification and changed file list. It reads actual code and compares to requirements line by line, with adversarial posture.

### Stage 2: Code Quality

Only after spec compliance passes. Dispatch the **code-quality-reviewer** with the git diff range. It evaluates quality, testing adequacy, and architecture, categorizes findings by severity, and gives a merge verdict.

### Review Failure

When either reviewer reports issues:
1. Dispatch the implementer (or a fix agent) with the specific findings.
2. After fixes, re-dispatch the same reviewer.
3. Repeat until approved. Never skip re-review.

Apply receiving-code-review's verify-before-implement discipline and YAGNI enforcement when processing findings.

After 3 review-fix cycles without PASS, stop. The problem is structural — see @references/lifecycle-loops.md for escalation protocol.

## Phase 4: Status-Driven Branching

Interpret implementer status and route:

| Status | Route |
|---|---|
| DONE | Dispatch spec-reviewer |
| DONE_WITH_CONCERNS | Delegate concern classification to an agent. Correctness/scope → address before review. Observational → note and proceed. |
| NEEDS_CONTEXT | Identify missing information. Provide it. Re-dispatch. |
| BLOCKED | Delegate root cause diagnosis. See escalation below. |

The orchestrator reads status codes from completion summaries. Any analysis beyond the code itself — classifying concerns, diagnosing blockers — is delegated.

### BLOCKED Escalation

Dispatch a diagnosis agent to determine the cause:

1. **Missing context** — provide the missing information, re-dispatch implementer.
2. **Insufficient reasoning** — re-dispatch with a more capable model.
3. **Task too large** — decompose further, dispatch sub-units.
4. **Plan defect** — the plan's assumptions are wrong. Escalate to the user.

Never force retry without changing inputs.

## Debugging Escalation

When implementation produces unexpected failures (tests fail for unclear reasons, behavior deviates from spec without obvious cause):

Apply systematic-debugging's 4-phase root cause protocol: investigate before fixing, trace data flow, form hypotheses, test minimally.

For multi-hypothesis investigation, apply the parent's speculative-parallel pattern: dispatch parallel agents each investigating one hypothesis independently. Compare their evidence. This is faster than sequential investigation and catches the root cause more reliably.

### When to Enter

- Implementer reports BLOCKED due to unrelated test failures
- Review reveals behavior contradicting spec but implementation looks correct
- A fix creates new failures elsewhere (architectural coupling signal)
- 3+ fix attempts on the same issue without resolution

## Multi-Unit Integration

After all units pass individual review:

1. Run the full test suite (not just unit-level tests).
2. Dispatch an integration verification agent to check interface compatibility between units (types, signatures, data contracts) and end-to-end behavior against the original spec.
3. If issues arise, determine which unit is at fault and re-enter the implement-review loop for that unit only.

### Cross-Cutting Review

For multi-unit features, dispatch a cross-cutting review after integration passes. Decompose by CONCERN, not by module. Module-scoped reviews repeat shallow checks. Concern-scoped reviews find cross-cutting bugs.

| Concern | What it catches |
|---------|-----------------|
| Spec fidelity | Missing features, spec drift, scope creep |
| Data flow integrity | Schema drift, silent data loss, interface mismatches |
| Simplicity | Unnecessary complexity, tangled concerns |
| DRY/YAGNI | Duplicated knowledge, unused features |

Fan out one agent per concern — this is the parent's fan-out-by-concern pattern applied to dev review.

### Test Quality Audit

After the test suite stabilizes, classify every test:

| Classification | Action |
|----------------|--------|
| VALUABLE | Tests a specific behavior that could regress. Asserts a property, not a value. Keep. |
| SMOKE | Verifies code runs without crashing. Low value but cheap. Keep only if truly cheap. |
| TAUTOLOGICAL | Asserts defaults equal hardcoded copies, or tests library guarantees. Delete. |
| MISSING | A test that should exist. Prioritize by risk of the bug it would catch. Add. |

Theatrical test coverage is worse than low coverage — it creates false confidence. Delete tautological tests and add missing critical ones.

## Anti-Patterns

**Code in orchestrator context.** The orchestrator dispatches and decides. It does not write code, read implementation files, or debug test failures.

**Skipping spec review.** Implementer self-review is not spec compliance. Adversarial spec review catches drift, missing requirements, and scope creep.

**Reviewing quality before spec compliance.** Polishing code that doesn't meet requirements is wasted work.

**Batch-fixing review findings.** Fix one issue, test, commit, repeat. All-at-once creates compound failures.

**Ignoring DONE_WITH_CONCERNS.** Correctness or scope concerns must be addressed before review.

**Theatrical test coverage.** Tests that assert defaults equal hardcoded copies or test library guarantees provide zero protection. They create false confidence. Delete them and add tests for actual risk areas.

**Module-scoped cross-cutting reviews.** Reviewing each module independently misses cross-module issues (data flow bugs, interface mismatches, duplicated knowledge). Decompose final reviews by concern, not by module.

## References

- @references/lifecycle-loops.md — State machine, entry/exit criteria, loop limits, multi-unit coordination
- @references/agent-dispatch.md — Context requirements, status interpretation, re-dispatch patterns, parallel coordination
- @references/domain-context-examples.md — Domain-specific examples for constructing agent context briefs
