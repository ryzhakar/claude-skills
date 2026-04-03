# Agent Dispatch

Prompt templates, context requirements, and status interpretation for dispatching development agents. Each section covers what to send, when to dispatch, how to interpret results, and what to do when the preferred agent is unavailable.

## Implementer Dispatch

### When to Dispatch

Dispatch an implementer agent for each implementation unit that:
- Has a concrete specification (files, behavior, verification)
- Is scoped to 1-3 files
- Can be independently tested
- Does not require orchestrator-level decisions

Do NOT dispatch an implementer for:
- Tasks requiring architectural judgment (orchestrator decides, then dispatches)
- Exploratory investigation (use investigation agents instead)
- Tasks under ~10 lines of trivially obvious changes (execute directly)

### Context Requirements

Every implementer dispatch must include:

1. **Task specification** -- the exact unit from the implementation plan, including code expectations and verification commands.
2. **File paths** -- absolute paths to files the agent must read for context (existing interfaces, types, related modules). List only what is necessary; excessive context causes drift.
3. **TDD flag** -- whether this unit requires test-driven development. If yes, the agent writes tests first.
4. **Scope boundaries** -- explicit DO and DO NOT lists. What to build, what to leave alone, what patterns to follow, what patterns are forbidden.
5. **Scene-setting context** -- 2-3 sentences explaining where this unit fits in the larger feature. Agents with no situational awareness produce technically correct but architecturally disconnected code.

### Prompt Template

If the dev-discipline implementer agent is available, dispatch it with the task brief as the agent message. The agent's system prompt already covers TDD discipline, self-review, and status reporting.

Otherwise, construct the agent prompt directly:

```
Implement the following task. Follow TDD if specified. Report status when complete.

## Task
{task_specification}

## Context Files
Read these files for context before implementing:
{list of absolute file paths}

## TDD Required: {yes/no}
{If yes: Write the failing test first. Verify it fails. Implement minimally. Verify it passes. Commit.}

## Scope
DO:
- {what to build}
- {patterns to follow}
- {conventions from the codebase}

DO NOT:
- {what not to touch}
- {patterns to avoid}
- {scope boundaries}

## Report Format
When complete, report:
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
What was implemented: [description]
Tests: [what was tested and results]
Files changed: [list]
Concerns: [if any]
```

### Model Selection

If the agentic-delegation skill is available, apply its Model Ladder: start with the cheapest capable model, upgrade on observed failure.

Otherwise, use this heuristic:

| Task Characteristics | Model Tier |
|---|---|
| 1-2 files, complete spec, mechanical changes | Cheapest available (haiku-class) |
| Multi-file coordination, pattern matching | Mid-tier (sonnet-class) |
| Design judgment, broad codebase understanding | Most capable available |

**Upgrade trigger:** Agent reports BLOCKED or produces clearly incorrect output. Do not debug the output -- re-dispatch with a more capable model.

## Spec-Reviewer Dispatch

### When to Dispatch

Dispatch a spec-reviewer immediately after an implementer reports DONE or DONE_WITH_CONCERNS (with concerns addressed). Never skip this step.

Dispatch order: spec review BEFORE quality review. Always.

### Context Requirements

1. **Task specification** -- the same spec the implementer received.
2. **Implementer report** -- the status report (for context, not as trusted evidence).
3. **Changed files** -- list of files the implementer modified or created. The reviewer reads these directly.

### Prompt Template

If the dev-discipline spec-reviewer agent is available, dispatch it with the specification and changed file list.

Otherwise:

```
Verify that the implementation matches the specification. Read actual code -- do not trust the implementer's report.

## Specification
{task_specification}

## Implementer Report (context only -- do not trust)
{implementer_status_report}

## Files to Review
Read these files and compare to the specification line by line:
{list of changed files}

## Verification Process
1. Read the specification completely.
2. Read each changed file.
3. For each requirement: find the implementing code, verify it fulfills the requirement.
4. Report any requirements that are: missing, partial, misinterpreted, or extra (not in spec).

## Output
If compliant:
  PASS -- Spec compliant. All [N] requirements verified in code.

If issues found:
  FAIL -- Issues found:
  Missing: [requirement] -- not implemented
  Partial: [requirement] -- [what exists] but [what is missing]
  Extra: [file:line] -- [feature] not requested
  Misinterpreted: [requirement] -- built [X] but spec requires [Y]

Include file:line references for every finding.
```

### Interpreting Results

**PASS:** Proceed to quality review.

**FAIL:** Dispatch the implementer (or a fix agent) with the specific findings. After fixes, re-dispatch the spec-reviewer. The re-review scope narrows to the previously failing items plus a check that fixes did not break passing items.

