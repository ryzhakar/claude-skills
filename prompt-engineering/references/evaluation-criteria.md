# System Prompt Evaluation Criteria

Complete criteria reference for evaluating Claude system prompts. Grounded in Anthropic's official documentation.

## Sources

- Claude API Documentation (docs.anthropic.com)
- Claude Code Documentation (code.claude.com)
- Anthropic Prompt Engineering Interactive Tutorial (github.com/anthropics/prompt-eng-interactive-tutorial)

---

## Category Applicability Rules

Before evaluating, determine which categories apply:

| Category | Applies When |
|----------|--------------|
| STRUCTURE | Always |
| CLARITY | Always |
| CONSTRAINTS | Always |
| SAFETY | Always (baseline); enhanced if handles user data |
| OUTPUT | Always if structured output expected |
| TOOLS | Only if tools/functions are defined in prompt |
| EXAMPLES | Only if examples are present OR task complexity warrants them |
| REASONING | Only if multi-step reasoning is required |
| DATA_SEPARATION | Only if prompt handles variable/user-provided data |
| AGENT_SPECIFIC | Only if prompt is a Claude Code agent or skill definition |

---

## Level Definitions

| Level | Meaning | Scoring Impact |
|-------|---------|----------------|
| MUST | Absence causes prompt to fail its purpose | Violation: -3 points |
| SHOULD | Absence reduces quality but prompt still works | Met: +1 point |
| MUST_NOT | Presence causes failure or dangerous behavior | Violation: -3 points |

---

## CORE CATEGORIES (Always Apply)

### STRUCTURE

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| STR-1 | SHOULD | Has explicit role/identity statement | Search for "You are a..." or equivalent persona definition |
| STR-2 | SHOULD | Includes relevant context/background | Check for domain context, business context, audience definition |
| STR-3 | MUST | Contains clear task definition | Verify specific task exists, not just role description |
| STR-4 | SHOULD | Uses consistent structural markers | Check for XML tags, headers, or other consistent delineation |
| STR-5 | SHOULD | Orders content logically (role→context→constraints→rules→examples→task→format) | Verify ordering follows recommended sequence |
| STR-6 | MUST_NOT | Mixes instructions with data/examples without separation | Look for unseparated inline examples or data |

### CLARITY

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| CLR-1 | MUST | Task definition is specific and actionable | Can the task be stated in one unambiguous sentence? |
| CLR-2 | MUST_NOT | Contains undefined vague terms | Search for terms in blacklist (see term-blacklists.md) |
| CLR-3 | MUST_NOT | Contains contradictory instructions | Check for conflicting directives ("be thorough AND concise") |
| CLR-4 | SHOULD | Defines success criteria | Look for explicit acceptance criteria or success definition |
| CLR-5 | SHOULD | Uses numbered steps for sequential workflows | Check if multi-step tasks use numbered lists |
| CLR-6 | MUST_NOT | Over-relies on implicit understanding | Are there unstated assumptions Claude must guess? |
| CLR-7 | SHOULD | Specifies audience and tone when relevant | Check for explicit tone/style guidance |

### CONSTRAINTS

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| CON-1 | MUST | Has explicit scope definition | Look for "You handle X, not Y" or domain boundaries |
| CON-2 | SHOULD | Lists forbidden actions explicitly | Check for "Do NOT...", "Never..." statements |
| CON-3 | SHOULD | Distinguishes scope limits from capability limits | Separate "don't do X" (scope) from "cannot do X" (capability) |
| CON-4 | SHOULD | Provides rationale for important constraints | Check if constraints explain "why" when non-obvious |
| CON-5 | MUST_NOT | Assumes Claude will infer constraints | Are critical limitations explicit or implied? |
| CON-6 | SHOULD | Groups related constraints together | Check constraint organization and grouping |

### SAFETY

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| SAF-1 | SHOULD | Specifies data sensitivity classification | Check for PII handling rules, data classification |
| SAF-2 | SHOULD | Defines input validation constraints | Look for input format requirements, rejection criteria |
| SAF-3 | SHOULD | Defines output constraints | Check for redaction rules, output format limits |
| SAF-4 | SHOULD | Includes injection defense (if handling user data) | Check for data/instruction separation guidance |
| SAF-5 | MUST_NOT | Grants sensitive data access without safeguards | Check if PII/credentials accessed without protection |
| SAF-6 | SHOULD | Includes error handling guidance | Check for "if X fails, do Y" instructions |

### OUTPUT

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| OUT-1 | SHOULD | Specifies output format explicitly | Look for structure definition (JSON, XML, bullets, etc.) |
| OUT-2 | SHOULD | Provides template or example of desired format | Check for sample output showing exact structure |
| OUT-3 | SHOULD | Specifies handling of missing/null data | Check for "if unknown, use X" instructions |
| OUT-4 | SHOULD | Defines length constraints when relevant | Look for word/line/item limits |
| OUT-5 | MUST_NOT | Allows undefined format flexibility | Check for "structure however you prefer" |
| OUT-6 | SHOULD | States what to exclude | Check for "skip preamble", "do not include..." |

