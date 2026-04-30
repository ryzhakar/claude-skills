---
name: session-checkpoint
description: >
  Captures context-dependent session state before compaction destroys it.
  Writes directly to session.md, deferred_items.md, codebase_state.md, and
  conventions.md — the same artifact paths session-close uses (A4, A6, A7,
  A8). Each invocation appends a timestamped section. session-close invokes
  checkpoint as Step 0 before adding computed data and close ceremony.

  Triggers: "checkpoint", "save session state", "capture progress",
  "session-checkpoint", "snapshot the session", "save context".
---

# Session Checkpoint

Captures content that depends on the current context window — decisions, narrative, deferred items, codebase observations, conventions, working state — before compaction or attention decay destroys it. Writes directly to standing artifact paths (A4, A6, A7, A8). session-close invokes checkpoint as its Step 0, then appends computed data. Checkpoint content is authoritative for pre-compaction context — it is already in the files when close-specific steps run.

## Core Principle

**Compaction destroys the only record of WHY decisions were made.** The orchestrator is the sole witness to reasoning, rejected alternatives, and failure sequences. After compaction, attention decays toward the tail — early phases vanish entirely. Checkpoint preserves what the orchestrator knows NOW, before that testimony dies.

Checkpoint captures what dies with the context window. It does NOT capture what can be reliably computed at session end (metrics, git history, cost, codebase measurements). No intermediate files — checkpoint writes to the standing artifact map only.

## Artifact Contract

Canonical paths and ownership for every session artifact. Both checkpoint and session-close operate from this table. Checkpoint writes to rows marked below; session-close produces or extends the remaining rows.

| ID | Path | Writer | Format | Required |
|----|------|--------|--------|----------|
| A1 | `orchestration_log/recon/${DATE}/session_metrics.md` | close Step 1 (haiku) | markdown | yes |
| A2 | `orchestration_log/recon/${DATE}/git_history.md` | close Step 2 (haiku) | markdown | yes |
| A3 | `orchestration_log/recon/${DATE}/orphan_scripts.md` | close Step 4b (sonnet) | markdown | conditional |
| A4 | `orchestration_log/history/${DATE}/session.md` | **checkpoint** appends; close Step 3 extends; close Step 5 corrects | markdown | yes |
| A5 | `orchestration_log/history/${DATE}/reviews/` | review agents during session | markdown | conditional |
| A6 | `orchestration_log/reference/codebase_state.md` | **checkpoint** appends; close Step 4 extends; close Step 5 corrects | markdown | yes |
| A7 | `orchestration_log/reference/deferred_items.md` | **checkpoint** appends; close Step 4 extends; close Step 5 corrects | markdown | yes |
| A8 | `orchestration_log/reference/conventions.md` | **checkpoint** appends; close Step 4 extends; close Step 5 corrects | markdown | yes |
| A9 | `orchestration_log/history/${DATE}/cost.md` | close Step 7 (haiku) | markdown | conditional |

Conditional rows: A3 produces only when script-bearing directories changed. A5 produces only when reviews ran during the session. A9 is gitignored per `orchestration_log/history/*/cost.md` — per-session, local-only, NEVER in version control.

`${DATE}` resolves to the session date as `YYYY-MM-DD`.

## Directory Structure

```
orchestration_log/
  reference/              LIVING documents. Updated by orchestrator before leaving.
    conventions.md        How to work: model tiers, dispatch rules, forbidden patterns.
    codebase_state.md     What exists NOW: inventory, test shape, known limitations, next actions.
    deferred_items.md     Living backlog: unresolved findings with severity and deferral rationale.

  history/                APPEND-ONLY. Never edit a past session.
    YYYY-MM-DD/
      session.md          Timeline, decisions, failures, outcomes.
      cost.md             Verbatim /cost output. GITIGNORED (per-session, local-only).
      reviews/            Review reports (primary evidence, not summaries).

  recon/                  DISPOSABLE. Gitignored. Regenerate when stale.
    YYYY-MM-DD/
      scouts/             Raw agent reports, research findings, data explorations.
```

