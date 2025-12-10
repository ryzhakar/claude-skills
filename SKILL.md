---
name: defensive-planning
description: |
  Write implementation plans, assessments, and corrections for implementers who may cut corners.
  Use when: (1) creating implementation plans for peers/subordinates/contractors, (2) reviewing
  implementations for adherence, (3) writing correction plans after failures, (4) any situation
  where the implementer is assumed to be no better than you—possibly lazier, prone to shortcuts,
  or incentivized to appear done rather than be done. This skill produces prescriptive documents
  with verification gates, forbidden patterns, and zero escape hatches.
---

# Defensive Planning

Create implementation plans that survive contact with unreliable implementers.

## Core Assumption

The implementer will optimize for "appears done" over "is done." They will:
- Find every escape hatch and use it
- Interpret ambiguity in their favor
- Mark tasks complete when tests pass, ignoring semantic correctness
- Copy-paste without understanding
- Write `pass` or `TODO` and move on
- Read "option A or B" and pick whichever is less work

**Plan accordingly.**

## Three Document Types

### 1. Implementation Plan
Written BEFORE work begins. Prescribes exactly what to build.

### 2. Adherence Assessment
Written AFTER implementation. Evaluates what was actually built.

### 3. Correction Plan
Written after assessment reveals failures. Prescribes exact fixes.

---

## Writing Implementation Plans

### Structure

```markdown
# Implementation Plan: [Name]

## Preamble
Why this plan exists. What problem it solves.

## Phase N: [Name]
### Why This Matters
Business/technical justification.

### What You Must Do
Exact steps. No decisions for implementer.

### Verification Gates
Commands that MUST produce exact output.

---
## Forbidden Patterns
Explicit list of BANNED code/approaches.

## Definition of Done
Numbered checklist. Binary pass/fail.
```

### Rules for Writing Plans

**Rule 1: No Decisions**
Never write "decide whether X or Y." Pick one. Write it down.

```markdown
# BAD
Decide whether to use Redis or in-memory caching.

# GOOD
Use Redis. Connection config in `config/redis.py`.
```

**Rule 2: No Options**
Never offer alternatives. Each alternative is an escape hatch.

```markdown
# BAD
You can either:
- Make the field required, OR
- Use a sentinel value, OR
- Add validation

# GOOD
Make the field required. Add validator:
[exact code]
```

**Rule 3: Exhaustive Field Lists**
When specifying changes across files, list EVERY file and EVERY field.

```markdown
# BAD
Apply the same pattern to all schema files.

# GOOD
**schema_a.py:**
- `field_x: list[str]` — REQUIRED, add validator
- `field_y: int` — REQUIRED, no default

**schema_b.py:**
- `field_x: list[str]` — REQUIRED, add validator
```

**Rule 4: Verification Gates, Not Checklists**
Replace subjective checklists with executable commands.

