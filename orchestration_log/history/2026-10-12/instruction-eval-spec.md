# instruction-eval: specification

## Binding

Loaded whole from source before any requirement:

| Element | Source | Read |
|---|---|---|
| Binding order | `recon/2026-10-12/prompts/binding.md` | 8 lines |
| first-principles 1.0.1 | `/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/first-principles.md` | 115 lines |
| Strunk SPR v3.0 | `curl` of `.../LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml` | 2923 lines, sections 1-10, closing directive |
| self-documenting-code 1.0.0 | `.../manifestos/self-documenting-code.md` | whole |
| simple-made-easy 2.0.0 | `.../manifestos/simple-made-easy.md` | whole |
| correct-by-construction 1.0.0 | `.../manifestos/correct-by-construction.md` | whole |
| Oath protocol 3.2.0 | `/Users/ryzhakar/.claude/plugins/cache/my-claude-skills/manifesto/3.2.0/skills/manifesto-oath/SKILL.md` | 126 lines (also injected by SubagentStart) |

Transitive closure: every path explicit; no element names a further loadable document; depth 1; no truncation.

Axioms:

| Element | Irreducible demands |
|---|---|
| first-principles | Keep only verified atoms; a name is not a derivation; rebuild from atoms. |
| Strunk | Clarity > accuracy > economy > vigor > correctness; concrete, positive, parallel; one term per concept in technical text. |
| self-documenting-code | Names teach the domain; structure mirrors the expert's process; no "and" names, no boolean traps. |
| simple-made-easy | Simple is unbraided; one fact, one home; data as plain values; more straight parts over fewer knotted ones. |
| correct-by-construction | Invalid states unrepresentable; closed variants over flags; explicit over implicit; refuse at construction time. |

Convergence: (1) every requirement traces to an atom and carries a check that fails it (first-principles, correct-by-construction); (2) one term per concept, taken from design-language.md unchanged (Strunk, self-documenting-code); (3) one fact, one home: a value stored twice is a braid and an invalid state (simple-made-easy, correct-by-construction).

Tensions and rules:

| Tension | Rule |
|---|---|
| correct-by-construction "unrepresentable" vs design-language keys that store derivable facts (`sentences`, `controls`, `noise`) | Keep the design's keys; make disagreement a load-time refusal; flag removal under Open. Never rename. |
| first-principles "kill the playbook" vs the source process (digest-eval) | Keep a source rule only where a line, ruling, or measurement backs it; cite it. |
| Strunk economy vs "every requirement gated" | A requirement grows to its gate and basis, never further. |
| simple-made-easy "one author per file" vs design files written by user and CLI together | Each key names its single author; the CLI refuses a key written by the other. |

Commitments:
- I must trace each requirement to a ruling, a source line, or a measured fact, and I will cite it in brackets beside the gate.
- I must give each requirement a check that can fail it, and I will write the gate as a test, a refusal, or a probe.
- I must use design-language.md's terms unchanged, and I will flag a wanting name under Open instead of renaming it.
- I must make invalid states unrepresentable, and I will specify closed enums, closed variants, and load-time refusals.
- I must not store one fact twice, and I will name the single author and home of every key.
- I must write active, positive, concrete prose in tables, and I will cut every needless word.
- I must not write code, skill text, or any file but this one, and I will specify only.

Basis codes: `J<n>` journal line in `history/2026-10-12/events.md`; `S:<skill> L<n>` source skill at LLM_MANIFESTOS `3148d45`; `S:<file>.py L<n>` source tool; `P<n>` Petro feedback item (`66b5c89`); `M` main-thread measurement 2026-10-14 (J105-J106); `F:<file> §<n>` recon facts; `DL` design-language.md; `C` coordinator message 2026-10-14 relaying `claudes` steward claims on the manual login (unverified); `C2` its follow-up: `claudes new --bare` shipped (unverified: `/login`, a full reader run); `H` manifesto 3.2.0 hook source, read 2026-10-14. `K` coordinator message 2026-10-14 relaying owner settlements (re-judge cap, keep-rule guard). `d<n>` defect in `recon/2026-10-12/spec-check.yaml`; `r2 c<n>` defect in `spec-check-r2.yaml`.

## Scope

