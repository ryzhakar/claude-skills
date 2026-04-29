---
name: dev-orchestration
description: |
  Extension of agentic-delegation for software development.
  Adds the Plan→Implement→Review→Fix loop, TDD gates,
  status-driven branching, and debugging escalation.

  Prerequisite: agentic-delegation (orchestration plugin — must be read first).
  Same-plugin agents: implementer, spec-reviewer, code-quality-reviewer.

  Triggers: "implement a feature end-to-end", "execute an implementation plan",
  "build this with agents", "orchestrate development", "run the dev loop",
  "implement using subagents", "dispatch implementers", "coordinate implementation and review".
---

# Dev Orchestration

Extends agentic-delegation with the development lifecycle. The orchestrator drives the Plan→Implement→Review→Fix loop; agents do all coding, testing, and reviewing.

**Read agentic-delegation's SKILL.md (orchestration plugin) before proceeding.** This is a hard gate, not a suggestion. The parent skill provides model ladder, decomposition, prompt anatomy, execution patterns, quality governance, and session persistence. None are restated here.

## Artifact Contract

Canonical map of every artifact this skill's workflow produces. Body prose may reference rows by ID but MUST NOT contradict the table.

| ID | Path | Producer | Consumer | Format | Required |
|----|------|----------|----------|--------|----------|
| A1 | implementer return text | implementer | orchestrator | status block (see implementer.md `Report Format`) | yes |
| A2 | implementer worktree (`.git`) | platform | orchestrator | git repository on disk | yes |
| A3 | `orchestration_log/recon/${DATE}/reviews/spec-${branch}-${timestamp}.md` | spec-reviewer | orchestrator | markdown verdict file (see spec-reviewer.md `Verdict File`) | yes |
| A4 | `orchestration_log/recon/${DATE}/reviews/quality-${branch}-${timestamp}.md` | code-quality-reviewer | orchestrator | markdown report file (see code-quality-reviewer.md `Report File`) | yes |
| A5 | spec-reviewer return text | spec-reviewer | orchestrator | one line: absolute path to A3 | yes |
| A6 | code-quality-reviewer return text | code-quality-reviewer | orchestrator | one line: absolute path to A4 | yes |

`${DATE}` is `YYYY-MM-DD` (UTC). `${branch}` is the implementer's worktree branch (slashes replaced with `-`). `${timestamp}` is `HHMMSS` (UTC).

Branch and SHA are NOT artifacts — they are derived from A2 by direct git query (see Branch and SHA Source of Truth).

## Branch and SHA Source of Truth

Git is authoritative. The implementer reports only its worktree path (A1). The orchestrator queries git for everything else:

```bash
test -d "$WORKTREE/.git" || fail "implementer reported invalid worktree path"
BRANCH=$(git -C "$WORKTREE" branch --show-current)
HEAD_SHA=$(git -C "$WORKTREE" rev-parse HEAD)
BASE_SHA=$(git -C "$WORKTREE" merge-base HEAD "$INTEGRATION_BRANCH")
```

Trust surface reduces to one check: did the implementer report a valid worktree path? Verifiable by filesystem existence. The orchestrator MUST NOT parse branch or SHA from agent return text — git is the single source.

## Worktree Discipline (Orchestrator Side)

Worktrees are the default vehicle for any real implementation work, not optional ceremony. The implementer agent declares `isolation: worktree` in its frontmatter precisely because every dispatch deserves its own checkout. The orchestrator MUST dispatch implementation work through worktree-isolated agents. The orchestrator MUST NOT execute implementation work in its own context, and MUST NOT route implementation through agents that bypass worktree isolation.

**CWD-drift hazard.** The platform can shift the orchestrator's CWD into a worktree without any explicit `cd` action by the orchestrator. After drift, CWD-relative shell operations resolve in the wrong tree, and any subagent dispatched inherits the wrong starting CWD (subagents start in the main conversation's CWD; `cd` inside a subagent does not persist).

**Defense — awareness, not checklist.** Keep this hazard in mind. Check `pwd` whenever a CWD-relative shell operation or a subagent dispatch is about to propagate failure. No fixed gate; exercise judgment.

