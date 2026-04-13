# Synthesis: manifesto-writing

**Baseline:** 1324 tokens (153 lines, no refs)

---

## Core Points (D2 -- untouchable)

1. Compression plus conviction: strip hedging, state positions as facts, build urgency
2. Name the enemy early: establish opposition and stakes in the opening section
3. Imperative commands over suggestions: "Do X." not "You should consider doing X."
4. Preserve distinctions/vocabulary/aphorisms; cut scaffolding/repetition/asides
5. Crystallization for sympathetic audiences -- not discovery, nuance, or first-principles persuasion

---

## Inline from References

No external references exist. Nothing to inline.

---

## Cut

### C1. Description over-length (~50 words -> ~25)

D3 (R13, moderate): 50-word trigger description with nested clauses and repeated concepts.

**Before:**
```
Trigger when users ask to turn talks, essays, or docs into a manifesto--or request manifesto tone, command-style guidance, or enemy-and-stakes framing--and then write the imperative version: name the enemy early, strip hedging, compress to core distinctions and sharp aphorisms, and end with a stark choice.
```

**After:**
```
Trigger when users request manifestos or manifesto tone. Name the enemy, strip hedging, compress to sharp distinctions, end with stark choice.
```

**Citation:** D3 lines 59-66 (R13 needless words); plugin-dev-ecosystem.md section 1.2 (250-char truncation in skill listing).

**Delta:** -25 tokens.

### C2. "Core Transformation" header + negative opening

D3 (R13 minor, R11 moderate): "Core" in header is needless. "A manifesto is not a lecture" opens with negative before the positives follow.

**Action:** Rename to "## Transformation". Delete "A manifesto is not a lecture." -- the three sentences "It declares. It commands. It names enemies." already convey this.

**Citation:** D3 lines 226-228 (R13); D3 lines 112-118 (R11).

**Delta:** -8 tokens.

### C3. Needless words throughout body

| Location | Before | After | Reason |
|---|---|---|---|
| line 21 | "builds gradually" | "builds" | "gradually" redundant |
| line 38 | "Audience interaction, jokes, asides" | "Audience asides" | subsume list |
| line 39 | "Extended examples and digressions" | "Extended examples" | "digressions" subsumed |
| line 131 | "Read source completely" | "Read source" | implied by "architecture before cutting" |
| line 136 | "on a pass dedicated to this" | "in a separate pass" | tighter |
| line 149 | "(manifestos flatten nuance)" | delete parenthetical | restates the obvious |
| line 152 | "from scratch" | delete | colloquial filler |

**Citation:** D3 lines 57-106 (R13 moderate instances).

**Delta:** -20 tokens.

### C4. "When Not to Write" negative framing -> positive prerequisites

D3 (R11 moderate): Four conditions stated as negatives. D4 (AP-CON-01) flags absence of positive constraints.

**Before:** "When Not to Write a Manifesto" with four negative conditions.

**After:** Reframe as "## Prerequisites" with positive requirements: "Manifestos require conviction. Manifestos flatten nuance. Manifestos assume sympathetic readers. Manifestos sacrifice precision for force."

**Citation:** D3 lines 139-143 (R11: reframe as positive requirements).

**Delta:** -5 tokens.

---

## Restructure

### R1. Move "Process" section earlier

The 9-step process at line 130 is buried after tone markers and attribution. Per ordering-guide.md (Agent/Skill pattern: Role -> Purpose -> Constraints -> Workflow -> Output -> Error handling), workflow should appear before output specifications.

**Action:** Move ## Process to appear immediately after ## Structural Principles, before ## Tone Markers.

**Citation:** ordering-guide.md "Agent/Skill System Prompt" pattern.

**Delta:** 0 tokens (reorder only).

---

## Strengthen

### S1. Quantify vague qualifiers

D4 (CLR-2, medium): "memorable aphorisms," "short sentences, short sections," "punchy rhythm."

**Action:**
- "Short sentences" -> "Short sentences (under 20 words)"
- "Short sections" -> "Short sections (under 150 words)"
- "Memorable aphorisms" -> "Memorable aphorisms -- lines under 15 words that capture a core distinction"

Do NOT quantify "punchy rhythm" -- tone descriptor resists tokenizable definition. Do NOT expand "tighten until it hurts" -- intentional metaphor for a manifesto-writing skill.

**Citation:** D4 WARN CLR-2 (lines 38-44); prompt-compression-strategies.md section 5.3 (match freedom to fragility -- high-freedom creative work, quantify structure not rhythm).

**Delta:** +15 tokens.

### S2. Abstract line concretized

D3 (R12 severe): "The transformation is compression plus conviction." -- abstract nouns without grounding.

**Action:** Replace with: "The transformation: cut words, state positions as facts."

**Citation:** D3 lines 28-35.

**Delta:** -2 tokens.

### S3. Passive in closing

D3 (R10 severe): "If they need convincing, this is the wrong document."

**Action:** "If they need convincing, choose another form."

**Citation:** D3 lines 13-15.

**Delta:** 0 tokens.

---

## Projected Token Delta

| Category | Tokens |
|---|---|
| Baseline | 1324 |
| Cut: description compression (C1) | -25 |
| Cut: header + negative opening (C2) | -8 |
| Cut: needless words body (C3) | -20 |
| Cut: negative-to-positive reframe (C4) | -5 |
| Strengthen: quantify qualifiers (S1) | +15 |
| Strengthen: concretize abstract (S2) | -2 |
| **Projected total** | **1279** |
| **Net delta** | **-45 (-3.4%)** |

This skill is already well-written (D4: 82/100, D3: "strong command of Strunk principles"). Changes are surgical polish, not structural overhaul. No refs to inline. No hooks needed.
