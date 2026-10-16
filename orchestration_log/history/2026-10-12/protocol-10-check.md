# Check of protocol 10 (draft/10-skills @ 2da4feb) against claude-skills/instruction-eval's feedback and daily work

## Binding
Loaded in full: first-principles, self-documenting-code, simple-made-easy, Strunk SPR v3, manifesto-oath, memento:skill-creation. Convergence: derive from each cited line, one procedure per unit, plain names; tension: simple-made-easy accepts more parts, first-principles doubts the 25-part split; rule: judge a split by the one-sentence test, not by count.
I must tie each objection to a skill line and a fact of this member's work, and I will cite `<skill>:<line>` every time. I must not decide or edit, and I will write nothing but this file and message no one.

Lines cite the file as shown by `git show draft/10-skills:peers/skills/<skill>/SKILL.md`.

## The five points
[BLOCKS] 1 Level 1 cost: NOT. Level 1 still goes to every live session "whatever the receiver's state", with no cap or coalescing; a `[quote]` with no known scope goes society-wide at level 1 — tell:63, ontology:205, quote:39. Refusal of an escalation still costs a full turn — ontology:213.
[BLOCKS] 2 Level 2 at a dead agent: PARTLY. "Live" now excludes a member that stopped at a usage limit — ontology:137 — but nothing detects or marks that stop (the changes file lists it as open, rewrite/protocol-10-skills-changes.md:200). The hold has no expiry past reply time and no re-send rule — tell:65, ontology:207.
[NOTE] 3a Relay a subagent's reports: PARTLY. One line tells the main session to send what its subagent reports — tell:15, tell:5 — with no step that checks the report (vouch) and none that names the subagent as the claim's source.
[BLOCKS] 3b Hook off switch: PARTLY. `PEERS_HOOKS=off`, `PEERS_SEND_STAMP=off`, `PEERS_JOIN_HOOK=off` exist in code (changes file:131-136), but no skill names them, says who sets them, or how to clear them; ontology:247-249 map the hooks and stop there.
[NOTE] 4 One procedure per skill: PARTLY. receive, card, scribe, tend, tell are cut down; four still hold several (see Two procedures).
[NOTE] 5 Existing card on a restart: ADDRESSED. join searches `members/` and `departed/` by `project`, project directory, and `checkout` before writing, so a changed ref, name, or login does not mint a member — join:33, join:35, join:39; resume sends restarts there — resume:13. One defect on this path is under Breaks (join:35).

## Breaks the member's work
[BLOCKS] join: "never take a member id whose card's address presence lists live" — after a compaction or clear the member's own card address is live, so resume:13 (which sends compaction through join) forbids it its own id — join:35, resume:13.
[BLOCKS] card: dnd and dormant are set only on the owner's order, "never on your own judgment", and the owner is away at all times; a member in an unattended build can never shield itself from level 1 or wakes — card:83-89, ontology:69.
[BLOCKS] ask-around: "never read it as a lost delivery to resend" — for a peer dead at its limit, the seeker reads the held ask as "doesn't know" and gives up; this forbids the re-send point 2 asks for — ask-around:29, tell:79.
[NOTE] receive: "Check every claim by vouch before you use it" collides with level 1 "acted on before the receiver's next step" — receive:21, ontology:205; a hazard has no checked-yet-fast path.
[NOTE] tell: "Send freely ... no proof of gain" and "weigh a peer's time above your own" push sends at logins that share one limit — tell:21, tell:23.
[NOTE] heartbeat: "set your wake again ... never let it lapse" is unconditional, while join says "decide whether to keep a wake" — heartbeat:29-31, join:69; each wake is a full-context turn on a limit.

## Missing hand-offs
[BLOCKS] card -> tell/receive: no skill sets or clears a "stopped at limit" mark, yet `live` depends on it — ontology:137, card:71, card:83-89.
[BLOCKS] tell -> presence: a held message has no skill that rechecks the receiver's state and releases it — tell:65 ("until that state clears"), tell:73.
[NOTE] heartbeat -> receive: the default wake prompt names no inbox read, so a `reads` time has no timer — heartbeat:21, receive:13, card:67.
[NOTE] receive -> protocol-change: `[notice] protocol v<N>` is not in the hand-on list; only protocol-change's own description catches it — receive:44-52, protocol-change:5.
[NOTE] tell -> vouch: a subagent's report goes to peers with no named check — tell:15.
[NOTE] hooks -> any skill: the off switch has no skill to hand off to — ontology:247-249.

