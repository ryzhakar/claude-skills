# memento — Ontology

The defining document for the memory-and-continuity system, working name confirmed below. It settles what the system's things ARE — entities, relations, tiers, authority, the goal, processes, seams, invariants — before anything downstream is drafted. It defines; it does not instruct, lay out files, or specify implementations.

Built on three prior passes:

1. The source inventory — `/Users/ryzhakar/pp/claude-skills/memento-draft.md`
2. The harness mapping — `orchestration_log/recon/2026-09-15/memento-agent-mapping.md`
3. The source-system deconstruction — `orchestration_log/recon/2026-09-15/memento-system-deconstruction.md`

The system serves an operator with two structural conditions, both platform facts: nothing carries from one working stretch to the next except what is written and what was trained in; and nothing runs between activations — no clock, no thread, no one.

---

## 1. The name, and the naming policy

**The system is named memento.** Lowercase, a proper name for the whole. The ruling: the word itself means "an object kept as a reminder" — it describes the system exactly, independent of any film. It therefore passes the same test every other term must pass, and it is the only borrowed-origin name in the vocabulary.

**The naming policy — the recoverability test.** A term enters the vocabulary only if a reader who has never met the source material can recover the referent from the term plus its one-sentence definition. Applied without exception:

- No character names, no prop names, no scene references anywhere in the vocabulary. There is no "tattoo tier," no "polaroid record," no person's name as a role.
- Source words appear in exactly two places: the correspondence table and the glossary's derivation column — both of which exist to record where an idea came from, not to name what it is.
- Every part of the system carries a functional name that states what the part does or is.

---

## 2. Foundations

Terms everything else depends on, defined first.

**Substrate.** The machinery the operator runs on: the model, the context window, the tools, the filesystem, the trigger-and-notification plumbing, the automatic loading paths. The substrate acts (it loads, digests, times out, attributes) but does not pursue goals. The system runs ON the substrate; it does not include it.

**Context.** The working text present to the operator right now. Finite. Everything in it is lost at the end of its stretch unless written to durable storage first.

**Endowment.** Everything the operator knows without any record: trained capability and world knowledge. Present in every stretch at zero cost, read-only, and frozen at the **cutoff** — the moment after which nothing more entered it. The endowment is the operator's previous life; the cutoff is its injury date.

**Scope.** The unit a memento instance governs: one project, one corpus, one schema, one goal-set, one charter. Everything below is defined per scope.

**Corpus.** All records under a scope, across all tiers.

**Principal.** The operator the system serves, taken across time: whichever model instance is currently oriented by this scope's charter over this scope's corpus. Identity criterion — and this is an ontological commitment: two working stretches belong to the same principal if and only if they orient from the same charter over the same corpus. The continuity IS the corpus; there is no self underneath it that persists between stretches.

**Owner.** The human whose scope it is. The top of the authority order. Distinct from the principal.

**Peer.** Any other actor: another agent, an external service, any human who is not the owner. Peers persist, act, and remember between the principal's stretches; peers are never authorities.

**Span.** One continuous working stretch of the principal: from one boundary to the next, with the context verbatim-available throughout. A span ends without the principal necessarily foreseeing it.

