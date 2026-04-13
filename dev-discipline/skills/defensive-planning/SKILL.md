---
name: defensive-planning
description: >
  Write implementation plans, assessments, and corrections for implementers who may cut corners.
  Use when: creating implementation plans, reviewing implementations for adherence, writing
  correction plans after failures, or when the implementer may choose appearing done over being done.
  Produces prescriptive documents with verification gates, forbidden patterns, and zero escape hatches.
---

# Defensive Planning

Create implementation plans that survive contact with unreliable implementers.

## Core Assumption

The implementer will choose appearing done over being done. They will:
- Find every escape hatch and use it
- Interpret ambiguity in their favor
- Mark tasks complete when tests pass, ignoring semantic correctness
- Copy-paste without understanding
- Write `pass` or `TODO` and move on
- Read "option A or B" and pick whichever is less work

**Plan accordingly.**

## Three Document Types

### 1. Implementation Plan
Write BEFORE work begins. Prescribes exactly what to build.

### 2. Adherence Assessment
Write AFTER implementation. Evaluates what was actually built.

### 3. Correction Plan
Write after assessment reveals failures. Prescribes exact fixes.

---

## Writing Implementation Plans

### Structure

```markdown
# Implementation Plan: [Name]

## Preamble
What problem this solves.

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
Never write "decide whether X or Y." Pick one.

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

**Rule 7: Make All Behavior Explicit**
If a default means something, it's implicit. Ban it.

```markdown
# BAD (implicit: empty means "all")
categories: list[str] = []

# GOOD (explicit: must specify)
categories: list[str]  # Required, validated non-empty
```

### TDD Micro-Task Structure

For plans targeting TDD workflows, structure each task as a 2-5 minute red-green cycle with checkbox tracking:

- **Files:** List exact paths to create, modify, and test
- **Step 1:** Write failing test (include test code)
- **Step 2:** Run test, verify it fails (include command and expected failure)
- **Step 3:** Write minimal implementation (include code)
- **Step 4:** Run test, verify it passes (include command and expected output)
- **Step 5:** Commit (include exact git commands)

Never batch all tests then all implementation (horizontal slicing produces tests verifying imagined behavior).

**File decomposition before tasks:** Map which files will be created or modified. Each file has one responsibility. Files that change together live together. Each task produces self-contained changes.

**Plan self-review after writing:**
1. Spec coverage: point each requirement to the task implementing it. List gaps.
2. Placeholder scan -- all are plan failures: "TBD", "TODO", "implement later", "add appropriate error handling", "similar to Task N", steps without code blocks, references to undefined types/functions.
3. Type consistency: verify names and signatures in later tasks match what earlier tasks defined.

### Module Design Heuristics

**Deep modules:** Encapsulate complex functionality behind a simple interface. Ask: can I reduce the number of methods? Simplify parameters? Hide more complexity inside? Shallow modules (large interface, thin implementation) create overhead without encapsulation.

**Testability as decomposition criterion:** Module boundaries should coincide with testability boundaries. A module that accepts dependencies (not creates them), returns results (not side effects), and has a small surface area is testable through its public interface alone.

**Testing decisions section in plans:**

```markdown
## Testing Decisions
- Tests verify behavior through public interfaces, not implementation details
- Tests survive internal refactoring
- Modules tested: [Module A] -- [behaviors]; [Module B] -- [behaviors]; [Module C] -- not tested (justification)
- Test runner, naming convention, prior art paths
```

This runs before task decomposition: file structure identifies modules, deep-modules heuristic evaluates interfaces, testability confirms each module can be tested through its interface.

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
Passing tests prove nothing about semantic correctness. Verify function output matches specification.

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
- **CRITICAL**: Feature is broken or missing. Blocks usage.
- **HIGH**: Feature works incorrectly. Produces wrong results.
- **MODERATE**: Feature works but has issues. Creates inconsistency or maintainability debt.
- **LOW**: Minor quality issues. Affects style or documentation.

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
Every "or" lets implementers choose the easier option.

### Anti-Pattern: "If Needed" Language
Conditional language ("if needed") invites omission.

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

## Plan Execution Protocol

### Pre-Execution Review Gate

Before starting implementation: read the plan completely, identify questions or gaps, raise concerns with the user BEFORE starting. A plan that looked good during writing may reveal gaps from an executor's perspective.

### Task State Tracking

Track each task: `not_started -> in_progress -> completed | blocked`. Use markdown checkboxes. Mark completed only after all verification gates pass.

### Blocker Escalation

STOP executing when: hit a missing dependency, test failure contradicts plan, instruction is ambiguous, verification gate fails 2+ times. Ask for clarification rather than guessing. Report: which task, what is failing, what was attempted, what is needed.

### Two-Stage Review Ordering

After each task:
1. **Spec compliance first:** verify implementation matches specification line by line. Do not trust self-reports.
2. **Code quality second (only after Stage 1 passes):** verify quality, testing, architecture. Categorize: Critical / Important / Minor.

Reviewing quality before confirming spec compliance wastes effort -- polishing code that does not meet requirements is wasted work.

### Status-Driven Branching

| Status | Action |
|---|---|
| DONE | Proceed to spec compliance review |
| DONE_WITH_CONCERNS | Read concerns; address if about correctness, note if observations |
| NEEDS_CONTEXT | Provide missing context and re-dispatch |
| BLOCKED | Assess: context problem, reasoning problem, task too large, or plan wrong |

---

Every escape hatch will be used.
Every ambiguity will be resolved in favor of less work.
Every subjective check will pass without verification.

Plan defensively.

---

*Enhanced with patterns from writing-plans and executing-plans, and write-a-prd. Adapted and enhanced for this plugin.*
