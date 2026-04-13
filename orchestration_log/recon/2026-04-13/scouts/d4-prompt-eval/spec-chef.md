# Prompt Evaluation Report: spec-chef

**Type**: Skill (Claude Code agent)  
**Evaluated**: 2026-04-13  
**Evaluator**: Claude Sonnet 4.5

---

## Overall Score: 91/100 (Excellent)

**Rating**: Excellent - Production-ready with minor improvements possible  
**Status**: Production-ready

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- TOOLS ✓ (AskUserQuestion tool referenced)
- EXAMPLES ✓ (question anatomy example provided)
- REASONING ✓ (multi-tier reasoning required)
- DATA_SEPARATION ✗ (no variable user data beyond structured questions)
- AGENT_SPECIFIC ✓

---

## Critical Issues

None. All MUST and MUST_NOT criteria are satisfied.

---

## Warnings (SHOULD violations)

### STR-2: Context/Background
**Status**: Partial  
**Evidence**: Provides rationale ("Why This Works") but lacks audience definition  
**Quote**: "Stakeholders know more than they've written. Documentation has gaps because writers assume context readers lack."  
**Impact**: Very Low - the 5-point rationale is strong, missing only audience definition (product managers? developers? both?)

### AGT-4: Tool Restrictions
**Status**: Not specified  
**Evidence**: No `tools` or `disallowedTools` field in frontmatter  
**Impact**: Low - skill needs broad tool access for exploration, but could restrict Write/Edit until Phase 4

### AGT-5: Permission Mode
**Status**: Not specified  
**Evidence**: No `permissionMode` field in frontmatter  
**Impact**: Medium - writing artifacts and updating project documentation suggests need for permission control

### OUT-6: Exclusions Stated
**Status**: Missing  
**Evidence**: No guidance on what to skip in output  
**Impact**: Very Low - artifact templates provide implicit structure

---

## Anti-Patterns Detected

### AP-EXM-01: Examples Without Outputs (Minor)
**Location**: Phase 3 "Question anatomy"  
**Evidence**: Shows question structure but not stakeholder response or how to handle response  
**Severity**: Very Low  
**Context**: The example demonstrates input format for `AskUserQuestion` tool, not conversation flow, so missing output is acceptable

### AP-CLR-05: Implicit Success Criteria (Minor)
**Location**: No explicit success criteria section  
**Evidence**: Phase 5 mentions "Update project documentation" but no completion signal  
**Severity**: Low  
**Impact**: Success is implicit in artifact creation + indexing

---

## Strengths

### 1. Exceptional Clarity of Purpose (CLR-1, STR-1)
**Quote**: "Transform implicit stakeholder knowledge into explicit artifacts through systematic gap detection and constrained questioning."  
Clear, specific, actionable task statement.

### 2. Strong Rationale Section (STR-2, CON-4)
**Quote**: "Why This Works" section with 5 numbered principles  
Provides both purpose and constraints with rationale.

### 3. Explicit Tool Requirements (TLS-1, TLS-2, TLS-3, TLS-4)
**Evidence**: Dedicated "Tool Requirements" section specifying:
- Tool name: `AskUserQuestion`
- Required parameters: `questions` array, `options` array, `multiSelect`, `header`
- Parameter details: option structure (`label`, `description`)
- Constraints: 1-4 questions, 2-4 options, header ≤12 chars

### 4. Excellent Example Structure (EXM-1, EXM-3)
**Quote**: "Question anatomy:" with structured example showing header, question, options with labels and descriptions  
Clear markers, shows both structure and expected format.

### 5. Progressive Disclosure (AGT-9)
**Evidence**: Skill body is 126 lines; references 4 external files:
- @references/terminology-extraction.md
- @references/gap-heuristics.md
- @references/dependency-tiers.md
- @references/artifact-separation.md  
Excellent use of progressive disclosure to keep core prompt focused.

### 6. Structured Workflow with Dependencies (STR-5, RSN-4)
**Evidence**: Phase 2 dependency mapping with visual tier cascade:
```
Tier 0: Foundation
   ↓
Tier 1: User Model
   ↓
...
```
Shows evidence gathering before artifact creation.

### 7. Clear Constraints (CON-2, CON-6)
**Evidence**: "Anti-Patterns" table with Do/Don't pairs:
- "Ask open-ended questions" → "Offer 2-4 concrete options"
- "Bundle multiple decisions" → "One question per decision"
- "Wait to codify" → "Write artifacts immediately"

