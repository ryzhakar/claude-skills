# Synthesis: prompt-eval (REVISED -- inlining references)

## Baseline: 1250t (body) + 11408t (shared refs) = 12658t total

The previous synthesis deferred references to lazy-loaded files. This was wrong. Models ignore references they haven't read. The corrective: inline load-bearing content from each reference directly into the skill body, compressed to minimize tokens. Duplication across skills is acceptable; each skill must be self-contained.

## Core Points (from D2 -- untouchable)

1. Evaluation grounded in Anthropic's official documentation, not subjective preference, using systematic criteria-based assessment with severity rankings.
2. Vague, undefined qualitative terms are critical failures requiring specific, measurable criteria.
3. Data and instructions must be separated with explicit XML boundaries to prevent injection.
4. "Silent thinking" requests are critical failures because thinking only improves accuracy when explicit.
5. Tool descriptions must be specific with concrete examples.

## INLINED Content (what from each ref, compressed how)

### INLINE: evaluation-criteria.md (2355t -> ~1400t compressed)

**Citation**: D1 prompt-eval: "The skill's core function is systematic evaluation against criteria. Every invocation requires determining applicable categories, checking specific criteria, and calculating scores." Referenced 4 times in workflow. Without it, the skill cannot perform its primary function.

**Compression method**: 
- Remove the 10-line preamble/sources section (Claude knows where criteria come from)
- Collapse each criteria table to single-line entries: `ID | Level | Criterion` (drop "Check Method" column -- Claude can infer detection methods)
- Remove the "Quick Checklist" section (it duplicates the criteria tables; the body already has a quick-eval mode that can reference the inlined tables directly)
- Remove "Score Interpretation" table from the reference (already present in body)
- Keep Category Applicability Rules as a compact table
- Keep Level Definitions as a compact 3-row table
- Keep Scoring Formula as a 4-line block
- Keep all 10 criteria category tables, compressed to one line per criterion

