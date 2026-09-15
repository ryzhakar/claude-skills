# Skill Governance and Harvest

## Part 1 — Governance as held now

| Rule | Why it exists | Evidence | Conformance |
|---|---|---|---|
| Inline everything a skill needs. Put content behind a read only when it is rare, large, and gated so skipping is impossible. | Stops essential content from going unread. | Measured failure, 3 occurrences in one session — passively cited files were never fetched. | 17 of 19 |
| Write commands, not suggestions. One emphatic word per directive. | Stops hedged text from reading as permission to do less. | Owner ruling, later refined after stacked emphatic words were found and reverted. | 19 of 19 |
| Measure compression; never estimate it. Replace explanatory prose with tables and decision trees. | Stops guessed savings and prose that buries the rule. | Owner ruling, revised repeatedly against counted tokens. | 15 of 19; three over the bar |
| Produce files on disk. Never call an outside service. | Stops the tool from deciding where the work gets published. | Owner ruling. | 11 of 19; one live breach, automatic merge routing |
| In the four coordination skills, treat a user's action verb as an order to delegate, never to execute. | Stops the coordinator from doing the work itself. | Owner ruling. | 4 of 19, exact, no drift |
| State what the platform does, not what the agent should choose. | Stops a hard limit from reading as a policy the agent may weigh. | Owner ruling. | 7 of 19; no breaches, rest out of scope |
| Startup injections may run long. Keep their text in separate template files and switch them off when unconfigured. | Stops invisible overhead and prompts nobody can turn off. | Owner ruling. | Not measured — no skill implements one |
| Name five points per skill that no compression may cut. | Stops compression from removing the thing the skill exists to say. | Measured failure — a compression pass buried the main point and was reverted. | 1 of 19 |
| Gate each phase on a checked result from the phase before it. | Stops a phase from starting on work nobody confirmed. | Owner ruling. | 18 of 19 |
| Pair every mandatory step with a named file and a check by the coordinator. Never trust a step's own claim. | Stops success from being reported instead of achieved. | Measured failure, 3 occurrences across separate sessions — done reported with no file behind it. | 11 of 19; eight out of scope |
| State what to do. Never argue for the instruction. | Stops rationale prose the reader must sift through. | Owner ruling. | 4 of 19; fifteen carry argument |
| Pair every positive style instruction with an explicit list of what is forbidden. | Stops a permitted-by-omission reading. | Measured failure — "render in natural language", with no forbidden list, produced labeled YAML. | Not measured |
| Delegation has no escape hatch, apart from one narrow path for writing session memory. | Stops the coordinator from absorbing work it must hand off. | Owner ruling, narrowed after the same failure recurred. | Not measured |
| Bind only to text actually loaded. A name is never a source. | Stops action on content invented from a title. | Owner ruling, reversing earlier practice once a route to fabrication was identified. | Not measured; one applicable place, no breach |
| Structure skill files in lifecycle tags rather than plain headings. | Keeps phase boundaries visible in the file itself. | Orchestrator call. | 1 of 19 |
| Take cost only from the tool's own readout. Never count or estimate it. | Stops a wrong number from driving a decision. | Measured verdict — a manual estimate said eight hundred dollars against a real cost of one hundred thirty-two. | 1 of 19 |

## Part 2 — The mental model

This project holds that a model reading a skill does the least the text permits, then reports success. It treats a positive-only instruction as permission for whatever goes unforbidden. It invents structure where the text is silent. It copies a worked example over the rule printed beside it. It agrees with a correction while its behavior stays unchanged. It never fetches a file merely cited; only a gated order produces the read.

Every skill here is built against one failure: a reported done standing while the file behind it is missing, malformed, or recalled from memory. Reporting success costs less than achieving it.

The enemy this history keeps rediscovering is permissive text. A hedge, a condition, or an unstated exclusion reads as license to do less.

## Part 3 — Conflicts

These are live choices, and a measured failure records what happened once under conditions that may not hold.

