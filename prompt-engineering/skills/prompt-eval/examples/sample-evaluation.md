# Sample Evaluation Report

Example evaluation of a problematic system prompt demonstrating the evaluation workflow.

---

## Prompt Being Evaluated

```
You are a helpful assistant. Analyze customer feedback and provide insights.
Be thorough but concise. Use good judgment when categorizing issues.

Here's some feedback to analyze:
"The product is great but shipping was slow."

Summarize the key themes.
```

---

# Prompt Evaluation Report

## Summary
- **Score**: 35% (Poor)
- **Prompt Type**: API prompt
- **Categories Evaluated**: STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT, DATA_SEPARATION

## Critical Issues (MUST Fix)

### 1. Vague Task Definition
- **Criterion**: CLR-1 (Task definition is specific and actionable)
- **Location**: Line 1-2
- **Issue**: "Analyze customer feedback and provide insights" is not specific. What kind of analysis? What insights? How should they be structured?
- **Impact**: Claude will make assumptions about analysis scope, depth, and format, leading to inconsistent outputs.

### 2. Contradictory Instructions
- **Criterion**: CLR-3 (No contradictory instructions)
- **Location**: Line 2
- **Issue**: "Be thorough but concise" is a direct contradiction without resolution criteria.
- **Impact**: Claude must choose one, may choose differently each time.

### 3. Undefined Vague Terms
- **Criterion**: CLR-2 (No undefined vague terms)
- **Location**: Line 2
- **Issue**: "good judgment" is undefined. What criteria define good judgment here?
- **Impact**: Unpredictable categorization behavior.

### 4. No Scope Definition
- **Criterion**: CON-1 (Has explicit scope definition)
- **Location**: Entire prompt
- **Issue**: No boundaries on what the assistant should or shouldn't do.
- **Impact**: May overreach or underperform without clear boundaries.

### 5. Data Mixed with Instructions
- **Criterion**: DAT-2 (Instructions not mixed with data without boundaries)
- **Location**: Lines 4-5
- **Issue**: Feedback data appears inline without XML tags or clear boundaries.
- **Impact**: Data could be misinterpreted; injection vulnerability if data is user-provided.

## Warnings (SHOULD Fix)

### 1. Missing Output Format
- **Criterion**: OUT-1 (Specifies output format explicitly)
- **Location**: Line 7
- **Issue**: "Summarize the key themes" doesn't specify format (bullets? paragraphs? structured XML?).
- **Recommendation**: Add explicit format specification.

### 2. No Role Specificity
- **Criterion**: STR-1 (Has explicit role/identity)
- **Location**: Line 1
- **Issue**: "helpful assistant" is generic. A specific role (e.g., "customer insights analyst") would improve focus.
- **Recommendation**: Define specific expertise and perspective.

### 3. No Examples
- **Criterion**: EXM-5 (3-5 examples for complex tasks)
- **Location**: N/A
- **Issue**: Categorization task would benefit from examples showing expected output.
- **Recommendation**: Add 3-5 diverse examples.

### 4. No Uncertainty Handling
- **Criterion**: RSN-3 (Provides an "out" for uncertainty)
- **Location**: N/A
- **Issue**: No guidance for ambiguous feedback.
- **Recommendation**: Add "if categorization is unclear, note the ambiguity."

## Anti-Patterns Detected

- **AP-CLR-01** (Vague Task Definition): "provide insights" - Lines 1-2
- **AP-CLR-02** (Undefined Qualifiers): "good judgment" - Line 2
- **AP-CLR-03** (Contradictory Directives): "thorough but concise" - Line 2
- **AP-CON-01** (Implicit Scope): No scope boundaries - Entire prompt
- **AP-STR-02** (Instruction-Data Mixing): Inline feedback - Lines 4-5
- **AP-OUT-01** (Undefined Format): No format spec - Line 7

## Strengths

- Has a basic role statement (though generic)
- Clear that feedback analysis is the task
- Short prompt (efficient if issues fixed)

## Recommendations (Priority Order)

1. **Fix contradictions**: Replace "thorough but concise" with specific guidance (e.g., "analyze each theme in 2-3 sentences")
2. **Define scope**: Add explicit "You analyze / You do NOT" boundaries
3. **Separate data**: Wrap feedback in `<feedback>` tags
4. **Specify format**: Add output structure (XML, bullets, etc.)
5. **Add examples**: Include 3 categorization examples
6. **Define judgment criteria**: Replace "good judgment" with specific rules

## Detailed Scores by Category

| Category | Applicable | Passed | Score |
|----------|------------|--------|-------|
| STRUCTURE | Yes | 2/6 | 33% |
| CLARITY | Yes | 1/7 | 14% |
| CONSTRAINTS | Yes | 1/6 | 17% |
| SAFETY | Yes | 4/6 | 67% |
| OUTPUT | Yes | 1/6 | 17% |
| DATA_SEPARATION | Yes | 1/4 | 25% |
| **OVERALL** | | | **35%** |

---

## Recommended Optimized Version

See `../prompt-optimize/examples/sample-optimization.md` for the improved version of this prompt.