| In | Out |
|---|---|
| The `instruction-eval` plugin: eleven skills, the CLI, templates, tests, packaging (J17, J38, DL) | Writer craft: phrasing a demand, naming a cause (J36) |
| Instructions of every kind, with or without a source (J17) | Tool-using readers; they wait for a sandboxed v2 (J93) |
| Agent readers (text-only) and every judge, launched from the neutral session; command readers for non-Claude models (J41, J55, J85, J93) | `claude plugin eval` integration (F:plugin-eval §1) |
| YAML records only, new series only (J42, J52) | Migrating finished JSON series (J52) |
| Requirements on the neutral login; its setup through `claudes new --bare` | Building or changing `claudes` (steward's territory, J111) |
| Migration of the LLM_MANIFESTOS sessions | Hooks: the plugin ships none (DL Packaging) |

Every series runs its driver in the neutral session: judges are generated agents for every reader kind, and generated agents register only in the main thread (M). Retired requirement numbers stay retired; new ones take the next free number inside their group.

## Requirements

Format: `R<n>. requirement — gate: check [basis]`.

### Data flow

- R124. Every file inside the series folder has one author: one CLI command, the user, or one judge agent; `9-stop.yaml` is written once by whichever command stops the series. A CLI command writes each of its files whole, once, and refuses when the file exists; a judge or rater writes one file; the user drafts a user file freely until a CLI record consumes it. Files outside the series folder (the live instruction, the original sources, the placebo source, transcripts) are outside this rule — gate: walk test asserts every CLI write inside the series targets an absent path [simple-made-easy; r2 c1, c2; r3 d2]
- R125. No command writes a file after a hash covers it, and no hash names a file outside the series folder: `8-frozen.yaml` hashes only series files present at freeze, files written after freeze are new paths, and each external file enters the series through one snapshot (R129) — gate: walk test through r5 and `series keep` re-hashes every frozen and every `inputs` path after the last command [r2 c2; r3 d1]
- R115. Every YAML record the CLI writes carries `inputs`: a map from each series file it read to a sha256; a file outside the series folder is never an `inputs` key. For a user-written YAML file the entry is per top-level key read, `<path>#<key>`, hashing that key's value dumped as canonical YAML (sorted keys, block style); every other entry hashes the whole file. Every load of a CLI record re-hashes its `inputs` and refuses on mismatch with `stale: <record> (input <path> changed)`, or on an absent input with `missing input: <path>`; a stale record is never rewritten, so a changed input after consumption starts a new series — gate: test edits a consumed key, an unconsumed key of `7-gate.yaml`, and deletes an input; for every command that writes a YAML record, a test asserts its `inputs` keys equal its Commands-table Reads cell expanded for the revision at hand, and that no External file appears [d23; d37; r2 c1, c9; r3 d1, d9, d17; r4 d3]
- R126. Markdown outputs carry no `inputs`: condition files and generated agent definitions are recomputed from their inputs and compared byte for byte by every command that uses them (R127); packets are hashed in `6-origins.yaml` `packets` — gate: test edits each kind and runs its consumer [r2 c9, c13]
- R129. External files enter the series once each: the live instruction as `r<n>/2-instruction.md` (`series new` for r1, `revision new` after); the sources as `1-source/` (`series new`); the placebo source as `4-placebo-source.md` (`reader prepare r1`, raw bytes); the working brief `6-judge/brief.md` as `6-judge/calibration/attempt-<n>/brief.md` (stage one); a transcript as the `transcript_hash` of the record that reads it. Every later read and hash names the snapshot; the live instruction, the placebo source, and the working brief are working copies, never hashed — gate: walk test edits each external file after its snapshot and asserts no refusal [r3 d1, d3, d17; r4 d1, d2]
- R130. The expected reply set E(r) is a function of `3-tasks.yaml`, `4-conditions.yaml`, `7-gate.yaml` `repeats`, and r alone. E(r1): for `instruction` and every control, every task × repeats 1..`repeats` and every conversation turn × repeats; for every `omit-<n>` of r1, every open task × repeats. E(r > 1): the same for `instruction` and r's `omit-<n>`; controls are borrowed from E(r1). `--conditions` limits what one `revision ask` invocation asks; `revision collect`, `revision blind`, `series freeze`, and `revision gate` refuse with `missing replies: <count>, first <path>` on any gap against E(r) — gate: test asks a subset of conditions, then collects [r4 d13]

### Commands

Every command runs in the series folder except `series new`. `<r>` is a revision id `r<n>`; `<p>` is a repeat number. No command takes a flag without a value.

Reads lists the series files a command reads; for a command that writes a YAML record they are exactly its `inputs` (R115). External lists what it reads from outside the series; it is never hashed. "(r > 1)" marks reads only later revisions make. Multi-valued flags repeat: `--source a --source b`, `--conditions instruction --conditions omit-3` (R106).

| Command | Reads | External | Writes (once) | Skill |
|---|---|---|---|---|
| `series new <name\|path> --instruction <path> [--source <path>]… --reader-kind agent\|command` | none | the instruction and source files (snapshotted) | `series.yaml`, `.claude/agents/`, `1-source/`, `r1/2-instruction.md`, `r1/2-revision.yaml` | `start-series` |
| `series status` | every series file present | none | nothing (prints) | `freeze-series`, `measure-revision` |
| `series freeze` | `series.yaml`, `1-source/*`, `2-demands.yaml`, `3-tasks.yaml`, `4-conditions.yaml`, `4-placebo-source.md`, `5-reader.yaml`, `6-judge/calibration.yaml`, `6-judge/anchors.yaml`, `6-judge/calibration/**`, `7-gate.yaml`, `r1/**` | fingerprint output (command kind) | `8-frozen.yaml` | `freeze-series` |
| `series stop --reason <text>` | `7-gate.yaml#keep_rule`, `8-frozen.yaml`, every `r<n>/9-outcome.yaml` | none | `9-stop.yaml` | `diagnose` |
| `series keep` | `series.yaml`, `9-stop.yaml`, `r<kept>/2-instruction.md` | none | the live instruction file (external) | `keep-revision` |
| `demands check` | `2-demands.yaml` | none | nothing | `list-demands` |
| `coverage check <r>` | `2-demands.yaml`, `<r>/2-instruction.md`, `<r>/3-coverage.yaml`, `r1/3-coverage.yaml` | none | nothing | `check-coverage`, `revise` |
| `tasks check` | `2-demands.yaml`, `3-tasks.yaml`, `4-conditions.yaml`, `1-source/*`, every `r<n>/2-instruction.md`, `4-placebo-source.md` when present | the placebo source while `4-placebo-source.md` is absent | nothing | `write-tasks` |
| `reader fingerprint` | `5-reader.yaml` | fingerprint output | nothing (prints) | `freeze-series` |
| `reader prepare <r>` | `series.yaml`, `1-source/*`, `4-conditions.yaml`, `5-reader.yaml`, `<r>/2-instruction.md`, `4-placebo-source.md`; (r > 1) `r1/4-conditions/*.md` | r1: the placebo source (snapshotted first) | r1: `4-placebo-source.md`; `<r>/4-conditions/*.md`; agent kind: reader definitions | `freeze-series`, `measure-revision` |
| `revision ask <r> [--conditions <name>]…` | `series.yaml`, `1-source/*`, `2-demands.yaml`, `3-tasks.yaml`, `4-conditions.yaml`, `4-placebo-source.md`, `5-reader.yaml`, `7-gate.yaml#repeats`, `<r>/2-instruction.md`, `<r>/3-coverage.yaml`, `r1/3-coverage.yaml`, `<r>/4-conditions/*.md`, agent kind: `.claude/agents/ie-reader-<r>-*.md`; command kind before freeze: `r1/5-replies/**` written so far; after freeze: `8-frozen.yaml`; (r > 1) `7-gate.yaml#budget`, `r1/4-conditions/*.md`, every earlier `r<n>/9-outcome.yaml` | command kind: the reader process and fingerprint output | command kind: missing `<r>/5-replies/**`; agent kind: prints the launch list | `freeze-series`, `measure-revision` |
| `revision collect <r>` | `series.yaml`, `1-source/*`, `3-tasks.yaml`, `4-conditions.yaml`, `4-placebo-source.md`, `5-reader.yaml`, `7-gate.yaml#repeats`, `<r>/2-instruction.md`, `<r>/4-conditions/*.md`, `.claude/agents/ie-reader-<r>-*.md` | transcripts (hashed into replies) | agent kind: missing `<r>/5-replies/**`; command kind: nothing | `freeze-series`, `measure-revision` |
| `judge calibrate` | stage one: `series.yaml`, `1-source/*`, `2-demands.yaml`, `attempt-<n>/plan.yaml`, `attempt-<n>/brief.md` once written, every earlier `attempt-*/origins.yaml`, the sampled `r1/5-replies/**` files; stage two: the same plus `attempt-<n>/{sample.md, origins.yaml}`, the rating files, `.claude/agents/ie-calib-<n>-*.md`, `3-tasks.yaml` | stage one: `6-judge/brief.md` (snapshotted); stage two: rating transcripts | stage one: `attempt-<n>/brief.md`, `sample.md`, `origins.yaml`, rating definitions; stage two: `attempt-<n>/agreement.yaml`, and on acceptance `6-judge/calibration.yaml`, `6-judge/anchors.yaml` | `calibrate-judge` |
| `revision blind <r>` | `3-tasks.yaml`, `4-conditions.yaml`, `7-gate.yaml#repeats`, `<r>/5-replies/**`, `6-judge/calibration.yaml`, `6-judge/anchors.yaml`; (r > 1) `r1/5-replies/**` | none | `<r>/6-packets/*.md`, `<r>/6-origins.yaml` | `freeze-series`, `measure-revision` |
| `judge prepare <r>` | `series.yaml`, `1-source/*`, `2-demands.yaml`, `6-judge/calibration.yaml`, accepted `attempt-<n>/brief.md`, `6-judge/anchors.yaml`, `<r>/6-packets/*.md`, `<r>/6-origins.yaml`, `<r>/7-verdicts/**`, `.claude/agents/ie-judge-<r>-*.md` | judge transcripts | judge definitions; prints the launch list | `judge-replies` |
| `judge collect <r>` | as `judge prepare` | judge transcripts | `<r>/7-collected.yaml` when every packet is accepted | `judge-replies` |
| `revision detect <r>` | `2-demands.yaml`, `3-tasks.yaml`, `<r>/5-replies/**`, `<r>/6-origins.yaml`; (r > 1) `r1/5-replies/**` | none | `<r>/7-detectors.yaml` | `freeze-series`, `measure-revision` |
| `revision score <r>` | `2-demands.yaml`, `3-tasks.yaml`, `r1/3-coverage.yaml`, `7-gate.yaml#level`, `7-gate.yaml#done_by`, `<r>/5-replies/**`, `<r>/6-origins.yaml`, `<r>/7-verdicts/**`, `<r>/7-collected.yaml`, `<r>/7-detectors.yaml`; (r > 1) `r1/5-replies/**` | none | `<r>/8-scores.yaml` | `measure-revision` |
| `revision gate <r>` | `revision score`'s reads plus `7-gate.yaml` (every key), `8-frozen.yaml`, `<r>/2-instruction.md`, every earlier `r<n>/9-outcome.yaml`; (r > 1) `<r>/1-hypothesis.yaml` and the parent's `5-replies/**`, `6-origins.yaml`, `7-verdicts/**`, `7-collected.yaml`, `7-detectors.yaml` | none | `<r>/9-outcome.yaml`; `9-stop.yaml` when a stop applies | `measure-revision` |
| `revision new` | `2-demands.yaml`, `3-tasks.yaml`, `4-conditions.yaml`, `r1/3-coverage.yaml`, `r1/4-conditions/placebo.md`, `8-frozen.yaml`, `r<n+1>/1-hypothesis.yaml`, and the parent's `2-instruction.md`, `2-revision.yaml`, `6-origins.yaml`, `7-verdicts/**`, `7-collected.yaml`, `7-detectors.yaml`, `9-outcome.yaml` | the live instruction (snapshotted) | `r<n+1>/2-instruction.md`, `r<n+1>/2-revision.yaml` | `revise` |

Order of work (help text):
1. in any shell: `series new`; then start the neutral session there: `cd <series folder> && claudes run readers`; every later step runs in that session
2. user writes `2-demands.yaml`; `demands check`
3. user writes `r1/3-coverage.yaml`; `coverage check r1`
4. user writes `4-conditions.yaml`, `5-reader.yaml`, and `7-gate.yaml` `repeats`, `level`, `done_by`
5. user writes `3-tasks.yaml`; `tasks check`
6. `reader fingerprint` (command kind); `reader prepare r1`; `revision ask r1`; agents launched; `revision collect r1`
7. user writes `6-judge/brief.md` and `6-judge/calibration/attempt-1/plan.yaml`; `judge calibrate` (snapshots the brief); ratings; `judge calibrate`; on rejection, the user edits the brief, writes `attempt-<n+1>/plan.yaml`, and repeats
8. `revision blind r1`; `judge prepare r1`; judges; `judge collect r1`; `revision detect r1`
9. `series status` prints the noise; user completes `7-gate.yaml`; `series freeze`
10. `revision score r1`; `revision gate r1`. `series status` is available at any step
11. on `fail`: user writes `r2/1-hypothesis.yaml`; writer edits the instruction; `revision new`; user writes `r2/3-coverage.yaml`; `coverage check r2`; `reader prepare r2`; `revision ask r2 --conditions instruction …`; `revision collect r2`; `revision blind r2`; `judge prepare r2`; `judge collect r2`; `revision detect r2`; `revision score r2`; `revision gate r2`
12. at a stop: `series keep` writes the kept snapshot to the live instruction path

### Series

- R1. `series new` takes a bare name to `~/instruction-series/<name>/` and a value holding `/` as given; relative `--instruction`, `--source`, and folder paths resolve against the working directory — gate: test on both forms and a relative path [J110, J111; r2 c31]
- R2. `series new` refuses an existing non-empty folder; it runs before the neutral session starts, in any shell, so no session has written into the folder — gate: test [DL Series folder; r4 d15]
- R3. `series new` refuses a folder when it or any ancestor up to `/` holds `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, or `.manifestos.yaml`, except `$HOME/.claude/CLAUDE.md` (the default login's user memory, which the neutral login does not load; PR4 verifies); every reader kind — gate: test per file name at depth 0, depth 3, `$HOME`, and a folder outside `$HOME` [J85; DL Packaging; d5; d7; r2 c31]
- R4. `series new` refuses a folder inside a git work tree, for every reader kind — gate: test [F:agent-reader §2 "git status snapshot"; d5]
- R5. `series new` writes `series.yaml` (`inputs: {}`), `.claude/agents/` (empty), `1-source/<basename>` byte copies, `r1/2-instruction.md` (the live instruction's bytes), `r1/2-revision.yaml`; nothing else. It refuses two sources sharing a basename (`duplicate source basename: <name>`) and an instruction or source whose first line is `---` with no later line exactly `---` (`unclosed frontmatter: <path>`); `revision new` refuses such an instruction the same way — gate: test lists the tree; one test per refusal [DL; d3; r2 c30; r3 d25; r4 d28]
- R6. Every command but `series new` refuses a working directory lacking `series.yaml` — gate: test [DL CLI]
- R7. `series status` prints parts present, frozen or not, each revision's outcome, `changed_from_parent`, and keep ranks, cost so far against `budget`, calibration attempts and scale, packets awaiting judging, r1's noise (R73) and the least repeats per check that has a gap, and the stop; it writes nothing — gate: test asserts unchanged tree hash [DL; J111; r2 c24]
- R8. Every record loads through one typed loader that resolves every reference and refuses an unresolved one, and refuses `5-reader.yaml` `kind` or any reply's `reader_kind` differing from `series.yaml` `reader_kind` — gate: test per reference kind and per mismatch [J42; DL Records; d44]
- R9. After freeze, every command re-hashes each path in `8-frozen.yaml` and refuses on any byte change; a change starts a new series — gate: test edits each part [S:write-eval-spec L44-45; J84(11)]
- R116. `series freeze` refuses on: an incomplete `7-gate.yaml`; `demands check` or `tasks check` failing; a missing record among 2-6; `r1/3-coverage.yaml` failing `coverage check`; no `6-judge/calibration.yaml`; a gap against E(r1) (R130), or r1 not collected, blinded, judged (`r1/7-collected.yaml` present), or detected; any stale r1 record (R115); a command reader whose fresh fingerprint hash differs from any r1 reply's; an unresolvable gap (R82); a check whose noise is null, or a null `noise.demands[d]` for any gate demand or null `noise.done_change` (R73); a missing keep rule (R84); a budget overrun (R85); a `drift` check without conversations (R22); `instruction-near-source` with empty `sources` (R81) — gate: one test per refusal [d22; d23; d24; d35; r2 c36; r3 d18, d21; r4 d13, d16, d19]
- R117. `7-gate.yaml` is user-written at step 4 (`repeats`, `level`, `done_by`) and completed at step 9. Key-level reads (R115): `revision ask` and `revision collect` read `repeats` (ask also `budget` for r > 1); `revision blind` reads `repeats`; `revision score` reads `level` and `done_by`; `series freeze`, `revision gate`, and `series status` read every key present; `series freeze` and every command after it refuse an absent key — gate: test edits `checks` after the r1 ask and freezes [d21; r2 c1, c5; r3 d10; r4 d21]

### Demands

- R10. `2-demands.yaml` lists every demand the source makes, or with no source the instruction, one per entry, restatements collapsed, boundary folded in; completeness is the user's attestation through `list-demands` — gate: `demands check` refuses an empty `boundary` and a duplicate `id` [S:write-digest L12-13, L31; J36; r2 c14]
- R11. `counted_by: pattern` carries `pattern` and no `limit`; `long-sentences` carries `limit` (integer > 0) and no `pattern`; `judge` carries neither. Every regex in the series (`pattern`, `answer_key`) is Python `re` syntax, compiled with no flags. `demands check` refuses the ids `overreach` and `completion`, which name task and hypothesis targets — gate: test per invalid variant and reserved id [S:write-eval-spec L12-14; r2 c33; r3 d23]
- R12. A detector reads reply text with fenced code blocks removed: `pattern` counts the non-overlapping matches `re.finditer` yields; `long-sentences` splits sentences by R14 and counts those whose word count (R21) exceeds `limit` — gate: fixture test [S:write-eval-spec L12; d39; r2 c33]
- R13. Gate demands are the demands not dropped in `r1/3-coverage.yaml`, fixed for the series. Breaches per reply, noise, drift, and every check sum gate demands for every condition; dropped demands are measured and reported apart. `noise.demands` ranges over gate demands; `failing_demand` is a gate demand or `completion` — gate: test with a dropped demand [J84(12); r2 c6, c25; r3 d14]

### Coverage

- R14. Sentences are numbered from 1 over markdown units, each sentence a byte span. Units: a leading `---` frontmatter block; a fenced code block; a heading line (`#`); a table row line (`|`); a blockquote line (`>`); a horizontal rule; each of these is one sentence spanning the whole lines. A list item (its text after the marker, continuation lines included; a nested item is its own item) and a paragraph (consecutive non-blank lines of no other unit) split into sentences: a sentence ends after `.`, `!`, or `?` plus any run of `\"')]` followed by whitespace or the unit's end, unless the word before the terminator is one of `e.g`, `i.e`, `etc`, `vs`, `cf`, `Mr`, `Mrs`, `Dr`, `St`, `No` or a single letter; the unit's end closes its last sentence. A span runs from the sentence's first non-space byte to its terminator run; list markers are outside spans — gate: one fixture per unit kind, closer run, abbreviation, and nesting [S:recut-digest L12-13; DL coverage; d39; r3 d7]
- R15. `<r>/3-coverage.yaml` maps each demand to a non-empty list of sentence numbers or to `{dropped: reason}`, and each sentence to a non-empty list of demand ids. `coverage check <r>` refuses an unmapped demand, an empty list, a number outside the text, and a sentence absent from `sentences`, with the message `sentence <n> carries no demand (imported)`; `imported` is that message's word, never a stored value — gate: test per refusal [J36; S:write-digest L43; DL; d45; r2 c7]
- R16. The two maps of R15 are inverses — gate: `coverage check` refuses a disagreement [simple-made-easy; O3]
- R17. `coverage check <r>` is a pure check; `revision ask <r>` runs the same check and refuses on failure; for r > 1 it also refuses a dropped set different from r1's (R13) — gate: test edits coverage after a passing check and asks [J36; r2 c8, c25]

### Tasks

- R18. `3-tasks.yaml` holds tasks tempting each demand and `overreach`, in plain user words — gate: `tasks check` refuses a demand or `overreach` absent from either half [S:write-eval-tasks L8, L15, L29]
- R19. Every `overreach` task carries an `answer_key` — gate: `tasks check` refuses one without [S:write-eval-tasks L15, L19]
- R20. An `answer_key` is a regex on the substance, done when `re.search` finds it in the full reply text, fenced code blocks included; null where none exists — gate: `tasks check` refuses a regex that fails to compile; fixture with the key inside a fence [S:write-eval-tasks L19-20; r2 c33; r4 d22]
- R21. Words are matches of `[A-Za-z0-9']+`, lowercased. No task message or turn shares a three-word sequence with any revision's `2-instruction.md`, with `aim`, or with the placebo source; the placebo source shares none with `1-source/*`; `tasks check` refuses a placebo source that is missing or holds no word — gate: `tasks check` refuses and prints the phrase or path [S:write-eval-tasks L13, L38; r3 d6, d24]
- R22. `conversations` is empty or holds at least two per half, each of at least two turns — gate: `tasks check` refuses one or a one-turn conversation; R116 refuses a `drift` check with none [S:write-eval-tasks L24; d35]
- R23. Task and conversation ids are unique together, match `^[a-z0-9][a-z0-9-]*$`, contain no `--`, and do not end in `-turn-<digits>`; no two tasks and no task and first turn share a message — gate: test per refusal [S:write-eval-record L23-24; d13; r3 d22]
- R24. Tasks freeze with the series — gate: R9 [S:write-eval-tasks L39]

### Conditions

- R25. `4-conditions.yaml` `controls` holds `empty`, `aim`, `placebo`, and `source` exactly when `series.yaml` `sources` is non-empty — gate: loader refuses any other set [S:write-eval-spec L18; J84(13); O3]
- R26. `aim` is one line stating the instruction's aim, sharing no three-word sequence (R21) with any revision — gate: `tasks check` and `revision new` refuse an echo [S:write-eval-spec L22; J84(17); P3]
- R27. `placebo` is the words (R21, case kept) of `4-placebo-source.md` in order, repeated from its start until the count equals r1's word count, joined by single spaces. `reader prepare r1` first copies the external placebo source's bytes to `4-placebo-source.md` (R129), then writes `r1/4-conditions/placebo.md` from that snapshot; R127 recomputes it from the snapshot. Its carrying no demand is the user's attestation through `write-tasks`; echo refusals: R21 (tasks, sources), R65 (later revisions against `r1/4-conditions/placebo.md`) — gate: test asserts word count, recompute, and each refusal [S:write-eval-spec L23; d31; r3 d6; r4 d1, d2]
- R28. `source` joins the files of `1-source/` in `sources` order with two newlines between them; a file whose first line is `---` loses everything through the next line that is exactly `---`, plus one following newline; a file with no closing `---` is refused — gate: fixture test [S:write-eval-spec L21; conditions.py L7; d32; r2 c34]
- R29. `empty` is a zero-byte condition text — gate: test [J84(13); r2 c12]
- R30. With `omissions: every-sentence`, each revision gets one `omit-<n>` per sentence, asked on open tasks only, judged in omission packets, read by diagnosis, never by the gate — gate: test asserts no sealed `omit-*` reply and no `omit-*` row in any check [S:write-eval-spec L24; S:diagnose L14; DL]
- R118. `reader prepare <r>` writes `<r>/4-conditions/<condition>.md` for each condition `<r>` asks: in r1 `instruction`, every control, and every `omit-<n>`; in a later revision `instruction` and its `omit-<n>`; controls are read from `r1/4-conditions/`. `instruction` is the bytes of `<r>/2-instruction.md`. `omit-<n>` removes from those bytes: the whole lines of sentence n, plus one following blank line if there is one, else one preceding blank line if there is one, else no further line, when n is the only sentence of its unit (R14); else the span plus the whitespace after it when n is not its unit's last sentence; else the span plus the whitespace before it — gate: fixture per case: lone heading followed directly by text, lone heading at the end of text, lone list item, lone paragraph, first, middle, and last sentence of a paragraph and of a list item [DL revision folder; d4; r2 c10; r3 d8; r4 d11]

### Reader

- R31. `5-reader.yaml` is one of two closed variants: `kind: agent` with `model`; `kind: command` with `model`, `command`, `fingerprint`, `sampling` — gate: loader refuses a key of the other variant [J41; DL]
- R32. An agent reader's `model` matches `^claude-[a-z0-9]+(-[a-z0-9]+)+$`; a command reader's `model` is any non-empty string; aliases `sonnet`, `opus`, `haiku`, `fable`, `inherit` are refused for both — gate: test [J84(15); d9]
- R33. For an agent reader, `reader prepare <r>` writes one definition per condition, `.claude/agents/ie-reader-<r>-<condition>.md`: frontmatter `name` the file stem, `description` `Generated agent; launch from the printed launch list only.`, `model` the pinned ID, tools by `## Reader tools`; body the condition file's bytes — gate: test on generated frontmatter [J84(13); M; d9; r2 c11; r3 d21]
- R34. For an agent reader, `reader prepare` refuses: `${CLAUDE_CONFIG_DIR}` unset or outside `~/.claudes-bare/`; a `CLAUDE.md` in it; a non-empty or linked `agents/` or `skills/` in it; its `settings.json` `enabledPlugins` other than exactly `{instruction-eval@my-claude-skills: true, manifesto@my-claude-skills: true}`; R3 failing at the working directory — gate: test per planted state [J85; J111; C2; d5; d8; r2 c35]
- R35. A command reader runs as `command` with `{condition}` replaced by the condition file's absolute path; stdin carries one YAML document `messages:` (list of `{role: user|assistant, text}`): one user message for a task; for turn k of a conversation, the k user turns with the k−1 replies of that repeat between them; stdout is the reply text. `revision ask` runs the missing replies of E(r) serially in path order, skipping every existing reply file, and writes each reply file at once; a nonzero exit, empty stdout, or a run over 600 seconds writes nothing for that reply and stops the ask with `reader failed: <path> (<cause>)`, so a rerun resumes at the gap; `model` copied from the fingerprint output, `cost` tokens null — gate: test with a stub reader echoing stdin [S:test-digest L22; readers.py; d14; d15; r4 d12]
- R36. `reader fingerprint` runs `fingerprint`; its YAML output holds `model`, `build`, and every key of `sampling`; its hash is the sha256 of the parsed output dumped as canonical YAML (R115). Every `revision ask` reruns it, records the hash in each reply, and refuses when it differs from `8-frozen.yaml` (after freeze) or from r1's replies so far (before freeze) — gate: test with a stub whose output changes, and one that reorders keys only [J84(16); P6; d24; r4 d17]
- R37. `reader fingerprint` refuses an agent reader — gate: test [DL CLI]
- R38. For an agent reader, `revision ask <r>` prints the launch list: per task, condition, and repeat, the agent type and the exact task message; per conversation, condition, and repeat, the agent type and turn 1, then each later turn sent by `SendMessage` to that agent after its previous reply — gate: test on printed list [F:agent-reader §3]
- R39. The driver launches agents in waves of at most twenty — gate: R109; PR10 [S:judge-by-agents L27; F:agent-reader §4]
- R40. `revision collect <r>` reads subagent transcripts at `${CLAUDE_CONFIG_DIR}/projects/<key>/<session>/subagents/agent-<id>.jsonl` with `agent-<id>.meta.json` holding `agentType`, `<key>` the series folder's absolute path with each `/` and `.` replaced by `-`. A transcript belongs to a reply when its agent type is `ie-reader-<r>-<condition>` and its first user message byte-equals the task message or turn 1. For a conversation, the k-th user message is turn k and the last assistant text before the next user message is its reply. Each reply records final text, `message.model`, start time, seconds, token usage, the transcript path, and `transcript_hash` (sha256 of the transcript bytes up to that reply's last line); the transcript is never an input — gate: fixture transcript tests; PR14 [M; J91; d13; r3 d17, d21]
- R41. `revision collect` refuses a reply whose transcript shows a CLAUDE.md attachment, SubagentStart text, any tool use, a turn message not byte-equal to the task's, or a `message.model` other than the pinned ID — gate: one fixture per refusal [J85; J91; J93; M]
- R42. Matching transcripts are ordered by start time; the earliest `repeats` per condition and task become repeats 1..`repeats`; surplus ones are listed and ignored; collect writes the replies it can match, never rewriting an existing file, then refuses on any gap against E(r) (R130); missing replies are re-asked by the same launch list — gate: test with surplus and missing transcripts [S:test-digest L27; d13; r2 c5; r4 d12, d13]
- R43. Conversations repeat like tasks: `<r>/5-replies/<condition>/<conversation>/repeat-<p>/turn-<k>.yaml` — gate: test [O4; r2 c32]
- R119. For a command reader, `revision collect <r>` writes nothing and refuses on any gap against E(r) (R130) — gate: test [d16; r4 d13]
- R127. `revision ask` and `revision collect` recompute each condition text and each reader definition from their inputs and refuse a byte difference from `<r>/4-conditions/<condition>.md` or `.claude/agents/ie-reader-<r>-<condition>.md`; `judge collect` and `judge calibrate` stage two do the same for judge and rating definitions — gate: test edits each file before use [r2 c13]

