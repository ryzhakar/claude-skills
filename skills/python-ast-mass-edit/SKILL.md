---
name: python-ast-mass-edit
description: Systematic workflow for AST-based mass edits in Python codebases. Use when editing 3+ files with structural changes (decorators, function signatures, imports, class definitions). Includes pre-surveying with grep/pyright, idempotent transformations, and validation protocol. NOT for simple string replacements or <5 instances.
---

# AST-Based Mass Edit Protocol

## When to Use AST

**Trigger condition:** Editing **3+ files** with **structural changes** (decorators, function signatures, imports, class definitions).

**Test question:** Can you say "find all functions with X and change to Y"? If yes, use AST.

**When NOT to use:**
- String content changes (comments, docstrings, literals) → Use manual edits or sed
- < 5 instances total → Manual edits faster than script setup
- Complex logic requiring semantic understanding → Manual review safer

## 4-Step Execution Protocol

### Step 1: Survey (Pre-index instances)

Build line-number-with-structured-annotations index BEFORE writing transformer:

**For general patterns:**
```bash
grep -rn "pattern" src/ | wc -l  # Count instances
grep -rn "pattern" src/           # See all locations
```

**For type errors (when fixing pyright issues):**
```bash
uv run pyright file.py --outputjson | python3 -c "
import json,sys
for e in json.load(sys.stdin)['generalDiagnostics']:
    print(f'L{e[\"range\"][\"start\"][\"line\"]+1}: {e[\"message\"]}')" > error_index.txt
```

**Output:** Line-indexed list of ALL transformation targets. This is your ground truth.

### Step 2: Transform (Throwaway AST script)

Write one-time-use `fix_X.py` in project root. Use the bundled `scripts/template_transformer.py` as starting point.

**Critical requirements:**
```python
import ast

class MyTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # 1. IDEMPOTENCY: Guard clause to only transform what needs changing
        if node.name.startswith("query_"):
            # Make change
            print(f"  Transformed: {node.name}")  # 2. VISIBILITY: Print all changes

        return self.generic_visit(node)  # 3. TRAVERSAL: Always call generic_visit

# Read → Parse → Transform → Unparse → Write
source = file.read_text()
tree = ast.parse(source)
new_tree = MyTransformer().visit(tree)
new_source = ast.unparse(new_tree)  # 4. UNPARSE: Always use ast.unparse()
file.write_text(new_source)
```

**Run and observe:**
```bash
python3 fix_X.py
# Should print every change made for verification
```

### Step 3: Validate (Non-optional checks)

```bash
# 1. Format (AST unparse output needs formatting)
ruff format .

# 2. Review diff (catch unintended transformations)
git diff

# 3. Clear caches (stale imports cause false test passes)
rm -rf **/__pycache__ .pytest_cache

# 4. Run tests
pytest

# If ANY step fails: git checkout . and fix the script
```

**The diff review is non-negotiable.** AST transformations can have subtle bugs.

### Step 4: Commit (Proof-of-work)

```bash
# Delete the throwaway script
rm fix_X.py

# Final validation
pytest

# Commit with evidence
git add .
git commit -m "refactor: rename 'arg' → 'column' in WindowExpr/AggregateExpr

- Transformed 20 function calls across 4 files
- Tests pass (36 → 36 passing)
"
```

**Never commit:**
- The transformation script itself
- Partial transformations (all-or-nothing)
- Code that doesn't pass tests

## Common AST Patterns

**Rename function parameter:**
```python
def visit_Call(self, node):
    if isinstance(node.func, ast.Name) and node.func.id == "MyFunc":
        for kw in node.keywords:
            if kw.arg == "old_name":
                kw.arg = "new_name"
    return self.generic_visit(node)
```

**Change decorator argument:**
```python
def visit_FunctionDef(self, node):
    for dec in node.decorator_list:
        if isinstance(dec, ast.Call) and dec.func.id == "register":
            for kw in dec.keywords:
                if kw.arg == "query_number":
                    old_val = kw.value.value
                    kw.value = ast.Constant(value=old_val + 100)
    return self.generic_visit(node)
```

**Update import:**
```python
def visit_ImportFrom(self, node):
    if node.module == "old_package":
        node.module = "new_package"
    return self.generic_visit(node)
```

## Idempotency Patterns

**Problem:** Running script twice makes unwanted changes.

**Solution:** Guard clauses that detect already-transformed code:

```python
# ❌ BAD - No guard, will keep incrementing
kw.value = ast.Constant(value=kw.value.value + 100)

# ✅ GOOD - Only transform if in original range
old_val = kw.value.value
if 1 <= old_val <= 7:
    kw.value = ast.Constant(value=old_val + 100)
```

## Troubleshooting

**"Transformation didn't catch all instances"**
→ Check your survey. Did you miss a variant pattern? Re-run Step 1.

**"Tests pass but code is broken"**
→ Stale cache. Run `rm -rf **/__pycache__` and test again.

**"Git diff shows unrelated changes"**
→ `ruff format` changed other code. Review diff carefully before committing.

**"Script errors on complex code"**
→ AST can't handle all Python syntax (f-strings with complex nesting, etc.). Consider manual edits.

## Bundled Resources

### scripts/template_transformer.py
Starting template for AST transformations with best practices built-in (idempotency checks, change logging, error handling).
