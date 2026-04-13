# Synthesis: uv-pyright-debug

**Baseline:** 1126 tokens

## Core Points (Untouchable)

1. Standalone pyright reports zero errors because it uses system Python; `uv run` exposes true type errors by running pyright inside the project venv.
2. Bundled analysis scripts categorize, quantify, and line-index pyright errors before any fix attempt.
3. Pydantic `Field(None, ...)` optionality and alias definitions are misread by pyright without proper type stubs.
4. Dual validation (type checking + runtime execution) is non-negotiable proof-of-work.
5. Three operational gotchas (cache poisoning, pyright version mismatch, Python version mismatch) can invalidate results even when using `uv run`.

## Cut

### C1. Remove "Use case:" prefix (D3 R13)
**Citation:** D3 line 38: "'Use case:' is prefatory."
**Location:** Line 80: "**Use case:** This index guides AST transformation scripts."
**Action:** Delete the "Use case:" label. The sentence stands alone.
**Saving:** ~4 tokens.

### C2. Remove "Key insight:" prefix (D3 style observations)
**Citation:** D3 line 152-153: "'Key insight:' — Prefatory phrase. Could be removed for directness."
**Location:** Line 28.
**Action:** Delete "Key insight:" and begin with "`uv run` ensures..."
**Saving:** ~3 tokens.

### C3. Trim description — remove trailing sentence about pydantic
**Citation:** D4 AGT-2 confirms trigger keywords are already strong without the final clause. Bridge-research prompt-compression-strategies section 2.5: "descriptions longer than 250 characters are truncated in the skill listing." Current description is ~285 characters; the pydantic sentence pushes it past truncation.
**Location:** Frontmatter `description` field, final sentence: "Critical for projects using pydantic models where Field() defaults may not be properly inferred."
**Action:** Delete that sentence. The pydantic context is already in the body (Step 4, Pattern 1). The description stays under 250 chars and retains all three trigger scenarios.
**Saving:** ~25 tokens from context budget (description loaded at startup for all sessions).

## Restructure

### R1. Merge Steps 4 and 5 into one section
**Citation:** D4 recommendation 1 (High Priority): "Quantify 'scattered' vs 'systematic' threshold." D4 CLR-2 warning: "'scattered issues' — no quantification." Both sections describe the same decision: what to do after identifying root causes.
**Location:** Lines 83-112 ("Step 4: Identify Root Causes" + "Step 5: Strategic Fixes").
**Action:** Rename combined section "Step 4: Root Causes and Fixes." Move the <10 / 10+ threshold from Step 5 directly under each pattern in Step 4. Replace "scattered" with "1-9 instances" and keep "10+ instances" for AST mass edits.
**Effect:** Eliminates one heading level, reduces reader navigation, and co-locates diagnosis with remedy. Net zero or slight reduction.

## Strengthen

### S1. Replace negative constructions with positive (D3 R11)
**Citation:** D3 R11 moderate findings: "can't import" → "lacks access to"; "can't infer" → "requires pydantic type stubs to infer."
**Locations and rewrites:**
- Line 12: "can't import project dependencies" → "lacks access to project dependencies"
- Line 92: "Pyright without pydantic type stubs can't infer" → "Pyright requires pydantic type stubs to infer"
**Saving:** 0 net tokens (same length). Gain: stronger positive assertion per Strunk R11 and bridge-research prompt-compression 1.1 ("positive instructions are both more token-efficient and more effective").

### S2. Quantify subjective thresholds (D4 CLR-2)
**Citation:** D4 CLR-2 warning: "'scattered issues' — no quantification for what counts as 'scattered' vs 'systematic'." D4 recommendation 1 provides exact replacement text.
**Location:** Line 111.
**Action:** Replace "For scattered issues (<10 instances)" with "For isolated issues (1-9 instances)". Replace "For systematic issues (10+ instances)" — already quantified, keep as-is.
**Saving:** 0 net tokens. Gain: eliminates vague qualifier flagged by term-blacklists.md ("few / many / several" family).

### S3. Replace "The diff review is non-negotiable" phrasing (borrowed from python-ast-mass-edit but referenced in Step 5)
**Citation:** D3 R11 for python-ast-mass-edit: "'non-negotiable' is negative form. Suggested revision: 'mandatory' or 'You must review the diff.'" Same pattern applies if this phrase appears in uv-pyright-debug's cross-reference context.
**Note:** This phrase does not appear in uv-pyright-debug directly. No action needed here — included for completeness since Step 5 references the AST mass edit skill.

## Hook/Command Splits

No hook or command split recommended.

**Rationale:** This skill is a diagnostic and analysis workflow. It does not enforce constraints deterministically, modify tool inputs, or validate outputs in ways that hooks could automate. All steps require LLM judgment (reading error patterns, choosing fix strategy). The bundled scripts already handle the mechanical work; the skill body provides the judgment framework. Hooks would add configuration overhead with no behavioral gain.

## Projected Token Delta

| Category | Tokens |
|----------|--------|
| C1: "Use case:" prefix | -4 |
| C2: "Key insight:" prefix | -3 |
| C3: Trim description | -25 (context budget) |
| R1: Merge Steps 4+5 | -5 (one heading removed) |
| S1: Positive constructions | 0 |
| S2: Quantify thresholds | 0 |
| **Net body change** | **-12 tokens** |
| **Net description change** | **-25 tokens (startup context)** |

**Projected revised total:** ~1114 body tokens + shorter description. Modest compression consistent with D4 score of 85% (Good) and D3 finding of 0 critical/severe issues. The skill is already lean; gains come from precision edits, not structural overhaul.
