# Strunk Analysis: defensive-planning

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 31: "Written BEFORE work begins."**
- **Violation**: Passive voice obscures actor
- **Severity**: Severe
- **Revision**: "You write this BEFORE work begins." or "Write this BEFORE work begins."

**Line 34: "Written AFTER implementation."**
- **Violation**: Passive voice obscures actor
- **Severity**: Severe
- **Revision**: "You write this AFTER implementation." or "Write this AFTER implementation."

**Line 37: "Written after assessment reveals failures."**
- **Violation**: Passive voice obscures actor
- **Severity**: Severe
- **Revision**: "You write this after assessment reveals failures." or "Write this after assessment reveals failures."

**Line 62: "## Forbidden Patterns / Explicit list of BANNED code/approaches."**
- **Violation**: Passive construction "BANNED" without clear agent
- **Severity**: Severe
- **Revision**: "Patterns you MUST NOT use" or "Ban these patterns explicitly"

**Line 206: "'Tests pass' means nothing."**
- **Violation**: While not technically passive, "Tests pass" is weak intransitive where active construction would strengthen
- **Severity**: Moderate (borderline)
- **Revision**: "Passing tests prove nothing about semantic correctness."

**Line 278: "Whatever they exploited, explicitly forbid it."**
- **Violation**: Passive infinitive "forbid it"
- **Severity**: Severe
- **Revision**: "Whatever they exploited, you must forbid explicitly."

### R12 (Concrete/Specific/Definite) - Severe

**Line 18-25: "The implementer will optimize for 'appears done' over 'is done.'"**
- **Violation**: The list that follows is concrete, but the opening phrase "optimize for" is abstract corporate jargon
- **Severity**: Moderate
- **Revision**: "The implementer will choose speed over correctness. They will:"

**Line 206-214: "'Tests pass' means nothing. Check actual behavior."**
- **Violation**: "actual behavior" is vague; what counts as "actual"?
- **Severity**: Moderate
- **Revision**: "Tests pass' means nothing. Check semantic correctness: verify the function returns expected values, not just that no exceptions occur."

## Moderate

### R13 (Omit Needless Words) - Moderate

**Line 4-9: Full description block**
- **Quote**: "Use when: (1) creating implementation plans for peers/subordinates/contractors, (2) reviewing implementations for adherence, (3) writing correction plans after failures, (4) any situation where the implementer is assumed to be no better than you—possibly lazier, prone to shortcuts, or incentivized to appear done rather than be done."
- **Violation**: Wordy elaboration; point (4) contains entire concept already stated in (1-3)
- **Severity**: Moderate
- **Revision**: "Use when creating implementation plans, reviewing adherence, or writing correction plans for implementers who may cut corners."

**Line 49: "Why this plan exists. What problem it solves."**
- **Violation**: Redundant—both say same thing
- **Severity**: Moderate
- **Revision**: "What problem this solves."

**Line 76: "Never write 'decide whether X or Y.' Pick one. Write it down."**
- **Violation**: "Write it down" is needless after "Pick one"—picking implies documenting
- **Severity**: Minor
- **Revision**: "Never write 'decide whether X or Y.' Pick one."

**Line 102: "When specifying changes across files, list EVERY file and EVERY field."**
- **Violation**: "EVERY" repeated needlessly for emphasis
- **Severity**: Minor (stylistic choice, but Strunk would flag)
- **Revision**: "List every file and every field."

**Line 118-130: Verification Gates example**
- **Quote**: "```markdown\n# BAD\n- [ ] Ensure no empty list defaults remain\n\n# GOOD\n**Gate: No empty list defaults**\n```bash\ngrep -n \"= \\[\\]\" src/schemas/*.py\n```\n**REQUIRED OUTPUT:** Zero matches.\n```"
- **Violation**: "REQUIRED OUTPUT: Zero matches" could be "OUTPUT: Zero matches"—REQUIRED is implied by gate context
- **Severity**: Minor
- **Revision**: "OUTPUT: Zero matches"

**Line 206: "Test Semantic Correctness / 'Tests pass' means nothing. Check actual behavior."**
- **Violation**: "'Tests pass' means nothing" is needlessly dramatic; the point is made without hyperbole
- **Severity**: Minor
- **Revision**: "'Tests pass' is insufficient. Check semantic correctness."

**Line 290-300: "Don't explain options. Give orders."**
- **Violation**: The section title "Prescriptive, Not Consultative" already makes the point; "Don't explain options. Give orders" repeats it
- **Severity**: Minor
- **Revision**: Remove "Don't explain options. Give orders." or integrate into title

