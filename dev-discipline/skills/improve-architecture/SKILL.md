---
name: improve-architecture
description: >
  Find architectural friction — places where understanding a codebase breaks down — explore in parallel several designs for a deepened module — one hiding more implementation behind a smaller interface — and write an RFC — a proposal document — recommending one.
  "improve the architecture", "find refactoring opportunities", "deepen shallow modules", "reduce coupling", "simplify the module structure",
  "this module is hard to navigate", or any mention of architectural friction or module boundaries.
---

<explore-for-friction>
Explore the codebase as a developer new to it, reading the code behind each concept the task touches; never grep for keywords alone.

Note each friction — a place where understanding breaks down — with the files that show it; never note a friction without its files.

Count as frictions: bouncing — understanding one concept takes many small files; a shallow module — a module, a file or directory that outside code reaches through one interface, whose interface is nearly as complex as its internals; testability extraction — pure functions pulled out for tests while bugs live in the integration; tight coupling — modules sharing types or co-owning a concept; a test gap — a module untested or tested through elaborate mocks; never count a style complaint as a friction.
</explore-for-friction>

<rank-the-candidates>
Write each deepening candidate — a cluster of modules that could hide behind one smaller interface — as an entry of the ranked list the RFC's `Problem` section carries, with the modules involved, the coupling signal — the shared types, call patterns, or co-owned concept that tie them — and the existing tests a boundary test — a test through the cluster's new interface — would replace; never write a candidate missing one of the three.

Describe each module by its responsibility; never describe one by its file path alone.

Rank the candidates by the count of modules each hides divided by the count of public entry points that production code outside the cluster calls today; never rank by taste.

Take the first-ranked candidate; never ask which to explore.
</rank-the-candidates>

<classify-the-dependencies>
Classify each dependency of the candidate — each module of this repository and each remote service the cluster's code calls from outside itself — by the first class that matches, in this order: in-process when it involves no I/O — no reading or writing outside the process; a port when the remote service is built and deployed from this repository; local-substitutable when the repository already holds or runs a local stand-in for the service, such as a fake, an emulator, or a container of the service itself; external otherwise; never leave a dependency unclassified.

State in the design brief how each dependency is handled, by class: move an in-process dependency into the deepened module, keeping the original where other modules still import it, and unit-test it directly; define for a port a set of domain operations — operations named in the business's own terms — and inject an adapter — the code that carries those operations to the service; test a local-substitutable dependency against its stand-in at the boundary — the edge where the deepened module meets that dependency; mock an external dependency at the boundary and contract-test the real client; never handle a dependency outside its class's way.

Mock at the boundary; never mock inside it.
</classify-the-dependencies>

<write-the-design-brief>
Write the design brief — the text every design agent receives — with the constraints any new interface has to satisfy, the dependencies with their classes, the complexity to hide, the file paths, and a rough sketch of a call site; never write a brief missing one of the five.

Label the sketch illustrative in the brief; never let a design agent read it as a proposal.
</write-the-design-brief>

<explore-designs-in-parallel>
Launch three or more agents through `agentic-delegation`, each with the same design brief and one distinct constraint: the smallest interface, one to three entry points; the widest flexibility, many uses and extension points; the trivial common case, the most frequent caller's call reduced to one line; a ports-and-adapters shape when a dependency of any class but in-process exists; never give two agents the same distinct constraint.

Require from each agent the interface signature, a usage example, the complexity it hides, the handling of each dependency, and where the design breaks down; never accept a design missing one of the five.

Continue an agent whose design misses one of the five until all five are present; never fill a missing part in its place.
</explore-designs-in-parallel>

<compare-and-recommend>
Compare the designs on where they agree — the likely true boundaries, where they diverge — the real tensions, which needs the fewest lines for the common case, and which survives a requirement change best; never list the designs without the comparison.

Recommend one design, or a hybrid of named parts, with the reason; never present a menu.
</compare-and-recommend>

<write-the-rfc>
Write the RFC to the project's RFC directory — `docs/rfcs/`, `rfcs/`, or the directory the project already uses, created as `docs/rfcs/` when none exists — named like the RFCs already there, else `<slug>.md` with `<slug>` the name the recommended design gives the deepened module, in lowercase hyphenated words; never return the RFC as conversation text.

Give the RFC five sections: `Problem` — the frictions with their files as evidence, the ranked candidates, the integration risk in the seams — where the shallow modules meet — and the cost to navigation, testing, and maintenance; `Proposed interface` — the comparison, the recommendation with its reason, the signature, a usage example, the hidden complexity; `Dependency strategy` — each dependency's class and handling; `Testing strategy` — the boundary tests to write, the existing tests they replace and the deletion of those, the stand-ins or adapters needed; `Implementation recommendations` — what the module owns, hides, and exposes, how callers migrate, whether the callers' interface or a dependency's adapter comes first; never leave a section out.

Describe modules by responsibility and behavior outside `Problem`; never describe one by its current file layout there.

Print the RFC's path; never print its content.
</write-the-rfc>
