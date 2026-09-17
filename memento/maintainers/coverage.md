# memento — As-Built Coverage

The plugin's as-built state against the slicing plan, the residue each shipped skill carries, and what a change to a skill requires.

Three documents stand behind this one. The settled design is `memento/ONTOLOGY.md`, authoritative and changed only by owner ruling. The inventory, the item → slice accounting, the slice contracts, and the five-check verification protocol are `orchestration_log/history/2026-09-16/reviews/memento-slicing-plan.md`. Every ruling that governs the build, with its rationale, is `orchestration_log/reference/decisions.md`.

## What the build reached

Every skill slice the plan names, at `memento/skills/`, with `skill-creation` among them as the routine-creation slice. The shipped default schema at `memento/config/default.yaml`.

These slices remain unbuilt, with the inventory items each was to carry:

| Slice | Path | Items |
|---|---|---|
| Orientation hook at wake | `memento/hooks/`, `templates/orient.txt` | 29, 45, 56, 100, 126 |
| Config parser | `memento/hooks/read-config.py` | Realizes schema-resolution's resolution rule |

The orientation hook after attenuation is out of scope, not unbuilt. Attenuation fires at the owner's whim or the system's, never the agent's, so nothing detects it, resists it, or decides anything about it. Tracing it as an event kind is the whole available response, and `event-capture` carries that. `decisions.md`, 2026-09-17.

Two skills are specified and unwritten. `decisions.md`, 2026-09-17, holds both.

`/setup` explains the system to an owner new to both the concept and the implementation and sets up the configuration, sourcing from the owner what only an owner decides and settling the rest. It is the one skill that may read `ONTOLOGY.md`, and it must, which makes the ontology a shipped runtime dependency with a single reader rather than a maintainer document travelling with the plugin.

`memento:init` points at `pat-down` and `span-closure` and instructs the reader to follow every skill reference to maximum depth. It carries no procedure of its own.

The plan's wave 4 has not run: plugin-validator over the whole plugin, resolution of every named path, the prose-carriage audit over the full slice set. `memento/README.md` is current for the shipped skills.

The item → slice rows have not been verified against the shipped skill bodies. The plan's number floor holds for the plan, not yet for the plugin.

## Reference graph, as built

Verified by grepping each shipped body for every sibling name.

| Skill | Names in its body |
|---|---|
| authority-check | corpus-reconciliation, owner-ruling, record-writing, skill-creation |
| corpus-reconciliation | authority-check, event-capture, record-writing, schema-resolution |
| event-capture | authority-check, record-writing, schema-resolution |
| owner-ruling | authority-check, event-capture, record-writing |
| pat-down | authority-check, event-capture, schema-resolution, staging-relay |
| record-promotion | authority-check, record-writing, schema-resolution |
| record-writing | authority-check, corpus-reconciliation, event-capture, owner-ruling, record-promotion, schema-resolution |
| schema-resolution | event-capture, record-promotion |
| skill-creation | — |
| span-closure | event-capture, record-writing, schema-resolution, staging-relay |
| staging-relay | authority-check, event-capture, record-writing |

`record-writing`'s frontmatter also names event-capture, record-promotion, staging-relay, span-closure, corpus-reconciliation, and owner-ruling. That list is a trigger enumeration of callers, not a dependency.

`skill-creation` takes inbound references only. The ten may name it; it names none of them, and its row stays empty by ruling. `decisions.md`, 2026-09-17.

The built graph departs from the plan's:

The plan records schema-resolution and authority-check as leaves. Neither is. `skill-creation` is the graph's only leaf.

These pairs name each other: authority-check ↔ corpus-reconciliation, authority-check ↔ owner-ruling, authority-check ↔ record-writing, corpus-reconciliation ↔ record-writing, event-capture ↔ record-writing, event-capture ↔ schema-resolution, owner-ruling ↔ record-writing, record-promotion ↔ record-writing, record-promotion ↔ schema-resolution. The plan's graph is acyclic; the built graph is not. The plan's wave ordering no longer derives from it.

