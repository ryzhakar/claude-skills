# User Story Anti-Patterns

Form addiction symptoms and their cures.

## Table of Contents
- [Template Worship](#template-worship)
- [The Technical Story](#the-technical-story)
- [The Epic in Disguise](#the-epic-in-disguise)
- [The Componentized Story](#the-componentized-story)
- [The Orphan Card](#the-orphan-card)
- [The Implementation Leak](#the-implementation-leak)
- [The Moving Target](#the-moving-target)
- [The Checkbox AC](#the-checkbox-ac)

---

## Template Worship

**Symptom:** Story follows "As a... I want... so that..." perfectly but team still asks "what does this actually mean?"

**Example:**
```
As a user, I want better performance so that the system is faster.
```

**Diagnosis:** Template compliance without substance. The form is satisfied; the function is absent.

**Cure:** Ask "What observable behavior changes?" Rewrite with specificity:
```
As a shopper, I want search results in under 2 seconds so I don't abandon my search.
```

---

## The Technical Story

**Symptom:** Story describes system behavior, not user value. Often starts with "As a developer..." or "As the system..."

**Examples:**
```
As a developer, I want to refactor the database layer so the code is cleaner.
As the system, I want to cache API responses so performance improves.
```

**Diagnosis:** Work that serves the system, not the user. May be necessary, but shouldn't masquerade as a user story.

**Cure:** Either:
1. Find the user value: "As a user, I want pages to load instantly so I stay engaged" (caching is implementation)
2. Acknowledge it's technical debt/enabler and track separately

---

## The Epic in Disguise

**Symptom:** Story seems reasonable but takes multiple sprints. Team keeps discovering more work.

**Example:**
```
As a user, I want to manage my account settings so I can control my experience.
```

**Diagnosis:** Scope is unbounded. "Manage settings" could mean 50 different things.

**Cure:** Decompose by specific setting categories:
```
1. As a user, I want to change my password
2. As a user, I want to update my email preferences
3. As a user, I want to configure notification frequency
```

Each is completable. Each delivers incremental value.

---

## The Componentized Story

**Symptom:** Stories map to technical layers instead of user value. Sequential dependencies block parallel work.

**Example:**
```
Sprint 1: Build user profile database schema
Sprint 2: Build user profile API
Sprint 3: Build user profile UI
```

**Diagnosis:** Sliced by architecture, not by value. No deployable value until Sprint 3 completes.

**Cure:** Slice thin vertically through all layers:
```
1. User can view their name (DB + API + UI, minimal)
2. User can edit their name (adds mutation)
3. User can upload avatar (adds file handling)
```

Each slice touches all layers but delivers complete value.

---

## The Orphan Card

**Symptom:** Card exists but no one discusses it. Goes straight from backlog to sprint without refinement.

**Diagnosis:** Missing the Conversation from the 3 C's. The card is a placeholder; without discussion, it's incomplete documentation.

**Cure:** Require refinement session before sprint commitment. Story isn't ready until:
- Team can estimate without wild variance
- Edge cases are identified
- AC are agreed upon
- Dependencies are known

---

## The Implementation Leak

**Symptom:** Acceptance criteria describe HOW, not WHAT.

**Example:**
```
AC:
- Click submit button
- System calls POST /api/users
- Database inserts row into users table
- Success toast appears
```

**Diagnosis:** Implementation decisions embedded in acceptance. Constrains solutions, doesn't describe value.

**Cure:** Describe observable outcomes:
```
AC:
- Given valid form data, when submitted, user sees confirmation
- Given invalid email, when submitted, user sees specific error
- User appears in admin list after successful registration
```

Implementation is team's decision. AC verify value was delivered.

---

## The Moving Target

**Symptom:** Story changes during sprint. Scope creeps. "One more thing" becomes three more things.

**Diagnosis:** Insufficient conversation before commitment, OR product owner using stories as living requirements.

**Cure:**
1. Stories are frozen once committed to sprint
2. New requirements become new stories (prioritized for future sprint)
3. If change is critical, remove story from sprint, refine, re-commit

Stories are commitments. Moving targets destroy predictability.

---

## The Checkbox AC

**Symptom:** AC list technical checkboxes that don't prove value delivery.

**Example:**
```
AC:
- [ ] Button exists
- [ ] Button is blue
- [ ] Button has text "Submit"
- [ ] Button calls handler on click
```

**Diagnosis:** Testing existence, not function. All boxes could be checked while feature is broken for users.

**Cure:** AC should be user-verifiable:
```
AC:
- User can submit form and receive confirmation within 3 seconds
- User sees clear error message if submission fails
- User's data appears in their account after successful submission
```

If a QA engineer can verify it without understanding the user, it's too technical.
