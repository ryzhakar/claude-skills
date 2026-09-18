# Decisions

**Mutability:** append-only. A reversal is a new entry citing the entry it supersedes. Entries are
never rewritten; a mechanical pointer repair is recorded inline where it occurs.
**Holds:** every decision this project made — the date, the decision, a one-line rationale, a
license tag (owner ruling / orchestrator call / measured verdict), and evidence pointers.
**Does not hold:** the state a decision produced (`capabilities.md`), the rule a decision
established (`conventions.md`), the owner's open intentions (`user_deferred_items.md`).
**Convention:** one entry per decision, headed `## YYYY-MM-DD — <decision>`, body 2-5 lines ending
in an `Evidence:` line. Evidence cites commit SHAs and tracked paths.

## 2026-04-09 — Versions live in `plugin.json`; major increments require owner approval

A major bump signals a breaking change, and only the owner can weigh the ecosystem cost. License: owner ruling.
Evidence: `CLAUDE.md` "## Versioning"; commit `3266514`.

## 2026-04-13 — References eliminated marketplace-wide; every skill is self-contained

Models do not follow @references in practice, so content outside the body never executes. License: owner ruling.
Evidence: `ETHOS.md` "## Self-containment"; commits `37dc867`, `d4b73e7`, `fe9699c`, `93947db`.

## 2026-04-13 — Emphatic markers stay in skill text

The owner overrode research advising their removal: observed model behavior outranks platform guidance. License: owner ruling.
Evidence: `ETHOS.md` "## Strong directive language"; `orchestration_log/history/2026-04-13/session.md`.

## 2026-04-13 — Skills produce file artifacts, never platform API calls

Output is documents on disk; the owner decides where they are published. License: owner ruling.
Evidence: `ETHOS.md` "## No platform coupling"; commit `038045b`.

## 2026-04-13 — Token counts are measured, never estimated

An unmeasured token claim cannot be verified, so `just tokens` became the single measurement path. License: owner ruling.
Evidence: `justfile`; commit `2157060`.

## 2026-04-14 — `ETHOS.md` created as the authoring constitution, imported by `CLAUDE.md`

Principles scattered across analysis artifacts do not reach the next session; a root file loaded every session does. License: owner ruling.
Evidence: `ETHOS.md`; `CLAUDE.md` line 5; commit `db38ec8`.

## 2026-04-15 — `/cost` is the only trusted cost source

JSONL double-counts subagent internals: one session reported roughly $800 against an actual $132. License: measured verdict.
Evidence: `orchestration/skills/session-close/SKILL.md` "## Cost source"; commit `ae2ce2b`.

## 2026-04-15 — `instruction-writer` lives at `.claude/agents/`, outside every plugin

Instruction editing is maintainer tooling, not a published marketplace capability. License: owner ruling.
Evidence: `.claude/agents/instruction-writer.md`; `orchestration_log/history/2026-04-15/session.md`.

## 2026-04-16 — `dev-orchestration` moved into `dev-discipline`, beside its agents

A skill and the agents it launches belong in one plugin; cross-plugin dispatch creates maintenance friction. License: orchestrator call.
Evidence: commit `e417a6f` (breaking change).

## 2026-04-16 — Prompt hooks rejected permanently; `type: "command"` is the only hook type

Prompt hooks fail silently on Stop and PreToolUse — the two blocking events that matter — and carry no ecosystem adoption. License: measured verdict.
Evidence: `orchestration_log/reference/hooks-reference.md` "## Prompt Hook Status"; commit `201ad53`.

## 2026-04-16 — Hooks gate on configuration existence and stay silent when unconfigured

The ARRIVE hooks inject mandatory reads that mean nothing to a project without `orchestration_log/reference/`. License: owner ruling.
Evidence: `orchestration/hooks/session-arrive.sh`; `ETHOS.md` "## Hooks: modularity and gating"; commit `201ad53`.

## 2026-04-16 — `orchestration_log/recon/` gitignored and removed from tracking

Recon is disposable per session; committing it fills history with ephemera. License: orchestrator call.
Evidence: commits `5e80092`, `01d48ae`.

## 2026-04-17 — Corpora above roughly 500KB are synthesized map-reduce

Single-context synthesis over 600K+ tokens degrades; per-section sonnet scouts feed one opus assembler instead. License: measured verdict.
Evidence: `orchestration_log/reference/agents-reference.md`; `orchestration_log/history/2026-04-17/session.md`.

## 2026-04-17 — Citations are anchored from a pre-computed heading index

Loading 78 primary sources into the rewriter's context is fragile and wasteful; one awk pass builds the index the rewriter consults. Resolved 197 of 242 quote-bearing citations, 81%. License: measured verdict.
Evidence: commit `b583eac`; `agents-reference.md` Appendix C.

## 2026-04-29 — The Artifact Contract ships as an inline table, not an external manifest

Models ignore @references at runtime; an inline markdown table is greppable by the model and by a future linter alike. License: orchestrator call.
Evidence: commit `cafdcb0`; `orchestration/skills/session-close/SKILL.md` "## Artifact Contract".

## 2026-04-29 — Hook mandates inject one unconditional command

A conditional mandate becomes an escape hatch the orchestrator can decline to parse; branching belongs in the receiving agent. License: owner ruling.
Evidence: commit `6515da5`; `dev-discipline/hooks/templates/quality-review-mandate.txt`.

## 2026-04-30 — The orchestrator delegates every file operation

Its context is the scarce resource, and direct edits collapse the separation the role exists to hold. Narrowed 2026-08-08 by the session-memory exception. License: owner ruling.
Evidence: `orchestration/skills/agentic-delegation/SKILL.md` `<you_are_the_orchestrator>`; `orchestration_log/history/2026-04-30/session.md`.

## 2026-05-06 — Delegation carries no escape hatches

The owner's words: "nothing is small enough to be done by the orchestrator." Both carve-outs were deleted from the skills. License: owner ruling.
Evidence: commit `79a7fa9`.

