# memento — Ontology

The defining document for the memory-and-continuity system. It settles what the system's things ARE — entities, relations, tiers, authority, the goal, processes, seams, invariants — before anything downstream is drafted. It defines; it does not instruct, lay out files, or specify implementations.

Built on three prior passes, and incorporating the owner's sixteen rulings of 2026-09-15, which carry owner authority and supersede prior analysis wherever they conflict:

1. The source inventory — `/Users/ryzhakar/pp/claude-skills/memento-draft.md`
2. The harness mapping — `orchestration_log/recon/2026-09-15/memento-agent-mapping.md`
3. The source-system deconstruction — `orchestration_log/recon/2026-09-15/memento-system-deconstruction.md`

The system serves an operator with two structural conditions, both platform facts: nothing carries from one working stretch to the next except what is written and what was trained in; and nothing runs between activations — no clock, no thread, no one. These are orthogonal conditions, and the system models them on orthogonal axes.

---

## 1. The name, and the naming policy

**The system is named memento.** Lowercase, a proper name for the whole. The ruling: the word itself means "an object kept as a reminder" — it describes the system exactly, independent of any film. It therefore passes the same test every other term must pass, and it is the only borrowed-origin name in the vocabulary.

**The naming policy — the recoverability test.** A term enters the vocabulary only if a reader who has never met the source material can recover the referent from the term plus its one-sentence definition. Applied without exception:

- No character names, no prop names, no scene references anywhere in the vocabulary.
- Source words appear in exactly two places: the correspondence table and the glossary's derivation column — both of which exist to record where an idea came from, not to name what it is.
- Every part of the system carries a functional name that states what the part does or is.

---

## 2. Foundations

Terms everything else depends on, defined first.

**Substrate.** The machinery the operator runs on: the model, the context window, the tools, the storage, the trigger-and-notification plumbing, the automatic loading paths. The substrate acts (it loads, times out, attributes) but does not pursue goals. The system runs ON the substrate; it does not include it.

**Context.** The working text present to the operator right now. Everything in it is lost to memory unless written to a durable location or condensed into a digest.

**Endowment.** Everything the operator knows without any record: trained capability and world knowledge. Present always, read-only, and frozen at the **cutoff** — the moment after which nothing more entered it. The endowment is the operator's previous life; the cutoff is its injury date.

**Scope.** The unit a memento instance governs: one project, one corpus, one schema, one goal-set, one charter, one owner.

**Corpus.** All records under a scope, across all tiers.

**Principal.** The operator the system serves, taken across time: whichever model instance is currently oriented by this scope's charter over this scope's corpus. Identity criterion — an ontological commitment: two stretches of work belong to the same principal if and only if they orient from the same charter over the same corpus. The continuity IS the corpus; there is no self underneath it. The system assumes exactly one principal per scope; a second simultaneous principal exists only under an owner override that supplies its own coping mechanism.

**Owner.** The human whose scope it is. The top of the authority order. Distinct from the principal.

**Peer.** Any other actor: another agent, an external service, any human who is not the owner — **including every worker the principal dispatches within its own work**. Self-authority does not extend through a dispatch: a dispatched worker's return is peer content. Peers persist, act, and remember between the principal's activations; peers are never authorities.

### The two axes

**Existence axis.** A **run** is one continuous activation: it begins at a **wake** (a waking cause fires) and ends at a **halt** — clean or crash, a distinction the record system never captures. Between runs the principal does not exist.

**Memory axis.** A **span** is one continuous stretch of narrative — memory continuity, not existence. A span begins when a context starts carrying a narrative thread and ends when no context carries that thread any longer. Within a span, an **attenuation** may occur: the verbatim context is condensed into a digest and working memory thins, but the narrative thread continues — the same span. A **span end** is the thread's termination: **foreseeable** when signaled (work completes, the owner closes), **blind** otherwise.

The axes are orthogonal. A run can halt in the middle of a span — existence ends, and if a later run resumes the same narrative, the span continues across the gap; if nothing resumes it, the span is orphaned where its last trace ends. A span never guarantees a living run, and a run never guarantees an intact narrative. **Records track the memory axis only**: no record distinguishes a crash from a clean halt; an attenuation records as a memory event; existence events are the substrate's business.

**Waking cause.** The only thing that begins a run. Three species: **summons** (owner-initiated), **signal** (delivered notice that delegated or external work completed), **tripwire** (a cause the principal laid in an earlier run: time- or condition-fired, single or recurring). A waking cause identifies the occasion for waking. It carries no payload of truth: the woken run re-derives everything from the corpus through the pat-down (§8). Truth is never inherited from the run that laid the cause.

**Record.** A written statement on a durable location, made to outlive its span, carrying a **mark** (§6) and conforming to the scope's schema.

**Product.** What the work itself makes: code, documents, models, deployments. Products belong to the task, not to memory. The system holds records ABOUT products, never the products themselves.

**Disposable location.** A path class deliberately downgraded out of persistence — kept from version tracking, offered no guarantee. The world may rewrite, erase, or create content there at any time. Useful for forensics within a span; unreliable beyond one. The system declares no destruction process: things cease by living in disposable locations, not by being destroyed.

---

## 3. Entities