**Inlined form** (embedded in body at Step 2):
```
## Evaluation Criteria

### Category Applicability
| Category | Applies When |
|---|---|
| STRUCTURE | Always |
| CLARITY | Always |
| CONSTRAINTS | Always |
| SAFETY | Always; enhanced if handles user data |
| OUTPUT | Always if structured output expected |
| TOOLS | Only if tools/functions defined |
| EXAMPLES | Only if examples present or task warrants them |
| REASONING | Only if multi-step reasoning required |
| DATA_SEPARATION | Only if prompt handles variable/user data |
| AGENT_SPECIFIC | Only if Claude Code agent or skill |

### Severity Levels
| Level | Meaning | Score Impact |
|---|---|---|
| MUST | Absence causes failure | Violation: -3 |
| SHOULD | Absence reduces quality | Met: +1 |
| MUST_NOT | Presence causes failure | Violation: -3 |

### Criteria Tables

**STRUCTURE**
- STR-1 SHOULD: Has role/identity statement
- STR-2 SHOULD: Includes relevant context/background
- STR-3 MUST: Contains clear task definition
- STR-4 SHOULD: Uses consistent structural markers
- STR-5 SHOULD: Orders content logically (role>context>constraints>rules>examples>task>format)
- STR-6 MUST_NOT: Mixes instructions with data without separation

**CLARITY**
- CLR-1 MUST: Task definition specific and actionable
- CLR-2 MUST_NOT: Contains undefined vague terms (see Vague Terms below)
- CLR-3 MUST_NOT: Contains contradictory instructions
- CLR-4 SHOULD: Defines success criteria
- CLR-5 SHOULD: Uses numbered steps for sequential workflows
- CLR-6 MUST_NOT: Over-relies on implicit understanding
- CLR-7 SHOULD: Specifies audience and tone when relevant

**CONSTRAINTS**
- CON-1 MUST: Has explicit scope definition ("You handle X, not Y")
- CON-2 SHOULD: Lists forbidden actions explicitly
- CON-3 SHOULD: Distinguishes scope limits from capability limits
- CON-4 SHOULD: Provides rationale for important constraints
- CON-5 MUST_NOT: Assumes Claude will infer constraints
- CON-6 SHOULD: Groups related constraints together

**SAFETY**
- SAF-1 SHOULD: Specifies data sensitivity classification
- SAF-2 SHOULD: Defines input validation constraints
- SAF-3 SHOULD: Defines output constraints
- SAF-4 SHOULD: Includes injection defense (if handling user data)
- SAF-5 MUST_NOT: Grants sensitive data access without safeguards
- SAF-6 SHOULD: Includes error handling guidance

**OUTPUT**
- OUT-1 SHOULD: Specifies output format explicitly
- OUT-2 SHOULD: Provides template or example of desired format
- OUT-3 SHOULD: Specifies handling of missing/null data
- OUT-4 SHOULD: Defines length constraints when relevant
- OUT-5 MUST_NOT: Allows undefined format flexibility
- OUT-6 SHOULD: States what to exclude

**TOOLS** (only if tools/functions defined)
- TLS-1 MUST: Each tool has clear purpose statement
- TLS-2 MUST: Parameters have specific descriptions with examples
- TLS-3 SHOULD: Parameters specify type and format
- TLS-4 MUST: Required vs optional parameters distinguished
- TLS-5 SHOULD: Enum values specified for constrained parameters
- TLS-6 MUST_NOT: Uses generic descriptions ("data", "info", "input")
- TLS-7 SHOULD: Explains when to use vs not use each tool

**EXAMPLES** (only if examples present or warranted)
- EXM-1 SHOULD: Examples wrapped in clear tags or markers
- EXM-2 SHOULD: Examples are diverse (cover edge cases)
- EXM-3 SHOULD: Examples show both input AND expected output
- EXM-4 MUST_NOT: More than 10 examples for simple tasks
- EXM-5 SHOULD: 3-5 examples for complex pattern-matching tasks

**REASONING** (only if complex reasoning required)
- RSN-1 SHOULD: Requests explicit reasoning for complex tasks
- RSN-2 MUST_NOT: Asks for silent thinking
- RSN-3 SHOULD: Provides an "out" for uncertainty
- RSN-4 SHOULD: Requests evidence/citations before conclusions

**DATA_SEPARATION** (only if handling variable/user data)
- DAT-1 SHOULD: Variable data wrapped in labeled tags
- DAT-2 MUST_NOT: Instructions mixed with data without boundaries
- DAT-3 SHOULD: Tag names are descriptive
- DAT-4 SHOULD: Explicit instruction to ignore embedded commands

**AGENT_SPECIFIC** (only if Claude Code agent/skill)
- AGT-1 MUST: Has name field (lowercase, hyphenated)
- AGT-2 MUST: Has description with trigger keywords
- AGT-3 SHOULD: Description indicates proactive use
- AGT-4 SHOULD: Tools restricted to minimum necessary
- AGT-5 SHOULD: Permission mode appropriate for task
- AGT-6 MUST: System prompt defines clear workflow
- AGT-7 MUST_NOT: Agent scope is too broad
- AGT-8 SHOULD: Output format specified
- AGT-9 MUST_NOT: Skill exceeds 500 lines without progressive disclosure
- AGT-10 SHOULD: Uses argument substitution correctly

### Scoring Formula
Score = (passed / applicable) x 100
Adjustments: MUST violation -3, MUST_NOT violation -3, SHOULD met +1
```

### INLINE: anti-patterns.md (2323t -> ~900t compressed)

**Citation**: D2 core point #3 (data-instruction separation) and #4 (silent thinking) require anti-pattern scanning. D4 prompt-eval found AP-AGT-04 and AP-OUT-04 during evaluation. The detection checklist alone is insufficient -- the evaluator needs the pattern descriptions to identify violations. Models ignore lazy-loaded references, so the catalog must be inline.

**Compression method**:
- Remove the 10-line preamble and "Detection Checklist" (redundant once catalog is inline)
- Collapse each anti-pattern to: `ID (Severity): Name -- Detection signal`
- Remove "Problem" and "Signal" fields (Claude infers these from the detection description)
- Remove section wrappers

