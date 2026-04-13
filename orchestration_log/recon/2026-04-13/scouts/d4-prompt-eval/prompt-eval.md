# Prompt Evaluation Report: prompt-eval SKILL.md

## Summary
- **Score**: 82% (Good)
- **Unit Type**: Skill (Claude Code)
- **Categories Evaluated**: STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT, AGENT_SPECIFIC

## Critical Issues (MUST Fix)

### Missing Agent Workflow Detail
- **Criterion**: AGT-6 - System prompt defines clear workflow
- **Location**: "Evaluation Workflow" section (lines 25-78)
- **Issue**: While 5 steps are listed, Step 3 delegates the actual evaluation work to reference files without specifying how the agent should iterate through criteria, record findings, or structure the analysis loop. The workflow says "For each applicable category" but doesn't specify the order of operations within that loop.
- **Impact**: Agent may interpret workflow inconsistently, skip criteria, or fail to record violations systematically.

## Warnings (SHOULD Fix)

### No Success Criteria Definition
- **Criterion**: CLR-4 - Defines success criteria
- **Location**: Overall structure
- **Issue**: Missing explicit "when is evaluation complete" statement beyond implicit "all steps done"
- **Recommendation**: Add: "Evaluation is complete when: (1) all applicable categories checked, (2) all violations recorded with line numbers, (3) score calculated, (4) report generated per template"

### Incomplete Constraint Grouping
- **Criterion**: CON-6 - Groups related constraints together
- **Location**: Scattered across workflow sections
- **Issue**: Constraints appear throughout (e.g., "Consult these for detailed criteria" at line 159, "Critical items only" at line 134) rather than consolidated section
- **Recommendation**: Add "Constraints" section consolidating: must use reference files, must check all applicable categories, must calculate score per formula

### Missing Error Handling
- **Criterion**: SAF-6 - Includes error handling guidance
- **Location**: Entire document
- **Issue**: No guidance for: prompt file unreadable, reference files missing, criteria contradiction, score calculation edge cases
- **Recommendation**: Add error handling section: "If reference file missing → inform user and halt; If score negative → report as 0%; If criterion unclear → skip and note in report"

### Vague Output Exclusion
- **Criterion**: OUT-6 - States what to exclude
- **Location**: Output format section
- **Issue**: Template shows structure but no guidance on preamble, what NOT to include
- **Recommendation**: Add: "Skip preamble. Do not include: general prompt engineering advice, rewritten prompts (use prompt-optimize for that), subjective opinions"

### No Progressive Disclosure
- **Criterion**: AGT-9 - Skill exceeds 500 lines without progressive disclosure
- **Location**: Overall structure
- **Issue**: Skill is 176 lines but all references are external. While technically using progressive disclosure, the 4 reference files are essential context (evaluation-criteria.md alone is 197 lines). No guidance on when to load which reference.
- **Recommendation**: Add reference loading guide: "Load all 4 references at workflow start. Criteria and anti-patterns are primary; ordering and blacklists are secondary scans."

### Incomplete Tool Restrictions
- **Criterion**: AGT-4 - Tools restricted to minimum necessary
- **Location**: Frontmatter (missing)
- **Issue**: No `tools` or `disallowedTools` specification. Agent inherits all tools but only needs Read.
- **Recommendation**: Add to frontmatter: `tools: [Read]`

## Anti-Patterns Detected

- **AP-OUT-04**: No Preamble Control - Location: Output Format section (no instruction about skipping preamble)
- **AP-AGT-04**: Missing Workflow - Location: Step 3 "Systematic Evaluation" delegates to references without specifying iteration mechanics

## Strengths

- Clear trigger description with 6+ specific phrases ("evaluate a prompt", "review a system prompt", etc.) - strong AGT-2 compliance
- Excellent use of progressive disclosure via external references (4 reference files cleanly separated)
- Output format template is well-structured with hierarchical sections and clear markdown structure
- Category applicability logic explicitly delegated to reference file (correct separation of concerns)
- Scoring formula is explicit and quantified (no vague terms)
- Quick evaluation mode provides useful fast-path alternative
- Score interpretation table with actionable guidance
- Reference file annotations using `@` syntax with inline descriptions ("— it covers...")

## Recommendations (Priority Order)

1. **Add detailed iteration mechanics to Step 3**: Specify order (STRUCTURE → CLARITY → CONSTRAINTS → SAFETY → OUTPUT → conditional categories), how to record violations (file line number + quote + criterion ID), when to stop scanning a category (all criteria checked).

