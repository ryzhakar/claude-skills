# Core Points: improve-architecture

## Iteration 1

**Point**: Deep modules with small interfaces hiding large implementations are superior to shallow modules where interface complexity matches implementation complexity because deep modules concentrate testing at boundaries rather than forcing tests to mirror internal structure.

**Evidence**:
- SKILL.md lines 17-28: "A deep module (John Ousterhout, 'A Philosophy of Software Design') has a small interface hiding a large implementation. Deep modules are: More testable: test at the boundary, not inside [...] The opposite -- shallow modules where the interface is nearly as complex as the implementation -- creates integration risk in the seams between modules and forces tests to mirror internal structure."
- SKILL.md lines 121-128: "When deepening modules, follow this testing principle: Old unit tests on shallow modules are waste once boundary tests exist -- delete them [...] Tests must survive internal refactors -- they describe behavior, not implementation"
- rfc-template.md lines 36-39: "New boundary tests to write: behaviors to verify at the interface / Old tests to delete: shallow module tests that become redundant"

## Iteration 2

**Point**: Architectural friction is discovered through organic navigation of the codebase rather than rigid heuristics, with difficulty understanding the code serving as the primary signal that reveals problems every future developer will face.

**Evidence**:
- SKILL.md lines 34-46: "Navigate the codebase organically. Do NOT follow rigid heuristics -- explore as a developer would and note where understanding breaks down: Bouncing: Understanding one concept requires reading many small files [...] The friction experienced during exploration IS the signal. Difficulty navigating the code reveals the same friction every future developer (and AI agent) will face."
- SKILL.md lines 3-8: "This skill should be used when the user asks to 'improve the architecture', 'find refactoring opportunities', 'deepen shallow modules', 'consolidate tightly-coupled code' [...] or mentions architectural friction, shallow modules, or module boundaries"
- rfc-template.md lines 8-15: "Describe the architectural friction: Which modules are shallow and tightly coupled / What integration risk exists in the seams between them / Why this makes the codebase harder to navigate, test, and maintain"

## Iteration 3

**Point**: Dependencies must be classified into four categories (in-process, local-substitutable, ports-and-adapters, true external) because each category requires a different testing strategy and determines whether to merge modules, use local stand-ins, define ports, or mock at boundaries.

**Evidence**:
- SKILL.md lines 56-57: "Dependency category: Classify using the 4-category framework in @references/dependency-categories.md"
- dependency-categories.md lines 1-5: "When assessing a module for deepening, classify each of its dependencies into one of four categories. The category determines the testing strategy and refactoring approach."
- dependency-categories.md lines 86-96: Full selection flowchart showing decision tree from "Does the dependency involve I/O?" through all four categories with distinct strategies for each

## Iteration 4

**Point**: Multiple parallel design agents must explore radically different interfaces with distinct constraints (minimize interface, maximize flexibility, optimize common case, ports-and-adapters) to reveal genuine design tensions through disagreement and likely-correct boundaries through convergence.

**Evidence**:
- SKILL.md lines 76-88: "Launch 3 or more parallel agents, each producing a radically different interface for the deepened module [...] [table showing 4 agents with distinct constraints: Minimize the interface, Maximize flexibility, Optimize for the most common caller, Design around ports and adapters]"
- SKILL.md lines 103-111: "Present designs sequentially, then compare them in prose: Where do designs agree? (Likely correct boundaries) / Where do they diverge? (Genuine design tension) [...] Provide an opinionated recommendation: which design is strongest and why"
- SKILL.md lines 62-72: "After the user selects a candidate, write a user-facing explanation BEFORE launching design agents: Constraints any new interface must satisfy [...] Present this to the user, then immediately proceed to Phase 4. The user reads and thinks about the problem while design agents work in parallel."

## Iteration 5

**Point**: The refactor RFC must be published directly as a GitHub issue using durable, location-independent descriptions of responsibilities and behaviors rather than specific file paths so the documentation survives code reorganization.

**Evidence**:
- SKILL.md lines 115-118: "After the user selects a design (or accepts the recommendation), create a GitHub issue using `gh issue create` with the template in @references/rfc-template.md. Do NOT ask the user to review before creating -- publish directly and share the URL."
- rfc-template.md lines 13-15: "Do NOT reference specific file paths or line numbers. Describe modules by responsibility and behavior so the issue survives reorganization."
- rfc-template.md lines 43-49: "Durable guidance NOT coupled to current file layout: What the module should own (responsibilities) / What it should hide (implementation details) / What it should expose (the interface contract) / How callers should migrate to the new interface / Suggested implementation order"

## Rank Summary

1. **Deep module philosophy** — The foundational principle that drives all other decisions in the skill; everything else exists to achieve deep modules with small interfaces
2. **Dependency classification system** — The 4-category framework is the technical backbone determining testing strategy and refactoring approach for every module
3. **Multi-design parallel exploration** — The distinctive methodology that differentiates this skill from simple refactoring; reveals design tensions through structured disagreement
4. **Friction-driven discovery** — The diagnostic method that identifies what to refactor; organic navigation as the detection mechanism
5. **Durable RFC publication** — Important execution detail ensuring persistence of decisions but less conceptually central than the principles above
