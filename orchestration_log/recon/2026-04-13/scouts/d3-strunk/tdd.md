# Strunk Analysis: TDD Skill

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 23: "DO NOT write all tests first, then all implementation. This produces tests that verify imagined behavior rather than actual behavior."**

- **Issue**: Passive construction "imagined behavior rather than actual behavior" obscures agency
- **Severity**: Severe - weakens force of the warning
- **Suggestion**: "DO NOT write all tests first, then all implementation. This produces tests that verify what you imagined, not what the code actually does."

**Line 36: "Horizontal slicing causes tests to be insensitive to real changes -- they pass when behavior breaks and fail when behavior is fine."**

- **Issue**: Passive "to be insensitive" - no clear actor
- **Severity**: Severe - dilutes the warning about a critical anti-pattern
- **Suggestion**: "Horizontal slicing makes tests ignore real changes -- they pass when behavior breaks and fail when behavior is fine."

**Line 52: "Not everything can be tested."**

- **Issue**: Passive voice removes agency; who makes this decision?
- **Severity**: Severe - weakens practical guidance
- **Suggestion**: "You cannot test everything." or "Focus testing effort..."

**Line 62: "This proves the path works end-to-end before committing to the full test suite."**

- **Issue**: Passive "before committing" - who commits?
- **Severity**: Moderate - but specified rule R10 makes this severe
- **Suggestion**: "This proves the path works end-to-end before you commit to the full test suite."

**Lines 103-104: "**Good tests** are integration-style: they exercise real code paths through public APIs."**

