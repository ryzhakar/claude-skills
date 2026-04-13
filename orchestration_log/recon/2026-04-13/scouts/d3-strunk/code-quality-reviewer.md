# Strunk Analysis: code-quality-reviewer.md

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 43: "Your review is scoped to a specific git range"**
- Issue: Passive "is scoped"
- Severity: Moderate
- Revision: "Scope your review to a specific git range"

**Line 50: "Categorize findings by severity with actionable recommendations"**
- Issue: Active imperative - good
- Severity: None

**Line 51: "Acknowledge strengths -- balanced feedback is more useful than pure criticism"**
- Issue: Passive "is more useful"
- Severity: Minor - this is comparing abstract concepts, passive acceptable
- Revision: Could be active but not necessary: "balanced feedback helps more than pure criticism"

**Line 65: "Code Quality: Clean separation of concerns?"**
- Issue: Adjective phrase, not passive - acceptable in checklist
- Severity: None

**Line 71: "Names are clear and descriptive?"**
- Issue: Passive "are"
- Severity: Minor - checklist question format
- Revision: "Do names clearly describe what they reference?"

**Line 74: "Sound design decisions?"**
- Issue: Fragment, not passive
- Severity: None

**Line 77: "Are units decomposed so they can be understood and tested independently?"**
- Issue: Passive "are decomposed" and "can be understood"
- Severity: Moderate - obscures who decomposes and understands
- Revision: "Can you understand and test each unit independently?"

**Line 78: "Is the implementation following the file structure from the plan (if applicable)?"**
- Issue: Progressive "is following" - not technically passive but weak
- Severity: Minor
- Revision: "Does the implementation follow the file structure from the plan?"

**Line 79: "Did this change create files that are already large or significantly grow existing files?"**
- Issue: Mixed - "Did create" is active but "are already large" is passive
- Severity: Minor - acceptable
- Revision: Could be "Did this change create large files or significantly grow existing files?"

**Line 82: "Tests actually test behavior (not just mock behavior)?"**
- Issue: Active "test" - good
- Severity: None

**Line 83: "Edge cases covered in tests?"**
- Issue: Passive "covered"
- Severity: Moderate
- Revision: "Do tests cover edge cases?"

**Line 88: "No hardcoded secrets or credentials?"**
- Issue: Passive participle "hardcoded"
- Severity: Minor - acceptable in security checklist
- Revision: "Does the code hardcode any secrets or credentials?"

**Line 89: "Backward compatibility considered?"**
- Issue: Passive "considered"
- Severity: Moderate
- Revision: "Does the implementation consider backward compatibility?"

**Line 118: "**Issue:** [What is wrong]"**
- Issue: Template uses passive copula; when filled in, could be active or passive
- Severity: Minor - template flexibility acceptable

**Line 145: "Focus on what THIS change contributed (not pre-existing issues)"**
- Issue: Passive "contributed" - acceptable as past participle modifying "what"
- Severity: None

### R12 (Concrete Language) - Severe

**Line 66: "Proper error handling (not swallowed, not generic)?"**
- Issue: "Proper" is vague; "not swallowed, not generic" adds some concreteness
- Severity: Moderate
- Revision: "Error handling uses specific messages and propagates errors?"

**Line 68: "Type safety (if applicable)?"**
- Issue: Abstract concept without concrete guidance
- Severity: Moderate - for a checklist, needs more detail
- Revision: "Types prevent invalid data? Type annotations complete?"

**Line 69: "DRY principle followed?"**
- Issue: Jargon without concrete description
- Severity: Moderate
- Revision: "No duplicated logic that could be extracted to functions?"

**Line 70: "Edge cases handled?"**
- Issue: Very vague - which edge cases?
- Severity: Severe - needs concrete examples
- Revision: "Edge cases handled (null values, empty arrays, boundary conditions)?"

**Line 74: "Sound design decisions?"**
- Issue: "Sound" is subjective/abstract
- Severity: Moderate
- Revision: "Design decisions support the requirements without over-engineering?"

**Line 75: "Does each file have one clear responsibility?"**
- Issue: "One clear responsibility" is somewhat abstract but acceptable (SRP)
- Severity: Minor

**Line 76: "Are units decomposed so they can be understood and tested independently?"**
- Issue: "Decomposed" and "understood independently" are somewhat abstract
- Severity: Moderate
- Revision: "Can you read and test each function/class without understanding the entire file?"