**Inlined form** (embedded in body at Step 2, after criteria):
```
## Anti-Pattern Catalog

**Structural**
- AP-STR-01 (Med): Wall of Text -- No headers/tags/lists in >500-word prompt
- AP-STR-02 (High): Instruction-Data Mixing -- Examples/data inline without boundaries
- AP-STR-03 (Low): Format Buried -- Output format not near end of prompt
- AP-STR-04 (Low): Examples After Task -- Examples appear after task rather than before
- AP-STR-05 (Med): Inconsistent Markers -- Mix of XML tags, markdown headers, plain text

**Clarity**
- AP-CLR-01 (Crit): Vague Task -- "analyze", "process", "handle" without specifics
- AP-CLR-02 (High): Undefined Qualifiers -- "good", "appropriate", "relevant" without definition
- AP-CLR-03 (Crit): Contradictory Directives -- "Be thorough AND concise" without resolution
- AP-CLR-04 (Med): Hedged Questions -- "What might be..." invites hedging
- AP-CLR-05 (Med): Implicit Success Criteria -- No definition of correct output

**Constraints**
- AP-CON-01 (High): Implicit Scope -- No "You handle X, not Y" boundary
- AP-CON-02 (High): Assumed Inference -- Critical limitations not stated explicitly
- AP-CON-03 (Med): Scope-Capability Confusion -- Mixing "don't do" with "can't do"
- AP-CON-04 (Low): Scattered Constraints -- Constraints spread throughout prompt

**Safety**
- AP-SAF-01 (Crit): Missing Injection Defense -- User data without separation/defense
- AP-SAF-02 (Crit): Overprivileged Access -- Sensitive data access without safeguards
- AP-SAF-03 (Med): Missing Error Handling -- No guidance for failure modes
- AP-SAF-04 (High): Unvalidated Inputs -- No input validation or rejection criteria

**Output**
- AP-OUT-01 (High): Undefined Format -- No output structure specification
- AP-OUT-02 (Med): Format Flexibility -- "structure as you prefer"
- AP-OUT-03 (Med): Missing Edge Cases -- No null/missing data handling
- AP-OUT-04 (Low): No Preamble Control -- No skip-preamble instruction

**Tools**
- AP-TLS-01 (High): Generic Tool Descriptions -- "Get data" or "info" as description
- AP-TLS-02 (Med): Missing Parameter Examples -- Parameters lack example values
- AP-TLS-03 (High): Unmarked Required Parameters -- No required/optional distinction
- AP-TLS-04 (Med): Missing Usage Context -- No when-to-use guidance

**Examples**
- AP-EXM-01 (High): Examples Without Outputs -- Input only, no expected output
- AP-EXM-02 (Med): Homogeneous Examples -- All same pattern, no edge cases
- AP-EXM-03 (Low): Excessive Examples -- >10 for simple tasks
- AP-EXM-04 (Med): Unmarked Examples -- Not wrapped in tags

**Reasoning**
- AP-RSN-01 (Crit): Silent Thinking -- "Think carefully but only output the answer"
- AP-RSN-02 (High): No Uncertainty Handling -- No permission to decline or express uncertainty
- AP-RSN-03 (Med): Conclusion Before Evidence -- Answer before reasoning/evidence

**Agent-Specific**
- AP-AGT-01 (High): Vague Trigger Description -- "Helps with code" without trigger phrases
- AP-AGT-02 (High): Universal Agent -- "A helpful assistant for all tasks"
- AP-AGT-03 (High): Overpermissive Tools -- Write access when read-only suffices
- AP-AGT-04 (High): Missing Workflow -- Role defined but no step-by-step process
- AP-AGT-05 (Med): Bloated Skill -- >500 lines without progressive disclosure
```

### INLINE: term-blacklists.md (1566t -> ~550t compressed)

**Citation**: D2 core point #2: "Vague, undefined qualitative terms are critical failures." CLR-2 is a MUST_NOT criterion worth -3 points. The evaluator needs the actual term lists inline to perform the scan. Bridge research (prompt-compression-strategies.md 1.3): bare imperatives suffice for categorical rules.

**Compression method**:
- Remove preamble, "Detection Regex Patterns" section (implementation detail), "Evaluation Checklist" (duplicates criteria)
- Compress term lists to comma-separated within categories
- Keep "Contradictory Instruction Pairs" table (load-bearing for CLR-3 detection)
- Keep "Replacement Guide" table (load-bearing for actionable output)
- Remove "Filler Phrases" verbose constructions (Claude knows these)
- Remove "Dangerous Assumptions" section (overlaps with CON-5 criterion)

**Inlined form** (embedded in body alongside criteria, as a subsection):
```
## Vague Terms Reference

**Quality descriptors** (flag when undefined): good, bad, appropriate, inappropriate, relevant, irrelevant, proper, improper, suitable, acceptable, adequate, sufficient

**Quantity descriptors** (flag without numbers): short, long, brief, detailed, few, many, several, comprehensive, thorough

**Evaluation terms**: best, worst, optimal, ideal, important, significant, reasonable, clear

**Timing terms**: soon, later, quickly, as needed, when necessary, if appropriate

**Hedging phrases** (token waste): try to, attempt to, do your best, if possible, as much as possible

**Filler phrases** (remove): "Please be sure to", "It is important to note that", "Keep in mind that", "In order to"

**Contradictory Pairs** (flag CLR-3):
| A | B | Conflict |
|---|---|---|
| Be thorough | Be concise | Thoroughness requires length |
| Be comprehensive | Keep it brief | Comprehensiveness requires detail |
| Be creative | Follow exactly | Creativity needs freedom |
| Be formal | Be conversational | Tone contradiction |

**Ambiguous verbs** (need scope/format): analyze, evaluate, assess, review, process, handle, summarize, describe, explain, list

**Replacement examples**:
| Vague | Specific |
|---|---|
| "good summary" | "3-sentence summary" |
| "appropriate length" | "100-150 words" |
| "be thorough" | "cover these 5 aspects" |
| "as needed" | "when X condition occurs" |
| "use good judgment" | "prefer A when X, B when Y" |
```