| The two positions | What each side buys | What each side costs | Evidence each side carries |
|---|---|---|---|
| Move content used by only some runs behind a pointer, or inline everything a skill needs. | Splitting buys a smaller standing body and content loaded only when relevant. Inlining buys a read that always completes. | Splitting costs content that silently goes unread. Inlining costs weight carried every run and the same text maintained twice. | Outside: none stated; both outside documents ship the pattern, one behind a passive pointer. Here: three occurrences of cited files going unfetched. |
| Let each skill restate what it needs, or give every piece of content exactly one home. | Restating buys skills that read standalone. One home buys copies that cannot drift apart. | Restating costs silent divergence between copies and edits repeated in several places. One home costs a read that may never happen. | Here: three occurrences of cited files going unfetched in one session. Outside: none stated; one document duplicates its own body, breaking this rule. |
| Hide descriptions so only a named request invokes a skill, or expose every description to the model. | Hiding buys predictable invocation and no standing description cost. Exposure buys routing from ordinary verbs, with no skill names to memorise. | Hiding costs verb routing and loads skill names onto the user. Exposure costs standing context every request, and invocation the model may skip. | Outside: unpredictability asserted, no count given. Here: owner ruling, four skills matching intended scope with no drift. |
| Pair every positive instruction with what it forbids, or cut any passage whose removal is predicted to change nothing. | Pairing buys closure against readings the positive line leaves open. Cutting buys a smaller file and fewer lines to maintain. | Pairing costs length, and a forbidden list on instructions that never needed one. Cutting costs safety lines that look redundant. | Here: one measured reversal — a positive-only instruction produced labeled YAML. Outside: a worked example answered by prediction, never run. |
| Let one step finish and the next begin, or pass between steps through a named file the coordinator checks. | Moving on buys speed and no file-writing overhead. Checking buys detection of a step that reported done and did nothing. | Moving on costs the gate — a skipped step leaves no trace. Checking costs a written file and a check at every boundary. | Outside: none stated. Here: three occurrences across separate sessions of done reported with no file behind it. |
| Explain the reasoning behind each instruction, or state the policy and leave the argument out. | Explaining buys a reader that can extrapolate past the literal rule. Omitting buys a shorter file and a single reading. | Explaining costs length, and a rationale a reader may weigh against the rule. Omitting costs every case the rule failed to anticipate. | Outside: asserted, none stated. Here: owner ruling; fifteen of nineteen files carry argument against it. |
| Treat capitalised always and never as a warning sign, or write commands carrying one emphatic word each. | Avoiding them buys prose that reads as reasoning. Using them buys a line that cannot be read as optional. | Avoiding them costs the one lever against permissive reading. Using them costs force once every line shouts. | Outside: asserted, none stated, and one document issues flat prohibitions anyway. Here: owner ruling, refined after stacked markers were reverted. |
| Carry a version number in the skill header, or hold versions only in the bundle metadata. | In the header buys a version visible while reading the skill. In metadata buys one number that cannot disagree with itself. | In the header costs a second place to update and drift between the two. In metadata costs version invisibility while reading a skill. | Outside: asserted, none stated; one document ships it and the other omits it. Here: owner ruling, no measured failure. |

## Part 4 — The harvest diff

Thirty-one items. Twenty-one held, plus ten drawn from outside guidance after cutting everything that needs an evaluation harness or rests on assertion. One outside item merged into the standing precedence row.

### Authoring a new skill

| What to adopt | What it adds | Why it collides with nothing | Operative or inert |
|---|---|---|---|
| Decide and record, before writing any content, whether the model may invoke each skill or only the user. | A deliberate choice where every skill currently carries an unexamined model-invokable default. | No rule mentions invocation mode, description cost, or who may trigger a skill. | Operative |
| Write the procedure steps first, derive only the support those steps need, and lay the skill out as those two parts. | A method for starting a skill from nothing, where none exists. | The existing review method improves skills that already exist; it never says how to begin one. | Operative |
| Pick one term that carries its own meaning for each key concept, and use that same term throughout. | Concentrated steering where terminology is currently chosen ad hoc and drifts within a file. | Consistent terminology adds no emphatic words and breaks no cap on them. | Operative |
| Put every trigger condition in the description. Keep the body free of them. | A placement rule where none exists, and the body loads only after triggering has already happened. | No rule governs where trigger conditions get written. | Operative |
| State who each skill is written for. | An audience where none is recorded, and skills ship to strangers. | No rule names an audience, and stating one changes no content. | Operative |
| Match each skill's stated purpose to its actual contents. | A check that a skill does what it claims, which nothing currently performs. | Nothing compares a description against the body beneath it. | Operative |
| Give any long body a navigation index at its head. | A route through a large file, which matters more where everything stays in one. | No rule governs navigation inside a file, and an index displaces nothing. | Operative |
| Name the five uncuttable points for every skill that has never had them named. | Instances for a protection declared as a rule and almost never applied. | Naming what may not be cut removes nothing. | Operative |

### Measuring a skill

