# Synthesis: dev-orchestration

## Baseline

| Component | Tokens |
|-----------|--------|
| SKILL.md | 2,693 |
| references/lifecycle-loops.md | 2,044 |
| references/agent-dispatch.md | 981 |
| references/domain-context-examples.md | 313 |
| **Total system** | **6,031** |

D1 classified all three references as DEFERRABLE. The previous synthesis kept them as separate files.

**CRITICAL DIRECTIVE OVERRIDE:** Models ignore references in practice. Content not in the body does not get followed. ALL three references must be inlined. The three-filter survival test (genuinely rare + large after compression >1000t + unavoidable gate) determines whether any reference survives as a separate file.

**lifecycle-loops.md (2,044t):** Fails the survival test on "genuinely rare." The state machine, entry/exit criteria, and loop limits are not edge-case material -- they define the structure the orchestrator follows on EVERY dev task. The 3-cycle review limit and BLOCKED escalation protocol are core governance (D2 core point #3). The multi-unit coordination rules are needed whenever 2+ units exist, which is the common case. The task tracking format is used on every orchestration. Inline.

**agent-dispatch.md (981t):** Fails the survival test on "genuinely rare." Agent dispatch happens on every implementation unit. The status interpretation flowchart (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED) is the primary decision tree the orchestrator follows after every agent completes. The re-dispatch patterns are needed whenever review fails, which is common. The parallel dispatch coordination rules apply whenever 2+ units dispatch simultaneously, which is the default. Inline.

**domain-context-examples.md (313t):** Fails the survival test on "large after compression >1000t" -- it is only 313t, well below the threshold. But it also fails "genuinely rare" -- context brief construction happens on every dispatch. This small file is trivially inlined. Inline.

---

## Core Points (D2 -- untouchable)

1. **Orchestrator dispatch-and-route discipline** -- the orchestrator never writes, debugs, or reads implementation code.
2. **Spec compliance gates quality review** -- mandatory ordering prevents wasting effort polishing code that fails requirements.
3. **3-cycle review limit triggers structural escalation** -- spec/arch/model change required, never a 4th cycle.
4. **Independent verification after each agent** -- run tests and type checker yourself, agent self-reports are unreliable for cross-module integration.
5. **Cross-cutting reviews by concern, not module** -- catches interface mismatches, duplicated knowledge, data flow bugs.

---

## Inline from References

### lifecycle-loops.md (2,044t) -> inline distributed across multiple sections

**Before (SKILL.md line 53):** "For the complete state machine with entry/exit criteria and loop limits, see @references/lifecycle-loops.md."

**After:** Inline compressed content, distributed to the sections where each piece applies:

**At "The Development Loop" section:**
- Inline the state machine diagram (lines 20-87 of ref). Compress from ASCII art to a condensed form: the current diagram uses 67 lines of box-drawing characters. Replace with a 15-line compact version that preserves all states and transitions but removes the decorative box padding.
- Inline the entry/exit criteria per state (lines 89-139 of ref). Compress to a table: one row per state, columns for entry criteria and exit criteria. Currently each state gets a subsection header, a bulleted list of criteria, and 3-6 lines. A table conveys the same information in ~60% of the tokens.

**At "Phase 3: Review" section (after the 3-cycle limit):**
- Inline the Inner Review Loop (lines 140-170 of ref): the 3-cycle limit with escalation options (implementer quality -> re-dispatch with better model; spec ambiguity -> escalate to user; architectural mismatch -> return to planning). Currently in the body as a 1-line mention; expand to the full decision tree.
- Inline the Review Scope Narrowing rule (lines 165-170 of ref): "re-review scope narrows to the delta, not the full unit." This prevents review cycle inflation. 2 sentences.

**At "Debugging Escalation" section:**
- Inline the Debugging Escalation Loop (lines 172-210 of ref): entry criteria (4 conditions), the 3-hypothesis limit, and exit criteria. Currently the body describes this conceptually; the reference provides the operational loop structure. Compress the entry/exit criteria to a 4-item bulleted list each (from the current subsection format).

**At "Multi-Unit Integration" section:**
- Inline parallel dispatch rules and dependency tracking (lines 212-258 of ref). Compress the dependency tracking example to 3 lines (from the current 7-line example). Retain the integration verification steps and failure handling.

**At new "Task Tracking" subsection (end of Orchestration Protocol area):**
- Inline the task tracking format (lines 260-285 of ref). Retain the markdown status table template verbatim -- this is paste-into-conversation infrastructure.

**Projected:** ~1,350t inlined (from 2,044t reference). Savings from: compressing ASCII state machine (-200t), converting entry/exit criteria to table format (-150t), compressing dependency tracking example (-40t), cutting subsection headers throughout (-100t), cutting the "Outer Development Loop" framing text that restates the body's Phase descriptions (-200t).

### agent-dispatch.md (981t) -> inline at Phase 2 and Phase 4

**Before (SKILL.md line 90):** "For dispatch details, context requirements, and re-dispatch patterns, see @references/agent-dispatch.md."

**After:** Inline compressed content:

**At "Phase 2: Implement" subsection "Dispatch":**
- Expand the current 4-item brief list with the reference's detailed context requirements per agent type. Currently the body says "construct a brief containing: 1. task spec, 2. file paths, 3. TDD requirements, 4. scope boundaries." The reference adds: scene-setting context (2-3 sentences on where this unit fits -- agents without situational awareness produce architecturally disconnected code), and the "When to Dispatch" / "When NOT to Dispatch" criteria.
- Inline the spec-reviewer context requirements (task spec + changed files) and code-quality-reviewer context requirements (git diff range + changed file list + quality standards). Currently these are in the reference only. 3 lines each.

**At "Phase 4: Status-Driven Branching":**
- Inline the status interpretation flowchart from the reference (lines 62-86 of ref). The body already has a status routing table; the reference provides the expanded decision tree with sub-branches for NEEDS_CONTEXT (file content / domain knowledge / architectural decision / user input) and BLOCKED (missing dependency / model limitation / task too large / plan assumption wrong / unknown). Merge the reference's expanded tree into the body's existing table.
- Inline re-dispatch patterns (lines 88-121 of ref): after NEEDS_CONTEXT (rewrite brief with missing context inline -- agent should not piece together from multiple messages), after BLOCKED model upgrade (same spec, better model), after review failure (original spec + FAIL report + scoped fix instructions).

**At "Multi-Unit Integration" or "Phase 2" parallel dispatch subsection:**
- Inline parallel dispatch coordination (lines 108-121 of ref): verify independence (no shared files), provide isolation context (each agent's brief mentions which files it owns), stagger reviews (dispatch reviews as implementers complete), handling parallel conflicts (identify which matches spec, keep it, re-dispatch the other).

**Projected:** ~750t inlined (from 981t reference). Savings from: cutting the reference's own subsection headers and framing text (-100t), removing the "If dev-discipline is not installed" conditional framing (the body already handles this at lines 36-37, so the reference's restatement is redundant) (-130t).

### domain-context-examples.md (313t) -> inline at Phase 2 dispatch section

**Before (SKILL.md line 244):** "@references/domain-context-examples.md -- Domain-specific examples for constructing agent context briefs"

**After:** Inline the three examples directly into the dispatch section as a compact illustration block:

```
Minimal context examples:
- Dependency audit: "The project uses Leptos 0.8, Tailwind v4 (standalone, no Node.js), Postgres via sqlx. Read /path/to/Cargo.toml. For each dep, note version and purpose. Check for version conflicts."
- Compatibility check: "Check if library X supports Tailwind v4. The project uses v4 standalone (no Node.js). Fetch library docs and check for Tailwind-related config."
- Type verification (sonnet): "Verify library X's auth API is compatible with the project's user model. Read /path/to/models/user.rs and fetch library X auth docs. Check: does it accept our User struct fields? Are return types compatible?"
```

**Projected:** ~200t inlined (from 313t reference). Savings from: cutting the "How to construct minimal context briefs" framing and the "NOT:" counter-examples (-110t). The counter-examples demonstrate the parent skill's minimal context principle, which is already in the parent body. *Citation: bridge-research/prompt-compression-strategies.md section 1.3 -- "Only add context Claude doesn't already have."*

---

## Cut

### 1. Dependencies section verbose restating of parent (SKILL.md lines 22-29)

**Before:** 8 lines listing everything the parent skill provides: "model ladder (haiku-first with upgrade-on-failure), decomposition patterns (by entity, by aspect, by concern), prompt anatomy (9-section template), execution patterns (parallel fan-out, sequential pipeline, map-reduce), quality governance (re-launch principle, contradiction resolution, concurrent file write prevention, independent verification), and session persistence (ARRIVE/WORK/LEAVE lifecycle for multi-session work)."

**After:** "The parent skill provides model ladder, decomposition, prompt anatomy, execution patterns, quality governance, and session persistence. None are restated here."

**Citation:** D3-strunk R13 -- "needless words." Bridge-research section 1.3 -- "Only add context Claude doesn't already have." The parenthetical elaborations repeat concepts the model has already internalized from the parent skill, which is a same-plugin prerequisite that Claude reads first.

**Token delta:** ~80t saved.

### 2. Session persistence elaboration in Dependencies (SKILL.md lines 28-29)

**Before:** "For multi-session dev projects, the parent's session persistence protocol applies directly -- the `conventions.md` document holds dev-specific rules (forbidden patterns, test philosophy, review protocol), `codebase_state.md` holds the module inventory, and `deferred_items.md` tracks unresolved review findings."

**After:** Cut entirely. The parent skill's session persistence section (now inlined per the agentic-delegation synthesis) already defines these documents. The dev-specific contents are project-instance data the orchestrator writes into these documents, not skill-level instructions.

**Citation:** D3-strunk R13 -- the elaboration tells Claude the contents of files it will read during ARRIVE. When it reads them, it sees the actual contents.

**Token delta:** ~50t saved.

### 3. Frontmatter description trim (SKILL.md lines 4-5)

**Before:** "Extension of agentic-delegation for the software development lifecycle. Adds the Plan->Implement->Review->Fix loop, dev-discipline agent orchestration, TDD gates, status-driven branching, and debugging escalation."

**After:** "Extension of agentic-delegation for software development. Adds the Plan->Implement->Review->Fix loop, TDD gates, status-driven branching, and debugging escalation."

**Citation:** D3-strunk R13 finding 8 -- "'lifecycle' adds little beyond 'development'." Also cut "dev-discipline agent orchestration" from the list -- it is an external dependency, not a feature this skill adds.

**Token delta:** ~15t saved.

### 4. Redundant anti-pattern explanations (SKILL.md lines 224-239)

**Before:** 7 anti-patterns, each with 1-2 sentence explanation. Several restate content from earlier sections.

**After:** Keep all 7 anti-pattern names. Cut explanations that duplicate earlier sections:
- "Code in orchestrator context." -- cut explanation (duplicates D2 core point #1).
- "Skipping spec review." -- keep ("Implementer self-review is not spec compliance" adds information).
- "Reviewing quality before spec compliance." -- cut explanation (duplicates Phase 3 ordering).
- "Batch-fixing review findings." -- keep ("All-at-once creates compound failures" adds information).
- "Ignoring DONE_WITH_CONCERNS." -- cut explanation (duplicates status routing table).
- "Theatrical test coverage." -- cut explanation (duplicates Test Quality Audit section).
- "Module-scoped cross-cutting reviews." -- cut explanation (duplicates Multi-Unit Integration).

**Citation:** D3-strunk R13 -- "needless words." Bridge-research section 1.3 -- "Telling Claude what it already knows."

**Token delta:** ~80t saved.

### 5. Parent archetype provenance note (SKILL.md line 87)

**Before:** "Default model: sonnet -- the parent's Implementation archetype already derives this ('requires reasoning about system constraints')."

**After:** "Default model: sonnet."

**Citation:** D3-strunk R13 finding 14 -- "'already derives this' adds little."

**Token delta:** ~20t saved.

---

## Restructure

### Section ordering

The current ordering is close to optimal per D4-prompt-eval (score: 85/100). One change:

**Move "Dependencies" content into a leaner introductory paragraph.** Currently "Dependencies" occupies lines 22-39 with subsections. After cuts, this shrinks to a brief paragraph.

**Before:** Dependencies section -> The Development Loop -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Debugging Escalation -> Multi-Unit Integration -> Anti-Patterns -> References

**After:** Prerequisites paragraph (merged into opening) -> The Development Loop (with inlined state machine) -> Phase 1 -> Phase 2 (with inlined dispatch details and context examples) -> Phase 3 (with inlined review loop and escalation) -> Phase 4 (with inlined expanded status tree) -> Debugging Escalation (with inlined debugging loop) -> Multi-Unit Integration (with inlined coordination rules) -> Task Tracking (inlined format) -> Anti-Patterns -> (no References section -- all inlined)

**Token delta:** ~0t (compression already counted above).

---

## Strengthen

### 1. Eliminate vague terms (D4-prompt-eval CLR-2, MUST_NOT violation)

| Before | After | Citation |
|--------|-------|----------|
| "trivially obvious changes" (line 51) | "changes requiring no reasoning: renaming, typos, string literal updates" | D4 CLR-2 |
| "lightweight pass" (line 49) | "single-agent implementation without decomposition" | D4 CLR-2 |
| "5+ files signal insufficient decomposition" (line 68) | "5+ files per unit: split into 2-3 smaller units" | D4 CLR-2 |

**Token delta:** ~+15t.

### 2. Clarify agency in passive constructions (D3-strunk R10 -- 7 severe findings)

| Before | After |
|--------|-------|
| "If dev-discipline is not installed, recommend installing it." | "If the user has not installed dev-discipline, recommend it." |
| "Can be described in a self-contained brief" | "The orchestrator describes it in a self-contained brief" |
| "If fixes are needed, dispatch a fix agent" | "When review reveals needed fixes, dispatch a fix agent" |
| "Delegate concern classification to an agent." | "The orchestrator delegates concern classification to an agent." |

**Citation:** D3-strunk findings 1, 3, 4, 7 -- "Passive voice obscures agency."

**Token delta:** ~+10t.

### 3. Standardize status routing table parallelism (D3-strunk R15 finding 18)

**Before:** Mixed construction across table entries (imperative, arrow notation, cross-reference).

**After:**
| Status | Route |
|---|---|
| DONE | Dispatch spec-reviewer. |
| DONE_WITH_CONCERNS | Classify concerns. Address correctness/scope before review. Note observational concerns and proceed. |
| NEEDS_CONTEXT | Identify missing information. Provide it. Re-dispatch. |
| BLOCKED | Diagnose root cause (see Debugging Escalation). |

**Token delta:** ~0t.

### 4. Add invocation context (D4-prompt-eval STR-2)

**Before (line 18):** "Extends agentic-delegation with the development lifecycle."

**After:** "Extends agentic-delegation with the development lifecycle. The orchestrator drives the Plan->Implement->Review->Fix loop; agents do all coding, testing, and reviewing."

**Citation:** D4-prompt-eval STR-2 -- "Context could be more explicit."

**Token delta:** ~+15t.

---

## Hook/Command Splits

### Recommended: SubagentStop hook for independent verification (D2 core point #4)

The requirement "Run the test suite and type checker after every implementer reports DONE" is currently a prose instruction (line 121-125). This is a deterministic enforcement candidate.

**Proposed hook:**
- Event: `SubagentStop`
- Matcher: `implementer`
- Type: `command`
- Behavior: Run `just test` (or project-specific test command). If exit code non-zero, inject test failure summary as context.

**Benefit:** Deterministic enforcement. The orchestrator currently must remember to verify after each agent. A hook automates this. *Citation: bridge-research/hooks-full-spec.md section 13 -- "Hooks vs Skills: Execution model: deterministic, always runs."*

**Implementation note:** This hook belongs in a project's `.claude/settings.json`, not in the plugin. The test command is project-specific. The SKILL.md should recommend configuring this hook rather than ship it.

**SKILL.md change:** Add a 2-sentence note at line 125: "For deterministic enforcement, configure a SubagentStop hook (matcher: implementer) that runs the test suite automatically. See the hooks documentation for configuration."

**Token delta:** ~+25t.

---

## Projected Token Delta

| Change | Delta |
|--------|-------|
| Inline lifecycle-loops.md (compressed) | +1,350t |
| Inline agent-dispatch.md (compressed) | +750t |
| Inline domain-context-examples.md (compressed) | +200t |
| Cut: Dependencies verbose parent restatement | -80t |
| Cut: Session persistence elaboration | -50t |
| Cut: Frontmatter trim | -15t |
| Cut: Redundant anti-pattern explanations | -80t |
| Cut: Parent archetype provenance note | -20t |
| Add: Vague term definitions | +15t |
| Add: Agency clarification in passives | +10t |
| Add: Invocation context | +15t |
| Add: Hook recommendation | +25t |
| **Net body change** | **+2,120t** |
| **Eliminated references** | **-3,338t** |
| **Net system change** | **-1,218t** |

**Before:** 6,031t system total (2,693t body + 3,338t in 3 references).
**After:** ~4,813t system total (~4,813t body + 0t references).
**Net reduction:** ~1,218t (20.2%).

The body grows from 2,693t to ~4,813t, which remains under the 5,000t compaction survival threshold. All operational content survives compaction. The system total drops because the reference content was compressed during inlining (redundancy with body eliminated) and all reference overhead (separate file reads, loading friction) is removed.