**Line 321-322: "Every 'or' is a door to the easy path."**
- **Violation**: Metaphorical where concrete would serve; "the easy path" is vague
- **Severity**: Moderate
- **Revision**: "Every 'or' lets implementers choose the easier option."

**Line 325: "'Add base class if needed' → They won't add it."**
- **Violation**: "if needed" already implies optionality; the arrow and explanation are needless
- **Severity**: Minor
- **Revision**: "Conditional language ('if needed') invites shortcuts."

**Line 333: "Long explanations get skimmed. Code blocks get copied."**
- **Violation**: Economical and effective—NO VIOLATION (this is model Strunk prose)
- **Severity**: None

**Line 372-374: "The implementer optimizes for completion, not correctness."**
- **Quote**: "The implementer optimizes for completion, not correctness.\nYour plan must make 'appearing done' harder than 'being done.'"
- **Violation**: These two sentences say the same thing from different angles; one would suffice
- **Severity**: Moderate
- **Revision**: "Your plan must make appearing done harder than being done."

**Line 376-378: Triple repetition**
- **Quote**: "Every escape hatch will be used.\nEvery ambiguity will be resolved in favor of less work.\nEvery subjective check will pass without verification."
- **Violation**: NOT A VIOLATION—this is purposeful repetition for rhetorical emphasis (Rule 15 parallel construction)
- **Severity**: None (justified by parallel structure)

### R11 (Positive Form) - Moderate

**Line 76: "Never write 'decide whether X or Y.'"**
- **Violation**: Negative instruction ("Never write") where positive alternative exists
- **Severity**: Minor
- **Revision**: "Pick one option. State it directly." (though original is forceful, so borderline)

**Line 87: "Never offer alternatives."**
- **Violation**: Negative instruction
- **Severity**: Minor
- **Revision**: "Commit to one approach."

**Line 102: "Rule 3: Exhaustive Field Lists"**
- **Violation**: NOT A VIOLATION—rule title is positive

**Line 164: "Rule 7: No Implicit Behavior"**
- **Violation**: "No" in title; negative framing
- **Severity**: Minor
- **Revision**: "Rule 7: Make All Behavior Explicit"

**Line 206: "Test Semantic Correctness / 'Tests pass' means nothing."**
- **Violation**: Negative ("means nothing") where positive would be clearer
- **Severity**: Moderate
- **Revision**: "'Tests pass' tells you only that code executes without error. Check semantic output."

**Line 217-218: "Replace 'mostly works' with numbers."**
- **Violation**: NOT A VIOLATION—positive instruction

**Line 325: "'Add base class if needed' → They won't add it."**
- **Violation**: Negative prediction
- **Severity**: Minor
- **Revision**: "'Add base class if needed' invites omission."

**Line 327: "Ensure code is clean → Unverifiable."**
- **Violation**: Negative assessment
- **Severity**: Minor
- **Revision**: "Ensure code is clean → Too subjective to verify."

### R15 (Parallel Construction) - Moderate

**Line 52-61: Phase structure headers**
- **Quote**: "### Why This Matters\nBusiness/technical justification.\n\n### What You Must Do\nExact steps. No decisions for implementer.\n\n### Verification Gates\nCommands that MUST produce exact output."
- **Violation**: NOT A VIOLATION—parallel structure maintained ("Why/What/Verification")

**Line 18-25: Core Assumption list**
- **Quote**: "They will:\n- Find every escape hatch and use it\n- Interpret ambiguity in their favor\n- Mark tasks complete when tests pass, ignoring semantic correctness\n- Copy-paste without understanding\n- Write `pass` or `TODO` and move on\n- Read 'option A or B' and pick whichever is less work"
- **Violation**: Inconsistent verb forms—first four use infinitives ("Find," "Interpret," "Mark," "Copy-paste"), last two shift to present tense ("Write," "Read")
- **Severity**: Minor (all are imperatives/base forms, so technically parallel, but "Copy-paste" vs others feels slightly off)
- **Revision**: All items already use base verb form—technically parallel. No change needed.

**Line 227-231: Severity Levels**
- **Quote**: "- **CRITICAL**: Feature is broken/missing. Blocks usage.\n- **HIGH**: Feature works incorrectly. Produces wrong results.\n- **MODERATE**: Inconsistency or maintainability issue.\n- **LOW**: Style or documentation issue."
- **Violation**: First two have two sentences; last two have one sentence
- **Severity**: Minor
- **Revision**: Maintain two-sentence structure:
  - **MODERATE**: Feature works but has issues. Creates inconsistency or maintainability debt.
  - **LOW**: Minor quality issues. Affects style or documentation.

