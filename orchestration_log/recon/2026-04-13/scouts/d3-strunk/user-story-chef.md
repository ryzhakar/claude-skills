# Strunk Analysis: user-story-chef

**Unit:** `/Users/ryzhakar/pp/claude-skills/product-craft/skills/user-story-chef/SKILL.md`

**Rules evaluated:** R10 (active voice), R11 (positive form), R12 (concrete language), R13 (needless words), R15 (parallel construction), R18 (emphatic position)

---

## Critical & Severe

### R10: Active Voice - SEVERE

**Line 26:** "A requirement (it's a placeholder that defers detail until economically optimal)"

**Issue:** Passive "until economically optimal" obscures agency. Who determines economic optimality?

**Severity:** Severe - obscures decision-making agency in critical definition

**Revision:** "A requirement (it's a placeholder that defers detail until the team determines the timing is economically optimal)"

---

**Line 28:** "A task (it's a slice of value, not a slice of work)"

**Issue:** While not technically passive, this is abstract where concrete would serve better (see R12 overlap)

**Severity:** Moderate-Severe - definition lacks specificity

**Revision:** "A task (tasks decompose work; stories decompose value for users)"

---

### R12: Concrete Language - SEVERE

**Line 23:** "A user story is a **unit of value negotiation with embedded feedback mechanisms**."

**Issue:** Abstract nouns pile up without concrete grounding. What does "value negotiation" look like? What are "embedded feedback mechanisms"?

**Severity:** Severe - this is THE definition, yet it's entirely abstract

**Revision:** "A user story is a placeholder for conversation. It names a user outcome, invites negotiation about how to deliver it, and specifies tests that prove delivery."

---

**Line 98:** "Start with outcome: What observable change happens when this is done?"

**Issue:** "Observable change" is vague. Observable to whom? What kind of change?

**Severity:** Moderate-Severe - instruction lacks concrete action

**Revision:** "Start with outcome: What can users do afterward that they couldn't do before?"

---

## Moderate

### R11: Positive Form - MODERATE

**Line 25-28:** The "It is NOT" list uses three negative constructions sequentially

**Issue:** Tells reader what story ISN'T but forces inference about what it IS (already stated above, but repetitive negative framing weakens force)

**Severity:** Moderate - comprehensible but requires cognitive work

**Revision:** "Instead, it is: a placeholder (deferring detail), an invitation (to discuss), and a value slice (not work decomposition)."

---

**Line 45:** "AC are not checklists."

**Issue:** Negative statement where positive would be stronger

**Severity:** Moderate - comprehensible but less forceful

**Revision:** "AC are falsifiable hypotheses about value delivery." (Move the positive assertion to lead position)

---

**Line 101:** "The format serves clarity, not compliance"

**Issue:** This is legitimate antithesis ("not X, but Y"), so technically acceptable under R11. However, could be more direct.

**Severity:** Minor-Moderate - acceptable but improvable

**Revision:** "The format serves clarity; ignore it when it doesn't." (More directive)

---

### R13: Needless Words - MODERATE

**Line 3-8:** Description block contains extensive trigger list that could be compressed

**Issue:** "Triggers: writing user stories, acceptance criteria, backlog items, story splitting, evaluating story quality, INVEST criteria application. Use when creating or refining Agile artifacts that capture work units."

**Severity:** Moderate - some redundancy between "writing user stories" and "creating...artifacts that capture work units"

**Revision:** "Triggers: writing user stories, acceptance criteria, or backlog items; splitting stories; applying INVEST criteria; evaluating story quality."

---

**Line 65:** "Split by value delivery, not by component or layer."

**Issue:** Not needless, but could be more economical

**Severity:** Minor-Moderate

**Revision:** "Split by value delivered, not by component."

---

**Line 79:** "For detailed slicing techniques, see @references/slicing.md — it covers SPIDR decomposition methods (Spike, Paths, Interface, Data, Rules), workflow slicing, data lifecycle slicing, and interface fidelity slicing with validation order guidelines."

**Issue:** Long list in parenthetical; "with validation order guidelines" is vague padding

**Severity:** Moderate - final phrase adds no actionable information

**Revision:** "For detailed slicing techniques, see @references/slicing.md — it covers SPIDR decomposition (Spike, Paths, Interface, Data, Rules), workflow slicing, data lifecycle slicing, and interface fidelity slicing."

