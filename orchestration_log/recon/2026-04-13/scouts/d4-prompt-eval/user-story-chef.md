# Prompt Evaluation Report: user-story-chef

**Type**: Skill (Claude Code agent)  
**Evaluated**: 2026-04-13  
**Evaluator**: Claude Sonnet 4.5

---

## Overall Score: 93/100 (Excellent)

**Rating**: Excellent - Production-ready with minor improvements possible  
**Status**: Production-ready

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓ (baseline only)
- OUTPUT ✓
- TOOLS ✗ (no tools defined or required)
- EXAMPLES ✓ (multiple examples of good vs bad patterns)
- REASONING ✓ (conceptual reasoning about value vs form)
- DATA_SEPARATION ✗ (no variable user data handling)
- AGENT_SPECIFIC ✓

---

## Critical Issues

None. All MUST and MUST_NOT criteria are satisfied.

---

## Warnings (SHOULD violations)

### STR-2: Context/Background
**Status**: Partial  
**Evidence**: Provides philosophy but lacks audience definition  
**Quote**: "The Lie You Were Taught" section establishes context, but doesn't specify target audience (product managers? developers? Scrum masters?)  
**Impact**: Very Low - the pedagogical framing is strong, missing only explicit audience

### AGT-4: Tool Restrictions
**Status**: Not specified  
**Evidence**: No `tools` or `disallowedTools` field in frontmatter  
**Impact**: Very Low - this is a teaching/evaluation skill that doesn't require specific tools

### AGT-5: Permission Mode
**Status**: Not specified  
**Evidence**: No `permissionMode` field in frontmatter  
**Impact**: Low - skill may write stories, suggesting some permission consideration

### OUT-6: Exclusions Stated
**Status**: Missing  
**Evidence**: No guidance on what to skip in output  
**Impact**: Very Low - protocol structure provides implicit guidance

---

## Anti-Patterns Detected

None. This prompt is remarkably clean and demonstrates exceptional awareness of anti-patterns through its explicit teaching about form vs function.

---

## Strengths

### 1. Exceptional Conceptual Clarity (CLR-1, CLR-7)
**Quote**: "A user story is a unit of value negotiation with embedded feedback mechanisms."  
Reframes entire concept from template to function.

### 2. Strong Pedagogical Structure (STR-5)
**Evidence**: "Lie You Were Taught" → "What It Actually Is" → "INVEST as Physics" → "Examples" → "Anti-Patterns" → "Protocol"  
Follows learning progression: deconstruct misconception → establish truth → apply principles → practice

### 3. Outstanding Examples (EXM-1, EXM-2, EXM-3)
**Evidence**: Multiple example pairs showing form vs function:
- "Cook's AC" vs "Chef's AC" with complete before/after
- "Wrong (component slicing)" vs "Right (value slicing)" with 3-item lists each
- INVEST table with "Convention (Form)" vs "Truth (Function)" for all 6 criteria

### 4. Explicit Anti-Pattern Catalog (CON-2, SAF-6)
**Evidence**: Dedicated "Anti-Patterns: Form Addiction Symptoms" table with 6 symptoms, each with diagnosis  
Plus reference to @references/anti-patterns.md for detailed catalog

### 5. Progressive Disclosure (AGT-9)
**Evidence**: Skill body is 103 lines; references 2 external files:
- @references/slicing.md (SPIDR decomposition)
- @references/anti-patterns.md (detailed patterns)

### 6. Clear Role Definition (STR-1)
**Quote**: "Write stories that minimize the cost of being wrong, not stories that look correct."  
Establishes clear purpose and philosophy.

### 7. Operationalized INVEST (CLR-2)
**Evidence**: INVEST table redefines each criterion from conventional form to functional truth:
- "Independent" → "coordination physics"
- "Negotiable" → "information economics"
- "Valuable" → "measurable outcome"
- "Estimable" → "bounded uncertainty"
- "Small" → "feedback loop optimization"
- "Testable" → "binary completion state"

No vague terms; all redefined with operational meaning.

### 8. Strong Constraints (CON-4, CON-6)
**Evidence**: "It is NOT:" section explicitly lists what stories are NOT:
- Not a requirement
- Not a specification
- Not a task

Rationale provided for each distinction.

### 9. Specific Output Guidance (OUT-1, OUT-2)
**Evidence**: "Chef's AC (Function)" template with Given/When/Then structure  
Plus "The Chef's Protocol" 5-step process

