## Binding
Loaded whole: first-principles.md, Strunk SPR v3 (curl), manifesto-oath SKILL.md, self-documenting-code.md (read in full; the oath file read to line 30 only, the rest is the protocol text the hook injected).
Convergence: a name carries the act and the answer to "why does this exist" (atoms; names that reveal intent); both reject a name borrowed from habit. Tension: Strunk's brevity against "reveal intent": a bare verb is short but may hide the addressee. Rule: the addressee stays in the name, nothing else does.
I must derive the name from the act, not from the working title, and I will test the working title against four lenses before keeping or dropping it. I must not echo `ask-owner` for being offered, and I will not keep it unless a lens line supports it.

## Name
`ask-owner`. The working title survives; it was tested, not inherited. Verdict: it wins on the lenses, not on the order it was offered.
The act the agent does: put a question to the owner. One verb, one addressee.

## Namespace
`agent-conduct:ask-owner`. Folder name is the skill name; the plugin supplies the namespace. Siblings (check-back, git-etiquette, work-silently) are verb-phrases in hyphens, so the form fits.
Pair with `peers:ask-around`: same verb, different addressee, the contrast is the point. Typing `ask` lists both and each says whom it asks. "Owner" is the owner's own word for the role and ranks no one in the name; the culture file calls the owner a deity outside the society, never a member.

