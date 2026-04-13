# Strunk Elements of Style Analysis: dev-orchestration

Analysis against R10 (active voice), R11 (positive form), R12 (concrete language), R13 (needless words), R15 (parallel construction), R18 (emphatic position).

---

## Critical & Severe

### Finding 1: Passive voice obscures agency (R10 - Severe)

**Line 28:** "If dev-discipline is not installed, recommend installing it."

**Issue:** The passive construction "is not installed" is followed by the imperative "recommend installing it," but the agent (who should install, who should recommend) is unclear.

**Severity:** Severe - This is instructional text where clarity about who performs actions is critical.

**Suggested revision:** "If the user has not installed dev-discipline, recommend installing it."

---

### Finding 2: Abstract language where concrete available (R12 - Severe)

**Line 64:** "The parent's decomposition patterns (by entity, by aspect, by concern) apply."

**Issue:** "apply" is vague and abstract. Apply how? Apply when? Apply where?

**Severity:** Severe - In instructional context, vagueness about application creates ambiguity.

**Suggested revision:** "Use the parent's decomposition patterns (by entity, by aspect, by concern) for dev tasks."

---

### Finding 3: Passive construction obscures actor (R10 - Severe)

**Line 67:** "Can be described in a self-contained brief"

**Issue:** Who describes? The implementer? The orchestrator? Passive voice leaves this unclear.

**Severity:** Severe - Critical for understanding workflow.

**Suggested revision:** "The orchestrator can describe it in a self-contained brief"

---

### Finding 4: Passive voice with unclear agent (R10 - Severe)

**Line 94:** "Require TDD for all behavior-carrying code."

**Issue:** While imperative mood is generally strong, the context lacks clarity about who enforces this requirement. The full sentence context shows passive patterns: "Each unit follows the red-green-refactor cycle" uses active voice, but the enforcement agent is unclear.

**Severity:** Severe - In orchestration context, knowing who enforces rules is critical.

**Suggested revision:** "The orchestrator requires TDD for all behavior-carrying code."

---

### Finding 5: Negative construction where positive clearer (R11 - Severe)

**Line 78:** "Never implement in orchestrator context."

**Issue:** This tells what NOT to do but doesn't state the positive directive clearly in the same breath.

**Severity:** Severe - The positive form would be more forceful.

**Suggested revision:** "Dispatch agents to implement. The orchestrator dispatches and decides only."

(Note: The following sentence does state the positive, but combining them would be stronger.)

---

### Finding 6: Abstract language replacing concrete action (R12 - Severe)

**Line 122:** "Agent self-reports are unreliable for cross-module integration"

**Issue:** "unreliable" is abstract. What actually happens? They miss failures, they report false success, they don't detect integration issues?

**Severity:** Severe - Precision matters for understanding the failure mode.

**Suggested revision:** "Agent self-reports miss cross-module failures — an agent may report DONE while its changes break tests in modules it didn't touch."

(Note: The next sentence does provide this concrete detail, but leading with the abstraction weakens impact.)

---

### Finding 7: Passive obscuring responsibility (R10 - Severe)

**Line 162:** "Delegate concern classification to an agent."

**Issue:** While "delegate" is active, this is imperative mood addressing an unclear actor. Who delegates?

**Severity:** Severe - Orchestration instructions must clarify the delegating party.

**Suggested revision:** "The orchestrator delegates concern classification to an agent."

---

## Moderate

### Finding 8: Needless words in phrase (R13 - Moderate)

**Line 4-5:** "Extension of agentic-delegation for the software development lifecycle."

**Issue:** "for the software development lifecycle" could be "for software development" - "lifecycle" adds little beyond "development" in this context.

**Severity:** Moderate - Minor wordiness that could be tightened.

**Suggested revision:** "Extension of agentic-delegation for software development."

---

### Finding 9: Weak negative construction (R11 - Moderate)

**Line 37:** "If dev-discipline is not installed, recommend installing it. If that isn't happening immediately, construct equivalent agent prompts"