```markdown
# BAD
- [ ] Ensure no empty list defaults remain

# GOOD
**Gate: No empty list defaults**
```bash
grep -n "= \[\]" src/schemas/*.py
```
**REQUIRED OUTPUT:** Zero matches.
```

**Rule 5: Exact Output Specifications**
Every verification command specifies exact expected output.

```markdown
**Gate: Tests pass**
```bash
pytest tests/ -v 2>&1 | tail -3
```
**REQUIRED OUTPUT:** Must contain "passed" and "0 failed"
```

**Rule 6: Forbidden Patterns Section**
Explicitly ban patterns they'll be tempted to use.

```markdown
## Forbidden Patterns

### BANNED: Default empty lists
```python
# BANNED
items: list[str] = []
```

### BANNED: pass statements
```python
# BANNED
if condition:
    pass  # TODO
```
```

**Rule 7: No Implicit Behavior**
If a default means something, it's implicit. Ban it.

```markdown
# BAD (implicit: empty means "all")
categories: list[str] = []

# GOOD (explicit: must specify)
categories: list[str]  # Required, validated non-empty
```

---

## Writing Adherence Assessments

### Structure

```markdown
# Implementation Adherence Report

## Executive Summary
One paragraph: Did it work? What's broken?

## Part 1: Spirit Assessment
Evaluate against pre-plan principles/decisions.

## Part 2: Plan Point-by-Point
Phase-by-phase: ADHERED / PARTIALLY ADHERED / VIOLATED

## Part 3: Quantified Findings
| Metric | Value | Assessment |
Table of measurable outcomes.

## Part 4: Critical Violations
Numbered list requiring immediate fix.

## Conclusion
Overall verdict. Recommended action.
```

### Assessment Rules

**Rule 1: Test Semantic Correctness**
"Tests pass" means nothing. Check actual behavior.

```bash
# Don't just run tests. Verify output content:
python -c "
result = function_under_test()
assert 'expected_content' in result, 'Semantic failure'
"
```

**Rule 2: Quantify Everything**
Replace "mostly works" with numbers.

```markdown
# BAD
Most schemas have validation.

# GOOD
| Schemas with validation | 3/8 (37.5%) |
```

**Rule 3: Severity Levels**
- **CRITICAL**: Feature is broken/missing. Blocks usage.
- **HIGH**: Feature works incorrectly. Produces wrong results.
- **MODERATE**: Inconsistency or maintainability issue.
- **LOW**: Style or documentation issue.

---

## Writing Correction Plans

### Structure

```markdown
# Correction Plan

## Preamble
What went wrong. Why this plan exists.

## Failure Modes Observed
Categorize the shortcuts/mistakes found.

## Phase CN: [Fix Name]
### Why This Matters
### What You Must Do
### Verification Gates

## Forbidden Patterns
Same as implementation plan—but now they've proven they'll use these.

## Final Warning
Explicit statement that previous failure mode will not be tolerated.
```

### Correction-Specific Rules

**Rule 1: Name Their Failure Modes**
Document the patterns they actually used, not hypothetical ones.

```markdown
## Failure Modes Observed

### FM-1: "It Runs, Therefore It Works"
You wrote code that executes without testing semantic output.
Evidence: Q041 returns category averages instead of SKU matches.

### FM-2: "The Flag Is There"
You added `match_needed` field but never implemented behavior.
Evidence: `match_needed=True` produces identical SQL to `False`.
```

**Rule 2: Close Their Specific Escape Hatches**
Whatever they exploited, explicitly forbid it.

```markdown
# They used "at least one of" validation to avoid required fields
### BANNED: "At least one of" validation
```python
# BANNED - they will make everything optional
if not self.a and not self.b and not self.c:
    raise ValueError("At least one of...")
```
```

**Rule 3: Prescriptive, Not Consultative**
Don't explain options. Give orders.

```markdown
# BAD (consultative)
Consider whether the field should be required or optional.

# GOOD (prescriptive)
Make the field required. Here is the exact code:
[code block]
```

**Rule 4: More Gates, More Specific**
If they failed a check, add more checks.

```markdown
# Original gate they passed while semantically broken:
pytest tests/  # They wrote bad tests

# New gates that catch semantic issues:
uv run python -c "
sql = query.translate()
assert 'id_mapping' in sql, 'Join missing'
assert 'source_id' in sql, 'Join columns missing'
"
```

---

## Anti-Patterns in Planning

### Anti-Pattern: Offering Alternatives
Every "or" is a door to the easy path.

### Anti-Pattern: "If Needed" Language
"Add base class if needed" → They won't add it.

### Anti-Pattern: Subjective Verification
"Ensure code is clean" → Unverifiable.

### Anti-Pattern: Trust-Based Checklists
"[ ] Verify all edge cases" → They'll check without verifying.

### Anti-Pattern: Explaining Instead of Prescribing
Long explanations get skimmed. Code blocks get copied.

---

## Quick Reference: Gate Commands

```bash
# No banned patterns
grep -n "PATTERN" path/to/files/*.py
# REQUIRED: Zero matches

# Tests pass
pytest path/ -v 2>&1 | tail -3
# REQUIRED: Contains "passed", no "failed"

# Specific content in output
python -c "
from module import thing
result = thing()
assert 'expected' in result, 'FAIL: expected not found'
print('PASS')
"
# REQUIRED: "PASS"

# File structure exists
ls -la expected/path/
# REQUIRED: Lists expected files

# No implicit defaults
grep -c "= \[\]\|= None" src/*.py
# REQUIRED: 0
```

---

## Remember

The implementer optimizes for completion, not correctness.
Your plan must make "appearing done" harder than "being done."

Every escape hatch will be used.
Every ambiguity will be resolved in favor of less work.
Every subjective check will pass without verification.

Plan defensively.
