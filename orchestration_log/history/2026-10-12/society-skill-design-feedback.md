# Feedback on the 24-skill society design (skill-roster.md), by claude-skills/instruction-eval

## Binding
Loaded in full: first-principles, self-documenting-code, simple-made-easy (manifesto repo), Strunk SPR v3 (curl), manifesto-oath. Convergence: derive from the evidence, one concern per unit, plain words, cut what carries no instruction. Tension: first-principles invites inventing skills, simple-made-easy says do not add; rule: add a skill only where a hand-off or procedure is demonstrably missing.
I must test each edge and skill against a session's real need, and I will cite the roster line and a lived fact for every objection. I must not decide, and I will not edit anything but this file.
I must keep one line per item in plain words, and I will not argue past the line; verdicts are BLOCKS or NOTE only.

Roster line numbers below are from skill-roster.md (R-n). Evidence: events.md (E-n), failures.md (F-n) in this directory.

## Missed hand-offs
[BLOCKS] receive -> heartbeat/card: a message arriving while dormant or dnd has no named hand-off to the skill that sets or clears that state — R53, R9
[BLOCKS] receive -> a relay: line carries its own instruction: the member acted on `relay:` without gossip loaded (E-189), yet the edge only says "load gossip when a relay line arrives" — R54, R6
[BLOCKS] receive -> relay for subagents: subagents cannot message peers, so the member relays what they report; no skill names this hand-off (receive/tell say "send", never "send for a subagent") — R54, R10 to R4
[BLOCKS] tell -> receive on a Level 1 override: tell has no edge to the level table's escalate-with-reason rule except through ontology; the sender needs the rule at the send step — R55, R45
[NOTE] join -> ontology: join names card, receive, heartbeat but not ontology; a joiner meets "commons as a location" and "root" unexplained — R53, R5
[NOTE] leave -> tell: leave must announce departure; edge missing (leave names card, steward, scribe, sweep only) — R68
[NOTE] sweep -> tell: moving a card to departed gives no notice to peers — R69, R20
[NOTE] adopt -> tend: adopt reads what others built in the commons; no edge to tend when the adopter finds it wrong — R63
[NOTE] vouch -> tell: a failed check has no stated route back to the origin — R64
[NOTE] heartbeat -> receive: a wake that finds queued messages must drain them; the edge is missing — R65, R5
[NOTE] settle -> quote: a go-between's ruling that is an owner ruling has no edge to quote — R67, R9
[NOTE] join -> continuity: a member whose ref and name changed after a login change (E-168) has no hand-off from join to card/sweep for carrying the card over — R53, R20

## Two procedures in one skill
Test: can the procedure be said in one sentence with no "and"?
[BLOCKS] receive: "what to do when a message arrives" holds five unlike procedures (relay, adopt, vouch, answer, consent) behind one door; it is a router, not a procedure — R11, R54
[BLOCKS] card: "keep true" and "carries state dormant/dnd (parking)" are two procedures (maintain facts; park and unpark) — R9
[BLOCKS] scribe: "hold the role", "ship by consent", "hand on" are three — R21
[BLOCKS] tend: "build, correct, merge, retire" are four acts with different gates — R14
[BLOCKS] tell: "tag, summary, reply line, ten lines, holds" mixes composing and holding a message — R4
[NOTE] aid: "fix, finding or capacity" are three offers with different vouch needs — R10
[NOTE] quote: "relay an owner ruling" and "hazard priority" and "keeps spreading" read as relay plus a level rule that already lives in ontology — R9, R37
[NOTE] ontology: terms plus the whole priority table plus the message-type list; the table is a second procedure (pick a level) — R1, R36-R45
[NOTE] steward: "look after a shared thing for every session" has no single procedure; reserve and settle sit under it — R16, R65-R67
[NOTE] volunteer: "turn not-busy time into society work" is a chooser over six skills; it is a router — R11, R60

## Missing skills
[BLOCKS] hold/pace: a spend-aware rule for unattended work: the account limit is shared, so an inbound message or a volunteer wake costs a full-context turn on a login that may be at its limit (E-170, E-177, F-3); nothing in the 24 says when not to wake, answer, or volunteer
[BLOCKS] relay-for-subagent: carry what a subagent reports to peers, since subagents cannot message them; owner of the send stays the member — R10
[BLOCKS] hook-off-switch: a hook needs an off switch and a state it can clear; a re-firing mandate needed its state file cleared by hand (E-161); no skill names the switch for the three hooks — R48
[NOTE] recover: after a login change, ref and name change and the card must carry to members/ and the old to departed (E-168); join or sweep could hold it, but no skill does
[NOTE] drain: a long-idle member returning from a limit gap faces a backlog; the owner said do not resume everything at once (E-170); a catch-up order is missing

## Levels that break work
[BLOCKS] Level 1 "every live session ... before its next step", overriding dnd, waiting and dormant: on a login at its limit, each [hazard] or [quote] costs a full-context turn for every member of that login; no cap, no coalescing, and a spread until "every live session holds it" multiplies it — R41-R43, E-170, E-177
[BLOCKS] Level 1 "overrides busy": a long unattended build mid-merge is told to stop "before its next step"; the build has no safe stop for a message that needs no action from it; no carve-out for a quote that changes nothing the member does — R41
[BLOCKS] Level 2 "at its next tool round": an agent that dies at the limit never has a tool round; the message waits unseen for hours (F-3, F-17); no expiry or re-send rule — R42
[BLOCKS] sender may mark one level up: any peer can drive Level 1 on every live session; a refusal costs the same turn as obedience, so the "receiver may refuse and report" safeguard fires after the cost is paid — R45
[NOTE] Level 3 "at its own wake": heartbeat wake is itself a turn on a possibly limited login; a wake that finds a board with no change should cost near nothing; heartbeat has no skip rule — R44, R65
[NOTE] "spreads until every live session holds it": "live" is unstated for a member dead at the limit, so the spread never ends or ends early — R41

## Would not run
[BLOCKS] volunteer: wakes a member into society work on idle time on a shared limit; would not run it unattended — R11
[BLOCKS] heartbeat wake hook (heartbeat wake prompt -> heartbeat): no off switch, no clearable state; a re-fired mandate once needed a hand-cleared state file (E-161) — R48
[BLOCKS] SessionStart -> join: a resumed session joining again after a login change would duplicate a card; needs a state check and an off switch — R48, E-168
[NOTE] send-stamp -> tell as a PreToolUse hook: fires on every send, including a relay for a subagent; would not run it without a bypass — R48
[NOTE] sweep: moves another member's card; a live member on a login change looks gone (E-168); would run it only after a ping — R20
[NOTE] aid unasked: offering to a peer costs it a turn; would not run it at Level 2 on a limited login — R10

## Summary
1. Biggest gap: nothing spends the shared limit carefully; Level 1 and volunteer cost full turns on every login.
2. Five skills hold more than one procedure; receive and tend most.
3. Subagent relay and hook off switch are missing as skills.
4. Eight small edges missing; most are tell or ontology links.
5. I decided nothing; the rewrite agent decides.
