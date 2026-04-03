# Question Dependency Tiers

Structure for ordering questions so later answers can depend on earlier ones.

## Table of Contents
- [The Principle](#the-principle)
- [Generic Tier Structure](#generic-tier-structure)
- [Domain Variations](#domain-variations)
- [Mapping Your Own Tiers](#mapping-your-own-tiers)

---

## The Principle

Some questions can't be answered without prior answers:

- "What file formats?" depends on "Who's the user?"
- "What's the abuse model?" depends on "What's the privacy model?"
- "What's MVP?" depends on "Who's the user and what motivates them?"

**Rule:** If answering Question B requires knowing Answer A, then Question A must come first.

---

## Generic Tier Structure

Most products follow this dependency order:

### Tier 0: Foundation
Everything else depends on these. Ask first.

- **Identity**: What IS this product? Who is it for?
- **Scale**: How big? How many users/items/operations?
- **Privacy/Access**: Public or private? Who can see what?

### Tier 1: User Model
Depends on Tier 0 (can't design users without knowing what product is).

- **User identity**: Accounts? Anonymous? Sessions?
- **Discovery**: How do users find/access the product?
- **Permissions**: What can different users do?

### Tier 2: Incentives
Depends on Tier 0+1 (can't design incentives without knowing users).

- **Motivation**: Why would users engage?
- **Feedback**: What do users see/feel during use?
- **Rewards**: What do users get for participating?

### Tier 3: Lifecycle
Depends on Tier 0+1+2 (can't design lifecycle without knowing user journey).

- **Creation**: How are things made?
- **Modification**: Can things change? When? By whom?
- **Completion/Deletion**: How do things end?

### Tier 4: Edge Cases
Depends on all above (edge cases are deviations from the happy path).

- **Errors**: What happens when things fail?
- **Abuse**: What happens when users misbehave?
- **Recovery**: How do we get back to good state?

### Tier 5: Success Criteria
Meta-tier. Requires understanding full picture.

- **MVP scope**: What's the minimum viable product?
- **Metrics**: How do we measure success?
- **Done criteria**: When is the product "finished"?

---

## Domain Variations

### Consumer App
```
Tier 0: Target audience, market positioning
Tier 1: Onboarding, account model
Tier 2: Engagement loops, notifications
Tier 3: Content lifecycle, user-generated content
Tier 4: Moderation, safety
Tier 5: Growth metrics, retention
```

### B2B Tool
```
Tier 0: Target company size, use case
Tier 1: Team structure, roles, permissions
Tier 2: Integration points, workflow fit
Tier 3: Data lifecycle, compliance
Tier 4: Support model, SLA
Tier 5: Revenue metrics, churn
```

### Internal Tool
```
Tier 0: Who uses it, what problem it solves
Tier 1: Access control, authentication
Tier 2: Training needs, documentation
Tier 3: Maintenance, updates
Tier 4: Fallback if tool fails
Tier 5: Adoption metrics, time saved
```

### API/Platform
```
Tier 0: Target developers, use cases
Tier 1: Authentication, rate limits
Tier 2: Developer experience, documentation
Tier 3: Versioning, deprecation
Tier 4: Error handling, debugging support
Tier 5: Adoption, integration count
```

---

## Mapping Your Own Tiers

1. **List all questions** you need answered
2. **For each question**, ask: "What do I need to know first?"
3. **Draw dependency arrows** from prerequisite to dependent
4. **Group into tiers** where no question in a tier depends on another in same tier
5. **Validate** by checking: "Can I answer Tier N without knowing Tier N-1?"

**Visual technique:**
```
Q1 ──→ Q4
Q2 ──→ Q4
Q3 ──→ Q5
Q4 ──→ Q5
Q5 ──→ Q6

Tiers:
0: Q1, Q2, Q3 (no dependencies)
1: Q4 (depends on Q1, Q2)
2: Q5 (depends on Q3, Q4)
3: Q6 (depends on Q5)
```
