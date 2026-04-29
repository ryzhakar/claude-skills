---
name: session-close
description: >
  Governs the ARRIVE/WORK/LEAVE session lifecycle for orchestration sessions. Covers
  session start (reference doc ingestion), session work (convention adherence), and
  session close (metric extraction, session record, reference updates, cost capture to gitignored cost.md, VCS commit).

  Triggers: "close the session", "do session paperwork", "write the session record",
  "execute the LEAVE protocol", "wrap up the session", "start a session", "ARRIVE",
  "session lifecycle"; or at the natural end of a development orchestration session.
  Also invoked by model when session persistence context is needed.
---

# Session Lifecycle

Governs the ARRIVE/WORK/LEAVE lifecycle for orchestration sessions. Produces durable institutional memory by combining objective data extracted from raw session files on disk with orchestrator context that only the active session possesses.

## Core Principle

**The orchestrator holds context no agent can reconstruct.** Agents extract objective data (metrics, git history, file changes) from disk. The orchestrator synthesizes that with the actual decisions made, failures encountered, and reasoning behind choices — then corrects the agents' reconstructions before committing.

Never delegate the final synthesis and correction to an agent. The orchestrator owns the session record.

## Artifact Contract

Canonical paths and ownership for every artifact this skill produces or consumes. Skill body prose may cite rows by ID. Prose MUST NOT contradict this table.

| ID | Path | Producer | Consumer | Format | Required |
|----|------|----------|----------|--------|----------|
| A1 | `orchestration_log/recon/${DATE}/session_metrics.md` | Step 1 haiku agent | Step 3 draft agent, Step 5 orchestrator | markdown | yes |
| A2 | `orchestration_log/recon/${DATE}/git_history.md` | Step 2 haiku agent | Step 3 draft agent, Step 5 orchestrator | markdown | yes |
| A3 | `orchestration_log/recon/${DATE}/orphan_scripts.md` | Step 4b sonnet agent | Step 5 orchestrator | markdown | conditional |
| A4 | `orchestration_log/history/${DATE}/session.md` | Step 3 sonnet agent drafts; Step 5 orchestrator corrects | next-session ARRIVE, future Step 3 drafts (format reference) | markdown | yes |
| A5 | `orchestration_log/history/${DATE}/reviews/` | review-producing agents during the session | next-session ARRIVE, audits | markdown | conditional |
| A6 | `orchestration_log/reference/codebase_state.md` | Step 4 sonnet agent; Step 5 orchestrator corrects | every ARRIVE | markdown | yes |
| A7 | `orchestration_log/reference/deferred_items.md` | Step 4 sonnet agent; Step 5 orchestrator corrects | every ARRIVE | markdown | yes |
| A8 | `orchestration_log/reference/conventions.md` | Step 4 sonnet agent; Step 5 orchestrator corrects | every ARRIVE | markdown | yes |
| A9 | `orchestration_log/history/${DATE}/cost.md` | Step 7 (orchestrator dispatches haiku to write verbatim `/cost` output) | human only (audit / record-keeping at close); NOT consumed by next-session ARRIVE | markdown | conditional (skip when user directs no cost capture; otherwise required) |

Conditional rows: A3 produces only when Step 4b runs (script-bearing directories changed). A5 produces only when reviews ran during the session. A9 (cost.md) is gitignored per `**/cost.md` — per-session, local-only, NEVER in version control. Cost data is operational, not historical artifact; stewardship lives outside git. The session record (A4) carries only a pointer line, never the cost number itself. Not recoverable retroactively: `/cost` reports only the current live session.

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
| `reference/` | Living -- updated each session | What is true NOW |
| `history/` | Frozen -- never edited after session ends | What happened THEN |
| `recon/` | Disposable -- gitignored, regenerate | Raw scouting data |

Living documents that are not updated become lies. Frozen documents that get edited destroy the historical record. Disposable documents that are not gitignored bloat the repository.

### Documentation Categories

Five categories govern documentation drift behavior. Observed in one project's forensics; the abstract pattern likely generalizes — each project should evaluate fit and define its own category-to-location mapping in `reference/conventions.md`. The skill names the categories and the Interface Specification prohibition; location mapping stays in project conventions.

