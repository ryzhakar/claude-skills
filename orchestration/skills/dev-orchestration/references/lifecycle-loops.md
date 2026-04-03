# Lifecycle Loops

State machines, entry/exit criteria, and loop limits for the development orchestration workflow. The orchestrator uses these to decide when to advance, when to loop back, and when to escalate.

## The Outer Development Loop

The primary loop governing any development task:

```
PLAN --> IMPLEMENT --> REVIEW --> [PASS] --> INTEGRATE --> DONE
                         |
                      [FAIL]
                         |
                       FIX --> REVIEW (re-enter)
```

### State Machine

```
                    +-----------+
                    |  PLANNING |
                    +-----+-----+
                          |
                    plan approved
                          |
               +----------v-----------+
          +--->|    IMPLEMENTING       |
          |    +----------+-----------+
          |               |
          |        agent reports status
          |               |
          |    +----------v-----------+
          |    |  STATUS EVALUATION   |
          |    +--+--+--+--+---------+
          |       |  |  |  |
          |    DONE  |  |  BLOCKED
          |       |  |  |     |
          |       |  |  |  escalate
          |       |  |  |     |
          |       |  |  NEEDS_CONTEXT
          |       |  |     |
          |       |  |  provide + re-dispatch
          |       |  |     |
          |       |  +-----+
          |       |  DONE_WITH_CONCERNS
          |       |     |
          |       |  evaluate concerns
          |       |     |
          |    +--v-----v------------+
          |    |   SPEC REVIEWING    |
          |    +--+--+---------------+
          |       |  |
          |    PASS  FAIL
          |       |     |
          |       |  fix + re-review
          |       |     |
          |       |  +--+
          |       |  |
          |    +--v--v---------------+
          |    | QUALITY REVIEWING   |
          |    +--+--+---------------+
          |       |  |
          |    PASS  FAIL
          |       |     |
          |       |  fix + re-review
          |       |     |
          |    +--v-----+
          |    | UNIT COMPLETE       |
          |    +----------+----------+
          |               |
          |         more units?
          |          yes  |  no
          |           |   |
          +----------+   |
                    +-----v-----------+
                    |  INTEGRATING    |
                    +-----+-----------+
                          |
                     all pass?
                    yes   |   no
                     |    |    |
                     |    +----+ (re-enter implement for failing unit)
                     |
               +-----v-----------+
               |      DONE       |
               +-----------------+
```

### Entry Criteria Per State

**PLANNING:**
- A development task or feature request exists
- The codebase context is understood (file structure, conventions, dependencies)
- The scope is clear enough to decompose into units

**IMPLEMENTING:**
- An approved plan exists with concrete unit specifications
- Each unit has: files to touch, behavior to produce, verification commands
- Dependencies between units are mapped

**SPEC REVIEWING:**
- The implementer has reported DONE or DONE_WITH_CONCERNS (with concerns addressed)
- Changed files are committed
- The task specification is available for comparison

**QUALITY REVIEWING:**
- Spec review has passed (PASS verdict)
- The git diff range is known (BASE_SHA..HEAD_SHA)

**INTEGRATING:**
- All individual units have passed both review stages
- The full test suite is runnable

### Exit Criteria Per State

**PLANNING exits when:**
- Every unit has a self-contained specification
- Dependencies between units are explicit
- Verification commands with expected output exist for each unit
- No TBD, TODO, or placeholder language remains

**IMPLEMENTING exits when:**
- The agent reports a terminal status (DONE, DONE_WITH_CONCERNS, BLOCKED)
- Code is committed (for DONE/DONE_WITH_CONCERNS)

**SPEC REVIEWING exits when:**
- The reviewer reports PASS, or
- The reviewer reports FAIL and the fix-then-re-review loop produces PASS

**QUALITY REVIEWING exits when:**
- The reviewer reports "Ready to merge: Yes" or equivalent, or
- All Critical and Important findings are addressed and re-review passes

**INTEGRATING exits when:**
- Full test suite passes
- Interface compatibility is verified between units
- End-to-end behavior matches original specification

## The Inner Review Loop

The review cycle has its own sub-loop with hard limits to prevent infinite cycling:

```
Review --> FAIL --> Fix --> Re-Review --> FAIL --> Fix --> Re-Review --> FAIL --> ESCALATE
           |                              |
         PASS                           PASS
           |                              |
         exit                           exit
```

