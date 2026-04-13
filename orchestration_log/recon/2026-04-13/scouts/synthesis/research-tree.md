# Synthesis: research-tree

## Baseline

| Component | Tokens |
|-----------|--------|
| SKILL.md | 2,872 |
| references/agent-templates.md | 2,474 |
| references/report-formats.md | 1,783 |
| references/tier-playbook.md | 2,064 |
| references/anti-patterns.md | 2,222 |
| **Total system** | **11,415** |

D1 classified agent-templates.md and report-formats.md as ESSENTIAL (needed for every agent prompt construction). tier-playbook.md and anti-patterns.md were classified DEFERRABLE.

**CRITICAL DIRECTIVE OVERRIDE:** Models ignore references in practice. Content not in the body does not get followed. ALL four references must be inlined. The three-filter survival test (genuinely rare + large after compression >1000t + unavoidable gate) determines whether any reference survives as a separate file.

**tier-playbook.md (2,064t):** Fails the survival test. Tier transitions happen on EVERY research invocation. The orchestrator needs agent count heuristics and completion gates at every tier launch -- this is the common path, not a rare edge case. Inline.

**anti-patterns.md (2,222t):** Fails the survival test. Anti-pattern detection is required before launching each tier and after scanning completion summaries -- again, every invocation. The "10 failure modes" detection checklist is operational infrastructure the orchestrator applies continuously, not a debugging-only resource. Inline.

---

## Core Points (D2 -- untouchable)

1. **Disk-based communication (no context relay)** -- agents write reports to disk, orchestrator routes file paths, never relays content.
2. **Primary source verification** -- documentation and marketing are hypotheses; verification means fetching manifests, source code, registry APIs.
3. **Need-driven organization** -- structure research by stakeholder decisions, not source categories.
4. **Parallel execution within tiers** -- all agents in a tier launch simultaneously; no within-tier dependencies.
5. **Fresh eyes for re-research** -- second-round agents receive raw facts only, never prior conclusions or ratings.

---

## Inline from References

### agent-templates.md (2,474t) -> inline at new "Agent Prompt Templates" section

**Before (SKILL.md line 125):** One-sentence pointer: "For domain-adaptable skeletons, see @references/agent-templates.md."

