# Synthesis Report: executor-agent

## Baseline

| Component | Tokens |
|-----------|--------|
| Agent body | 1,035 |
| file-protocol.md (referenced) | 4,155 |
| failure-heuristics.md (referenced) | 3,915 |
| **Total (body + refs)** | **9,105** |

Body references 2 files: "Read these files from disk before proceeding." The executor already has the core classification regex patterns inlined (lines 53-58) but points to failure-heuristics.md for "classification decision tree, regex patterns, flaky taxonomy" and file-protocol.md for "artifact schemas and output format." The inline regex is a partial duplicate -- the reference adds decision trees, false positive scenarios, flaky taxonomy, cross-browser patterns, and output schemas.

## Core Points (D2 -- untouchable)

1. **CLI-exclusive execution** -- MCP has no test execution capability; all runs via `npx playwright test`.
2. **Healable count = locator only** -- timing failures are NOT healable; exclude from healable_count.
3. **Seed health check gate** -- seed must pass before suite runs; NEEDS_CONTEXT if broken.
4. **Flaky detection excludes healing** -- retry with --retries=2; flaky=true tests skip locator healing.
5. **Cross-browser pattern analysis** -- single-browser failure = browser-specific issue; all-browser = real bug.

## INLINED Content

### From file-protocol.md (4,155t) into executor body

**What to inline:** Executor-specific output schemas (.ai-failures.json structure, results.json expectations). Executor read/write matrix. Output artifact paths (results.json at project root, .ai-failures.json at project root, test-results/ traces, playwright-report/).

**Compression:** Remove all non-executor artifacts (planner, generator, healer, orchestrator). Remove directory structure tree (executor writes to known paths). Remove all template examples (session-report, healing-results, verification evidence, test-plan -- not executor outputs). Remove naming conventions (executor reads tests, does not create them). Keep: .ai-failures.json full schema with one failure entry example. Output path list.

**Compressed form (~250t):** .ai-failures.json schema with summary + per-category arrays + one example entry. 4 output paths.

**Net:** 4,155t reference -> ~250t executor-specific. **Saves ~3,905t.**

### From failure-heuristics.md (3,915t) into executor body

**What to inline:** Decision tree for classification (the executor must verify locator failures are genuine, not reclassified as data/assertion/infrastructure). Flaky vs broken vs real bug discrimination table. Cross-browser failure flags with known browser-specific patterns (WebKit list role, Firefox caption/alert/combobox/form name filters). Output schema for .ai-failures.json failure entries.

**Compression:** Remove false positive scenarios section (healer concern -- executor classifies, healer validates). Remove classification confidence table (healer concern). Remove common error messages classification table (executor already has regex patterns inline). Remove the six-category taxonomy section header material (executor already has this at lines 53-58 -- only add what is missing). Keep: decision tree as compact indented text. Flaky taxonomy as compact table. Browser-specific patterns as 5-row table. Note on `browser_specific: true` flag.

Body already contains the regex patterns (lines 53-58). The inlined content supplements, not duplicates: decision tree for reclassification, flaky taxonomy, browser-specific patterns.

**Compressed form (~400t):** Decision tree (3 reclassification checks). Flaky taxonomy 5-row table (category, %, fix, heal?). Browser-specific patterns 5-row table (browser, locator, problem, workaround).

**Net:** 3,915t reference -> ~400t inlined (non-duplicating supplement). **Saves ~3,515t.**

## Cut

| Item | Location | Rationale | Tokens |
|------|----------|-----------|--------|
| "## References" section | Lines 101-105 | Replaced by inlined content. | ~55 |
| "Read these files from disk before proceeding:" | Line 102 | Content is in body. | ~10 |
| "@references/file-protocol.md -- artifact schemas and output format" | Line 103 | Schemas now inlined. | ~12 |
| "@references/failure-heuristics.md -- classification decision tree, regex patterns, flaky taxonomy" | Line 104 | Decision tree + taxonomy now inlined. | ~15 |

**Total cut: ~92t**

## Restructure

1. **Inline decision tree after "## Failure Classification"** section, after the regex patterns. The executor classifies by regex first, then must verify via decision tree (reclassify assertion failures that look like locator failures, check console errors, check cluster size).

2. **Inline flaky taxonomy after "## Flaky Detection"** section. Executor detects flaky tests and must know the five categories and their correct responses.

3. **Inline browser-specific patterns after "## Cross-Browser Analysis"** section. Executor flags browser_specific and needs the known problem patterns.

4. **Inline .ai-failures.json full schema after "## Outputs"** section. Executor writes this file and needs the complete structure.

5. **Remove "## References" section.**

6. **Clarify workflow sequence** (D4 W6): Renumber as explicit steps: "1. Run full suite. 2. Read results.json. 3. Classify failures by regex. 4. Verify classifications via decision tree. 5. Re-run failures with --retries=2. 6. Update flaky flags. 7. Write .ai-failures.json. 8. Write status file."

7. **D3 Strunk fixes:**
   - "Timing failures are NOT healable. Do not include timing in healable_count." -> "Only locator failures are healable. Exclude timing from healable_count." (R11 positive form, severe).
   - Pre-flight step 5 parallel structure: "Check dev server if..." -> "Check dev server (if playwright.config.ts lacks webServer):" (R15).

8. **D4 prompt-eval fixes:**
   - Add scope boundary: "You do NOT: generate tests, fix locators, create PRs, modify test code" (CON-1).
   - "Install browsers: ... (if needed)" -> "Install browsers if ~/.cache/ms-playwright/ is empty" (CLR-2).
   - "Flag with browser_specific: true when applicable" -> "Flag browser_specific: true when failure occurs in exactly one browser project but passes in others" (CLR-2).

## Strengthen

| Fix | Source | Description |
|-----|--------|-------------|
| Add scope boundary | D4 W1 | "You do NOT: generate tests, fix locators, modify test code, create PRs" |
| Define "if needed" | D4 W2 | Replace with detection logic for browser installation |
| Explicit workflow sequence | D4 W6 | 8-step numbered list replacing implicit sequence |
| Precise browser_specific flag | D4 W5 | "exactly one browser project fails, others pass" |
| Add NEEDS_CONTEXT example | D4 W6 | Show status JSON when seed fails |

## Hook/Command Splits

No hooks. Executor is a subagent dispatched by orchestrator. All logic is classification and reporting -- prompt-based judgment on error messages.

The seed health check (step 4 of pre-flight) could be a SessionStart hook for the orchestrator, but the executor runs it as part of its own pre-flight, not as a standalone gate. **Keep as prompt logic.**

## Surviving References

**Both references fail the three-condition survival test:**

| Reference | Rare? | >1000t compressed? | Gate unskippable? | Verdict |
|-----------|-------|--------------------|--------------------|---------|
| file-protocol.md | NO | NO (~250t) | NO | INLINE executor portion |
| failure-heuristics.md | NO | NO (~400t) | NO | INLINE executor portion |

**Zero surviving references.** Executor body is self-contained.

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| Executor body | 1,035 | ~1,750 | +715 |
| file-protocol.md (runtime load) | 4,155 | 0 | -4,155 |
| failure-heuristics.md (runtime load) | 3,915 | 0 | -3,915 |
| **Total at executor runtime** | **9,105** | **~1,750** | **-7,355 (-80.8%)** |

The executor was the leanest agent body but referenced the largest combined content. Self-contained body absorbs only what the executor needs: output schemas, decision tree, flaky taxonomy, browser patterns. No cross-agent content included.
