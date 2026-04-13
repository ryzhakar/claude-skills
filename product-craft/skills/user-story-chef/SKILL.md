---
name: user-story-chef
description: >
  Writes user stories as value negotiation units, not template-filling exercises.
  Triggers: writing user stories, acceptance criteria, backlog items, story splitting,
  evaluating story quality, INVEST criteria application. Use when creating or refining
  Agile artifacts that capture work units.
---

# User Story Chef

Write stories that minimize the cost of being wrong, not stories that look correct.

## The Lie You Were Taught

**Form:** "As a [persona], I want [need] so that [benefit]"

**Truth:** The template is scaffolding for conversation, not the deliverable. A story following the template perfectly can be worthless. A story violating it can deliver more value.

## What a User Story Actually Is

A user story is a **unit of value negotiation with feedback mechanisms**.

It is NOT:
- A requirement (it's a placeholder that defers detail until the team determines the timing is right)
- A specification (it's an invitation to discuss)
- A task (tasks decompose work; stories decompose value for users)

## INVEST as Physics, Not Checklist

| Criterion | Convention (Form) | Truth (Function) |
|-----------|-------------------|------------------|
| **Independent** | "Stories shouldn't depend on each other" | Enables parallel work and flexible prioritization -- coordination physics |
| **Negotiable** | "Details can change" | Preserves optionality until last responsible moment -- information economics |
| **Valuable** | "Delivers user value" | Produces measurable outcome -- enables prioritization |
| **Estimable** | "Team can estimate it" | Bounds uncertainty -- predictability for planning |
| **Small** | "Fits in a sprint" | Optimizes feedback loops -- smaller = faster learning |
| **Testable** | "Has acceptance criteria" | Creates binary completion state -- prevents ambiguity |

A story violating INVEST isn't "bad" -- it has suboptimal feedback characteristics. Fix the physics, not the form.

## Acceptance Criteria as Hypotheses

AC are falsifiable hypotheses about value delivery.

**Cook's AC (Form):**
```
- User can click button
- System shows message
- Data saves to database
```

**Chef's AC (Function):**
```
Given [precondition that makes this valuable]
When [action that delivers the value]
Then [observable outcome that proves value was delivered]
```

Each criterion should answer: "If this passes but users still complain, what did we miss?"

## Story Slicing

Split by value delivery, not by component or layer.

**Wrong (component slicing):**
1. Build database schema
2. Build API endpoints
3. Build frontend form

**Right (value slicing):**
1. User can submit simplest case (happy path, hardcoded everything else)
2. User can handle rejection case (adds error value)
3. User can see history (adds retrospective value)

Each slice is deployable and testable. Each delivers incremental value.

### SPIDR Decomposition

Five techniques for splitting stories:

| Technique | When to Use | Example |
|-----------|-------------|---------|
| **Spike** | Uncertainty blocks estimation | Extract time-boxed investigation; then build on the decision |
| **Paths** | Multiple workflow variations | Split "checkout" into: saved payment, new card, PayPal, failed+retry |
| **Interface** | Multiple channels/devices | Split "view dashboard" into: desktop, mobile, email summary |
| **Data** | Varying data scope | Split "export users" into: single user, filtered subset, all with progress |
| **Rules** | Varying business rule complexity | Split "calculate tax" into: single-state, exemptions, multi-jurisdiction |

### Additional Slicing Patterns

- **Workflow slicing**: Decompose by stages of a user journey (initiate, review, input, choose, transact, confirm). Each stage is independently valuable.
- **Data lifecycle slicing**: Decompose by CRUD operations. Start with READ (proves data exists), then CREATE, then UPDATE/DELETE.
- **Interface fidelity slicing**: Decompose by interaction richness (exact match, fuzzy match, filters, sorting, suggestions). Each layer adds richness.

### Validation Order

When multiple slices exist, order by:
1. **Highest risk** -- validate assumptions that could invalidate everything
2. **Highest learning** -- get feedback that informs remaining slices
3. **Highest value** -- deliver what matters most if project is cut short

Every slice must be independently deployable and deliver observable value. Test: can a user tell the difference before and after this slice ships?

## Anti-Patterns: Form Addiction Symptoms

When you see these, you're mimicking, not thinking:

| Symptom | Diagnosis |
|---------|-----------|
| Story fits template but team asks "what does this mean?" | Card without Conversation |
| AC list technical steps, not user outcomes | Implementation leaking into specification |
| Story can only be done by one specialist | Sliced by skill, not by value |
| "As a developer, I want..." | Story serves system, not user |
| Story takes multiple sprints | Not a story -- it's an epic wearing a mask |
| Team debates story during implementation | Insufficient Conversation before commitment |

### Detailed Anti-Pattern Catalog

| Anti-Pattern | Symptom | Cure |
|-------------|---------|------|
| **Template Worship** | Follows template perfectly, team still asks "what does this actually mean?" | Ask "what observable behavior changes?" and rewrite with specificity |
| **Technical Story** | "As a developer..." or "As the system..." | Find the user value it enables, or track as technical debt separately |
| **Epic in Disguise** | Seems reasonable, takes multiple sprints, scope keeps growing | Decompose by specific, completable sub-outcomes |
| **Componentized Story** | Maps to technical layers (DB -> API -> UI), sequential dependencies | Slice thin vertically through all layers; each slice delivers complete value |
| **Orphan Card** | Card goes straight from backlog to sprint without refinement | Require refinement session: team estimates without wild variance, edge cases identified, AC agreed |
| **Implementation Leak** | AC describe HOW (calls POST /api/users, inserts row) not WHAT | Rewrite AC as observable outcomes: "user sees confirmation", "user appears in admin list" |
| **Moving Target** | Story changes during sprint, "one more thing" becomes three | Stories freeze once committed; new requirements become new stories for future sprints |
| **Checkbox AC** | AC test existence (button exists, button is blue) not function | AC should be user-verifiable: "user submits form and receives confirmation within 3 seconds" |

## The Chef's Protocol

1. **Start with outcome**: What can users do afterward that they couldn't do before?
2. **Find the smallest slice**: Identify the minimum that delivers that outcome
3. **Write AC as experiments**: Specify how to prove the outcome occurred
4. **Use template if helpful**: The format serves clarity, not compliance
5. **Invite conversation**: The card begins discussion, not documentation
