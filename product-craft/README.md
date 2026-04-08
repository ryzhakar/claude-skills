# product-craft

Product definition and architecture skills: extract specs from stakeholders, write user stories, triage bugs, improve codebase architecture, and establish ubiquitous language.

`product` `spec` `user-stories` `agile` `triage` `architecture` `refactoring` 
## Skills

### [improve-architecture](skills/improve-architecture/SKILL.md)

This skill should be used when the user asks to "improve the architecture", "find refactoring opportunities", "deepen shallow modules", "consolidate tightly-coupled code", "make this codebase more testable", "reduce coupling", "simplify this module structure", or mentions architectural friction, shallow modules, or module boundaries. Produces multi-design exploration with dependency-aware testing strategy and a refactor RFC as GitHub issue.


**References:** [`dependency-categories.md`](skills/improve-architecture/references/dependency-categories.md) · [`rfc-template.md`](skills/improve-architecture/references/rfc-template.md)
---

### [spec-chef](skills/spec-chef/SKILL.md)

Extract implicit product decisions from stakeholders into durable artifacts. Triggers: analyzing incomplete specs, stakeholder interviews, finding documentation gaps, "what questions should I ask", extracting product requirements, defining MVP scope. Use when existing documentation has gaps, implicit assumptions, or undefined behaviors that require stakeholder input to resolve. Produces separated artifacts (spec, personas, stories).


**References:** [`artifact-separation.md`](skills/spec-chef/references/artifact-separation.md) · [`dependency-tiers.md`](skills/spec-chef/references/dependency-tiers.md) · [`gap-heuristics.md`](skills/spec-chef/references/gap-heuristics.md) · [`terminology-extraction.md`](skills/spec-chef/references/terminology-extraction.md)
---

### [triage-issue](skills/triage-issue/SKILL.md)

This skill should be used when the user reports a bug, says "this is broken", asks to "triage an issue", "investigate a bug", "find the root cause", "file an issue for this bug", "create a GitHub issue", or wants autonomous diagnosis of a problem in the codebase. Produces root cause analysis, TDD fix plan, and a GitHub issue.


---

### [user-story-chef](skills/user-story-chef/SKILL.md)

Write user stories as value negotiation units, not template-filling exercises. Triggers: writing user stories, acceptance criteria, backlog items, story splitting, evaluating story quality, INVEST criteria application. Use when creating or refining Agile artifacts that capture work units. Teaches function (value decomposition, falsifiable AC, feedback optimization) over form (templates).


**References:** [`anti-patterns.md`](skills/user-story-chef/references/anti-patterns.md) · [`slicing.md`](skills/user-story-chef/references/slicing.md)
---

