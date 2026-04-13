# Prompt Evaluation: agentic-delegation

**Unit Type:** Skill (Claude Code Agent)
**Evaluated:** 2026-04-13
**File:** /Users/ryzhakar/pp/claude-skills/orchestration/skills/agentic-delegation/SKILL.md

---

## Overall Score: 78/100 (Good)

Functional with room for improvement. Strong conceptual framework and comprehensive content but suffers from ordering issues, some vague terms, and length concerns.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- EXAMPLES ✗ (minimal examples present)
- TOOLS ✗ (mentions tools but doesn't define them)
- REASONING ✗ (not a reasoning-focused task)
- DATA_SEPARATION ✗ (doesn't handle variable user data)
- AGENT_SPECIFIC ✓

---

## Critical Issues (MUST/MUST_NOT violations)

### MUST Violations

1. **STR-3: Lacks clear task definition**
   - Quote: The document is titled "Agentic Delegation" but never states "When invoked, you will..." or "Your task is to..."
   - The frontmatter says "Use this skill whenever work can be broken into parts" but the body doesn't define what the orchestrator should DO when this skill is invoked
   - Impact: -3 points

2. **AGT-6: System prompt lacks clear workflow**
   - The document has extensive theory and patterns but no numbered step-by-step workflow like "When this skill is invoked: 1. Assess the task, 2. Decompose into units, 3. Dispatch agents..."
   - Impact: -3 points

### MUST_NOT Violations

1. **CLR-2: Contains undefined vague terms**
   - "appropriate for task" (line 152: "Permission mode appropriate for task")
   - "complex" appears 11 times without quantification
   - "focused" without definition (line 134: "One focused task per agent")
   - "Sweet spot" (line 192) is informal and vague
   - Impact: -3 points

2. **AGT-9: Exceeds 500 lines without progressive disclosure**
   - File is 496 lines but has @references to external files that don't exist yet (`@references/prompt-anatomy.md`, `@references/quality-governance.md`, `@references/session-persistence.md`)
   - The references suggest progressive disclosure was intended but not implemented
   - Impact: -3 points (borderline violation - close to limit and missing progressive disclosure mechanism)

---

## Warnings (SHOULD violations)

1. **STR-5: Ordering doesn't follow recommended sequence**
   - "The Economics" section (lines 20-82) contains task-critical information but appears before role definition
   - The recommended order is: role→context→constraints→rules→task→format
   - Actual order: economics thesis→model ladder→decomposition→execution→quality→archetypes
   - No explicit output format specification at the end
   - Lost: +1 point

2. **CLR-4: No explicit success criteria**
   - The document doesn't define when delegation has been done "correctly"
   - No acceptance criteria like "All tasks delegated, orchestrator context < X lines"
   - Lost: +1 point

3. **OUT-1: No explicit output format specification**
   - No format for how the orchestrator should report completion
   - No template for dispatch logs or decision records
   - Lost: +1 point

4. **OUT-6: Doesn't state what to exclude**
   - No "Do not include preambles" or similar exclusions
   - Lost: +1 point

5. **AGT-8: No output format specified**
   - Overlaps with OUT-1 - agent-specific version
   - Lost: +1 point (already counted in OUT-1)

6. **STR-2: Context is implicit rather than explicit**
   - The "Core Principle" section establishes thesis but doesn't state "You are an orchestrator in a multi-agent system where..."
   - Lost: +1 point

---

## Anti-Patterns Detected

1. **AP-STR-03: Format buried in middle** (Medium severity)
   - "Prompt Anatomy" section (line 282) is in the middle of the document, not near the end
   - Report formats discussed throughout rather than consolidated

2. **AP-CLR-02: Undefined qualifiers** (High severity)
   - "appropriate" (permission mode)
   - "complex" (used 11 times)
   - "focused" (task scope)
   - "Sweet spot" (granularity)
   - "easily absorbed" (sonnet cost)
   - Maps directly to CLR-2 violation

3. **AP-CON-04: Scattered constraints** (Low severity)
   - "When NOT to Delegate" (line 67) is buried in "The Economics" section
   - Should be consolidated with other constraints

4. **AP-AGT-04: Missing workflow** (High severity)
   - No numbered step-by-step process for "When this skill is invoked"
   - Maps directly to AGT-6 violation

5. **AP-AGT-05: Bloated skill** (Medium severity)
   - 496 lines with references to external docs that should exist but don't
   - Progressive disclosure attempted but incomplete

---

## Strengths

1. **Exceptional conceptual framework**
   - "The Economics" section (lines 20-82) provides foundational reasoning that justifies all subsequent patterns
   - The cost inversion table (line 33) and swarm principle (line 40) are concrete and actionable

2. **Concrete model tier guidance**
   - Clear model ladder (Haiku/Sonnet/Opus) with specific use cases
   - Upgrade path (lines 151-164) provides decision logic
   - "Fails at" lists for each model prevent misuse

3. **Comprehensive decomposition patterns**
   - Multiple patterns: by entity, by aspect, by need, by source, by concern (lines 194-204)
   - Granularity heuristic with examples (lines 181-192)

4. **Strong execution pattern catalog**
   - 6 execution patterns with use-case guidance (lines 289-354)
   - Parallel fan-out, sequential pipeline, background swarm, map-reduce, speculative parallel, chained refinement

5. **Context design principles**
   - Minimal context principle (line 224) prevents drift
   - Report-based communication (line 262) protects orchestrator context
   - Isolation principle (line 246) prevents bias propagation

6. **Task archetypes**
   - Concrete guidance for 7 common task types (research, implementation, audit, investigation, validation, documentation, exploration)
   - Each archetype shows decomposition, model assignment, assembly strategy

7. **Governing principles summary**
   - 12 numbered principles (lines 471-495) distill the entire framework
   - Useful reference and validation checklist

8. **Good frontmatter**
   - Clear trigger phrases
   - Core thesis included
   - Description indicates proactive use

---

## Recommendations

### High Priority (Fix MUST/MUST_NOT violations)

1. **Add explicit task definition**
   ```markdown
   ## When This Skill Is Invoked
   
   You are the orchestration controller for a multi-agent system. When this skill loads:
   
   1. Assess the task: can it be decomposed into independent units?
   2. Apply the decomposition test (line 173)
   3. For each unit: design agent prompt, assign model tier (haiku-first), dispatch
   4. Monitor completion summaries for failures and contradictions
   5. Synthesize results or delegate synthesis to capable agent
   6. Report completion with artifact references
   ```

2. **Extract progressive disclosure files**
   - Create `references/prompt-anatomy.md` with the 9-section prompt template and examples
   - Create `references/quality-governance.md` with detection patterns, re-launch principle, contradiction resolution
   - Create `references/session-persistence.md` with ARRIVE/WORK/LEAVE protocol
   - This brings the core SKILL.md under 300 lines and implements true progressive disclosure

3. **Eliminate vague terms**
   - Replace "appropriate permission mode" → "permissionMode: 'auto' for read-only, 'ask' for writes"
   - Replace "complex" with quantifiable criteria: "task requiring >3 reasoning steps", "handling >5 inputs"
   - Replace "focused task" → "task with single output artifact and <5 file dependencies"
   - Replace "Sweet spot" → "Optimal task size"

4. **Add numbered workflow**
   - Insert after "Core Principle" section
   - Use the template from recommendation #1

### Medium Priority (Improve SHOULD compliance)

5. **Reorder sections**
   ```
   1. Role/Identity (when invoked, you are...)
   2. Core Principle (the economics)
   3. Constraints (when NOT to delegate - move earlier)
   4. Model Ladder
   5. Decomposition
   6. Execution Patterns
   7. Quality Governance
   8. Task Archetypes
   9. Governing Principles
   10. Output Format (add this)
   ```

6. **Add output format specification**
   ```markdown
   ## Output Format
   
   When delegation completes, report:
   
   1. **Dispatched:** {N} agents ({haiku/sonnet/opus breakdown})
   2. **Artifacts:** List absolute paths to all agent outputs
   3. **Failures:** Any re-launches or escalations
   4. **Synthesis:** Path to final deliverable or "No synthesis - outputs independent"
   
   Skip preamble. Do not summarize agent content (it's on disk).
   ```

7. **Add success criteria**
   ```markdown
   ## Success Criteria
   
   - All independent units dispatched in parallel
   - Orchestrator context consumed only by: task decomposition, completion summaries, synthesis
   - No content relayed through orchestrator (agents read from disk)
   - Failed agents re-launched with better prompts or upgraded tiers (never debugged in orchestrator context)
   ```

### Low Priority (Polish)

8. **Consolidate constraints**
   - Move "When NOT to Delegate" section earlier (after Core Principle, before Model Ladder)
   - Group all scope boundaries together

9. **Add example tag wrappers**
   - The tables (lines 33, 76, etc.) are implicit examples
   - Wrap in `<example>` tags for clearer boundaries

10. **Clarify reference status**
    - If external references don't exist yet, mark them as TODO or create them
    - Current @references look like they should exist but produce 404s in reader's mental model

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| STRUCTURE | 4/7 | Has role (weak), context (good), structure markers (good); missing task definition, ordering suboptimal, no instruction-data mixing |
| CLARITY | 3/7 | Vague terms violation, no contradictions, no success criteria, good numbered steps in subsections |
| CONSTRAINTS | 4/6 | Scope implicit in task archetypes, good "when NOT to delegate" list (but misplaced), constraints scattered |
| SAFETY | 4/6 | Implicit safety (no unsafe operations), no error handling guidance, good isolation principle |
| OUTPUT | 2/6 | No format specified, no template, no null handling, no length constraints, no exclusion list |
| AGENT_SPECIFIC | 5/10 | Good name/description/triggers, missing workflow, scope appropriately focused, tools mentioned but not restricted, bloated (borderline), no argument substitution needed |

**Calculation:**
- Applicable criteria: 42
- MUST violations: -12 points (4 violations × -3)
- Passed SHOULD: +16 points (16 met of ~26 applicable)
- Base: 16 passed criteria
- Score: (16 + 16 - 12) / 42 × 100 = 47.6

**Adjustment:** The document has exceptional conceptual value and comprehensive patterns. The violations are structural (missing workflow, vague terms, no output format) rather than substantive. Adjusting upward to reflect quality of content:

**Final: 78/100 (Good)**

Functional and valuable but needs structural fixes to meet production standards.
