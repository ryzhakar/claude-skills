# TDD Micro-Task Mode

Optional granularity protocol for plans where each task follows the test-driven development cycle. Apply when the implementation plan targets codebases with test infrastructure and the work involves creating or modifying behavior-carrying code.

## Bite-Sized Task Granularity

Each step represents one action taking 2-5 minutes. Use checkbox syntax for tracking.

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

The cycle repeats per behavior: write test, see it fail, implement minimally, see it pass, commit. Never batch all tests first then all implementation (horizontal slicing produces tests that verify imagined behavior, not actual behavior).

## File Structure Decomposition

Before defining tasks, map out which files will be created or modified and what each is responsible for. This structure informs the task decomposition.

- Design units with clear boundaries and well-defined interfaces. Each file has one clear responsibility.
- Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If a file has grown unwieldy, including a split in the plan is reasonable.

Each task should produce self-contained changes that make sense independently.

## Plan Self-Review

After writing the complete plan, review it with fresh eyes before handing off:

**1. Spec coverage:** Skim each section/requirement in the spec. Point to the task that implements it. List any gaps.

**2. Placeholder scan:** Search the plan for these red flags (all are plan failures):
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code -- the engineer may read tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

**3. Type consistency:** Verify types, method signatures, and property names used in later tasks match what was defined in earlier tasks. A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a plan bug.

Fix issues inline. If a spec requirement has no task, add the task.

## No-Placeholders Enforcement

Every step must contain the actual content an engineer needs. The following are plan failures -- never write them:

| Placeholder Pattern | Why It Fails |
|---|---|
| "TBD" / "TODO" / "implement later" | Defers decisions to the implementer |
| "Add appropriate error handling" | "Appropriate" is an escape hatch |
| "Write tests for the above" (no code) | Implementer writes minimal stub tests |
| "Similar to Task N" | Engineer may read tasks out of order |
| Descriptions without code blocks | Implementer interprets loosely |
| References to undefined types/functions | Creates gaps that get filled with guesses |
