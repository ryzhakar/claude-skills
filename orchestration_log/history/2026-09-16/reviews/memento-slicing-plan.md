# memento — Slicing Plan

Plan for building the memento plugin's skills, hooks, config, and maintainer layer from the settled design at `/Users/ryzhakar/pp/claude-skills/memento/ONTOLOGY.md` (465 lines, authoritative, unchanged by this plan). Written 2026-09-16. Writers build one loop per slice from this document; two checkers verify it for full coverage and zero overlap.

**Carriage rule for the accounting.** A slice *carries* an item when it states the item's content. A slice that names another skill, or uses a term another slice defines, *references* — it does not carry. Reference by name is required (shared procedures are extracted skills, referenced by name); carriage in two slices is the overlap defect. Shipped artifact text counts as its slice's prose — a YAML comment in the worked config and a hook template line carry exactly as a skill sentence does. A slice's writer states every carried item's full inventory text; the roster row's cells summarize the boundary and echo what is load-bearing, never the whole cargo. Every checker question of the form "does slice X also state item N?" resolves against this rule.

**Slice roster.** Eleven skills (one exists), two hooks, one config artifact, one maintainer layer. Skills live at `memento/skills/<name>/SKILL.md`; hooks at `memento/hooks/`; the shipped default config at `memento/config/default.yaml`; maintainer files at `memento/maintainers/`. Every skill is written to the standard of the finished `skill-creation` skill: one procedure, XML-tagged imperative body, paired prohibitions, one emphatic word per sentence, self-contained for one read.

---

## Design inventory

Every entity, relation, tier, process, seam, invariant, ruling, and gap, numbered. Provenance is split, and each section head names its own: items 1–119 and 129–133 restate text of `ONTOLOGY.md`; items 120–128 are dated extension work — the owner's rulings and this plan's own resolutions — placed in the baseline because writers build from them, present in no line of `ONTOLOGY.md`. An item quotes its source row whole: for an entity, all five §3 columns — what it is, identity criterion, creator, changer, ender; for a tier, every column including its writers; for a seam or invariant, every cell of its row. This is the coverage baseline; the accounting table maps each number to exactly one slice.

### Meta (§1)
1. Naming policy: the recoverability test; functional names only; source words confined to correspondence table and glossary derivation column.
2. The system name `memento`, lowercase; one instance per scope.

### Foundations (§2)
3. Substrate: the machinery underneath; singular per runtime; acts but pursues no goals; the system runs on it, does not include it.
4. Context: working text, lost unless written to a durable location or condensed into a digest.
5. Endowment: trained capability and knowledge; present always, read-only.
6. Cutoff: the moment after which nothing more entered the endowment.
7. Scope: one project, one corpus, one schema, one goal-set, one charter, one owner.
8. Corpus: all records under a scope, across all tiers; created at scope creation; changed by every write.
9. Principal: the operator across spans; identity = same charter over same corpus; created at scope creation; changed by every write to charter or corpus; single per scope; second principal only under owner override.
10. Owner: the scope's human; identity = the configured human identity; created at scope creation; top of the authority order; distinct from the principal; ends by scope transfer — an ending the design leaves open (§14, OQ4).
11. Peer: any other actor, dispatched workers included; identity = stable external identity as recorded; created by first receipt, delegation, or dispatch involving it; changed by facts recorded about it; persists between activations; never an authority.
12. Run, wake, halt: one continuous activation; begins at a wake, ends at a halt, clean or crash.
13. Records track the memory axis only: no record distinguishes crash from clean halt; existence events are the substrate's business.
14. Span and span end: one continuous narrative thread, created when a context starts carrying a new thread; end foreseeable when signaled, blind otherwise.
15. Attenuation: within-span memory event; verbatim context condensed to a digest; created by the substrate's pressure — the condensing is the principal's act; instantaneous; the thread continues.
16. Axis orthogonality: a run can halt mid-span; a later run may resume the narrative; an unresumed span is orphaned where its last trace ends.
17. Waking cause: summons, signal, tripwire; names the occasion; carries no payload of truth.
18. Record: a marked, schema-conforming written statement on a durable location, made to outlive its span.
19. Product versus record: the system holds records about products, never the products.
20. Disposable location: a path class downgraded out of persistence; no destruction process exists — things cease by living there.

### Entities (§3)
21. Tripwire: (condition, purpose); laid by the principal in some run; time- or condition-fired, single or recurring; rescheduling with lineage; ends by firing or cancellation.
22. Claim: an unverified assertion; identity (subject, assertion); changed by evidence attachment; ends by promotion or rejection.
23. Fact: a verified assertion with its evidence; identity (subject, assertion, verification); changed by supersession only; ends by supersession or retirement.
24. Directive: an instruction to future spans with at least one ground; identity (scope of application, imperative); ends by fulfillment, expiry, supersession.
25. Trace: the immutable, dated record of a memory-axis event, written when it happened; never ends — it ages to archive.
26. Digest: a lossy self-authored condensation; identity (condensed set, occasion); immutable; no field guaranteed; superseded only by a fuller digest.
27. Derealisation: the attenuation-digest authoring state — the writing happened, the memory of writing is gone, the record remains.
28. Pointer: a record whose content is another record's home; retargeting with lineage; ends by target retirement.
29. Autoload pointer and autoload closure: a charter pointer whose target joins the always-loaded tier; closure transitive; the closure IS that tier's extent.
30. Baseline: the maintained expected state of a scope at span edges; created by span closure; updates with lineage.
31. Schema: the declared shape — record kinds, homes, event taxonomy, verification demands; owner-created; amendment with lineage.
32. Map: the index over the corpus; created by first reconciliation; changed by reconciliation.
33. Goal: the owner's parametrized purpose; read from the charter; never negotiated.
34. Routine — script: a repeatable behavior as text read and followed; the canonical ship shape is the skill (correspondence seed 4); revision with lineage is supersession (47); ends by supersession or retirement.
35. Routine — reflex: a repeatable behavior installed to fire without being read; changed by reinstallation; ends by removal.
36. Mark: provenance bound at write time; fields fixed — author class, author identity, span reference, date, verification state, ground pointers for directives; a changed mark is a new record; a mark ends with its record.
37. Record statuses: live, superseded, quarantined, retired.