The plan gives record-writing one outbound edge. It has the most of any skill.

No skill names pat-down or span-closure. Both are entered by occasion alone. Each reaches every other skill but the other, so the pair is the minimal cover and no single entry point reaches the whole graph.

## Per-skill residue

Residue is what a skill ships with unclosed after its last compliance report and its last usability report. Three filters strike a finding before it reaches this list: a sibling skill named by name is never a defect; a term another slice owns needs only a gloss sufficient to parse its sentence, and only a term the skill itself owns can be residue; an enumeration whose items are defined immediately after satisfies define-at-first-use. `decisions.md` carries all three with the evidence behind each.

**pat-down.** Both its last findings — the `situation` / `found state` term collision and the missing span-start marker in the journal read — were closed by edits made after both reports. A compliance audit of the shipped text found 0 violations: `what the found state is` at line 66 and the journal's backward read bounded at the span-event event-capture writes both hold. `orchestration_log/recon/2026-09-16/pat-down-shipped-compliance.md` holds the report.

**event-capture.** A trace names its event in no stated form; a slug, a sentence, and an identifier each satisfy the instruction. The receipt trace's "from whom" does not settle the proximate deliverer against the originator. `<treat-the-working-text-as-lost>` requires arriving content written where it outlives the work, and `<write-the-receipt-trace>` forbids copying that content into the trace, while no other durable home is named. Its compliance residue is entirely corpus vocabulary.

**record-promotion.** A newly set goal has no route from the bench: `<settle-the-move>` forbids skipping a tier, no dossier gate admits a goal, and `<write-the-move>` keeps the goal off the dossier outright. `<take-the-owners-word>`'s "grounds" is tied neither to `<check-the-ground>`'s ground nor to `<shape-the-goal>`'s rationale. Carrying a parent's constraints down to a subgoal states no form — copy or reference.

**staging-relay.** A posted directive has no stated medium or location. Rescheduling a tripwire reads as cancel-and-lay or as amend-in-place; supersession and the two declared end-modes go unreconciled. `<watch-no-running-process>` pairs its positive half with the prohibition of a different concern.

**span-closure.** `foreseeable end` first appears in the tag name `<enter-at-a-foreseeable-end>` and is defined two sentences later. A summary's distinguishing set and occasion may be carried neither by its content nor by a named field, and nothing else is named to carry them. "Written down as undone" names no mechanism. `<let-the-end-come>`'s closing clause reads as a gate over the four steps or as an override of that gate.

**corpus-reconciliation.** A fault is defined as a defect inside a record, while an orphan's defect is the map's omission and adoption stands among the fault repairs. The quarantine and retirement records `<repair-each-fault>` requires have no declared kind, home, author, or date, and nothing distinguishes the two shapes. A refused orphan's disposition — quarantine replacing adoption, or stacking with it — follows from the one-to-one hold and from no instruction. Retirement turns on a "decision" whose actor is unnamed. The map's row structure is fixed and its serialization is not. "Aged" carries no threshold.

**owner-ruling.** `<rule-on-a-routine>`'s channel precondition sits after `<carry-out-the-shape-given>`, which performs the act that precondition must precede; a linear read ratifies an online-sourced routine before reaching the refusal. "Send a refused ruling back to the owner for another shape" names no form for the request. "Who wrote it and when" has no referent for a scope, the one thing ruled on that nobody authored.

**schema-resolution.** Its last compliance report's two violations — one sentence carrying two instructions, and a record-keeping instruction with no paired prohibition — were closed by an edit made after the report. A compliance audit of the shipped text found 1 violation: in the pointer definition at line 18, `home` appears at its first occurrence in the document with no definition; the only gloss for it arrives at line 34. The line-40 split and the missing-or-unreadable-target rule both checked clean. `home` belongs to `record-writing`, which owns homes; whether it needs a definition here or only a gloss sufficient to parse its sentence turns on the term-ownership ruling in `decisions.md`. It names the shipped default as `config/default.yaml` "in this plugin", with no root, so no concrete path is derivable from the skill's own text. `orchestration_log/recon/2026-09-16/schema-resolution-shipped-compliance.md` holds the report.