### 8. Artifact Separation Table (OUT-1, OUT-2)
**Evidence**: Phase 4 table showing what each artifact contains and does NOT contain  
Prevents common mixing errors.

### 9. Numbered Sequential Steps (CLR-5)
5 phases with clear progression: Analyze → Map → Extract → Codify → Index

### 10. Agent Metadata (AGT-1, AGT-2, AGT-3)
**Frontmatter name**: "spec-chef" ✓  
**Frontmatter description**: Multiple triggers including "analyzing incomplete specs", "stakeholder interviews", "finding documentation gaps" ✓  
**Proactive framing**: "Use when existing documentation has gaps..." ✓

### 11. No Vague Terms (CLR-2)
All qualitative terms are operationalized:
- "Gap" defined by 6 categories with signals
- "Constrained choices" defined as "2-4 options"
- "Tier" defined by dependency structure
- "Immediately" defined as "after each tier (or at most after all tiers complete)"

### 12. Specific Output Format (OUT-1, OUT-4)
**Evidence**: 
- 2-4 options per question
- 1-4 questions per round
- Header ≤12 chars
- Reference to templates in @references/artifact-separation.md

---

## Detailed Criteria Scores

### STRUCTURE (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| STR-1 | Role/identity statement | ✓ | "Transform implicit stakeholder knowledge..." |
| STR-2 | Context/background | ⚠ | Strong rationale, minor: lacks audience definition |
| STR-3 | Clear task definition | ✓ | Specific task in opening line |
| STR-4 | Consistent structural markers | ✓ | Headers, tables, code blocks, references |
| STR-5 | Logical ordering | ✓ | Role→Rationale→Protocol→Tool Requirements |
| STR-6 | No instruction/data mixing | ✓ | Clean separation, example clearly marked |

### CLARITY (7/7)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CLR-1 | Specific, actionable task | ✓ | "Gap detection + constrained questioning + codification" |
| CLR-2 | No undefined vague terms | ✓ | All terms operationalized |
| CLR-3 | No contradictions | ✓ | No conflicts |
| CLR-4 | Success criteria | ✓ | Implicit in Phase 5 indexing |
| CLR-5 | Numbered sequential steps | ✓ | 5 phases |
| CLR-6 | No implicit understanding | ✓ | Process fully explicit |
| CLR-7 | Audience/tone specified | ✓ | Stakeholder-facing questions, artifact-focused |

### CONSTRAINTS (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CON-1 | Explicit scope definition | ✓ | Spec extraction from docs, not greenfield spec writing |
| CON-2 | Forbidden actions listed | ✓ | Anti-Patterns table with "Don't" column |
| CON-3 | Scope vs capability distinction | ✓ | Clear |
| CON-4 | Rationale for constraints | ✓ | "Why This Works" section |
| CON-5 | No assumed inference | ✓ | Explicit guidance throughout |
| CON-6 | Grouped constraints | ✓ | Anti-Patterns table groups related constraints |

### SAFETY (4/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| SAF-1 | Data sensitivity classification | N/A | No PII handling |
| SAF-2 | Input validation | ✓ | Structured questions with options validate input |
| SAF-3 | Output constraints | ✓ | Artifact separation table |
| SAF-4 | Injection defense | N/A | Structured tool use, not free text |
| SAF-5 | No unsafe data access | ✓ | Read existing docs, write new artifacts |
| SAF-6 | Error handling guidance | ✓ | "Other" option escape hatch |

### OUTPUT (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| OUT-1 | Format specified | ✓ | Artifact templates, question structure |
| OUT-2 | Template/example provided | ✓ | Question anatomy + artifact table |
| OUT-3 | Missing/null data handling | ✓ | "Other" option for stakeholder escape |
| OUT-4 | Length constraints | ✓ | Header ≤12 chars, 2-4 options, 1-4 questions |
| OUT-5 | No undefined flexibility | ✓ | Structured formats throughout |
| OUT-6 | Exclusions stated | ⚠ | Minor: no "skip preamble" guidance |