**After:** Inline compressed templates:
- Retain the Prime Directive Block verbatim -- it appears in every research agent prompt (D2 core point #2 depends on it).
- Retain all 8 template skeletons (Index Parser, Need-Category Surveyor, Project Auditor x3, Candidate Verifier, Breadth Expander, Contradiction Resolver, Production Inspector, Synthesizer).
- Compress each template: merge "Model:" and "Tools needed:" footer lines into a single-line header annotation (e.g., "**Index Parser** (cheapest; WebFetch, Write)"). Saves ~10t per template, ~80t total.
- Cut the Template Adaptation Checklist (lines 335-348 of ref, ~100t). This restates prompt structure requirements already in the parent skill's prompt anatomy. *Citation: bridge-research/prompt-compression-strategies.md section 1.3 -- "Only add context Claude doesn't already have."*
- Replace `[paste from @references/report-formats.md -- X template]` placeholders in templates with "Paste the relevant format from the Report Format Templates section below." The formats are now in the same file.

**Projected:** ~2,300t inlined (from 2,474t reference).

### report-formats.md (1,783t) -> inline at new "Report Format Templates" section

**Before (SKILL.md line 219):** One-sentence pointer in references list.

**After:** Inline all format templates:
- Retain all 6 format templates verbatim (Index, Category Survey, Deep Verification, Project Audit, Contradiction Resolution, Synthesis). These are paste-into-prompt infrastructure -- every character matters for agent output consistency.
- Cut the "Format Enforcement" trailing section (lines 245-253 of ref, ~80t). The enforcement principle ("paste template, deviations indicate misunderstanding") is already stated in the agent design section. *Citation: D3-strunk R13 -- needless words.*
- Retain the rating scale definitions (ADOPT/EVALUATE/SKIP, VERIFIED/UNVERIFIED/INCOMPATIBLE) -- these are vocabulary the synthesis agent depends on.

**Projected:** ~1,700t inlined (from 1,783t reference).

### tier-playbook.md (2,064t) -> inline at expanded "Tier System" section

**Before (SKILL.md line 83):** "For skip conditions and heuristics, see @references/tier-playbook.md -- it covers tier definitions, completion gates, and agent count heuristics."

**After:** Inline compressed tier-by-tier operational details:
- Per tier, compress to: **Purpose** (1 sentence), **Agent count heuristic** (1 line), **Completion gate** (bulleted checklist), **Common failure / model selection** (1-2 lines). The current playbook uses full subsections with tables for each; compress tables to inline text.
- Retain the "Tier Transition Decisions" section compressed: the "How Many Tiers?" table (4 rows mapping research need to tiers used), "When to Add Agents," "When to Stop Early," "When to Launch a Second Round" -- each compressed to 2-3 lines from the current 5-8 lines.
- Cut the verbose "Agent Design" tables per tier (lines 17-24, 47-52, 77-82, etc. of ref) -- these repeat information already in the agent templates section. The templates ARE the agent design.
- Merge the "Orchestrator Decision" note from Tier 1 ("Read ONLY the statistics/category list, ~20 lines") into the existing Tier 1 prose since this is a key operational constraint.
- Retain "How to Define Need-Categories" from Tier 2 verbatim (lines 86-91 of ref) -- this is the operational expression of D2 core point #3 and agents fail without it.

**Projected:** ~1,200t inlined (from 2,064t reference).

### anti-patterns.md (2,222t) -> inline at expanded "Anti-Patterns" section

**Before (SKILL.md lines 206-211):** 3-line summary of the "three most damaging" plus pointer to full catalog.

**After:** Inline all 10 anti-patterns compressed:
- Retain all 10 anti-pattern names and their core descriptions. Currently each AP gets 10-20 lines (pattern + why it fails + detection + fix). Compress each to: name, 1-sentence problem statement, 1-sentence fix. The verbose "Why it fails" explanations restate principles already in the body (context relay = body's "Reports are the product"; README trust = body's prime directive; etc.). *Citation: bridge-research/prompt-compression-strategies.md section 1.3 -- "Only add context Claude doesn't already have."*
- Retain the two detection checklists verbatim ("Before launching each tier" and "Before launching synthesis"). These are operational checklists the orchestrator runs at tier transitions -- paste-and-apply infrastructure.
- Cut AP-4 (Model Waste) verbose explanation -- the body's "Model Selection" table already covers this. Keep the AP name and 1-line fix.
- Cut AP-5 (Sequential Addiction) verbose explanation -- the body's "Parallel execution within tiers" (D2 core point #4) already covers this. Keep the AP name and 1-line fix.

**Projected:** ~1,400t inlined (from 2,222t reference).

---

## Cut

### 1. "Philosophy" section opening abstraction (SKILL.md lines 22-23)

**Before:** "Research is not a procedure. It is a series of decisions about scope, depth, and course correction. The tiers below are default gravity -- not a script."

**After:** "Research is deciding where to look, how deep to go, and when to change course. The tiers below are default gravity -- not a script."

**Citation:** D3-strunk R12 finding -- "'Series of decisions' remains somewhat abstract." The revision makes the decisions tangible.

**Token delta:** ~5t saved.

### 2. Redundant tier descriptions between diagram and prose (SKILL.md lines 67-96)

**Before:** The tier system appears twice: once as an ASCII diagram (lines 67-81) and again as prose paragraphs (lines 85-96). The prose paragraphs elaborate each tier with 2-3 sentences.

**After:** Retain the ASCII diagram. Replace the separate prose paragraphs with the inlined tier-playbook content (compressed). Each tier gets its operational detail from the playbook rather than a separate restating paragraph. This eliminates the current redundancy where the diagram says "GROUND TRUTH" and the prose below says "Before evaluating any external option, establish what the stakeholder has and needs" -- which repeats the diagram.

**Citation:** D3-strunk R13 -- "needless words." The diagram + inlined playbook per tier replaces diagram + prose + separate reference file.

**Token delta:** ~100t saved (prose paragraphs cut; replaced by playbook content accounted separately).

### 3. "Session Persistence" section (SKILL.md lines 61-66)

**Before:** 6-line section explaining how session persistence applies to research-tree, ending with "Read the parent's session-persistence reference for the full ARRIVE/WORK/LEAVE lifecycle."

**After:** Compress to 2 sentences: "For multi-session research, the parent's ARRIVE/WORK/LEAVE lifecycle applies. The `reference/` layer holds research-specific conventions and findings inventory; `recon/` holds raw scouting data (gitignored)."

**Citation:** D3-strunk R13 -- the current text explains the three persistence layers with full sentences where a parenthetical listing suffices. The parent skill (now with inlined session-persistence content) carries the protocol details.

**Token delta:** ~40t saved.

### 4. "Adapting to Different Domains" table (SKILL.md lines 194-204)

**Before:** 5-row table showing domain adaptation (Software, Market, Academic, Regulatory, API) with Primary Source, Registry/DB, and Verification Method columns.

**After:** Retain the table but cut the "API ecosystem" row -- it is a subset of "Software ecosystem" with minor differences. Merge its distinctive verification methods (latency measurements, rate limit checks) into the Software row as parentheticals.

**Citation:** D3-strunk R13 -- the API row adds minimal unique information.

**Token delta:** ~20t saved.

### 5. "References" section trailing list (SKILL.md lines 215-219)

**Before:** 5-line section listing all reference files with descriptions.

**After:** Remove all entries -- all four references are now inlined. Remove the examples entry (awesome-leptos-session.md) from the references list -- it is a historical worked example, not operational infrastructure. If a user needs it, they can find it in the examples directory.

**Token delta:** ~50t saved.

---

## Restructure

### Section ordering (D4-prompt-eval STR-5)

**Before:** Philosophy -> Tier System -> Agent Design -> Orchestration Protocol -> Directory Structure -> Domain Adaptation -> Anti-Patterns -> References

**After:**
1. **Philosophy** (context -- Five Truths + Model Selection)
2. **The Tier System** (diagram + inlined per-tier operational detail from tier-playbook)
3. **Tier Transitions** (inlined from tier-playbook: how many tiers, when to stop, when to add agents, when to re-research)
4. **Orchestration Protocol** (workflow -- moved UP from position 4, per D4 finding)
5. **Agent Design** (Prime Directive + prompt structure spec)
6. **Agent Prompt Templates** (inlined from agent-templates.md)
7. **Report Format Templates** (inlined from report-formats.md)
8. **Directory Structure** (output format)
9. **Domain Adaptation** (compressed table)
10. **Anti-Patterns** (all 10 compressed, detection checklists verbatim)

**Citation:** D4-prompt-eval -- "Workflow should come before detailed agent design." ordering-guide.md -- "Agent prompt: Role -> Purpose -> Constraints -> Workflow -> Output."

**Token delta:** ~0t (reordering only).

---

## Strengthen

### 1. Eliminate vague terms (D4-prompt-eval CLR-2, MUST_NOT violation)

| Before | After | Citation |
|--------|-------|----------|
| "promising" (line 148) | "rated PROMISING in survey report (compatibility confirmed, recent activity)" | D4 CLR-2 |
| "relevance threshold" (line 149) | "relevance: mentioned in 2+ survey reports OR directly addresses a stakeholder need" | D4 CLR-2 |
| "high-confidence recommendation" (line 153) | "recommendation backed by a Tier 3 verification report with primary source citations" | D4 CLR-2 |
| "extraordinary claim" (line 150) | "claim contradicting 2+ other reports OR asserting capability without primary source evidence" | D4 CLR-2 |
| "sufficient coverage" (line 143) | "all need-categories have survey reports and all PROMISING candidates have verification reports" | D4 CLR-2 |

**Token delta:** ~+50t.

### 2. Convert negative constructions to positive (D3-strunk R11)

| Before | After |
|--------|-------|
| "Don't stop at the provided list." | "Search beyond the provided list." |
| "Don't trust claims without primary-source verification." | "Verify all claims against primary sources." |
| "Don't conflate similarly-named entities." | "Distinguish similarly-named entities by exact names, URLs, identifiers." |
| "Don't make strategic recommendations." | "Report findings with evidence. Leave strategic recommendations to the synthesis agent." |
| "No unresolved contradictions" (completion criteria) | "All contradictions resolved" |
| "Do not read full reports unless arbitration is needed." | "Read full reports only when arbitration is needed." |

**Token delta:** ~-15t (positive constructions are slightly shorter).

### 3. Standardize completion criteria parallelism (D3-strunk R15)

**Before:** Mixed construction: "Synthesis report exists" / "is backed by" / "No unresolved" / "has a definitive"

**After:** All active verbs: "Synthesis complete." / "All recommendations backed by verification reports." / "All contradictions resolved." / "Stakeholder's question answered definitively with grounded evidence."

**Token delta:** ~0t.

### 4. Strengthen emphatic positions (D3-strunk R18)

| Before | After |
|--------|-------|
| "Agents do the looking." | "Agents execute." |
| "the synthesis step handles quality." | "quality emerges in synthesis." |

**Token delta:** ~-5t.

---

## Hook/Command Splits

No hook or command split recommended. Research-tree is judgment-intensive at every step (deciding what enters the next tier, detecting contradictions, choosing verification depth). No deterministic enforcement pattern applies.

---

## Projected Token Delta

| Change | Delta |
|--------|-------|
| Inline agent-templates.md (compressed) | +2,300t |
| Inline report-formats.md (compressed) | +1,700t |
| Inline tier-playbook.md (compressed) | +1,200t |
| Inline anti-patterns.md (compressed) | +1,400t |
| Cut: Tier description redundancy (prose replaced by playbook) | -100t |
| Cut: Session persistence compression | -40t |
| Cut: Domain table API row | -20t |
| Cut: References list (all inlined) | -50t |
| Cut: Philosophy abstraction | -5t |
| Add: Vague term definitions | +50t |
| Add: Emphatic strengthening | -5t |
| Strunk tightening (positive form, parallel) | -15t |
| **Net body change** | **+6,415t** |
| **Eliminated references** | **-8,543t** |
| **Net system change** | **-2,128t** |

**Before:** 11,415t system total (2,872t body + 8,543t in 4 references).
**After:** ~9,287t system total (~9,287t body + 0t references).
**Net reduction:** ~2,128t (18.6%).

The body grows from 2,872t to ~9,287t. This exceeds the 5,000t compaction survival threshold. The first ~5,000t contains Philosophy, Tier System with operational details, Tier Transitions, Orchestration Protocol, Agent Design, and the Prime Directive block -- the operationally critical content survives compaction. The templates (agent prompts + report formats) appear later and may be truncated after compaction, but they are paste-into-prompt infrastructure needed only during active agent dispatch. After compaction the orchestrator re-invokes the skill to re-load the templates if needed.

The body also exceeds the 500-line guideline. Mitigation: the skill governs a 6-tier multi-agent workflow with 8 template types and 6 report formats. This is not bloat -- it is the irreducible operational surface. The alternative (separate reference files) demonstrably fails: models ignore references in practice. The inlined body ensures all content is followed.