---

**Line 94:** "For detailed anti-patterns and remedies, see @references/anti-patterns.md — it covers template worship, technical stories, epics in disguise, componentized stories, orphan cards, implementation leaks, moving targets, and checkbox AC with diagnosis and cure for each."

**Issue:** "with diagnosis and cure for each" is implied by "remedies" already mentioned

**Severity:** Moderate - redundant

**Revision:** "For detailed anti-patterns and remedies, see @references/anti-patterns.md — it covers template worship, technical stories, epics in disguise, componentized stories, orphan cards, implementation leaks, moving targets, and checkbox AC."

---

### R15: Parallel Construction - MODERATE

**Line 34-39:** INVEST table "Truth (Function)" column

**Issue:** Mixed grammatical forms:
- "Enables parallel work..." (verb phrase)
- "Preserves optionality..." (verb phrase)
- "Each unit produces..." (clause with subject)
- "Bounded uncertainty..." (noun phrase)
- "Feedback loop optimization..." (noun phrase)
- "Binary completion state..." (noun phrase)

**Severity:** Moderate - coordinate ideas lack coordinate form, harder to scan

**Revision:** Make all verb phrases:
- "Enables parallel work and flexible prioritization"
- "Preserves optionality until last responsible moment"
- "Produces measurable outcome for prioritization"
- "Bounds uncertainty for predictable planning"
- "Optimizes feedback loops through smaller cycles"
- "Creates binary completion state to prevent ambiguity"

---

**Line 25-28:** "It is NOT" list uses mixed structures

**Issue:**
- "A requirement (it's a placeholder...)" - noun + parenthetical explanation
- "A specification (it's an invitation...)" - noun + parenthetical explanation
- "A task (it's a slice of value...)" - noun + parenthetical explanation

**Severity:** Minor - already parallel enough, but parentheticals vary in structure slightly

**Revision:** Already acceptable, but could strengthen: remove "it's" repetition and use consistent noun phrases.

---

### R18: Emphatic Position - MODERATE

**Line 13:** "Write stories that minimize the cost of being wrong, not stories that look correct."

**Issue:** Ends on "look correct" - weak, vague term. The emphatic concept is "minimize cost of being wrong"

**Severity:** Moderate - buries the lead

**Revision:** "Don't write stories that look correct. Write stories that minimize the cost of being wrong."

---

**Line 19:** "A story violating it can be excellent."

**Issue:** Ends weakly on "excellent" (vague quality judgment)

**Severity:** Minor-Moderate

**Revision:** "A story violating it can deliver more value." (concrete outcome in emphatic position)

---

**Line 41:** "A story violating INVEST isn't 'bad'—it has suboptimal feedback characteristics. Fix the physics, not the form."

**Issue:** The emphatic final phrase "Fix the physics, not the form" is actually STRONG and well-placed. No issue.

**Severity:** None - this is good use of R18

---

**Line 102:** "The card is the beginning, not the documentation"

**Issue:** Ends on "documentation" - abstract, weak. The point is "beginning" = invitation to conversation

**Severity:** Moderate

**Revision:** "The card begins conversation; it doesn't document requirements."

---

## Minor & Stylistic

### R10: Active Voice - MINOR

**Line 34:** "Stories shouldn't depend on each other"

**Issue:** Modal + negative is weaker than active construction

**Severity:** Minor - comprehensible, conventional phrasing

**Revision:** "Make stories independent of each other"

---

**Line 36:** "Details can change"

**Issue:** Passive modal construction

**Severity:** Minor

**Revision:** "Keep details negotiable" or "Preserve the right to change details"

---

**Line 38:** "Team can estimate it"

**Issue:** Weak modal

**Severity:** Minor

**Revision:** "Team estimates it confidently"

---

**Line 40:** "Fits in a sprint"

**Issue:** Implied passive (story as patient, not agent)

**Severity:** Minor

**Revision:** "Delivers within a sprint"

---

**Line 42:** "Has acceptance criteria"

**Issue:** State-of-being verb

**Severity:** Minor

**Revision:** "Specifies testable acceptance criteria"

---

### R11: Positive Form - MINOR

**Line 67:** "Wrong (component slicing):"