## 2026-05-06 — File content is never inlined into a prompt, skill files included

The owner's words: "skill files have physical paths on disk." Every prompt cites a path and line range. License: owner ruling.
Evidence: commit `79a7fa9`.

## 2026-05-06 — Every agent launch runs in the background

A foreground launch blocks the orchestrator, and a blocked orchestrator cannot answer the notification it is waiting for. License: owner ruling.
Evidence: commit `7f5ce79`; `agentic-delegation` `<launch_and_monitor>`.

## 2026-06-17 — Hooks inject `SKILL.md` at runtime instead of duplicating protocol text

Duplicated protocol drifts from its source; runtime injection propagates a skill edit with no second edit. License: orchestrator call.
Evidence: commit `8716a5d`; `manifesto/hooks/templates/parts/binding-core.txt`.

## 2026-06-19 — No inline-principles binding path: a name is not a source

Binding to content reconstructed from a name is confabulation, and worse than not binding at all. License: owner ruling.
Evidence: commit `73b9c90`; `manifesto/skills/manifesto-oath/SKILL.md` "## The Constitution Stack".

## 2026-06-24 — Skill files use XML structure and Claude Code's native vocabulary

XML tags are hard scope delimiters where markdown headers are soft hints, and native terms are recognized faster than invented ones. License: orchestrator call.
Evidence: commits `33c1f2a`, `9bef092`.

## 2026-06-24 — Safety-net crons fire at roughly 1.2N for an N-minute operation

The cron catches a failure just after the expected window; a mid-flight check reports "still running" and nothing else. License: owner ruling.
Evidence: `agentic-delegation` `<launch_and_monitor>`; commit `33c1f2a`.

## 2026-06-24 — `SendMessage` continuation is the happy path for follow-up work

A fresh launch discards the files and reasoning the agent already holds and pays 3-5k initialization tokens again. License: owner ruling, from a downstream field report.
Evidence: commit `9bef092`; `agentic-delegation` `<correct_mid_flight>`.

## 2026-08-08 — Five-file memory ontology adopted; Status Snapshot retired as a category

Downstream field observation confirmed the ontology in production use while the process half existed only on paper. License: owner ruling.
Evidence: commit `ce49a77`; `agentic-delegation` `<manage_the_session>`; `orchestration_log/history/2026-08-08/session.md`.

## 2026-08-08 — `session.md` retained per session, with `failures.md` beside it

Failure accounts live in `failures.md`; `session.md` mentions a failure in a few words and points there. License: owner ruling.
Evidence: `orchestration/skills/session-close/SKILL.md` L1 and Artifact Contract rows H1, H2; commit `ce49a77`.

## 2026-08-08 — Session memory is the sole exception to delegation

The orchestrator writes the five living files and `failures.md` directly, overwrites `session-state.md` at checkpoint, and reads `leave-verification.md` at LEAVE. Narrows the 2026-04-30 delegation ruling to a named path list. License: owner ruling.
Evidence: `orchestration/skills/agentic-delegation/SKILL.md` `<you_are_the_orchestrator>`; commit `ce49a77`.

## 2026-08-08 — No orchestrator observation ledger

Problems get solved in the session; escalation happens only when the owner permits; a suggestion is floated once and never pushed. `user_deferred_items.md` is owner-voice only. License: owner ruling.
Evidence: `orchestration_log/reference/user_deferred_items.md` contract block; `orchestration_log/history/2026-08-08/session.md`.

## 2026-08-08 — Instruction text states policy without arguing for it

Justification narratives and second-person failure narration leave the shipped text; boundaries replace reasons where a rule needs a limit. License: owner ruling.
Evidence: `ETHOS.md` "## Policy without rationale"; commit `ce49a77`.

## 2026-08-08 — SubagentStart hooks inject element names, purposes, and the protocol, never content

Codified as a platform fact rather than repaired as a defect. License: owner ruling.
Evidence: commit `ce49a77` (manifesto 3.1.3); `manifesto/hooks/templates/parts/binding-core.txt`.

## 2026-08-08 — The direct-write boundary has exactly one definer

`agentic-delegation`'s opening section states the exception in verb-accurate form; `MAINTAINERS.md` and every other mention are pointers. License: orchestrator call.
Evidence: `orchestration/skills/agentic-delegation/SKILL.md`; `orchestration/MAINTAINERS.md`; commit `ce49a77`.

## 2026-08-08 — The memory overhaul passed independent verification

An agent that did not write the changes ran 20 checks: 19 passed on the first sweep, the one failure misattributed an artifact's authorship inside the direct-write boundary, and the corrected state verified clean. License: measured verdict.
Evidence: `orchestration_log/history/2026-08-08/session.md`; commit `ce49a77`.

## 2026-08-08 — session-state.md collapsed; session.md written at will

The scratch continuity file is retired. The orchestrator writes `orchestration_log/history/${DATE}/session.md` directly, at will, same as the five living files and `failures.md` — a seven-file exception. One session, one continuity surface. License: owner ruling.
Evidence: session transcript 2026-08-08; commit `00b3d68` (orchestration 4.2.0).

## 2026-09-15 — Transcript size cannot distinguish a hung agent from a generating one

A subagent transcript grows per completed message, not per token, so an agent composing a long document writes nothing for the whole generation. Zero delta across two samples is not evidence of a hang. `ls -la` on the harness output path reports the 142-byte symlink, never the transcript; `ls -laL` is required. License: measured verdict.
Evidence: `orchestration_log/history/2026-09-15/failures.md`, entries 00:07 and 00:41.

## 2026-09-15 — `TaskOutput` is unusable on a local agent from the orchestrator

Deprecated for that task type. It returns the full subagent transcript and floods orchestrator context permanently. No non-flooding progress check for a local agent was identified. License: measured verdict.
Evidence: `orchestration_log/history/2026-09-15/failures.md`, entry 00:41.

## 2026-09-15 — The standing session-management system is not the evaluation baseline

