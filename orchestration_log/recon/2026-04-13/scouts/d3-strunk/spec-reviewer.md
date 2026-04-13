# Strunk Analysis: spec-reviewer.md

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 45: "Your posture is adversarial"**
- Issue: Weak "is" construction
- Severity: Moderate - could be more direct
- Revision: "Adopt an adversarial posture" or "Take an adversarial stance"

**Line 58: "claims about completeness" (line 57)**
- Issue: Good active construction overall in the DO/DON'T section
- Severity: None - well executed

**Line 63: "Compare actual implementation to requirements line by line"**
- Issue: Active imperative, strong
- Severity: None

**Line 74: "Find the code that implements it"**
- Issue: Active imperative, strong
- Severity: None

**Line 84: "Claims of implementation that are not actually present in code?"**
- Issue: Passive "are not actually present"
- Severity: Moderate
- Revision: "Claims of implementation that the code does not actually contain?"

**Line 88: "Features built that were not requested?"**
- Issue: Passive "were not requested"
- Severity: Moderate - though checklist format somewhat justifies
- Revision: "Features built that the spec did not request?"

**Line 92: "Requirements interpreted differently than intended?"**
- Issue: Double passive "interpreted" and "intended"
- Severity: Severe
- Revision: "Requirements the implementer interpreted differently than you intended?"

**Line 100: "All [N] requirements verified in code"**
- Issue: Passive "verified"
- Severity: Moderate
- Revision: "You verified all [N] requirements in code"

**Line 108: "not implemented. Expected in [expected location]. Not found."**
- Issue: Passive construction series
- Severity: Moderate - report format somewhat justifies, but could be stronger
- Revision: "not implemented. You expected it in [expected location]. You found nothing."

### R12 (Concrete Language) - Severe

**Line 45: "the implementer finished suspiciously quickly"**
- Issue: "Suspiciously quickly" is concrete and specific
- Severity: None - good

**Line 46: "their report may be incomplete, inaccurate, or optimistic"**
- Issue: Concrete adjectives
- Severity: None

**Line 82: "Missing pieces the implementer claimed to have built"**
- Issue: "Missing pieces" is somewhat vague
- Severity: Moderate
- Revision: "Missing functions, classes, or features the implementer claimed to have built"

**Line 89: "Over-engineering or unnecessary abstractions?"**
- Issue: "Over-engineering" and "unnecessary abstractions" are somewhat abstract
- Severity: Moderate - in context of checklist, acceptable but could be more concrete
- Revision: "Extra base classes, middleware, or abstraction layers the spec didn't require?"

**Line 113: "Extra: [File:line] -- [Feature description] -- not requested in spec"**
- Issue: Template forces concrete file:line references, good structure
- Severity: None

## Moderate

### R11 (Positive Form) - Moderate

**Line 55: "DO NOT: Take the implementer's word..."**
- Issue: Entire section is negative imperatives
- Severity: Moderate - BUT the rhetorical effect of contrasting DO/DON'T is strong
- Revision: Not recommended - the antithesis structure serves purpose (R11 exception)

**Line 84: "not actually present in code"**
- Issue: Negative construction
- Severity: Minor - denial use case
- Revision: Could be "absent from code" but not significantly better

**Line 91: "Missing requirements"**
- Issue: Negative framing
- Severity: Minor - in report template, clear category label
- Revision: Could be "Unfulfilled requirements" but "Missing" is clearer

**Line 108: "not implemented... Not found"**
- Issue: Double negatives
- Severity: Moderate
- Revision: "absent. You expected it in [location]. You found nothing there."

**Line 120: "Verify by reading code, not by trusting reports"**
- Issue: Antithesis construction (not X, but Y)
- Severity: None - justified rhetorical use of negative

### R13 (Needless Words) - Moderate

**Line 45: "Your posture is adversarial: the implementer finished suspiciously quickly and their report may be incomplete, inaccurate, or optimistic"**
- Issue: Efficient, no needless words
- Severity: None

**Line 53: "Critical Rule: Do Not Trust the Report"**
- Issue: Concise
- Severity: None

**Line 63: "Compare actual implementation to requirements line by line"**
- Issue: "line by line" adds specificity, not needless
- Severity: None

**Line 74: "Verify the implementation actually fulfills the requirement (not just partially)"**
- Issue: "(not just partially)" is clarifying, serves purpose
- Severity: None

