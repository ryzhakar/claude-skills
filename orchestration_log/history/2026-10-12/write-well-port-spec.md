# write-well port spec

Target: skill `agent-conduct:write-well`, invoked `/write-well`. No skill text here.
Sources read whole: v3 (`strunk_spr_v3_complete.xml`, 27,097 tokens), v4 (`strunk_spr_v4_compressed.xml`, 3,458 tokens; 2,468 without comments), sparse-priming-representations.md, CATO_instruction_writer.md, claude-think.md, memento `skill-creation` 0.6.2, stop-yapping, ETHOS.md, both CLAUDE.md files, siblings (`git-etiquette` 1,489 tokens, `work-silently` 1,494, `check-back` 1,204; measured with `just tokens`).
Line numbers: v3/v4 = lines of the original XML files. Inference is marked `(inf)`.
Tokens of v4 parts (measured, comments stripped): rules R1-R18 965; usage 448; severity 191; genre 169; mandate 130; judgment 129; activation 128; conflicts 85; exemplars 181. Rules + usage alone = 1,413, leaving 76 tokens of the 1,489 cap for frontmatter and everything else. v4 as written needs a cut of 40-57%.

## Recommendation
Design B: one procedure, "run the severity-ranked pass over each prose block before it is sent", whose input is the draft in hand (own output this turn, or the file the call names).
Body is a v3-derived imperative checklist of about 1,300-1,500 tokens (inf; unmeasured): R1-R18 as one command each, with the v3 exceptions that change meaning (I4, I5), v4's cut list for usage, no reference file.
Seven repo and Strunk clashes (I9-I15) need an owner ruling first; I9 and I16 block most.

## Rule map v3 to v4

Structure map (answers Q1: unit of porting = one procedure, a ranked pass; not all rules, not a bare tier):

| v3 section | v4 | Skill `<section>` (imperative tag, inf) |
|---|---|---|
| 1 execution_mandate (primary, authority, self_monitoring, override) | mandate | `<run-the-pass-before-sending>`; self_monitoring step 4 dropped (I13) |
| 2 philosophical_foundation (objective, excellence, judgment_over_algorithm, hierarchy) | hierarchy only | `<settle-conflicts-by-rank>`: hierarchy, one line |
| 3 severity_taxonomy L5-L1 + triage | severity_levels + triage | `<fix-by-severity>`; the triage line is the pass order |
| 4 judgment_protocol (4 conditions, 4 heuristics, humility, mastery) | judgment (4 tests), gray_areas | `<break-a-rule-only-by-named-condition>` (I1) |
| 5-7 punctuation / composition / usage | punctuation / composition / usage | `<apply-the-rules>` as one-line commands |
| 8 genre_protocols | genre | `<match-the-register>` (I8, I15) |
| 9 edge_case_resolution | conflicts, default | merged into `<settle-conflicts-by-rank>` |
| 10 exemplar_showcase | exemplars (3 of 5) | dropped: no instruction (I12) |
| closing_directive | activation | dropped; persistence is I16 |

Rule table (verdict col = in-skill, inf):

