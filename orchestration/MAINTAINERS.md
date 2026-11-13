# Orchestration Plugin — Maintainer Guide

Implicit decisions and structural invariants for anyone modifying skills in this plugin.

## Skill Hierarchy

```
agentic-delegation          <-- root (the universal framework)
  |
  +-- research-tree         <-- domain extension: research workflows

orchestration-economics     <-- sibling root: the cost of every act; model and effort
```

agentic-delegation is the parent; research-tree is a domain extension. orchestration-economics stands beside agentic-delegation, not under it: agentic-delegation and every domain extension read it whole before the session's first launch, continuation, or stop of an agent, and again after each compaction. This is not a flat collection of independent skills.

**dev-orchestration moved to the dev-discipline plugin in v3.0.0 and became `dev-cycle` in the dev-cycle plugin on 2026-10-06.** It lives with its agents (spec-capturer, implementer, spec-reviewer, code-quality-reviewer). The cross-plugin prerequisite remains — dev-cycle gates on reading agentic-delegation and orchestration-economics first.

## The Hard Prerequisite Rule

Domain extensions MUST gate on the parent.

When research-tree is loaded, the model MUST read agentic-delegation's and orchestration-economics's SKILL.md first. Not optional. Not "if available." A hard gate. The parent establishes the decomposition patterns, the prompt anatomy, the execution patterns, and the quality governance; orchestration-economics establishes the cost of every act and the choice of model and effort. Domain skills assume all of this is already internalized.

Cross-plugin domain extensions (dev-cycle in the dev-cycle plugin) follow the same rule — they gate on reading agentic-delegation and orchestration-economics before proceeding. The gate is a content dependency, not a packaging dependency.

## Composition Principles

### Cached Derivations, Not Overrides

When the parent's reasoning already reaches a conclusion for a specific domain, the domain skill caches that conclusion as shorthand. It does not override the parent.

Model and effort are never cached derivations. No skill in this plugin, or in a domain extension, carries a tier table, a default model, or a model assigned to a role; each chooses model and effort per act by orchestration-economics.

If a domain skill appears to contradict the parent, one of two things is true:
1. The domain skill is wrong (most likely).
2. The domain has a justified deviation that must be explicitly acknowledged, traced to the parent rule it deviates from, and explained.

Silent divergence is a bug.

### Delta-Only Content

Domain skills contain ONLY what the parent does not cover:
- research-tree adds: phased research structure, need-driven organization, re-research protocols.
- dev-cycle (the dev-cycle plugin) adds: the Plan-Implement-Review-Fix loop, status-driven branching, TDD gates, debugging escalation, multi-unit integration.

If the parent already defines a pattern (speculative-parallel, fan-out-by-concern, map-reduce, prompt anatomy), the domain skill references it. It does not restate it. Not even as a summary.

**Why:** One source of truth. When the parent changes, domain skills automatically benefit. Restated copies silently diverge. Derivations break loudly.

### Reference Files Follow the Same Rule

Reference docs in domain skills (e.g., `agent-dispatch.md`, `lifecycle-loops.md`) contain domain-specific content only. If a reference file mostly restates the parent's content with minor domain adjustments, it should be reduced to the delta or removed.

## Cross-Plugin References

### Same Plugin (orchestration internals)

Always direct references. No "if available" guards. No fallback branches.

### External Plugins (e.g., dev-discipline)

dev-cycle lives in the dev-cycle plugin alongside its agents. No cross-plugin agent references needed for that skill.

For other cross-plugin references (e.g., a future domain extension that needs agents from another plugin), the pattern remains:

1. Reference the preferred agent by name.
2. If absent, recommend installing the plugin.
3. If installation isn't happening immediately, a single sentence fallback suffices.
4. No full fallback prompt templates. Those duplicate agent definitions and diverge silently.

## The Orchestrator Contract

These invariants apply to ALL orchestration skills in this plugin.

### What the Orchestrator Does

