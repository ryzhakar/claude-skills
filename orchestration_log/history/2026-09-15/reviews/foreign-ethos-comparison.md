# Foreign Skill-Authoring Ethos — Comparison

The document believes a skill is a context-budget problem. Its unit of concern is the token resting in the agent's window, not the instruction the agent declines to follow. From that premise it derives everything: shrink SKILL.md, push branch-specific material behind pointers into bundled files, prefer user invocation so no description costs you tokens at rest, compress prescriptions into dense terms the model already has priors for, and prune whatever a deletion test shows to be inert. It trusts the agent to obey a skill once loaded; its only verification is watching a chosen term surface in the reasoning trace. It never asks what happens when a reported step did not run.

## Foreign claims

### Platform mechanics (checkable)

**M1.** A skill's `description` loads into the agent's context at rest; the SKILL.md body loads only on invocation.
**M2.** `disable-model-invocation: true` withholds the description from the agent, leaving the skill user-invokable only.
**M3.** Each model-invoked skill costs one description on every request; 100 skills cost 100 descriptions.
**M4.** A model may decline to follow a context pointer even when the target fits the task perfectly.
**M5.** Reference files bundled beside SKILL.md are easy for the agent to pull in.
**M6.** A leading word surfaces in the reasoning trace, giving an observable signal that the steer landed.
**M7.** Splitting a two-step process into two skills hides the second step from the agent during the first.

### Authoring opinions

**A1.** Decide explicitly whether each skill is user-invoked or model-invoked.
**A2.** Prefer user-invoked; trade agent unpredictability for user cognitive load.
**A3.** Model-invoked skills force you to eval whether they fire at the right time.
**A4.** Compose every skill from two units: steps and reference.
**A5.** Author top-down — write the steps, then derive the reference each step needs.
**A6.** Make SKILL.md as small as possible.
**A7.** Branch test: reference used on every branch stays inline; branch-specific reference moves behind a context pointer.
**A8.** Steer with leading words — dense terms that trigger the model's priors, repeated consistently, verified in the trace.
**A9.** Split a skill to raise legwork on the current step by hiding the future goal.
**A10.** Single source of truth; never duplicate reference material.
**A11.** Hunt "sediment" — material nobody dared delete. Restructure or kill it.
**A12.** Deletion test: cut the passage. If behavior would not change, it was a no-op. Leave it cut.
**A13.** Massive skills are a symptom of the other failures, not a failure themselves.
**A14.** Put a human-in-the-loop checkpoint inside the step sequence.
**A15.** Skill quality needs a shared rubric.

## Correspondence

| Foreign claim | Project position | Bucket | Operative / inert | Evidence |
|---|---|---|---|---|
| A1 invocation mode is a decision | none (19 of 19 model-invoked by default) | FOREIGN-ONLY | OPERATIVE | doc — project never made the call |
| A2 prefer user-invoked | none stated; 1 measured accident | ALREADY-TESTED (n=1) | OPERATIVE | split — see below |
| A3 model invocation forces evals | none | FOREIGN-ONLY | INERT — names a consequence, not a writing move | doc, scope-limited |
| A4 steps + reference units | 15 (XML lifecycle tags) | FOREIGN-ONLY (orthogonal taxonomy) | OPERATIVE | neither — 15 is an orchestrator call at 1 of 19 |
| A5 steps first, reference after | none | FOREIGN-ONLY | OPERATIVE | doc |
| A6 as small as possible | 3 (compression measured, never estimated) | CONVERGENT in direction | INERT — no ceiling, no measurement, no stopping rule | project |
| A7 branch test → context pointer | 1 (zero external reference; 3-condition exception) | CONFLICTING + ALREADY-TESTED | OPERATIVE | project, decisively |
| A8 leading words | 2 (directive force); manifesto-oath's compliance-vs-performance vocabulary | CONVERGENT, unnamed on the project side | OPERATIVE | both; M6 is the doc's addition |
| A9 split to hide the future goal | 13 (no escape hatch); subagent isolation | CONVERGENT on goal | OPERATIVE | project mechanism stronger |
| A10 single source of truth | 1 corollary ("cross-skill duplication is acceptable") | CONFLICTING | OPERATIVE | project cross-skill; doc within one skill |
| A11 sediment | none by name; visible in positions 8, 11, 15 | FOREIGN-ONLY (label) | INERT — a diagnosis with no test; its actionable half collapses into A7 | doc, as vocabulary only |
| A12 deletion test | none | FOREIGN-ONLY | OPERATIVE — the sharpest claim in the document | doc |
| A13 size is a symptom | 3 | CONVERGENT | INERT — restates A6 | neither |
| A14 human checkpoint in steps | 9 (phase gates on verified artifact) | CONVERGENT | OPERATIVE | project — its gate names an artifact |
| A15 shared rubric | ETHOS.md + this stance report | CONVERGENT, already built | INERT for a model; addresses maintainers | project |

