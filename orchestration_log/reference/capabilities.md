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

Nine plugins, each a top-level directory. `.claude-plugin/plugin.json` inside a plugin carries its
version; `.claude-plugin/marketplace.json` at the root lists them all. Every hook in the marketplace
is `type: "command"` — a bash script that emits template text (measured 2026-08-08).

**orchestration** — agent delegation and discontinuous-existence coping mechanisms. Memory,
record continuity, and the orientation hooks moved to `memento` 2026-09-18; `session-checkpoint` and
`session-close` are retired, thin pointers to `memento:event-capture` and `memento:span-closure`.
Skills: `agentic-delegation` (decompose, launch, verify, assemble; owns the orchestrator identity
and the liveness/monitoring mechanics for a discontinuous entity), `research-tree` (breadth-first
survey then depth-first verification across a knowledge surface), `session-checkpoint` (retired,
pointer), `session-close` (retired, pointer). No hooks.

**memento** — memory and record-keeping for agents without continuity across sessions. Thirteen
skills (entry point `init`, orientation `pat-down`, closure `span-closure`, plus ten supporting
skills — full inventory not yet carried in this file).
Hooks: SessionStart on `startup|resume` and PostCompact on `*` (moved from `orchestration`
2026-09-18), both running `session-start.sh`, which renders `templates/orientation-reminder.txt` — a
pointer to `memento:init` — when `CLAUDE.md` exists. The script tests that one condition and has no
other branch.

**dev-discipline** — the software-development extension of delegation.
Skills: `dev-orchestration` (Plan→Implement→Review→Fix loop), `defensive-planning`,
`systematic-debugging`, `tdd`, `triage-issue`, `improve-architecture`, `receiving-code-review`.
Agents: `implementer` (runs in worktree isolation), `spec-reviewer`, `code-quality-reviewer`.
Hooks: three SubagentStop hooks, matching `implementer`, `spec-reviewer`, and
`code-quality-reviewer`, each injecting a single unconditional next-dispatch mandate from
`hooks/templates/`.

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
  regenerates every README from frontmatter; `just check-readmes` fails on a stale README.
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
- Absolute paths in a dispatch prompt defeat `isolation: worktree` silently. `Edit` and `Write`
  resolve absolute paths against the main working tree, so an agent's changes land outside its
  worktree while the worktree stays empty. The three dev-discipline review-chain agents re-root
  marketplace-prefixed paths defensively; no other agent type does.
- `manifesto-oath` names the default manifesto repository path literally in its Tier 1 text. A
  project that sets `manifesto_dir` receives the override in hook output but not in the skill body.
  Observed 2026-06-24, unchanged 2026-08-08.
- 45 of the 298 citations in `agents-reference.md` are URL-only, carrying no section anchor: the
  automated rewriter could not match those quotes against source. Measured 2026-04-20.
- `.claude/agents/instruction-writer.md` is project-local. It is not packaged in any plugin and does
  not travel with the marketplace.
- No plugin ships an `.mcp.json`.
