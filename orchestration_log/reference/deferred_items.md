# Deferred Items
Last updated: 2026-04-29

Known defects and improvement opportunities that are tracked but not immediately scheduled. Update severity when context changes. Remove entries when resolved.

---

## Format

Each entry:
- **Title** — Short, searchable label
- **ID** — Sequential (DI-N)
- **Date** — When surfaced
- **Severity** — HIGH / MEDIUM / LOW
- **Description** — What the problem is, why it matters
- **Proposed remediation** — Concrete next action
- **Evidence** — File path or URL

---

## Open Items

### DI-1 — Manifesto Repo Path Unreliable in Agent Binding Preambles

**Date**: 2026-04-20
**Severity**: HIGH
**Description**: `/tmp/claude-manifesto-repo/LLM_MANIFESTOS/manifestos/Manifesto, first-principles - "break the mold".md` was absent for multiple scout agents during the 2026-04-17 wave. At least 4 agents fell back to fetching from the upstream raw GitHub URL before proceeding. The `ensure-repo.sh` script in the manifesto plugin is expected to clone this repo, but the clone is either not persisting across agent contexts or the path is not being created correctly. Every agent that hits this gap must curl upstream, adding latency and a network dependency.

**Proposed remediation**: Inspect `manifesto/hooks/ensure-repo.sh` (or equivalent). Verify it writes to `/tmp/claude-manifesto-repo/LLM_MANIFESTOS/` and that the manifesto file name (with space and quotes in path) is handled correctly. Fix or document the fallback as the intended behavior. Update binding preambles to always include the fallback as a required step, not an optional recovery.

**Evidence**: `orchestration_log/recon/2026-04-17/TIDY-REPORT.md` (Anomalies: none — but upstream fetch was observed in agent logs); session manifesto binding preamble in task instructions (2026-04-17 wave). The task instruction itself says "Try local; if absent, fetch from upstream" — confirming this is a known failure pattern.

---

### DI-2 — 45 Citations in agents-reference.md Are URL-Only (No Section Anchor)

**Date**: 2026-04-20
**Severity**: MEDIUM
**Description**: 45 of 298 citations in `orchestration_log/reference/agents-reference.md` are URL-only (`[slug](url)`) because the automated citation rewriter could not grep-match the quote in the source file. Root causes: (1) quotes contain backtick `<placeholder>` syntax that doesn't match verbatim source; (2) quotes from callout boxes / admonitions that Mintlify renders differently from body prose; (3) prose paraphrases attributed with em-dash but not verbatim. These citations are correct but lack the section anchor that makes them actionable for readers.

**Proposed remediation**: Run a fuzzy-match pass over the 45 unmatched citations. Strategy: for each `url_only_quote_unmatched` entry, fetch the source page (`.md` URL trick), strip markdown, normalize whitespace, run trigram or edit-distance match against quote fragments, then look up the nearest heading in `heading-index.tsv`. The citation-rewrite tooling at `orchestration_log/recon/2026-04-17/agents-v2/synthesis/citation-rewrite/` provides the index files needed. Expected improvement: push deep-link rate from 78% toward 90%+.

**Evidence**: `orchestration_log/recon/2026-04-17/agents-v2/synthesis/citation-rewrite/REPORT.md` — "url_only_quote_unmatched: 45, Quote present but grep failed to match in source."

---

