# queue skill: specification

Written by the orchestrator, 2026-10-20T20:24+0300, from the owner's rulings in a question round on 2026-10-20. Owner quotes verbatim. [inference] marks what the orchestrator derived. The name comes from the naming agent only.

## Purpose
One skill holds the between-rounds discipline: what an agent does with a decision that is the owner's to make while the owner is away. Aim, owner's words: \"autonomy with steering effective towards the work and efficient towards the owners attention.\"

## Owner rulings
- Split: \"we need to care for the 'queue' skill in the same way we would with new \"target\" skills. the same care to naming, structure, etc. additionally, it must be referenced by both.\" (both = work-silently and office-hours)
- Behavior: \"queue, eagerly try to decide as much of the queue with reversible decisions written down with a single closest alternative considered; after writing the decision and the considered alternative down, solve according to decision. on office hours, the whole queue gets reviewed, unsolved first.\"
- Home: \"we as maintaners count on agents to use memento. but we cannot make it a dependency. so we sharpen the requirement towards memento without actually requiring using the plugin and without naming it even.\"

## Functional requirements
- Q1 Standalone and loadable on its own; a session or an agent definition can load it; no sentence presumes work-silently or office-hours is loaded.
- Q2 The queue is a list in the agent's durable records, the store that survives a restart and a context compaction. The skill names no plugin and requires none.
- Q3 Two entry kinds. Unsolved: a question the agent could not settle with a reversible decision. Solved: a reversible decision the agent made, written with its single closest alternative.
- Q4 The agent queues every decision that is the owner's to make, tries eagerly to settle as much of the queue as it can with reversible decisions, writes each decision and its one closest alternative down first, then acts on the decision.
- Q5 A choice that cannot be undone is never decided by the agent: it stays an unsolved entry, and only the work that depends on it waits; all other work continues. [moved from work-silently's existing rule, restricted to irreversible choices]
- Q6 The agent writes each queue entry into the records the turn it arises. [inference]
- Q7 Review order at a round: the whole queue, unsolved first. The round itself belongs to office-hours; the skill states the order only.
- Q8 When the owner picks the alternative of a solved entry, the agent switches the work to the alternative. [inference]
- Q9 Bad/good example pairs only from quoted failures, in the `<never_do_this reason>` / `<do_exactly_this>` form: the pacing question escalated and blocked on (owner: \"you failed by escalating and blocking yourself with it.\"), moved from work-silently.
- Q10 work-silently and office-hours each reference this skill where they rely on the queue and restate none of its rules.

## Non-functional requirements
- X1 Name and structure: the same care as a target skill; the name from the naming agent, folder name = skill name, in agent-conduct.
- X2 Authoring: an opus instruction-writer bound by memento:skill-creation (main, with the example-block rule: /Users/ryzhakar/pp/memento/plugin/skills/skill-creation/SKILL.md) and Strunk SPR v3 in full.
- X3 Size: at most 1300 tokens, near the marketplace median of 1270 [inference; confirm]. work-silently returns to its pre-queue size plus one reference and its carve-out.
- X4 Marketplace ETHOS: directives, one emphatic marker each, platform facts not policy rules, no rationale narration, positive form, self-contained.
- X5 Description: triggers on needing a decision the owner has not given, never on any other moment.
- X6 Verification: blind compliance read gates it; usability read advisory once.
- X7 Release: ships in agent-conduct 1.10.0 with office-hours. Owner: \"if you're done with it, you can release.\"