**Line 99: "If everything matches:"**
- Issue: Concise
- Severity: None

**Line 120: "Include file:line references for every finding. Verify by reading code, not by trusting reports."**
- Issue: Two short, punchy sentences - both necessary
- Severity: None

### R15 (Parallel Construction) - Moderate

**Line 48-51: Core Responsibilities numbered list**
- Issue: All items follow pattern "Verb + object" - good parallel
- Severity: None

**Line 55-65: DO NOT / DO sections**
- Issue: Both sections use parallel bullet structure with verb phrases
- Severity: None - well executed

**Line 83-94: "What to Check" section with three subsections**
- Issue: Each subsection has header + questions, but question formats vary
- Severity: Minor - questions mix statement and interrogative forms
- Revision: Make all sections use consistent question format

**Line 104-118: Output Format for FAIL case**
- Issue: Each category (Missing, Partial, Extra, Misinterpreted) has same structure
- Severity: None - excellent parallel construction

## Minor & Stylistic

### R18 (Emphatic Position) - Moderate

**Line 45: "their report may be incomplete, inaccurate, or optimistic"**
- Issue: Ends with "optimistic" which is the weakest/most interesting term - good emphasis
- Severity: None

**Line 48: "Detect misinterpretations of requirements"**
- Issue: Final item in list, gets emphasis
- Severity: None

**Line 63: "Compare actual implementation to requirements line by line"**
- Issue: Ends with "line by line" - emphatic detail about thoroughness
- Severity: None - good

**Line 74: "Verify the implementation actually fulfills the requirement (not just partially)"**
- Issue: Ends with parenthetical "(not just partially)" 
- Severity: Minor - parenthetical reduces emphasis
- Revision: "Verify the implementation fulfills the requirement completely, not just partially"

**Line 75: "Note if the requirement is missing, partial, or misinterpreted"**
- Issue: Ends with weakest term "misinterpreted" 
- Severity: Minor - could reorder for emphasis
- Revision: "Note if the requirement is misinterpreted, partially met, or missing entirely"

**Line 100: "PASS -- Spec compliant. All [N] requirements verified in code."**
- Issue: Ends strongly with "verified in code" - good
- Severity: None

**Line 108: "not implemented. Expected in [expected location]. Not found."**
- Issue: Ends with "Not found" - emphatic but negative
- Severity: Minor
- Revision: "not implemented. Expected in [expected location]. Code is absent."

**Line 120: "Verify by reading code, not by trusting reports"**
- Issue: Ends with "trusting reports" (the wrong action) rather than "reading code" (correct action)
- Severity: Moderate
- Revision: "Do not trust reports; verify by reading code"

### R10 (Active Voice) - Additional Minor Cases

**Line 69: "Read the specification/requirements completely"**
- Issue: Active imperative - strong
- Severity: None

**Line 72: "Read the actual implementation code using Read and Grep tools"**
- Issue: Active imperative - strong
- Severity: None

## Summary

**Overall Assessment:**
The spec-reviewer.md agent definition demonstrates strong adversarial prose with effective use of contrasting DO/DON'T structures. Main weaknesses:

1. **Passive voice in checklists (R10 - Severe)**: Several question forms use passive constructions ("were not requested," "are not present," "interpreted"). While checklists somewhat justify this, active forms would be stronger.

2. **Double passive constructions (R10 - Severe)**: Line 92 "Requirements interpreted differently than intended" chains two passives, creating confusion about agency.

3. **Some abstract language (R12 - Moderate)**: "Over-engineering," "unnecessary abstractions," "missing pieces" could be more concrete

4. **Emphatic position (R18 - Moderate)**: A few sentences end weakly or with wrong element emphasized

**Strengths:**
- Excellent parallel construction in output format template
- Strong DO/DON'T antithesis structure (justified negative use per R11)
- Concrete, specific verification steps
- Clear adversarial posture with specific directives
- Minimal needless words throughout

**Priority Fixes:**
1. Line 92: "Requirements the implementer interpreted differently than the spec intended" - Critical passive fix
2. Line 84, 88: Reframe checklist questions with active verbs
3. Line 120: "Do not trust reports; verify by reading code" - Emphatic position fix
4. Line 89: Add concrete examples of over-engineering