_(DI-3 removed: the CLI/SDK CLAUDE.md inheritance contradiction lives as MD-19 in `agents-reference.md` Appendix A and §7. Tracking it here would duplicate the reference manual's own open-question registry.)_

---

### DI-4 — Worktree Isolation Defeated by Absolute Paths in Dispatch Prompts

**Date**: 2026-04-24
**Status**: PARTIALLY RESOLVED 2026-04-29 (agent-side defense in dev-discipline 1.4.2; convention codified). Remaining: instruction-writer-side preflight to flag absolute paths in incoming briefs.
**Severity**: HIGH (now MEDIUM in residual form)
**Description**: Agents dispatched with `isolation: "worktree"` receive an isolated git checkout, but their `Edit`/`Write` tools still resolve absolute filesystem paths normally. When a dispatch prompt cites target files by absolute path into the main repo (`/Users/ryzhakar/pp/claude-skills/...`), the agent's edits land in main rather than its worktree — silently. Observed in session 2026-04-24: dispatches A and C used absolute paths and edited main; dispatch B used relative paths and stayed isolated. Recurred 2026-04-29 in dispatch E (one path leaked despite explicit "RELATIVE PATHS ONLY" in brief).

**Resolution landed**:
- dev-discipline 1.4.2 implementer/spec-reviewer/code-quality-reviewer agents now defensively re-root all incoming paths (strip repo-root prefix, resolve relative to own worktree, surface re-rooted paths in status). Defense in depth — even if orchestrator prompts leak absolute paths, agents re-root transparently.
- `conventions.md` Worktree Dispatches: Relative Paths Only section codifies the orchestrator-side discipline.

**Remaining remediation**: instruction-writer agent could preflight its incoming brief — scan for `/Users/.../plugin/...` patterns and refuse the dispatch (or warn) before applying. Would close the orchestrator-side gap completely. Low-priority since agent-side defense now catches the failure.

**Evidence**: Session 2026-04-24, dispatches A and C; session 2026-04-29 dispatch E. Resolution evidence: dispatch E's edits to dev-discipline agent files (commit 6515da5).

---

### DI-5 — Drift-Prevention Linter for Artifact Contract Tables

**Date**: 2026-04-24
**Severity**: MEDIUM
**Description**: Three plugins now carry inline `## Artifact Contract` tables in their orchestrator skills (orchestration/session-close, dev-discipline/dev-orchestration, qa-automation/qa-orchestration — landed session 2026-04-24). The tables are the canonical source for paths, producers, consumers, format, and required-status. They were added precisely because path scatter across agent and orchestrator files produced silent drift. Without an audit-time check, the same drift will recur as files are edited independently.

**Proposed remediation**: Write `just audit-artifacts` (or equivalent shell pipeline) that, for each multi-skill plugin's orchestrator skill: (1) parses the `## Artifact Contract` table, (2) for each row, greps the producer agent body for the declared path, (3) greps the consumer file for the declared path, (4) reports mismatches. Wire to pre-commit hook. Block commits that introduce drift. ~50 lines of shell or Python; reuses the markdown-table parsing approach from session 2026-04-17's deep-link citation rewrite (`orchestration_log/recon/2026-04-17/agents-v2/synthesis/citation-rewrite/`).

**Evidence**: Session 2026-04-24 audit at `orchestration_log/recon/2026-04-24/artifact-ownership-audit/` (3 reports, 25 gaps total — all stem from path-scatter). Inline contract tables now present in: `orchestration/skills/session-close/SKILL.md`, `dev-discipline/skills/dev-orchestration/SKILL.md`, `qa-automation/skills/qa-orchestration/SKILL.md`.

---

### DI-6 — Abandoned Locked Worktree

**Date**: 2026-04-24
**Severity**: LOW
**Description**: `git worktree list` shows `.claude/worktrees/agent-a4955c76` (branch `worktree-agent-a4955c76`, locked, at commit `e417a6f` — a Feb 2026 commit). Predates session 2026-04-24. Lock prevents auto-cleanup. Status of any work it contains is unknown.

**Proposed remediation**: Inspect the worktree's working tree and branch. If empty and stale: `git worktree remove -f -f` and `git branch -D`. If it contains work: surface to the user before destroying.

**Evidence**: `git worktree list` output, session 2026-04-24.

---

### DI-8 — `extract_metrics.py` Carries Dead-Code Cost Computation

**Date**: 2026-04-29
**Severity**: LOW
**Description**: `orchestration/skills/session-close/scripts/extract_metrics.py` includes `COST_PER_1M`, `compute_cost`, and a "Total estimated cost" row in its output. Session-close's Cost Source section explicitly forbids JSONL-derived cost numbers ("NEVER derive cost from JSONL — JSONL double-counts subagent internals"). The script's cost-computation logic is dead code per the convention — its output is structurally untrusted and unused by any LEAVE step. As of orchestration 3.2.3, cost capture lives entirely in gitignored `cost.md` written from `/cost` output, not from JSONL parsing.

**Proposed remediation**: Strip `COST_PER_1M`, `compute_cost`, and the cost row + cost column from the script's output. The metrics report stays useful (token counts by tier, agent counts by tier, tool calls, message counts). Removing the cost lines aligns the script with the documented Cost Source rule and prevents future readers from mistaking the JSONL-derived number for a trusted figure.

**Evidence**: `orchestration/skills/session-close/scripts/extract_metrics.py` lines 21, 41-42, 112-113, 128, 133, 149, 153, 158. Session-close `### Cost Source` section (post-3.2.3 version) explicitly prohibits JSONL-derived cost.

---

### DI-7 — Platform-Induced Orchestrator CWD Drift (Undocumented)

**Date**: 2026-04-29
**Severity**: MEDIUM
**Description**: The orchestrator's CWD can shift into a worktree without explicit `cd` action by the orchestrator. agents-reference.md documents inherited subagent CWD behavior (a subagent starts in the main conversation's CWD; `cd` inside subagents does not persist) but does NOT document orchestrator-side platform-induced drift. Observed in session 2026-04-24 and confirmed as a class of failure distinct from operator-induced drift. Effect: CWD-relative shell operations misroute; subagents dispatched after drift inherit the wrong CWD.

**Proposed remediation**: Add a session-vagueness item to `orchestration_log/reference/agents-reference.md` Appendix B (open questions / observed platform behavior) describing the orchestrator-side drift. Cite the dev-orchestration SKILL.md "Worktree Discipline (Orchestrator Side)" subsection as the operational defense already in place. This is documentation work — separate dispatch.

**Evidence**: Session 2026-04-24 (orchestrator's CWD drifted into Dispatch B's worktree during diagnostic queries). Session 2026-04-29 (user confirmed platform-induced variant exists separately from operator-induced drift).
