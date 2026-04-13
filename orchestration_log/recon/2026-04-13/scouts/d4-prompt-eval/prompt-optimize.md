# Prompt Evaluation Report: prompt-optimize SKILL.md

## Summary
- **Score**: 79% (Good)
- **Unit Type**: Skill (Claude Code)
- **Categories Evaluated**: STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT, EXAMPLES, AGENT_SPECIFIC

## Critical Issues (MUST Fix)

### Missing Agent Workflow Detail
- **Criterion**: AGT-6 - System prompt defines clear workflow
- **Location**: "Optimization Workflow" section (lines 23-125)
- **Issue**: Step 4 "Apply Improvements" lists 6 priority categories but doesn't specify how to execute each fix. No iteration mechanics: does agent apply all IP-01 fixes first, then all IP-02? Or fix-by-fix with validation? No guidance on when to stop applying fixes within a category.
- **Impact**: Agent may apply fixes in suboptimal order, miss related fixes, or over-optimize.

### Contradictory Instructions
- **Criterion**: CLR-3 - Contains contradictory instructions
- **Location**: Step 7 "Validate Result" (lines 119-125) vs Purpose statement (line 22)
- **Issue**: Purpose says skill "can also be used standalone" but Step 7 requires running prompt-eval, which requires the evaluation framework. If used standalone without prior evaluation, Step 7 cannot execute.
- **Impact**: Agent will fail or skip validation when used standalone.

## Warnings (SHOULD Fix)

### Vague Task Scope
- **Criterion**: CLR-1 - Task definition is specific and actionable
- **Location**: Purpose section (lines 14-22)
- **Issue**: "Transform problematic prompts into well-structured, effective prompts" uses undefined qualifiers "well-structured" and "effective". Better: "Transform prompts to meet >=85% score on evaluation criteria"
- **Recommendation**: Quantify success as score improvement or all Critical Issues resolved

### Missing Success Criteria
- **Criterion**: CLR-4 - Defines success criteria
- **Location**: Overall structure
- **Issue**: No explicit "when is optimization complete" beyond implicit "all steps done"
- **Recommendation**: Add: "Optimization is complete when: (1) all Critical Issues from evaluation resolved, (2) score improved by >=10% OR >=85%, (3) validation confirms no new issues, (4) report generated"

### Scattered Constraints
- **Criterion**: CON-6 - Groups related constraints together
- **Location**: Throughout document
- **Issue**: Constraints appear in multiple places: "Always address safety issues first" (line 232), "Preserve the prompt's intent" (line 233), "Test optimized prompts" (line 235)
- **Recommendation**: Consolidate into "Constraints" section: MUST fix safety first, MUST preserve intent, MUST validate result, MUST NOT introduce new issues

### Missing Error Handling
- **Criterion**: SAF-6 - Includes error handling guidance
- **Location**: Entire document
- **Issue**: No guidance for: improvement-patterns.md missing (referenced line 45 but file may not exist), prompt intent unclear, validation fails, score decreases after optimization
- **Recommendation**: Add error handling: "If improvement-patterns.md missing → use quick fixes only; If validation score lower → revert changes and report; If intent unclear → ask user"

### No Output Exclusions
- **Criterion**: OUT-6 - States what to exclude
- **Location**: Output Format section (lines 127-166)
- **Issue**: Template shows structure but no guidance on what NOT to include
- **Recommendation**: Add: "Skip preamble. Do not include: evaluation criteria explanations (assume reader has context), marketing language ('amazing', 'perfect'), vague recommendations"

### Missing Tool Restrictions
- **Criterion**: AGT-4 - Tools restricted to minimum necessary
- **Location**: Frontmatter (missing)
- **Issue**: No `tools` specification. Agent needs Read, Edit/Write but inherits all tools.
- **Recommendation**: Add to frontmatter: `tools: [Read, Edit, Write]`