| v3 rule (severity) | v4 id (sev) | Status | v3 content v4 loses | Verdict |
|---|---|---|---|---|
| R1 possessive (severe) | R1 L4 | kept | pronoun possessives take no apostrophe (line 373) | keep, add its/hers clause |
| R2 series comma (moderate) | R2 L3 | kept, adds "[L1 in journalism]" | firm-name exception, default INCLUDE (line 414) | keep one line |
| R3 parenthetic (severe) | R3 L4 | kept | always-parenthetic list (date year, etc.); "If UNCERTAIN, include commas" (2600) | keep, add default |
| R4 comma before conjunction (severe) | R4 L4 | CHANGED (I4) | `"but" REQUIRES comma`; dependent-clause exception; subordination alternatives | keep v3 form |
| R5 no comma splice (critical) | R5 L5 | kept, loses adverb rule | semicolon still required before adverbial transition (therefore, thus...), line 611 | keep with adverb rule |
| R6 fragments (severe) | R6 L4 | kept | dialogue exception | keep (I10) |
| R7 participial (critical) | R7 L5 | kept | extends to appositives and adjectives at sentence opening | keep with extension |
| R8 paragraph (moderate) | R8 L3 | kept | outline frameworks | keep, one line |
| R9 topic sentence (moderate) | R9 L3 | kept | development methods, transition, narrative variant | one line (I15) |
| R10 active (severe) | R10 L4 | kept; double passive raised to NEVER | "obvious from context" passive case | keep |
| R11 positive form (moderate) | R11 L3 | kept (I5) | strong-negative carve-outs; "Don't force positive where negative is semantically needed" | keep v3 form |
| R12 concrete (severe) | R12 L4 | kept | "THE MOST IMPORTANT principle" (1192); exposition and degree-of-specification | keep, top of core |
| R13 needless words (moderate) | R13 L3 | kept | sentence_combining; most violation pairs | keep (I10) |
| R14 loose succession (minor) | R14 L2 | kept | balanced_use | optional; cut first |
| R15 parallel (moderate) | R15 L3 | kept | large_numbers (table instead of prose) | keep |
| R16 related words (moderate) | R16 L3 | kept compressed | "only"/"not all" and antecedent-group cases | keep |
| R17 summary tense (moderate) | R17 L3 | CHANGED (I7) | indirect discourse; avoid_summary_mode | keep v3 intercalate; summary-mode line |
| R18 emphatic end (moderate) | R18 L3 | kept | periodic sentence; subject emphasis | keep |

Usage entries (26 in v3, 12 in v4; v4 U-ids in brackets):

| v3 entry (severity) | v4 | Note |
|---|---|---|
| like_vs_as (severe) | U1 L4 | kept |
| data (moderate) | U2 L3 | changed (I4) |
| less_vs_fewer (moderate) | U3 L3 | kept |
| different_than (moderate) | U4 L3 | kept |
| due_to (moderate) | U5 L3 | kept |
| while (moderate) | U6 L3 | kept |
| however_placement (moderate) | U7 L2 | demoted |
| fact (moderate) | U8 L2 | demoted; "the fact that" also in R13 L3 |
| claim_verb (moderate) | U9 L2 | demoted |
| literally (moderate) | U10 L2 | demoted |
| split_infinitive (minor) | U11 L1 | demoted; taxonomy lists it at L2 (I3) |
| they_with_singular_antecedent (moderate) | U12 L1 | changed (I4, I14) |
| can_vs_may, most_vs_almost, shall_will (moderate); one_of_the_most incl. agreement_error (severe); case, compare_to_vs_with, etc, factor, feature, interesting, nature, possess, respective, worth_while (minor) | dropped | 14 dropped (I6) |

Decision (Q2): no v3 content needs the long text. The long-only material is rationale, worked examples, outlines and exemplars; the rule-deciding parts are single lines (listed in the "loses" column) and fit the cap. v3 as a reference fails ETHOS on all three: trigger not rare (every call), 27,097 tokens (size condition holds), no unavoidable loading gate (ETHOS: "Models ignore @references in practice"). A reference of only the dropped usage tail is under 1,000 tokens (inf), so it fails the size test.

## Incompatibilities
Format: clash; side A; side B; why; options; default. Groups: I1-I8 v3 vs v4; I9-I15 Strunk vs repo; I16-I18 design.

**I1. Override latitude (v3 vs v4).**
A (v3 line 275, purpose_test): `If uncertain → follow rule (default to convention)`; precedent_test (287): `If rarely`→ follow rule.
B (v4 line 49, purpose): `Does breaking this rule serve communicative purpose? If yes → deviate`; (51, precedent): `If widely → permissible`; override (19-23) adds `Purpose clearly demands it`.
Why: v4 lets any rule be broken on the writer's own judgment of purpose; a blind reader cannot test it. ETHOS: "name the boundary — a line ceiling, a path, a count — and make it checkable."
Options: (a) v3 defaults (uncertain → follow); (b) only the three named conditions (user asks, genre or house style, two rules conflict); (c) v4 as written.
Default: (b) plus v3's uncertain → follow rule. Drop purpose, precedent and consciousness tests.

