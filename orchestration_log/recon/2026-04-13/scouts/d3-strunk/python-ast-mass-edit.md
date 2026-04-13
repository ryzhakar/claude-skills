# Strunk Analysis: python-ast-mass-edit

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 5: "NOT for simple string replacements or <5 instances."**
- Negative prohibition (acceptable in negative constraints).
- No violation - this is proper use of negative for denial/constraint.

**Line 12: "Test question: Can you say 'find all functions with X and change to Y'? If yes, use AST."**
- Active imperative. No violation.

**Line 16: "Manual edits faster than script setup"**
- Elliptical construction (verb omitted). Acceptable in bulleted list context.
- No violation in this genre.

**Line 38: "This is your ground truth."**
- Active declarative. No violation.

**Line 63: "new_source = ast.unparse(new_tree)  # 4. UNPARSE: Always use ast.unparse()"**
- Imperative comment. Active. No violation.

**Line 90: "The diff review is non-negotiable."**
- Passive construction: "review is non-negotiable."
- Severity: Moderate
- Suggested revision: "You must review the diff." OR "Never skip the diff review."

**Line 149: "Transformation didn't catch all instances"**
- Negative construction but in quoted troubleshooting context (diagnostic message).
- No violation - quoting a problem statement.

**Line 169: "AST can't handle all Python syntax"**
- Negative construction.
- Severity: Moderate
- Suggested revision: "AST fails on some complex Python syntax (f-strings with complex nesting, etc.)."

### R12 (Concrete Language) - Severe

**Line 10: "Trigger condition: Editing **3+ files** with **structural changes**"**
- Concrete number (3+), concrete category (structural). Good.
- No violation.

**Line 16: "< 5 instances total"**
- Specific threshold. Concrete.
- No violation.

**Line 23: "Build line-number-with-structured-annotations index BEFORE writing transformer"**
- Concrete deliverable. No violation.

**Line 107: "git commit -m 'refactor: rename 'arg' → 'column' in WindowExpr/AggregateExpr"**
- Specific file names, specific parameter names. Excellent concreteness.
- No violation.

**Line 154: "Stale cache. Run `rm -rf **/__pycache__` and test again."**
- Concrete command. No violation.

### R13 (Needless Words) - Moderate

**Line 3 (description): "Systematic workflow for AST-based mass edits in Python codebases."**
- "Systematic workflow" - is "systematic" needless?
- Analysis: Adds semantic value (distinguishes from ad-hoc approach). Not needless.

**Line 5: "NOT for simple string replacements or <5 instances."**
- Could be tighter: "Avoid for simple string replacements or <5 instances."
- Severity: Minor
- Current form emphatic, which serves purpose.

**Line 20: "## 4-Step Execution Protocol"**
- "Execution" - could be just "4-Step Protocol"
- Severity: Minor
- Suggested revision: "## 4-Step Protocol"

**Line 38: "**Output:** Line-indexed list of ALL transformation targets. This is your ground truth."**
- "This is your ground truth" - emphatic restatement.
- Severity: Minor
- Analysis: Second sentence adds emphasis but could be omitted. Acceptable for emphasis.

**Line 110: "Never commit:"**
- Terse imperative. Good economy.
- No violation.

## Moderate

### R11 (Positive Form) - Moderate

**Line 5: "NOT for simple string replacements or <5 instances."**
- Negative prohibition. In this context (defining scope), negative is appropriate.
- No violation (proper use of negative for denial).

**Line 12: "When NOT to use:"**
- Negative heading for exclusion criteria.
- Severity: Minor
- Suggested revision: "Use only when:" (then list positive criteria) OR keep negative for clarity about exclusions.
- Current form acceptable - clearly signals constraint.

**Line 51: "# 1. IDEMPOTENCY: Guard clause to only transform what needs changing"**
- "only transform what needs changing" contains "only" limiting word but is positive assertion.
- No violation.

**Line 86: "# If ANY step fails: git checkout . and fix the script"**
- Negative conditional (failure). Appropriate for error handling.
- No violation.

**Line 90: "The diff review is non-negotiable."**
- "non-negotiable" is negative form.
- Severity: Moderate
- Suggested revision: "The diff review is mandatory." OR "You must review the diff."

**Line 110: "Never commit:"**
- Strong negative prohibition.
- Severity: Minor
- Analysis: In prohibitions/constraints, negative is often stronger and clearer. "Never" is forceful (see Strunk note on "never," "nothing," "no" being strong).
- Acceptable use.

**Line 149: "Transformation didn't catch all instances"**
- Negative problem statement (quoted troubleshooting scenario).
- No violation - describing error condition.

**Line 169: "AST can't handle all Python syntax"**
- Negative capability statement.
- Severity: Moderate
- Suggested revision: "AST fails on some complex Python syntax"

### R15 (Parallel Construction) - Moderate

**Lines 15-17: "When NOT to use" list**
```
- String content changes (comments, docstrings, literals) → Use manual edits or sed
- < 5 instances total → Manual edits faster than script setup
- Complex logic requiring semantic understanding → Manual review safer
```
- Pattern: [Condition] → [Recommendation]
- First two follow pattern. Third follows pattern.
- All parallel. Good.
- No violation.