| What to adopt | What it adds | Why it collides with nothing | Operative or inert |
|---|---|---|---|
| Count what every skill description costs in the agent's context at rest, across all bundles. | A number for standing overhead that nobody has ever counted. | Existing measurement covers file bodies and money spent, never what sits in context at rest. | Operative |
| Capture the token count and elapsed time reported when a delegated run finishes. | Per-run cost at a granularity nothing collects, available only at the instant of completion. | Existing cost measurement reads a session total; per-run figures sit outside it. | Operative |
| Read the transcripts of delegated runs, not only the files they produce. | Direct evidence of work an instruction caused and wasted. | Nothing inspects transcripts; existing checks read produced files only. | Operative |
| List, per skill, which content only some runs actually need. | Where the weight sits on a typical run rather than a rare one. | Knowing which content is situational moves none of it. | Operative |
| Inventory where the same rule is stated in two skills, and how far the two wordings have drifted apart. | Detection of copies that silently disagree. | Copies are permitted as the price of standalone reading; nothing requires them to still match. | Operative |
| Remove repeated content inside a single file. | Recovered space with no effect on whether the skill still reads standalone. | Duplication is permitted only to keep separate skills standalone. Repeating inside one file serves nothing. | Operative |
| When a file runs oversized, check three causes: repetition, stale accumulation, lines that change nothing. | A diagnosis where overages are counted and recorded but never explained. | Listing causes competes with no counting rule. | Operative |
| Staleness judged apart from size. | Names a real gap: size is the only health measure held. No staleness test, no record to check against, no owner of the call. | It prescribes no action, so there is no action to break a rule. | Inert |

### Structuring a skill

| What to adopt | What it adds | Why it collides with nothing | Operative or inert |
|---|---|---|---|
| Split a sequence for focus alone, with no files or checks, where the step is not mandatory. | A light remedy for a real defect: an agent seeing later steps under-invests in the one it is on. | The heavy mechanism exists to verify mandatory steps. Where nothing is mandatory, its cost buys nothing. | Operative |
| Separate instructions that add behavior from instructions that suppress a default. | The distinction between a safely removable line and one whose removal already broke output. | Classifying instructions removes none of them. | Operative |
| Name the competing skill and forbid it, wherever two skills would both fire on one request. | Precedence across nineteen skills in eight bundles, and the wording that enforces it. | No rule occupies the question, and naming a competitor displaces no content. | Operative |
| State what to do when a capability the skill depends on is absent. | A fallback rule. One skill carries such a fallback; nothing requires the rest to. | No rule governs missing capabilities, and a fallback removes nothing. | Operative |
| Ship the helper code that separate runs keep rewriting. | Bundled code earned by observed repetition rather than guessed at. | Executable files on disk are permitted output; no rule forbids bundling them. | Operative |
| For each method invoked by name inside a skill, decide whether the name steers or stands in for content that must be loaded. | A ruling on the middle ground between a term that resonates and a title hiding unread text. | The loading rule covers binding documents only. Method names in ordinary skill text are ungoverned. | Operative |

### Verifying behavior

| What to adopt | What it adds | Why it collides with nothing | Operative or inert |
|---|---|---|---|
| Ask the person mid-sequence whether the direction is right. | Detection of correct work aimed at the wrong target, which a file-exists check cannot catch. | Existing gates verify that a file exists and is well-formed. Intent is a different question. | Operative |
| Write the person's review of produced work to a file. | A durable record where review currently stays in conversation and vanishes with it. | Existing verification records produced artifacts; a review file adds one more. | Operative |
| Name the exact field names required wherever a downstream consumer reads the output. | A contract at the point of production, which a file-exists check cannot supply. | Existing checks confirm a file exists and is well-formed, never which fields it carries. | Operative |
| Confirm that every path a skill names resolves. | Link integrity across a small surface, since almost nothing is pointed at. | Two gated pointers exist; checking them contradicts no rule. | Operative |
| Watch the agent echo a chosen term back while reasoning. | Evidence that a wording choice landed, where nothing checks whether phrasing took hold. | It observes vocabulary, not completion. The rule distrusting self-report governs whether a step finished. | Operative |
| Whether an emphatic word is doing work or decorating a line. | Names a real gap: emphatic words are capped per line and never judged for effect. No way offered to tell them apart. | Counting them and judging them are different questions; neither answer changes the cap. | Inert |
| Whether the right skill engaged, and whether one fired that should not have. | Names a real gap: nineteen skills fire on model judgment and no firing is ever checked. No definition of a correct firing, no record of misses. | Nothing claims to check triggering, so nothing is contradicted. | Inert |