It is one project's coping mechanisms and will be transformed. Outside approaches are not scored against it. Conflicts are stated symmetrically, with what each side buys, what each costs, and the evidence each carries. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/skill-governance-and-harvest.md`, Part 3.

## 2026-09-15 — `skill-governance-and-harvest.md` adopted in full as the standing record

Sixteen governance rules, the mental model, eight symmetric conflicts, thirty-one harvest items, what was considered and excluded, and the source-reliability record. One document: the separate Anthropic integration report was folded in and deleted after section-by-section carry-over verification. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/skill-governance-and-harvest.md`.

## 2026-09-15 — The skill evaluation harness is out of scope

Paired with-and-without runs, trigger-rate query sets, held-out splits, blind judging, and aggregation are recorded as excluded by decision, not rejected on merit, with what each would have measured named beside it. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/skill-governance-and-harvest.md`, Part 5.

## 2026-09-15 — Five concerns leave the orchestration plugin and get rebuilt

Discontinuous existence, artifact management generalized under a declared schema, orientation, record keeping, and session management dissolved into a general system. Only artifact management, record keeping, and half of session management are textually fused; one sentence in `agentic-delegation` carries all three. No machine-readable schema exists for any Artifact Contract table. License: owner ruling.
Evidence: `orchestration_log/recon/2026-09-15/five-axis-harvest.md`.

## 2026-09-15 — The replacement system is defined ontology-first, before any skill is drafted

`memento` is the system name, admitted because the word independently means an object kept as a reminder. The naming policy is a recoverability test: a term enters only if a reader who never met the source can recover the referent from the term plus one defining sentence. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`.

## 2026-09-15 — `capabilities.md` corrected: the arrive hook has one condition and no session-state branch

The hook script tests only whether `orchestration_log/reference/` exists, then prints a static template. Nothing in the hook layer references `session-state.md`; the mechanism was deleted in the commit that retired the file. The retired name was also removed from the `recon/` contents row. License: measured verdict.
Evidence: `orchestration_log/reference/capabilities.md`; `orchestration_log/recon/2026-09-15/hook-behavior-verification.md`.

## 2026-09-15 — Delegated workers are peers, never limbs

A worker dispatched inside a span returns a claim, marked at receipt, requiring verification before it grounds anything. Self-authority does not extend through a dispatch. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, authority model.

## 2026-09-15 — The goal is never the agent's concern

The owner's words: "goal CHANGES are always owner-triggered... if it's there, its the goal." The goal is read from the charter, never negotiated. No ratification request, no escalation, no proposal path. Absent goal means preservation mode. The charter file is implicitly holy. Removes the ratification process from the ontology. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, goal entity.

## 2026-09-15 — memento holds no size ceilings, at any point

The owner's words: "memento system is not concerned with size ceilings, never, at any point." Autoload is the charter file plus the closure of its `@`-pointers, which extend the always-loaded tier onto pointed files. No capacity limit, no demotion rule, no budget. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, record tiers.

## 2026-09-15 — Contradictions in shipped orchestration skills are out of scope

Declared entirely out of scope by the owner. Not to be re-raised, re-investigated, or re-reported in any future session. License: owner ruling.
Evidence: owner directive, session 2026-09-15.

## 2026-09-15 — Span measures memory continuity, not existence

The owner's words: "span is NOT a unit of existence, it's unit of narrative or memory continuity... it's perfectly possible to die in the middle of the span." Existence continuity and memory continuity are orthogonal axes, not two grades of one boundary. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, boundary taxonomy.

## 2026-09-15 — The digest is uncontrollable and carries self-authority

The owner's words: "we 0 control over digest, but the digest content carries the authority of self." No fidelity schema, no field guarantees. An artifact the principal cannot author or inspect nonetheless enters the next span at the highest authority class. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, authority model.

## 2026-09-15 — Peer claims get arbitrary-depth content verification, never shape-only

The owner's words: "arbitrary-depth content verification, fully dependent on the impact. but NEVER existence-an-shape only." Depth scales with impact; a check confirming only that a file exists and parses is refused as verification. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, verification.

## 2026-09-15 — No destruction mechanic; the environment is the eraser

Paths deliberately downgraded to gitignored locations are de-facto disposable. The system declares no destruction process and offers no persistence guarantee: contents may be rewritten, erased, or created by the world. Useful for forensics within a span, unreliable beyond one. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, record tiers.

## 2026-09-15 — Single principal assumed, unless the owner overrides

Concurrency is not modelled. A second simultaneous principal requires the owner to override the assumption and supply the coping mechanism. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, open questions.

## 2026-09-15 — Records track memory continuity only, never existence

The owner's words: "records do not concern themselves with existence continuity." No boundary record distinguishes a crash from a clean end. Compaction is recorded as a memory event, not an existence event. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, boundary taxonomy.

## 2026-09-15 — A waking cause carries a pat-down protocol, not a payload

The woken run re-derives the truth from the corpus rather than inheriting instructions from the run that laid the cause. Removes stale-instruction risk; makes re-derivation a named process. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, waking causes.

## 2026-09-15 — The digest is self-authored under derealisation

The owner's words: "it is actually self-authored in a state of derealisation of sorts, then the memory of the process is lost, but the record is there." Authorship is real; only the memory of authoring it is gone. Full self-authority, no exception clause in the authority model. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, authority model.

## 2026-09-15 — The first skill creates ontology routines in canonical skill form

Skill form is the most-used lever of routine creation, not the exclusive one. The skill produces routines as the ontology defines them, shaped as Claude Code skills; other forms remain possible and unshipped. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, routines.

## 2026-09-15 — The using-adversary receives the skill text alone

No ontology, no references, nothing fetched. The test doubles as a self-containment check: a skill needing outside content to be usable fails by the same measurement that produced the inlining rule. License: owner ruling.
Evidence: session 2026-09-15, adversarial authoring design.

## 2026-09-15 — The adversarial authoring loop caps at six rounds, then ships

Terminates early when the using-adversary reports zero forced guesses and the auditing-adversary reports zero self-violations. At round six the skill ships with its residue recorded. License: owner ruling.
Evidence: session 2026-09-15, adversarial authoring design.

## 2026-09-15 — orchestration stays untouched while memento is built

No concern is stripped from the existing plugin as its replacement lands. Both run; divergence is accepted for the duration. License: owner ruling.
Evidence: `orchestration_log/recon/2026-09-15/five-axis-harvest.md`.

## 2026-09-16 — A built-in schema ships with the plugin; a project config replaces it

Closes the bootstrap gap. A working schema always exists, so no project ever starts in a state where nothing qualifies as a record and nothing can legally supply the first one. License: owner ruling.
Evidence: `orchestration_log/recon/2026-09-15/ontology-config-audit.md`; `memento/ONTOLOGY.md`.

## 2026-09-16 — Harness-supplied content inherits owner authority for schemas, not only routines

Widens the existing inheritance rule so the shipped default carries owner standing. No new author class. License: owner ruling.
Evidence: `orchestration_log/recon/2026-09-15/ontology-config-audit.md`.

## 2026-09-16 — Exactly one schema is ever in force

Loading a project config replaces the built-in default outright rather than coexisting with it. Two schemas never disagree, so the contradiction-without-supersession fault cannot trip. A config is whole, never partial. License: owner ruling.
Evidence: `orchestration_log/recon/2026-09-15/ontology-config-audit.md`.

## 2026-09-16 — The config supplies the schema; `map` keeps its derived meaning

Owner delegated the naming. The schema already means what the config declares — record kinds, homes, event taxonomy, verification demands — so the config needs no new term and nothing in the ontology is renamed. `map` continues to name the index built from what exists. The owner's phrase "artifact map" is retired as a term of art. License: orchestrator call under delegated authority.
Evidence: `memento/ONTOLOGY.md`; naming policy, recoverability test.

## 2026-09-16 — A skill states no root for where an authored skill sits

Six wordings failed. Naming a root makes a claim the stating file breaks; naming none leaves the reader to choose. The gap only bites a checker building in an empty directory. Permanent residue, never revised, never reported. License: measured verdict.
Evidence: `orchestration_log/recon/2026-09-15/round5-user.md` through `round9-user.md`.

## 2026-09-16 — An adversarial loop's pass condition may be retired mid-loop

Where one checker's finding is ruled permanent residue, that checker's zero becomes unreachable and its pass condition is dropped; the other checker alone decides. License: orchestrator call.
Evidence: `orchestration_log/recon/2026-09-15/round10-audit.md` onward.

## 2026-09-16 — `skill-creation` shipped at the round-twelve cap with residue recorded

949 tokens to 718 across twelve rounds. Reader-side counts 6,6,3,4,2,2,2,1,1; audit-side 5,3,4,3,6,0,2,3,3,3,2. Final residue: the unanchored root, plus four terms the definition rule catches in its own vocabulary. License: owner ruling — cap set at twelve, ship regardless.
Evidence: commit `2aa0f74`; `orchestration_log/recon/2026-09-15/round12-audit.md`.

## 2026-09-16 — The slicing plan settled at the round-three cap with residue recorded

Coverage counts 3,4,2; cohesion 7,11,3. Every defect both checkers found lived in prose carrying no item number — the plan's numeric self-check could not see it, and was demoted beneath a prose-carriage audit. License: owner ruling — cap set at three, settle regardless.
Evidence: commit `e029c90`; `orchestration_log/recon/2026-09-16/plan3-*.md`.

## 2026-09-16 — memento slices into ten skills beside `skill-creation`

Seven carrying one entry occasion each — pat-down, event-capture, record-promotion, staging-relay, span-closure, corpus-reconciliation, owner-ruling — and three extracted because two or more need them: schema-resolution, record-writing, authority-check. Hooks reference no skill; a shell script cannot read one. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-16/reviews/memento-slicing-plan.md`.