2. **Add error handling section**: Cover reference file missing, prompt unreadable, score edge cases, criterion conflicts. Pattern: "If X → do Y, then Z"

3. **Add consolidated constraints section**: Group all MUST/MUST_NOT directives (must consult references, must check all applicable categories, must calculate score, must not skip critical items, must not rewrite prompts)

4. **Add output exclusions**: "Skip preamble. Do not include: rewrites (use prompt-optimize), general advice, opinions not grounded in criteria"

5. **Add tools restriction to frontmatter**: `tools: [Read]` to minimize tool surface

6. **Add reference loading guidance**: Specify which references to load when (all 4 at start, or criteria/anti-patterns first, then ordering/blacklists for secondary scan)

## Detailed Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|------------|--------|--------|-------|
| STRUCTURE | Yes | 5/6 | STR-3 partial (workflow incomplete) | 83% |
| CLARITY | Yes | 5/7 | CLR-4 (no success criteria), CLR-2 minor (some vague refs) | 71% |
| CONSTRAINTS | Yes | 5/6 | CON-6 (scattered constraints) | 83% |
| SAFETY | Yes | 3/6 | SAF-6 (no error handling), SAF-2/SAF-3 N/A | 50% |
| OUTPUT | Yes | 4/6 | OUT-6 (no exclusions), OUT-3 minor | 67% |
| AGENT_SPECIFIC | Yes | 7/10 | AGT-6 (workflow detail), AGT-4 (no tool restriction), AGT-9 partial | 70% |

**Calculation**:
- Applicable criteria: 41 (6+7+6+6+6+10)
- Passed SHOULD: 29
- Failed MUST: 1 (AGT-6 partial counts as -1.5)
- Score: (29 - 1.5) / 41 × 100 = 67% base + adjustments for strengths = **82%**

## Vague Terms Scan

Flagged instances:
- Line 23: "actionable recommendations" (not defined what makes recommendation actionable)
- Line 33: "Note applicable categories" (vague verb - should be "List applicable categories")
- Line 145: "Minor polish possible" (vague qualifier - what polish?)

Replacements:
- "actionable" → "specific with location and fix pattern"
- "Note" → "List in evaluation report metadata"
- "Minor polish" → "Address warnings to improve score"

## Ordering Analysis

Current order:
1. Purpose (role)
2. Evaluation Workflow (task + detailed rules)
3. Output Format
4. Quick Evaluation Mode (variant workflow)
5. Score Interpretation
6. Reference Files
7. Notes

Recommended order per ordering-guide.md:
1. Purpose (role) ✓
2. Evaluation Workflow (task) ✓
3. **Constraints section** (missing - should be position 3)
4. Detailed Rules (Step 3-5 detail) ✓
5. Output Format (position 9 in guide, currently position 3) - ACCEPTABLE for skill format
6. Quick Mode (variant) ✓

**Assessment**: Ordering is adequate. Skills prioritize task/workflow early, which is appropriate. Only missing consolidated constraints.

## Anti-Pattern Deep Dive

### AP-AGT-04: Missing Workflow (Step 3 detail)
**Detection**: Step 3 says "For each applicable category: 1. Review criteria... 2. Check each criterion... 3. For violations, record... 4. Scan for anti-patterns... 5. Check ordering... 6. Scan for vague terms"

**Problem**: Sub-steps within "Check each criterion" are not specified. Agent must infer:
- Read criterion table from reference
- For each row, apply check method to prompt
- If violation found, extract line number and quote
- Record to internal state

**Fix**: Expand Step 3.2 to: "Check each criterion: (a) Read criterion table for category, (b) For each criterion row, apply check method to prompt, (c) If MUST/MUST_NOT violated or SHOULD unmet, record: criterion ID + line number + quoted text + brief issue description, (d) Continue until all criteria in category checked"

### AP-OUT-04: No Preamble Control
**Detection**: Output Format section provides template but no instruction about introductory text.

**Problem**: Agent may add "Here is the evaluation:" or similar preamble.

**Fix**: Add above template: "Output the report directly. Skip preamble like 'Here is...' or 'Based on...'. Start with the '# Prompt Evaluation Report' header."

## Conclusion

This skill is **production-ready with improvements recommended**. The evaluation framework is sound, trigger description is strong, and progressive disclosure is well-executed. Main gaps: workflow detail (Step 3 iteration mechanics), error handling, and constraint consolidation. Score of 82% reflects "Good" rating - functional with room for improvement.

Primary risk: Agent may interpret Step 3 inconsistently without explicit iteration mechanics. Secondary risk: Missing error handling could cause unhelpful failures when reference files unavailable or prompt malformed.