| Category | Definition | Drift behavior |
|----------|------------|----------------|
| Decision Record | Architectural choices, rationale, rejected alternatives. Falsifiable only by human reversal. | Stable across refactoring. |
| Capability Inventory | Semantic descriptions of what the system does — modules, commands, behaviors. | Stable across refactoring; reviewed each LEAVE. |
| Status Snapshot | Point-in-time measurements (test counts, type-checker status, build metrics, evaluation results). | Decays within hours; MUST be regenerated by commands. |
| Interface Specification | Function signatures, parameter lists, CLI flag examples. | Decays within hours; PROHIBITED in reference docs — the source code (type-annotated) plus `--help` is the source of truth. |
| Session Record | Append-only per-session narrative. | Frozen at LEAVE; never edited. |

Reference docs MUST carry only Decision Record, Capability Inventory, and (regenerated) Status Snapshot content. Reference docs MUST NOT carry Interface Specifications.

## Session Data on Disk

Claude Code stores structured session data at:

```
~/.claude-shared/projects/{project-slug}/
  {session-id}.jsonl          — main conversation (orchestrator turns)
  {session-id}/
    subagents/
      agent-{id}.jsonl        — per-agent conversation
      agent-{id}.meta.json    — agent metadata
    tool-results/             — persisted tool outputs
```

The project slug is the filesystem-safe form of the project path (e.g., `-Users-ryzhakar-competera-embedding-finetuning-for-ecommerce`).

### JSONL Record Structure

Each line is a JSON object:

```json
{
  "parentUuid": "uuid-or-null",
  "isSidechain": true,
  "promptId": "uuid",
  "agentId": "agent-{hex-string}",
  "type": "user" | "assistant",
  "message": {
    "role": "user" | "assistant",
    "model": "claude-opus-4-6" | "claude-sonnet-4-5-*" | "claude-haiku-4-5-*",
    "content": [
      {"type": "tool_use", "name": "Read", "input": {}},
      {"type": "tool_result", "tool_use_id": "...", "content": "..."},
      {"type": "tool_use", "name": "Agent", "input": {"description": "...", "model": "sonnet"}},
      {"type": "text", "text": "..."}
    ],
    "usage": {
      "input_tokens": 945,
      "output_tokens": 22048,
      "cache_read_input_tokens": 32000000,
      "cache_creation_input_tokens": 5200000
    }
  },
  "timestamp": "2026-04-09T19:27:12.161000+00:00",
  "sessionId": "uuid",
  "gitBranch": "main"
}
```

### Model Tier Detection

Model tier: "haiku" if model contains "haiku", "sonnet" if "sonnet", "opus" if "opus".

### Agent Dispatch Counting

Count agents in TWO separate groupings:

**By model tier.** How many agents ran on haiku, sonnet, opus. Extract from `message.model` field in each agent's JSONL.

**By agent type.** How many of each `subagent_type` were dispatched (e.g., 5 implementers, 3 spec-reviewers, 15 haiku research agents). Extract from agent metadata or the `subagent_type` field.

Both groupings. Separately. Not collapsed into one table.

### Cost Source

`/cost` is the ONLY trusted cost source. No manual counting. No estimation. No JSONL-derived cost numbers — JSONL double-counts subagent internals.

BEFORE trusting `/cost`, cross-verify scope:
- **Wall time range** — does the reported period match this session?
- **Branching** — a branched session's `/cost` covers only that branch, not the parent.
- **Multiple sessions** — did more than one session contribute? `/cost` reports one session.

The verification confirms `/cost` reports for the RIGHT scope. It does not compute an alternative number.

**Where the captured cost lives.** Step 7 writes verbatim `/cost` output to gitignored `orchestration_log/history/${DATE}/cost.md` (Artifact Contract row A9). The verbatim `/cost` output IS the artifact — a Status Snapshot per the Documentation Categories taxonomy, regenerated only at session close and never reformatted. Cost numbers MUST NOT be embedded inline in session.md, MUST NOT be parsed or summarized, MUST NOT be committed (cost.md matches `**/cost.md` in `.gitignore`). The session record carries a pointer line only.

## Session Record Format

### Header Template

