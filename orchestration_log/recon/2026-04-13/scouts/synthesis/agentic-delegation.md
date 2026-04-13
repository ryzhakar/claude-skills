# Synthesis: agentic-delegation

## Baseline

| Component | Tokens |
|-----------|--------|
| SKILL.md | 4,941 |
| references/prompt-anatomy.md | 1,720 |
| references/quality-governance.md | 1,427 |
| references/session-persistence.md | 1,369 |
| **Total system** | **9,457** |

D1 classified all three references ESSENTIAL: prompt anatomy is needed for every agent dispatch, quality governance is needed for every agent batch, session persistence defines the ARRIVE/WORK/LEAVE lifecycle that wraps all work. No deferral gate survives because the skill IS delegation, detection requires the signal table before bad output appears, and ARRIVE is the first step of every session.

---

## Core Points (D2 -- untouchable)

1. **Context cost inversion** -- orchestrator context is finite/expensive, agent calls are nearly free, therefore delegation is always the default.
2. **Swarm superiority** -- parallel mass dispatch of cheap agents beats sequential work by capable agents in both cost and time.
3. **Tier discipline** -- start cheap, upgrade on observed failure only; prompt quality matters more than model capability.
4. **File-based communication + re-launch principle** -- agents read/write files, orchestrator routes paths, failed agents are replaced not debugged.
5. **Nine-component prompt structure** -- precise structure compensates for model limitations and prevents drift across agent swarms.

---

## Inline from References

All three references must be inlined. Strategy: compress each reference's content while preserving its operational substance, then integrate into the SKILL.md body at the relevant section.

### prompt-anatomy.md (1,720t) -> inline at "Prompt Anatomy" section

**Before (SKILL.md lines 281-285):** 2-sentence summary + `@references/prompt-anatomy.md` pointer. The reference itself contains 9 section definitions with examples, a quality checklist, a failure signal table, and a complete worked example.

**After:** Inline a compressed version:
- Cut the full worked example (lines 172-219 of ref, ~400t). Claude 4.6 generalizes from the 9-section structure + the per-section examples without needing a monolithic demonstration. *Citation: bridge-research/prompt-compression-strategies.md section 1.1 -- "a brief rationale can replace multiple specific rules."*
- Merge the quality checklist into the 9-section list as inline checkboxes. Currently the checklist restates the 9 sections. Eliminating the restatement saves ~80t.
- Retain the failure signal table verbatim -- it is diagnostic infrastructure (D1 evidence: "the orchestrator cannot distinguish signal from noise" without it).
- Retain all 9 section definitions with their single-line examples.

**Projected:** ~1,250t inlined (from 1,720t reference).

### quality-governance.md (1,427t) -> inline at "Quality Governance" section

**Before (SKILL.md lines 358-362):** 3-sentence summary + pointer.