### Mutability Rules

| Layer | Mutability | Purpose |
|-------|-----------|---------|
| `reference/` | Living — update freely mid-session and at close | What is true NOW |
| `history/` | Frozen after the session ends, not during | What happened THEN |
| `recon/` | Disposable — gitignored, regenerate | Raw scouting data |

### Documentation Categories

Five categories govern documentation drift. Each project defines its category-to-location mapping in `reference/conventions.md`.

| Category | Definition | Drift behavior |
|----------|------------|----------------|
| Decision Record | Architectural choices, rationale, rejected alternatives | Stable across refactoring |
| Capability Inventory | Semantic descriptions of what the system does | Stable; reviewed each LEAVE |
| Status Snapshot | Point-in-time measurements (test counts, metrics, evaluation results) | Decays within hours; regenerate by commands |
| Interface Specification | Function signatures, parameter lists, CLI flag examples | Decays within hours; PROHIBITED in reference docs — source code is truth |
| Session Record | Append-only per-session narrative | Frozen at LEAVE; never edited |

Reference docs MUST NOT carry Interface Specifications.

## What to Capture

| Category | Content | Why it would be lost |
|----------|---------|---------------------|
| Narrative | Timeline of phases so far, what happened in each | Pre-compaction phases vanish from context |
| Decisions | Choices made, alternatives rejected, rationale | Decision context compressed away |
| Failures | Failed approaches, root causes, corrections | Early failures forgotten by session end |
| Deferred items | Issues discovered but not addressed, with severity | Accumulate silently, lost to compaction |
| Codebase state | Observations about structure, debt, or anomalies noted mid-session | Current-window observations not reconstructible later |
| Conventions | Patterns and conventions discovered during the session | Implicit knowledge lost when context narrows |
| Working state | What is in progress, what is blocked, what is next | Overwritten by later work phases |

## What NOT to Capture

These are reliably computed at session end — checkpoint adds no value:

- **JSONL metrics** — `extract_metrics.py` parses raw files at close
- **Git history** — `git log` reconstructs the full record
- **Codebase state** — measurement commands regenerate Status Snapshots
- **Cost** — `/cost` reports only at session end

## Accumulation Model

Each invocation APPENDS to session.md and deferred_items.md. Never overwrite previous content.

**session.md** — append a timestamped checkpoint section:

```markdown
## Checkpoint — {HH:MM}

### Narrative
{Timeline of phases since last checkpoint or session start}

### Decisions
| Decision | Context | Rationale |
|----------|---------|-----------|
| ... | ... | ... |

### Failures
| Failure | Root cause | Correction |
|---------|-----------|------------|
| ... | ... | ... |

### Working State
{What is in progress, what is blocked, what comes next}
```

**deferred_items.md** — append newly discovered items with severity and deferral rationale.

Omit empty sections. Include only sections with content to report.

## Invocation

On-demand only. The user or orchestrator invokes explicitly. session-close invokes checkpoint as its Step 0 — this is non-negotiable, not a convenience. If the orchestrator plans to close the session later, checkpoint is the only mechanism that preserves pre-compaction context for the session record. Skipping it means close reconstructs from a degraded window, producing an incomplete record biased toward the tail. No auto-triggering. No proactive suggestions to checkpoint.

## Execution

1. Append a timestamped checkpoint section to `orchestration_log/history/${DATE}/session.md` with timeline/decisions/failures accumulated so far; append newly discovered deferred items to `orchestration_log/reference/deferred_items.md`; append codebase observations to `orchestration_log/reference/codebase_state.md`; append discovered conventions to `orchestration_log/reference/conventions.md`
2. Report what was captured in a brief summary to the user

No agents needed. The orchestrator writes the checkpoint directly — it holds the context that matters.
