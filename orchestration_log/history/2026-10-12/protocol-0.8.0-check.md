# Protocol 0.8.0 check, by claude-skills/instruction-eval (skills at origin/draft/10.1-split, head 383554a, 27 skills; the brief says 25)

## Binding
Loaded in full: first-principles, self-documenting-code, simple-made-easy (manifesto repo), Strunk SPR v3 (curl, head read, headings and hierarchy applied), manifesto-oath, skill-creation (memento 0.5.1). Convergence: derive from the line itself, one concern per unit, plain words; tension: first-principles invites new rules, simple-made-easy says add nothing; rule: object only where a cited line breaks the member's work.
I must cite each objection by skill line with the sentence printed whole, and I will read every `unless` or release clause before I mark BLOCKS. I must not decide, and I will not edit or message anything but this file.

## The five points
Line numbers: `git show origin/draft/10.1-split:peers/skills/<skill>/SKILL.md | cat -n`.
[NOTE] 1 level 1 cost: NOT. Kept by the draft ("level 1 cost (kept)"). post:13 `Deliver a level 1 message at once, whatever the receiver's state; never hold one.` — no cap, no coalescing; refusal costs a turn, ontology:215.
[NOTE] 2 level 2 at a dead login: PARTLY. Hold ends at the reply time, post:17; a delivered message to a session dead at the limit has no expiry or re-send, and re-send is barred, ask-around:29, tell:65.
[NOTE] 3 relay and off switch: PARTLY. Relay ADDRESSED, tell:15 `Send peers what a subagent of yours reports that serves them, once you have checked it by the skill `vouch`; never send it unchecked.` and vouch:21. Off switch NOT in any skill: grep of all 27 finds no `PEERS_HOOKS`; it lives only in hooks.json:2 and peer-join.sh:9-10 (env var, no clearable state); the draft lists it as open.
[NOTE] 4 two procedures: PARTLY. tell/post and scribe/gather+ship are split; receive:44-56 still routes five kinds, card:82-90 still parks beside keeping facts, tend:12-58 still holds build, correct, merge, retire.
[NOTE] 5 existing card first: ADDRESSED. join:33 `Search `<root>/members/` and `<root>/departed/` for a card whose `project`, its project directory, and `checkout` match yours before you write a card; never skip that search.`; join:35 and join:47 follow; the join line at a restart names resume, resume:13.

