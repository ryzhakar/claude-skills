# Validation Report: prompt-engineering plugin rewrite

**Date**: 2026-04-13
**Scope**: prompt-eval SKILL.md, prompt-optimize SKILL.md
**Verdict**: PASS (all checklist items pass)

---

## 1. Core points preserved? -- PASS

### prompt-eval (5 D2 core points)

| # | Core Point | Status | Evidence |
|---|---|---|---|
| 1 | Evaluation grounded in Anthropic's official documentation, not subjective preference | PRESENT, PROMINENT | Opening line: "Evaluate Claude system prompts against Anthropic's official criteria." Also in frontmatter description. |
| 2 | Vague terms are critical failures requiring specific criteria | PRESENT, PROMINENT | CLR-2 MUST_NOT at line 77. Full Vague Terms Reference section (lines 213-247). AP-CLR-02 in anti-pattern catalog. |
| 3 | Data-instruction separation with XML boundaries | PRESENT | DAT-1 through DAT-4 criteria (lines 131-134). AP-STR-02 (line 159). SAF-4 injection defense criterion. |
| 4 | Silent thinking is a critical failure | PRESENT | RSN-2 MUST_NOT at line 126. AP-RSN-01 Critical severity at line 202. |
| 5 | Tool descriptions must be specific with examples | PRESENT | TLS-1 through TLS-7 criteria (lines 108-115). AP-TLS-01 through AP-TLS-04 (lines 190-194). |

### prompt-optimize (5 D2 core points)

| # | Core Point | Status | Evidence |
|---|---|---|---|
| 1 | Safety-first prioritization | PRESENT, PROMINENT | Opening line: "Address safety issues first." Priority ordering places Safety (IP-04, IP-05) as item 1. |
| 2 | Vague language elimination | PRESENT | IP-01 pattern with before/after. Step 3 scans for vague terms. Full Vague Terms Reference section. Validation checklist item CLR-2. |
| 3 | Canonical element ordering (10-position) | PRESENT | Full 10-element table with Required? column. 5 ordering anti-patterns listed. Step 3 directive to restructure. |
| 4 | Data-instruction separation | PRESENT | IP-04 (injection defense) and IP-09 (separate data from instructions) both with before/after examples. Quick-scan items 4-5. Validation checklist DAT-2. |
| 5 | Output format specification | PRESENT | IP-03 with before/after example including edge case handling. Priority item 3 in Step 2. Validation checklist OUT-5. |

---

## 2. Critical criteria inlined? -- PASS

### prompt-eval: evaluation criteria

- **All criteria IDs present**: STR-1 through STR-6, CLR-1 through CLR-7, CON-1 through CON-6, SAF-1 through SAF-6, OUT-1 through OUT-6, TLS-1 through TLS-7, EXM-1 through EXM-5, RSN-1 through RSN-4, DAT-1 through DAT-4, AGT-1 through AGT-10. **56/56 present.**
- **Severity levels**: 3-row table with MUST (-3), SHOULD (+1), MUST_NOT (-3). Present.
- **Scoring formula**: `Score = (passed / applicable) x 100` with adjustments. Present.
- **Applicability rules**: 10-row table mapping categories to conditions. Present.

### prompt-optimize: improvement patterns

- **All 12 patterns present**: IP-01 through IP-12, each with Before/After example. **12/12 present.**
- **Conflicting Constraints bonus pattern**: Present (lines 115-117).
- **Canonical ordering table**: 10-element table. Present.
- **Priority sequence**: 6-level priority ordering (Safety > Clarity > Output > Structure > Tools > Agent). Present in Step 2.

---

## 3. Cross-domain coverage? -- PASS

### prompt-eval: light coverage of improvement patterns

- Does NOT inline full improvement patterns (correctly removed per synthesis spec).
- Contains single reference: "To fix identified issues, invoke `/prompt-optimize`." (line 55). Sufficient for cross-referral.

### prompt-optimize: light coverage of evaluation criteria

- 9-item validation checklist referencing criterion IDs: STR-3, CLR-1, CLR-2, CLR-3, CON-1, CON-5, SAF-5, DAT-2, AGT-6, OUT-5.
- References prompt-eval in frontmatter ("Works best after prompt-eval identifies problems") and Step 4 ("If prompt-eval is available, re-run evaluation").
- Quick-scan maps 10 anti-pattern IDs to improvement pattern IDs. Sufficient.

---

## 4. Vague terms and anti-patterns? -- PASS

### Term blacklist content

