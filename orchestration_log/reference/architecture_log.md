# Architecture Log

**What this is.** How this marketplace's core mechanics changed over time to become what they are now.
Append-only, flat, oldest first. Every entry is a dated past-tense statement about one change, which is
why append-only is correct here where it is wrong for a living document: a claim about what happened on
a date cannot go stale.

**What it is not.** `capabilities.md` describes the system as it is NOW and has no past tense — go there
for current shape. `ground-truth.md` holds the problem frame, which does not change. `conventions.md`
holds what a reader must DO, each rule stating its own why. Git holds every change, including the ones
that shaped nothing.

**Admission, both halves required.** An entry needs a BEFORE — a shape the system actually HELD, not a
plan that was abandoned — and it must have changed what is COMPUTED or what is RUNNABLE. `runnable`
means the boundary between impossible and possible moved for a skill, a hook, or a dispatch: a silent
failure mode closed, a dependency removed, a file a live protocol reads or writes relocated. `computed`
means the shape of an artifact or record changed. Tooling, CLI surface, documentation, process, style
preference, and review outcomes never qualify, however much work they represent.

**The core is five things:** how a skill is structured and loaded; how a hook fires and what it may
inject; how an agent is dispatched and supervised; how session memory and continuity are modeled; how a
plugin's skills and agents are bounded and grouped.

**`INVALIDATES` is the field to read before relying on an older design.** A path, a hook step, or a
prompt pattern named there no longer holds once its entry lands.

Assembled 2026-09-18 from `orchestration_log/reference/decisions.md`, which held 90 entries of mixed
content — architecture changes beside style rulings, process calls, and governance decisions already
stated with their own rationale in `ETHOS.md`, `CLAUDE.md`, and `conventions.md` — and was replaced by
this file. 24 changes survived the admission test.

**Resolving a `SOURCE` line.** Lines cite `decisions.md`'s dated section headers, which no longer exist
in the working tree. The file is retrievable in full at commit `a6ba4a7f929ef08849484999aaa3d7516670bb35`,
the last commit in which it existed:
`git show a6ba4a7f929ef08849484999aaa3d7516670bb35:orchestration_log/reference/decisions.md`.

---

## 2026-04-13 — References eliminated marketplace-wide; every skill becomes self-contained
KIND:          runnable
FROM → TO:     skills citing external files by `@`-reference, trusted to be read at runtime → every
               skill inlines its own content; references eliminated marketplace-wide
WHY:           models do not follow `@`-references in practice, so referenced content never executes
INVALIDATES:   any skill design relying on cross-file `@`-reference resolution at runtime
SOURCE:        decisions.md 2026-04-13

## 2026-04-13 — Skills are scoped to file artifacts; no platform API calls
KIND:          runnable
FROM → TO:     a skill free to call an external platform API → a skill produces only file artifacts on
               disk; publishing is left to the user
WHY:           platform coupling ties a skill's behavior to one ecosystem's API surface and removes the
               user's choice of where output goes
INVALIDATES:   nothing shipped; forecloses platform-calling skill designs going forward
SOURCE:        decisions.md 2026-04-13

## 2026-04-16 — `dev-orchestration` merges into `dev-discipline`, beside its agents
KIND:          runnable
FROM → TO:     the skill and the agents it launches split across two plugins, requiring cross-plugin
               dispatch → both live in one plugin
WHY:           a skill and the agents it launches belong together; cross-plugin dispatch created
               maintenance friction
INVALIDATES:   any dispatch path assuming the skill's prior plugin location
SOURCE:        decisions.md 2026-04-16 (breaking change, commit `e417a6f`)

## 2026-04-16 — Prompt hooks rejected permanently; `command` is the only hook type
KIND:          runnable
FROM → TO:     hooks authored as either `prompt` or `command` type → `command`-type only,
               marketplace-wide
WHY:           prompt hooks fail silently on `Stop` and `PreToolUse`, the two blocking events that
               matter, and carry no ecosystem adoption
INVALIDATES:   any hook design relying on the `prompt` type on `Stop` or `PreToolUse`
SOURCE:        decisions.md 2026-04-16

## 2026-04-16 — Hooks gate on configuration existence and stay silent when unconfigured
KIND:          runnable
FROM → TO:     a hook fires unconditionally regardless of project setup → a hook checks for its config
               directory or file first and stays silent when absent
WHY:           an ARRIVE hook injecting mandatory reads means nothing to a project carrying no
               `orchestration_log/reference/`
INVALIDATES:   nothing measured; removes false-positive hook firing on an unconfigured project
SOURCE:        decisions.md 2026-04-16