```markdown
# Session: YYYY-MM-DD

**Orchestrator:** Claude Opus 4.6 (1M context)
**Session ID:** {session-id}          ← links to raw JSONL files
**Branch:** {git branch, if branched}  ← omit if main
**Duration:** {X}h {Y}m API, {Z}h {W}m wall
**Cost:** see local `cost.md` (gitignored; per-session)
**Code changes:** {N} lines added, {M} removed
**Outcome:** {1-2 sentence summary of what shipped}
```

The session ID links directly to `~/.claude-shared/projects/{slug}/{session-id}.jsonl`. The Cost line is static text pointing at `cost.md` — the cost.md file is the truth, written by Step 7. NEVER substitute a placeholder, NEVER inline the cost number. Skipped capture (per user direction): replace the line with `**Cost:** not captured this session (per user direction)`.

### Required Sections

**Timeline** — chronological phases, anchored to git commits. Each phase: what happened, what was decided, what failed, commit hashes.

**Decision Log** — table: Decision | Context | Rationale | Outcome. Include reversals, choices between valid options, architectural commitments, responses to failures.

**Failure Log** — table: Failure | Root cause | Correction | Prevention. Include OOM/resource failures, agent spec violations, tool failures, skipped protocol steps, wrong initial approaches. The failure log is the most valuable part. Conventions are born from it.

**Quantitative Summary** — table: Metric | Value. API time, wall time, git commits, code changes, tests, pyright errors, agent dispatches. Cost lives in gitignored `cost.md` (Step 7), NEVER in this table.

**Next Session Priorities** — ordered list connecting to `deferred_items.md`.

### What Agents Get Wrong

Agents reconstruct from git history and file artifacts. They systematically miss: research phases (no commits), failed first attempts (context lost), conversation-driven decisions, tool failures, user corrections, skipped protocol steps, stale numbers, guessed function signatures.

The orchestrator must add all of the above after reviewing the agent draft.

---

## ARRIVE Protocol

Every session begins here. No exceptions.

1. Read `reference/conventions.md` -- how to work
2. Read `reference/codebase_state.md` -- what exists, what is next
3. Read `reference/deferred_items.md` -- known debt
4. `git log --oneline -20` -- recent changes

This takes 2 minutes and prevents the orchestrator from repeating solved problems, violating established conventions, or missing known risks.

---

## WORK Protocol

Follow conventions. Dispatch agents per the `agentic-delegation` skill (decomposition, model ladder, prompt anatomy, execution patterns). Conventions are constraints derived from prior failures — every rule exists because violating it caused a documented problem.

---

## LEAVE Protocol

The orchestrator executes in this order. Run Steps 1-4 in parallel. Step 4b (orphan-script audit) is optional and parallel-eligible. Step 5 requires orchestrator participation. Steps 6-7 are sequential.

### Step 1: Extract session metrics (haiku, background)

Dispatch a haiku agent to parse all JSONL files in the session directory. Agent writes to `orchestration_log/recon/{YYYY-MM-DD}/session_metrics.md`.

Dispatch the agent with instructions to extract:
- **Agent counts by model tier** — how many agents ran on haiku, sonnet, opus (from `message.model`)
- **Agent counts by type** — how many of each `subagent_type` (e.g., 5 implementers, 3 spec-reviewers, 15 research agents). From agent metadata or `subagent_type` field
- Messages by model tier (haiku / sonnet / opus)
- Tool calls by tool name
- Token totals by model tier (input, output, cache_read, cache_creation)
- Timestamp range

Report the two agent groupings as separate tables.

Use `scripts/extract_metrics.py` for reliable parsing.

Step 1 provides agent counts and message volumes. NEVER derive cost from JSONL. See Cost Source section — `/cost` is the only trusted source. Step 7 captures cost to gitignored `cost.md`.

### Step 2: Extract git history (haiku, background)

Dispatch a haiku agent to extract the git log for the session period. Agent writes to `orchestration_log/recon/{YYYY-MM-DD}/git_history.md`.

Commands to run:
- `git log --format="%ai %H %s" --since="{session-start-date}" --reverse`
- `git diff --stat {first-session-commit}..HEAD`

### Steps 3-4: Conditional Drafting

