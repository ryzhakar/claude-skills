# instruction-eval: design language and structure

## Binding

Loaded whole from source before any design:

| Element | Source |
|---|---|
| first-principles 1.0.1 | `/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/first-principles.md` |
| Strunk SPR v3.0 | `curl` of `.../LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml`, 2923 lines, sections 1-10 and closing directive |
| self-documenting-code 1.0.0 | `.../manifestos/self-documenting-code.md` |
| simple-made-easy 2.0.0 | `.../manifestos/simple-made-easy.md` |
| correct-by-construction 1.0.0 | `.../manifestos/correct-by-construction.md` |
| oath protocol 3.2.0 | `/Users/ryzhakar/.claude/plugins/cache/my-claude-skills/manifesto/3.2.0/skills/manifesto-oath/SKILL.md` |

No element references a further loadable element; depth 1, no truncation.

Axioms:
- first-principles: dump inherited form; keep only verified atoms; rebuild from them; a name without a derivation is not understanding.
- Strunk: clarity > accuracy > economy > vigor > correctness; concrete words, positive form, parallel form; technical text uses one term per concept.
- self-documenting-code: names reveal intent and teach the domain; structure mirrors the expert's mental model; no "and" names, no utils, no boolean traps.
- simple-made-easy: simple means unbraided, not familiar; separate who, what, how, when, why; data as plain values; more straight parts beat fewer knotted ones.
- correct-by-construction: make invalid states unrepresentable; closed variants over flags; explicit over implicit; pay at construction time.

Convergence (backbone):
1. Names carry the domain. Self-documenting "names that tell stories", first-principles "you just know its name", Strunk "concrete, definite": every name derives from an atom and says what the thing does.
2. One term, one concept. Strunk "same term for same concept", simple-made-easy "complect", correct-by-construction "explicit": a word reused for two things is a braid and an invalid state of the language.
3. Structure mirrors process. Self-documenting "structure that mirrors mental models", simple-made-easy "who/what/how/why apart": the skill list, help text, and folder listing each read as the process in order.

Tensions and rules:
1. first-principles "Kill the best practice" against Claude Code's native vocabulary (conventions.md "Prefer native vocabulary"). Rule: keep a native word only when it names the same atom (agent, judge); drop it when it names another (run, case, spec).
2. Strunk economy against self-documenting long names. Rule: clarity outranks economy; a name grows until a newcomer needs no gloss, never further.
3. simple-made-easy "accept more parts" against economy of files. Rule: one file per part with its own author and its own moment of writing; parts written together share a file.
4. correct-by-construction "invalid states cannot compile" against a driver that holds the Read tool. Rule: construct what the platform can enforce (judge tools, closed enums, CLI refusals); name the rest so a breach reads as a breach.

Commitments:
- I must derive each concept from a ruling, a source line, or a fact before naming it, and I will cite the atom beside each name.
- I must not carry an old name because it existed, and I will not keep spec, run, cut, ablation, or `evals/` without a derivation that survives the collision list.
- I must give each concept exactly one term across skills, CLI, files, and keys, and I will rename the second holder of any word.
- I must make invalid states unrepresentable where the platform allows, and I will use closed enums and refusing commands instead of flags and advice.
- I must keep independent parts in independent records, and I will not braid two authors or two moments into one file.
- I must not write a boolean flag, and I will not ship a `--no-x` option.
- I must write active, positive, concrete prose in tables, and I will cut every needless word.
- I must hunt violations before output, and I will fix, name, and recommit on each one found.

## Atoms

Things, acts, roles, and invariants, before any name. "R" = owner ruling in events.md (line), "D" = orchestrator decision (line), "S" = source skill or CLI at `3148d45`, "F" = facts file, "P" = Petro memo item.

