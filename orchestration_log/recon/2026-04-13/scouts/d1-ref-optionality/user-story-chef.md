# Reference Optionality Analysis: user-story-chef

## Skill Overview
- **Name:** user-story-chef
- **Core Purpose:** Write user stories as value negotiation units, not template-filling exercises
- **Trigger Contexts:** writing user stories, acceptance criteria, backlog items, story splitting, evaluating story quality, INVEST criteria

## Current Reference Architecture
SKILL.md currently references 2 reference files:
1. `slicing.md` (line 79: "For detailed slicing techniques, see @references/slicing.md")
2. `anti-patterns.md` (line 94: "For detailed anti-patterns and remedies, see @references/anti-patterns.md")

---

## Reference 1: slicing.md

**File:** `/Users/ryzhakar/pp/claude-skills/product-craft/skills/user-story-chef/references/slicing.md`
**Lines:** 144 lines
**Content Summary:** Value decomposition methods for breaking epics into stories and stories into smaller stories. Covers:
- SPIDR decomposition methods (Spike, Paths, Interface, Data, Rules)
- Workflow slicing
- Data lifecycle slicing
- Interface fidelity slicing
- Validation order guidelines

### Classification: DEFERRABLE

**Reasoning:**
- SKILL.md already covers the core principle of story slicing (lines 63-78)
- The core message "split by value delivery, not by component" is clearly stated with examples
- The reference provides EXPANSION: specific techniques, patterns, and systematic approaches
- Not needed for basic story creation or AC writing
- Only needed when user explicitly asks about slicing techniques or epic decomposition

**Proposed Loading Gate:**
```
IF (user asks about "story slicing" OR "epic decomposition" OR "break down story" OR "SPIDR" OR "split this story" OR user has a large/multi-sprint story that needs decomposition)
THEN read @references/slicing.md
```

**Gate Robustness:** STRONG
- The gate captures both explicit requests (mentions "slicing", "decomposition", "split")
- Captures implicit need (story too large)
- Condition is falsifiable: if user is NOT asking about slicing, reference is NOT needed
- SKILL.md body is sufficient for all other user-story-chef invocations

---

## Reference 2: anti-patterns.md

**File:** `/Users/ryzhakar/pp/claude-skills/product-craft/skills/user-story-chef/references/anti-patterns.md`
**Lines:** 179 lines
**Content Summary:** Form addiction symptoms and their cures. Covers 8 anti-patterns:
1. Template Worship
2. The Technical Story
3. The Epic in Disguise
4. The Componentized Story
5. The Orphan Card
6. The Implementation Leak
7. The Moving Target
8. The Checkbox AC

Each pattern includes: symptom description, example, diagnosis, and cure.

### Classification: DEFERRABLE

**Reasoning:**
- SKILL.md already covers anti-pattern recognition at conceptual level (lines 82-93)
- The core diagnostic symptoms are listed in the table
- The reference provides DEPTH: detailed examples, specific diagnoses, and remediation steps
- Not needed for basic story writing
- Only needed when user presents problematic stories for evaluation, or asks "why is this story bad", or requests anti-pattern guidance

**Proposed Loading Gate:**
```
IF (user asks to "evaluate story quality" OR "review this story" OR "what's wrong with this story" OR "why is this bad" OR mentions anti-patterns OR provides story text that exhibits anti-pattern symptoms)
THEN read @references/anti-patterns.md
```

**Gate Robustness:** STRONG
- Captures explicit evaluation requests
- Captures implicit evaluation (user provides story text to analyze)
- Captures anti-pattern mentions
- Condition is falsifiable: if user is writing NEW stories (not evaluating existing ones), reference is NOT needed
- SKILL.md's anti-pattern table (lines 82-93) provides sufficient awareness for most creation tasks

---

## Summary Verdict

| Reference | Classification | Confidence | Loading Trigger |
|-----------|---------------|------------|-----------------|
| `slicing.md` | DEFERRABLE | HIGH | User asks about slicing/decomposition OR has multi-sprint story |
| `anti-patterns.md` | DEFERRABLE | HIGH | User asks to evaluate/review story quality OR provides story text to analyze |

**Both references are DEFERRABLE.**

### Workflow Coverage Analysis

**Core workflow (ESSENTIAL, handled by SKILL.md body):**
1. Understanding what a user story actually is (value negotiation unit)
2. INVEST criteria interpretation (physics, not checklist)
3. Writing acceptance criteria as falsifiable hypotheses
4. Basic story slicing principle (value vs. component)
5. Basic anti-pattern awareness
6. The Chef's Protocol (5-step creation process)

**Extended workflows (DEFERRABLE, handled by references with gates):**
1. Systematic epic decomposition using SPIDR → `slicing.md`
2. Complex slicing scenarios (workflow/data/interface) → `slicing.md`
3. Validation ordering strategies → `slicing.md`
4. Detailed anti-pattern diagnosis and remediation → `anti-patterns.md`
5. Specific anti-pattern examples and cures → `anti-patterns.md`

**Gate Integrity:**
Both gates are IMPOSSIBLE to ignore when conditions are met:
- If user asks "how do I split this epic?", the slicing gate triggers → read mandatory
- If user asks "what's wrong with this story?", the anti-pattern gate triggers → read mandatory
- If user is just writing a new story from scratch, neither gate triggers → references not needed

**No coverage gaps identified.** The SKILL.md body contains sufficient core knowledge for basic story creation and evaluation. References provide depth only when explicitly or implicitly requested.
