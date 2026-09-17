# Session 2026-09-16

Continues 2026-09-15 without a break. That record covers the skill-writing stance, the foreign comparison, the standing governance record, and the memento design. This one covers the plugin's construction.

## Phase 1 — The tool

`skill-creation` ran twelve adversarial rounds: an author, a reader given the file and nothing else, and an auditor extracting the file's own rules then checking the file against them. 949 tokens to 718.

Reader-side defects 6, 6, 3, 4, 2, 2, 2, 1, 1. Audit-side 5, 3, 4, 3, 6, 0, 2, 3, 3, 3, 2.

Every round that cut a rule moved the numbers. Every round that added a qualifier did not. Three rules were deleted whole rather than repaired: one that classified where a skill came from and never acted on the answer, one splitting lines into two kinds nobody could sort, and one demanding a list of steps with no way to build it.

The location rule failed six times under six wordings and was ruled permanent residue. Naming a root makes a claim the stating file breaks; naming none leaves the reader to choose. The reader's pass condition was retired with it, leaving the auditor to decide the loop.

Shipped at the cap as `2aa0f74`.

## Phase 2 — The plan

A fable planner sliced the design into skills, hooks, a configuration format, and a maintainer layer. Three check rounds: one agent rebuilding the design's inventory independently and reporting what no slice carried, one reading the plan alone and reporting what two slices both claimed.

Coverage 3, 4, 2. Cohesion 7, 11, 3.

Every defect lived in prose carrying no item number. The plan's own check matched numbers and could not see restated substance; it was demoted beneath a prose-carriage audit that counts shipped file comments and templates as slice text. Two claimed strips were found still live in the file.

Settled at the cap as `e029c90`.

## Phase 3 — Rulings sourced

Four configuration contradictions between the design and the owner's requirement went to the owner and came back settled: a built-in schema ships and a project config replaces it whole; harness-supplied content inherits owner authority for schemas; exactly one schema is ever in force; and the config simply supplies the schema, so nothing is renamed. Committed as `6870cf1`.

The owner then withdrew with full autonomy granted and no further escalations.

## Phase 4 — Ten skills

Ten authors dispatched concurrently, each bound to the shipped tool and following it literally, each writing one slice.

schema-resolution 637, event-capture 689, staging-relay 695, owner-ruling 701, span-closure 721, record-writing 1047, corpus-reconciliation 1136, pat-down 1283, record-promotion 1288, authority-check 1755.

All ten passed the forbidden-pattern gate. Four showed a single grep hit each, all false positives on inspection — two quoted trigger phrases, one temporal word, one clause describing an expected state.

## In flight

Nineteen of twenty round-one checkers, two per skill: one reading the skill against the tool, one reading the skill alone and following it. The twentieth was refused by the twenty-agent ceiling and is queued.

Each skill loops at most four rounds, then ships with residue.

## Direction

When all ten end: regenerate READMEs, one commit, then the maintainer layer the plan specifies — the design document already in place unreferenced, a map from each skill to the parts of the design it covers, the checker briefs kept as reusable tooling, and a note on re-running them after any change.

Hooks remain undrafted. The plan specifies two, reading the schema at session start and at compaction, silent when unconfigured.

## Failures

`failures.md` for 2026-09-15 carries the three orchestration failures, all from the liveness problem: a check run against a symlink, a working agent killed on two zero-delta size samples, and a deprecated call that flooded orchestrator context. The lesson that generalized: transcript size answers whether a process lives, never whether an agent works.

A session limit killed two agents mid-task at 16:30. Both had bound and neither had written. Restarted without loss.

A second limit at 17:55 killed nine at once: six authors mid-revision, three checkers mid-check. Several had already triaged their findings and announced what they would cut before dying, so their reasoning survives in the notifications and none of it needs re-deriving. Nothing was written and nothing was lost.

## Round one, all ten skills

Compliance then usability: authority-check 10/4, staging-relay 5/12, span-closure 3/8, pat-down 5/6, record-writing 6/7, schema-resolution 4/4, owner-ruling 3/—, corpus-reconciliation —/6, event-capture —/3, record-promotion —/3.

