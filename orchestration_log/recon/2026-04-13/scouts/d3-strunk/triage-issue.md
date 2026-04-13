# Strunk Analysis: triage-issue

## Critical & Severe

### 1. Passive voice obscuring agency (R10, Severe)

**Line 4-5:** "This skill should be used when the user reports a bug..."

**Issue:** Passive construction ("should be used") obscures actor. Who uses it? The system? Claude?

**Suggested revision:** "Use this skill when the user reports a bug..." (active imperative)

---

**Line 12:** "Autonomously diagnose a reported bug, trace its root cause..."

**Issue:** "reported bug" - passive participle. Who reported it?

**Suggested revision:** "Autonomously diagnose bugs users report, trace their root cause..." (active construction maintains agent clarity)

---

**Line 17:** "Bug triage benefits from depth of investigation..."

**Issue:** While "benefits from" is active, the abstract subject weakens agency.

**Suggested revision:** "Deep investigation improves bug triage more than broad questioning." (concrete verb "improves" with clear subject-object relationship)

---

**Line 25:** "Get a brief description of the issue from the user. If they have not provided one..."

**Issue:** "have not provided" - past perfect obscures timeline.

**Suggested revision:** "Get a brief description of the issue from the user. If they haven't yet described it..." (more direct temporal relationship)

---

**Line 49-50:** "If the agentic-delegation skill is available, apply its Speculative Parallel pattern..."

**Issue:** Passive construction "is available" separates condition from action.

**Suggested revision:** "If you have access to the agentic-delegation skill, apply its Speculative Parallel pattern..." (active construction, clearer agency)

---

**Line 61:** "the smallest change that addresses the root cause"

**Issue:** "that addresses" is active but weak. The change doesn't actively address; it fixes.

**Suggested revision:** "the smallest change that fixes the root cause" (stronger active verb)

---

**Line 98:** "Actual behavior: what happens now"

**Issue:** "happens" is active but generic. More specific verb would strengthen.

**Suggested revision:** "Actual behavior: what the code does now" (concrete agent + action)

---

**Line 107:** "Do NOT include specific file paths, line numbers, or implementation details that couple to the current code layout."

**Issue:** "that couple to" - weak verb for describing relationship.

**Suggested revision:** "Do NOT include specific file paths, line numbers, or implementation details tied to current code layout." (stronger verb "tied")

---

**Line 111:** "The issue must remain useful after major refactors."

**Issue:** Passive construction ("must remain") obscures who ensures usefulness.

**Suggested revision:** "Write the issue so major refactors won't invalidate it." (active construction with clear subject)

---

**Line 127:** "Root cause is addressed, not just the symptom"

**Issue:** Passive "is addressed" in acceptance criteria obscures who addresses it.

**Suggested revision:** "Fix addresses root cause, not just the symptom" (active construction)

---

**Line 130:** "Existing tests still pass"

**Issue:** Active but weak. "Pass" doesn't show agency clearly.

**Suggested revision:** "All existing tests continue passing" (continuous action emphasizes ongoing state)

---

**Line 137:** "Document the investigation path, hypotheses tested, and why reproduction failed."

**Issue:** "hypotheses tested" - passive participle obscures who tested.

**Suggested revision:** "Document the investigation path, which hypotheses you tested, and why reproduction failed." (active construction with clear agent)

---

**Line 144:** "If the root cause is a design flaw that needs architectural rework..."

**Issue:** "is a design flaw" + "needs rework" - double passive weakens force.

**Suggested revision:** "If the root cause stems from flawed design requiring architectural rework..." (active verb "stems" + participle "requiring")

---

## Moderate

### 2. Needless words (R13, Moderate)

**Line 3-7:** "This skill should be used when the user reports a bug, says 'this is broken', asks to 'triage an issue', 'investigate a bug', 'find the root cause', 'file an issue for this bug', 'create a GitHub issue', or wants autonomous diagnosis of a problem in the codebase."

**Issue:** Excessive enumeration. List could be condensed.

**Suggested revision:** "Use this skill when the user reports bugs, requests investigation, or wants autonomous diagnosis and issue creation." (removes redundant trigger phrases)

---

**Line 18:** "One question to the user ('What's the problem?') then full autonomous exploration."

**Issue:** "full autonomous exploration" - "full" is needless intensifier.

**Suggested revision:** "One question to the user ('What's the problem?') then autonomous exploration." (omit "full")

---

**Line 19:** "Follow-up questions waste the user's time when the codebase contains all the evidence."

**Issue:** "all the evidence" - "all" overstates and adds no precision.

**Suggested revision:** "Follow-up questions waste the user's time when the codebase contains the evidence." (omit "all")

---

**Line 32:** "Launch a deep investigation of the codebase."

