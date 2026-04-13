---
name: improve-architecture
description: >
  Explores codebases for architectural friction, discovers module-deepening opportunities,
  and proposes refactors through multi-design exploration. Triggers: "improve architecture",
  "find refactoring opportunities", "deepen shallow modules", "reduce coupling",
  "simplify module structure", mentions of architectural friction or module boundaries.
  Writes refactor RFC as a report file.
---

# Improve Architecture

Explore a codebase to surface architectural friction, discover module-deepening opportunities,
and propose concrete refactors via multi-design exploration. Write results as an RFC document to disk.

## Core Philosophy: Deep Modules

A **deep module** (John Ousterhout, "A Philosophy of Software Design") hides a large
implementation behind a small interface. Deep modules are:

- **More testable**: test at the boundary, not inside
- **More navigable**: fewer entry points to understand
- **More maintainable**: internals change without rippling through callers

The opposite -- shallow modules where the interface is nearly as complex as the
implementation -- creates integration risk in the seams and forces tests to mirror
implementation rather than behavior.

## The Protocol

### Phase 1: Explore for Friction

Explore as a developer would, noting where understanding breaks down:

- **Bouncing**: understanding one concept requires reading many small files
- **Shallow interfaces**: a module's public API is nearly as complex as its internals
- **Testability extraction**: pure functions extracted solely for testability while real bugs hide in integration
- **Tight coupling**: modules share types, call each other extensively, or co-own concepts
- **Test gaps**: modules untested or requiring elaborate mocking

Difficulty navigating the code reveals the same friction every future developer
(and AI agent) will face.

### Phase 2: Present Candidates

Present a numbered list of deepening opportunities. For each candidate:

| Field | Content |
|-------|---------|
| **Cluster** | Which modules and concepts are involved |
| **Coupling signal** | Shared types, call patterns, co-ownership of a concept |
| **Dependency category** | Classify using the flowchart below |
| **Test impact** | Which existing tests would boundary tests replace |

Describe modules by responsibility, not file paths.

Ask the user: "Which of these candidates would you like to explore?"

## Dependency Categories

Classify each dependency:

```
Does the dependency involve I/O?
  NO  -> In-Process: merge modules, test directly with unit tests
  YES -> Is there a local stand-in?
    YES -> Local-Substitutable: test with stand-in at module boundary
    NO  -> Do we own the remote service?
      YES -> Ports & Adapters: define port (domain ops, not transport), inject adapter
      NO  -> True External: mock at boundary only, contract test for real client
```

Boundary rule: never mock deeper than the immediate boundary.

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

Launch 3 or more parallel agents, each producing a radically different interface
for the deepened module. Give each agent a technical brief (file paths, coupling
details, dependency category, what complexity gets hidden) AND a distinct
design constraint:

| Agent | Constraint |
|-------|-----------|
| 1 | Minimize the interface -- aim for 1-3 entry points maximum |
| 2 | Maximize flexibility -- support many use cases and extension points |
| 3 | Optimize for the most common caller -- make the default case trivial |
| 4 | Design around ports and adapters for cross-boundary dependencies (if applicable) |

If you have access to the agentic-delegation skill, apply its Parallel Fan-Out execution
pattern and Model Ladder for agent tier selection. Otherwise, launch agents with
the cheapest available model, each with its own design constraint.

Each agent outputs:
1. Interface signature (types, methods, parameters)
2. Usage example showing how callers consume it
3. What complexity gets hidden internally
4. Dependency strategy (which category, how deps are handled)
5. Trade-offs and where this design breaks down

### Phase 5: Compare and Recommend

Present designs sequentially, then compare in prose:

- Where do designs agree? (Likely correct boundaries)
- Where do they diverge? (Genuine design tension)
- Which requires fewest lines for the common case?
- Which survives future requirement changes best?

Provide an opinionated recommendation: which design is strongest and why.
If elements from different designs combine well, propose a hybrid.
The user wants a strong read, not a menu.

### Phase 6: Create Refactor RFC

After the user selects a design (or accepts the recommendation), write an
RFC document to a file in the project's docs directory (e.g., `docs/rfcs/`, `rfcs/`, or the project's convention) with this structure.
Write the file directly and share the file path.

```
## Problem

Describe the architectural friction:
- Which modules are shallow and tightly coupled
- What integration risk exists in the seams between them
- Why this makes the codebase harder to navigate, test, and maintain

Describe modules by responsibility and behavior so the issue survives reorganization.

## Proposed Interface

The selected interface design:
- Interface signature (types, methods, parameters)
- Usage example showing how callers consume the new interface
- What complexity the module hides internally

## Dependency Strategy

Which category applies (in-process, local-substitutable, ports & adapters,
true external) and how dependencies are handled.

## Testing Strategy

- **New boundary tests**: behaviors to verify at the interface
- **Old tests to delete**: shallow module tests that become redundant
- **Test environment needs**: local stand-ins or adapters required

## Implementation Recommendations

Durable guidance NOT coupled to current file layout:
- What the module should own (responsibilities)
- What it should hide (implementation details)
- What it should expose (the interface contract)
- How callers should migrate to the new interface
- Suggested implementation order (which boundaries to draw first)
```

## Testing Strategy: Replace, Don't Layer

When deepening modules:

- Boundary tests supersede old unit tests on shallow modules -- delete the old tests
- Write new tests at the deepened module's interface boundary
- Tests assert on observable outcomes through the public interface, not internal state
- Tests survive internal refactors -- they describe behavior, not implementation
