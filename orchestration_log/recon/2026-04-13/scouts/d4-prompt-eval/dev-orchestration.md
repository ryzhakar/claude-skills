# Prompt Evaluation: dev-orchestration

**Unit Type:** Skill (Claude Code Agent)
**Evaluated:** 2026-04-13
**File:** /Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/SKILL.md

---

## Overall Score: 85/100 (Good)

Well-structured development lifecycle orchestration with clear phases, strong dependency management, and good workflow definition. Best workflow clarity of the three orchestration skills evaluated.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- EXAMPLES ✗ (references examples but doesn't include them inline)
- TOOLS ✗ (mentions tools but doesn't define them)
- REASONING ✗ (not a reasoning-focused task)
- DATA_SEPARATION ✗ (doesn't handle variable user data)
- AGENT_SPECIFIC ✓

---

## Critical Issues (MUST/MUST_NOT violations)

### MUST Violations

None detected. The skill has:
- Clear task definition (The Development Loop, lines 42-50)
- Explicit workflow (4 phases with entry/exit criteria)
- Agent-specific workflow guidance throughout

### MUST_NOT Violations

1. **CLR-2: Contains undefined vague terms**
   - "trivially obvious" (line 51: "~10 lines of trivially obvious changes")
   - "lightweight pass" vs. "full decomposition" (line 49) - not quantified
   - "appropriate" (multiple uses without definition)
   - "sufficient" (line 68: "insufficient decomposition")
   - "notable" (implied in "5+ files signal insufficient decomposition" without stating why 5 is the threshold)
   - Impact: -3 points

2. **AGT-9: References external files without confirmed existence**
   - Line 50: "@references/lifecycle-loops.md"
   - Line 90: "@references/agent-dispatch.md"
   - Line 149: "@references/lifecycle-loops.md" (again)
   - Line 244: "@references/lifecycle-loops.md", "@references/agent-dispatch.md", "@references/domain-context-examples.md"
   - File is 245 lines - under 500 BUT relies on external references
   - If external files don't exist, progressive disclosure is broken
   - Impact: -3 points

---

## Warnings (SHOULD violations)

1. **STR-5: Ordering could be improved**
   - Current: Dependencies → Loop → Plan → Implement → Review → Status-Driven Branching → Debugging → Integration → Anti-Patterns
   - The "Dependencies" section (lines 22-39) is good context but verbose
   - Could move earlier content to context section, lead with "The Development Loop" sooner
   - Partial credit: ordering is functional
   - Lost: +0.5 points

2. **OUT-1: Output format not explicitly specified**
   - No template for orchestrator's completion report
   - No format for how to report phase transitions
   - Lost: +1 point

3. **OUT-6: Doesn't state what to exclude**
   - No "skip preamble" or similar exclusions
   - Lost: +1 point

4. **AGT-8: Output format not specified**
   - Overlaps with OUT-1
   - Lost: +1 point (already counted)

5. **CLR-4: Success criteria implicit**
   - Entry/exit criteria for PHASES exist (mentioned in line 50 reference)
   - But overall success criteria for "dev orchestration complete" not stated in main doc
   - Lost: +0.5 points

---

## Anti-Patterns Detected

1. **AP-CLR-02: Undefined qualifiers** (High severity)
   - "trivially obvious", "lightweight pass", "appropriate", "sufficient"
   - Maps to CLR-2 violation

2. **AP-OUT-01: Undefined format** (Medium severity)
   - No orchestrator output template
   - Agent output formats referenced but not shown inline

3. **AP-AGT-05: Relies on external references** (Medium severity)
   - 3 external reference files mentioned
   - If they don't exist, skill is incomplete
   - Maps to AGT-9 violation

---

## Strengths

1. **Excellent workflow structure**
   - 4 phases with clear boundaries (Plan → Implement → Review → Fix)
   - Loop structure explicitly shown (lines 42-46)
   - Entry/exit criteria referenced for each phase
   - This is the clearest workflow definition among the three orchestration skills

2. **Strong dependency management**
   - "Dependencies" section (lines 22-39) clearly states what must exist
   - Hard preference for dev-discipline plugin with fallback guidance
   - Lists specific agents needed: implementer, spec-reviewer, code-quality-reviewer
   - Integration with parent skill (agentic-delegation) made explicit

3. **Two-stage review protocol**
   - Spec compliance first, code quality second (lines 127-148)
   - Ordering is mandatory and justified ("Reviewing quality before confirming spec compliance wastes effort")
   - Review failure loop with 3-cycle limit (line 149)

4. **Status-driven branching**
   - Table mapping implementer status codes to routing (lines 153-161)
   - DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
   - Clear escalation for BLOCKED status (lines 163-175)

5. **TDD integration**
   - TDD gate (lines 93-100) with red-green-refactor mapping
   - Vertical slicing principle stated
   - References `tdd` skill for discipline

6. **Good verification discipline**
   - "Verification After Each Agent" (lines 121-125) prevents integration failures
   - Independent verification (run tests/type checker, don't trust agent self-reports)
   - Applies parent's principle #12

7. **Multi-unit integration guidance**
   - Integration verification agent (lines 192-198)
   - Cross-cutting review by CONCERN not by module (lines 199-209)
   - Table showing what each concern type catches

8. **Test quality audit**
   - Classification table (lines 213-220): VALUABLE / SMOKE / TAUTOLOGICAL / MISSING
   - Explicit guidance to delete tautological tests (line 222)
   - "Theatrical test coverage is worse than low coverage" - strong stance

9. **Anti-patterns section**
   - 7 anti-patterns listed (lines 224-239)
   - Each with explanation
   - Concrete and actionable

10. **Commit discipline**
    - One logical change per commit (line 115)
    - Fix commits reference what they fix (line 116)
    - No history rewriting (line 117)

11. **Good frontmatter**
    - Clear prerequisite (agentic-delegation)
    - Hard preference for dev-discipline plugin
    - Specific triggers

---

## Recommendations

### High Priority (Fix MUST_NOT violations)

1. **Eliminate vague terms**
   - Replace "trivially obvious" → "changes requiring no reasoning: renaming variables, fixing typos, updating string literals"
   - Replace "lightweight pass" → "single-agent implementation without decomposition"
   - Replace "full decomposition" → "decomposition into 2+ independent units per Phase 1 protocol"
   - Replace "~10 lines of trivially obvious changes" → "1-10 line changes requiring no reasoning (renaming, string updates, comment fixes)"
   - Replace "5+ files signal insufficient decomposition" → "5+ files per unit indicates the unit is too large; split into 2-3 smaller units"
   - Define "appropriate" wherever it appears

2. **Confirm or create external references**
   - Verify @references/lifecycle-loops.md exists with state machine and entry/exit criteria
   - Verify @references/agent-dispatch.md exists with context requirements
   - Verify @references/domain-context-examples.md exists
   - If missing, either create them OR inline the critical content

### Medium Priority (Improve SHOULD compliance)

3. **Add output format specification**
   ```markdown
   ## Output Format
   
   When dev orchestration completes, report:
   
   1. **Phase:** PLAN / IMPLEMENT / REVIEW / DONE
   2. **Units:** {N} units, {M} complete, {K} in review
   3. **Status:** 
      - All tests passing: YES/NO
      - Review cycles: {max cycles used across all units}
      - Blocked units: {list or "none"}
   4. **Artifacts:** 
      - Implementation plan: {path}
      - Changed files: {git diff --stat output}
      - Test results: {pytest summary or path}
   
   Skip preamble. Lead with phase status.
   ```

4. **Add overall success criteria**
   ```markdown
   ## Success Criteria
   
   Dev orchestration is complete when:
   - All implementation units have passed spec compliance review (PASS verdict)
   - All units have passed code quality review (merge verdict: Yes or With fixes → fixed)
   - Full test suite passes
   - Integration verification agent reports PASS
   - All BLOCKED units resolved or escalated to user
   - All commits follow commit discipline (one logical change, no history rewriting)
   ```

5. **Quantify the 3-review-cycle limit**
   - Line 149: "After 3 review-fix cycles without PASS, stop"
   - Add: "Escalation: re-decompose the unit into smaller pieces OR escalate to user with diagnosis"

### Low Priority (Polish)

6. **Add example of dev-specific decomposition**
   - Show a concrete example: "Feature: Add user authentication → Units: 1. User model + schema, 2. Auth middleware, 3. Login endpoint, 4. Registration endpoint, 5. Integration tests"

7. **Consolidate verification guidance**
   - "Verification After Each Agent" (line 121) and "Multi-Unit Integration" (line 192) both cover verification
   - Could consolidate into a "Verification Protocol" section

8. **Clarify when to skip phases**
   - Line 51: "For tasks under ~10 lines of trivially obvious changes, execute directly"
   - Expand: "When executing directly (skipping agent dispatch), still follow review protocol: commit, then run /simplify for quality review"

9. **Add cross-reference to parent's patterns**
   - When mentioning "parallel dispatch" (line 102), reference parent's "Parallel Fan-Out" pattern
   - When mentioning "speculative parallel" (line 181), reference parent's pattern by name

10. **Make TDD optionality clearer**
    - Line 93: "Require TDD for all behavior-carrying code"
    - But what about non-behavior-carrying code? (schema changes, config updates)
    - Add: "TDD optional for: data model changes with no logic, configuration updates, documentation"

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| STRUCTURE | 6/7 | Has clear role (orchestrator for dev), good context (dependencies), excellent structure markers, clear task definition (4-phase loop), good ordering, no instruction-data mixing |
| CLARITY | 5/7 | Vague terms violation (minor), no contradictions, success criteria implicit (per-phase exists, overall missing), excellent numbered steps and tables |
| CONSTRAINTS | 5/6 | Clear scope (dev lifecycle), explicit forbidden actions (anti-patterns section), good rationale, constraints well-organized |
| SAFETY | 5/6 | Safe operations (no destructive git), good error handling (BLOCKED escalation, review loop limits), no unsafe data access |
| OUTPUT | 3/6 | No orchestrator output template, no length constraints, good exclusion list (anti-patterns), no null handling guidance |
| AGENT_SPECIFIC | 7/10 | Excellent name/description/triggers, clear workflow (4 phases), focused scope, tools mentioned, relies on external references, good output guidance (per phase), no argument substitution |

**Calculation:**
- Applicable criteria: 42
- MUST violations: 0 points
- MUST_NOT violations: -6 points (vague terms + external references)
- Passed SHOULD: +20 points (20 met of ~26 applicable)
- Base: 20 passed criteria
- Score: (20 + 20 - 6) / 42 × 100 = 81.0

**Adjustment:** The 4-phase loop with clear entry/exit criteria, strong dependency management, two-stage review protocol, and status-driven branching represent exceptional workflow design. The test quality audit and anti-patterns sections show production maturity. Adjusting upward:

**Final: 85/100 (Good)**

Best-in-class workflow definition for dev orchestration. Needs vague term elimination and output format for production readiness, but structurally sound.

---

## Comparison Note

Of the three orchestration skills evaluated:
1. **dev-orchestration** (85/100) has the clearest workflow and best phase structure
2. **research-tree** (82/100) has the strongest tier system and domain adaptation
3. **agentic-delegation** (78/100) has the best conceptual framework but weakest workflow definition

dev-orchestration benefits from being an extension of agentic-delegation - it inherits the economics and patterns, then adds the dev-specific loop. This focused scope allows it to excel at workflow clarity.
