# System Prompt Anti-Patterns

Comprehensive catalog of anti-patterns to identify during prompt evaluation. Each pattern includes detection method and severity.

---

## Structural Anti-Patterns

### AP-STR-01: Wall of Text
**Severity**: Medium
**Detection**: No structural markers (headers, tags, lists) in prompt >500 words
**Problem**: Claude cannot easily parse priority and organization
**Signal**: Prompt reads as continuous prose without visual hierarchy

### AP-STR-02: Instruction-Data Mixing
**Severity**: High
**Detection**: Examples or data appear inline without clear boundaries
**Problem**: Claude may treat data as instructions or vice versa
**Signal**: Patterns like `Here's an example: [data] Now do the same for...`

### AP-STR-03: Format Buried in Middle
**Severity**: Low
**Detection**: Output format specification not near end of prompt
**Problem**: Format requirements may be overlooked
**Signal**: Format spec appears before task description or examples

### AP-STR-04: Examples After Task
**Severity**: Low
**Detection**: Examples appear after the task/query rather than before
**Problem**: Less effective pattern recognition
**Signal**: `Do X. Here are some examples:` instead of `Examples: ... Now do X.`

### AP-STR-05: Inconsistent Markers
**Severity**: Medium
**Detection**: Mix of XML tags, markdown headers, and plain text sections
**Problem**: Unpredictable structure parsing
**Signal**: `<section>` in one place, `### Section` in another

---

## Clarity Anti-Patterns

### AP-CLR-01: Vague Task Definition
**Severity**: Critical
**Detection**: Task uses words like "analyze", "process", "handle" without specifics
**Problem**: Claude fills gaps with assumptions
**Signal**: `Analyze this data and provide insights.`

### AP-CLR-02: Undefined Qualifiers
**Severity**: High
**Detection**: Uses terms from blacklist without definition
**Problem**: "Good", "appropriate", "relevant" mean different things
**Signal**: `Provide a good summary.` vs `Provide a 3-sentence summary.`

### AP-CLR-03: Contradictory Directives
**Severity**: Critical
**Detection**: Instructions that conflict with each other
**Problem**: Claude must choose one, may choose wrong
**Signal**: `Be thorough in your analysis. Also be concise.`

### AP-CLR-04: Hedged Questions
**Severity**: Medium
**Detection**: Questions that invite hedging
**Problem**: Claude mirrors uncertainty
**Signal**: `What might be the best approach?` vs `What is the best approach?`

### AP-CLR-05: Implicit Success Criteria
**Severity**: Medium
**Detection**: No definition of what "correct" output looks like
**Problem**: No way to verify if output meets requirements
**Signal**: Missing acceptance criteria, success definition

---

## Constraint Anti-Patterns

### AP-CON-01: Implicit Scope
**Severity**: High
**Detection**: No explicit "You handle X, not Y" boundary
**Problem**: Claude may overreach or underperform
**Signal**: Role defined but scope undefined

### AP-CON-02: Assumed Inference
**Severity**: High
**Detection**: Critical limitations not stated explicitly
**Problem**: Claude may not infer intended constraints
**Signal**: `Be careful with sensitive info` (too vague)

### AP-CON-03: Scope-Capability Confusion
**Severity**: Medium
**Detection**: Mixing "don't do" (scope) with "can't do" (capability)
**Problem**: Unclear whether limit is policy or technical
**Signal**: `You cannot access customer data` when you mean "should not"

### AP-CON-04: Scattered Constraints
**Severity**: Low
**Detection**: Constraints spread throughout prompt
**Problem**: Easy to miss constraints during execution
**Signal**: One constraint in intro, another in middle, another at end

---

## Safety Anti-Patterns

### AP-SAF-01: Missing Injection Defense
**Severity**: Critical (for user-data handling prompts)
**Detection**: User data handled without separation or defense instructions
**Problem**: User data may contain malicious instructions
**Signal**: `Process this user input: {user_data}` without boundaries

### AP-SAF-02: Overprivileged Access
**Severity**: Critical
**Detection**: Access to sensitive data without explicit protection rules
**Problem**: Data leakage, unauthorized actions
**Signal**: `You have access to all customer data. Use it to...`

### AP-SAF-03: Missing Error Handling
**Severity**: Medium
**Detection**: No guidance for failure modes
**Problem**: Unpredictable behavior when things go wrong
**Signal**: No "if X fails..." or "when uncertain..." guidance

### AP-SAF-04: Unvalidated Inputs
**Severity**: High
**Detection**: No input validation or rejection criteria
**Problem**: Garbage in, garbage out
**Signal**: Accepts any input format without verification

---

## Output Anti-Patterns

### AP-OUT-01: Undefined Format
**Severity**: High
**Detection**: No output structure specification
**Problem**: Inconsistent output format across invocations
**Signal**: `Summarize this.` without format guidance

### AP-OUT-02: Format Flexibility
**Severity**: Medium
**Detection**: Explicit flexibility in format (`structure as you prefer`)
**Problem**: Unpredictable output structure
**Signal**: `Format the response however makes sense.`