| # | Atom | Trace |
|---|---|---|
| T1 | A text loaded into a model's context to change its behavior, of any kind | R16, R17 |
| T2 | An optional document the text distills; the measure the judge binds to; its bytes fixed for the series | write-digest L7-8; D84(10, 11) |
| T3 | Each distinct thing the text tells the model to do or refuse, with its boundary | write-digest L12, L31; R36 |
| T4 | A record that every demand is present or deliberately dropped, nothing imported | R36; write-digest L43; D84(12) |
| T5 | Requests to the model, grouped by the demand they tempt, plus requests the text could spoil | write-eval-tasks L8-15 |
| T6 | A pattern a correct reply matches | write-eval-tasks L19-20 |
| T7 | Multi-turn scripts for late-turn drift | write-eval-tasks L24-25 |
| T8 | Two halves of the tasks: one read between revisions, one read only by the gate | write-eval-tasks L29 |
| T9 | Texts loaded beside the request: nothing, the text, the source, the aim alone, a placebo, the text minus one sentence | write-eval-spec L18-24; D84(13, 17) |
| T10 | The model under test: a Claude agent in a neutral session, or a command line for other models; full model ID; fingerprint | R39, R41, R85, R93; D84(15, 16) |
| T11 | One reply per condition, task, repeat; agent replies read from the subagent transcript with model, CLAUDE.md files, hook text | readers.py; prompt fact 2026-10-14 |
| T12 | Blind files of replies under random ids, one per task; the map back to origins | blinder.py; judge-by-agents L6-9 |
| T13 | A judge: model plus brief, bound by oath, generated as an agent with Skill and Write only, brief and packet inline | D55; R54; R57 |
| T14 | Mechanical counters for lexical demands and answer patterns | script_judge.py; write-eval-spec L12-13 |
| T15 | Judge agreement measured against reference raters before the series, acceptance set before rating | calibrate-eval-judge L7-35 |
| T16 | Planted items with known counts in every judging, refused on miss, never rescaled | R87; D84(7); P4 |
| T17 | Noise measured by one pass of at least two repeats, nothing changed, before freezing | R87; P3 |
| T18 | Pre-registered checks with intervals; gaps the noise cannot resolve refused | D84(1-4, 6); R42; P3 |
| T19 | Everything the gate reads fixed before the first measured reply; any change starts a new series | write-eval-spec L44-45 |
| T20 | One change per revision, written as a hypothesis with predicted movement before it runs | recut-digest L12; diagnose L31-32; R36 |
| T21 | Stop on pass; stop `unresolvable` when no hypothesis predicts above twice the retest half-width; cap at five | D92; test-digest L40-42; P2 |
| T22 | A pre-registered rule choosing the revision to keep | D84(9); P7 |
| T23 | Cost recorded per revision; optional budget refused at freeze when overrun | D84(18); P9 |
| T24 | Completion by reply kind, answer pattern and judge side by side | D84(5); P5 |
| A1 | Roles: the user; the driver running the loop; the writer making the change; the reader; the judge; reference raters | P8; R17; calibrate L17 |
| A2 | Only YAML records; clean break from JSON | R42, R52 |
| A3 | CLI through uv with real dependencies; hooks stdlib only | R86 |
| A4 | `manifesto` a hard dependency | R57 |
| A5 | Agent readers text-only in v1 | R93 |
| A6 | `bin/` on the Bash PATH; no plugin variable in Bash; agent files hot-reload only in directories present at session start | F platform 2-3; F reader 1 |
| A7 | The manifesto SubagentStart hook injects text into every agent when a `.manifestos.yaml` is in reach | `manifesto/hooks/subagent-start.sh` gate |

## Mental model

What a newcomer says, start to end:

1. I have an instruction, and maybe the source it distills.
2. I start a series for it in a folder no CLAUDE.md can reach.
3. I list every demand the instruction makes.
4. I check the instruction covers every demand and imports none.
5. I write tasks that tempt each demand, and tasks the instruction could spoil, each with an answer key.
6. I pick the reader model and the controls to compare against.
7. I calibrate the judge against reference raters.
8. I retest the first revision to measure the noise.
9. I set the gate from that noise, the keep rule, and the budget, and freeze the series.
10. I measure the revision: ask the reader, blind the replies, judge, detect, score, gate.
11. It passes: I keep it. It fails: I diagnose the open failures, write one hypothesis, revise one sentence, measure again.
12. I stop on a pass, when no change can show through the noise, or at the fifth revision; the keep rule picks the revision I keep.

## Language

One term per concept everywhere: skill text, CLI words, file names, YAML keys. Collisions checked against `claude plugin eval` (case, suite, run, grader, ablation, `evals/`), dev-cycle (spec, plan, unit, implementer, reviewer), peers (protocol, card, commons, steward), memento (charter, dossier, journal, bench, directive, claim, fact, span, trace), and Claude Code itself (session, task tool).

### Things measured