### Loop Limit: 3 Review Cycles

After 3 review-fix-re-review cycles on the same unit without reaching PASS:

1. STOP the review loop.
2. Assess whether the issue is:
   - **Implementer quality** -- re-dispatch with a more capable model.
   - **Specification ambiguity** -- the spec needs clarification. Escalate to the user.
   - **Architectural mismatch** -- the unit cannot be implemented as specified because the design is wrong. Return to PLANNING.
3. Never enter a 4th review cycle without changing something structural (model, spec, or decomposition).

### Review Scope Narrowing

On re-review after fixes, the reviewer checks:
- All previously identified issues are resolved
- The fixes did not introduce new issues
- The original passing criteria still hold

The re-review scope narrows to the delta, not the full unit. This prevents review cycle inflation where each pass finds new tangential issues.

## The Debugging Escalation Loop

When implementation failures cannot be explained by the implementation itself:

```
Unexpected Failure
      |
  Form hypotheses (3 max)
      |
  Dispatch parallel investigation agents
      |
  Evaluate evidence
      |
  [Evidence found] --> Apply targeted fix --> Verify
      |
  [No evidence] --> Expand investigation OR escalate to user
```

### Entry Criteria

Enter the debugging loop when:
- Tests fail for reasons unrelated to the current unit's changes
- Behavior contradicts spec but implementation appears correct
- A fix creates failures in unrelated areas
- The implementer reports BLOCKED due to environmental or infrastructure issues

### Exit Criteria

Exit the debugging loop when:
- Root cause is identified and a targeted fix resolves the failure
- The issue is determined to be outside the current task's scope (environmental, infrastructure, pre-existing bug) and the user is informed

### Loop Limit: 3 Hypotheses

Test a maximum of 3 hypotheses before escalating. If 3 independent investigation agents fail to identify the root cause, this signals:
- The problem is architectural (triggers the systematic-debugging architectural questioning threshold)
- The problem is environmental (outside code scope)
- The problem requires domain knowledge the agents lack

Escalate to the user with evidence gathered so far.

## Multi-Unit Coordination

### Parallel Dispatch Rules

Dispatch units in parallel when:
- They touch different files (no write conflicts)
- They do not depend on each other's outputs (no interface dependencies)
- They can be independently tested

Dispatch units sequentially when:
- Unit B imports from or calls into Unit A
- Unit B's tests require Unit A's implementation to exist
- Units share mutable state (database schema, configuration files)

### Dependency Tracking

Track unit dependencies with a simple adjacency list:

```
Unit A: no dependencies (dispatch immediately)
Unit B: depends on A (dispatch after A completes)
Unit C: no dependencies (dispatch with A in parallel)
Unit D: depends on A, C (dispatch after both A and C complete)
```

### Integration Verification

After all units pass individual review, verify integration:

1. **Full test suite execution.** Run all tests, not just the tests from individual units. Cross-unit failures emerge here.

2. **Interface verification.** For each unit boundary (where Unit A calls Unit B), verify:
   - Function signatures match between caller and callee
   - Type expectations align (return types, parameter types)
   - Error handling is consistent across the boundary

3. **End-to-end smoke test.** If the feature has a user-visible behavior, verify it works as specified from the user's perspective. This catches integration gaps that pass unit-level tests.

### Integration Failure Handling

When integration verification fails:

1. Identify which unit boundary is broken.
2. Determine which unit needs to change (usually the dependent unit adapts to the foundational unit's interface).
3. Re-enter the implement-review loop for that unit only.
4. Re-run integration verification after the fix.

Do not re-review units that passed individually unless their code was changed during integration fixes.

## Task Tracking Format

Track the overall orchestration state with a summary block:

```markdown
## Orchestration Status

### Units
| Unit | Status | Spec Review | Quality Review | Notes |
|------|--------|-------------|----------------|-------|
| A: Data model | DONE | PASS | PASS | -- |
| B: API handler | DONE | PASS | In Progress | -- |
| C: CLI command | IMPLEMENTING | -- | -- | -- |
| D: Integration | WAITING | -- | -- | Depends on A, C |

### Integration
- [ ] Full test suite
- [ ] Interface verification
- [ ] End-to-end smoke test

### Blockers
None.
```

Update this summary after each state transition. The orchestrator reads summaries, not implementation details.
