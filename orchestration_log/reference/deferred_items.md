# Deferred Items
Last updated: 2026-04-24

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
**Severity**: HIGH
**Description**: Agents dispatched with `isolation: "worktree"` receive an isolated git checkout, but their `Edit`/`Write` tools still resolve absolute filesystem paths normally. When a dispatch prompt cites target files by absolute path into the main repo (`/Users/ryzhakar/pp/claude-skills/...`), the agent's edits land in main rather than its worktree — silently. Observed in session 2026-04-24: dispatches A and C used absolute paths and edited main; dispatch B used relative paths and stayed isolated. The agents' return summaries cited their worktree paths as if work was isolated, but the worktrees were empty (auto-cleaned for "no changes") while main accumulated the diffs.

**Proposed remediation**: Add a convention to `conventions.md`: "Worktree dispatches MUST use only relative paths in the task body. Absolute paths into the main repo defeat isolation silently. Cite files as `plugin/skills/foo/SKILL.md`, never `/Users/.../plugin/skills/foo/SKILL.md`." Optionally extend instruction-writer agent's preflight to flag absolute paths in its incoming brief and refuse the dispatch.

**Evidence**: Session 2026-04-24, dispatches A and C. Dispatch reports at `orchestration_log/recon/2026-04-24/dispatches/{A-orchestration,C-qa-automation}.md` cite worktree paths that no longer exist; `git status` after the dispatches shows the edits in main's working tree.

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

### DI-7 — Platform-Induced Orchestrator CWD Drift (Undocumented)

**Date**: 2026-04-29
**Severity**: MEDIUM
**Description**: The orchestrator's CWD can shift into a worktree without explicit `cd` action by the orchestrator. agents-reference.md documents inherited subagent CWD behavior (a subagent starts in the main conversation's CWD; `cd` inside subagents does not persist) but does NOT document orchestrator-side platform-induced drift. Observed in session 2026-04-24 and confirmed as a class of failure distinct from operator-induced drift. Effect: CWD-relative shell operations misroute; subagents dispatched after drift inherit the wrong CWD.

**Proposed remediation**: Add a session-vagueness item to `orchestration_log/reference/agents-reference.md` Appendix B (open questions / observed platform behavior) describing the orchestrator-side drift. Cite the dev-orchestration SKILL.md "Worktree Discipline (Orchestrator Side)" subsection as the operational defense already in place. This is documentation work — separate dispatch.

**Evidence**: Session 2026-04-24 (orchestrator's CWD drifted into Dispatch B's worktree during diagnostic queries). Session 2026-04-29 (user confirmed platform-induced variant exists separately from operator-induced drift).
