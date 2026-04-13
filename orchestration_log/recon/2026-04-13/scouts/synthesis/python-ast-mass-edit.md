# Synthesis: python-ast-mass-edit

**Baseline:** 1294 tokens

## Core Points (Untouchable)

1. Pre-surveying with a ground-truth index of all transformation targets is mandatory before writing any AST transformation script.
2. AST transformations must be idempotent through guard clauses that prevent already-transformed code from being modified on subsequent runs.
3. The diff review is mandatory and must be performed manually to catch unintended transformations before committing.
4. Transformation scripts are throwaway tools that must be deleted after use and never committed to the repository.
5. AST-based mass edits are only appropriate for structural changes affecting 3+ files, not for simple string replacements or small-scale edits.

## Cut

### C1. Remove "4-Step Execution Protocol" — trim heading word
**Citation:** D3 R13 minor finding: "'Execution' — could be just '4-Step Protocol'."
**Location:** Line 20: "## 4-Step Execution Protocol"
**Action:** Change to "## 4-Step Protocol"
**Saving:** ~2 tokens.

### C2. Remove "This is your ground truth." sentence
**Citation:** D3 R13 minor finding: "'This is your ground truth' — emphatic restatement. Could be omitted."
**Location:** Line 38.
**Action:** Delete the sentence. The preceding line "Line-indexed list of ALL transformation targets" already communicates the concept. The emphasis marker "ALL" (caps) carries the weight. Removing the restatement respects Core Point 1 by keeping the ground-truth concept via the preceding sentence while cutting the redundant echo.
**Saving:** ~7 tokens.

### C3. Trim trailing parenthetical in troubleshooting
**Citation:** D3 R18 moderate finding: "Line 169: Ends with parenthetical examples — weak position."
**Location:** Line 175-176: "AST can't handle all Python syntax (f-strings with complex nesting, etc.). Consider manual edits."
**Action:** Rewrite to "AST fails on some complex Python syntax: nested f-strings and similar edge cases. Use manual edits instead." Moves specifics out of parenthetical into main clause; replaces "can't handle" with "fails on" per D3 R10/R11; replaces "Consider" (hedging, per term-blacklists.md) with direct imperative.
**Saving:** ~2 tokens (shorter construction). Gain: fixes 3 issues in one edit (R10 active voice, R11 positive form, R18 emphatic position).

## Restructure

No structural changes recommended.

**Rationale:** D4 scored this skill at 91% (Excellent). D3 found 0 critical/severe issues. The 4-step protocol ordering (Survey → Transform → Validate → Commit) maps directly to the core points and follows the ordering-guide.md "Agent prompt" pattern (Role → Purpose → Constraints → Workflow → Format → Error handling). The "When to Use" section before the workflow matches ordering-guide.md position 2-3 (Context + Constraints before Task). Reordering would disrupt a structure that already scores optimally.

## Strengthen

### S1. Replace "non-negotiable" with "mandatory" (D3 R11)
**Citation:** D3 R11 moderate finding: "'non-negotiable' is negative form. Suggested revision: 'mandatory' or 'You must review the diff.'"
**Location:** Line 90: "**The diff review is non-negotiable.** AST transformations can have subtle bugs."
**Action:** Rewrite to "**You must review the diff.** AST transformations can have subtle bugs." Direct imperative, active voice, positive form. Preserves bold emphasis marker (intentional, per synthesis directives).
**Saving:** -1 token (slightly shorter). Gain: fixes R11 negative form.

### S2. Replace "can't handle" with active construction (D3 R10)
**Citation:** D3 R10 moderate finding: "AST can't handle all Python syntax — Negative construction."
**Location:** Already addressed in C3 above (combined edit). No separate action needed.

### S3. Tighten the description — front-load trigger within 250 chars
**Citation:** Bridge-research prompt-compression-strategies section 2.5: "descriptions longer than 250 characters are truncated in the skill listing." Current description is ~310 characters.
**Location:** Frontmatter `description` field.
**Action:** Rewrite to: "Systematic workflow for AST-based mass edits in Python codebases. Use when editing 3+ files with structural changes (decorators, function signatures, imports, class definitions). Includes pre-surveying, idempotent transformations, and validation." Drop "NOT for simple string replacements or <5 instances" from description — this exclusion is stated in the body's "When NOT to use" section and costs ~45 characters in the description where space is premium.
**Saving:** ~8 tokens from description context budget. The exclusion criteria remain in the body (lines 15-17) where Claude reads them after invocation.

## Hook/Command Splits

No hook or command split recommended.

**Rationale:** The skill's value is procedural judgment (when to use AST, how to write idempotent transformers, what to validate). None of these steps are deterministic enough for hooks. The validation protocol (Step 3) involves `ruff format`, `git diff`, cache clearing, and `pytest` — these could theoretically become a PostToolUse hook on Write/Edit, but the skill already instructs Claude to run them sequentially. A hook would add configuration complexity without improving compliance, since the validation is already non-optional in the instruction text and Claude 4.6 follows procedural instructions reliably without hook enforcement (per bridge-research prompt-compression-strategies section 1.2: "Claude 4.6 is significantly more proactive").

## Projected Token Delta

| Category | Tokens |
|----------|--------|
| C1: Trim heading | -2 |
| C2: Remove restatement | -7 |
| C3: Rewrite troubleshooting line | -2 |
| S1: "non-negotiable" → "must" | -1 |
| S3: Trim description | -8 (context budget) |
| **Net body change** | **-12 tokens** |
| **Net description change** | **-8 tokens (startup context)** |

**Projected revised total:** ~1282 body tokens + shorter description. Minimal compression consistent with D4 score of 91% (Excellent) and D3 finding of 0 critical/severe issues. This skill is already near-optimal; the edits are surgical fixes to specific D3 findings, not structural rework. The primary value of synthesis here is confirming the skill needs almost no changes — a finding that itself saves implementation effort.