- **Issue**: Passive "are integration-style" - descriptive rather than active
- **Severity**: Moderate (acceptable in definitional context per Strunk's "topical focus" exception)
- **Note**: This is borderline; passive maintains topical focus on "good tests" throughout paragraph

**Lines 105-106: "**Bad tests** are coupled to implementation: they mock internal collaborators, test private methods, or verify through external means"**

- **Issue**: Passive "are coupled" - descriptive
- **Severity**: Moderate (same topical focus exception applies)
- **Note**: Parallel structure with previous sentence justifies passive here

**Line 119: "Mock at system boundaries only"**

- **Issue**: Imperative without actor (implicit "you")
- **Severity**: Not a violation - imperative mood is active
- **Note**: No change needed

**Line 136: "identify the smallest behavior that can be tested through a public interface"**

- **Issue**: Passive "can be tested"
- **Severity**: Moderate
- **Suggestion**: "identify the smallest behavior you can test through a public interface"

---

## Moderate

### R13 (Needless Words) - Moderate

**Line 17: "A good test reads like a specification."**

- **Issue**: "like a specification" could be more concrete
- **Severity**: Moderate - vague comparison
- **Suggestion**: "A good test specifies behavior." (but this loses nuance; original may be justified)

**Line 44: "Confirm with the user what interface changes are needed."**

- **Issue**: "with the user" is standard phrasing, but "confirm what interface changes are needed" has nested passives
- **Severity**: Moderate
- **Suggestion**: "Ask the user what interface changes they need."

**Line 45: "Confirm which behaviors to test and their priority."**

- **Issue**: "their priority" - possessive adds a word; could be tighter
- **Severity**: Minor
- **Suggestion**: "Confirm which behaviors to test and prioritize them."

**Line 46-47: "Identify opportunities for deep modules — see @references/deep-modules.md for the small-interface, deep-implementation pattern."**

- **Issue**: "see @references/deep-modules.md for" could be tighter
- **Severity**: Minor
- **Suggestion**: "Identify opportunities for deep modules (@references/deep-modules.md explains the small-interface, deep-implementation pattern)."

**Line 52: "Not everything can be tested. Focus testing effort on critical paths and complex logic, not every possible edge case."**

- **Issue**: "testing effort" is nominal form; "every possible edge case" is slightly wordy
- **Severity**: Moderate
- **Suggestion**: "You cannot test everything. Test critical paths and complex logic, not every edge case."

**Lines 55-56: "Write ONE test that confirms ONE thing about the system"**

- **Issue**: "ONE thing about the system" - "about the system" adds little
- **Severity**: Minor
- **Suggestion**: "Write ONE test that confirms ONE behavior"

**Line 89: "**Never refactor while RED.** Get to GREEN first."**

- **Issue**: "Get to GREEN first" - "first" is redundant with "Never...while"
- **Severity**: Minor
- **Suggestion**: "**Never refactor while RED.** Get to GREEN."

**Line 107: "For side-by-side examples of good and bad tests with explanations, see @references/tests.md"**

- **Issue**: "For side-by-side examples...with explanations" is wordy
- **Severity**: Moderate
- **Suggestion**: "See @references/tests.md for examples comparing good and bad tests."

**Line 119: "Mock at system boundaries only — see @references/mocking.md for detailed patterns"**

- **Issue**: "see @references/mocking.md for detailed patterns" - "detailed patterns" is slightly redundant
- **Severity**: Minor
- **Suggestion**: "Mock at system boundaries only (see @references/mocking.md for patterns)"

**Lines 135-136: "If the agentic-delegation skill is available, apply its decomposition patterns to break complex feature implementations into independently testable units, each suitable for a single red-green-refactor cycle."**

- **Issue**: Long sentence with nested subordination; "each suitable for" could be tighter
- **Severity**: Moderate
- **Suggestion**: "If the agentic-delegation skill is available, apply its decomposition patterns to break complex features into independently testable units. Each unit should fit one red-green-refactor cycle."

**Lines 136-138: "Otherwise, decompose manually: identify the smallest behavior that can be tested through a public interface, implement it, then move to the next."**

- **Issue**: Colon followed by three clauses could be tighter
- **Severity**: Minor
- **Note**: This is clear enough; parallel structure justifies length

### R11 (Positive Form) - Moderate

**Line 23: "DO NOT write all tests first, then all implementation."**

- **Issue**: Negative command
- **Severity**: Moderate - but justified as denial of common anti-pattern
- **Note**: This is appropriate use of negative per Strunk's "denial or antithesis" exception
- **No change needed**

**Line 52: "Not everything can be tested."**

- **Issue**: Negative statement
- **Severity**: Moderate
- **Suggestion**: "Test only critical paths and complex logic." (but this loses the cautionary tone; original may be better)

**Line 76: "Do not anticipate future tests."**

- **Issue**: Negative command
- **Severity**: Moderate - but justified in rule list context
- **Note**: In a list of discipline rules, negative prohibitions are appropriate

**Line 89: "**Never refactor while RED.**"**

- **Issue**: Negative with "never"
- **Severity**: Minor - "never" is strong negative (Strunk approves)
- **Note**: No change needed; "never" carries force

**Line 99: "No speculative features added"**

- **Issue**: Negative in checklist
- **Severity**: Minor - checklist context justifies
- **Note**: Could say "Only necessary features added" but negative is clearer here

**Lines 109-116: Red flags (all negative)**

- **Issue**: Entire list is negative ("Mocking internal...", "Testing private...", etc.)
- **Severity**: Moderate - could be reframed positively
- **Suggestion**: Add positive framing: "Green flags indicating good tests: Testing public interfaces, Asserting on outcomes, Test survives refactoring"

**Lines 127-130: "**Do not mock:**" list**

- **Issue**: Negative list
- **Severity**: Minor - contrasts with "**Mock:**" list above, creating antithesis
- **Note**: Parallel structure with positive list justifies this

### R15 (Parallel Construction) - Moderate

**Lines 43-50: Planning phase numbered list**

- **Issue**: Items 1-2 start with "Confirm"; items 3-4 start with "Identify"/"Design"; item 5 starts with "List"; item 6 starts with "Get"
- **Severity**: Moderate - breaks parallel structure
- **Suggestion**: Standardize verb forms:
  1. Confirm interface changes with the user
  2. Confirm behaviors to test and their priority
  3. Identify opportunities for deep modules
  4. Design interfaces for testability
  5. List behaviors to test (not implementation steps)
  6. Get user approval on the plan

**Lines 74-77: Red-green rules**

- **Issue**: Mix of sentence fragments and full sentences
  - "One test at a time." (fragment)
  - "Only enough code to pass the current test." (fragment)
  - "Do not anticipate future tests." (command)
  - "Keep tests focused on observable behavior." (command)
- **Severity**: Moderate
- **Suggestion**: Standardize to imperatives:
  - Write one test at a time
  - Write only enough code to pass the current test
  - Do not anticipate future tests
  - Keep tests focused on observable behavior

**Lines 83-87: Refactor phase**

- **Issue**: Mix of imperatives and infinitives
  - "Extract duplication." (imperative)
  - "Deepen modules..." (imperative)
  - "Apply SOLID principles..." (imperative)
  - "Consider what new code reveals..." (imperative)
  - "Run tests after each refactor step." (imperative)
- **Severity**: None - these are already parallel
- **Note**: Good parallel construction here

**Lines 95-99: Checklist**

- **Issue**: Mix of noun phrases and negatives
  - "Test describes behavior, not implementation" (assertion)
  - "Test uses public interface only" (assertion)
  - "Test would survive internal refactor" (conditional)
  - "Code is minimal for this test" (assertion)
  - "No speculative features added" (negative assertion)
- **Severity**: Moderate
- **Suggestion**: Standardize to assertions:
  - Test describes behavior, not implementation
  - Test uses public interface only
  - Test survives internal refactoring
  - Code is minimal for this test
  - Features are necessary, not speculative

**Lines 109-116: Red flags list**

- **Issue**: Mix of gerunds and noun phrases
  - "Mocking internal collaborators" (gerund)
  - "Testing private methods" (gerund)
  - "Asserting on call counts..." (gerund)
  - "Test breaks when..." (clause)
  - "Test name describes HOW not WHAT" (clause)
  - "Verifying through external means..." (gerund)
- **Severity**: Moderate
- **Suggestion**: Standardize to gerunds:
  - Mocking internal collaborators
  - Testing private methods
  - Asserting on call counts or call order
  - Breaking when refactoring without behavior change
  - Describing HOW in test name, not WHAT
  - Verifying through external means instead of interface

**Lines 122-125 vs 127-130: Mock/Do not mock lists**

- **Issue**: "Mock:" list uses nouns; "Do not mock:" list uses nouns - parallel is good
- **Severity**: None - good parallel structure
- **Note**: Well done

### R12 (Concrete Language) - Moderate

**Line 13: "Philosophy and technique for building software through the red-green-refactor cycle."**

- **Issue**: "Philosophy and technique" is abstract
- **Severity**: Moderate - acceptable in introductory context
- **Note**: The document provides concrete details below, so this abstract intro is justified

**Line 17: "Tests describe WHAT the system does, not HOW it does it."**

- **Issue**: "the system" is generic
- **Severity**: Minor - "system" is standard in TDD discourse
- **Note**: Acceptable

**Line 19: "The litmus test:"**

- **Issue**: "litmus test" is metaphorical, but then gives concrete example
- **Severity**: None - metaphor followed by concrete illustration
- **Note**: Good pattern

**Line 36: "Horizontal slicing causes tests to be insensitive to real changes"**

- **Issue**: "insensitive to real changes" is abstract
- **Severity**: Moderate - then gives concrete examples ("they pass when behavior breaks")
- **Note**: Acceptable because concrete examples follow

**Line 52: "critical paths and complex logic"**

- **Issue**: "critical paths" and "complex logic" are somewhat abstract
- **Severity**: Moderate - could use examples
- **Suggestion**: "critical paths (user authentication, data persistence) and complex logic (calculations, state transitions)"

**Line 103: "Good tests are integration-style: they exercise real code paths through public APIs."**

- **Issue**: "integration-style" and "real code paths" are somewhat abstract
- **Severity**: Moderate - acceptable in definitional context
- **Note**: Document provides concrete examples in referenced file

### R18 (Emphatic Position) - Moderate

**Line 17: "Code can change entirely; tests should not break unless behavior changes."**

- **Issue**: Ends with "unless behavior changes" - conditional clause weakens ending
- **Severity**: Moderate
- **Suggestion**: "Code can change entirely without breaking tests; only behavior changes should break tests." or "Tests should break only when behavior changes, not when code changes."

**Line 19: "If tests break but behavior has not changed, those tests were testing implementation, not behavior."**

- **Issue**: Ends strongly with "not behavior" - good emphatic position
- **Severity**: None - well constructed
- **Note**: Good example of emphatic ending

**Line 36: "Horizontal slicing causes tests to be insensitive to real changes -- they pass when behavior breaks and fail when behavior is fine."**

- **Issue**: Ends with "when behavior is fine" - weak ending
- **Severity**: Moderate
- **Suggestion**: "Horizontal slicing causes tests to be insensitive to real changes -- they fail when behavior is fine and pass when behavior breaks." (puts the worse outcome last for emphasis)

**Line 52: "Focus testing effort on critical paths and complex logic, not every possible edge case."**

- **Issue**: Ends with negative "not every possible edge case"
- **Severity**: Moderate
- **Suggestion**: "Focus testing effort on critical paths and complex logic, ignoring minor edge cases." or reframe entirely: "Test critical paths and complex logic, not every edge case."

**Line 62: "This proves the path works end-to-end before committing to the full test suite."**

- **Issue**: Ends with "before committing to the full test suite" - preparatory rather than emphatic
- **Severity**: Moderate
- **Suggestion**: "This proves the path works end-to-end before you build the full test suite."

**Line 89: "**Never refactor while RED.** Get to GREEN first."**

- **Issue**: Ends with "first" - weak adverb
- **Severity**: Moderate
- **Suggestion**: "**Never refactor while RED.** Get to GREEN." or "**Get to GREEN before refactoring.**"

**Line 104: "They survive refactors because they do not care about internal structure."**

- **Issue**: Ends with "internal structure" - concrete, but could be stronger
- **Severity**: Minor
- **Suggestion**: "They survive refactors by ignoring internal structure." (active verb at end)

**Line 106: "verify through external means (like querying a database directly instead of using the interface)."**

- **Issue**: Ends with parenthetical example - weakens sentence ending
- **Severity**: Moderate
- **Suggestion**: Move example earlier or make it primary: "verify by querying a database directly instead of using the interface"

**Line 132: "use dependency injection (pass dependencies in, do not create them internally)"**

- **Issue**: Ends with parenthetical explanation - weakens ending
- **Severity**: Moderate
- **Suggestion**: "use dependency injection: pass dependencies in rather than creating them internally"

---

## Minor & Stylistic

### R13 (Needless Words) - Minor

**Line 3-8: Description frontmatter**

- **Issue**: Long trigger list with some redundancy
- **Severity**: Stylistic - frontmatter serves discovery purpose
- **Note**: Redundancy may be intentional for matching user queries

**Line 11: "# Test-Driven Development"**

- **Issue**: Title is spelled out fully vs abbreviation elsewhere
- **Severity**: Stylistic - appropriate for heading
- **Note**: No change needed

**Line 13: "Philosophy and technique for building software through the red-green-refactor cycle."**

- **Issue**: "through the" could be "via"
- **Severity**: Minor
- **Note**: "through" is clearer and more natural

**Line 17: "A good test reads like a specification."**

- **Issue**: "like" could be "as" (formal)
- **Severity**: Stylistic
- **Note**: "like" is more natural; no change needed

**Line 20: "Rename an internal function."**

- **Issue**: Could be "Renaming" for parallel with conditional "If tests break"
- **Severity**: Minor
- **Note**: Imperative is appropriate for "litmus test" framing

### R15 (Parallel Construction) - Minor

**Lines 141-146: Reference files list**

- **Issue**: Inconsistent em-dash spacing (all use "—" consistently)
- **Severity**: None - formatting is parallel
- **Note**: Well formatted

**Lines 57-60: Tracer bullet code block**

- **Issue**: Uses arrows and different formatting than Phase 3
- **Severity**: Stylistic - distinguishes phases
- **Note**: Intentional variation is acceptable

### R11 (Positive Form) - Minor

**Line 20: "If tests break but behavior has not changed"**

- **Issue**: Negative construction "has not changed"
- **Severity**: Minor - conditional context justifies
- **Suggestion**: "If tests break when behavior remains unchanged" (positive form "remains")

### R10 (Active Voice) - Minor

**Line 150: "*Originally based on tdd from https://github.com/mattpocock/skills, MIT licensed. Adapted and enhanced for this plugin.*"**

- **Issue**: Passive "based on", "licensed", "Adapted and enhanced"
- **Severity**: Minor - attribution context justifies passive
- **Note**: No change needed; passive is appropriate for credits

---

## Summary

**Overall Assessment**: The TDD skill document is well-written with strong clarity and practical structure. Most violations are minor or justified by context (checklists, rule lists, attributions).

**Critical/Severe Findings**: 7 findings, primarily R10 (active voice) violations that dilute the force of important warnings and guidance. The anti-pattern warnings (lines 23, 36) would benefit most from active voice to strengthen their impact.

**Moderate Findings**: 29 findings across R10, R11, R12, R13, R15, and R18. The most impactful improvements would be:
1. Standardizing parallel construction in lists (planning phase, red-green rules, checklists, red flags)
2. Tightening wordy reference phrases
3. Strengthening sentence endings to place emphatic content in final position
4. Converting some passive constructions to active for vigor

**Minor/Stylistic Findings**: 6 findings, mostly acceptable in context. No significant changes needed.

**Strengths**:
- Clear structure with logical progression
- Good use of concrete examples (code blocks, specific anti-patterns)
- Strong imperative voice in many sections
- Effective use of formatting (bold, bullets, code blocks) to aid comprehension
- Reference system is well-organized

**Recommendations**:
1. **Priority 1** (Severe): Convert passive constructions in anti-pattern warnings to active voice (lines 23, 36, 52)
2. **Priority 2** (Moderate): Standardize parallel construction in all lists
3. **Priority 3** (Moderate): Strengthen sentence endings by placing key points in final position
4. **Priority 4** (Moderate): Tighten wordy phrases, especially around reference links

The document effectively teaches TDD principles. With targeted revisions to the severe findings, it would achieve stronger rhetorical force while maintaining its current clarity and practical value.
