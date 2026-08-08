---
name: session-checkpoint
description: >
  Flushes decisions not yet written and brings the session record current.
  Two functions, nothing else: append any decision made this session that is missing from
  orchestration_log/reference/decisions.md, and append to
  orchestration_log/history/${DATE}/session.md what has happened since its last write — phases
  completed, work in flight, and current direction.

  Triggers: "checkpoint", "save session state", "capture progress", "session-checkpoint",
  "snapshot the session", "save context".
---

# Session Checkpoint

## Execution

**Function 1 — decision flush.** Scan the session for every ruling, call, and measured verdict.
Append each one missing from `orchestration_log/reference/decisions.md` as
`## YYYY-MM-DD — <decision>`, 2-5 lines, ending in an `Evidence:` line that cites commit SHAs and
tracked paths. An empty flush is a clean result — report it and move on.

**Function 2 — session record update.** Append to
`orchestration_log/history/${DATE}/session.md` what has happened since its last write: phases
completed, work in flight, blocked items, and the direction now set. Append — entries already
written stand as written.

Report both results in one line to the user.

Checkpoint writes these two paths and no others. Invoke it on demand. `session-close` does not
invoke it.

## Artifact Contract

`${DATE}` resolves to the session date as `YYYY-MM-DD`.

| ID | Path | Producer | Consumer | Format | Required |
|----|------|----------|----------|--------|----------|
| L1 | `orchestration_log/reference/ground-truth.md` | orchestrator, in the turn an owner override lands | ARRIVE step 1 | markdown | yes |
| L2 | `orchestration_log/reference/capabilities.md` | orchestrator, in the turn a capability changes | ARRIVE step 4 | markdown | yes |
| L3 | `orchestration_log/reference/decisions.md` | orchestrator, in the turn a decision is made; checkpoint flushes any missed | ARRIVE step 3 (tail) | markdown, append-only | yes |
| L4 | `orchestration_log/reference/conventions.md` | orchestrator, in the turn a rule is established or retired | ARRIVE step 5 | markdown | yes |
| L5 | `orchestration_log/reference/user_deferred_items.md` | orchestrator, on owner deferral; entry deleted on resolution | ARRIVE step 2 | markdown | yes |
| H1 | `orchestration_log/history/${DATE}/session.md` | orchestrator, at will during the session; frozen at close | retroactive mining, audits — never ARRIVE | markdown, frozen at close | yes |
| H2 | `orchestration_log/history/${DATE}/failures.md` | orchestrator, in the turn a failure is diagnosed | retroactive mining, convention derivation | markdown, append-only, frozen at close | conditional (absent when the session had no failures) |
| H3 | `orchestration_log/history/${DATE}/reviews/` | review-producing agents during the session | audits, LEAVE verification | markdown, frozen | conditional (reviews ran) |
| H4 | `orchestration_log/history/${DATE}/cost.md` | LEAVE L6, haiku writes verbatim `/cost` | human audit only — never ARRIVE | markdown, gitignored, never committed | conditional (skip when the user directs no cost capture; otherwise required) |
| S2 | `orchestration_log/recon/${DATE}/leave-verification.md` | LEAVE L2 sonnet agent | orchestrator at L3 | markdown, disposable, gitignored | yes at close |
| S3 | `orchestration_log/recon/${DATE}/*.md` | dispatched agents during the session | orchestrator, same session | markdown, disposable, gitignored | conditional |
| S4 | `orchestration_log/recon/${DATE}/session_metrics.md` | LEAVE L6 haiku via `extract_metrics.py` | human audit — no LEAVE step consumes it | markdown, disposable, gitignored | optional telemetry |
| S5 | `orchestration_log/recon/${DATE}/orphan_scripts.md` | LEAVE L6 sonnet agent | orchestrator | markdown, disposable, gitignored | optional |