**Lines 46-49: Critical requirements list in code comment**
```
# 1. IDEMPOTENCY: Guard clause to only transform what needs changing
# 2. VISIBILITY: Print all changes
# 3. TRAVERSAL: Always call generic_visit
# 4. UNPARSE: Always use ast.unparse()
```
- Pattern: [NUMBER]. [PRINCIPLE]: [Description]
- All parallel. Excellent.
- No violation.

**Lines 75-85: Validation steps**
```
# 1. Format (AST unparse output needs formatting)
# 2. Review diff (catch unintended transformations)
# 3. Clear caches (stale imports cause false test passes)
# 4. Run tests
```
- Pattern: [NUMBER]. [Action] ([reason])
- All parallel. Good.
- No violation.

**Lines 110-113: "Never commit" list**
```
- The transformation script itself
- Partial transformations (all-or-nothing)
- Code that doesn't pass tests
```
- First: noun phrase (the script)
- Second: noun phrase with parenthetical (transformations)
- Third: noun phrase with relative clause (code that...)
- All noun phrases. Parallel structure maintained.
- No violation.

### R18 (Emphatic Position) - Moderate

**Line 12: "Test question: Can you say 'find all functions with X and change to Y'? If yes, use AST."**
- Ends with "use AST" - the key action in emphatic position. Good.
- No violation.

**Line 20: "## 4-Step Execution Protocol"**
- Title, not sentence. N/A.

**Line 38: "This is your ground truth."**
- Ends with "ground truth" - emphatic emphasis. Good.
- No violation.

**Line 63: "file.write_text(new_source)  # 4. UNPARSE: Always use ast.unparse()"**
- Code line with comment. Comment ends with function name.
- Not prose sentence. N/A.

**Line 90: "AST transformations can have subtle bugs."**
- Ends with "subtle bugs" - the risk in emphatic position. Good.
- No violation.

**Line 154: "Run `rm -rf **/__pycache__` and test again."**
- Ends with "test again" - the action.
- Severity: Minor
- Could be: "Clear caches (`rm -rf **/__pycache__`) and rerun tests." (Ends with more specific action)
- Current form acceptable.

**Line 169: "AST can't handle all Python syntax (f-strings with complex nesting, etc.)."**
- Ends with parenthetical examples - weak position.
- Severity: Moderate
- Suggested revision: "AST fails on some complex Python syntax: f-strings with complex nesting and similar edge cases." (Ends with "edge cases" - the category)

**Line 176: "Consider manual edits."**
- Ends with "manual edits" - the recommendation. Good.
- No violation.

### R12 (Concrete Language) - Moderate instances

**Line 23: "Build line-number-with-structured-annotations index"**
- "line-number-with-structured-annotations" is specific.
- No violation.

**Line 107: "- Transformed 20 function calls across 4 files"**
- Specific numbers. Excellent concreteness.
- No violation.

## Minor & Stylistic

### Style observations

**Line 1-4: Frontmatter description**
- Long single sentence with multiple clauses.
- Clarity acceptable but could be split.
- Severity: Minor
- No structural violation.

**Line 6: "# AST-Based Mass Edit Protocol"**
- Clear title. No issue.

**Lines 46-64: Code block with inline comments**
- Excellent use of concrete examples.
- Comments use imperative and declarative clearly.
- No violations.

**Line 86: "# If ANY step fails: git checkout . and fix the script"**
- ALL CAPS for emphasis. Acceptable in comments/asides.

**Line 110: "Never commit:"**
- Colon introduces list. Standard.
- No violation.

### Comma usage

**Line 12: "If yes, use AST."**
- Comma after conditional clause. Correct per R3/R4.

**Line 90: "The diff review is non-negotiable."**
- No comma issues.

**Line 149: "Check your survey."**
- Imperative. No comma needed.

## Summary

**Critical/Severe findings:** 0
**Moderate findings:** 4
- R10 (active voice): 2 instances (passive constructions)
- R11 (positive form): 2 instances (negative where positive clearer)

**Minor findings:** 5
- R11: 1 instance ("non-negotiable" vs "mandatory")
- R13: 2 instances (potentially needless words)
- R18: 2 instances (emphasis placement)

**Overall assessment:** Prose is exceptionally clear, concrete, and well-structured. Strong use of parallel construction in lists. Excellent use of specific numbers and examples. Most violations are minor and several negative constructions are justified (strong prohibitions where "never" carries appropriate force per Strunk's note on strong negatives).

**Strengths:**
- Outstanding parallel construction in all list structures
- Excellent concrete specificity (numbers, file names, parameter names)
- Clear imperative mood throughout
- Code examples well-integrated with prose explanations
- Strong organizational structure (numbered steps)

**Weaknesses:**
- 2 passive constructions could be active
- 2 negative constructions could be positive (though severity is low)
- Minor emphasis placement issues in 2 sentences

**Recommended focus:** Convert "The diff review is non-negotiable" to "You must review the diff"; rephrase "AST can't handle" to "AST fails on"; consider moving parenthetical to stronger position in line 169.