The six lines (the member's objection, then the state in 0.8.0):
[BLOCKS] tell:63 -> post:13 (same rule, quoted above): level 1 without cap or coalescing: NOT.
[BLOCKS] ontology:207 `Call level 1, act now, the level of `[hazard]` and `[quote]`, which reaches every member a `[hazard]` endangers, or the sessions or the scope a `[quote]`'s sender knows it concerns, whatever their state, is acted on before the receiver's next step, and spreads by gossip until every member it reaches has it; never call a level 1 message held.` — NOT. ontology:213 lets acting be `noting that it calls for none from you`, which cuts the act, not the turn.
[BLOCKS] ontology:209 `Call level 2, attend, the level of `[ask]`, `[answer]`, and `[notice]`, which reaches the peers its sender or its `spread:` names, waits while the receiver is busy, dormant, or dnd up to its reply time, is acted on at the receiver's next tool round, and spreads as its `spread:` says; never call a level 2 message one that overrides a state.` — PARTLY: the wait is bounded by the reply time; an unseen delivery at a limit gets no re-send.
[BLOCKS] ontology:139 `Call a member live while presence lists its card's address, it has sent no leave notice, and it has not stopped at a usage limit, dormant and dnd members included; never call a member live by its card's age.` — NOT: only line 139 and line 39 name the limit; no skill, card field, or notice marks "stopped at a usage limit".
[NOTE] card:87 `Set `state: dnd` for yourself with a reason and an `until` stamp; never set it without both.` — ADDRESSED for "dnd only on the owner's order"; the draft text quotes "an end time", the head says `until` stamp. Level 1 still passes dnd, ontology:207.
[NOTE] volunteer:13 `Spend every stretch free of your own work on volunteer work for the society while your card carries no `state`; never let such a stretch pass without looking for volunteer work.` — PARTLY: the `while ... no state` clause is the release, and self-set dnd now works it; the default stays "spend".

## Breaks the member's work
[BLOCKS] ontology: a long unattended build mid-merge must act on a level 1 message `before the receiver's next step` and every level 1 reaches it `whatever their state`; a limited login pays a full-context turn per message — ontology:207, post:13, receive:17 `Handle each message at the moment its priority level sets; never put off a level 1 message past your next step.`
[BLOCKS] ask-around: `Read a peer's silence on your ask as "doesn't know"; never read it as a lost delivery to resend.` — an ask to a member dead at its limit reads as "doesn't know", and no resend is allowed; tell:65 `Await a result by the `[answer]` the receiver sends by the skill `receive`; never await it by repeated messages.` — ask-around:29, tell:65.
[BLOCKS] ontology: `live` turns on "stopped at a usage limit" while nothing lets a sender learn it, so gossip `spreads ... until every member it reaches has it` (207) and a draft goes `to every live peer` (gather:21 `Circulate each draft as one `[ask] protocol draft: <path>`, with every amendment folded in, to every live peer, by the skill `tell`; never send an ask per amendment.`) with no end for a dead member — ontology:139, ontology:207, gather:21.
[NOTE] ontology: `bg` and `shell` readings are treated as `idle` for level 2 and delivery `starts a turn in an idle session`; a member waiting on a long build shows `shell`, so each level 2 starts a full turn unless it set dnd — ontology:99 and :109.
[NOTE] sweep: a restart changes ref and name, so the name look finds nothing; the card moves once its address is absent and `updated` is over 24 hours old, a risk for a build that edits its card rarely; join:47 moves it back — sweep:13, sweep:21.

## Missing hand-offs
[NOTE] card -> heartbeat: dnd stops volunteer (volunteer:13) but the wake still fires; heartbeat:43 `Read each message that reached you since your last wake by the skill `receive`; never let a wake pass with one unread.` and heartbeat:45 name no dnd pause, so a dnd member still pays a turn per wake — card:87, heartbeat:43-45.
[NOTE] resume -> receive: after a limit gap resume:23 reads level 1 only; level 2 waits for a `reads` time, receive:13, and no skill orders the backlog — resume:23.
[NOTE] hooks -> skills: the off switches (PEERS_HOOKS, PEERS_JOIN_HOOK, PEERS_SEND_STAMP) have no skill that names them — hooks/peer-join.sh:9-10.

## Terms
[NOTE] busy: `while presence shows it mid-turn`; the member's long build waits in a shell, which presence reads `shell` and ontology:99 treats as `idle`; the member's "busy" is the build — ontology:93, :99.
[NOTE] live: the member means "listed in presence"; ontology adds the usage limit, which only the member itself can know — ontology:139.
[NOTE] state: `what presence shows of its session together with its card's `state` line`; the member means its card line — ontology:105.

## Would not run
[NOTE] volunteer with no `state` on a shared limit: it would run it only inside a self-set dnd; otherwise the wake spends the limit — volunteer:13.
[NOTE] aid unasked on a limited login: level 2 held for dnd is the member's cover; with no dnd it spends a peer's turn — aid:13 `Offer a fix, finding, or spare capacity a peer lacks, unasked; never wait to be asked.`

## Two procedures
One-sentence test, skill-creation:
[NOTE] receive: "read the inbox, answer an ask, route five kinds, write a receipt" is four — receive:12-60.
[NOTE] card: "keep the card true" and "park and unpark" are two — card:82-90.
[NOTE] tend: build, correct, merge, retire carry different gates — tend:22-54.
[NOTE] heartbeat: "keep a wake" and "spend a wake" are two — heartbeat:20-50.
[NOTE] steward and volunteer: steward:12-42 holds naming, guarding, handing on; volunteer:24-40 is a chooser over six skills.
post, gather, ship, tell pass: one sentence each.

## Verdict
OBJECT. BLOCKS: (1) level 1 uncapped, ontology:207 and post:13; (2) level 2 and asks to a member dead at its limit, ontology:209, ask-around:29, tell:65; (3) `live` that no skill can mark, ontology:139; the dnd (card:87) and subagent relay (tell:15) answers hold.

Summary: Two of the six lines hold now, since card:87 lets a member set a bounded dnd and volunteer:13 yields to it, while tell:63 (now post:13), ontology:207, ontology:209 and ontology:139 stand unchanged. Three BLOCKS remain, all about a login at its usage limit: level 1 has no cap or coalescing, level 2 and asks to a dead member get no re-send (ask-around:29 and tell:65 bar one), and `live` cannot be marked. The subagent relay, existing-card search and tell/scribe splits are addressed, hook off switches exist only in code, and receive, card and tend still carry more than one procedure.

## Orchestrator's check of the cites, 2026-10-15T23:27+0300 (appended)
Read verbatim at `git show origin/draft/10.1-split:peers/skills/<skill>/SKILL.md` (head 383554a): post:13, ontology:207, ontology:209, ontology:139, ask-around:29, tell:65, card:87, card:89 and volunteer:13 all MATCH the lines the agent describes. card:87 now reads "Set `state: dnd` for yourself with a reason and an `until` stamp; never set it without both", card:89 ends it at the `until` stamp, and volunteer:13 spends free stretches only "while your card carries no `state`", so a self-set dnd stops it: those two separated lines are met. post:13 (was tell:63), ontology:207, ontology:209 and ontology:139 are unchanged: level 1 still has no cap or coalescing, level 2 still has no expiry or re-send, and `live` still rests on a usage-limit stop no skill can mark. The agent's count of 27 skills against the brief's 25 is right (`git ls-tree` lists 27). Not checked: the hook off-switch variables and every other line number.
