---
name: tdd
description: >
  This skill should be used when the user asks to "implement using TDD", "write tests first",
  "use test-driven development", "red-green-refactor", "write a failing test", "add test coverage
  with TDD", "what makes a good test", or when code review reveals implementation-coupled tests.
  Provides the philosophy, workflow, and technique of test-driven development including good/bad
  test patterns, mocking strategy, interface design for testability, and refactoring discipline.
---

# Test-Driven Development

Philosophy and technique for building software through the red-green-refactor cycle. Tests verify behavior through public interfaces, not implementation details.

## Core Principle

Tests describe WHAT the system does, not HOW it does it. A good test reads like a specification. Code can change entirely; tests should not break unless behavior changes.

**The litmus test:** Rename an internal function. If tests break but behavior has not changed, those tests were testing implementation, not behavior.

## Anti-Pattern: Horizontal Slicing

DO NOT write all tests first, then all implementation. This produces tests that verify imagined behavior rather than actual behavior.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED->GREEN: test1->impl1
  RED->GREEN: test2->impl2
  RED->GREEN: test3->impl3
```

Horizontal slicing causes tests to be insensitive to real changes -- they pass when behavior breaks and fail when behavior is fine. Each test should respond to what was learned from implementing the previous one.

## Workflow

### Phase 1: Planning

Before writing code:

1. Confirm with the user what interface changes are needed.
2. Confirm which behaviors to test and their priority.
3. Identify opportunities for deep modules — see @references/deep-modules.md for the small-interface, deep-implementation pattern.
4. Design interfaces for testability — see @references/interface-design.md for dependency injection, return-over-side-effect, and small surface area heuristics.
5. List behaviors to test (not implementation steps).
6. Get user approval on the plan.

Not everything can be tested. Focus testing effort on critical paths and complex logic, not every possible edge case.

### Phase 2: Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior -> test fails
GREEN: Write minimal code to pass -> test passes
```

This proves the path works end-to-end before committing to the full test suite.

### Phase 3: Incremental Loop

For each remaining behavior:

```
RED:   Write next test -> fails
GREEN: Minimal code to pass -> passes
```

Rules:
- One test at a time.
- Only enough code to pass the current test.
- Do not anticipate future tests.
- Keep tests focused on observable behavior.

### Phase 4: Refactor

After all tests pass, look for refactor candidates — see @references/refactoring.md for the post-TDD extraction patterns (duplication, shallow modules, feature envy, primitive obsession).

- Extract duplication.
- Deepen modules (move complexity behind simple interfaces).
- Apply SOLID principles where natural.
- Consider what new code reveals about existing code.
- Run tests after each refactor step.

**Never refactor while RED.** Get to GREEN first.

## Per-Cycle Checklist

Before committing each red-green cycle:

- [ ] Test describes behavior, not implementation
- [ ] Test uses public interface only
- [ ] Test would survive internal refactor
- [ ] Code is minimal for this test
- [ ] No speculative features added

## Good Tests vs Bad Tests

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe what the system does. They survive refactors because they do not care about internal structure.

**Bad tests** are coupled to implementation: they mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface).

For side-by-side examples of good and bad tests with explanations, see @references/tests.md — it covers behavior-testing vs implementation-coupling patterns.

Red flags indicating implementation coupling:
- Mocking internal collaborators
- Testing private methods
- Asserting on call counts or call order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

## Mocking Strategy

Mock at system boundaries only — see @references/mocking.md for detailed patterns including dependency injection and SDK-style interface design.

**Mock:**
- External APIs (payment, email, third-party services)
- Databases (sometimes -- prefer test database)
- Time and randomness
- File system (sometimes)

**Do not mock:**
- Own classes or modules
- Internal collaborators
- Anything under direct control

At system boundaries, design interfaces that are easy to mock: use dependency injection (pass dependencies in, do not create them internally), and prefer SDK-style interfaces (specific functions per operation) over generic fetchers.

## Composability

If the agentic-delegation skill is available, apply its decomposition patterns to break complex feature implementations into independently testable units, each suitable for a single red-green-refactor cycle. Otherwise, decompose manually: identify the smallest behavior that can be tested through a public interface, implement it, then move to the next.

When the defensive-planning skill is available, use its TDD micro-task mode (@references/tdd-mode.md) for structuring plans around the red-green-refactor cycle. Otherwise, follow the vertical slicing discipline described above.

## Reference Files

- @references/tests.md — Good and bad test examples with explanations
- @references/mocking.md — When to mock, dependency injection, SDK-style interfaces
- @references/deep-modules.md — Small interface + deep implementation philosophy
- @references/interface-design.md — Testability heuristics: accept dependencies, return results, small surface area
- @references/refactoring.md — Post-TDD refactor candidates: duplication, shallow modules, feature envy

---

*Originally based on tdd from https://github.com/mattpocock/skills, MIT licensed. Adapted and enhanced for this plugin.*