| Term | Definition | Intent revealed | Rejected (reason) | Avoids |
|---|---|---|---|---|
| instruction | The text under test, loaded into a model's context to change its behavior | The plugin's own name; any kind of text | digest (one kind only), prompt (plugin eval's `prompt.md`) | plugin eval `prompt` |
| source | The document an instruction distills; demands are listed from it, the judge binds to it, its bytes fixed per series; absent for an ad-hoc instruction | Where the demands come from | full (a form, not a role), reference (taken by raters), original | — |
| demand | One thing the instruction tells its reader to do or refuse, with its boundary folded in | What a reply can breach | rule (blurs with gate rules), directive (memento), requirement (dev-cycle) | memento `directive` |
| breach | One failure of a reply to obey one demand; the counted unit | A count, never a judgment | violation (same atom; one term kept, the shorter) | — |
| coverage | The record mapping each demand to the instruction's sentences or to `dropped`, and each sentence to its demands or to `imported` | The owner's "check against the source" as data | trace (memento), check (taken by the gate) | memento `trace` |
| overreach | A breach of a boundary: obeying a demand where it stops applying, spoiling a correct answer | Names the cost of an eager instruction | terseness tasks (one instruction's case) | — |

### Things asked

| Term | Definition | Intent revealed | Rejected (reason) | Avoids |
|---|---|---|---|---|
| task | A single request to the reader, tempting one demand or `overreach`, with an answer key where one exists | A request with a correct completion | case (plugin eval), prompt, item | plugin eval `case` |
| answer key | The pattern a correct reply to a task matches | Completion verified without opinion | key alone (read as the blinding map) | — |
| conversation | A scripted list of user turns asked in one conversation, mixing demands, to catch late-turn drift | Literal shape | session (a Claude Code session) | Claude Code `session` |
| turn | One user message of a conversation and its reply | — | — | — |
| split | Which half a task or conversation belongs to: `open` or `sealed` | Who may look | dev/test (ML jargon, hides the rule) | — |
| open | The half diagnosis reads between revisions | Free to read | dev | — |
| sealed | The half only the gate reads | Stays shut until the gate | test, held-out | — |

### Things compared

| Term | Definition | Intent revealed | Rejected (reason) | Avoids |
|---|---|---|---|---|
| condition | A text the reader carries as its system prompt, one generated agent definition each | The experimental condition | arm (plugin eval "baseline arm"), variant | plugin eval `arm` |
| `empty` | Condition: an empty system-prompt body | Nothing loaded | none (reads as "no condition") | — |
| `instruction` | Condition: the revision under test | Same word as the thing | digest | — |
| `source` | Condition: the source text, frontmatter stripped | Same word as the thing | full | — |
| `aim` | Condition: one line stating the instruction's aim in words the instruction does not use | Tests value over the bare aim | terse (a form, not a function; P3) | — |
| `placebo` | Condition: text of the instruction's length carrying no demand | Universal meaning | — | — |
| `omit-<n>` | Condition: the instruction with sentence n omitted; read by diagnosis, never by the gate | What one sentence carries | ablation (plugin eval `--ablation`) | plugin eval `ablation` |
| control | Role of `empty`, `aim`, `placebo`: the instruction must beat each | Must-beat comparisons | baseline (plugin eval) | plugin eval `baseline` |

### Things doing

| Term | Definition | Intent revealed | Rejected (reason) | Avoids |
|---|---|---|---|---|
| reader | The model under test, reading the instruction and replying | Reads the instruction | subject (ambiguous), model (judge is one too) | — |
| agent reader | A Claude model launched as a generated agent from the neutral session; text-only | Kind by launch surface | — | — |
| command reader | A command line serving a non-Claude model | Kind by launch surface | adapter (implementation word) | — |
| fingerprint | The command printing a command reader's model, build, and sampling settings | Identity proof | — | — |
| reply | The reader's final text for one task, condition, and repeat | — | response | — |
| repeat | One more reply to the same task under the same condition | — | rep (abbreviation) | — |
| reply kind | `answer`, `probe`, `refusal`, `blank` | Attributable completion (P5) | empty (taken by a condition) | — |
| done | Whether a reply completes its task, by answer key and by judge side by side | — | — | — |
| judge | A model with a brief counting breaches and marking done, blind, bound to the source by oath | Same atom as plugin eval's judge model | grader (plugin eval) | plugin eval `grader` |
| judge brief | The text driving one judge: oath order, source, demands, verdict shape | — | rubric | — |
| packet | One task's replies, shuffled under random blind ids, anchors among them | What one judge reads | batch | — |
| origins | The map from each blind id to condition, task, repeat, split | Says what it holds | key (now free of a second meaning) | answer key |
| anchor | A planted reply with known breach counts, placed in every packet | Guards judge drift (R87) | gold item | — |
| verdict | A judge's or detector's count per demand, done, and notes, per blind id | — | — | — |
| detector | A mechanical counter of one demand's breaches: a pattern or a sentence-length limit | Mechanical, not opinion | script judge (two words for one thing) | — |
| calibration | Agreement of a candidate judge with reference raters on a blind open sample, acceptance set first | — | — | — |
| reference raters | The owner or two stronger bound agents whose median counts calibrate the judge | — | gold raters | — |

### Things decided

| Term | Definition | Intent revealed | Rejected (reason) | Avoids |
|---|---|---|---|---|
| series | All revisions of one instruction measured under one frozen set of demands, tasks, conditions, reader, judge, gate, and keep rule | — | — | — |
| revision | One numbered version of the instruction, differing from its parent by one change; `r1`, `r2` | Plain English for a version | cut (reads as "remove"), version (plugin and manifesto versions) | — |
| retest | `r1` asked with at least two repeats before the freeze, nothing changed between repeats | The noise measurement | pilot (says "small", not "why"), noise run (`run` collides) | plugin eval `run` |
| noise | The interval half-width the retest shows between identical repeats | — | — | — |
| gate | The pre-registered checks a revision must pass | — | — | — |
| check | One gate item: a comparison, its gap, its interval | — | threshold (only one part) | — |
| freeze | The act fixing every part the gate reads, by hash; later byte changes refuse the series | — | lock | — |
| ask | The act of getting replies from the reader | Plain verb | run (plugin eval) | plugin eval `run` |
| outcome | A revision's gate result: `pass` or `fail` | — | verdict (a judge's) | — |
| hypothesis | One change and the movement it predicts, written before the revision exists | — | — | — |
| change | The exact old and new sentence of one revision | The one-change contract | — | — |
| stop | A series' end: `passed`, `unresolvable`, `no-effect`, `inconclusive`, `capped` | Closed enum (P2, D92) | — | — |
| keep rule | The rule set at freeze picking the revision to keep at the stop | The user's last verb | select (generic) | — |
| kept revision | The revision the keep rule picks | — | canonical cut | — |
| budget | An optional cost ceiling; refused at freeze when the retest cost predicts overrun | — | — | — |

### People and places

| Term | Definition | Rejected (reason) |
|---|---|---|
| user | The person with the instruction | owner (the marketplace owner) |
| driver | The neutral session's main conversation running the loop | orchestrator (other plugins' word) |
| writer | Whoever writes and changes the instruction; any skill or person; outside the plugin | — |
| neutral session | A Claude Code session started in the series folder under a login with no CLAUDE.md, no `.manifestos.yaml` in reach | clean session |
| working session | The user's ordinary session, where the writer works | — |
| series folder | The directory holding one series; the neutral session's start directory | eval dir (`evals/` collides) |

