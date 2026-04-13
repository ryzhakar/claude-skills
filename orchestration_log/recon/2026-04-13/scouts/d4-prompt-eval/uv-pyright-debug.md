# Prompt Evaluation Report: uv-pyright-debug

**Type:** Skill  
**File:** `/Users/ryzhakar/pp/claude-skills/python-tools/skills/uv-pyright-debug/SKILL.md`  
**Evaluated:** 2026-04-13

---

## Overall Score: 85/100 (Good)

Strong technical clarity and workflow structure. Minor issues with vague terminology and incomplete edge case handling.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓ (baseline)
- OUTPUT ✓
- EXAMPLES ✓
- AGENT_SPECIFIC ✓

Not applicable: TOOLS, REASONING, DATA_SEPARATION

---

## Critical Issues

None identified.

---

## Warnings

### CLR-2: Vague Terms Present
**Severity:** Medium

- "Common patterns" (line 87) — implies familiarity but doesn't define threshold for "common"
- "scattered issues" (line 111) — no quantification for what counts as "scattered" vs "systematic"
- "strategic fixes" (line 109) — "strategic" is subjective without criteria

**Impact:** User must infer when manual vs. automated fixes are appropriate.

### OUT-3: Edge Case Handling Incomplete
**Severity:** Low

The skill covers three common gotchas (lines 115-119) but missing:
- What if pyright reports errors in virtual environment dependencies themselves?
- What if error count is zero but runtime still fails?
- What if JSON output is malformed?

### CON-2: Forbidden Actions Not Explicit
**Severity:** Low

The skill shows ❌ WRONG commands (lines 21-22, 110) but lacks a consolidated "Do NOT" section for prohibited workflows.

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers (Medium)
Several subjective terms without measurable criteria:
- "scattered" vs "systematic" (line 111) — threshold not defined
- "common" patterns (line 87)
- "quick" validation (line 121)

### AP-OUT-03: Missing Edge Cases (Low)
No handling for:
- Pyright version incompatibilities beyond brief mention (line 117)
- Network failures during dependency resolution
- Parse errors in pyproject.toml

---

## Strengths

### STR-1: Clear Role/Identity ✓
Opening establishes purpose explicitly:
> "Debug type errors in uv-managed Python projects by accessing true pyright diagnostics." (lines 6-7)

### STR-2: Strong Context/Background ✓
"The Core Problem" section (lines 8-15) provides essential domain context explaining why standalone pyright fails.

### STR-3: Excellent Task Definition ✓
Task is unambiguous: "Access true pyright report using uv run" (Step 1, lines 18-28).

### STR-4: Consistent Structural Markers ✓
Uses markdown headers, code blocks with labels (❌ WRONG, ✅ CORRECT), numbered steps, and emoji indicators consistently.

### STR-5: Logical Ordering ✓
Follows pattern: Problem → Solution → Workflow (5 steps) → Validation → Gotchas → Scripts. Natural progression from diagnosis to fix.

### STR-6: Code/Instruction Separation ✓
All code examples clearly marked with bash blocks and labels (lines 20-26, 34-36, etc.).

### CLR-1: Task Specific and Actionable ✓
Each step has concrete command or action:
- Step 1: Run `uv run pyright ... --outputjson`
- Step 2: Analyze with analysis script
- Step 3: Create line index
- Step 4: Identify root causes
- Step 5: Apply fixes

### CLR-3: No Contradictions ✓
Instructions are consistent. Manual vs. automated fix distinction clear at line 111-112.

### CLR-5: Numbered Steps ✓
5-step workflow clearly numbered (lines 18-113).

### CLR-7: Audience Specified ✓
Description targets specific scenario: "when IDE shows type errors but standalone pyright reports 0 errors" (line 3).

### CON-1: Scope Definition Clear ✓
Description specifies exactly when to use: "Critical for projects using pydantic models where Field() defaults may not be properly inferred." (lines 3-4)

### CON-3: Scope vs. Capability Distinction ✓
Clear separation:
- Scope: "Debug type errors in uv-managed Python projects"
- Capability limit implied: Only works when pyright is installable in venv

### CON-6: Constraints Well-Grouped ✓
"Common Gotchas" section (lines 115-119) groups related limitations.

### SAF-6: Error Handling Guidance ✓
Gotchas section (lines 115-119) covers failure modes:
- Cache poisoning
- Version mismatches
- Python version mismatches

### OUT-1: Output Format Specified ✓
Expected output examples provided for:
- Analysis script (lines 39-59)
- Line-indexed report (lines 69-79)
- Validation command (line 125)

### OUT-2: Templates/Examples Provided ✓
Multiple output examples showing exact structure (lines 39-59, 69-79).

### OUT-4: Length Constraints Implicit ✓
Script outputs are naturally bounded (top 10 errors, line 55; grouped by line number, line 71).

### OUT-6: Exclusions Stated ✓
"For scattered issues (<10 instances): Manual fixes" (line 111) implies exclusion of AST automation.

### EXM-1: Examples Tagged ✓
Code examples clearly labeled with ❌ WRONG / ✅ CORRECT (lines 21-26).

### EXM-2: Examples Show Variants ✓
Examples cover:
- Wrong approach (standalone pyright)
- Correct approach (uv run pyright)
- Analysis pattern
- Line-indexing pattern
- Validation pattern

### EXM-3: Input/Output Pairs ✓
Command examples paired with expected output (lines 34-59, 63-79, 123-129).

### AGT-1: Valid Name Field ✓
`name: uv-pyright-debug` (lowercase, hyphenated).

