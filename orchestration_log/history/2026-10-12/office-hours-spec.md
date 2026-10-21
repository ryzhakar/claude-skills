# office-hours: specification

Written by the orchestrator (session instruction-iteration-skill-adoption), 2026-10-20, from the owner's rulings in an office-hours round held that day. Owner quotes are verbatim. [peer] marks a quote relayed by a peer and unchecked at its source. [inference] marks what the orchestrator derived.

## Purpose
`agent-conduct:office-hours` governs one event: a round of questions held with the owner. Owner: "let's frame this as a round of questions, a particular event. not general guidance on all questions ever."

## Definitions
- Round: the span in which the owner answers questions put through the question tool.
- Queue: the agent's durable list of what waits for a round. Entry kinds: unsolved (no decision made) and solved (a reversible decision made, written down with its single closest alternative).
- Settled: a question the owner answered in a round, or one a standing word of the owner answers.
- Present: the owner's direct answer to a presence question states "i'm present".

## Functional requirements
- F1 Scope. The skill acts only in a round. A one-off question mid-task never invokes it.
- F2 Owner-opened round. No presence check. "most of the time i will trigger the questioning round."
- F3 Agent-opened round. The agent may ask to open one "whenever they think it would be reasonable. but the severe non-assumption-of-presence constraints must hold."
- F4 Presence. "it cannot assume i'm present under ANY circumstances. because i'm not. they must ask me explicitly and only count me present if I actually directly answer the question explicitly stating \"i'm present\". no other message counts as presence, ever." Also: "the agent must explicitly verify the owner is not away, with presence NEVER assumed."
- F5 Presence words. Only words the owner types into the free-text field of the presence question count. A clicked button never counts. (owner: "Typed words only")
- F6 No answer to a presence question. The agent keeps working, decides every reversible choice itself, queues what needs the owner, and does not ask presence again until a round opens. (owner: "Keep working, queue, stay quiet")
- F7 Between rounds. "queue, eagerly try to decide as much of the queue with reversible decisions written down with a single closest alternative considered; after writing the decision and the considered alternative down, solve according to decision."
- F8 Review at a round. "on office hours, the whole queue gets reviewed, unsolved first."
- F9 Flush. Everything in the queue goes out "in as many question tool calls as required to flush all." Platform fact: one call carries 1 to 4 questions, each with 2 to 4 options.
- F10 Queue home. The queue lives in the agent's durable records, the store that survives a restart and a context compaction. The skill names no plugin and requires none: "we as maintaners count on agents to use memento. but we cannot make it a dependency. so we sharpen the requirement towards memento without actually requiring using the plugin and without naming it even."
- F11 Re-raising. Re-raising a settled question is the gravest breach of a round. Before any question the agent searches its records for an answer. "severe penalty on re-raising anything otherwise settled." (owner: "Gravest breach plus a records search"). No mechanism beyond the search.
- F12 Tool only. Questions go through the question tool, never conversation text. [peer] "the questions: ask them via the dedicated tool. i don't answer in conversations, generally."; "use the tool, exclusively."
- F13 Context inside the call. [peer] "everything the owner must see during questioning goes inside the question tool call, portable, assuming no prior knowledge; conversation text stays minimal"; "i won't read your walls of text here, ever."
- F14 Portable. Each question carries what answering it needs; it names no branch, SHA, gate, draft or id as if the owner knew it. [peer] "this was not fucking portable and assumed me reading something beyond the question in the tool."; "this is not portable. i don't have a clue on what those are."
- F15 Explained terms. Every command, term and id is explained inside the question text where it appears. "you never explained what it does. not in the question, which should have been portable." [peer] "what's t1?"
- F16 No shorthand. "portability, context, tools, no shorthands".
- F17 Option consequences. Each option states what choosing it does. [peer] support is the weakest in this spec.
- F18 No errands. "you never tell me what to do, it's the opposite. i'm not your errand boy." Exception: an act only the owner can perform.
- F19 Never block. "you failed by escalating and blocking yourself with it." [peer] blocking on escalations "was an utter failure."
- F20 Batch size. One question per call, except a rapid-fire set the owner asks for: "Walk me through each" against "rapid-fire mode: any questions, portably, with no assumptions, via tool".
- F21 Rejected or unclear question. The agent stops, never reposts it, waits for the owner's word, and replaces it with the missing definitions added. "i don't get this bullshit question. come back with a better one."
- F22 Owner's clarifying question. The agent answers it directly, in the owner's terms.
- F23 Silence exclusion. Silent mode (work-silently) and a round are mutually exclusive: "on .work-silently marker the tool must be blocked." A hook denies the question tool while the marker `.claude/work-silently` exists.
- F24 Exception window. "office hours create an exception window. the agent remove the marker before office-hours and reapply it immediately after." The agent removes the marker as a round begins and recreates it the moment the round ends. A queue question in silence waits in the queue; the agent never asks presence in silence, because the tool is blocked there. [inference on the last clause]
- F25 Record. Each answer is written into the records the turn it is given, so F11 can check "settled". [inference]