**Restoration.** When `pwd` reveals drift away from the project root, `cd` back to the known root. The orchestrator already knows the root — no portable command lives in this skill.

**Bilateral rules.**
- The orchestrator MUST `cd` back to the project root the moment `pwd` reveals drift.
- The orchestrator MUST NOT proceed with CWD-relative operations or subagent dispatches after detecting drift, until restoration is verified by a fresh `pwd`.

## Invariants

Two invariants govern this skill. They are not guidelines. They are structural constraints.

**Review is inevitable.** Every implementer dispatch produces a full review chain. Three SubagentStop hooks (same plugin) enforce it as unconditional, sequential mandates:

1. `implementer` stop → mandates spec-reviewer dispatch.
2. `spec-reviewer` stop → mandates code-quality-reviewer dispatch (unconditional; the spec verdict semantics move into the code-quality-reviewer itself, which short-circuits on a FAIL spec verdict).
3. `code-quality-reviewer` stop → mandates the merge decision (integrate, re-dispatch implementer with findings, or surface to the user).

The orchestrator cannot skip, defer, or conditionally bypass any stage. It no longer evaluates the spec verdict at the spec→quality boundary — that judgment lives inside code-quality-reviewer.

**Worktree isolation is total.** The implementer agent runs in a platform-provided worktree. All reads, writes, and commits happen in that worktree. The orchestrator passes the worktree path and branch to reviewers. No agent touches the main working tree during implementation.

## Verb Interpretation

Every action verb from the user implies agent-delegated execution. The orchestrator decomposes, delegates, and assembles. It never executes.

- "implement/build/create X" — dispatch implementer agents for X.
- "fix/debug/repair X" — dispatch debugging agents for X, following the escalation protocol.
- "review/check/audit X" — dispatch spec-reviewer and code-quality-reviewer agents for X.
- "test X" — dispatch test agents or verify test results independently.
- "refactor/improve X" — dispatch implementer agents with refactoring scope.
- "plan X" — decompose X into implementation units, then dispatch agents for each.

No exceptions. The orchestrator never writes code, never reads implementation files, never debugs test failures in its own context. Every line of code is written by an agent.

## Dependencies

The parent skill (agentic-delegation) lives in the orchestration plugin. It must be installed and read before this skill.

This plugin provides three purpose-built agents: **implementer**, **spec-reviewer**, **code-quality-reviewer**. Reference them directly — they are same-plugin, always available.

This plugin also provides skills referenced below: **defensive-planning**, **tdd**, **systematic-debugging**, **receiving-code-review**.

## The Development Loop

```
PLAN ──→ IMPLEMENT ──→ REVIEW ──→ [PASS] ──→ INTEGRATE ──→ DONE
                          │
                        [FAIL]
                          │
                        FIX ──→ REVIEW (re-enter)
```

The orchestrator drives this loop. Each phase has entry/exit criteria and agent dispatch patterns. Skipping phases produces spec drift, quality regression, or wasted effort.

Apply the full loop for any task touching behavior-carrying code: new features, bug fixes, refactors, migrations. Scale to task size — changes requiring no reasoning (renaming, typos, string literal updates) can be executed directly without agent dispatch; everything else goes through the loop.

### State Machine

| State | Entry Criteria | Exit Criteria |
|-------|---------------|---------------|
| PLANNING | Task exists; codebase context understood; scope clear enough to decompose | Every unit has self-contained spec; dependencies explicit; verification commands defined; no TBD/TODO/placeholder language |
| IMPLEMENTING | Approved plan with concrete unit specs; each unit has files, behavior, verification; dependencies mapped | Agent reports terminal status (DONE/DONE_WITH_CONCERNS/BLOCKED); code committed |
| SPEC REVIEWING | Implementer reported DONE or DONE_WITH_CONCERNS (addressed); changes committed; task spec available | Reviewer reports PASS, or fix-re-review loop produces PASS |
| QUALITY REVIEWING | Spec review passed; git diff range known | Reviewer reports merge-ready, or all Critical/Important findings addressed and re-review passes |
| INTEGRATING | All units passed both review stages; full test suite runnable | Full test suite passes; interface compatibility verified; end-to-end behavior matches spec |

