# Core Points: prompt-eval

## Iteration 1

**Point**: Evaluation must be grounded in Anthropic's official documentation, not subjective preference, using systematic criteria-based assessment with severity rankings.

**Evidence**:
1. SKILL.md line 12: "Systematic evaluation of Claude system prompts against criteria derived from Anthropic's official documentation."
2. evaluation-criteria.md lines 5-9: Lists official sources as Claude API Documentation, Claude Code Documentation, and Anthropic Prompt Engineering Interactive Tutorial as the exclusive grounding.
3. SKILL.md line 172: "Evaluation is against Anthropic's official guidance, not subjective preference" - explicitly states this as the fundamental principle.

## Iteration 2

**Point**: Vague, undefined qualitative terms (like "good", "appropriate", "thorough") in prompts are critical failures that require specific, measurable criteria instead.

**Evidence**:
1. term-blacklists.md lines 7-43: Comprehensive catalog of vague terms across quality descriptors, quantity descriptors, evaluation terms, and timing terms that require definition.
2. evaluation-criteria.md line 61 (CLR-2, MUST_NOT level): "Contains undefined vague terms" with explicit check method "Search for terms in blacklist" - this is a critical violation worth -3 points.
3. anti-patterns.md lines 49-53 (AP-CLR-02, High severity): "Undefined Qualifiers" pattern with example showing "Provide a good summary" as problematic vs "Provide a 3-sentence summary" as correct.

## Iteration 3

**Point**: Data and instructions must be separated with explicit XML boundaries to prevent prompt injection attacks where user data could be misinterpreted as commands.

**Evidence**:
1. evaluation-criteria.md line 140 (DAT-2, MUST_NOT level): "Instructions mixed with data without boundaries" asking "Could data be misinterpreted as instructions?" - critical violation.
2. anti-patterns.md lines 15-20 (AP-STR-02, High severity): "Instruction-Data Mixing" flagged when "Claude may treat data as instructions or vice versa" with detection pattern looking for inline examples without boundaries.
3. improvement-patterns.md lines 351-388 (IP-09): Entire pattern dedicated to separating data from instructions, showing before/after with injection attempt neutralized by XML tags.

## Iteration 4

**Point**: "Silent thinking" requests (asking Claude to think but not show reasoning) are critical failures because thinking only improves accuracy when made explicit and visible.

**Evidence**:
1. anti-patterns.md lines 217-222 (AP-RSN-01, Critical severity): "Silent Thinking Request" with signal "Think carefully but only output the answer" and problem statement "Thinking only counts when out loud."
2. ordering-guide.md line 176: "Critical note: Thinking only counts when out loud. Silent thinking has no effect" - emphasized as a critical note in canonical ordering guidance.
3. evaluation-criteria.md line 131 (RSN-2, MUST_NOT level): "Asks for silent thinking" as a critical violation, checking for "think silently and output only" patterns.

## Iteration 5

**Point**: Tool and parameter descriptions must be specific with concrete examples rather than generic terms, as vague tool specs prevent Claude from determining when and how to use tools correctly.

**Evidence**:
1. evaluation-criteria.md line 109 (TLS-2, MUST level): "Parameters have specific descriptions with examples" checking for "e.g., San Francisco, CA" style examples - this is required, not optional.
2. anti-patterns.md lines 161-167 (AP-TLS-01, High severity): "Generic Tool Descriptions" with signal showing "description: Get data" or "parameter: info" as failures because "Claude cannot determine when/how to use tool."
3. improvement-patterns.md lines 214-258 (IP-06): Shows transformation from "description: Search for things" to detailed description with parameter examples like "e.g., 'wireless headphones'" demonstrating the required specificity level.

## Rank Summary

1. Evaluation must be grounded in Anthropic's official documentation, not subjective preference, using systematic criteria-based assessment with severity rankings.
2. Vague, undefined qualitative terms in prompts are critical failures that require specific, measurable criteria instead.
3. Data and instructions must be separated with explicit XML boundaries to prevent prompt injection attacks.
4. "Silent thinking" requests are critical failures because thinking only improves accuracy when made explicit.
5. Tool descriptions must be specific with concrete examples rather than generic terms to enable correct usage.
