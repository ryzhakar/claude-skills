# Synthesis: improve-architecture (REVISED -- full inline)

**Baseline**: 1228 tokens (SKILL.md) + 327 tokens (rfc-template.md) + 803 tokens (dependency-categories.md) = **2358 tokens total**
**D4 Score**: 85/100
**References**: 2 files, both inlined. Zero surviving reference files.

---

## Core Points (Untouchable)

1. **Deep module philosophy** -- small interface hiding large implementation; drives all decisions. (D2 rank 1)
2. **4-category dependency classification** -- in-process, local-substitutable, ports-and-adapters, true external; each requires different testing strategy. (D2 rank 2)
3. **Multi-design parallel exploration** -- 3+ agents with distinct constraints reveal design tensions through structured disagreement. (D2 rank 3)
4. **Friction-driven discovery** -- difficulty understanding code IS the signal for architectural problems. (D2 rank 4)
5. **Durable RFC publication** -- describe modules by responsibility and behavior, not file paths. (D2 rank 5)

---

## Inline from References

### dependency-categories.md (803t) -> INLINE as flowchart (~140t)

Previous synthesis already planned this. Flowchart is load-bearing; prose descriptions of each category are inferrable by Claude. Cut examples (parsers, PostgreSQL, Stripe, etc.), cut testing prose, cut validation notes.

**Inlined**: Selection flowchart + one-line strategy per category.

### rfc-template.md (327t) -> INLINE as compressed template (~180t)

Previous synthesis kept this as lazy reference. Under the revised directive, 327t is under 1000t-after-compression. INLINE.

The template structure is needed exactly once at Phase 6. Inlining adds ~180t but eliminates a file-read round-trip and the risk of Claude skipping the reference.

**Inlined**: Issue template with section headers and guidance compressed into imperative instructions.

---

## Proposed SKILL.md

```markdown
---
name: improve-architecture
description: >
  Explores codebases for architectural friction, discovers module-deepening opportunities,
  and proposes refactors through multi-design exploration. Triggers: "improve architecture",
  "find refactoring opportunities", "deepen shallow modules", "reduce coupling",
  "simplify module structure", mentions of architectural friction or module boundaries.
  Publishes refactor RFC as GitHub issue.
---

# Improve Architecture

Explore a codebase to surface architectural friction, discover module-deepening opportunities,
and propose concrete refactors via multi-design exploration. Publish results as a GitHub issue RFC.

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

After the user selects a design (or accepts the recommendation), create a
GitHub issue using `gh issue create` with this structure.
Publish directly and share the URL.

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
```

---

## Change Log vs Previous Synthesis

| Change | Citation | Rationale |
|--------|----------|-----------|
| rfc-template.md INLINED (was kept as lazy ref) | Critical directive: ALL refs under 1200t must inline | 327t file, well under threshold. Template needed once at Phase 6; inlining eliminates file-read risk. Compressed from 327t to ~180t. |
| dependency-categories.md INLINED (same as previous) | Previous synthesis already planned this | Flowchart + one-line strategies. 803t -> ~140t. |
| Description rewritten: third-person active, front-loaded | D3 R10; plugin-dev-ecosystem 1.2; compression-strategies 7.2 | Was passive "This skill should be used when...". |
| Phase 1: three overlapping directives collapsed to one | D3 R13 "Three directives saying similar things"; D4 CLR-2 "'organically' undefined" | "Navigate organically" + "Do NOT follow rigid heuristics" + "explore as a developer would" -> single line. Friction list operationally defines approach. |
| Friction signal list: parallel construction fixed | D3 R15 "mixed grammatical forms" | All noun-phrase labels with explanatory clauses. |
| "Do NOT propose interfaces yet" -> cut | D3 R13 "'yet' implied by next sentence"; R11 "negative construction" | Next sentence ("Ask the user...") sequences the work. |
| "Do NOT ask the user to review before creating" -> "Publish directly and share the URL" | D3 R13 "redundant" | Positive construction, same meaning. |
| "through structured multi-design exploration" -> "via multi-design exploration" | D3 R13 "wordy" | Shorter. |
| Deep module definition: "hides a large implementation behind a small interface" | D3 R18 "ends with 'implementation' (weak)" | Ends with "interface" -- the key concept. |
| Shallow module sentence: "...forces tests to mirror implementation rather than behavior" | D3 R18 "ends with 'internal structure' -- weak" | Ends with behavior/implementation contrast. |
| "Most naturally" -> "Requires fewest lines for the common case" | D4 CLR-2 "'most naturally' is vague/subjective" | Concrete, measurable. |
| Added "Describe modules by responsibility, not file paths" to Phase 2 | D2 core point 5 | Durability principle surfaces earlier. |
| Boundary rule added after flowchart | dependency-categories.md line 79-82 | Load-bearing constraint: "Never mock deeper than the immediate boundary." |
| Preserved: "The user wants a strong read, not a menu." | D2 core point 3 | Load-bearing anti-hedging constraint. |
| Preserved: "delete the old tests" | D2 core point 1 | Emphatic testing replacement principle. |
| Attribution footer -> removed | Context cost | To ATTRIBUTION file. |

---

## Projected Token Delta

| Category | Tokens |
|----------|--------|
| Baseline (SKILL.md + 2 refs) | 2358 |
| Inline dependency flowchart | +140 (into SKILL.md) |
| Inline RFC template | +180 (into SKILL.md) |
| Delete dependency-categories.md | -803 |
| Delete rfc-template.md | -327 |
| Strunk compression + D4 fixes | -65 |
| **Projected** | **~1483** |
| **Net reduction** | **~875 tokens (37.1%)** |
| **Surviving reference files** | **0** |

All content now in a single SKILL.md. Both references eliminated. The dependency flowchart
(140t) replaces 803t of prose. The RFC template (180t) replaces 327t through light compression
of section guidance text.