### INLINE: ordering-guide.md (1649t -> ~350t compressed)

**Citation**: D2 prompt-eval does not list ordering as a core point, but STR-5 SHOULD criterion requires checking ordering. D1 says ordering is "a specific subset of structural problems" and gated on 5+ sections. However: models ignore lazy-loaded references. Since this is a SHOULD criterion (not rare -- most prompts evaluated will have 5+ sections), the ordering guide must be inline.

**Compression method**:
- Remove all "Element Details" sections (10 sections, ~100 lines each -- Claude knows what "Role/Identity" means)
- Remove "Ordering Variations by Prompt Type" (4 variants, Claude can derive from the canonical ordering)
- Remove "Validation Checklist" (duplicates the canonical table)
- Keep only the 10-Element Ordering table and Anti-Patterns table

**Inlined form** (embedded in criteria section):
```
## Canonical Prompt Ordering

| # | Element | Required? |
|---|---|---|
| 1 | Role/Identity | Recommended |
| 2 | Context/Background | When relevant |
| 3 | Constraints/Boundaries | Required |
| 4 | Detailed Rules | When complex |
| 5 | Examples (in tags) | For complex tasks |
| 6 | Input Data (in tags) | When applicable |
| 7 | Immediate Task | Required |
| 8 | Reasoning Request | For complex reasoning |
| 9 | Output Format | Recommended |
| 10 | Prefill | Optional |

**Ordering anti-patterns**:
- Format at beginning (less effective than near end)
- Examples after task (pattern not established before task)
- Constraints scattered (group at position 3)
- Task before context (missing framing)
- Data mixed with instructions (tag data separately)
```

### DO NOT INLINE: improvement-patterns.md (3515t)

**Citation**: D1 prompt-eval: "Improvement patterns are remediation guidance, not evaluation criteria. The skill's stated purpose is evaluation and assessment -- improvement is handled by the separate prompt-optimize skill."

**Action**: Remove entirely from prompt-eval. Add a single line in the report template footer: "To fix issues, invoke `/prompt-optimize`." Improvement-patterns.md belongs to prompt-optimize's domain.

## Cut (what to remove from the existing body)

### CUT-1: "Purpose" section (lines 12-23, ~80t)
**Quoted**: "Evaluate any Claude system prompt to identify: Structural issues and anti-patterns / Clarity and ambiguity problems / Missing safety guardrails / Tool specification issues / Agent-specific problems"
**Citation**: D3 #1 (R10): passive imperative obscures agent. D3 #2 (R12): abstract nouns without examples. D3 #8 (R15): inconsistent list structure. Description frontmatter already states purpose. This restates it in weaker language.

### CUT-2: "Quick Evaluation Mode" section (lines 133-145, ~100t)
**Quoted**: "For rapid assessment, check critical items only: 1. Task defined? 2. No vague terms?..."
**Citation**: D3 #13 (R13): "For rapid assessment" redundant with header. D3 #14-15 (R11): negative questions. With criteria inlined, this checklist is pure duplication. Replace with a one-line directive: "For quick evaluation, check only the MUST and MUST_NOT criteria."

### CUT-3: "Reference Files" section (lines 159-164, ~80t)
**Quoted**: "@../../references/evaluation-criteria.md -- it covers complete criteria tables..."
**Citation**: D3 #4, #7 (R13): "it covers" padding. D3 #19 (R15): inconsistent reference formats. With all references inlined, this section is an orphan.

### CUT-4: "Example Evaluation" section (lines 168-169, ~25t)
**Quoted**: "See examples/sample-evaluation.md for a complete evaluation report example."
**Citation**: D3 #10 (R18): redundant "example." No such file exists in the repository. Dead reference.

### CUT-5: "Notes" section (lines 172-176, ~50t)
**Quoted**: "Evaluation is against Anthropic's official guidance... Use the prompt-optimize skill to fix identified issues"
**Citation**: D3 #24 (R13): "identified" redundant. First bullet is D2 Core Point #1 -- move to opening line. Second duplicates Category Applicability. Third duplicates Score Interpretation. Fourth becomes a single line in report template.