**Line 90: "No obvious performance issues?"**
- Issue: "Obvious" is vague
- Severity: Moderate
- Revision: "No N+1 queries, infinite loops, or unnecessary recomputations?"

**Line 93: "Bugs, security vulnerabilities, data loss risks, broken functionality. These block merge."**
- Issue: Good concrete categories
- Severity: None

**Line 96: "Architecture problems, missing error handling, test gaps, missing features."**
- Issue: Concrete categories
- Severity: None

**Line 99: "Code style, optimization opportunities, documentation improvements."**
- Issue: Concrete categories
- Severity: None

**Line 154: "Unclear code intent: Note the ambiguity and request clarification rather than guessing"**
- Issue: Concrete directive
- Severity: None

## Moderate

### R11 (Positive Form) - Moderate

**Line 66: "Proper error handling (not swallowed, not generic)?"**
- Issue: Double negative construction
- Severity: Moderate
- Revision: "Error handling uses specific messages and propagates errors up the call stack?"

**Line 82: "Tests actually test behavior (not just mock behavior)?"**
- Issue: Parenthetical negative
- Severity: Minor - clarifying aside acceptable
- Revision: "Tests verify behavior through real interactions?"

**Line 88: "No hardcoded secrets or credentials?"**
- Issue: Negative question
- Severity: Minor - security checklist appropriately uses negative
- Revision: Could be positive but "no X" is clearer for security: "Secrets use environment variables?"

**Line 89: "Backward compatibility considered?"**
- Issue: Positive form - good
- Severity: None

**Line 90: "No obvious performance issues?"**
- Issue: Negative question
- Severity: Minor
- Revision: "Performance is acceptable for expected load?"

**Line 141: "DO NOT: Say 'looks good' without reading the code"**
- Issue: Negative imperative list
- Severity: Minor - DO/DO NOT antithesis serves purpose (R11 exception)

**Line 151: "Give feedback on code not in the diff range"**
- Issue: In "DO NOT" section, using negative; appropriate for prohibitions
- Severity: None - justified

### R13 (Needless Words) - Moderate

**Line 43: "Your review is scoped to a specific git range -- review only what changed, not the entire codebase"**
- Issue: Second clause explains first; some redundancy but serves clarity
- Severity: Minor
- Revision: "Review only the specific git range, not the entire codebase"

**Line 51: "balanced feedback is more useful than pure criticism"**
- Issue: "more useful" vs just "useful" - comparison serves purpose
- Severity: None

**Line 75: "Does each file have one clear responsibility?"**
- Issue: "one clear" - both words needed
- Severity: None

**Line 93-94: "Bugs, security vulnerabilities, data loss risks, broken functionality. These block merge."**
- Issue: Two sentences where one could work, but short punchy style effective
- Severity: None

**Line 107: "## Code Quality Review"**
- Issue: Efficient header
- Severity: None

**Line 108: "[2-3 sentence overview of changes and overall quality assessment]"**
- Issue: Template instruction clear and concise
- Severity: None

**Line 148: "Be specific (file:line references, not vague)"**
- Issue: Parenthetical adds clarity
- Severity: None

### R15 (Parallel Construction) - Moderate

**Line 46-51: Core Responsibilities numbered list**
- Issue: Items 1-4 are "Verb + object" imperatives; item 5 shifts to "Acknowledge strengths -- [explanation]"
- Severity: Minor - mostly parallel
- Revision: "5. Acknowledge strengths to balance criticism"

**Line 65-71: Code Quality checklist**
- Issue: Mix of fragments ("Clean separation"), questions with copula ("Names are clear"), and questions without ("Edge cases handled?")
- Severity: Moderate - inconsistent structure
- Revision: Make all questions follow same format: "Is there clean separation?" or "Clean separation of concerns?"

**Line 74-79: Architecture checklist**
- Issue: Mix of fragments ("Sound design decisions?") and full questions ("Does each file...")
- Severity: Moderate
- Revision: Standardize question format

**Line 82-85: Testing checklist**
- Issue: Mix of full questions and fragments
- Severity: Moderate
- Revision: Standardize

**Line 88-90: Production Readiness checklist**
- Issue: All negative questions ("No X?")
- Severity: None - parallel within section

**Line 140-152: DO / DO NOT sections**
- Issue: Both use bullet points with imperative phrases
- Severity: None - good parallel

