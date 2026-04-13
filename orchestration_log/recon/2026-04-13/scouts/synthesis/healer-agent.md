# Synthesis Report: healer-agent

## Baseline

| Component | Tokens |
|-----------|--------|
| Agent body | 1,494 |
| ten-tier-algorithm.md (referenced) | 4,076 |
| confidence-scoring.md (referenced) | 2,131 |
| failure-heuristics.md (referenced) | 3,915 |
| file-protocol.md (referenced) | 4,155 |
| locator-strategy.md (referenced) | 2,583 |
| **Total (body + refs)** | **18,354** |

Healer references 5 files -- the most of any agent. Body says "Read these files from disk before proceeding" (line 164). The healer's entire operational algorithm (ten-tier discovery, confidence scoring, failure classification validation) lives in external files. Without them, the agent has thresholds and iron law but no algorithm to execute. This is the unit most damaged by reference non-reading.

## Core Points (D2 -- untouchable)

1. **Iron Law (no assertion healing)** -- element found + wrong value = application bug; score 0.0 and skip.
2. **Deterministic ten-tier + confidence thresholds** -- tiers 1-3 HIGH (2-5% FP), 4-6 MEDIUM (5-10%), 7-10 LOW (10-15%); apply fixes only at >= 0.60.
3. **Mandatory DOM verification for tiers 7+** -- verify proposed locator exists in live DOM via playwright-cli before applying. Mandatory when all tiers return null.
4. **Cross-cycle lessons feedback** -- read .playwright/lessons.md before starting; append discoveries after healing. Prevents repeating failed selectors.
5. **Circuit breaker (read-only, 2 attempts max)** -- max 2 healing attempts per test from .github/healing-state.json; orchestrator updates after aggregation.

## INLINED Content

### From ten-tier-algorithm.md (4,076t) into healer body

**What to inline:** Tier priority table (10 tiers with strategy, example, confidence band). ElementPattern interface. DOMExtractor algorithm logic (tier cascade). SmartFind self-healing wrapper concept. Selector encoding format. "How the Healer Uses This Algorithm" section.

**Compression:** Remove full TypeScript implementation of LocatorCache (cache persistence -- implementation detail, not instruction). Remove full TypeScript implementation of SmartFind.click(), SmartFind.fill(), SmartFind.isVisible(), SmartFind.text() (convenience methods the healer does not need instruction for -- it edits test files, it does not use SmartFind at runtime). Remove SmartFind.dismissOverlays() (implementation detail). Remove full DOMExtractor TypeScript implementation -- replace with pseudocode summary (the healer applies the algorithm conceptually, not by running this TypeScript). Keep: tier table (compact). ElementPattern as field list. Algorithm as pseudocode (try each tier in order, 1500ms timeout, first match wins). Selector encoding format (role::, text::, CSS). "How healer uses" 4-step summary.

**Compressed form (~500t):** Tier table (10 rows, 4 columns: tier, strategy, example, confidence). ElementPattern fields. Pseudocode cascade. Encoding format. 4-step usage.

**Net:** 4,076t reference -> ~500t inlined. **Saves ~3,576t.**

### From confidence-scoring.md (2,131t) into healer body

**What to inline:** Hard rejection rules (5 scenarios). Scoring algorithm (7 signals with weights). Decision thresholds (4 tiers). Element similarity scoring (Similo 14-property weights). Flaky test exclusion rule.

**Compression:** Body already has thresholds (lines 82-88) and hard rejection (lines 61-67) -- deduplicate. Remove "Typical Score Scenarios" (4 worked examples -- thresholds sufficient). Remove "Application in the Healer Workflow" section (healer IS the workflow). Remove cluster analysis table (subsumed by hard rejection for 10+). Keep: scoring algorithm as signal list with max weights (compress from prose to numbered list). Element similarity scoring compressed to weighted property list. Flaky exclusion as one-liner.

**Compressed form (~350t):** Scoring signals (7 items with weights, deduplicated with existing body). Element similarity (14 properties with weights, compressed to table). Flaky exclusion one-liner.

**Net:** 2,131t reference -> ~350t inlined (after deduplication with existing body). **Saves ~1,781t.**

### From failure-heuristics.md (3,915t) into healer body

**What to inline:** The healer needs the decision tree for VALIDATING that a failure is truly a locator issue (reclassification check). False positive scenarios (healer must watch for these). "Flaky vs broken vs real bug" discrimination table.