## Terms
[BLOCKS] ontology: "live" needs "not stopped at a usage limit", a fact presence cannot show; the member reads the term one way, a sender another — ontology:137, ontology:241.
[NOTE] ontology: `state` is "what presence shows together with the card's `state` line", but only the owner may write that line, so a member's own `state` can never name its limit — ontology:103, card:87.
[NOTE] ontology: `wake` is "a recurring timer", yet `reads` times and one-time reminders have no term — ontology:43, card:67.
[NOTE] ontology: `idle` is "between turns"; a session waiting on a background build is idle here and gets delivery that starts a full turn — ontology:95, ontology:107.
[NOTE] ontology: `harness-ref` "changed on restart" matches the member's fact — ontology:21, ontology:241 (confirmation).

## Would not run
[BLOCKS] volunteer: "never let such a stretch pass doing nothing" spends the shared usage limit that the unattended build needs, and the member cannot set a state to stop it — volunteer:13, volunteer:37, card:87.
[NOTE] quote: the member would run it, but its level 1 society-wide default is the main source of cost — quote:39.
[NOTE] heartbeat (default wake): pays a turn per cadence for "no output" — heartbeat:21; the member would set it only at a long cadence.
[NOTE] settle, reserve, steward, sweep: the member would run them as written; reserve fits its GPU and port use — reserve:13-19.

## Two procedures
[NOTE] scribe: taking the stewardship, keeping text, circulating, shipping, handing on — five sentences, not one — scribe:12, scribe:18, scribe:26, scribe:36, scribe:52.
[NOTE] heartbeat: choose and set, restore after restart, spend free time, end — heartbeat:12, heartbeat:28, heartbeat:38, heartbeat:42.
[NOTE] tell: write a message, deliver or hold by state, append to an inbox, await an answer — tell:46, tell:62, tell:76.
[NOTE] card: keep the card true, announce changes, mark parking — card:12, card:78, card:82.
[NOTE] gossip: originate an envelope, relay one — gossip:22, gossip:40.
[NOTE] tend: build, tend what stands, carry to peers (hand-off to spread-around, tend:56-58).
[NOTE] receive: read the inbox, answer an ask, hand on each kind; it holds as a dispatcher — receive:12, receive:26, receive:44.

## Verdict
OBJECT. BLOCKS items: (1) level 1 cap/coalescing absent — tell:63, ontology:205; (2) no limit-stop mark, no expiry, no re-send, and ask-around:29 forbids re-send — ontology:137, tell:65; (3) hook off switch named in no skill; (4) join:35 forbids a member its own id on compaction; (5) card:87 leaves a member no self-set dnd; (6) tell:65 has no release step; (7) volunteer:13 spends the limit.

Three-sentence summary: Protocol 10 fixes the card-search point (join:33) and part of the subagent-relay point (tell:15), but the usage-limit points and the hook off switch stay open. Seven BLOCKS items remain, led by level 1 with no cap (tell:63), `live` resting on an unmarkable limit stop (ontology:137), and join:35 forbidding a member its own id after compaction. Verdict is OBJECT; no file but this one was edited and no one was messaged.

## Orchestrator's check of the cites, 2026-10-15T21:22+0300 (appended; the text above stays as the agent wrote it)
Read against `git show draft/10-skills:peers/skills/<skill>/SKILL.md`:
- MATCH: tell:63 (level 1 delivered at once, never held), card:87 (dnd only on the owner's order), ask-around:29 (silence read as "doesn't know", never a resend), volunteer:13 (spend every free stretch).
- WRONG, retracted: join:35 — the line ends "unless that address is your own", so the member may take its own id; the BLOCKS item is void. tell:65 "no release step" — tell:67 says "Deliver a held message once its receiver's state clears or its reply time passes"; the release rule exists, demoted to NOTE (nothing prompts the recheck).
- CITE OFF: the live definition that excludes a usage-limit stop is ontology:139, not 137; the finding stands.
- UNCHECKED: the hook off-switch variables (changes file lines 131-136) and every other line number.
Verdict after the check: OBJECT on five BLOCKS — level 1 without cap or coalescing; `live` resting on a limit stop nothing can mark; no skill names the hook off switches (unchecked); card:87 leaving a member no self-set dnd; volunteer:13 spending the shared limit — with ask-around:29 forbidding the resend that point 2 needs.