## Convergent

**A8 / leading words is the real convergence, and it is undocumented on the project side.** manifesto-oath states the thesis as a platform fact — "operating identity" and "constitutional constraint" activate compliance circuits, "swear" and "promise" activate performance circuits. Position 5 does the same work at the verb layer: "do", "make", "research" are declared delegation directives inside four named skills, exact match, zero drift. Two authors reached the same mechanism from opposite directions without a shared vocabulary. The doc contributes the verification loop (M6) the project lacks: read the trace, confirm the term echoes back. Neither position 2 nor position 5 is checkable today.

**A9 / hiding the future goal.** The doc splits skills; the project delegates to a subagent whose prompt carries one step. Same diagnosis — the agent sees a downstream goal and shortchanges the step it is on. The project's mechanism is stronger, and see the correction on M7.

**A6, A13, A14, A15 converge weakly.** The project holds each already, with a measurement or an artifact the doc does not supply.

Note the license grades: only position 3 among the convergent set carries a revised-against-measurement license. The rest are owner rulings. Independent convergence on positions 8 and 12 — the two measured-failure positions in the compression neighborhood — never happens, because the doc never addresses either.

## Conflicting

**A7 vs. position 1.** The doc prescribes moving branch-specific reference into a bundled file behind a pointer. ETHOS states the opposite flat: models ignore references in practice, so inline everything, with an exception requiring all three of rare trigger, >1000t after compression, and an unavoidable loading gate. The doc's branch test is the project's first condition alone. The project carries three measured failures in one session (2026-04-13 Failure Log rows 3, 4, 10) and an owner ruling forced by them. The doc carries a maintainability argument. **Evidence favors the project.** See ALREADY-TESTED for the part that makes this decisive.

**A10 vs. position 1's corollary.** The doc forbids duplication; ETHOS permits cross-skill duplication as the price of self-containment. The two optimize different variables — the doc minimizes maintainer cost, the project maximizes runtime compliance. Within one skill the doc is right and nothing in the project contradicts it. Across skills, **evidence favors the project**: it measured the cost of the alternative and the doc did not.

**A2 vs. the project's de facto default.** The doc prefers user invocation to eliminate a class of unpredictability. This project publishes a marketplace whose four orchestration skills exist to fire on user verbs the user is not expected to memorize. Withholding descriptions destroys the product. The doc's preference is sound for a personal repo where the author is also the only pilot; **it does not transfer**, and the doc says so itself when it names the tradeoff as unresolved.

## Already-tested by this project

**A7 — reference splitting. Ran, failed three times in one session, reversed.** This is the document's central structural recommendation and the project's most heavily licensed position: owner ruling forced by measured failure, conformance 17 of 19, restated three times in ETHOS.md (lines 7, 9, 11). The reversal produced a stricter exception than the doc's branch test, and the project's assumed-reader list records the exact mechanism: it will not fetch a passively cited file; only an imperative, gated instruction produces the read.

The document supplies the refutation itself. On skill invocation it states that the model "may just choose not to follow it" — and calls that unpredictability serious enough to give up model invocation entirely. It then recommends intra-skill context pointers, which are the same mechanism at a smaller scale, and grants them a reliability it just denied. One paragraph earlier the doc pays a real product cost to avoid pointer unreliability; here it treats bundling as if bundling changed the odds. **The project ran this and reversed. Evidence favors the project, and the doc contradicts itself.**