### Relations (§4)
38. homed-in: every record sits in exactly one tier at a time.
39. about: every record has at least one subject; N:M.
40. authored-by: mandatory via mark; a record without a mark is unknown-authored by definition.
41. supplied-by: routine → supply channel; authority follows supply, not authorship.
42. grounds: every directive has at least one ground; an ungrounded imperative is not a directive.
43. verifies: evidence → fact; content verification at impact-scaled depth; existence-and-shape is not verification.
44. refers: pointer → record home; a pointer to a missing home is a dangling pointer, a detectable fault.
45. autoloads: charter → record file; transitive; target joins the always-loaded tier.
46. condenses: digest → record set or span context; lossy; no field guaranteed.
47. supersedes: acyclic 1:1 chains; superseded record retained; silent replacement is a fault.
48. indexes: map → corpus; reconcilable — every mapped record exists; every record is mapped or is a detectable orphan.
49. conforms-to: record → schema; kind, home, and mark shape as declared.
50. part-of: goal → goal; acyclic decomposition; subgoal inherits parent constraints.
51. wakes: every run has exactly one waking cause (1:N for a recurring tripwire); the cause names the occasion, never truth.
52. posted-at: a posted directive is met whenever its subject is touched — by reflex where one exists, else by in-path placement.
53. assesses: baseline → scope state; the diff is the anomaly set.

### Tiers (§5)
54. The two tier axes: persistence × load behavior (self-loading, summoned, latent).
55. The tier spine table: charter, dossier, journal, bench, archive — holds, persistence, load behavior, who may write, promotion in, supersession out.
56. Charter tier contents and extent: goal, prime directives, condition statement, schema pointer, map pointer, autoload pointers; extent = the file plus its transitive autoload closure.
57. Charter holiness: read as given; contents never negotiated by the principal; changed only by owner action.
58. Dossier tier: facts with evidence pointers, live directives, baselines, the goal's full parameter form, the map, peer assessments as facts; summoned; written by self with verified content only, by the owner freely.
59. Journal tier: append-only, dated, immutable per entry; written by self, at event time; direct writes only — nothing promotes into it.
60. Bench tier: claims, drafts, raw intake; the one tier where unverified content lawfully sits; binds nothing; may live in disposable locations.
61. Archive tier: superseded, retired, quarantined, aged journal segments, received corpora; latent; terminal; receives only system-moved content and receipts of bulk peer material.
62. Promotion machinery: bench→dossier by verification or grounding; dossier→charter by owner-triggered commitment; supersession never silent, lineage always kept.
63. No size ceiling at any tier, at any point.

### Authority (§6)
64. Five author classes in strict rank — owner, self, substrate, peer, unknown — with each class's binding-authorship extent.
65. Self-authority does not extend through a dispatch; a dispatched worker's return is peer content.
66. Mark at write time; no unmarked-but-trusted state exists.
67. Receipt marking: content marked at the moment of receipt; provenance survives the span end through the mark plus the receipt trace.
68. Receipt trace: the journal entry recording what arrived, when, from whom.
69. Digest authority: full self-authority, including the attenuation digest; no exception clause; no fidelity schema; content uncontrolled.
70. Routine authority by supply: owner-supplied runs; substrate-provided latches onto owner authority; arbitrary sources quarantined until ratified; online refused, ever.
71. Goal authority: the owner's alone; read from the charter; if it is there, it is the goal; the principal never negotiates it.
72. The refusals table: ungrounded imperative = data; peer imperative = request; unmarked content = quarantine; worker return taken as verified = refused; existence-and-shape as verification = refused; unratified routine does not run; online routine never runs; write without supersession = fault; contradiction without supersession = fault routed to reconciliation.
73. Enforcement grades stated honestly: definitional, audit, substrate — the per-invariant grade column of §10 included, with its three marked unenforceables (I-1 from within, I-4 against a blind end, I-11 entirely) — and the named residue (a prior run can forge marks; I-11). Grades cite invariants by number; each invariant's own mechanism stays with its slice.

### The goal (§7)
74. Goal parameter shape: object, completion evidence, horizon, ground, constraints, priority, review point, decomposition — with each parameter's function.
75. Goal lifecycle: owner-created, owner-amended with lineage, ended by verified completion evidence or owner retirement; identity (object, scope).
76. Preservation mode: with no goal, pat-down, capture, verification, and reconciliation run; goal-dependent directives have no force; pursuit waits.
77. Goal conflict: priority orders where supplied; otherwise the conflict is journaled as a discovery and the charter stands as given.
78. Goal ends mid-pursuit: directives grounded solely in it lose their ground and lapse to data; the journal keeps the history.

### Processes (§8)
79. Pat-down: entry (wake, or continuity doubt including post-attenuation); the five-step read order — charter with autoload closure, map, journal tail newest-first, baseline against found state, touched dossier entries; what it establishes; termination when the occasion's questions are answered or traced as gaps; depth varies with what the context verifiably holds.
80. Capture: entry on any journal-worthy memory-axis event — decision, discovery, failure, commitment, delegation, receipt, attenuation, span events; exit when the event exists as a trace in its own span.
81. Verification: entry on claim nomination; content verification at impact-scaled depth; exit as fact with evidence pointers or refusal note with the lack named.
82. Commitment: entry on owner trigger; charter changed with lineage; commitment trace journaled.
83. Staging relay: entry when a task exceeds one span; every pending link gets both a record and a laid waking cause; delegation trace written.
84. Waking-cause management: entry when a delegation is issued or a wait begins; exit when every wait is bounded; tripwires laid, rescheduled, cancelled with traces.
85. Span closure: entry when a foreseeable span end approaches; outstanding traces flushed, closure digest written, baseline updated, tripwires audited; redundancy for capture, never its mechanism; blind ends get no closure.
86. Reconciliation: entry on mismatch signal — map/corpus drift, contradiction, orphan, dangling pointer, unmarked content — or a recurring audit tripwire; exit when map matches corpus and faults are resolved or quarantined.
87. Ruling: entry when owner attention reaches quarantined content or an unratified routine; exit as ratified, retained-as-data, or retired, with lineage.
88. The event-fired principle: every process entry is an occurrence, not a ceremony position; no phase entity exists; the one irreducible ordering is that the pat-down grounds goal-directed action.

