# Strunk Elements Analysis: systematic-debugging

Evaluated against R10 (active voice), R11 (positive form), R12 (concrete language), R13 (needless words), R15 (parallel construction), R18 (emphatic position).

---

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 13: "Random fixes waste time and create new bugs."**
- **Issue**: Abstract nouns ("fixes", "bugs") as agents performing actions
- **Rule**: Active voice names actors doing actions; prefer concrete agents
- **Severity**: Severe - obscures actual human agency in debugging
- **Revision**: "When developers apply random fixes, they waste time and create new bugs."

**Line 22: "If Phase 1 has not been completed, no fix may be proposed."**
- **Issue**: Passive "has not been completed" + passive "may be proposed"
- **Rule**: Active voice clarifies who performs actions
- **Severity**: Severe - critical directive needs clarity about actor
- **Revision**: "Complete Phase 1 before proposing any fix."

**Line 44: "Error messages often contain the exact solution."**
- **Issue**: "contain" weakens agency; messages don't actively contain, they state
- **Rule**: Active voice with proper agent
- **Severity**: Severe - passive construction in critical instruction
- **Revision**: "Error messages often state the exact solution." OR "Read error messages carefully—they often state the exact solution."

**Line 56: "When a system has multiple components... add diagnostic instrumentation BEFORE proposing fixes"**
- **Issue**: Imperative buried after conditional; passive "has"
- **Rule**: Active voice for commands
- **Severity**: Severe - critical procedural instruction
- **Revision**: "Multi-component systems require diagnostic instrumentation before you propose fixes. Add instrumentation to:"

**Line 113: "Did it work? If yes, proceed to Phase 4. If no, form a NEW hypothesis. Do not add more fixes on top."**
- **Issue**: "Did it work?" - passive construction, unclear referent
- **Rule**: Active voice clarifies what/who performed action
- **Severity**: Severe - test verification step needs precision
- **Revision**: "Did the change fix the issue? If yes, proceed to Phase 4. If no, form a NEW hypothesis. Do not stack additional fixes."

**Line 158: "After fixing the root cause, add validation at every layer the bad data passed through."**
- **Issue**: Passive "the bad data passed through"
- **Rule**: Active voice for concrete process description
- **Severity**: Severe - implementation guidance needs clarity
- **Revision**: "After fixing the root cause, add validation at every layer through which the bad data passed."

---

## Moderate

### R12 (Concrete Language) - Moderate

**Line 13: "Quick patches mask underlying issues."**
- **Issue**: Abstract "underlying issues" - what specific things are masked?
- **Rule**: Prefer concrete to abstract; definite to vague
- **Severity**: Moderate - weakens rhetorical force
- **Revision**: "Quick patches mask the root causes."

**Line 30: "Just one quick fix" seems obvious**
- **Issue**: Quoted phrase lacks concrete context
- **Rule**: Specific examples create vivid understanding
- **Severity**: Moderate - teaching moment weakened by abstraction
- **Revision**: ""Just add a null check" seems obvious" OR ""Just restart the service" seems obvious"

**Line 48: "If not reproducible, gather more data -- do not guess."**
- **Issue**: "gather more data" - abstract instruction, what specific data?
- **Rule**: Definite, specific, concrete language
- **Severity**: Moderate - practical guidance needs specificity
- **Revision**: "If not reproducible, gather more evidence: logs, timestamps, environment state, request payloads. Do not guess."

**Line 96: "What assumptions does it make?"**
- **Issue**: "it" - vague pronoun, "assumptions" abstract
- **Rule**: Concrete, specific language
- **Severity**: Moderate - question needs specificity
- **Revision**: "What does the broken code assume about inputs, state, environment, or dependencies?"

**Line 118: "Say "I do not understand X." Do not pretend to know."**
- **Issue**: "X" placeholder; "pretend to know" vague
- **Rule**: Concrete examples
- **Severity**: Moderate - teachable moment needs concreteness
- **Revision**: "Say "I do not understand why this callback fires twice." Do not propose fixes when understanding is incomplete."

### R13 (Needless Words) - Moderate

**Line 3-8 (frontmatter description):**
```
This skill should be used when the user reports a "bug", "test failure", "unexpected behavior",
"error", "crash", "flaky test", asks to "debug this", "find root cause", "why is this failing",
"fix this error", or when multiple fix attempts have failed. Provides a mandatory 4-phase
root cause protocol that prevents random fixes and symptom patching. Apply BEFORE proposing
any fix, especially under time pressure.
```
- **Issue**: 72 words; trigger list dominates; "Provides" buries lede
- **Rule**: Omit needless words; every word must tell
- **Severity**: Moderate - metadata verbosity reduces signal
- **Revision**: "Mandatory 4-phase root cause protocol for bugs, test failures, errors, or unexpected behavior. Prevents random fixes and symptom patching. Apply BEFORE proposing any fix, especially when multiple attempts have failed or time pressure tempts guessing."