## Non-functional requirements
- N1 Name and place: `agent-conduct:office-hours`, folder `office-hours`. Name ruling: "office-hours!!! great name!"
- N2 Size: at most 1489 tokens (git-etiquette's), measured with `just tokens FILE`.
- N3 Description: triggers only on an office-hours round (one the owner starts, or one the agent opens by asking about presence); never on a one-off question. "the naming must be sharpened, to not overapply the skill."
- N4 Authoring: an opus instruction-writer bound by `memento:skill-creation` writes the skill from this spec. "we set functional and non-functional specification on this, then opus instruction-writer bound by skill-creation skill writes the skill."
- N5 ETHOS: strong directives (one emphatic marker each), platform facts not policy rules, no rationale narration, positive form, self-contained. No Russian-authored source.
- N6 Examples: bad/good pairs in agentic-delegation's `<never_do_this reason>` / `<do_exactly_this>` schema, only from quoted failures: unexplained `claudes run`; an internal id in an option; a rejected question reposted; an errand; blocking on the owner.
- N7 Orthogonal: the skill carries no silence, wake or commit rules and conflicts with none of work-silently, check-back, git-etiquette. The one coupling is F23 and F24, written in office-hours and enforced by the hook.
- N8 Hook (F23): stdlib-only Python (owner: "stdlib only for hooks specifically"), a PreToolUse hook on the question tool, gated on the marker's existence (invisible when the marker is absent), denial text in `hooks/templates/*.txt`, registered in agent-conduct's `hooks/hooks.json`, with tests beside `tests/test_check_back.py`.
- N9 Verification: blind compliance reads gate it; one usability read is advisory, once.
- N10 Release: agent-conduct 1.9.0 to 1.10.0, version in `plugin.json` only; merge to main only on the owner's word, under git-etiquette.

## Not in the spec (no quote supports it)
Most-influential-first ordering; a batch size when no mode word is given; recommended-option-first (the tool's own convention).

## Open
- How the owner opens a round in words (trigger phrases for the description): "office hours", "questioning round" are candidates. [inference]
- The exact denial text the hook returns.
- Whether work-silently's own text must mention the exception window (F24) or only office-hours does. [inference: only office-hours does]

## Reading list for the writer
`memento:skill-creation`; this file; /Users/ryzhakar/pp/claude-skills.worktrees/instruction-eval/orchestration_log/recon/2026-10-14/reports/question-preferences.md; the [peers] answer lines dated 2026-10-20 in events.md; agent-conduct work-silently, check-back, git-etiquette and `hooks/` on origin/main; agentic-delegation's example schema; the first draft on branch worktree-agent-aa2d9143386d09a65 (reference only).

## Amendments (2026-10-20, second round; these override the requirements above where they differ)
Owner rulings, verbatim:
- Round end: "Whichever comes first" (every queue entry answered, or the owner says the round ends; unanswered entries stay queued).
- Presence: "you don't fucking ask if i'm present by using the tool, that's EXACTLY what we're trying to avoid."
- Between rounds: "i think this other thing nests into work-silently easily, or at least into a separate skill. what we're trying to achieve is autonomy with steering effective towards the work and efficient towards the owners attention."

Changes:
- A1 (replaces F4, F5, F6 wording). The presence question is asked in conversation text, never through the question tool. Presence counts only when the owner types a message stating "i'm present"; no other message counts, ever. No answer: the agent keeps working and does not ask again until a round opens. In silent mode the agent asks nothing (the tool is blocked and text is forbidden), so only the owner opens a round there.
- A2 (narrows F12). The question tool carries every question of a round except the presence question.
- A3 (adds F26). A round ends when every queue entry has an answer or when the owner says it ends, whichever comes first; unanswered entries stay queued; the agent restores the marker (F24) at that moment.
- A4 (moves F7 and F10). The between-rounds rules (queue what needs the owner, decide reversible choices eagerly, write each decision with its single closest alternative, then act on the decision; keep the queue in durable records, no plugin named) live in work-silently, where the agent works while the owner is away. office-hours keeps only the round: F1-F5, F8-F9, F11-F26 as amended. Aim of the pair, owner's words: "autonomy with steering effective towards the work and efficient towards the owners attention."
- A5 (settled by the orchestrator from the compliance read, [inference] where marked). A solved queue entry is put to the owner as: the decision, its one alternative, options "keep the decision" and "take the alternative" [inference]. After a rejected question and its replacement the flush continues with the remaining entries [inference]. A confirmed "i'm present" begins the review and flush [inference]. "Never wait for the owner" holds outside a round; inside a round the agent waits for the answers it asked for [inference]. The skill states the F9 platform fact (a call carries 1 to 4 questions, each with 2 to 4 options) and the F23 fact (the tool is denied while the silence marker exists; the agent removes the marker with `rm` and recreates it with the `touch` command work-silently already gives). The skill drops what no requirement backs: the trigger "rapid-fire", "never in the conversation alone", the gloss "an owner rule still in force", the empty-turn good example. Triggers in the description: "office hours", "questioning round".
- A6 (revises N7). The one coupling between the two skills is the queue: work-silently fills it, office-hours empties it; the marker exception window (F24) stays in office-hours and is enforced by the hook (N8).

- A7 (2026-10-20T20:13+0300, owner ruling: "carve-out in work-silently, not for this plugin specifically, but for temporary marker removal."). work-silently carries one generic carve-out: the marker may be removed temporarily and is restored the moment the temporary reason ends; it names no other skill. office-hours keeps the exception window (F24) and relies on that carve-out. A6's "exception window stays in office-hours only" is replaced: the permission sits in work-silently, the use in office-hours. Resolves compliance read 3, finding (d).

- A8 (2026-10-20T20:24+0300, owner rulings in a question round). (1) Dismissal: a question the owner dismisses without answering returns to the queue unanswered; the round continues with the remaining entries and ends only as A3 says. (2) Answers the owner gives through the question tool count as the owner's words inside a round; no carve-out is written, "i think there's no actual confusion there." (3) Split: the queue rules (F7, F10, A4) leave work-silently and live in their own skill, specified in queue-skill-spec.md; work-silently and office-hours each reference it and restate none of its rules. work-silently returns to its pre-queue form plus its generic marker carve-out (A7).

- A9 (2026-10-20T20:31+0300, orchestrator, settling the fourth compliance read; [inference] unless a quote is given). (1) N2's 1489-token limit was the orchestrator's own number, not the owner's; office-hours may reach 1500 tokens. (2) N6's blocking-on-the-owner example moved to decide-while-away with the rules it shows (A4, A8); office-hours keeps the other four. (3) F20: a rapid-fire set is one the owner asks for; the skill states no naming rule. (4) While the silence marker is absent (temporary removal, A7), silence is not held, so work-silently's silence rules do not apply in that span. (5) Asking whether the owner is present does not open a round; the round opens only when the owner types "i'm present" (A1). (6) decide-while-away's "never wait for the owner" holds while the owner is away; work that depends on an unsolved entry waits. (7) decide-while-away settles as much of the queue as it can with reversible decisions (Q4); it carries no absolute "never leave a reversible choice unsolved".