**I2. Force of MUST/NEVER (v3 vs v4 vs ETHOS).**
A (v3 lines 102-103): `When this instruction set says "MUST" or "NEVER," understand this as: "Default strongly to this pattern UNLESS you have specific justification for deviation."`
B (v4 R3): `NEVER one comma only—critical error.`; U1: `NEVER "like I did"`; R10: `NEVER: double passive`. v4 has no softening sentence yet allows override (I1). ETHOS: "Models need a strong hand... Emphatic markers (MUST, NEVER, CRITICAL) are intentional design".
Why: v3's sentence turns every command in the skill into a suggestion; the repo measured failure for permissive wording (skill-writing-stance position 12, 2026-09-15 review).
Options: (a) hard commands for L5-L4, override only via I1(b); (b) v3 soft reading; (c) silent like v4.
Default: (a). Cut the v3 sentence.

**I3. Severity ranks disagree, and demote ETHOS's six (v3 vs v4, each internally).**
A: ETHOS line 21 names `active voice, positive form, concrete language, omit needless words, parallel construction, emphatic position` = R10, R11, R12, R13, R15, R18. v4 ranks them L4, L3, L4, L3, L3, L3; v4 triage: `Fix L5-L4 during generation. L3 if easy. L2-L1 only if already attending to polish.` So four of six become optional.
B: inconsistencies inside the sources: v3 L1 list (line 208) `Oxford comma` but R2 moderate (381), v4 R2 `L3`; v3 L4 list (161) `Negative constructions where positive clearer` but R11 moderate, v4 R11 `L3`; v4 L2 `(split infinitives, terminal prepositions, redundancy)` but U11 `sev="L1"`; v3 moderate entries `however`, `fact`, `claim`, `literally` become v4 `L2`.
Why: the pass order is the severity order; a wrong rank skips a rule ETHOS requires.
Options: (a) add a top tier "core six" always applied; (b) v4 ranks; (c) v3 ranks.
Default: (a): tiers = mechanics L5-L4 and the core six always; rest only while polishing.

**I4. Meaning-changing compressions of mechanics (v3 vs v4).**
- R4 exception. v3 (558-559): `"but" REQUIRES comma: "I have heard his arguments, but am still unconvinced."` / `"and" OPTIONAL if relation is close`. v4 R4: `Exception: same subject expressed once + tight connection → optional` (covers `but` too).
- R5. v3 (611): `If second clause begins with adverb (accordingly, besides, then, therefore, thus), semicolon is STILL required.` v4 R5: `NO COMMA SPLICE. Use semicolon/period/conjunction+comma.` (adverb case gone; this is the most common splice in agent prose, inf).
- data. v3 (1928): `In technical writing and formal prose, maintain plural.` v4 U2: `data: plural (data are, datum is). [L1 in computing/informal]`. Agent text is technical; v3 says plural, v4 says ignore.
- R3. v3 (2600): `If UNCERTAIN, include commas`; always-parenthetic list. v4: both absent.
Why: v4's "~95% semantic preservation" (header, line 4) does not hold for these four.
Options: keep v3 wording for each; or accept v4; or drop `data`.
Default: v3 wording for R4, R5, R3; `data` follows v3 (plural) unless owner says otherwise (see Question 6).

**I5. Positive form carve-outs (v3 vs v4).**
A (v3 1178, 1161): `Don't force positive where negative is semantically needed.`; `Negative words other than "not" are usually strong:`.
B (v4 R11): `PUT STATEMENTS IN POSITIVE FORM. Avoid evasive negatives... Use "not" only for denial/antithesis, never evasion.`
Why: without the carve-outs, "never"-form prohibitions and exact denials ("not supported") read as violations (see I11).
Default: keep v3's two sentences, compressed.

**I6. Usage list selection (v3 vs v4).**
A: v4 comment (line 119): `USAGE: Common errors (severity-ranked selection)`. v3 severities: can_vs_may, most_vs_almost, shall_will `moderate`; one_of_the_most `agreement_error severity="severe"` (line 2197: `Wrong: "One of the ablest men that HAS attacked this problem"`).
B: v4 drops those and keeps U11 `L1`, U12 `L1`.
Why: the stated selection rule fails by v3's own ranks. In the skill, usage can occupy the cap that the rules need.
Options: (a) keep only L5-L4 usage (U1) + `data`, `due to`, `while`, `fact`; (b) v4's 12; (c) v4's 12 + `one of the` agreement.
Default: (a) plus the `one of the ... that have` agreement line; others dropped for tokens.