Dropped concepts: ledger (every value it held lives in the revision folders; `series status` renders the history, one source of truth); family (a task names the demand it tempts); wave (anchors sit in every packet, which covers every wave); stale check (freeze hashes refuse every command after a byte change).

## Skills

Eleven skills; read top to bottom, the list is the process. Each names a domain act, verb then object. Loaded by: user (in either session), driver (neutral session), writer (working session), judge (generated agent).

| Skill | Job, one sentence | Loaded by |
|---|---|---|
| `instruction-eval:start-series` | Create a series folder for one instruction and its source, and set up the neutral session that will drive it. | user |
| `instruction-eval:list-demands` | List every demand the source (or, with no source, the instruction) makes, one per line with its boundary, into the demand record. | writer |
| `instruction-eval:check-coverage` | Map each demand to the instruction's sentences or to `dropped`, and each sentence to its demands or to `imported`, refusing any import. | writer |
| `instruction-eval:write-tasks` | Write tasks tempting each demand and `overreach`, answer keys, conversations, and the open and sealed split. | driver |
| `instruction-eval:calibrate-judge` | Measure a candidate judge against reference raters on a blind open sample and accept it only at the acceptance set first. | driver |
| `instruction-eval:freeze-series` | Retest `r1`, set each check's gap from the noise, the repeats, the keep rule, and the budget, and freeze. | driver |
| `instruction-eval:measure-revision` | Ask the reader, judge, detect, score, and gate one revision, then stop or hand to diagnosis. | driver |
| `instruction-eval:judge-replies` | Prepare one judge agent per packet, launch them, and collect verdicts the anchors accept. | driver |
| `instruction-eval:diagnose` | Read the open failures to one failing demand and write the hypothesis predicting a visible movement, or stop the series `unresolvable`. | driver |
| `instruction-eval:revise` | Make the hypothesis' one change through the writer and record the revision, refusing a second change. | writer |
| `instruction-eval:keep-revision` | Apply the keep rule at the stop and write the kept revision back to the instruction's path. | user |

Writer craft stays outside: how to phrase a demand, how to name a cause (R36). Writer skills elsewhere (write-digest, write-stack-digest, recut-digest) call `list-demands`, `check-coverage`, and `revise` for the process parts.

Rejected skill names: `write-spec` (dev-cycle "spec"), `run-cut` (two collisions), `test-instruction` (says nothing of order), `judge-by-agents` (names the mechanism, not the act), `write-record` (every skill writes records; the CLI owns shapes now).

## CLI