## 2026-04-17 — Corpora above roughly 500KB synthesize via map-reduce scouts, not single-context read
KIND:          computed
FROM → TO:     one context ingesting a whole corpus for synthesis → per-section sonnet scouts feeding
               one opus assembler once a corpus crosses roughly 500KB
WHY:           single-context synthesis over 600K+ tokens measurably degrades
INVALIDATES:   any synthesis attempted in one context above the threshold
SOURCE:        decisions.md 2026-04-17

## 2026-04-29 — Hook mandates inject exactly one unconditional command
KIND:          runnable
FROM → TO:     a hook mandate could branch conditionally, letting the orchestrator decline to parse a
               branch → exactly one unconditional command per mandate; branching moves to the receiving
               agent
WHY:           a conditional mandate becomes an escape hatch the orchestrator can decline
INVALIDATES:   any hook mandate authored with conditional branches
SOURCE:        decisions.md 2026-04-29

## 2026-04-30 — The orchestrator delegates every file operation
KIND:          runnable
FROM → TO:     the orchestrator free to edit files directly → every file operation delegated to a
               subagent
WHY:           the orchestrator's context is the scarce resource; direct edits collapse the separation
               the role exists to hold
INVALIDATES:   nothing shipped
SUPERSEDED-BY: 2026-08-08 — narrowed by the session-memory exception
SOURCE:        decisions.md 2026-04-30

## 2026-05-06 — Delegation loses both escape hatches; prompts never inline file content
KIND:          runnable
FROM → TO:     two carve-outs existed in the delegation rule, and a prompt could inline file content
               directly, skill files included → both carve-outs deleted; every prompt cites a path and
               line range instead
WHY:           owner ruling: "nothing is small enough to be done by the orchestrator"; "skill files have
               physical paths on disk"
INVALIDATES:   any prompt authored with inlined file content or a standing orchestrator carve-out
SOURCE:        decisions.md 2026-05-06

## 2026-05-06 — Every agent launch runs in the background
KIND:          runnable
FROM → TO:     an agent launch could block the orchestrator in the foreground → every launch is
               backgrounded
WHY:           a blocked orchestrator cannot answer the notification it is waiting for
INVALIDATES:   any dispatch pattern relying on a foreground, blocking launch
SOURCE:        decisions.md 2026-05-06

## 2026-06-17 — Hooks inject `SKILL.md` at runtime instead of duplicating protocol text
KIND:          runnable
FROM → TO:     protocol text duplicated inline inside hook templates → hooks inject the skill file
               itself at runtime
WHY:           duplicated protocol drifts from its source; runtime injection propagates a skill edit
               with no second edit
INVALIDATES:   any hook template carrying its own copy of protocol text
SOURCE:        decisions.md 2026-06-17

## 2026-06-19 — No inline-principles binding path: a name is not a source
KIND:          runnable
FROM → TO:     a binding could proceed from a principle set's name alone → binding requires loading the
               actual source content; naming without loading is refused
WHY:           binding to content reconstructed from a name is confabulation
INVALIDATES:   any binding performed from a name with no source load
SOURCE:        decisions.md 2026-06-19

## 2026-06-24 — Skill files adopt XML structure and Claude Code's native vocabulary
KIND:          computed
FROM → TO:     skills structured as markdown-header prose → XML-tagged sections using the platform's
               native terms
WHY:           XML tags are hard scope delimiters where markdown headers are soft hints, and native
               terms are recognized faster than invented ones
INVALIDATES:   nothing shipped; supersedes markdown-header skill authoring going forward
SOURCE:        decisions.md 2026-06-24

## 2026-06-24 — Safety-net crons fire at roughly 1.2N minutes for an N-minute operation
KIND:          runnable
FROM → TO:     no standing rule for safety-net cron timing → crons set to fire at roughly 1.2x the
               expected operation duration
WHY:           firing just after the expected window catches a real failure; firing mid-flight only
               reports "still running"
INVALIDATES:   nothing shipped
SOURCE:        decisions.md 2026-06-24

## 2026-06-24 — `SendMessage` continuation becomes the happy path for follow-up work
KIND:          runnable
FROM → TO:     follow-up work re-launched a fresh agent, discarding the files and reasoning it already
               held → `SendMessage` continuation is the default
WHY:           a fresh launch pays 3-5k reinitialization tokens and discards held context, per a
               downstream field report
INVALIDATES:   any follow-up dispatch pattern defaulting to a fresh launch
SOURCE:        decisions.md 2026-06-24