**I7. Summary writing (v3 vs v4).**
A (v3 1694, 1702): `avoid intercalating expressions like:` he said / he stated; `Indicate clearly at outset, once for all, that what follows is summary. Then waste no words in repeating the notification.` avoid_summary_mode (1706-1718): `in analytical writing, summary is failure to analyze.`
B (v4 R17): `Don't intercalate "he said/stated" constantly.`
Why: agent reports repeat "the reviewer found... the agent then said..." (inf); v4 turns an absolute into a frequency.
Default: v3 intercalate line; one line from avoid_summary_mode for reports.

**I8. Genre divergence (v3 vs v4).**
A (v3 2534): `This instruction matrix does not apply to poetry composition.`; technical (2468-2469): `Active voice for user actions ("You must restart")` / `Passive voice for system actions ("The file is saved automatically")`; business (2509): `Passive voice to soften criticism`.
B (v4 genre): `technical>Passive common ("system is configured"). Imperative dominant.`; no poetry entry.
Why: neither list has the registers an agent writes (status line, commit subject, final report, code comment, instruction file). Either list is a guess for them.
Options: (a) drop genre; replace by one rule: house style of the project overrides Strunk (both versions already say so for journalism: v3 `house_style_dominance`, v4 `House style (AP/Chicago) overrides Strunk if conflict`); (b) v4 genre; (c) v3 genre.
Default: (a). It is also the settlement lever for I10, I12, I15.

**I9. Clarity over economy vs compress beyond comprehension (Strunk vs CLAUDE.md).**
A (v3 2568-2569, v4 157): `CHOOSE CLARITY. Terse prose that confuses is worse than verbose prose that communicates. Add words if needed for comprehension.` / `Economy vs Clarity → CLARITY`; hierarchy (v4 26): `Clarity > Accuracy > Economy > Vigor > Correctness`.
B (claude-skills/CLAUDE.md, "Compressed communication"): `I literally demand compression of user-facing communication BEYOND comprehension.`; `Any communication gap is on me`. stop-yapping, "Before You Send": `Stop when removing one more word would destroy meaning.` (stops at meaning; CLAUDE.md does not).
Why: the skill's top-ranked value contradicts the project's top demand. A skill that says "add words for clarity" loses to CLAUDE.md in this repo (inf) or makes the user's output longer than they ordered.
Options: (a) skill ranks Economy above Clarity (repo order; contradicts both Strunk versions in their strongest line); (b) keep Clarity first, scope the skill to prose the reader must understand cold (reports, docs, messages to people outside the session); (c) keep Clarity first everywhere, CLAUDE.md compression demand is out of scope for this skill.
Default: (b).

**I10. Fragments, articles, sentence length (Strunk vs stop-yapping).**
A (v4 R6): `No sentence fragments. Exception: emphatic expression when emphasis warranted and meaning clear`; (R15): `Articles/prepositions: use before first only OR before each.`; (R13): `NOT "make all sentences short" but "make every word purposeful"`; v3 sentence_combining (1353-1375) merges series of short sentences into one.
B (stop-yapping): `Articles. "A", "an", "the". Gone.`; `Fragments. "Bug in auth middleware." Done. Your instinct to make these into pretty sentences? That's the disease.`; `Sentence over 15 words? You're yapping again. BREAK IT.`
Related: CATO prototype `Current transmission mechanisms inefficient. Latency high` drops verbs while its own constraints demand `Rigid adherence to vigorous grammatical standards`.
Why: the two standards cannot both govern one sentence. An agent bound to both will oscillate.
Options: (a) Strunk governs sentences kept; telegraphic registers (commit subject, status line) fall under project house style (I8-a); (b) stop-yapping wins: R6, R15, article rules switched off; (c) Strunk wins everywhere.
Default: (a), plus delete sentence_combining (conflicts with one instruction per sentence, I12).

