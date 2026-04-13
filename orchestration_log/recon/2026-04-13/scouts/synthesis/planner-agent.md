# Synthesis Report: planner-agent

## Baseline

| Component | Tokens |
|-----------|--------|
| Agent body | 1,566 |
| file-protocol.md (referenced) | 4,155 |
| mcp-tools.md (referenced) | 3,261 |
| locator-strategy.md (referenced) | 2,583 |
| seed-file-spec.md (referenced) | 1,521 |
| **Total (body + refs)** | **13,086** |

Body references 4 files at bottom: "Read these files from disk before proceeding." Models do not follow these directives. The planner-agent operates without its own locator strategy, MCP tool reference, artifact schemas, or seed spec knowledge.

## Core Points (D2 -- untouchable)

1. **Live exploration mandate (Iron Law)** -- every plan traces to browser observation; unvisited pages cannot appear in plan.
2. **CLI-over-MCP default** -- playwright-cli at ~50 tokens/command vs MCP ~4,000; unlimited session length.
3. **Orchestrator status protocol** -- status file (DONE/NEEDS_CONTEXT/BLOCKED) with artifacts array enables multi-phase pipeline.
4. **DOM quality scoring** -- quantitative 0-100 rubric rewarding semantic HTML, penalizing clickable divs; scores to .playwright/pages.md.
5. **MCP security gate** -- CVE-2025-9611 version check >= 0.0.40, hard stop if vulnerable.

## INLINED Content

### From file-protocol.md (4,155t) into planner body

**What to inline:** Planner-specific artifact schemas (test-plan.md template, pages.md template, selector-strategy.md template, project-config.md template, VERIFICATION.md template). Planner read/write matrix. Naming conventions for test files/page objects/fixtures/seed.

**Compression:** Remove all non-planner artifacts from the map (executor, healer, orchestrator artifacts irrelevant). Remove per-agent read/write matrices for other agents. Remove JSON examples for orchestrator-status (already in body), healing-results, session-report. Remove directory structure (planner creates .playwright/ subdirectory, path is obvious). Keep templates but compress to field lists, not full markdown blocks.

**Compressed form (~350t):** 5 output artifact field lists. Planner reads list. Naming conventions as 4-line compact list.

**Net:** 4,155t reference -> ~350t planner-specific. **Saves ~3,805t.**

### From mcp-tools.md (3,261t) into planner body

**What to inline:** CLI vs MCP decision tree. @playwright/cli key commands (session management, page inspection, element interaction). MCP core tools (browser_navigate, browser_snapshot, browser_click, browser_type, browser_fill_form). Version requirement + CVE check.

**Compression:** Remove standard `npx playwright` commands (executor handles test execution). Remove all optional capability sets (storage, network, devtools, vision, PDF, config -- planner never uses them). Remove MCP advanced tools (browser_evaluate, browser_run_code, browser_drag, browser_file_upload, browser_handle_dialog, browser_resize -- planner explores, does not test). Remove "Common Incorrect Tool Names" table (low value). Remove architecture priority section (already stated in body as CLI default). Collapse CLI commands to essential 6 (open, goto, snapshot, click, fill, close-all). Collapse MCP tools to essential 4 (navigate, snapshot, click, fill_form).

**Compressed form (~400t):** Decision tree as 3-line rule. CLI 6 commands with syntax. MCP 4 tools with parameters. CVE check (already in body, deduplicate).

**Net:** 3,261t reference -> ~400t inlined (minus CVE duplication). **Saves ~2,861t.**

### From locator-strategy.md (2,583t) into planner body

**What to inline:** Locator decision tree (8 steps). Safe role list (button, link, textbox, checkbox, radio, heading, img). Risky locator table (caption, list, form, alert, combobox). Shadow DOM detection + parent-component-first chaining. WASM/Leptos wait strategy.

**Compression:** Remove ten-tier hierarchy table (healer concern). Remove fallback patterns code examples (generator concern). Remove locator priority for generated tests (generator concern). Remove assertions section (generator/executor concern). Remove cross-browser testing configuration (executor concern). Keep decision tree compressed. Keep risky locator table compressed. Keep shadow DOM as 2-line pattern. WASM note already in body (line 171-173), deduplicate.

**Compressed form (~350t):** Decision tree as 8-step compact list. Safe roles one-liner. Risky locators as 5-row table (role, browser, workaround). Shadow DOM 2-liner.

**Net:** 2,583t reference -> ~350t inlined. **Saves ~2,233t.**

### From seed-file-spec.md (1,521t) into planner body

**What to inline:** Seed file location (tests/seed.spec.ts). Required components (5: import, navigation, interaction, assertion, accessibility-first locators). How planner uses seed (reads to understand fixtures, imports, patterns).