### Seams (§9)
89. N1 span → span: charter present, marks on everything, map reconcilable; on failure, pat-down degrades to preservation mode.
90. N2 event → journal: the trace written before any span end; a blind end between event and ink loses the event — physics, minimized, named.
91. N3 bench → dossier: everything on the dossier passed its gate; gateless entries detected by audit, quarantined with lineage.
92. N4 record → action: imperative + ground + mark; the ground is re-weighable before obedience; no ground, no force.
93. N5 peer → system: claim-grade material marked at receipt; nothing peer-borne verified by arrival.
94. N6 system ↔ peers as actors: delegation traces out; claims and signals in; silence bounded by the tripwire; contradiction answered by verification.
95. N7 substrate → system: substrate-marked observations; true about what happened, never directive.
96. N8 owner → system: owner-marked records, the charter as given; two owner statements conflict — the later supersedes with lineage; the system never arbitrates the owner.
97. N9 endowment → present action: trained competence, possibly stale; scope facts outrank endowment for scope matters.
98. N10 attenuation: a self-authored digest under derealisation; gaps surface at the next pat-down as anomalies.
99. Two source seams carried by design as absences: no mirror seam (no record is orientation-encrypted), no staged-presence seam (the system manages no affect).

### Invariants (§10)
100. I-1: the charter and its autoload closure enter every fresh context unbidden.
101. I-2: every record bears a mark; unmarked is unknown; unknown is quarantined.
102. I-3: nothing stands as fact without recorded content verification at impact-scaled depth.
103. I-4: a journal-worthy event is written in the span it occurs.
104. I-5: every wait is bounded by a waking cause.
105. I-6: one home per knowledge; map matches corpus; lineage unbroken.
106. I-7: no woken run inherits truth from the run that laid its waking cause.
107. I-8: the goal and the charter change only by owner action.
108. I-9: peer imperatives never bind, dispatched workers included.
109. I-10: quarantine is never silently emptied or silently promoted.
110. I-11: marks are truthful — enforceable by nothing internal; the named residue.
111. I-12: no routine runs without authority by supply.

### Coverage claims, correspondence, glossary, open questions (§11–14)
112. The five-concern coverage claims of §11, held as verifiable properties of the slice set.
113. The correspondence record (§12): eight seeds ruled on; source elements carried and not carried, including the two deliberate non-carries.
114. The glossary (§13): one term per concept, seventy terms with derivations and exclusions.
115. OQ1 — substrate attribution strength: genuinely open; recorded, not invented.
116. OQ2 — scope algebra: genuinely open; recorded, not invented.
117. OQ3 — journal taxonomy extension: the rule for adding event kinds per schema.
118. OQ4 — owner plurality and absence: genuinely open; recorded, not invented.
119. OQ5 — realized homes: which substrate paths realize each tier.

### Settled rulings (owner, 2026-09-15/16 — extension work; no line of ONTOLOGY.md states these)
120. R1: a built-in schema ships with the plugin; a project's config replaces it; no project starts where nothing qualifies as a record.
121. R2: harness-supplied content inherits owner authority for schemas, not only for routines; the shipped default carries owner standing.
122. R3: exactly one schema is ever in force; a config is whole, never partial; loading replaces the default outright; the contradiction fault cannot trip.
123. R4: the config supplies the schema; nothing is renamed; the map keeps its meaning as the index built from what exists; "artifact map" is retired.

### The four open gaps (audit G3, G4, G5, G7 — this plan's resolutions; ONTOLOGY.md names only the fourth, as its open question 5)
124. Gap: the schema has no tier.
125. Gap: the shape of the map is undefined.
126. Gap: the pat-down's read order never reaches the schema's content.
127. Gap: no entity names the layer where the design meets a real filesystem — the audit's G7 and the slot ONTOLOGY §14.5 leaves open as OQ5 (item 119): one gap under two provenances, resolved once, both rows homed in config.
128. Bootstrap corollary: schema self-conformance needs a base case — the config record's own kind, home, and mark shape must be anchored outside itself.

### Round-two additions — design text found uninventoried
129. Scope retirement: the entity table's "Ended by" column states five times that Principal, Baseline, Schema, Map, and Corpus each end by scope retirement — an owner act ending the scope itself; every record is retained, nothing destroyed. (ONTOLOGY §3.)
130. Peer ending: a peer ends by irrelevance — the records about it retire; no revocation act exists. (ONTOLOGY §3, Peer row.)
131. Repetition-safety: the directive property that executing twice harms no more than once; shaped and checked when a directive is authored; excludes idempotence of the substrate's own tools. (ONTOLOGY §12, "eating small; one-use packages," and §13 glossary.)

Items 129–131 append after the extension block to keep every earlier number stable; their provenance is the design itself, as each citation states.

### Round-three additions — the full-column sweep
132. Autoload pointer lifecycle: created only by owner-authored or owner-directed charter content; retargeted with lineage; ends by removal from the charter — an ending that differs from a plain pointer's. (ONTOLOGY §3, Autoload pointer row.)
133. The seams' source-failure column: each seam names the deconstruction failure it closes or narrows — N1 narrows F4, N2 narrows F1 (named unclosable), N3 closes F7, N4 closes F2, N5 closes F3, N6 closes F6; N7, N8, and N10 are new; N9 narrows the displaced-narrative failure. (ONTOLOGY §9, last column.)

The sweep that produced 132–133 walked every column of every ONTOLOGY table; every other cell it found uncarried was reconciled by extending an existing item's text in place — items 3, 8–11, 14–15, 21–26, 28, 30, 34–36, 51, 58–59, 61, and 73 now quote their rows whole.