**Issue:** "deep" is vague intensifier. What makes it deep?

**Suggested revision:** "Launch a thorough investigation of the codebase." (or specify what "deep" means: "multi-file investigation")

---

**Line 57:** "Based on investigation, determine:"

**Issue:** "Based on investigation" - wordy prepositional phrase.

**Suggested revision:** "From your investigation, determine:" (more direct)

---

**Line 71:** "Rules for the fix plan:"

**Issue:** Colon after "Rules for" creates needless setup.

**Suggested revision:** "Fix plan rules:" (more direct)

---

**Line 72:** "Vertical slices only."

**Issue:** Fragment used for emphasis (acceptable) but could be clearer.

**Suggested revision:** "Use vertical slices only." (complete sentence, equally emphatic)

---

**Line 73:** "Each cycle writes one test then one implementation change."

**Issue:** "then" as conjunction is informal here.

**Suggested revision:** "Each cycle writes one test, then one implementation change." (comma clarifies sequence)

---

**Line 92:** "Create the issue using `gh issue create` with the structure below."

**Issue:** "with the structure below" - "below" is needless direction.

**Suggested revision:** "Create the issue using `gh issue create` with this structure:" (direct reference)

---

**Line 93:** "Do NOT ask the user to review before creating -- publish directly and share the URL."

**Issue:** "before creating" repeats concept from "publish directly."

**Suggested revision:** "Do NOT ask the user to review first -- publish directly and share the URL." (more concise)

---

**Line 103:** "Describe the investigation findings:"

**Issue:** "findings" is implied by "investigation."

**Suggested revision:** "Describe your investigation:" (omit redundant "findings")

---

**Line 109:** "Do NOT include specific file paths, line numbers, or implementation details that couple to the current code layout."

**Issue:** "that couple to the current code layout" is wordy.

**Suggested revision:** "Do NOT include specific file paths, line numbers, or layout-coupled implementation details." (more concise)

---

**Line 110:** "Describe modules, behaviors, and contracts."

**Issue:** This sentence stands alone but adds no new information beyond previous sentence.

**Suggested revision:** Merge with previous: "Describe modules, behaviors, and contracts instead of file paths or line numbers." (combines two ideas)

---

**Line 140:** "partial diagnosis is more valuable than no documentation."

**Issue:** "no documentation" is negative construction (see R11).

**Suggested revision:** "partial diagnosis beats silence." (positive, concrete)

---

**Line 146:** "note this in the issue and suggest using the improve-architecture skill for the design phase."

**Issue:** "for the design phase" is needless qualifier.

**Suggested revision:** "note this in the issue and suggest using the improve-architecture skill." (omit obvious qualifier)

---

### 3. Abstract language where concrete available (R12, Severe)

**Line 16:** "Why Autonomous"

**Issue:** "Autonomous" is abstract adjective used as noun concept.

**Suggested revision:** "Why Investigate Autonomously" (verb form more concrete)

---

**Line 17:** "Bug triage benefits from depth of investigation, not breadth of questioning."

**Issue:** "depth" vs "breadth" - abstract spatial metaphors.

**Suggested revision:** "Bug triage needs thorough investigation, not extensive questioning." (more concrete qualifiers)

---

**Line 58:** "Type: regression (worked before), missing feature (never implemented), or design flaw (works as coded but coded wrong)"

**Issue:** Good concrete examples in parentheses, but "Type" is abstract.

**Suggested revision:** "Classification: regression (worked before)..." (more specific term)

---

**Line 77:** "Public interface tests."

**Issue:** "interface" is abstract in this context.

**Suggested revision:** "Test through public boundaries." (more concrete action)

---

**Line 79:** "Durable descriptions."

**Issue:** "Durable" is metaphorical abstraction.

**Suggested revision:** "Refactor-proof descriptions." (concrete quality)

---

**Line 83:** "Survival criterion."

**Issue:** Biological metaphor for code quality.

**Suggested revision:** "Refactoring resilience test." (concrete technical term)

---

**Line 106:** "Contributing factors (missing validation, incorrect assumption, race condition, etc.)"

**Issue:** Good concrete examples, but "factors" is abstract.

**Suggested revision:** "Contributors (missing validation, incorrect assumption, race condition, etc.)" (slightly more concrete)

---

### 4. Negative constructions where positive clearer (R11, Moderate)

**Line 28:** "Do NOT ask follow-up questions."

**Issue:** Pure prohibition without positive alternative.

**Suggested revision:** "Skip follow-up questions. Start investigating immediately." (positive instruction follows)

---

**Line 74:** "Never batch all tests first then all implementation."

**Issue:** Negative prohibition.

**Suggested revision:** "Interleave tests and implementation." (positive directive)

---