## Phase 1: Plan

Decompose the work into implementation units before touching code.

Use defensive-planning to produce the implementation plan with verification gates, forbidden patterns, and exhaustive field lists.

### Dev-Specific Decomposition

The parent's decomposition patterns (by entity, by aspect, by concern) apply. For dev tasks, the natural unit is measured in files and testable behaviors:

- Touches 1-3 files
- Produces independently testable behavior
- The orchestrator describes it in a self-contained brief (no "see previous task" references)
- Takes an implementer agent 2-10 minutes

5+ files per unit: split into 2-3 smaller units.

### Ordering

Build foundational units first (data models, interfaces), then dependent units (logic, integration), then verification units (integration tests, end-to-end checks). Use the parent's sequential pipeline pattern for dependent units.

## Phase 2: Implement

Dispatch one agent per implementation unit. The orchestrator never implements in its own context.

### Dispatch

For each unit, construct a brief containing:
1. **Task specification** — exact code expectations and verification commands
2. **File paths** — absolute paths to files the agent must read (existing interfaces, types, related modules)
3. **TDD requirements** — whether this unit requires test-driven development
4. **Scope boundaries** — what to build, what NOT to build
5. **Scene-setting context** — 2-3 sentences on where this unit fits in the system. Agents without situational awareness produce architecturally disconnected code.

Dispatch the **implementer** agent with this brief. The implementer runs in a platform-provided worktree (`isolation: worktree` in its frontmatter). The platform creates the worktree automatically — the orchestrator does not manage worktree creation. Default model: sonnet. Upgrade only if an agent reports BLOCKED citing reasoning limitations.

**Minimal context examples:**
- Dependency audit: "The project uses Leptos 0.8, Tailwind v4 (standalone, no Node.js), Postgres via sqlx. Read /path/to/Cargo.toml. For each dep, note version and purpose. Check for version conflicts."
- Compatibility check: "Check if library X supports Tailwind v4. The project uses v4 standalone (no Node.js). Fetch library docs and check for Tailwind-related config."
- Type verification (sonnet): "Verify library X's auth API is compatible with the project's user model. Read /path/to/models/user.rs and fetch library X auth docs. Check: does it accept our User struct fields? Are return types compatible?"

### Context Requirements by Agent Type

**Implementer:** Task specification + file paths + TDD flag + scope boundaries + scene-setting context. The platform creates the worktree automatically. The implementer reports its worktree path in status (A1).

**Spec-reviewer:** Task specification + worktree path + branch (from git query on A2) + verdict file path to write (A3). The reviewer reads actual code from that branch and writes its verdict to A3.

**Code-quality-reviewer:** Worktree path + branch + diff range `BASE_SHA..HEAD_SHA` (from git queries on A2) + report file path to write (A4) + project-specific quality standards if they exist.

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

Agents commit their own work with descriptive messages. When review reveals needed fixes, dispatch a fix agent — the orchestrator does not edit code, does not commit code, does not debug code.

One logical change per commit. Fix commits reference what they fix. No history rewriting (no rebase, no amend, no force push).

### Verification After Each Agent

Run the test suite and type checker after every implementer reports DONE. Agent self-reports are unreliable for cross-module integration — an agent may report DONE while its changes break tests in modules it did not touch.

This plugin includes three SubagentStop hooks (matchers: `implementer`, `spec-reviewer`, `code-quality-reviewer`) that fire when each agent type stops. Each hook injects an unconditional next-step mandate into orchestrator context — spec review after implementer, quality review after spec-reviewer, merge decision after code-quality-reviewer — making the full chain structurally inevitable. The orchestrator no longer evaluates the spec verdict at the spec→quality boundary; that judgment moved into the code-quality-reviewer agent itself.

## Phase 3: Review

Review is not optional. It is the only exit from the IMPLEMENTING state.

Two-stage review after each unit. Order is mandatory: spec compliance first, code quality second. Reviewing quality before confirming spec compliance wastes effort on code that may not meet requirements. The orchestrator derives branch and SHAs from git (A2) — never from parsed agent text — and supplies them to each reviewer alongside the verdict-file path the reviewer must write.

