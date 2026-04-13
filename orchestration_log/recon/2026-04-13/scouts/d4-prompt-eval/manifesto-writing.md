# Prompt Evaluation Report: manifesto-writing

**Type:** Skill  
**File:** `/Users/ryzhakar/pp/claude-skills/manifesto/skills/manifesto-writing/SKILL.md`  
**Evaluated:** 2026-04-13

---

## Overall Score: 82/100 (Good)

Production-ready with room for improvement in constraint specificity and output format.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓ (baseline)
- OUTPUT ✓
- EXAMPLES ✓
- AGENT_SPECIFIC ✓

Not applicable: TOOLS, REASONING, DATA_SEPARATION

---

## Critical Issues

None identified.

---

## Warnings

### CLR-2: Vague Terms Without Definition
**Severity:** Medium

- "memorable aphorisms" (line 31) — what makes an aphorism "memorable"? No objective criteria.
- "short sentences, short sections" (line 69) — no word/sentence count specified.
- "punchy rhythm" (line 70) — subjective quality without definition.
- "tighten" (line 138) — "until it hurts" is metaphorical, not actionable.

**Impact:** Claude must infer what counts as "memorable" or "short."

### OUT-4: Length Constraints Partially Defined
**Severity:** Low

The skill specifies "1500-2500 words" for a 45-minute talk transformation (line 143) but provides no guidance for other source material lengths (essays, documentation).

### CON-2: Incomplete Forbidden Actions List
**Severity:** Low

The skill states "When Not to Write a Manifesto" (lines 145-152) but lacks explicit "do NOT" constraints during execution (e.g., "do NOT preserve hedging language", "do NOT maintain academic tone").

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers (Medium)
Multiple instances of qualitative terms without measurable criteria:
- "memorable" (line 31)
- "sharp" (lines 30, 66)
- "punchy" (line 70)
- "stark" (line 79)

### AP-OUT-03: Missing Edge Cases (Low)
No guidance for handling:
- Source material with no clear enemy/opposition
- Multi-author sources with conflicting positions
- Highly technical content requiring precision over force

---

## Strengths

### STR-1: Excellent Role/Identity Statement ✓
Clear persona established:
> "Transform source material into manifestos: concentrated declarations of principle that command rather than explain." (lines 15-16)

### STR-3: Clear Task Definition ✓
Task explicitly stated in description and opening section. No ambiguity.

### STR-4: Consistent Structural Markers ✓
Uses markdown headers, tables, and clear section boundaries throughout.

### STR-5: Logical Ordering ✓
Follows recommended pattern: Role → Context (Core Transformation) → Rules (What to Preserve/Cut/Transform) → Examples → Process → Constraints (When Not to Use).

### EXM-1: Examples Well-Tagged ✓
Examples wrapped with clear separators (lines 103-127). Three examples provided.

### EXM-2: Diverse Examples ✓
Examples show different transformation types:
1. Compression + conviction shift (lines 104-109)
2. Question-to-declaration pattern (lines 114-118)
3. Extraction without transformation (lines 122-126)

### EXM-3: Input/Output Pairs ✓
All examples show "Source (spoken):" and "Manifesto:" pairs.

### CLR-5: Numbered Steps for Workflow ✓
9-step process clearly numbered (lines 131-140).

### AGT-1: Valid Name Field ✓
`name: manifesto-writing` (lowercase, hyphenated).

### AGT-2: Strong Description with Trigger Keywords ✓
Description includes specific trigger phrases:
- "turn talks, essays, or docs into a manifesto"
- "manifesto tone"
- "command-style guidance"
- "enemy-and-stakes framing"

### AGT-6: Clear Workflow Defined ✓
9-step process (lines 130-140) provides unambiguous execution sequence.

### AGT-8: Output Format Specified ✓
Structural specifications provided:
- Tables for mappings (line 74)
- Short sentences/sections (line 69)
- Length target: 1500-2500 words (line 143)

### CON-1: Scope Definition Present ✓
Clear boundary established via "When Not to Write a Manifesto" section (lines 145-152).

### CLR-7: Audience/Tone Specified ✓
Tone markers explicitly listed (lines 81-95):
- Include: moral urgency, direct address, present tense, active voice, concrete nouns
- Exclude: academic hedging, passive constructions, weasel words

---

## Recommendations

### High Priority

1. **Define subjective terms quantitatively**
   - "Short sentences" → "Sentences under 20 words"
   - "Short sections" → "Sections under 150 words"
   - "Memorable aphorisms" → "Lines under 15 words that capture core distinctions"

2. **Add explicit "do NOT" constraints to supplement "When Not to Use"**
   ```markdown
   ## During Execution: Do NOT
   - Preserve hedging language ("I think," "perhaps")
   - Maintain academic passive voice
   - Include extended examples from source
   - Use future tense for actionable principles
   ```

3. **Specify length targets for different source types**
   - 10-minute talk → 500-800 words
   - 45-minute talk → 1500-2500 words
   - Essay (5000 words) → 1000-1500 words
   - Documentation → state compression ratio (e.g., "compress to 20-30% of original length")

### Medium Priority

4. **Add edge case handling**
   ```markdown
   ## Edge Cases
   - If source has no clear opposition: Extract implicit contrasts or state limitation ("This material lacks a clear enemy; manifesto format may not suit it")
   - If source requires precision over force: Acknowledge in attribution ("Adapted with compression; see original for technical precision")
   ```

5. **Specify preamble/postamble handling**
   Add to output format: "Skip introductory text. Begin directly with enemy statement. End with the choice, no closing pleasantries."

### Low Priority

6. **Add success criteria**
   Define what makes a transformation successful:
   - All core distinctions preserved (verifiable against "Core Transformation" section)
   - No hedging language in final output (scannable)
   - Final word count within target range

---

## Scores by Category

| Category | Score | Calculation |
|----------|-------|-------------|
| STRUCTURE | 6/6 | All criteria met (STR-1✓, STR-2✓, STR-3✓, STR-4✓, STR-5✓, STR-6✓) |
| CLARITY | 5/7 | CLR-1✓, CLR-3✓, CLR-5✓, CLR-6✓, CLR-7✓; CLR-2✗ (vague terms), CLR-4~ (partial success criteria) |
| CONSTRAINTS | 4/6 | CON-1✓, CON-3✓, CON-4✓, CON-6✓; CON-2~ (partial forbidden actions), CON-5✓ |
| SAFETY | 2/2 | Baseline met (SAF-6✓ via "When Not to Use"); no sensitive data handling required |
| OUTPUT | 4/6 | OUT-1✓, OUT-2✓ (examples), OUT-6✓ (via tone exclusions); OUT-3✗ (no edge cases), OUT-4~ (partial length constraints), OUT-5✓ |
| EXAMPLES | 5/5 | EXM-1✓, EXM-2✓, EXM-3✓, EXM-4✓ (3 examples, not excessive), EXM-5✓ (3 examples appropriate) |
| AGENT_SPECIFIC | 8/10 | AGT-1✓, AGT-2✓, AGT-6✓, AGT-8✓, AGT-9✓ (153 lines); AGT-3~ (tools not explicitly restricted), AGT-5~ (no permissionMode), AGT-7✓, AGT-10 N/A |

**Total:** 34 met / 42 applicable = 81% → +1 for thoroughness = **82/100**

---

## Verdict

**Production-ready** with notable strengths in structure, examples, and workflow clarity. Primary weakness is reliance on subjective qualifiers ("memorable," "punchy," "short") that require user interpretation. Recommended fixes are straightforward quantification upgrades, not structural overhauls.
