# Packet digest: silence (work-silently skill and hook)

## Binding

Loaded whole from source: first-principles.md, self-documenting-code.md, simple-made-easy.md (all under `/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/`); Strunk SPR v3 (curl, raw XML, composition rules read in the part fetched); oath protocol (`manifesto/3.2.0/skills/manifesto-oath/SKILL.md`, injected and read).
Axioms. First principles: only the verified remains; a name is not a source. Self-documenting code: the artifact itself must teach why; a gloss that drifts is a lie. Simple made easy: simple means not interleaved; more separate parts beat fewer tangled ones. Strunk: omit needless words, active voice, concrete terms, positive form.
Convergence: one fact per cell, each tied to its source. Tension: first principles demands re-derivation, Strunk demands brevity, simplicity accepts more parts, the 160-line cap forbids them. Rule: the cap wins; a table row carries one claim and one pointer; no commentary prose; a fix is an old-sentence to new-sentence pair, never a rewrite. Claim and fix stay in separate sections.
I must treat each peer figure as a claim, and I will re-count it from the packet file or mark it "claim". I must copy quotes by substring, and I will cite `file:line` for each. I must read the skill and hook myself, and I will cite their lines for every behavior I state. I must not decide or edit outside the two outputs, and I will not. I must not cite a Russian-authored source, and I will not; every citation is a repo, packet, or journal file.

## Today

1. Skill (`agent-conduct/skills/work-silently/SKILL.md`, 58 lines): enter silence at call, create `.claude/work-silently` (:9, :13); outside events never count as the user's message (:15, :17).
2. Work goes on through tool calls with bare-label descriptions; decisions, progress, findings go to records (:21-31).
3. Every silent turn ends with the empty string; no call to fill a turn, "a sleep, or a check whose answer cannot have changed" (:37-41); waits end by "a call that waits ... or a notification" (:43).
4. A user message gets an answer, then silence returns; an asked report is delivered once ready; only the user ends silence; the marker is deleted at the end (:47-57).
5. Hook: `hooks.json:4-14` runs `session-start.sh` at SessionStart (startup, resume, compact, fork); it exits unless the marker exists (`session-start.sh:8`), then prints `silence-mandate.txt` (one line) and the skill body (:10-13). No hook fires at any later moment. The Stop hook (`hooks.json:26-35`) belongs to check-back. The skill file is unchanged since v1.2.1 (937224c, 2026-09-27); cache copies 1.2.1, 1.7.0, 1.8.0 share one md5.

## Reports

Key: O = `own/`, P = `peers/`, E = `extracts/`. 25 files read; E1 (journal lines) used for two owner rulings.

| file | claim | evidence |
|---|---|---|
| O1 silence-ask | scribe asks peers to dig records for silence failures | owner order quoted :3 |
| O2 silence-answers | 13 answers, 8 peers; written rules failed, trigger removal and owner's literal words held | peer claims, :3-27 |
| O3 silence-report | adherence by project; 6 held, 4 failed | built from O2, :6-28 |
| O4 silence-records-findings | 1 typed silence failure (J14:218); break of 2026-10-16 never recorded; 12 gaps | table rows, :9-69 |
| O5 silence-records-brief | brief to a records auditor | no data |
| O6 silence-self-measure | scribe session: 41 turns, 8 model-text, 91 calls, 24 no-progress, 3 rebukes | transcript lines, :11-16, :62, :89-91 |
| O7 silence-self-brief | brief for O6 | no data |
| O8 silence-dig-deeper | owner: "nothing new" wake lines are a failure; asks for counts | :3 |
| O9 ambiguity-feedback | 4 gossip-protocol defects | not about silence |
| O10 bash-true-ask | count bare `true` calls in transcripts | method :8-9 |
| O11 bash-true-answers | LLM 20, memento 0, embedding 40 (corrected: session not mapped to d7) | :3-9 |
| O12 bash-true-self | scribe: 4 of 395 Bash calls are `true` | jq count :8-14 |
| P1 offline-kit silence | held in part; one undated padding line; doctor and commons wakes lack no-output rule | handoff.md:44, :24 as cited :11-12 |
| P2 offline-kit padding | 0 nothing-new records; 32 skipped-sync lines in an unattended log | :6, :9 |
| P3 LLM silence | 13 records, 0 recorded failures; 3 unwritten; no record of a system notice | :19-23, :29 |
| P4 LLM bash-true | 20 of 262 Bash calls are `true`, labelled "End the tick"/"End the turn" | :8, :10 |
| P5 gym silence | 81 text breaches, 10 filler lines; prose fixes failed; trigger removal and "empty strings" held | script table :33-39; fixes :58-69 |
| P6 pc silence | held badly; 8 no-op calls in a row (2026-10-06); report to owner after peer events | :7, :13 |
| P7 pc padding | 25 of 46 heartbeat entries say nothing new; prompt demands a record each wake | :5, :7 |
| P8 memento silence | no records of either order; 20 heartbeat lines; status lines to nudges | :6-7, :12 |
| P9 memento padding | 20 lines (15 strict) in 11 commits; cron step 5 is the cause | :5, :7 |
| P10 memento bash-true | 0 of 338 Bash calls | :5 |
| P11 embedding silence | d7: 6+ text turns, 190 padding lines; 8b: 7 text breaches; owner orders held, rules did not | table :9-17, mechanisms :64-77 |
| P12 embedding quiet-records | 5 nothing-new lines of 27; 21 other quiet lines; prompt collision | :13-19, :44 |
| P13 embedding bash-true | 40 `true`-class calls of 30440 Bash calls, one session tree | :6-8 |

