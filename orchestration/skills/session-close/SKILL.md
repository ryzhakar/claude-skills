---
name: session-close
description: >
  Governs the ARRIVE/WORK/LEAVE session lifecycle for orchestration sessions. Covers
  session start (reference doc ingestion), session work (convention adherence), and
  session close (metric extraction, session record, reference updates, cost capture, VCS commit).

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
| `reference/` | Living -- updated each session | What is true NOW |
| `history/` | Frozen -- never edited after session ends | What happened THEN |
| `recon/` | Disposable -- gitignored, regenerate | Raw scouting data |

Living documents that are not updated become lies. Frozen documents that get edited destroy the historical record. Disposable documents that are not gitignored bloat the repository.

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

## Session Record Format

### Header Template

```markdown
# Session: YYYY-MM-DD

**Orchestrator:** Claude Opus 4.6 (1M context)
**Session ID:** {session-id}          ← links to raw JSONL files
**Branch:** {git branch, if branched}  ← omit if main
**Duration:** {X}h {Y}m API, {Z}h {W}m wall
**Cost:** ${total} (from /cost, scope-verified)
**Code changes:** {N} lines added, {M} removed
**Outcome:** {1-2 sentence summary of what shipped}
```

The session ID links directly to `~/.claude-shared/projects/{slug}/{session-id}.jsonl`. Cost line: fill PLACEHOLDER after running `/cost`. Format: `[PLACEHOLDER - run /cost to fill]` until then. Cross-verify `/cost` scope before filling (see Cost Source section).

### Required Sections

**Timeline** — chronological phases, anchored to git commits. Each phase: what happened, what was decided, what failed, commit hashes.

**Decision Log** — table: Decision | Context | Rationale | Outcome. Include reversals, choices between valid options, architectural commitments, responses to failures.

**Failure Log** — table: Failure | Root cause | Correction | Prevention. Include OOM/resource failures, agent spec violations, tool failures, skipped protocol steps, wrong initial approaches. The failure log is the most valuable part. Conventions are born from it.

**Quantitative Summary** — table: Metric | Value. API time, wall time, git commits, code changes, tests, pyright errors, agent dispatches, cost.

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

The orchestrator executes in this order. Run Steps 1-4 in parallel. Step 5 requires orchestrator participation. Steps 6-7 are sequential.

### Step 1: Extract session metrics (haiku, background)

Dispatch a haiku agent to parse all JSONL files in the session directory. Agent writes to `docs/orchestration_log/recon/{YYYY-MM-DD}/session_metrics.md`.

Dispatch the agent with instructions to extract:
- **Agent counts by model tier** — how many agents ran on haiku, sonnet, opus (from `message.model`)
- **Agent counts by type** — how many of each `subagent_type` (e.g., 5 implementers, 3 spec-reviewers, 15 research agents). From agent metadata or `subagent_type` field
- Messages by model tier (haiku / sonnet / opus)
- Tool calls by tool name
- Token totals by model tier (input, output, cache_read, cache_creation)
- Timestamp range

Report the two agent groupings as separate tables.

Use `scripts/extract_metrics.py` for reliable parsing.

Step 1 provides agent counts and message volumes. NEVER derive cost from JSONL. See Cost Source section — `/cost` is the only trusted source. Step 7 captures cost.

### Step 2: Extract git history (haiku, background)

Dispatch a haiku agent to extract the git log for the session period. Agent writes to `docs/orchestration_log/recon/{YYYY-MM-DD}/git_history.md`.

Commands to run:
- `git log --format="%ai %H %s" --since="{session-start-date}" --reverse`
- `git diff --stat {first-session-commit}..HEAD`

### Steps 3-4: Conditional Drafting

**Gate:** If reference docs were updated within the current session (agents already ran LEAVE steps, or orchestrator edited reference docs directly), skip Steps 3-4. The orchestrator reviews existing docs directly in Step 5 instead of reviewing agent drafts. This prevents redundant agent dispatches when docs are already current.

### Step 3: Draft session record (sonnet, background)

