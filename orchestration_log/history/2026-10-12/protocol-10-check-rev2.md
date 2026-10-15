# Protocol 10 check, revision 2 (draft/10-skills at ee8fd61), by claude-skills/instruction-eval

## Binding
Loaded in full: first-principles, self-documenting-code, simple-made-easy (manifesto repo), Strunk SPR v3 (curl), manifesto-oath, skill-creation. Convergence: test each line against the member's real work, one procedure per unit, one term per concept, plain words; tension: first-principles invites inventing skills, simple-made-easy says do not add, so I name a missing skill only where the member's work stalls without it.
I must cite the skill line verbatim for every BLOCKS and read the whole sentence, `unless` clauses included, and I will not call a clipped sentence a break.
I must decide nothing, and I will edit nothing but this file; line numbers are those of `git show draft/10-skills:peers/skills/<skill>/SKILL.md`.

## The five points
1. Level 1 cost: PARTLY. Reach now narrowed to members a hazard endangers or a quote concerns, and "acting" may be "noting that it calls for none" (ontology 207, 213); no cap, no coalescing, refusal still costs the turn (tell 63). Draft open item 1.
2. Level 2 for an agent dead at the limit: NOT. "live" now excludes limit-stopped members (ontology 139) but no skill reads that state, and no expiry or re-send rule exists (ontology 209, tell 65-67); two lines forbid re-sending (ask-around 29, tell 83). Open item 6.
3. Missing skills: PARTLY. Subagent relay lives in tell 15 (send after vouch) and quote 41 (forward rulings down). Hook off switch exists in code (`PEERS_HOOKS=off`, `PEERS_SEND_STAMP`, `PEERS_JOIN_HOOK`; hooks.json description) and no skill names it; hooks hold no state to clear.
4. One procedure per skill: PARTLY. Tend and receive lost lines (tend 57 delegates carry to spread-around; receive record lines now one), scribe is its own skill; receive, card, tell still hold two (see Two procedures).
5. SessionStart to join checks for an existing card: ADDRESSED. join 33 searches members/ and departed/ by `project` and `checkout`; join 35 refuses an address presence lists live unless it is yours; join 47 pulls a departed card back; join 73 owes the name notice on rejoin.

## Breaks the member's work
[BLOCKS] tell: a limit-stopped login pays a full turn per level 1 message to every session on it, with no cap, no coalescing, no skip for a message that needs nothing from the member — tell 63: `Deliver a level 1 message at once, whatever the receiver's state; never hold one.` Also ontology 207: `...whatever their state, is acted on before the receiver's next step...`. Owner-decided override; cost is open item 1.
[BLOCKS] ontology: a level 2 message to an agent dead at the limit has no expiry and no re-send, and "live" turns on a state nobody can read — ontology 209: `...waits while the receiver is busy, dormant, or dnd up to its reply time, is acted on at the receiver's next tool round...` and ontology 139: `...and it has not stopped at a usage limit, dormant and dnd members included...`. Open item 6.
[NOTE] ask-around: the sender of an ask to a dead agent may not re-send — ask-around 29: `Read a peer's silence on your ask as "doesn't know"; never read it as a lost delivery to resend.`; tell 83: `Await a result by the `[answer]` the receiver sends by the skill `receive`; never await it by repeated messages.` Part of the point-2 gap.
[NOTE] card: a focus change owes a notice with no receivers named, so a build that moves through phases sends one per phase to unnamed peers — card 79: `Send a `[notice]` by the skill `tell` in the turn your name, focus, writes, or stewards change, ...`.
[NOTE] sweep: a long build whose card `updated` passes 24 hours, on a login change, meets sweep's gone test; the name look and the ask (sweep 5-7) and join 47 recover it — sweep 21: `...once presence lacks its address and its `updated` is over 24 hours old...`.
[NOTE] gossip: confirmed for acting on lines without the skill loaded — gossip 41: `Relay a gossip on seeing its `relay:` line, whatever skill text you have loaded; ...`, and the fixed line gossip 29 carries the instruction.

## Missing hand-offs
[NOTE] receive -> subagents: a `[hazard]` or `[notice]` that bears on a running subagent has no forward; only a ruling goes down — quote 41: `Forward to each running subagent of yours a ruling that bears on its task; never withhold one from it.` Level 1 "acting" (ontology 213) may cover a hazard.
[NOTE] resume -> heartbeat: resume 21 sets the wake from the card without naming heartbeat, whose restore rules (heartbeat 33-37) carry the cadence and expiry.
[NOTE] tell -> a limit-stopped receiver: no skill gives the sender a route for a member listed by presence yet stopped at the limit; tell 71 covers only a member presence does not list.
[NOTE] hooks -> any skill: no skill names the off switches, so a member told "turn the hook off" finds the answer only in hooks.json or the scripts.

