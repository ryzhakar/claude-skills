# Synthesis Report: qa-orchestration

## Baseline

| Component | Tokens |
|-----------|--------|
| SKILL.md body | 2,420 |
| file-protocol.md (referenced) | 4,155 |
| confidence-scoring.md (referenced) | 2,131 |
| failure-heuristics.md (referenced) | 3,915 |
| cicd-workflow.md (referenced) | 5,008 |
| mcp-tools.md (referenced) | 3,261 |
| multi-app-patterns.md (referenced) | 1,293 |
| seed-file-spec.md (referenced) | 1,521 |
| locator-strategy.md (referenced) | 2,583 |
| ten-tier-algorithm.md (referenced) | 4,076 |
| **Total (body + all refs)** | **30,363** |

The orchestrator SKILL.md says "Read ALL of these before Phase 1" and points to 9 reference files via `@references/` links. D1 classified 3 as ESSENTIAL (file-protocol, confidence-scoring, failure-heuristics) and 6 as DEFERRABLE. This distinction is moot: models do not follow reference links. Content not in the body does not get read.

## Core Points (D2 -- untouchable)

1. Five-phase loop (Prerequisites, Plan, Generate, Execute, Heal, Report) with inner Generate-Execute-Heal cycle and four explicit exit conditions.
2. File-based communication: agents write artifacts to disk, orchestrator routes to file paths, never relays or summarizes content.
3. Confidence scoring: seven-signal weighted algorithm with hard rejection at 0.0 for assertion failures, runtime errors, console fatal, mass clusters, zero-candidate. Routes to auto-merge (>=0.85), review (0.60-0.84), reject (<0.60).
4. Six-category failure taxonomy (locator 28%, timing 30%, data 14%, visual 10%, interaction 10%, other 8%) with regex classification. Only locator failures healable. Assertion failures strictly forbidden from healing.
5. Ten-tier deterministic locator discovery with per-tier 1500ms timeout, <1s resolution at tiers 1-3, zero LLM cost.

## INLINED Content

### From file-protocol.md (4,155t) into orchestrator body

**What to inline:** Artifact map (22 artifacts: path, producer, consumer), directory structure, orchestrator-status.json schema (DONE/NEEDS_CONTEXT/BLOCKED), phase marker format, healed output schema, naming conventions.

**Compression:** Remove 4 per-agent read/write matrices (each agent gets its own in its body). Remove verbose JSON examples for session-report, healing-results, verification evidence templates (condense to field lists). Remove progress tracking checkbox examples (obvious). Remove failure classification format (duplicated; executor has it). Collapse directory tree to compact list. Remove "Core Rule" prose (already stated in body line 20).

**Compressed form (~600t):** Artifact map as compact table (path, producer, consumer -- format obvious from extension). Directory tree as flat path list. Status schema one-liner per value. Healed output field list.

**Net:** 4,155t reference -> ~600t inlined. **Saves ~3,555t.**

### From confidence-scoring.md (2,131t) into orchestrator body

**What to inline:** Hard rejection rules (5 scenarios -> score 0.0), decision thresholds table (4 tiers), scoring algorithm signal list with weights.

**Compression:** Remove "Typical Score Scenarios" (4 worked examples -- thresholds table sufficient). Remove element similarity scoring detail (Similo 14-property weights -- healer needs this, not orchestrator). Remove flaky test detection (executor handles). Remove cluster analysis table (subsumed by hard rejection for 10+ concurrent). Remove "Application in the Healer Workflow" (healer has own copy).

**Compressed form (~450t):** Hard rejection list (5 items, one line each). Thresholds table (4 rows). Scoring signals numbered with max weights. Tier adjustment one-liner.

**Net:** 2,131t reference -> ~450t inlined. **Saves ~1,681t.**

### From failure-heuristics.md (3,915t) into orchestrator body

**What to inline:** Six-category taxonomy with regex patterns and healability flags. Decision tree for Phase 3 routing.

**Compression:** Remove detailed "Common messages" tables per category (regex patterns sufficient). Remove false positive scenarios (healer concern). Remove classification confidence table (healer concern). Remove flaky vs broken vs real bug table (executor handles). Remove cross-browser failure flags (executor handles). Remove output schema (executor has it).

