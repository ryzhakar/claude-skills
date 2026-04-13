# Synthesis: user-story-chef (REVISED -- full inline)

**Baseline**: 978 tokens (SKILL.md) + 1171 tokens (anti-patterns.md) + 919 tokens (slicing.md) = **3068 tokens total**
**D4 Score**: 93/100 -- strongest unit in the set
**References**: 2 files, both inlined. Zero surviving reference files.

---

## Core Points (Untouchable)

1. **Value negotiation units** -- stories are placeholders for conversation with feedback mechanisms, not requirements/specifications/tasks. (D2 rank 1)
2. **INVEST as physics** -- each criterion describes coordination/information/feedback physics, not checklist compliance. (D2 rank 2)
3. **Falsifiable AC hypotheses** -- acceptance criteria prove value delivery; each should answer "if this passes but users still complain, what did we miss?" (D2 rank 3)
4. **Value slicing** -- split by value delivery through all layers, never by component or architectural layer. (D2 rank 4)
5. **Conversation over compliance** -- template is scaffolding for conversation, not the deliverable. (D2 rank 5)

---

## Inline from References

### anti-patterns.md (1171t) -> INLINE compressed (~280t)

Previous synthesis kept as lazy reference. Under revised directive: 1171t < 1200t, must inline.

**Compression strategy**: The SKILL.md body already has a 6-row anti-pattern summary table. The reference adds 8 detailed patterns with symptom/example/diagnosis/cure structure. Inline the 8 patterns as compressed entries: one-line symptom, one-line cure. Cut the full examples and detailed diagnosis prose -- the summary table plus compressed entries give Claude enough signal to diagnose. Keep the two patterns not represented in the existing table (Orphan Card, Moving Target).

### slicing.md (919t) -> INLINE compressed (~200t)

Previous synthesis kept as lazy reference. Under revised directive: 919t < 1200t, must inline.

**Compression strategy**: SKILL.md already has the core slicing principle with before/after example. Inline SPIDR as a compressed 5-technique table (one line per technique with before/after). Inline workflow slicing, data slicing, and interface slicing as one-line descriptions. Inline validation order (3 criteria). Cut the full multi-paragraph examples per technique.

---

## Proposed SKILL.md

```markdown
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
```

---

## Change Log vs Previous Synthesis

| Change | Citation | Rationale |
|--------|----------|-----------|
| anti-patterns.md INLINED (was kept as lazy ref) | Critical directive: ALL refs under 1200t must inline | 1171t file. Compressed to ~280t: 8 patterns as table rows (symptom + cure). Full examples and detailed diagnosis cut. |
| slicing.md INLINED (was kept as lazy ref) | Critical directive: ALL refs under 1200t must inline | 919t file. Compressed to ~200t: SPIDR table (5 rows), 3 additional patterns as one-liners, validation order (3 criteria), deployability test. |
| Description compressed | D3 R13 "partial overlap with body content" | Removed "Teaches function... over form" -- duplicates body's pedagogical arc. Kept triggers. |
| "embedded feedback mechanisms" -> "feedback mechanisms" | D3 R13 "'embedded' implied by 'with'" | Drop word. |
| INVEST table: "Truth" column fixed to parallel verb phrases | D3 R15 "coordinate ideas lack coordinate form" | All entries now verb-initial: Enables, Preserves, Produces, Bounds, Optimizes, Creates. |
| "A story violating it can be excellent" -> "can deliver more value" | D3 R18 "'excellent' is vague quality judgment" | Concrete outcome in emphatic position. |
| Chef's Protocol step 1: "What observable change happens" -> "What can users do afterward that they couldn't do before?" | D3 R12 "'observable change' is vague" | Concrete, user-centered question. |
| Chef's Protocol: all items standardized to imperative + explanation | D3 R15 "items 1-3 use imperative+question, items 4-5 use imperative+statement" | All now imperative + explanatory clause. |
| "The card is the beginning, not the documentation" -> "The card begins discussion, not documentation" | D3 R18 "ends on 'documentation' -- abstract, weak" | Active verb form. |
| Line 26: passive definition rewritten | D3 R10 "passive 'until economically optimal' obscures agency" | "until the team determines the timing is right" |
| Line 28: "a slice of value, not a slice of work" -> "tasks decompose work; stories decompose value for users" | D3 R12 "abstract where concrete would serve better" | Concrete contrast. |
| Preserved: "The Lie You Were Taught" framing | D2 core point 1; D4 "Strong pedagogical structure" | Distinctive confrontational pedagogy. |
| Preserved: "Fix the physics, not the form." | D2 core point 2; D3 R18 "STRONG and well-placed" | Motto in correct emphatic position. |
| Preserved: "It is NOT" list | D2 core point 1 | Load-bearing negations dismantling misconceptions. |
| Preserved: all form-vs-function contrast pairs | D2 core points 3-4; D4 "Outstanding examples" | Before/after pairs are the most reliable steering mechanism. |
| Attribution footer -> removed | Context cost | To ATTRIBUTION file. |

---

## Projected Token Delta

| Category | Tokens |
|----------|--------|
| Baseline (SKILL.md + 2 refs) | 3068 |
| Inline anti-patterns catalog | +280 |
| Inline slicing techniques | +200 |
| Delete anti-patterns.md | -1171 |
| Delete slicing.md | -919 |
| Strunk compression + D4 fixes | -45 |
| **Projected SKILL.md** | **~1413** |
| **Net reduction** | **~1655 tokens (53.9%)** |
| **Surviving reference files** | **0** |

The anti-patterns compress from 1171t to ~280t by converting 8 detailed symptom/example/diagnosis/cure blocks into a summary table. The slicing techniques compress from 919t to ~200t by converting full multi-paragraph SPIDR examples into a table + one-line pattern descriptions.

SKILL.md grows from ~978t to ~1413t (+435t), well within the 500-line / 5000-token guideline. In exchange, 2090t of reference files are eliminated. Total context footprint drops from 3068t to ~1413t.

The previous synthesis argued these references were "genuinely deferrable with strong gates." That analysis was correct on optionality but wrong on the cost calculation: models in practice ignore lazy reference gates. Inlining at 35% compression ratio produces a net token reduction AND guarantees the content is present when needed.
