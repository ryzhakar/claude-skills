---
name: user-story-chef
description: >
  Write user stories as value negotiation units, not template-filling exercises.
  Triggers: writing user stories, acceptance criteria, backlog items, story splitting,
  evaluating story quality, INVEST criteria application. Use when creating or refining
  Agile artifacts that capture work units. Teaches function (value decomposition,
  falsifiable AC, feedback optimization) over form (templates).
---

# User Story Chef

Write stories that minimize the cost of being wrong, not stories that look correct.

## The Lie You Were Taught

**Form:** "As a [persona], I want [need] so that [benefit]"

**Truth:** The template is scaffolding for conversation, not the deliverable. A story following the template perfectly can be worthless. A story violating it can be excellent.

## What a User Story Actually Is

A user story is a **unit of value negotiation with embedded feedback mechanisms**.

It is NOT:
- A requirement (it's a placeholder that defers detail until economically optimal)
- A specification (it's an invitation to discuss)
- A task (it's a slice of value, not a slice of work)

## INVEST as Physics, Not Checklist

| Criterion | Convention (Form) | Truth (Function) |
|-----------|-------------------|------------------|
| **Independent** | "Stories shouldn't depend on each other" | Enables parallel work and flexible prioritization—coordination physics |
| **Negotiable** | "Details can change" | Preserves optionality until last responsible moment—information economics |
| **Valuable** | "Delivers user value" | Each unit produces measurable outcome—enables prioritization |
| **Estimable** | "Team can estimate it" | Bounded uncertainty—predictability for planning |
| **Small** | "Fits in a sprint" | Feedback loop optimization—smaller = faster learning |
| **Testable** | "Has acceptance criteria" | Binary completion state—prevents ambiguity |

A story violating INVEST isn't "bad"—it has suboptimal feedback characteristics. Fix the physics, not the form.

## Acceptance Criteria as Hypotheses

AC are not checklists. They are **falsifiable hypotheses about value delivery**.

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

See `references/slicing.md` for decomposition techniques.

## Anti-Patterns: Form Addiction Symptoms

When you see these, you're mimicking, not thinking:

| Symptom | Diagnosis |
|---------|-----------|
| Story fits template but team asks "what does this mean?" | Card without Conversation |
| AC list technical steps, not user outcomes | Implementation leaking into specification |
| Story can only be done by one specialist | Sliced by skill, not by value |
| "As a developer, I want..." | Story serves system, not user |
| Story takes multiple sprints | Not a story—it's an epic wearing a mask |
| Team debates story during implementation | Insufficient Conversation before commitment |

See `references/anti-patterns.md` for detailed patterns and remedies.

## The Chef's Protocol

1. **Start with outcome**: What observable change happens when this is done?
2. **Find the smallest slice**: What's the minimum that delivers that outcome?
3. **Write AC as experiments**: How would you prove the outcome occurred?
4. **Use template if helpful**: The format serves clarity, not compliance
5. **Invite conversation**: The card is the beginning, not the documentation
