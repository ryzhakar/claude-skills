# Synthesis Report: generator-agent

## Baseline

| Component | Tokens |
|-----------|--------|
| Agent body | 2,194 |
| locator-strategy.md (referenced) | 2,583 |
| seed-file-spec.md (referenced) | 1,521 |
| file-protocol.md (referenced) | 4,155 |
| **Total (body + refs)** | **10,453** |

Body references 3 files in pre-flight reads (lines 65-67) plus locator-strategy.md at line 48 (Hard Rule 4). The generator already has substantial inline content: risky locators table (lines 139-143), shadow DOM pattern (lines 148-153), page objects guidance (lines 156-159), test data factory (lines 162-171). It duplicates some locator-strategy.md content but lacks the decision tree and safe role list.

## Core Points (D2 -- untouchable)

1. **Two-mode operation (create/fix)** -- create from plan, fix structural test architecture problems the healer cannot handle.
2. **Mandatory live DOM verification before writing** -- playwright-cli snapshot; 5 documented field failures from unverified selectors.
3. **Strict one-at-a-time with green gate** -- write ONE test, run, fix until green (max 3 edit-run cycles), STOP on failure.
4. **No hollow tests** -- every test has real assertion (expect()); unimplementable -> test.skip with reason, not passing placeholder.
5. **Seed file prerequisite** -- tests/seed.spec.ts must exist and pass before any generation.

## INLINED Content

### From locator-strategy.md (2,583t) into generator body

**What to inline:** Locator decision tree (8-step). Safe role list. Cross-browser safety matrix (risky locators). Fallback patterns (.or() dual-locator). Locator priority for generated tests. Assertions: web-first only. WASM/Leptos navigation pattern.

**Compression:** Body already has risky locators table (lines 139-143) and shadow DOM (lines 148-153) -- deduplicate. Remove ten-tier hierarchy table (healer concern, not generation). Remove cross-browser testing configuration (executor concern). Keep decision tree compressed. Keep safe role list one-liner. Keep assertion rules (web-first only). Keep WASM pattern.

**Compressed form (~350t):** 8-step decision tree (compact). Safe roles: button, link, textbox, checkbox, radio, heading, img. Risky locators already in body (deduplicate, save ~80t). Fallback .or() pattern as 2-line example. Web-first assertions as do/don't list (3 correct, 3 wrong). WASM pattern as 3-line code block.

**Net:** 2,583t reference -> ~350t inlined (after deduplication). **Saves ~2,233t.**

### From seed-file-spec.md (1,521t) into generator body

**What to inline:** Required 5 components of a seed file (import, navigation, interaction, assertion, accessibility-first locators). Seed file template code. Quality attributes checklist. Anti-pattern seed (DO NOT GENERATE example). Few-shot reference tests distinction from seed. How generator uses seed.

**Compression:** Body already has seed prerequisite check (Hard Rule 1, lines 42-43) and pre-flight seed run (lines 70-81). Remove multi-seed strategy (rare, not default workflow). Remove agent usage table (generator only needs its own row). Keep: 5 required components as one-liner list. Keep template code compressed (one good example, ~8 lines). Keep quality attributes as compact checklist. Keep anti-pattern as compressed "avoid these" list (CSS selectors, hardcoded waits, sync assertions). Keep few-shot distinction as 3-line note.

**Compressed form (~300t):** 5 components list. Template (8 lines). Quality checklist (6 items). Anti-patterns (3 items). Few-shot note (3 lines).

**Net:** 1,521t reference -> ~300t inlined. **Saves ~1,221t.**

### From file-protocol.md (4,155t) into generator body

