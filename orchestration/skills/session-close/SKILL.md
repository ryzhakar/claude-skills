---
name: session-close
description: >
  Runs the LEAVE protocol: verify memory completeness, then commit. Six ordered steps — verify
  the .gitignore patterns, finalize orchestration_log/history/${DATE}/failures.md, dispatch a
  verification sweep across the five living files, dispose every finding by direct write, finalize
  orchestration_log/history/${DATE}/session.md, commit orchestration_log/. Optional
  telemetry follows: session metrics, verbatim /cost into gitignored cost.md, orphan-script sweep.

  Triggers: "close the session", "do session paperwork", "write the session record",
  "execute the LEAVE protocol", "wrap up the session", "session-close". Invoked ONLY when the
  user explicitly requests session close.
---

# Session Close

LEAVE is verification, then commit.

## ARRIVE

The SessionStart and PostCompact hooks inject the read order when `orchestration_log/reference/` exists: `ground-truth.md`, `user_deferred_items.md`, the tail of `decisions.md`, `capabilities.md`, `conventions.md` — then `git log --oneline -20` and `git status --short` for repo state.
The `agentic-delegation` skill owns that order. This skill owns LEAVE.

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

## LEAVE Protocol

Six steps, in order. L0-L5 are required; L6 is optional telemetry.

### L0 — Verify gitignore (orchestrator)

    grep -F "orchestration_log/recon/" .gitignore
    grep -F "orchestration_log/history/*/cost.md" .gitignore

Append either pattern that is missing.

### L1 — Finalize failures.md (orchestrator)

Append every orchestration failure diagnosed this session that is missing from
`orchestration_log/history/${DATE}/failures.md`: an agent that violated its brief, a protocol step
skipped, a tool or resource failure, an approach abandoned mid-session. Each entry:
`## HH:MM — <failure>`, then root cause, then correction. Leave the file absent when the session had
no failures.

### L2 — Verification sweep (sonnet agent)

Dispatch one agent to run seven checks and write findings to
`orchestration_log/recon/${DATE}/leave-verification.md`. Give the agent the session's ruling list and
its first commit SHA. Each check reports PASS or one row per violation.

| Gate | Check |
|---|---|
| G1 rulings captured | For each ruling in the supplied list, `grep -n` its subject in `reference/decisions.md`. Report every ruling with no matching entry. |
| G2 capabilities current | `git diff --name-status <first-commit>..HEAD`. For every module file added, removed, or renamed, `grep` its name in `reference/capabilities.md`. Report every path the inventory does not name. |
| G3 owner items current | List every `## ` entry in `reference/user_deferred_items.md` with its first line. |
| G4 pointer durability | `grep -n "recon/" reference/*.md`. For each hit, report whether its containing entry also cites a commit SHA or a `history/` path. |
| G5 self-description bound | For each of the five living files: confirm the contract block ends by line 12, and that `sed -n '13,$p'` yields no `**Mutability:**`, `**Holds:**`, `**Does not hold:**`, or `**Convention:**` line and no heading matching `^#{2,3} *(About\|Status\|Overview of this\|How this file\|Maintenance\|Process)`. |
| G6 failure separation | `grep -niE "^#{2,3} .*(failure\|root cause)" history/${DATE}/session.md` — report every hit. |
| G7 snapshots absent | `grep -nE "\b[0-9]{2,} (tests?\|errors?\|warnings?\|files?)\b" reference/capabilities.md` — report every hit whose entry carries no measurement date. |

### L3 — Dispose findings (orchestrator, direct write)

Read `leave-verification.md`. Fix every row: append the missing decision, correct the capabilities
entry, delete resolved owner items, replace or supplement gitignored pointers, compress an
overlong contract block, move failure content to `failures.md`, date or delete a bare count.
This step is not delegated.

### L4 — Session record (orchestrator, direct write)

Bring `orchestration_log/history/${DATE}/session.md` to final form: the canonical header block, a
timeline of phases anchored to commits, and pointers. Draw on `decisions.md` entries dated today,
`history/${DATE}/failures.md`, prior session records for format, and `git log`. Failures appear as a
few words plus `see failures.md`. Cover phases that produced no commits, conversation-driven
decisions, and user corrections, and verify every file path and signature against source.
This step is not delegated.

### L5 — Commit (haiku)

    git add orchestration_log/
    git commit -m "doc: session ${DATE} LEAVE protocol — memory verification + session record"

### L6 — Telemetry (optional)

Run when a consumer for the numbers exists; LEAVE completes without it.
- **Metrics:** dispatch haiku to run `scripts/extract_metrics.py` into
  `recon/${DATE}/session_metrics.md`.
- **Cost:** run `/cost`, cross-verify scope, dispatch haiku to paste the verbatim output into
  `history/${DATE}/cost.md`. Skip entirely when the user directs no cost capture.
- **Orphan scripts:** dispatch sonnet to report tracked scripts with no reference across `scripts/`,
  `.claude/scripts/`, and plugin `hooks/` into `recon/${DATE}/orphan_scripts.md`. Dispose by
  annotating the reference path or by `git rm`.

## Cost source

`/cost` is the ONLY trusted cost source. No manual counting. No estimation. No JSONL-derived cost numbers.

Cross-verify scope before trusting the figure:
- **Wall time range** — does the reported period match this session?
- **Branching** — a branched session's `/cost` covers only that branch, not the parent.
- **Multiple sessions** — did more than one session contribute? `/cost` reports one session.

The haiku agent pastes the output as a fenced code block behind a one-line scope note. NEVER parse, reformat, summarize, or substitute a placeholder — the verbatim output is the artifact. `cost.md` matches the `orchestration_log/history/*/cost.md` ignore pattern, so `git add orchestration_log/` skips it. The session record carries a pointer line.

## Session record header

```markdown
# Session: YYYY-MM-DD

**Orchestrator:** {model}
**Session ID:** {session-id}
**Branch:** {branch, when not main}
**Code changes:** {N} added, {M} removed
**Failures:** see `failures.md` | none this session
**Cost:** see local `cost.md` (gitignored) | not captured this session (per user direction)
**Outcome:** {one or two sentences on what shipped}
```