### Stage 1: Spec Compliance

Dispatch the **spec-reviewer** with task specification, worktree path, branch, and the A3 path to write. It reads actual code from the branch with adversarial posture and writes its verdict to A3.

After dispatch, the orchestrator verifies A3 exists and reads the `Verdict:` line from it. The reviewer's return text serves only to point at A3; the file is the source of truth.

### Stage 2: Code Quality

Only after spec compliance passes. Dispatch the **code-quality-reviewer** with worktree path, branch, `BASE_SHA..HEAD_SHA` diff range, and the A4 path to write. It evaluates quality, testing adequacy, and architecture, categorizes findings by severity, and writes a merge verdict to A4.

After dispatch, the orchestrator verifies A4 exists and reads the `Ready to merge:` line. The file is the gating evidence.

### The Inner Review Loop

```
Review → FAIL → Fix → Re-Review → FAIL → Fix → Re-Review → FAIL → ESCALATE
```

After 3 review-fix cycles without PASS, stop. The problem is structural:

1. **Implementer quality** — re-dispatch with a more capable model.
2. **Specification ambiguity** — the spec needs clarification. Escalate to the user.
3. **Architectural mismatch** — the unit cannot be implemented as specified because the design is wrong. Return to PLANNING.

Never enter a 4th review cycle without changing something structural (model, spec, or decomposition).

**Review scope narrows on re-review:** the reviewer checks that previously identified issues are resolved, that fixes did not introduce new issues, and that original passing criteria still hold. Re-review scope narrows to the delta, not the full unit — this prevents review cycle inflation.

Apply receiving-code-review's verify-before-implement discipline and YAGNI enforcement when processing findings.

## Phase 4: Status-Driven Branching

Interpret implementer status and route:

| Status | Route |
|---|---|
| DONE | Dispatch spec-reviewer. |
| DONE_WITH_CONCERNS | Classify concerns. Address correctness/scope before review. Note observational concerns and proceed. |
| NEEDS_CONTEXT | Identify missing information. Provide it. Re-dispatch. |
| BLOCKED | Diagnose root cause (see Debugging Escalation). |

The orchestrator reads status codes from completion summaries. Analysis beyond the code itself — classifying concerns, diagnosing blockers — is delegated.

### NEEDS_CONTEXT Handling

Determine what is missing:
- **File content** → provide paths, re-dispatch
- **Domain knowledge** → provide explanation, re-dispatch
- **Architectural decision** → make decision, update spec, re-dispatch
- **User input required** → ask user, then re-dispatch

Construct a new dispatch with the original brief plus missing context. Rewrite the relevant section inline — the agent should not piece together context from multiple messages.

### BLOCKED Escalation

Dispatch a diagnosis agent to determine the cause:

1. **Missing dependency** — provide it, re-dispatch implementer.
2. **Insufficient reasoning** — re-dispatch with a more capable model. Same spec.
3. **Task too large** — decompose into sub-units.
4. **Plan defect** — the plan's assumptions are wrong. Escalate to the user.
5. **Unknown** — dispatch investigation agents.

Never force retry without changing inputs.

### Re-Dispatch After Review Failure

Dispatch a fix agent with:
1. The original task specification (reference)
2. The reviewer's specific findings (the FAIL report)
3. Instructions to fix ONLY the identified issues, test each individually, and report status

Scope the fix to the specific findings.

## Debugging Escalation

When implementation produces unexpected failures (tests fail for unclear reasons, behavior deviates from spec without obvious cause):

Apply systematic-debugging's 4-phase root cause protocol: investigate before fixing, trace data flow, form hypotheses, test minimally.

For multi-hypothesis investigation, apply the parent's speculative-parallel pattern: dispatch parallel agents each investigating one hypothesis independently. Compare their evidence.

### When to Enter

- Implementer reports BLOCKED due to unrelated test failures
- Review reveals behavior contradicting spec but implementation looks correct
- A fix creates new failures elsewhere (architectural coupling signal)
- 3+ fix attempts on the same issue without resolution

### The Debugging Loop

