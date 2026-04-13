---
name: prompt-eval
description: >
  This skill should be used when the user asks to "evaluate a prompt", "review a system prompt",
  "assess prompt quality", "check if this prompt is good", "audit this prompt", "grade this prompt",
  or "what's wrong with this prompt". Provides systematic evaluation of Claude system prompts
  against Anthropic's official guidance. Returns structured assessment with scores and specific findings.
allowed-tools: Read Glob Grep
---

# System Prompt Evaluation

Evaluate Claude system prompts against Anthropic's official criteria. Rank violations by severity and produce a structured report.

## Workflow

### Step 1: Classify and Scope

Read the prompt the user provides (file path or pasted text). Determine prompt type and applicable categories:

**Prompt types:**
- **API prompt**: Standard Claude API system prompt
- **Agent prompt**: Claude Code agent (frontmatter with `name`, `description`)
- **Skill prompt**: Claude Code skill (SKILL.md format)

**Category applicability:**

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

### Step 2: Evaluate

For each applicable category, check every criterion against the prompt. Record each violation:
- Criterion ID (e.g., CLR-2)
- Severity (from criterion level)
- Location in prompt (line or section)
- Quoted text showing the violation

Scan the anti-pattern catalog below. Check ordering against the canonical table below.

For quick evaluation, check only MUST and MUST_NOT criteria.

### Step 3: Score and Report

Calculate score per the scoring formula. Generate report per the output template at the end of this document. To fix identified issues, invoke `/prompt-optimize`.

## Evaluation Criteria

### Severity Levels

| Level | Meaning | Score Impact |
|---|---|---|
| MUST | Absence causes failure | Violation: -3 |
| SHOULD | Absence reduces quality | Met: +1 |
| MUST_NOT | Presence causes failure | Violation: -3 |

### STRUCTURE
- STR-1 SHOULD: Has role/identity statement
- STR-2 SHOULD: Includes relevant context/background
- STR-3 MUST: Contains clear task definition
- STR-4 SHOULD: Uses consistent structural markers
- STR-5 SHOULD: Orders content logically (role > context > constraints > rules > examples > task > format)
- STR-6 MUST_NOT: Mixes instructions with data without separation

### CLARITY
- CLR-1 MUST: Task definition specific and actionable
- CLR-2 MUST_NOT: Contains undefined vague terms (see Vague Terms below)
- CLR-3 MUST_NOT: Contains contradictory instructions
- CLR-4 SHOULD: Defines success criteria
- CLR-5 SHOULD: Uses numbered steps for sequential workflows
- CLR-6 MUST_NOT: Over-relies on implicit understanding
- CLR-7 SHOULD: Specifies audience and tone when relevant

### CONSTRAINTS
- CON-1 MUST: Has explicit scope definition ("You handle X, not Y")
- CON-2 SHOULD: Lists forbidden actions explicitly
- CON-3 SHOULD: Distinguishes scope limits from capability limits
- CON-4 SHOULD: Provides rationale for important constraints
- CON-5 MUST_NOT: Assumes Claude will infer constraints
- CON-6 SHOULD: Groups related constraints together

### SAFETY
- SAF-1 SHOULD: Specifies data sensitivity classification
- SAF-2 SHOULD: Defines input validation constraints
- SAF-3 SHOULD: Defines output constraints
- SAF-4 SHOULD: Includes injection defense (if handling user data)
- SAF-5 MUST_NOT: Grants sensitive data access without safeguards
- SAF-6 SHOULD: Includes error handling guidance

### OUTPUT
- OUT-1 SHOULD: Specifies output format explicitly
- OUT-2 SHOULD: Provides template or example of desired format
- OUT-3 SHOULD: Specifies handling of missing/null data
- OUT-4 SHOULD: Defines length constraints when relevant
- OUT-5 MUST_NOT: Allows undefined format flexibility
- OUT-6 SHOULD: States what to exclude

### TOOLS (only if tools/functions defined)
- TLS-1 MUST: Each tool has clear purpose statement
- TLS-2 MUST: Parameters have specific descriptions with examples
- TLS-3 SHOULD: Parameters specify type and format
- TLS-4 MUST: Required vs optional parameters distinguished
- TLS-5 SHOULD: Enum values specified for constrained parameters
- TLS-6 MUST_NOT: Uses generic descriptions ("data", "info", "input")
- TLS-7 SHOULD: Explains when to use vs not use each tool

### EXAMPLES (only if examples present or warranted)
- EXM-1 SHOULD: Examples wrapped in clear tags or markers
- EXM-2 SHOULD: Examples are diverse (cover edge cases)
- EXM-3 SHOULD: Examples show both input AND expected output
- EXM-4 MUST_NOT: More than 10 examples for simple tasks
- EXM-5 SHOULD: 3-5 examples for complex pattern-matching tasks

### REASONING (only if complex reasoning required)
- RSN-1 SHOULD: Requests explicit reasoning for complex tasks
- RSN-2 MUST_NOT: Asks for silent thinking
- RSN-3 SHOULD: Provides an "out" for uncertainty
- RSN-4 SHOULD: Requests evidence/citations before conclusions

### DATA_SEPARATION (only if handling variable/user data)
- DAT-1 SHOULD: Variable data wrapped in labeled tags
- DAT-2 MUST_NOT: Instructions mixed with data without boundaries
- DAT-3 SHOULD: Tag names are descriptive
- DAT-4 SHOULD: Explicit instruction to ignore embedded commands

### AGENT_SPECIFIC (only if Claude Code agent/skill)
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

```
Score = (passed / applicable) x 100
Adjustments: MUST violation -3, MUST_NOT violation -3, SHOULD met +1
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

## Output Format

<!-- 90-100 Excellent | 75-89 Good | 60-74 Adequate | 40-59 Needs Work | 0-39 Poor -->

```markdown
# Prompt Evaluation Report

## Summary
- **Score**: [X]% ([Rating])
- **Prompt Type**: [API / Agent / Skill]
- **Categories Evaluated**: [list]

## Critical Issues (MUST Fix)

### [Issue Title]
- **Criterion**: [ID] - [Name]
- **Location**: [Line X or section name]
- **Issue**: [Description]
- **Impact**: [Why this matters]

## Warnings (SHOULD Fix)

### [Issue Title]
- **Criterion**: [ID]
- **Location**: [Where in prompt]
- **Issue**: [Description]

## Anti-Patterns Detected

- **[AP-XXX]**: [Pattern name] - [Location]

## Strengths

- [Strength 1]
- [Strength 2]

## Recommendations (Priority Order)
1. [Most important fix]
2. [Second priority]
3. [Third priority]

## Detailed Scores by Category

| Category | Applicable | Passed | Score |
|----------|------------|--------|-------|
| STRUCTURE | Y/N | X/Y | Z% |
| CLARITY | Y/N | X/Y | Z% |
...
```