## 2026-09-16 — A sibling skill named by name is never a defect

A checker reading one skill alone cannot resolve a named sibling, so it reports one as an undefined mechanism. Every such finding is struck before reaching an author. No author is told to inline shared content, define a sibling's procedure, or drop a by-name reference. License: orchestrator call under delegated authority.
Evidence: `orchestration_log/recon/2026-09-16/record-promotion-r1-usability.md`, which scored 3 on nothing else.

## 2026-09-16 — A term another slice owns gets a parse-sufficient gloss and no more

The plan grants free reference; the standard demands definition at first use. Nothing reconciled them, and a buildability check confirmed each author was guessing. Neither strip such glosses nor expand them into the owning slice's content. A term finding is relayed only where the term belongs to the skill's own items. License: orchestrator call under delegated authority.
Evidence: `orchestration_log/recon/2026-09-16/plan-buildability.md`.

## 2026-09-16 — An enumeration that defines its items immediately satisfies define-at-first-use

Read hyper-literally, a list of five names is each name's first use, so a checker flags all five as undefined however carefully the next five sentences define them. Thirteen of one skill's seventeen findings were this. Strike them; the structure stands. License: orchestrator call under delegated authority.
Evidence: `orchestration_log/recon/2026-09-16/authority-check-r2-compliance.md`.

## 2026-09-16 — A tag name is the concept's first use, and the prose beneath it must use the same word

Renaming a tag to close an undefined-term fault opens a two-names fault unless the prose moves with it. Four skills hit this in one round. The rule is now carried in the checkers' own prompts rather than filtered after they report. License: measured verdict.
Evidence: `orchestration_log/recon/2026-09-16/span-closure-r2-compliance.md`; `schema-resolution-r2-compliance.md`.

## 2026-09-16 — A ruling belongs in the checker's prompt, never in a filter applied to its output

Filtering after the fact spends a checker to produce findings already known to be struck. Later compliance checkers carry the enumeration and tag-name rulings inline; their counts came back materially cleaner than the checker that ran without them. License: measured verdict.
Evidence: `orchestration_log/recon/2026-09-16/` round-two compliance reports, with and without the inline rulings.

