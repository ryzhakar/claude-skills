# Strunk Analysis: implementer.md

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 46: "Your job is to produce working, tested, committed code"**
- Issue: Passive construction "is to produce" weakens the directive
- Severity: Severe - obscures direct agency and action
- Revision: "You must produce working, tested, committed code"

**Line 56: "It is always acceptable to pause and clarify"**
- Issue: Expletive "it is" construction creates weak passive voice
- Severity: Severe - dilutes force of permission
- Revision: "Always pause and clarify rather than guess" or "You may always pause and clarify"

**Line 77: "Bad work is worse than no work"**
- Issue: While grammatically passive in comparison, this is acceptable as aphorism
- Severity: Minor - stylistic choice for emphasis

**Line 86: "Report BLOCKED or NEEDS_CONTEXT with specifics: what is stuck, what was tried"**
- Issue: Passive "what was tried" 
- Severity: Moderate - could be more direct
- Revision: "Report BLOCKED or NEEDS_CONTEXT with specifics: what is stuck, what you tried"

**Line 109: "If issues are found during self-review, fix them"**
- Issue: Passive "are found" obscures agent
- Severity: Severe - implementer is the agent who finds issues
- Revision: "If you find issues during self-review, fix them"

**Line 123: "Work is complete, tested, committed, self-reviewed"**
- Issue: Series of passive participles
- Severity: Moderate - acceptable in status report format, but could be stronger
- Revision: "You completed, tested, committed, and self-reviewed the work"

### R12 (Concrete Language) - Severe

**Line 81: "Understanding code beyond what was provided is necessary"**
- Issue: Abstract "understanding" as subject, vague "code beyond what was provided"
- Severity: Severe - unclear what triggers escalation
- Revision: "You cannot understand dependencies or context from the provided files"

**Line 84: "Progress has stalled after reading file after file without gaining understanding"**
- Issue: "File after file" is somewhat concrete but "gaining understanding" is abstract
- Severity: Moderate - partially concrete
- Revision: "You have read ten files but still cannot determine where the authentication logic lives"

## Moderate

### R13 (Needless Words) - Moderate

**Line 49: "exactly what the task specifies -- nothing more, nothing less"**
- Issue: "nothing more, nothing less" is somewhat redundant with "exactly"
- Severity: Minor - the emphasis serves rhetorical purpose
- Revision: "exactly what the task specifies" (though original has useful emphasis)

**Line 56: "rather than guess"**
- Issue: Efficient, no needless words
- Severity: None

**Line 60: "Read the task specification completely"**
- Issue: "completely" is somewhat redundant with "read" in this imperative context
- Severity: Minor - serves emphasis
- Revision: "Read the entire task specification"

**Line 70: "Follow the file structure defined in the plan"**
- Issue: Concise, no needless words
- Severity: None

**Line 71: "Each file should have one clear responsibility with a well-defined interface"**
- Issue: "one clear responsibility" and "well-defined interface" - both are concrete enough
- Severity: None

**Line 80: "The task requires architectural decisions with multiple valid approaches"**
- Issue: Concrete and specific
- Severity: None

**Line 127: "Never silently produce work that is uncertain"**
- Issue: "silently produce" - both words needed
- Severity: None

### R11 (Positive Form) - Moderate

**Line 49: "nothing more, nothing less"**
- Issue: Negative construction used for emphasis
- Severity: Minor - rhetorical negatives acceptable for antithesis
- Revision: N/A - justified use

**Line 72: "do not restructure things outside the task scope"**
- Issue: Negative instruction
- Severity: Moderate - could be more positive
- Revision: "Restructure only what the task scope covers"

**Line 100: "No overbuilding (YAGNI)?"**
- Issue: Negative question
- Severity: Minor - checklist format justifies negative
- Revision: "Built only what was requested?"

**Line 127: "Never silently produce work that is uncertain"**
- Issue: Double negative ("never" + negative outcome)
- Severity: Moderate
- Revision: "Always surface doubts through the status system"

### R15 (Parallel Construction) - Moderate

**Line 49-53: Core Responsibilities list**
- Issue: Items 1-3 are imperative verb phrases, item 4 is "Report status honestly"
- Severity: Minor - all are imperatives, parallel enough
- Revision: Consider "1. Implement... 2. Follow... 3. Self-review... 4. Report..."

**Line 90-107: Self-Review Checklist structure**
- Issue: Mixed question formats - some are "All requirements...?" others are "Names are clear...?"
- Severity: Moderate - inconsistent question structure
- Revision: Make all questions follow same pattern

**Line 122-125: Status meanings**
- Issue: DONE and DONE_WITH_CONCERNS use "Work is complete" but NEEDS_CONTEXT uses "Cannot proceed"
- Severity: Moderate - should parallel
- Revision: "DONE: Work is complete... / NEEDS_CONTEXT: Work is blocked..."

## Minor & Stylistic

### R18 (Emphatic Position) - Moderate

**Line 46: "Your job is to produce working, tested, committed code that exactly matches the task specification"**
- Issue: Ends with "task specification" rather than the strong constraint
- Severity: Minor - acceptable order
- Alternative: "Your job is to produce code that exactly matches the task specification: working, tested, committed"

**Line 56: "It is always acceptable to pause and clarify rather than guess"**
- Issue: Ends weakly with "guess"
- Severity: Moderate
- Revision: "Rather than guess, pause and clarify—always acceptable"

**Line 77: "Bad work is worse than no work"**
- Issue: Ends emphatically with "no work" which is the weaker element; "bad work" is the point
- Severity: Minor - aphoristic structure acceptable
- Alternative: "No work is better than bad work"

**Line 127: "Never silently produce work that is uncertain"**
- Issue: Ends with abstract "uncertain" rather than concrete action
- Severity: Minor
- Revision: "Never produce uncertain work silently" or better, use positive form

**Line 131: "If the agentic-delegation skill is available, follow its prompt anatomy for structuring work reports and its quality governance patterns for self-assessment"**
- Issue: Sentence ends with abstract "self-assessment" rather than concrete "quality governance patterns"
- Severity: Minor - both are abstract, hard to improve
- Revision: "If the agentic-delegation skill is available, follow its quality governance patterns and prompt anatomy"

### R10 (Active Voice) - Additional Minor Cases

**Line 52: "Report status honestly, including doubts"**
- Issue: Active voice, good
- Severity: None

**Line 91: "All requirements in the spec fully implemented?"**
- Issue: Passive "implemented" acceptable in checklist questions
- Severity: None - justified by format

## Summary

**Overall Assessment:**
The implementer.md agent definition shows generally strong prose with clear imperatives. Main weaknesses cluster around:

1. **Passive voice overuse (R10 - Severe)**: Five significant instances where passive constructions weaken directives or obscure the implementer as agent ("are found," "is to produce," "it is acceptable")

2. **Abstract language (R12 - Severe)**: Two critical instances where escalation triggers are described abstractly rather than concretely

3. **Negative constructions (R11 - Moderate)**: Several instances that could be reframed positively for greater force

4. **Parallel structure inconsistencies (R15 - Moderate)**: Status definitions and checklist questions mix formats

**Strengths:**
- Generally concise with minimal needless words
- Most action steps use clear active imperatives
- Concrete examples in the description section
- Strong structure and organization

**Priority Fixes:**
1. Line 109: "If you find issues" (not "are found") - Critical for agency
2. Line 46: "You must produce" (not "Your job is to produce") - Severe, weakens directive
3. Line 81: Make escalation triggers concrete with specific examples
4. Line 122-125: Parallel status definitions structure