**I11. Positive form vs required "never" pairs (Strunk vs skill-creation, ETHOS).**
A (v4 R11): `PUT STATEMENTS IN POSITIVE FORM.`
B (skill-creation): `Pair every positive instruction with the prohibition of that same instruction; never pair it with the prohibition of another concern.` ETHOS: `"NEVER Y" not "Try to avoid Y."`
Why: a skill that obeys skill-creation breaks R11 on its face; a blind judge reading R11 literally fails the sibling skills.
Resolution already in v3: prohibition is denial (`Use "not" as means of denial`) and `Negative words other than "not" are usually strong`. Compatible only if I5 default holds.
Default: keep as is; note in skill that prohibitions are denial.

**I12. Rationale, examples, and non-instruction sentences (Strunk vs skill-creation, ETHOS).**
A (v3): every rule carries `<rationale>`, `<transformation>` pairs, gray_area, exemplars (Browning, Stevenson, Lincoln, Churchill, Hemingway).
B (skill-creation): `Keep every sentence that instructs or forbids; never keep another.`; `State the instruction; never argue for it.`; `Inside a tag write prose and inline backticks; never write anything else.`; `Carry a tag's whole meaning in its content; never give a tag an attribute.` ETHOS: `Instruction text states what to do. It does not argue for itself.` Also: `Define every term outside ordinary English... in the sentence that first uses it`: R3, R7, R14, R18 use nonrestrictive, participial, loose, periodic.
Counter-evidence: sibling `work-silently` carries `<never_do_this reason="text in silence">` blocks with attributes and tool-call XML (observation: sibling practice departs from skill-creation).
Why: error-to-fix pairs are the fidelity carrier for rules like R7; without them, rules degrade to labels. Definitions cost tokens.
Options: (a) fold each example into an instruction sentence (`Write "It rained every day for a week", never "A period of unfavorable weather set in"`); (b) use the sibling `never_do_this`/`do_exactly_this` blocks (breaks skill-creation, matches siblings); (c) no examples.
Default: (a) for the six core rules only; (c) elsewhere.

**I13. Hedging and flagging uncertainty (Strunk vs stop-yapping).**
A (v3 300, 311-312): `ACKNOWLEDGE UNCERTAINTY in gray areas.` / `It's better to say "This is controversial but I'm choosing X because..."`; self_monitoring (48): `Flag internal uncertainty when rules conflict or gray areas arise`; v4 gray_areas: `acknowledge uncertainty exists`.
B (stop-yapping): `"I think", "perhaps", "it seems" — COWARDICE`; `Hedging... Say it or don't open your mouth.`
Why: acknowledging uncertainty in output prose is a hedge by stop-yapping's table.
Default: drop acknowledge/flag; keep "choose a defensible position, apply it consistently".

**I14. Pronoun rule (Strunk vs harness).**
A (v3 2298, 2317): `Use "he" unless antecedent is or must be feminine.`; `Conservative approach: Follow traditional rule or restructure to avoid issue.` v4 U12: `traditional = use "he" or "he or she"... Choose based on audience; be consistent`.
B (harness rule, in the agent system prompt): when pronouns are not stated, use they/them; never infer from a name.
Why: v3's default contradicts the harness rule for every unknown person.
Default: omit the rule; write nothing on `they` (harness governs). Cost: v3/v4 U12 content dropped.

**I15. Paragraph prose vs tables and trees (Strunk vs ETHOS).**
A (v3 842, 784): `As a rule, do NOT write or print single sentences as paragraphs.`; R9 `begin each paragraph with a topic sentence`.
B (ETHOS): `Tables replace prose for mappings. Decision trees replace explanatory paragraphs.` Siblings are strings of one-sentence paragraphs. v3 R15 large_numbers already says "consider table format rather than prose".
Also: skill-creation governs instruction files and is more specific than Strunk there.
Options: (a) the skill excludes instruction files and tabular output (house style wins, I8-a); (b) apply to all.
Default: (a).

