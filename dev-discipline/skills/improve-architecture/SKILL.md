---
name: improve-architecture
description: >
  Find architectural friction in a codebase, explore several designs for a deeper module in parallel, and write a refactor RFC recommending one.
  "improve the architecture", "find refactoring opportunities", "deepen shallow modules", "reduce coupling", "simplify the module structure",
  "this module is hard to navigate", or any mention of architectural friction or module boundaries.
---

<explore-for-friction>
Explore the codebase as a developer new to it, reading the code behind each concept the task touches; never grep for keywords alone.

Note each friction: bouncing — understanding one concept takes many small files; a shallow interface — a module whose public surface is nearly as complex as its internals; testability extraction — pure functions pulled out for tests while bugs live in the integration; tight coupling — modules sharing types or co-owning a concept; a test gap — a module untested or tested through elaborate mocks; never note a friction without the files that show it.
</explore-for-friction>

<rank-the-candidates>
Write each deepening candidate — a cluster of modules that could hide behind one smaller interface — with the modules involved, the coupling signal, and the tests a boundary test would replace; never describe a module by its file path alone.

Rank the candidates by how much complexity each hides behind how small an interface, and take the first; never ask which to explore.
</rank-the-candidates>

<classify-the-dependencies>
Classify each dependency of the candidate: in-process when it involves no I/O — merge and unit-test directly; local-substitutable when a local stand-in exists — test against the stand-in at the boundary; a port when the remote service is this project's own — define a port of domain operations and inject an adapter; external when the remote service is foreign — mock at the boundary and contract-test the real client; never mock deeper than the immediate boundary.
</classify-the-dependencies>

<frame-the-constraints>
Write the constraints any new interface has to satisfy, the dependencies the module relies on, and a rough sketch of a call site that makes the constraints concrete; never present the sketch as a proposal.
</frame-the-constraints>

<explore-designs-in-parallel>
Launch three or more agents through `agentic-delegation`, each with the same brief — the file paths, the coupling details, the dependency classes, the complexity to hide — and one distinct constraint: the smallest interface, one to three entry points; the widest flexibility, many uses and extension points; the trivial common case, the most frequent caller's call reduced to one line; a ports-and-adapters shape when a cross-boundary dependency exists; never give two agents the same constraint.

Require from each agent the interface signature, a usage example, what complexity it hides, how it handles each dependency, and where the design breaks down; never accept a design missing one of the five.
</explore-designs-in-parallel>

<compare-and-recommend>
Compare the designs on where they agree — the likely true boundaries, where they diverge — the real tensions, which needs the fewest lines for the common case, and which survives a requirement change best; never list the designs without the comparison.

Recommend one design, or a hybrid of named parts, with the reason; never present a menu.
</compare-and-recommend>

<write-the-rfc>
Write the RFC to the project's RFC directory — `docs/rfcs/`, `rfcs/`, or the directory the project already uses — with five sections: `Problem` (the friction, the integration risk in the seams, the cost to navigation, testing, and maintenance), `Proposed interface` (signature, usage example, hidden complexity), `Dependency strategy` (the class of each dependency and its handling), `Testing strategy` (new boundary tests, old tests to delete, stand-ins or adapters needed), and `Implementation recommendations` (what the module owns, hides, and exposes, how callers migrate, which boundary to draw first); never return the RFC as conversation text.

Describe modules by responsibility and behavior throughout; never describe one by its current file layout.

Print the RFC's path; never print its content.
</write-the-rfc>

<replace-the-tests>
Write new tests at the deepened module's boundary asserting observable outcomes, and delete the old tests on the shallow modules they supersede; never keep both.
</replace-the-tests>
