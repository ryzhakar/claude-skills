# Story Slicing Techniques

Value decomposition methods for breaking epics into stories and stories into smaller stories.

## Table of Contents
- [The Slicing Principle](#the-slicing-principle)
- [SPIDR Techniques](#spidr-techniques)
- [Workflow Slicing](#workflow-slicing)
- [Data Slicing](#data-slicing)
- [Interface Slicing](#interface-slicing)
- [Validation Order](#validation-order)

---

## The Slicing Principle

**Every slice must be independently deployable and deliver observable value.**

If a slice requires another slice to be useful, you sliced wrong. Go back.

Test: Can a user tell the difference before and after this slice ships?

---

## SPIDR Techniques

Five primary decomposition strategies:

### S — Spike
When uncertainty blocks estimation, extract a time-boxed investigation.

**Before:** "As a user, I want AI-powered recommendations so I get relevant content"
**After:**
1. SPIKE: Investigate recommendation algorithms (2 days, output: decision document)
2. "As a user, I want content ranked by simple popularity so I see what others like"
3. "As a user, I want personalized ranking based on [chosen algorithm]"

### P — Paths
Split by user workflow variations.

**Before:** "As a user, I want to checkout so I can complete my purchase"
**After:**
1. "...checkout with saved payment method" (happy path)
2. "...checkout with new card" (adds input flow)
3. "...checkout with PayPal" (adds integration)
4. "...checkout with failed payment and retry" (adds error handling)

### I — Interface
Split by interaction channel or device.

**Before:** "As a user, I want to view my dashboard"
**After:**
1. "...view dashboard on desktop" (primary)
2. "...view dashboard on mobile" (responsive)
3. "...receive dashboard summary via email" (async channel)

### D — Data
Split by data scope or volume.

**Before:** "As an admin, I want to export all user data"
**After:**
1. "...export single user's data" (minimal)
2. "...export filtered subset of users" (adds query)
3. "...export all users with progress indicator" (adds scale handling)

### R — Rules
Split by business rule complexity.

**Before:** "As a user, I want the system to calculate my tax"
**After:**
1. "...calculate tax for single-state, standard rate" (simplest case)
2. "...calculate tax with exemptions" (adds rules)
3. "...calculate tax across multiple jurisdictions" (adds complexity)

---

## Workflow Slicing

Decompose by stages of a user journey:

```
Epic: User completes purchase

Stories:
1. User adds item to cart (initiation)
2. User views cart summary (review)
3. User enters shipping address (input)
4. User selects shipping method (choice)
5. User completes payment (transaction)
6. User receives confirmation (feedback)
```

Each stage is independently valuable—user can stop at any stage and resume later.

---

## Data Slicing

Decompose by data entity lifecycle:

```
Epic: User manages their profile

Stories:
1. User creates profile (CREATE)
2. User views profile (READ)
3. User updates profile fields (UPDATE)
4. User deletes profile (DELETE)
5. User exports profile data (EXPORT)
```

Start with READ (proves data exists), then CREATE (proves data can be made), then others.

---

## Interface Slicing

Decompose by interaction fidelity:

```
Epic: User searches products

Stories:
1. User searches by exact name match (basic)
2. User searches with partial match (fuzzy)
3. User filters results by category (refinement)
4. User sorts results by price/rating (ordering)
5. User sees search suggestions while typing (enhancement)
```

Each layer adds richness. First slice is usable, subsequent slices are better.

---

## Validation Order

When multiple slices exist, order by:

1. **Highest risk** — validate assumptions that could invalidate everything
2. **Highest learning** — get feedback that informs remaining slices
3. **Highest value** — deliver what matters most if project is cut short

Never order by "easiest first" unless easy also validates assumptions.