## 2026-08-08 — Five-file memory ontology adopted; Status Snapshot retired as a category
KIND:          computed
FROM → TO:     memory held under a partial ontology including a Status Snapshot category →
               `ground-truth.md`, `capabilities.md`, `conventions.md`, `user_deferred_items.md`,
               `decisions.md`; Status Snapshot retired
WHY:           downstream field observation confirmed the ontology in production use while the process
               half existed only on paper
INVALIDATES:   any memory read/write path assuming a Status Snapshot category
SUPERSEDED-BY: 2026-09-15 in part — the concerns this ontology carried begin dissolving into `memento`;
               2026-09-18 in part — `decisions.md` itself is retired, replaced by this file
SOURCE:        decisions.md 2026-08-08

## 2026-08-08 — Session memory becomes the sole exception to full delegation
KIND:          runnable
FROM → TO:     the 2026-04-30 delegation rule held with no exception → the orchestrator writes the five
               living files, `failures.md`, and `session.md` directly; every other file stays delegated
WHY:           narrows the delegation rule to a named path list rather than leaving it absolute
INVALIDATES:   any reading of the 2026-04-30 entry as still absolute
SOURCE:        decisions.md 2026-08-08

## 2026-08-08 — `SubagentStart` hooks inject element names, purposes, and protocol, never content
KIND:          runnable
FROM → TO:     unstated injection scope for `SubagentStart` → the hook injects names, purposes, and
               protocol only; content itself is never injected at this hook
WHY:           codified as a platform fact rather than repaired as a defect
INVALIDATES:   any `SubagentStart` hook design injecting full content
SOURCE:        decisions.md 2026-08-08

## 2026-08-08 — `session-state.md` collapsed; `session.md` written at will
KIND:          runnable
FROM → TO:     a separate scratch continuity file (`session-state.md`) alongside `session.md` →
               `session-state.md` retired; the orchestrator writes `session.md` directly at will, a
               seventh direct-write exception beside the five living files and `failures.md`
WHY:           one session, one continuity surface
INVALIDATES:   any read or write path targeting `session-state.md`
SOURCE:        decisions.md 2026-08-08

## 2026-09-15 — `TaskOutput` deprecated for local-agent progress checks
KIND:          runnable
FROM → TO:     `TaskOutput` used to check a local agent's progress → deprecated for that task type, no
               non-flooding replacement identified
WHY:           `TaskOutput` returns the full subagent transcript and floods orchestrator context
               permanently
INVALIDATES:   any progress-check path calling `TaskOutput` on a local agent
SOURCE:        decisions.md 2026-09-15

## 2026-09-15 — Five memory and session concerns leave the orchestration plugin for a ground-up rebuild
KIND:          runnable
FROM → TO:     discontinuous existence, artifact management, orientation, record keeping, and session
               management held (partially, textually fused) inside the orchestration plugin → all five
               dissolve out of orchestration and are rebuilt as a separate system (`memento`),
               ontology-first
WHY:           only artifact management, record keeping, and half of session management were textually
               fused, in one sentence, with no machine-readable schema for any Artifact Contract table
INVALIDATES:   any assumption that orchestration owns these five concerns going forward
SOURCE:        decisions.md 2026-09-15

## 2026-09-18 — `envsubst` and PyYAML dependencies removed; every plugin runs on stdlib only
KIND:          runnable
FROM → TO:     hooks across manifesto, orchestration, and dev-discipline called `envsubst` and imported
               PyYAML, both unverified third-party dependencies → `envsubst` replaced by
               `render_template()` (python3 stdlib `re.sub`), PyYAML replaced by `mini_yaml.py` (a
               block-style subset parser); every plugin now depends on nothing beyond bash, git, and
               stock python3
WHY:           a fresh sandbox crashed every manifesto hook and the orchestration ARRIVE hook; the YAML
               failure was masked by `2>/dev/null` under `set -euo pipefail`, turning a plain
               `ModuleNotFoundError` into an opaque hook error
INVALIDATES:   the general hooks reference's prior `envsubst` prescription as the template-output
               pattern
SOURCE:        decisions.md 2026-09-18

## 2026-09-18 — The manifesto clone moves from `/tmp` to the project, and `ensure_repo` finally runs
KIND:          runnable
FROM → TO:     `ensure_repo()` existed since the manifesto plugin's first version but was never called
               from any hook; every environment relied on a hand-cloned `/tmp/claude-manifesto-repo` →
               wired into `SessionStart` and `PostCompact`; clone target moves to
               `<project_dir>/.claude/manifesto-repo/LLM_MANIFESTOS`, project-local, with a
               self-ignoring `.gitignore`
WHY:           no hook had ever invoked `ensure_repo()`, so every fresh sandbox depended on a manual
               clone step no automation performed