**Line 92-93:** "Do NOT ask the user to review before creating -- publish directly and share the URL."

**Issue:** Starts with negative, but positive follows.

**Suggested revision:** "Publish directly and share the URL without asking for review." (positive construction with negative as modifier)

---

**Line 107-109:** "Do NOT include specific file paths, line numbers, or implementation details that couple to the current code layout."

**Issue:** Long negative prohibition.

**Suggested revision:** "Describe modules, behaviors, and contracts instead of file paths, line numbers, or implementation details." (positive alternative stated first)

---

**Line 127:** "Root cause is addressed, not just the symptom"

**Issue:** Negative contrast construction.

**Suggested revision:** "Fix targets root cause beyond mere symptoms" (positive assertion)

---

**Line 130:** "No regression in adjacent functionality"

**Issue:** Negative construction.

**Suggested revision:** "Adjacent functionality remains intact" (positive assertion)

---

### 5. Parallel construction violations (R15, Moderate)

**Line 36-37:** "WHERE does the bug manifest? | Trace entry points: UI components, API handlers, CLI commands"

**Issue:** Question uses "WHERE" (location), but method uses "Trace" (action). Not parallel with other rows.

**Analysis:** The other three rows use question word matching the method's focus. This one shifts from location to action.

**Suggested revision:** "WHERE does the bug manifest? | Locate entry points: UI components, API handlers, CLI commands" (verb "Locate" matches "WHERE")

---

**Line 75-76:** "Public interface tests. Tests verify behavior through module boundaries (API responses, function return values, observable state changes), not through implementation internals (private methods, internal data structures)."

**Issue:** "API responses, function return values, observable state changes" vs "private methods, internal data structures" - first list has three items with varied structure, second has two.

**Analysis:** First list mixes noun phrases of different types; not strictly parallel.

**Suggested revision:** "Tests verify behavior through module boundaries (API responses, function returns, state changes), not through implementation internals (private methods, internal structures)." (parallel noun phrases)

---

**Line 87:** "if cleanup is needed (extract shared logic, rename for clarity, remove duplication)."

**Issue:** Three parallel infinitive phrases, but varying in structure: "extract [object]", "rename [PP]", "remove [object]"

**Analysis:** Close to parallel, but "rename for clarity" breaks pattern with prepositional phrase.

**Suggested revision:** "if cleanup is needed (extract shared logic, clarify names, remove duplication)." (all verb + object)

---

**Line 98-100:** "Actual behavior: what happens now / Expected behavior: what should happen / Reproduction: steps or conditions (if applicable)"

**Issue:** First two use "what" clauses, third uses "steps or conditions" (noun phrase).

**Analysis:** Parallel structure breaks in third item.

**Suggested revision:** "Actual behavior: what happens now / Expected behavior: what should happen / Reproduction: how to trigger it (if applicable)" (all "what/how" clauses)

---

**Line 115-119:** TDD Fix Plan numbered items

**Issue:** Each item uses parallel structure internally ("RED: ... / GREEN: ...") but the pattern is consistent.

**Analysis:** This is GOOD parallel construction. No violation.

---

**Line 127-130:** Acceptance Criteria checkboxes

**Issue:** Four items with varied structure:
- "Root cause is addressed" (passive)
- "All new tests pass" (active)
- "Existing tests still pass" (active)
- "No regression in adjacent functionality" (negative noun phrase)

**Analysis:** Mixed voice and form breaks parallel structure.

**Suggested revision:**
- "Fix addresses root cause, not just symptom" (active)
- "All new tests pass" (active)
- "All existing tests pass" (active)
- "Adjacent functionality remains intact" (active)

(All active voice, parallel structure)

---

## Minor & Stylistic

### 6. Emphatic position (R18, Moderate)

**Line 12:** "Autonomously diagnose a reported bug, trace its root cause, design a TDD fix plan, and publish a GitHub issue -- all with minimal user interaction."

**Issue:** Ends with weak qualifier "minimal user interaction" rather than main point.

**Suggested revision:** "With minimal user interaction, autonomously diagnose a reported bug, trace its root cause, design a TDD fix plan, and publish a GitHub issue." (moves weak element to front, ends with strong action "publish a GitHub issue")

---

**Line 19:** "Follow-up questions waste the user's time when the codebase contains all the evidence."

**Issue:** Ends with "all the evidence" (abstract). Key point is "waste time."

**Suggested revision:** "When the codebase contains the evidence, follow-up questions waste the user's time." (ends with emphatic "waste the user's time")

---

**Line 28:** "Do NOT ask follow-up questions. Start investigating immediately."

**Issue:** Good emphatic positioning - "immediately" in final position.

**Analysis:** This is GOOD emphatic positioning. No violation.

---