**Compression:** Remove six-category taxonomy (executor handles classification; healer receives already-classified .ai-failures.json). Remove regex patterns (executor concern). Remove classification algorithm (executor concern). Remove output schema (executor concern). Remove cross-browser failure flags (executor concern). Keep: reclassification decision tree (3 checks: assertion masquerading as locator? Console errors? Cluster size?). False positive scenarios (5 scenarios compressed to 1-line each). Flaky vs broken vs real bug discrimination (3-column summary).

**Compressed form (~300t):** 3 reclassification checks. 5 false positive scenarios (1-line each). Discrimination table (3 rows: flaky/bug/broken locator with signals and action).

**Net:** 3,915t reference -> ~300t healer-specific. **Saves ~3,615t.**

### From file-protocol.md (4,155t) into healer body

**What to inline:** Healer read/write matrix. Output artifact paths and schemas (.playwright/healed/{test-name}.json, .healing-results.json, .github/healing-state.json). Circuit breaker state schema.

**Compression:** Remove all non-healer artifacts. Remove directory structure. Remove naming conventions. Remove template examples for planner/executor/orchestrator outputs. Body already has healed output schema (lines 137-149) and status file (lines 151-162) -- deduplicate. Keep: healer reads list (5 items). Healer writes list (4 items). Circuit breaker schema (compact JSON).

**Compressed form (~150t):** Read list. Write list. Circuit breaker JSON schema (already partially in body at lines 52-58, deduplicate).

**Net:** 4,155t reference -> ~150t healer-specific. **Saves ~4,005t.**

### From locator-strategy.md (2,583t) into healer body

**What to inline:** Safe role list (which roles are reliable for getByRole). Risky locator table (caption, list, form, alert, combobox -- which to avoid or use without name). Cross-browser safety matrix. Shadow DOM handling pattern. Fallback .or() pattern.

**Compression:** Remove locator decision tree (generator concern -- healer repairs existing locators, does not write new tests from scratch). Remove locator priority for generated tests (generator concern). Remove assertions section (executor/generator concern). Remove WASM/Leptos section (generator concern). Keep: safe roles one-liner. Risky locators 5-row table. Cross-browser matrix compressed. Shadow DOM 2-liner. Fallback pattern.

**Compressed form (~250t):** Safe roles. Risky locators table. Cross-browser compressed. Shadow DOM + fallback.

**Net:** 2,583t reference -> ~250t healer-specific. **Saves ~2,333t.**

## Cut

| Item | Location | Rationale | Tokens |
|------|----------|-----------|--------|
| "## References" section | Lines 164-172 | Replaced by inlined content. | ~70 |
| "Read these files from disk before proceeding:" | Line 165 | Content is in body. | ~10 |
| All 5 @references/ lines | Lines 166-171 | Content inlined. | ~40 |
| "Apply from @references/ten-tier-algorithm.md" | Line 71 | Algorithm now inlined. | ~8 |
| "Apply Similo-based scoring from @references/confidence-scoring.md" | Line 81 | Scoring now inlined. | ~10 |
| Threshold duplication between body and confidence-scoring inline | Lines 82-88 | Merge: keep one copy in "Confidence Scoring" section. | ~60 |
| Hard rejection duplication between body and confidence-scoring inline | Lines 61-67 | Merge: keep one copy in "Hard Rejection" section. | ~50 |

**Total cut: ~248t**

## Restructure

1. **Create "## Ten-Tier Algorithm" section** with inlined tier table, ElementPattern fields, pseudocode cascade, selector encoding. Place after "Hard Rejection" section, before "Confidence Scoring". The healer must know the algorithm before scoring results.

2. **Expand "## Confidence Scoring"** section with inlined scoring signals (7 items with weights) and element similarity scoring. Merge existing thresholds (lines 82-88) with inlined content. Deduplicate.

3. **Create "## Failure Validation" section** with inlined reclassification checks, false positive scenarios, and flaky/broken/locator discrimination. Place after Iron Law, before Ten-Tier Algorithm. Healer must validate classification before attempting repair.

4. **Create "## Locator Safety" section** with safe roles, risky locators, cross-browser matrix, shadow DOM, fallback pattern. Place after Ten-Tier Algorithm. Healer uses this when proposing replacement locators.

5. **Inline artifact protocol into "## Output"** section: read list, write list, circuit breaker schema. Merge with existing output schemas (lines 137-162). Deduplicate.

6. **Remove all @references/ directives.**

