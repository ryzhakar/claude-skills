# Core Points: user-story-chef

## Iteration 1

**Point**: User stories are units of value negotiation with embedded feedback mechanisms, not requirements, specifications, or tasks.

**Evidence**:
- SKILL.md line 23: "A user story is a **unit of value negotiation with embedded feedback mechanisms**."
- SKILL.md lines 25-28: It is NOT a requirement (placeholder that defers detail), NOT a specification (invitation to discuss), NOT a task (slice of value, not work)
- SKILL.md line 19: "The template is scaffolding for conversation, not the deliverable. A story following the template perfectly can be worthless."

## Iteration 2

**Point**: INVEST criteria describe feedback physics and coordination economics rather than template compliance checkboxes.

**Evidence**:
- SKILL.md lines 32-39: Table reframes each INVEST criterion from "Convention (Form)" to "Truth (Function)" with explanations like "coordination physics", "information economics", "feedback loop optimization"
- SKILL.md line 41: "A story violating INVEST isn't 'bad'—it has suboptimal feedback characteristics. Fix the physics, not the form."
- SKILL.md line 38: "**Small**" means "Feedback loop optimization—smaller = faster learning" not just "Fits in a sprint"

## Iteration 3

**Point**: Acceptance criteria must be falsifiable hypotheses about value delivery, not technical implementation checklists.

**Evidence**:
- SKILL.md line 45: "AC are not checklists. They are **falsifiable hypotheses about value delivery**."
- SKILL.md line 61: "Each criterion should answer: 'If this passes but users still complain, what did we miss?'"
- anti-patterns.md lines 155-177: The Checkbox AC anti-pattern shows AC testing existence (button exists, button is blue) versus user-verifiable outcomes (user receives confirmation within 3 seconds)

## Iteration 4

**Point**: Story slicing must be done by value delivery through all layers, never by technical component or architectural layer.

**Evidence**:
- SKILL.md lines 65-77: "Wrong (component slicing)" shows database/API/frontend as separate stories; "Right (value slicing)" shows each slice is deployable and testable with incremental value
- anti-patterns.md lines 75-96: The Componentized Story anti-pattern shows Sprint 1-3 doing DB/API/UI versus slicing vertically where "Each slice touches all layers but delivers complete value"
- slicing.md line 17: "**Every slice must be independently deployable and deliver observable value.**" with test "Can a user tell the difference before and after this slice ships?"

## Iteration 5

**Point**: The template format serves clarity and conversation, not compliance or documentation completeness.

**Evidence**:
- SKILL.md line 101: In The Chef's Protocol, step 4 is "**Use template if helpful**: The format serves clarity, not compliance"
- SKILL.md line 102: Step 5 is "**Invite conversation**: The card is the beginning, not the documentation"
- anti-patterns.md lines 99-110: The Orphan Card shows that without conversation (one of the 3 C's), "The card is a placeholder; without discussion, it's incomplete documentation"

## Rank Summary

1. **Value negotiation units** — Foundational ontological claim that defines what stories ARE versus what they're mistaken for
2. **Physics not checklist** — Reframes the canonical INVEST model from template to function, pervades entire diagnostic approach
3. **Falsifiable hypotheses** — Transforms AC from passive lists to active experiments, directly impacts story execution
4. **Value slicing** — The primary decomposition strategy, covered extensively in SKILL.md and dedicated slicing.md reference
5. **Conversation over compliance** — Meta-principle about template usage that prevents all form-over-function anti-patterns
