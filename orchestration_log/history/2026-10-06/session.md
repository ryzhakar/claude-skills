# Session 2026-10-06 — dev-cycle restructure

Status: complete, 2026-10-06 ~21:10 UTC; PR #3 reviewed by the owner, revised, tidied, and merged into main on the owner's word; heartbeat Routine disabled.

Opened at the owner's GO (~18:00 UTC) under `/work-silently`, after the PR #2 review of the morning's dev-discipline iteration asked for a restructure: planning the orchestration is the orchestrator's work, the agentic implementer and the prescription-following executor are different dynamics, and the loop needs an owner-interviewing spec stage. Plan frozen at `reviews/dev-cycle-restructure-plan.md`; rulings in `history/2026-10-05/events.md`.

## What shipped

dev-discipline 3.0.0 keeps the five agent-agnostic skills; `dev-orchestration`, `defensive-planning`, the three agents, and the review-chain hooks left as git renames. dev-cycle 1.0.0 holds the loop `specify → plan → implement → review → integrate` (the orchestrator plans units itself; every code-changing continuation returns the unit to the spec review and re-integration), `spec-capturer` (asks through `AskUserQuestion`, no fallback; a background launch the user enters, or a sibling `claude --agent` session), the moved agents loading `dev-discipline:tdd` through the `Skill` tool, and the hooks under the `dev-cycle:` prefix (20 tests green). dev-cycle-lite 1.0.0 holds `prescriptive-planning` (every signature fixed, gates as one matched output line), `lite-cycle`, `prescriber` (opus), `suborchestrator` (sonnet, holds `Agent`), `executor` (haiku, worktree, disposable); no hooks. Earlier in the day, before GO: `manifesto:maximalist-reviewer` at 3.2.0.

Platform facts measured: `AskUserQuestion` is stripped from subagents (docs); a same-plugin `skills:` preload lands and a cross-plugin one does not (headless `claude -p --plugin-dir` probes, `recon/2026-10-06/preload-probe/`); `claude --agent` and `--plugin-dir` exist in 2.1.291; the owner descends into running subagents locally (owner-stated).

## The checker loop

Three blind author–checker rounds, compliance and usability, over seven files (dev-cycle, spec-capturer, lite-cycle, prescriptive-planning, prescriber, executor, suborchestrator): r1 7/26, 7/8, 7/8, 3/15, 1/6, 7/5, 4/3; r2 7/21, 4/5, 4/9, 4/17, 1/9, 3/9, 2/3; r3 4/21, 3/4, 3/8, 5/15, 2/7, 2/5, 2/4. Every finding applied; struck: `permissionMode` on spec-capturer (a Claude Code field the standard's list omits), terms owned by `agentic-delegation` or sibling agents. Rounds closed at r3 — compliance single-digit everywhere, usability steady as checkers invent fresh cases. Reports under `recon/2026-10-06/checks/`, prompts beside them, ids in `agents.md` there. One blind seam checker over the three-layer chain found 30 mismatches, all applied toward the producer: the hook mandates carry the agents' delta items and skip malformed reviewer stops (21 tests); the implementer takes every continuation item the loop sends; the quality re-review carries the fresh spec verdict path; the spec-capturer sends `Spec:` from a sibling session; dev-cycle names its exceptions to `agentic-delegation`, passes absolute spec paths, launches implementers with the prompt text inline, fixes `briefs/`, and gained `dispatch-the-lite-cycle`; lite-cycle takes four items, re-prescribes to `-4`, names the findings file per failure kind, relaunches malformed agents; the prescription carries exact step text, numbered steps, `re` gates, and a `Commit` section; `agentic-delegation` points at `dev-cycle` (orchestration 5.0.1).

## The owner's review and the second pass

The owner's PR #3 review (fourteen threads, discussed in session) reset four design points: the plan assigns requirements and gates and never names an interface — the implementer designs the outermost interface through `tdd`, the prescriber through its prescription; every dispatch answers to wall-time and token spend, units run as parallel lanes, a shared file is the integration agent's merge, and sequential lanes through the scope are forbidden; a worktree gone after an agent's death is recreated by the orchestrator with `git worktree add` on the branch the implementer now reports, and the same implementer is continued, never a fresh dispatch; after integration the whole diff gets a full spec and quality cycle and every deferred nit is fixed on the integration branch. Smaller rulings: no `permissionMode` in agent frontmatter; the spec-capturer follows spec-chef with one most-influential self-contained question at a time; the quality review runs only after `Verdict: PASS`; lite knows the full cycle and the full cycle knows nothing of lite — the suborchestrator is dispatched from `lite-cycle`; invented helper-role names are gone. The tidy pass derived SHAs from the reported branch at the project root, moved `briefs/` and the executor's report form into lite, and pointed ETHOS and the orchestration maintainer notes at `dev-cycle`.

## Deviations from the plan

One PR (#3) carries steps 1–3 together, on the owner's "new integration branch, new PR" ruling; the plan said two. No planner agent in dev-cycle and no orchestration-planning skill — planning folded into the loop skill on the owner's question. The lite administrator is named `suborchestrator`, the opus planner `prescriber`.

## Where the rest is

Events and failures in `history/2026-10-05/` (the day's one journal); core-shape changes in `reference/architecture_log.md` (two entries dated 2026-10-06 for the split and the preload); the standing description in `reference/capabilities.md`; conventions and hooks reference corrected; READMEs regenerated.

## Residue

- Tokens: ten instruction files total ~14.9k after the seam round (14296 before it) (dev-cycle skill 3860, its agents 5086, lite skills 2799, lite agents 2551); no ceilings were set for this span.
- The hook chain has not run in a live session under the `dev-cycle:` prefix; the suborchestrator has not launched at depth 1 with hooks firing beneath it.
- `spec-chef`'s own output shape is unchanged; the spec-capturer folds its artifacts into one file by instruction alone.
- Four pre-existing `${CLAUDE_PLUGIN_ROOT}` quoting warnings in `manifesto/hooks/hooks.json` stand untouched.
