# Strunk Analysis: uv-pyright-debug

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 10: "IDE shows hundreds of type errors, but `pyright file.py` reports 0 errors."**
- First clause active (good), second clause active (good). No violation.

**Line 12: "Standalone pyright uses system Python and can't import project dependencies (pydantic, etc.) installed in the uv-managed venv."**
- Active voice throughout. No violation.

**Line 14: "Always run pyright through the project's virtual environment using `uv run`."**
- Passive "run pyright through" could be more direct.
- Severity: Moderate
- Suggested revision: "Always invoke pyright through the project's virtual environment using `uv run`." OR "Always use `uv run` to invoke pyright."

**Line 28: "Key insight: `uv run` ensures pyright sees the exact Python environment your code runs in, revealing type errors that depend on third-party package type stubs."**
- Mixed construction: "ensures pyright sees" (active) but "revealing" dangles without clear subject.
- Severity: Moderate
- Suggested revision: "Key insight: `uv run` ensures pyright sees the exact Python environment your code runs in. This reveals type errors that depend on third-party package type stubs."

**Line 92: "Pyright without pydantic type stubs can't infer that `Field(None, ...)` makes parameters optional."**
- Active voice with clear subject "Pyright." No violation.

**Line 116: "After fixing imports/dependencies, run `rm -rf **/__pycache__` before re-running pyright"**
- Imperative (active). No violation.

### R13 (Needless Words) - Moderate

**Line 3 (description): "Debug type errors in uv-managed Python projects by accessing true pyright diagnostics."**
- "true pyright diagnostics" - is "true" needless?
- Severity: Minor
- Analysis: "True" adds semantic value (contrasts with misleading zero-error reports), so not needless.

**Line 80: "Use case: This index guides AST transformation scripts."**
- "Use case:" is prefatory.
- Severity: Minor
- Suggested revision: "This index guides AST transformation scripts." (Remove "Use case:")

**Line 110: "For scattered issues (<10 instances): Manual fixes using the line-indexed report."**
- Fragment structure acceptable in this instructional context.
- No violation.

**Lines 129-131: "Both must pass for proof-of-work."**
- Concise and direct. No violation.

## Moderate

### R11 (Positive Form) - Moderate

**Line 14-15: "can't import project dependencies"**
- Negative construction where positive exists.
- Severity: Moderate
- Suggested revision: "Standalone pyright uses system Python and lacks access to project dependencies (pydantic, etc.) installed in the uv-managed venv."

**Line 22: "❌ WRONG - Uses system Python, misses venv packages"**
- "misses" is negative framing.
- Severity: Minor
- Suggested revision: "❌ WRONG - Uses system Python, ignores venv packages" OR "lacks venv packages"

**Line 28: "type errors that depend on third-party package type stubs"**
- Neutral, not negative. No violation.

**Line 92: "Pyright without pydantic type stubs can't infer"**
- Negative construction.
- Severity: Moderate
- Suggested revision: "Pyright requires pydantic type stubs to infer that `Field(None, ...)` makes parameters optional."

**Line 102: "No parameter named 'from_'"**
- This is a quoted error message, not prose. No violation (quoted material exempt).

**Line 118: "Version mismatch: IDE pyright version may differ from CLI."**
- "may differ" is negative framing.
- Severity: Minor
- Suggested revision: "Version mismatch: IDE pyright version might not match CLI version." (Still negative but clearer) OR "Check IDE and CLI pyright versions match."

### R12 (Concrete Language) - Severe

**Line 10: "hundreds of type errors"**
- "Hundreds" is vague. The example later shows 819 - that's specific.
- Severity: Moderate
- Suggested revision: "IDE shows many type errors (often hundreds), but `pyright file.py` reports 0 errors."

**Line 80: "Know exactly which lines need fixing before writing the transformer."**
- "Exactly which lines" is concrete. No violation.

**Line 106: "Type narrowing fails when pyright can't see discriminator field definitions from imported models."**
- Concrete scenario. No violation.

### R15 (Parallel Construction) - Moderate

