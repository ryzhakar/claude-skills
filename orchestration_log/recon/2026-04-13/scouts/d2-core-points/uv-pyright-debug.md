# Core Points Extraction: uv-pyright-debug

## Iteration 1

**Point:** Standalone pyright reports zero errors while IDEs show hundreds because it runs against system Python without access to the uv-managed virtual environment's dependencies, causing pyright to fall back to lenient type inference.

**Evidence:**
1. Lines 10-12: "**Symptom:** IDE shows hundreds of type errors, but `pyright file.py` reports 0 errors. **Root Cause:** Standalone pyright uses system Python and can't import project dependencies (pydantic, etc.) installed in the uv-managed venv."
2. Lines 21-26: The side-by-side comparison explicitly shows "❌ WRONG - Uses system Python, misses venv packages" versus "✅ CORRECT - Uses project venv with all dependencies" when demonstrating `pyright` vs `uv run pyright`.
3. Lines 28-29: "**Key insight:** `uv run` ensures pyright sees the exact Python environment your code runs in, revealing type errors that depend on third-party package type stubs."

## Iteration 2

**Point:** The skill provides a complete pre-processing workflow using bundled analysis scripts to categorize, quantify, and line-index pyright errors before attempting any fixes, ensuring systematic understanding of error patterns.

**Evidence:**
1. Lines 32-58: Step 2 demonstrates the `analyze_errors.py` script that produces statistical breakdowns showing "Total errors: 819" with percentage distribution across error patterns and top error rules.
2. Lines 62-81: Step 3 introduces `line_index_errors.py` for creating line-indexed reports with explicit use case: "This index guides AST transformation scripts. Know exactly which lines need fixing before writing the transformer."
3. Lines 110-112: Step 5 distinguishes between manual fixes for "scattered issues (<10 instances)" versus "AST-based mass edits" for "systematic issues (10+ instances)" using "the error index as your guide."

## Iteration 3

**Point:** Pydantic model field optionality and alias definitions are frequently misunderstood by pyright when it lacks proper type stub access, causing it to treat Field(None, ...) parameters as required and fail to recognize field aliases.

**Evidence:**
1. Lines 87-95: "**Pattern 1: Optional Field Inference Failure**" shows how pyright without pydantic stubs "can't infer that `Field(None, ...)` makes parameters optional" despite the explicit None default.
2. Lines 97-103: "**Pattern 2: Field Alias Issues**" demonstrates the error "No parameter named 'from_'" when "Pyright sees parameter name `from_` but user code uses `from` (the alias)."
3. Lines 3-4 (description): The skill explicitly states it's "Critical for projects using pydantic models where Field() defaults may not be properly inferred."

## Iteration 4

**Point:** The skill enforces dual validation requiring both successful type checking through uv-run pyright and runtime execution to prove fixes are complete, rejecting type-check-only solutions.

**Evidence:**
1. Lines 120-131: The "Quick Validation" section explicitly requires "After fixes, confirm with both" and then lists type checking and runtime validation steps.
2. Line 131: "Both must pass for proof-of-work" makes dual validation non-negotiable.
3. Line 14: The solution statement "Always run pyright through the project's virtual environment using `uv run`" establishes the baseline that all validation must occur in the proper runtime context.

## Iteration 5

**Point:** Three operational gotchas can invalidate pyright results even when using uv run correctly: cache poisoning from stale pycache files, version mismatches between IDE and CLI pyright installations, and Python version mismatches between venv and pyproject.toml.

**Evidence:**
1. Line 116: "**Cache poisoning:** After fixing imports/dependencies, run `rm -rf **/__pycache__` before re-running pyright" identifies the first gotcha with explicit remediation.
2. Line 117: "**Version mismatch:** IDE pyright version may differ from CLI. Check with `pyright --version`" warns about tooling inconsistency.
3. Line 118: "**Python version mismatch:** Ensure venv Python matches pyproject.toml `requires-python`. Check with `ls -la .venv/bin/python*`" identifies environment configuration drift.

## Rank Summary

1. **Primary mechanism** (Iteration 1): The core diagnostic insight explaining why the skill exists - the uv run wrapper is essential for exposing true type errors.
2. **Workflow methodology** (Iteration 2): The systematic pre-analysis process using bundled scripts establishes the skill's operational approach before any fixes.
3. **Domain-specific pattern** (Iteration 3): The most common error category in the target domain (pydantic projects) that users will encounter.
4. **Success criteria** (Iteration 4): The non-negotiable validation requirement that defines when the debugging task is complete.
5. **Operational hazards** (Iteration 5): The environmental pitfalls that can undermine correct usage of the primary mechanism.