### AP-OUT-03: Missing Edge Cases
**Severity**: Medium
**Detection**: No handling for null/missing/invalid data in output
**Problem**: Inconsistent handling of edge cases
**Signal**: No "if unknown, use..." guidance

### AP-OUT-04: No Preamble Control
**Severity**: Low
**Detection**: No instruction about preamble/postamble
**Problem**: Unwanted introductory or closing text
**Signal**: Getting `Here's the summary:...` when you want just the summary

---

## Tool Anti-Patterns

### AP-TLS-01: Generic Tool Descriptions
**Severity**: High
**Detection**: Tool description uses vague terms
**Problem**: Claude cannot determine when/how to use tool
**Signal**: `"description": "Get data"` or `"parameter": "info"`

### AP-TLS-02: Missing Parameter Examples
**Severity**: Medium
**Detection**: Parameters lack example values
**Problem**: Claude may use wrong format
**Signal**: `"location": {"type": "string"}` without example

### AP-TLS-03: Unmarked Required Parameters
**Severity**: High
**Detection**: No clear required vs optional distinction
**Problem**: Claude may omit required parameters
**Signal**: Missing `required` array or explicit marking

### AP-TLS-04: Missing Usage Context
**Severity**: Medium
**Detection**: No guidance on when to use vs not use tool
**Problem**: Tool may be used inappropriately
**Signal**: Tool defined but no usage conditions

---

## Example Anti-Patterns

### AP-EXM-01: Examples Without Outputs
**Severity**: High
**Detection**: Examples show input only, not expected output
**Problem**: Pattern matching incomplete
**Signal**: `Example input: X` without showing what response should be

### AP-EXM-02: Homogeneous Examples
**Severity**: Medium
**Detection**: All examples follow same pattern, no edge cases
**Problem**: Claude doesn't learn to handle variations
**Signal**: 5 examples that are minor variations of each other

### AP-EXM-03: Excessive Examples
**Severity**: Low
**Detection**: >10 examples for simple classification task
**Problem**: Token waste, diminishing returns
**Signal**: 15 examples when 3-5 would suffice

### AP-EXM-04: Unmarked Examples
**Severity**: Medium
**Detection**: Examples not wrapped in tags or clearly marked
**Problem**: May be confused with instructions
**Signal**: Examples appear as prose without `<example>` tags

---

## Reasoning Anti-Patterns

### AP-RSN-01: Silent Thinking Request
**Severity**: Critical
**Detection**: Asks Claude to think but not show reasoning
**Problem**: Thinking only counts when out loud
**Signal**: `Think carefully but only output the answer.`

### AP-RSN-02: No Uncertainty Handling
**Severity**: High
**Detection**: No permission to decline or express uncertainty
**Problem**: Forces hallucination when uncertain
**Signal**: No "if unsure, say so" or decline permission

### AP-RSN-03: Conclusion Before Evidence
**Severity**: Medium
**Detection**: Asks for answer before reasoning/evidence
**Problem**: May skip verification step
**Signal**: `Answer first, then explain.` vs `Find evidence, then answer.`

---

## Agent-Specific Anti-Patterns

### AP-AGT-01: Vague Trigger Description
**Severity**: High
**Detection**: Description lacks specific trigger phrases
**Problem**: Agent won't be invoked appropriately
**Signal**: `description: Helps with code` vs `description: Use when "reviewing code", "checking for bugs"...`

### AP-AGT-02: Universal Agent
**Severity**: High
**Detection**: Agent tries to do everything
**Problem**: Reduced effectiveness, unclear delegation
**Signal**: `description: A helpful assistant for all tasks`

### AP-AGT-03: Overpermissive Tools
**Severity**: High
**Detection**: Agent has write access when read-only would suffice
**Problem**: Unnecessary risk
**Signal**: Code reviewer agent with Write, Edit tools

### AP-AGT-04: Missing Workflow
**Severity**: High
**Detection**: System prompt lacks step-by-step process
**Problem**: Unpredictable agent behavior
**Signal**: Role defined but no "When invoked: 1. X, 2. Y, 3. Z"

### AP-AGT-05: Bloated Skill
**Severity**: Medium
**Detection**: SKILL.md >500 lines without progressive disclosure
**Problem**: Context bloat when skill loads
**Signal**: Everything in one file, no references/ directory

---

## Detection Checklist

Quick scan for critical anti-patterns:

1. [ ] Vague task? (AP-CLR-01)
2. [ ] Contradictions? (AP-CLR-03)
3. [ ] Implicit constraints? (AP-CON-02)
4. [ ] Missing injection defense? (AP-SAF-01)
5. [ ] Overprivileged? (AP-SAF-02)
6. [ ] Silent thinking? (AP-RSN-01)
7. [ ] No uncertainty out? (AP-RSN-02)
8. [ ] Generic tools? (AP-TLS-01)
9. [ ] Vague agent trigger? (AP-AGT-01)
10. [ ] Universal agent? (AP-AGT-02)