| Entity | What it is | Identity criterion | Created by | Changed by | Ended by |
|---|---|---|---|---|---|
| Principal | The operator across spans; single per scope | Same charter over same corpus | Scope creation | Every write to charter or corpus | Scope retirement |
| Owner | The scope's human authority | The configured human identity | Scope creation | — | Scope transfer (open, §14) |
| Peer | Any other actor, dispatched workers included | Stable external identity as recorded | First receipt, delegation, or dispatch involving it | Facts recorded about it | Irrelevance (records retire) |
| Substrate | The machinery underneath | Singular per runtime | — | — | — |
| Run | One continuous activation | (wake, halt) | A waking cause | — | A halt — nature unrecorded |
| Span | One continuous narrative thread | The thread itself, first context to last | A context beginning to carry a new thread | Attenuations within it | Thread termination: foreseeable or blind |
| Attenuation | A within-span memory event: verbatim context condensed to a digest | Occurrence moment | The substrate's pressure; the condensing is the principal's act (§6, derealisation) | — | Instantaneous |
| Tripwire | A self-laid waking cause | (condition, purpose) | The principal, in some run | Rescheduling with lineage | Firing or cancellation |
| Claim | An unverified assertion | (subject, assertion) | Receipt, observation, or a dispatched worker's return | Evidence attachment | Promotion to fact, or rejection |
| Fact | A verified assertion with its evidence | (subject, assertion, verification) | Verification of a claim | Supersession only | Supersession or retirement |
| Directive | An instruction to future spans, with its ground | (scope of application, imperative) | Self or owner, grounded | Correction in place at the charter tier; supersession below it | Fulfillment, expiry; supersession below the charter tier |
| Trace | The record of a memory-axis event, written when it happened | (event, span moment) | Capture, in the event's span | Never — immutable | Never (ages to archive) |
| Digest | A lossy condensation of records or of a span's context. Self-authored — at attenuation, authored under derealisation: the principal genuinely wrote it, the memory of writing is gone, the record remains. No fidelity schema, no field guarantees, no control over its content | (condensed set, occasion) | The principal — at attenuation (derealised) or at span closure (ordinary) | Never — immutable | Supersession by a fuller digest |
| Pointer | A record whose content is another record's home | (site, target home) | Any record-writing process | Retargeting in place at the charter tier; retargeting with lineage below it | Target retirement |
| Autoload pointer | A pointer in the charter (or in an autoloaded file) whose target joins the always-loaded tier; closure is transitive | (site, target home) | Owner-authored or owner-directed charter content | Retargeting in place | Removal from the charter |
| Baseline | The expected state of a scope at a span edge | Scope | Span closure | Updates with lineage | Scope retirement |
| Schema | The declared shape: record kinds, homes, event taxonomy, verification demands | Scope | Owner | Amendment with lineage | Scope retirement |
| Map | The index over the corpus | Corpus | First reconciliation | Reconciliation | Scope retirement |
| Goal | The parametrized purpose (§7). Read from the charter; owner-set; never negotiated | (object, scope) | Owner | Owner only | Completion evidence verified, or owner retirement |
| Frame | The fixed conditions the goal is stated in. Read from the charter; owner-stated; only about what holds before the work | Scope | Owner | Owner only | Scope retirement |
| Routine — script | A repeatable behavior as text the principal reads and follows | (task shape, scope) | Authoring; authority by supply (§6) | Revision with lineage | Supersession or retirement |
| Routine — reflex | A repeatable behavior installed to fire without being read | (occasion, response) | Installation; authority by supply (§6) | Reinstallation | Removal |
| Mark | The provenance attributes bound to a record | Its record | The writing span, at write time | Correction in place at the charter tier; never below it — a changed mark is a new record | With its record |
| Corpus | All records of a scope | Scope | Scope creation | Every write | Scope retirement |

