# Capabilities

**Mutability:** living — corrected in the turn a capability changes.
**Holds:** what the system is and does — module inventory, command surface, artifact layout, domain
vocabulary, known limitations, and measured operational facts, each measured fact carrying its
measurement date.
**Does not hold:** core-shape change narratives (`architecture_log.md`); status snapshots — test
counts, lint counts, build metrics — regenerate these by command; interface specifications —
signatures, parameter lists, flag examples — read these from source; session or process content
(`history/`).
**Convention:** where a fact here has a history worth knowing, the pointer is one line — "changed
YYYY-MM-DD, see `architecture_log.md`" — never a restatement of the reasoning.

## Plugins

Eleven plugins, each a top-level directory (counted 2026-10-06). `.claude-plugin/plugin.json` inside a plugin carries its
version; `.claude-plugin/marketplace.json` at the root lists them all. Every hook in the marketplace
is `type: "command"` — a bash script that emits template text (measured 2026-08-08).

**orchestration** — agent delegation and discontinuous-existence coping mechanisms (5.0.1, 2026-10-06: `agentic-delegation` points at `dev-cycle`). Memory,
record continuity, and the orientation hooks moved to `memento` 2026-09-18; `session-checkpoint` and
`session-close` are retired, thin pointers to `memento:event-capture` and `memento:span-closure`.
Skills: `agentic-delegation` (decompose, launch, verify, assemble; owns the orchestrator identity
and the liveness/monitoring mechanics for a discontinuous entity), `research-tree` (breadth-first
survey then depth-first verification across a knowledge surface), `session-checkpoint` (retired,
pointer), `session-close` (retired, pointer). No hooks.

**memento** — memory and record-keeping for agents without continuity across sessions. Thirteen
skills (entry point `init`, orientation `pat-down`, closure `span-closure`, plus ten supporting
skills — full inventory not yet carried in this file).
Hooks: one SessionStart hook, matcher `startup|resume|compact` (moved from `orchestration`
2026-09-18; PostCompact dropped the same day — its `additionalContext` is schema-rejected outright,
confirmed via github.com/anthropics/claude-code/issues/46191, closed not-planned; SessionStart's
`compact` matcher has a parallel confirmed bug for the JSON form, issues/28305, also closed
not-planned, so plain stdout is the only viable channel and carries no documented matcher
carve-out). Runs `session-start.sh`, which renders `templates/orientation-reminder.txt` — a pointer
to `memento:init` — when `CLAUDE.md` exists. The script tests that one condition and has no other
branch.

**dev-discipline** — agent-agnostic software-engineering skills, 3.0.0 (split 2026-10-06, see
`architecture_log.md`): `tdd` (outermost failing test first, pretend calls, signatures with stub bodies,
recursion to the leaves, side effects passed down from the top, no comments, one-line docstrings, refactor
after green, tests held at the barrier, property tests below it), `systematic-debugging` (with
`scripts/find-polluter.sh <pollution-path> <test-command> <files...>`), `triage-issue`,
`improve-architecture`, `receiving-code-review`. No agents, no hooks, no dependencies. Every skill carries
user trigger phrases; `tdd` is also loaded by dev-cycle's implementer and code-quality-reviewer and by
lite-cycle's suborchestrator through the `Skill` tool, `systematic-debugging` by `dev-cycle` and
`triage-issue`, `improve-architecture` by `triage-issue`.