- Reads status codes from completion summaries
- Pattern-matches on metadata shape (contradictions between summaries, anomalies, extraordinary claims, suspiciously short reports)
- Routes: maps status to next dispatch action via deterministic state machine
- Dispatches agents with precise, minimal prompts

### What the Orchestrator Does NOT Do

- Read implementation files, source code, or full agent reports
- Perform content-level analysis (classifying concerns, diagnosing root causes, evaluating trade-offs)
- Write code
- Debug failed agents by tracing their reasoning

Any analysis beyond reading a status code is itself work that must be re-delegated to agents, preferably in parallel.

**Stated exceptions only.** The orchestrator never reads or edits a product file. It writes its own prompt files and records with `Write`, takes the looks agent-conduct's check-back prescribes (`tail -n 1` only on a background command's output file), and runs one plain `rm` on absolute paths agents list as left behind. No other file touch exists.

### Communication Model

Agents communicate through artifacts on disk. The orchestrator routes via completion summaries.

What "artifact on disk" means varies by domain:
- **Research:** structured report files in a research directory
- **Dev:** changed source files, inspectable via git diff
- **Both:** the completion summary is the routing signal; the artifact is the substance

The orchestrator never relays content between agents. It provides file paths. Agents read files.

## Quality Governance

### The Parent's Governance