**record-writing.** The five tiers are named under one shared description, and nothing tells one from another. "A record that instructs later work" goes unsettled against descriptive content a later reader relies on. The supersession link is load-bearing for the superseded status and has no stated home, the mark's field list being closed by "never add a field." `<write-the-pointer>` gives retargeting a method and no occasion, and names no end for a pointer at all.

**authority-check.** Shipped with both violations of its last compliance report open: `return`, a dispatched worker's, is never defined, and `authorship` is used in `<classify-the-author>` before `<record-authorship-on-arrival>` defines it. A compliance audit of the shipped text found two more, both one term per concept: the tag `<state-what-enforcement-holds>` first-uses `state` and the prose beneath substitutes `grade`; `operator` enters at line 19 as a second term for `self`, which line 21 then glosses as "the operator reading this", and recurs through the file. "The operator this system serves" is neither defined nor tied to self. A peer is identified by the identity it arrived with while its record opens at dispatch, before anything arrives. An author identity has no stated stored form. For unknown-class content, whether to record the claimed sender label or none is unsettled. No rule says which author class may supply the evidence attached to a claim. A ground that "fails" is undefined. The enforcement grades cover neither a rule applied continuously nor a disposition of already-flagged content, and no rule is mapped to one of the three. `orchestration_log/recon/2026-09-17/authority-check-standing-compliance.md` holds the report.

pat-down, schema-resolution, and authority-check have been independently audited against the shipped text, and the rename of `standing` to `force` in event-capture and span-closure was audited for force and scope. The correction-in-place, archive-pointer, and resolved-deferral edits to corpus-reconciliation, record-promotion, and record-writing are later than any report covering them.

## Corpus vocabulary

`working text`, `stretch of work`, `closing ceremony`, `the machinery`, and `working context` are load-bearing across several skills and defined in none. They belong to the plugin, not to whichever skill a checker happened to read.

They form a third residue class beside a skill's own terms and a named sibling's. Charge no checker finding about them to a skill. Never gloss one inside a single slice, and never repeat a gloss across slices. Close the class by one owner decision fixing each term's definition and its home.

## Open for the owner

One ground puts content out of force and the status derivation reads none of it. `authority-check` ends a peer by irrelevance and lets the records about it retire, naming no actor that performs the retirement and none that records it, while `record-writing` reads retired from an owner-ruling decision or from a record retiring it. Peer records so ended read as live.

A routine's standing is a separate axis from a record's status, so the unratified-channel and online-channel grounds were never status questions and are gone. `authority-check` owns standing, names the four supply channels, writes the established channel through `record-writing`, and derives standing from what is written. `decisions.md`, 2026-09-17.

Two ontology items stand for the owner. `ground` names a goal parameter in §7 and what a directive cites in §4 and §13 — two concepts under one name. §11's third concern gives the charter's autoload closure as holding the goal and the condition statement, where §5 gives the charter the frame and the prime directives as well.

## The audit's detection gap

`corpus-reconciliation`'s `<read-before-repairing>` reads the map, every record in the corpus, each record's recorded authorship, and each record's lineage. It does not read the mark's verification state.

`record-promotion`'s `<write-the-move>` hands a gateless dossier entry to that audit, which is to strip its force and hold it in quarantine with its lineage. The audit's reading cannot find one. A gateless dossier entry is therefore never detected and never quarantined.

Close it by extending the audit's reading, not by moving the detection to the gate that the entry bypassed.

## The shipped default schema

`memento/config/default.yaml` declares the record kinds across the five tiers, each with its home, its tier, and its verification depth, beside the event taxonomy, the verification depths, the kind form, and the provenance form. `schema-resolution`'s `<stop-the-check-at-the-shipped-default>` resolves through it.

