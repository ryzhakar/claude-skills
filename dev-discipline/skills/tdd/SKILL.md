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

DO NOT write all tests first, then all implementation. This produces tests that verify what you imagined, not what the code does.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED->GREEN: test1->impl1
  RED->GREEN: test2->impl2
  RED->GREEN: test3->impl3
```

Horizontal slicing makes tests ignore real changes -- they fail when behavior is fine and pass when behavior breaks. Each test should respond to what was learned from implementing the previous one.

## Workflow

### Phase 1: Planning

Before writing code:

1. Confirm with the user what interface changes are needed.
2. Confirm which behaviors to test and their priority.
3. Identify opportunities for deep modules: can I reduce methods? Simplify parameters? Hide more complexity inside?
4. Design interfaces for testability: accept dependencies (not create them), return results (not side effects), small surface area (fewer methods = fewer tests).
5. List behaviors to test (not implementation steps).
6. Get user approval on the plan.

You cannot test everything. Test core business logic and code with conditional branches. Skip trivial getters and boilerplate.

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

After all tests pass, look for refactor candidates:

- **Duplication** -- extract function/class
- **Long methods** -- break into private helpers (keep tests on public interface)
- **Shallow modules** -- combine or deepen
- **Feature envy** -- move logic to where data lives
- **Primitive obsession** -- introduce value objects
- **Existing code** the new code reveals as problematic

- Extract duplication.
- Deepen modules (move complexity behind simple interfaces).
- Apply SOLID principles where natural.
- Consider what new code reveals about existing code.
- Run tests after each refactor step.

**Never refactor while RED.** Get to GREEN.

## Per-Cycle Checklist

Before committing each red-green cycle:

- [ ] Test describes behavior, not implementation
- [ ] Test uses public interface only
- [ ] Test survives internal refactoring
- [ ] Code is minimal for this test
- [ ] Features are necessary, not speculative

## Good Tests vs Bad Tests

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe what the system does. They survive refactors because they do not care about internal structure.

**Bad tests** are coupled to implementation: they mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface).

**Good test (behavior through interface):**
```typescript
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

**Bad test (implementation coupling):**
```typescript
// BAD: mocks internal collaborator
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

**Bad test (bypasses interface):**
```typescript
// BAD: queries database directly instead of using interface
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
});

// GOOD: verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

Red flags indicating implementation coupling:
- Mocking internal collaborators
- Testing private methods
- Asserting on call counts or call order
- Breaking when refactoring without behavior change
- Describing HOW in test name, not WHAT
- Verifying through external means instead of interface

## Mocking Strategy

Mock at system boundaries only.

**Mock:**
- External APIs (payment, email, third-party services)
- Databases (sometimes -- prefer test database)
- Time and randomness
- File system (sometimes)

**Do not mock:**
- Own classes or modules
- Internal collaborators
- Anything under direct control

**Designing for mockability at system boundaries:**

1. **Dependency injection** -- pass dependencies in, do not create them internally:
   ```typescript
   // Testable: mock paymentClient
   function processPayment(order, paymentClient) { return paymentClient.charge(order.total); }
   // Hard to test: internal construction
   function processPayment(order) { const client = new StripeClient(process.env.STRIPE_KEY); ... }
   ```

2. **SDK-style interfaces** -- specific functions per operation, not one generic fetcher:
   ```typescript
   // GOOD: each mock returns one shape, no conditional logic in test setup
   const api = { getUser: (id) => fetch(`/users/${id}`), createOrder: (data) => ... };
   // BAD: mock requires conditional logic
   const api = { fetch: (endpoint, options) => fetch(endpoint, options) };
   ```

## Composability

If the agentic-delegation skill is available, apply its decomposition patterns to break features into independently testable units. Otherwise, find the smallest testable behavior, implement it, move to the next.

If the defensive-planning skill is available, use its TDD micro-task structure for plan granularity.

---

*Originally based on tdd, adapted and enhanced for this plugin.*
