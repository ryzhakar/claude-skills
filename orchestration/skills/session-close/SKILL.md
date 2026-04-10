---
name: session-close
description: This skill should be used when the user asks to "close the session", "do session paperwork", "write the session record", "execute the LEAVE protocol", "wrap up the session", or at the natural end of a development orchestration session. Governs the full session close-out workflow including agent-based metric extraction from raw session data on disk, session record authoring, reference document updates, cost capture, and VCS commit.
version: 1.0.0
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

Each JSONL line is a JSON object with:
- `message.model` — model used (`claude-opus-4-6`, `claude-sonnet-4-5-*`, `claude-haiku-4-5-*`)
- `message.content[]` — array of text/tool_use/tool_result blocks
- `message.usage` — token counts: `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`
- `agentId` — identifies which agent produced the message
- `timestamp` — ISO 8601

See `references/data-schema.md` for full field reference and parsing patterns.

## LEAVE Protocol

Execute in this order. Steps 1-4 run in parallel. Step 5 requires orchestrator participation. Steps 6-8 are sequential.

### Step 1: Extract session metrics (haiku, background)

Dispatch a haiku agent to parse all JSONL files in the session directory. Agent writes to `docs/orchestration_log/recon/{YYYY-MM-DD}/session_metrics.md`.

Brief the agent to count:
- Unique agentId values (= subagents dispatched)
- Messages by model tier (haiku / sonnet / opus)
- Tool calls by tool name
- Token totals by model tier (input, output, cache_read, cache_creation)
- Timestamp range

Use `scripts/extract_metrics.py` for reliable parsing. See `references/data-schema.md` for field names and cost formulas.

### Step 2: Extract git history (haiku, background)

Dispatch a haiku agent to extract the git log for the session period. Agent writes to `docs/orchestration_log/recon/{YYYY-MM-DD}/git_history.md`.

Commands to run:
- `git log --format="%ai %H %s" --since="{session-start-date}" --reverse`
- `git diff --stat {first-session-commit}..HEAD`
- `find matchtuner tests -name "*.py" | wc -l` and `wc -l matchtuner/*.py`
- `uv run python -m pytest tests/ --co -q 2>&1 | tail -1`

### Step 3: Draft session record (sonnet, background)

Dispatch a sonnet agent to draft `docs/orchestration_log/history/{YYYY-MM-DD}/session.md`. Point the agent at:
- `docs/orchestration_log/history/` — prior session records for format reference
- The git history recon file (when available)
- `docs/orchestration_log/reference/` — current reference docs for state context

The agent reconstructs from artifacts. **It will miss things and get things wrong.** The orchestrator corrects in Step 5.

See `references/session-record-format.md` for required sections and format.

### Step 4: Draft reference doc updates (sonnet, background)

Dispatch a sonnet agent to update the three living reference documents:
- `docs/orchestration_log/reference/codebase_state.md` — read actual code (`grep -n "^def "`, `wc -l`, pytest count)
- `docs/orchestration_log/reference/deferred_items.md` — add new findings, remove resolved items
- `docs/orchestration_log/reference/conventions.md` — add patterns discovered this session

The agent must read actual code — not guess at function signatures.

### Step 5: Orchestrator review and correction (orchestrator)

Read the draft session record. Correct:
- Missing phases (agents reconstruct from git, they miss non-code work)
- Wrong numbers (agents may use stale data from earlier in session)
- Missing failures (agents omit failures that aren't in git history)
- Wrong attribution (which decisions were made vs. which were imposed)
- Guessed function signatures (agent must read actual code, not infer)

This step cannot be delegated. The orchestrator has context no agent can access.

### Step 6: Commit (haiku)

Dispatch a haiku agent to stage and commit all orchestration log changes.

```
git add docs/orchestration_log/
git commit -m "doc: session {YYYY-MM-DD} LEAVE protocol — session record + reference updates"
```

Do NOT commit recon/ data — it is gitignored.

### Step 7: Capture cost (orchestrator)

Run `/cost` command in Claude Code. Dispatch a haiku agent to fill the cost placeholder in the session record:

```
docs/orchestration_log/history/{YYYY-MM-DD}/session.md
# Find: [PLACEHOLDER - run /cost to fill]
# Replace with actual numbers
```

The agent commits with: `"doc: fill session {YYYY-MM-DD} cost data (${TOTAL} total)"`

### Step 8: Note on recon data

The `docs/orchestration_log/recon/` directory is gitignored — session metrics and raw git history are disposable. They exist only to assist the session close-out. Regenerate if needed.

## Backlinking Convention

Every session record header must include the session ID for traceability:

```markdown
# Session: YYYY-MM-DD

**Orchestrator:** Claude Opus 4.6 (1M context)
**Session ID:** {session-id from JSONL filenames}
**Branch:** {git branch if session was branched}
**Duration:** {API time} API, {wall time} wall
**Cost:** ${total} total (${opus} Opus, ${sonnet} Sonnet, ${haiku} Haiku)
```

The session ID links directly to the raw JSONL files in `~/.claude-shared/projects/{slug}/{session-id}.jsonl`.

## Quality Gates

Before closing:

- [ ] Session record covers all major phases (including failures)
- [ ] Reference docs updated: codebase_state, deferred_items, conventions
- [ ] Function signatures read from actual code, not guessed
- [ ] Gold standard results documented if evaluation was run
- [ ] Cost placeholder filled
- [ ] Everything committed
- [ ] Recon files NOT committed (gitignored)

## Additional Resources

- **`references/data-schema.md`** — JSONL field reference, model tier detection, cost formulas
- **`references/session-record-format.md`** — Required sections, format template, common omissions
- **`scripts/extract_metrics.py`** — Reliable parser for session JSONL files
