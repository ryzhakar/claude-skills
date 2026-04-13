# Core Points Extraction: TDD Skill

## Iteration 1

**Point**: Tests must verify behavior through public interfaces, not implementation details, so that refactoring internal code does not break tests unless actual behavior changes.

**Evidence**:
1. SKILL.md line 17-19: "Tests describe WHAT the system does, not HOW it does it. A good test reads like a specification. Code can change entirely; tests should not break unless behavior changes. **The litmus test:** Rename an internal function. If tests break but behavior has not changed, those tests were testing implementation, not behavior."
2. SKILL.md lines 103-106: "**Good tests** are integration-style: they exercise real code paths through public APIs. They describe what the system does. They survive refactors because they do not care about internal structure. **Bad tests** are coupled to implementation: they mock internal collaborators, test private methods, or verify through external means"
3. tests.md lines 17-23: "Characteristics: Tests behavior users/callers care about, Uses public API only, Survives internal refactors, Describes WHAT, not HOW"

## Iteration 2

**Point**: TDD must follow vertical slicing (red-green cycle per behavior) rather than horizontal slicing (all tests then all implementation) to ensure tests respond to what was learned from implementing previous behaviors.

**Evidence**:
1. SKILL.md lines 21-36: "DO NOT write all tests first, then all implementation. This produces tests that verify imagined behavior rather than actual behavior... WRONG (horizontal): RED: test1, test2, test3, test4, test5 GREEN: impl1, impl2, impl3, impl4, impl5 RIGHT (vertical): RED->GREEN: test1->impl1, RED->GREEN: test2->impl2, RED->GREEN: test3->impl3. Horizontal slicing causes tests to be insensitive to real changes -- they pass when behavior breaks and fail when behavior is fine. Each test should respond to what was learned from implementing the previous one."
2. SKILL.md lines 66-77: "For each remaining behavior: RED: Write next test -> fails, GREEN: Minimal code to pass -> passes. Rules: One test at a time. Only enough code to pass the current test. Do not anticipate future tests."
3. SKILL.md lines 98-100: "Per-Cycle Checklist... Code is minimal for this test, No speculative features added"

## Iteration 3

**Point**: Mock only at system boundaries (external APIs, databases, time) and never mock internal collaborators or classes under direct control, designing boundary interfaces with dependency injection and SDK-style patterns for mockability.

**Evidence**:
1. SKILL.md lines 119-133: "Mock at system boundaries only... **Mock:** External APIs (payment, email, third-party services), Databases (sometimes -- prefer test database), Time and randomness, File system (sometimes). **Do not mock:** Own classes or modules, Internal collaborators, Anything under direct control. At system boundaries, design interfaces that are easy to mock: use dependency injection (pass dependencies in, do not create them internally), and prefer SDK-style interfaces (specific functions per operation) over generic fetchers."
2. mocking.md lines 3-14: "Mock at **system boundaries** only: External APIs (payment, email, etc.), Databases (sometimes - prefer test DB), Time/randomness, File system (sometimes). Don't mock: Your own classes/modules, Internal collaborators, Anything you control"
3. mocking.md lines 37-59: "Prefer SDK-style interfaces over generic fetchers: Create specific functions for each external operation instead of one generic function with conditional logic... The SDK approach means: Each mock returns one specific shape, No conditional logic in test setup, Easier to see which endpoints a test exercises, Type safety per endpoint"

## Iteration 4

**Point**: Refactoring must only occur after achieving green (all tests pass), never while red (tests failing), to maintain the discipline of the red-green-refactor cycle.

**Evidence**:
1. SKILL.md line 89: "**Never refactor while RED.** Get to GREEN first."
2. SKILL.md lines 79-88: "After all tests pass, look for refactor candidates... Extract duplication. Deepen modules (move complexity behind simple interfaces). Apply SOLID principles where natural. Consider what new code reveals about existing code. Run tests after each refactor step."
3. SKILL.md lines 54-62: "Phase 2: Tracer Bullet... RED: Write test for first behavior -> test fails, GREEN: Write minimal code to pass -> test passes. This proves the path works end-to-end before committing to the full test suite."

## Iteration 5

**Point**: Design interfaces as deep modules with small surfaces (few methods, simple parameters) that hide complex implementation, making them easier to test and maintain.

**Evidence**:
1. SKILL.md lines 45-46: "Identify opportunities for deep modules — see @references/deep-modules.md for the small-interface, deep-implementation pattern... Design interfaces for testability — see @references/interface-design.md for dependency injection, return-over-side-effect, and small surface area heuristics."
2. deep-modules.md lines 5-17: "**Deep module** = small interface + lots of implementation... Small Interface (Few methods, simple params), Deep Implementation (Complex logic hidden). **Shallow module** = large interface + little implementation (avoid)"
3. interface-design.md lines 29-32: "**Small surface area**: Fewer methods = fewer tests needed, Fewer params = simpler test setup"

## Rank Summary

1. **Behavior-over-implementation testing** (Iteration 1) - The foundational principle that determines test quality and resilience
2. **Vertical slicing discipline** (Iteration 2) - The workflow pattern that ensures tests reflect reality rather than imagination
3. **Boundary-only mocking** (Iteration 3) - The constraint that prevents implementation coupling through excessive mocking
4. **Green-before-refactor** (Iteration 4) - The discipline that maintains TDD cycle integrity
5. **Deep module design** (Iteration 5) - The interface philosophy that makes code testable and maintainable