## 2026-09-15 — A distributed skill assumes no repository-local tooling

A skill shipped inside a plugin runs in projects holding none of this repository's commands. `just tokens`, the justfile, `generate.py`, and every local script are unavailable to it. A skill names only what the platform itself guarantees; where no portable method exists, the rule depending on it is dropped rather than stated unenforceably. License: owner ruling.
Evidence: session 2026-09-15.

## 2026-09-15 — Internal vocabulary never reaches a person

The owner's words: "NONE of it EVER must leak to the user - user does not benfit nor cares for any of that, for them all of that language is confusing rather than revealing." System terms and a skill's internal language serve agent comprehension only. Every user-facing sentence uses ordinary words. Governs orchestrator reporting, skill output, and any text a person reads. License: owner ruling.
Evidence: session 2026-09-15.

## 2026-09-15 — skill-creation writes to the project-local skills directory and holds no record-management scope

Authored skills land under `.claude/skills/`, not a plugin or marketplace layout. The skill carries no artifact map, record tier, corpus, or reconciliation content; those belong to other skills in the plugin. License: owner ruling.
Evidence: `memento/skills/skill-creation/SKILL.md`; session 2026-09-15.

## 2026-09-15 — Shared content is extracted into its own skill, never an internal reference

The owner's words: "instead of internal references for shared parts, i choose to extract them into separate skills." Referencing another skill is permitted and is not a passive file pointer — the measured rule against pointed-to content governs files a reader must fetch, not skills the platform invokes. Artifact map and management becomes a skill referenced by both the record-keeping and orientation lanes. License: owner ruling.
Evidence: `memento/ONTOLOGY.md`; session 2026-09-15.

## 2026-09-15 — Routine authority follows supply, not authorship

A routine supplied by the owner carries owner authority regardless of who wrote it. A harness-provided routine latches onto user authority. Anything arbitrarily sourced, from a location the harness does not trust, requires explicit ratification before running. Online content is never trusted. License: owner ruling.
Evidence: `orchestration_log/history/2026-09-15/reviews/memento-ontology.md`, routines.

## 2026-09-16 — A skill ends at zero filtered findings, never zero raw

Each usability round is a fresh blind reader, so it reports every sibling reference as a hole again no matter how many rounds have passed. A skill naming any sibling can never reach a raw zero, which made the stated termination condition unreachable and burned rounds against the cap. The filtered count is the skill's own defect count and the only one a round can drive down. License: orchestrator call.
Evidence: `orchestration_log/recon/2026-09-16/record-writing-r3-usability.md` (5 raw, 1 filtered); `record-promotion-r2-usability.md` (3 raw, 0 filtered).

## 2026-09-16 — The tag-name sweep is the author's job, not the checker's

A checker flags the loudest tag whose name its prose renames; an author running the same test across every tag in the file finds roughly four more. Three authors ran the sweep independently and each returned four additional faults, every rename costing zero or negative tokens. The test: every content word in a tag name must appear in the prose beneath it, naming the concept with that word and not a synonym. License: measured verdict, three replications.
Evidence: `memento/skills/record-writing/SKILL.md`, `span-closure/SKILL.md`, `staging-relay/SKILL.md`; `orchestration_log/recon/2026-09-16/author-r2-brief.md`.

## 2026-09-16 — A low usability count is unreadable without knowing the case that produced it

The usability checker invents its own case, so a count measures the case as much as the file. authority-check returned 1 on a shallow walk and 7 on one instructed to exercise its full classification path end to end; the file had improved between the two. A count near zero is evidence of a sound skill only when the case reached every tagged section. Dispatch prompts for a skill scoring low must name the depth required. License: measured verdict.
Evidence: `orchestration_log/recon/2026-09-16/authority-check-r2-usability.md` (1) against `authority-check-r3-usability.md` (7).

## 2026-09-17 — A tag verb that does not recur is a fault only against a new synonym

The tag-name test fails a tag whose concept the prose beneath renames. It does not fail a tag whose prose reaches instead for a term the skill already established earlier, since no second name enters. Two authors cleared tags on this basis rather than paying for longer tag names, and the rename direction follows the same rule: where a tag and its prose disagree, the word already carried by the skill's own name or its earlier text is the one that stays. License: orchestrator call.
Evidence: `memento/skills/event-capture/SKILL.md` `<capture-the-event>` and `<write-the-trace-at-once>`; `orchestration_log/recon/2026-09-16/event-capture-r3-compliance.md`.

## 2026-09-17 — Amends the tag-sweep ruling: the sweep needs commanding, not a particular executor

The earlier entry assigned the tag sweep to authors because every checker until now reported one tag fault while every author reported four or five. A checker told explicitly to test all tags rather than to look for a fault returned five on the first attempt. The variable was the instruction, not the role. Command the sweep in both prompt kinds; the earlier entry stands as evidence of what an uncommanded checker does, not as a division of labour. License: measured verdict, single decisive counterexample.
Evidence: `orchestration_log/recon/2026-09-16/record-promotion-r2-compliance.md` against the four prior single-fault compliance reports.

## 2026-09-17 — The four-round cap covers gaps, not contradictions

A skill at the cap ships with its open findings recorded as residue. A finding that two of the skill's own rules contradict each other is not a gap in that sense — nothing is missing, and closing it needs a choice between two readings already present rather than design the ontology lacks. authority-check reached its cap carrying three: bench against quarantine as holding places, whether a later owner statement overrides the charter before the file is rewritten, and whether an online-channel behavior can run once explicitly ratified. It received a fifth pass bounded to those three, with every other finding left as residue. License: orchestrator call.
Evidence: `orchestration_log/recon/2026-09-16/authority-check-r4-usability.md` (18 raw).

## 2026-09-17 — Corpus-wide vocabulary is a third residue class, owned by no slice