**Line 376-378: Emphatic closing**
- **Quote**: "Every escape hatch will be used.\nEvery ambiguity will be resolved in favor of less work.\nEvery subjective check will pass without verification."
- **Violation**: NOT A VIOLATION—perfect parallel construction for rhetorical force

## Minor & Stylistic

### R18 (Emphatic Position) - Moderate

**Line 14: "Create implementation plans that survive contact with unreliable implementers."**
- **Violation**: Ends with "unreliable implementers" (weak, general). The emphatic concept is "survive contact"
- **Severity**: Minor
- **Revision**: "Create implementation plans that survive implementers who cut corners." (ends with action, not label)

**Line 26: "Plan accordingly."**
- **Violation**: NOT A VIOLATION—emphatic imperative at end

**Line 56: "Exact steps. No decisions for implementer."**
- **Violation**: Second sentence ends on "implementer" (weak). Should end on key concept
- **Severity**: Minor
- **Revision**: "Exact steps. Leave implementers no decisions to make."

**Line 76: "Never write 'decide whether X or Y.' Pick one. Write it down."**
- **Violation**: Ends on "Write it down" (weak action). Should end on key concept
- **Severity**: Minor
- **Revision**: "Never write 'decide whether X or Y.' Pick one and document it." or simply "Pick one."

**Line 217: "Replace 'mostly works' with numbers."**
- **Violation**: NOT A VIOLATION—ends emphatically on "numbers"

**Line 333: "Long explanations get skimmed. Code blocks get copied."**
- **Violation**: NOT A VIOLATION—ends emphatically on "copied" (the action you want)

**Line 372-374: "Your plan must make 'appearing done' harder than 'being done.'"**
- **Violation**: NOT A VIOLATION—perfect emphatic ending on the key contrast

**Line 380: "Plan defensively."**
- **Violation**: NOT A VIOLATION—emphatic imperative closes document

### R13 (Needless Words) - Minor instances

**Line 69: "For plans targeting TDD workflows with 2-5 minute task granularity, see @references/tdd-mode.md"**
- **Violation**: "For plans targeting" is wordy
- **Severity**: Minor
- **Revision**: "For TDD workflows with 2-5 minute tasks, see @references/tdd-mode.md"

**Line 71: "For module decomposition heuristics during plan design, see @references/module-design.md"**
- **Violation**: "during plan design" is needless—when else would you use decomposition heuristics?
- **Severity**: Minor
- **Revision**: "For module decomposition heuristics, see @references/module-design.md"

**Line 369: "For executing plans after writing them, see @references/execution.md"**
- **Violation**: "after writing them" is obvious from "executing"
- **Severity**: Minor
- **Revision**: "For plan execution, see @references/execution.md"

### R10 (Active Voice) - Minor instances

**Line 144: "### BANNED: Default empty lists"**
- **Violation**: "BANNED" is passive adjective; could be more direct
- **Severity**: Minor
- **Revision**: "### DO NOT USE: Default empty lists" or "### You must not write: Default empty lists"

**Line 282: "### BANNED: 'At least one of' validation"**
- **Violation**: Same as above
- **Severity**: Minor
- **Revision**: "### DO NOT USE: 'At least one of' validation"

## Summary

### Severity Distribution
- **Critical**: 0 findings
- **Severe**: 7 findings (6 x R10 active voice, 1 x R12 concrete language)
- **Moderate**: 13 findings (3 x R10, 2 x R12, 5 x R13 needless words, 2 x R11 positive form, 1 x R15 parallel)
- **Minor**: 18 findings (3 x R10, 4 x R13, 3 x R11, 1 x R15, 7 x R18)

### Overall Assessment

The defensive-planning skill shows **strong command of Strunk principles** with targeted violations that serve instructional clarity. Most severe issues involve passive voice in structural elements (document type definitions) where imperative mood would strengthen the directive tone.

**Strengths:**
- Excellent use of parallel construction for rhetorical force (lines 376-378)
- Concrete examples throughout (Rule 12 compliance)
- Economical phrasing in key sections ("Long explanations get skimmed. Code blocks get copied.")
- Strong emphatic positioning in closing imperatives

**Primary weaknesses:**
1. **Passive voice in document type definitions** (lines 31, 34, 37)—these should use imperative mood to match the skill's prescriptive purpose
2. **Corporate jargon** ("optimize for," "actual behavior") where concrete language would clarify
3. **Redundant elaboration** in frontmatter description and some rule explanations
4. **"BANNED" construction** throughout—passive adjective where direct prohibition would be more forceful

**Recommendation:** The skill is highly effective as written. Revisions to passive constructions and corporate abstractions would align tone with content—a skill about prescriptive directness should model that directness in its own prose.

**Strunk Compliance Score:** 7.5/10 (strong adherence with room for stylistic tightening)