The kinds and their homes are the live downstream project's working set. The default succeeds the orchestration plugin's artifact contract, whose maintenance is deprecated.

The file carries no comments. Anything stating what a record admits takes one free-prose field, `admits`, carried by every kind and declared like any other field. `decisions.md`, 2026-09-17.

The goal is not among the kinds. It is committed to `CLAUDE.md` inside the charter, written the way prime directives are, and `frame` holds what remains at `docs/ground-truth.md`. `decisions.md`, 2026-09-17.

## After changing a skill

1. Filter the accounting rows naming that skill in the slicing plan, and confirm each item's content still appears in the skill body.
2. Run the prose-carriage audit both ways: the changed skill's full text against every other slice's assigned items, and every other slice's text against the changed skill's items. Each substantive statement traces to the slice's own items or stands as a reference by name. A grep for terms does not satisfy this step.
3. Run the changed skill against `skill-creation`'s own verify step — read the finished skill against every instruction, and deliver nothing that breaks one.
4. Measure the file with `just tokens FILE` before and after the change.
5. Bump `memento/.claude-plugin/plugin.json` — patch for a fix, minor for an addition, major never without owner approval — and regenerate the plugin README.
6. After a change to `schema-resolution`, confirm the skill and `hooks/read-config.py` state and realize one identical resolution rule. The parser half is unbuilt, so this step is inert until it exists.

A change to `ONTOLOGY.md`, which only an owner ruling makes, additionally reruns step 1 across every slice the changed section maps to and reruns the source sweep — every assertion of the changed section marked inventoried or not, table columns included.

A cross-slice contradiction reopens a shipped skill. The four-round cap governs a skill's own findings and does not license shipping two slices that disagree.

## The authoring loop

Three agents ran per skill per round, each rebinding to First Principles and the standard from source. The reports live under `orchestration_log/recon/${DATE}/` as `<skill>-r<N>-<kind>.md`, gitignored and disposable.

**The compliance checker** reads two files: the standard at `memento/skills/skill-creation/SKILL.md` and the draft. It extracts every instruction the standard states, numbered and tagged with the standard's line number, writes that extraction to the report, and only then reads the draft and checks it instruction by instruction. Each violation quotes the draft's offending text verbatim with its line number. Line 1 of the report is a bare integer, written last.

**The usability checker** reads the draft alone — not the standard, not the ontology, not a sibling. It invents one concrete case, follows the procedure step by step, and logs each forced guess in the turn it happens. A forced guess is one of five kinds: a step that does not say what to do, a term the draft uses but never defines, a decision the draft leaves open, an instruction that admits two readings, a thing the draft references but never supplies. Line 1 is a bare integer, written last.

**The author** receives both reports and the three filters inline, triages each finding as valid or struck, names the ruling that strikes each struck one, and revises the draft in place. Refusing a wrong finding with a diagnosis outranks a compliant edit that breaks coverage.

The checkers are blind to each other, to the author's reasoning, and to every sibling skill. Carry a settled ruling in the checker's own prompt, never in a filter applied to its output. Command the tag-name sweep in both checker prompts — every content word in a tag name appears in the prose beneath it, naming the concept with that word and not a synonym.

A round drives the filtered count, never the raw count. A skill naming any sibling never reaches a raw zero. The loop caps at four rounds, after which the skill ships with its open findings recorded as residue. A contradiction between two of a skill's own rules earns one bounded pass past the cap, and that pass closes the contradiction plus whatever else is cheap and certain.

**One known defect in the compliance brief.** It requires the whole extraction written to the report before the draft is read. Three checkers reached the 64,000-token output ceiling doing so and two ended there. Keep the two-phase split; never let a checker read the draft before its extraction stands written. Fix the extraction's form instead: one line per instruction, carrying the standard's line number and the instruction as stated, and no commentary.