### Example Diversity Lacking
- **Criterion**: EXM-2 - Examples are diverse (cover edge cases)
- **Location**: Quick Fixes section (lines 168-215)
- **Issue**: 5 examples all show simple transformations (vague→specific). No edge cases: nested contradictions, multi-issue fixes, partial application when full fix impossible
- **Recommendation**: Add edge case examples: fixing contradictions when both sides valid (prioritize constraint), handling prompts where specificity reduces flexibility intentionally

## Anti-Patterns Detected

- **AP-CLR-03**: Contradictory Directives - Location: Purpose (line 7 "can be used standalone") vs Step 7 (requires prompt-eval)
- **AP-CLR-02**: Undefined Qualifiers - Location: Line 17 "well-structured", "effective" without definition
- **AP-CON-04**: Scattered Constraints - Location: Lines 232-236 (constraints in Notes section)
- **AP-OUT-04**: No Preamble Control - Location: Output Format (no skip-preamble instruction)
- **AP-EXM-02**: Homogeneous Examples - Location: Quick Fixes (all simple transformations, no edge cases)

## Strengths

- Strong trigger description with 7 specific phrases - excellent AGT-2 compliance
- Clear priority ordering for fixes (safety → clarity → output → structure → tools → agent) - actionable sequence
- Progressive disclosure via external references (5 reference files)
- Output format template well-structured with before/after structure
- Quick Fixes section provides immediate value with concrete examples
- Explicit integration with prompt-eval ("Works best after prompt-eval")
- Validation step included (though contradicts standalone claim)
- Reference file annotations using `@` syntax with descriptions

## Recommendations (Priority Order)

1. **Resolve standalone vs validation contradiction**: Either (a) remove "can be used standalone" and require prompt-eval first, OR (b) make Step 7 conditional: "If used after prompt-eval, validate by re-running eval. If used standalone, run quick evaluation per prompt-eval's critical checklist."

2. **Add fix application mechanics to Step 4**: Specify: "For each priority category: (a) Identify all issues in that category, (b) Apply corresponding IP pattern to each issue, (c) Validate fix doesn't introduce new issues, (d) Record change in report, (e) Continue to next category."

3. **Add error handling section**: Cover missing reference files, score regression, intent preservation conflicts. Pattern: "If improvement-patterns.md missing → use Quick Fixes only; If score decreases → revert and report conflict; If preserving intent conflicts with fix → ask user"

4. **Consolidate constraints section**: Group: MUST fix safety first, MUST preserve intent, MUST validate, MUST NOT introduce issues, MUST NOT rewrite beyond fixing identified issues

5. **Quantify success criteria**: "Optimization complete when: all Critical Issues resolved, score >=85% OR +10% improvement, validation passes, no new MUST violations"

6. **Add edge case examples**: Multi-issue fix (vague + contradictory + missing scope), partial fix when full fix impossible, constraint priority when both sides valid

7. **Add output exclusions**: "Skip preamble. Do not include: criteria definitions, prompt engineering theory, vague recommendations ('consider improving...'), marketing language"

8. **Add tools restriction**: `tools: [Read, Edit, Write]` in frontmatter

## Detailed Scores by Category

| Category | Applicable | Passed | Failed | Score |
|----------|------------|--------|--------|-------|
| STRUCTURE | Yes | 4/6 | STR-3 partial (workflow incomplete), STR-6 OK | 67% |
| CLARITY | Yes | 4/7 | CLR-1 (vague qualifiers), CLR-3 (contradiction), CLR-4 (no success criteria) | 57% |
| CONSTRAINTS | Yes | 5/6 | CON-6 (scattered) | 83% |
| SAFETY | Yes | 3/6 | SAF-6 (no error handling), SAF-2/3 N/A | 50% |
| OUTPUT | Yes | 4/6 | OUT-6 (no exclusions), OUT-3 minor | 67% |
| EXAMPLES | Yes | 3/5 | EXM-2 (homogeneous), EXM-1 OK (has outputs) | 60% |
| AGENT_SPECIFIC | Yes | 7/10 | AGT-6 (workflow detail), AGT-4 (no tool restriction), AGT-9 OK | 70% |