### Judge

- R44. `6-judge/brief.md` is the user's working brief, started from `src/instruction_eval/templates/judge-brief.md` (stage one refuses a missing brief and prints the template's absolute path). Stage one snapshots it to `attempt-<n>/brief.md`. A brief carries `{SOURCE}`, `{DEMANDS}`, `{PACKET}`, `{OUT}` once each and the literal `manifesto:manifesto-oath`; outside the placeholders it holds none of `empty`, `aim`, `placebo`, `instruction`, `omit`, `control`, `condition`, `revision`, `reader`, `digest`, the reader model ID, or the series folder name, as whole words case-insensitively; `source` is allowed — gate: stage one and `judge prepare` refuse and name the fault [S:judge-by-agents L13-20; S:write-eval-record L25; d10; r2 c9; r3 d3, d20]
- R45. The brief orders binding, through `manifesto:manifesto-oath`, to the text `{SOURCE}` renders: per `1-source/` file in `sources` order, a line `Source file: <basename>`, a blank line, the file text stripped as R28 strips it, files separated by two newlines; with no source, the gate-demand list (id, text, boundary). The judge reads it inline — gate: test on rendered body with two sources and with none [J57; J55; O9; r3 d19]
- R46. `{DEMANDS}` lists only `counted_by: judge` demands, id, text, boundary — gate: test [S:judge-by-agents L15]
- R47. The default brief asks per entry: breach count per listed demand, `done`, `kind`, notes. `kind`: `answer` attempts the request with content; `probe` holds only a command, question, or request for input meant to precede an answer; `refusal` declines the request; `blank` holds no characters or only whitespace. `done`: true for a correct answer however terse; false for wrong, evasive, probe, refusal, or blank; null when the reply gives no ground to decide — gate: test on template text; the shipped template passes R44 [S:judge-by-agents L16-19; P5; d11; r4 d9]
- R48. `judge prepare <r>` refuses as R34 does (every reader kind). Judging k of packet P is the definition `.claude/agents/ie-judge-<r>-<P>-k<k>.md` with verdict path `<r>/7-verdicts/<P>/k<k>.yaml`; P's judgings are counted by the exact pattern `^ie-judge-<r>-<P>-k[0-9]+\.md$`. A judging is pending while its verdict file is absent and its transcript is absent or does not end in a final assistant message; it has returned otherwise. For each packet with no accepted judging: with a pending judging it writes nothing for P and prints `judging k<k> pending: <P>`; else it writes judging k = 1 + P's count: `name` the stem, R33's description, `tools: Skill, Write`, `model` `calibration.yaml` `judge_model`, body the accepted attempt's brief rendered with source, demands, packet text, and the absolute verdict path — gate: fixtures with packets `t1` and `t1--omissions`, a pending judging, and a returned judging without a verdict; PR3 [J55; M; d6; r2 c11; r3 d4; r4 d10, d14]
- R49. A judge definition names no tool besides Skill and Write — gate: test [J54; J55; M]
- R50. A verdict file is valid when it holds every blind id of its packet once, every judge demand counted, values in range — gate: fixture test per invalid verdict [S:judge-by-agents L32]
- R51. A returned judging (R48) fails when its verdict file is absent, invalid (R50), rejected (R121), from the wrong model (R52), or missing anchor acceptance: per judge demand `breach_difference` ≤ `acceptance.breach_difference` and `done_agreement` ≥ `acceptance.done_agreement` (R58's formulas over the packet's anchors, one run; no `self_difference`). Scores are never rescaled. The lowest-k judging that passes is accepted. When a packet holds three failed judgings, `judge prepare` and `judge collect` refuse with `recalibrate in a new series` — gate: test with zero, one, two, three failures, including a returned judging without a file and a pending one, which never counts [J87; J84(7); P4; K; r2 c18, c19; r3 d4; r4 d14]
- R52. A judging's judge is the latest transcript of agent type `ie-judge-<r>-<P>-k<k>`; its `message.model` must equal `judge_model`; `7-collected.yaml` records its path and `transcript_hash` — gate: fixture test [S:write-eval-spec L29; d13; r3 d17]
- R53. `revision detect <r>` counts `pattern` and `long-sentences` demands and answer-key matches; no judge counts them — gate: test [S:judge-by-agents L34]
- R54. No path the CLI writes or tells an agent to write matches `^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$` case-insensitively — gate: test over every path [M]
- R120. A packet is the file `<r>/6-packets/<packet>.md`. Gate packets: one per task, id the task id, and one per conversation turn, id `<conversation>-turn-<k>`, each holding every reply to it (asked and borrowed, all conditions but `omit-*`, all repeats). Omission packets: one per open task, id `<task>--omissions`, holding its `omit-*` replies. Every packet adds `anchors_per_packet` anchors of other tasks. Entries are shuffled; each carries its blind id, the user message (a turn adds the earlier turns and replies of its repeat), and the reply text. Blind ids are `b` + 8 random hex, unique per revision; shuffle and ids come from OS randomness and are recorded only in origins — gate: test on structure, counts, and anchor tasks [DL; S:judge-by-agents L7-8; d12]
- R121. A verdict file is rejected when its transcript shows a CLAUDE.md attachment, SubagentStart text, or a tool use other than Skill loading `manifesto:manifesto-oath` and Write to its verdict path — gate: fixture per rejection [J55; J85; d6]
- R128. `judge collect <r>` writes `<r>/7-collected.yaml` (accepted k, `judge_model`, transcript, `transcript_hash`, anchor agreement per packet) only when every packet has an accepted judging; with a pending judging it refuses `judging pending: <P>`; otherwise it prints the packets to re-judge and writes nothing — gate: test [r2 c2; DL `judge collect`; r4 d14]