**Line 41: "BEFORE attempting ANY fix:"**
- **Issue**: "attempting" is wordy vs. "attempting"
- **Rule**: Omit needless words
- **Severity**: Moderate - could be more direct
- **Revision**: "BEFORE proposing ANY fix:"

**Line 59: "For EACH component boundary:"**
- **Issue**: "For EACH" - "For" is needless
- **Rule**: Economy
- **Severity**: Moderate
- **Revision**: "At EACH component boundary:"

**Line 84: "Locate similar working code in the same codebase."**
- **Issue**: "in the same codebase" is implied by "similar"
- **Rule**: Omit needless words
- **Severity**: Moderate
- **Revision**: "Locate similar working code."

**Line 107: "Make the SMALLEST possible change to test the hypothesis."**
- **Issue**: "possible" is redundant with "smallest"
- **Rule**: Every word must tell
- **Severity**: Moderate
- **Revision**: "Make the SMALLEST change to test the hypothesis."

**Line 124: "Write the simplest possible reproduction as an automated test."**
- **Issue**: "possible" again redundant
- **Rule**: Omit needless words
- **Severity**: Moderate
- **Revision**: "Write the simplest reproduction as an automated test."

**Line 129: "Address the root cause identified in Phase 3."**
- **Issue**: "identified in Phase 3" - implied by context
- **Rule**: Omit needless words when context suffices
- **Severity**: Moderate
- **Revision**: "Address the root cause."

**Line 194: "Emergency, no time for process" | "Systematic debugging is FASTER than guess-and-check thrashing."**
- **Issue**: "guess-and-check thrashing" - three words where one or two suffice
- **Rule**: Concise vigor
- **Severity**: Moderate
- **Revision**: "Systematic debugging is FASTER than thrashing through guesses."

### R11 (Positive Form) - Moderate

**Line 22: "no fix may be proposed"**
- **Issue**: Negative form; tells what NOT to do
- **Rule**: Put statements in positive form
- **Severity**: Moderate - loses force through negation
- **Revision**: "Complete Phase 1 before proposing fixes."

**Line 34: "Do not skip when:"**
- **Issue**: Negative instruction header
- **Rule**: Positive form preferred
- **Severity**: Moderate
- **Revision**: "Apply even when:" OR "Required when:"

**Line 49: "do not guess"**
- **Issue**: Negative command
- **Rule**: State what TO do, not what NOT to
- **Severity**: Moderate - paired with positive "gather more data" helps, but could be stronger
- **Revision**: "gather more evidence until reproducible"

**Line 92: "Do not assume "that cannot matter.""**
- **Issue**: Double negative construction
- **Rule**: Positive form for clarity
- **Severity**: Moderate
- **Revision**: "Assume every difference might matter."

**Line 112: "Do not fix multiple things at once."**
- **Issue**: Negative instruction
- **Rule**: Positive form
- **Severity**: Moderate
- **Revision**: "Fix one thing at a time."

**Line 118: "Do not pretend to know."**
- **Issue**: Negative phrasing
- **Rule**: Positive form
- **Severity**: Moderate
- **Revision**: "Acknowledge gaps in understanding."

**Line 130: "No "while I'm here" improvements. No bundled refactoring."**
- **Issue**: Two negative prohibitions
- **Rule**: State positive directive
- **Severity**: Moderate
- **Revision**: "Change only what addresses the root cause. Defer improvements and refactoring."

**Line 196: "I'll write test after confirming fix works" | "Untested fixes do not stick."**
- **Issue**: Negative construction
- **Rule**: Positive assertion
- **Severity**: Moderate
- **Revision**: "Tests prove fixes work and prevent regressions."

### R15 (Parallel Construction) - Moderate

**Lines 28-32:**
```
Apply especially when:
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- Multiple fixes have already been attempted
- The previous fix did not work
- The issue is not fully understood
```
- **Issue**: Mixed construction - some noun phrases, some clauses; tense inconsistency
- **Rule**: Coordinate ideas require similar form
- **Severity**: Moderate - list structure weakened
- **Revision**:
```
Apply especially when:
- Time pressure makes guessing tempting
- A quick fix seems obvious
- Multiple fixes have already failed
- The previous fix did not work
- The issue is not fully understood
```