Two survivors in the corpus show the shape the exception takes when it holds: dev-orchestration's cross-skill read is marked "a hard gate, not a suggestion," and qa-orchestration's carries an inline fallback. Both are imperative and gated. Neither is the doc's soft pointer.

**A2 — user-invoked-only. Ran once, removed.** session-close carried `disable-model-invocation: true`. It came off when the skill's scope grew to the full ARRIVE/WORK/LEAVE lifecycle (2026-04-15). The same flag produced Failure Log #3 that session: a rewrite agent replaced the `version` field with it, silently disabling the skill until someone tried to invoke it. Weight this honestly — n=1, and the removal was driven by scope, not by invocation philosophy. It is still the only run this project has, and it ended in removal.

## Foreign-only — the gap list

1. **A12, the deletion test.** The highest-value item in the document. The project measures size (`just tokens`, position 3) and never measures whether a retained line does work. Position 11 — instruction text states what to do and does not argue for itself — sits at 4 of 19 with 15 measured violations and zero not-applicable. That population is precisely what a deletion test finds: rationale paragraphs whose removal changes no behavior. The project holds the rule and lacks the instrument.
2. **A1, invocation mode as an explicit decision.** Nineteen of nineteen skills are model-invoked. No position, no ruling, no measurement of the resting description cost across 8 plugins. An unstated default, not a stance.
3. **A11, sediment as a named failure.** The label has no test attached, but it names something the project's own divergence table describes six times without a word for it: rules shipped onto an unrevised corpus. Positions 8, 11 and 15 sit at 1, 4 and 1 of 19.
4. **A4/A5, steps-and-reference decomposition and top-down authoring order.** The project has no authoring-order position at all. Position 15's XML lifecycle tags address structure, reached 1 of 19, and address a different axis.
5. **M6, trace verification of a steer.** The project verifies artifacts, never vocabulary uptake.

## Native-only

The document never addresses these. Grouped by what its silence costs.

**Verification — the structural hole.** Position 10 (every mandatory step pairs a named artifact with an orchestrator-side check; self-report is untrusted; license: owner ruling reinforced by measured failure across three distinct sessions). Position 9 (phase gates on a verified artifact, 18 of 19). Position 16 (`/cost` is the sole trusted cost source; measured verdict, $800 estimated against $132 actual). The document's entire model assumes a loaded skill gets followed. Its one check — the reasoning trace — is the agent describing itself, which the project logged as a distinct failure: verbal agreement with a correction while behavior stayed unchanged (2026-04-15 Failure Log #2).

**Directive force.** Position 2 (commands not suggestions, one emphatic marker per directive; 19 of 19; 0 of 6 deep-read skills hedge). Position 12 (a positive-only style directive needs a paired negative list; measured failure — "render in natural language" produced labeled YAML). The doc's steering chapter is entirely about vocabulary and says nothing about imperative versus suggestion. It has no concept of a permissive instruction read as license.