## Code-Quality-Reviewer Dispatch

### When to Dispatch

Dispatch ONLY after spec review passes. Never before.

### Context Requirements

1. **Git diff range** -- the BASE_SHA and HEAD_SHA bounding the implementation's changes.
2. **Changed file list** -- for the reviewer to read.
3. **Quality standards** -- any project-specific coding standards, if they exist. Otherwise, the reviewer applies general production-readiness criteria.

### Prompt Template

If the dev-discipline code-quality-reviewer agent is available, dispatch it with the git diff range.

Otherwise:

```
Review the following code changes for production readiness. Review ONLY what changed -- not the entire codebase.

## Scope
Git diff range: {BASE_SHA}..{HEAD_SHA}
Changed files:
{list of changed files}

## Quality Checklist
Evaluate:
- Code quality (readability, maintainability, error handling, DRY)
- Testing adequacy (behavior-based tests, edge cases, test quality)
- Architecture (separation of concerns, file responsibility, design soundness)
- Production readiness (no secrets, backward compatibility, performance)

## Severity Categories
Critical (must fix): Bugs, security issues, data loss risks
Important (should fix): Architecture problems, test gaps, missing error handling
Minor (nice to have): Style, optimization, documentation

## Output
Summary: [2-3 sentence overview]
Strengths: [specific positives with file:line]
Critical Issues: [if any, with file:line and fix recommendation]
Important Issues: [if any, with file:line and fix recommendation]
Minor Issues: [if any]
Assessment: Ready to merge: Yes / With fixes / No
```

### Interpreting Results

**Ready to merge: Yes** -- unit is complete. Mark as done.

**Ready to merge: With fixes** -- dispatch fix agent with Important and Critical findings. Re-dispatch quality reviewer after fixes.

**Ready to merge: No** -- significant issues. Dispatch fix agent with all Critical findings. After fixes, re-dispatch quality reviewer for full review.

## Status Interpretation Decision Tree

When an implementer agent reports status, follow this decision tree:

```
DONE
  --> Dispatch spec-reviewer

DONE_WITH_CONCERNS
  --> Read concerns
  --> Is the concern about correctness or scope?
      YES --> Address concern (clarify spec, adjust scope, re-dispatch)
      NO  --> Note concern for future reference, dispatch spec-reviewer

NEEDS_CONTEXT
  --> What is missing?
      --> Specific file content --> Provide file paths, re-dispatch
      --> Domain knowledge --> Provide explanation, re-dispatch
      --> Architectural decision --> Make decision, update spec, re-dispatch
      --> User input required --> Ask user, then re-dispatch

BLOCKED
  --> What is the blocker?
      --> Missing dependency --> Install/provide dependency, re-dispatch
      --> Test infrastructure issue --> Fix infrastructure, re-dispatch
      --> Task too complex for model --> Re-dispatch with more capable model
      --> Task too large --> Decompose into sub-units, dispatch each
      --> Plan assumption wrong --> Return to planning phase
      --> Environmental issue --> Investigate, fix, re-dispatch
      --> Unknown --> Dispatch investigation agent(s) to diagnose
```

## Re-Dispatch Patterns

### After NEEDS_CONTEXT

Construct a new dispatch with the original brief plus the missing context. Do not append -- rewrite the relevant section to include the new information inline. The agent should not need to piece together context from multiple messages.

### After BLOCKED (model upgrade)

Re-dispatch the same task specification to a more capable model. Do not modify the spec -- the task is the same, only the executor changes.

### After Review Failure

Dispatch a fix agent (or the same implementer) with:
1. The original task specification (for reference)
2. The reviewer's specific findings (copy the FAIL report)
3. Instructions to fix ONLY the identified issues, test each fix individually, and report status

Do not include the full review context. Scope the fix agent to the specific findings.

## Parallel Dispatch Coordination

When dispatching multiple implementer agents in parallel:

1. **Verify independence.** No two agents may write to the same file. If they do, make them sequential.
2. **Provide isolation context.** Each agent's brief mentions which other units exist and which files they own. This prevents agents from "helpfully" modifying files outside their scope.
3. **Stagger reviews.** As implementers complete, dispatch their reviews immediately. Do not wait for all implementers to finish before starting any reviews.
4. **Track status centrally.** Maintain the orchestration status table (see lifecycle-loops.md) and update it as each agent completes.

### Handling Parallel Conflicts

If two parallel agents produce conflicting changes (despite precautions):
1. Identify which agent's output is correct for the spec.
2. Keep that output.
3. Re-dispatch the other agent with updated context (the kept output as a given).