```
Unexpected Failure
      |
  Form hypotheses (3 max)
      |
  Dispatch parallel investigation agents
      |
  Evaluate evidence
      |
  [Evidence found] → Apply targeted fix → Verify
      |
  [No evidence] → Expand investigation OR escalate to user
```

Test a maximum of 3 hypotheses before escalating. If 3 independent investigation agents fail to identify the root cause, the problem is architectural, environmental, or requires domain knowledge the agents lack. Escalate to the user with evidence gathered so far.

## Multi-Unit Integration

After all units pass individual review:

1. Run the full test suite (not just unit-level tests).
2. Dispatch an integration verification agent to check interface compatibility between units (types, signatures, data contracts) and end-to-end behavior against the original spec.
3. If issues arise, determine which unit is at fault and re-enter the implement-review loop for that unit only.

### Parallel Dispatch Coordination

When dispatching multiple implementers in parallel:

1. **Verify independence.** No two agents may write to the same file. If they do, make them sequential.
2. **Provide isolation context.** Each agent's brief mentions which other units exist and which files they own.
3. **Stagger reviews.** As implementers complete, dispatch their reviews immediately. Do not wait for all to finish.
4. **Handle conflicts.** If two parallel agents produce conflicting changes, identify which matches the spec, keep it, re-dispatch the other with updated context.

### Dependency Tracking

Track unit dependencies:
```
Unit A: no dependencies (dispatch immediately)
Unit B: depends on A (dispatch after A completes)
Unit C: no dependencies (dispatch with A in parallel)
```

### Cross-Cutting Review

For multi-unit features, dispatch a cross-cutting review after integration passes. The orchestrator delegates concern classification to an agent. Decompose by CONCERN, not by module. Module-scoped reviews repeat shallow checks. Concern-scoped reviews find cross-cutting bugs.

| Concern | What it catches |
|---------|-----------------|
| Spec fidelity | Missing features, spec drift, scope creep |
| Data flow integrity | Schema drift, silent data loss, interface mismatches |
| Simplicity | Unnecessary complexity, tangled concerns |
| DRY/YAGNI | Duplicated knowledge, unused features |

Fan out one agent per concern — the parent's fan-out-by-concern pattern applied to dev review.

### Test Quality Audit

After the test suite stabilizes, classify every test:

| Classification | Action |
|----------------|--------|
| VALUABLE | Tests a specific behavior that could regress. Asserts a property, not a value. Keep. |
| SMOKE | Verifies code runs without crashing. Low value but cheap. Keep only if truly cheap. |
| TAUTOLOGICAL | Asserts defaults equal hardcoded copies, or tests library guarantees. Delete. |
| MISSING | A test that should exist. Prioritize by risk of the bug it would catch. Add. |

Theatrical test coverage is worse than low coverage — it creates false confidence. Delete tautological tests and add missing critical ones.

## Task Tracking

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

## Anti-Patterns

**Code in orchestrator context.** The orchestrator dispatches and decides. It never writes, reads, or debugs code.

**Skipping spec review.** Review is a structural invariant, not a discretionary step. The SubagentStop hook enforces this — but even without the hook, the orchestrator treats review as the only exit from IMPLEMENTING. Implementer self-review is not spec compliance.

**Reviewing quality before spec compliance.** Polishing code that does not meet requirements is wasted work.

**Batch-fixing review findings.** Fix one issue, test, commit, repeat. All-at-once creates compound failures.

**Ignoring DONE_WITH_CONCERNS.** Correctness or scope concerns must be addressed before review.

**Theatrical test coverage.** Tests that assert defaults equal hardcoded copies provide zero protection.

**Module-scoped cross-cutting reviews.** Reviewing each module independently misses cross-module issues.

**Worktree escape.** The implementer runs in a worktree. If code appears in the main working tree after implementation, the worktree discipline failed. All implementation artifacts live in the worktree branch until review passes and integration merges them.

**Parsing branch or SHA from agent text.** The orchestrator derives branch and SHA from git (A2). Parsing them from the implementer's return text is fragile — formats drift, fields go missing, reviewers silently read main. See Branch and SHA Source of Truth.

**Trusting reviewer return text as the verdict.** Return text can be lost to compaction. The verdict files (A3, A4) are the gating evidence. Read them.
