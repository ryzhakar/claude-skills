# Deferred Items
Last updated: 2026-04-20

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
