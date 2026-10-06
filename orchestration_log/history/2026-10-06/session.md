# Session 2026-10-06 — dev-cycle restructure

Status: in progress; seam round running; every commit pushed to `claude/dev-cycle-restructure`, PR #3.

Opened at the owner's GO (~18:00 UTC) under `/work-silently`, after the PR #2 review of the morning's dev-discipline iteration asked for a restructure: planning the orchestration is the orchestrator's work, the agentic implementer and the prescription-following executor are different dynamics, and the loop needs an owner-interviewing spec stage. Plan frozen at `reviews/dev-cycle-restructure-plan.md`; rulings in `history/2026-10-05/events.md`.

## What shipped

dev-discipline 3.0.0 keeps the five agent-agnostic skills; `dev-orchestration`, `defensive-planning`, the three agents, and the review-chain hooks left as git renames. dev-cycle 1.0.0 holds the loop `specify → plan → implement → review → integrate` (the orchestrator plans units itself; every code-changing continuation returns the unit to the spec review and re-integration), `spec-capturer` (asks through `AskUserQuestion`, no fallback; a background launch the user enters, or a sibling `claude --agent` session), the moved agents loading `dev-discipline:tdd` through the `Skill` tool, and the hooks under the `dev-cycle:` prefix (20 tests green). dev-cycle-lite 1.0.0 holds `prescriptive-planning` (every signature fixed, gates as one matched output line), `lite-cycle`, `prescriber` (opus), `suborchestrator` (sonnet, holds `Agent`), `executor` (haiku, worktree, disposable); no hooks. Earlier in the day, before GO: `manifesto:maximalist-reviewer` at 3.2.0.

Platform facts measured: `AskUserQuestion` is stripped from subagents (docs); a same-plugin `skills:` preload lands and a cross-plugin one does not (headless `claude -p --plugin-dir` probes, `recon/2026-10-06/preload-probe/`); `claude --agent` and `--plugin-dir` exist in 2.1.291; the owner descends into running subagents locally (owner-stated).

## The checker loop

Three blind author–checker rounds, compliance and usability, over seven files (dev-cycle, spec-capturer, lite-cycle, prescriptive-planning, prescriber, executor, suborchestrator): r1 7/26, 7/8, 7/8, 3/15, 1/6, 7/5, 4/3; r2 7/21, 4/5, 4/9, 4/17, 1/9, 3/9, 2/3; r3 4/21, 3/4, 3/8, 5/15, 2/7, 2/5, 2/4. Every finding applied; struck: `permissionMode` on spec-capturer (a Claude Code field the standard's list omits), terms owned by `agentic-delegation` or sibling agents. Rounds closed at r3 — compliance single-digit everywhere, usability steady as checkers invent fresh cases. Reports under `recon/2026-10-06/checks/`, prompts beside them, ids in `agents.md` there. One seam checker over the three-layer chain follows.

## Deviations from the plan

One PR (#3) carries steps 1–3 together, on the owner's "new integration branch, new PR" ruling; the plan said two. No planner agent in dev-cycle and no orchestration-planning skill — planning folded into the loop skill on the owner's question. The lite administrator is named `suborchestrator`, the opus planner `prescriber`.

## Where the rest is

Events and failures in `history/2026-10-05/` (the day's one journal); core-shape changes in `reference/architecture_log.md` (two entries dated 2026-10-06 for the split and the preload); the standing description in `reference/capabilities.md`; conventions and hooks reference corrected; READMEs regenerated.

## Residue

- Tokens: ten instruction files total 14296 (dev-cycle skill 3860, its agents 5086, lite skills 2799, lite agents 2551); no ceilings were set for this span.
- The hook chain has not run in a live session under the `dev-cycle:` prefix; the suborchestrator has not launched at depth 1 with hooks firing beneath it.
- `spec-chef`'s own output shape is unchanged; the spec-capturer folds its artifacts into one file by instruction alone.
- Four pre-existing `${CLAUDE_PLUGIN_ROOT}` quoting warnings in `manifesto/hooks/hooks.json` stand untouched.
