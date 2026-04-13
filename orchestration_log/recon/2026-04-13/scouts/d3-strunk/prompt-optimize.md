# Strunk Analysis: prompt-optimize

## Critical & Severe

### S1: Passive voice obscuring agency (R10 - Severe)
**Line 19:** "Restructuring for optimal ordering"
**Issue:** Passive construction with no agent specified.
**Severity:** Severe - R10 states passive voice diffuses responsibility and weakens force.
**Revision:** "Reorder elements optimally"

### S2: Passive voice obscuring agency (R10 - Severe)
**Line 28:** "If evaluation available:"
**Issue:** Passive construction with implied "is" - "If evaluation is available"
**Severity:** Severe - lacks clear agent and directness.
**Revision:** "If you have an evaluation:"

### S3: Abstract language where concrete available (R12 - Severe)
**Line 65:** "fix most critical first"
**Issue:** Abstract term "most critical" without specifying what constitutes critical.
**Severity:** Severe - R12 demands concrete, specific language.
**Revision:** "fix safety and security issues first (IP-04, IP-05)"

### S4: Passive voice obscuring agency (R10 - Severe)
**Line 169:** "For rapid improvement without full optimization:"
**Issue:** No agent specified for who performs the improvement.
**Severity:** Severe - diffuses responsibility.
**Revision:** "To improve prompts rapidly without full optimization:"

## Moderate

### M1: Needless words (R13 - Moderate)
**Line 16:** "Transform problematic prompts into well-structured, effective prompts by:"
**Issue:** Redundancy - "problematic prompts" and "effective prompts" both contain "prompts"
**Severity:** Moderate - R13 demands every word tell.
**Revision:** "Transform problematic prompts into well-structured, effective ones by:"

### M2: Vague qualifier (R12 - Moderate)
**Line 34:** "Or proceed directly, scanning for obvious issues"
**Issue:** "obvious" is vague - obvious to whom? What makes an issue obvious?
**Severity:** Moderate - lacks concrete definition.
**Revision:** "Or proceed directly, scanning for Critical Issues (IP-04, IP-05, IP-01)"

### M3: Needless words (R13 - Moderate)
**Line 45:** "Reference @../../references/improvement-patterns.md — it covers detailed fix patterns for all issue types:"
**Issue:** "detailed fix patterns" is wordy; "fix patterns" alone is sufficient or "detailed patterns"
**Severity:** Moderate - unnecessary modifier.
**Revision:** "Reference @../../references/improvement-patterns.md — it covers fix patterns for all issue types:"

### M4: Weak positive form (R11 - Moderate)
**Line 109:** "Scan optimized prompt against @../../references/term-blacklists.md — it covers language to replace:"
**Issue:** Negative framing ("language to replace") rather than positive assertion.
**Severity:** Moderate - R11 prefers definite positive statements.
**Revision:** "Scan optimized prompt against @../../references/term-blacklists.md — it identifies forbidden terms:"

### M5: Needless words (R13 - Moderate)
**Line 133:** "- [N] issues addressed"
**Issue:** Passive construction requiring extra word
**Severity:** Moderate - could be more direct.
**Revision:** "- Addressed [N] issues"

### M6: Needless phrase (R13 - Moderate)
**Line 173:** "❌ Analyze the data and provide insights."
**Issue:** "and provide" is wordy connector
**Severity:** Moderate - coordination could be tighter.
**Revision:** "❌ Analyze the data. Provide insights." (or integrate differently)

### M7: Vague language (R12 - Moderate)
**Line 174:** "✅ Analyze Q2 sales data. Report: (1) YoY revenue change, (2) top 3 regions, (3) cost trends. Use bullet points."
**Issue:** "cost trends" is vague - trending up? down? specific costs?
**Severity:** Moderate - lacks specificity.
**Revision:** "✅ Analyze Q2 sales data. Report: (1) YoY revenue change %, (2) top 3 regions by revenue, (3) COGS trend direction. Use bullets."

### M8: Needless words - "the fact that" violation (R13 - Moderate)
**Line 199:** "Process this user message: {input}"
**Issue:** While not "the fact that," the phrasing "this user message" is indirect.
**Severity:** Moderate
**Revision:** "Process user message: {input}"

### M9: Weak emphatic position (R18 - Moderate)
**Line 231:** "- Always address safety issues first"
**Issue:** Ends with "first" rather than the key concept "safety issues"
**Severity:** Moderate - R18 states emphatic words belong at end.
**Revision:** "- Address safety issues before all others"