## Terms
[NOTE] ontology 99: `bg` and `shell` sessions count as idle for level 2; the member's build-running session is busy in its own sense, so level 2 starts a turn mid-build (tell 65 holds only `busy`).
[NOTE] ontology 43: a wake is recurring only; the member's one-time timers after a build are not wakes.
[NOTE] heartbeat 21, 49 and volunteer 13: "free time" and "stretch free of your own work" have no ontology entry; skill-creation requires a definition for a narrow sense.
[NOTE] ontology 139: "live" folds in a usage-limit condition no check reads; "peer" (ontology 143) inherits it.

## Would not run
[NOTE] volunteer: on a shared limit the member would not run it unattended; volunteer 13 carves out stretches with work in hand, so a build in flight is not free, and the opt-out `state: dnd` is owner-only (card 87). Open items 2 and 3.
[NOTE] aid: unasked offers cost a peer a turn on a shared limit; the member would not run aid 13 (`Offer a fix, finding, or spare capacity a peer lacks, unasked; never wait to be asked.`) unattended. Open item 3 adjacent.
[NOTE] heartbeat: the member keeps no default wake while a long build runs; join 69 leaves the choice to it, so it would run heartbeat, set to a long cadence.

## Two procedures
[BLOCKS] receive: description line 4 `Handle a message that arrives from a peer: read it, check it, answer an ask, and hand each other kind to the skill that handles it.` Inbox reading (receive 13-21), answering an ask (26-42), and routing (44-54) fail the one-sentence test.
[BLOCKS] card: description line 4 `Keep your own member card true and current: its shape, its facts read afresh, its fields, the notice each change owes, and its parking state.` Parking (card 83-89) is a second procedure beside maintaining facts.
[BLOCKS] tell: description line 4 `Send a peer a tagged message: pick its receivers and type, write its type line, second line, and message body, then deliver it, hold it, or append it to an inbox by the receiver's state.` Composing (tell 18-60) and delivering (tell 62-80) differ. Open item 5, owner-held.
[NOTE] scribe: take, keep, circulate, ship, hand on (scribe 12-59); owner ruled it its own skill, split open item 5.
[NOTE] tend, steward, heartbeat, volunteer, gossip: each carries a router or a second step (tend 56-58, steward 28-34, heartbeat 42-50, volunteer 28-40, gossip 12-20 against 22-38 and 40-68); they pass the one-sentence test with an effort.

## Verdict
OBJECT. BLOCKS items: (1) level 1 cost, tell 63 and ontology 207; (2) level 2 to a limit-dead agent and unreadable "live", ontology 209 and 139; (3) receive holds more than one procedure, receive 4; (4) card holds two, card 4; (5) tell holds two, tell 4.
Items 1, 2, and 5 are draft open items 1, 6, and 5, so they go to the owner; items 3 and 4 are text fixes the draft does not list.

Summary: Point 5 is addressed (join 33-47), points 1-4 are partly or not addressed, and the draft's open items 1, 5, 6 match the member's remaining objections. No sentence the member could not work under was found beyond the level 1 cost (tell 63) and the level 2 dead-agent gap (ontology 209). Verdict is OBJECT with five BLOCKS items; hook off switches exist in code but no skill names them.

## Orchestrator's check of the cites, 2026-10-15T21:58+0300 (appended)
Read verbatim at `git show draft/10-skills:peers/skills/<skill>/SKILL.md`: all seven cites MATCH — tell:63, ontology:207, ontology:209, ontology:139, and the description lines receive:4, card:4, tell:4. Also read: card:87 ("never set it on your own judgment") and volunteer:13 ("never let such a stretch pass without looking for volunteer work") are unchanged in rev 2; the agent did not list them, but they are my own earlier BLOCKS (open items 2 and 3 of the draft) and stand.
My verdict: OBJECT. Blocking: level 1 without cap or coalescing (tell:63, ontology:207); level 2 to a member dead at a usage limit with no expiry or re-send, and `live` resting on a limit stop no skill can mark (ontology:209, ontology:139); owner-only dnd (card:87); volunteer spending the shared limit (volunteer:13). Not blocking: the hook off switches (named in code only — NOTE), and the receive, card, tell splits (NOTE; I told proudhon splits do not block me).