## Failure modes

Counts: peers raising it with nonzero evidence, of 13; "text" = what SKILL.md says now.

**1. Status text answering the harness "no visible output" notice.** Peers: P5, P6, P8, P11 (4); P3 finds none recorded; own O6: 1 of 9 notices drew text (O6:102). Quote: `the harness line was read as the owner's message` (P5:48). Text: prevents in effect, never names the notice (SKILL:15, :17). A near-identical fix, `harness prompts for visible output get tool calls only`, failed with 18 more breaches (P5:60).
Old (SKILL:15) `including a notification, a tool's result, a reminder, a summary of earlier context` → new `including a notification, a tool's result, a reminder, a notice that your previous response had no visible output, a summary of earlier context`. Confidence low: text alone has not held (O3:23).

**2. Text or report after a peer message, heartbeat, notification, wake.** Peers: P5, P6, P8, P11 (4); P3 flags the risk, records none. Own: O6 3 of 8 model-text turns follow peer messages. Quote: `why'd you tell me this? i'm not the one asking. the society is.` (P6:13). Text: prevents (SKILL:17), and permits through the report clause (:49); O6:99 notes `no owner report ask in the boundary` for a 1154-character turn.
Old (SKILL:49) `never write past what that message asked.` → new `never write past what that message asked, and never deliver one because an outside event arrived.`

**3. Text answering an owner message that asks nothing (order, rebuke).** Peers: 0 firm (P8:12 weak); P5:47 records no owner-message trigger. Own: O6 3 of 4 owner-message turns carry text (O6:39); the owner replied `and now again .... gosh` (O6:90) to an apology. Owner ruling: `anybody writing ANY message besides literally empty ones is failing in silent work.` (E1, journal line 56). Text: causes (SKILL:47 `never stay silent toward it`; frontmatter :4).
Old (SKILL:47) `Pause silence to answer the user's message when the user writes; never stay silent toward it.` → new `Pause silence to answer a question the user's message asks; never answer an order or a rebuke.` See Particular 1.

**4. Bare no-op calls to end a turn (`true`, `echo`, short `sleep`).** Peers: P1, P4, P5, P6, P11, P13 (6); P10 reports 0. Own: O12 4 of 395. Quote: `a bare tool call made to end a turn the harness would otherwise nudge for "no visible output"` (O11:3). Labels pass SKILL:25 (`"End the tick" 16, "End the turn" 4`, P4:10). Text: prevents (:41) yet `Keep every turn in silence to tool calls alone` (:37) reads as a call per turn; P11:53 `re-prompt read as a turn that must contain a call`; P5:54 same.
Old (SKILL:37) `Keep every turn in silence to tool calls alone; never write text in one,` → new `Keep every turn in silence to tool calls alone, or to nothing when no work remains; never write text in one,`

**5. Records written on a quiet wake to show it ran.** Peers: P6, P7, P8, P9, P12 (5); P2 finds 0 records but 32 filler lines in an unattended log; P1 0. Quote: `(5) Write events in the memento journal for what happened.` (P9:7); `the 10-15 prompt carried both "silent when unchanged" and "journal each wake"` (P12:44). Text: permits (SKILL:31 sends progress to records; no sentence bars an empty one). The wake prompts live outside this plugin (peers heartbeat skill 0.8.0, :21 and :25, in the plugin cache).
Old (SKILL:31) `Write decisions, progress, and findings to the records; never write them to the conversation.` → new `Write a decision, progress, or a finding to the records when one has occurred, and never a record that nothing happened; never write them to the conversation.`

**6. Silence lost after compaction, resume, or on wakes laid without the rule.** Peers: P1, P5, P11 (3). Quote: `after the owner's compaction, three silent turns ended on text` (P5:51). Held once: a standing-orders digest restored after compaction (O2:27). Text: hook covers re-entry only (`session-start.sh:8-13`); whether the hook ran in gym is unknown (P5:102).
Old (`silence-mandate.txt:1`) `...and continue every task in hand under it; its text follows.` → new `...and continue every task in hand under it; every turn ends with zero characters until the user types stop; its text follows.` Confidence low.