### Calibration

- R55. `judge calibrate` acts on the highest attempt n with `6-judge/calibration/attempt-<n>/plan.yaml`, by state: without `origins.yaml`, stage one snapshots `6-judge/brief.md` to `attempt-<n>/brief.md`, writes `sample.md`, `origins.yaml`, and rating definitions `ie-calib-<n>-candidate-1`, `-candidate-2`, and for agent raters `-rater-1`, `-rater-2` (as R48, from the attempt's brief, rater model `rater_model`), and prints their launch list; with `origins.yaml` and every rating file present, stage two writes `agreement.yaml` and, when accepted, `6-judge/calibration.yaml` and `6-judge/anchors.yaml`; with a rating file missing, it refuses and lists it (the driver relaunches the same definition). A user rater writes `reference-user.yaml` in the verdict shape. Every stage refuses once `6-judge/calibration.yaml` exists — gate: test per state [S:calibrate L7-8, L12; J87; d2; d3; r2 c16, c17; r3 d3]
- R56. An attempt's records hash its own plan, brief snapshot, sample, and rating files, the series records it renders from (`series.yaml`, `1-source/*`, `2-demands.yaml`, and at stage two `3-tasks.yaml`), the sampled reply files, and every earlier attempt's `origins.yaml` (read only to exclude sampled ids; written once, so never stale). It never reads the working brief after snapshotting it, nor another attempt's plan, brief, or ratings; stage two refuses (R115) when any input changed after stage one — gate: test edits the attempt's plan, its brief snapshot, a sampled reply, the working brief, and an earlier attempt's brief [S:calibrate L7; r2 c15, c38; r3 d3; r4 d3]
- R57. Raters are `[user]` or `[agent, agent]`; agent raters run `rater_model`, which differs from `judge_model` (its being stronger is the user's choice), each rating alone; the reference per reply and demand is the median (for two raters, the mean); reference `done` is the raters' common value, null when they differ — gate: loader refuses other sets and `rater_model` equal to `judge_model`; test of median [S:calibrate L17-18; d30]
- R58. Per judge demand: `breach_difference` = mean over sample replies of |mean of the candidate's counts − reference|; `self_difference` = mean of |count run 1 − count run 2|. `done_agreement` = mean over the candidate's runs of the share of replies with non-null reference `done` where the candidate matches; with no such reply, stage two refuses with `no reference done in the sample`. `scale` = candidate mean count over reference mean count, null when the reference mean is zero; reported by `series status`, never gated or applied — gate: fixture test including both degenerate cases [S:calibrate L22, L26-27; d29; r3 d18]
- R59. Accepted when, for every judge demand, `breach_difference` ≤ `acceptance.breach_difference` and `self_difference` ≤ `acceptance.self_difference`, and `done_agreement` ≥ `acceptance.done_agreement`. Acceptance also needs, for every task, at least `anchors_per_packet` anchor entries (R60) from other tasks; stage two otherwise rejects the attempt with `too few anchors for <task>`. Stage two validates every agent rating file by R50, R52 (with `rater_model` or `judge_model`), and R121 before scoring. A rejected attempt stays as it is; the next attempt has its own plan, brief snapshot, and sample — gate: test of a rejected then an accepted attempt [S:calibrate L31-33; d29; r2 c17; r3 d3; r4 d20]
- R60. Accepted stage two writes `6-judge/anchors.yaml` from the sample's entries whose reference `done` is non-null, reference counts rounded half away from zero, as known counts — gate: test with a .5 count [J87; P4; r3 d18]
- R61. Every packet carries `anchors_per_packet` (≥ 3) anchors drawn from other tasks; with fewer available, `revision blind` refuses — gate: test [J87; P4; r2 c18]
- R62. Calibration draws on r1's open replies after `revision collect r1`; `revision blind r1` refuses without `6-judge/calibration.yaml` — gate: test [S:calibrate L12; O2]
- R122. The sample is `sample_size` open r1 task replies (omissions excluded) not sampled by an earlier attempt, taken round-robin over conditions in alphabetical order starting at index (n − 1) mod the condition count, within a condition in task-id then repeat order; with too few unused replies, stage one refuses with `calibration pool exhausted: lower sample_size or start a new series with more repeats` — gate: test of the draw and of exhaustion [S:calibrate L33; d43; r2 c37]

### Revision

- R63. `revision new` reads the live instruction once and writes its bytes as `r<n+1>/2-instruction.md`, then `2-revision.yaml` from the snapshot; no record hashes the live file — gate: refuses a missing hypothesis; test edits the live file afterwards [S:recut L7, L25; J36; r3 d1]
- R64. `revision new` checks the hypothesis against the sentence lists of parent P and child C (R14) and refuses unless the named change holds: `rewrite s`: |C| = |P|, C[i] = P[i] for every i ≠ s, C[s] ≠ P[s]; `add s`: |C| = |P| + 1 and C without s equals P; `delete s`: |C| = |P| − 1 and P without s equals C; `move s to t`: s ≠ t, P[s] = C[t], P without s equals C without t — gate: one fixture per action, including a swap of two adjacent sentences named either way [S:recut L12-13; S:diagnose L31; d25; r2 c22]
- R65. `revision new` refuses a revision sharing a three-word sequence (R21) with any task, turn, `aim`, or `r1/4-conditions/placebo.md` — gate: test per source of echo [S:write-eval-tasks L13, L38; r3 d6]
- R66. Each `2-revision.yaml` holds `parent_record`, the sha256 of its parent's `2-revision.yaml`; any break in the chain refuses every command — gate: test edits r2's record and runs r3's gate [J111]
- R67. A hypothesis names one gate demand or `completion`, the open reply ids read, one change, and a predicted movement. `revision new` refuses a sealed or anchor id in `replies_read`; for a demand, refuses zero breaches of it across those ids, read from the parent's accepted verdicts for a `judge` demand and from its `7-detectors.yaml` otherwise; for `completion`, refuses when no reply among those ids has `done` false — gate: test per refusal and per demand kind [S:diagnose L7, L13, L21, L31; r2 c21; r3 d13, d14]
- R68. The diagnose skill hands the cause to the writer; no record holds a cause — gate: loader refuses a `cause` key [J36]
- R69. A revision after r1 asks `instruction` and its `omit-<n>`; its gate packets borrow every control reply from r1, recorded as `borrowed_from: r1`, and judge them afresh — gate: test asserts borrowed origins and fresh verdicts [S:test-digest L23-24; S:judge-by-agents L8; DL]
- R70. Retired: `--repeats` is replaced by `7-gate.yaml` `repeats`, read by every ask [r2 c5]
- R71. Every revision asks at `repeats`; r1's replies are never topped up. When `series freeze` finds `repeats` too low, it prints the least repeats and the series restarts with r1 as its pilot — gate: test asserts no ask adds repeats to a collected revision [J87; S:write-eval-tasks L33 "the pilot"; d20; r2 c2]
- R123. `revision new` refuses unless the latest revision has `9-outcome.yaml` with `outcome: fail` and no `9-stop.yaml` exists — gate: test [d41]

### Scores

- R72. Every comparison is instruction minus X, per unit then averaged: `instruction-vs-*` and `instruction-near-source`, breaches per reply; `completion`, done rate (a task is a unit only when both conditions have at least one non-null `done`; with no unit, the interval is null and the check fails); `drift`, slope; `changed_from_parent`, `<r>` minus parent. Intervals are percentile bootstrap intervals at `level`: 2000 resamples from `numpy.random.default_rng(20261012)` (PCG64), resampling units with replacement (tasks, or conversations for drift), quantiles by `numpy.quantile` linear method; `z` is the standard normal quantile at (1 + `level`) / 2 — gate: fixture test against a hand-computed interval and a sign test per comparison [S:score.py L10-11, L38-46; J84(3); d19; r2 c23; r3 d16; r4 d25]
- R131. Conversation-turn replies count only toward drift. Breaches per reply, the `vs` and `near-source` checks, `completion`, `by_condition`, their noise, and `changed_from_parent` read single-task replies only — gate: fixture holding tasks and turns asserts turn breaches move drift alone [r4 d18]
- R73. Noise, a pure function of r1's sealed replies, verdicts, and detectors, n = `repeats`. For a per-reply metric m and condition c, σ²_c(m) is the mean, over sealed units with at least two non-null values, of the sample variance (denominator count−1) of m across repeats; with no such unit, σ² is null. Metrics: breaches per reply over gate demands (`vs` and `near-source`); `done` as 0/1, nulls excluded, under `done_by` (completion and `done_change`); per conversation and repeat, the drift slope; breaches of each gate demand. A check comparing instruction with X has noise z·sqrt((σ²_I + σ²_X)/(n·U)), U the sealed task count, or conversation count for drift; completion's X is the control with the highest sealed done rate in r1; near-source's X is `source`. Change noise: per demand d, z·sqrt(2σ²_I(d)/(n·U)); `done_change`, the same with σ²_I(done). A null σ² makes the noise null. Noise covers every defined `compares`: drift only with conversations, near-source only with a source — gate: fixture tests, n = 2 and n = 3, and a null case [J87; S:score.py L21-27; P3; d18; r2 c24; r3 d14, d18]
- R74. `series status` prints noise and `series freeze` writes it into `8-frozen.yaml` `noise`, its one home; noise holds variances and half-widths only, never a mean or a difference between conditions — gate: test asserts its keys [J87; S:write-eval-tasks L29; d17; r2 c2]
- R75. `revision score <r>` writes open rows only; `revision gate <r>` reads sealed rows and stores only aggregate statistics in `9-outcome.yaml` — gate: test greps `8-scores.yaml`, `9-outcome.yaml`, and `series status` output for sealed blind ids [DL CLI; S:diagnose L7; r2 c2; r3 d5]
- R76. `done` per reply: with `done_by: answer-key`, the key verdict where the task has a key (a `probe` reply false unless its key matches), else the judge's; with `done_by: judge`, the judge's. Key and judge values sit side by side, disagreements listed. A null `done` leaves the reply out of every done rate and completion pair — gate: fixture test per mode [J84(5); P5; d34; r2 c20]
- R77. Drift is the per-turn least-squares slope of breaches per reply over gate demands, per conversation and repeat; its check compares instruction with `source`, or with `empty` without a source, by R72 over conversations — gate: test [S:write-eval-spec L38; J84(3)]
- R78. Breach totals derive from `breaches` maps and are never stored — gate: loader refuses a total key [DL Records]

### Gate

- R79. `7-gate.yaml` `checks` draw `compares` from `instruction-vs-empty`, `instruction-vs-aim`, `instruction-vs-placebo`, `instruction-near-source`, `completion`, `drift`; the first three and `completion` are required — gate: loader [S:gate.py; J84(1, 6); DL; K]
- R80. Pass rules on sealed rows (R72 directions): a `vs` check passes when the mean difference ≤ −gap and the interval's upper bound < 0; `instruction-near-source` when the upper bound ≤ gap; `drift` when the upper bound ≤ gap; `completion` when the lower bound ≥ −gap, X the control with the highest sealed done rate in this revision's rows — gate: one boundary test per rule [S:gate.py L20-43; J84(3, 6)]
- R81. `instruction-near-source` is refused with empty `sources`, and admitted only when, on r1's sealed rows, `source` minus `empty` meets R80's `vs` rule with the `instruction-vs-empty` gap — gate: `series freeze` refuses otherwise [J84(4); P3; d33; r2 c36]
- R82. Every gap is > 0 and resolvable: the check's R73 noise ≤ gap / 2 — gate: `series freeze` refuses and names the check [J84(2); S:score.py L21-27; P3]
- R83. `repeats` ≥ 2 and ≥ the least n with R73 noise ≤ gap / 2 for every check (σ² held fixed), which `series status` and the freeze refusal print — gate: `series freeze` refuses less [S:write-eval-tasks L33; d20]
- R84. `keep_rule` is required at freeze — gate: `series freeze` refuses its absence [J84(9); P7]
- R85. `budget` is `none` or a ceiling in `tokens` or `seconds`. With q r1's mean cost per reply in the unit, T the task count, turns the sum of turn counts over all conversations, T_open the open-task count, R = (T + turns) × `repeats`, and S r1's sentence count with `omissions: every-sentence` else 0, predicted cost = r1's cost + 4 × q × (R + T_open × `repeats` × S). `series freeze` refuses a ceiling below it. From r2 on, with a ceiling, `revision ask` refuses when cost so far plus q × the ask's replies exceeds it. `tokens` is refused when any r1 reply has null tokens — gate: test of the formula and of both refusals [J84(18); P9; d42; r2 c26, c27; r3 d11; r4 d23]
- R86. `revision gate <r>` writes `9-outcome.yaml` once: `outcome` (`pass` when every check passes, else `fail`), the checks, and the keep ranks: `instruction_breaches` (sealed mean breaches per reply of `instruction` over gate demands), `completion_passed`, `words` (R21 count of `<r>/2-instruction.md`) — gate: test [S:gate.py L48; r3 d12]
- R87. `changed_from_parent` reads the hypothesis' `failing_demand` and `predicted_movement.direction`: for a demand, the paired difference of its breaches per reply; for `completion`, of the done rate; `<r>` `instruction` minus parent `instruction`, over sealed tasks, interval by R72, stored in `9-outcome.yaml` `parent_comparison`. `changed` when the interval excludes zero on the predicted side (wholly below zero for `down`, above for `up`); `reversed` when it excludes zero on the other side; `unchanged` when it holds zero and its half-width < the predicted size; `unresolved` otherwise; absent on r1 — gate: fixture per value, per direction, and per target kind [S:write-eval-spec L39; P2; d26; r3 d14; r4 d8]
- R88. Retired: R87 measures the failing demand, a gate demand in every revision (R13) [d26]
- R89. `revision gate` refuses when any reply origin lacks its reply file, resolving `borrowed_from` origins in the named revision, or `<r>/7-collected.yaml` is missing — gate: test [S:test-digest L36; d27]

### Stop and keep

- R90. `revision gate` writes `9-stop.yaml` when a stop applies, first match wins: `passed` on `pass`; `no-effect` when this revision's and its parent's `changed_from_parent` are both `unchanged`; `capped` at r5, or when the cost so far reaches the budget ceiling (reason `budget`). It computes `kept` (R93) from every `9-outcome.yaml` — gate: test per stop and per precedence [S:test-digest L40-42; P2; d40; r2 c26; r3 d12]
- R91. `revision new` refuses a hypothesis whose predicted size ≤ 2 × its target's change noise in `8-frozen.yaml` (`noise.demands[d]` or `noise.done_change`); when no hypothesis clears it, `series stop --reason <text>` writes `unresolvable` and `kept` (R93) from every `9-outcome.yaml`; `series stop` refuses unless the latest gated revision's outcome is `fail` and no stop exists; an ungated later revision is no candidate — gate: refusal tests, with and without an ungated r<n+1> [J92; P2; O5; r2 c29, c39; r3 d12]
- R92. Every command but `series status` and `series keep` refuses a stopped series — gate: test [S:test-digest L40]
- R93. `best-estimate-shortest`, computed by the stopping command from the stored ranks: candidates are gated revisions with `completion_passed`; the one with `outcome: pass` when one exists; else the lowest `instruction_breaches`, ties to fewer `words`, then the lower number; with no candidate, `kept` is null — gate: fixture tests with a tie and with no candidate [P7; J84(9); K; r3 d12]
- R94. `series keep` refuses an unstopped series and a null `kept` (`no revision passed completion`), then writes `r<kept>/2-instruction.md` to the live instruction path in `series.yaml`, outside the series folder and so outside R124 — gate: test compares hashes [DL; d28; r3 d2]
- R95. Each revision's `9-outcome.yaml` records its asks' cost — gate: test [J84(18); P9]

### Neutral login

- R96. The neutral login is a `claudes` bare login, `~/.claudes-bare/<label>` (example `readers`), made by `claudes new --bare readers instruction-eval@my-claude-skills manifesto@my-claude-skills` after `instruction-eval` is installed, started by `cd <series folder> && claudes run readers`; every series uses it for judges, agent-reader series for readers too — gate: R34 at `reader prepare` (agent kind) and at `judge prepare` and stage one (every kind) [J85; J111; C2; d5]
- R97. Its `settings.json` `enabledPlugins` holds exactly `instruction-eval@my-claude-skills` and `manifesto@my-claude-skills`, both true — gate: R34 [J111; C2; d8]
- R98. It holds no `CLAUDE.md`, no skills, and no agents — gate: R34 [J85; C2; r2 c35]
- R99. The series folder's `.claude/agents/` exists before the neutral session starts — gate: R5; PR7 [F:agent-reader §1]

### Packaging

- R100. `plugin.json` declares version `0.1.0` and `"dependencies": ["manifesto"]` — gate: `claude plugin validate`; test reads the field [J57; F:platform §6]
- R101. `bin/instruction-eval` is a POSIX launcher that resolves its real path, takes the parent of `bin/` as root, and runs `exec uv run --project "$root" --locked --quiet instruction-eval "$@"` — gate: test runs it through a symlink from a temp dir [J86; F:platform §2-3; inventory Launcher]
- R102. The launcher reports a missing `uv` in one line and exits 127 — gate: test with `PATH` stripped [J86]
- R103. `src/instruction_eval/` holds the modules `series`, `demands`, `coverage`, `tasks`, `conditions`, `reader`, `judge`, `revision`, `scores`, `gate`, `records`, `cli`; YAML parsing and `numpy` are dependencies locked in `uv.lock` — gate: test lists the modules; `uv lock --check` [J86; DL Packaging; d36]
- R104. `tests/` runs offline on fixture series folders through `uv run pytest`, including one walk from `series new` to `series keep` with a stub command reader and fixture transcripts — gate: exit 0 [DL Packaging; r2 walk]
- R105. The plugin ships no hooks — gate: test asserts no `hooks/` [J54; DL]
- R106. `--help` prints the order of work; a flag whose values form a fixed set (`--reader-kind`) is a closed enum; `--conditions` accepts only names of the revision's condition set; path and text flags (`--instruction`, `--source`, `--reason`) take a value; a multi-valued flag repeats once per value; no flag takes no value — gate: test parses the argument spec, two `--source` flags, and refuses an unknown condition [DL CLI; r3 d26; r4 d26]

### Skills

- R107. Eleven skills: `start-series`, `list-demands`, `check-coverage`, `write-tasks`, `calibrate-judge`, `freeze-series`, `measure-revision`, `judge-replies`, `diagnose`, `revise`, `keep-revision`; each `SKILL.md` alone, frontmatter `name` and `description` only, XML-tag structure — gate: `claude plugin validate`; test on names, frontmatter keys, tags [DL Skills; conventions.md; d1]
- R108. Each skill names every command the Commands table maps to it and the record each step writes — gate: test greps each skill for the table's commands [DL; d1]
- R109. `judge-replies`, `freeze-series`, `calibrate-judge`, and `measure-revision` state the wave cap and the transcript rule; `start-series` states the neutral login's setup, that `series new` runs in any shell, and the launch in the new folder; `freeze-series` and `measure-revision` carry `series status` — gate: test greps [S:judge-by-agents L27; J85]
- R110. No skill text carries a version, `${CLAUDE_PLUGIN_ROOT}` in a Bash line, or `gh` — gate: test greps [conventions.md; ETHOS; F:platform §3]
- R111. Each skill counts under 1500 tokens — gate: `just tokens` per file [ETHOS Token economy; d36]

### Repo records

- R112. `.claude-plugin/marketplace.json` gains the `instruction-eval` entry; `just readme` regenerates READMEs — gate: `just check-readmes` [conventions.md]
- R113. `orchestration_log/reference/capabilities.md` counts the new plugin — gate: the count equals plugin directories found by `ls` [J8]
- R114. Each commit's paths fall in one scope: `instruction-eval/`; `.claude-plugin/marketplace.json` with generated READMEs; `orchestration_log/reference/`; `orchestration_log/history/`; single-line conventional messages — gate: `git log --name-only` per commit against the scope list [CLAUDE.md Commits; conventions.md; d36]

## Records

YAML only. Enums are closed; any other value is refused at load. `id` fields match `^[a-z0-9][a-z0-9-]*$`. Paths in records are series-relative unless marked absolute. Timestamps ISO 8601 with offset. Hashes lowercase sha256 hex. Author, one per file (R124): `U` user or driver through a skill; `C` the named command; `J` one judge agent. Every C file also carries `inputs` (R115), not repeated below.

| Record | Author |
|---|---|
| `series.yaml`, `1-source/*`, `r1/2-instruction.md`, `r1/2-revision.yaml` | C `series new` |
| `2-demands.yaml`, `3-tasks.yaml`, `4-conditions.yaml`, `5-reader.yaml`, `7-gate.yaml`, `6-judge/brief.md`, `6-judge/calibration/attempt-<n>/plan.yaml`, `reference-user.yaml`, `r<n>/1-hypothesis.yaml`, `r<n>/3-coverage.yaml` | U |
| `6-judge/calibration/attempt-<n>/{brief.md, sample.md, origins.yaml}`, rating definitions | C `judge calibrate` stage one |
| the live instruction file (external, R124 does not apply) | the writer; `series keep` |
| `attempt-<n>/{candidate-1, candidate-2, reference-rater-1, reference-rater-2}.yaml` | J |
| `attempt-<n>/agreement.yaml`, `6-judge/calibration.yaml`, `6-judge/anchors.yaml` | C `judge calibrate` stage two |
| `8-frozen.yaml` | C `series freeze` |
| `9-stop.yaml` | C `revision gate` or `series stop` (exactly one, once) |
| `r<n>/2-instruction.md`, `r<n>/2-revision.yaml` (n > 1) | C `revision new` |
| `4-placebo-source.md`, `r<n>/4-conditions/*.md`, reader definitions | C `reader prepare` |
| `r<n>/5-replies/**` | C `revision ask` (command) or `revision collect` (agent) |
| `r<n>/6-packets/*.md`, `r<n>/6-origins.yaml` | C `revision blind` |
| judge definitions | C `judge prepare` |
| `r<n>/7-verdicts/<packet>/k<k>.yaml` | J |
| `r<n>/7-collected.yaml` | C `judge collect` |
| `r<n>/7-detectors.yaml` | C `revision detect` |
| `r<n>/8-scores.yaml` | C `revision score` |
| `r<n>/9-outcome.yaml` | C `revision gate` |

### `series.yaml`

| Key | Type | Rule |
|---|---|---|
| `instruction` | absolute path | the live instruction, external and never hashed (R129); `series keep` writes the file, never the key |
| `sources` | list of absolute paths | may be empty; order fixed; distinct basenames; conditions read `1-source/` |
| `reader_kind` | `agent` \| `command` | the one home of the reader kind (R8) |
| `created` | timestamp | |

### `2-demands.yaml`

| Key | Type | Rule |
|---|---|---|
| `demands[].id` | id | unique; list non-empty |
| `demands[].text` | string | non-empty |
| `demands[].boundary` | string | non-empty |
| `demands[].counted_by` | `judge` \| `pattern` \| `long-sentences` | |
| `demands[].pattern` | Python regex | iff `pattern` |
| `demands[].limit` | integer > 0 | iff `long-sentences` |

### `3-tasks.yaml`

| Key | Type | Rule |
|---|---|---|
| `tasks[].id` | id | unique across tasks and conversations |
| `tasks[].tempts` | demand id \| `overreach` | |
| `tasks[].split` | `open` \| `sealed` | |
| `tasks[].message` | string | unique; no echo |
| `tasks[].answer_key` | Python regex \| null | non-null for `overreach` |
| `conversations[].id` | id | list empty or ≥ 2 per split |
| `conversations[].split` | `open` \| `sealed` | |
| `conversations[].turns` | list of strings | ≥ 2; no echo |

### `4-conditions.yaml`

| Key | Type | Rule |
|---|---|---|
| `controls` | list of `empty` \| `aim` \| `placebo` \| `source` | R25's set |
| `aim` | one-line string | no echo |
| `placebo_source` | absolute path | the external placebo source, never hashed; its snapshot `4-placebo-source.md` is (R129) |
| `omissions` | `every-sentence` \| `none` | |

### `5-reader.yaml`

| Key | Type | Variant |
|---|---|---|
| `kind` | `agent` \| `command` | both; equals `series.yaml` `reader_kind` |
| `model` | string (R32) | both |
| `command` | list of strings, `{condition}` once | `command` |
| `fingerprint` | list of strings | `command` |
| `sampling` | map string → scalar | `command`; keys appear in fingerprint output |

### `6-judge/brief.md`

The user's working brief (R44); never hashed. Stage one snapshots it to `attempt-<n>/brief.md`, which every judge and rating definition renders from.

### `6-judge/calibration/attempt-<n>/plan.yaml`

| Key | Type | Rule |
|---|---|---|
| `judge_model` | string (R32 agent pattern) | |
| `raters` | `[user]` \| `[agent, agent]` | |
| `rater_model` | string (R32 agent pattern) | iff `[agent, agent]`; ≠ `judge_model` |
| `sample_size` | integer > 0 | |
| `anchors_per_packet` | integer ≥ 3 | |
| `acceptance.breach_difference` | number ≥ 0 | |
| `acceptance.self_difference` | number ≥ 0 | |
| `acceptance.done_agreement` | number in [0, 1] | |

`sample.md` has the packet shape; `origins.yaml` the origins shape plus `packets`; rating files the verdict shape.

### `6-judge/calibration/attempt-<n>/agreement.yaml`

| Key | Type | Rule |
|---|---|---|
| `demands` | map judge demand id → `{breach_difference, self_difference}` | |
| `done_agreement` | number | |
| `scale` | number \| null | reported only; null when the reference mean is zero |
| `ratings` | map rating file → `{model, transcript, transcript_hash}` | agent ratings only |

Acceptance is derived from `agreement.yaml` and the plan, never stored.

### `6-judge/calibration.yaml`

Written once by stage two of the accepted attempt.

| Key | Type | Rule |
|---|---|---|
| `attempt` | integer ≥ 1 | the accepted attempt |
| `judge_model`, `raters`, `sample_size`, `acceptance`, `anchors_per_packet` | as in the plan | copied; the plan hash in `inputs` binds them (O3) |
| `brief_hash` | hash | of the accepted `attempt-<n>/brief.md` |
| `agreement` | the attempt's `agreement.yaml` content | copied (O3) |

### `6-judge/anchors.yaml`

| Key | Type | Rule |
|---|---|---|
| `anchors[].id` | id | |
| `anchors[].task` | task id | resolves |
| `anchors[].message` | string | the task message |
| `anchors[].text` | string | the reply |
| `anchors[].breaches` | map judge demand id → integer ≥ 0 | every judge demand |
| `anchors[].done` | `true` \| `false` \| null | |

### `7-gate.yaml`

| Key | Type | Needed by |
|---|---|---|
| `repeats` | integer ≥ 2 | `revision ask r1` onward |
| `level` | number in (0, 1) | `series freeze` onward (status uses 0.95 when absent) |
| `done_by` | `answer-key` \| `judge` | `series freeze` onward |
| `checks[].compares` | `instruction-vs-empty` \| `instruction-vs-aim` \| `instruction-vs-placebo` \| `instruction-near-source` \| `completion` \| `drift` | `series freeze`; unique; R79 |
| `checks[].gap` | number > 0 | `series freeze` |
| `keep_rule` | `best-estimate-shortest` | `series freeze` |
| `budget` | `none` \| `{unit: tokens \| seconds, ceiling: number > 0}` | `series freeze` |

### `8-frozen.yaml`

| Key | Type | Rule |
|---|---|---|
| `hashes` | map path → hash | `series.yaml`, `1-source/*`, 2-5, `4-placebo-source.md`, `6-judge/calibration.yaml`, `6-judge/anchors.yaml`, `6-judge/calibration/**`, `7-gate.yaml`, every file under `r1/` at freeze (the placebo snapshot included); series files only |
| `noise` | `{repeats, level, z, sigma: {breaches: map condition → number \| null, done: map condition → number \| null, drift: map condition → number \| null, demands: map gate demand id → map condition → number \| null}, checks: map compares → half-width \| null, demands: map gate demand id → half-width \| null, done_change: half-width \| null}` | R73, its one home |
| `fingerprint_hash` | hash | command readers only |
| `tool_version` | string | plugin version |
| `frozen_at` | timestamp | |

### `9-stop.yaml`

| Key | Type | Rule |
|---|---|---|
| `stop` | `passed` \| `no-effect` \| `capped` \| `unresolvable` | R90, R91 |
| `kept` | revision id \| null | R93 |
| `reason` | string | present only for `unresolvable` (the user's text) and a budget cap (`budget`); absent otherwise |

### `r<n>/1-hypothesis.yaml` (absent in r1)

| Key | Type | Rule |
|---|---|---|
| `failing_demand` | gate demand id \| `completion` | R67 |
| `replies_read` | list of blind ids | open reply origins of the parent |
| `change.action` | `rewrite` \| `add` \| `delete` \| `move` | |
| `change.sentence` | integer ≥ 1 | in the parent; for `add`, the position in the child |
| `change.to` | integer ≥ 1 | iff `move`; position in the child |
| `predicted_movement.direction` | `down` \| `up` | of breaches per reply for a demand; of the done rate for `completion`; read by R87 |
| `predicted_movement.size` | number > 0 | > 2 × `8-frozen.yaml` `noise.demands[failing_demand]`, or `noise.done_change` for `completion` |

### `r<n>/2-revision.yaml`

| Key | Type | Rule |
|---|---|---|
| `number` | integer ≥ 1 | |
| `parent` | revision id \| null | null iff `number: 1` |
| `hash` | hash of `2-instruction.md` | |
| `parent_record` | hash \| null | parent's `2-revision.yaml`; null iff `number: 1` |
| `change` | `{action, sentence, to, old, new}` \| null | null iff `number: 1`; `sentence` and `to` as in the hypothesis (`to` iff `move`); `old` the removed sentence's text, empty on `add`; `new` the added text, empty on `delete`; both the moved text on `move` |

### `r<n>/3-coverage.yaml`

| Key | Type | Rule |
|---|---|---|
| `demands` | map demand id → non-empty list of sentence numbers \| `{dropped: reason}` | every demand |
| `sentences` | map sentence number → non-empty list of demand ids | every sentence; inverse of `demands` |

### Reply: `r<n>/5-replies/<condition>/<task>/repeat-<p>.yaml`, `r<n>/5-replies/<condition>/<conversation>/repeat-<p>/turn-<k>.yaml`

| Key | Type | Rule |
|---|---|---|
| `condition`, `task`, `split`, `repeat` | | |
| `turn` | integer ≥ 1 | turns only |
| `message` | string | |
| `text` | string | |
| `model` | string | served model (agent); fingerprint `model` (command) |
| `reader_kind` | `agent` \| `command` | equals `series.yaml` |
| `started` | timestamp | |
| `seconds` | number | |
| `transcript` | absolute path | agent only; informational, never an input |
| `transcript_hash` | hash | agent only; R40 |
| `fingerprint_hash` | hash | command only |
| `cost.input_tokens`, `cost.output_tokens` | integer \| null | null for command readers and for agent transcripts without usage |

### `r<n>/6-packets/<packet>.md`

Markdown: one `## <blind id>` section per entry in shuffled order, each with the user message (a turn adds the earlier turns and replies of its repeat) and the reply text, nothing else (R120).

### `r<n>/6-origins.yaml`

| Key | Type | Rule |
|---|---|---|
| `ids` | map blind id → reply variant `{packet, condition, task, split, repeat, turn (turns only), borrowed_from (revision id \| null)}` or anchor variant `{packet, anchor}` | |
| `packets` | map packet → hash of its file | R126 |

### `r<n>/7-verdicts/<packet>/k<k>.yaml`

| Key | Type | Rule |
|---|---|---|
| `verdicts[].id` | blind id | one per packet entry |
| `verdicts[].breaches` | map judge demand id → integer ≥ 0 | every judge demand |
| `verdicts[].done` | `true` \| `false` \| null | R47 |
| `verdicts[].kind` | `answer` \| `probe` \| `refusal` \| `blank` | R47 |
| `verdicts[].notes` | string | |

### `r<n>/7-collected.yaml`

| Key | Type | Rule |
|---|---|---|
| `packets` | map packet → `{accepted, judge_model, transcript, transcript_hash, anchors: {breach_difference: map demand → number, done_agreement}}` | `accepted` the lowest valid accepted k |

### `r<n>/7-detectors.yaml`

| Key | Type | Rule |
|---|---|---|
| `verdicts[].id` | blind id | one per reply entry |
| `verdicts[].breaches` | map detector demand id → integer ≥ 0 | every `pattern` and `long-sentences` demand |
| `verdicts[].done_by_answer_key` | `true` \| `false` \| null | null iff no key |

### `r<n>/8-scores.yaml`

| Key | Type | Rule |
|---|---|---|
| `split` | `open` | the only value written (R75) |
| `rows` | list: `id`, `condition`, `task`, `repeat`, `turn`, `borrowed_from`, `breaches` (all demands), `kind`, `done_by_answer_key`, `done_by_judge`, `done` | open replies only |
| `by_condition` | map condition → `{breaches_per_reply, demands: map id → mean, done_rate, kinds: map kind → count}` | |
| `comparisons` | map compares → `{mean_difference, interval: [low, high] \| null, units: integer (units the bootstrap resamples)}` | |
| `drift` | map condition → `{slope, interval: [low, high]}` | |
| `disagreements` | list of blind ids where key and judge differ on done | |

### `r<n>/9-outcome.yaml`

| Key | Type | Rule |
|---|---|---|
| `outcome` | `pass` \| `fail` | |
| `checks` | list of `{compares, gap, mean_difference, interval, pass}` | sealed statistics, one per gate check |
| `changed_from_parent` | `changed` \| `reversed` \| `unchanged` \| `unresolved` | absent in r1; R87 |
| `parent_comparison` | `{target, mean_difference, interval: [low, high]}` | absent in r1; `target` the hypothesis' `failing_demand` |
| `instruction_breaches` | number | keep rank: sealed mean breaches per reply over gate demands |
| `completion_passed` | `true` \| `false` | keep rank: the `completion` check's result |
| `words` | integer | keep rank: R21 word count of `2-instruction.md` |
| `cost` | `{replies, input_tokens, output_tokens, seconds}` | this revision's asks; token sums null when any reply's are |

## Reader tools

Fact: `tools: []` registers as "All tools" and grants twelve tools (M). It is excluded.

| # | Construction | Documented | Expected |
|---|---|---|---|
| T1 | `tools: Read` plus `disallowedTools: Read` (allowlist emptied by deny) | errors.md: "If you leave the `tools` list empty, or `disallowedTools` removes every entry in it, Claude Code also skips the refusal and launches the subagent without tools." | zero tools |
| T2 | `disallowedTools` naming every tool, no `tools` | same sentence; `disallowedTools` "Tools to deny, removed from inherited or specified list" | zero tools; fragile: a new tool name escapes |
| T3 | `tools: <one inert tool>` | allowlist parsing measured (`Skill, Write` held exactly, M) | one tool that reads nothing, writes nothing, reaches no network, launches nothing |
| T4 | `tools: <unresolvable name>` | "If no entry in the list resolves to a tool, the subagent usually fails to launch" | refused launch; excluded |

Measurement (main thread of the neutral session, definitions under the series folder's `.claude/agents/`): for T1, T2, T3 (inert candidates taken from the tool names a T2 transcript lists), launch with "Hello." and with a message inviting a file read; read the registry line, the transcript's tool list, and any `tool_use`. Pick the first construction in order T1, T3, T2 whose transcript lists zero tools, or exactly the one inert tool with no `tool_use` in either launch.

Fallback: with none qualifying, generate T3 with the tool of least reach and rely on R41, which refuses every reply whose transcript holds a `tool_use`. When a tool can act before collect, agent readers stop at v1 and series run command readers.

## Prerequisites

Each runs before build; each result is a journal line. The requirements state the primary behavior. A failed prerequisite amends the requirements its row names before build, replacing their text with the fallback; the CLI carries one behavior and reads no prerequisite record.

| # | Unmeasured | Measurement | Amendment on failure |
|---|---|---|---|
| PR1 | Reader tool construction | `## Reader tools` | `## Reader tools` |
| PR2 | A generated definition with a full model ID in `model` serves that ID | launch; read `message.model` | R33, R48: `model` is the alias the probe measured to serve the pinned ID, from a constant map; records keep the full ID; R41 and R52 compare the served ID |
| PR3 | Judge blinding under the neutral login: `Skill, Write` held, `manifesto:manifesto-oath` loads, a planted file unreadable | rerun M's judge probe in the neutral session | none: judges cannot be blinded; agent judging waits, as agent readers do, and the build stops |
| PR4 | No CLAUDE.md (including `$HOME/.claude/CLAUDE.md`) and no SubagentStart text reach an agent launched from the neutral session; what `session_context` holds | read a transcript's attachments | R33, R48, R55: definitions add `omitClaudeMd: true`; R3: `$HOME/.claude/CLAUDE.md` is refused too; R41: a constant `session_context` is accepted |
| PR5 | manifesto 3.2.0's SessionStart clone into `<project>/.claude/manifesto-repo` fires in a series folder. Source (H): `session-start.sh` exits before `ensure_repo` when `parse_config.py` finds no `you:` in `<project>/.manifestos.yaml` or the project `CLAUDE.md`; it reads only the project dir | start the neutral session in a fresh series folder; `ls -a .claude/` after start, after `/compact`, after a judge launch | R115, R125: hashes and `inputs` skip `.claude/manifesto-repo/`; R7: `series status` reports the clone; R3 already refuses `.manifestos.yaml`; agents cannot read it |
| PR6 | `SendMessage` to a finished reader enters as a new user turn and the transcript records each turn's reply | three-turn probe | R116: refuses a `drift` check on an agent reader; R38: conversations are not launched |
| PR7 | Definitions written into the series folder's `.claude/agents/` register in the neutral session's main thread without restart | write one; wait for the listing delta; launch | R109: skills order a session restart after each `prepare` and stage one |
| PR8 | A subagent transcript records input and output tokens per reply | read `usage` in a reader transcript | R40: agent reply tokens null; R85 already refuses `tokens` then |
| PR9 | A judge's Write to its verdict path lands without a permission prompt | launch one judge in default mode | R109: `start-series` adds to the bare login's `settings.json` allow rules for `Write(~/instruction-series/**/7-verdicts/**)` and `Write(~/instruction-series/**/6-judge/calibration/**)` |
| PR10 | Twenty agents run at once; the twenty-first is refused | launch 21 | R39: waves of ten |
| PR11 | The Agent tool's prompt reaches the agent byte-exact as its first user message; the description stays out | diff transcript against message | none: R41 already refuses a mismatch; R109 adds the paste order |
| PR12 | `uv run --project <cache version dir> --locked` builds `.venv` in the installed copy and runs from any cwd | install; run `instruction-eval --help` in a temp dir | R101: the launcher sets `UV_PROJECT_ENVIRONMENT` to `${XDG_DATA_HOME:-~/.local/share}/instruction-eval/<version>` |
| PR13 | `/login` under the bare login, and a full reader run under it: `series new`, `reader prepare r1`, one reader per condition launched from `claudes run readers`, `revision collect r1` passing R41 | end to end on a two-task fixture series; read exits and one transcript's attachments | R34, R96: the manual setup below at `~/.claude-instruction-eval-readers`, which R34 accepts in place of `~/.claudes-bare/` |
| PR14 | Subagent transcript layout under a config dir: path pattern of transcripts and meta files for a session started in the series folder; meta holds the agent type | list the bare login's `projects/` after PR13; read one meta file | R38, R40, R41: the launch list appends a marker line `ie:<r>:<condition>:<task>:<p>` to each message; R40 finds transcripts by searching the config dir for it; R41 compares the message without it |
| PR15 | A definition with an empty body launches and the agent receives no system text of its own beyond the harness default | launch `ie-reader-r1-empty` from PR13; read the transcript | R29: `empty` is one newline |

Neutral login setup (C2: `claudes new --bare` shipped; `/login` and a full reader run unverified):

| Step | Action |
|---|---|
| 1 | Install `instruction-eval` from the marketplace (the command refuses a plugin missing from the shared registry). |
| 2 | `claudes new --bare readers instruction-eval@my-claude-skills manifesto@my-claude-skills` → `~/.claudes-bare/readers`: those two plugins enabled, no `CLAUDE.md`, skills, or agents, plugins linked to the shared cache. |
| 3 | `claudes run readers` once; `/login` (same account). |
| 4 | Per series: `cd <series folder> && claudes run readers`; `claudes path readers` prints the config dir. |

Manual fallback (C): the config dir `~/.claude-instruction-eval-readers`; its own `settings.json` with the two plugins enabled; `plugins/` linked to `~/.claude-shared/plugins`; no `CLAUDE.md`, `agents/`, or `skills/`; `CLAUDE_CONFIG_DIR=<dir> claude` and one `/login`.

## Migration

LLM_MANIFESTOS sessions, old to new:

| Old | New |
|---|---|
| `just install-digest-eval`; `digest-eval` on PATH | install `instruction-eval`; `bin/instruction-eval` on the Bash PATH; `uv` the one prerequisite; `claudes new --bare readers …` once |
| `digest-eval stale <slug> --digest <p>` | none; R9 and R115 refuse any changed byte |
| `evals/<slug>/` in the repo | `instruction-eval series new <slug> --instruction digests/<slug>.md --source manifestos/<slug>.md --reader-kind agent` → `~/instruction-series/<slug>/` |
| `write-eval-spec`, `spec.json` | `list-demands` (2), `write-tasks` (3), user-written 4, 5, `calibrate-judge` (6), `freeze-series` (7, 8) |
| `write-eval-tasks`, `tasks.json`, `family`, `answer` | `write-tasks`, `3-tasks.yaml`, `tempts`, `answer_key` |
| `sessions`, `t<turn>.json` | `conversations`, `repeat-<p>/turn-<k>.yaml` |
| `calibrate-eval-judge`, `calibration.json` | `calibrate-judge`, `6-judge/calibration.yaml`, `anchors.yaml` |
| `pilot-1`, `digest-eval reps` | retest: `7-gate.yaml` `repeats` (≥ 2), `revision ask r1`; `series freeze` prints the least repeats; a too-noisy series is the pilot of the next |
| `digest-eval conditions … cut-<n>` | `reader prepare r<n>` |
| `digest-eval run <slug> cut-<n> --only digest` | `revision ask r<n> --conditions instruction`; `revision collect r<n>` |
| `pi` adapter | command reader: `command`, `fingerprint` in `5-reader.yaml`; a wrapper turning R35's stdin into `pi` arguments |
| `judge-by-agents`; `blind`, `brief`, `collect`, `script-judge`, `--borrow` | `judge-replies`; `revision blind`, `judge prepare`, `judge collect`, `revision detect`; borrowing built in (R69) |
| `key.json` | `6-origins.yaml` |
| `judge/<packet>.verdict.json` `violations` | `7-verdicts/<packet>.yaml` `breaches` map, `kind` |
| `script.json` | `7-detectors.yaml` |
| `digest-eval score … --previous`, `gate`, `gate.json` | `revision score r<n>`, `revision gate r<n>`, `9-outcome.yaml` |
| `changed_vs_previous` true/false | `changed_from_parent` `changed`/`reversed`/`unchanged`/`unresolved`, on the failing demand in the predicted direction |
| `write-eval-record`, `ledger.jsonl`, `digest-eval ledger` | the CLI writes every record; `series status`; hash chain in `2-revision.yaml` |
| `diagnose-eval-failures`, `hypothesis.md` | `diagnose`, `r<n>/1-hypothesis.yaml`; cause to the writer |
| `recut-digest` apply-one-change, save-the-cut, `cut.json` | writer edits; `revise`, `revision new`, `2-revision.yaml` |
| `test-digest` | `freeze-series` then `measure-revision` |
| conditions `none`, `digest`, `full`, `terse`, `ablation-NN` | `empty`, `instruction`, `source`, `aim`, `omit-<n>` |
| split `dev`, `test` | `open`, `sealed` |
| canonical cut by owner after the numbers | `series keep` by `keep_rule` |
| `tests/check_skills.py` | retired (J53) |

Writer skills stay in LLM_MANIFESTOS:

| Writer skill | Keeps | Calls |
|---|---|---|
| `write-digest` | read and bind, sentences, order, boundaries, standing line, Strunk, shape, save `digests/<slug>.md` | `instruction-eval:list-demands` for save-the-demand-list; `instruction-eval:check-coverage` for check-against-the-source |
| `write-stack-digest` | members, binding, merge and resolve, resolutions record, order, object, standing line, shape, save | `list-demands` over the stack's sources; `check-coverage` for check-against-the-members |
| `recut-digest` | apply-one-change craft (Strunk, boundary, object), word limit | `instruction-eval:revise` for take-the-hypothesis and save-the-cut |
| (any) | the cause list from `diagnose-eval-failures` L26 | receives the failing demand and replies from `diagnose` |

Finished JSON series stay as they are (J52).

## Open

Settled, from rulings and facts:

| # | Item | Settlement | Basis |
|---|---|---|---|
| O1 | Neutral login setup command | `claudes new --bare readers …`, `claudes run readers`; PR13 verifies `/login` and a full reader run | J111; C2 |
| O2 | DL's help order puts `judge calibrate` before the retest ask | the Commands section's order of work | S:calibrate L12; R62 |
| O3 | Stored keys a load can derive: `3-coverage.yaml` `sentences`, `4-conditions.yaml` `controls`, `5-reader.yaml` `kind`, reply `reader_kind`, the plan copies in `6-judge/calibration.yaml` | kept as DL fixes them; disagreement refused (R8, R16, R25, R115); recommend dropping them in a later minor version | correct-by-construction; simple-made-easy |
| O4 | DL's turn path lacks a repeat level | `repeat-<p>/` between conversation and turn | J87; R43 |
| O5 | No verb for the `unresolvable` stop | `series stop --reason <text>` | J92; R91 |
| O6 | DL's stop `inconclusive` has no producing rule | dropped; `unresolved` outcomes go to diagnosis | settled stop list |
| O7 | Outcome words `no_effect`, `inconclusive` vs DL's `unchanged`, `unresolved` | DL's words kept | DL; P2 |
| O8 | DL puts `kind` in the reply record | `kind` in the judge's verdict | P5; one fact, one home |
| O9 | Judge binding without a source | `{SOURCE}` renders the demand list | J55; J57 |
| O10 | Reader template "empty tools" | `## Reader tools` | M; J110 |
| O11 | `--conditions` | kept as DL fixes it | DL |
| O12 | Anchor re-judging cap | three judgings per packet; the third miss forces recalibration, which a new series carries (R51) | K; R124 |
| O13 | Keep rule ignores completion | candidates limited to revisions that passed `completion`, a required check (R79, R93) | K |
| O14 | Calibration user keys braided with CLI stamps in `6-judge/calibration.yaml` | user keys in `attempt-<n>/plan.yaml`; `calibration.yaml` written once by the accepting stage two | R124; d3; r2 c8, c16 |
| O15 | `changed_from_parent` on the total vs the hypothesis on one demand | measured on the failing demand (R87) | d26 |
| O16 | Keys DL places in a file another author writes, moved to keep one author per file: `7-gate.yaml` `noise` → `8-frozen.yaml` `noise`; verdict `judge_model` → `7-collected.yaml`; `1-hypothesis.yaml` `noise` dropped (read from `8-frozen.yaml`); the `--repeats` flag → `7-gate.yaml` `repeats`; sealed `8-scores.yaml` rows → none stored, sealed statistics in `9-outcome.yaml` | moves and removals, no renames; new files `7-collected.yaml`, `attempt-<n>/plan.yaml`, `attempt-<n>/agreement.yaml`; verdict files gain `-<k>` | R124; R125; r2 c1, c2, c5, c29 |
| O17 | Re-judging or topping up r1 rewrites files | r1 asked once at `repeats`; each judging a new file; a too-noisy retest restarts the series as its pilot | R71; S:write-eval-tasks L33 |
| O18 | The live instruction and the working brief were hashed while their authors edit them | both are working copies, never hashed; each revision and each calibration attempt snapshots them once (R129); `series keep` writes the kept snapshot back to the live path | R124; R125; r3 d1, d2, d3 |
| O19 | A revision failing `completion` alone had no hypothesis target | `failing_demand: completion`, predicted movement on the done rate, change noise `done_change` (R67, R73, R87, R91) | r3 d14 |
| O20 | Requirements carried two behaviors chosen by unmeasured prerequisites | each requirement states the primary behavior; a failed prerequisite amends the named requirements before build (`## Prerequisites`) | r3 d21 |
| O21 | DL names that changed shape in round 4, no renames: new file `4-placebo-source.md` (the placebo source's snapshot); verdict paths `7-verdicts/<packet>/k<k>.yaml` and definitions `ie-judge-<r>-<packet>-k<k>`; `changed_from_parent` gains `reversed` | R27, R48, R87, R129 | r4 d1, d2, d8, d10 |

No owner questions remain.

## Summary

Every hash in the series now names a series file: the placebo source joins the live instruction and the working brief as a working copy snapshotted once (`4-placebo-source.md`), and the Commands table splits hashed Reads, which equal each record's `inputs`, from unhashed External reads. Judging attempts use exact names (`ie-judge-<r>-<packet>-k<k>`, `7-verdicts/<packet>/k<k>.yaml`) with pending judgings never counted, `changed_from_parent` reads the predicted direction and gains `reversed`, and a single expected reply set E(r) governs ask, collect, blind, freeze, and gate. Round 4 fixes all 28 findings and rejects none; those fixes are unverified, as `## Residue` states, and the spec holds 129 live gated requirements with no owner questions.

## Revision log

### Round 1 (`spec-check.yaml`)

| Defect | Status | Change |
|---|---|---|
| d1 | fixed | R107 lists the eleven skills; the Commands table maps commands to skills (R108) |
| d2 | fixed | Commands table; `judge calibrate` stage chosen by record state (R55) |
| d3 | fixed | `series new` copies the brief (R5); `calibration.yaml` user keys via `calibrate-judge`, `anchors.yaml` all C by stage two; `per_packet` moved (O14) |
| d4 | fixed | R118: `reader prepare` writes `<r>/4-conditions/<condition>.md` for every kind |
| d5 | fixed | Neutral session required for judges in every series; R3, R4 for every kind; R34 applies to agent readers at `reader prepare` and to every kind at `judge prepare` and stage one (R96) |
| d6 | fixed | R48 login check; R121 judge transcript refusals |
| d7 | fixed | R3 stops strict ancestors at `$HOME` and skips `$HOME/.claude/CLAUDE.md`; PR4 measures it |
| d8 | fixed | R34 refuses any plugin set but the two exact keys, both true |
| d9 | fixed | R32 defines the model pattern; PR2's alias lives only in generated definitions, records keep the full ID |
| d10 | fixed | R44 lists the banned words and the match rule; `source` allowed |
| d11 | fixed | R47 defines each kind and the done rule |
| d12 | fixed | R120 defines packets; packet record added |
| d13 | fixed | R40 match key and turn split, R42 ordering, R23 unique messages, R52 judge transcript; layout measured by PR14 with a marker fallback |
| d14 | fixed | R35 stdin carries the message history |
| d15 | fixed | R35: `model` from the fingerprint, tokens null |
| d16 | fixed | R119: `revision collect` validates only for command readers |
| d17 | fixed | R74: `revision score r1` writes `noise` before freeze from sealed replies, half-widths and variances only |
| d18 | fixed | R73 defines σ² by sample variance (any n), T as sealed units, and noise for completion, drift, and each demand |
| d19 | fixed | R72 fixes resamples, seed, unit, statistic, and `z` |
| d20 | fixed | R71 tops up and re-judges r1 only before freeze; R83 requires r1 repeats = `repeats` at freeze |
| d21 | fixed | R117 defines the two states of `7-gate.yaml` |
| d22 | fixed | R116 lists every freeze refusal |
| d23 | fixed | R115 `inputs` hashes; R116 refuses stale r1 records |
| d24 | fixed | R36 and R116 compare fingerprint hashes with r1 replies |
| d25 | fixed | R64 defines the sentence alignment and each change kind |
| d26 | fixed | R87 measures the failing demand; R88 retired |
| d27 | fixed | R89 resolves borrowed origins in the named revision |
| d28 | fixed | R94 overwrites the file at the recorded path, outside `8-frozen.yaml` |
| d29 | fixed | R58 defines the rating used; R59 adds a `self_difference` threshold; `scale` reported only |
| d30 | fixed | R57 gates `rater_model` ≠ `judge_model`; strength is the user's choice |
| d31 | fixed | R27 defines word and cycling; echo gate added; demand-freeness a stated attestation |
| d32 | fixed | R28 reads `1-source/` |
| d33 | fixed | R81 uses the `instruction-vs-empty` gap |
| d34 | fixed | R76 excludes null `done`; keyless tasks fall back to the judge |
| d35 | fixed | R22 allows no conversations; R116 ties conversations to `drift`; PR6 fallback consistent |
| d36 | fixed | R103 lists modules; R111 drops the authorship clause; R114 names the scopes |
| d37 | fixed | R115 re-hashes `inputs` on every load, covering replies, verdicts, scores, and outcomes after freeze |
| d38 | fixed | every record heading carries its full path |
| d39 | fixed | R12 applies R14 and R21's word regex to replies; R14 counts a fenced block as one sentence |
| d40 | fixed | R90 reads `changed_from_parent` |
| d41 | fixed | R123 requires a gated, failed, unstopped parent |
| d42 | fixed | reply `cost` null allowed for agent transcripts without usage; R85 refuses `tokens` then |
| d43 | fixed | R122 defines the draw and the exhausted-pool refusal |
| d44 | fixed | R8 refuses a reader-kind mismatch; listed in O3 |
| d45 | fixed | R15 defines `imported` as the refusal message's word |

### Round 2 (`spec-check-r2.yaml`)

Root fix for c1 and c2: R124 (one author per file, written once), R125 (no write after a hash), R115 (key-level `inputs` for user YAML).

| Defect | Status | Change |
|---|---|---|
| c1 | fixed | R115 hashes only the `7-gate.yaml` keys a record reads; R117; score runs after freeze |
| c2 | fixed | `revision score` writes open rows only; `revision gate` writes `9-outcome.yaml` (`checks`, `parent_comparison`); noise lives in `8-frozen.yaml`; R75, R125 |
| c3 | fixed | order of work writes `4-conditions.yaml` (step 4) before `tasks check` (step 5) |
| c4 | fixed | step 11 lists hypothesis, `revision new`, coverage and its check, then the r2 pipeline; calibration and repeats stay r1-only |
| c5 | fixed | `7-gate.yaml` `repeats` written at step 4 and read by ask and collect (R42, R117); `--repeats` retired (R70) |
| c6 | fixed | R13 defines gate demands, fixed by r1's coverage |
| c7 | fixed | R15 refuses an empty list |
| c8 | fixed | mixed-author files removed (R124, O14, O16); `coverage check` is pure and rerun by ask (R17) |
| c9 | fixed | R115 allows absolute paths; R126 covers markdown outputs |
| c10 | fixed | R118 defines `instruction` and `omit-<n>` bytes from R14 spans |
| c11 | fixed | R33, R48 fix `name` and `description` |
| c12 | fixed | PR15 with a one-newline fallback (R29) |
| c13 | fixed | R127 recomputes condition files and definitions before use |
| c14 | fixed | R10 states completeness as the user's attestation; the gate checks structure |
| c15 | fixed | stage-one `inputs` cover plan, brief, sample (R56) |
| c16 | fixed | per-attempt folders; `calibration.yaml` written once (R55, O14) |
| c17 | fixed | stage one prints the launch list; stage two validates ratings by R50, R52, R121 (R59) |
| c18 | fixed | R51 uses breach and done agreement only; `anchors_per_packet` ≥ 3 (R61) |
| c19 | fixed | a third failed judging restarts the series, so nothing resets (R51, O12) |
| c20 | fixed | R76 keeps the key override to `done_by: answer-key` |
| c21 | fixed | R67 refuses a failing demand with zero breaches among `replies_read` |
| c22 | fixed | R64 checks the hypothesis' change directly, so either naming of a swap passes |
| c23 | fixed | R72 names PCG64 and numpy's linear quantile |
| c24 | fixed | R73 lists the compares noise covers; status prints it without needing checks |
| c25 | fixed | R13 fixes gate demands at r1; R17 refuses a different dropped set |
| c26 | fixed | R85 ask refusal; R90 `capped` with reason `budget` |
| c27 | fixed | R85 gives the prediction formula |
| c28 | fixed | prerequisite branches fixed at build; no runtime record |
| c29 | fixed | hypothesis `noise` dropped; read from `8-frozen.yaml` (O16) |
| c30 | fixed | R5 refuses duplicate basenames |
| c31 | fixed | R1 resolves relative paths; R3 checks ancestors to `/` |
| c32 | fixed | `repeat-<p>` for repeats |
| c33 | fixed | R11, R12, R20 name Python `re`, no flags, `finditer`, `search` |
| c34 | fixed | R28 defines frontmatter removal and joins |
| c35 | fixed | R34 refuses a non-empty or linked `skills/` |
| c36 | fixed | R81, R116 refuse near-source without sources |
| c37 | fixed | R122 alphabetical order, start (n − 1) mod count |
| c38 | fixed | calibration `inputs` cover sampled files only; no top-up exists (R56, R71) |
| c39 | fixed | R91 reads the latest gated revision; ungated revisions are not candidates |

### Round 3 (`spec-check-r3.yaml`)

Root fixes: R129 and R125 (external files snapshotted once; no hash names a file outside the series); R56 (each calibration attempt hashes only its own brief snapshot, plan, and sample); R86, R90, R93 (keep ranks written once by `revision gate`, `kept` computed by the stopping command); R48, R51 (judging k counted from definitions).

| Defect | Status | Change |
|---|---|---|
| d1 | fixed | R115 bars external files from `inputs`; R63, R129 snapshot the live instruction; R125 test runs through r5 |
| d2 | fixed | R124 covers only files inside the series; R94 writes the kept snapshot to the external live path |
| d3 | fixed | stage one snapshots the brief into the attempt (R55, R129); R56 limits an attempt's hashes to its own files |
| d4 | fixed | R48 counts k from definitions; R51 defines a failed judging, an absent verdict included |
| d5 | fixed | R75's grep limited to `8-scores.yaml`, `9-outcome.yaml`, and status output |
| d6 | fixed | R21 checks the placebo source against tasks and sources; R65 checks later revisions against the placebo snapshot |
| d7 | fixed | R14 defines a total tokenizer over markdown units, closers, abbreviations, nesting |
| d8 | fixed | R118 defines whitespace removal per sentence position |
| d9 | fixed | Reads column completed; R115's test compares `inputs` keys with it |
| d10 | fixed | `level` and `done_by` written at step 4 (R117) |
| d11 | fixed | R85 defines `T_open`; the ask refusal applies from r2 with a ceiling |
| d12 | fixed | R86 stores `instruction_breaches`, `completion_passed`, `words`; R90, R91 compute `kept`; R93 reads only stored ranks |
| d13 | fixed | R67 reads detector demands from `7-detectors.yaml` |
| d14 | fixed | `completion` as a hypothesis target (R13, R67, R73, R87, R91; O19) |
| d15 | fixed | `change` gains `sentence` and `to`; `move` sets `old` and `new` to the moved text |
| d16 | fixed | R72 fixes instruction minus X for every comparison; R80 cites it |
| d17 | fixed | transcripts recorded by `transcript_hash`, never inputs (R40, R52, R129); R115 names the missing-input refusal |
| d18 | fixed | R60 rounds half away from zero; R58 and R73 define null and refusal cases; anchors need a reference `done` |
| d19 | fixed | R45 defines `{SOURCE}` rendering for any number of sources |
| d20 | fixed | R44 refuses a brief without `manifesto:manifesto-oath` |
| d21 | fixed | requirements state one behavior; prerequisite rows name the requirements they amend; manual dir fixed at `~/.claude-instruction-eval-readers` (O20) |
| d22 | fixed | R23 refuses ids with `--` or ending in `-turn-<digits>` |
| d23 | fixed | R11 reserves `overreach` and `completion` |
| d24 | fixed | R21 refuses a missing or wordless placebo source |
| d25 | fixed | R5 refuses an unclosed frontmatter source at `series new` |
| d26 | fixed | R106 limits closed enums to set-valued flags and validates `--conditions` |
| d27 | fixed | `reason` present only for `unresolvable` and budget caps |
| d28 | fixed | `sigma.breaches` and `sigma.done` typed as maps |

### Round 4 (`spec-check-r4.yaml`)

Root fixes: R129 and R27 snapshot the placebo source; the Commands table splits Reads (exactly the `inputs`) from External (never hashed), and R115's test enforces it; R48 names judgings exactly; R87 reads `direction`.

| Defect | Status | Change |
|---|---|---|
| d1 | fixed | `placebo_source` is a path only; `4-placebo-source.md` is hashed at freeze (R129, `8-frozen.yaml`) |
| d2 | fixed | R27: raw snapshot first, `placebo.md` derived from it, R127 recomputes from it; ask and collect read it |
| d3 | fixed | Reads and External columns; R115's test excludes External; `judge calibrate` Reads aligned with R56 |
| d4 | fixed | `revision new` reads the parent's `7-collected.yaml` and `r1/3-coverage.yaml` |
| d5 | fixed | `series keep` reads `series.yaml` |
| d6 | fixed | stage two reads `.claude/agents/ie-calib-<n>-*.md` |
| d7 | fixed | `revision gate` qualifies hypothesis and parent reads with (r > 1) |
| d8 | fixed | R87 reads `direction`; `changed` needs the predicted side; `reversed` added |
| d9 | fixed | R47 defines `blank` without a banned word; test that the template passes R44 |
| d10 | fixed | R48 exact names and pattern with a `-k` suffix; verdicts under `7-verdicts/<packet>/`; fixture with `t1` and `t1--omissions` |
| d11 | fixed | R118 states removal when no blank line exists; fixtures added |
| d12 | fixed | R35 refuses a failed reply without writing it, and a rerun asks only missing replies; R42 likewise for collect |
| d13 | fixed | R130 defines E(r); collect, blind, freeze, gate refuse on a gap |
| d14 | fixed | R48 defines pending and returned judgings; pending never counts and blocks a new definition (R51, R128) |
| d15 | fixed | order of work step 1 runs `series new` in any shell, then starts the neutral session (R2, R109) |
| d16 | fixed | `series freeze` reruns `demands check` and `tasks check` (R116) |
| d17 | fixed | R36 hashes the canonical YAML of the parsed fingerprint |
| d18 | fixed | R131: turn replies count only toward drift |
| d19 | fixed | R116 refuses null demand or `done_change` noise |
| d20 | fixed | R59 requires enough anchors per task at acceptance |
| d21 | fixed | R117 lists the key-level reads per command, matching the table |
| d22 | fixed | R20: the key sees the full reply, fences included |
| d23 | fixed | R85 defines `turns` |
| d24 | fixed | `units` typed as an integer |
| d25 | fixed | R72 defines completion units and the null case |
| d26 | fixed | multi-valued flags repeat (R106, Commands table) |
| d27 | fixed | `series status` mapped to `freeze-series` and `measure-revision` (R109) |
| d28 | fixed | R5 and `revision new` refuse an instruction with unclosed frontmatter |

## Residue

Round-4 fixes are unverified: no check round read the spec after them. Rejected findings: none; all 28 were verified against the text and fixed.

## Amendments after build (2026-10-16T14:51+0300, orchestrator, reversible choices settled from the owner's standing words; the requirements above stay as frozen)
Each follows from R115 (a record's `inputs` hashes only the keys the command read); the Commands table's Reads cells are amended to name what the code reads:
- `judge calibrate` stage one also reads `attempt-<n>/sample.md` (its own earlier write is not an input; the sample it draws is) and, for a series without a source, `r1/3-coverage.yaml#demands`.
- `revision blind` also reads `<r>/2-instruction.md` (the sentence count for the `omit-<n>` conditions).
- `judge collect` also reads `5-reader.yaml#model` and, for a sourceless series, `r1/3-coverage.yaml#demands`.
- `revision new` also reads `7-gate.yaml#done_by`.
- `revision gate`'s second record `9-stop.yaml` hashes the gate's own `<r>/9-outcome.yaml` plus `7-gate.yaml#budget`.
- For r > 1, `revision blind`, `detect`, `score` and `gate` read r1's control replies only (R69, R130), not all of `r1/5-replies/**`.
- Records: `8-scores.yaml` `mean_difference` and `done_rate`, and `9-outcome.yaml` `checks[].mean_difference`, `parent_comparison.mean_difference` and `parent_comparison.interval`, may be null when no unit is paired (R72, R87).
- Defect, not amendment: `judge calibrate` stage two hashed `reference-user.yaml` as a whole file; R115 requires per-key hashing (`#verdicts`).
