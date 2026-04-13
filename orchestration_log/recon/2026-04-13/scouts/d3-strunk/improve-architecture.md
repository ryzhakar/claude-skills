# Strunk Analysis: improve-architecture

## Critical & Severe

### R10 (Active Voice) - Severe
**Line 5-6:** "This skill should be used when the user asks to..."
- **Issue:** Passive construction obscures agent and weakens directive force
- **Severity:** Severe (R10 severity per Strunk taxonomy)
- **Revision:** "Use this skill when the user asks to..." OR "Claude should use this skill when..."

**Line 34:** "Do NOT follow rigid heuristics"
- **Issue:** While imperative is active, the negative weakens. Per R11, positive form is clearer.
- **Cross-reference:** See R11 findings below
- **Revision:** "Follow organic navigation patterns" or "Explore as a developer would"

**Line 56:** "Dependency category | Classify using the 4-category framework..."
- **Issue:** Passive implied ("is classified using"). Table format makes this borderline acceptable.
- **Severity:** Moderate (context-sensitive)
- **Note:** Tables trade vigor for structure; acceptable here

**Line 116:** "After the user selects a design (or accepts the recommendation), create a GitHub issue..."
- **Issue:** "is selected" implied in parenthetical
- **Severity:** Minor
- **Note:** Main verb "create" is active and imperative; parenthetical acceptable

### R12 (Concrete Language) - Severe
**Line 34-35:** "Navigate the codebase organically. Do NOT follow rigid heuristics -- explore as a developer would"
- **Issue:** "Organically" is abstract metaphor; "as a developer would" lacks specificity
- **Severity:** Severe (vague guidance for critical phase)
- **Revision:** "Navigate by following imports, tracing call chains, and reading files that reference each other. Note where understanding breaks down."

**Line 45-46:** "The friction experienced during exploration IS the signal."
- **Issue:** "Friction" as metaphor is acceptable, but "IS the signal" is abstract
- **Severity:** Moderate
- **Revision:** "Difficulty navigating the code reveals the same friction every future developer (and AI agent) will face." (This already exists at line 46-47, making line 45 somewhat redundant)

**Line 108:** "Which handles the common case most naturally?"
- **Issue:** "Most naturally" is vague/subjective
- **Severity:** Moderate
- **Revision:** "Which requires fewest lines for the common case?" OR "Which exposes the simplest interface for typical callers?"

### R13 (Needless Words) - Moderate
**Line 3-8:** Description block contains redundant trigger phrases
- **Issue:** "improve the architecture", "find refactoring opportunities", "deepen shallow modules", "consolidate tightly-coupled code" are near-synonyms. List is exhaustive to aid matching but borders on verbose.
- **Severity:** Minor (frontmatter context justifies thoroughness for skill discovery)
- **Note:** Acceptable for skill discovery; would be severe in prose body

**Line 34:** "Navigate the codebase organically. Do NOT follow rigid heuristics -- explore as a developer would and note where understanding breaks down"
- **Issue:** Three directives saying similar things
- **Severity:** Moderate
- **Revision:** "Explore as a developer would, noting where understanding breaks down" (eliminates "organically" and "Do NOT follow rigid heuristics")

**Line 59-60:** "Do NOT propose interfaces yet. Ask the user: 'Which of these candidates would you like to explore?'"
- **Issue:** "yet" is implied by "Ask the user"; sequence is clear
- **Severity:** Minor
- **Revision:** "Ask the user: 'Which of these candidates would you like to explore?'" (omit first sentence)

**Line 117:** "Do NOT ask the user to review before creating -- publish directly and share the URL."
- **Issue:** "publish directly" and "Do NOT ask... before creating" are redundant
- **Severity:** Moderate
- **Revision:** "Publish the issue directly and share the URL." OR "Create the issue without asking for review; share the URL."

## Moderate

### R11 (Positive Form) - Moderate
**Line 34:** "Do NOT follow rigid heuristics"
- **Issue:** Negative construction; reader must infer what TO do
- **Severity:** Moderate
- **Revision:** "Explore fluidly, following connections as they emerge" OR "Follow organic navigation patterns"