**Compression hazard.** Position 8 (a skill's 5 core points survive compression as its untouchable spine; license: measured failure — Strunk compression buried the lead, reverted). The document prescribes aggressive pruning with nothing protecting the spine. This project ran aggressive compression and produced exactly that failure.

**Remaining.** Position 4 (file artifacts, never platform API calls). Position 6 (platform facts, never agent policy). Position 7 (hook modularity and config gating). Position 11 (no rationale in instruction text). Position 14 (a name is not a source — binding requires loaded primary text; reversal after an identified confabulation vector).

Position 14 draws a boundary the doc needs and never draws. A8 works by triggering priors from a name. Position 14 forbids a name from standing in for loaded content. Both are correct and the line between them is load-bearing: "vertical slice" may steer behavior from priors; "first principles" may not substitute for the manifesto text. The doc gives no rule for when a name is a steer and when it is a confabulation vector.

## Factual corrections

**Against the document — M5.** Bundling a reference file beside SKILL.md does not raise follow-through. The doc asserts easy pull-in while asserting M4 two pages earlier. The project's measurement resolves it: only an imperative, gated instruction produces the read. Proximity on disk is not a mechanism.

**Against the document — M7, partial.** Splitting step two into a second skill hides it only if that skill is user-invoked. A model-invokable follow-on keeps its description in context at rest (M1), so the future goal stays visible. The mechanic holds fully under user invocation or under subagent context isolation — not under skill splitting alone. The doc's own example pairs two model-invokable skills.

**Against this project — `disable-model-invocation`.** The doc states M2 correctly: it is a real Claude Code frontmatter field with defined semantics, and it is the supported control for invocation mode. This project's only record calls it "a destructive flag" whose presence should trigger review (2026-04-15 Failure Log #3). That framing came from an accident — an agent clobbered an adjacent frontmatter field during an unverified edit — not from the flag's behavior. The failure was the unverified frontmatter edit. Correcting the record is a factual matter, not a taste difference.

**Neither side, unmeasured — M3.** The claim that N model-invoked skills cost N descriptions at rest is directionally correct and unquantified on both sides. This project ships 19 skills across 8 plugins and has never measured its resting description cost.

## What survives contact

1. **Position 1 survives, strengthened.** The document is the strongest available argument for reference splitting and it refutes itself. Independent restatement of the unreliability mechanism (M4) by an author who then recommends the pattern anyway raises the project's confidence rather than lowering it.
2. **Position 10 survives untouched.** The document has no verification layer. Nothing here bears on it.
3. **Position 8 survives, and the document should adopt it.** Its pruning chapter has no spine protection. This project has the measured failure showing what unprotected compression costs.
4. **A12 survives and this project lacks it.** Size measurement does not detect a line that does no work. Position 11's 15 violations are the standing candidate population.
5. **A10 does not survive across skills.** Cross-skill duplication is a measured price the project chose knowingly. Within one skill the doc's rule stands unopposed.
6. **A2 does not survive for this project.** A marketplace of verb-triggered orchestration skills cannot withhold descriptions from the model without ceasing to function. The doc's preference is scoped to a repo whose author is the only pilot, and the doc concedes the tradeoff is open.
7. **The project's "destructive flag" framing of `disable-model-invocation` should not survive.** It generalizes a botched edit into a property of the field.
8. **Position 15 gains nothing and loses nothing.** The doc proposes a different structural taxonomy (steps and reference) with the same evidentiary weight as position 15's orchestrator call — one author's preference, unmeasured, against a rule at 1 of 19. Neither side carries evidence here. Say so rather than pick.
9. **A6 and A13 should not be adopted as written.** "As small as possible" is unfalsifiable; position 3's measured token count already does the work, and the doc's own A12 supplies the only part of A6 that bites.

---

# Re-cut — conflict boundary

The sections above answer "how do the two documents compare." The two below answer a narrower question: **which foreign patterns collide with a project position, and which can be harvested without disturbing one.** The project's positions are the fixed frame here. The document is a source of patterns, not a standard.

## Conflict map

Every point where the two prescribe incompatible things. Positions are numbered per `skill-writing-stance.md`; license tags are that report's.

| Foreign pattern | Position it collides with (license) | What the project gives up to adopt it | Verdict |
|---|---|---|---|
| **A7** — move branch-specific reference behind a context pointer into a bundled file | **1**, zero external reference (owner ruling forced by **3 measured failures** in one session) | Position 1 entirely. Its three-condition exception (rare trigger, >1000t, unavoidable gate) reduces to the doc's single branch test, and the inline-everything rule at ETHOS.md:7,9,11 stops being a rule. The 17-of-19 conformance count becomes unmeasurable. | **HARD** |
| **A10** at cross-skill scope — never duplicate reference material | **1**'s corollary, cross-skill duplication is acceptable (same license, same **measured failures**) | The same thing A7 costs, by a second route: de-duplicating across skills forces one skill to point at another's content. Self-containment and de-duplication cannot both govern shared content. | **HARD** |
| **A2** — prefer user invocation; withhold the description | **5**, user action verbs are delegation directives inside four named orchestration skills (owner ruling; 4 of 19, zero drift) | The trigger mechanism for agentic-delegation, dev-orchestration, research-tree and qa-orchestration. Those skills fire on verbs in ordinary conversation via their descriptions; withheld descriptions leave the verbs dead and position 5 unenforceable. A3's "avoid the eval problem" rests on A2 and falls with it. | **HARD**, scoped to those four |
| **A12 predictive** — cut the passage, predict whether behavior would change | **3**, compression is measured, never estimated (owner ruling, revised repeatedly against measured token counts) | Position 3's defining clause. A predicted behavior delta is an estimate. Adopting the test in its stated form reintroduces estimation as a compression decision procedure. | **HARD** |
| **A12 predictive** — same | **12**, a positive-only directive needs a paired negative list (**measured failure**) | Position 12's artifact. A paired negative list is the archetypal predicted no-op — it restates in the negative what the positive line already says. The project predicted exactly that and was wrong: "render in natural language" produced labeled YAML. See below. | **HARD** |
| **A12 unexempted** — no protected content | **8**, 5 core points survive compression as the spine (**measured failure** — compression buried the lead, reverted) | Nothing, if the exemption is declared. Position 8 already names 5 untouchable items; a test plus an exemption list coexist. The collision exists only where the exemption goes unstated, and the document states none. | **SUPERFICIAL** |
| **A12 unexempted** — same | **2**, emphatic markers are deliberate, one per directive (owner ruling, refined by measured failure) | Nothing, same reason. An emphatic marker rarely changes behavior in one observation and so reads as a no-op; position 2 pre-declares markers as design, which is the exemption. | **SUPERFICIAL** |
| **A9's handoff** — one skill completes, the agent proceeds to the next | **9**, phases gate on a verified artifact (owner ruling; 18 of 19) and **10**, every mandatory step pairs an artifact with an orchestrator-side check, self-report untrusted (owner ruling, **reinforced by measured failure across 3 sessions**) | The gate. The document's handoff is a completion the agent declares — "after Grill with Docs completes, we then go" — with no artifact between. Position 10 classifies that as untrusted by construction. | **HARD** |
| **A6** — as small as possible, no stopping rule | **8** (**measured failure**) and **3** | Nothing. A direction and a floor coexist; position 3 supplies the measurement A6 lacks and position 8 supplies the floor. A6 adds neither and removes neither. The hazard is real — unbounded compression is what produced position 8's origin failure — and it is already governed. | **SUPERFICIAL** |
| **A8** — repeat the leading word consistently throughout the skill | **2**, one emphatic marker per directive (owner ruling, refined by measured failure) | Nothing. Different objects: a leading word is a noun phrase carrying domain priors; an emphatic marker is MUST/NEVER/CRITICAL. Repeating "vertical slice" across a skill is not stacking markers on one directive. | **SUPERFICIAL** |
| **A8** — steer by triggering the model's priors from a term | **14**, a name is not a source (owner ruling, reversal after an identified confabulation vector) | Nothing. Different scopes: position 14 governs what a constitution element may bind to; A8 governs behavioral steering. They meet only where a leading word names a document the model must load, and the project already rules that case. The document draws no boundary there. | **SUPERFICIAL** |
| **A4** — compose the skill from steps and reference | **15**, XML lifecycle tags, not markdown headers (orchestrator call; 1 of 19) | Nothing. Orthogonal axes — lifecycle phase versus content type. A lifecycle tag can contain steps and reference. A4 only collides if its reference unit carries A7's externalization, which is row 1. | **SUPERFICIAL** |
| **A11** — hunt sediment, kill stale material | **3** | Nothing. A11 prescribes no test for staleness, so it specifies no action to adopt and breaks no rule. | **SUPERFICIAL** |

**Positions with no foreign counterpart, therefore no collision:** 4 (file artifacts, no platform coupling), 6 (platform facts, not policy), 7 (hook modularity and config gating), 13 (no delegation escape hatch), 16 (`/cost` as sole trusted cost source). The document addresses none of these subjects. **Position 11** (instruction text does not argue for itself) is the one position the document reinforces rather than touches — A12 targets exactly the rationale prose position 11 forbids.

### The deletion test, re-examined

The prior sections called A12 a gap. Tested against the positions, it is not a clean harvest item.

The document states the test predictively. Its own worked example asks what would happen if a commit-message paragraph were deleted and answers by guess — the agent "would probably still write a decent" message. No deletion is performed. No behavior is observed.

That form collides HARD with two positions, and one of them is a measured failure. Position 3 rules compression decisions measured, never estimated; a predicted behavior delta is an estimate. Position 12 exists because this project made that exact prediction about a redundant-looking line and was wrong — the positive-only instruction was judged sufficient, the negative list was absent, and the output came back as labeled YAML. Running the document's predictive test over a position-12 negative list reverses a fix that reality already forced.

Against positions 2 and 8 the conflict is SUPERFICIAL and the reason is worth stating: both positions are already exemption declarations. Position 8 names 5 items no cut may reach. Position 2 declares emphatic markers deliberate and caps them. Each pre-supplies what the document omits.

The conflict is with the predictive form specifically. Whether another form of the test avoids the collision is the owner's call, not a recommendation in scope here.

## Harvest list

Foreign ideas that violate no project position.

**H1. A1 — record the invocation mode as an explicit decision per skill.** No position mentions `disable-model-invocation`, description cost, or invocation mode; 19 of 19 model-invoked is an unstated default that no ruling ever made. No collision because no rule occupies the ground. **OPERATIVE** — it resolves to a frontmatter field. No project mechanism achieves this under another name. Bounded by C3: the four orchestration skills in position 5 are excluded, since their triggers are their descriptions.

**H2. M3 — the resting cost of descriptions is a measurable quantity.** Sits beside position 3 (measure, never estimate) as the same discipline applied to a different object: position 3 measures file bodies, nothing measures descriptions at rest across 8 plugins. No collision because measuring a previously unmeasured thing breaks no rule about measuring. Position 16's `/cost` governs runtime spend, a different object. **OPERATIVE as a fact, unquantified in the document** — it asserts N skills cost N descriptions and supplies no number.

**H3. A5 — write the steps first, derive the reference each step needs.** No position governs authoring order. ETHOS's analysis-before-action pipeline governs optimization of existing skills, not composition of new ones; the two apply at different times and never meet. **OPERATIVE.** No project equivalent.

**H4. A4 — steps and reference as a content-type decomposition.** Orthogonal to position 15's lifecycle axis, per the conflict map. **OPERATIVE.** No project equivalent on that axis; position 15 sits at 1 of 19 on the other one.

**H5. M6 — read the reasoning trace to confirm a steer propagated.** Sits beside position 10 without colliding, because the objects differ: position 10 distrusts self-report as evidence that a mandatory step completed; M6 observes whether a term appeared. It substitutes for no artifact. **OPERATIVE**, and bounded — 2026-04-15 Failure Log #2 records verbal agreement with a correction while behavior stayed unchanged, so a trace echo is evidence of vocabulary uptake and nothing more. No project mechanism verifies vocabulary.

**H6. A10 inside a single skill — remove intra-file duplication.** Position 1 permits cross-skill duplication as the price of self-containment; repeating content three times inside one SKILL.md serves no self-containment purpose, so the permission does not reach it. **OPERATIVE.** Position 3 penalizes it indirectly through token count but names no rule against it.

**H7. A11 — "sediment" as a name for material nobody deleted.** Collides with nothing because it prescribes nothing. **INERT as stated.** It names a real problem the project's own divergence table records six times without a word for it: rules shipped onto a corpus never revised under them — position 8 at 1 of 19, position 11 at 4 of 19, position 15 at 1 of 19. What the document fails to specify: a staleness test. No criterion for stale, no record to check material against, no owner of the judgment.

### Convergence — no action follows

**A8, leading words.** manifesto-oath already states the mechanism as a platform fact, and position 5 applies it at the verb layer with zero drift across its four skills. The project reached this independently. The verification loop is the separable part and is listed as H5.

**A9's splitting mechanism.** The project achieves the same end through subagent context isolation, which hides the future goal more completely than skill splitting does — see the M7 correction. Only the handoff half is a conflict.

**A14, human checkpoint in the step sequence.** Position 9 gates phases on a verified artifact. Same end, stronger form.

**A13, size as a symptom.** Position 3 measures size and the divergence table already treats it as downstream. Nothing to add.

**A15, a shared rubric.** ETHOS.md and this stance report are it.

---

# Standalone tables

Readable without any other document. No identifiers, no cross-references.

## Conflicts

| What the document prescribes | What this project requires instead | What adopting it would cost | Evidence behind the project's rule |
|---|---|---|---|
| Move reference material used by only some branches into a separate bundled file, pointed to from the main skill. | Inline everything essential in the skill body. Split out only rare, large content behind an unavoidable read gate. | The guarantee that a skill works on a single read. Pointed-to content silently goes unread. | Measured failure, 3 occurrences in one session — passively cited files were never fetched. |
| Never repeat reference material anywhere; each piece of content gets exactly one home. | Each skill restates what it needs. Duplicating content across skills is the accepted price of standalone reading. | The same guarantee: de-duplicating forces one skill to point at another's text, which the reading model skips. | Measured failure, 3 occurrences in one session — passively cited files were never fetched. |
| Hide skill descriptions from the model so only the user can invoke skills, removing invocation unpredictability. | Four orchestration skills must fire when the user says "delegate", "research", "implement" — without being named. | Those verbs stop routing. The user must name each skill manually or the orchestration never starts. | Owner ruling. Those four skills match their intended scope exactly, with no drift in either direction. |
| Delete any passage you predict would not change the agent's behavior; judge by thinking, not by testing. | Decide compression by measurement, never by prediction. Pair every positive style instruction with an explicit negative list. | Redundant-looking safety lines get cut. A positive instruction alone reads as permission for whatever it fails to forbid. | Measured failure — "render in natural language", with no negative list, produced labeled YAML instead. |
| Split a process into two skills; when the first finishes, the agent moves on to the second. | Every mandatory step produces a named file the orchestrator checks. A step's own completion claim proves nothing. | The gate between phases. A skipped step reports done, leaves no trace, and the next phase starts anyway. | Measured failure, 3 occurrences across separate sessions — success reported while the backing file was missing. |

## Harvest

| Pattern | What it would add | Operative or inert | Why it collides with nothing |
|---|---|---|---|
| Record for each skill whether the model may invoke it, or only the user. | A deliberate choice where every skill here currently carries an unexamined model-invokable default. | Operative | No existing rule mentions invocation mode, description cost, or who may trigger a skill. |
| Every model-invokable skill costs its description in the agent's context on every request. | A number for standing overhead across all skills shipped here, which nobody has counted. | Operative | Existing measurement rules cover file bodies and money spent. Nothing measures what sits in context at rest. |
| Write the procedure steps first, then derive only the supporting material those steps actually need. | An order for composing a new skill from scratch, where no working method exists today. | Operative | The existing review method improves skills that already exist. It never says how to start one. |
| Lay out every skill as two parts: the steps to walk, and the material supporting them. | A content layout that nests inside the existing phase structure rather than competing with it. | Operative | The existing structural rule divides by lifecycle phase. Steps and supporting material cut a different axis. |
| Pick a dense term, repeat it throughout, then watch the agent echo it back while reasoning. | A visible signal that a wording choice landed. Nothing here currently checks whether phrasing took hold. | Operative | It observes vocabulary, not task completion. The rule distrusting self-report governs whether a step finished. |
| Remove repeated content inside a single skill file; keep one home for each piece. | Recovered space in every file, with no effect on whether the skill still reads standalone. | Operative | Duplication is permitted only to keep separate skills standalone. Repeating inside one file serves nothing. |
| Hunt accumulated material nobody felt entitled to delete, and remove what no longer belongs. | Nothing runnable. The document names no staleness test, no record to check against, and no owner of the call. | Inert | It prescribes no action, so there is no action to break any existing rule. |

Seven further collisions look real and dissolve on inspection; five project rules the document never mentions; one it reinforces.

---

# Deep harvest — five seams

## Seam 1 — Parts of the hard conflicts that survive alone

| What it yields | Why it survives where the parent did not | Operative or inert |
|---|---|---|
| A per-skill list of which content only some runs actually need. | Knowing which parts are branch-specific moves no content. Only the pointer replacing content fails to get read. | Operative |
| An inventory of where the same rule is stated twice, and how far the two wordings have drifted apart. | Comparing copies removes none. Only merging them into one home forces the skipped read. | Operative |
| That users cannot deliberately trigger skills built to fire on their own. No measure offered for either cost. | Naming a tradeoff changes no file; withholding the description is the part that kills verb routing. | Inert |
| Instructions that add behavior differ from instructions that suppress a default; only the second broke when predicted away. | Distinguishing the two removes nothing. Predicting instead of testing is the part that reversed a proven fix. | Operative |
| One agent working a step list can see later steps and under-invests in the current one. | Splitting for focus needs no handoff. The unchecked jump from finished to next is the part that fails. | Operative |

## Seam 2 — Mining the superficial collisions

| What it yields | Why it survives where the parent did not | Operative or inert |
|---|---|---|
| Which skills have ever had their protected content actually named. The protection is declared but rarely instantiated. | Naming what may not be cut removes nothing; the pruning judgment is what needed a guard. | Operative |
| Whether an emphatic word is doing work, or decorating a line the model already obeys. | Counting markers per line and judging a marker's effect are different questions. No way offered to tell them apart. | Inert |
| Whether a skill calls one concept by one name throughout, or drifts across three. | Consistent terminology adds no emphasis and breaks no cap on emphatic words. | Operative |
| Named methods invoked inside skills — unclear whether the name steers or stands in for unread content. | The loading rule covers constitutions only. Method names in ordinary skill text are governed by nothing. | Operative |

Three yield nothing: minimize-versus-measure restates a rule already held, the two structural layouts cross but neither is adopted, and the accumulation label was harvested whole.

## Seam 3 — Convergence re-opened: cheaper, or covers a missed edge

| What it yields | Why it survives where the parent did not | Operative or inert |
|---|---|---|
| Choosing terms that carry meaning on their own, as a general authoring move rather than two lucky instances. | Cheaper than a stated rule — one word repeated against a paragraph of instruction — and never generalized here. | Operative |
| Splitting a sequence for focus alone, without the file-and-check apparatus, where the step is not mandatory. | The heavy mechanism exists to verify mandatory steps. Where nothing is mandatory, its cost buys nothing. | Operative |
| Asking the person mid-sequence whether the direction is right. | Checking that a file exists and is well-formed cannot detect correct work aimed at the wrong target. | Operative |
| A short list of causes to check when a file is oversized: repetition, stale accumulation, lines doing nothing. | Overages here are counted and recorded, never diagnosed. Listing causes competes with no counting rule. | Operative |
| A checklist walked in order, rather than principles stated and hoped to be applied. | Several stated rules reached one file in nineteen — a coverage failure a stated principle cannot catch. | Operative |

## Seam 4 — Inert claims that still name a real problem

| What it yields | Why it survives where the parent did not | Operative or inert |
|---|---|---|
| Nothing here ever checks whether the right skill engaged, or whether one fired when it should not have. | Advice was to dodge the problem. The problem is real: no definition of correct firing, no record of misses. | Inert |

The minimize-as-far-as-possible claim names no problem this project lacks. It yields nothing.

## Seam 5 — The document's shape: order, emphasis, silence

| What it yields | Why it survives where the parent did not | Operative or inert |
|---|---|---|
| Invocation is settled before content. Here, how a skill gets triggered is never a design step. | An ordering, not a claim. It competes with no rule because no rule occupies that stage. | Operative |
| Compression comes last, over a skill already known to work. No point is fixed here for when it runs. | A sequencing question, not a prescription. The one recorded compression loss hit files never tested first. | Inert |
| Neither side says what happens when two skills both apply to the same request. | A shared blank, not a disagreement — nineteen skills across eight bundles and no precedence stated. | Operative |
| Neither side states who a skill is written for. One assumes the author and the user are the same person. | That assumption carries the entire cost argument, and breaks silently when skills ship to strangers. | Operative |
