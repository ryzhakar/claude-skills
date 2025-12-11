---
name: uv-pyright-debug
description: Debug type errors in uv-managed Python projects by accessing true pyright diagnostics. Use when IDE shows type errors but standalone pyright reports 0 errors, or when systematic analysis of type errors is needed before mass edits. Critical for projects using pydantic models where Field() defaults may not be properly inferred.
---

# UV-Pyright Debugging Workflow

## The Core Problem

**Symptom:** IDE shows hundreds of type errors, but `pyright file.py` reports 0 errors.

**Root Cause:** Standalone pyright uses system Python and can't import project dependencies (pydantic, etc.) installed in the uv-managed venv. Without proper imports, pyright falls back to lenient type inference, hiding real errors.

**Solution:** Always run pyright through the project's virtual environment using `uv run`.

## Debug Workflow

### Step 1: Access True Pyright Report

```bash
# ❌ WRONG - Uses system Python, misses venv packages
pyright structured_query_builder/examples.py

# ✅ CORRECT - Uses project venv with all dependencies
uv run pyright structured_query_builder/examples.py --outputjson > errors.json
```

**Key insight:** `uv run` ensures pyright sees the exact Python environment your code runs in, revealing type errors that depend on third-party package type stubs.

### Step 2: Analyze Error Patterns

Use the bundled analysis script to identify error categories and frequency:

```bash
uv run pyright file.py --outputjson | python3 scripts/analyze_errors.py
```

**Output example:**
```
📊 Pyright Error Analysis
============================================================
Total errors: 819

Error Pattern Distribution:
  Argument missing (single param)           584 ( 71.3%)
  Arguments missing (multiple params)       159 ( 19.4%)
  No parameter named                         50 (  6.1%)
  Type mismatch                              26 (  3.2%)

Top Error Rules:
  reportCallIssue                            793
  reportArgumentType                          26

First 10 Errors (with line numbers):
   1. Line   63: Arguments missing for parameters "from", "where", "group_by"...
   2. Line   65: Argument missing for parameter "alias"
   ...
```

### Step 3: Create Line-Indexed Error Report (For Mass Edits)

Before applying AST-based transformations, pre-index errors by line number:

```bash
uv run pyright file.py --outputjson | python3 scripts/line_index_errors.py > error_index.txt
```

**Output example:**
```
Line-Indexed Error Report (819 total errors)
================================================================================

L63: (2 errors)
  • Arguments missing for parameters "from", "where", "group_by"
  • Argument missing for parameter "alias"

L65: (1 error)
  • Argument missing for parameter "table_alias"
```

**Use case:** This index guides AST transformation scripts. Know exactly which lines need fixing before writing the transformer.

### Step 4: Identify Root Causes

Common patterns in uv-managed projects:

**Pattern 1: Optional Field Inference Failure**
```python
# Pydantic model
class Query(BaseModel):
    select: list[SelectExpr] = Field(...)  # Required
    where: Optional[WhereL1] = Field(None, ...)  # Optional but pyright thinks required
```

**Cause:** Pyright without pydantic type stubs can't infer that `Field(None, ...)` makes parameters optional.

**Pattern 2: Field Alias Issues**
```python
from_: FromClause = Field(..., alias="from")
```

**Error:** "No parameter named 'from_'"
**Cause:** Pyright sees parameter name `from_` but user code uses `from` (the alias).

**Pattern 3: Discriminated Union Issues**
Type narrowing fails when pyright can't see discriminator field definitions from imported models.

### Step 5: Strategic Fixes

**For scattered issues (<10 instances):** Manual fixes using the line-indexed report.

**For systematic issues (10+ instances):** Use AST-based mass edits with the error index as your guide.

## Common Gotchas

1. **Cache poisoning:** After fixing imports/dependencies, run `rm -rf **/__pycache__` before re-running pyright
2. **Version mismatch:** IDE pyright version may differ from CLI. Check with `pyright --version`
3. **Python version mismatch:** Ensure venv Python matches pyproject.toml `requires-python`. Check with `ls -la .venv/bin/python*`

## Quick Validation

After fixes, confirm with both:
```bash
# Type checking
uv run pyright file.py --outputjson | python3 -c "import json,sys; print(f\"Errors: {json.load(sys.stdin)['summary']['errorCount']}\")"

# Runtime validation
uv run python -m your_module
```

Both must pass for proof-of-work.

## Bundled Scripts

### scripts/analyze_errors.py
Parse pyright JSON output, categorize errors by pattern, show frequency distribution and top 10 errors with line numbers.

### scripts/line_index_errors.py
Create line-indexed error report from pyright JSON. Groups errors by line number for pre-surveying before AST-based mass edits.
