# Core Points: python-ast-mass-edit

## Iteration 1

**Point**: Pre-surveying with a ground-truth index of all transformation targets is mandatory before writing any AST transformation script.

**Evidence**:
- Line 23: "Build line-number-with-structured-annotations index BEFORE writing transformer"
- Line 39: "Output: Line-indexed list of ALL transformation targets. This is your ground truth."
- Line 166: "Transformation didn't catch all instances → Check your survey. Did you miss a variant pattern? Re-run Step 1."

## Iteration 2

**Point**: AST transformations must be idempotent through guard clauses that prevent already-transformed code from being modified on subsequent runs.

**Evidence**:
- Line 51: "1. IDEMPOTENCY: Guard clause to only transform what needs changing"
- Line 147-161: Entire "Idempotency Patterns" section with Problem/Solution and BAD vs GOOD examples
- Line 154-160: Shows concrete guard clause pattern checking "if 1 <= old_val <= 7" to prevent double-transformation

## Iteration 3

**Point**: The diff review step is non-negotiable and must be performed manually to catch unintended transformations before committing.

**Evidence**:
- Line 78: "2. Review diff (catch unintended transformations)"
- Line 90: "The diff review is non-negotiable. AST transformations can have subtle bugs."
- Line 171: "Git diff shows unrelated changes → ruff format changed other code. Review diff carefully before committing."

## Iteration 4

**Point**: Transformation scripts are throwaway tools that must be deleted after use and never committed to the repository.

**Evidence**:
- Line 42: "Write one-time-use fix_X.py in project root"
- Line 95: "Delete the throwaway script"
- Line 110-112: "Never commit: The transformation script itself"

## Iteration 5

**Point**: AST-based mass edits are only appropriate for structural changes affecting 3+ files, not for simple string replacements or small-scale edits.

**Evidence**:
- Line 10: "Trigger condition: Editing 3+ files with structural changes (decorators, function signatures, imports, class definitions)"
- Line 14-17: Three explicit "When NOT to use" cases including "< 5 instances total → Manual edits faster than script setup"
- Line 3 (description): "Use when editing 3+ files with structural changes... NOT for simple string replacements or <5 instances"

## Rank Summary

1. **Pre-survey ground truth** - The foundation that enables all other steps; emphasized as occurring "BEFORE" transformation and referenced in troubleshooting
2. **Idempotency** - First principle listed in critical requirements section; dedicated subsection with anti-patterns
3. **Non-negotiable diff review** - Explicitly called "non-negotiable"; safety checkpoint before permanent changes
4. **Throwaway scripts** - Architectural decision affecting workflow hygiene; emphasized in both Step 2 and Step 4
5. **Structural-only scope** - Gatekeeper decision determining whether to use the entire protocol; stated in trigger conditions and description
