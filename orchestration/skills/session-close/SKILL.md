---
name: session-close
description: This skill should be used when the user asks to "close the session", "do session paperwork", "write the session record", "execute the LEAVE protocol", "wrap up the session", or at the natural end of a development orchestration session. Governs the full session close-out workflow including agent-based metric extraction from raw session data on disk, session record authoring, reference document updates, cost capture, and VCS commit.
disable-model-invocation: true
---

# Session Close

Governs the LEAVE protocol for orchestration sessions. Produces durable institutional memory by combining objective data extracted from raw session files on disk with orchestrator context that only the active session possesses.

## Core Principle

**The orchestrator holds context no agent can reconstruct.** Agents extract objective data (metrics, git history, file changes) from disk. The orchestrator synthesizes that with the actual decisions made, failures encountered, and reasoning behind choices — then corrects the agents' reconstructions before committing.

Never delegate the final synthesis and correction to an agent. The orchestrator owns the session record.

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

Count unique `agentId` values across all JSONL files (excluding orchestrator ID), or count `Agent` tool_use blocks in orchestrator JSONL.

### Cost Formulas

| Tier | Input | Output | Cache Read | Cache Write | (per 1M tokens) |
|------|-------|--------|------------|-------------|-----------------|
| Opus | $15.00 | $75.00 | $1.50 | $3.75 | |
| Sonnet | $3.00 | $15.00 | $0.30 | $0.75 | |
| Haiku | $0.80 | $4.00 | $0.08 | $0.20 | |

Cost = sum of (tokens / 1M * rate) for each of the four token categories per tier.

### Cache Dominates Cost

In long sessions, `cache_read_input_tokens` can be 100-800x larger than direct `input_tokens`. The orchestrator's context window accumulates and is re-sent as cache every turn. This is why Opus dominates cost even when agents do most work — the orchestrator's long context is expensive to cache-read repeatedly.

## Session Record Format

### Header Template

```markdown
# Session: YYYY-MM-DD

**Orchestrator:** Claude Opus 4.6 (1M context)
**Session ID:** {session-id}          ← links to raw JSONL files
**Branch:** {git branch, if branched}  ← omit if main
**Duration:** {X}h {Y}m API, {Z}h {W}m wall
**Cost:** ${total} total (${opus} Opus, ${sonnet} Sonnet, ${haiku} Haiku)
**Code changes:** {N} lines added, {M} removed
**Outcome:** {1-2 sentence summary of what shipped}
```

The session ID links directly to `~/.claude-shared/projects/{slug}/{session-id}.jsonl`. Cost line: fill PLACEHOLDER after running `/cost`. Format: `[PLACEHOLDER - run /cost to fill]` until then.

### Required Sections

**Timeline** — chronological phases, anchored to git commits. Each phase: what happened, what was decided, what failed, commit hashes.

**Decision Log** — table: Decision | Context | Rationale | Outcome. Include reversals, choices between valid options, architectural commitments, responses to failures.

**Failure Log** — table: Failure | Root cause | Correction | Prevention. Include OOM/resource failures, agent spec violations, tool failures, skipped protocol steps, wrong initial approaches. The failure log is the most valuable part. Conventions are born from it.

**Quantitative Summary** — table: Metric | Value. API time, wall time, git commits, code changes, tests, pyright errors, agent dispatches, cost.

**Next Session Priorities** — ordered list connecting to `deferred_items.md`.

### What Agents Get Wrong

Agents reconstruct from git history and file artifacts. They systematically miss: research phases (no commits), failed first attempts (context lost), conversation-driven decisions, tool failures, user corrections, skipped protocol steps, stale numbers, guessed function signatures.

The orchestrator must add all of the above after reviewing the agent draft.

## LEAVE Protocol

The orchestrator executes in this order. Run Steps 1-4 in parallel. Step 5 requires orchestrator participation. Steps 6-7 are sequential.

### Step 1: Extract session metrics (haiku, background)

Dispatch a haiku agent to parse all JSONL files in the session directory. Agent writes to `docs/orchestration_log/recon/{YYYY-MM-DD}/session_metrics.md`.

Dispatch the agent with instructions to count:
- Unique agentId values (= subagents dispatched)
- Messages by model tier (haiku / sonnet / opus)
- Tool calls by tool name
- Token totals by model tier (input, output, cache_read, cache_creation)
- Timestamp range

Use `scripts/extract_metrics.py` for reliable parsing.

### Step 2: Extract git history (haiku, background)

Dispatch a haiku agent to extract the git log for the session period. Agent writes to `docs/orchestration_log/recon/{YYYY-MM-DD}/git_history.md`.

Commands to run:
- `git log --format="%ai %H %s" --since="{session-start-date}" --reverse`
- `git diff --stat {first-session-commit}..HEAD`

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

Run `/cost` command in Claude Code. Dispatch a haiku agent to fill the cost placeholder in the session record:

```
docs/orchestration_log/history/{YYYY-MM-DD}/session.md
# Find: [PLACEHOLDER - run /cost to fill]
# Replace with actual numbers
```

The agent commits with: `"doc: fill session {YYYY-MM-DD} cost data (${TOTAL} total)"`

## Quality Gates

Before closing:

- [ ] Session record covers all phases that changed code, updated docs, or made decisions (including failures)
- [ ] Reference docs updated: codebase_state, deferred_items, conventions
- [ ] Function signatures read from actual code, not guessed
- [ ] Gold standard results documented if evaluation was run
- [ ] Cost placeholder filled
- [ ] Everything committed
- [ ] Recon files NOT committed (gitignored)