**I16. Target and persistence (design).**
A (v3 closing, ~2916; v4 mandate): `These instructions remain active throughout conversation unless user overrides them.`; `APPLY THESE RULES TO ALL PROSE YOU GENERATE starting now.` Standing mode.
B: skill-creation `Cover one procedure per skill; never cover a second.` Siblings keep standing modes alive with a marker file plus hook (`work-silently`: `.claude/work-silently`, `hooks/session-start.sh`); text that was in context is condensed away at compaction (check-back text: "Compaction ... shrinks the conversation to a summary").
Why: three readings: (i) standing mode; (ii) this-turn pass; (iii) pass over a named file. (i) needs a marker plus hook (adds scope, ETHOS: hooks gated on config); (iii) is review, which `manifesto:maximalist-reviewer` already does for a diff; (ii)+(iii) share one procedure if the input is "the draft in hand".
Default: (ii) with (iii) as the same pass on the named draft; no standing mode, no marker.

**I17. Two Strunk bindings (design).**
A: CLAUDE.md "Agent dispatch": agents bind to v3 by curl each dispatch; `.manifestos.yaml` (strunk-spr-v3 for instruction-writer); `instruction-writer.md:37` reads a local v3.
B: v4 is referenced nowhere in the marketplace except 2026-10-05 session and events logs, where one orchestrator bound `Strunk SPR v4` for the conduct-skill task (precedent for v4 on conduct skills). The skill will be a third source, v3-derived, 1,300-1,500 tokens.
Why: three Strunk texts in force; subagents do not inherit skills, so dispatch binding continues in parallel (inf: agent `skills` frontmatter could preload it; not verified).
Options: (a) skill is the in-session tool only, dispatch preamble unchanged; (b) dispatch preamble switches to the skill; (c) retire v3 curl.
Default: (a). Owner decides whether v3 or v4 is the standard (Question 9).

**I18. Emphasis style (design, low).**
A (v4): ALL-CAPS phrases in R5, R10-R13, R15, R16, R18 (e.g. `NO COMMA SPLICE.`, `PUT STATEMENTS IN POSITIVE FORM.`).
B (skill-creation): `Cap each sentence at one emphatic word — never, always, only, must`; ETHOS: dial back stacking.
Default: convert to commands with one `never` or `must` per sentence.

## Candidate designs
Scores 1 (bad) to 5 (good). Size = fit to the 1,489 cap.

| Design | Size | Fidelity | Self-contained | Overapplication risk (5 = low) | Blind-read test (5 = easy) | Notes |
|---|---|---|---|---|---|---|
| A. v4 verbatim as body | 1 (3,458; 2,468 stripped) | 3 (v4 loses I4-I7) | 5 | 2 (I1 permissive; standing mandate) | 2 (judgment tests) | Breaks skill-creation form (attributes, non-prose); I9-I15 unresolved |
| B. v3-derived ranked checklist, one pass | 4 (1,300-1,500 inf) | 4 (R1-R18 + exceptions that change meaning) | 5 | 4 (named override conditions) | 5 (seed text with defects at known ids; check fixes) | Recommended; needs token measure after drafting; may force R14, R8, R9 to one line |
| C. Two-tier: B body + v3 as gated reference | 1 (27,097 loaded) | 5 | 2 | 4 | 5 | Fails all three ETHOS reference conditions |
| D. Core tier only: L5 mechanics + ETHOS six | 5 (about 700 inf) | 2 | 5 | 5 | 5 | Cheapest; loses R2, R8, R9, R14, R16, R17 and all usage |
| E. Review mode: named file in, findings out | 4 | 3 | 5 | 5 | 4 | Duplicates `manifesto:maximalist-reviewer`; two procedures if kept beside the writing pass (I16) |

Reference test (Q2): C fails trigger-rarity, loading gate, and ETHOS "Models ignore @references in practice".