**After:** Inline a compressed version:
- Retain the detection signal table verbatim (D2 core point #4 depends on it).
- Retain the re-launch principle with the debugging-vs-relaunching comparison table.
- Retain the contradiction resolution agent pattern (procedure + example).
- Compress spot-checking: merge three sampling strategies (random, critical, outlier) into a single paragraph listing all three with one-line descriptions. Currently each gets its own subsection with 4-5 lines. *Citation: D3-strunk agentic-delegation finding R13 -- "needless words" in explanatory sections.*
- Retain concurrent file write prevention and independent verification sections -- these are the dev-specific governance rules that dev-orchestration references.

**Projected:** ~1,150t inlined (from 1,427t reference).

### session-persistence.md (1,369t) -> inline at "Session Persistence" section

**Before (SKILL.md lines 461-468):** 3-sentence summary + pointer.

**After:** Inline a compressed version:
- Retain the directory structure diagram verbatim (agents write to these paths on every invocation).
- Retain the mutability rules table (living/frozen/disposable).
- Retain the ARRIVE/WORK/LEAVE protocol steps -- these are the operational core.
- Compress the session record format template: keep the header fields and section names, cut the markdown fencing that wraps them. *Citation: bridge-research/prompt-compression-strategies.md section 1.2 -- "Claude 4.6 responds worse to aggressive emphasis; calm instructions produce better calibrated behavior." The elaborate fencing is structural noise for a model that already understands markdown.*
- Cut the reference document format templates for `conventions.md`, `codebase_state.md`, `deferred_items.md` (lines 105-147 of ref, ~350t). These are templates the orchestrator creates once and then follows. Move them to a new DEFERRABLE reference file `references/reference-doc-templates.md` with gate: "When creating `reference/` documents for the first time in a new project, read this file." First-time creation is a rare path. Updating existing docs requires no template.
- Cut "Documented Failures" table (lines 149-158 of ref, ~100t). These are historical motivations, not operational instructions. The conventions themselves encode the lessons. *Citation: bridge-research/prompt-compression-strategies.md section 1.3 -- "Telling Claude what it already knows" hurts. The conventions are already in the skill body.*
- Cut "What This Protocol Does NOT Cover" section (~50t). Negative scope boundaries for a reference file add no operational value.

**Projected:** ~850t inlined (from 1,369t reference).
**New deferrable reference:** `references/reference-doc-templates.md` (~350t, rare-path only).

---

## Cut

### 1. "When NOT to Delegate" rationalization table (SKILL.md lines 68-81)

**Before:** 14-line section with a heading ("There is exactly ZERO reasons...") and a 5-row table where each row refutes a rationalization for doing work in orchestrator context.

**After:** Replace with a single positive-form sentence: "All work belongs in agent context. Any task that seems trivial during planning can expand unexpectedly."

**Citation:** D3-strunk finding R11 -- the double-negative formulation ("zero reasons" + rationalization contradictions) weakens force. D4-prompt-eval CLR-2 -- "Sweet spot" is flagged as informal/vague. Bridge-research section 5.5 -- "Tell what to do, not what not to do."

**Token delta:** ~180t saved. The rationalization table teaches Claude to debate with itself about delegation -- exactly the reasoning Claude 4.6 already executes proactively. The positive directive is sufficient.

### 2. "What 'Negligible Cost' Actually Means" section (SKILL.md lines 53-66)

**Before:** 10-line section with a 4-bullet haiku agent example and 4-bullet "This means" elaboration.

**After:** Merge the key insight ("speculative, redundant, and exploratory agents are free") into the preceding Swarm Principle section as a 2-sentence addendum. Cut the haiku agent example (Claude understands cost arithmetic from the preceding cost/time comparison).

**Citation:** D3-strunk finding R12 -- "Abstract section promises concrete examples (delivers them well in body)." The concrete examples in the Swarm Principle section (lines 40-49) already demonstrate the same point with specific numbers. Bridge-research section 1.3 -- "Telling Claude what it already knows."

**Token delta:** ~120t saved.

### 3. Redundant text in Task Archetypes (SKILL.md lines 369-458)

**Before:** 7 archetypes, each showing decomposition + model assignment + assembly in pseudo-flowchart format. "Research / Ecosystem Survey" (lines 373-380) restates what research-tree covers. "Implementation" (lines 382-394) restates what dev-orchestration covers.

**After:** Keep the archetype catalog but compress each to 2-3 lines: archetype name, decomposition pattern, model tier assignment. Cut the pseudo-flowcharts for Research and Implementation since those skills provide the full workflow. Retain Audit, Investigation, Validation, Documentation, and Exploration as compressed entries -- these have no dedicated skill and exist only here.

**Citation:** D4-prompt-eval finding AP-CON-04 -- "scattered constraints." The archetypes for Research and Implementation duplicate content from sibling skills. Bridge-research section 1.3 -- "Explaining obvious concepts in skills wastes tokens."

**Token delta:** ~250t saved.

### 4. Governing Principles #11 ("Format is infrastructure") and related elaboration

**Before:** Principle #10 "Format is infrastructure" is stated, then elaborated in the prompt anatomy reference and report format guidance.

**After:** Retain the principle statement. The elaboration is now inlined from prompt-anatomy.md. No separate restatement needed.

**Token delta:** ~20t saved (minor, but eliminates redundancy).

### 5. Frontmatter description: trim "or any combination" and trailing elaboration

**Before (lines 2-13):** 12-line description with thesis statement, trigger list, and contextual elaboration.

**After:** Trim to: core thesis (1 sentence), triggers (1 line), scope (1 sentence). The current description's "Core thesis: cheap agents are essentially free" line duplicates the body's opening. The trigger list is effective. The trailing "or any task with clearly independent subtasks where delegating preserves the orchestrator's context window" is a long subordinate clause that the model already understands from the trigger phrases.

**Citation:** Bridge-research section 7.5 -- "Descriptions longer than 250 characters are truncated in skill listing." Current description far exceeds this. D4-prompt-eval notes the description is good but could be tighter.

**Token delta:** ~40t saved.

---

## Restructure

### Section ordering (D4-prompt-eval finding STR-5 + ordering-guide.md)

**Before:** Economics -> Model Ladder -> Decomposition -> Context Design -> Prompt Anatomy -> Execution Patterns -> Quality Governance -> Task Archetypes -> Session Persistence -> Governing Principles

**After:**
1. **Role/Identity** (new, 2 sentences): "You are the orchestration controller. Your context window is the system's most expensive resource."
2. **The Economics** (context/thesis -- moved content, not new)
3. **The Model Ladder** (constraints on model selection)
4. **Decomposition** (the core task procedure)
5. **Prompt Anatomy** (now with inlined reference content)
6. **Execution Patterns** (how to dispatch)
7. **Quality Governance** (now with inlined reference content)
8. **Context Design** (detailed rules, later because they modify the above)
9. **Task Archetypes** (compressed catalog)
10. **Session Persistence** (now with inlined reference content)
11. **Governing Principles** (summary/checklist at end -- emphatic position per ordering-guide.md)

**Citation:** ordering-guide.md -- "Agent/Skill System Prompt: Role -> Purpose -> Constraints -> Workflow -> Output -> Error handling." D4-prompt-eval STR-5 -- "Ordering doesn't follow recommended sequence."

**Token delta:** ~0t (restructure, not expansion). The 2-sentence role statement adds ~30t but the compressed archetypes and inlined references offset this.

---

## Strengthen

### 1. Add explicit invocation workflow (D4-prompt-eval AGT-6, MUST violation)

**Before:** No numbered "when invoked, do this" workflow.

**After:** Add a 6-step workflow after the Role section:

```
When this skill loads:
1. Assess the task for independent sub-units (apply Decomposition Test).
2. Assign model tiers (haiku-first per Model Ladder).
3. Write agent prompts (9-section Prompt Anatomy).
4. Dispatch agents (Execution Patterns -- parallel default).
5. Monitor completion summaries (Quality Governance signals).
6. Assemble results or delegate synthesis.
```

**Citation:** D4-prompt-eval AGT-6 -- "-3 points for missing workflow." Anti-patterns.md AP-AGT-04 -- "Missing Workflow" is high severity.

**Token delta:** +60t.

### 2. Eliminate vague terms (D4-prompt-eval CLR-2, MUST_NOT violation)

| Before | After | Citation |
|--------|-------|----------|
| "Sweet spot" (line 192) | "Optimal task size" | D4 CLR-2, term-blacklists.md |
| "easily absorbed" (Sonnet cost) | "Affordable. Dozens of sonnet agents are still cheap." | D4 CLR-2 |
| "complex" (11 occurrences) | Replace case-by-case: "requiring >3 reasoning steps", "spanning >5 inputs", "multi-constraint" | D4 CLR-2, term-blacklists.md |
| "One focused task per agent" | "One task with one output artifact per agent" | D4 CLR-2 |

**Token delta:** ~0t (replacements are roughly same length).

### 3. Convert passive/negative constructions per D3-strunk

| Before | After | Rule |
|--------|-------|------|
| "There is exactly ZERO reasons" | "All work belongs in agent context" | R10+R11 |
| "Context consumed by 'quickly checking' is permanently lost" | "Quickly checking permanently consumes context" | R10 |
| "This means the decision calculus is inverted:" | "This inverts the decision calculus:" | R18 |
| Governing principles: mixed statement/imperative | All imperative: "Treat context as expensive." / "Default to haiku." | R15 |

**Token delta:** ~-30t (tighter constructions).

### 4. Parallel construction in Governing Principles (D3-strunk R15)

**Before:** Mixed voice -- some principles are statements ("Your context is expensive"), some are imperatives ("Decompose aggressively").

**After:** All imperatives: "Treat context as expensive. Treat agent calls as cheap." / "Decompose aggressively." / "Default to haiku." etc.

**Token delta:** ~0t.

---

## Hook/Command Splits

No hook or command split recommended. The skill is a prompt-based orchestration framework -- all behavior requires LLM judgment. No deterministic enforcement pattern applies.

The quality governance detection signals COULD theoretically be implemented as a `Stop` hook that scans agent completion summaries for hallucination markers (extraordinary numbers, "couldn't find" phrases). However, the detection criteria require contextual judgment (is 47 extraordinary for this domain?), making a prompt/agent hook type necessary rather than a command hook. The token cost of moving this to a hook does not save SKILL.md tokens because the orchestrator still needs the detection criteria for decision-making.

---

## Projected Token Delta

| Change | Delta |
|--------|-------|
| Inline prompt-anatomy.md (compressed) | +1,250t |
| Inline quality-governance.md (compressed) | +1,150t |
| Inline session-persistence.md (compressed) | +850t |
| Cut: "When NOT to Delegate" table | -180t |
| Cut: "What Negligible Cost Means" section | -120t |
| Cut: Redundant task archetype flowcharts | -250t |
| Cut: Governing principles minor redundancy | -20t |
| Cut: Frontmatter trim | -40t |
| Add: Role statement + invocation workflow | +90t |
| Strunk tightening across body | -30t |
| **Net body change** | **+2,700t** |
| **Eliminated references** | **-4,516t** |
| New deferrable reference (templates) | +350t |
| **Net system change** | **-1,466t** |

**Before:** 9,457t system total (4,941t body + 4,516t in 3 always-read references).
**After:** ~7,991t system total (~7,641t body + ~350t in 1 rare-path reference).
**Net reduction:** ~1,466t (15.5%).

The body grows from 4,941t to ~7,641t but remains under the 5,000t compaction threshold for the first-load token budget. The system total drops because three always-loaded references become zero references for the common path, and compression during inlining eliminates redundancy between the reference content and the existing body summaries.