Dispatch a sonnet agent to draft `docs/orchestration_log/history/{YYYY-MM-DD}/session.md`. Point the agent at:
- `docs/orchestration_log/history/` — prior session records for format reference
- The git history recon file (when available)
- `docs/orchestration_log/reference/` — current reference docs for state context

The agent must use the header template and required sections defined above. Include the session ID for backlinking.

The agent reconstructs from artifacts. **It will miss things and get things wrong.** The orchestrator corrects in Step 5.

### Step 4: Draft reference doc updates (sonnet, background)

Dispatch a sonnet agent to update the three living reference documents:
- `docs/orchestration_log/reference/codebase_state.md` — update from actual code (`grep`, `wc -l`, pytest)
- `docs/orchestration_log/reference/deferred_items.md` — add new findings, remove resolved items
- `docs/orchestration_log/reference/conventions.md` — add patterns discovered this session

The agent must read actual code — not guess at function signatures.

### Step 5: Review and correct drafts (orchestrator, after Steps 1-4 complete)

Read the draft session record. Correct:
- Missing phases (agents reconstruct from git, they miss non-code work)
- Wrong numbers (agents may use stale data from earlier in session)
- Missing failures (agents omit failures that are not in git history)
- Wrong attribution (which decisions were made vs. which were imposed)
- Guessed function signatures (agent must read actual code, not infer)

This step cannot be delegated. The orchestrator has context no agent can access.

### Step 6: Commit (haiku)

Dispatch a haiku agent to stage and commit all orchestration log changes.

```
git add docs/orchestration_log/
git commit -m "doc: session {YYYY-MM-DD} LEAVE protocol — session record + reference updates"
```

Commit only `docs/orchestration_log/history/` and `docs/orchestration_log/reference/`. The recon/ directory is gitignored and disposable; regenerate if needed.

### Step 7: Capture cost (orchestrator)

Run `/cost`. Before filling the placeholder, cross-verify scope:
1. Wall time range matches this session.
2. No branching split the session (branched `/cost` covers only the branch).
3. No multi-session contribution inflates the number.

If scope checks pass, dispatch a haiku agent to fill the cost placeholder in:

```
docs/orchestration_log/history/{YYYY-MM-DD}/session.md
# Find: [PLACEHOLDER - run /cost to fill]
# Replace with actual /cost number and note "scope-verified"
```

The agent commits with: `"doc: fill session {YYYY-MM-DD} cost data (${TOTAL} total)"`

## Artifact Management

Four practices govern artifact hygiene during session close.

**Per-session artifact index.** Every `session.md` ends with an `## Artifacts` section listing committed files (with descriptions), recon files (gitignored, regenerable), and generated data (with regeneration commands). The recon index is especially valuable — recon files are gitignored and will be lost without it.

**Consolidation sweep.** Before close, sweep `reference/` for redundancy (two files on same topic — merge), supersession (newer version exists — delete stale), dead weight (fully resolved — delete), and undiscoverability (not referenced anywhere — add to artifact map or delete). If a file is not discoverable from CLAUDE.md or a session.md, it is dead weight.

**No new files for existing concerns.** When information belongs to an existing file, extend that file. Separate files for the same concern drift immediately. The test: if updating requires touching two files, consolidate.

**Gitignore regenerables.** Any file regenerable from a command (`just test-all`, `just summary`) belongs in `.gitignore`. The command IS the artifact. Document the regeneration command in the artifact index. Exception: deliverables handed to stakeholders (PO reports in `history/`) are committed as point-in-time snapshots.

## Quality Gates

Before closing:

- [ ] Session record covers all phases that changed code, updated docs, or made decisions (including failures)
- [ ] Reference docs updated: codebase_state, deferred_items, conventions
- [ ] Function signatures read from actual code, not guessed
- [ ] Gold standard results documented if evaluation was run
- [ ] Cost placeholder filled
- [ ] Everything committed
- [ ] Recon files NOT committed (gitignored)
- [ ] Artifact index present in session.md
- [ ] Consolidation sweep completed
