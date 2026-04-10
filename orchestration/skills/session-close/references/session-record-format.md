# Session Record Format

Required structure for `docs/orchestration_log/history/{YYYY-MM-DD}/session.md`.

## Header

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

Cost line: fill PLACEHOLDER after running `/cost`. Format: `[PLACEHOLDER - run /cost to fill]` until then.

## Required Sections

### Timeline

Chronological phases, anchored to git commits where possible. Each phase:

```markdown
### Phase N: {Name} ({HH:MM} -- {HH:MM})

{What happened. What was decided. What failed.}

**Commits:**
- {hash}: {message}
```

**Common phases agents miss when reconstructing from git:**
- Investigation/research phases (no commits)
- Failed attempts that were reverted (commits exist but context is lost)
- Conversations and decisions (never in git)
- Tool failures (MCP hangs, OOM, etc.)
- User corrections to orchestrator behavior

### Decision Log

Table of non-obvious decisions with outcomes:

```markdown
| Decision | Context | Rationale | Outcome |
|----------|---------|-----------|---------|
```

Include decisions that were:
- Reversals of prior approaches
- Choices between two valid options
- Architectural commitments that will shape future work
- Responses to failures

### Failure Log

Every process failure, not just bugs:

```markdown
| Failure | Root cause | Correction | Prevention |
|---------|-----------|------------|------------|
```

Include:
- OOM / resource failures
- Agent spec violations
- Tool failures (MCP hangs, rate limits)
- Skipped protocol steps (review, etc.)
- Wrong initial approaches that had to be reverted

### Quantitative Summary

```markdown
| Metric | Value |
|--------|-------|
| API time | {Xh Ym} |
| Wall time | {Xh Ym} |
| Git commits | {N} |
| Code changes | +{N} lines, -{M} lines |
| Tests | {N} (up from {M}, +{delta}) |
| Pyright errors | 0 |
| Agent dispatches | ~{N} |
| Cost | ${total} |
```

### Next Session Priorities

Ordered list of what to do first in the next session. Should connect to deferred_items.md.

## What Agents Get Wrong

Agents reconstruct from git history and file artifacts. They systematically miss:

1. **Research/investigation phases** — no commits, no artifacts
2. **Failed first attempts** — commits exist but context (why it failed) is lost
3. **Conversation-driven decisions** — never captured in any file
4. **Tool failures** — MCP hangs, OOM crashes don't appear in git
5. **User corrections** — "you're doing it wrong, fix it" moments
6. **Skipped protocol steps** — the failure to do the right thing isn't in git
7. **Correct numbers** — agents use file-derived data which may be stale
8. **Function signatures** — agents guess instead of reading actual code

The orchestrator must add all of the above after reviewing the agent draft.

## Backlinking to Raw Data

The session ID in the header links the frozen session record to the live raw data:

```
~/.claude-shared/projects/{slug}/{session-id}.jsonl
~/.claude-shared/projects/{slug}/{session-id}/subagents/
```

Future orchestrators can re-run metric extraction on the same raw data if the session record needs correction or the recon files were discarded.