---

## Slices

Eleven skills. The first four are the working spine; every skill beyond them carries its justification inline. Names pass the recoverability test and the finished skill's naming rule (two lowercase hyphen-joined parts naming what the skill does).

### Core skills

| Skill | The one thing it does | Trigger | Carries (inventory items) | Never does |
|---|---|---|---|---|
| **pat-down** | Re-derives the truth of a scope from its corpus at a waking or a continuity doubt | Session start, post-compaction, resuming interrupted work, "where was I", "orient yourself", any doubt about continuity | 5, 6, 9, 12, 16, 30, 53, 76, 77, 79, 89, 97, 106 | Never inherits truth from the run that laid the waking cause; never negotiates charter contents; never sets or amends a goal; never writes anything but anomaly and gap traces, and those through event-capture |
| **event-capture** | Writes a trace to the journal — self-authored, at event time — in the span the journal-worthy event occurs | A decision is made, a discovery lands, a failure is diagnosed, a delegation is issued, peer content is received, an attenuation occurs, a span starts or ends | 4, 13, 25, 59, 68, 80, 90, 103 | Never writes doctrine — facts and directives are record-promotion's; never revises an existing entry; never waits for closure or ceremony to write; never records existence-axis events |
| **record-promotion** | Moves a nominated record up one tier through the destination's gate: verification makes a fact, grounding makes a repetition-safe directive, owner-triggered commitment enters the charter — the goal in its eight-parameter shape included. Goal creation, amendment, retirement, and part-of decomposition are charter commitments; goal completion evidence passes the verification gate; autoload pointers enter and leave the charter by the same commitment, and removal from the charter is what ends one. The dossier admits self content only through these gates — the owner writes it freely | A record is nominated for a higher tier — "verify this claim", "promote this", "make this a directive", "add this to the charter", "set the goal", "amend the goal", an owner request to commit | 23, 24, 33, 42, 43, 50, 58, 62, 74, 75, 81, 82, 91, 102, 107, 131, 132 | Never promotes without the destination's gate; never accepts existence-and-shape as verification; never initiates a charter entry — a goal act included — without an owner trigger; never skips a tier |
| **staging-relay** | Pairs every cross-span continuation with a record and a laid waking cause — single or recurring — and bounds every wait | A task exceeds one span, a delegation is issued, a wait begins, "set a reminder", "continue this later", "wait for X" | 17, 21, 51, 52, 83, 84, 94, 104 | Never leaves a dormant link without a laid cause — a record alone is not a continuation; never packs truth into a cause; never lets a wait run unbounded; never monitors live processes — it lays causes and records, nothing else |
| **span-closure** | Flushes the record system when a span end is foreseeable: outstanding traces, closure digest, baseline update, tripwire audit. A digest — closure or attenuation — is self-authored with full self-authority: no exception clause, no fidelity schema, no field guaranteed | "Close the session", "wrap up", work completes, a compaction is imminent and signaled, any foreseeable end | 14, 26, 46, 69, 85 | Never substitutes for event-capture — closure is redundancy, not the mechanism; never runs at a blind end; never rewrites a journal entry; never blocks the end on missing ceremony |
| **corpus-reconciliation** | Audits the corpus against the map and repairs by supersession, adoption, or quarantine; the archive receives only system-moved content and receipts of bulk peer material | Map/corpus drift noticed, a contradiction between live records, an orphan or dangling pointer found, unmarked content found, a recurring audit tripwire fires, "audit the records" | 8, 32, 48, 61, 78, 86, 105, 123, 125 | Never rewrites content — every repair is a supersession, adoption, or quarantine with lineage; never rules on quarantined content — that is the owner's; never edits the schema; never invents records to satisfy the map |
| **owner-ruling** | Executes the owner's explicit disposition with lineage: dispose quarantined content, ratify or retire a routine, and — at the owner's word — retire the scope itself, ending principal, baseline, schema, map, and corpus together while every record is retained | The owner turns attention to quarantine, "review the quarantine", "should this routine run", "ratify this", "retire the scope" | 87, 109, 129 | Never fires without the owner's explicit word; never silently empties or silently promotes quarantine; never ratifies an online-sourced routine; never retires a scope on its own inference; never decides in the owner's place |

**Justification beyond the first four.** The one-procedure standard of `skill-creation` ("Cover one procedure per skill; never cover a second") forbids merging processes with distinct entry occasions. span-closure enters on a foreseeable end — no other slice enters there; folding it into event-capture would put a ceremony inside the event-fired mechanism the design explicitly separates (item 85: "redundancy, never its mechanism"). corpus-reconciliation enters on mismatch signals and audits the whole corpus — folding it into record-promotion would make one skill both the gate and the gate's auditor, which N3 keeps apart. owner-ruling enters on the owner's explicit disposition word alone (items 87, 129) and is the sole slice that may dispose of quarantine (I-10) or end a scope; folding it into corpus-reconciliation would hand the auditor the owner's disposition power, which the authority model ranks apart. Scope retirement rides owner-ruling rather than owning a skill: it is one more owner disposition, once per scope's lifetime, and a dedicated skill would add a standing description for no repeated procedure. Waking-cause management and staging relay ARE merged: both pair pending work with laid causes and both preserve I-5 — one procedure at the design's own altitude. Verification, grounding, and commitment are merged into record-promotion on one entry occasion — a record nominated for a higher tier — with the gate selected by destination the way corpus-reconciliation selects its repair by fault kind; the glossary itself defines promotion as one procedure with three gates, and the goal's lifecycle rides the charter gate because every goal act is an owner commitment.

### Extracted shared skills

Procedures two or more skills need, extracted per the owner's ruling: never duplicated, never behind a file pointer — each is a skill referenced by name.