**dev-cycle** — the development loop over dev-discipline, orchestration, and product-craft, 1.0.0
(created 2026-10-06). Skill `dev-cycle`: `specify → plan → implement → review → integrate`, delta-only
against `agentic-delegation`; the orchestrator plans the units itself (contract, gates, dependency order,
files, tier by risk) and writes plan, status file, and prompt files; every code-changing continuation
returns the unit to the spec review and re-integration. Agents: `spec-capturer` (interviews the user
through `AskUserQuestion` by `product-craft:spec-chef`, one spec file, returns `Spec: <path>`; provisioned
as a background launch the user enters or as a sibling `claude --agent dev-cycle:spec-capturer` session),
`implementer` (`isolation: worktree`, loads `dev-discipline:tdd` through the `Skill` tool — a cross-plugin
`skills:` preload does not land, measured 2026-10-06 — merges the integration branch first, reports
`NEEDS_CONTEXT` or `BLOCKED` instead of asking), `spec-reviewer` (Bash, Skill), `code-quality-reviewer`
(checks `tdd`'s rules). Hooks: one script, `hooks/review-chain.py`, behind five entries — three
`SubagentStop` matchers `^(dev-cycle:)?implementer$`, `^(dev-cycle:)?spec-reviewer$`,
`^(dev-cycle:)?code-quality-reviewer$`, which record a pending stage; `PostToolUse` on
`^(Agent|SendMessage)$`, which retires the stage a launched or continued agent satisfies and injects the
mandate for a foreground completion; an implementer stop opens a stage only on `Status: DONE`; and
`Stop`, which continues the orchestrator's turn with the pending stage's mandate from `hooks/templates/`
up to three times, once for a merge decision. State under `${CLAUDE_PLUGIN_DATA}/review-chain/<session>.json`,
pruned after 7 days; a reviewer stop whose message begins `Dispatch malformed:` opens no stage. Tests: `just hooks-test`
(21, measured 2026-10-06). Artifacts under `orchestration_log/recon/${DATE}/`; the spec under `docs/specs/`. A run
the user marks lite dispatches dev-cycle-lite's `suborchestrator` from `dispatch-the-lite-cycle` in place of the stages below it.

**dev-cycle-lite** — the cost-tiered cycle over dev-cycle and dev-discipline, 1.0.0 (created
2026-10-06), no hooks. Skills: `prescriptive-planning` (the former `defensive-planning`, now fixing every
signature beneath the outermost interface), `lite-cycle` (delta over `dev-cycle` from `plan-the-units`
on: every unit on haiku, an opus prescription per unit, the suborchestrator reviews each unit itself,
re-prescription after a failed review, escalation at the third failed cycle). Agents: `prescriber`
(`model: opus`, preloads `dev-cycle-lite:prescriptive-planning`), `suborchestrator` (`model: sonnet`,
holds `Agent`, runs `lite-cycle` at depth 1, reviews each unit itself), `executor` (`model: haiku`, `isolation: worktree`,
disposable, executes the prescription's exact text, matches gates as Python `re` patterns, reports `DONE` or `BLOCKED`).

**manifesto** — constitution binding.
Skills: `manifesto-oath` (identity construction from loaded constitution elements; tiered name
resolution), `manifesto-writing`.
Hooks: SessionStart, PostCompact, SubagentStart, and UserPromptSubmit (tagline drift reminder).
Hook scripts compose `templates/parts/binding-core.txt` with a per-event preamble. SessionStart and
PostCompact call `ensure-repo.sh`'s `ensure_repo()`, cloning the manifesto repo to
`<project>/.claude/manifesto-repo/LLM_MANIFESTOS` on first use and pulling on later sessions;
SubagentStart and UserPromptSubmit read that clone but never fetch it themselves. `parse_taglines.py`
reads manifesto frontmatter. Neither `envsubst` nor PyYAML is a dependency: `ensure-repo.sh`'s
`render_template()` and `parse_config.py`/`mini_yaml.py` replace them with python3-stdlib-only
equivalents (measured 2026-09-18, after both were found absent in a fresh sandbox and crashing every
manifesto hook silently).
Config schema for `.manifestos.yaml`: `manifesto/SCHEMA.md`.

**qa-automation** — the Playwright test lifecycle.
Skill: `qa-orchestration` (Plan→Generate→Execute→Heal→Report).
Agents: `planner-agent` (explores a live app, produces test plans and selector strategies),
`generator-agent` (writes `.spec.ts` files from the plan), `executor-agent` (runs suites via CLI,
classifies failures), `healer-agent` (repairs locators by a ten-tier confidence algorithm).

**product-craft** — product definition. Skills: `spec-chef` (extracts implicit decisions from
stakeholders into separated artifacts), `user-story-chef`.

**prompt-engineering** — agents only, no skills: `prompt-eval` (scores a prompt against a rubric,
writes a report file), `prompt-optimize` (applies improvement patterns, writes the rewritten prompt
plus a changes report).

**python-tools** — skills: `python-ast-mass-edit` (AST-based edits across 3+ files),
`uv-pyright-debug` (true pyright diagnostics in uv-managed projects).

**userland-utilities** — skill: `fix-macos-app` (clears quarantine and re-signs blocked macOS apps).

## Repo tooling

- `justfile` — `just tokens FILE` measures tokens with tiktoken `cl100k_base`; `just readme`
  regenerates every README from frontmatter; `just check-readmes` fails on a stale README;
  `just hooks-test` runs the dev-discipline hook tests.
- `generate.py` with `templates/marketplace.md` and `templates/plugin.md` renders the root and
  per-plugin READMEs from skill, agent, and hook metadata.
- `.claude/agents/instruction-writer.md` — project-local agent that edits skill definitions, agent
  definitions, and hook templates.
- `.manifestos.yaml` — this repo's own constitution stack, read by the manifesto hooks.

## orchestration_log layout

| Path | Contents | Tracking |
|---|---|---|
| `reference/` | the five living files (`decisions.md` retired, replaced by `architecture_log.md`) plus two standalone manuals | tracked |
| `history/${DATE}/` | `session.md`, `failures.md`, `reviews/`, `cost.md` | tracked, except `cost.md` |
| `recon/${DATE}/` | agent reports, `leave-verification.md`, telemetry | gitignored |

`.gitignore` carries exactly two orchestration patterns: `orchestration_log/recon/` and
`orchestration_log/history/*/cost.md`.

Two standalone manuals sit beside the living files and belong to no ontology slot:

- `reference/agents-reference.md` — the Claude Code platform contract for plugin-defined agents:
  frontmatter, discovery, dispatch, execution, termination, plus consolidated footguns (Appendix A),
  documented silences (Appendix B), and a citation index (Appendix C).
- `reference/hooks-reference.md` — hook events, the four hook types, the command-hook contract, and
  the prompt-hook failure analysis.

## Measured facts

- `agents-reference.md`: 2,790 lines, 11 sections and 3 appendices, extracted from 78 Claude Code
  documentation pages across 9 topic clusters. 298 citations, of which 197 resolve to deep links —
  81% of the 242 that carry a quote. Measured 2026-04-20.
- `hooks-reference.md`: 913 lines. Measured 2026-09-18 (envsubst examples replaced with the
  python3 stand-in after the fresh-sandbox incident).

## Known limitations

- Hooks serve the installed plugin cache, not the working tree. An edit to a hook script or template
  reaches hook output only after the plugin is reinstalled or synced. Observed 2026-08-08.
- The harness blocks subagent writes to report files: agents instructed to write a report to disk
  returned it inline instead, leaving the declared path empty. Observed 2026-08-08.
- Whether `CLAUDE.md` loads into a subagent launched through the Claude Code CLI's Agent tool is
  unresolved — the CLI and SDK sources disagree, and neither settles it. Filed as MD-19 in
  `agents-reference.md` Appendix A (Moderate band).
- `SubagentStop` hook output — `additionalContext` or `decision: block` — reaches the stopping
  subagent and keeps it running; it never reaches the orchestrator. Parent-side injection goes
  through `PostToolUse` on the `Agent` tool, or a main-session `Stop` hook reading recorded state, which
  is how dev-discipline's review chain works since 2026-10-05. The platform refuses, from a
  worktree-isolated subagent, every edit and command that resolves to the main checkout (Claude Code
  ≥2.1.203), so no agent re-roots paths any more. Measured against hooks.md and worktrees.md 2026-10-05.
- A subagent worktree branches from the repository's default branch unless `worktree.baseRef` is
  `"head"`; dev-discipline's implementer merges the integration branch named in its brief before any
  change. Measured 2026-10-05.
- `manifesto-oath` names the default manifesto repository path literally in its Tier 1 text. A
  project that sets `manifesto_dir` receives the override in hook output but not in the skill body.
  Observed 2026-06-24, unchanged 2026-08-08.
- 45 of the 298 citations in `agents-reference.md` are URL-only, carrying no section anchor: the
  automated rewriter could not match those quotes against source. Measured 2026-04-20.
- `.claude/agents/instruction-writer.md` is project-local. It is not packaged in any plugin and does
  not travel with the marketplace.
- No plugin ships an `.mcp.json`.
