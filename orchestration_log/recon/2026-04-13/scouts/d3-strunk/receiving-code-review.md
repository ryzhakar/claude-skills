# Strunk Analysis: receiving-code-review

Analysis of `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/receiving-code-review/SKILL.md` against Strunk's Elements of Style rules R10 (active voice), R11 (positive form), R12 (concrete language), R13 (needless words), R15 (parallel construction), R18 (emphatic position).

---

## Critical & Severe

### R10: Active Voice (Severity: Severe)

**Line 52: "Performative agreement detection"**
> "When responses contain gratitude or agreement phrases, remove them and state the technical action instead."

**Issue:** Passive construction "state the technical action" where active would be more direct.

**Suggested revision:** "When responses contain gratitude or agreement phrases, remove them and state what technical action you will take."

**Severity:** Moderate (borderline severe) - reduces clarity and directness in an instruction.

---

**Line 88: "Should [investigation/user input/proceeding] occur?"**
> "Cannot verify this without [X]. Should [investigation/user input/proceeding] occur?"

**Issue:** Passive-like construction "should occur" obscures agency. Who performs the investigation?

**Suggested revision:** "Cannot verify this without [X]. Should I [investigate/consult the user/proceed]?"

**Severity:** Severe - creates ambiguity about who acts in a protocol step.

---

**Line 102: "should not be added"**
> "Features that nothing calls should not be added."

**Issue:** Passive voice obscures agent. Who should not add them?

**Suggested revision:** "Do not add features that nothing calls."

**Severity:** Severe - weakens a core prohibition in the protocol.

---

**Line 103: "should not be built"**
> "Infrastructure for hypothetical future needs should not be built."

**Issue:** Passive voice in prohibition.

**Suggested revision:** "Do not build infrastructure for hypothetical future needs."

**Severity:** Severe - same as above; weakens imperative force.

---

**Line 157: "Batching implementations without individual testing is prohibited."**
> "Batching implementations without individual testing is prohibited."

**Issue:** Passive "is prohibited" instead of direct command.

**Suggested revision:** "Do not batch implementations without individual testing."

**Severity:** Severe - weakens a critical testing requirement.

---

### R12: Concrete Language (Severity: Severe)

**Line 89: "the suggestion conflicts with the user's prior decisions"**
> "When the suggestion conflicts with the user's prior decisions, stop and consult with the user before proceeding."

**Issue:** "Prior decisions" is vague. What kind of decisions? Architectural? Implementation? Styling?

**Suggested revision:** "When the suggestion conflicts with the user's architectural decisions, stop and consult with the user before proceeding."

**Note:** This is already partially addressed on line 112 ("architectural decisions"), but line 89 should match.

**Severity:** Moderate - creates potential ambiguity about when to escalate.

---

## Moderate

### R11: Positive Form (Severity: Moderate)

**Line 72: "Omit performative agreement."**
> "Omit performative agreement."

**Issue:** Negative instruction (what not to do). Could state positive alternative.

**Suggested revision:** "Use technical restatement or direct action."

**Severity:** Minor - the negative is clear enough, and the positive alternatives are listed separately in lines 44-48.

---

**Line 157: "is prohibited"**
> "Batching implementations without individual testing is prohibited."

**Issue:** Negative form. See also R10 issue above.

**Suggested revision:** "Test each fix individually."

**Severity:** Moderate - combines with passive voice issue to weaken the instruction.

---

### R13: Needless Words (Severity: Moderate)

**Line 50: "adds no technical value and wastes time"**
> "Performative agreement adds no technical value and wastes time."

**Issue:** "adds no technical value" already implies waste; "and wastes time" is somewhat redundant.

**Suggested revision:** "Performative agreement adds no technical value."

**Severity:** Minor - the redundancy reinforces the point, though technically needless.

---

**Line 68: "Trusted Source"**
> "### From the User (Trusted Source)"

**Issue:** "(Trusted Source)" parenthetical is explanatory but unnecessary given the context.

**Suggested revision:** "### From the User"

**Severity:** Minor - adds minimal value; clarity is not impaired.

---

**Line 94: "When a reviewer suggests 'implementing properly' or adding a feature:"**
> "When a reviewer suggests 'implementing properly' or adding a feature:"

**Issue:** "'implementing properly' or adding a feature" - the quoted phrase and the general case are not quite parallel, creating slight awkwardness.

**Suggested revision:** "When a reviewer suggests adding a feature or 'implementing properly':"

**Severity:** Minor - word order improvement for clarity.

---

**Line 140: "Checked [X] and it does [Y]. Implementing now."**
> "Checked [X] and it does [Y]. Implementing now."

**Issue:** "Implementing now" could be "Implementing."

**Suggested revision:** "Checked [X] and it does [Y]. Implementing."

**Severity:** Minor - "now" is implied by present progressive; adds one needless word.

---

### R15: Parallel Construction (Severity: Moderate)

**Line 79-84: Verification questions**
> "1. Technically correct for THIS codebase?
> 2. Breaks existing functionality?
> 3. Reason for the current implementation?
> 4. Works on all target platforms/versions?
> 5. Does the reviewer understand the full context?"

**Issue:** Questions 1-4 are fragments (no subject/verb), while question 5 is a complete sentence. This breaks parallel construction.