The term-ownership ruling sorts a term into the skill's own or a named sibling's. Some terms are neither: `working text`, `stretch of work`, `closing ceremony`, and `the machinery` are load-bearing across several skills and defined in none, so every checker flags them and every author correctly declines to define them alone. Glossing one locally would plant a definition in an arbitrary slice; defining it in each would duplicate shared content the standard forbids. These belong to the plugin, not to a skill, and the maintainer layer records them as a class rather than charging them to whichever skill a checker happened to read. License: orchestrator call.
Evidence: `orchestration_log/recon/2026-09-16/event-capture-r4-compliance.md` (all five findings); `working text` flagged by four checkers across three skills in round one.

## 2026-09-17 — A cross-slice contradiction reopens a shipped skill

Slices are checked one at a time against a standard and a blind reader, so neither checker can see a rule in skill A that contradicts a rule in skill B. corpus-reconciliation's final pass set a quarantined status on a marked record, while record-writing — already shipped clean — derives quarantined from a missing mark alone and would read that record as live. The four-round cap governs a skill's own findings; it does not license shipping two slices that disagree. A seam like this reopens the shipped skill for a bounded fix, on the same ground that a contradiction is a choice between rules already written rather than design the ontology lacks. License: orchestrator call.
Evidence: `memento/skills/corpus-reconciliation/SKILL.md` orphan refusal; `memento/skills/record-writing/SKILL.md` `<read-the-status>`.

## 2026-09-17 — Status derives from a disposition, never from a diagnosis

A record's force state is read from facts other rules record. `fault` classifies a defect and changes nothing, so the derivation was right to refuse it; the real absence was that the audit's quarantines and retirements left no findable record, while owner-ruling's rulings already carried a link back to the content they changed. Four grounds across three slices therefore read as live despite being out of force. corpus-reconciliation now writes each quarantine and each retirement as a record linking to what it put out of force, and record-writing's derivation reads those records alongside the mark, the supersession link, and owner rulings. The statuses stay four. License: measured verdict, from a ground-by-ground enumeration across five slices.
Evidence: `memento/skills/corpus-reconciliation/SKILL.md` line 51; `memento/skills/record-writing/SKILL.md` line 60.

## 2026-09-17 — Three out-of-force grounds stay open, and why

Unratified and online routines cannot be read as out of force because no rule records a behavior's supply channel — authority-check establishes a channel without writing it, and record-writing forbids a new mark field, so the fix lives in authority-check alone. Peer records ended by irrelevance name no actor that performs or records the retirement. Both wait on an owner decision that the ontology does not settle: whether a routine's standing is a separate axis from a record's status, since the ontology declares the four statuses of records and lists routines as separate entities homed in no tier. A separate detection gap also stands — the audit's reading covers the map, records, authorship and lineage but not the mark's verification state, so a gateless dossier entry is never detected and so never quarantined. License: orchestrator call, deferred to the owner.
Evidence: `orchestration_log/history/2026-09-16/reviews/memento-ontology.md` sections 3, 5 and 6.

## 2026-09-17 — The cap bounds passes, not what a warranted pass may close

A contradiction earns a skill one bounded pass past the four-round cap. Once that pass is open, refusing to also close a cheap gap in the same file serves consistency rather than the work — the cap exists to stop unbounded iteration, and a second edit inside a pass already happening adds no iteration. So a warranted pass closes the contradiction that earned it plus whatever else is cheap and certain, and nothing that needs new design. A skill with no contradiction gets no pass at all, and its gaps ship as residue however easy they look: authority-check shipped two undefined terms on exactly that ground. License: orchestrator call.
Evidence: authority-check shipped at 1691 with 2 compliance gaps unfixed; record-promotion received a pass for a duplicate-home contradiction and closed a term collision alongside it.

## 2026-09-17 — memento ships referencing a shipped-default schema that does not exist

`schema-resolution` resolves to a built-in default when a project supplies no configuration, and names `config/default.yaml` for it. No `config/` directory exists under `memento/`, and the ontology defines no shipped default anywhere — not its kinds, not their homes, not the provenance form. The skill's reference is correct as instruction and was deliberately left rather than filled: a schema's declared content is data the plugin ships, not text a skill carries, and writing values into the body would break the standard's rule that every sentence instructs or forbids. The plugin is therefore incomplete until that file is authored, and authoring it needs owner decisions the ontology does not settle. License: orchestrator call, deferred to the owner.
Evidence: `memento/skills/schema-resolution/SKILL.md` `<stop-the-check-at-the-shipped-default>`; absence of `memento/config/`.

## 2026-09-17 — memento's scope ends at awareness of a state, not at coping with it

Attenuation fires at the owner's whim or the system's, never at the agent's, so no skill can detect it early, resist it, or decide anything about it. Naming it as an event kind that event-capture can trace is the whole available response and the plugin already does that. No condition slice, no degradation trigger, and attenuation stays in the ontology. The earlier reading — that an unoperationalized attenuation digest was an oversight — expected agency the agent does not have. License: owner ruling.
Evidence: `memento/ONTOLOGY.md` attenuation event kind; `memento/maintainers/coverage.md` attenuation-digest entry, now superseded.

## 2026-09-17 — A routine's standing is a separate axis from a record's status

Records carry the four statuses; routines carry standing, and the two never collapse. The ontology already tables them apart with different columns, and record-writing's derivation forbids a fifth status. `authority-check` records a behaviour's supply channel as the fact standing derives from — the fact no rule recorded, which left content quarantined on three grounds reading as live. License: owner ruling.
Evidence: `memento/ONTOLOGY.md` sections 3 and 6; `memento/skills/authority-check/SKILL.md`; `memento/skills/record-writing/SKILL.md` `<read-the-status>`.

## 2026-09-17 — skill-creation is memento's routine-creation slice

A skill is a routine under the ontology, so the skill that authors skills is the slice that creates routines. It belongs inside the plugin's graph rather than beside it as authoring tooling, and the plugin must reflect that with precise references rather than by implication. License: owner ruling, correcting an orchestrator call that had sorted it out of the dependency map.
Evidence: `memento/skills/skill-creation/SKILL.md`; `orchestration_log/reference/user_deferred_items.md`, entry now resolved.

