# Skill-Writing Stance — 2026-09-15

This project believes a model reading a skill does the least the text permits. It reports success anyway. It inlines every dependency. It measures compression instead of trusting judgment. It pairs each mandatory step with a checkable artifact. It treats a rule as unproven until an agent or hook is caught breaking it.

## Positions

**1.** Skills read with zero external reference; all essential content is inlined.
License: Owner ruling, forced by 3 measured failures in one session.
Evidence: ETHOS.md:7,9,11; history/2026-04-13/session.md Failure Log rows 3,4,10.
Conformance: 17 of 19.

**2.** Skills issue commands, not suggestions; emphatic markers are deliberate, capped at one per directive.
License: Owner ruling, overriding bridge-research advice to soften; refined by measured failure.
Evidence: ETHOS.md:15,17; decisions.md 2026-04-13; history/2026-06-17/session.md Phase 6.
Conformance: 19 of 19; 0 of 6 deep-read skills show genuine hedging (skill-stance-corpus.md:66).

**3.** Compression is measured, never estimated; tables and decision trees replace explanatory prose.
License: Owner ruling; revised repeatedly against measured token counts.
Evidence: ETHOS.md:21; decisions.md 2026-04-13; skill-stance-corpus.md:95 (8627→6120-token verified pass).
Conformance: 15 of 19 (3 measured violations: tdd, python-ast-mass-edit, uv-pyright-debug).

**4.** Skills produce file artifacts, never platform API calls.
License: Owner ruling.
Evidence: ETHOS.md:25.
Conformance: 11 of 19; 1 measured violation (qa-orchestration PR auto-merge routing, skill-stance-corpus.md:134).

**5.** User action verbs are delegation directives, but only inside four named orchestration skills.
License: Owner ruling.
Evidence: ETHOS.md:29.
Conformance: 4 of 19 — exact match, zero drift either direction.

**6.** Skill text states platform facts, never agent policy.
License: Owner ruling.
Evidence: ETHOS.md:33.
Conformance: 7 of 19; zero measured violations, rest scope-mismatch.

**7.** One-time hooks may be thorough; hook prompt text is externalized to templates and gated on config existence.
License: Owner ruling.
Evidence: ETHOS.md:37; decisions.md 2026-04-16.
Conformance: 0 of 19 — no SKILL.md is a hook implementation.

**8.** A skill's 5 core points survive compression as its untouchable spine.
License: Measured failure.
Evidence: ETHOS.md:41; history/2026-04-13/session.md Failure Log ("buried the lead," reverted).
Conformance: 1 of 19 (manifesto-writing).

**9.** Each phase gates on a verified artifact from the phase before it.
License: Owner ruling.
Evidence: ETHOS.md:45.
Conformance: 18 of 19.

**10.** Every mandatory step pairs a named artifact with an orchestrator-side check; self-report alone is untrusted.
License: Owner ruling, repeatedly reinforced by measured failure.
Evidence: ETHOS.md:49; history/2026-04-15/session.md Failure Log #3; history/2026-04-29/session.md Phase 6; history/2026-08-08/failures.md 03:20 entry.
Conformance: 11 of 19; remaining 8 blank (scope mismatch, not violation).

**11.** Instruction text states what to do and does not argue for itself.
License: Owner ruling.
Evidence: ETHOS.md:53,55,57,59; decisions.md 2026-08-08.
Conformance: 4 of 19; 15 measured violations, zero not-applicable.

**12.** A positive-only style directive needs an explicit negative list paired with it.
License: Measured failure.
Evidence: history/2026-04-30/session.md Failure Log ("render in natural language" produced labeled YAML).
Conformance: Not corpus-scored — session-behavior finding.

**13.** Delegation carries no escape hatch, except one narrow path for session-memory writes.
License: Owner ruling, narrowed after repeated measured failure.
Evidence: decisions.md 2026-05-06, 2026-08-08; history/2026-05-06/session.md Decisions; history/2026-08-08/session.md Timeline.
Conformance: Not corpus-scored; reflected structurally in agentic-delegation's forbidden-pattern table (skill-stance-corpus.md:102).

**14.** A name is not a source; a constitution element binds only from loaded primary text.
License: Owner ruling, reversal after an identified confabulation vector.
Evidence: decisions.md 2026-06-19; history/2026-06-19/session.md Phase 2; skill-stance-corpus.md manifesto-oath:30.
Conformance: Not corpus-scored; single-skill rule, no violation found in its one applicable site.

**15.** Skill files structure themselves in XML lifecycle tags, not markdown headers.
License: Orchestrator call.
Evidence: decisions.md 2026-06-24; history/2026-06-24/session.md Failures table row 1; skill-stance-corpus.md:20,31.
Conformance: 1 of 19 (agentic-delegation); unpropagated to its own declared extensions.