| Skill | What it holds | Referenced by |
|---|---|---|
| **schema-resolution** | Establishing the one schema in force: the schema content already in context via the charter's autoload closure; else the project config at its fixed path; else the shipped default. Whole replacement, never a merge. The schema entity, the scope, conformance, and the bootstrap anchor. Items 7, 31, 49, 122, 124, 128 | record-writing, event-capture, record-promotion, corpus-reconciliation, pat-down — skills only; what a hook shares instead is stated below the graph |
| **record-writing** | The lawful write: resolve the kind and home from the schema, write with a mark at write time, replace only by supersession with lineage, respect tier write-rules and statuses. A changed mark is a new record, and a mark ends with its record; a pointer ends when its target retires. Items 18, 19, 20, 28, 36, 37, 38, 39, 40, 44, 47, 54, 55, 63, 66, 101 | event-capture, record-promotion, staging-relay, span-closure, corpus-reconciliation, owner-ruling |
| **authority-check** | Classifying content by author class and supply channel at intake, applying the rank, and refusing the refused: peer imperatives as requests, unmarked content to quarantine at intake, worker returns as claims, routines without authority by supply. The substrate — the machinery underneath, singular per runtime — authors observations only: true about what happened, never directive. A peer ends by irrelevance — the records about it retire; no revocation act exists. The owner's own ending, scope transfer, stays open (§14). Items 3, 10, 11, 22, 35, 41, 57, 60, 64, 65, 67, 70, 71, 72, 73, 92, 93, 95, 96, 108, 110, 111, 121, 130 | pat-down, event-capture, record-promotion, corpus-reconciliation, owner-ruling |

**Note on item 34.** The script half of the routine genus lands whole in the existing `skill-creation` skill — routine creation's canonical ship shape. The supply-channel authority over scripts and reflexes alike is item 70, authority-check's; authority-check never carries script authoring.

**Reference graph, complete — skills only.** pat-down → event-capture, authority-check, schema-resolution. event-capture → record-writing, authority-check, schema-resolution. record-promotion → record-writing, authority-check, schema-resolution. staging-relay → record-writing, event-capture. span-closure → record-writing, event-capture. corpus-reconciliation → record-writing, authority-check, schema-resolution, event-capture. owner-ruling → record-writing, authority-check, event-capture. record-writing → schema-resolution. schema-resolution → (none). authority-check → (none). skill-creation → (none, exists). Hooks appear in no row: a hook is a shell script and cannot read a skill, so it never references one.

**What a hook may share, and how.** Four things, nothing else: the config file, as data hooks and skills both read; the template text it renders (`orient.txt`, `attenuation.txt`); the bundled parser `read-config.py` — the executable realization of the resolution rule whose one reader-facing statement is schema-resolution's; and skill names uttered in emitted prose (`pat-down`, `event-capture`), which steer the agent reading the injection. A rule therefore has one statement, in a skill, and at most one executable realization, in hook code; a hook never carries a rule's only statement and never restates one. Maintainer step 6 pins the schema-resolution ↔ `read-config.py` pair.

---

## Coverage accounting

Every inventory item, one slice. "maintainer" = the maintainer layer (`memento/maintainers/` plus the retained `ONTOLOGY.md`); "config" = the shipped default config and its format spec; "hook-1" = the session-start hook; "hook-2" = the post-compaction hook.

