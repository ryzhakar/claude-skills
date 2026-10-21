# write-well: specification

Written by the orchestrator (session instruction-iteration-skill-adoption), 2026-10-20, from the scout's port spec (write-well-port-spec.md) and the owner's rulings in a question round that day. Owner quotes verbatim. [inference] marks what the orchestrator derived.

## Purpose
`agent-conduct:write-well` (`/write-well`) carries Strunk's rules for writing, rewritten from both Strunk texts, as one self-consistent skill. It cares about nothing outside Strunk. Owner: "the skill gets self-consistent and has no business caring about anything else."

## Owner rulings
- Scope: "loading the skill into context cannot be reverted, so there's no meaningful way of scoping it. however, it opens a way to make agents depend on the skill or whatever."
- Clash with repo rules (clarity vs compression, fragments, articles, tables, instruction files, pronouns): "you don't need to concern yourself with this. it's a runtime concern." and "same, the skill gets self-consistent and has no business caring about anything else."
- Examples: "bock format is great, simply great. if current version of skill-writing skill forbids it, we may need to revise this to encourage."
- v3 against v4 wording: "skill-writer won't paste things verbatim, i assume, so this becomes irrelevant. it's a full rewrite task."
- Escape hatches: "don't hand an escape hatch to an agent. they will find their own anyway. let the skill deal in absolutes."
- MUST: hard commands (the long text's softening sentence is dropped).
- Size: "3k tokens".

## Functional requirements
- W1 Standing text. The skill states rules for every piece of prose the agent writes once the skill is in context. It names no mode, turn limit or call scope.
- W2 Dependable. The skill works when an agent definition preloads it (a `skills:` entry) and when a session invokes it; no sentence presumes either path. [inference from the owner's "make agents depend on the skill"]
- W3 Absolutes. Every rule is an absolute command: no exception clause, no override latitude, no named reasons to break a rule, no "if easy" tier. Rules conflict only where Strunk's own text orders the conflict; the skill states that ordering.
- W4 Severity order. Rules are presented most serious first; severity orders the text and never softens a rule. [inference]
- W5 Self-consistency. No rule contradicts another rule in the skill. A rule from either Strunk text that contradicts a kept rule is dropped. The skill mentions no repo, project, harness, other skill or register.
- W6 Full rewrite. The skill copies no Strunk sentence; each rule is rewritten as a command in the marketplace's skill form. The writer takes both texts into account at once: every rule of the long text (v3, strunk_spr_v3_complete.xml) and of the short text (v4, strunk_spr_v4_compressed.xml) is accounted for: kept, merged or dropped, in the writer's report.
- W7 Gender-specific usage. The skill omits any rule on the pronoun for an unspecified person. [inference: carrying either side would clash with something outside Strunk, which the skill ignores; confirm]
- W8 Examples. Bad/good pairs in the `<never_do_this reason>` / `<do_exactly_this>` block form, where an example sharpens a rule.

## Non-functional requirements
- X1 Name and place: `agent-conduct:write-well`, folder `write-well`.
- X2 Size: at most 3000 tokens, measured with `just tokens FILE`.
- X3 Authoring: an opus instruction-writer bound by `memento:skill-creation` and by Strunk SPR v3 in full writes it. The `<never_do_this reason>` attribute and the example blocks break skill-creation's current form; the owner wants skill-creation revised to encourage the block form, so the writer follows the owner and flags the clash. [peer notice to the memento steward sent]
- X4 Marketplace rules: ETHOS (strong directives, one emphatic marker each, platform facts not policy rules, no rationale narration, positive form, self-contained, no reference files).
- X5 Description: states what the skill makes an agent do and when to load it, without overapplying; trigger phrases "write-well", "write well" [inference].
- X6 Verification: a blind compliance read (every rule traces to a rule of v3 or v4; no rule from outside Strunk; no contradiction between kept rules) gates it; one usability read is advisory, once.
- X7 Release: bump agent-conduct to the next minor in `plugin.json` only; merge to main only on the owner's word, under git-etiquette.

## Open
- W7 (pronoun rule omitted) and X5 trigger phrases are inferences to confirm.
- Whether the plugin should ship agent definitions that preload the skill (W2); not asked, not in scope.

## Amendment (2026-10-20T20:07+0300)
- B1 (resolves the flag in X3). memento:skill-creation now permits the example blocks: no attribute inside a tag except the `reason` of a never_do_this block; a rule easier shown than told takes a pair of blocks, the wrong text then the right one (memento main commit 288b401, /Users/ryzhakar/pp/memento/plugin/skills/skill-creation/SKILL.md lines 42-46; tag v0.8.0 lacks it, so the writer reads it from that path; peer claim from memento-manager, checkable at that file).

- B2 (2026-10-21T00:23+0300, owner ruling, replaces W7): the skill carries Strunk's rule on the pronoun for a person whose sex is unspecified, with singular "they" in place of "he": "do the same with \"they\" :)". The rule is an absolute command with its paired prohibition, like every other rule.