Two filters were ruled before any finding reached an author, and both are recorded in `decisions.md`. A sibling named by name is never a defect — the usability checkers read one skill alone and report every cross-skill reference as a hole, which would have driven authors to inline the very content the extraction ruling exists to separate. And a term another slice owns takes a gloss just sufficient to parse its sentence, settling a conflict the plan and the standard never reconciled.

After filtering, the real defects are all internal and mostly one shape: a term used before it is defined, or a second name arriving for something already named. `working text` alone was flagged by four checkers across three skills.

Six authors were briefed and revising when the limit hit: authority-check, staging-relay, span-closure, pat-down, record-writing, schema-resolution. Four skills still need briefing once their pairs complete.

## Round one closed, round two running

All ten authors revised. Sizes after: schema-resolution 687, event-capture 719, owner-ruling 739, staging-relay 742, record-writing 919, span-closure 771, corpus-reconciliation 1267, pat-down 1301, record-promotion 1336, authority-check 1656. Only record-writing shrank, deleting two value vocabularies rather than supplying the mapping between them, on the reasoning that the tier is derived from the home and never chosen — so naming the tiers invited the very choice the skill forbids elsewhere.

Round two is running on all ten. Usability improved nearly everywhere: authority-check 4 to 1, staging-relay 12 to 6, span-closure 8 to 6, record-writing 7 to 5, pat-down 6 to 5. schema-resolution held at 4 with different findings. Compliance so far: span-closure 2, schema-resolution 3, staging-relay 5, authority-check 17 raw and 4 after filtering.

Two skills show round two finding a fresh layer rather than the same one — the surface defects closed and what sat beneath them surfaced. That is the loop working rather than stalling.

## Three filters, and a lesson about where a ruling belongs

Three rulings now stand between raw findings and authors, each forced by evidence rather than taste, all recorded in `decisions.md`. A sibling named by name is never a defect. A term another slice owns takes a parse-sufficient gloss and no more. An enumeration that defines its items immediately is compliant.

The third arrived the expensive way. One skill's compliance count rose from ten to seventeen while the file improved on every other measure, because a checker read define-at-first-use hyper-literally and flagged five enumerated names as undefined at their enumeration. Filtering that after the fact wastes the checker. The later compliance checkers carry the rulings inline in their own prompts, and their counts came back materially cleaner — which is the same move the authors keep making on their own files: fix the cause, not the symptom.

## The authors pushed back, correctly

Twice they refused an instruction and were right. schema-resolution rejected a deletion that would have broken its coverage, diagnosing the real fault as a missing consumer and naming one. record-promotion conceded half a challenge and defended the other half, rewriting the line so the distinction showed in the text rather than only in its reasoning — retirement is not an upward move and left the gate; an amended goal is new content nominated and superseding, so it stayed.

## Blocked and carried

The plan's reference graph is stale in three places. authority-check names corpus-reconciliation; record-writing names authority-check and record-promotion; schema-resolution names event-capture and record-promotion. Every edge is legitimate under the sibling filter and none was in the graph the plan recorded before drafting. The as-built graph belongs in the coverage file when the maintainer layer is written.

Hooks remain undrafted. The plan specifies two, reading the schema at session start and at compaction, silent when unconfigured.

## Rounds two through four

All ten skills ran to the four-round cap or ended earlier at zero filtered findings. Final sizes: authority-check 1691, record-promotion 1377, pat-down 1329, corpus-reconciliation 1278, record-writing 962, schema-resolution 838, owner-ruling 836, span-closure 817, staging-relay 744, event-capture 713. Shipped as `951123f`, memento 0.2.0.

Three skills reached a clean compliance pass: record-writing twice, corpus-reconciliation twice, record-promotion once.

The loop's one measurable effect was the tag-name test. An author running it across every tag found roughly four faults its checker had reported one of, and every rename cost zero or negative tokens. Six authors replicated it. The rule then sharpened twice under evidence — first that a tag verb failing to recur is a fault only against a new synonym, not against a term the skill already owns, and then that the sweep needs commanding rather than a particular executor, after a checker told to test all tags returned five where four earlier checkers had each returned one. Both corrections are in `decisions.md`. The sharpened form paid immediately: pat-down's checker flagged all eight of its tags and six of those flags did not survive it.