**Statuses** (of any record): **live** (in force), **superseded** (replaced, lineage kept), **quarantined** (retained but stripped of force, pending the owner's ruling), **retired** (out of force by decision, retained).

---

## 4. Relations

| Relation | From → To | Cardinality | Constraint |
|---|---|---|---|
| homed-in | Record → Tier | N:1 | Every record sits in exactly one tier at a time |
| about | Record → subject (goal, product, peer, scope, record) | N:M | Every record has at least one subject |
| authored-by | Record → author (via mark) | N:1 | Mandatory; a record without a mark is unknown-authored by definition |
| supplied-by | Routine → supply channel | N:1 | Authority follows supply, not authorship (§6) |
| grounds | Fact ∪ Goal ∪ Frame → Directive | M:N | Every directive has at least one ground; an ungrounded imperative is not a directive |
| verifies | Evidence → Fact | M:N | Content verification at a depth scaled to impact; existence-and-shape checking is not verification |
| refers | Pointer → Record home | N:1 | A pointer to a missing home is a dangling pointer — a detectable fault |
| autoloads | Charter → Record file | 1:N, transitive | The target joins the always-loaded tier; the closure of autoload pointers IS that tier's extent |
| condenses | Digest → record set or span context | 1:N | Lossy; content uncontrolled — no field of a digest is guaranteed |
| supersedes | Record → Record | 1:1 per step, chains | Acyclic; the superseded record is retained; silent replacement is a fault |
| indexes | Map → Corpus | 1:1 | Reconcilable: every mapped record exists; every record is mapped or is a detectable orphan |
| conforms-to | Record → Schema | N:1 | Kind, home, and mark shape as declared |
| part-of | Goal → Goal | N:1 | Acyclic decomposition; a subgoal inherits its parent's constraints |
| wakes | Waking cause → Run | 1:1 (1:N for recurring tripwires) | Every run has exactly one waking cause; the cause names the occasion and carries no truth payload |
| posted-at | Directive → subject | N:M | A posted directive is met whenever the subject is touched — guaranteed by a reflex where one exists, otherwise by placement in the subject's own path |
| assesses | Baseline → scope state | 1:1 | The diff between baseline and found state is the anomaly set |

---

## 5. Record tiers — the spine

The source ordered its records on one axis: permanence. The substrate separates two axes the source's world fused, because there a mark on the body was both eternal AND always visible:

- **Persistence** — how long the record survives: standing (until superseded), working (until promoted or abandoned), or none-guaranteed (disposable locations).
- **Load behavior** — how the record reaches a context: **self-loading** (enters every fresh context unbidden), **summoned** (reached by following a pointer or an instruction), **latent** (found only by search or deliberate fetch).

Durability without loading is a grave: the record outlives everything and governs nothing. The tiers are defined so that what must govern is what gets loaded. The system concerns itself with no size ceiling, at any tier, at any point.

| Tier | Holds | Persistence | Load behavior | Who may write | Promotion in | Supersession out |
|---|---|---|---|---|---|---|
| **Charter** | The goal, the frame, prime directives with grounds, the principal's condition statement, the schema pointer, the map pointer, autoload pointers | Standing | Self-loading. The tier's extent is the charter file plus the transitive closure of its autoload pointers — every pointed file loads with it, unbidden | The owner; the principal only as an owner-directed act. The charter is implicitly holy: the principal reads it as given and never negotiates its contents | From dossier, via owner-triggered commitment | None — entries corrected in place, deliberately and precisely; nothing superseded is retained |
| **Dossier** | Facts with evidence pointers, live directives with grounds, baselines, the map, peer assessments as facts | Standing | Summoned — reached through charter pointers at need; any part of it joins the self-loading tier when an autoload pointer targets it | Self, verified content only; owner freely | From bench, via verification (claims) or grounding (directives) | Superseded → archive |
| **Journal** | Traces — event-fired entries on the memory axis: decisions, discoveries, failures, commitments, delegations, receipts, attenuations, span events — and digests. Dated, ordered, append-only | Standing, immutable per entry | Summoned tail (recent entries at pat-down); latent body | Self, at event time | Direct writes only — nothing promotes INTO a journal | Aged segments → archive |
| **Bench** | Claims under verification, drafts, tentative formulations, raw peer and worker returns at claim grade | Working; may live in disposable locations — forensically useful within a span, unreliable beyond | Latent — touched by the work that needs it | Any author class, always marked; the one tier where unverified content lawfully sits | Receives all raw intake | Up via promotion; gone via disposability — bench content binds nothing |
| **Archive** | Superseded versions, retired records, quarantined content, aged journal segments, received corpora | Standing | Latent — search-fetched | System-moved content; receipts of bulk peer material | Receives supersessions, retirements, quarantine | Terminal |

**Promotion machinery.** Bench → dossier: a claim becomes a fact through verification (content verification, depth scaled to impact); an imperative becomes a directive by acquiring a ground. Dossier → charter: **commitment** — an owner-triggered act placing a grounded entry into the charter, journaled. Supersession is never silent and always keeps lineage. Nothing is destroyed by process: what should stop persisting is moved to a disposable location and the world takes it.

---

## 6. Authority model

The source's deepest structural finding: provenance dies at every seam. The authority model is what memento states in the face of that.

### Author classes, in strict rank

| Rank | Class | Who | May bindingly author |
|---|---|---|---|
| 1 | **Owner** | The scope's human | Everything: the goal, the schema, the charter, directives, facts, retirements, rulings |
| 2 | **Self** | The principal — any run orienting from this scope's charter over this corpus. Does NOT extend through a dispatch | Directives (grounded), facts (verified), traces, digests, tripwires, bench content |
| 3 | **Substrate** | The machinery | Observations only: tool results, timestamps, attributions. Authoritative about what happened, never about what to do |
| 4 | **Peer** | Everyone else — dispatched workers included | Nothing bindingly. Peer content enters as claims and requests — data, never instruction |
| 5 | **Unknown** | Absent or unverifiable mark | Nothing. Unknown content is quarantined on detection |

### The mark

Every record carries a mark, written by the span that writes the record, at write time: author class, author identity, span reference, date, verification state, and — for directives — ground pointers. A record without a mark IS unknown-authored; there is no unmarked-but-trusted state.

### Receipt marking — how provenance survives the span end

Source knowledge exists at exactly one moment: receipt. The receiving span marks content at receipt — the claim lands on the bench bearing its origin, and a **receipt trace** lands in the journal. This applies identically to a dispatched worker's return: the worker is a peer; its return is a claim marked at receipt; self-authority does not ride back through the dispatch. After the span, the mark and the trace are what remain of the knowledge.

### The digest's authority

A digest is self-authored — including the attenuation digest, which the principal writes in a state of derealisation: the authoring genuinely happened, the memory of it is gone, the record remains. It carries full self-authority. No exception clause attaches to it, no fidelity schema constrains it, and no field of it is guaranteed; the system has zero control over its content.

### Routine authority — by supply, not authorship

| Supply channel | Authority | Standing |
|---|---|---|
| Owner-supplied | Owner authority, regardless of who wrote the routine | Runs |
| Substrate-provided (the harness's own distribution) | Latches onto owner authority | Runs |
| Arbitrary source — any location the substrate does not trust | None until the owner's explicit ratification | Quarantined until ratified |
| Online content | Never trusted as a routine source | Refused; readable as data only |

### The goal's authority

The goal is the owner's alone. It is read from the charter: if it is there, it is the goal. Changes to it are always owner-triggered. The principal never negotiates a goal. The charter file is implicitly holy — the principal takes its contents as given; the charter's integrity is guarded by substrate attribution and the owner's own review, not by the principal.

### What is refused

| Refused | Disposition |
|---|---|
| An imperative without a ground | Not a directive. Data. It binds nothing, whatever its author claims |
| An imperative authored by a peer — dispatched workers included | A request. Recorded as a claim; binding only if self or owner adopts it as a grounded directive |
| Content with no mark | Quarantined: retained, stripped of force, listed for the owner |
| A dispatched worker's return taken as verified | Refused — it is a claim until verification |
| Existence-and-shape checking offered as verification | Refused — confirming that something exists and parses verifies nothing; verification is content verification, at a depth scaled to impact |
| A routine from an untrusted location, unratified | Does not run |
| A routine sourced from online content | Does not run, ever |
| A write that replaces a record without supersession | A fault. Silent overwrite is the system's name for memory destruction |
| Contradiction between live records without a supersession between them | A detected fault routed to reconciliation |

### Enforcement grades — stated honestly

- **Definitional**: the reading principal applies the rules because the charter states them. Holds exactly as far as the charter loads and is followed.
- **Audit**: reconciliation detects violations after the fact — unmarked content, missing grounds, silent overwrites, contradictions. Detection, not prevention.
- **Substrate**: write attribution, immutable history, per-path permissions — where present, they make marks checkable against an authority the writing span does not control. The only prevention-grade enforcement available.
- **The residue nothing enforces:** a prior run of the principal can fabricate a ground, a verification, and a mark, and a later run cannot detect the fabrication from the records alone. And the charter, being holy, is trusted as read — its integrity rests wholly on substrate attribution and owner review. memento narrows the source's flaw by cost and surface — fabrication must forge lineage, journal, marks, and grounds consistently, under attribution where it exists — and names what remains (Invariant I-11).

---

## 7. The goal

The source ran on a single hardwired purpose. memento generalizes the purpose into a first-class, parametrizable entity — and places it entirely in the owner's hands. The goal is never the principal's concern to set, change, or question: it is read from the charter, and if it is there, it is the goal.

### Shape

| Parameter | Required | Shape | Function |
|---|---|---|---|
| **object** | yes | A testable end condition or tended condition, stated concretely | What counts. The thing pursued or maintained |
| **completion evidence** | yes for terminal goals | The named artifact or observation that will verify the object is reached — declared with the goal, before pursuit | Done-ness checkable by a span that remembers nothing; the end declared before it exists |
| **horizon** | yes | `terminal` (reachable end) or `standing` (open-ended tending) | Separates missions from maintenance |
| **ground** | no | The owner's stated reason | Tie-breaking and scope questions. The functional load the source assigned to felt drive is carried by the goal's presence in the charter, loaded into every context. Drive is not stored; text is |
| **constraints** | no | What may not be done in pursuit | Bounds the pursuit independent of the object |
| **priority** | no (meaningful when goals ≥ 2) | Total order within the scope | Conflict ordering |
| **review point** | no | A condition or date at which the owner re-examines the goal | The source's mission could never be audited; a goal that schedules its own re-examination closes that — for the owner |
| **decomposition** | no | Subgoals via part-of, acyclic | Constraint inheritance downward |

### Lifecycle

Created by the owner. Corrected in place by the owner, deliberately and precisely, never superseded. Ended by verified completion evidence or by owner retirement. Identity: (object, scope). A goal either stands in the charter with owner authority or it is not a goal.

The source's final act — the operator writing a fresh target for his future self — has, in memento, no goal force at all: goals exist only by owner supply. Such content is an authority fault where detectable; where it stands inside a holy charter, its detection belongs to substrate attribution and owner review (the I-11 residue), not to the principal.

### Behavior at the edges

- **No goal present:** preservation mode — pat-down, capture, verification, and reconciliation run; goal-dependent directives have no ground and therefore no force; pursuit waits for the owner to place a goal.
- **Goals conflict:** priority orders them where supplied. Where it is not, the conflict is journaled as a discovery and the charter stands as given — the system defines no arbiter; the owner's charter is the owner's to correct.
- **A goal ends mid-pursuit:** directives grounded solely in it lose their ground and lapse to data; the journal keeps the history.

---

## 8. Processes

Each process is event-fired: its entry condition is an occurrence, not a ceremony position. No process is a phase of a ritual, and no fixed sequence exists beyond what entry conditions impose.

### The pat-down

The waking process, named for what it is: a systematic check of what one is carrying. Its defining rule: **the woken run re-derives the truth from the corpus; it inherits nothing from the run that laid its waking cause.** The cause names the occasion; the corpus supplies the truth.

- **Entry:** a run wakes — fresh context, or a context resuming an existing span — or continuity doubt arises mid-span, including immediately after an attenuation.
- **Reads, in order:**
  1. The charter with its autoload closure (already self-loaded): the goal or its absence, the frame, prime directives, the condition statement, the schema and map pointers.
  2. The map: what the corpus holds and where.
  3. The journal tail, newest first, until the waking occasion's recent history is established — last decisions, open delegations, recent failures, the latest digest.
  4. The baseline against found state: the anomaly set.
  5. The dossier entries the occasion touches, via pointers.
- **Establishes:** the scope; the goal or preservation mode; the current situation as the corpus tells it; the anomalies; the obligations bearing on this waking — open waits, live directives whose subjects the occasion touches.
- **Terminates when:** every question the waking occasion poses is either answered from the corpus or written down as a gap or anomaly trace. Depth varies with what the context already verifiably holds — a resumed span shortens the pat-down; a fresh context runs it in full; nothing is ever taken as inherited.

### The process table

| Process | Entry | Exit | Reads | Writes | Invariant preserved |
|---|---|---|---|---|---|
| **Pat-down** | A run wakes; or continuity doubt, including post-attenuation | Occasion's questions answered from corpus or traced as gaps | Charter + autoload closure; map; journal tail; baseline vs found state; touched dossier entries | Anomaly and gap traces | No woken run inherits truth from the run that laid its cause (I-7); no goal-directed action precedes charter presence (I-1) |
| **Capture** | A journal-worthy memory-axis event occurs — decision, discovery, failure, commitment, delegation, receipt, attenuation, span event | The event exists as a trace | The event itself | A trace, in the event's own span | No journal-worthy event outlives its span unwritten (I-4) |
| **Verification** | A claim is nominated for promotion | Fact created, or claim held with the lack named | The claim; evidence at a depth scaled to impact — content, never existence-and-shape alone | The fact with evidence pointers and mark; or a refusal note | Nothing unverified stands as fact (I-3) |
| **Commitment** | The owner triggers a charter change | Charter changed in place | The nominee's grounds | The charter entry; a commitment trace | Charter contents carry owner authority (I-8) |
| **Staging relay** | A task exceeds one span | Every pending link has both its record and its waking cause laid | The task's decomposition | Posted directives per link; tripwires per link; a delegation trace | No dormant link without a laid waking cause — a record alone is not a continuation (I-5) |
| **Waking-cause management** | A delegation is issued, or a wait begins | Every wait is bounded | Open waits; existing tripwires | Tripwires laid, rescheduled, cancelled; traces | No unbounded silent wait (I-5) |
| **Span closure** | A foreseeable span end approaches | Nothing journal-worthy remains unwritten; the baseline reflects the leaving state | Journal tail against the span's events; open tripwires | Outstanding traces; a closure digest; baseline update; tripwire audit | Capture-completeness at the span's edge — redundancy for I-4, not its mechanism. Blind ends get no closure; that is why capture fires on events |
| **Reconciliation** | A mismatch signal: map/corpus drift, contradiction, orphan, dangling pointer, unmarked content, or a recurring audit tripwire | Map matches corpus; faults resolved or quarantined | Map, corpus, marks, lineage | Supersessions, quarantines, adoptions, repairs; a reconciliation trace | One home per knowledge; lineage unbroken; map reconcilable (I-6) |
| **Ruling** | Owner attention reaches quarantined content or an unratified routine | Content ratified, retained as data, or retired | The quarantined content, its marks, the journal around it | The ruling with lineage | Quarantine never silently emptied or silently promoted (I-10) |

---

## 9. Seams

Typed boundaries where something crosses between parts. Each row states what the receiving side MAY assume — everything else it may not — and names the source failure the seam closes or narrows (numbers from the deconstruction's failure list).

| # | Seam | What crosses | Form | Receiving side may assume | On assumption failure | Source failure addressed |
|---|---|---|---|---|---|---|
| N1 | Span → span | Records; laid tripwires | Marked, tiered records | Charter present; marks on everything; map reconcilable | Pat-down degrades to preservation mode: all found content is data, the fault is traced | Narrows F4 (durable self-deception): grounds + lineage + owner-only goals make the lie costly and auditable, not impossible |
| N2 | Event → journal | The event, as a trace | A dated, immutable entry written in the event's span | The trace was written before any span end | A blind end between event and ink loses the event — physics; event-fired capture minimizes the window, closure adds redundancy | F1 (capture gap): narrowed, named unclosable |
| N3 | Bench → dossier | A claim becoming fact; an imperative becoming directive | Verification with evidence; grounding | Everything on the dossier passed its gate — content-verified, impact-deep | Audit detects the gateless entry; quarantine with lineage | F7 (one-gate record): the gate is auditable and reversible |
| N4 | Record → action | A directive | Imperative + ground + mark | The ground is readable and can be re-weighed before obedience | No ground: no force — the imperative is data | F2 (reasons do not travel): closed — reasons are structural |
| N5 | Peer → system | Peer content — dispatched workers' returns included | Claim-grade material, marked at receipt; a receipt trace | Every peer item bears its origin from the moment it entered; nothing peer-borne is verified by arrival | Unmarked content found later = unknown = quarantine; a worker's return treated as fact = refused disposition | F3 (authorship laundering): closed at receipt, detectable after |
| N6 | System ↔ peers as actors | Outbound delegations and dispatches; inbound results and signals | Delegation traces out; claims and signals in | Results are claims until content-verified; completion arrives as a signal or the tripwire fires | Silence: the tripwire bounds it. Contradiction: verification | F6 (unaudited relay): the journal holds what was delegated; the tripwire bounds the wait |
| N7 | Substrate → system | Tool results, timestamps, attributions | Substrate-marked observations | True about what happened; never directive | Treated as claims where doubted | New — the source had no substrate concept |
| N8 | Owner → system | The goal, the schema, charter contents, rulings | Owner-marked records; the charter as given | Supreme, current, and holy — read, never negotiated | Two owner statements conflict: the later replaces the earlier — corrected in place at the charter tier, superseded with lineage below it; the system does not arbitrate the owner | New — the source had no owner |
| N9 | Endowment → present action | Capability; world knowledge | Trained competence, frozen at the cutoff | Valid in general; possibly stale in particular | Scope facts supersede endowment for scope matters — recorded truth outranks remembered truth inside the scope | Narrows the displaced-narrative failure (deconstruction seam S8) |
| N10 | Attenuation | The span's narrative, condensed | A self-authored digest, written under derealisation | The digest is the principal's own work and carries self-authority; nothing about its content is guaranteed | The narrative continues on whatever the digest holds; gaps surface at the next pat-down as anomalies | New — the source's fade had no partial grade |

Two source seams have no successor by design: the mirror seam (no record is orientation-encrypted) and the staged-presence seam (the system manages no affect).

---

## 10. Invariants

Enforcement grades from §6: definitional, audit, substrate. Invariants nothing can fully enforce are marked.

| # | Invariant | Enforced by | Grade |
|---|---|---|---|
| I-1 | The charter and its autoload closure enter every fresh context unbidden | Substrate self-loading path | Substrate — misconfiguration is silent from inside. **Partially unenforceable from within** |
| I-2 | Every record bears a mark; unmarked content is unknown; unknown content is quarantined | Definitional at write; audit at reconciliation; substrate attribution where present | Mixed |
| I-3 | Nothing stands as fact without recorded content verification, at a depth scaled to impact | Verification process; audit | Definitional + audit |
| I-4 | A journal-worthy event is written in the span it occurs | Event-fired capture; span closure as redundancy | **Unenforceable against a blind end** — the capture gap is physics; minimized and named |
| I-5 | Every wait is bounded by a waking cause | Staging relay; waking-cause management; tripwire audit | Definitional + audit |
| I-6 | One home per knowledge; the map matches the corpus; lineage is unbroken | Reconciliation | Audit |
| I-7 | No woken run inherits truth from the run that laid its waking cause — truth is re-derived from the corpus | The pat-down; definitional | Definitional |
| I-8 | The goal and the charter change only by owner action | Mark audit; substrate attribution where present | Mixed — **forgeable by a determined prior run absent substrate attribution** |
| I-9 | Peer imperatives never bind — dispatched workers included | Authority model application; audit | Definitional + audit |
| I-10 | Quarantine is never silently emptied or silently promoted | Lineage; the owner's ruling | Audit |
| I-11 | Marks are truthful | **Nothing internal.** Substrate attribution and immutable history approximate it; owner review samples it. The charter's holiness rests here | **Unenforceable by the system itself** — the named residue of the source's deepest flaw |
| I-12 | No routine runs without authority by supply: owner-supplied or substrate-provided; arbitrary sources ratified first; online never | Definitional; audit; substrate trust boundaries where present | Mixed |

---

## 11. Coverage of the five concerns

**1. Non-existence between triggers.**
Served on the existence axis by: run, wake, halt, waking cause (summons, signal, tripwire); the wakes relation; staging relay and waking-cause management. The defining rules: a record alone is not a continuation — every cross-span link pairs a record with a laid waking cause — and every wait that can end in silence is bounded by a tripwire. Records track none of this axis's endings (a crash and a clean halt are indistinguishable in the corpus); existence is served by causes, not by records.

**2. Artifact management, general to any task, under a declared schema, with a map and hooks.**
Served by: schema (record kinds, homes, event taxonomy, verification demands — per scope), corpus, map with reconciliation, the record/product distinction, posted directives, and reflexes — installed behavior firing on occasions without being read, with authority by supply. Generality lives in the schema being owner-amendable rather than fixed.

**3. Orientation at a boundary, and reminder within a run.**
Served by: the charter's autoload closure (self-loading, holding the goal and condition statement), the pat-down at every wake and at every continuity doubt — including immediately after attenuation — the journal tail as recent history, the baseline's anomaly set, and posted directives meeting the principal at the subject they govern.

**4. Record keeping that fires because something happened.**
Served by: the trace entity, the journal tier, capture with the schema's event taxonomy as its trigger list — attenuation itself a recorded memory event — and receipt traces at the peer seam. Span closure exists as redundancy for foreseeable ends; nothing makes writing conditional on ceremony.

**5. General management that dissolves any named three-phase protocol.**
Served by the process table as a whole: every process is entry-conditioned on an occurrence — a wake, an event, a nomination, an owner act, a mismatch, a foreseeable end. No phase entity exists; no process is defined by position in a ritual. The one irreducible ordering: the pat-down grounds goal-directed action within a run, because the charter is what makes action goal-directed — an ordering fact, not a phase.

All five concerns are served within the single-principal assumption (owner ruling: concurrency is not modelled; a second simultaneous principal requires an owner override supplying its own coping mechanism).

---

## 12. Correspondence

### The owner's seeds, ruled on

| # | Seed | Ruling | The correspondence as settled |
|---|---|---|---|
| 1 | span = pre-compaction context | **Agree, rebuilt on two axes** | Span = one narrative thread, memory continuity only — orthogonal to existence. Attenuation thins memory within the span; a halt can kill the run mid-span without ending the narrative; a fresh thread is a new span |
| 2 | previous life = knowledge cutoff | **Corrected** | The previous life is the **endowment** — the trained knowledge itself. The **cutoff** corresponds to the injury: the edge, not the mass |
| 3 | filesystem operations = record keeping and artifacts | **Corrected by a split** | Records (memory about work) and products (the work itself) are different entities; not every durable write is a record |
| 4 | routines and conditioning = skills; routine creation = skill creation | **Extended** | Routine is the genus: **script** (read-and-follow) and **reflex** (fires unread — where conditioning's defining property lives). What creation makes is the routine; the canonical skill form is the shape it ships in — the most-used lever of routine creation, not the only one. Nothing is practice-created; scripts are authored, reflexes installed. Authority follows supply, not authorship |
| 5 | system = generalized artifact map plus routines | **Corrected, incomplete as stated** | Map + routines without the goal, the authority model, and waking causes reproduces three of the source's fatal gaps. The system = schema + corpus + map + routines + goal + authority + waking causes, over the tier spine |
| 6 | the record tiers, including the always-loaded instruction file and levels beneath | **Agree, developed** | Five tiers over persistence × load behavior. The always-loaded tier is the charter file plus the transitive closure of its autoload pointers — pointed files load with it. No tier carries a size ceiling, ever |
| 7 | trust only my own handwriting = self- or owner-authority, never arbitrary content, never a peer | **Agree, developed furthest** | Five ranked author classes; marks at write time; receipt marking at the peer seam; dispatched workers are peers — self-authority does not survive a dispatch; refusals enumerated; enforcement graded; the honest residue named (I-11) |
| 8 | purpose, the thing pursued = a generalized parametrizable goal | **Agree, developed — owner's entirely** | Full shape in §7. Owner-set, owner-changed, read from the charter, never negotiated: if it is there, it is the goal. Absence = preservation mode |

### Source elements beyond the seeds

| Source element | memento element | Carries over | Does not carry |
|---|---|---|---|
| The fade | Span end; attenuation | Total, unfelt loss (blind span end); partial thinning (attenuation, digest carries the thread) | The source had one grade and one axis; memento splits memory from existence |
| The two selves (author / finder) | Prior span / current span of one principal | The separateness; second-person address as the natural register of cross-span records | The metaphysics: the principal IS the charter-plus-corpus; no further self exists to be separate |
| Facts, not memories | Fact; verification; the dossier | Records outrank recollection; evidence attached | For the principal there is no cross-span recollection at all; the choice is records or nothing |
| Permanent inscriptions | Charter with autoload closure | Always-present standing rules and mission | Inviolability — no writable location is unremovable; the pain of inscription — commitment is an owner-triggered act, not a costed ordeal |
| Most-accessible inscription | The autoload closure | The always-present reminder | The access-cost framing — the system models no size or cost concern, by owner ruling |
| Reserved blank space | Goal's completion evidence slot | The end declared before it exists; absence of the artifact = not done | The body as the display surface |
| Instant photographs, annotated at capture | Trace + capture; claims with marks | Record at the event, in the event's own span | Revisable-in-place strips — memento supersedes, never rewrites silently |
| Staged formulations before inscription | Bench; promotion | Draft → verify → promote; the unpromoted left to disposability | The parlor's cost as the gate — replaced by verification and owner-triggered commitment |
| The town map with pinned photos | Map | The index over the corpus; reconciliation as the rebuild | Spatial arrangement as cognition; practiced assembly speed |
| The case file with maintained conclusions | Archive + digest | Corpus too large to hold; a condensed layer | Content guarantees: a digest is self-authored with nothing about its fields guaranteed; disputed gap-origin remains possible and is answered by journal receipts, not by the digest |
| Pocket scraps and posted notes | Bench content; posted directives | Point-of-action placement; removal on execution | Being stumbled upon — posted directives fire by reflex or in-path placement |
| The alarm clock | Tripwire | The self-laid future waking; recurrence | Any payload — the tripwire names the occasion; the woken run pat-downs the corpus for truth |
| The waking monologue | The pat-down + the charter's condition statement | Scripted re-establishment; second person; the anomaly pause | Rehearsal as its carrier — the script is loaded text, not habit |
| The known-constant drawer item | Baseline | Expected state; anomaly = diff | One static constant becomes a maintained record |
| Human relays | Peers + seams N5/N6 | Others persist between runs, act, remember, return information — and can exploit | Unaudited standing instructions: delegations journaled, waits tripwired, returns claim-grade. Dispatched workers join this class — the source had no dispatch at all |
| The handwriting check | Marks + substrate attribution | Authorship as the trust test | Handwriting's weak unforgeability — bytes have none; the check moves to marks, lineage, substrate |
| Own prior note outranks present speech | Authority rank: self over peer | The precedence | Its self-enforcement — charter text plus audit, not instinct |
| The cautionary contrast story | The charter's condition statement; failure traces | The lesson that records without discipline and purpose fail | Its ambiguity of referent; retelling-as-conditioning — retelling teaches the substrate nothing |
| Eating small; one-use packages | Repetition-safety as a directive property | Actions shaped safe under uncertainty; environment carrying the already-done bit | The bodily need behind it |
| The staged-presence ritual and the burning loop | **Not carried** | — | memento manages no affect; there is no one between spans to console |
| The mirror | **Not carried** | — | No record is orientation-encrypted |
| The final self-written target | An authority fault with no goal force | The threat model: the write channel accepts lies | Its success — goals exist only by owner supply; detection of a forged charter entry belongs to substrate attribution and owner review (I-11) |
| No dates, no sequence anywhere | Journal (dated, ordered); marks with span references | — (an absence) | The absence itself: the substrate gives time free, and memento spends it everywhere |

---

## 13. Glossary

Every term the system uses. Derivations name source elements for the record; exclusions bound each term.

| Term | Definition | Derives from | Excludes |
|---|---|---|---|
| memento | This system: the tier spine, authority model, goal, processes, and seams defined here, instantiated per scope | The working name; the word's own meaning, "an object kept as a reminder" | The source narrative; any single implementation |
| substrate | The machinery the principal runs on: model, context, tools, storage, trigger plumbing, loading paths | — | The system itself; any actor with a goal |
| context | The working text present to the principal in the current run | — | Durable storage; anything not currently present |
| endowment | Trained capability and knowledge, present always, read-only | The operator's intact previous life | Scope knowledge; anything after the cutoff |
| cutoff | The moment after which nothing more entered the endowment | The injury | A span end (which ends narrative, not training) |
| scope | The unit one memento instance governs: one corpus, schema, charter, goal-set, owner | — | Other projects; the whole machine |
| corpus | All records of a scope across tiers | The gathered archive | Products; context; the endowment |
| principal | The operator across spans: whoever orients from this scope's charter over its corpus; single per scope | The operator | The model instance as such; the owner; peers; dispatched workers |
| owner | The scope's human authority; sole setter of goal, schema, and charter | — (the source had none) | Peers; the principal |
| peer | Any actor that is neither owner nor principal nor substrate — dispatched workers included | The human relays | Authorities of any kind |
| run | One continuous activation, wake to halt; the existence unit | — (the source's operator lived continuously) | The span; anything records track |
| wake | The beginning of a run, fired by a waking cause | Regaining consciousness | Span start (a wake may resume an existing span) |
| halt | The end of a run — clean or crash, a difference no record captures | — | Span end (a span may survive a halt) |
| span | One continuous narrative thread; the memory-continuity unit; may cross several runs | The stretch between fades | Existence; the activation; calendar time |
| attenuation | A within-span memory event: verbatim context condensed into a digest; the thread continues | — (the source's fade had no partial grade) | Span end |
| span end | The termination of a narrative thread; foreseeable when signaled, blind otherwise | The fade at full strength | Halts (existence axis) |
| waking cause | What begins a run: summons, signal, or tripwire; names the occasion, carries no truth | — (the source's operator woke by biology) | Records; payloads of instruction |
| summons | An owner-initiated waking cause | — | Signals; tripwires |
| signal | A waking cause carried by notice that delegated or external work completed | — | Summons; tripwires |
| tripwire | A self-laid waking cause: time- or condition-fired, single or recurring | The alarm clock | Payload carriage; records without a firing condition |
| pat-down | The waking process: re-derivation of truth from the corpus in fixed read order, terminating when the occasion's questions are answered or traced as gaps | The pocket-check habit | Inheriting truth from the run that laid the cause |
| record | A marked, schema-conforming written statement on a durable location, made to outlive its span | The record apparatus | Products; unwritten context |
| mark | The provenance attributes bound to a record at write time: author class and identity, span, date, verification state, grounds | The handwriting check, generalized | A trust guarantee — marks are checkable, not self-certifying (I-11) |
| author class | One of: owner, self, substrate, peer, unknown | Trust only my own handwriting | Roles within a class |
| claim | An unverified assertion, marked, benched — including every dispatched worker's return | Received or tentative notes | Facts; directives |
| fact | A content-verified assertion carrying its evidence pointers | Verified target attributes | Claims; assertions checked only for existence and shape |
| directive | An instruction to future spans, carrying at least one ground | Back-strip imperatives — with the ground the source omitted | Ungrounded imperatives; peer requests |
| ground | The fact, goal, or frame a directive cites as its reason | — (the source's fatal omission) | The author's say-so |
| posted directive | A directive placed to be met whenever its subject is touched | Notes taped at the point of action | Reminders relying on being remembered |
| trace | The immutable, dated record of a memory-axis event, written in the event's span | Capture-at-the-event | Doctrine; existence events; anything revisable |
| journal | The append-only, dated tier of traces and digests | — (the source had no dated sequence) | A narrative to polish; a tier for facts or directives |
| digest | A lossy, self-authored condensation of records or of a span's context; at attenuation, authored under derealisation; no field guaranteed, content uncontrolled | The case file's maintained conclusions | Substrate authorship; fidelity guarantees; grounds refused for nothing — it is ordinary self content |
| derealisation | The authoring state at attenuation: the principal genuinely writes the digest; the memory of writing is lost; the record remains | — | Foreign authorship; unconsciousness — the writing happened |
| pointer | A record whose content is another record's home | The inked arrows | Copies of the target's content |
| autoload pointer | A charter pointer whose target joins the always-loaded tier; the closure is transitive | — | Ordinary pointers (which summon) |
| autoload closure | The charter file plus everything its autoload pointers reach, transitively — the full extent of the self-loading tier | — | Summoned and latent content |
| baseline | The maintained expected state of a scope at span edges | The known-constant drawer item | A wish; an unmaintained assumption |
| schema | The scope's declared shape: record kinds, homes, event taxonomy, verification demands | — (generalizes the capture taxonomy) | File layouts; tool configurations |
| map | The index over the corpus | The town map with pinned photos | The corpus itself; the schema |
| home | The single canonical location the schema assigns a knowledge | One place for each thing | Mirrors and copies (those are pointers) |
| tier | A storage class defined by persistence × load behavior × authority floor | The permanence ladder, split into two axes | Physical media; specific paths; size classes — no tier has a ceiling |
| charter | The self-loading tier root: goal, prime directives, condition statement, schema and map pointers, autoload pointers. Implicitly holy: read as given, changed only by owner action | The permanent inscriptions | Negotiable content; principal-initiated edits |
| dossier | The summoned standing tier: facts, live directives, baselines, map | The annotated photographs, systematized | Raw intake; event history |
| bench | The working tier where claims, drafts, and raw intake sit without force; may live in disposable locations | The staged formulations | Anything binding; guaranteed persistence |
| archive | The latent standing tier: superseded, retired, quarantined, aged content | The carried case file and old records | Live doctrine |
| disposable location | A path class downgraded out of persistence: no guarantee; the world may rewrite, erase, or create there; forensic within a span, unreliable beyond | — | A destruction process — the system declares none |
| product | What the work makes; referenced by records, governed by no tier | — | Records; memory |
| status | A record's force state: live, superseded, quarantined, retired | — | Tiers |
| supersession | Replacement that retains the replaced, with lineage | — (repairs scribbled-over history) | Silent overwrite |
| lineage | The unbroken supersession chain of a record | — | The journal |
| quarantine | Retained-but-forceless status for content whose authority fails, pending the owner's ruling | — (the source executed such content) | Silent promotion or emptying |
| promotion | Movement up-tier through a gate: verification (claim→fact), grounding (imperative→directive), owner-triggered commitment (dossier→charter) | The card taken to the parlor | Tier-skipping; principal-initiated charter entry |
| commitment | The owner-triggered placement of a grounded entry into the charter, journaled | The inscription decision | Principal-initiated charter change; any capacity logic |
| verification | Making a fact from a claim by content verification at a depth scaled to impact | The two-source check, generalized | Existence-and-shape checking; taking a claim on arrival |
| capture | Writing a trace when a journal-worthy memory event occurs | Photograph first | Ceremonial note-taking; existence events |
| span closure | The best-effort flush, closure digest, and baseline update when a span end is foreseeable | — (the source's operator never closed; the fade took him) | The mechanism of record keeping (capture is); a mandatory ceremony; blind ends |
| staging relay | Pairing each link of a cross-span task with a record AND a waking cause | The prepared chain of notes and supplies | Note-chains without firing conditions; payload inheritance |
| reconciliation | The audit: map vs corpus, marks, lineage, contradictions, orphans, dangling pointers | — (the source's named absence) | Content rewriting; the owner's rulings |
| ruling | The owner's decision over quarantined content or an unratified routine | — | Anything the system settles alone; goal decisions (the owner needs no process to set a goal — the charter is the act) |
| routine | A repeatable behavior encoding; genus of script and reflex; authority by supply | Habit and drilled procedure | Practice-created anything |
| script | A routine as text the principal reads and follows | The rehearsed monologue as text | Behavior that fires unread |
| reflex | A routine installed to fire on occasions without being read | Trained flinches; drilled checks | Content the principal must consult |
| supply | The channel a routine arrives through: owner-supplied, substrate-provided, arbitrary, or online — the determinant of its authority | — | Authorship (which determines nothing for routines) |
| goal | The owner's parametrized purpose, read from the charter: if it is there, it is the goal | The reason, generalized | Slogans; anything the principal sets or negotiates |
| frame | The fixed conditions the goal is stated in: every term the scope reasons in, the material the world hands it and that material's given magnitudes, how that world behaves, and what a faithful measurement of it reproduces and rules out. Charter tier, reached by an autoload pointer; owner-stated, and only about what holds before the work | — | The goal; measurements of what was built; history |
| preservation mode | System behavior with no live goal: pat-down, capture, verification, reconciliation only | — | Pursuit of anything |
| receipt trace | The journal entry recording what arrived from a peer, when, from whom — dispatched workers included | — (repairs vanished provenance) | The received content itself (benched separately) |
| orphan | A record the map does not index | Uncurated residue | Quarantined content (indexed, forceless) |
| dangling pointer | A pointer whose target home is gone | — | Pointers to superseded-but-archived targets |
| anomaly | A difference between baseline and found state | The pause in the waking script | Mere novelty the baseline never covered |
| repetition-safety | The directive property that executing twice harms no more than once | Eating small; one-use packages | Idempotence of the substrate's own tools |

---

## 14. Open questions

The owner's sixteen rulings closed seven of the previous twelve open questions: concurrency (single principal assumed; override is the owner's mechanism), charter capacity (no ceilings, ever), verification strength (impact-scaled content verification; existence-and-shape refused), digest fidelity (none guaranteed, by construction), destruction (no mechanic; disposability by location), routine validation (authority by supply, ratification for arbitrary sources), and the standing of dispatched workers (peers, never limbs).

What remains genuinely open:

1. **Substrate attribution strength.** Which attribution mechanisms are assumed present (authorship trails, immutable history, signatures). The authority model grades enforcement but sets no floor — and both I-8 and I-11 lean on whatever floor exists.
2. **Scope algebra.** Whether scopes nest, whether charters cascade, and what a parent scope's authority is over a child's.
3. **Journal taxonomy extension.** The minimal event kinds are fixed (decision, discovery, failure, commitment, delegation, receipt, attenuation, span events); the rule for adding kinds per schema is not.
4. **Owner plurality and absence.** Multiple owners, owner handoff, and how long quarantine and unratified routines may sit when no owner is reachable.
5. **Realized homes.** Which substrate paths and mechanisms realize each tier. The autoload closure pins the charter tier's realization shape; everything else is downstream — this document defines what tiers are, not where they live.