**Gate:** If reference docs were updated within the current session (agents already ran LEAVE steps, or orchestrator edited reference docs directly), skip Steps 3-4. The orchestrator reviews existing docs directly in Step 5 instead of reviewing agent drafts. This prevents redundant agent dispatches when docs are already current.

### Step 3: Draft session record (sonnet, background)

Dispatch a sonnet agent to draft `orchestration_log/history/{YYYY-MM-DD}/session.md`. Point the agent at:
- `orchestration_log/history/` — prior session records for format reference
- The git history recon file (when available)
- `orchestration_log/reference/` — current reference docs for state context

The agent must use the header template and required sections defined above. Include the session ID for backlinking.

The agent reconstructs from artifacts. **It will miss things and get things wrong.** The orchestrator corrects in Step 5.

### Step 4: Draft reference doc updates (sonnet, background)

Dispatch a sonnet agent to update the three living reference documents:
- `orchestration_log/reference/codebase_state.md` — update from actual code (`grep`, `wc -l`, pytest)
- `orchestration_log/reference/deferred_items.md` — add new findings, remove resolved items
- `orchestration_log/reference/conventions.md` — add patterns discovered this session

The agent must read actual code — not guess at function signatures.

**Status Snapshot regeneration.** Identify every Status Snapshot section in the reference docs (test counts, type-checker status, build metrics, evaluation results). Run the project's measurement commands as defined in `reference/conventions.md` and paste verbatim output. Status Snapshots MUST be regenerated by measurement commands; they MUST NOT be reconstructed from session memory or carried over from earlier in the session. The skill prescribes the principle, not the commands — specific tooling (test runners, type checkers, evaluation harnesses) lives in the project's conventions.

**Decision Record trigger.** If the session made any architectural decision (new module, new strategy, rejected approach, changed data model, changed external dependency posture), the agent MUST write both a narrative entry in the project's living decision document AND an index row in the project's decision log, in the same commit. Architectural decisions MUST NOT be left to live only in the session record. The skill states the dual-write obligation; the project's conventions name the two files.

### Step 4b: Orphan tracked-script audit (sonnet, optional, advisory)

Optional. LEAVE completes whether or not this runs. Skip when no scripts changed and no script-bearing directories were touched this session.

Dispatch a sonnet agent to identify tracked scripts with zero references across the marketplace. Scope:
- `scripts/`
- `.claude/scripts/`
- every plugin `hooks/` directory

Detection: a script is a candidate when no skill (`SKILL.md`), agent (`.md` under `agents/`), hook (`hooks.json`, hook scripts, hook templates), or workflow file references it by path or by basename. Reference judgment requires reading surrounding context — a string match alone does not establish use.

The agent writes a report to `orchestration_log/recon/{YYYY-MM-DD}/orphan_scripts.md`. Each candidate gets a row: script path, the directories searched for references, and a one-line rationale for why no reference was found.

Disposition (orchestrator, in Step 5):
- **Justify** — annotate the canonical reference path that legitimizes the script (e.g., a hook command, a skill instruction, a `justfile` recipe). Update the consuming file if the reference is missing.
- **Remove** — `git rm` the orphan and stage with the LEAVE commit.

Boundaries:
- Removal happens in Step 5 by the orchestrator, not by the audit agent. The agent reports; it does not delete.
- A missing or incomplete report does not block LEAVE. Steps 5-7 proceed regardless.
- Haiku does not dispatch this step. Reference judgment requires sonnet — string matching alone misclassifies.
- Audit scope NEVER extends to `recon/`. Recon is gitignored and disposable; `rm -rf recon/{old-date}/` covers that hygiene separately.

### Step 5: Review and correct drafts (orchestrator, after Steps 1-4 complete)

Read the draft session record. Correct:
- Missing phases (agents reconstruct from git, they miss non-code work)
- Wrong numbers (agents may use stale data from earlier in session)
- Missing failures (agents omit failures that are not in git history)
- Wrong attribution (which decisions were made vs. which were imposed)
- Guessed function signatures (agent must read actual code, not infer)

This step cannot be delegated. The orchestrator has context no agent can access.

If Step 4b ran, read `orphan_scripts.md` and dispose of each candidate (justify with an annotated reference path, or `git rm`). Stage removals for the Step 6 commit.

