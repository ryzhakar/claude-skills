# dev-cycle restructure plan

— written by the orchestrator, 2026-10-06, from the owner's PR #2 review and the rulings in `history/2026-10-05/events.md`; frozen on GO.

## Rulings in force
- Every touched plugin's change is breaking; majors are the orchestrator's call.
- Separate agents for context isolation. Orchestration stays with the main agent; a suborchestrator exists only in lite.
- The spec-capturer asks through `AskUserQuestion`, no fallback. Provisioning: `Agent` launch the owner descends into, or `claude --agent dev-cycle:spec-capturer` as a sibling session messaging the orchestrator.
- Lite ships without hooks and depends on dev-cycle. Three-layer chain, each skill delta-only over the layer beneath: `agentic-delegation` → `dev-cycle` → `lite-cycle`.
- No separate orchestration-planning skill; planning folds into the dev-cycle loop skill.
- Writing standard: `memento:skill-creation`. Orchestrator writes every instruction file; blind checkers audit.

## Versions
| plugin | from | to | ground |
|---|---|---|---|
| dev-discipline | 2.2.0 | 3.0.0 | removes dev-orchestration, defensive-planning, agents, hooks |
| dev-cycle | — | 1.0.0 | new |
| dev-cycle-lite | — | 1.0.0 | new |
| manifesto | 3.2.0 | 3.2.0 | maximalist-reviewer was additive |
| product-craft, orchestration | — | unchanged | untouched |

## Step 0 — recon (one live test, one doc check)
- Cross-plugin `skills:` preload: an agent in dev-cycle preloading `dev-discipline:tdd`. Fallback stays in bodies: invoke with the `Skill` tool when absent.
- `claude --agent <plugin>:<agent>` syntax and sibling messaging: confirm from docs; record as platform facts in the loop skill.

## Step 1 — dev-discipline 3.0.0
Delete `skills/dev-orchestration`, `skills/defensive-planning`, `agents/`, `hooks/`. Drop the `orchestration` dependency. Keep `tdd`, `systematic-debugging`, `triage-issue`, `improve-architecture`, `receiving-code-review` untouched. Rewrite description and keywords. justfile `hooks-test` path moves with the hooks.

## Step 2 — dev-cycle 1.0.0 (deps: dev-discipline, orchestration, product-craft)
Skill `dev-cycle` — one loop: `specify → plan → implement → review → integrate`.
- specify: provision the spec-capturer (either provisioning), take `Spec: <path>` as its only accepted return, ignore every other stop.
- plan: from `dev-orchestration`'s `plan-the-units` plus the contract/gate sentences of `defensive-planning` (fix each unit's outermost contract and gates, leave inner signatures to the implementer) plus one sentence assigning tier by unit risk; the orchestrator writes the plan, the status file, and the implementer prompt files.
- implement, review, integrate: `dev-orchestration`'s remaining tags, agent names rescoped to `dev-cycle:*`.
Agents:
- `spec-capturer` — new. Preloads `product-craft:spec-chef`. Tools wide, `AskUserQuestion` required, `permissionMode` liberal. Interviews to a single spec file; returns `Spec: <path>`.
- `implementer`, `spec-reviewer`, `code-quality-reviewer` — moved; `skills:` preload `dev-discipline:tdd` (step 0 result decides the wording).
Hooks: `review-chain.py`, templates, 20 tests moved; matchers `^(dev-cycle:)?implementer$` etc.; `just hooks-test` repointed.

## Step 3 — dev-cycle-lite 1.0.0 (deps: dev-cycle, dev-discipline; no hooks)
Skills:
- `prescriptive-planning` — `defensive-planning` moved whole: no decision, no option, no unverifiable step, every signature fixed.
- `lite-cycle` — the administrator's loop as a delta over `dev-cycle`: planner launch, executor launch per unit, both reviews, integrate; no spec stage of its own (reuses dev-cycle's).
Agents:
- `lite-planner` — `model: opus`, preloads `prescriptive-planning`; spec or unit contract in, prescription out.
- `administrator` — `model: sonnet`, holds `Agent`; suborchestrator running `lite-cycle` at depth 1; launches executors, runs or launches both reviews, integrates.
- `executor` — `model: haiku`, `isolation: worktree`, disposable; follows the prescription literally; reports `DONE` or `BLOCKED`, never designs.

## Step 4 — records
`reference/architecture_log.md` one entry per plugin; `reference/capabilities.md` plugin inventory; `reference/conventions.md` chain rule; `.claude-plugin/marketplace.json`; READMEs regenerated; digest at `history/2026-10-06/session.md`.

## Step 5 — checks
Blind compliance + usability rounds per new or rewritten instruction file (dev-cycle skill, spec-capturer, lite-cycle, lite-planner, administrator, executor, moved agents' changed lines); one seam round across the three layers; `just hooks-test` green; `claude plugin validate` on all four plugins; `just check-readmes`.

## Delivery
One PR per step 1+2 (dev-discipline split and dev-cycle), one PR for step 3; records ride each. Push after every commit; single-line conventional commits, atomic by artifact class.