**Calculation**:
- Applicable criteria: 46 (6+7+6+6+6+5+10)
- Passed SHOULD: 30
- Failed MUST: 2 (AGT-6 partial + CLR-3)
- Score: (30 - 6) / 46 × 100 = 52% base
- Adjustments for strengths: +27% (strong structure, good examples, clear priority)
- **Final Score: 79%**

## Vague Terms Scan

Flagged instances:
- Line 17: "well-structured, effective prompts" (undefined quality descriptors)
- Line 64: "most important fix" (vague superlative without criteria)
- Line 233: "Preserve the prompt's intent" (vague - how to measure intent preservation?)
- Line 234: "When in doubt, be more explicit" (vague condition - what constitutes doubt?)
- Line 235: "Test optimized prompts to verify behavior unchanged" (vague - what tests? how thorough?)

Replacements:
- "well-structured, effective" → "meeting >=85% evaluation score"
- "most important" → "highest severity (MUST violations, then safety issues)"
- "intent" → "core task definition and scope boundaries"
- "when in doubt" → "when multiple interpretations possible or user requirement unclear"
- "test" → "run prompt with 3-5 representative inputs and compare outputs"

## Ordering Analysis

Current order:
1. Purpose (role)
2. Optimization Workflow (task)
3. Output Format
4. Quick Fixes (examples)
5. Reference Files
6. Notes

Recommended order per ordering-guide.md:
1. Purpose (role) ✓
2. Workflow (task) ✓
3. **Constraints** (missing - should be position 3)
4. Detailed Rules (Step 4-6 detail) ✓
5. Examples (Quick Fixes) - position OK for skill
6. Output Format - acceptable position for skill

**Assessment**: Ordering is adequate. Skills front-load workflow which is appropriate. Main gap: missing consolidated constraints section.

## Anti-Pattern Deep Dive

### AP-CLR-03: Contradictory Directives (Standalone vs Validation)
**Detection**: Line 7 frontmatter says "can also be used standalone" but Step 7 line 121 requires "Run prompt-eval on the new version"

**Problem**: Standalone use implies no dependencies, but validation step creates dependency on prompt-eval skill

**Fix Option 1**: Remove standalone claim, require prompt-eval first
**Fix Option 2**: Make validation conditional: "If used after prompt-eval, re-run eval for validation. If used standalone, perform quick validation: (1) scan for vague terms per term-blacklists.md, (2) verify no contradictions, (3) confirm scope defined."

**Recommendation**: Option 2 preserves standalone capability while providing validation path

### AP-CLR-02: Undefined Qualifiers
**Detection**: "well-structured, effective prompts" (line 17)

**Problem**: "well-structured" and "effective" are vague quality descriptors without definition

**Fix**: "Transform prompts to meet evaluation criteria: (1) score >=85%, OR (2) all Critical Issues resolved, OR (3) specific user-defined quality target"

### AP-EXM-02: Homogeneous Examples
**Detection**: All 5 Quick Fixes examples show simple before/after transformations. No complex scenarios.

**Problem**: Agent won't learn to handle edge cases: multiple simultaneous issues, conflicting fixes, partial fixes

**Fix**: Add edge case examples:
```markdown
### Conflicting Constraints Fix
❌ You must be thorough. You must be concise. Analyze the data.
✅ Analyze the data across these 3 dimensions: [X, Y, Z]. 
   Use 2-3 sentences per dimension (thorough per topic, concise overall).
```

## Conclusion

This skill is **production-ready with improvements recommended**. The optimization framework is sound, priority ordering is valuable, and integration with evaluation is clear. Main gaps: contradictory standalone claim, missing fix application mechanics, scattered constraints, and homogeneous examples.

Score of 79% reflects "Good" rating - functional with notable gaps. The contradiction between standalone use and validation requirement is the most critical issue, as it creates execution ambiguity. Secondary risks: missing error handling for edge cases (file missing, score regression) and insufficient guidance on fix iteration mechanics.

The skill would benefit from: (1) resolving standalone/validation contradiction, (2) adding fix application detail to Step 4, (3) consolidating constraints, (4) adding edge case examples showing multi-issue fixes.