### TOOLS (7/7)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| TLS-1 | Clear purpose statement | ✓ | "AskUserQuestion tool" for constrained choices |
| TLS-2 | Parameters with examples | ✓ | Example shows header, question, options with descriptions |
| TLS-3 | Parameters specify type/format | ✓ | Array types, string lengths specified |
| TLS-4 | Required vs optional | ✓ | "requires" statement + parameter list |
| TLS-5 | Enum values specified | ✓ | multiSelect boolean, header length |
| TLS-6 | No generic descriptions | ✓ | All parameters have specific purpose |
| TLS-7 | When to use tool | ✓ | Phase 3 specifies usage timing |

### EXAMPLES (3/5)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| EXM-1 | Clear tags/markers | ✓ | "Question anatomy:" header + code block |
| EXM-2 | Diverse examples | ⚠ | Only one example, not diverse |
| EXM-3 | Input and output | ⚠ | Shows input structure, not response handling |
| EXM-4 | Not excessive | ✓ | 1 example appropriate for single tool |
| EXM-5 | 3-5 for complex tasks | N/A | Tool usage not complex pattern-matching |

### REASONING (4/4)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| RSN-1 | Requests explicit reasoning | ✓ | Phase 2 dependency mapping IS reasoning structure |
| RSN-2 | No silent thinking | ✓ | Not requested |
| RSN-3 | Uncertainty handling | ✓ | "Other" option provides escape |
| RSN-4 | Evidence before conclusions | ✓ | Analyze (Phase 1) before Extract (Phase 3) |

### AGENT_SPECIFIC (8/10)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| AGT-1 | Name field | ✓ | "spec-chef" |
| AGT-2 | Description with triggers | ✓ | Multiple trigger phrases |
| AGT-3 | Proactive use indicated | ✓ | "Use when existing documentation has gaps..." |
| AGT-4 | Tools restricted | ⚠ | No tools field |
| AGT-5 | Permission mode | ⚠ | No permissionMode |
| AGT-6 | Clear workflow | ✓ | 5-phase protocol |
| AGT-7 | Focused scope | ✓ | Spec extraction only |
| AGT-8 | Output format | ✓ | Artifact templates referenced |
| AGT-9 | Progressive disclosure | ✓ | 126 lines, 4 external references |
| AGT-10 | Argument substitution | N/A | No arguments |

---

## Recommendations

### High Priority

1. **Add permissionMode to frontmatter**
   ```yaml
   permissionMode: ask
   ```
   Rationale: Writing artifacts and updating project documentation should require permission.

### Medium Priority

2. **Add tool restrictions**
   ```yaml
   tools: [Read, Grep, Glob, AskUserQuestion, Write]
   ```
   Rationale: Explicitly list required tools to clarify dependencies and prevent unnecessary tool availability.

3. **Add explicit success criteria**
   ```
   ## Success Criteria
   - All tiers with identified gaps have been questioned
   - Stakeholder selections captured for each question
   - Artifacts written for Product Spec, Personas, User Stories (as applicable)
   - Project documentation updated with artifact references
   ```

### Low Priority

4. **Expand example coverage**
   Add a second example showing how to handle stakeholder response:
   ```
   Example question → stakeholder selects "Medium (50-200)" → 
   captured in artifact: "System supports 50-200 concurrent users (Medium scale)"
   ```

5. **Add audience definition**
   Add to "Why This Works":
   ```
   This skill is for product teams creating specifications from incomplete
   documentation or stakeholder interviews. Assumes access to project docs
   and stakeholder availability via AskUserQuestion tool.
   ```

6. **Add preamble control**
   Add to Phase 4:
   ```
   Write artifacts directly without preamble. Begin each file with its frontmatter
   or first heading.
   ```

---

## Scoring Breakdown

**Applicable criteria**: 56  
**Passed criteria**: 51  
**SHOULD violations**: 5  
**MUST violations**: 0  
**MUST_NOT violations**: 0

**Formula**:
```
Base score = (51 / 56) × 100 = 91.1%
Adjustments = +0
Final score = 91/100
```

---

## Conclusion

The spec-chef skill is exceptionally well-designed with clear structure, comprehensive tool specification, excellent progressive disclosure, and strong operational definitions for all key terms. It excels in defining constrained questioning mechanics, artifact separation, and tier-based dependency mapping. The only notable gaps are agent-specific metadata (permissionMode, tool restrictions) and minor example expansion opportunities. This is one of the strongest prompts in the evaluation set, demonstrating production-ready quality with only metadata enhancements needed. The skill successfully operationalizes all vague terms and provides clear rationale for its approach.