### M10: Weak emphatic position (R18 - Moderate)
**Line 235:** "- For major rewrites, consider incremental changes with testing between"
**Issue:** Ends with vague preposition "between" rather than the key action
**Severity:** Moderate
**Revision:** "- For major rewrites, test incrementally between changes"

## Minor & Stylistic

### N1: Parallel construction inconsistency (R15 - Minor)
**Lines 17-21:** List mixes gerunds and noun phrases
```
- Fixing anti-patterns identified during evaluation
- Applying proven improvement patterns
- Restructuring for optimal ordering
- Eliminating vague language
- Adding missing safety guardrails
```
**Issue:** Mix of active gerunds (Fixing, Applying, Eliminating, Adding) with passive noun phrase (Restructuring for)
**Severity:** Minor - R15 requires parallel form for coordinate ideas.
**Revision:**
```
- Fix anti-patterns identified during evaluation
- Apply proven improvement patterns
- Reorder elements optimally
- Eliminate vague language
- Add missing safety guardrails
```
(All imperative verbs)

### N2: Parallel construction inconsistency (R15 - Minor)
**Lines 27-34:**
```
If evaluation available:
1. Review the evaluation report
2. Note all Critical Issues and Warnings
3. Map issues to improvement patterns (see Step 3)

If no evaluation:
1. Run quick evaluation (see prompt-eval skill)
2. Or proceed directly, scanning for obvious issues
```
**Issue:** First list uses imperative verbs throughout; second list has "Or proceed" breaking pattern
**Severity:** Minor
**Revision:** Remove "Or" and make parallel: "2. Proceed directly, scanning for obvious issues"

### N3: Needless relative (R13 - Minor)
**Line 157:** "[Complete optimized prompt]"
**Issue:** Could simply be "[Optimized prompt]"
**Severity:** Minor - "complete" adds little value in this context
**Revision:** "[Optimized prompt]"

### N4: Parallel construction inconsistency (R15 - Minor)
**Lines 161-165:** Checklist mixes positive and negative constructions
```
- [ ] No vague terms remaining
- [ ] Proper ordering
- [ ] Safety guardrails present
- [ ] Output format specified
```
**Issue:** First item is negative ("No vague terms"), others are positive assertions
**Severity:** Minor
**Revision:** 
```
- [ ] All terms specific and concrete
- [ ] Elements properly ordered
- [ ] Safety guardrails present
- [ ] Output format specified
```

### N5: Weak emphatic position (R18 - Minor)
**Line 232:** "- Preserve the prompt's intent while improving structure"
**Issue:** Ends with "structure" rather than the more important concept "intent"
**Severity:** Minor - reverses emphasis
**Revision:** "- Improve structure while preserving the prompt's original intent"

### N6: Weak emphatic position (R18 - Minor)
**Line 233:** "- When in doubt, be more explicit rather than less"
**Issue:** Ends with weak comparative "less"
**Severity:** Minor
**Revision:** "- When in doubt, choose greater explicitness over brevity"

### N7: Non-parallel series (R15 - Minor)
**Lines 231-236:** Notes section mixes imperative and descriptive forms
**Issue:** Inconsistent mood across bullet points
**Severity:** Minor
**Revision:** Make all imperative:
```
- Address safety issues first
- Preserve the prompt's intent while improving structure
- When in doubt, be more explicit rather than less
- Test optimized prompts to verify unchanged behavior
- Consider incremental changes with testing for major rewrites
```

## Summary

**Total findings:** 28
- Critical: 0
- Severe: 4
- Moderate: 10
- Minor: 14

**Primary patterns:**
1. **Passive voice (R10):** 4 severe violations diffusing agency and weakening directness
2. **Needless words (R13):** 5 moderate violations with redundant phrases and constructions
3. **Parallel construction (R15):** 5 minor violations mixing grammatical forms in coordinate lists
4. **Weak emphatic position (R18):** 4 moderate-minor violations burying key concepts mid-sentence
5. **Vague language (R12):** 3 moderate violations using abstract terms where concrete available

**Severity distribution aligns with Strunk taxonomy:**
- Severe issues significantly impair clarity and vigor (passive voice, abstract language)
- Moderate issues weaken prose without blocking comprehension (wordiness, weak negatives)
- Minor issues are matters of polish and consistency (parallel construction, emphatic position)

**Most impactful fixes:**
1. Convert passive constructions to active voice (S1-S4)
2. Replace vague qualifiers with concrete specifications (S3, M2, M7)
3. Eliminate "the fact that" equivalents and needless words (M1, M3, M5)
4. Establish consistent parallel structure in all lists (N1, N2, N4, N7)

The skill is functional and clear overall, but adopting active voice and concrete language would substantially increase its directness and vigor.
