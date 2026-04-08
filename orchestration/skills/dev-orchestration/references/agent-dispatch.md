# Agent Dispatch

Context requirements, status interpretation, and coordination patterns for dispatching dev-discipline agents. If dev-discipline is not installed, construct equivalent agent prompts using the context requirements below and the parent skill's prompt anatomy (9-section template).

## Implementer

### When to Dispatch

Dispatch for each implementation unit that:
- Has a concrete specification (files, behavior, verification)
- Is scoped to 1-3 files
- Can be independently tested

Do NOT dispatch for:
- Tasks requiring architectural judgment (orchestrator decides, then dispatches)
- Exploratory investigation (use investigation agents)
- Tasks under ~10 lines of trivially obvious changes (execute directly)

### Context Requirements

Every implementer dispatch must include:

1. **Task specification** — the exact unit from the implementation plan, including code expectations and verification commands.
2. **File paths** — absolute paths to files the agent must read (existing interfaces, types, related modules). Only what is necessary.
3. **TDD flag** — whether this unit requires test-driven development.
4. **Scope boundaries** — explicit DO and DO NOT lists.
5. **Scene-setting context** — 2-3 sentences on where this unit fits. Agents without situational awareness produce architecturally disconnected code.

### Model Selection

The parent's model ladder prescribes sonnet for implementation ("requires reasoning about system constraints"). Upgrade only on observed BLOCKED citing reasoning limitations.

## Spec-Reviewer

### When to Dispatch

Immediately after an implementer reports DONE or DONE_WITH_CONCERNS (with concerns addressed). Never skip.

Dispatch order: spec review BEFORE quality review. Always.

### Context Requirements

1. **Task specification** — the same spec the implementer received.
2. **Changed files** — list of files the implementer modified or created.

The implementer's status report may be provided as context but is not trusted evidence. The reviewer reads actual code. This is a sequential pipeline stage — the reviewer's job is to check the implementer's work — so providing the report does not violate the parent's isolation principle (which governs parallel independent evaluation).

## Code-Quality-Reviewer

### When to Dispatch

ONLY after spec review passes.

### Context Requirements

1. **Git diff range** — BASE_SHA and HEAD_SHA bounding the changes.
2. **Changed file list** — for the reviewer to read.
3. **Quality standards** — project-specific coding standards, if they exist.

## Status Interpretation

```
DONE
  → Dispatch spec-reviewer

DONE_WITH_CONCERNS
  → Delegate concern classification
  → Correctness/scope concern?
      YES → Address (clarify spec, adjust scope, re-dispatch)
      NO  → Note, dispatch spec-reviewer

NEEDS_CONTEXT
  → What is missing?
      → File content → Provide paths, re-dispatch
      → Domain knowledge → Provide explanation, re-dispatch
      → Architectural decision → Make decision, update spec, re-dispatch
      → User input required → Ask user, then re-dispatch

BLOCKED
  → Delegate diagnosis
      → Missing dependency → Provide, re-dispatch
      → Task too complex for model → Re-dispatch with more capable model
      → Task too large → Decompose into sub-units
      → Plan assumption wrong → Return to planning phase
      → Unknown → Dispatch investigation agents
```

## Re-Dispatch Patterns

### After NEEDS_CONTEXT

Construct a new dispatch with the original brief plus missing context. Rewrite the relevant section inline — the agent should not piece together context from multiple messages.

### After BLOCKED (model upgrade)

Same task specification, more capable model. Do not modify the spec.

### After Review Failure

Dispatch a fix agent with:
1. The original task specification (reference)
2. The reviewer's specific findings (the FAIL report)
3. Instructions to fix ONLY the identified issues, test each individually, and report status

Scope the fix to the specific findings.

## Parallel Dispatch Coordination

When dispatching multiple implementers in parallel:

1. **Verify independence.** No two agents may write to the same file. If they do, make them sequential.
2. **Provide isolation context.** Each agent's brief mentions which other units exist and which files they own, preventing out-of-scope modifications.
3. **Stagger reviews.** As implementers complete, dispatch their reviews immediately. Do not wait for all to finish.
4. **Track status.** Maintain the orchestration status table (see lifecycle-loops.md).

### Handling Parallel Conflicts

If two parallel agents produce conflicting changes:
1. Identify which agent's output matches the spec.
2. Keep that output.
3. Re-dispatch the other with updated context.
