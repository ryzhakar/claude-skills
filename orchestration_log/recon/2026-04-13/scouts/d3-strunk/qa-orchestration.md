# Strunk Analysis: qa-orchestration

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 64: "Prerequisites → Plan → (Generate → Execute → Heal)* → Report"**
- **Text**: Full section, lines 79-86
- **Violation**: Passive construction "Base URL known" (line 83)
- **Severity**: Severe
- **Issue**: Obscures agency - who knows the URL? Who checks?
- **Suggested revision**: "Check the base URL: extract from the user's argument, or check `.playwright/project-config.md`. If neither exists, ask the user."

**Line 81-82: "Seed file exists"**
- **Text**: "Seed file exists: Check `tests/seed.spec.ts`. If missing, STOP."
- **Violation**: Passive/existential construction
- **Severity**: Severe
- **Issue**: Weak construction lacks direct action
- **Suggested revision**: "Check `tests/seed.spec.ts` exists. If missing, STOP."

### R12 (Concrete Language) - Severe

**Line 18-19**
- **Text**: "establishes the economics (agents are cheap, orchestrator context is expensive), the model ladder (haiku-first with upgrade-on-failure), execution patterns (parallel fan-out, sequential pipeline)"
- **Violation**: Abstract nominalizations ("economics", "patterns") when concrete alternatives exist
- **Severity**: Severe
- **Issue**: Reader must translate abstractions to specifics
- **Suggested revision**: "establishes economic constraints (agents are cheap, orchestrator context is expensive), model tier assignments (haiku-first with upgrade-on-failure), execution strategies (parallel fan-out, sequential pipeline)"

**Line 26**
- **Text**: "Provides: model ladder, decomposition patterns, prompt anatomy, execution patterns, quality governance..."
- **Violation**: Vague list of abstract concepts
- **Severity**: Moderate-to-Severe
- **Issue**: "Decomposition patterns" and "prompt anatomy" lack specificity
- **Suggested revision**: Consider more specific formulation or accept as technical terminology

## Moderate

### R13 (Needless Words) - Moderate

**Line 20**
- **Text**: "If the orchestration plugin is installed, **read agentic-delegation's SKILL.md before proceeding.** If not installed, recommend installing it."
- **Violation**: Redundant "installed" - first clause establishes the condition
- **Severity**: Moderate
- **Suggested revision**: "If the orchestration plugin is installed, **read agentic-delegation's SKILL.md before proceeding.** Otherwise, recommend installing it."

**Line 28**
- **Text**: "For multi-session QA work, the parent's session persistence protocol applies"
- **Violation**: "the parent's" is needless - context is clear
- **Severity**: Minor-to-Moderate
- **Suggested revision**: "For multi-session QA work, session persistence protocol applies"

**Line 34-36**
- **Text**: "writes tests one-at-a-time with TDD-style verify loop, accessibility-first locators. Also owns structural test fixes (fix mode) for timing, fixture, and architecture issues."
- **Violation**: "Also owns" - weak construction, "owns" is vague technical jargon
- **Severity**: Moderate
- **Suggested revision**: "writes tests one-at-a-time with TDD-style verify loop, accessibility-first locators. Repairs structural test failures (fix mode): timing, fixture, and architecture issues."

**Line 42**
- **Text**: "**Read ALL of these before Phase 1.** They contain the operational details summarized below."
- **Violation**: "They contain the operational details summarized below" is needless - reader can infer
- **Severity**: Minor-to-Moderate
- **Suggested revision**: "**Read ALL of these before Phase 1.**" (omit second sentence entirely)

**Line 123-125**
- **Text**: "Before routing failures, check that passing tests are substantive. A test that navigates to a page and logs 'needs implementation' without asserting or comparing anything is a hollow pass — it provides false confidence."
- **Violation**: "— it provides false confidence" restates what "hollow pass" already implies
- **Severity**: Moderate
- **Suggested revision**: "Before routing failures, check that passing tests are substantive. A test that navigates to a page and logs 'needs implementation' without asserting or comparing anything is a hollow pass."

**Line 150**
- **Text**: "After all healer results are collected:"
- **Violation**: Passive construction where active is clearer
- **Severity**: Moderate
- **Suggested revision**: "After collecting all healer results:"

### R11 (Positive Form) - Moderate

**Line 72**
- **Text**: "**All tests pass.** No failures of any category."
- **Violation**: Negative construction in second sentence where positive clearer
- **Severity**: Minor
- **Suggested revision**: "**All tests pass.** Every test succeeds." (or simply omit the second sentence as needless)

**Line 73-74**
- **Text**: "**Only non-healable failures remain.** All locator failures healed; remaining failures are timing, assertion, or infrastructure issues that require human intervention."
- **Violation**: Multiple negatives ("non-healable", explanation uses negation)
- **Severity**: Moderate
- **Suggested revision**: "**Only structural failures remain.** All locator failures healed; remaining failures are timing, assertion, or infrastructure issues requiring human intervention."