## Lens lines
- self-documenting-code: `self-documenting-code.md:50` "Names are your most powerful tool. They should reveal intent, not implementation."
- Anarchy philosophy: `roots.md:32` "seeking my attention directly will only block you and bring your failure." (the owner is away by default; the skill governs the rare ask, and the name carries its addressee)
- Peer-to-peer: `ask-around/SKILL.md:23` "Carry in every ask the need behind the question; never send a bare question." (the society's own ask-verb; `ask-owner` joins that family)
- Namespace mechanics: `agent-conduct/.claude-plugin/plugin.json:2` `"name": "agent-conduct",` (the plugin is the namespace, so the folder needs no `agent-conduct-` or `conduct-` prefix)
(Anarchy lens source is Black via roots.md; no Russian-authored source cited.)

## Clash check
`ls pp/claude-skills/*/skills/ .claudes/meta/plugins/cache/*/*/*/skills/ pp/claude-skills.worktrees/instruction-eval/*/skills/ | grep -E -i "^(ask|pose|put|owner|raise|consult|query)" | sort | uniq -c`
Result: `1 ask-around`, `5 owner-ruling`. No `ask-owner`, `pose`, `put-*`, `raise`, `consult`, `query`.
- `peers:ask-around`: different addressee; the pair reads as a pair.
- `memento:owner-ruling` carries a ruling the owner already made; `ask-owner` puts a question. Different act, different namespace.
- `AskUserQuestion`: the tool is the means; the skill name says "owner" and not "user" or "question", so the name never names the tool (implementation).

## Struck
Twelve drafted: ask-owner, pose, put-to-owner, ask-plainly, ask-by-tool, escalate, petition, appeal, consult-owner, raise, ask-once-well, bring-it-to-owner.
- `escalate`, `petition`, `appeal`: a rank, someone above to climb to.
- `ask-by-tool`: implementation, and it blurs with the tool name.
- `consult-owner`: the owner is a deity, not an advisory body; "consult" implies a council.
- `raise`: no addressee; collides in feel with raising issues anywhere.
- `ask-once-well`: names the manner, not the act; also starts with `ask-` and blurs with `ask-around`.
- `bring-it-to-owner`: long, and "bring" hides that it is a question.

## Runners-up
1. `pose`: bare verb in the `peers:<verb>` style the owner likes (`agent-conduct:pose`); loses on intent, since "pose" alone hides the addressee and reads as "pose as".
2. `put-to-owner`: names the act and the addressee, and ducks `ask-around`'s prefix; loses on idiom, since "put to" fits less naturally in a slash command.

Summary: `ask-owner` is the pick; the working title passed four lenses and a clash check rather than being kept by default. Its only near neighbours are `peers:ask-around` (a contrast the namespaces keep clean) and `memento:owner-ruling` (a different act). Runners-up are `pose` and `put-to-owner`.

## Second round (2026-10-20)
The owner struck `ask-owner`: "the naming must be sharpened, to not overapply the skill." The skill governs one event, not asking. Name the event.

### Name
`question-round`. A round of questions held with the owner: opened by the owner (or by the agent's presence question), closed when the piled questions are flushed. A one-off question mid-task is no round, so it never matches. The noun names the event; the owner's own phrase was "a round of questions, a particular event."

### Namespace
`agent-conduct:question-round`. Folder name is the skill name. Sibling shape holds (`check-back`, `git-etiquette`): hyphen phrase, noun-led exception to `peers:<verb>`, which the owner allows "when needed". The owner's "round" word carries over from the society, where a round is a bounded event with an open and a close.

### Lens lines
- self-documenting-code: `self-documenting-code.md:50` "Names are your most powerful tool. They should reveal intent, not implementation."
- Anarchy philosophy: `roots.md:32` "seeking my attention directly will only block you and bring your failure." (a round happens only when the owner is present; the name says event, not entitlement to ask)
- Peer-to-peer: `gather/SKILL.md:5` "\"open a protocol round\", \"close the round\"" (the society's own bounded event, opened and closed; `question-round` borrows the noun)
- Namespace mechanics: `agent-conduct/.claude-plugin/plugin.json:2` `"name": "agent-conduct",` (the plugin carries "conduct"; the folder carries the event only)

### Clash check
`ls pp/claude-skills/*/skills/ .claudes/meta/plugins/cache/*/*/*/skills/ pp/claude-skills.worktrees/instruction-eval/*/skills/ pp/claude-skills/*/agents pp/claude-skills.worktrees/instruction-eval/*/agents | grep -E -i "round|question|office|rapid|session|interview|present" | sort | uniq -c`
Result: `ask-around`, `spread-around` (substring "around" only), `session-checkpoint`, `session-close`. No skill or agent named `question-round`, `round*`, `office-hours`, `rapid-fire`. The session listing names (spec-chef, spec-capturer) carry no clash; `dev-cycle:spec-capturer` interviews through the tool but names an agent, not an event.
Note: `peers:protocol-change` and `peers:gather` use "round" inside their text for protocol rounds; their names do not, and the plugin namespace separates them.

### Struck
`ask-owner`, `pose`, `put-to-owner` (ordered). Also `ask` and every bare `ask` form, `question-time` (parliamentary, legislative), `audience` (rank: an audience is granted from above), `roundtable` (implies many equals), `round-up` (cattle, and blurs with gathering), `check-in` (blurs with `check-back`), `presence-check` (names the opening step, not the event), `owner-present` (a state, not an event), `hold-a-round` (verb phrase hides what is asked).

### Runners-up
1. `round-of-questions`: the owner's own words, plainest reading; loses to `question-round` on length and on the sibling-name shape.
2. `office-hours`: the owner is away by default and present in windows; wink included. Loses on intent: "hours" implies the owner keeps a schedule, and the skill's trigger is the owner's word, not a clock.

Summary: `question-round` names the event the skill governs, so a one-off mid-task question never matches it. It passed the four lenses and a clash check over the full skill and agent list, with no folder or agent of that name. Runners-up are `round-of-questions` and `office-hours`.

## Queue skill (2026-10-20)
Act from queue-skill-spec.md: an owner's decision falls due while the owner is away; the agent settles it reversibly, writes it beside its one closest alternative, and acts. Irreversible choices stay unsolved.

### Name
`decide-while-away`. It names the act (decide) and the condition (the owner is away). Noting a to-do decides nothing, so it never matches; neither does deciding the agent's own matter. Beside the siblings it reads as the pair of presence states: `office-hours` when the owner is here, `decide-while-away` when not. `work-silently` and `check-back` stay verb-led, so the shape fits.

### Namespace
`agent-conduct:decide-while-away`. Folder name is the skill name; the plugin carries "conduct". "Queue" stays out of the name: the queue is the means, "away" is the intent, and a name reveals intent.

### Lens lines
- self-documenting-code: `self-documenting-code.md:50` "Names are your most powerful tool. They should reveal intent, not implementation."
- Anarchy philosophy: `roots.md:32` "and i am? i am away. always by default." (the owner's own cosmology; away is the standing state, so the skill is the default case, not an exception)
- Peer-to-peer: `peers/skills/post/SKILL.md:15` "Hold a level 2 message for a session presence shows `busy`, or for a dormant or dnd member, until that state clears" (the society already names conduct by the receiver's state; this skill does the same for an absent owner)
- Namespace mechanics: `agent-conduct/.claude-plugin/plugin.json:2` `"name": "agent-conduct",` (no `conduct-` prefix in the folder)

### Clash check
`ls pp/claude-skills/*/skills/ .claudes/meta/plugins/cache/*/*/*/skills/ pp/claude-skills.worktrees/instruction-eval/*/skills/ pp/claude-skills/*/agents pp/claude-skills.worktrees/instruction-eval/*/agents pp/agents-of-anarchy-marketplace/*/skills | grep -E -i "decid|away|queue|provision|stand|hold|park|defer|absen|default" | sort | uniq -c`
Result: no match. No skill or agent shares the name or any of its words.

### Struck
`queue` (the owner's loose label; names the means, and any to-do list matches it), every bare `ask` form, `stand-in` (a deputy, so a rank), `proxy` (same), `defer` (names what the skill refuses to do for reversible choices), `park` (covers only the unsolved half), `hold-the-call` (ambiguous, a phone call), `decide-and-note` (names two steps, matches any note), `autopilot` (implementation, and a wink at the owner's expense), `owner-decisions` (a noun, not an act, and presumes the owner), `pending-decisions` (a list, matches a to-do).

### Runners-up
1. `decide-for-now`: names the reversible, provisional core; loses on intent, since it omits why (the owner is away) and so could match any agent's own interim choice.
2. `provisional-decision`: names the entry, not the act; loses on the act-for-the-name rule and matches any tentative choice.

Summary: `decide-while-away` names the act and the owner's absence, so a plain to-do note never matches. It reads as the pair to `office-hours` beside `work-silently` and `check-back`, and the clash check over skills and agents found nothing. Runners-up are `decide-for-now` and `provisional-decision`.