**Lines 42-52 (Phase 1 subsections):**
```
### 1. Read Error Messages Carefully
### 2. Reproduce Consistently
### 3. Check Recent Changes
### 4. Gather Evidence in Multi-Component Systems
### 5. Trace Data Flow
```
- **Issue**: Headers vary between imperatives and noun phrases
- **Rule**: Parallel structure in coordinate series
- **Severity**: Moderate
- **Revision**: All imperatives OR all gerunds:
```
### 1. Read Error Messages Carefully
### 2. Reproduce the Issue Consistently
### 3. Check Recent Changes
### 4. Gather Evidence in Multi-Component Systems
### 5. Trace Data Flow Backward
```

**Lines 83-96 (Phase 2 subsections):**
```
### 1. Find Working Examples
### 2. Compare Against References
### 3. Identify Differences
### 4. Understand Dependencies
```
- **Issue**: #2 breaks pattern with "Compare Against" vs imperative verb alone
- **Rule**: Parallel construction
- **Severity**: Moderate
- **Revision**: "Compare With References" OR restructure all to match that form

**Lines 167-177 (Red Flags list):**
```
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems:" (listing fixes without investigation)
- Proposing solutions before tracing data flow
- "One more fix attempt" (when 2+ already tried)
- Each fix reveals a new problem in a different place
```
- **Issue**: Mix of quoted thoughts and descriptive phrases
- **Rule**: Express coordinate ideas in similar form
- **Severity**: Moderate - pattern recognition weakened by form variation
- **Revision**: All quotes OR all descriptions:
```
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems to fix"
- "Let me propose solutions before understanding the flow"
- "One more fix attempt won't hurt"
- "This fix revealed a new problem elsewhere"
```

**Lines 180-186 (User Signals):**
```
- "Is that not happening?" -- assumed without verifying
- "Will it show us...?" -- should have added evidence gathering
- "Stop guessing" -- proposing fixes without understanding
- "Ultrathink this" -- need to question fundamentals, not just symptoms
```
- **Issue**: Pattern "quote -- explanation" but explanations vary in form
- **Rule**: Parallel construction for coordinate series
- **Severity**: Moderate
- **Revision**: Make all explanations parallel noun phrases:
```
- "Is that not happening?" -- assumption without verification
- "Will it show us...?" -- missing evidence gathering
- "Stop guessing" -- fixes without understanding
- "Ultrathink this" -- symptom focus instead of fundamental questioning
```

### R18 (Emphatic Position) - Moderate

**Line 13: "Random fixes waste time and create new bugs."**
- **Issue**: Ends on "new bugs" (good), but could emphasize process failure
- **Rule**: Place emphatic words at end
- **Severity**: Moderate - acceptable but could be stronger
- **Revision**: "Random fixes waste time. Worse: they create new bugs."

**Line 25: "Apply for ANY technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues."**
- **Issue**: List trails off without emphasis
- **Rule**: Emphatic position at end
- **Severity**: Moderate
- **Revision**: "Apply for ANY technical issue: unexpected behavior, performance problems, build failures, test failures, production bugs, integration failures."

**Line 37: "Time is short (systematic debugging is faster than thrashing)"**
- **Issue**: Ends on weak "thrashing" when could end on benefit
- **Rule**: Emphatic final position
- **Severity**: Moderate
- **Revision**: "Time is short (thrashing wastes more time than systematic debugging saves)"

**Line 74: "Fix at source, not at symptom."**
- **Issue**: Ends on negative "symptom" rather than positive "source"
- **Rule**: Emphatic position for key point
- **Severity**: Moderate
- **Revision**: "Fix the originating source, not downstream symptoms."

**Line 159: "Make the bug structurally impossible, not just fixed."**
- **Issue**: Ends weakly on "just fixed"
- **Rule**: Emphatic words at end
- **Severity**: Moderate
- **Revision**: "Don't just fix the bug—make it structurally impossible."

---

## Minor & Stylistic

### R13 (Needless Words) - Minor

**Line 15: "```\nNO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST\n```"**
- **Issue**: "FIRST" is implied by "BEFORE"
- **Rule**: Omit needless words
- **Severity**: Minor - adds emphasis, arguably purposeful
- **Revision**: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION"

