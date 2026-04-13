# Synthesis Report: tdd (Re-synthesis)

**Baseline:** 1318t (SKILL.md) + 331t (mocking.md) + 200t (deep-modules.md) + 359t (tests.md) + 150t (interface-design.md) + 87t (refactoring.md) = 2445t total

**Previous synthesis:** Inlined 3 tiny refs (refactoring, interface-design, deep-modules) at 437t. Kept mocking.md (331t) and tests.md (359t) as lazy references. This re-synthesis inlines ALL references since all are under 1400t.

---

## Core Points (Untouchable)

1. Tests verify behavior through public interfaces, not implementation details -- the litmus test: rename an internal function; if tests break but behavior has not changed, those tests tested implementation
2. Vertical slicing (red-green per behavior) not horizontal slicing (all tests then all implementation) -- each test responds to what was learned from implementing the previous one
3. Mock only at system boundaries (external APIs, databases, time) -- never mock internal collaborators or classes under direct control
4. Never refactor while RED -- get to GREEN first
5. Design interfaces as deep modules: small surface (few methods, simple parameters) hiding complex implementation

---

## Inline from References

### INLINE: refactoring.md (87t) -- FULL INLINE (unchanged from previous synthesis)
**Action:** Merge 6-item bullet list into Phase 4: duplication, long methods, shallow modules, feature envy, primitive obsession, existing code the new code reveals as problematic.
**Net cost:** +20t.

### INLINE: interface-design.md (150t) -- FULL INLINE (unchanged from previous synthesis)
**Action:** Move 3-item summary into Phase 1 step 4: accept dependencies (not create them), return results (not side effects), small surface area (fewer methods = fewer tests).
**Net cost:** +30t.

### INLINE: deep-modules.md (200t) -- FULL INLINE (unchanged from previous synthesis)
**Action:** Inline 3 design questions into Phase 1 step 3: Can I reduce methods? Simplify parameters? Hide more complexity inside?
**Net cost:** +15t.

### INLINE: mocking.md (331t) -- NEW INLINE

Cite: Previous synthesis kept this as lazy reference. Directive overrides: all refs under 1400t must inline. The SKILL.md already contains the mock/don't-mock lists and DI+SDK summary. The reference adds code examples.

**Content to inline (compressed ~180t):**

Expand the existing Mocking Strategy section with the key patterns:

```
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
```

**Savings from deleting reference file:** 331t removed. Body grows ~180t. Net: -151t.

### INLINE: tests.md (359t) -- NEW INLINE

Cite: Previous synthesis kept this as lazy reference. Directive overrides: all refs under 1400t must inline. Models skip lazy references.

**Content to inline (compressed ~200t):**

Expand the "Good Tests vs Bad Tests" section with the code examples:

```
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
```

**Savings from deleting reference file:** 359t removed. Body grows ~200t. Net: -159t.

---

## Cut

### CUT-1: "possible" in "simplest possible reproduction" (~1t)
Cite: D3 Strunk R13.

### CUT-2: "first" in "Get to GREEN first" (~1t)
Cite: D3 Strunk R13.

### CUT-3: Remaining reference link sentences (~10t)
All @references/ links removed since content is inlined. Reference Files section at bottom deleted entirely.

### CUT-4: Composability sentence compression (lines 135-139, ~15t)
Cite: D3 Strunk R13.
**Action:** Compress: "If agentic-delegation is available, use its decomposition patterns to break features into independently testable units. Otherwise, find the smallest testable behavior, implement it, move to the next." / "If defensive-planning is available, use its TDD micro-task structure for plan granularity."

**Total cut savings:** ~27t

---

## Restructure

### RESTRUC-1: Active voice for anti-pattern warnings
Cite: D3 Strunk R10 Severe.
- "This produces tests that verify imagined behavior" -> "This produces tests that verify what you imagined, not what the code does"
- "causes tests to be insensitive to real changes" -> "makes tests ignore real changes"
- "Not everything can be tested" -> "You cannot test everything"

### RESTRUC-2: Parallel construction in per-cycle checklist (lines 95-99)
Cite: D3 Strunk R15.
- "Test describes behavior, not implementation"
- "Test uses public interface only"
- "Test survives internal refactoring"
- "Code is minimal for this test"
- "Features are necessary, not speculative"

### RESTRUC-3: Parallel construction in red flags (lines 109-116)
Cite: D3 Strunk R15. Standardize to gerunds:
- "Mocking internal collaborators"
- "Testing private methods"
- "Asserting on call counts or call order"
- "Breaking when refactoring without behavior change"
- "Describing HOW in test name, not WHAT"
- "Verifying through external means instead of interface"

---

## Strengthen

### STR-1: Emphatic position for horizontal slicing warning (line 36)
Cite: D3 Strunk R18.
**Action:** "they fail when behavior is fine and pass when behavior breaks" (worse outcome last).

### STR-2: Replace vague "critical paths and complex logic" (line 52)
Cite: D4 CLR-2.
**Action:** "Test core business logic and code with conditional branches. Skip trivial getters and boilerplate."

### STR-3: DI colon instead of parenthetical (line 132)
Cite: D3 Strunk R18.
**Action:** "use dependency injection: pass dependencies in rather than creating them internally"

---

## Hook/Command Splits

No hook candidates. TDD is a development methodology, not an enforcement pattern.

---

## Delete List

- `dev-discipline/skills/tdd/references/refactoring.md`
- `dev-discipline/skills/tdd/references/interface-design.md`
- `dev-discipline/skills/tdd/references/deep-modules.md`
- `dev-discipline/skills/tdd/references/mocking.md`
- `dev-discipline/skills/tdd/references/tests.md`

---

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| SKILL.md body | 1318t | ~1683t | +365t |
| mocking.md | 331t | 0 (deleted) | -331t |
| deep-modules.md | 200t | 0 (deleted) | -200t |
| tests.md | 359t | 0 (deleted) | -359t |
| interface-design.md | 150t | 0 (deleted) | -150t |
| refactoring.md | 87t | 0 (deleted) | -87t |
| **Total** | **2445t** | **~1683t** | **-762t (-31.2%)** |

31% total reduction vs previous synthesis's 16%. Previous synthesis left mocking.md and tests.md as lazy refs (690t combined) that models ignored. Now everything is inline. Body grows to ~1683t (under 2000t, well within skill body budget). All 5 reference files deleted.
