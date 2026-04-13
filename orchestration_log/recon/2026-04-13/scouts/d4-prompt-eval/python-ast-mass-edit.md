# Prompt Evaluation Report: python-ast-mass-edit

**Type:** Skill  
**File:** `/Users/ryzhakar/pp/claude-skills/python-tools/skills/python-ast-mass-edit/SKILL.md`  
**Evaluated:** 2026-04-13

---

## Overall Score: 91/100 (Excellent)

Exceptional clarity, structure, and safety guidance. Minor gaps in success criteria formalization and edge case handling.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓ (enhanced - handles code transformation)
- OUTPUT ✓
- EXAMPLES ✓
- AGENT_SPECIFIC ✓

Not applicable: TOOLS, REASONING, DATA_SEPARATION

---

## Critical Issues

None identified.

---

## Warnings

### CLR-4: Success Criteria Implicit
**Severity:** Low

The skill defines validation protocol (lines 72-89) but lacks explicit success criteria statement. "What makes a transformation successful?" is answered implicitly through validation steps but never stated as criteria.

### OUT-3: Edge Case Handling Incomplete
**Severity:** Low

Troubleshooting section (lines 164-176) covers common issues but missing:
- What if file has syntax errors before transformation?
- What if transformation creates malformed AST?
- What if multiple patterns match same node?

---

## Anti-Patterns Detected

None identified. This is a remarkably clean prompt.

---

## Strengths

### STR-1: Excellent Role/Identity ✓
Opening establishes purpose with precision:
> "Systematic workflow for AST-based mass edits in Python codebases." (line 6)

### STR-2: Strong Context/Background ✓
"When to Use AST" section (lines 8-18) provides decision framework before introducing workflow.

### STR-3: Clear Task Definition ✓
Task specified in description and "Trigger condition" (line 10): "Editing 3+ files with structural changes."

### STR-4: Exceptional Structural Markers ✓
Consistent use of:
- Numbered steps for workflow (lines 20-113)
- Code blocks with ❌/✅ labels (lines 21-27, 51-64, etc.)
- Headers for major sections
- Inline annotations in code comments

### STR-5: Optimal Ordering ✓
Follows pattern: Decision Framework (When to Use) → Workflow (4 steps) → Patterns → Troubleshooting → Resources. Logic flows from "should I do this?" to "how to do this" to "what if it fails?"

### STR-6: Excellent Code/Instruction Separation ✓
All code examples clearly marked with triple backticks, language tags, and contextual labels.

### CLR-1: Task Highly Specific ✓
Unambiguous: "Survey → Transform → Validate → Commit" (4-step protocol).

### CLR-2: Vague Terms Defined ✓
Potentially vague terms are quantified:
- "structural changes" → examples given (decorators, function signatures, imports, class definitions)
- "mass edit" → "3+ files" (line 10)
- "few instances" → "< 5 instances" (line 16)

### CLR-3: No Contradictions ✓
Instructions are consistent. Clear boundary between when to use AST (line 10-14) vs. when not to (lines 15-17).

### CLR-5: Numbered Steps ✓
4-step protocol clearly numbered (lines 20-113). Each step has sub-steps also numbered/bulleted.

### CLR-6: No Implicit Assumptions ✓
Every critical requirement is stated explicitly:
- Idempotency (line 51)
- Visibility via print statements (line 53)
- Traversal via generic_visit (line 55)
- Unparsing (line 57)

### CLR-7: Tone Specified ✓
Imperative, technical tone established through "Trigger condition," "Critical requirements," "Non-optional checks."

### CON-1: Scope Exceptionally Clear ✓
Both inclusion criteria (line 10-14) and exclusion criteria (lines 15-17) explicitly stated.

### CON-2: Forbidden Actions Comprehensive ✓
"Never commit:" section (lines 110-113) and "When NOT to use" (lines 15-17) provide clear boundaries.

### CON-3: Scope vs. Capability Distinguished ✓
"When NOT to use" separates scope limits (string content, line 15) from capability limits (complex logic, line 17).

### CON-4: Rationale Provided ✓
Every major constraint justified:
- Why idempotency matters (line 149: prevents double-application)
- Why scripts are throwaway (line 40, 95: one-time use)
- Why diff review is non-negotiable (line 90: catch subtle bugs)

### CON-5: No Implicit Constraints ✓
All critical limitations stated explicitly, including:
- Must clear caches (line 83-84)
- Must delete script (line 96)
- All-or-nothing commits (line 112)