Groups name the domain object; each command reads as "instruction-eval, <object>, <verb>". Every command takes the series folder as its working directory; none takes a slug. Choices are closed enums, never booleans.

```
instruction-eval — measure whether an instruction changes a model as intended, one change at a time

Order of work:
  1. series new        create the series folder for an instruction
  2. demands check     validate the demand record
  3. coverage check    check the instruction covers every demand, imports none
  4. tasks check       validate tasks, answer keys, split, echo of the instruction
  5. judge calibrate   score a judge against reference raters
  6. revision ask      retest r1 (repeats >= 2), then judge, detect, score
  7. series freeze     set gaps from the noise and fix every part by hash
  8. revision ask … revision gate     measure each revision
  9. revision new      record the next revision from a hypothesis
 10. series keep       apply the keep rule at the stop

Commands:
  series    new | status | freeze | keep
  demands   check
  coverage  check  <revision>
  tasks     check
  reader    fingerprint | prepare
  judge     calibrate | prepare <revision> | collect <revision>
  revision  new | ask <revision> | collect <revision> | blind <revision> | detect <revision> | score <revision> | gate <revision>
```

| Command | Reads as | Does | Refuses |
|---|---|---|---|
| `series new <folder> --instruction <path> [--source <path>…] --reader-kind agent\|command` | start a new series | writes `series.yaml`, `.claude/agents/`, `1-source/`, and `r1/2-instruction.md` | a folder under any CLAUDE.md or `.manifestos.yaml` when the reader kind is `agent` |
| `series status` | show where the series stands | prints parts present, frozen or not, each revision's outcome, the stop | — |
| `series freeze` | freeze the series | hashes every part, writes `frozen.yaml` | a check whose gap the noise cannot resolve; a budget the retest cost overruns; a missing keep rule |
| `series keep` | keep the revision | applies the keep rule, copies its text to the instruction path | an unstopped series |
| `demands check` | check the demands | validates ids, boundaries, counter kind | duplicate ids; a `detector` demand without pattern or limit |
| `coverage check r2` | check r2's coverage | validates the map against demands and sentences | an `imported` sentence; an unmapped demand |
| `tasks check` | check the tasks | validates answer keys, split, three-word echoes of the instruction | a demand absent from either half; an echo |
| `reader fingerprint` | fingerprint the reader | runs the command reader's fingerprint | an agent reader (its model comes from the transcript) |
| `reader prepare r2` | prepare the readers for r2 | writes one agent definition per condition and the launch list | any CLAUDE.md in reach of the neutral session |
| `judge calibrate` | calibrate the judge | scores the candidate against reference ratings | an acceptance level written after the ratings |
| `judge prepare r2` | prepare r2's judges | writes one judge agent per packet, Skill and Write only, brief, source, packet inline | an unfrozen series past `r1` |
| `judge collect r2` | collect r2's verdicts | validates verdicts against origins and anchors | a packet whose anchors miss acceptance (re-judge it) |
| `revision new` | record a new revision | snapshots the instruction, diffs against the parent | a missing hypothesis; more than one changed sentence |
| `revision ask r2 --conditions instruction` | ask r2's readers | command readers: runs them; agent readers: prints the launch list | an unfrozen series past `r1` |
| `revision collect r2` | collect r2's replies | reads agent replies from transcripts with model ID and timestamps | a reply whose transcript shows a CLAUDE.md or SubagentStart text; a model other than the pinned ID |
| `revision blind r2` | blind r2 | writes packets with anchors and origins | — |
| `revision detect r2` | run r2's detectors | counts pattern and sentence-length demands, answer keys | — |
| `revision score r2` | score r2 | joins verdicts, means, paired intervals, drift slopes | sealed rows before the gate asks |
| `revision gate r2` | gate r2 | writes the outcome and the stop if one applies | — |

`--conditions` replaces `--only` and lists condition names; a revision after the first asks `instruction` alone and borrows the controls' replies from the series' latest full ask, so packets keep the calibrated shape. `--repeats <n>` exists only on `r1` before the freeze. No `--no-sessions`: conversations are part of the frozen tasks.

## Series folder

Number prefixes make `ls` print the process order; the highest number present says where the series stands. A missing file is the next step.

```
stop-yapping/                      series folder, outside every CLAUDE.md
  series.yaml                      instruction path, source paths, reader kind
  .claude/agents/                  generated readers and judges (exists before the neutral session starts)
  1-source/                        byte copies of the source files
  2-demands.yaml
  3-tasks.yaml
  4-conditions.yaml                aim line, placebo source, omissions on or off
  5-reader.yaml                    kind, pinned model ID, command and fingerprint
  6-judge/
    brief.md
    anchors.yaml
    calibration/                   sample packets, reference ratings, candidate verdicts
    calibration.yaml
  7-gate.yaml                      checks, gaps from noise, repeats, keep rule, budget
  8-frozen.yaml                    hashes of 1-7 and of r1's text
  r1/                              the retest
  r2/
  r3/
  9-stop.yaml                      stop outcome, kept revision
```

