---
name: improve-architecture
description: >
  This skill should be used when the user asks to "improve the architecture",
  "find refactoring opportunities", "deepen shallow modules", "consolidate tightly-coupled code",
  "make this codebase more testable", "reduce coupling", "simplify this module structure",
  or mentions architectural friction, shallow modules, or module boundaries. Produces
  multi-design exploration with dependency-aware testing strategy and a refactor RFC as GitHub issue.
---

# Improve Architecture

Explore a codebase to surface architectural friction, discover module-deepening opportunities,
and propose refactors through structured multi-design exploration. Publish results as
a GitHub issue RFC.

## Core Philosophy: Deep Modules

A **deep module** (John Ousterhout, "A Philosophy of Software Design") has a small interface
hiding a large implementation. Deep modules are:

- **More testable**: test at the boundary, not inside
- **More navigable**: fewer entry points to understand
- **More maintainable**: internals change without rippling through callers

The opposite -- shallow modules where the interface is nearly as complex as the
implementation -- creates integration risk in the seams between modules and forces
tests to mirror internal structure.

## The Protocol

### Phase 1: Explore for Friction

Navigate the codebase organically. Do NOT follow rigid heuristics -- explore as a
developer would and note where understanding breaks down:

- **Bouncing**: Understanding one concept requires reading many small files
- **Shallow interfaces**: A module's public API is nearly as complex as its internals
- **Testability extraction**: Pure functions extracted solely for testability, but
  real bugs hide in caller patterns and integration points
- **Tight coupling**: Modules share types, call each other extensively, or co-own
  a concept without clear ownership boundaries
- **Test gaps**: Modules that are untested or require elaborate mocking to test

The friction experienced during exploration IS the signal. Difficulty navigating
the code reveals the same friction every future developer (and AI agent) will face.

### Phase 2: Present Candidates

Present a numbered list of deepening opportunities. For each candidate:

| Field | Content |
|-------|---------|
| **Cluster** | Which modules and concepts are involved |
| **Coupling signal** | Shared types, call patterns, co-ownership of a concept |
| **Dependency category** | Classify using the 4-category framework in @references/dependency-categories.md |
| **Test impact** | Which existing tests would boundary tests replace |

Do NOT propose interfaces yet. Ask the user: "Which of these candidates
would you like to explore?"

### Phase 3: Frame the Problem Space

After the user selects a candidate, write a user-facing explanation BEFORE
launching design agents:

- Constraints any new interface must satisfy
- Dependencies the module would need to rely on
- A rough illustrative code sketch making the constraints concrete
  (this is NOT a proposal -- just grounding for the constraints)

Present this to the user, then immediately proceed to Phase 4. The user reads
and thinks about the problem while design agents work in parallel.

### Phase 4: Multi-Design Exploration

Launch 3 or more parallel agents, each producing a **radically different** interface
for the deepened module. Give each agent a technical brief (file paths, coupling
details, dependency category, what complexity gets hidden) AND a distinct
design constraint:

| Agent | Constraint |
|-------|-----------|
| 1 | Minimize the interface -- aim for 1-3 entry points maximum |
| 2 | Maximize flexibility -- support many use cases and extension points |
| 3 | Optimize for the most common caller -- make the default case trivial |
| 4 | Design around ports and adapters for cross-boundary dependencies (if applicable) |

If the agentic-delegation skill is available, apply its Parallel Fan-Out execution
pattern and Model Ladder for agent tier selection. Otherwise, launch agents with
the cheapest available model, each working independently with its own design constraint.

Each agent outputs:
1. Interface signature (types, methods, parameters)
2. Usage example showing how callers consume it
3. What complexity gets hidden internally
4. Dependency strategy (how deps are handled -- see @references/dependency-categories.md)
5. Trade-offs and where this design breaks down

### Phase 5: Compare and Recommend

Present designs sequentially, then compare them in prose:

- Where do designs agree? (Likely correct boundaries)
- Where do they diverge? (Genuine design tension)
- Which handles the common case most naturally?
- Which survives future requirement changes best?

Provide an opinionated recommendation: which design is strongest and why.
If elements from different designs combine well, propose a hybrid.
The user wants a strong read, not a menu.

### Phase 6: Create Refactor RFC

After the user selects a design (or accepts the recommendation), create a
GitHub issue using `gh issue create` with the template in @references/rfc-template.md.
Do NOT ask the user to review before creating -- publish directly and share the URL.

## Testing Strategy: Replace, Don't Layer

When deepening modules, follow this testing principle:

- Old unit tests on shallow modules are waste once boundary tests exist -- delete them
- Write new tests at the deepened module's interface boundary
- Tests assert on observable outcomes through the public interface, not internal state
- Tests must survive internal refactors -- they describe behavior, not implementation

## Reference Files

- @references/dependency-categories.md -- 4-category framework for classifying
  dependencies and selecting testing strategy for each category
- @references/rfc-template.md -- GitHub issue template for the refactor RFC

---

*Originally based on improve-codebase-architecture from https://github.com/mattpocock/skills, MIT licensed. Adapted and enhanced for this plugin.*