**Spec lifecycle sweep.** Sweep the project for any spec document — regardless of file location — carrying a "Status: Ready for implementation" header (or equivalent) that the session implemented in whole or in part. Any such spec MUST be archived before the session closes; ready-for-implementation specs MUST NOT remain in their pre-implementation location once the code lands. The three-action close-out: (1) extract architectural decisions from the spec into the project's decision record, (2) move the spec to the project's history directory with an archive header marking it IMPLEMENTED (with actual file locations), (3) record the move in the session record.

### Step 6: Commit (haiku)

Dispatch a haiku agent to stage and commit all orchestration log changes.

```
git add orchestration_log/
git commit -m "doc: session {YYYY-MM-DD} LEAVE protocol — session record + reference updates"
```

Commit only `orchestration_log/history/` and `orchestration_log/reference/`. The recon/ directory is gitignored and disposable; regenerate if needed.

### Step 7: Capture cost (orchestrator)

Run `/cost`. Cross-verify scope before trusting the number:
1. Wall time range matches this session.
2. No branching split the session (branched `/cost` covers only the branch).
3. No multi-session contribution inflates the number.

If scope checks pass, dispatch a haiku agent to write the VERBATIM `/cost` output to:

```
orchestration_log/history/{YYYY-MM-DD}/cost.md
```

The agent pastes `/cost` output as a fenced code block, prefixed by a one-line scope-verification note. The agent MUST NOT parse, reformat, summarize, or substitute placeholders — the verbatim output IS the artifact. The agent MUST NOT commit cost.md and MUST NOT embed the cost number inline in session.md.

NO commit. The file is gitignored per `**/cost.md` (Artifact Contract row A9). The Step 6 `git add orchestration_log/` silently skips cost.md because of this gitignore rule — the no-commit fact is enforced by the ignore pattern, not by the agent. Cost is operational data; stewardship lives outside git history.

Skip Step 7 entirely when the user directs no cost capture. Note `**Cost:** not captured this session (per user direction)` in the session record header and proceed without writing cost.md.

## Artifact Management

Four practices govern artifact hygiene during session close.

**Per-session artifact index.** Every `session.md` ends with an `## Artifacts` section listing committed files (with descriptions), recon files (gitignored, regenerable), and generated data (with regeneration commands). The recon index is especially valuable — recon files are gitignored and will be lost without it.

**Consolidation sweep.** Before close, sweep `reference/` for five flagged content classes:
- **Redundancy** — two files on the same topic. Merge.
- **Supersession** — a newer version exists. Delete the stale one.
- **Dead weight** — fully resolved or unreferenced. Delete. If a file is not discoverable from CLAUDE.md or a session.md, it is dead weight.
- **Undiscoverability** — not referenced anywhere. Add to the artifact map or delete.
- **Interface Specification** — function signatures, parameter lists, or CLI flag examples in reference docs. These decay within hours; the source code (type-annotated) plus `--help` is the source of truth. Remove or redirect to source files. Reference docs MUST NOT carry Interface Specifications (see Documentation Categories).

**No new files for existing concerns.** When information belongs to an existing file, extend that file. Separate files for the same concern drift immediately. The test: if updating requires touching two files, consolidate.

**Gitignore regenerables.** Any file regenerable from a command (`just test-all`, `just summary`) belongs in `.gitignore`. The command IS the artifact. Document the regeneration command in the artifact index. Exception: deliverables handed to stakeholders (PO reports in `history/`) are committed as point-in-time snapshots.

## Quality Gates

Before closing:

- [ ] Session record covers all phases that changed code, updated docs, or made decisions (including failures)
- [ ] Reference docs updated: codebase_state, deferred_items, conventions
- [ ] Function signatures read from actual code, not guessed
- [ ] Gold standard results documented if evaluation was run
- [ ] cost.md written at orchestration_log/history/${DATE}/cost.md (or skip explicitly noted in session record)
- [ ] Everything committed
- [ ] Recon files NOT committed (gitignored)
- [ ] Artifact index present in session.md
- [ ] Consolidation sweep completed
- [ ] Status Snapshots regenerated by measurement commands (verbatim output), not from session memory
- [ ] Any spec marked ready-for-implementation that was implemented this session has been archived to history
- [ ] Sessions that made architectural decisions have written both a decision narrative and an index row