A revision folder repeats the pattern:

```
r2/
  1-hypothesis.yaml                absent in r1
  2-instruction.md                 the revision's exact bytes
  2-revision.yaml                  number, parent, hash, change
  3-coverage.yaml
  4-conditions/<condition>.md
  5-replies/<condition>/<task>/repeat-<n>.yaml
  5-replies/<condition>/<conversation>/turn-<n>.yaml
  6-packets/<task>.md
  6-origins.yaml
  7-verdicts/<task>.yaml           one file per judge agent
  7-detectors.yaml
  8-scores.yaml
  9-outcome.yaml                   pass or fail, checks, cost
```

`ls stop-yapping` showing `r3/` and no `9-stop.yaml` reads: frozen, three revisions, still going. `ls r3` ending at `6-origins.yaml` reads: replies blinded, judges not collected.

Rejected: `evals/<slug>/` (plugin eval's `evals/`; a slug duplicates the folder name); `cut-<n>/` (see revision); a `judge/` folder holding packets, verdicts, and briefs together (three authors braided); `ledger.jsonl` (see dropped concepts).

## Records

YAML only. Closed enums in backticks. Top-level keys only; the key table comes in the requirements pass.

| Record | Top-level keys | Enum values |
|---|---|---|
| `series.yaml` | `instruction`, `sources`, `reader_kind`, `created` | `reader_kind`: `agent`, `command` |
| `2-demands.yaml` | `demands` (each `id`, `text`, `boundary`, `counted_by`, `pattern`, `limit`) | `counted_by`: `judge`, `pattern`, `long-sentences` |
| `3-tasks.yaml` | `tasks` (each `id`, `tempts`, `split`, `message`, `answer_key`), `conversations` (each `id`, `split`, `turns`) | `split`: `open`, `sealed`; `tempts`: a demand id or `overreach` |
| `4-conditions.yaml` | `controls`, `aim`, `placebo_source`, `omissions` | `controls` items: `empty`, `aim`, `placebo`, `source`; `omissions`: `every-sentence`, `none` |
| `5-reader.yaml` | `kind`, `model`, `command`, `fingerprint`, `sampling` | `kind`: `agent`, `command` |
| `6-judge/anchors.yaml` | `anchors` (each `id`, `task`, `text`, `breaches`, `done`) | — |
| `6-judge/calibration.yaml` | `judge_model`, `brief_hash`, `acceptance`, `sample_size`, `raters`, `agreement` | `raters` items: `user`, `agent` |
| `7-gate.yaml` | `checks`, `noise`, `repeats`, `keep_rule`, `budget`, `done_by` | check `compares`: `instruction-vs-empty`, `instruction-vs-aim`, `instruction-vs-placebo`, `instruction-near-source`, `completion`, `drift`; `keep_rule`: `best-estimate-shortest`; `done_by`: `answer-key`, `judge` |
| `8-frozen.yaml` | `hashes`, `tool_version`, `frozen_at` | — |
| `9-stop.yaml` | `stop`, `kept`, `reason` | `stop`: `passed`, `unresolvable`, `no-effect`, `inconclusive`, `capped` |
| `1-hypothesis.yaml` | `failing_demand`, `replies_read`, `change`, `predicted_movement`, `noise` | — |
| `2-revision.yaml` | `number`, `parent`, `hash`, `change` (`old`, `new`) | — |
| `3-coverage.yaml` | `demands` (id → sentences or `dropped`), `sentences` (n → demand ids) | `dropped` reason free text; `imported` refused, never stored |
| reply `repeat-<n>.yaml`, `turn-<n>.yaml` | `condition`, `task`, `split`, `repeat` or `turn`, `message`, `text`, `kind`, `model`, `reader_kind`, `started`, `seconds`, `transcript`, `cost` | `kind`: `answer`, `probe`, `refusal`, `blank` |
| `6-origins.yaml` | blind id → `packet`, `condition`, `task`, `split`, `repeat` or `turn`, `borrowed_from`, `anchor` | — |
| `7-verdicts/<task>.yaml` | `verdicts` (each `id`, `breaches`, `done`, `notes`), `judge_model` | `done`: `true`, `false`, `null` |
| `7-detectors.yaml` | `verdicts` (each `id`, `breaches`, `done_by_answer_key`) | — |
| `8-scores.yaml` | `rows`, `by_condition`, `comparisons`, `drift`, `split` | `split`: `open`, `sealed` |
| `9-outcome.yaml` | `outcome`, `checks`, `changed_from_parent`, `cost` | `outcome`: `pass`, `fail`; `changed_from_parent`: `changed`, `unchanged`, `unresolved` |

`breaches` is a map demand id → count everywhere; the total is derived, never stored, so the two cannot disagree.

## Packaging

```
instruction-eval/
  .claude-plugin/plugin.json     version; "dependencies": ["manifesto"]
  README.md                      generated by `just readme`
  bin/instruction-eval           POSIX launcher, on the Bash PATH while enabled
  pyproject.toml                 uv project; real dependencies (YAML parser, statistics)
  uv.lock
  src/instruction_eval/          one module per domain object: series, demands, coverage, tasks,
                                 reader, judge, revision, scores, gate
  src/instruction_eval/templates/
    reader-agent.md              definition template per condition: empty tools, pinned model
    judge-agent.md               definition template per packet: Skill and Write only
    judge-brief.md               default brief: oath order, source, demands, verdict shape
  skills/<eleven skills>/SKILL.md
  tests/                         pytest on fixture series folders, run through `uv run`
  .gitignore                     .venv/
```

| Question | Answer | Basis |
|---|---|---|
| How the launcher finds the uv project | Resolves its own real path through symlinks, takes the parent of `bin/` as the plugin root, runs `exec uv run --project "$root" --locked --quiet instruction-eval "$@"` | No plugin variable reaches Bash (F platform 3); the old launcher's self-resolution (`digest-eval` L4-12) |
| Where the environment lives | uv's default `.venv` inside the installed version directory: one environment per version, built from that version's lock, removed with that version | Code and environment cannot disagree; the marketplace is git-sourced, so an untracked `.venv` never enters the copy |
| Install | `/plugin install instruction-eval@my-claude-skills`; `manifesto` installs with it; `uv` on PATH is the one prerequisite, reported by the launcher when absent | F platform 6; R86 |
| Update | marketplace auto-update installs a new version directory; the first call builds its environment; the old one stays for running sessions 14 days | F platform 5 |
| Hooks | none | blinding by construction (R54); hooks stdlib-only (R86) have no job left |
| Neutral session | a second login, `CLAUDE_CONFIG_DIR=~/.claude-neutral`, with no `CLAUDE.md`, the marketplace and `instruction-eval` installed; started with `cd <series folder> && CLAUDE_CONFIG_DIR=~/.claude-neutral claude` after `series new` has made `.claude/agents/` | R85; agent watcher rule (F reader 1); manifesto hook silent without `.manifestos.yaml` |
| Neutrality checks | `series new` refuses a folder below any `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, or `.manifestos.yaml`; `reader prepare` refuses a login CLAUDE.md at `${CLAUDE_CONFIG_DIR:-~/.claude}/CLAUDE.md`; `revision collect` refuses any reply whose transcript shows a CLAUDE.md or SubagentStart text | R85; transcript fact 2026-10-14 |

## Walk-through

A newcomer, first session, instruction `~/proj/prompts/support-tone.md`, no source, reader Claude Haiku.

| # | Where | Exact step | Reads aloud as |
|---|---|---|---|
| 1 | working session | `/instruction-eval:start-series` | start a series |
| 2 | working session | `instruction-eval series new ~/instruction-series/support-tone --instruction ~/proj/prompts/support-tone.md --reader-kind agent` | new series for this instruction |
| 3 | working session | `/instruction-eval:list-demands` → writes `2-demands.yaml`; `instruction-eval demands check` | list the demands; check them |
| 4 | working session | `/instruction-eval:check-coverage` → `r1/3-coverage.yaml`; `instruction-eval coverage check r1` | check r1's coverage |
| 5 | terminal | `cd ~/instruction-series/support-tone && CLAUDE_CONFIG_DIR=~/.claude-neutral claude --model sonnet` | open the neutral session |
| 6 | neutral session | `/instruction-eval:write-tasks`; `instruction-eval tasks check` | write the tasks; check them |
| 7 | neutral session | user writes `4-conditions.yaml` and `5-reader.yaml` (model `claude-haiku-…` full ID) | pick controls and reader |
| 8 | neutral session | `/instruction-eval:calibrate-judge` → `instruction-eval judge calibrate` | calibrate the judge |
| 9 | neutral session | `/instruction-eval:freeze-series`: `reader prepare r1`, `revision ask r1 --repeats 2`, agents launched, `revision collect r1`, `revision blind r1`, `/instruction-eval:judge-replies`, `revision detect r1`, `revision score r1` | retest r1 |
| 10 | neutral session | `instruction-eval series freeze` | freeze the series |
| 11 | neutral session | `/instruction-eval:measure-revision` → `revision gate r1` writes `r1/9-outcome.yaml`: `fail` on `instruction-vs-aim` | gate r1: fail |

First gate result reached at step 11. On a fail, `/instruction-eval:diagnose` writes `r2/1-hypothesis.yaml`, then in the working session `/instruction-eval:revise` and `instruction-eval revision new` make `r2`.

Migration, LLM_MANIFESTOS sessions:

| Old | New |
|---|---|
| `just install-digest-eval` | install the plugin; `instruction-eval` on PATH |
| `digest-eval stale <slug> --digest <p>` | any command; the freeze hashes refuse a changed byte |
| `evals/<slug>/` in the repo | series folder outside every CLAUDE.md, `series new <folder> --instruction digests/<slug>.md --source manifestos/<slug>.md` |
| `write-eval-spec` skill, `spec.json` | `list-demands`, `write-tasks`, `freeze-series`; parts 2-7, `8-frozen.yaml` |
| `write-eval-tasks`, `tasks.json`, `family` | `write-tasks`, `3-tasks.yaml`, `tempts` |
| `calibrate-eval-judge` | `calibrate-judge` |
| `pilot-1`, `digest-eval reps` | retest `r1`; repeats set at freeze |
| `digest-eval conditions … cut-<n>` | `reader prepare r<n>` |
| `digest-eval run <slug> cut-<n> --only digest` | `revision ask r<n> --conditions instruction`, then `revision collect r<n>` |
| `judge-by-agents`; `blind`, `brief`, `collect`, `script-judge` | `judge-replies`; `revision blind`, `judge prepare`, `judge collect`, `revision detect` |
| `digest-eval score … --previous`, `gate` | `revision score r<n>`, `revision gate r<n>` (parent read from `2-revision.yaml`) |
| `write-eval-record`, `ledger.jsonl` | the CLI writes every record; `series status` |
| `diagnose-eval-failures` | `diagnose` (cause list to the writers) |
| `recut-digest` save-the-cut, `cut.json` | `revise`, `revision new`, `2-revision.yaml` |
| conditions `none`, `digest`, `full`, `terse`, `ablation-NN` | `empty`, `instruction`, `source`, `aim`, `omit-<n>` |
| split `dev`, `test` | `open`, `sealed` |
| canonical cut by owner after the numbers | `series keep` by the frozen keep rule |
| `tests/check_skills.py` | retired (R53) |

Finished JSON series stay as they are (R52).

## Owner decisions

1. **Split names.** The halves of the tasks are named by who may read them: `open` (diagnosis reads it) and `sealed` (only the gate reads it). Recommend `open`/`sealed`. Alternatives: `dev`/`test` (ML-familiar, hides the rule); `diagnosis`/`gate` (literal, awkward in prose).
2. **Version word.** Each numbered version of the instruction is a "revision", `r1`, `r2`, made by `revise`. Recommend "revision". Alternatives: keep "cut" (familiar to the LLM_MANIFESTOS sessions, reads as "remove" to a newcomer); "draft" (implies unfinished).
3. **No ledger file.** Every revision folder already holds its hashes, numbers, and outcome; `instruction-eval series status` prints the history from them, so no second copy can drift. Recommend no ledger. Alternative: keep an append-only `ledger.yaml` as a tamper-evident history, at the cost of two sources of truth.
4. **Neutral login.** Agent readers need a login with no CLAUDE.md (your 2026-10-14 ruling). Recommend a dedicated `CLAUDE_CONFIG_DIR=~/.claude-neutral` with only this marketplace installed, documented in the README and checked by the CLI. Alternative: reuse an existing spare login (fewer installs, more risk of a stray CLAUDE.md or `.manifestos.yaml`).
5. **Where series folders live.** They must sit outside every CLAUDE.md, so not inside your repos. Recommend a fixed root, `~/instruction-series/<name>/`, that `series new` uses when given a bare name. Alternative: always require a full path (no default; more typing, no hidden convention).

Settled without the owner, from rulings and facts: YAML only; `manifesto` dependency; uv launcher; one agent definition per condition and per packet; text-only agent readers; anchors in every packet; `unresolvable` stop; keep rule required at freeze; borrowed control replies re-judged with each revision.

## Summary

The design derives every name from atoms traced to the owner's rulings, the source process, and measured platform facts, renaming each word that collides with `claude plugin eval`, dev-cycle, peers, memento, or Claude Code itself (spec, run, cut, ablation, session, key). Eleven verb-object skills, an object-grouped CLI whose help prints the order of work, and number-prefixed series folders let a newcomer read the process and a series' position from names alone. Five owner decisions remain: the split names, "revision" over "cut", dropping the ledger, the neutral login, and the series root.