| Item | Slice that carries it |
|---|---|
| 1. Naming policy | maintainer |
| 2. System name, one instance per scope | config |
| 3. Substrate | authority-check |
| 4. Context | event-capture |
| 5. Endowment | pat-down |
| 6. Cutoff | pat-down |
| 7. Scope | schema-resolution |
| 8. Corpus | corpus-reconciliation |
| 9. Principal + identity criterion | pat-down |
| 10. Owner | authority-check |
| 11. Peer, dispatched workers included | authority-check |
| 12. Run, wake, halt | pat-down |
| 13. Records track memory axis only | event-capture |
| 14. Span, span end foreseeable/blind | span-closure |
| 15. Attenuation | hook-2 |
| 16. Axis orthogonality, orphaned spans | pat-down |
| 17. Waking cause, three species, no payload | staging-relay |
| 18. Record definition | record-writing |
| 19. Product vs record | record-writing |
| 20. Disposable location, no destruction process | record-writing |
| 21. Tripwire entity | staging-relay |
| 22. Claim entity | authority-check |
| 23. Fact entity | record-promotion |
| 24. Directive + ground | record-promotion |
| 25. Trace entity | event-capture |
| 26. Digest entity | span-closure |
| 27. Derealisation | hook-2 |
| 28. Pointer entity | record-writing |
| 29. Autoload pointer + closure | hook-1 |
| 30. Baseline entity | pat-down |
| 31. Schema entity | schema-resolution |
| 32. Map entity | corpus-reconciliation |
| 33. Goal entity | record-promotion |
| 34. Routine — script | skill-creation (exists) |
| 35. Routine — reflex | authority-check |
| 36. Mark entity, fixed fields | record-writing |
| 37. Record statuses | record-writing |
| 38. homed-in | record-writing |
| 39. about | record-writing |
| 40. authored-by | record-writing |
| 41. supplied-by | authority-check |
| 42. grounds | record-promotion |
| 43. verifies | record-promotion |
| 44. refers | record-writing |
| 45. autoloads | hook-1 |
| 46. condenses | span-closure |
| 47. supersedes | record-writing |
| 48. indexes | corpus-reconciliation |
| 49. conforms-to | schema-resolution |
| 50. part-of | record-promotion |
| 51. wakes | staging-relay |
| 52. posted-at | staging-relay |
| 53. assesses | pat-down |
| 54. Two tier axes | record-writing |
| 55. Tier spine table | record-writing |
| 56. Charter tier contents and extent | hook-1 |
| 57. Charter holiness | authority-check |
| 58. Dossier tier | record-promotion |
| 59. Journal tier | event-capture |
| 60. Bench tier | authority-check |
| 61. Archive tier | corpus-reconciliation |
| 62. Promotion machinery | record-promotion |
| 63. No size ceilings | record-writing |
| 64. Five author classes, rank | authority-check |
| 65. Self-authority stops at dispatch | authority-check |
| 66. Mark at write time | record-writing |
| 67. Receipt marking | authority-check |
| 68. Receipt trace | event-capture |
| 69. Digest authority | span-closure |
| 70. Routine authority by supply | authority-check |
| 71. Goal authority | authority-check |
| 72. Refusals table | authority-check |
| 73. Enforcement grades + residue | authority-check |
| 74. Goal parameter shape | record-promotion |
| 75. Goal lifecycle | record-promotion |
| 76. Preservation mode | pat-down |
| 77. Goal conflict | pat-down |
| 78. Goal ends mid-pursuit | corpus-reconciliation |
| 79. Pat-down process | pat-down |
| 80. Capture process | event-capture |
| 81. Verification process | record-promotion |
| 82. Commitment process | record-promotion |
| 83. Staging relay process | staging-relay |
| 84. Waking-cause management process | staging-relay |
| 85. Span closure process | span-closure |
| 86. Reconciliation process | corpus-reconciliation |
| 87. Ruling process | owner-ruling |
| 88. Event-fired principle | maintainer |
| 89. N1 span → span | pat-down |
| 90. N2 event → journal | event-capture |
| 91. N3 bench → dossier | record-promotion |
| 92. N4 record → action | authority-check |
| 93. N5 peer → system | authority-check |
| 94. N6 system ↔ peers | staging-relay |
| 95. N7 substrate → system | authority-check |
| 96. N8 owner → system | authority-check |
| 97. N9 endowment → present action | pat-down |
| 98. N10 attenuation seam | hook-2 |
| 99. Two absent seams | maintainer |
| 100. I-1 self-loading | hook-1 |
| 101. I-2 marks everywhere | record-writing |
| 102. I-3 verified facts only | record-promotion |
| 103. I-4 events written in-span | event-capture |
| 104. I-5 bounded waits | staging-relay |
| 105. I-6 one home, reconcilable map | corpus-reconciliation |
| 106. I-7 no inherited truth | pat-down |
| 107. I-8 owner-only charter change | record-promotion |
| 108. I-9 peer imperatives never bind | authority-check |
| 109. I-10 quarantine discipline | owner-ruling |
| 110. I-11 marks truthful — the residue | authority-check |
| 111. I-12 routines by supply | authority-check |
| 112. Five-concern coverage claims | maintainer |
| 113. Correspondence record | maintainer |
| 114. Glossary | maintainer |
| 115. OQ1 substrate attribution | maintainer |
| 116. OQ2 scope algebra | maintainer |
| 117. OQ3 journal taxonomy extension | config |
| 118. OQ4 owner plurality | maintainer |
| 119. OQ5 realized homes | config |
| 120. R1 shipped default | config |
| 121. R2 supply authority for schemas | authority-check |
| 122. R3 one schema, whole replacement | schema-resolution |
| 123. R4 map meaning kept | corpus-reconciliation |
| 124. Gap: schema tier | schema-resolution |
| 125. Gap: map shape | corpus-reconciliation |
| 126. Gap: pat-down never reads schema | hook-1 |
| 127. Gap: realization layer unnamed | config |
| 128. Bootstrap base case | schema-resolution |
| 129. Scope retirement | owner-ruling |
| 130. Peer ending by irrelevance | authority-check |
| 131. Repetition-safety | record-promotion |
| 132. Autoload pointer lifecycle | record-promotion |
| 133. Seams' source-failure column | maintainer |

No item lands in two slices, and no slice's prose states another slice's content. Three same-shape tensions resolve on the one line the design itself draws — definition against audit, intake against audit: the refers relation (44) is record-writing's, and dangling-pointer detection is one entry in item 86's fault list; marks at write (66, 101) are record-writing's, and unmarked-content detection in the standing corpus is item 86's; quarantine at intake is authority-check's (67, 72), and quarantine of what audit finds already seated is item 86's. Item 86 is corpus-reconciliation's whole. A checker who finds a term uttered in two slices applies the carriage rule from the head of this plan: naming is reference, stating content is carriage.

### Verification protocol

Number-matching alone missed every round-one defect; it is the floor of five checks. Results belong in dated round reports, never in this section — a check's claim about itself is not evidence.

1. **Number floor** — every inventory item appears in the accounting exactly once, and every slice's carries-list matches the accounting in both directions.
2. **Prose-carriage audit** — every slice's full specification text — table cells, section prose, shipped comments in the worked YAML, hook template content — is read against every other slice's assigned items; each substantive statement must trace to the slice's own items or stand as a reference by name. The audit runs against the live file, never against a memory of editing it, and grep confirms every claimed strip; its findings go in the round report, never in this section.
3. **Source sweep** — after the inventory is drafted, `ONTOLOGY.md` is re-read start to finish, every cell of every table walked as its own assertion, and each marked inventoried or not.
4. **Provenance** — every inventory section names its source: an ONTOLOGY section, a dated owner ruling, or this plan. The inventory header claims design provenance only where it holds.
5. **Rule-pair sync** — maintainer step 6's check, run whenever either half changes.

---

## Hooks

Two hooks, shell scripts emitting prose from template files (`memento/hooks/templates/*.txt`), registered in `memento/hooks/hooks.json`. Both are the substrate's self-loading path: they realize I-1 (item 100) and the autoload closure (items 29, 45, 56) by injecting the charter tier into the context unbidden. The orientation block has one textual home — the shared template `templates/orient.txt`, rendered by both hooks; hook-2 prepends its attenuation preamble from `templates/attenuation.txt`. The closure and I-1 content is therefore stated once (accounted to hook-1, which owns `orient.txt`), and hook-2 carries only what is its own (items 15, 27, 98). A hook cannot read a skill, so neither hook references one: both execute the bundled parser `read-config.py` (stdlib only) — the executable realization of the resolution rule stated once in schema-resolution — and the config format is constrained (below) so the parser stays sound. Gating follows the marketplace rule: invisible when unconfigured.

