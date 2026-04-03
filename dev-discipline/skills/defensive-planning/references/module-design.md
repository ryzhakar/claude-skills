# Module Design Heuristics

Decomposition guidance for structuring modules within implementation plans. Apply when deciding how to break work into units, where to draw interfaces, and what to test.

## Deep Modules Philosophy

A **deep module** encapsulates a lot of functionality behind a simple, testable interface that rarely changes.

```
Deep Module (preferred):
+---------------------+
|   Small Interface   |  <- Few methods, simple params
+---------------------+
|                     |
|                     |
| Deep Implementation |  <- Complex logic hidden
|                     |
|                     |
+---------------------+

Shallow Module (avoid):
+---------------------------------+
|       Large Interface           |  <- Many methods, complex params
+---------------------------------+
|  Thin Implementation            |  <- Just passes through
+---------------------------------+
```

When designing modules, ask:
- Can the number of methods be reduced?
- Can parameters be simplified?
- Can more complexity be hidden inside?

Shallow modules (large interface, thin implementation) create integration overhead without encapsulation value. They force callers to understand internals they should not care about.

## Testability as Decomposition Criterion

Actively look for opportunities to extract modules that can be tested in isolation. Module boundaries should coincide with testability boundaries:

- A module that accepts dependencies rather than creating them is testable (dependency injection).
- A module that returns results rather than producing side effects is testable (pure functions).
- A module with a small surface area needs fewer tests to cover (small interface = fewer test cases).

When decomposing work, verify that each proposed module can have its behavior confirmed through its public interface alone. If testing a module requires reaching into its internals or inspecting side effects through back channels, the interface needs redesign.

## Testing Decisions Template

Include this section in implementation plans to make testing strategy explicit:

```markdown
## Testing Decisions

**What makes a good test for this project:**
- Tests verify external behavior through public interfaces, not implementation details
- Tests survive internal refactoring (if behavior unchanged, tests should still pass)
- [Project-specific criteria from codebase conventions]

**Modules that will be tested:**
- [Module A]: [What behaviors to verify]
- [Module B]: [What behaviors to verify]
- [Module C]: Not tested -- [justification: trivial wrapper, pure delegation, etc.]

**Prior art:**
- Existing tests in [path] follow [pattern]
- Test runner: [tool and configuration]
- Test naming convention: [convention from codebase]
```

Making testing decisions explicit prevents two failure modes: undertesting (implementer skips tests for "obvious" code) and overtesting (implementer writes implementation-coupled tests that break on every refactor).

## Integration with Plan Structure

When writing implementation plan phases:

1. **File structure decomposition** identifies modules and their responsibilities.
2. **Deep modules heuristic** evaluates whether the proposed interfaces are appropriately deep.
3. **Testability criterion** confirms each module can be tested through its interface.
4. **Testing decisions section** documents which modules get tests and what those tests verify.

This sequence runs before task decomposition. The module structure determines the task structure, not the other way around.