**Compressed form (~500t):** Six categories as compact table (name, regex, %, healable?). Decision tree as indented text.

**Net:** 3,915t reference -> ~500t inlined. **Saves ~3,415t.**

### From cicd-workflow.md (5,008t) into orchestrator body

**What to inline:** Circuit breaker schema (healing-state.json structure + 3 rules). PR routing (HIGH/MEDIUM/LOW actions). Cost model.

**Compression:** Remove entire GitHub Actions YAML (~400 lines -- CI implementation, not orchestration). Remove job dependency chain. Remove production deployment checklist. Remove trace parsing note.

**Compressed form (~300t):** Circuit breaker JSON schema + 3 rules. PR routing 3 bullets. Cost model 2 rows.

**Net:** 5,008t reference -> ~300t inlined. **Saves ~4,708t.**

### From mcp-tools.md (3,261t) -- NOT inlined into orchestrator

**Rationale:** Orchestrator does not use MCP tools. MCP content belongs in planner-agent and generator-agent bodies.

**Disposition:** Inline compressed into planner-agent and generator-agent. **Zero tokens added to orchestrator.**

### From multi-app-patterns.md (1,293t) into orchestrator body

**What to inline:** Phase adaptations (per-app artifacts, dual-context fixtures, comparison-as-findings, finding taxonomy).

**Compression:** Remove TypeScript fixture code (generator gets it). Remove comparison test code (generator gets it). Remove auth section (planner/generator concern).

**Compressed form (~200t):** Four phase adaptation bullets. Finding taxonomy 4-row table.

**Net:** 1,293t reference -> ~200t inlined. **Saves ~1,093t.**

### From seed-file-spec.md (1,521t) -- NOT inlined into orchestrator

**Rationale:** Orchestrator only checks "does tests/seed.spec.ts exist and pass?" Template, quality attributes, anti-pattern seed, few-shot guidance belong in generator-agent.

**Disposition:** Inline compressed into generator-agent. **Zero tokens added to orchestrator.**

### From locator-strategy.md (2,583t) -- NOT inlined into orchestrator

**Rationale:** Orchestrator does not select locators. Content belongs in planner/generator/healer bodies.

**Disposition:** Inline compressed into planner-agent, generator-agent, healer-agent. **Zero tokens added to orchestrator.**

### From ten-tier-algorithm.md (4,076t) -- NOT inlined into orchestrator

**Rationale:** Orchestrator does not execute the ten-tier algorithm. Healer execution logic.

**Disposition:** Inline compressed into healer-agent. **Zero tokens added to orchestrator.**

## Cut

| Item | Location | Rationale | Tokens |
|------|----------|-----------|--------|
| "## References -- Hard Requirement" section | Lines 42-49 | Replaced by inlined content. No "read these files" directives remain. | ~120 |
| "Read ALL of these before Phase 1." | Line 42 | Content is in the body. | ~15 |
| "See @references/cicd-workflow.md for PR creation implementation" | Line 152 | PR routing now inlined. | ~15 |
| "See @references/confidence-scoring.md for threshold details" | Line 152 | Thresholds now inlined. | ~12 |
| "see @references/seed-file-spec.md for the template" | Line 81 | Generator owns seed spec. | ~10 |
| Redundant dependency prose about parent framework | Lines 18-28 | D3 flagged wordy (R13). Compress to terse list. | ~200 |
| "They contain the operational details summarized below." | Line 43 | D3 R13: needless. | ~10 |
| "-- it provides false confidence" | Line 125 | D3 R13: "hollow pass" implies this. | ~5 |

**Total cut: ~387t**

## Restructure

1. **Merge "## Dependencies" and inlined artifact map** into "## System Architecture": parent framework summary (compressed), four agents with model assignments, artifact map table, directory structure.

2. **Quality gates before the loop** -- correct position, preserve.

3. **Inline failure taxonomy after Phase 3 heading**, before failure routing bullets. Orchestrator branching at Phase 3 depends on six-category knowledge. Place compressed taxonomy table + decision tree here.

4. **Inline confidence scoring + circuit breaker after Phase 4 heading**, before dispatch rules. Routing at Phase 4 depends on thresholds + circuit breaker rules.