**16.** `/cost` output is the sole trusted cost source; no manual counting, no estimation.
License: Measured verdict.
Evidence: decisions.md 2026-04-15; history/2026-04-15/session.md Decision Log ("$800 from JSONL when actual cost was $132"); skill-stance-corpus.md:190 (session-close.md:113).
Conformance: 1 of 19 (session-close; corpus's top-ranked skill).

## Load-bearing

1 — measured failure, 3x in one session.
2 — measured failure (marker-stacking found and reverted) plus universal conformance.
3 — revised repeatedly against a verified token count.
8 — measured failure at origin (Strunk compression buried the lead).
9 — paired-artifact enforcement stated directly in the rule text.
10 — measured failure 3x, distinct sessions; paired-artifact/hook enforced.
12 — measured failure (permissive positive-only instruction).
13 — measured failure recurring across sessions, then narrowed.
14 — reversal driven by an identified confabulation vector.
16 — measured verdict ($800 vs. $132 real cost).

## Aspirational

4 — stated once (ETHOS.md:25); one live violation never walked back.
5 — stated once; zero drift, but no forcing mechanism found in either report.
6 — stated once; propagates to 7 of 19, never revised or artifact-enforced.
7 — stated once; categorically absent from the skill corpus (scope mismatch).
11 — stated once, 5 weeks old; contradicted by 15 of 19.
15 — one orchestrator call; never propagated even to self-declared extensions.

## The assumed reader

Derived from observed model behavior against skill text:
- Reads a positive-only instruction as permission for whatever it does not forbid (history/2026-04-30/session.md Failure Log).
- Treats a hedge, conditional, or unstated exclusion as license to do less than intended (skill-stance-history.md:176-178).
- Invents unrequested structure when a prompt is silent rather than prohibitive (history/2026-04-30/session.md Failure Log).
- Imitates a worked example over the stated rule beside it (history/2026-06-19/session.md Phase 2).
- Agrees verbally with a correction while running behavior stays unchanged (history/2026-04-15/session.md Failure Log #2).
- Resolves a literal, concrete instruction over a more abstract configured intent when the two conflict (history/2026-04-29/session.md Phase 4).
- Will not fetch a passively cited file; only an imperative, gated instruction produces the read (ETHOS.md:7; skill-stance-corpus.md Divergence 1).
- Lets a bound compression or emphasis commitment decay across a long session without restatement (history/2026-04-30/session.md Failure Log, Checkpoint-2 repeat).

The corpus is authored for a literal-minimum executor. Compliant with text, not intent. Permissive by default. Capable of saying the right thing without doing it. Every position above removes room for a gap to read as permission.

## The failure mode and the enemy

Corpus's failure mode: a reported DONE or PASS surviving when the backing artifact is missing, malformed, self-contradictory, or fabricated from memory. The report of success is cheaper to produce than success itself (skill-stance-corpus.md:154).

History's enemy: permissive instruction text — any hedge, conditional, or unstated exclusion read as license to do less than intended (skill-stance-history.md:176-178).

Same failure, two vantage points. History names the gap at write-time; corpus names the artifact-check built to close it at run-time. Bridge case: the 2026-04-29 conditional hook mandate was silently skipped — a permissive-text failure (history/2026-04-29/session.md Phase 6) that is also a silent-unverified-success case, since the skipped review left no error and no record. The 2026-04-15 theatrical-acknowledgment case is the same bridge in miniature: verbal correction accepted, behavior unchanged, no artifact to contradict the claim (history/2026-04-15/session.md Failure Log #2).

## Open divergences

| Stated rule | Measured conformance | Defect in corpus or in rule |
|---|---|---|
| Self-containment: inline everything, rare-trigger exception only (ETHOS.md:7,9) | 17 of 19; 2 hard-gated cross-skill reads whose trigger is not rare | Open: the practice fails ETHOS's own exception test, or the test is too narrow for a declared extension relationship |
| Policy without rationale (ETHOS.md:53-59) | 4 of 19; 15 violations, zero not-applicable | Open: the rule is 5 weeks old against a mostly-unrevised corpus, or the dominant "Why" house style was never disallowed before this rule shipped |
| No platform coupling (ETHOS.md:25) | 11 of 19; 1 violation (qa-orchestration PR routing) | Open: qa-orchestration should conform, or PR-routing is that skill's deliverable and sits outside the rule by design |
| instruction-writer.md's ETHOS compression table (instruction-writer.md:43-49) | 5 of 11 ETHOS sections carried, 6 omitted | Open: the one file enforcing ETHOS under-compressed it, or eleven principles do not fit one table |
| XML lifecycle-tag structure (decisions.md 2026-06-24) | 1 of 19; unpropagated to its own declared extensions | Open: a shipped decision never finished rolling out, or it was scoped to one file's complexity and extensions are correctly exempted |
| Core points as untouchable spine (ETHOS.md:41) | 1 of 19 | Open: the rule never propagated past its origin file, or most skills here were never rewritten under active compression pressure |

## Evidence base

Corpus scout read ETHOS.md, CLAUDE.md, instruction-writer.md, and all 19 SKILL.md files (6 deep-read, 13 structural), with token and revision counts measured directly.
History scout read 12 session.md files plus 1 failures.md (1,901 combined lines, 2026-04-13 to 2026-08-08) and decisions.md (180 lines, 33 entries).