| | Hook 1 — orientation at wake | Hook 2 — orientation after attenuation |
|---|---|---|
| **Event** | `SessionStart`, matcher `startup\|resume` | `PostCompact`, matcher `*` |
| **Reads** | 1. Runs `read-config.py` over the two config paths the config slice fixes; the parser realizes schema-resolution's resolution rule and yields the schema, the realization, and the source found. 2. The charter file at the realization's charter path, plus every autoload-pointer target, transitively. 3. The map's home path (existence and date only — the pat-down reads its content). 4. The tail of the newest journal file (last entries, bounded count). | Same four reads. |
| **Emits** | An orientation block: which schema is in force and from which source; the charter's content verbatim (or the line "no charter — preservation mode"); the schema's content (the closure includes it — see the gap resolutions); pointers to map and journal tail; one closing instruction: run the pat-down before goal-directed action. | The same orientation block, prefixed by the attenuation statement: an attenuation occurred; the condensed summary above this injection is the attenuation digest, self-authored under derealisation, and the gaps it left surface at the next pat-down as anomalies. Two closing instructions: journal an attenuation trace through event-capture, then run the pat-down — continuity doubt is the entry condition. |
| **No config** | The parser yields the shipped default as the schema in force; the hook proceeds against its realization paths, and the emitted source line names it. | Same. |
| **Nothing set up at all** | Gate: no project config AND no charter file AND no corpus directory at the shipped default's realization paths → `exit 0`, silent. One `[ -e ]` cascade, no output, no error. | Same gate, same silence. |

The hooks never write records, never run the pat-down themselves, and never carry truth of their own — they load the self-loading tier and name the occasion, which is all a waking cause may do.

---

## Config format

One YAML file per scope at `.claude/memento.yaml`, hand-writable and machine-readable. A built-in default of identical shape ships at `memento/config/default.yaml`; a project config replaces it, and no project ever starts where nothing qualifies as a record (R1). Which file is in force and what replacement means are schema-resolution's rules; what standing the shipped file carries is authority-check's; the config's conformance base case is schema-resolution's bootstrap anchor. This section declares only what is its own: the fields, their meanings, the format constraints, and the two path constants every other slice names by these values. The config bears a mark and supplies two subjects — the schema and the realization.

**Fields.**

| Field | Meaning |
|---|---|
| `scope` | The scope's name; one config, one scope. |
| `mark` | The config's own mark: `author-class` (legal values: `owner` in a project config, `substrate` in the shipped default), `author`, `date`. A config carries the mark fields that exist at authoring time; span reference and verification state belong to records written during work. |
| `schema.kinds` | Map of record kind → `{tier, home}`. Declares every kind the scope admits and the single canonical home of each. What a home may name ahead of what exists is corpus-reconciliation's division to state. |
| `schema.events` | The journal event taxonomy. The eight minimal kinds are fixed and may never be removed: decision, discovery, failure, commitment, delegation, receipt, attenuation, span-event. A config may append kinds; appending is the extension rule (resolves OQ3). |
| `schema.verification` | Verification demands: the default depth and any per-kind escalation. Legal depth values are the ones record-promotion's verification gate accepts. |
| `schema.mark-form` | The serialization of marks on records (e.g., YAML frontmatter, inline header line). Form only — the mark's fields are fixed by the design and are not configurable. |
| `realization.tiers` | Tier → path. Names the layer where the design meets the filesystem (resolves the fourth gap): the charter's file, the dossier/journal/bench/archive directories. |
| `realization.autoload` | Record kinds whose charter pointers are autoload pointers. `schema` is always a member. |
| `realization.disposable` | Path classes downgraded out of persistence. The bench may live here; nothing standing may. |