**Line 113-130: Issue template structure**
- Issue: Critical uses "File/Issue/Impact/Fix" structure; Important uses "File/Issue/Fix"; Minor uses "File/Suggestion"
- Severity: Moderate - should parallel
- Revision: Use same field structure for all severity levels

## Minor & Stylistic

### R18 (Emphatic Position) - Moderate

**Line 43: "review only what changed, not the entire codebase"**
- Issue: Ends with "entire codebase" (what NOT to review) rather than "what changed" (what to review)
- Severity: Moderate
- Revision: "review what changed, not the entire codebase" or "scope to changes, not the entire codebase"

**Line 51: "balanced feedback is more useful than pure criticism"**
- Issue: Ends with "pure criticism" (the wrong approach) rather than "balanced feedback" (right approach)
- Severity: Moderate
- Revision: "pure criticism is less useful than balanced feedback"

**Line 66: "Proper error handling (not swallowed, not generic)?"**
- Issue: Ends with parenthetical negatives, weak position
- Severity: Minor
- Revision: "Error handling that propagates with specific messages?"

**Line 76: "Are units decomposed so they can be understood and tested independently?"**
- Issue: Ends with "independently" - good emphasis on key quality
- Severity: None

**Line 93-94: "Bugs, security vulnerabilities, data loss risks, broken functionality. These block merge."**
- Issue: Second sentence ends emphatically with "block merge" - strong
- Severity: None - good

**Line 107-108: "Summary: [2-3 sentence overview of changes and overall quality assessment]"**
- Issue: Template ends with "quality assessment" - appropriate emphasis
- Severity: None

**Line 118-120: Critical issue template ends with "Fix: [How to fix it]"**
- Issue: Ends with fix (solution) - emphatic and constructive
- Severity: None - good

**Line 134: "Assessment: **Ready to merge:** [Yes / With fixes / No]"**
- Issue: Ends with the verdict - emphatic
- Severity: None - excellent

**Line 148: "Be specific (file:line references, not vague)"**
- Issue: Ends with "not vague" - negative and weak
- Severity: Minor
- Revision: "Be specific with file:line references, not vague statements"

**Line 154: "Note the ambiguity and request clarification rather than guessing"**
- Issue: Ends with "guessing" (wrong action) not "clarification" (right action)
- Severity: Moderate
- Revision: "Rather than guess, note the ambiguity and request clarification"

### R10 (Active Voice) - Additional Minor Cases

**Line 55: "Identify the scope:"**
- Issue: Active imperative - strong
- Severity: None

**Line 58: "Read the changed files using Read and Grep tools"**
- Issue: Active imperative - strong
- Severity: None

**Line 59: "Evaluate against the quality checklist below"**
- Issue: Active imperative - strong
- Severity: None

**Line 140: "DO: Categorize by actual severity"**
- Issue: Active imperative - strong
- Severity: None

## Summary

**Overall Assessment:**
The code-quality-reviewer.md agent definition provides comprehensive review guidance with well-structured severity tiers and output templates. Main weaknesses:

1. **Passive checklist questions (R10 - Moderate)**: Numerous checklist items use passive constructions ("are clear," "covered," "considered") instead of active agent-focused questions.

2. **Abstract checklist items (R12 - Severe)**: Several quality checks use vague terms ("proper," "sound," "obvious," "edge cases") without concrete examples or specific criteria.

3. **Parallel construction breaks (R15 - Moderate)**: Checklists mix question formats (fragments vs. full questions vs. copula questions); issue templates use different field structures across severity levels.

4. **Emphatic position problems (R18 - Moderate)**: Several sentences end with the wrong element or negative constructions, weakening impact.

**Strengths:**
- Clear severity taxonomy with concrete examples (Critical vs. Important vs. Minor)
- Comprehensive quality checklist covering multiple dimensions
- Strong DO/DO NOT antithesis structure
- Actionable output format template
- Balanced approach (acknowledge strengths + identify issues)
- Scope discipline (review changes, not entire codebase)

**Priority Fixes:**
1. Lines 70, 66, 90: Add concrete examples to abstract checklist items (edge cases, proper error handling, performance issues)
2. Lines 65-90: Standardize checklist question format to parallel structure
3. Lines 113-130: Use consistent field structure for all severity level templates
4. Lines 77, 83, 89: Convert passive checklist questions to active: "Can you test X independently?" not "Are units decomposed?"
5. Line 154: Fix emphatic position - "Rather than guess, request clarification"