**Line 70: "This reveals which layer fails (e.g., secrets pass from workflow to build script but not from build script to signing script)."**
- **Issue**: "e.g.," could be "for example," or example could be more concise
- **Rule**: Omit needless words
- **Severity**: Minor - example is illustrative and concrete
- **Keep as-is**: Example serves teaching purpose

**Line 88: "read the reference implementation COMPLETELY"**
- **Issue**: "COMPLETELY" emphasized but redundant with "Do not skim" on next line
- **Rule**: Omit needless words
- **Severity**: Minor - repetition serves emphasis
- **Keep as-is**: Repetition intentional for emphasis

**Line 104: "State clearly: "I think X is the root cause because Y.""**
- **Issue**: "clearly" may be needless
- **Rule**: Every word must tell
- **Severity**: Minor
- **Revision**: "State your hypothesis: "I think X is the root cause because Y.""

### R11 (Positive Form) - Minor

**Line 88: "Do not skim."**
- **Issue**: Negative command
- **Rule**: Positive form
- **Severity**: Minor - follows positive "read...COMPLETELY" so context mitigates
- **Revision**: "Read every line."

**Line 170: "Skip the test, I'll manually verify"**
- **Issue**: Negative construction in red flag
- **Rule**: Positive form
- **Severity**: Minor - intentionally showing bad thought pattern
- **Keep as-is**: Captures realistic inner monologue

### R10 (Active Voice) - Minor

**Line 25: "Apply for ANY technical issue"**
- **Issue**: "Apply" without explicit subject (implied "you")
- **Rule**: Active voice with clear actor
- **Severity**: Minor - imperative mood is acceptable active form
- **Keep as-is**: Imperative is direct and clear

**Line 204: "When debugging flaky tests caused by timing issues"**
- **Issue**: Passive "caused by"
- **Rule**: Active voice
- **Severity**: Minor - acceptable in subordinate clause
- **Alternative**: "When timing issues cause flaky tests"

### R15 (Parallel Construction) - Minor

**Lines 217-221 (Quick Reference table):**
```
| Phase | Key Activities | Success Criteria |
|---|---|---|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |
```
- **Issue**: "Success Criteria" column varies: noun phrases vs. clauses
- **Rule**: Parallel construction
- **Severity**: Minor - functional table
- **Revision**: Make all Success Criteria parallel noun phrases or all verb phrases:
```
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understanding of WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identified differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed hypothesis or new one |
| 4. Implementation | Create test, fix, verify | Resolved bug, passing tests |
```

### R18 (Emphatic Position) - Stylistic

**Line 100: "Apply the scientific method."**
- **Issue**: Short sentence; emphasis automatic but could be strengthened
- **Rule**: Emphatic position
- **Severity**: Stylistic
- **Alternative**: "Apply the scientific method: form hypotheses, test them, verify results."

**Line 122: "Fix the root cause, not the symptom."**
- **Issue**: Ends on "symptom" (negative) vs "root cause" (positive)
- **Rule**: Emphatic position
- **Severity**: Stylistic - acceptable for contrast
- **Keep as-is**: Contrast is intentional rhetorical device

---

## Summary

**Critical & Severe (7 findings):**
- R10 violations dominate: passive voice obscures agency in procedural instructions (Lines 13, 22, 44, 56, 113, 158)
- Critical fix: Active imperatives for debugging protocol steps

**Moderate (38 findings):**
- R13 (needless words): 11 instances, mostly redundant modifiers and wordy phrases
- R15 (parallel construction): 7 instances in lists and headings
- R12 (concrete language): 6 instances of abstract terms where specific examples would strengthen
- R11 (positive form): 8 instances of negative constructions
- R18 (emphatic position): 6 instances of weak sentence endings

**Minor & Stylistic (11 findings):**
- Mostly acceptable variations in specific contexts
- Some intentional (quoted thought patterns, emphasis through repetition)
- Table formatting and imperative mood uses

**Overall Assessment:**
The skill exhibits strong procedural structure but suffers from passive voice in critical instructions and needless words in metadata/lists. Concrete examples are generally good (e.g., git diff, stack traces) but some abstractions ("underlying issues", "gather more data") weaken teaching moments. Parallel construction issues appear primarily in bulleted lists where mixed grammatical forms reduce pattern recognition.

**Priority Fixes:**
1. Convert passive procedural commands to active imperatives (Severe - R10)
2. Trim redundant modifiers and wordy constructions (Moderate - R13)
3. Standardize list/heading structure for parallel construction (Moderate - R15)
4. Replace abstract terms with concrete examples where teaching moments exist (Moderate - R12)