**7. Reflex text; the corrected rule is never consulted at reply time.** Peers: P3, P5, P6, P11, P12 (5). Quote: `the reflex fires before the rule is consulted` (P5:53). Held once: `Check "before ending any turn, name what started it"` (P11:75, 0 breaches in 3 days; the count was later withdrawn as a recording gap, O2:13). Text: no sentence asks for the check.
Old (SKILL:39 tail) `never end one with a period, a status word, a summary, or any other character.` → new `...or any other character. Before ending a turn, name what started it; when the user did not type it, end it empty.`

**8. Polling and waiting calls while a wait is pending (CronList, git status, sleep).** Peers: P2, P5 (2). Own: O6 24 of 91 calls, 17 of them CronList (O6:62). Quote: `the harness prompt was treated as a demand for a tool call` (P5:54). Text: SKILL:41 bars them; SKILL:43 allows `a call that waits for it to finish`; check-back (same plugin) orders `On each wake, look at every pending run; never skip one.` (check-back SKILL:47) and a CronList sweep (:63).
Old (SKILL:43) `through a call that waits for it to finish or a notification sent when it finishes` → new `through a notification sent when it finishes, from a background command or a Monitor`. Basis: owner words `background bash only` (P8:12, one report).

## Conflicts

1. Rebukes: "twice" (O1:5) against three (O6:89-91).
2. Turns: journal says 8 text, 13 tool-only, 19 empty (O4:34); O6 table sums 9+13+19=41 with one harness-written text.
3. "Twelve calls" in the scribe's own answer (O6:56) against 24 strict and 13 in one window (O6:62, :83).
4. Top trigger: nudge (P5:48, P11:50) against O6, where 1 of 8 model-text turns follows a nudge and 3 follow owner messages (O6:39-41).
5. No owner-message trigger recorded (P5:47) against O6:39.
6. Matchtuner audit reads 0 breaches 10-13 to 10-16 (P11:15); its correction records about ten text turns after 15:47 (O2:13).
7. d7 190 padding calls (P11:44) against 40 `true`-class calls in the whole project tree (P13:7); definitions differ; the d7-to-session map is unchecked (O11:9).
8. Gym record counts 22 and 28 against script 25 and 37 (P5:41).
9. "Owner orders held" (O2:13) against P11:69, where two owner orders failed or were substituted by padding.
10. Wake prompt with a no-output rule held (P11:76) against P3 via O2:15, where a prompt saying `Write nothing to the conversation` still saw about 14 "Tick done: nothing new" lines.
11. Cause of padding calls: the nudge (O11:3, P5:54) against `it is not caused by a nudge` (E1, journal line 75).
12. Monitor: counted as no-progress (O6:60); recommended by check-back (SKILL:37) and held by memento (P8:12); failed alone for 8b (P11:72).
13. Skill length: P8:3 reads `SKILL.md 50 of 50`; the file has 58 lines (md5 identical in all cache versions).
14. Skill against skill: work-silently:41 against check-back:47 and :63.

## Unmeasured

- Per-turn text rates in any peer project: records only, by owner order (P5:96).
- Marker creation and deletion in practice; gym found it untracked (P5:82). Skill :13 says "directory the session started in", hook uses `CLAUDE_PROJECT_DIR` (`session-start.sh:5`); equality is assumed, not tested.
- Whether any hook event fires on the harness notice or can read the last turn's text.
- Whether check-back's text drove the 17 CronList calls in O6.
- Hook installation in each project when breaches occurred (P5:102).
- Any session run without the skill as control.
- Records were written by the sessions that breached (P5:71).
- Not asked: resident-anarchist answered late; instruction-iteration-skill-adoption never (O3:3).

## Particulars for the owner

1. May any text appear in silence? (a) Never; answers go to a file. (b) Only an answer to a typed question. (c) As today. Pick (a): your last ruling says only empty messages count, and two projects record that you read no conversation text (P3:34-35).
2. What does a wake with nothing new write? (a) Nothing: no line, commit, message, card edit. (b) One line, batched into the next real commit. Pick (a): you named the lines a failure (E1, journal line 53); liveness shows in the card.
3. How may a wait end? (a) Notification only. (b) Notification or Monitor; no sleep, no poll. (c) As today. Pick (b): Monitor is a notification source and check-back uses it.
4. When silence and check-back collide, which wins? (a) Silence: look only after a wake or notice fires. (b) Check-back. Pick (a): 24 of 91 calls in one session were such checks.
5. Fix by text only, or add a mechanical gate? (a) Text pairs above. (b) Also a hook, once the platform is shown to allow it. Pick (b): written fixes failed in gym, matchtuner, product-catalog (O3:23).
6. Wake prompts live in the peers heartbeat skill and in project crons, outside this plugin. Send the finding to that steward? (a) Yes. (b) No, this plugin only. Pick (a): FM 5 cannot close here.