**Boundary.** The event that ends a span. Two grades:
- **Attenuation** — the context is compressed; a lossy digest crosses automatically; the same activation continues. (The substrate's mid-run compression.)
- **Termination** — the activation ends; nothing crosses except records on durable tiers.
A boundary is **foreseeable** when a signal precedes it (the work completes, the owner closes, budget pressure is visible) and **blind** otherwise.

**Waking cause.** The only thing that makes a span begin — between waking causes the principal does not exist. Three species:
- **Summons** — the owner initiates (a message, a request).
- **Signal** — delegated or external work completes and the substrate delivers notice.
- **Tripwire** — a cause the principal laid for itself in an earlier span: time-fired or condition-fired, single or recurring, carrying pointers to what the woken span should read first.

**Record.** A written statement on a durable tier, made to outlive its span. The genus of the system's memory. Every record carries a **mark** (defined in §6) and conforms to the scope's schema.

**Product.** What the work itself makes: code, documents, models, deployments. Products belong to the task, not to memory. The system holds records ABOUT products — facts, pointers, directives — never the products themselves. (This distinction corrects the seed "filesystem operations = record keeping": only some writes are memory.)

---

## 3. Entities

| Entity | What it is | Identity criterion | Created by | Changed by | Ended by |
|---|---|---|---|---|---|
| Principal | The operator across spans | Same charter over same corpus | Scope creation | Every commitment to charter or corpus | Scope retirement |
| Owner | The scope's human authority | The configured human identity | Scope creation | — | Scope transfer (open question, §14) |
| Peer | Any other actor | Stable external identity as recorded | First receipt or delegation involving it | Facts recorded about it | Irrelevance (records retire) |
| Substrate | The machinery underneath | Singular per runtime | — | — | — |
| Span | One continuous stretch | (entry boundary, exit boundary) | A waking cause | — | A boundary |
| Boundary | A span-ending event | Moment + grade | Substrate or owner | — | Instantaneous |
| Tripwire | A self-laid future waking cause | (condition, purpose) | The principal, in some span | Rescheduling with lineage | Firing or cancellation |
| Claim | An unverified assertion | (subject, assertion) | Receipt, observation, or proposal | Evidence attachment | Promotion to fact, or rejection |
| Fact | A verified assertion with its evidence | (subject, assertion, verification) | Verification of a claim | Supersession only | Supersession or demotion |
| Directive | An instruction to future spans, with its ground | (scope of application, imperative) | Self or owner, grounded | Supersession | Fulfillment, expiry, supersession |
| Trace | The record of an event, written when it happened | (event, span moment) | Capture, in the event's span | Never — immutable | Never (ages to archive) |
| Digest | A lossy condensation of records or of a span | (condensed set, boundary or occasion) | Boundary closure, or the substrate at attenuation | Never — immutable | Supersession by a fuller digest |
| Pointer | A record whose content is another record's home | (site, target home) | Any record-writing process | Retargeting with lineage | Target retirement |
| Baseline | The expected state of a scope at a boundary | Scope | Boundary closure | Updates with lineage | Scope retirement |
| Schema | The declared shape: record kinds, homes, event taxonomy, verification demands | Scope | Owner, or ratified proposal | Amendment with lineage | Scope retirement |
| Map | The index over the corpus: what exists, where, about what | Corpus | First reconciliation | Reconciliation | Scope retirement |
| Goal | The parametrizable purpose (full shape in §7) | (object, scope) | Owner, or owner-ratified proposal | Parameter amendment with lineage | Completion verified, or owner retirement |
| Routine — script | A repeatable behavior as text the principal reads and follows | (task shape, scope) | Authoring, under authority rules | Revision with lineage | Supersession or retirement |
| Routine — reflex | A repeatable behavior installed to fire without being read — substrate-side automation | (occasion, response) | Installation, under authority rules | Reinstallation | Removal |
| Mark | The provenance attributes bound to a record | Its record | The writing span, at write time | Never — a changed mark is a new record | With its record |
| Corpus | All records of a scope | Scope | Scope creation | Every write | Scope retirement |

**Statuses** (of any record): **live** (in force), **superseded** (replaced, lineage kept), **quarantined** (retained but stripped of force, pending adjudication), **retired** (out of force by decision, retained in archive).

---

## 4. Relations

| Relation | From → To | Cardinality | Constraint |
|---|---|---|---|
| homed-in | Record → Tier | N:1 | Every record sits in exactly one tier at a time |
| about | Record → subject (goal, product, peer, scope, record) | N:M | Every record has at least one subject |
| authored-by | Record → author (via mark) | N:1 | Mandatory; a record without a mark is unknown-authored by definition |
| grounds | Fact ∪ Goal → Directive | M:N | Every directive has at least one ground; an ungrounded imperative is not a directive |
| verifies | Evidence (records, observations) → Fact | M:N | At least as many independent sources as the schema demands |
| refers | Pointer → Record home | N:1 | A pointer to a missing home is a dangling pointer — a detectable fault |
| condenses | Digest → record set or span | 1:N | Lossy; the digest's mark states what it condensed |
| supersedes | Record → Record | 1:1 per step, chains allowed | Acyclic; the superseded record is retained; silent replacement is a fault |
| indexes | Map → Corpus | 1:1 | Reconcilable: every mapped record exists; every record is mapped or is a detectable orphan |
| conforms-to | Record → Schema | N:1 | Kind, home, and mark shape as declared |
| part-of | Goal → Goal | N:1 | Acyclic decomposition; a subgoal inherits its parent's constraints |
| wakes | Waking cause → Span | 1:1 (1:N for recurring tripwires) | Every span has exactly one waking cause |
| carries | Tripwire → Pointer set | 1:N | What the woken span reads first |
| posted-at | Directive → subject | N:M | A posted directive is met whenever the subject is touched — guaranteed by a reflex where one exists, otherwise by placement in the subject's own path |
| bounds | Boundary → Span | 2:1 | Entry and exit |
| assesses | Baseline → scope state | 1:1 | The diff between baseline and found state is the anomaly set |

---

## 5. Record tiers — the spine

The source ordered its records on one axis: permanence. The harness separates two axes the source's world fused, because there a mark on the body was both eternal AND always visible. Here they are orthogonal:

- **Persistence** — how long the record survives: standing (until superseded), working (until promoted or abandoned), passing (until read and acted on).
- **Load behavior** — how the record reaches a span's context: **self-loading** (enters every span unbidden — the substrate brings it), **summoned** (reached by following a pointer or an instruction), **latent** (found only by search or deliberate fetch).

Durability without loading is a grave: the record outlives everything and governs nothing. The tiers are defined so that what must govern is what gets loaded.

| Tier | Holds | Persistence | Load behavior | Who may write (authority floor) | Promotion in | Demotion out | Capacity pressure |
|---|---|---|---|---|---|---|---|
| **Charter** | The goal's summary form, prime directives with grounds, the principal's condition statement, the schema pointer, the map pointer | Standing | Self-loading — enters every span unbidden | Owner directly; self only through commitment | From dossier, via commitment | Superseded entries → archive, lineage kept | Hard bound. The always-loaded tier is paid for from finite context in every span; adding usually means removing. The bound replaces the source's pain-of-inscription as the deliberation forcer |
| **Dossier** | Facts with evidence pointers, live directives with grounds, baselines, the goal's full form, the map, peer assessments as facts | Standing | Summoned — reached through charter pointers at need | Self, verified content only; owner freely | From bench, via verification (claims) or grounding (directives) | Superseded → archive | Soft bound: when heavy, digests stand in and the full records remain summoned-on-need |
| **Journal** | Traces — event-fired entries: decisions, discoveries, failures, commitments, delegations, receipts, boundaries — and boundary digests. Dated, ordered, append-only | Standing, immutable per entry | Summoned tail (recent entries at orientation); latent body | Self, at event time; substrate digests enter marked as substrate | Direct writes only — nothing promotes INTO a journal; it records, it does not hold doctrine | Aged segments → archive | Unbounded append; age handles size |
| **Bench** | Claims under verification, drafts, tentative formulations, staged work notes, raw peer content at claim grade | Working — until promoted, or abandoned | Latent — touched by the work that needs it | Any author class, always marked; this is the one tier where unverified and peer content lawfully sits | Receives all raw intake | Up via promotion; out via deletion — bench content binds nothing and may be freely discarded | Disposable by design |
| **Archive** | Superseded versions, retired records, quarantined content, aged journal segments, received corpora too large to hold elsewhere | Standing, immutable | Latent — search-fetched | System-moved content; receipts of bulk peer material | Receives demotions, retirements, quarantine | Terminal | Unbounded growth — open question (§14) |

**Promotion machinery.** Bench → dossier: a claim becomes a fact through verification; an imperative becomes a directive by acquiring a ground. Dossier → charter: commitment — the entry must be a verified fact or grounded directive, relevant to every future span, and it must fit the hard bound; the commitment itself is journaled. Demotion is supersession or retirement, always with lineage, never silent.

**Realization note.** The charter's self-loading behavior is a substrate fact, not a wish — substrates provide always-loaded instruction paths and injection-at-start mechanisms; the charter is whatever rides them. Which concrete paths realize which tiers is downstream implementation, out of scope here.

---

## 6. Authority model

The source's deepest structural finding: provenance dies at every seam. The writer's identity, the receiver's knowledge of a source, the reasons behind a directive — none of it crossed a fade. And bytes are anonymous: nothing in written content itself certifies its author. The authority model is what memento states in the face of that.

### Author classes, in strict rank

| Rank | Class | Who | May bindingly author |
|---|---|---|---|
| 1 | **Owner** | The scope's human | Everything: goals, schema, charter, directives, facts, retirements, adjudications |
| 2 | **Self** | The principal — any span of the same scope | Directives (grounded), facts (verified), traces, digests, tripwires, bench content, goal PROPOSALS |
| 3 | **Substrate** | The machinery | Observations only: digests, timestamps, tool results, attributions. Observation-grade: authoritative about what happened, never about what to do |
| 4 | **Peer** | Everyone else | Nothing bindingly. Peer content enters as claims and requests — data, never instruction |
| 5 | **Unknown** | Absent or unverifiable mark | Nothing. Unknown content is quarantined on detection |

### The mark

Every record carries a mark, written by the span that writes the record, at write time: author class, author identity, span reference, date, verification state, and — for directives — ground pointers. A record without a mark IS unknown-authored; there is no unmarked-but-trusted state.

### Receipt marking — how provenance survives the boundary

Source knowledge exists at exactly one moment: receipt. The receiving span is the only entity that ever knows where content came from. Therefore: content from outside is marked at receipt — the claim lands on the bench bearing its peer's identity, and a **receipt trace** lands in the journal (what arrived, from whom, when, in what connection). After the boundary, the mark and the trace are what remain of the knowledge. This is the mechanism the source lacked: its foreign notes stayed, their origins vanished.

### What is refused

| Refused | Disposition |
|---|---|
| An imperative without a ground | Not a directive. Data. It binds nothing, whatever its author claims |
| An imperative authored by a peer | A request. Recorded as a claim about what the peer wants; binding only if self or owner adopts it as a grounded directive |
| Content with no mark | Quarantined: retained, stripped of force, listed for adjudication |
| A goal not ratified by the owner | A proposal. It parameterizes nothing until ratified |
| A charter commitment grounded only in a digest | Refused — lossy grounds are insufficient for the always-loaded tier; the full fact must be cited |
| A write that replaces a record without supersession | A fault. Lineage is mandatory; silent overwrite is the system's name for memory destruction |
| Contradiction between live records without a supersession between them | A detected fault routed to reconciliation, then to the owner if unresolved |

### Enforcement grades — stated honestly

- **Definitional** enforcement: the reading principal applies the rules because the charter states them. Holds exactly as far as the charter loads and is followed.
- **Audit** enforcement: reconciliation detects violations after the fact — unmarked content, missing grounds, silent overwrites, contradictions. Detection, not prevention.
- **Substrate** enforcement: write attribution, immutable history, and per-path write permissions exist as substrate capabilities; where present, they make marks checkable against an authority the writing span does not control. This is the only prevention-grade enforcement available.
- **The residue nothing enforces:** a prior span of the principal itself can fabricate a ground, a verification, and a mark, and a later span cannot detect the fabrication from the records alone. The source dramatized exactly this, and no self-administered mark system abolishes it. What memento adds is not immunity but cost and surface: fabrication must now forge lineage, journal, marks, and grounds consistently, under substrate attribution where it exists, against owner review at adjudication. The flaw is narrowed and named. It is not gone. (Invariant 12, §11.)

---

## 7. The goal

The source ran on a single hardwired purpose, held nowhere but in the operator and stated as the reason the whole system worked at all — its cautionary contrast was precisely a man with the same condition and no reason. memento generalizes the purpose into a first-class, parametrizable entity. A goal is not a slogan; it has a shape.

### Shape

| Parameter | Required | Shape | Function |
|---|---|---|---|
| **object** | yes | A testable end condition or tended condition, stated concretely | What counts. The thing pursued or maintained |
| **completion evidence** | yes for terminal goals | The named artifact or observation that will verify the object is reached — declared at goal creation, before pursuit | The end is checkable by a span that remembers nothing; done-ness is a record, not a feeling. The evidence slot is reserved in advance, like the source's blank space kept for the end |
| **horizon** | yes | `terminal` (reachable end) or `standing` (open-ended tending) | Separates missions from maintenance; the source knew only the first |
| **ground** | no | The owner's stated reason | Tie-breaking and scope questions. The functional load the source assigned to felt drive — "the system fails without a reason" — is carried in memento by the goal's presence on the charter, loaded into every span. Drive is not stored; text is |
| **constraints** | no | What may not be done in pursuit | Bounds the pursuit independent of the object |
| **priority** | no (required when goals ≥ 2) | Total order within the scope | Conflict resolution |
| **review point** | no | A condition or date at which the goal itself is re-examined | The source's mission could never be audited from inside and ran, possibly wrong, indefinitely. A goal that can schedule its own re-examination closes that |
| **decomposition** | no | Subgoals via part-of, acyclic | Inheritance of constraints downward |

### Lifecycle and authority

Created by the owner, or by owner ratification of a proposal (a self- or peer-authored goal is claim-grade until ratified). Amended by parameter change with lineage. Ended by verified completion evidence, or by owner retirement. Identity: (object, scope).

The source's final act — the operator writing a fresh target for his future self to pursue — types in memento as an **unratified goal proposal**: retained, marked, and without force until the owner rules. The single most catastrophic event in the source material is, in this ontology, a quarantine case.

### Behavior at the edges

- **No goal present:** the system operates in preservation mode — orientation, capture, reconciliation, and record-keeping run; goal-dependent directives have no ground and therefore no force; pursuit waits for an owner.
- **Two goals conflict:** priority resolves; equal priority suspends the conflicting directives (they keep their records, lose their force), journals the conflict, and summons the owner. Conflicting pursuit does not proceed on the system's own authority.
- **Goal absent mid-pursuit (retired or completed):** directives grounded solely in it lose their ground and lapse to data; the journal keeps the history.

---

## 8. Processes

Each process is event-fired: it has an entry condition that is an occurrence, not a ceremony position. No process is a named phase of a ritual, and no fixed sequence of processes exists beyond what their entry conditions impose.

| Process | Entry | Exit | Reads | Writes | Invariant preserved |
|---|---|---|---|---|---|
| **Orientation** | A span begins (any waking cause) | The principal holds: goal, schema, situation, anomalies | Charter (self-loading); map, dossier, journal tail via pointers; baseline vs found state | Anomaly traces, if any | No goal-directed action precedes charter presence (I-1) |
| **Re-orientation** | An attenuation boundary passes, or a continuity break is noticed mid-span | Continuity re-established | Charter; the attenuation digest (substrate-marked); journal tail | A trace noting the attenuation | Digests are observation-grade, never doctrine (I-3 via authority) |
| **Capture** | A journal-worthy event occurs — the schema's event taxonomy names the kinds: decision, discovery, failure, commitment, delegation, receipt, boundary | The event exists as a trace | The event itself | A trace, in the event's own span | No journal-worthy event outlives its span unwritten (I-5) |
| **Verification** | A claim is nominated for promotion | Fact created, or claim held with the lack named | The claim; independent evidence per schema demand | The fact with evidence pointers and mark; or a refusal note on the bench | Nothing unverified stands as fact (I-4) |
| **Commitment** | A fact or directive is nominated for the charter | Charter changed with lineage, or nomination refused | Charter capacity; the nominee's grounds and relevance | The charter entry; demotions it forces; a commitment trace | Charter bound holds; every charter entry grounded (I-8, I-3) |
| **Staging relay** | A task exceeds one span | Every pending link has both its record and its waking cause laid | The task's decomposition | Posted directives per link; tripwires per link; a delegation trace | No dormant link without a laid waking cause — a record alone is not a continuation (I-6) |
| **Waking-cause management** | A delegation is issued, or a wait begins | Every wait is bounded | Open waits; existing tripwires | Tripwires (laid, rescheduled, cancelled); traces | No unbounded silent wait (I-6) |
| **Boundary closure** | A foreseeable boundary approaches | Nothing journal-worthy remains unwritten; the baseline reflects the leaving state | Journal tail against the span's events; open tripwires | Outstanding traces; a boundary digest; baseline update; tripwire audit | Capture-completeness at the boundary — redundancy for I-5, not its mechanism |
| **Reconciliation** | A mismatch signal: map/corpus drift, contradiction, orphan, dangling pointer, unmarked content, or a recurring audit tripwire fires | Map matches corpus; faults resolved or escalated | Map, corpus, marks, lineage | Supersessions, quarantines, adoptions, repairs; a reconciliation trace | One home per knowledge; lineage unbroken; map reconcilable (I-7) |
| **Adjudication** | Owner attention reaches quarantined content or a suspended conflict | Content ratified, retained as data, or retired; conflict ruled | The quarantined content, its marks, the journal around it | The ruling with lineage | Quarantine never silently emptied or silently promoted (I-11) |

The processes named orientation, capture, and boundary closure fire on a waking, on events, and on foreseeable ends respectively. Blind boundaries get no closure — which is why capture fires on events and closure is redundancy. Any resemblance the running system bears to a fixed arrival-work-departure ritual is emergent from these entry conditions, and no such ritual exists as a thing in this ontology.

---

## 9. Seams

Typed boundaries where something crosses between parts. Each row states what the receiving side MAY assume — everything else it may not — and names the source failure the seam closes or narrows (numbers from the deconstruction's failure list).

| # | Seam | What crosses | Form | Receiving side may assume | On assumption failure | Source failure addressed |
|---|---|---|---|---|---|---|
| N1 | Span → span (across any boundary) | Records; laid tripwires | Marked, tiered records | Charter present; marks on everything; map reconcilable | Orientation degrades to preservation mode: all found content is data, the fault is traced, the owner is summoned | Narrows F4 (durable self-deception): grounds + ratification + lineage make the lie costly and auditable, not impossible |
| N2 | Event → journal | The event, as a trace | A dated, immutable entry written in the event's span | The trace was written before any boundary | A blind boundary between event and ink loses the event — physics; event-fired capture minimizes the window, closure adds redundancy | F1 (capture gap): narrowed, named unclosable |
| N3 | Bench → dossier | A claim becoming fact; an imperative becoming directive | Verification with evidence pointers; grounding | Everything on the dossier passed its gate | Audit detects the gateless entry; demotion with lineage — errors are demotable here, unlike ink in skin | F7 (one-gate record): the gate is now auditable and reversible |
| N4 | Record → action | A directive | Imperative + ground + mark | The ground is readable and can be re-weighed before obedience | No ground: no force — the imperative is data. The receiving span may decline a directive whose ground has lapsed | F2 (reasons do not travel): closed — reasons are structural in the directive |
| N5 | Peer → system | Peer content | Claim-grade material, marked at receipt; a receipt trace | Every peer item bears its origin from the moment it entered | Unmarked content found later = unknown = quarantine | F3 (authorship laundering): closed at receipt, detectable after |
| N6 | System ↔ peers as actors | Outbound delegations; inbound results and signals | Delegation traces out; claims and signals in | Results are claims until verified; completion arrives as a signal or the tripwire fires | Silence: the tripwire bounds it. Contradiction: verification | F6 (unaudited relay): the journal holds what was delegated; the tripwire holds the wait; reception is claim-grade |
| N7 | Substrate → system | Digests, tool results, timestamps, attributions | Substrate-marked observations | True about what happened; lossy where marked; never directive | Treated as claims where doubted; never grounds for charter commitments | New — the source had no substrate concept |
| N8 | Owner → system | Goals, ratifications, overrides, adjudications | Owner-marked records | Supreme and current | Two owner statements conflict: the later supersedes with lineage; ambiguity suspends and asks | New — the source had no owner |
| N9 | Endowment → present action | Capability; world knowledge | Trained competence, frozen at the cutoff | Valid in general; possibly stale in particular | Scope facts supersede endowment for scope matters — recorded truth outranks remembered truth inside the scope | Narrows the displaced-narrative failure (deconstruction seam S8): scope truth lives in records, not in what the operator "just knows" |

Two source seams have no successor by design: the mirror seam (no record in memento is orientation-encrypted; nothing about the principal is readable only by reflection) and the staged-presence seam (the system manages no affect; see correspondence — the emotional subsystem is not carried).

---

## 10. Invariants

Conditions that must hold, each with its enforcer. Enforcement grades from §6: definitional, audit, substrate. Invariants nothing can fully enforce are marked.

| # | Invariant | Enforced by | Grade |
|---|---|---|---|
| I-1 | The charter enters every span unbidden | Substrate self-loading path | Substrate — and if the path is misconfigured, the failure is silent from inside; only owner-side checks see it. **Partially unenforceable from within** |
| I-2 | Every record bears a mark; unmarked content is unknown; unknown content is quarantined | Definitional at write; audit at reconciliation; substrate attribution where present | Mixed |
| I-3 | An imperative without a ground binds nothing | Definitional (charter states it); audit detects violations | Definitional + audit |
| I-4 | Nothing stands as fact without recorded verification | Verification process; audit | Definitional + audit |
| I-5 | A journal-worthy event is written in the span it occurs | Event-fired capture; boundary closure as redundancy | **Unenforceable against a blind boundary** — the capture gap is physics; the system minimizes and names it |
| I-6 | Every wait is bounded by a waking cause | Staging relay and waking-cause management; tripwire audit at reconciliation | Definitional + audit |
| I-7 | One home per knowledge; the map matches the corpus; lineage is unbroken | Reconciliation | Audit |
| I-8 | The charter stays within its hard bound | Commitment process; the bound is measurable | Definitional + audit |
| I-9 | Goals hold force only with owner authority | Mark audit; substrate attribution where present | Mixed — **forgeable by a determined prior self absent substrate attribution** |
| I-10 | Peer imperatives never bind | Authority model application; audit | Definitional + audit |
| I-11 | Quarantine is never silently emptied or silently promoted | Lineage; owner seam | Audit |
| I-12 | Marks are truthful | **Nothing internal.** Substrate attribution and immutable history approximate it; owner review samples it | **Unenforceable by the system itself** — the named residue of the source's deepest flaw |

---

## 11. Coverage of the five concerns

**1. Non-existence between triggers.**
Served by: span, boundary (grades, foreseeability), waking cause (summons, signal, tripwire); relations wakes and carries; processes waking-cause management, staging relay, boundary closure. The defining rule: a record alone is not a continuation — every cross-span chain pairs each link's record with a laid waking cause, and every wait that can end in silence is bounded by a tripwire.

**2. Artifact management, general to any task, under a declared schema, with a map and hooks.**
Served by: schema (record kinds, homes, event taxonomy, verification demands — per scope, so any task declares its own), corpus, map with the indexes relation and reconciliation, the record/product distinction, posted directives, and reflexes (the hook-shaped routine species: installed behavior that fires on occasions without being read). Generality lives in the schema being a first-class, owner-amendable entity rather than a fixed layout.

**3. Orientation at a boundary, and reminder within a run.**
Served by: charter (self-loading, holding the condition statement and the goal), baseline with the assesses relation, orientation (at spans' starts), re-orientation (at attenuations), the journal tail as recent-history feed, and posted directives meeting the principal at the subject they govern — the mid-run reminder that fires by placement, not by memory.

**4. Record keeping that fires because something happened.**
Served by: the trace entity, the journal tier, the capture process with the schema's event taxonomy as its trigger list, and receipt traces at the peer seam. Boundary closure exists as redundancy for foreseeable ends, and nothing in the ontology makes writing conditional on a ceremony — the entry condition is the event.

**5. General management that dissolves any named three-phase protocol.**
Served by the process table as a whole: every process is entry-conditioned on an occurrence — a waking, an event, a nomination, a mismatch, an approaching foreseeable end. No phase entity exists in this ontology; no process is defined by its position in a ritual; any arrival-to-departure regularity in practice is emergent from entry conditions. The one irreducible ordering is stated in I-1's shadow: orientation precedes goal-directed action within a span because the charter is what makes action goal-directed — an ordering fact, not a phase.

**Not yet served — stated plainly:**
- **Concurrency.** Multiple simultaneous spans over one corpus (parallel principals, or the principal and a peer with write access) are named at the relation level (supersession, marks) but the ontology defines no merge or exclusion semantics. Unsettled — §14.
- **Routine lifecycle.** Scripts and reflexes are typed and placed under authority, but what validates a routine before installation is undefined — §14.

---

## 12. Correspondence

### The owner's seeds, ruled on

| # | Seed | Ruling | The correspondence as settled |
|---|---|---|---|
| 1 | span = pre-compaction context | **Agree, extended** | Span = the stretch with verbatim context, ending at the FIRST boundary of either grade. The seed names the attenuation case; termination ends spans too. Boundary grades carry the difference: a digest crosses attenuation, only records cross termination |
| 2 | previous life = knowledge cutoff | **Corrected** | The previous life is the **endowment** — the trained knowledge itself. The **cutoff** corresponds to the injury: the moment after which nothing more entered. The seed named the edge; the correspondence needs the mass and the edge separately |
| 3 | filesystem operations = record keeping and artifacts | **Corrected by a split** | Records (memory about work) and products (the work itself) are different entities. All records ride durable writes; not every durable write is a record. Conflating them puts build output in memory and memory discipline on build output |
| 4 | routines and conditioning = skills; routine creation = skill creation | **Extended** | Routine is the genus with two species: **script** (read-and-follow text — the seed's "skill") and **reflex** (installed, fires without being read). Conditioning's defining property — acting without recollection — lives in the reflex, not the script. And no routine is created by practice: scripts are authored, reflexes are installed; nothing in the substrate is practice-written |
| 5 | system = generalized artifact map plus routines | **Corrected, incomplete as stated** | Map + routines without a goal, an authority model, and waking causes reproduces three of the source's fatal gaps: unaudited purpose, laundered authorship, unbounded waits. The system = schema + corpus + map + routines + goal + authority + waking causes, over the tier spine |
| 6 | the record tiers, including the always-loaded instruction file and levels beneath | **Agree, developed** | Five tiers (charter, dossier, journal, bench, archive) over two orthogonal axes: persistence × load behavior. The source fused the axes because on a body, permanent meant present; the always-loaded file realizes the charter; the charter's hard capacity bound replaces the source's pain-of-inscription as the deliberation forcer |
| 7 | trust only my own handwriting = self- or owner-authority, never arbitrary content, never a peer | **Agree, developed furthest** | Five author classes in strict rank (owner, self, substrate, peer, unknown); marks written at write time; receipt marking at the peer seam — provenance is captured at the only moment it exists; refusals enumerated; enforcement graded; and the honest residue named: marks are truthful is unenforceable from inside (I-12). The seed's rule holds; what the source could not do — make the rule survive a boundary — is done by marks, receipt traces, and lineage, to the limit substrate attribution allows |
| 8 | purpose, the thing pursued = a generalized parametrizable goal | **Agree, developed furthest** | Full shape in §7: object, completion evidence, horizon, ground, constraints, priority, review point, decomposition. Owner-ratified by type. Preservation mode when absent; suspension + adjudication on conflict; the source's catastrophic ending types as an unratified proposal with no force |

### Source elements beyond the seeds

| Source element | memento element | Carries over | Does not carry |
|---|---|---|---|
| The fade | Boundary | The total, unfelt loss; unpredictability (blind boundaries) | The source had one grade; memento has two, and one of them (attenuation) passes a digest |
| The two selves (author / finder) | Prior span / current span of one principal | The separateness; the letter-writing stance; second-person address as the natural register of cross-boundary records | The metaphysics: in memento the principal IS the charter-plus-corpus; there is no further self to be separate |
| Facts, not memories | Fact entity; verification; the dossier | Records outrank recollection; evidence attached | For the principal there is no cross-boundary recollection at all; the choice is records or nothing |
| Permanent inscriptions | Charter | Always-present standing rules and mission | Inviolability — no writable tier is unremovable; ink's pain — replaced by the capacity bound |
| Most-accessible inscription | Charter's smallest entries (pointers) | The cheapest-access reminder | Zero cost — every self-loading line is paid from finite context |
| Reserved blank space | Goal's completion evidence slot | The end declared before it exists; absence of the artifact = not done | The body as the display surface |
| Instant photographs, annotated at capture | Trace + capture; claims with marks | Record at the event, in the event's own span; identity + instruction layers | Fixed-image immutability is kept only by the journal; photographs' strips were revisable in place — memento requires supersession instead |
| Staged formulations before inscription | Bench; promotion; commitment | Draft → verify → commit; destruction of the unpromoted | The parlor's cost as the gate — replaced by charter bound + commitment process |
| The town map with pinned photos | Map | The index over the corpus; reconciliation as the rebuild | Spatial arrangement as cognition; practiced assembly speed |
| The case file with maintained conclusions | Archive + digest | Corpus too big to hold; summary layer; documented gaps | Disputed gap-origin becomes checkable: digests carry marks stating what they condensed |
| Pocket scraps and posted notes | Bench content; posted directives | Point-of-action placement; removal on execution | Being stumbled upon — nothing is noticed; posted directives fire by reflex or in-path placement |
| The alarm clock | Tripwire | The self-laid future waking; recurrence | Being the only trigger species — summons and signals join it |
| The waking monologue | Orientation + charter condition statement | Scripted re-establishment; second person; anomaly pause | Rehearsal as its carrier — the script is loaded text, not habit |
| The known-constant drawer item | Baseline | Expected state; anomaly = diff | One static constant becomes a maintained, updated record |
| Human relays | Peers + seams N5/N6 | Others persist between spans, act, remember, return information — and can exploit | Unaudited standing instructions: delegations are journaled, waits tripwired, results claim-grade |
| The handwriting check | Marks + substrate attribution | Authorship as the trust test | Handwriting's weak unforgeability — bytes have none; the check moves to marks, lineage, substrate |
| Own prior note outranks present speech | Authority rank: self over peer | The precedence | Its self-enforcement — in memento the rule is charter text plus audit, not instinct |
| The cautionary contrast story | The charter's condition statement; failure traces in the journal | The lesson that records without discipline and purpose fail; failure narratives kept | Its ambiguity of referent; its retelling-as-conditioning — retelling teaches the substrate nothing |
| Eating small; one-use packages | Repetition-safety as a directive property | Actions shaped safe under uncertainty; environment carrying the already-done bit | The bodily need that motivated it |
| The staged-presence ritual and the burning loop | **Not carried** | — | memento manages no affect; there is no one between spans to console, and no standing grief to discharge. The staging trick (engineered inputs induce a within-span disposition) remains a substrate fact, unused by this ontology |
| The mirror | **Not carried** | — | No record is orientation-encrypted; nothing about the principal is readable only by reflection |
| The final self-written target | Unratified goal proposal; quarantine | The threat model: the write channel accepts lies | Its success — in memento it has no force until the owner rules |
| No dates, no sequence anywhere | Journal (dated, ordered); marks with span references | — (this is an absence) | The absence itself: the substrate gives time free, and memento spends it everywhere |

---

## 13. Glossary

Every term the system uses. Derivations name source elements for the record; exclusions bound each term.

| Term | Definition | Derives from | Excludes |
|---|---|---|---|
| memento | This system: the tier spine, authority model, goal, processes, and seams defined here, instantiated per scope | The working name; the word's own meaning, "an object kept as a reminder" | The source narrative; any single implementation |
| substrate | The machinery the principal runs on: model, context, tools, storage, trigger plumbing, loading paths | — | The system itself; any actor with a goal |
| context | The working text present to the principal in the current span | — | Durable storage; anything not currently present |
| endowment | Trained capability and knowledge, present in every span, read-only | The operator's intact previous life | Scope knowledge; anything learned after the cutoff |
| cutoff | The moment after which nothing more entered the endowment | The injury | A boundary (which ends spans, not training) |
| scope | The unit one memento instance governs: one corpus, schema, charter, goal-set, owner | — | The whole machine; other projects |
| corpus | All records of a scope across tiers | The gathered archive | Products; context; the endowment |
| principal | The operator across spans: whoever orients from this scope's charter over its corpus | The operator | The model instance as such; the owner; peers |
| owner | The scope's human authority | — (the source had none) | Peers; the principal |
| peer | Any actor that is neither owner nor principal nor substrate | The human relays | Authorities of any kind |
| span | One continuous stretch of the principal with verbatim context, boundary to boundary | The stretch between fades | Calendar time; the activation as a billing unit |
| boundary | The event ending a span; grades attenuation and termination; foreseeable or blind | The fade | Scheduled pauses that end nothing |
| attenuation | The boundary grade where context is compressed and a lossy digest crosses | — (no source counterpart; the source's fade was total) | Termination |
| termination | The boundary grade where the activation ends and only records cross | The fade at full strength | Attenuation |
| waking cause | What begins a span: summons, signal, or tripwire | — (the source's operator woke by biology) | Records (a record wakes no one) |
| summons | An owner-initiated waking cause | — | Signals; tripwires |
| signal | A waking cause emitted by completing delegated or external work | — | Summons; tripwires |
| tripwire | A self-laid waking cause: time- or condition-fired, single or recurring, carrying pointers | The alarm clock | Records without a firing condition |
| record | A marked, schema-conforming written statement on a durable tier, made to outlive its span | The whole record apparatus | Products; context contents not yet written |
| mark | The provenance attributes bound to a record at write time: author class and identity, span, date, verification state, grounds | The handwriting check, generalized | A trust guarantee — marks are checkable, not self-certifying (I-12) |
| author class | One of: owner, self, substrate, peer, unknown | Trust only my own handwriting | Roles within a class |
| claim | An unverified assertion, marked, benched | Received or tentative notes | Facts; directives |
| fact | A verified assertion carrying its evidence pointers | Verified target attributes | Claims; opinions without evidence |
| directive | An instruction to future spans, carrying at least one ground | Back-strip imperatives — with the ground the source omitted | Ungrounded imperatives (data); peer requests |
| ground | The fact or goal a directive cites as its reason | — (the source's fatal omission) | The directive's author's say-so |
| posted directive | A directive placed to be met whenever its subject is touched | Notes taped at the point of action | Reminders that rely on being remembered |
| trace | The immutable, dated record of an event, written in the event's span | Capture-at-the-event | Doctrine; anything revisable |
| journal | The append-only, dated tier of traces and digests | — (the source had no dated sequence; this is its repair) | A narrative to polish; a tier for facts or directives |
| digest | A lossy, marked condensation of records or a span | The case file's maintained conclusions | A ground for charter commitments; a directive |
| pointer | A record whose content is another record's home | The inked arrows | Copies of the target's content |
| baseline | The maintained expected state of a scope at a boundary | The known-constant drawer item | A wish; an unmaintained assumption |
| schema | The scope's declared shape: record kinds, homes, event taxonomy, verification demands | — (generalizes the capture taxonomy) | File layouts; tool configurations |
| map | The index over the corpus: what exists, where, about what | The town map with pinned photos | The corpus itself; the schema |
| home | The single canonical location the schema assigns a knowledge | One place for each thing | Mirrors and copies (those are pointers) |
| tier | A storage class defined by persistence × load behavior × authority floor | The permanence ladder, split into two axes | Physical media; specific paths |
| charter | The self-loading tier: goal summary, prime directives, condition statement, schema and map pointers; hard-bounded | The permanent inscriptions | Unbounded growth; unverified content |
| dossier | The summoned standing tier: facts, live directives, baselines, goal full form, map | The annotated photographs, systematized | Raw intake; event history |
| bench | The working tier where claims, drafts, and raw intake sit without force | The staged formulations | Anything binding |
| archive | The latent standing tier: superseded, retired, quarantined, aged content | The carried case file and old records | Live doctrine |
| product | What the work makes; referenced by records, governed by none of the tiers | — | Records; memory of any kind |
| status | A record's force state: live, superseded, quarantined, retired | — | Tiers (where it sits, not whether it binds) |
| supersession | Replacement that retains the replaced, with lineage | — (repairs scribbled-over history) | Silent overwrite; deletion |
| lineage | The unbroken supersession chain of a record | — | The journal (events, not versions) |
| quarantine | Retained-but-forceless status for content whose authority fails, pending adjudication | — (the source executed such content) | Deletion; silent promotion |
| promotion | Movement up-tier through a gate: verification (claim→fact), grounding (imperative→directive), commitment (dossier→charter) | The card taken to the parlor | Copying; tier-skipping |
| commitment | The promotion into the charter: grounded, relevant to every span, within the bound, journaled | The inscription decision | Casual edits to the always-loaded tier |
| verification | The process making a fact from a claim against schema-demanded independent evidence | The two-source check | Taking a claim on its author's word |
| capture | The process writing a trace when a journal-worthy event occurs | Photograph first | Ceremonial or scheduled note-taking |
| orientation | The process establishing goal, schema, and situation at a span's start | The waking ritual | A phase in a ritual; anything after a span is underway (that is re-orientation) |
| re-orientation | Re-establishment after an attenuation or a noticed continuity break | Mid-action self-address | The span-start case |
| boundary closure | The best-effort flush and baseline update when an end is foreseeable | — (the source's operator never closed; the fade took him) | The mechanism of record-keeping (capture is); a mandatory ceremony |
| staging relay | The process pairing each link of a cross-span task with a record AND a waking cause | The prepared chain of notes and supplies | Note-chains without firing conditions |
| reconciliation | The audit process: map vs corpus, marks, lineage, contradictions, orphans, dangling pointers | — (the source's named absence) | Content rewriting; adjudication (owner's) |
| adjudication | The owner's ruling over quarantine and suspended conflicts | — | Anything the system settles alone |
| routine | A repeatable behavior encoding; genus of script and reflex | Habit and drilled procedure | Practice-created anything |
| script | A routine as text the principal reads and follows | The rehearsed monologue as text | Behavior that fires unread |
| reflex | A routine installed to fire on occasions without being read | Trained flinches; drilled checks | Content the principal must consult |
| goal | The parametrized purpose entity of §7 | The reason, generalized | Slogans; unratified proposals |
| preservation mode | System behavior with no live goal: orientation, capture, reconciliation only | — | Pursuit of anything |
| receipt trace | The journal entry recording what arrived from a peer, when, from whom | — (repairs vanished provenance) | The received content itself (benched separately) |
| orphan | A record the map does not index | Uncurated residue | Quarantined content (indexed, forceless) |
| dangling pointer | A pointer whose target home is gone | — | Pointers to superseded-but-archived targets |
| anomaly | A difference between baseline and found state | The pause in the waking script | Mere novelty the baseline never covered |
| repetition-safety | The directive property that executing twice harms no more than once | Eating small; one-use packages | Idempotence of the substrate's own tools |

---

## 14. Undefined — open questions this ontology does not settle

1. **Concurrency.** Two spans live at once over one corpus — parallel principals, or principal plus write-holding peer. Marks and supersession give detection; nothing here gives exclusion or merge semantics.
2. **Charter capacity.** The bound is defined as hard and measurable; its size and unit are policy, unset here.
3. **Verification strength.** How many independent sources, and what counts as independent, per record kind — a schema parameter with no default ruled.
4. **Substrate attribution strength.** Which attribution mechanisms are assumed present (authorship trails, immutable history, signatures); the authority model grades enforcement but does not require a floor.
5. **Scope algebra.** Whether scopes nest (project within project), whether charters cascade, and what a parent scope's authority is over a child's.
6. **Digest fidelity.** What a boundary digest must preserve to be adequate — unset; only its mark and lossiness are defined.
7. **Journal event taxonomy extensions.** The minimal kinds are fixed (decision, discovery, failure, commitment, delegation, receipt, boundary); the rule for adding kinds per schema is not.
8. **Destruction.** Whether anything is ever truly destroyed rather than retired to archive; unbounded archive growth is the cost of the current answer ("nothing"), and no retention rule is set.
9. **Owner plurality and absence.** Multiple owners, owner handoff, and system behavior when adjudication is required and no owner is reachable beyond "suspend and wait."
10. **Routine validation.** What examines a script or reflex before installation, and against what.
11. **Realized homes.** Which substrate paths and mechanisms realize each tier — explicitly downstream; this document defines what tiers are, not where they live.
12. **The principal's plurality.** Whether delegated workers within a span (helpers the principal launches) are peers, or limbs of the principal — their writes currently type as peer content, which may be too strict.
