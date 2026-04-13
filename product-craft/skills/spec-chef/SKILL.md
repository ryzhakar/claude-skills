---
name: spec-chef
description: >
  Extracts implicit product decisions from stakeholders into durable artifacts through
  systematic gap detection and constrained questioning. Triggers: analyzing incomplete specs,
  stakeholder interviews, finding documentation gaps, "what questions should I ask",
  extracting product requirements, defining MVP scope. Produces separated artifacts
  (spec, personas, stories).
---

# Spec Chef

Transform implicit stakeholder knowledge into explicit artifacts through systematic gap detection and constrained questioning.

## Why This Works

Stakeholders know more than they've written. Documentation has gaps because writers assume context their readers don't have.

1. **Detects gaps** in existing docs
2. **Orders questions** by dependency
3. **Constrains choices** to 2-4 options
4. **Codifies immediately** before stakeholders forget
5. **Separates concerns** across distinct artifacts

## The Protocol

### Phase 1: Analyze

**Terminology check**: When working with multi-author documentation or inconsistent domain vocabulary, extract domain terminology first:

1. Scan for domain nouns, verbs, and concepts
2. Flag ambiguities:

| Problem | Example | Risk |
|---------|---------|------|
| Same word, different concepts | "account" = Customer AND User | Specs describe wrong entity |
| Different words, same concept | "purchase", "order", "transaction" | Inconsistent specs, duplicated logic |
| Vague or overloaded terms | "process the request" | Undefined behaviors slip through |

3. Select ONE canonical term per concept; list aliases to avoid
4. State relationships with explicit cardinality
5. Write `UBIQUITOUS_LANGUAGE.md` and index it in project documentation

Skip when domain vocabulary is already consistent.

**Gap detection**: Read existing documentation. Identify gaps using these categories:

| Gap Type | Signal | What's Missing | Questions to Surface |
|----------|--------|----------------|---------------------|
| Missing personas | "users" without specifics | WHO specifically, their constraints, what they know | Who is the PRIMARY user? What's their time budget? Who is explicitly NOT a user? |
| Undefined behaviors | "handles errors gracefully" | HOW specifically, what the user sees | What exactly appears on screen? Can it be undone? What state is preserved? |
| Implicit assumptions | Decisions without rationale | WHY this choice, what alternatives were rejected | What constraints drove this? Is this revisitable or locked? |
| Missing edge cases | Happy path only | What happens when things go wrong | Invalid input? Timeout? User abandons mid-flow? Abuse/spam? |
| No success criteria | No way to know "done" | How do we know it worked | What's MVP vs nice-to-have? What would make this a failure? |
| Unclear scope | No explicit "NOT building" | What are we NOT building | What's explicitly out of scope? What's deferred to later? |

Detection technique -- for each documentation section ask:
1. Could two engineers interpret this differently? (ambiguity gap)
2. Does this assume knowledge not stated? (assumption gap)
3. What questions would a new team member ask? (context gap)
4. What could go wrong that isn't mentioned? (edge case gap)
5. How would we demo this? (behavior gap)
6. Who decides if this is done? (success gap)

### Phase 2: Map Dependencies

Order questions into tiers. Later tiers depend on earlier answers.
Complete each tier before starting the next.

```
Tier 0: Foundation (identity, scale, privacy)
   |
Tier 1: User Model (accounts, sessions, discovery)
   |
Tier 2: Incentives (motivation, feedback, rewards)
   |
Tier 3: Lifecycle (create, modify, complete, delete)
   |
Tier 4: Edge Cases (errors, abuse, recovery)
   |
Tier 5: Success (MVP scope, metrics)
```

**Domain-specific tier content**:

| Domain | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|--------|--------|--------|--------|--------|--------|--------|
| Consumer | audience, positioning | onboarding, accounts | engagement, notifications | content lifecycle | moderation, safety | growth, retention |
| B2B | company size, use case | teams, roles, permissions | integrations, workflow | data lifecycle, compliance | support, SLA | revenue, churn |
| Internal | who, what problem | access, auth | training, docs | maintenance, updates | fallback | adoption, time saved |
| API | target devs, use cases | auth, rate limits | DX, documentation | versioning, deprecation | error handling, debugging | adoption, integration count |

### Phase 3: Extract

Use `AskUserQuestion` tool with constrained choices:

**Rules:**
- 2-4 options per question (forces concrete decisions)
- Include trade-off in each option's description
- One decision per question (don't bundle)
- 1-4 questions per round (don't overwhelm)
- "Other" is always available (stakeholder can escape)

**Question anatomy:**
```
header: "Scale" (<=12 chars, categorizes)
question: "What scale should X support?" (specific, ends with ?)
options:
  - label: "Small (10-50)"
    description: "Use case A, trade-off B"
  - label: "Medium (50-200)"
    description: "Use case C, trade-off D"
```

Ask tier-by-tier. Capture answers before advancing to the next tier.

### Phase 4: Codify

Write artifacts IMMEDIATELY after each tier (or at most after all tiers complete). Don't wait -- stakeholders forget details and rationales fade.

**Artifact separation:**

| Artifact | Contains | Does NOT Contain |
|----------|----------|------------------|
| Product Spec | Decisions, constraints, behaviors | Technical architecture |
| Personas | Users, jobs-to-be-done, anti-personas | Implementation details |
| User Stories | Value units, AC as hypotheses | How to build |
| Architecture | Technical decisions, patterns | Business logic |

**When uncertain where information belongs, use this decision matrix:**

| Information Type | Spec | Personas | Stories | Architecture |
|------------------|:----:|:--------:|:-------:|:------------:|
| User identity model | X | | | |
| User motivations | | X | | |
| Feature behavior | X | | | |
| Acceptance criteria | | | X | |
| Technology choices | | | | X |
| Scale constraints | X | | | X |
| Privacy model | X | | | |
| Jobs-to-be-done | | X | | |
| Error handling UX | X | | X | |
| Error handling impl | | | | X |
| MVP scope | X | | | |
| Story dependencies | | | X | |
| Data schemas | | | | X |
| Success metrics | X | | | |

**Separation rules:**
- Don't mix WHAT and HOW (behavior in Spec, implementation in Architecture)
- Don't mix WHO and WHAT (persona details in Personas, constraints in Spec)
- Don't write stories without user value (technical work goes in Architecture)
- Don't duplicate decisions across artifacts (single source, references not copies)

When a decision changes, update the source artifact. Single source of truth.

### Phase 5: Index

Update project documentation (CLAUDE.md or equivalent) to reference new artifacts. Future sessions must find them.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Ask open-ended questions | Offer 2-4 concrete options |
| Bundle multiple decisions | One question per decision |
| Wait to codify | Write artifacts immediately |
| Mix WHAT/WHO/HOW | Separate into distinct files |
| Assume tier order | Validate dependencies for domain |

## Tool Requirements

This skill requires `AskUserQuestion` tool with:
- `questions` array (1-4 questions)
- `options` array per question (2-4 options)
- `multiSelect` boolean (usually false)
- `header` string (<=12 chars)

Each option needs `label` and `description`.