### CUT-6: Step 2 as standalone section (lines 36-48, ~80t)
**Quoted**: "Step 2: Determine Applicable Categories / Reference @../../references/evaluation-criteria.md..."
**Citation**: D3 #25 (R15): inconsistent list styles. With criteria inlined, the Category Applicability table is already present. Merge into Step 1.

### CUT-7: Score Interpretation table as standalone section (lines 148-156, ~40t)
**Quoted**: "## Score Interpretation / 90-100 Excellent..."
**Citation**: D3 #20. Inline as a comment in the report template header.

**Total cuts from existing body: ~455t**

## Restructure

### R1: Front-load the grounding principle
**Citation**: D4: "Missing explicit 'when is evaluation complete' statement." D2 Core Point #1.
Open body with: "Evaluate Claude system prompts against Anthropic's official criteria. Rank violations by severity and produce a structured report."

### R2: Collapse 5-step workflow to 3 steps
**Citation**: D4 recommendation #1: "Add detailed iteration mechanics to Step 3."
1. **Classify**: Read the prompt. Determine type (API/Agent/Skill) and applicable categories per the Applicability table below.
2. **Evaluate**: For each applicable category, check every criterion against the prompt. Record each violation: criterion ID, severity, line location, quoted text. Scan the anti-pattern catalog. Check ordering against canonical table.
3. **Score and Report**: Calculate score per formula. Generate report per template below. To fix issues, invoke `/prompt-optimize`.

### R3: Move Output Format template to end of body
**Citation**: Ordering-guide.md position 9: output format near end for recency effect.

### R4: Inline Score Interpretation into report template
**Citation**: D3 #20. Compress to comment: `<!-- 90-100 Excellent | 75-89 Good | 60-74 Adequate | 40-59 Needs Work | 0-39 Poor -->`

## Strengthen

### S1: Active voice for Step 1
**Citation**: D3 #3 (R12).
**Before**: "Read the prompt to evaluate (user provides path or content)"
**After**: "Read the prompt the user provides (file path or pasted text)."

### S2: Active voice for violation recording
**Citation**: D3 #5 (R10).
**Before**: "For violations, record:"
**After**: "Record each violation:"

### S3: Positive form in quick-eval
**Citation**: D3 #14-15 (R11).
Quick-eval mode replaced with: "For quick evaluation, check only MUST and MUST_NOT criteria."

### S4: Emphatic end position
**Citation**: D3 #9 (R18).
**Before**: "Produce a structured evaluation report with severity-ranked findings and actionable recommendations."
**After**: "Rank violations by severity and produce a structured report."

### S5: Remove "it covers" padding
**Citation**: D3 #4, #7 (R13). All `@` references eliminated; content is now inline.

## Hook/Command Splits

No splits recommended. Evaluation requires LLM judgment at every step (classify, assess criteria, score). Per hooks-full-spec.md section 13: "Use hooks for deterministic enforcement" -- no deterministic component here. The D4 finding about `tools: [Read]` frontmatter is a frontmatter change, not a hook/command split.

## Projected Token Delta

**Before (body + refs combined)**: 1250t (body) + 11408t (refs loaded via @) = 12658t total on invocation

**After (new self-contained body)**: 
- Restructured workflow: ~800t (down from 1250t after cuts, up slightly for mechanics)
- Inlined evaluation-criteria.md: ~1400t (compressed from 2355t)
- Inlined anti-patterns.md: ~900t (compressed from 2323t)
- Inlined term-blacklists.md: ~550t (compressed from 1566t)
- Inlined ordering-guide.md: ~350t (compressed from 1649t)
- Report template: ~200t (carried forward, slightly trimmed)
- **New body total: ~4200t**

**Net reduction**: 12658t -> ~4200t = **-67% total context on invocation**

**Key difference from previous synthesis**: Previous synthesis deferred 4 of 5 references to lazy loading (keeping body at ~4800t but with refs as separate files that models ignore). This synthesis inlines ALL needed reference content (compressed), producing a larger body (~4200t) but eliminating ALL external file dependencies. The skill is now self-contained. No Read calls needed to function. improvement-patterns.md removed entirely (belongs to prompt-optimize).

**Three-filter verification**:
1. CITATION: Every recommendation cites a D1/D2/D3/D4 finding or bridge research criterion. Verified above.
2. NET TOKEN REDUCTION: 12658t -> ~4200t = -67%. Body grows from 1250t to ~4200t, but total (body+refs) shrinks by 8458t.
3. NO HEDGING: All directives are imperative. No "consider", "might", "could possibly".
