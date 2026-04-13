# Reference Optionality: prompt-eval

## Essential References (must inline into SKILL.md)

### evaluation-criteria.md
- **Why essential**: The skill's core function is systematic evaluation against criteria. Every invocation requires determining applicable categories (lines 36-42 of SKILL.md reference this), checking specific criteria (Step 3 workflow), and calculating scores (Step 4). Without the criteria tables, the skill cannot perform its primary function. The skill references this file 4 times in the workflow and includes it in the final output report structure.
- **What to inline**: 
  - Category Applicability Rules (lines 14-29 in criteria file) - needed for Step 2
  - All criteria tables (STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT, TOOLS, EXAMPLES, REASONING, DATA_SEPARATION, AGENT_SPECIFIC) - needed for Step 3
  - Level Definitions (MUST/SHOULD/MUST_NOT) - needed for scoring
  - Scoring Formula - needed for Step 4
  - Quick Checklist - needed for Quick Evaluation Mode (lines 133-145 in SKILL.md)

## Deferrable References (need loading gates)

### anti-patterns.md
- **Why deferrable**: Anti-patterns are a supplementary detection layer. Many evaluations can complete successfully using only criteria violations without anti-pattern scanning. This is a secondary diagnostic tool, not the core evaluation mechanism.
- **Loading gate**: IF the prompt being evaluated has passed basic criteria checks (score > 60%) OR the user requests comprehensive evaluation, THEN read /Users/ryzhakar/pp/claude-skills/prompt-engineering/references/anti-patterns.md
- **Gate placement**: Between Step 3 (systematic evaluation) and Step 4 (scoring). Add conditional step: "3.5. If performing comprehensive evaluation or initial score > 60%, scan for anti-patterns using references/anti-patterns.md"

### ordering-guide.md
- **Why deferrable**: Ordering issues are a specific subset of structural problems. Not every prompt evaluation requires full ordering analysis - simple prompts may not have enough elements to warrant ordering review, and severely broken prompts have higher-priority issues.
- **Loading gate**: IF the prompt being evaluated contains 5+ distinct sections/elements (role, context, constraints, examples, task, etc.) OR criterion STR-5 (ordering) is flagged as violated, THEN read /Users/ryzhakar/pp/claude-skills/prompt-engineering/references/ordering-guide.md
- **Gate placement**: Within Step 3 evaluation, specifically when checking STRUCTURE category criterion STR-5. Modify instruction to: "STR-5 check: If prompt has 5+ sections, consult ordering-guide.md for canonical order"

### term-blacklists.md
- **Why deferrable**: Term scanning is a specific type of clarity check. It's most valuable for prompts that have already passed basic structural validation. Simple or severely broken prompts won't benefit from granular term analysis.
- **Loading gate**: IF evaluating CLARITY category AND the prompt is >100 words AND contains descriptive/analytical language (not purely imperative), THEN read /Users/ryzhakar/pp/claude-skills/prompt-engineering/references/term-blacklists.md
- **Gate placement**: Within Step 3, during CLARITY category evaluation. Modify criterion CLR-2 check: "For prompts >100 words with analytical content, scan against term-blacklists.md"

### improvement-patterns.md
- **Why deferrable**: Improvement patterns are remediation guidance, not evaluation criteria. The skill's stated purpose is evaluation and assessment - improvement is handled by the separate prompt-optimize skill. This reference is only needed when the user explicitly asks "how do I fix this?" rather than just "what's wrong?"
- **Loading gate**: IF the user's request includes fix/improve/remediate keywords ("how to fix", "what changes", "improve this", "remediate") OR the evaluation finds critical violations (score < 60%), THEN read /Users/ryzhakar/pp/claude-skills/prompt-engineering/references/improvement-patterns.md
- **Gate placement**: After Step 5 (report generation), as optional Step 6: "If user requested remediation guidance or critical issues found, consult improvement-patterns.md to add remediation section to report"

## Summary
- Essential: 1 of 5 references
- Deferrable: 4 of 5 references

## Rationale

The evaluation-criteria.md reference contains the core evaluation engine - the applicability rules, criteria tables, severity levels, and scoring formulas. The skill cannot function without this content because every step of the workflow references it directly. The skill's primary output (structured evaluation with scored findings) requires the criteria definitions.

The other four references provide supplementary diagnostic and remediation capabilities that enhance the evaluation but are not required for the core function. Each can be loaded conditionally based on prompt characteristics or user intent:

- **anti-patterns.md**: Secondary diagnostic layer for comprehensive evaluations
- **ordering-guide.md**: Specialized structural analysis for complex multi-section prompts
- **term-blacklists.md**: Granular clarity analysis for substantial analytical content
- **improvement-patterns.md**: Remediation guidance for prompts that need fixing

The current implementation references all files unconditionally via @../../references/ syntax, which loads 1,184 lines of reference material on every invocation. The essential content (evaluation-criteria.md, 197 lines) should be inlined, while the 987 lines of deferrable content can be loaded conditionally, reducing baseline context consumption by ~83%.