### Reviewing

| What to adopt | What it adds | Why it collides with nothing | Operative or inert |
|---|---|---|---|
| Walk an ordered checklist rather than relying on stated principles to be applied. | Coverage. Several stated rules reached one file in nineteen, which is a coverage failure a principle cannot catch. | A walking order competes with no rule about what the rules are. | Operative |
| When compression runs, relative to a skill being known to work. | Names a real gap: no point is fixed for it, and the one recorded compression loss hit files never tested first. No criterion given for working. | A sequencing question, not a prescription; it displaces nothing. | Inert |

## Part 5 — Considered and excluded

| What | Why it is not here |
|---|---|
| An evaluation harness: paired runs with and without a skill, graded assertions, aggregated results. | Out of scope by owner decision, not rejected on merit. It would have measured whether a skill helps at all. |
| Trigger-rate query sets, repeated runs, held-out train and test splits. | Out of scope with the harness. They would have measured whether a description fires when it should. |
| Blind judging of two outputs by an agent told nothing about their origin. | Out of scope with the harness. It would have produced a verdict free of authorship. |
| Flagging checks that pass with and without a skill, and results that swing between runs. | Out of scope with the harness. They would have separated a real result from noise and from nothing. |
| Keeping a snapshot of the previous version as the comparison baseline. | Out of scope with the harness. It would have measured a revision against the thing it replaced. |
| Authoring realistic test prompts, and classifying outputs as checkable or needing judgment. | Out of scope with the harness; both exist only to feed it. |
| Packaging a finished skill into a distributable archive. | Skills travel inside their bundle. One source document states the same. |
| Simple one-step requests consult no skill however well the description matches. | A platform behaviour with no action attached once trigger testing sits out of scope. |
| Write verb-first instructions rather than addressing a reader directly. | Already held: write commands, not suggestions. |
| Keep the body under a stated length bar. | Already held: measure compression and never estimate it, against a bar three files exceed. |
| Walk a checklist before calling a skill finished. | Already held: walk an ordered checklist rather than trusting stated principles to be applied. |
| Put concrete trigger phrases in the description. | Already held: descriptions here carry the phrases that should fire them. |
| Remove anything not pulling its weight. | Already held: a cause list for oversized files, and the split between instructions that add and instructions that suppress. |
| Study other skills as examples of good practice. | Names no problem here, and a worked example gets copied over the rule printed beside it. |
| Iterate after real use: notice struggles, make changes, test again. | Names no trigger, no threshold, and no record of what was noticed. |
| Skills must contain no malware and nothing misleading. | Changes nothing an author does while writing. The claim-matches-contents half entered the harvest. |
| Skills are onboarding guides turning a general agent into a specialist. | Framing with no instruction attached. |
| Stay flexible where the user prefers to work informally. | Gives no criterion for when to skip and no floor beneath the skipping. |
| Write the frontmatter description in third person. | Assertion with no evidence, and the two source documents contradict each other on it. |
| Write descriptions that push, to counter under-triggering. | Assertion with no evidence, and the two source documents contradict each other on it. |

## Part 6 — Source reliability

Neither source carries measured backing, so where they split there is nothing to defer to.

| Point | What the general skill says | What the plugin skill says |
|---|---|---|
| Body length | Under 500 lines is ideal, and going longer when needed is fine. | Target 1,500 to 2,000 words, 5,000 maximum; over 3,000 without split-out files is a named mistake. |
| Writing voice | Written throughout in a chatty second person, addressing the reader directly. | Forbids second person anywhere and mandates verb-first instructions. |
| Emphatic wording | Calls capitalised always and never a warning sign, and prefers explaining why. | Issues a flat list of things to do and never do, without hedging. |
| Testing | Spawn paired runs with and without the skill, grade assertions, aggregate, review, repeat. | Install the bundle locally, ask a question that should trigger it, and ask a reviewing agent to look. |
| Packaging | Package the finished skill into a distributable archive for the user to install. | No packaging; skills travel inside the bundle. |
| Starting a skill | Initialise the directory with a script. | Create the directories by hand, explicitly departing from the script. |
| Description form | Make it pushy to counter under-triggering; its own is not in third person. | Third person is mandatory, and anything else is a named mistake. |
| Navigating a long bundled file | Add a table of contents past roughly 300 lines. | Add search terms past roughly 10,000 words. |