**Issue:** "If that isn't happening immediately" - double negative construction (isn't + immediately) creates weak, evasive tone.

**Severity:** Moderate - Weakens directive force.

**Suggested revision:** "If dev-discipline is not installed, recommend installing it. If the user declines, construct equivalent agent prompts"

---

### Finding 10: Passive where active clearer (R10 - Moderate)

**Line 47:** "Skipping phases produces spec drift, quality regression, or wasted effort."

**Issue:** While this is technically active voice ("skipping" is the subject performing "produces"), the gerund subject creates a somewhat abstract construction.

**Severity:** Moderate - Not a pure passive violation, but could be more direct.

**Suggested revision:** "Skip phases and you produce spec drift, quality regression, or wasted effort." OR "When you skip phases, spec drift, quality regression, and wasted effort follow."

---

### Finding 11: Buried emphatic point (R18 - Moderate)

**Line 19:** "The parent skill establishes the economics, model ladder, decomposition patterns, prompt anatomy, execution patterns, and quality governance. This skill adds the Plan→Implement→Review→Fix loop that governs how those patterns apply to writing software."

**Issue:** The key differentiator (the PIRF loop) appears at the end of the second sentence, but the sentence ends weakly with "to writing software" rather than emphasizing the loop itself.

**Severity:** Moderate - The emphatic element should occupy final position.

**Suggested revision:** "The parent skill establishes the economics, model ladder, decomposition patterns, prompt anatomy, execution patterns, and quality governance. This skill governs how those patterns apply to writing software through the Plan→Implement→Review→Fix loop."

---

### Finding 12: Needless words in common phrase (R13 - Moderate)

**Line 59:** "Use defensive-planning to produce the implementation plan"

**Issue:** "to produce" could be tightened to "for" - more economical.

**Severity:** Moderate - Minor verbosity.

**Suggested revision:** "Use defensive-planning for the implementation plan"

---

### Finding 13: Weak final position (R18 - Moderate)

**Line 74:** "Build foundational units first (data models, interfaces), then dependent units (logic, integration), then verification units (integration tests, end-to-end checks)."

**Issue:** The sentence ends with "end-to-end checks" in parentheses - a weak, anticlimactic ending. The emphatic point (the ordering principle) is buried.

**Severity:** Moderate - Ending weakly undercuts the directive.

**Suggested revision:** "Sequence the work: foundational units first (data models, interfaces), then dependent units (logic, integration), then verification units (integration tests, end-to-end checks)."

(Still not ideal, but moves the action verb earlier to give it more weight)

---

### Finding 14: Needless phrase (R13 - Moderate)

**Line 87:** "Default model: sonnet — the parent's Implementation archetype already derives this"

**Issue:** "already derives this" adds little - if the parent derives it, stating "default model: sonnet" suffices.

**Severity:** Moderate - Mild redundancy.

**Suggested revision:** "Default model: sonnet (the parent's Implementation archetype)."

---

### Finding 15: Non-parallel construction in series (R15 - Moderate)

**Line 83-86:** The brief contains four items:
1. "The task specification with exact code expectations"
2. "File paths to read for context"
3. "TDD requirements (if applicable)"
4. "Scope boundaries (what to build, what NOT to build)"

**Issue:** Item 1 uses "with [detail]", item 2 uses "to [purpose]", item 3 stands alone, item 4 uses parenthetical expansion. Forms are not parallel.

**Severity:** Moderate - Parallel construction aids comprehension in lists.

**Suggested revision:**
1. "Task specification (exact code expectations)"
2. "File paths (for context)"
3. "TDD requirements (if applicable)"
4. "Scope boundaries (what to build, what to exclude)"

---

### Finding 16: Passive voice in key instruction (R10 - Moderate)

**Line 115-116:** "Agents commit their own work with descriptive messages. If fixes are needed, dispatch a fix agent"

**Issue:** "If fixes are needed" is passive - who determines fixes are needed?

**Severity:** Moderate - Less severe than some others because context suggests the orchestrator, but still weaker than active.

**Suggested revision:** "Agents commit their own work with descriptive messages. If you discover needed fixes, dispatch a fix agent"

---

### Finding 17: Weak ending (R18 - Moderate)

**Line 129:** "Order is mandatory: spec compliance first, code quality second. Reviewing quality before confirming spec compliance wastes effort on code that may not meet requirements."

**Issue:** Sentence ends with "requirements," which is abstract. The emphatic point (the waste) is buried mid-sentence.

**Severity:** Moderate - Emphatic element displaced.

**Suggested revision:** "Order is mandatory: spec compliance first, code quality second. Confirm spec compliance before reviewing quality; otherwise you waste effort polishing code that may fail to meet requirements."

---

### Finding 18: Non-parallel table entries (R15 - Moderate)

**Lines 155-160:** Status routing table has non-parallel construction:

| Status | Route |
|---|---|
| DONE | Dispatch spec-reviewer |
| DONE_WITH_CONCERNS | Delegate concern classification to an agent. Correctness/scope → address before review. Observational → note and proceed. |
| NEEDS_CONTEXT | Identify missing information. Provide it. Re-dispatch. |
| BLOCKED | Delegate root cause diagnosis. See escalation below. |

**Issue:** DONE uses imperative ("Dispatch"). DONE_WITH_CONCERNS uses imperative but then shifts to arrow notation. NEEDS_CONTEXT uses three imperatives. BLOCKED uses imperative plus cross-reference. Not parallel.

**Severity:** Moderate - Table format benefits from parallel structure.

**Suggested revision:** Standardize all entries to imperative verb + object format:
- DONE: Dispatch spec-reviewer
- DONE_WITH_CONCERNS: Classify concerns; address correctness/scope issues before review; note observational concerns and proceed
- NEEDS_CONTEXT: Identify missing information, provide it, re-dispatch
- BLOCKED: Diagnose root cause (see escalation below)

---

### Finding 19: Vague abstraction (R12 - Moderate)

**Line 199:** "For multi-unit features, dispatch a cross-cutting review after integration passes."

**Issue:** "after integration passes" - what does "passes" mean concretely? Tests pass? Review approves? Both?

**Severity:** Moderate - Context suggests "after integration verification passes" but could be explicit.

**Suggested revision:** "For multi-unit features, dispatch a cross-cutting review after integration verification confirms all units work together."

---

### Finding 20: Needless words (R13 - Moderate)

**Line 200:** "Decompose by CONCERN, not by module."

**Issue:** Works as is, but the following sentence "Module-scoped reviews repeat shallow checks" essentially restates the point. One could be tightened or merged.

**Severity:** Moderate - Border case; repetition may be pedagogically justified.

**Suggested revision:** No strong revision needed; acceptable as is for emphasis.

---

## Minor & Stylistic

### Finding 21: Slightly abstract phrasing (R12 - Minor)

**Line 20:** "This is a hard gate, not a suggestion."

**Issue:** "hard gate" is metaphorical/abstract. Could be more concrete.

**Severity:** Minor - The metaphor is clear in context.

**Suggested revision:** "You must read it before proceeding, not as a suggestion but as a requirement."

---

### Finding 22: Slight wordiness (R13 - Minor)

**Line 51:** "For tasks under ~10 lines of trivially obvious changes, execute directly without agent dispatch."

**Issue:** "of trivially obvious changes" is slightly wordy; "trivially obvious" is somewhat redundant.

**Severity:** Minor - Emphasis may justify the redundancy.

**Suggested revision:** "For tasks under ~10 lines with trivial changes, execute directly without agent dispatch."

---

### Finding 23: Passive in descriptive context (R10 - Minor)

**Line 134:** "Dispatch the **spec-reviewer** with the task specification and changed file list. It reads actual code and compares to requirements line by line, with adversarial posture."

**Issue:** Not passive per se, but "with adversarial posture" is prepositional phrase where active verb would be stronger.

**Severity:** Minor - The sentence is otherwise strong.

**Suggested revision:** "Dispatch the spec-reviewer with the task specification and changed file list. It adopts an adversarial posture, reading actual code and comparing it to requirements line by line."

---

### Finding 24: Slightly buried emphasis (R18 - Minor)

**Line 141:** "When either reviewer reports issues: 1. Dispatch the implementer (or a fix agent) with the specific findings."

**Issue:** The key instruction (dispatch with findings) ends with "findings" which is fine, but "specific" is a modifier that slightly weakens the final position.

**Severity:** Minor - Acceptable as is.

**Suggested revision:** "When either reviewer reports issues: 1. Dispatch the implementer (or a fix agent) with the findings."

---

### Finding 25: Minor non-parallelism (R15 - Minor)

**Lines 167-171:** BLOCKED escalation routes:

1. "**Missing context** — provide the missing information, re-dispatch implementer."
2. "**Insufficient reasoning** — re-dispatch with a more capable model."
3. "**Task too large** — decompose further, dispatch sub-units."
4. "**Plan defect** — the plan's assumptions are wrong. Escalate to the user."

**Issue:** Entries 1-3 use imperative verbs. Entry 4 uses declarative statement ("assumptions are wrong") then imperative. Slight asymmetry.

**Severity:** Minor - The explanation in #4 may justify the form.

**Suggested revision:** 
4. "**Plan defect** — the plan's assumptions are wrong; escalate to the user."

---

### Finding 26: Weak series ending (R18 - Minor)

**Line 202-207:** The concern table ends with "DRY/YAGNI | Duplicated knowledge, unused features"

**Issue:** "unused features" is a weak ending to the table. The most important concern (spec fidelity) is listed first, which violates the emphatic-position principle for tables.

**Severity:** Minor - Table ordering may follow logical sequence rather than emphasis.

**Suggested revision:** Consider reordering table by importance/severity if emphatic principle should apply. Otherwise, acceptable as is for logical flow.

---

### Finding 27: Slightly wordy construction (R13 - Minor)

**Line 222:** "Theatrical test coverage is worse than low coverage — it creates false confidence."

**Issue:** "it creates" could be tightened; the dash already sets up the explanation.

**Severity:** Minor - Current form is acceptable.

**Suggested revision:** "Theatrical test coverage is worse than low coverage — it breeds false confidence."

---

### Finding 28: Minor passive (R10 - Minor)

**Line 226:** "Code in orchestrator context."

**Issue:** This is a sentence fragment used as a heading, which is acceptable, but the following explanation uses passive: "It does not write code, read implementation files, or debug test failures."

**Severity:** Minor - The negative construction is appropriate for anti-pattern documentation.

**Suggested revision:** No change needed; negative form is correct for prohibitions.

---

### Finding 29: Slight abstraction (R12 - Minor)

**Line 228:** "Implementer self-review is not spec compliance."

**Issue:** "spec compliance" is abstract. Could be more concrete: "does not verify spec compliance" or "does not catch spec drift."

**Severity:** Minor - Acceptable as is; the abstraction is clear in context.

**Suggested revision:** "Implementer self-review does not verify spec compliance."

---

### Finding 30: Minor wordiness (R13 - Minor)

**Line 236:** "Tests that assert defaults equal hardcoded copies or test library guarantees provide zero protection."

**Issue:** "provide zero protection" could be "protect nothing" - slightly more economical.

**Severity:** Minor - Current form is emphatic and acceptable.

**Suggested revision:** "Tests that assert defaults equal hardcoded copies or test library guarantees protect nothing."

---

## Summary

**Total findings:** 30

**By severity:**
- Critical: 0
- Severe: 7 (findings 1-7)
- Moderate: 13 (findings 8-20)
- Minor: 10 (findings 21-30)

**By rule:**
- R10 (Active voice): 10 findings (1, 3, 4, 7, 10, 16, 23, 28 + portions of others)
- R11 (Positive form): 3 findings (5, 9, + embedded in 28)
- R12 (Concrete language): 6 findings (2, 6, 19, 21, 29 + portions of others)
- R13 (Needless words): 7 findings (8, 12, 14, 20, 22, 27, 30)
- R15 (Parallel construction): 3 findings (15, 18, 25)
- R18 (Emphatic position): 6 findings (11, 13, 17, 24, 26 + portions of others)

**Key patterns:**

1. **Passive voice in orchestration context** - The most significant issue. When describing orchestration workflows, the document frequently uses passive constructions or imperative mood without specifying the actor (orchestrator vs. implementer vs. user). This creates ambiguity about who performs actions, which is critical in delegation contexts.

2. **Abstract process descriptions** - Several key concepts ("apply," "passes," "unreliable") use abstract language where concrete descriptions of actual behavior would be clearer.

3. **Non-parallel structures in lists** - Lists and tables mix different grammatical forms (imperatives, declaratives, arrow notation), reducing scanability.

4. **Needless prepositional phrases** - Several instances of "to produce," "for the purpose of," etc., where shorter forms would suffice.

5. **Weak sentence endings** - Several sentences end with less important modifiers or abstractions rather than placing the emphatic point in final position.

**Overall assessment:**

The document is generally well-written and clear. Most issues are moderate or minor. The severe findings cluster around passive voice and unclear agency in orchestration instructions - this is the primary area for improvement. For instructional documentation in a delegation framework, active voice with explicit actors ("The orchestrator dispatches...") would substantially improve clarity.

The document shows good command of parallel structure in its overall organization (phases, stages, anti-patterns) but could tighten parallelism in tables and lists. Economy is generally good, with only minor instances of wordiness. Concrete language is mostly strong, with occasional lapses into abstraction.