INVALIDATES:   every doc reference to the old `/tmp/claude-manifesto-repo` path
SOURCE:        decisions.md 2026-09-18

## 2026-09-18 — `decisions.md` retired; this file becomes the core-change record
KIND:          runnable
FROM → TO:     every ruling logged to one append-only `decisions.md` ledger, read and written every
               session by the ARRIVE hook and the orchestration skills → core-shape changes recorded
               here alone; every other ruling is written directly into the file its rule, fact, or
               intention belongs to, in the turn it is made
WHY:           mirrors the restructuring already proven in `embedding_finetuning_for_ecommerce`;
               `decisions.md`'s mixed content — style, process, and governance calls already stated
               with their own rationale in `ETHOS.md`, `CLAUDE.md`, and `conventions.md` — added no
               signal this file's narrower admission test needed
INVALIDATES:   the ARRIVE hook's `decisions.md` tail-read step; `agentic-delegation`, `session-close`,
               and `session-checkpoint`'s `decisions.md` wiring (updated in the same change)
SOURCE:        `git show a6ba4a7f929ef08849484999aaa3d7516670bb35:orchestration_log/reference/decisions.md`

## 2026-09-18 — Session/artifact continuity leaves orchestration and dev-discipline; discontinuous-existence coping stays
KIND:          runnable
FROM → TO:     `agentic-delegation` owned the ARRIVE/WORK/LEAVE frame, the five-living-file contract,
               and a session-memory delegation exception; `session-checkpoint` and `session-close`
               ran the checkpoint and LEAVE protocols; the ARRIVE hook injected a five-file read
               order → all of it retired. `session-checkpoint` and `session-close` become thin
               pointers to `memento:event-capture` and `memento:span-closure`. The ARRIVE hook
               (renamed `session-start.sh`, template renamed `orientation-reminder.txt`) points at
               `memento:init` instead of injecting a read order, and gates on `CLAUDE.md` existing
               rather than `orchestration_log/reference/`. `agentic-delegation`'s
               `<launch_and_monitor>` block — liveness checks, safety-net crons, mid-flight
               correction, the discontinuous-existence framing — is untouched: it copes with a
               dispatch dying mid-flight, not with memory continuity across sessions, and stays at
               the orchestration level
WHY:           `memento` now owns record continuity end to end; duplicating that ownership in
               orchestration and dev-discipline produces two systems that can disagree
INVALIDATES:   any reference to `agentic-delegation`'s five-living-file contract, the session-memory
               delegation exception, or the ARRIVE/WORK/LEAVE frame; `session-close`'s LEAVE
               protocol steps L0-L6 and its `extract_metrics.py` script (removed, orphaned by the
               same change); `dev-orchestration`'s "audit test markers during ARRIVE" wording
SOURCE:        this migration

## 2026-09-18 — The orientation-reminder hooks move from orchestration to memento
KIND:          runnable
FROM → TO:     `session-start.sh` and `templates/orientation-reminder.txt` shipped inside
               `orchestration/hooks/`, a plugin that no longer owns memory or continuity → both move
               into `memento/hooks/`, alongside the `memento:init` entry point they point at
WHY:           a plugin's hooks belong with the plugin whose domain they serve; orchestration had
               already lost that domain to memento
INVALIDATES:   `orchestration/hooks/` as a path (directory removed); orchestration's own SessionStart
               and PostCompact hook registration
SOURCE:        this migration

## 2026-09-18 — The PostCompact hook is dropped; SessionStart absorbs its matcher
KIND:          runnable
FROM → TO:     two hooks, SessionStart (`startup|resume`) and PostCompact (`*`), both emitting plain
               stdout → one SessionStart hook, matcher `startup|resume|compact`, PostCompact removed
WHY:           PostCompact's `hookSpecificOutput.additionalContext` fails schema validation outright
               — "Invalid input"; the schema accepts only `PreToolUse`, `UserPromptSubmit`,
               `PostToolUse` — and PostCompact has no plain-stdout channel either, confirmed via
               github.com/anthropics/claude-code/issues/46191 (closed not-planned). SessionStart's
               `compact` matcher has a parallel, separately-reproduced bug for the JSON form
               (issues/28305, closed not-planned); plain stdout, already in use, is undocumented for
               `compact` specifically but carries no matcher carve-out in the docs and is the only
               channel left
INVALIDATES:   the "SessionStart and PostCompact hooks inject context" design pattern this repo's
               own `hooks-reference.md` recommended; any hook config pairing SessionStart with a
               PostCompact hook for context injection
SOURCE:        this migration; github.com/anthropics/claude-code/issues/46191,
               github.com/anthropics/claude-code/issues/28305