**Line 177-178**
- **Text**: "If any agent dispatch fails (no output file, agent error):"
- **Violation**: Negative construction
- **Severity**: Minor
- **Suggested revision**: "If agent dispatch fails (missing output file, agent error):"

**Line 180**
- **Text**: "Do not retry a failed phase more than once"
- **Violation**: Negative instruction where positive is clearer
- **Severity**: Moderate
- **Suggested revision**: "Retry a failed phase once, then stop"

### R15 (Parallel Construction) - Moderate

**Line 26**
- **Text**: "Provides: model ladder, decomposition patterns, prompt anatomy, execution patterns, quality governance (re-launch principle, contradiction resolution, concurrent file write prevention, independent verification), and session persistence (ARRIVE/WORK/LEAVE lifecycle for multi-session work)."
- **Violation**: Series mixes bare noun phrases with parenthetical elaborations inconsistently
- **Severity**: Moderate
- **Issue**: First four items are bare phrases; last two have parenthetical clarifications
- **Suggested revision**: Either add parentheticals to all or remove from last two for consistency

**Line 56-59 (Table)**
- **Text**: Gate mechanisms column
- **Violation**: Not parallel structure
- **Severity**: Minor
- **Issue**: 
  - Row 1: "Seed test must pass before any generation. If it fails, the session is invalid."
  - Row 2: "Thresholds determine auto-merge (>=0.85), review (0.60-0.84), or defer (<0.60). Hard rejection at 0.0..."
  - Row 3: "Max 2 healing attempts per test, max 3 PRs per session, blocklist for repeat offenders."
- **Suggested revision**: Make all three follow pattern: "Constraint. Consequence." or all imperative

**Line 128-132**
- **Text**: Failure routing list items mix completion and continuation forms
- **Violation**: 
  - "`DONE` with zero failures → check exit conditions, proceed to Report or re-enter inner loop"
  - "`DONE` with locator failures → proceed to Phase 4 (Heal)"
  - "`DONE` with timing failures where... → re-dispatch **generator-agent** in fix mode..."
- **Severity**: Minor
- **Issue**: First item uses two imperatives; second uses one; third uses one with long condition
- **Suggested revision**: Normalize structure

### R18 (Emphatic Position) - Moderate

**Line 18**
- **Text**: "Extends agentic-delegation with the Playwright test lifecycle."
- **Violation**: Ends with "Playwright test lifecycle" when emphasis should be on relationship to parent
- **Severity**: Minor-to-Moderate
- **Issue**: Not necessarily wrong, but "lifecycle" is less emphatic than the extension relationship
- **Suggested revision**: Consider "Extends agentic-delegation for Playwright test lifecycle orchestration" (ends on action)

**Line 33-34**
- **Text**: "**planner-agent** (sonnet) — explores live app via browser, produces test plan, page inventory, selector strategy"
- **Violation**: Ends with list of outputs; "selector strategy" less emphatic than primary outputs
- **Severity**: Minor
- **Issue**: List order doesn't build to climax
- **Suggested revision**: Consider reordering for emphasis: "...produces page inventory, selector strategy, test plan"

**Line 130-132**
- **Text**: "`DONE` with timing failures where locators are correct but test structure is wrong (serial execution of independent tests, missing waits, fixture teardown races) → re-dispatch **generator-agent** in fix mode with the failing test paths and error descriptions. The generator owns test architecture; the healer only owns locators."
- **Violation**: First sentence ends weakly with "error descriptions"; second sentence strong
- **Severity**: Minor
- **Issue**: Key point about ownership division comes after, not at end of routing instruction
- **Suggested revision**: Integrate ownership explanation into main sentence, or reverse order

## Minor & Stylistic

### R13 (Needless Words) - Minor

**Line 3-4**
- **Text**: "Extension of agentic-delegation for the Playwright test lifecycle."
- **Violation**: "for the" could be "for"
- **Severity**: Minor (stylistic)
- **Suggested revision**: "Extension of agentic-delegation for Playwright test lifecycle."

**Line 53**
- **Text**: "Three gates at three scopes subsume the parent's general quality governance for QA work:"
- **Violation**: "subsume the parent's general quality governance" is abstract/wordy
- **Severity**: Minor
- **Suggested revision**: "Three gates at three scopes govern QA work quality:"

**Line 97**
- **Text**: "Before proceeding to GENERATE, verify all 5 required artifacts exist:"
- **Violation**: "verify all 5 required artifacts exist" - "exist" is weak
- **Severity**: Minor
- **Suggested revision**: "Before proceeding to GENERATE, verify all 5 required artifacts:"

**Line 109**
- **Text**: "Dispatch **generator-agent**. Include `.playwright/lessons.md` path in the dispatch if it exists (agents must read it before starting — it contains discoveries from prior cycles)."
- **Violation**: Long parenthetical explanation could be condensed
- **Severity**: Minor
- **Suggested revision**: "Dispatch **generator-agent**. Include `.playwright/lessons.md` path if it exists (contains discoveries from prior cycles; agents must read before starting)."

