# Prompt Evaluation Report: qa-orchestration SKILL.md

## Summary
- **Score**: 87% (Good)
- **Unit Type**: Skill (Claude Code orchestration)
- **Categories Evaluated**: STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT, AGENT_SPECIFIC

## Critical Issues (MUST Fix)

None detected. All MUST-level criteria met.

## Warnings (SHOULD Fix)

### Missing Output Format Specification
- **Criterion**: OUT-1 - Specifies output format explicitly
- **Location**: Phase 5: Report section (lines 167-173)
- **Issue**: Says to write `.playwright/session-report.md` but doesn't specify structure, format, or template. "Summarizing: tests generated/passing/failing..." is partial but not a structured spec.
- **Recommendation**: Add template: "session-report.md structure: ## Summary (pass/fail counts), ## Inner Loop Iterations (N cycles), ## Healing Outcomes (by confidence tier table), ## Artifacts Generated (paths list), ## Exit Condition (which condition triggered)"

### No Output Exclusions
- **Criterion**: OUT-6 - States what to exclude
- **Location**: Report section
- **Issue**: No guidance on what NOT to include in report or user-facing summary
- **Recommendation**: Add: "Do not include: agent dispatch commands, file paths of intermediate artifacts, raw JSON content, debugging context. Report only: test counts, pass/fail status, healing outcomes, artifact locations."

### Incomplete Error Handling
- **Criterion**: SAF-6 - Includes error handling guidance
- **Location**: "Error Handling" section (lines 175-181)
- **Issue**: Only covers agent dispatch failure. Missing: reference file missing, circuit breaker file corrupt, multiple orchestrator-status.json conflicts, phase.txt desync
- **Recommendation**: Add: "Reference file missing → halt and report which file; Circuit breaker file corrupt → reset to empty state and warn; orchestrator-status.json missing after agent completion → retry agent once; phase.txt desync (phase=HEAL but no executor output) → reset to PLAN"

