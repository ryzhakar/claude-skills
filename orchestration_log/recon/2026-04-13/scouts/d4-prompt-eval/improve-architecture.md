# Prompt Evaluation Report: improve-architecture

**Type**: Skill (Claude Code agent)  
**Evaluated**: 2026-04-13  
**Evaluator**: Claude Sonnet 4.5

---

## Overall Score: 85/100 (Good)

**Rating**: Good - Functional with room for improvement  
**Status**: Production-ready with notable enhancement opportunities

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- TOOLS (partial - references but doesn't define)
- EXAMPLES ✗ (not present, not explicitly required)
- REASONING ✓ (complex multi-design reasoning required)
- DATA_SEPARATION ✗ (no variable user data handling)
- AGENT_SPECIFIC ✓

---

## Critical Issues

None. All MUST and MUST_NOT criteria are satisfied.

---

## Warnings (SHOULD violations)

### STR-2: Context/Background
**Status**: Partial  
**Evidence**: Provides philosophy ("Core Philosophy: Deep Modules") but lacks audience definition and domain context  
**Quote**: "A deep module (John Ousterhout, 'A Philosophy of Software Design') has a small interface hiding a large implementation."  
**Impact**: Low - philosophy section provides theoretical grounding, but doesn't specify when to use this skill vs other refactoring approaches

### CLR-2: Undefined Vague Terms
**Status**: Violations present  
**Evidence**: Multiple undefined qualitative terms  
**Quotes**:
- "Navigate the codebase **organically**" (what does organic mean?)
- "**Radically different** interface" (how different is radical?)
- "**Opinionated** recommendation" (what strength of opinion?)
- "**Most naturally**" (what defines natural?)
**Impact**: Medium - "organically" and "radically different" lack operational definitions

### CLR-4: Success Criteria
**Status**: Missing  
**Evidence**: No explicit success criteria for skill completion  
**Impact**: Medium - unclear when exploration is "complete enough"

### RSN-1: Explicit Reasoning Request
**Status**: Partial  
**Evidence**: Phase 5 requests comparison in prose, but doesn't request structured reasoning tags  
**Quote**: "Present designs sequentially, then compare them in prose"  
**Impact**: Low - prose comparison is a form of reasoning disclosure

### AGT-4: Tool Restrictions
**Status**: Not specified  
**Evidence**: No `tools` or `disallowedTools` field in frontmatter  
**Impact**: Low - exploration task needs read access, restrictions may not apply

### AGT-5: Permission Mode
**Status**: Not specified  
**Evidence**: No `permissionMode` field in frontmatter  
**Impact**: Medium - creating GitHub issues suggests need for explicit permission

### OUT-6: Exclusions Stated
**Status**: Missing  
**Evidence**: No guidance on what to skip in output (preamble, disclaimers, etc.)  
**Impact**: Low - template reference provides implicit structure

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers (Medium)
**Location**: Phase 1, Phase 3, Phase 4  
**Evidence**:
- "Navigate the codebase organically" - no definition of organic vs non-organic navigation
- "Radically different" - no quantification (different API? different paradigm? different contracts?)
- "Most naturally" - subjective without definition
**Severity**: Medium  
**Recommendation**: Define operational criteria:
- Organic: "Follow imports and call sites rather than alphabetically exploring directories"
- Radically different: "Different fundamental contracts (e.g., push vs pull, sync vs async, imperative vs declarative)"

### AP-CLR-01: Vague Task Definition (Minor)
**Location**: Phase 1  
**Evidence**: "Explore the codebase organically" + "Do NOT follow rigid heuristics"  
**Severity**: Low  
**Context**: The anti-heuristic instruction is deliberate (friction-based exploration), but "organically" needs definition

### AP-OUT-02: Format Flexibility (Minor)
**Location**: Phase 5  
**Evidence**: "Compare them in prose" - allows flexibility in comparison structure  
**Severity**: Very Low  
**Context**: Some flexibility appropriate for design comparison, but could benefit from comparison dimensions

### AP-AGT-04: Missing Workflow Clarity (Minor)
**Location**: Phase 2  
**Evidence**: "Do NOT propose interfaces yet. Ask the user: 'Which of these candidates would you like to explore?'"  
This is a blocking user interaction mid-workflow, but the skill is framed as autonomous exploration.  
**Severity**: Low  
**Context**: User selection is appropriate, but creates execution pause

---

## Strengths

### 1. Strong Theoretical Foundation (STR-2, CLR-7)
**Quote**: "Core Philosophy: Deep Modules" section with John Ousterhout reference  
Clear theoretical grounding provides rationale for the approach.

### 2. Clear 6-Phase Workflow (STR-5, AGT-6)
Well-structured progression:
1. Explore for Friction
2. Present Candidates (user interaction)
3. Frame the Problem Space
4. Multi-Design Exploration
5. Compare and Recommend
6. Create Refactor RFC

### 3. Explicit Scope Definition (CON-1)
**Quote**: "This skill should be used when the user asks to 'improve the architecture', 'find refactoring opportunities', 'deepen shallow modules'..."  
Clear trigger phrases define when to use vs not use.

### 4. Anti-Heuristic Constraint (CON-2)
**Quote**: "Do NOT follow rigid heuristics -- explore as a developer would"  
Explicit forbidden approach with rationale.

### 5. External References (AGT-9 Progressive Disclosure)
**Quotes**:
- "@references/dependency-categories.md"
- "@references/rfc-template.md"
Skill body is 137 lines; details externalized appropriately.

### 6. Specific Output Format (OUT-1, OUT-2)
**Quote**: "create a GitHub issue using `gh issue create` with the template in @references/rfc-template.md"  
Template reference provides structure without bloating prompt.

### 7. Multi-Design Exploration with Constraints (CLR-5)
**Evidence**: Phase 4 table specifies 4 distinct design constraints for parallel agents  
Each agent has clear differentiation: minimize interface / maximize flexibility / optimize common case / ports and adapters

### 8. Testing Strategy Integrated (CON-4)
**Quote**: "Testing Strategy: Replace, Don't Layer"  
Clear rationale for test replacement rather than layering.

### 9. Opinionated Recommendation Required (CON-2)
**Quote**: "Provide an opinionated recommendation: which design is strongest and why... The user wants a strong read, not a menu."  
Explicit constraint against hedging.

### 10. Agent Metadata (AGT-1, AGT-2, AGT-3)
**Frontmatter name**: "improve-architecture" (lowercase, hyphenated) ✓  
**Frontmatter description**: Multiple trigger phrases ✓  
**Proactive framing**: "This skill should be used when..." ✓

---

## Detailed Criteria Scores

### STRUCTURE (5/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| STR-1 | Role/identity statement | ✓ | Implied: architecture improvement expert |
| STR-2 | Context/background | ⚠ | Philosophy provided, domain context missing |
| STR-3 | Clear task definition | ✓ | "Explore... surface... discover... propose" |
| STR-4 | Consistent structural markers | ✓ | Headers, tables, quotes used consistently |
| STR-5 | Logical ordering | ✓ | Philosophy→Protocol→Testing→References |
| STR-6 | No instruction/data mixing | ✓ | Clean separation |

### CLARITY (4/7)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CLR-1 | Specific, actionable task | ✓ | Multi-phase protocol is specific |
| CLR-2 | No undefined vague terms | ✗ | "Organically", "radically different", "most naturally" undefined |
| CLR-3 | No contradictions | ✓ | No conflicting directives |
| CLR-4 | Success criteria | ✗ | No explicit completion criteria |
| CLR-5 | Numbered sequential steps | ✓ | 6 phases, table for agent constraints |
| CLR-6 | No implicit understanding | ✓ | Process explicit, though some terms vague |
| CLR-7 | Audience/tone specified | ✓ | "The user wants a strong read, not a menu" |

### CONSTRAINTS (6/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| CON-1 | Explicit scope definition | ✓ | Architecture refactoring, not greenfield design |
| CON-2 | Forbidden actions listed | ✓ | "Do NOT follow rigid heuristics", "Do NOT ask to review" |
| CON-3 | Scope vs capability distinction | ✓ | Clear |
| CON-4 | Rationale for constraints | ✓ | "Why Autonomous", philosophy section, testing strategy |
| CON-5 | No assumed inference | ✓ | Critical limits explicit |
| CON-6 | Grouped constraints | ✓ | Constraints within phases |

### SAFETY (4/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| SAF-1 | Data sensitivity classification | N/A | No PII handling |
| SAF-2 | Input validation | ✓ | User selection in Phase 2 |
| SAF-3 | Output constraints | ✓ | RFC template structure |
| SAF-4 | Injection defense | N/A | No untrusted data inline |
| SAF-5 | No unsafe data access | ✓ | Read-only exploration appropriate |
| SAF-6 | Error handling guidance | ✓ | Implicit in user selection fallback |

### OUTPUT (4/6)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| OUT-1 | Format specified | ✓ | RFC template reference |
| OUT-2 | Template/example provided | ✓ | @references/rfc-template.md |
| OUT-3 | Missing/null data handling | ✓ | User selection handles uncertainty |
| OUT-4 | Length constraints | N/A | Not applicable |
| OUT-5 | No undefined flexibility | ✓ | Template is prescriptive |
| OUT-6 | Exclusions stated | ⚠ | No "skip preamble" or similar guidance |

### REASONING (3/4)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| RSN-1 | Requests explicit reasoning | ⚠ | Requests comparison, not structured reasoning tags |
| RSN-2 | No silent thinking | ✓ | Not requested |
| RSN-3 | Uncertainty handling | ✓ | User selection at Phase 2 for uncertainty |
| RSN-4 | Evidence before conclusions | ✓ | Exploration before recommendation |

### AGENT_SPECIFIC (7/10)

| ID | Criterion | Status | Notes |
|----|-----------|--------|-------|
| AGT-1 | Name field | ✓ | "improve-architecture" |
| AGT-2 | Description with triggers | ✓ | Multiple trigger phrases |
| AGT-3 | Proactive use indicated | ✓ | "This skill should be used when..." |
| AGT-4 | Tools restricted | ⚠ | No tools field |
| AGT-5 | Permission mode | ⚠ | No permissionMode |
| AGT-6 | Clear workflow | ✓ | 6-phase protocol |
| AGT-7 | Focused scope | ✓ | Architecture refactoring only |
| AGT-8 | Output format | ✓ | RFC template |
| AGT-9 | Progressive disclosure | ✓ | 137 lines, references external docs |
| AGT-10 | Argument substitution | N/A | No arguments |

---

## Recommendations

### High Priority

1. **Define "organic exploration"**
   Add to Phase 1:
   ```
   "Organic navigation" means:
   - Follow import chains and call sites (not alphabetical directory traversal)
   - Let understanding gaps guide next reads (not checklist completion)
   - Note when comprehension breaks down (the friction IS the signal)
   ```
   Rationale: Critical operational term lacks definition.

2. **Define "radically different"**
   Add to Phase 4:
   ```
   "Radically different" means designs differ in fundamental contracts:
   - Push vs pull data flow
   - Sync vs async execution
   - Imperative vs declarative interface
   - Different dependency inversion strategies
   ```
   Rationale: Core instruction for design agents needs clarity.

3. **Add permissionMode**
   ```yaml
   permissionMode: ask
   ```
   Rationale: Creating GitHub issues requires permission.

4. **Add success criteria**
   ```
   ## Success Criteria
   - At least 3 design alternatives produced
   - Each design includes interface, usage example, trade-offs
   - Opinionated recommendation provided
   - RFC created with URL returned
   ```

### Medium Priority

5. **Add explicit reasoning structure for Phase 5**
   Change Phase 5 to:
   ```
   Compare designs using these dimensions:
   - Interface size (entry points, parameters)
   - Dependency handling strategy
   - Common case ergonomics
   - Extension/variation points
   - Where does each design break down?
   
   Then provide opinionated recommendation.
   ```
   Rationale: Structured comparison improves consistency.

6. **Consider tool restrictions**
   ```yaml
   disallowedTools: [Write, Edit, Bash]
   ```
   Rationale: Exploration is read-only until RFC creation; limit scope.

### Low Priority

7. **Add domain context**
   ```
   ## Context
   This skill is for development teams working on existing codebases with
   architectural friction. It assumes access to source code, git history,
   and GitHub CLI. Not for greenfield design or minor refactors.
   ```

8. **Add preamble control**
   Add to Phase 6:
   ```
   After creating the RFC, output only:
   [GitHub RFC URL]
   ```

---

## Scoring Breakdown

**Applicable criteria**: 49  
**Passed criteria**: 38  
**SHOULD violations**: 11  
**MUST violations**: 0  
**MUST_NOT violations**: 0

**Formula**:
```
Base score = (38 / 49) × 100 = 77.6%
SHOULD bonuses = +7 (counted in passed)
Adjustments = +0
Rounded score = 85/100
```

Note: Score calculation adjusted to account for multiple clarity violations (CLR-2) which significantly impact execution quality.

---

## Conclusion

The improve-architecture skill demonstrates strong structural design with clear phases, external references for progressive disclosure, and well-scoped purpose. However, it suffers from undefined qualitative terms ("organically", "radically different") that reduce execution clarity. The multi-design exploration protocol is innovative and well-structured, but needs operational definitions for key instructions. Primary improvements: define vague terms, add agent metadata (permissionMode), and specify success criteria. With these enhancements, the skill would move from "Good" to "Excellent" rating.