7. **D3 Strunk fixes:**
   - "Never touch assertion failures or runtime errors" -> "Process only locator failures, skipping assertion and runtime errors" (R11 positive form, moderate).
   - DOM Re-Discovery steps: standardize format (R15 parallel -- steps mix bare commands with full sentences).
   - "If `.playwright/lessons.md` exists, read it before starting" -> "Read .playwright/lessons.md if present before starting" (R13 tighter).

8. **D4 prompt-eval fixes:**
   - Add assertion failure detection criteria: "Detection: error contains expect(, toBe, toHaveText, toContain, toEqual" (CLR-2).
   - "all tiers return null" -> "all tiers yield no candidate locators (empty result sets)" (CLR-2).
   - "10+ concurrent test failures" -> "10+ failures in the same test run (same results.json batch)" (CLR-2).
   - Use mathematical intervals for thresholds: [0.85, 1.0], [0.60, 0.85), [0.40, 0.60), [0.0, 0.40) (CLR-3).
   - "recommended but not required" for tiers 1-6 -> "optional (confidence scores account for verification absence)" (CON-2).
   - Add flaky test handling: "If test flagged flaky:true in .ai-failures.json, skip (mark deferred)" (SAF-6).
   - Clarify LLM fallback: "When all tiers empty: LLM analyzes error + DOM to propose locator. Max confidence: MEDIUM. Never auto-apply." (CLR-1).

## Strengthen

| Fix | Source | Description |
|-----|--------|-------------|
| Assertion detection criteria | D4 W1 | Regex for identifying assertion vs locator failures |
| Define "null" precisely | D4 W2 | "no candidate locators at any tier" |
| Define "concurrent" | D4 W5 | "in the same test run batch" |
| Mathematical intervals | D4 W6 | [0.85, 1.0], [0.60, 0.85), etc. |
| Flaky handling | D4 W8 | "flaky:true -> skip, mark deferred" |
| LLM fallback clarity | D4 W10 | "max confidence MEDIUM, never auto-apply" |
| Circuit breaker schema | D4 W4 | Show healing-state.json structure |

## Hook/Command Splits

No hooks. Healer is a subagent dispatched by orchestrator. Its logic is algorithmic locator repair -- requires DOM access and judgment.

The "never heal assertion failures" Iron Law could theoretically be enforced by a PreToolUse hook on Edit tool matching `tests/*.spec.ts` files, checking if the edited line contains assertion-related code (expect, toBe, toHaveText). But this would require parsing test file context to distinguish locator edits from assertion edits -- too complex for a hook. **Keep as prompt logic.**

## Surviving References

**ALL 5 references fail the three-condition survival test:**

| Reference | Rare? | >1000t compressed? | Gate unskippable? | Verdict |
|-----------|-------|--------------------|--------------------|---------|
| ten-tier-algorithm.md | NO | NO (~500t) | NO | INLINE healer portion |
| confidence-scoring.md | NO | NO (~350t) | NO | INLINE healer portion |
| failure-heuristics.md | NO | NO (~300t) | NO | INLINE healer portion |
| file-protocol.md | NO | NO (~150t) | NO | INLINE healer portion |
| locator-strategy.md | NO | NO (~250t) | NO | INLINE healer portion |

**Zero surviving references.** Healer body is self-contained.

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| Healer body | 1,494 | ~2,800 | +1,306 |
| ten-tier-algorithm.md (runtime load) | 4,076 | 0 | -4,076 |
| confidence-scoring.md (runtime load) | 2,131 | 0 | -2,131 |
| failure-heuristics.md (runtime load) | 3,915 | 0 | -3,915 |
| file-protocol.md (runtime load) | 4,155 | 0 | -4,155 |
| locator-strategy.md (runtime load) | 2,583 | 0 | -2,583 |
| **Total at healer runtime** | **18,354** | **~2,800** | **-15,554 (-84.7%)** |

The healer was the most reference-dependent agent (5 files, 16,860t of references vs 1,494t body -- a 11:1 reference-to-body ratio). Every reference contained content the healer needs at execution time: the algorithm it runs, the scoring it computes, the validation it performs, the locator safety it applies, the artifacts it reads/writes. The previous architecture placed ALL operational knowledge in files the model never read. Self-contained body fixes this completely.

Cross-unit duplication: confidence thresholds appear in orchestrator AND healer. Failure validation checks appear in executor AND healer. Locator safety appears in planner AND generator AND healer. This duplication is the cost of self-containment. The alternative (shared references) produced units that operated without their own algorithms.