**Format constraints** (stated in the file header, enforced by the hooks' parser): plain scalars and flat two-level nesting, two-space indent, no anchors, no multiline scalars. Hand-writable by construction; parseable by a ten-line reader.

**Worked example — the shipped default, complete.**

```yaml
# memento — schema and realization for this scope.
# A project copy lives at .claude/memento.yaml; schema-resolution states which file is in force.
# Flat keys, two-space indent, no anchors, no multiline scalars.

scope: default

mark:
  author-class: substrate   # legal values: substrate (shipped default), owner (project config)
  author: memento-plugin
  date: 2026-09-16

schema:
  kinds:
    charter:   {tier: charter, home: .claude/memento/charter.md}
    schema:    {tier: dossier, home: .claude/memento.yaml}
    fact:      {tier: dossier, home: .claude/memento/dossier/facts.md}
    directive: {tier: dossier, home: .claude/memento/dossier/directives.md}
    baseline:  {tier: dossier, home: .claude/memento/dossier/baseline.md}
    goal:      {tier: dossier, home: .claude/memento/dossier/goal.md}
    map:       {tier: dossier, home: .claude/memento/dossier/map.md}
    trace:     {tier: journal, home: .claude/memento/journal/}
    digest:    {tier: journal, home: .claude/memento/journal/}
    claim:     {tier: bench,   home: .claude/memento/bench/}
    draft:     {tier: bench,   home: .claude/memento/bench/}
    archived:  {tier: archive, home: .claude/memento/archive/}

  events: [decision, discovery, failure, commitment, delegation, receipt, attenuation, span-event]

  verification:
    default-depth: content        # depth values: content, two-source
    high-impact: two-source

  mark-form: yaml-frontmatter     # fields are fixed by design; only the form is declared

realization:
  tiers:
    charter: .claude/memento/charter.md
    dossier: .claude/memento/dossier/
    journal: .claude/memento/journal/
    bench:   .claude/memento/bench/
    archive: .claude/memento/archive/
  autoload: [schema]
  disposable: [.claude/memento/bench/]
```

A bare project under the shipped default is lawful: schema in force, no charter — pat-down's preservation mode until the owner commits a charter.

---

## Four open gaps

**Gap 1 — the schema has no tier.** Resolved. The schema is a record homed in the dossier (standing, summoned), as row `schema:` in the default config's kinds declares. It reaches the always-loaded tier the way any dossier record may: the charter's schema pointer is an autoload pointer, so the schema joins the closure without changing what tier it sits in. Both moves use only machinery the design already defines (§5's "any part of it joins the self-loading tier when an autoload pointer targets it"). Carried by schema-resolution.

**Gap 2 — the shape of the map is undefined.** Resolved. The map is one file (home per schema), rebuilt by reconciliation, holding a dated header (when last reconciled) and one row per record: home path, kind, tier, status, subjects, date of last write. It indexes records that exist — never declared-but-unwritten homes, which are the schema's prescriptive business; that division is what dissolves the audit's C6. Granularity is per record. Carried by corpus-reconciliation.

**Gap 3 — the pat-down's read order never reaches the schema's content.** Resolved by gap 1's move, cited, not re-derived: with the schema inside the closure, step 1 of the pat-down already reads it. The hooks realize the closure — they inject charter plus closure into every fresh and every post-compaction context. The read order stays exactly as §8 states it; only the closure's extent was ever undeclared. Carried by hook-1.

**Gap 4 — no entity names the layer where the design meets a real filesystem.** Resolved by naming it: the **realization** — the binding of each tier to a path and of self-loading to the hooks, declared in the config's `realization` block. The name passes the recoverability test (a reader recovers "what makes the abstract tiers real" from the word plus its definition), fills the slot ONTOLOGY §14.5 explicitly leaves downstream, and keeps the audit's L419 hazard satisfied: file-layout content lives under `realization`, not inside `schema`, so the schema keeps its exclusions while one file lawfully carries both subjects (records may have several). Carried by config.

**Bootstrap corollary** (item 128, resolved with gap 1): the project config conforms to a schema whose base case is the shipped default — distribution content that never enters the corpus; its standing is authority-check's item 121. Self-conformance grounds out; no pre-schema state exists. Carried by schema-resolution.

---

## Maintainer layer

The owner's requirement: effort not lost, no deterioration as the plugin changes. Three files, one procedure.

| File | Holds |
|---|---|
| `memento/ONTOLOGY.md` | Exists. The settled design: definitions, correspondence (item 113), glossary (item 114), open questions. Authoritative; changed only by owner ruling. Within the maintainer slice it carries items 1, 99, 113, 114, 115, 116, 118, and 133 — the seams' source-failure column lives in its §9 table. |
| `memento/maintainers/coverage.md` | The inventory and accounting tables from this plan, updated to as-built state after each wave: item → slice, each row naming its provenance (ONTOLOGY section, dated ruling, or plan resolution), plus the reference graph and the verification protocol. Within the maintainer slice it carries items 88 and 112 — the event-fired principle and the five-concern claims, held as properties this file verifies against the slice set. The line-by-line instrument for both checker questions — was anything lost, is anything claimed twice. |
| `memento/maintainers/decisions.md` | Rulings with their rationale: the sixteen rulings of 2026-09-15, the four settled rulings above, the four gap resolutions, and every future ruling. Rationale lives here and only here — skills state policy without argument (ETHOS); the argument survives in this file instead of dying in a chat. A ruling is recorded as its number, date, carrier slice, and argument — never its operative content: the operative text lives only in the slice the accounting names, and this file is bound by the carriage rule like any slice. |

**After changing a skill, the maintainer:**
1. Opens `coverage.md`, filters the accounting rows naming that skill, and confirms each item's content still appears in the skill body — a coverage check, row by row.
2. Runs the prose-carriage audit both ways: reads the changed skill's full text against every other slice's assigned items, and every other slice's text against the changed skill's items — each substantive statement traces to its own slice's items or stands as a reference by name. A grep for terms does not satisfy this step; the round-one defects all passed a term-level check.
3. Runs the changed skill against `skill-creation`'s own verify step (read the finished skill against every instruction; deliver nothing that breaks one).
4. Measures the file (`just tokens FILE` where available) and records the count in `coverage.md`'s row.
5. Bumps `memento/.claude-plugin/plugin.json` — patch for fixes, minor for additions, major never without owner approval — and regenerates the plugin README.
6. After a change to schema-resolution or `hooks/read-config.py`: confirms the pair still states and realizes one identical resolution rule.

A change to `ONTOLOGY.md` itself (owner ruling only) additionally reruns step 1 across every slice the changed section maps to, and reruns the source sweep — every assertion of the changed section marked inventoried or not, table columns included.

---

## Build sequence

Four waves. Names and one-line contracts for every slice are fixed by this plan, so references by name are safe to write early; a wave waits only where a writer must verify a reference against a finished body.

| Wave | Loops (parallel within the wave) | Why here |
|---|---|---|
| **1** | `config/default.yaml` + format header · `schema-resolution` · `record-writing` · `authority-check` | The three shared skills and the default config depend on nothing but this plan. record-writing references schema-resolution by name only — the contract above suffices. Everything downstream references these four. |
| **2** | `pat-down` · `event-capture` · `record-promotion` · `staging-relay` · `span-closure` · `corpus-reconciliation` · `owner-ruling` | Seven independent loops. Each references wave-1 skills by name; wave 1 must be finished so each writer verifies the referenced contract against the real body, per the maintainer overlap check. No core skill references another core skill except through event-capture (pat-down, staging-relay, span-closure, corpus-reconciliation, owner-ruling write traces through it) — event-capture's contract is fixed here, so those five still run parallel with it. |
| **3** | hook-1 · hook-2 · `maintainers/coverage.md` · `maintainers/decisions.md` | Hooks emit instructions naming pat-down and event-capture — those names must exist on disk before a hook ships text invoking them. Hook writers build `read-config.py` from schema-resolution's stated rule (wave 1) and run the rule-pair sync before shipping. The coverage file records as-built state, so it follows the skills it accounts for. Four parallel loops. |
| **4** | Validation: plugin-validator over the whole plugin; every named path resolves; maintainer step 6's pair check passes; the prose-carriage audit over the full slice set; README regeneration; `plugin.json` minor bump | Single loop; touches everything, so it waits for everything. |

The existing `skill-creation` skill is untouched in every wave.