5. **Inline multi-app patterns as conditional subsection** after prerequisites: "If multiple base URLs detected" with compressed phase adaptations.

6. **Remove entire "## References" section.** All load-bearing content in body.

7. **D3 Strunk fixes:**
   - "Base URL known" -> "Check the base URL" (R10 active voice, severe).
   - "Seed file exists" -> "Check tests/seed.spec.ts exists" (R10).
   - "After all healer results are collected" -> "After collecting all healer results" (R10).
   - "Do not retry a failed phase more than once" -> "Retry a failed phase once, then stop" (R11 positive form).
   - "Only non-healable failures remain" -> "Only structural failures remain" (clarity).

8. **D4 prompt-eval fixes:**
   - Add session-report.md template structure to Phase 5 (OUT-1).
   - Expand error handling: reference file missing, circuit breaker corrupt, status.json missing post-dispatch, phase.txt desync (SAF-6).
   - Add output exclusions for user-facing summary (OUT-6).

## Strengthen

| Fix | Source | Description |
|-----|--------|-------------|
| Replace vague "planner completeness" | D4 vague terms | Parenthetical: "planner completeness (all 5 artifacts exist)" |
| Replace "substantive data" | D4 vague terms | "non-placeholder values (not 'TODO', 'needs implementation', empty strings)" |
| Consolidate scattered constraints | D4 CON-6 | Group: retry limit, PR budget, phase.txt preservation, no direct test file editing |
| Add uncertainty handling | D4 RSN-3 | "If exit condition ambiguous (hollow passes): re-enter at GENERATE. If status contradicts: surface to user." |

## Hook/Command Splits

No hooks or commands for this unit. Orchestrator logic is prompt-based dispatch. Circuit breaker state update could theoretically be a PostToolUse hook on Write matching `.playwright/healed/*.json`, but JSON parsing complexity exceeds hook utility. **Keep as prompt logic.**

## Surviving References

**ALL 9 references fail the three-condition survival test for the orchestrator:**

| Reference | Rare? | >1000t compressed? | Gate unskippable? | Verdict |
|-----------|-------|--------------------|--------------------|---------|
| file-protocol.md | NO | NO (~600t) | NO | INLINE |
| confidence-scoring.md | NO | NO (~450t) | NO | INLINE |
| failure-heuristics.md | NO | NO (~500t) | NO | INLINE |
| cicd-workflow.md | NO | NO (~300t) | NO | INLINE |
| mcp-tools.md | N/A | N/A | N/A | To agents |
| multi-app-patterns.md | YES | NO (~200t) | NO | INLINE |
| seed-file-spec.md | N/A | N/A | N/A | To generator |
| locator-strategy.md | N/A | N/A | N/A | To agents |
| ten-tier-algorithm.md | N/A | N/A | N/A | To healer |

**Zero surviving references.** The reference files remain on disk for human readers, but no unit body points to them with "read this file" directives. Every unit is self-contained.

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| Orchestrator body | 2,420 | ~3,700 | +1,280 |
| file-protocol.md (runtime load) | 4,155 | 0 | -4,155 |
| confidence-scoring.md (runtime load) | 2,131 | 0 | -2,131 |
| failure-heuristics.md (runtime load) | 3,915 | 0 | -3,915 |
| cicd-workflow.md (runtime load) | 5,008 | 0 | -5,008 |
| multi-app-patterns.md (runtime load) | 1,293 | 0 | -1,293 |
| mcp-tools.md (orchestrator share) | 3,261 | 0 | -3,261 |
| seed-file-spec.md (orchestrator share) | 1,521 | 0 | -1,521 |
| locator-strategy.md (orchestrator share) | 2,583 | 0 | -2,583 |
| ten-tier-algorithm.md (orchestrator share) | 4,076 | 0 | -4,076 |
| **Total at orchestrator runtime** | **30,363** | **~3,700** | **-26,663 (-87.8%)** |

The previous architecture assumed models read 9 files on command. They did not. Self-contained body eliminates that failure mode. Some content redistributes to agent bodies (not a system increase -- a move from "files nobody reads" to "bodies that execute"). Cross-unit duplication (confidence thresholds in orchestrator AND healer) is acceptable for self-containment.