**Line 59:** "Do NOT propose interfaces yet."
- **Issue:** Negative; reader knows what not to do but implication is clear from next sentence
- **Severity:** Minor (next sentence provides positive action)
- **Revision:** "Present candidates first. After user selects, frame the problem space (Phase 3)."

**Line 117:** "Do NOT ask the user to review before creating"
- **Issue:** Negative instruction
- **Severity:** Moderate
- **Revision:** "Publish directly without review and share the URL."

**Line 122:** "Old unit tests on shallow modules are waste once boundary tests exist -- delete them"
- **Issue:** "are waste" is negative framing
- **Severity:** Minor
- **Revision:** "Boundary tests supersede old unit tests on shallow modules -- delete the old tests."

**Line 84:** "Minimize the interface"
- **Issue:** "Minimize" is negative (reduce/remove). While concise, positive form exists.
- **Severity:** Stylistic (constraint tables may favor terse negatives)
- **Revision:** "Aim for 1-3 entry points maximum" (already present; "Minimize" adds force)

### R15 (Parallel Construction) - Moderate
**Line 22-24:** "More testable / More navigable / More maintainable"
- **Status:** CORRECT - parallel "More [adjective]: [explanation]" structure
- **Note:** No violation; exemplar of good parallelism

**Line 37-42:** Friction signal list
- **Issue:** Mixed grammatical forms:
  - "Bouncing: Understanding..." (gerund phrase)
  - "Shallow interfaces: A module's..." (noun phrase)
  - "Testability extraction: Pure functions..." (noun phrase)
  - "Tight coupling: Modules share..." (verb phrase)
  - "Test gaps: Modules that are..." (relative clause)
- **Severity:** Moderate
- **Revision:** Make all items noun phrases OR all complete sentences describing the phenomenon

**Line 54-57:** Table structure uses parallel construction correctly
- **Status:** CORRECT
- **Note:** All rows follow "Field | Content" pattern

**Line 93-97:** Agent outputs list
- **Issue:** Items 1-3 are noun phrases ("Interface signature", "Usage example", "What complexity..."). Items 4-5 shift to different structure.
- **Severity:** Minor (numbered list format is inherently parallel)
- **Note:** Item 3 "What complexity gets hidden internally" breaks from noun-phrase pattern of 1-2

**Lines 67-70:** Constraints/dependencies/sketch structure
- **Status:** CORRECT - all noun phrases ("Constraints...", "Dependencies...", "A rough...")
- **Note:** Good parallelism

### R18 (Emphatic Position) - Moderate
**Line 11:** "Explore a codebase to surface architectural friction, discover module-deepening opportunities, and propose refactors through structured multi-design exploration. Publish results as a GitHub issue RFC."
- **Issue:** First sentence ends with "structured multi-design exploration" (process) rather than "refactors" (outcome). Second sentence ends weakly with "RFC" (format) rather than outcome.
- **Severity:** Moderate
- **Revision:** "Explore a codebase to surface architectural friction, discover module-deepening opportunities, and propose concrete refactors. Publish results as a GitHub issue RFC for stakeholder review."

**Line 19:** "A deep module (John Ousterhout, 'A Philosophy of Software Design') has a small interface hiding a large implementation."
- **Issue:** Definition sentence ends with "implementation" - correct subject matter but weak word
- **Severity:** Minor
- **Revision:** "A deep module (John Ousterhout) hides a large implementation behind a small interface." (ends with "interface" - the key architectural concept)

**Line 26-28:** "The opposite -- shallow modules where the interface is nearly as complex as the implementation -- creates integration risk in the seams between modules and forces tests to mirror internal structure."
- **Issue:** Ends with "internal structure" - accurate but weak
- **Severity:** Minor
- **Revision:** "...creates integration risk in the seams and forces tests to mirror implementation rather than behavior." (ends with the key contrast: behavior vs. implementation)

**Line 46:** "Difficulty navigating the code reveals the same friction every future developer (and AI agent) will face."
- **Status:** CORRECT - ends emphatically with "will face" - the forward-looking consequence
- **Note:** Good emphatic positioning

**Line 71:** "this is NOT a proposal -- just grounding for the constraints"
- **Issue:** Ends with "constraints" - correct emphasis
- **Status:** ACCEPTABLE