**Lines 21-25: Code comment blocks**
```
# ❌ WRONG - Uses system Python, misses venv packages
# ✅ CORRECT - Uses project venv with all dependencies
```
- Both follow pattern: "Uses [X], [verb] [Y]"
- Second should be: "Uses project venv, accesses all dependencies" OR "Uses project venv with all dependencies" (keep prepositional)
- Severity: Minor
- Current form acceptable but could be more parallel.

**Lines 116-118: Common Gotchas list**
```
1. **Cache poisoning:** [explanation]
2. **Version mismatch:** [explanation]  
3. **Python version mismatch:** [explanation]
```
- All follow same pattern. Good parallelism.

**Lines 135-139: Bundled Scripts section**
- "Parse pyright JSON output, categorize errors by pattern, show frequency distribution and top 10 errors with line numbers."
- Series uses mixed verb forms: "Parse" (imperative), "categorize" (imperative), "show" (imperative) - parallel. Good.
- No violation.

### R18 (Emphatic Position) - Moderate

**Line 12: "Without proper imports, pyright falls back to lenient type inference, hiding real errors."**
- Ends with "hiding real errors" - emphatic position emphasizes the problem. Good use.

**Line 28: "revealing type errors that depend on third-party package type stubs."**
- Ends with description of what's revealed, not the action. 
- Severity: Minor
- Suggested revision: "This reveals type errors that depend on third-party package type stubs." (Ends with focus: the stubs)

**Line 80: "Know exactly which lines need fixing before writing the transformer."**
- Ends with "before writing the transformer" - temporal clause in emphatic position.
- Severity: Minor
- Suggested revision: "Before writing the transformer, know exactly which lines need fixing." OR "Know which lines need fixing before you write the transformer." (Clearer emphasis on "know" vs timing)

**Line 131: "Both must pass for proof-of-work."**
- Ends with "for proof-of-work" - purpose in emphatic position.
- Could be: "For proof-of-work, both must pass." (emphasizes passing) OR current form emphasizes purpose.
- Current form acceptable.

## Minor & Stylistic

### Style observations

**Line 6: "# UV-Pyright Debugging Workflow"**
- Clear heading. No issue.

**Line 8: "## The Core Problem"**
- Section structure clear and logical. No issue.

**Lines 21-25: Emoji usage (❌ ✅)**
- Not traditional prose but acceptable in technical documentation for quick visual scanning.
- No violation in this genre.

**Line 28: "Key insight:"**
- Prefatory phrase. Common in instructional writing.
- Severity: Minor
- Could be removed for directness, but adds useful emphasis in this context.

**Line 62: "**Use case:**"**
- See earlier note under R13.

**Lines 87-107: Code examples with comments**
- Clear, concrete examples. Excellent use of specificity (R12).

### Comma usage

**Line 12: "Standalone pyright uses system Python and can't import project dependencies (pydantic, etc.) installed in the uv-managed venv."**
- No comma before "and" because second clause shares subject. Correct per R4.

**Line 28: "Key insight: `uv run` ensures pyright sees the exact Python environment your code runs in, revealing type errors that depend on third-party package type stubs."**
- Comma before "revealing" - participial phrase. Acceptable but creates potential confusion (see active voice note above).

## Summary

**Critical/Severe findings:** 0
**Moderate findings:** 5
- R10 (active voice): 2 instances of improvable constructions
- R11 (positive form): 2 instances of negative constructions where positive alternatives exist
- R18 (emphatic position): 1 instance of suboptimal emphasis

**Minor findings:** 5
- R11: 1 instance (negative where positive clearer)
- R12: 1 instance (vague "hundreds")
- R13: 1 instance ("Use case:" prefatory)
- R15: 1 instance (parallelism could be tighter)
- R18: 2 instances (emphasis placement)

**Overall assessment:** Prose is clear, concrete, and purposeful. Most violations are minor. The document effectively uses specific examples (R12 strength) and maintains active voice in most cases. Primary improvement area: converting negative constructions to positive assertions and tightening participial phrases to maintain active voice clarity.

**Strengths:**
- Excellent use of concrete examples (819 errors, specific file names)
- Clear imperative mood in instructions
- Good paragraph unity and topic sentences
- Code examples well-chosen and specific

**Recommended focus:** Convert 2-3 negative constructions to positive form; tighten 2 participial/dangling constructions to maintain active voice clarity.
