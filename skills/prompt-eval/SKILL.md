---
name: prompt-eval
description: >
  This skill should be used when the user asks to "evaluate a prompt", "review a system prompt",
  "assess prompt quality", "check if this prompt is good", "audit this prompt", "grade this prompt",
  or "what's wrong with this prompt". Provides systematic evaluation of Claude system prompts
  against Anthropic's official guidance. Returns structured assessment with scores and specific findings.
---

# System Prompt Evaluation

Systematic evaluation of Claude system prompts against criteria derived from Anthropic's official documentation.

## Purpose

Evaluate any Claude system prompt to identify:
- Structural issues and anti-patterns
- Clarity and ambiguity problems
- Missing safety guardrails
- Tool specification issues
- Agent-specific problems (for Claude Code agents/skills)

Produce a structured evaluation report with severity-ranked findings and actionable recommendations.

## Evaluation Workflow

### Step 1: Obtain and Classify the Prompt

1. Read the prompt to evaluate (user provides path or content)
2. Determine prompt type:
   - **API prompt**: Standard Claude API system prompt
   - **Agent prompt**: Claude Code agent (has frontmatter with `name`, `description`)
   - **Skill prompt**: Claude Code skill (SKILL.md format)
3. Note applicable categories (see Step 2)

### Step 2: Determine Applicable Categories

Reference `references/evaluation-criteria.md` for full applicability rules.

**Always apply**: STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT

**Conditionally apply**:
- TOOLS: If tools/functions defined
- EXAMPLES: If examples present or task is complex
- REASONING: If multi-step reasoning required
- DATA_SEPARATION: If handles variable/user data
- AGENT_SPECIFIC: If Claude Code agent or skill

### Step 3: Systematic Evaluation

For each applicable category:

1. Review criteria in `references/evaluation-criteria.md`
2. Check each criterion (MUST / SHOULD / MUST_NOT)
3. For violations, record:
   - Criterion ID (e.g., CLR-2)
   - Severity (from criterion level)
   - Specific location in prompt
   - Brief description of issue

4. Scan for anti-patterns using `references/anti-patterns.md`
5. Check ordering against `references/ordering-guide.md`
6. Scan for vague terms using `references/term-blacklists.md`

### Step 4: Calculate Score

```
Score = (passed / applicable) × 100

Adjustments:
- MUST violation: -3 from numerator
- MUST_NOT violation: -3 from numerator
- SHOULD met: +1 to numerator
```

### Step 5: Generate Report

Produce structured report following output format below.

## Output Format

```markdown
# Prompt Evaluation Report

## Summary
- **Score**: [X]% ([Rating])
- **Prompt Type**: [API / Agent / Skill]
- **Categories Evaluated**: [list]

## Critical Issues (MUST Fix)
<!-- MUST or MUST_NOT violations -->

### [Issue Title]
- **Criterion**: [ID] - [Name]
- **Location**: [Line X or section name]
- **Issue**: [Description]
- **Impact**: [Why this matters]

## Warnings (SHOULD Fix)
<!-- SHOULD criteria not met -->

### [Issue Title]
- **Criterion**: [ID]
- **Location**: [Where in prompt]
- **Issue**: [Description]

## Anti-Patterns Detected
<!-- From anti-patterns.md -->

- **[AP-XXX]**: [Pattern name] - [Location]

## Strengths
<!-- What the prompt does well -->

- [Strength 1]
- [Strength 2]

## Recommendations (Priority Order)
1. [Most important fix]
2. [Second priority]
3. [Third priority]

## Detailed Scores by Category

| Category | Applicable | Passed | Score |
|----------|------------|--------|-------|
| STRUCTURE | Y/N | X/Y | Z% |
| CLARITY | Y/N | X/Y | Z% |
...
```

## Quick Evaluation Mode

For rapid assessment, check critical items only:

1. Task defined? (STR-3)
2. No vague terms? (CLR-2)
3. No contradictions? (CLR-3)
4. Scope defined? (CON-1)
5. No implicit constraints? (CON-5)
6. No unsafe data access? (SAF-5)
7. Data separated? (DAT-2)
8. Agent has workflow? (AGT-6)

If any critical item fails, flag for full evaluation.

## Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Minor polish possible |
| 75-89 | Good | Address warnings |
| 60-74 | Adequate | Fix critical issues |
| 40-59 | Needs Work | Significant revision needed |
| 0-39 | Poor | Consider rewriting |

## Reference Files

Consult these for detailed criteria and patterns:

- **`references/evaluation-criteria.md`** — Complete criteria tables with check methods
- **`references/anti-patterns.md`** — Catalog of anti-patterns with detection methods
- **`references/ordering-guide.md`** — Canonical prompt element ordering
- **`references/term-blacklists.md`** — Vague terms and filler phrases to flag

## Example Evaluation

See `examples/sample-evaluation.md` for a complete evaluation report example.

## Notes

- Evaluation is against Anthropic's official guidance, not subjective preference
- Some criteria are conditional — only apply when relevant
- Critical issues should block deployment; warnings are improvement opportunities
- Use the prompt-optimize skill to fix identified issues
