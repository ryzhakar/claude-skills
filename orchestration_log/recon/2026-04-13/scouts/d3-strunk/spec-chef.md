# Strunk Analysis: spec-chef

## Critical & Severe

### R10 (Active Voice) - Severe
**Line 18:** "Documentation has gaps because writers assume context readers lack."
- Passive: "writers assume context [that is] lack[ed by] readers"
- Suggested: "Documentation has gaps because writers assume context their readers don't have."
- Severity: Severe (passive participle creates parsing burden)

### R12 (Concrete Language) - Severe
**Line 23:** "Codifies immediately (artifacts before context decays)"
- Abstract: "context decays"
- Suggested: "Codifies immediately (capture decisions before stakeholders forget nuances)"
- Severity: Severe (metaphor "decays" is vague; what specifically happens?)

**Line 91:** "Write artifacts IMMEDIATELY after each tier (or at most after all tiers complete). Don't wait—context decays."
- Abstract: "context decays" (repeated)
- Suggested: "Don't wait—stakeholders forget details and rationales fade."
- Severity: Severe (same vagueness)

### R13 (Needless Words) - Severe
**Line 29:** "When working with complex business domains or multi-author documentation, consider extracting domain terminology first"
- Wordy: "consider extracting"
- Suggested: "extract domain terminology first"
- Severity: Severe ("consider" weakens the directive; skill text should be definite)

## Moderate