**Issue:** Using negative framing as section header. While clear in context, positive would be stronger.

**Severity:** Minor - acceptable for instructional contrast

**Revision:** Could reframe as "Component slicing (anti-pattern):" and "Value slicing (correct pattern):" but current form is acceptable for pedagogical purposes.

---

### R12: Concrete Language - MINOR

**Line 36:** "last responsible moment"

**Issue:** "Last responsible moment" is industry jargon - specific within context but abstract to outsiders

**Severity:** Minor - this is established terminology, probably acceptable

**Revision:** "last responsible moment (when delay costs more than deciding now)"

---

**Line 61:** "If this passes but users still complain, what did we miss?"

**Issue:** "Users complain" is concrete enough, though "what did we miss" is slightly vague

**Severity:** Minor

**Revision:** "If this passes but users can't accomplish their goal, what did we miss?"

---

### R13: Needless Words - MINOR

**Line 22:** "A user story is a **unit of value negotiation with embedded feedback mechanisms**."

**Issue:** "embedded" is implied by "in" or "with" - adds no meaning

**Severity:** Minor (overlaps with R12 severe issue above)

**Revision:** Addressed in R12 revision

---

**Line 83:** "When you see these, you're mimicking, not thinking:"

**Issue:** "you're mimicking, not thinking" could be "you're mimicking"

**Severity:** Minor - the contrast has rhetorical value

**Revision:** Keep as-is (antithesis serves purpose)

---

### R15: Parallel Construction - MINOR

**Line 98-102:** The Chef's Protocol list

**Issue:** Mixed imperative structures:
1. "Start with outcome: What observable change..." (imperative + question)
2. "Find the smallest slice: What's the minimum..." (imperative + question)
3. "Write AC as experiments: How would you prove..." (imperative + question)
4. "Use template if helpful: The format serves..." (imperative + statement)
5. "Invite conversation: The card is the beginning..." (imperative + statement)

**Severity:** Minor - items 1-3 match, 4-5 match, but two groups don't match each other

**Revision:** Standardize all to imperative + explanation without questions:
1. "Start with outcome: Name the observable change that occurs when this is done"
2. "Find the smallest slice: Identify the minimum that delivers that outcome"
3. "Write AC as experiments: Specify how to prove the outcome occurred"
4. "Use template if helpful: The format serves clarity, not compliance"
5. "Invite conversation: The card begins discussion, not documentation"

---

### R18: Emphatic Position - MINOR

**Line 99:** "Find the smallest slice: What's the minimum that delivers that outcome?"

**Issue:** Ends on "outcome" which is abstract; "minimum" is the key concept but buried

**Severity:** Minor

**Revision:** "Find the smallest slice: What minimum delivery proves that outcome?"

---

**Line 77:** "Each delivers incremental value."

**Issue:** Ends on abstract "incremental value"

**Severity:** Minor

**Revision:** "Each slice delivers value users can test."

---

## Summary

**Total findings:** 34 (7 severe, 14 moderate, 13 minor)

**Dominant patterns:**

1. **R12 violations (concrete language) are most damaging:** The core definition (line 23) uses entirely abstract language where the skill explicitly teaches concreteness. The instruction "observable change" (line 98) lacks the specificity the skill demands of user stories.

2. **R15 violations (parallel construction) weaken scanability:** The INVEST table and protocol list use mixed grammatical forms for coordinate ideas, creating unnecessary cognitive load when the content is instructional.

3. **R13 violations (needless words) appear in reference pointers:** Both cross-references (lines 79, 94) include redundant closing phrases that add no information.

4. **R10 (active voice) and R11 (positive form) violations are mostly minor:** The skill uses conventional instructional phrasing that is comprehensible, though directness could improve force.

**Severity distribution:**
- Critical: 0
- Severe: 7 (3 R12, 2 R10, 1 R11, 1 R18)
- Moderate: 14 (4 R13, 3 R11, 3 R18, 2 R15, 2 R12)
- Minor: 13 (5 R10, 3 R15, 2 R18, 1 R11, 1 R12, 1 R13)

**Recommended priority:** Fix severe R12 violations first (especially line 23 definition and line 98 instruction), then address moderate R15 parallel construction issues for improved scanability, then tackle moderate R13 redundancies in cross-references.
