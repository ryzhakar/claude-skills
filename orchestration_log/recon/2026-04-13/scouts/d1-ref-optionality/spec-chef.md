# Reference Optionality Analysis: spec-chef

**Analyzed:** 2026-04-13
**Skill Path:** `/Users/ryzhakar/pp/claude-skills/product-craft/skills/spec-chef/`
**References Analyzed:** 4

---

## Summary

All four reference files are **DEFERRABLE**. Each is already gated appropriately in SKILL.md with conditional loading patterns. The skill body contains the complete core workflow; references provide depth when specific conditions trigger.

---

## Reference Classifications

### 1. `terminology-extraction.md` — **DEFERRABLE**

**Current Gate (line 29):**
```
When working with complex business domains or multi-author documentation, 
consider extracting domain terminology first -- see @references/terminology-extraction.md
```

**Verdict:** DEFERRABLE  
**Condition:** Multi-author docs OR complex business domain terminology confusion  
**Rationale:**  
- Not needed for every invocation (many specs involve single-author or simple domains)
- Gate condition is clear: "complex business domains or multi-author documentation"
- Core workflow (analyze, map, extract, codify) works without it
- Reference provides optional pre-step for terminology cleanup before gap detection
- Content describes WHEN to run (inconsistent vocabulary, jargon conflicts) and full extraction protocol

**Gate Quality:** Strong. Impossible to ignore when multi-author complexity exists because the condition explicitly mentions "complex business domains or multi-author documentation" which surfaces naturally during Phase 1 analysis.

---

### 2. `gap-heuristics.md` — **DEFERRABLE**

**Current Gate (line 42):**
```
For detailed gap detection patterns, see @references/gap-heuristics.md — it covers 
signal phrases and question patterns for persona gaps, behavior gaps, assumption gaps, 
edge case gaps, success gaps, and scope gaps with detection techniques.
```

**Verdict:** DEFERRABLE  
**Condition:** Need for detailed signal patterns beyond the 6-row gap table  
**Rationale:**  
- Core gap taxonomy is in SKILL.md (table with 6 gap types + signals)
- Reference expands each category with exhaustive signal phrase lists and question templates
- Many invocations will succeed with just the table (experienced practitioners recognize gaps)
- Reference value: junior practitioners, unfamiliar domains, or when gaps are subtle
- Content covers 6 gap types with signal phrases, missing element descriptions, and detection questions

**Gate Quality:** Moderate. The table in SKILL.md may suffice for straightforward cases. Gate should be strengthened:

**Recommended Gate Revision:**
```
IF you find documentation but cannot confidently categorize the gaps, OR stakeholder 
responses reveal gaps you didn't detect initially, THEN read @references/gap-heuristics.md 
for exhaustive signal patterns and question templates.
```

---

### 3. `dependency-tiers.md` — **DEFERRABLE**

**Current Gate (line 63):**
```
For tier patterns by domain, see @references/dependency-tiers.md — it covers the 
generic tier structure (Foundation, User Model, Incentives, Lifecycle, Edge Cases, Success) 
plus domain-specific variations for consumer apps, B2B tools, internal tools, and 
APIs/platforms with tier mapping techniques.
```

**Verdict:** DEFERRABLE  
**Condition:** Need domain-specific tier customization OR creating custom tier structure  
**Rationale:**  
- Core generic tier structure (Tier 0-5 with descriptions) is in SKILL.md
- Reference provides 4 domain-specific mappings (consumer app, B2B, internal, API/platform)
- Reference also provides technique for creating custom tiers
- Many invocations will use generic structure as-is
- Content includes generic tier rationale, 4 domain templates, and tier mapping technique

**Gate Quality:** Strong. Generic tier structure handles most cases. Gate clearly signals when to load: domain-specific customization or custom tier creation.

---

### 4. `artifact-separation.md` — **DEFERRABLE**

**Current Gate (line 102):**
```
For artifact templates and separation guidelines, see @references/artifact-separation.md 
— it covers the four-artifact model (Product Spec, Personas, User Stories, Architecture), 
decision matrix for what goes where, templates for each artifact type, and common mistakes 
to avoid when separating concerns.
```

**Verdict:** DEFERRABLE  
**Condition:** Writing artifacts (Phase 4: Codify)  
**Rationale:**  
- Not needed during Phases 1-3 (Analyze, Map, Extract)
- Core separation table in SKILL.md (4 rows: what each artifact contains vs. NOT contains)
- Reference provides detailed decision matrix (14 info types × 4 artifacts), full templates, common mistakes
- Every invocation reaches Phase 4, but experienced practitioners may not need templates
- Content includes 4-artifact model, decision matrix, 4 full templates, 4 mistake patterns, maintenance rule

**Gate Quality:** Moderate. Phase 4 always happens, so reference will often be needed. Gate should be strengthened:

**Recommended Gate Revision:**
```
Before writing artifacts in Phase 4, IF you are uncertain where specific information 
belongs (e.g., "Does scale go in Spec or Architecture?"), THEN read 
@references/artifact-separation.md for the decision matrix, templates, and common mistakes.
```

---

## Gate Improvement Recommendations

### 1. Strengthen `gap-heuristics.md` gate

**Current:** Passive ("For detailed gap detection patterns, see...")  
**Problem:** Doesn't specify WHEN detail is necessary  
**Fix:** Add condition for uncertain categorization or missed gaps

### 2. Strengthen `artifact-separation.md` gate

**Current:** Generic pointer during Phase 4  
**Problem:** Phase 4 always executes, so gate doesn't prevent unnecessary loads  
**Fix:** Trigger only when classification uncertainty exists

---

## No ESSENTIAL References

All references provide expansion of concepts already summarized in SKILL.md:

- **Gap table → gap-heuristics:** 6 gap types table → exhaustive signal patterns
- **Tier diagram → dependency-tiers:** Generic 6-tier structure → domain-specific mappings
- **Separation table → artifact-separation:** 4-artifact model → decision matrix + templates
- **Terminology mention → terminology-extraction:** Conditional consideration → full protocol

Core workflow is self-contained. References are depth, not foundation.

---

## Compliance Notes

- All gates use conditional language ("When...", "For...by domain", "For...templates")
- No reference is required for minimal viable execution
- Current gates make ignoring references possible when conditions don't apply
- Two gates (gap-heuristics, artifact-separation) could be tightened to reduce false loads