**Line 61:** "Minimal fix: the smallest change that addresses the root cause"

**Issue:** Ends with "root cause" (key concept) - good emphatic positioning.

**Analysis:** This is GOOD emphatic positioning. No violation.

---

**Line 80:** "A good test description reads like a spec; a bad one reads like a diff."

**Issue:** Ends strongly with concrete contrast "diff" vs abstract "spec."

**Suggested revision:** "A good test description reads like a spec; a bad one reads like a diff." (keep as is - the contrast "spec/diff" works well in final position)

**Analysis:** Actually GOOD as written. The concrete "diff" provides strong ending to contrast.

---

**Line 81:** "The plan must remain useful after major refactors."

**Issue:** Ends with "major refactors" - somewhat weak.

**Suggested revision:** "Major refactors must not invalidate the plan." (ends with "the plan" - the subject of preservation)

**Alternative:** "The plan survives major refactors." (ends with strong verb)

---

**Line 93:** "Do NOT ask the user to review before creating -- publish directly and share the URL."

**Issue:** Ends with "the URL" (weak, administrative detail).

**Suggested revision:** "Do NOT ask the user to review before creating -- share the URL after publishing directly." (ends with strong action "publishing directly")

**Alternative:** "Publish directly without asking for review, then share the URL." (ends with "URL" but stronger action)

---

**Line 133:** "After creating the issue, print the issue URL and a one-line summary of the root cause."

**Issue:** Ends with "root cause" (strong concept) - good emphatic positioning.

**Analysis:** This is GOOD emphatic positioning. No violation.

---

**Line 140:** "Create the issue anyway with findings -- partial diagnosis is more valuable than no documentation."

**Issue:** Ends with negative "no documentation."

**Suggested revision:** "Create the issue anyway with findings -- partial diagnosis beats silence." (ends with concrete "silence")

---

### 7. Minor style issues

**Line 12:** "Autonomously diagnose a reported bug..."

**Issue:** Imperative sentence fragment (no subject).

**Analysis:** This is acceptable in instructional/command context. Imperative mood is standard for procedures.

---

**Line 72-74:** "Vertical slices only. Each cycle writes one test then one implementation change. Never batch all tests first then all implementation."

**Issue:** Three short declarative sentences. Could create monotony if pattern continues.

**Analysis:** Acceptable for emphasis in rule list. Variety in surrounding context prevents monotony.

---

**Line 150:** "*Originally based on triage-issue from https://github.com/mattpocock/skills, MIT licensed. Adapted and enhanced for this plugin.*"

**Issue:** Passive "based on" construction.

**Suggested revision:** "*Matt Pocock's triage-issue (https://github.com/mattpocock/skills, MIT licensed) inspired this version, which we adapted and enhanced.*" (active construction)

---

## Summary

**Total findings: 47**
- Critical & Severe: 14 (R10 active voice)
- Moderate: 33 (R13 needless words: 14, R12 concrete: 7, R11 positive: 6, R15 parallel: 5, R18 emphatic: 7)
- Minor & Stylistic: 3

**Most frequent violations:**
1. **R10 (Active Voice):** 14 instances of passive constructions obscuring agency, particularly in procedural instructions where active voice would clarify who acts.

2. **R13 (Needless Words):** 14 instances of wordiness, intensifiers ("all," "full," "deep"), and redundant qualifiers.

3. **R12 (Concrete Language):** 7 instances where abstract terms ("autonomous," "depth," "breadth," "durable," "factors") could be replaced with concrete alternatives.

4. **R18 (Emphatic Position):** 7 instances where weak qualifiers or abstract terms occupy final sentence position instead of key concepts.

5. **R15 (Parallel Construction):** 5 instances where coordinate ideas use varied grammatical forms (mixed voice in acceptance criteria, inconsistent question-answer structure in investigation table).

6. **R11 (Positive Form):** 6 instances of negative constructions where positive statements would be clearer.

**Overall assessment:**
The document demonstrates competent technical writing but suffers from passive voice in procedural contexts (where active imperatives would strengthen instruction), moderate wordiness (intensifiers and redundant qualifiers), and occasional abstract language where concrete terms exist. Parallel structure violations appear primarily in lists and criteria. The prose is functional but would gain vigor and clarity from applying Strunk's severity-4 corrections (active voice, concrete language) consistently.

**Severity distribution:**
- Severe (R10, R12): 21 findings requiring correction for clarity and force
- Moderate (R11, R13, R15, R18): 26 findings that would improve polish without blocking comprehension
- Minor (stylistic): 3 findings that are acceptable in context

**Recommended priority:** Address R10 (active voice) and R12 (concrete language) violations first, as these have severe ratings and most impact vigor and clarity. Then address R13 (needless words) and R15 (parallel construction) for polish.