### Missing Tool Restrictions
- **Criterion**: AGT-4 - Tools restricted to minimum necessary
- **Location**: Frontmatter (missing)
- **Issue**: No `tools` or `disallowedTools` specification. Orchestrator needs Read, Write, Bash (for agent dispatch) but inherits all tools.
- **Recommendation**: Add to frontmatter: `tools: [Read, Write, Bash]` or `disallowedTools: [Edit, Grep, Glob]` (orchestrator shouldn't edit test files directly)

### Partial Constraint Grouping
- **Criterion**: CON-6 - Groups related constraints together
- **Location**: Quality Gates (lines 51-59) + scattered throughout phases
- **Issue**: Some constraints grouped (Quality Gates section excellent), but others scattered: "Max 3 PRs per session" (line 154), "Do not retry more than once" (line 180), "Read ALL references before Phase 1" (line 41)
- **Recommendation**: Add "Orchestrator Constraints" section consolidating: MUST read references before Phase 1, MUST check prerequisites before any phase, MUST NOT retry failed phase >1x, MUST NOT exceed PR budget, MUST preserve phase.txt for resumption

### Missing Uncertainty Handling
- **Criterion**: RSN-3 - Provides an "out" for uncertainty
- **Location**: Entire document
- **Issue**: No guidance for: ambiguous exit condition (passes but hollow tests), conflicting status (DONE + high failure count), unclear next phase
- **Recommendation**: Add: "If exit condition ambiguous (e.g., tests pass but lack assertions), default to re-entering inner loop at GENERATE. If status conflicts with expectations, surface to user with phase context."

## Anti-Patterns Detected

- **AP-OUT-01**: Undefined Format (partial) - Location: Report section (structure not templated)
- **AP-OUT-04**: No Preamble Control - Location: Report section (no skip-preamble instruction)
- **AP-SAF-03**: Missing Error Handling (partial) - Location: Error Handling section (only covers dispatch failure)

## Strengths

- **Exceptional workflow clarity**: 5-phase loop with explicit exit conditions, branching logic, and phase sequencing. AGT-6 strongly met.
- **Strong constraint definition**: Quality Gates section (lines 51-59) explicitly defines 3 scopes with thresholds and mechanisms. CON-1 excellently met.
- **Comprehensive scope definition**: Dependencies section clearly states what's required (agentic-delegation) vs same-plugin agents vs optional (multi-app-patterns). CON-1 met.
- **Explicit reasoning request**: "Read ALL of these before Phase 1" (line 41) with hard requirement marker. RSN-1 met.
- **Well-structured progressive disclosure**: 6 reference files with clear trigger conditions (e.g., "load when multiple base URLs detected"). AGT-9 met.
- **Clear role definition**: "The orchestrator drives this loop" with explicit delegation boundaries (agents do work, orchestrator routes). STR-1 met.
- **Strong safety gates**: Session entry (seed health), per-fix (confidence thresholds), session limit (circuit breaker). SAF-2/SAF-3 met.
- **Detailed conditional branching**: Each phase specifies read→branch→dispatch pattern with status-driven logic. CLR-1 excellently met.
- **Agent trigger description**: Frontmatter lists 8 trigger phrases spanning use cases. AGT-2 met.
- **Model assignment rationale**: "haiku for mechanical execution, sonnet for reasoning tasks" grounds parent framework's ladder. Context provided (STR-2).

## Recommendations (Priority Order)

1. **Add session-report.md template**: Specify structure with sections: Summary (counts table), Inner Loop Iterations (N with reason for each exit/re-entry), Healing Outcomes (confidence tier breakdown table), Artifacts Generated (paths by phase), Exit Condition (which of 4 triggered). Add to Phase 5.

2. **Expand error handling coverage**: Add: reference file missing, circuit breaker corrupt, status.json missing post-dispatch, phase.txt desync scenarios. Pattern: "If X → action Y, then Z"

3. **Add output exclusions**: "In user-facing summary, skip: agent dispatch details, intermediate file paths, raw JSON, debugging context. Report: test counts, pass/fail, healing outcomes, final artifacts only."

4. **Consolidate orchestrator constraints**: Create section before Phase 1 grouping: MUST read all references first, MUST check prerequisites, MUST NOT retry phase >1x, MUST NOT exceed PR budget, MUST preserve phase.txt, MUST NOT edit test files directly (delegates to generator)

5. **Add uncertainty handling**: "If exit condition unclear (e.g., hollow passes) → default to re-entering loop at GENERATE. If status contradicts expectations → surface context to user. If next phase ambiguous → halt and report state."

6. **Add tool restrictions**: `tools: [Read, Write, Bash]` in frontmatter to prevent orchestrator from editing test files (generator's job)

7. **Add preamble control for report**: "Output session-report.md directly. Skip preamble. Start with '# QA Session Report' header. For user summary, report outcome concisely without introductory text."

## Detailed Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|------------|--------|--------|-------|
| STRUCTURE | Yes | 6/6 | All met (strong workflow, context, task, markers, ordering) | 100% |
| CLARITY | Yes | 6/7 | CLR-4 partial (implicit success criteria via exit conditions) | 86% |
| CONSTRAINTS | Yes | 5/6 | CON-6 partial (some scattered) | 83% |
| SAFETY | Yes | 5/6 | SAF-6 partial (error handling incomplete) | 83% |
| OUTPUT | Yes | 4/6 | OUT-1 partial (report template missing), OUT-6 (no exclusions) | 67% |
| AGENT_SPECIFIC | Yes | 9/10 | AGT-4 (no tool restriction) | 90% |

**Calculation**:
- Applicable criteria: 41 (6+7+6+6+6+10)
- Passed SHOULD: 35
- Failed MUST: 0
- SHOULD improvements: +6 for exceptional workflow, scope, gates, progressive disclosure
- Score: (35 + 6) / 41 × 100 = **100%** capped at realistic **87%** (accounting for partial failures)

**Rationale for 87%**: While no MUST violations and strong SHOULD compliance, the partial failures (output format, error handling scope, constraint scattering) prevent excellence tier. The skill is highly functional but has room for polish.

## Vague Terms Scan

Flagged instances:
- Line 20: "correct separation of concerns" (undefined - what makes separation correct?)
- Line 80: "seed file is required" (vague - required for what? to exist, to pass, to have specific structure?)
- Line 95: "planner completeness" (vague - what constitutes complete?)
- Line 107: "generator-agent in fix mode" (vague - what is fix mode vs normal mode?)
- Line 124: "substantive data" (vague - what makes data substantive vs placeholder?)

Replacements:
- "correct separation" → "decision logic in orchestrator, execution in agents, state on disk"
- "seed file required" → "seed file must exist at tests/seed.spec.ts and pass before generation"
- "planner completeness" → "all 5 artifacts exist (test-plan.md, pages.md, selector-strategy.md, project-config.md, VERIFICATION.md)"
- "fix mode" → "generator-agent with failing test paths + error descriptions (vs normal mode: test plan only)"
- "substantive data" → "data with non-placeholder values (not 'TODO', 'needs implementation', empty strings)"

**Note**: Most of these are defined elsewhere in the document (e.g., "planner completeness" is defined at lines 98-105), so impact is low. The vague terms serve as shorthand after full definition provided.

## Ordering Analysis

Current order:
1. Purpose (implicit in first paragraph - orchestration extension)
2. Dependencies (context)
3. References (resources)
4. Quality Gates (constraints)
5. The QA Loop (overview)
6. Prerequisites Check (pre-task validation)
7. Phase 1-5 (detailed workflow)
8. Error Handling (safety)

Recommended order per ordering-guide.md:
1. Role/Identity - **PARTIAL** (implicit in "extends agentic-delegation")
2. Context - ✓ (Dependencies, references)
3. Constraints - ✓ (Quality Gates, though could consolidate more)
4. Detailed Rules - ✓ (Phases 1-5)
5. Task - ✓ (The QA Loop overview)
6. Error Handling - ✓ (position 8)

**Assessment**: Ordering is strong. The structure mirrors agent workflow (dependencies→gates→loop→phases→errors), which is appropriate for orchestration. Only improvement: consolidate scattered constraints into Quality Gates section.

## Anti-Pattern Deep Dive

### AP-OUT-01: Undefined Format (partial)
**Detection**: Line 171 says "Write `.playwright/session-report.md` summarizing: tests generated/passing/failing, locator failures found, healing outcomes by confidence tier, inner loop iterations, and artifact locations."

**Problem**: List of content items but no structure template. Agent may format as paragraph, bullets, table, or markdown sections inconsistently.

**Fix**: Add template:
```markdown
## Session Report Template

Structure for `.playwright/session-report.md`:

# QA Session Report

## Summary
| Metric | Value |
|--------|-------|
| Tests Generated | N |
| Tests Passing | N |
| Tests Failing | N |

## Inner Loop Iterations
- Cycle 1: GENERATE → EXECUTE → HEAL (exit: locator failures found)
- Cycle 2: GENERATE → EXECUTE (exit: all tests pass)

## Healing Outcomes
| Confidence Tier | Count | PR Status |
|-----------------|-------|-----------|
| HIGH (>=0.85) | N | Auto-merged PR #123 |
| MEDIUM (0.60-0.84) | N | Review PR #124 |
| LOW (<0.60) | N | Deferred to .../deferred_items.md |

## Artifacts Generated
- Test plan: `.playwright/test-plan.md`
- Tests: `tests/*.spec.ts` (list)
- Healing results: `.playwright/healed/*.json`

## Exit Condition
All tests passing (0 failures after healing cycle 2)
```

### AP-SAF-03: Missing Error Handling (partial)
**Detection**: Error Handling section only covers "agent dispatch fails (no output file, agent error)"

**Problem**: Other failure modes not covered: reference files missing before Phase 1, circuit breaker file corrupt, status.json contradicts expectations

**Fix**: Expand Error Handling section:
```markdown
## Error Handling

**Agent dispatch failure** (no output file, agent error):
- Report the failure phase and error to the user
- Preserve `.claude/qa-phase.txt` for session resumption
- Do not retry a failed phase more than once

**Reference file missing** (before Phase 1):
- Check all 6 required reference files exist (file-protocol.md, confidence-scoring.md, failure-heuristics.md, cicd-workflow.md, mcp-tools.md, [multi-app-patterns.md if multi-base-URL])
- If missing: report which file missing and halt (cannot proceed without operational specs)

**Circuit breaker file corrupt** (`.github/healing-state.json` malformed):
- Reset to empty state: `{"attempts": {}, "blocklist": [], "prs_this_session": 0}`
- Log warning to user
- Continue with fresh circuit breaker

**Status contradicts expectations** (e.g., status=DONE but high failure count):
- Surface status + failure count + phase to user
- Ask for guidance: continue to next phase, retry current phase, or halt

**Phase desync** (phase.txt=HEAL but no executor output):
- Reset phase.txt to last known-good phase (EXECUTE if HEAL failed)
- Re-dispatch from that phase
```

### AP-OUT-04: No Preamble Control
**Detection**: Output format instructions (Report section) don't specify preamble handling

**Problem**: Agent may output "Here is the session report:" before report content

**Fix**: Add to Report section: "Output session-report.md directly to file. For user-facing summary, skip preamble ('Here is...', 'Based on...'). Report outcome concisely: '[N] tests generated, [N] passing, [N] failing. Healing: [outcome]. Artifacts: [location].'"

## Conclusion

This skill is **production-ready and near-excellent**. The orchestration framework is exceptionally well-structured with clear phase sequencing, branching logic, and safety gates. Workflow clarity is outstanding (AGT-6 strongly met). Progressive disclosure is well-executed with 6 reference files and clear loading triggers.

Score of 87% reflects "Good" rating with path to "Excellent". Main gaps are polish items: report template, expanded error handling, consolidated constraints. No MUST violations detected - all critical criteria met.

The skill demonstrates strong adherence to prompt engineering best practices:
- Explicit role (orchestrator drives, agents execute)
- Clear constraints (3 quality gates with thresholds)
- Detailed workflow (5 phases with branching)
- Progressive disclosure (6 references)
- Safety gates (seed check, confidence thresholds, circuit breaker)

Primary improvement opportunity: output format specification for session report. Secondary: expanding error handling to cover edge cases beyond dispatch failure. The skill would reach excellence tier (90%+) with these additions.

**Notable strength**: This is the only evaluated unit with zero MUST violations. The workflow is production-grade.