Both files contain the Vague Terms Reference section with:
- Quality descriptors (12 terms)
- Quantity descriptors (9 terms)
- Evaluation terms (8 terms)
- Timing terms (6 terms)
- Hedging phrases (5 phrases)
- Filler phrases (4 phrases)
- Contradictory Pairs table (4 rows) -- prompt-eval labels column "Conflict", prompt-optimize labels "Resolution" (correctly differentiated per each skill's role)
- Ambiguous verbs (10 verbs)
- Replacement examples table (5 rows)

### Anti-pattern catalog (prompt-eval)

All 38 anti-patterns present: AP-STR-01 through AP-STR-05, AP-CLR-01 through AP-CLR-05, AP-CON-01 through AP-CON-04, AP-SAF-01 through AP-SAF-04, AP-OUT-01 through AP-OUT-04, AP-TLS-01 through AP-TLS-04, AP-EXM-01 through AP-EXM-04, AP-RSN-01 through AP-RSN-03, AP-AGT-01 through AP-AGT-05. **38/38 present.**

### Quick-scan checklist (prompt-optimize)

10-item standalone quick-scan present with AP-to-IP mappings. **10/10 present.**

---

## 5. Workflow coherent? -- PASS

### prompt-eval: 3-step workflow

1. **Classify and Scope**: Read prompt, determine type (API/Agent/Skill), check applicability table. Clear.
2. **Evaluate**: Check criteria per category, record violations with ID/severity/location/quote, scan anti-patterns, check ordering. Clear.
3. **Score and Report**: Calculate per formula, generate per template, reference prompt-optimize for fixes. Clear.

A user can follow this: get input -> evaluate systematically -> produce output. Logical and complete.

### prompt-optimize: 4-step workflow

1. **Assess**: Extract issues from eval report OR run standalone quick-scan. Clear.
2. **Fix by Priority**: Apply patterns in safety-first order with explicit pattern references. Clear.
3. **Reorder and Clean**: Restructure to canonical ordering, scan for vague terms. Clear.
4. **Validate**: Run validation checklist or re-run prompt-eval. Clear.

A user can follow this: understand problems -> fix them -> restructure -> verify. Logical and complete.

---

## 6. Language strength? -- PASS

### Directive language

Both skills use imperative commands throughout:
- prompt-eval: "Evaluate", "Read", "Determine", "Check", "Record", "Scan", "Calculate", "Generate"
- prompt-optimize: "Fix", "Apply", "Replace", "Add", "Restructure", "Scan", "Run", "Confirm", "Extract", "Map"

### Hedging check

No hedging language in directive text. The only occurrences of "might", "try to", etc. are within the Vague Terms Reference itself (listing terms to flag), not in the skill's own instructions.

### Emphatic markers

- prompt-eval opens with a direct imperative: "Evaluate Claude system prompts against Anthropic's official criteria. Rank violations by severity and produce a structured report."
- prompt-optimize opens with: "Fix identified prompt issues using Anthropic-grounded patterns. Address safety issues first."
- Both use bold for priority labels and UPPERCASE for severity levels (MUST, SHOULD, MUST_NOT).

---

## 7. Token count verification -- PASS

### Measured token counts (cl100k_base via `just tokens`)

| File | Tokens |
|---|---|
| prompt-eval SKILL.md | 3138 |
| prompt-optimize SKILL.md | 2693 |

### Reduction calculation

**Per-skill reduction** (body + all referenced files that were loaded via `@` on each invocation):

| Metric | prompt-eval | prompt-optimize |
|---|---|---|
| Old body | 1250t | 1549t |
| Old shared refs (5 files) | 11408t | 11408t |
| Old total on invocation | 12658t | 12957t |
| New self-contained body | 3138t | 2693t |
| Reduction | 75% | 79% |

**Combined reduction**: 25615t -> 5831t = **77%**

The claimed 77% reduction is accurate when measured as the combined per-invocation context of both skills (each formerly loading all 5 shared reference files). The reduction is legitimate, not achieved by cutting content, but by:
1. Compressing reference content (removing preambles, check-method columns, element-detail sections, regex patterns)
2. Asymmetric inlining (each skill deeply inlines its own domain, shallowly the other's)
3. Removing dead references and redundant sections
4. Eliminating improvement-patterns.md from prompt-eval entirely (not its domain)

**Alternative accounting** (shared-refs model, counting refs once): 14207t -> 5831t = 59%. This represents the actual disk-space savings, but the 77% figure correctly represents per-invocation context savings, which is the relevant metric for prompt performance.

---

## Summary

| Checklist Item | Verdict |
|---|---|
| 1. Core points preserved | PASS |
| 2. Critical criteria inlined | PASS |
| 3. Cross-domain coverage | PASS |
| 4. Vague terms and anti-patterns | PASS |
| 5. Workflow coherent | PASS |
| 6. Language strength | PASS |
| 7. Token count verification | PASS |

**Overall: PASS. No critical content was lost. The 77% reduction is legitimate.**