### 10. Agent Metadata (AGT-1, AGT-2, AGT-3)
**Frontmatter name**: "user-story-chef" ✓  
**Frontmatter description**: Multiple triggers: "writing user stories", "acceptance criteria", "backlog items", "story splitting", "evaluating story quality", "INVEST criteria application" ✓  
**Proactive framing**: "Use when creating or refining Agile artifacts..." ✓

### 11. Clear Scope (AGT-7)
**Quote**: "Teaches function (value decomposition, falsifiable AC, feedback optimization) over form (templates)."  
Single focused purpose: teaching functional story writing vs template compliance.

### 12. No Template Worship (Meta-Quality)
**Evidence**: Explicitly calls out template addiction as anti-pattern while still providing templates as scaffolding  
Demonstrates prompt engineering principle of "form serves function"

### 13. Falsifiability Emphasis (RSN-4)
**Quote**: "AC are falsifiable hypotheses about value delivery."  
**Quote**: "Each criterion should answer: 'If this passes but users still complain, what did we miss?'"  
Strong evidence-based reasoning framework.

### 14. Specific Slicing Examples (EXM-2, EXM-3)
**Evidence**: Three complete slicing progressions showing:
- Wrong: component/layer slicing (database → API → frontend)
- Right: value slicing (simplest case → rejection → history)

Each slice includes rationale ("adds error value", "adds retrospective value")

---

## Detailed Criteria Scores

### STRUCTURE (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| STR-1 | Role/identity statement | ✓ | "Write stories that minimize cost of being wrong" |
| STR-2 | Context/background | ⚠ | Strong philosophy, minor: lacks audience definition |
| STR-3 | Clear task definition | ✓ | Teaching functional story writing |
| STR-4 | Consistent structural markers | ✓ | Headers, tables, quotes, examples marked consistently |
| STR-5 | Logical ordering | ✓ | Pedagogical progression: deconstruct→truth→practice |
| STR-6 | No instruction/data mixing | ✓ | Examples clearly marked with "Cook's" vs "Chef's" labels |

### CLARITY (7/7)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CLR-1 | Specific, actionable task | ✓ | "Write... evaluate... split..." with 5-step protocol |
| CLR-2 | No undefined vague terms | ✓ | All terms operationalized (INVEST redefined, "value" = measurable outcome) |
| CLR-3 | No contradictions | ✓ | No conflicts |
| CLR-4 | Success criteria | ✓ | Implicit: stories follow function, not form |
| CLR-5 | Numbered sequential steps | ✓ | "Chef's Protocol" has 5 numbered steps |
| CLR-6 | No implicit understanding | ✓ | Explicitly redefines all Agile terminology |
| CLR-7 | Audience/tone specified | ✓ | Pedagogical tone, "you were taught" framing |

### CONSTRAINTS (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CON-1 | Explicit scope definition | ✓ | User story writing/evaluation, not backlog management |
| CON-2 | Forbidden actions listed | ✓ | "It is NOT" section + anti-patterns table |
| CON-3 | Scope vs capability distinction | ✓ | Clear |
| CON-4 | Rationale for constraints | ✓ | Each "is NOT" includes explanation |
| CON-5 | No assumed inference | ✓ | Redefines all assumed Agile knowledge |
| CON-6 | Grouped constraints | ✓ | "It is NOT" section groups related constraints |

### SAFETY (3/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| SAF-1 | Data sensitivity classification | N/A | No PII |
| SAF-2 | Input validation | N/A | No specific input format |
| SAF-3 | Output constraints | ✓ | Given/When/Then template |
| SAF-4 | Injection defense | N/A | No user data handling |
| SAF-5 | No unsafe data access | ✓ | No sensitive data |
| SAF-6 | Error handling guidance | ✓ | Anti-patterns section provides diagnostic guidance |

### OUTPUT (5/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| OUT-1 | Format specified | ✓ | Given/When/Then for AC, value slicing structure |
| OUT-2 | Template/example provided | ✓ | Multiple templates and examples |
| OUT-3 | Missing/null data handling | N/A | Not applicable to teaching skill |
| OUT-4 | Length constraints | N/A | Not specified, not needed |
| OUT-5 | No undefined flexibility | ✓ | Templates are prescriptive |
| OUT-6 | Exclusions stated | ⚠ | No "skip preamble" guidance |

