# Reference Optionality Analysis: tdd

## Unit: tdd

## Reference Files Analyzed

1. `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/deep-modules.md`
2. `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/interface-design.md`
3. `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/mocking.md`
4. `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/refactoring.md`
5. `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/tests.md`

## Classification

### ESSENTIAL: None

All references can be loaded conditionally based on workflow phase.

### DEFERRABLE: deep-modules.md

**Loading gate:** IF Phase 1: Planning step 3 is reached ("Identify opportunities for deep modules"), THEN read `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/deep-modules.md`

**Gate location:** After step 2 (confirming behaviors to test) and before step 4 (designing interfaces for testability) in Phase 1: Planning workflow.

**Rationale:** The skill explicitly references this file only during the planning phase for identifying deep module opportunities. The main body already contains the core principle (small interface + deep implementation). The reference provides visual diagrams and detailed heuristics that are only needed when actively identifying deep module opportunities. The skill can execute all other phases (tracer bullet, incremental loop, refactor) without this content.

**Gate enforcement:** The planning phase is sequential and user-facing. Step 3 explicitly calls out "see @references/deep-modules.md for the small-interface, deep-implementation pattern." The gate is reached when the agent confirms behaviors and moves to identifying architectural opportunities.

### DEFERRABLE: interface-design.md

**Loading gate:** IF Phase 1: Planning step 4 is reached ("Design interfaces for testability"), THEN read `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/interface-design.md`

**Gate location:** After step 3 (identifying deep modules) and before step 5 (listing behaviors to test) in Phase 1: Planning workflow.

**Rationale:** The skill explicitly references this file during planning step 4 for "dependency injection, return-over-side-effect, and small surface area heuristics." The main body already summarizes the testability principle (tests verify behavior through public interfaces). The reference provides concrete code examples of testable vs hard-to-test patterns that are only needed when actively designing new interfaces. Phases 2-4 (tracer, loop, refactor) do not require this content.

**Gate enforcement:** Step 4 in Phase 1 explicitly calls out "see @references/interface-design.md for dependency injection, return-over-side-effect, and small surface area heuristics." The gate is reached when the agent moves from identifying deep module opportunities to designing specific testable interfaces.

### DEFERRABLE: mocking.md

**Loading gate:** IF the agent needs to mock dependencies during any test-writing phase (Phase 2: Tracer Bullet OR Phase 3: Incremental Loop), THEN read `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/mocking.md`

**Gate location:** At test-writing time in Phase 2 or Phase 3, when external dependencies must be isolated.

**Rationale:** The main body already contains the core mocking strategy (mock at system boundaries only, with specific lists of what to mock and what not to mock). It also summarizes the key patterns (dependency injection, SDK-style interfaces). The reference provides detailed code examples showing easy-to-mock vs hard-to-mock patterns. This detail is only needed when the agent encounters a concrete mocking scenario. Simple TDD cycles without external dependencies never need this content.

**Gate enforcement:** The "Mocking Strategy" section in the main body states "see @references/mocking.md for detailed patterns including dependency injection and SDK-style interface design." The gate is triggered when the agent writes a test that requires isolating external dependencies. The main body's guidance is sufficient for recognizing when mocking is needed; the reference provides implementation patterns.

### DEFERRABLE: refactoring.md

**Loading gate:** IF Phase 4: Refactor is reached ("look for refactor candidates"), THEN read `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/refactoring.md`

**Gate location:** After all tests pass in Phase 3, before beginning refactoring work in Phase 4.

**Rationale:** The skill explicitly references this file only during the refactor phase for "post-TDD extraction patterns (duplication, shallow modules, feature envy, primitive obsession)." The main body already provides high-level refactoring guidance (extract duplication, deepen modules, apply SOLID). The reference provides specific pattern recognition heuristics. Phases 1-3 (planning, tracer, incremental loop) do not require this content. The skill can function correctly without refactoring if the user stops after green tests.

**Gate enforcement:** Phase 4 explicitly states "look for refactor candidates — see @references/refactoring.md for the post-TDD extraction patterns." The gate is reached when all tests pass and the agent begins identifying refactoring opportunities. The sequential phase structure makes skipping impossible.

### DEFERRABLE: tests.md

**Loading gate:** IF the user asks "what makes a good test" OR the agent identifies implementation-coupled tests during any phase, THEN read `/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/references/tests.md`

**Gate location:** Triggered by user query or implementation-coupling detection during Phase 2 (Tracer Bullet), Phase 3 (Incremental Loop), or Phase 4 (Refactor).

**Rationale:** The main body already contains comprehensive good vs bad test guidance, including the core principle (tests describe WHAT not HOW), the litmus test (rename test), red flags (6 specific indicators), and the integration-style vs implementation-detail distinction. The reference provides side-by-side code examples with explanations. The skill description explicitly triggers on "what makes a good test" or "code review reveals implementation-coupled tests," indicating these are specific use cases where detailed examples are needed. Most TDD cycles can proceed correctly using only the main body's principles and red flags.

**Gate enforcement:** The skill description includes "what makes a good test" as a trigger phrase. The main body states "For side-by-side examples of good and bad tests with explanations, see @references/tests.md." The gate is triggered by: (1) user explicitly asking the trigger phrase, or (2) agent detecting red flags from the main body's list during test writing. The main body's red flags list enables detection without the reference.

## Summary

All 5 references are DEFERRABLE. Each has a concrete workflow gate:

- `deep-modules.md` — Phase 1, step 3
- `interface-design.md` — Phase 1, step 4  
- `mocking.md` — Phase 2/3, when mocking dependencies
- `refactoring.md` — Phase 4 entry
- `tests.md` — Triggered by user query or red flag detection

The main body provides sufficient guidance for the red-green-refactor cycle. References provide detailed patterns and examples that enhance execution quality but are not required for basic correctness.
