# Plan Execution Protocol

Methodology for executing an implementation plan once it has been written. Covers the gate between plan creation and implementation, blocker handling, task state tracking, and review sequencing.

## Pre-Execution Review Gate

Before starting any implementation work, critically review the plan:

1. Read the plan completely.
2. Identify questions, concerns, or gaps.
3. If concerns exist: raise them with the user BEFORE starting implementation.
4. If no concerns: proceed to execution.

This catches plan defects before implementation begins. A plan that looked good during writing may reveal gaps when read from an executor's perspective.

## Task State Tracking

Track each task through a simple state machine:

```
not_started -> in_progress -> completed
                          \-> blocked
```

Use markdown checkboxes as the tracking mechanism:

```markdown
- [ ] Task 1: Component setup          # not_started
- [x] Task 2: Core implementation      # completed
- [ ] Task 3: Integration (BLOCKED)    # blocked -- note reason inline
```

Mark a task `in_progress` before executing its steps. Mark `completed` only after all verification gates pass. Mark `blocked` with a reason if unable to proceed.

## Blocker Escalation Protocol

STOP executing immediately when:

- Hit a blocker (missing dependency, test failure that contradicts plan, instruction unclear)
- Plan has critical gaps preventing correct implementation
- An instruction is ambiguous and guessing risks wrong work
- A verification gate fails repeatedly (2+ attempts)

**Ask for clarification rather than guessing.** Bad work created from assumptions costs more to fix than the delay of asking.

When stopped, report:
- Which task is blocked
- What specifically is unclear or failing
- What was attempted
- What information or decision is needed to proceed

## Phase Revisit Criteria

Return to plan review when:
- The user updates the plan based on feedback
- Implementation reveals the fundamental approach needs rethinking
- A blocker suggests the plan's assumptions are wrong

Do not force through blockers. If the plan is wrong, fixing the plan is faster than implementing the wrong thing and then correcting it.

## Two-Stage Review Ordering

After each task implementation, apply reviews in this specific order:

**Stage 1: Spec Compliance Review**
- Verify the implementation matches the specification.
- Check: all requirements implemented, nothing missing, nothing extra.
- Compare actual code to requirements line by line.
- Do not trust the implementer's self-report -- read the code.

**Stage 2: Code Quality Review (only after Stage 1 passes)**
- Verify the implementation is well-built.
- Check: code quality, testing adequacy, architecture soundness.
- Categorize findings by severity: Critical / Important / Minor.

This ordering matters. Reviewing code quality before confirming spec compliance wastes effort -- polishing code that does not meet requirements is wasted work. Spec drift is a software-specific failure mode where implementation gradually diverges from requirements through small reinterpretations.

## Status-Driven Branching

When an implementer reports status, handle accordingly:

| Status | Action |
|---|---|
| DONE | Proceed to spec compliance review |
| DONE_WITH_CONCERNS | Read concerns first. If about correctness/scope: address before review. If observations: note and proceed to review. |
| NEEDS_CONTEXT | Provide missing context and re-dispatch |
| BLOCKED | Assess: context problem (provide more), reasoning problem (use more capable model), task too large (decompose), plan wrong (escalate to user) |

Never ignore an escalation or force retry without changes. If an implementer reports being stuck, something about the inputs must change.

## Composability

If the agentic-delegation skill is available, apply its Model Ladder for selecting implementer and reviewer model tiers, and its quality governance patterns for detecting bad agent output. Otherwise, prefer the cheapest available model for mechanical implementation tasks (isolated functions, 1-2 files, complete spec) and the most capable model for review and design tasks.
