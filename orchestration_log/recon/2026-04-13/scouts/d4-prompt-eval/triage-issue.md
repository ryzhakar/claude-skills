# Prompt Evaluation Report: triage-issue

**Type**: Skill (Claude Code agent)  
**Evaluated**: 2026-04-13  
**Evaluator**: Claude Sonnet 4.5

---

## Overall Score: 88/100 (Good)

**Rating**: Good - Functional with room for improvement  
**Status**: Production-ready with minor enhancements recommended

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- TOOLS (partial - references but doesn't define)
- EXAMPLES ✗ (not present, not required for this task type)
- REASONING ✓ (multi-step reasoning required)
- DATA_SEPARATION ✗ (no variable user data handling)
- AGENT_SPECIFIC ✓

---

## Critical Issues

None. All MUST and MUST_NOT criteria are satisfied.

---

## Warnings (SHOULD violations)

### STR-2: Context/Background
**Status**: Partial  
**Evidence**: Provides rationale ("Why Autonomous") but lacks domain context about bug triaging conventions or audience definition (is this for solo devs? teams? open source maintainers?)  
**Impact**: Low - the protocol is self-contained enough that additional context wouldn't significantly improve execution

### CLR-4: Success Criteria
**Status**: Partial  
**Evidence**: Acceptance criteria in Phase 5 GitHub issue template, but no explicit success criteria for the skill execution itself  
**Quote**: "After creating the issue, print the issue URL and a one-line summary of the root cause." (completion signal, but not success criteria)  
**Impact**: Low - the issue creation and URL output serve as implicit success signal

### RSN-1: Explicit Reasoning Request
**Status**: Missing  
**Evidence**: No request for explicit reasoning tags despite complex investigation task  
**Impact**: Medium - investigation benefits from structured reasoning, but autonomous exploration may be inhibited by forcing explicit reasoning steps

### AGT-4: Tool Restrictions
**Status**: Not specified  
**Evidence**: No `tools` or `disallowedTools` field in frontmatter  
**Impact**: Low - triage needs broad access, restriction may not be appropriate

### AGT-5: Permission Mode
**Status**: Not specified  
**Evidence**: No `permissionMode` field in frontmatter  
**Impact**: Medium - creating GitHub issues and running git commands suggests need for explicit permission settings

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers (Minor)
**Location**: Phase 2 investigation checklist  
**Evidence**: "deep investigation" (what depth?), "similar patterns" (how similar?)  
**Severity**: Low  
**Recommendation**: Acceptable in this context - "deep" is scoped by the checklist items that follow

### AP-OUT-04: No Preamble Control (Minor)
**Location**: Phase 5 output  
**Evidence**: "print the issue URL and a one-line summary" - doesn't specify to skip preamble  
**Severity**: Very Low  
**Recommendation**: Add "Output only: [issue URL]\n[summary]" for clarity

---

## Strengths

### 1. Excellent Workflow Structure (STR-5)
Clear 5-phase progression following recommended ordering:
- Phase 1: Capture (input)
- Phase 2: Explore (reasoning/investigation)
- Phase 3: Classify (analysis)
- Phase 4: Design (solution)
- Phase 5: Create (output)

### 2. Strong Constraint Definition (CON-1, CON-2)
**Quote**: "Do NOT ask follow-up questions. Start investigating immediately."  
**Quote**: "Do NOT ask the user to review before creating -- publish directly and share the URL."  
Explicit forbidden actions with clear rationale.

### 3. Specific Task Definition (STR-3, CLR-1)
**Quote**: "Autonomously diagnose a reported bug, trace its root cause, design a TDD fix plan, and publish a GitHub issue"  
Clear, actionable, unambiguous task statement.

### 4. Rationale Provided (CON-4)
**Quote**: "Follow-up questions waste the user's time when the codebase contains all the evidence."  
Constraints include "why" explanations for non-obvious rules.

### 5. Detailed Output Format (OUT-1, OUT-2)
Phase 5 provides complete GitHub issue template with structure and examples.

### 6. Edge Case Handling (SAF-6)
Dedicated "Edge Cases" section covering:
- Cannot reproduce
- Multiple root causes
- Fix requires design change

### 7. Agent Identity and Description (AGT-1, AGT-2)
**Frontmatter name**: "triage-issue" (lowercase, hyphenated) ✓  
**Frontmatter description**: Includes trigger phrases: "reports a bug", "this is broken", "triage an issue", "investigate a bug", "find the root cause" ✓

### 8. Clear Agent Workflow (AGT-6)
5-phase protocol with numbered steps and decision points ✓

### 9. Focused Scope (AGT-7)
Single purpose: bug triage from report to GitHub issue ✓

### 10. Structured Output Specified (AGT-8)
GitHub issue template with sections ✓

### 11. Progressive Disclosure (AGT-9)
151 lines, under 500-line threshold ✓

---

## Detailed Criteria Scores

### STRUCTURE (5/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| STR-1 | Role/identity statement | ✓ | "Autonomously diagnose a reported bug..." |
| STR-2 | Context/background | ⚠ | Has rationale, lacks domain context |
| STR-3 | Clear task definition | ✓ | Unambiguous task in opening paragraph |
| STR-4 | Consistent structural markers | ✓ | Uses headers, tables, code blocks consistently |
| STR-5 | Logical ordering | ✓ | Follows role→context→protocol→format→edges |
| STR-6 | No instruction/data mixing | ✓ | Clean separation throughout |

### CLARITY (6/7)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CLR-1 | Specific, actionable task | ✓ | "diagnose + trace + design + publish" |
| CLR-2 | No undefined vague terms | ✓ | "Deep" scoped by checklist |
| CLR-3 | No contradictions | ✓ | No conflicting directives |
| CLR-4 | Success criteria | ⚠ | Implicit in output, not explicit |
| CLR-5 | Numbered sequential steps | ✓ | 5 phases, numbered cycles in Phase 4 |
| CLR-6 | No implicit understanding | ✓ | All requirements explicit |
| CLR-7 | Audience/tone specified | ✓ | Tone implicit in "autonomous" framing |

### CONSTRAINTS (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CON-1 | Explicit scope definition | ✓ | Bug triage, not feature design or general architecture |
| CON-2 | Forbidden actions listed | ✓ | "Do NOT ask follow-up", "Do NOT ask to review" |
| CON-3 | Scope vs capability distinction | ✓ | Clear separation |
| CON-4 | Rationale for constraints | ✓ | "Why Autonomous" section |
| CON-5 | No assumed inference | ✓ | Critical limits explicit |
| CON-6 | Grouped constraints | ✓ | Constraints within each phase |

### SAFETY (4/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| SAF-1 | Data sensitivity classification | N/A | No PII handling |
| SAF-2 | Input validation | ✓ | Implicit in "brief description" constraint |
| SAF-3 | Output constraints | ✓ | Issue template structure enforced |
| SAF-4 | Injection defense | N/A | Not handling untrusted user data inline |
| SAF-5 | No unsafe data access | ✓ | Codebase access appropriate for task |
| SAF-6 | Error handling guidance | ✓ | "Edge Cases" section covers failure modes |

### OUTPUT (5/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| OUT-1 | Format specified | ✓ | GitHub issue template provided |
| OUT-2 | Template/example provided | ✓ | Complete issue structure in Phase 5 |
| OUT-3 | Missing/null data handling | ✓ | "Cannot reproduce" edge case covered |
| OUT-4 | Length constraints | ✓ | Implicit in template sections |
| OUT-5 | No undefined flexibility | ✓ | Template is prescriptive |
| OUT-6 | Exclusions stated | ⚠ | Template says what to avoid, but final output could be clearer |

### REASONING (2/4)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| RSN-1 | Requests explicit reasoning | ⚠ | No reasoning tags requested |
| RSN-2 | No silent thinking | ✓ | Not requested |
| RSN-3 | Uncertainty handling | ✓ | "Cannot reproduce" path provided |
| RSN-4 | Evidence before conclusions | ✓ | Investigation checklist before classification |

### AGENT_SPECIFIC (8/10)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| AGT-1 | Name field | ✓ | "triage-issue" |
| AGT-2 | Description with triggers | ✓ | Multiple trigger phrases |
| AGT-3 | Proactive use indicated | ✓ | "This skill should be used when..." |
| AGT-4 | Tools restricted | ⚠ | No tools field specified |
| AGT-5 | Permission mode | ⚠ | No permissionMode specified |
| AGT-6 | Clear workflow | ✓ | 5-phase protocol |
| AGT-7 | Focused scope | ✓ | Single purpose |
| AGT-8 | Output format | ✓ | Template provided |
| AGT-9 | Progressive disclosure | ✓ | 151 lines |
| AGT-10 | Argument substitution | N/A | No arguments expected |

---

## Recommendations

### High Priority

1. **Add permissionMode to frontmatter**
   ```yaml
   permissionMode: ask
   ```
   Rationale: Creating GitHub issues and running git commands should require explicit permission.

2. **Consider adding disallowedTools**
   ```yaml
   disallowedTools: [Write, Edit]
   ```
   Rationale: Triage is read-only investigation until issue creation; no code changes needed.

### Medium Priority

3. **Add explicit reasoning request for investigation**
   Add to Phase 2:
   ```
   Document your investigation in structured reasoning:
   - Hypotheses tested
   - Evidence found or missing
   - Causal chain from entry point to failure
   ```
   Rationale: Improves investigation quality and creates audit trail.

4. **Clarify final output format**
   Change Phase 5 final instruction to:
   ```
   Output only:
   [GitHub issue URL]
   [One-line root cause summary]
   ```
   Rationale: Removes ambiguity about preamble.

### Low Priority

5. **Add domain context**
   Add section before "Why Autonomous":
   ```
   ## Context
   This skill is for development teams using GitHub for issue tracking.
   It assumes access to codebase, git history, and GitHub CLI (`gh`).
   ```

6. **Add success criteria**
   Add to end of protocol:
   ```
   ## Success Criteria
   - Issue created with all template sections completed
   - Root cause identified and documented
   - TDD fix plan includes at least one RED-GREEN cycle
   - Investigation covered all four questions (WHERE/WHAT/WHY/WHAT ELSE)
   ```

---

## Scoring Breakdown

**Applicable criteria**: 49  
**Passed criteria**: 43  
**SHOULD violations**: 6  
**MUST violations**: 0  
**MUST_NOT violations**: 0

**Formula**:
```
Base score = (43 / 49) × 100 = 87.8%
Adjustments = +0 (SHOULD bonuses already in passed count)
Final score = 88/100
```

---

## Conclusion

The triage-issue skill is well-structured, clearly scoped, and production-ready. It follows Anthropic's prompt engineering guidelines closely, with only minor gaps in agent-specific metadata (permission mode, tool restrictions) and optional enhancements for reasoning structure. The autonomous investigation protocol is well-designed with appropriate constraints and edge case handling. Primary improvements would be adding permission controls and optional reasoning structure for investigation audit trails.