**Line 109:** "The user wants a strong read, not a menu."
- **Issue:** Ends with "menu" - the rejected option rather than the desired outcome
- **Severity:** Moderate
- **Revision:** "Provide an opinionated recommendation, not a menu. The user wants a strong read."

## Minor & Stylistic

### R10 (Active Voice) - Minor instances
**Line 8:** "Produces multi-design exploration with dependency-aware testing strategy"
- **Issue:** Implied subject (skill/process) makes this technically passive
- **Severity:** Stylistic (frontmatter description context)
- **Note:** Acceptable in description block; would revise in prose body

**Line 20:** "Deep modules are: More testable..."
- **Status:** CORRECT - "are" is linking verb with adjectives; not passive
- **Note:** No violation

**Line 50:** "Present a numbered list"
- **Status:** CORRECT - active imperative
- **Note:** Exemplar

### R13 (Needless Words) - Minor instances
**Line 13:** "Explore a codebase to surface architectural friction, discover module-deepening opportunities, and propose refactors through structured multi-design exploration."
- **Issue:** "through structured multi-design exploration" is wordy (5 words) for the method
- **Severity:** Minor (establishes methodology upfront)
- **Revision:** "...and propose refactors via multi-design exploration."

**Line 66:** "write a user-facing explanation BEFORE launching design agents"
- **Issue:** "BEFORE launching" is emphasized but "then immediately proceed to Phase 4" at line 72 creates redundancy
- **Severity:** Minor
- **Note:** Emphasis pattern (BEFORE... then immediately) ensures sequencing; acceptable

**Line 89:** "the cheapest available model, each working independently with its own design constraint"
- **Issue:** "each working independently" + "its own design constraint" both assert independence
- **Severity:** Minor
- **Revision:** "the cheapest available model, each with its own design constraint"

### R15 (Parallel Construction) - Minor instances
**Line 82-87:** Agent constraint table
- **Status:** CORRECT - all rows follow "Agent | Constraint [verb phrase]" pattern
- **Note:** Good parallelism; agent 4 has conditional ("if applicable") which is acceptable

### R18 (Emphatic Position) - Minor instances
**Line 32:** "Navigate the codebase organically."
- **Issue:** Ends with abstract adverb "organically"
- **Severity:** Minor (already flagged under R12)
- **Note:** Cross-reference to R12 finding

**Line 111:** "If elements from different designs combine well, propose a hybrid."
- **Status:** CORRECT - ends with "hybrid" (the recommended action)
- **Note:** Good emphatic positioning

## Summary

**Total findings:** 23 across all categories

**Critical & Severe (5 findings):**
- R10 violations: 1 clear passive construction (line 5-6)
- R12 violations: 3 instances of abstract/vague language in critical guidance (lines 34-35, 108)
- R13 violations: 1 moderate redundancy (line 117)

**Moderate (11 findings):**
- R11: 4 negative constructions where positive alternatives exist
- R15: 2 parallel construction breaks (friction list lines 37-42, outputs list line 93-97)
- R18: 5 weak emphatic positions (lines 11, 26-28, 109)

**Minor & Stylistic (7 findings):**
- R10: 1 borderline passive in frontmatter
- R13: 3 minor wordiness instances
- R15: 0 (all parallel structures correct or minor)
- R18: 3 minor weak endings

**Severity distribution:**
- Critical: 0
- Severe: 5 (2.1% of text by line count)
- Moderate: 11 (4.6%)
- Minor/Stylistic: 7 (2.9%)

**Overall assessment:** The skill exhibits strong technical writing with clear imperative voice and well-structured protocols. Primary weaknesses cluster around:
1. Abstract guidance in Phase 1 (R12) where concrete examples would strengthen
2. Negative constructions (R11) that could be reframed positively
3. Emphatic positioning (R18) that sometimes buries the lead

The parallel construction (R15) is generally excellent, especially in tables and lists. Active voice (R10) dominates except for the frontmatter passive. Economy (R13) is good overall; redundancies are minor and sometimes serve emphasis.

**Recommendation:** Address the 5 severe findings (lines 5-6, 34-35, 108, 117) to bring prose to high vigor. Moderate findings are refinements that improve but don't impair comprehension.