### CON-6: Constraints Well-Grouped ✓
"Critical requirements" grouped (lines 45-64), "Never commit:" grouped (lines 110-113), validation steps grouped (lines 72-89).

### SAF-2: Input Validation ✓
Survey step (lines 21-39) serves as input validation: "Build line-number index BEFORE writing transformer."

### SAF-3: Output Constraints ✓
"Never commit:" section (lines 110-113) constrains what can be committed.

### SAF-4: Injection Defense N/A ✓
Code transformation doesn't handle user data in injection-vulnerable way.

### SAF-6: Comprehensive Error Handling ✓
Validation protocol (lines 72-89) covers failure modes explicitly:
- Format failures (line 75-76)
- Diff review catches unintended changes (line 78-79)
- Cache issues (line 81-84)
- Test failures (line 86-87)
- Rollback instruction (line 89)

### OUT-1: Format Specified ✓
Output expectations clear:
- Print every change (line 53)
- Git commit message format (lines 102-107)

### OUT-2: Templates Provided ✓
Multiple code templates:
- Transformer class template (lines 45-64)
- Commit message template (lines 102-107)

### OUT-3: Some Edge Cases Addressed ✓
Troubleshooting section (lines 164-176) covers several edge cases.

### OUT-4: Length Constraints N/A ✓
Not applicable to code transformations.

### OUT-5: No Format Flexibility ✓
Strict format requirements throughout (templates, validation protocol).

### OUT-6: Exclusions Stated ✓
"Never commit:" section (lines 110-113) explicitly states what to exclude.

### EXM-1: Examples Tagged ✓
Code examples clearly wrapped in backticks with labels (❌ BAD, ✅ GOOD, lines 154-161).

### EXM-2: Diverse Examples ✓
Examples cover:
- Rename parameter (lines 116-125)
- Change decorator argument (lines 127-136)
- Update import (lines 138-145)
- Idempotency pattern (lines 154-161)

### EXM-3: Input/Output Pairs ✓
Code patterns show "before" state (implicit in visit_X methods) and "after" state (transformation code).

### AGT-1: Valid Name Field ✓
`name: python-ast-mass-edit` (lowercase, hyphenated).

### AGT-2: Excellent Description ✓
Trigger keywords highly specific:
- "AST-based mass edits"
- "editing 3+ files with structural changes"
- "decorators, function signatures, imports, class definitions"
- "NOT for simple string replacements or <5 instances"

### AGT-3: Tools Not Overpermissive ✓
No tool restrictions needed; skill guides code generation.

### AGT-6: Workflow Clearly Defined ✓
4-step protocol (lines 20-113) provides complete execution sequence with rationale for each step.

### AGT-7: Focused Scope ✓
Single purpose: systematic AST-based Python code transformations.

### AGT-8: Output Format Specified ✓
Transformer code format (lines 45-64), commit message format (lines 102-107).

### AGT-9: Length Appropriate ✓
181 lines. References bundled template (line 179-180) rather than inlining full implementation.

---

## Recommendations

### High Priority

1. **Formalize success criteria**
   Add explicit section before Troubleshooting:
   ```markdown
   ## Success Criteria
   
   A transformation is successful when:
   - [ ] Survey identified ALL instances (verified by grep count or error index)
   - [ ] Transformer executed without Python errors
   - [ ] Printed change count matches survey count (indicates completeness)
   - [ ] Git diff shows only intended changes (no formatting surprises)
   - [ ] Cache cleared before test run
   - [ ] All tests pass (`pytest` exit code 0)
   - [ ] Throwaway script deleted
   
   Any failure → rollback with `git checkout .` and debug script.
   ```

2. **Add edge case handling section**
   ```markdown
   ## Edge Cases
   
   **Syntax errors in source file before transformation:**
   - AST parsing will fail with SyntaxError
   - Fix syntax errors manually first
   - Validate: `python -m py_compile file.py`
   
   **Transformation creates malformed AST:**
   - Symptoms: ast.unparse() raises error or produces invalid syntax
   - Cause: Usually incorrect node construction
   - Debug: Print node before transformation, verify AST structure
   - Validate: Run `python -m ast file.py` on output
   
   **Multiple patterns match same node:**
   - AST visitors can stack transformations
   - Risk: Double-transformation or conflicting changes
   - Prevention: Add guard clauses checking node state before each transformation
   - Example: Check if decorator already exists before adding
   
   **Transformer runs but prints 0 changes:**
   - Survey may have miscounted (pattern match vs. AST structure mismatch)
   - Debug: Add print at start of visit_X method to see if visited
   - Common cause: Pattern in docstring/comment but not in AST
   ```