## What the authors refused

Six authors refused an instruction and were right each time. record-writing rejected both branches offered for where a status is stored and proved from its own quarantine and supersession rules that storage was impossible, rewriting the section around reading status from facts already recorded. record-promotion refused four of five flagged tag faults, one on the ground that the governing standard's own `<settle-the-skill>` has the identical shape the checker called a fault. schema-resolution refused to path `this plugin`, on the ground that any path would be wrong at most installs and the standard bars pathing to internal units. pat-down settled a disagreement between its two checkers from the text, noting that both sentences neighbouring the disputed one supply a locating mechanism where the disputed one supplies none.

The pattern holds across all six: a refusal carrying a diagnosis beat a compliant edit every time it appeared.

## What single-file checking could not see

Three defects spanned slices, and no checker reading one skill against the standard could reach any of them.

corpus-reconciliation set a quarantined status on a record bearing a mark, while record-writing — already shipped clean twice — derived quarantine from a missing mark alone and would have read that record as live. Repairing it exposed three more grounds of the same shape, including one in record-promotion that nobody had reported. One agent holding both files enumerated every way any slice puts content out of force and found the atom: status derives from a disposition, never from a diagnosis, and the audit's dispositions left no record where owner-ruling's rulings already carried a link back. Two sentences closed it.

schema-resolution's final pass redefined a pointer as content rather than as a record, contradicting the owning slice and three others that had borrowed the owning definition. The ontology settles it four ways. One clause restored it.

Both were found by asking whether a repair had created a disagreement, not by any scheduled check. Nothing in the loop looks for them.

## Failures

Five, all in `failures.md`. Two session limits killed thirteen and then two agents mid-flight; the thirteen-agent restart took one turn because every dispatch prompt was reconstructible from the orchestrator's notes. Three checkers hit the 64,000-token output ceiling and two died there, all three inside the compliance brief's extraction phase — which is the brief's design, not the agents', and the fix is recorded.

One liveness lesson inverted. A checker ran three hours against a thirty-minute ceiling and died generating; its transcript grew the whole time. Growth was the symptom, not the sign of health. What distinguishes a doomed agent from a slow one is elapsed time against the observed distribution for that task type. The recovery was to race a replacement on a separate output path rather than kill on suspicion, which costs one agent and risks nothing.

## Rulings

Fourteen reached `decisions.md` across this session: the enumeration and tag-name filters, where a ruling belongs, zero filtered rather than zero raw as the end condition, case depth as a precondition for reading a low count, the sharpened tag rule and its amendment, the cap covering gaps but not contradictions, the cap bounding passes rather than what a warranted pass may close, corpus vocabulary as a plugin-level class, cross-slice contradictions reopening a shipped skill, status deriving from a disposition, and the three out-of-force grounds deferred to the owner.

## Left for the owner

Whether a routine's standing is a separate axis from a record's status. Until that is settled, content quarantined on three grounds reads as live: behaviors from unratified and online channels, whose supply channel no rule records, and peer records ended by irrelevance, which names no actor.

`memento/config/default.yaml` does not exist. `schema-resolution` resolves to it correctly and the ontology never defines it, so the plugin is incomplete until it is authored.

Hooks remain undrafted. The plan specifies two, reading the schema at session start and at compaction, silent when unconfigured.

## Two gaps the maintainer layer surfaced

pat-down and schema-resolution shipped on edits made after their last audits, so no independent reader had seen their final text. Ground truth requires a change to land only after an agent that did not produce it verifies it, and both were self-verified only. Checks were dispatched against the committed text; whatever they return is residue, recorded in `memento/maintainers/coverage.md`.

The as-built reference graph is cyclic and no shipped skill is a leaf. The plan recorded an acyclic graph with schema-resolution and authority-check as leaves, and derived its wave ordering from that shape. Seven pairs now name each other. The ordering no longer follows from the graph, and any future wave plan must be rebuilt from the as-built edges rather than the plan's.