agentic-delegation defines general quality patterns: re-launch (don't debug), contradiction resolution (dispatch verification agents), spot-checking (sample-verify large batches). These are the default for any orchestration workflow.

### Domain Subsumption

Domain skills may define more structured quality gates that subsume the parent's general patterns for that domain:
- dev-cycle's two-stage review (in the dev-cycle plugin; the orchestrator tracks owed reviews) subsumes the parent's general patterns for dev work.
- research-tree's re-research at higher fidelity with fresh-eyes isolation subsumes the parent's contradiction resolution for research work.

The parent's patterns remain authoritative for any orchestration context not covered by a domain skill's specific gates.

## Isolation Principle — When It Applies

agentic-delegation's isolation principle ("agents forming opinions must not see other agents' opinions") applies to **parallel agents independently evaluating the same question**.

It does NOT apply to:
- **Sequential pipeline stages** where one agent verifies another's work (implementer -> reviewer -> fixer). These are adversarial verification chains.
- **Re-research** where higher-fidelity agents re-evaluate lower-fidelity findings. These get raw sources, not prior opinions — isolation is achieved by input design, not by hiding the prior agent's existence.

## Decomposition Units

Each domain has natural decomposition units. Do not force cross-domain mappings.

| Domain | Natural unit | Granularity heuristic |
|--------|-------------|----------------------|
| General (parent) | Time and output size | 30-120s, 20-200 lines of output |
| Research | Knowledge surface segment | One index category, one entity, one source |
| Dev | Files and testable behaviors | 1-3 files, independently testable, 2-10 minutes |

## Adding a New Domain Skill

When creating a new domain extension:

1. It MUST gate on reading agentic-delegation and orchestration-economics first.
2. Content is delta-only. Reference the parent for shared patterns.
3. Define domain-specific decomposition units if the parent's don't fit.
4. Define domain-specific quality gates if the parent's general governance is insufficient. Domain gates subsume, not layer.
5. Cached derivations of the parent's reasoning are encouraged as shorthand. Trace each to the parent rule it derives from.
6. Cross-plugin references use the hard-preference pattern (prefer, recommend install, succinct fallback).

## orchestration-economics Figure Provenance

Every figure in `skills/orchestration-economics/SKILL.md` sits in `<study-the-demonstrations>`; atoms and mechanics carry none. Each figure is a dated reading or arithmetic on one. The estafette project's lead session (claude-fable-5-2) and its agents took every reading on 2026-11-12: owner's Mac, Claude Code 2.1.322, session `73b37e7c`.

Path keys:
- `R/` = the tracked provenance copy, `orchestration_log/reference/economics-provenance/`; its `INDEX.md` maps each original path to its copy. Ledger = `R/records/spec-orchestration-economics-ingredients-2026-11-12.md`. Journal = `R/records/journal-2026-11-12-extract.md`.
- `R/estafette-just/` holds copies of the estafette repo's `just/` files. `usage-params.json` and `usage-prices.json` carry each figure with its `source`, `kind`, and `date`. `usage.py` and `usage.just` are the `just usage::*` recipes named below; they run in the estafette repo.
- `B/` = the handover bundle, `orchestration_log/recon/2026-11-13/extract/orchestration-economics/orchestration-economics-handover/` (gitignored; owner's machine). Only paid sources stay cited here.

`B/research/raw/` holds third-party captures: 22 pages of a paid SemiAnalysis article (`research-limit-mapping-semianalysis/pages/`), Artificial Analysis model pages, Anthropic docs. Cite them by path. NEVER copy their pages or text into this repo.

| Figure class (values in the skill) | Source | Taken | Method | Measured by | Refresh |
|---|---|---|---|---|---|
| Capability: opus 0.313 / 0.566 / 0.596; sonnet 0.207 / 0.439 / 0.636; haiku max 0.328; fable low 0.545, high and max 0.596 | Artificial Analysis, Terminal-Bench 4.0 (Intelligence Index v5.0.1), page data of `https://artificialanalysis.ai/models/claude-fable-5-1`, one record per variant. Extract: `B/research/raw/extract-pairs-reach-appetite/pairs.json`; `R/estafette-just/usage-params.json` `per_attempt.<model>.<effort>.capability` | Fetched 2026-11-12; AA's run date per record: source unrecorded | pass@1, 66 tasks × 3 repeats, one run per variant, Anthropic first-party endpoint; field `score` parsed from the JSON records by `aarec.py` | AA ran; estafette opus agent `extract-pairs-reach-appetite` (effort high) extracted; lead's `R/derive/check_pairs_against_raw.py` found all 36 cells in the raw page | Refetch the page; rebuild `pairs.json` by `R/research/briefs/extract-pairs-reach-appetite.md`; rerun `check_pairs_against_raw.py` |
| Appetite: opus 37,782 / 100,178 / 252,948 tokens | Same records; `...appetite_k` | Fetched 2026-11-12 | Field `outputTokensPerTask`, Terminal-Bench 4.0 | As capability | As capability |
| Dollars an attempt: opus 2.08 / 5.12 / 13.11; sonnet 1.28 / 2.19 / 12.65; haiku max 0.65; fable low 4.34 | Same records; `...attempt_dollars` | Fetched 2026-11-12 | Field `costPerTask`; what AA counts in it (its harness's caching): source unrecorded | As capability | As capability |
| Generation speed and time: opus 5.9 / 15.8 / 36.5 min; haiku max 22.6; sonnet max 43.7; fable low 9.1 | Same records, `headline.outputSpeed`; `...generation_speed_tokens_per_second` | Fetched 2026-11-12 | Output tokens ÷ total request time incl. time to first token, Anthropic first-party endpoint, AA's mean over its past 5 days; time = appetite ÷ speed | AA measured; `R/derive/demonstration_figures.py` divided | As capability; rerun `demonstration_figures.py` |
| Token prices: output, intake (5-minute, 1-hour), carry per model; ratios 100 and 200 carried tokens per output token, 1.6× intake at 1 hour, 25 / 50 / 40 / 80 steps per cold start | Anthropic, `https://platform.claude.com/docs/en/about-claude/pricing.md`, "Model pricing" table; `R/estafette-just/usage-prices.json` | Fetched 2026-11-12 | Table rows quoted; ratios derived | Anthropic published; estafette sonnet agent `research-token-prices` fetched (`R/research/reports/research-token-prices.md`) | Refetch; update `usage-prices.json` and its `fetched` date; rerun `demonstration_figures.py` |
| TTL: 5 minutes for agents, 1 hour for the main session | `https://code.claude.com/docs/en/prompt-caching.md` ("Which TTL each request gets", "Subagents and the cache"); session transcripts; `R/estafette-just/usage-params.json` `ttl_seconds` | 2026-11-12 | Docs quoted; TTL split (`ephemeral_1h_input_tokens`) of every cache write counted over 493 agent transcripts and the lead's | Estafette sonnet agents `research-token-prices` and `research-subagent-cache-lifetime` (effort low); lead's script | Refetch the doc; read the TTL column of `just usage::inflight` on fresh launches |
| Usage-limit windows: five-hour, seven-day, monthly | `https://code.claude.com/docs/en/statusline.md` (`rate_limits.five_hour`, `rate_limits.seven_day`, since Claude Code 2.1.80); `https://code.claude.com/docs/en/costs.md`; monthly: SemiAnalysis (next row) | Fetched 2026-11-12 | Docs quoted; live readings by `R/estafette-just/usage.py capture`, run by the `statusLine` command every 60 s | Estafette sonnet agent `research-usage-introspection` (`R/research/reports/research-usage-introspection.md`) | Refetch both pages; `just usage::limits` |
| Limit weights, Opus 5.5 on Claude Max 20x, percent of the monthly limit per million tokens: output 0.223, 5-minute intake 0.056, carry 0.0011; `200 : 50 : 1` | SemiAnalysis, "Anthropic Subscriptions Offer 5x+ More Value Than OpenAI", Andrew Megalaa, Max Kan, Dylan Patel, page 10; `https://newsletter.semianalysis.com/p/anthropic-subscriptions-offer-5x` (paid); `R/estafette-just/usage-params.json` `limit_weight_percent_per_million_tokens` | Published 2026-10-05; read 2026-11-12 | SemiAnalysis's own measurement, described at `B/research/reports/research-limit-mapping-semianalysis.md:22` | SemiAnalysis measured; estafette sonnet agent `research-limit-mapping-semianalysis` extracted; opus agent `verify-spend-model-figures` checked (`B/research/reports/verify-spend-model-figures.md`) | Replace by an own reading: `just usage::checkpoint` before and after one model's stretch, then `just usage::calibrate` |
| One opus attempt: 110 dollars, carry 54.63, intake 39.67, output 15.78 | Estafette in-flight table (`R/older-scripts/inflight.py`); ledger §1 | 2026-11-12 | Transcript tokens by part at list prices (`just usage::inflight`) | Estafette lead | `just usage::inflight` on the own project's agents |
| Cold starts: 72.5 % of opus agents' intake, 56.8 % of sonnet agents', 5-minute TTL | `just usage::coldturns` at estafette `fdf4d32`; Journal 16:16; ledger §6 | 2026-11-12 | Intake of turns whose gap to the previous model message exceeded the TTL, over all agent transcripts | Estafette lead | `just usage::coldturns` on the own project's session |
| Stop at the limit: 13 agents, 3.5M tokens, the lead 0.4M | `R/older-scripts/inflight.py`; Journal 14:38; ledger §6 | 2026-11-12 | Context held at 14:35, before the stop: 3,466k across 13 agents, lead 423k; rounded | Estafette lead | `just usage::inflight` before and after the next stop |
| Example inputs: 40k, 2k a step, 380k, 6.5 minutes, 440k, 60k, 80k, 300k, 3k, 400k, 100 messages, 12 percent, a 6-dollar check, 5 dollars of rework | Chosen by the skill's author; `R/README-2026-11-12.md`, "Figure trace" | — | None: inputs | — | Keep or replace |
| Every other figure: work-unit sums, carry sums, cold-start and continuation dollars, ratios | Arithmetic on the rows above | — | `R/derive/demonstration_figures.py`, output `R/derive/demonstration_figures.out.txt` | — | Rerun after any refresh |

Refresh in this order: refetch the price page and the Artificial Analysis page; rebuild `pairs.json`; run `check_pairs_against_raw.py` and `demonstration_figures.py`; rewrite the example figures and the dates of the two attribution sentences in `<study-the-demonstrations>`; update this table. Atoms and mechanics stay.

### Open points

- Artificial Analysis's run date for each Terminal-Bench 4.0 record: source unrecorded.
- What Artificial Analysis counts in `costPerTask`, its harness's caching included: source unrecorded.

## Hooks

None.