### R11 (Positive Form) - Minor

**Line 81**
- **Text**: "If missing, STOP."
- **Violation**: Negative condition
- **Severity**: Minor (acceptable for instructions)
- **Note**: This is standard conditional instruction format; revision not needed

**Line 105**
- **Text**: "If any are missing, re-dispatch planner-agent with explicit instructions to produce the missing artifacts."
- **Violation**: Double negative ("any missing" + "missing artifacts")
- **Severity**: Minor
- **Suggested revision**: "If artifacts are incomplete, re-dispatch planner-agent with explicit instructions to produce them."

### R15 (Parallel Construction) - Minor

**Line 108-114**
- **Text**: Branch patterns
- **Violation**: Inconsistent completion across phases
- **Severity**: Minor
- **Issue**: 
  - Phase 1: "verify planner completeness (see below), then write `PLAN` to `.claude/qa-phase.txt`, proceed to Phase 2"
  - Phase 2: "write `GENERATE` to `.claude/qa-phase.txt`, proceed to Phase 3"
- **Note**: Phase 1 has extra step (completeness check) making strict parallelism impossible

### R10 (Active Voice) - Minor

**Line 169**
- **Text**: "Validate findings before reporting. Generator must not log implementation gaps (harness errors, placeholder logic) as business findings. If findings exist, verify each has substantive data (not placeholder values). Strip or flag invalid findings."
- **Violation**: Last sentence uses imperative, but "If findings exist" in prior sentence is passive/existential
- **Severity**: Minor
- **Suggested revision**: "Validate findings before reporting. Generator must not log implementation gaps (harness errors, placeholder logic) as business findings. For each finding, verify substantive data (not placeholder values). Strip or flag invalid findings."

**Line 86**
- **Text**: "**Session resumption:** Read `.claude/qa-phase.txt` if it exists. Resume from the phase AFTER the one recorded (PLAN → resume at GENERATE, etc.). If missing, start from Phase 1."
- **Violation**: "If missing" is weak passive construction
- **Severity**: Minor
- **Suggested revision**: "**Session resumption:** Read `.claude/qa-phase.txt` if it exists. Resume from the phase AFTER the one recorded (PLAN → resume at GENERATE, etc.). If absent, start from Phase 1."

## Summary

**Total findings: 38**

**By severity:**
- Critical & Severe: 5 (R10: 2, R12: 3)
- Moderate: 17 (R13: 6, R11: 4, R15: 3, R18: 3, R10: 1)
- Minor & Stylistic: 16 (R13: 5, R11: 3, R15: 2, R10: 3, R18: 0, other: 3)

**By rule:**
- R10 (Active Voice): 6 findings (2 severe, 1 moderate, 3 minor)
- R11 (Positive Form): 7 findings (0 severe, 4 moderate, 3 minor)
- R12 (Concrete Language): 3 findings (3 severe, 0 moderate, 0 minor)
- R13 (Needless Words): 11 findings (0 severe, 6 moderate, 5 minor)
- R15 (Parallel Construction): 5 findings (0 severe, 3 moderate, 2 minor)
- R18 (Emphatic Position): 3 findings (0 severe, 3 moderate, 0 minor)

**Key patterns:**

1. **Passive/existential constructions** (R10): The document uses "exists," "known," "missing" constructions that obscure agency. While acceptable for technical prerequisites, they weaken instructional force.

2. **Abstract terminology** (R12): Terms like "economics," "patterns," "governance" appear frequently. Some are unavoidable technical vocabulary; others could be more concrete.

3. **Wordiness** (R13): Several instances of redundant explanation or weak constructions ("they contain," "also owns," needless elaborations after clear statements).

4. **Negative instructions** (R11): Multiple uses of "non-healable," "no failures," "do not" where positive alternatives exist. Technical documentation often requires negative formulations, but several instances could be reframed.

5. **Parallel structure breaks** (R15): Lists and series occasionally mix forms (bare phrases vs. parenthetical elaborations, different completion patterns).

6. **Weak endings** (R18): Several sentences end on weak elements rather than emphatic points. Not egregious but room for improvement.

**Context considerations:**

This is **technical instruction documentation**, not expository prose. Strunk's rules apply with modifications:
- Passive voice is more acceptable for prerequisite checks
- Negative formulations are standard for error conditions
- Abstract technical terminology is sometimes unavoidable
- Parallel construction matters more in lists than phase descriptions

**Overall assessment:** The document is competent technical prose with **moderate** Strunk adherence. Most violations are severity 2-3 (moderate/minor), not critical failures. The severe findings are concentrated in R10 and R12, suggesting opportunities to clarify agency and concretize abstractions without sacrificing technical precision.

**Recommended priority:** Fix severe R10/R12 violations first (5 items), then address moderate R13 wordiness (6 items). Minor findings can be refined opportunistically.