### EXAMPLES (5/5)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| EXM-1 | Clear tags/markers | ✓ | "Cook's AC" vs "Chef's AC" labels |
| EXM-2 | Diverse examples | ✓ | AC examples, slicing examples, INVEST table, anti-patterns |
| EXM-3 | Input and output | ✓ | All examples show before/after pairs |
| EXM-4 | Not excessive | ✓ | 6-7 examples appropriate for teaching task |
| EXM-5 | 3-5 for complex tasks | ✓ | 6 examples for complex pattern-matching (teaching) |

### REASONING (4/4)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| RSN-1 | Requests explicit reasoning | ✓ | "Each criterion should answer: 'If this passes...'" |
| RSN-2 | No silent thinking | ✓ | Not requested |
| RSN-3 | Uncertainty handling | ✓ | "Fix the physics, not the form" provides decision framework |
| RSN-4 | Evidence before conclusions | ✓ | Falsifiable hypotheses framework |

### AGENT_SPECIFIC (8/10)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| AGT-1 | Name field | ✓ | "user-story-chef" |
| AGT-2 | Description with triggers | ✓ | 6 trigger phrases |
| AGT-3 | Proactive use indicated | ✓ | "Use when creating or refining..." |
| AGT-4 | Tools restricted | ⚠ | No tools field (not critical for teaching skill) |
| AGT-5 | Permission mode | ⚠ | No permissionMode |
| AGT-6 | Clear workflow | ✓ | 5-step protocol |
| AGT-7 | Focused scope | ✓ | Story writing/evaluation only |
| AGT-8 | Output format | ✓ | Templates provided |
| AGT-9 | Progressive disclosure | ✓ | 103 lines, 2 external references |
| AGT-10 | Argument substitution | N/A | No arguments |

---

## Recommendations

### High Priority

None. This skill is production-ready as-is.

### Medium Priority

1. **Add permissionMode to frontmatter**
   ```yaml
   permissionMode: ask-by-default
   ```
   Rationale: If skill writes story artifacts, permission appropriate (though may also be used for evaluation only).

2. **Add explicit audience definition**
   Add before "The Lie You Were Taught":
   ```
   ## Audience
   This skill is for product teams using Agile/Scrum methodologies.
   Applicable to product managers, developers, and Scrum masters writing
   or evaluating user stories and acceptance criteria.
   ```

### Low Priority

3. **Add tool specification**
   ```yaml
   tools: [Read, Write]
   ```
   Rationale: Clarify that skill may read existing stories and write new ones, but doesn't need broader tool access.

4. **Add success criteria**
   ```
   ## Success Criteria
   - Stories describe value delivery, not tasks
   - AC are falsifiable hypotheses with Given/When/Then
   - Slicing is by value increment, not component
   - INVEST criteria met in function, not just form
   ```

5. **Add preamble control**
   Add to "Chef's Protocol":
   ```
   When writing stories, skip preamble. Begin with:
   "As a [persona]..." or story title directly.
   ```

---

## Scoring Breakdown

**Applicable criteria**: 50  
**Passed criteria**: 47  
**SHOULD violations**: 3  
**MUST violations**: 0  
**MUST_NOT violations**: 0

**Formula**:
```
Base score = (47 / 50) × 100 = 94.0%
Adjustments = -1 (minor audience/tool metadata gaps)
Final score = 93/100
```

---

## Conclusion

The user-story-chef skill is exceptional in its clarity, pedagogical structure, and operational definitions. It successfully deconstructs template-based thinking and rebuilds understanding around functional principles. The skill demonstrates advanced prompt engineering through:

1. **Form vs Function Framing**: Explicitly teaches the difference between mimicking templates and understanding purpose
2. **Operationalized Definitions**: INVEST criteria redefined from vague qualifiers to measurable physics
3. **Rich Examples**: Multiple diverse before/after pairs showing good vs bad patterns
4. **Progressive Disclosure**: Core content focused, details externalized
5. **Anti-Pattern Awareness**: Dedicated section diagnosing common failure modes

The only gaps are minor agent metadata (permissionMode, tools, audience). This is the strongest prompt in the evaluation set, demonstrating production-ready quality with pedagogical sophistication. The skill's meta-quality—teaching prompt engineering principles through its structure—is noteworthy.