**Compression:** Remove seed file template code (generator concern). Remove anti-pattern seed (generator concern). Remove multi-seed strategy (generator concern). Remove few-shot reference tests section (generator concern). Remove quality attributes checklist (generator concern). Keep only: location, 5 required components as one-liner list, planner usage as single sentence.

**Compressed form (~60t):** Location path + 5 components + usage sentence.

**Net:** 1,521t reference -> ~60t inlined. **Saves ~1,461t.**

## Cut

| Item | Location | Rationale | Tokens |
|------|----------|-----------|--------|
| "## References" section at bottom | Lines 176-182 | Replaced by inlined content. | ~80 |
| "Read these files from disk before proceeding:" | Line 177 | Content is in body. | ~10 |
| Duplicate MCP version check prose | Body has CVE check at lines 67-75 AND mcp-tools.md has same | Deduplicate: keep body version. | ~80 |
| WASM/Leptos section duplication | Body line 171-173 AND locator-strategy.md | Keep body version, skip from locator-strategy inline. | ~40 |
| "Produces structured test planning artifacts from browser exploration" | D3 R12 severe | Replace with concrete: "Produces test plans, selector strategies, DOM quality scores, verification evidence." | ~5 |

**Total cut: ~215t**

## Restructure

1. **Inline locator decision tree after "## 4. Define Selector Strategy"** heading. The planner decides selectors -- it needs the decision tree at this point.

2. **Inline CLI/MCP tool reference after "## Browser Exploration"** sections. Merge the inlined CLI commands into the existing CLI workflow. Merge inlined MCP tools into the existing MCP fallback section.

3. **Inline artifact templates after "## 5. Write Test Plan"** and "## 6. Write Status File." Each output step gets its compressed field list.

4. **Inline seed file usage in "## 1. Verify Prerequisites"** as a single line: "Read tests/seed.spec.ts to learn import patterns, fixture usage, naming conventions."

5. **Remove entire "## References" section.**

6. **D3 Strunk fixes:**
   - "structured test planning artifacts" -> "test plans, selector strategies, DOM quality scores" (R12 concrete, severe).
   - "If you have not visited a page, that page cannot appear in the plan" -> "Only visited pages appear in the plan" (R11 positive form + R13 fewer words).
   - Workflow step 3 format mismatch: standardize to backticked command pattern (R15 parallel).

7. **D4 prompt-eval fixes:**
   - Add "You do NOT: generate test code, execute tests, fix failing tests" scope boundary (CON-1).
   - Define "proper form elements" -> "native HTML input/select/textarea, not contenteditable divs" (CLR-2).
   - Define "ARIA labels work" -> "getByLabel('FieldName') resolves to visible element" (CLR-2).
   - Add MCP 10-interaction limit edge case: "If limit reached, write NEEDS_CONTEXT with blocker" (OUT-3).

## Strengthen

| Fix | Source | Description |
|-----|--------|-------------|
| Add scope boundaries | D4 W5 | "You do NOT: generate tests, execute tests, fix locators" |
| Define quality terms | D4 W2 | "proper form elements: native input/select/textarea"; "clickable divs: elements with onClick that are not button/a/input" |
| Consolidate CLI/MCP decision | D4 W4 | Single decision tree at top: "Default: CLI. Fallback: MCP when Bash unavailable." |
| MCP limit edge case | D4 W7 | "10-interaction limit reached -> NEEDS_CONTEXT status" |

## Hook/Command Splits

No hooks or commands. Planner is a subagent dispatched by the orchestrator. Its logic is inherently exploratory and judgment-based -- not deterministic enough for hooks.

## Surviving References

**ALL 4 references fail the three-condition survival test:**

| Reference | Rare? | >1000t compressed? | Gate unskippable? | Verdict |
|-----------|-------|--------------------|--------------------|---------|
| file-protocol.md | NO | NO (~350t) | NO | INLINE planner portion |
| mcp-tools.md | NO | NO (~400t) | NO | INLINE planner portion |
| locator-strategy.md | NO | NO (~350t) | NO | INLINE planner portion |
| seed-file-spec.md | NO | NO (~60t) | NO | INLINE planner portion |

**Zero surviving references.** Planner body is self-contained.

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| Planner body | 1,566 | ~2,550 | +984 |
| file-protocol.md (runtime load) | 4,155 | 0 | -4,155 |
| mcp-tools.md (runtime load) | 3,261 | 0 | -3,261 |
| locator-strategy.md (runtime load) | 2,583 | 0 | -2,583 |
| seed-file-spec.md (runtime load) | 1,521 | 0 | -1,521 |
| **Total at planner runtime** | **13,086** | **~2,550** | **-10,536 (-80.5%)** |

Self-contained body with all operational knowledge inlined. No reference file reads required. Cross-unit duplication with generator (locator strategy, seed spec) and healer (locator strategy) is acceptable for self-containment.