### R11 (Positive Form) - Moderate
**Line 7-8:** "Use when existing documentation has gaps, implicit assumptions, or undefined behaviors that require stakeholder input to resolve."
- Negative construction: "undefined behaviors"
- Suggested: "Use when documentation needs explicit behaviors, confirmed assumptions, or filled gaps requiring stakeholder input."
- Severity: Moderate (reader must infer what IS needed from what ISN'T present)

**Line 96:** "Does NOT Contain"
- Multiple negatives in table (lines 96, 97, 98, 99)
- Suggested: Reframe table header to "Contains ONLY" and use positive assertions
- Severity: Moderate (table structure forces negatives, but could be reframed)

### R13 (Needless Words) - Moderate
**Line 42:** "For detailed gap detection patterns, see @references/gap-heuristics.md — it covers signal phrases and question patterns for persona gaps, behavior gaps, assumption gaps, edge case gaps, success gaps, and scope gaps with detection techniques."
- Wordy: "it covers" + long enumeration
- Suggested: "For detailed gap detection patterns, see @references/gap-heuristics.md covering signal phrases, question patterns, and detection techniques for persona/behavior/assumption/edge-case/success/scope gaps."
- Severity: Moderate (repetitive structure "X gaps" appears 6 times)

**Line 62:** "For tier patterns by domain, see @references/dependency-tiers.md — it covers the generic tier structure (Foundation, User Model, Incentives, Lifecycle, Edge Cases, Success) plus domain-specific variations for consumer apps, B2B tools, internal tools, and APIs/platforms with tier mapping techniques."
- Wordy: "it covers" + verbose enumeration
- Suggested: "For tier patterns by domain, see @references/dependency-tiers.md covering generic tier structure and domain-specific variations (consumer apps, B2B tools, internal tools, APIs/platforms) with mapping techniques."
- Severity: Moderate (padding around core content)

**Line 101:** "For artifact templates and separation guidelines, see @references/artifact-separation.md — it covers the four-artifact model (Product Spec, Personas, User Stories, Architecture), decision matrix for what goes where, templates for each artifact type, and common mistakes to avoid when separating concerns."
- Wordy: "it covers" pattern (third instance)
- Suggested: "For templates and separation guidelines, see @references/artifact-separation.md covering the four-artifact model, decision matrix, templates, and common separation mistakes."
- Severity: Moderate (formulaic repetition; every reference uses "it covers")

### R15 (Parallel Construction) - Moderate
**Lines 19-23:** List items mix verb forms
- "Detects gaps" (present tense)
- "Orders questions" (present tense)
- "Constrains choices" (present tense)
- "Codifies immediately" (present tense + adverb)
- "Separates concerns" (present tense)
- Inconsistency: #4 adds parenthetical explanation in different voice
- Suggested: Either all bare verbs OR all with parallel explanatory structure
- Severity: Moderate (mostly parallel, but #4 breaks pattern with parenthetical)

**Lines 94-99:** Table mixes content types
- "Decisions, constraints, behaviors" (plural nouns)
- "Users, jobs-to-be-done, anti-personas" (mixed: plural noun, hyphenated concept, plural noun)
- "Value units, AC as hypotheses" (abbreviation + noun phrase)
- "Technical decisions, patterns" (inconsistent plurality)
- Suggested: Standardize plurality and structure within each cell
- Severity: Moderate (function is clear but form inconsistent)

### R18 (Emphatic Position) - Moderate
**Line 13:** "Transform implicit stakeholder knowledge into explicit artifacts through systematic gap detection and constrained questioning."
- Ends with method ("constrained questioning") not outcome
- Suggested: "Through systematic gap detection and constrained questioning, transform implicit stakeholder knowledge into explicit artifacts."
- Severity: Moderate (places emphasis on technique rather than result)

**Line 17:** "Stakeholders know more than they've written."
- Strong opening, but could be more emphatic
- Suggested: "Stakeholders know more than they've written—gaps exist because writers assume context readers don't have."
- Severity: Moderate (sentence is good but could combine with #18 for stronger punch)

## Minor & Stylistic

### R10 (Active Voice) - Minor
**Line 31:** "Identify gaps using these categories:"
- Could be more active by naming the actor explicitly
- Current form is acceptable imperative
- Severity: Minor (imperative mood is effectively active)

### R12 (Concrete Language) - Minor
**Line 35:** "Missing personas | 'users' without specifics"
- "Specifics" is somewhat abstract
- Suggested: "'users' without roles, contexts, or goals"
- Severity: Minor (example does provide concrete signal: "users")

### R13 (Needless Words) - Minor
**Line 69:** "Rules:"
- Could integrate into preceding sentence
- Severity: Minor (header serves organizational function)

**Line 86:** "Ask tier-by-tier. Capture answers before moving to next tier."
- "tier-by-tier" + "before moving to next tier" is slightly redundant
- Suggested: "Ask tier-by-tier, capturing answers before advancing."
- Severity: Minor (emphasis through repetition may be intentional)

### R15 (Parallel Construction) - Minor
**Lines 109-115:** Anti-patterns table mixes command types
- "Ask open-ended questions" (verb phrase)
- "Bundle multiple decisions" (verb phrase)
- "Wait to codify" (verb phrase)
- "Mix WHAT/WHO/HOW" (verb phrase)
- "Assume tier order" (verb phrase)
- All parallel in left column; good structure
- Severity: Minor (actually well-parallelized)

### R18 (Emphatic Position) - Minor
**Line 105:** "Update project documentation (CLAUDE.md or equivalent) to reference new artifacts. Future sessions must find them."
- First sentence ends weakly with "new artifacts" (object)
- Second sentence provides emphasis through imperative
- Suggested: "Update project documentation (CLAUDE.md or equivalent): future sessions must find new artifacts."
- Severity: Minor (two-sentence structure provides emphasis through separation)

## Summary

**Critical/Severe findings: 5**
- 1 passive voice issue (R10)
- 2 abstract language issues (R12) 
- 2 needless word issues (R13)

**Moderate findings: 11**
- 1 negative construction (R11)
- 4 needless word issues (R13)
- 2 parallel construction issues (R15)
- 2 emphatic position issues (R18)
- 2 table structure issues spanning multiple rules

**Minor/Stylistic findings: 7**
- Mostly refinement opportunities in concrete language, economy, and emphasis

**Primary patterns:**
1. **Formulaic reference structure** (R13): "see X — it covers Y" appears 3 times; creates padding and monotony
2. **Abstract metaphor** (R12): "context decays" used twice; vague mechanism (what exactly decays? memories? shared understanding? specific details?)
3. **Weakened imperatives** (R13 + R11): "consider extracting" instead of "extract"

**Strengths:**
- Clear hierarchical structure aids navigation
- Tables provide concrete categorization
- Protocol steps use mostly active, direct voice
- Anti-patterns section uses parallel construction well

**Recommendation priority:**
1. Replace "context decays" with concrete description (R12 - severe)
2. Eliminate "consider" hedging in directive text (R13 - severe)
3. Standardize reference link structure to reduce "it covers" repetition (R13 - moderate)
4. Convert negative table header to positive framing (R11 - moderate)