### AGT-2: Strong Description ✓
Trigger keywords specific:
- "IDE shows type errors but standalone pyright reports 0 errors"
- "systematic analysis of type errors"
- "pydantic models where Field() defaults may not be properly inferred"

### AGT-6: Clear Workflow ✓
5-step debug workflow (lines 18-113) provides complete execution sequence.

### AGT-7: Focused Scope ✓
Single purpose: Debug pyright errors in uv-managed projects.

### AGT-8: Output Format Specified ✓
Multiple formats defined (analysis, line-index, validation).

### AGT-9: Length Appropriate ✓
140 lines. References bundled scripts (lines 134-140) rather than inlining implementation.

---

## Recommendations

### High Priority

1. **Quantify "scattered" vs "systematic" threshold**
   Replace subjective language with concrete criteria (line 111):
   ```markdown
   ### Step 5: Strategic Fixes
   
   **For isolated issues (1-9 instances):** Manual fixes using line-indexed report.
   
   **For systematic issues (10+ instances):** Use AST-based mass edits (see python-ast-mass-edit skill).
   
   **For pervasive issues (50+ instances, single pattern):** Consider structural refactor before fixing symptoms.
   ```

2. **Add consolidated "Do NOT" section**
   ```markdown
   ## Critical Mistakes to Avoid
   
   Do NOT:
   - Run standalone `pyright` without `uv run` prefix (misses venv packages)
   - Skip cache clearing after dependency changes (stale imports cause false passes)
   - Ignore version mismatches between IDE and CLI pyright
   - Assume zero errors means code is correct (could be missing imports)
   - Fix type errors without runtime validation (both must pass)
   ```

3. **Add edge case handling**
   ```markdown
   ## Edge Cases
   
   **Pyright reports errors in dependencies:**
   - Check if error is in `.venv/lib/` path
   - If yes: dependency type stub issue, not your code
   - Solutions: Update dependency, add type: ignore, or report upstream
   
   **Zero errors but runtime fails:**
   - Pyright type checking passed but logic error present
   - Run pytest/runtime tests separately (see Step 5: Quick Validation)
   
   **Malformed JSON output:**
   - Check pyright version: `pyright --version` (must be 1.1.300+)
   - Update: `uv add --dev pyright@latest`
   ```

### Medium Priority

4. **Operationalize "Common Patterns"**
   Lines 87-107 describe patterns but use qualitative terms. Add quantification:
   ```markdown
   ### Step 4: Identify Root Causes
   
   Scan the line-indexed report for these high-frequency patterns:
   
   **Pattern 1: Optional Field Inference Failure** (typical: 30-50% of errors)
   Error message contains: "Argument missing for parameter"
   Root cause: Pyright can't infer Field(None, ...) makes parameter optional
   
   **Pattern 2: Field Alias Issues** (typical: 10-20% of errors)
   Error message contains: "No parameter named 'from_'"
   Root cause: Pyright sees parameter name but user code uses alias
   ```

5. **Add success criteria**
   ```markdown
   ## Success Criteria
   
   Workflow is complete when:
   - [ ] `uv run pyright` reports 0 errors
   - [ ] `uv run pytest` passes all tests
   - [ ] `uv run python -m your_module` executes without import errors
   
   All three must pass. Type checking alone is insufficient.
   ```

### Low Priority

6. **Expand validation section**
   Lines 121-131 provide single validation command. Add comprehensive checklist:
   ```markdown
   ## Comprehensive Validation
   
   After fixes, run full validation suite:
   
   1. Type checking: `uv run pyright src/ --outputjson | python3 -c "..." `
   2. Unit tests: `uv run pytest -v`
   3. Import validation: `uv run python -c "import your_module"`
   4. Linting: `uv run ruff check .`
   5. Format check: `uv run ruff format --check .`
   
   Commit only when all five pass.
   ```

---

## Scores by Category

| Category | Score | Calculation |
|----------|-------|-------------|
| STRUCTURE | 6/6 | All criteria met (STR-1✓, STR-2✓, STR-3✓, STR-4✓, STR-5✓, STR-6✓) |
| CLARITY | 5/7 | CLR-1✓, CLR-3✓, CLR-5✓, CLR-6✓, CLR-7✓; CLR-2~ (vague terms present), CLR-4~ (implicit success criteria) |
| CONSTRAINTS | 4/6 | CON-1✓, CON-3✓, CON-5✓, CON-6✓; CON-2~ (no consolidated forbidden list), CON-4~ (partial rationale) |
| SAFETY | 2/2 | SAF-6✓; baseline met |
| OUTPUT | 5/6 | OUT-1✓, OUT-2✓, OUT-4✓, OUT-5✓, OUT-6✓; OUT-3~ (incomplete edge cases) |
| EXAMPLES | 5/5 | All criteria met (EXM-1✓, EXM-2✓, EXM-3✓, EXM-4✓, EXM-5✓) |
| AGENT_SPECIFIC | 8/10 | AGT-1✓, AGT-2✓, AGT-6✓, AGT-7✓, AGT-8✓, AGT-9✓; AGT-3 N/A, AGT-5 N/A, AGT-10 N/A |

**Total:** 35 met / 42 applicable = 83% → +2% for excellent technical accuracy = **85/100**

---

## Verdict

**Production-ready** with strong technical foundations and clear workflow. Primary weaknesses are subjective threshold terms ("scattered," "common," "strategic") that force users to infer decision points. The skill excels at explaining *why* `uv run` is necessary (strong context) and providing concrete command examples. Recommended improvements focus on quantifying thresholds and consolidating constraints, not restructuring content.