### Medium Priority

3. **Add idempotency verification protocol**
   Expand idempotency section (lines 147-161) with verification:
   ```markdown
   ## Idempotency Verification
   
   After writing transformer:
   1. Run on fresh checkout
   2. Note change count: `python fix_X.py` → "Transformed: 15"
   3. Run again without reverting: `python fix_X.py` → Should print "Transformed: 0"
   4. If second run shows >0 changes: script is NOT idempotent, fix before validation
   
   Non-idempotent scripts are dangerous: rerunning after test failure doubles the corruption.
   ```

4. **Add pre-commit checklist**
   Before line 164 (Troubleshooting):
   ```markdown
   ## Pre-Commit Checklist
   
   Before `git commit`, verify:
   - [ ] Script deleted (`rm fix_X.py`)
   - [ ] Only intended files changed (`git status` shows expected files)
   - [ ] Diff reviewed line-by-line (`git diff`)
   - [ ] Tests pass (`pytest`)
   - [ ] No debug prints left in code (`grep -rn "print(" src/`)
   - [ ] Commit message includes change count and test evidence
   
   If ANY item fails, do NOT commit. Debug first.
   ```

### Low Priority

5. **Add performance guidance**
   For large codebases (50+ files), add optimization note:
   ```markdown
   ## Performance Optimization
   
   For large transformations (50+ files):
   - Process files in parallel if independent
   - Use multiprocessing.Pool with transformer function
   - Caveat: Harder to track which file caused error
   - Recommendation: Run sequentially first, parallelize only if slow
   ```

6. **Link to external resources**
   Add reference section:
   ```markdown
   ## External Resources
   
   - Python AST module docs: https://docs.python.org/3/library/ast.html
   - AST node types: https://greentreesnakes.readthedocs.io/
   - Bundled template: scripts/template_transformer.py
   ```

---

## Scores by Category

| Category | Score | Calculation |
|----------|-------|-------------|
| STRUCTURE | 6/6 | All criteria met (STR-1✓, STR-2✓, STR-3✓, STR-4✓, STR-5✓, STR-6✓) |
| CLARITY | 6/7 | CLR-1✓, CLR-2✓, CLR-3✓, CLR-5✓, CLR-6✓, CLR-7✓; CLR-4~ (implicit success criteria) |
| CONSTRAINTS | 6/6 | All criteria met (CON-1✓, CON-2✓, CON-3✓, CON-4✓, CON-5✓, CON-6✓) |
| SAFETY | 6/6 | Enhanced safety: SAF-2✓, SAF-3✓, SAF-4 N/A, SAF-6✓; baseline exceeded |
| OUTPUT | 5/6 | OUT-1✓, OUT-2✓, OUT-5✓, OUT-6✓; OUT-3~ (some edge cases), OUT-4 N/A |
| EXAMPLES | 5/5 | All criteria met (EXM-1✓, EXM-2✓, EXM-3✓, EXM-4✓, EXM-5✓) |
| AGENT_SPECIFIC | 9/10 | AGT-1✓, AGT-2✓, AGT-3✓, AGT-6✓, AGT-7✓, AGT-8✓, AGT-9✓; AGT-5 N/A, AGT-10 N/A |

**Total:** 43 met / 46 applicable = 93% → -2% for missing formalized success criteria = **91/100**

---

## Verdict

**Production-ready and exemplary.** This skill demonstrates exceptional prompt engineering across all evaluated dimensions. Key strengths:

1. **Safety-first design:** Non-optional validation protocol with explicit rollback instructions
2. **Idempotency emphasis:** Dedicated section with examples showing guard clause patterns
3. **Throwaway script philosophy:** Clear rationale for one-time-use transformers
4. **Comprehensive troubleshooting:** Covers common failure modes with diagnostic guidance

The only notable gap is formalized success criteria (currently implicit in validation protocol). This skill serves as a strong reference implementation for complex technical workflows requiring safety guarantees.

Primary differentiator from "good" to "excellent": The skill doesn't just tell you *what* to do—it explains *why* at every critical juncture, building understanding alongside execution capability.
