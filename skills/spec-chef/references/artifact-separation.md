# Artifact Separation Guide

What goes where. Keep concerns separated for maintainability and clarity.

## Table of Contents
- [The Four Artifacts](#the-four-artifacts)
- [Decision Matrix](#decision-matrix)
- [Templates](#templates)
- [Common Mistakes](#common-mistakes)

---

## The Four Artifacts

| Artifact | Question It Answers | Audience |
|----------|---------------------|----------|
| **Product Spec** | WHAT are we building? | Product, Engineering |
| **Personas** | WHO are we building for? | Product, Design |
| **User Stories** | WHAT VALUE does it deliver? | Engineering, QA |
| **Architecture** | HOW do we build it? | Engineering |

---

## Decision Matrix

When you have information to record, use this matrix:

| Information Type | Product Spec | Personas | User Stories | Architecture |
|------------------|:------------:|:--------:|:------------:|:------------:|
| User identity model | ✓ | | | |
| User motivations | | ✓ | | |
| Feature behavior | ✓ | | | |
| Acceptance criteria | | | ✓ | |
| Technology choices | | | | ✓ |
| Scale constraints | ✓ | | | ✓ |
| Privacy model | ✓ | | | |
| Jobs-to-be-done | | ✓ | | |
| Error handling UX | ✓ | | ✓ | |
| Error handling impl | | | | ✓ |
| MVP scope | ✓ | | | |
| Story dependencies | | | ✓ | |
| Data schemas | | | | ✓ |
| Success metrics | ✓ | | | |

---

## Templates

### Product Spec Template

```markdown
# Product Spec: [Name]

## Product Identity
What this is. What this is NOT.

## User Model
Identity, access, privacy decisions.

## Core Behaviors
Key feature decisions with rationale.

## Constraints
Scale, format, timing limits.

## Lifecycle
Creation, modification, completion, deletion.

## Edge Cases
Error handling, abuse, recovery.

## Success Criteria
MVP definition, metrics.

## Deferred
Explicitly out of scope for now.
```

### Personas Template

```markdown
# Personas: [Product]

## [Primary Persona Name]
**Who:** Demographics, context
**Goal:** What they want to achieve
**Constraints:** Time, skill, attention
**Success state:** What "done" looks like for them

## [Secondary Persona Name]
...

## Jobs to Be Done
1. [Persona]: "[Job statement]"
2. ...

## Anti-Personas (NOT building for)
- [Type]: Why not
```

### User Stories Template

```markdown
# User Stories: [Product]

## Epic 1: [Name]
[Brief description of value area]

### Story 1.1: [Name]
**Outcome:** What changes when this is done

\`\`\`
Given [precondition]
When [action]
Then [observable result]
\`\`\`

**AC (Hypotheses):**
- [Testable statement about value delivery]
- [Another testable statement]

## Story Dependencies
[Dependency diagram or list]

## Deferred Stories
- [Story]: [Reason for deferral]
```

### Architecture Template

```markdown
# Architecture: [Product]

## Overview
[Diagram or description of major components]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Area] | [Choice] | [Why] |

## Data Model
[Schemas, relationships]

## Integration Points
[External systems, APIs]

## Constraints
[Technical limits, dependencies]
```

---

## Common Mistakes

### Mixing WHAT and HOW

**Wrong:**
```
Product Spec: "Users authenticate via JWT tokens stored in httpOnly cookies"
```

**Right:**
```
Product Spec: "Sessions persist across browser restarts for logged-in users"
Architecture: "Implement via JWT in httpOnly cookies, 7-day expiry"
```

### Mixing WHO and WHAT

**Wrong:**
```
Product Spec: "Marcus, a busy commuter, needs fast load times"
```

**Right:**
```
Personas: "Marcus: mobile user with ~10 minutes, impatient"
Product Spec: "Pages load in <2 seconds on 3G"
```

### Stories Without Value

**Wrong:**
```
Story: "Build the database schema"
```

**Right:**
```
Architecture: "Database schema: [details]"
Story: "User can save progress and resume later" (value this enables)
```

### Duplicating Across Artifacts

**Wrong:**
```
Product Spec: "50-200 photos per campaign"
Architecture: "50-200 photos per campaign"
User Stories: "50-200 photos per campaign"
```

**Right:**
```
Product Spec: "50-200 photos per campaign"
(Others reference Product Spec, don't duplicate)
```

---

## Maintenance Rule

When a decision changes:

1. **Update the source artifact** (usually Product Spec)
2. **Check downstream artifacts** for consistency
3. **Don't duplicate** the decision in multiple places

Single source of truth. References, not copies.