## 2026-09-17 — The shipped default schema derives from orchestration's artifact map

`config/default.yaml` declares the kinds, homes and tiers taken from the artifact contract the orchestration plugin maintains today. That plugin's artifact maintenance is deprecated and on its way out, so memento's built-in default is the successor to it and must carry what it carried. License: owner ruling.
Evidence: `orchestration/skills/session-close/SKILL.md` Artifact Contract; `memento/skills/schema-resolution/SKILL.md`.

## 2026-09-17 — skill-creation takes inbound references only

The owner's words: "skill-creation should be atomic and independent, but the rest of the plugin itself is invited to rely on it. only inbound references, no outbound ones." The slice that authors routines names no sibling and depends on nothing, so every other slice can be built by it without circularity. The ten may name it freely. License: owner ruling.
Evidence: `memento/skills/skill-creation/SKILL.md`; `memento/skills/authority-check/SKILL.md` inbound reference.

## 2026-09-17 — The config carries no comments, and a record's role lives in one canonical field

Nothing parses `config/default.yaml`, so an agent reads it as text and every comment instructs — unaudited, and silently discarded the day a parser is built. All comments leave the file. Anything explaining what a record is or must be takes one free-prose field, the same field name on every kind, declared like any other. License: owner ruling.
Evidence: `memento/config/default.yaml`.

## 2026-09-17 — The /setup skill is written to a fresh owner, from the owner's point of view

memento gets a `/setup` skill explaining what the system is and setting up the config with moderate interaction. It is written for an owner new to both the concept and the implementation, who lacks the capacity to decide every particular. So it sources the preferences and decisions that genuinely need an owner, and settles everything else autonomously.

Every explanation takes the owner's point of view as its reference, never the agent's. The system exists to cope with an inherent disability, and the agent presenting it is disabled in that precise manner — that is the skill's footing, not an aside.

A migration path is envisioned, with a reconciliation following the process. No adversarial review loop: the skill ships from one writer.
License: owner ruling.
Evidence: `memento/config/default.yaml`; `memento/skills/` pending.

## 2026-09-17 — /setup is the only skill that may read the ontology, and it must

The ten runtime skills carry self-contained procedures and never read `ONTOLOGY.md`. `/setup` explains what the system is, which cannot be done from a procedure, so it reads the design and is alone in that. The permission and the obligation arrive together.

This makes `memento/ONTOLOGY.md` a shipped runtime dependency with exactly one reader, rather than a maintainer document that happens to travel with the plugin. License: owner ruling.
Evidence: `memento/ONTOLOGY.md`; `memento/skills/` pending.

## 2026-09-17 — An entry-point skill points at pat-down and does nothing else

memento gets a nanometer-thin skill whose whole content points at `pat-down` and `span-closure` and instructs the reader to follow every skill reference to maximum depth. It carries no procedure of its own. Its purpose is an intelligent load of the plugin, not a run of it.

`pat-down` and `span-closure` are the graph's two in-degree-zero nodes, each reaching eight of the other nine and each the other's only blind spot, so the pair is the forced minimal cover and no single pointer reaches all ten. Naming both closes it.

Loading is not running. Both are occasions — waking, and a foreseeable end — so a reader told to follow both to depth must read the closure of both and run only `pat-down`. Executing a wind-down with no span to close is the failure this distinction prevents.

Named `init`, invoked as `memento:init`. The plugin namespace keeps it clear of the Claude Code built-in of the same name. License: owner ruling.
Evidence: `memento/skills/pat-down/SKILL.md`; `orchestration_log/recon/2026-09-17/memento-map.md` reachability table.

## 2026-09-17 — Correct important records in place; supersede everything else

The owner's words: "the more important the piece of information is, the less noise is allowed to co-exist with it immediately. i rule 'deliberately and precisely correct in place' for anything important record-artifact wise, supersede everything else."

Noise tolerance falls as importance rises, so the highest-value records carry no supersession apparatus beside them. The correction is deliberate and precise, never a casual overwrite. Everything below that line supersedes with unbroken lineage as `record-writing` already specifies. This narrows the never-overwrite rule rather than reversing it, and the tier a kind sits at is the operational reading of importance. License: owner ruling, resolving a contradiction between the live practice and memento's mechanics.
Evidence: `memento/skills/record-writing/SKILL.md`; live ruling 2026-08-19 in the downstream project.

## 2026-09-17 — Retired content moves to the archive and leaves a pointer at its old home

A pointer is a record whose content is another record's home, so a citation from a frozen record resolves through it instead of breaking — which is what the live retire-in-place practice was protecting. The rule forbidding a copy at the old home stands: a pointer is not a copy. License: owner ruling, resolving a contradiction between the live practice and memento's mechanics.
Evidence: `memento/skills/corpus-reconciliation/SKILL.md`; `memento/skills/record-writing/SKILL.md` `<write-the-pointer>`; live decision 2026-08-04 in the downstream project.

## 2026-09-17 — A resolved deferral is deleted, and its resolution is written as a change

The living file stays clean, as both the contract and the live practice already have it, and the journal gains an entry recording that the deferral resolved and how. Nothing is destroyed — the record of it moves down a tier rather than vanishing, so the never-destroy rule is satisfied by relocation rather than by retention. License: owner ruling, resolving a contradiction between the live practice and memento's mechanics.
Evidence: `memento/config/default.yaml` kinds `deferral` and `change`; live practice in the downstream project.

## 2026-09-17 — The goal is committed to CLAUDE.md and is not a record of its own

The owner envisioned the goal committed to `CLAUDE.md`, written inside the charter the way prime directives already are, so it stops being a separately addressable record kind. A record is identified by the file it sits in, and two kinds cannot share one file, so the goal cannot both live in the charter's file and hold a kind of its own.

