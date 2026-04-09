# Session Persistence

Institutional memory protocol for maintaining orchestrator state across sessions. Without this, every session starts from zero — the orchestrator repeats solved problems, violates established conventions, and misses known risks.

Extracted from real orchestration work (~$150 in API cost, 250+ agent dispatches, 2 sessions of hard-won lessons).

## Why This Matters

A single orchestration session may involve 50-200+ agent dispatches. Hard-won lessons — which model tier works for which task, which patterns cause failures, what the codebase looks like now — live only in the session's context window. When the session ends, the context is gone.

This protocol makes that knowledge durable.

## Directory Structure

```
orchestration_log/
  reference/              LIVING documents. Updated by orchestrator before leaving.
    conventions.md        How to work: model tiers, dispatch rules, forbidden patterns.
    codebase_state.md     What exists NOW: inventory, test shape, known limitations, next actions.
    deferred_items.md     Living backlog: unresolved findings with severity and deferral rationale.

  history/                APPEND-ONLY. Never edit a past session.
    YYYY-MM-DD/
      session.md          Timeline, decisions, failures, cost, outcomes.
      reviews/            Review reports (primary evidence, not summaries).

  recon/                  DISPOSABLE. Gitignored. Regenerate when stale.
    YYYY-MM-DD/
      scouts/             Raw agent reports, research findings, data explorations.
```

### Mutability Rules

| Layer | Mutability | Purpose |
|-------|-----------|---------|
| `reference/` | Living — updated each session | What's true NOW |
| `history/` | Frozen — never edited after session ends | What happened THEN |
| `recon/` | Disposable — gitignored, regenerate | Raw scouting data |

These are not suggestions. Living documents that aren't updated become lies. Frozen documents that get edited destroy the historical record. Disposable documents that aren't gitignored bloat the repository.

## Lifecycle Protocol

### ARRIVE

Every session begins here. No exceptions.

1. Read `reference/conventions.md` — how to work
2. Read `reference/codebase_state.md` — what exists, what's next
3. Read `reference/deferred_items.md` — known debt
4. `git log --oneline -20` — recent changes

This takes 2 minutes and prevents the orchestrator from repeating solved problems, violating established conventions, or missing known risks.

### WORK

Follow conventions. Dispatch agents. The conventions are constraints derived from prior failures. Every rule exists because violating it caused a specific, documented problem.

### LEAVE

Every session ends here. No exceptions.

1. Create `history/YYYY-MM-DD/session.md` — full temporal record
2. Move review reports to `history/YYYY-MM-DD/reviews/`
3. **UPDATE** `reference/codebase_state.md` — current truth
4. **UPDATE** `reference/deferred_items.md` — add new findings, remove fixed ones
5. **UPDATE** `reference/conventions.md` — if patterns changed
6. Commit the log

The LEAVE step is the one that gets skipped. It's also the one that makes the next session productive instead of wasteful.

## Session Record Format

Each session gets `history/YYYY-MM-DD/session.md`:

```markdown
# Session: YYYY-MM-DD

**Orchestrator:** Model name
**Duration:** API time, wall time
**Cost:** Total (breakdown by tier)
**Code changes:** Lines added/removed
**Outcome:** One sentence

---

## Timeline
### Phase: [Name] (HH:MM -- HH:MM)
What happened. What was dispatched. What succeeded. What failed.

## Decision Log
| Decision | Context | Rationale | Outcome |

## Failure Log
| Failure | Root cause | Correction | Prevention |

## Quantitative Summary
| Metric | Value |
```

The failure log is the most valuable part. Conventions are born from it. A session without a failure log is a session that learned nothing.

## Reference Document Formats

### conventions.md

Living document. Present tense. Updated when patterns change.

Contents: model tier overrides for this project, dispatch rules, review protocol, forbidden patterns (project-specific), test philosophy, domain-specific sections.

Every rule should trace to a documented failure. Rules without provenance are superstition.

### codebase_state.md

Present tense. What exists NOW.

```markdown
# Codebase State
Last updated: YYYY-MM-DD

## Module Inventory
| Module | File | Lines | Tests | Status | Last reviewed |

## Test Suite
- Total, passing status, classification breakdown

## Known Limitations
Numbered list of known issues with mitigation status.

## Next Actions (Priority Order)
Numbered list of what to do next.
```

### deferred_items.md

Living backlog. Items added when found, removed when fixed.

```markdown
# Deferred Items
Last updated: YYYY-MM-DD

## From [Source] ([Date])
| ID | Severity | Description | File | Why deferred |
```

Every deferred item has a "why deferred" rationale. Items without rationale are not deferred — they're forgotten.

## Documented Failures

These happened in real orchestration sessions. Each cost real money and time.

| Anti-pattern | What happened | Prevention |
|-------------|---------------|------------|
| No session persistence | Orchestrator repeated mistakes from prior session. Same bugs, same wrong model choices. | ARRIVE/WORK/LEAVE protocol. Read reference docs first. |
| Conventions not updated | Session 2 repeated session 1's failures because LEAVE was skipped. | Update reference docs before ending every session. |
| Trusting agent self-reports | Agent reported "DONE, all tests pass." Tests had stale signatures. Not actually passing. | Verify independently: run the validation command yourself, don't trust the agent's claim about it. |
| Code in orchestrator context | Orchestrator wrote a fix directly instead of dispatching a fix agent. Consumed architect-tier budget on specialist-tier work. | The orchestrator dispatches and decides. All changes happen in agents. |

## What This Protocol Does NOT Cover

- How to write good agent prompts (see prompt-anatomy reference)
- How to decompose work into units (see Decomposition section in SKILL.md)
- Domain-specific knowledge (dev, QA, research — see domain extension skills)

This protocol covers institutional memory — how the orchestrator maintains state across sessions, learns from failures, and enforces discipline on itself.