**What to inline:** Generator read/write matrix. Output artifact paths (tests/*.spec.ts, tests/pages/*.page.ts, tests/fixtures.ts, tests/helpers/test-data.ts). Test plan checkbox update protocol. Naming conventions.

**Compression:** Remove all non-generator artifacts. Remove all other agents' read/write matrices. Remove directory structure (generator writes to tests/, path obvious). Remove JSON schema examples. Remove orchestrator-status templates (generator already has them inline at lines 207-226). Keep: read list (4 items). Write list (6 items). Naming conventions (4 lines).

**Compressed form (~150t):** Read list. Write list. Naming conventions.

**Net:** 4,155t reference -> ~150t generator-specific. **Saves ~4,005t.**

## Cut

| Item | Location | Rationale | Tokens |
|------|----------|-----------|--------|
| "## References" equivalent (pre-flight reads section) | Lines 65-67 | Replaced by inlined content. Remove file read directives. | ~40 |
| "@references/locator-strategy.md" at Hard Rule 4 | Line 48 | Decision tree now inlined. | ~8 |
| "@references/seed-file-spec.md" in pre-flight | Line 66 | Seed spec now inlined. | ~8 |
| "@references/file-protocol.md" in pre-flight | Line 67 | Artifact schemas now inlined. | ~8 |
| Risky locators duplication | Lines 139-143 vs locator-strategy inline | Merge: keep one copy in "Locator Safety" section. | ~80 |
| Shadow DOM duplication | Lines 148-153 vs locator-strategy inline | Merge: keep one copy. | ~50 |
| "AND" in caps (line 33) | D3 R13 | Replace with lowercase "and". | ~0 (style) |

**Total cut: ~194t**

## Restructure

1. **Create "## Locator Rules" section** consolidating: decision tree (from locator-strategy.md), safe roles, risky locators (from body lines 139-143), shadow DOM (from body lines 148-153), fallback .or() pattern, web-first assertions. Place after Hard Rules, before Workflow. Generator must know locator rules before writing any test.

2. **Create "## Seed File Spec" section** after Locator Rules: 5 required components, template code, quality attributes, anti-patterns. Replaces the pre-flight file reads.

3. **Inline artifact protocol into "## Completion"** section: what files generator reads, what it writes, naming conventions.

4. **Pre-flight reads become "check these exist"** instead of "read these reference files": check test-plan.md exists, check selector-strategy.md exists, check seed.spec.ts passes. No external file reads.

5. **Remove all @references/ directives.**

6. **D3 Strunk fixes:**
   - "if given a test plan reference, use create mode. If given specific test files" -> "test plan reference triggers create mode; test files + failure descriptions trigger fix mode" (R10 active voice, severe).
   - "If `tests/seed.spec.ts` is missing or failing, STOP... Do not proceed." -> "If tests/seed.spec.ts is missing or fails, STOP... exit." (R11 positive form; remove "Do not proceed" triple negative).
   - Hard Rules parallel structure: standardize to "**Title.** Directive. [Action on violation.]" format (R15).

7. **D4 prompt-eval fixes:**
   - Define "meaningful assertion" -> "verifies externally observable behavior (DOM state, URL, visibility), not internal state" (CLR-2).
   - Define "similar patterns" -> "matching page object style, assertion approach, describe/test structure" (CLR-2).
   - Add explicit mode detection: "If $ARGUMENTS contains 'fix' or paths to .spec.ts files: fix mode. Otherwise: create mode." (CLR-1).
   - Define "max 3 fix iterations" -> "max 3 edit-run cycles (one cycle = edit test + run test)" (OUT-3).
   - Add playwright-cli availability check to pre-flight (CLR-6).

## Strengthen

| Fix | Source | Description |
|-----|--------|-------------|
| Define "meaningful assertion" | D4 W2 | "verifies externally observable behavior (DOM state, URL, visibility)" |
| Explicit mode detection | D4 W7 | "$ARGUMENTS contains 'fix' or .spec.ts paths -> fix mode; else create" |
| Define iteration | D4 W6 | "one cycle = edit test + run test; max 3 cycles" |
| Clarify seed vs few-shot precedence | D4 W4 | "1. Read seed (fixtures). 2. Find few-shot (style). 3. Conflict: few-shot wins style, seed wins fixtures." |
| playwright-cli pre-flight | D4 W5 | "Verify: playwright-cli --version. If missing: NEEDS_CONTEXT." |

## Hook/Command Splits

No hooks. Generator is a subagent dispatched by orchestrator. Its logic is code generation and iterative fixing -- judgment-heavy, not deterministic.

The "one test at a time with green gate" pattern could theoretically be enforced by a Stop hook (block stop until current test passes), but this conflicts with the max-3-iterations escape hatch. **Keep as prompt logic.**

## Surviving References

**ALL 3 references fail the three-condition survival test:**

| Reference | Rare? | >1000t compressed? | Gate unskippable? | Verdict |
|-----------|-------|--------------------|--------------------|---------|
| locator-strategy.md | NO | NO (~350t) | NO | INLINE generator portion |
| seed-file-spec.md | NO | NO (~300t) | NO | INLINE generator portion |
| file-protocol.md | NO | NO (~150t) | NO | INLINE generator portion |

**Zero surviving references.** Generator body is self-contained.

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| Generator body | 2,194 | ~3,150 | +956 |
| locator-strategy.md (runtime load) | 2,583 | 0 | -2,583 |
| seed-file-spec.md (runtime load) | 1,521 | 0 | -1,521 |
| file-protocol.md (runtime load) | 4,155 | 0 | -4,155 |
| **Total at generator runtime** | **10,453** | **~3,150** | **-7,303 (-69.9%)** |

Generator was already the largest agent body (2,194t) with substantial inline content. The inlining adds locator decision tree, seed spec, and artifact protocol while deduplicating existing risky locators and shadow DOM sections. Net body growth is modest because deduplication offsets new content.