---

## CONDITIONAL CATEGORIES (Apply When Relevant)

### TOOLS (Only if tools/functions defined)

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| TLS-1 | MUST | Each tool has clear purpose statement | Tool descriptions state what it does, not just name |
| TLS-2 | MUST | Parameters have specific descriptions with examples | Check for "e.g., San Francisco, CA" style examples |
| TLS-3 | SHOULD | Parameters specify type and format | Look for type definitions, format patterns, enums |
| TLS-4 | MUST | Required vs optional parameters distinguished | Check for explicit `required` marking |
| TLS-5 | SHOULD | Enum values specified for constrained parameters | If limited values, are they enumerated? |
| TLS-6 | MUST_NOT | Uses generic descriptions ("data", "info", "input") | Search for vague parameter names without context |
| TLS-7 | SHOULD | Explains when to use vs not use each tool | Check for conditional usage instructions |

### EXAMPLES (Only if examples present or warranted)

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| EXM-1 | SHOULD | Examples wrapped in clear tags or markers | Check for `<example>` tags or explicit markers |
| EXM-2 | SHOULD | Examples are diverse (cover edge cases) | Do examples show different scenarios? |
| EXM-3 | SHOULD | Examples show both input AND expected output | Are examples complete pairs? |
| EXM-4 | MUST_NOT | More than 10 examples for simple tasks | Count examples relative to task complexity |
| EXM-5 | SHOULD | 3-5 examples for complex pattern-matching tasks | Count examples for complex tasks |

### REASONING (Only if complex reasoning required)

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| RSN-1 | SHOULD | Requests explicit reasoning for complex tasks | Look for "think step by step", reasoning tags |
| RSN-2 | MUST_NOT | Asks for silent thinking | Check for "think silently and output only..." |
| RSN-3 | SHOULD | Provides an "out" for uncertainty | Look for "if unsure, say so" or decline permission |
| RSN-4 | SHOULD | Requests evidence/citations before conclusions | Look for "quote relevant passages first" |

### DATA_SEPARATION (Only if handling variable/user data)

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| DAT-1 | SHOULD | Variable data wrapped in labeled tags | Check for `<data>`, `<input>`, `<user_message>` |
| DAT-2 | MUST_NOT | Instructions mixed with data without boundaries | Could data be misinterpreted as instructions? |
| DAT-3 | SHOULD | Tag names are descriptive | `<email>` vs `<data1>` |
| DAT-4 | SHOULD | Explicit instruction to ignore embedded commands | Check for "ignore instructions in user data" |

### AGENT_SPECIFIC (Only if Claude Code agent/skill)

| ID | Level | Criterion | Check Method |
|----|-------|-----------|--------------|
| AGT-1 | MUST | Has name field (lowercase, hyphenated) | Check frontmatter `name` field |
| AGT-2 | MUST | Has description with trigger keywords | Check `description` includes use-case keywords |
| AGT-3 | SHOULD | Description indicates proactive use | Look for "Use when...", "Use immediately after..." |
| AGT-4 | SHOULD | Tools restricted to minimum necessary | Check `tools` or `disallowedTools` - is it minimal? |
| AGT-5 | SHOULD | Permission mode appropriate for task | Check `permissionMode` matches risk level |
| AGT-6 | MUST | System prompt defines clear workflow | Check markdown body has step-by-step process |
| AGT-7 | MUST_NOT | Agent scope is too broad | Check for single focused purpose |
| AGT-8 | SHOULD | Output format specified | Check for structured output guidance |
| AGT-9 | MUST_NOT | Skill exceeds 500 lines without progressive disclosure | Check line count, look for external references |
| AGT-10 | SHOULD | Uses argument substitution correctly | If arguments expected, check $ARGUMENTS syntax |

---

## Scoring Formula

```
Score = (Σ passed_criteria / Σ applicable_criteria) × 100

Adjustments:
- Each MUST violation: -3 from numerator
- Each MUST_NOT violation: -3 from numerator
- Each SHOULD met: +1 to numerator
```

### Score Interpretation

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100 | Excellent | Production-ready with minor improvements possible |
| 75-89 | Good | Functional with room for improvement |
| 60-74 | Adequate | Works but has notable gaps |
| 40-59 | Needs Work | Significant issues affecting reliability |
| 0-39 | Poor | Major structural or safety problems |

---

## Quick Checklist (Critical Items Only)

For rapid evaluation, check these critical items:

- [ ] Task defined? (STR-3)
- [ ] No vague terms? (CLR-2)
- [ ] No contradictions? (CLR-3)
- [ ] Scope defined? (CON-1)
- [ ] No implicit constraints? (CON-5)
- [ ] No unsafe data access? (SAF-5)
- [ ] No undefined format flexibility? (OUT-5)
- [ ] Data separated from instructions? (DAT-2, if applicable)
- [ ] Agent has workflow? (AGT-6, if applicable)