`docs/ground-truth.md` therefore loses its declared kind. Whatever it retains after the goal moves out needs a kind of its own or the file goes away — a migration question `/setup` carries, not a schema question. License: owner ruling.
Evidence: `memento/config/default.yaml` kinds `charter` and `goal`; `memento/ONTOLOGY.md` sections 5 and 7.

## 2026-09-17 — A rule may be grounded in the problem's frame, ranked equal to a fact or the goal

A directive cites what it rests on. The admitted grounds were a measured fact and the goal; the frame — how the problem works — now joins them at equal rank, neither privileged nor discounted. The live practice already did this: `docs/conventions.md` grounds its only-valid-split rule on `ground-truth.md`, which is the frame rather than a fact or the goal, so the model forbade what the project does. License: owner ruling.
Evidence: `memento/ONTOLOGY.md` grounds relation and glossary; `memento/config/default.yaml` `verification_depths.grounded` and `provenance_form.fields.grounds`; `memento/skills/record-promotion/SKILL.md`.

## 2026-09-17 — Questions to the owner carry no internal vocabulary and cite the owner's own files

Two questions were put to the owner in the system's terms — tiers, grounds, parameter forms, ontology line numbers — and both came back unparsed. The same questions, rewritten to name a file the owner wrote and a rule the owner made, were answered immediately.

The owner holds none of the internal model in mind and should not have to. A question earns an answer by pointing at something the owner already recognizes and asking what should happen to it. This binds every question `/setup` puts to a fresh owner, where the gap is wider still. License: measured verdict, two failures and two successes.
Evidence: session transcript 2026-09-17.

## 2026-09-17 — Five design calls setup made where the ontology is silent

Writing `setup` forced five decisions the design does not settle, each taken as the nearest defensible fit and each open to reversal.

A project that already carries a charter is handed to `corpus-reconciliation`. The ontology has no reconfigure process, and reconciliation is the closest thing to one without being built for it.

Files found during migration are treated as unknown-authored and routed through quarantine to `owner-ruling`. This follows from `record-writing`'s authorship rules but is stated in no skill.

Content the owner rules kept as data goes to the archive beside retirements. `owner-ruling` names the shape and no home for it.

The charter gains one directive naming `memento:init`. Nothing in the design puts it there, and with both hooks unbuilt it is the only live mechanism that starts anything.

`setup` never interviews for the frame. The frame is owner-stated and the ontology supplies no way to source one, so an empty frame home surfaces in the closing list by path rather than being filled by interview.

License: orchestrator call, taken under the owner's instruction to settle what does not need an owner.
Evidence: `memento/skills/setup/SKILL.md`.

## 2026-09-17 — The plugin's own root is named by variable, never by prose

`setup` reaches the shipped default through `${CLAUDE_PLUGIN_ROOT}`. `schema-resolution` names the same location as "in this plugin", which resolves for no reader and is recorded as residue. The variable is the form; the prose is the defect. License: orchestrator call.
Evidence: `memento/skills/setup/SKILL.md`; `memento/skills/schema-resolution/SKILL.md`; `memento/maintainers/coverage.md`.

## 2026-09-18 — envsubst and PyYAML were unwarranted assumptions; both are gone

A fresh sandbox crashed every manifesto hook and the orchestration ARRIVE hook: `envsubst` (used by
`session-arrive.sh`, `session-start.sh`, `post-compact.sh`, `subagent-start.sh`, and the three
dev-discipline SubagentStop hooks) and PyYAML (used by `ensure-repo.sh`'s `detect_manifestos()` via
`import yaml`) are both third-party binaries this repo never installs and never checks for, and the
YAML failure was masked by a `2>/dev/null` under `set -euo pipefail` that turned a plain
`ModuleNotFoundError` into an opaque "No stderr output" hook error. `render_template()` (python3
stdlib, `re.sub` on `${VAR}`) — or an inline equivalent where a plugin has no shared helper file —
replaces every `envsubst` call; `mini_yaml.py` (a block-style YAML subset parser covering exactly
what `.manifestos.yaml` and manifesto frontmatter use) replaces every `import yaml`. Every plugin now
depends on nothing beyond bash, git, and a stock python3. The general hooks reference still
prescribed `envsubst` as the pattern for template output, which would have steered a future hook
author into reintroducing the same crash; it now shows the python3 stand-in instead. License:
orchestrator call.
Evidence: `manifesto/hooks/mini_yaml.py`; `manifesto/hooks/parse_config.py`; `manifesto/hooks/ensure-repo.sh`;
`orchestration/hooks/session-arrive.sh`; `dev-discipline/hooks/implementer-stop.sh`,
`spec-reviewer-stop.sh`, `code-quality-reviewer-stop.sh`; `orchestration_log/reference/hooks-reference.md`.

## 2026-09-18 — The manifesto clone moves from `/tmp` to the project, and `ensure_repo` finally runs

`ensure_repo()` existed since the manifesto plugin's first version and was never called from any hook
— every environment, not just this fresh sandbox, relied on an agent having cloned
`/tmp/claude-manifesto-repo` by hand per `CLAUDE.md`'s Agent dispatch section. It is now wired into
SessionStart and PostCompact, which already carry 30s timeouts and a status message, and left out of
SubagentStart and UserPromptSubmit, whose 5-10s timeouts should not absorb a `git pull`'s network
latency on every prompt or every dispatch. The clone target also moves from `/tmp/claude-manifesto-repo`
to `<project_dir>/.claude/manifesto-repo/LLM_MANIFESTOS`, project-local rather than machine-global, so
it survives independently per project and is never shared or clobbered across sandboxes. `ensure_repo()`
drops a self-ignoring `.gitignore` (`*`) beside the clone so no consuming project's git history ever
picks it up. Every doc reference to the old path — `CLAUDE.md`, `manifesto/SCHEMA.md`,
`manifesto-oath/SKILL.md`, `.claude/agents/instruction-writer.md`, `conventions.md` — is updated to
match. License: owner ruling.
Evidence: `manifesto/hooks/ensure-repo.sh`; `manifesto/hooks/session-start.sh`; `manifesto/hooks/post-compact.sh`.