## Name and trigger check
- `write-well`: two lowercase hyphen parts naming what it does (skill-creation). Directory must equal name.
- Collision: none. No `write-well` in any marketplace plugin (`agent-conduct`, `dev-cycle`, `dev-cycle-lite`, `dev-discipline`, `manifesto`, `orchestration`, `product-craft`, `python-tools`, `qa-automation`, `userland-utilities`), no plugin cache entry (`my-claude-skills/*`, `memento`, `peers`, `plugin-dev`, `example-skills`, `frontend-design`, `atlassian`), no `commands/` directory in the marketplace, no agent of that name (agents: instruction-writer, maximalist-reviewer, prompt-eval, prompt-optimize, dev-cycle set). Grep of the marketplace and `~/.claudes` for `write-well` found nothing.
- Near misses by trigger phrase: `memento:record-writing` ("write this down", "record this"); `instruction-eval:write-tasks`; `memento:skill-creation` ("write a skill"); `manifesto:manifesto-writing` ("manifestos or manifesto tone"); agent `manifesto:maximalist-reviewer` ("Hold this diff to Strunk, no mercy"). The description must avoid "write" phrases they own.
- Plugin facts: `agent-conduct` is 1.9.0 on origin/main (check-back, git-etiquette, work-silently); a new skill is a minor bump (1.10.0). The READMEs regenerate via `just readme` (`check-readmes` pre-commit). The plugin's stated purpose ("how an agent conducts itself while working") fits.
- Not renamed. Reported only.

## Questions the owner must answer
Each question is self-contained. "The skill" means the new `/write-well` skill. "The pass" means the skill's one procedure: the agent re-reads each piece of prose it is about to send and fixes rule violations, most serious first.

**1. What does calling `/write-well` change, and for how long?**
Options: (a) Standing mode: every prose block the agent writes for the rest of the session follows the rules. Consequence: the skill text is condensed away when the conversation is compacted (the harness shortens old context), so persistence needs a marker file and a startup hook like `work-silently`; this adds scope and files. (b) One turn: the agent applies the pass to prose it writes in the turn where it is called, and, if the call names a file or draft, to that text. Consequence: no marker, no hook; the user must call it again next turn. (c) File review only: the agent edits or reports on a named file, writing nothing of its own differently. Consequence: duplicates the existing `maximalist-reviewer` agent. Recommended: (b).

**2. When the rules say "be clear" and the project says "compress beyond comprehension", which wins?**
Strunk's both versions rank Clarity above Economy ("Terse prose that confuses is worse than verbose prose that communicates"). The project file CLAUDE.md demands that user-facing text be compressed "BEYOND comprehension". Options: (a) Economy outranks Clarity inside the skill. Consequence: the skill contradicts the strongest line of its source; blind readers who know Strunk will flag it. (b) Clarity first, and the skill applies only to prose a reader must understand without the session's context (reports, docs, messages to other people); chat replies stay under the compression demand. Consequence: two regimes; the agent must classify each text. (c) Clarity first everywhere. Consequence: replies grow longer than CLAUDE.md orders. Recommended: (b).

**3. May the skill allow telegraphic text (no articles, sentence fragments)?**
Strunk's rules say "No sentence fragments" and require articles to be repeated or dropped consistently across a series. The stop-yapping manifesto the project binds to says to delete articles, to write fragments, and to break any sentence over 15 words. Options: (a) Strunk governs every full sentence; named registers (commit subjects, status lines) follow the project's house style and are exempt. Consequence: needs a one-line "house style wins" rule; registers must be named. (b) stop-yapping wins; Strunk's fragment and article rules are switched off. Consequence: the skill loses about a third of its mechanics rules. (c) Strunk wins everywhere. Consequence: breaks the compression the project orders. Recommended: (a).

**4. Are before-and-after examples allowed in the skill text?**
The skill-writing rule skill-creation says keep only sentences that instruct or forbid, and no attributes or non-prose inside a tag. Strunk's rules lean on error-to-fix pairs. The sibling skill `work-silently` already uses `never_do_this`/`do_exactly_this` blocks that break the skill-creation rule. Options: (a) fold an example into one instruction sentence, for six core rules only. Consequence: about 120-200 tokens; fits the cap. (b) copy the sibling block format. Consequence: breaks skill-creation, costs about 3 times the tokens per example. (c) none. Consequence: rules read as labels; fixes may drift. Recommended: (a).

**5. Which rules are always applied, and which only when time allows?**
The marketplace file ETHOS.md names six Strunk rules as its writing standard (active voice, positive form, concrete language, omit needless words, parallel construction, emphatic position). Version 4 of the Strunk text ranks four of them at "L3" (fix only "if easy"). Options: (a) a top tier: the six plus the highest-severity mechanics (comma splice, dangling opener, missing comma pair) are always applied; the rest only when polishing. Consequence: ETHOS and the skill agree; the pass has two tiers. (b) use v4 ranks. Consequence: four ETHOS principles become optional. (c) use v3 ranks. Consequence: v3 ranks themselves contradict v3's own lists (Oxford comma, positive form). Recommended: (a).