**Suggested revision:** Make all complete questions or all fragments:
- "1. Is it technically correct for THIS codebase?"
- "2. Does it break existing functionality?"
- "3. What is the reason for the current implementation?"
- "4. Does it work on all target platforms/versions?"
- "5. Does the reviewer understand the full context?"

**Severity:** Moderate - the structural inconsistency creates minor cognitive friction.

---

**Line 161-169: Table rows**

The "Mistake | Correction" table structure is parallel and well-executed. No issue.

---

### R18: Emphatic Position (Severity: Moderate)

**Line 18: "Technical correctness over social comfort."**
> "Verify before implementing. Ask before assuming. Technical correctness over social comfort."

**Issue:** The emphatic final phrase is strong, but "social comfort" is the weaker element. Better to end with "technical correctness."

**Suggested revision:** "Verify before implementing. Ask before assuming. Choose technical correctness over social comfort."

**Severity:** Minor - the current form is already emphatic; this is refinement.

---

**Line 50: "Performative agreement adds no technical value and wastes time."**
> "Performative agreement adds no technical value and wastes time."

**Issue:** Sentence ends on "wastes time" rather than the stronger "technical value." 

**Suggested revision:** "Performative agreement wastes time and adds no technical value."

**Severity:** Minor - both endings are reasonably emphatic.

---

## Minor & Stylistic

### R10: Active Voice (Minor instances)

**Line 102-103: "Actual usage must be verified"**
> "Actual usage must be verified before investing effort."

**Issue:** Passive voice "must be verified."

**Suggested revision:** "Verify actual usage before investing effort."

**Severity:** Minor - the passive is acceptable here for emphasis on "usage," but active is stronger.

---

**Line 126: "Good catch"**
> "Good catch -- [specific issue]. Fixed in [location]."

**Issue:** "Good catch" is borderline performative, though the skill allows it as acceptable technical acknowledgment when paired with specifics.

**Suggested revision:** No change needed - this is explicitly listed as acceptable in context.

**Severity:** None - this is deliberate exception to the anti-performative rule.

---

### R13: Needless Words (Minor instances)

**Line 61: "implementation must wait"**
> "STOP -- implementation must wait"

**Issue:** "STOP" and "implementation must wait" both convey the same instruction.

**Suggested revision:** "STOP -- clarify all unclear items before implementing."

**Severity:** Minor - the redundancy serves emphasis in this gate condition.

---

**Line 113: "is appropriate when"**
> "Pushback is appropriate when:"

**Issue:** "is appropriate" is slightly wordy; could be more direct.

**Suggested revision:** "Push back when:"

**Severity:** Minor - the current form is acceptable; revision would save two words.

---

### R15: Parallel Construction (Minor)

**Line 35-39: Prohibited patterns list**
> "- 'Absolutely right!'
> - 'Great point!' / 'Excellent feedback!'
> - 'Thanks for catching that!' / 'Thanks for [anything]'
> - Any gratitude expression
> - 'Let me implement that now' (before verification)"

**Issue:** Most items are quoted examples, but "Any gratitude expression" is a category description. Minor inconsistency.

**Suggested revision:** 
> "- 'Absolutely right!'
> - 'Great point!' / 'Excellent feedback!'
> - 'Thanks for catching that!' / 'Thanks for [anything]'
> - 'Thank you' / 'I appreciate this'
> - 'Let me implement that now' (before verification)"

**Severity:** Minor - the current form is clear; this is stylistic consistency.

---

**Line 44-48: Required patterns**
> "Instead, use:
> - Technical restatement of the requirement
> - Clarifying questions
> - Technical pushback with reasoning if the suggestion is incorrect
> - Direct action without commentary"

**Issue:** All items are noun phrases except "Technical pushback with reasoning if the suggestion is incorrect," which includes a conditional clause.

**Suggested revision:**
> "- Technical restatement of the requirement
> - Clarifying questions about unclear items
> - Technical pushback with reasoning when the suggestion is incorrect
> - Direct action without commentary"

**Severity:** Minor - improves parallelism slightly.

---

## Summary

**Critical/Severe findings:** 5 instances
- 4 passive voice constructions in protocol instructions (R10) that weaken imperative force
- 1 vague term that could cause ambiguity in escalation criteria (R12)

**Moderate findings:** 7 instances
- Parallel construction inconsistency in verification questions (R15)
- Several needless word opportunities (R13)
- Negative constructions that could be positive (R11)
- Minor emphatic position improvements (R18)

**Minor/Stylistic findings:** 7 instances
- Additional passive voice opportunities for improvement
- Further needless word reductions
- Parallel construction refinements in lists

**Overall assessment:** The skill demonstrates strong technical writing with clear, imperative instructions. The main issues are:
1. Excessive use of passive voice in protocol prohibitions (should use active imperatives)
2. One structural inconsistency in the verification questions list (parallel construction)

The prose is otherwise clear, concrete, and economical. Most findings are minor refinements rather than clarity blockers.

**Recommendation:** Address the 5 severe findings (passive voice in lines 88, 102, 103, 157 and vague reference in line 89) to strengthen protocol force and clarity. The moderate and minor findings are optional improvements.
