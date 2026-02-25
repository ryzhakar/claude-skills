---
name: spec-chef
description: >
  Extract implicit product decisions from stakeholders into durable artifacts.
  Triggers: analyzing incomplete specs, stakeholder interviews, finding documentation gaps,
  "what questions should I ask", extracting product requirements, defining MVP scope.
  Use when existing documentation has gaps, implicit assumptions, or undefined behaviors
  that require stakeholder input to resolve. Produces separated artifacts (spec, personas, stories).
---

# Spec Chef

Transform implicit stakeholder knowledge into explicit artifacts through systematic gap detection and constrained questioning.

## Why This Works

Stakeholders know more than they've written. Documentation has gaps because writers assume context readers lack. This workflow:

1. **Detects gaps** in existing docs
2. **Orders questions** by dependency (foundational → detailed)
3. **Constrains choices** (2-4 options, not open-ended)
4. **Codifies immediately** (artifacts before context decays)
5. **Separates concerns** (WHAT/WHO/VALUE/HOW never mixed)

## The Protocol

### Phase 1: Analyze

Read existing documentation. Identify gaps using these categories:

| Gap Type | Signal |
|----------|--------|
| Missing personas | "users" without specifics |
| Undefined behaviors | "handles errors" without how |
| Implicit assumptions | Decisions without rationale |
| Missing edge cases | Happy path only |
| No success criteria | No way to know "done" |
| Unclear scope | No explicit "NOT building" |

See `references/gap-heuristics.md` for detailed detection patterns.

### Phase 2: Map Dependencies

Order questions into tiers. Later tiers depend on earlier answers.

```
Tier 0: Foundation (identity, scale, privacy)
   ↓
Tier 1: User Model (accounts, sessions, discovery)
   ↓
Tier 2: Incentives (motivation, feedback, rewards)
   ↓
Tier 3: Lifecycle (create, modify, complete, delete)
   ↓
Tier 4: Edge Cases (errors, abuse, recovery)
   ↓
Tier 5: Success (MVP scope, metrics)
```

See `references/dependency-tiers.md` for tier patterns by domain.

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
header: "Scale" (≤12 chars, categorizes)
question: "What scale should X support?" (specific, ends with ?)
options:
  - label: "Small (10-50)"
    description: "Use case A, trade-off B"
  - label: "Medium (50-200)"
    description: "Use case C, trade-off D"
```

Ask tier-by-tier. Capture answers before moving to next tier.

### Phase 4: Codify

Write artifacts IMMEDIATELY after each tier (or at most after all tiers complete). Don't wait—context decays.

**Artifact separation:**

| Artifact | Contains | Does NOT Contain |
|----------|----------|------------------|
| Product Spec | Decisions, constraints, behaviors | Technical architecture |
| Personas | Users, jobs-to-be-done, anti-personas | Implementation details |
| User Stories | Value units, AC as hypotheses | How to build |
| Architecture | Technical decisions, patterns | Business logic |

See `references/artifact-separation.md` for templates.

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
- `header` string (≤12 chars)

Each option needs `label` and `description`.