**6. Which rule text wins where v3 and v4 differ?**
Examples: whether "but" always needs a comma before it when two clauses share a subject (v3 yes, v4 optional); whether a semicolon is required before "therefore" after a full clause (v3 yes, v4 silent); whether "data" must be plural in technical text (v3 yes, v4 low priority). Options: (a) v3 wording for each, v4 only as the cut list. Consequence: more tokens per rule, higher fidelity. (b) v4 wording. Consequence: smaller; three or four mechanics behave differently from the long text. (c) drop the contested rules. Consequence: loses common agent errors (comma splice before adverb). Recommended: (a).

**7. How freely may the agent break a rule?**
v4 allows breaking a rule whenever "purpose clearly demands it" or breaking it "serves communicative purpose". v3 adds "if uncertain, follow the rule". Options: (a) break only for three named reasons: the user asks, a named register's house style requires it, or two rules conflict (then the ranking decides); in doubt, follow the rule. Consequence: checkable by a blind reader. (b) v4's open purpose test. Consequence: the agent can justify any deviation; compliance is untestable. Recommended: (a).

**8. Does "MUST" mean must?**
Strunk v3 tells the reader that its own MUST and NEVER mean only "default strongly unless justified". The marketplace rule file ETHOS.md says directive words are deliberate and must keep full force. Options: (a) drop the softening sentence; commands are hard, deviations come only through the named reasons in question 7. Consequence: the skill is stricter than its source. (b) keep the softening. Consequence: the skill's commands behave as suggestions, which the repo measured as failure. Recommended: (a).

**9. Which Strunk standard is the project's standard?**
CLAUDE.md, `.manifestos.yaml` and the agent `instruction-writer` bind subagents to the long text (v3, 27,097 tokens) by fetching it at each dispatch. A past orchestrator bound the compressed text (v4) for writing conduct skills. The new skill would be a third text, derived from v3. Options: (a) the skill serves in-session writing; dispatch binding stays v3. Consequence: three texts exist; drift possible; no change to existing dispatch. (b) change the dispatch rule to load the skill instead. Consequence: one source for agents, but a subagent must load skills (not verified to work by default). (c) retire the curl binding and keep only the skill. Consequence: changes CLAUDE.md, which this task may not edit. Recommended: (a).

**10. Does the skill apply to instruction files and tables?**
The rules favor prose paragraphs with topic sentences. The marketplace says tables replace prose for mappings, and skill files follow skill-creation's one-instruction-per-sentence, tag-structured form, which breaks the paragraph rules by design. Options: (a) exclude instruction files, tables and lists; they follow their own standard. Consequence: clear boundary; one extra sentence. (b) apply to everything. Consequence: skills it rewrites fail skill-creation. Recommended: (a).

**11. What may the skill say about the pronoun "they" and similar gender-sensitive rules?**
Strunk (both versions) prefers "he" for an unspecified person, or restructuring. The agent harness rule says to use "they" when a person's pronouns are not stated. Options: (a) the skill omits the rule; the harness rule governs. Consequence: loses one usage entry; no conflict. (b) the skill states "singular they". Consequence: costs a sentence; makes the harness rule explicit. (c) keep Strunk's rule. Consequence: contradicts the harness. Recommended: (a).

**12. Should the unit be scoped by the token cap or by the rules?**
The cap is 1,489 tokens (the size of `git-etiquette`). The compressed text alone, stripped of comments, is 2,468 tokens. Options: (a) cut to the cap by dropping examples, exemplars, ranking commentary and 14 low-value usage entries. Consequence: about 1,300-1,500 tokens (estimate); verify with `just tokens` after drafting. (b) raise the cap to about 2,400. Consequence: the skill is the largest in the plugin; more rules survive. (c) keep the cap and ship only the core tier (about 700 tokens). Consequence: cheapest; loses commas, paragraphs, tense, usage. Recommended: (a).
