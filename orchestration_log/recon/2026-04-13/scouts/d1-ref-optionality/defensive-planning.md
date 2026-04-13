# Reference Optionality Analysis: defensive-planning

## Unit
`defensive-planning`

## Reference Files Analyzed
- `references/tdd-mode.md`
- `references/execution.md`
- `references/module-design.md`

---

## Classification

### DEFERRABLE: `references/tdd-mode.md`

**Rationale:**
The skill explicitly introduces this reference with conditional language: "For plans targeting TDD workflows with 2-5 minute task granularity, see @references/tdd-mode.md". The reference provides an optional granularity protocol applicable only when:
1. The implementation plan targets codebases with test infrastructure
2. The work involves creating or modifying behavior-carrying code
3. The user or context indicates TDD workflow preference

The skill functions correctly without this reference when writing non-TDD plans, correction plans, or adherence assessments.

**Loading Gate:**
```
IF (document_type == "Implementation Plan") AND 
   (user requests TDD workflow OR context indicates test-first development OR 
    plan targets codebase with existing TDD patterns),
THEN read /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/defensive-planning/references/tdd-mode.md
```

**Gate Location in Workflow:**
Insert immediately after the main skill section "Writing Implementation Plans" → "Structure", before beginning task decomposition. The gate condition should be evaluated when determining plan granularity strategy.

---

### DEFERRABLE: `references/execution.md`

**Rationale:**
The skill explicitly positions this as post-creation guidance: "For executing plans after writing them, see @references/execution.md". This reference is only needed when the agent moves from planning to implementation, not during plan creation, adherence assessment, or correction planning.

The reference covers:
- Pre-execution review gate
- Blocker escalation protocol
- Task state tracking
- Two-stage review ordering
- Status-driven branching

None of these are required to write a defensive plan. They only become relevant when executing that plan.

**Loading Gate:**
```
IF (document_type == "Implementation Plan") AND 
   (plan_status == "complete" OR plan_status == "approved") AND
   (user requests execution OR next step is implementation),
THEN read /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/defensive-planning/references/execution.md
```

**Gate Location in Workflow:**
Insert at the transition point between "plan complete" and "begin implementation". This gate should trigger before any implementation work starts, immediately after plan finalization.

---

### DEFERRABLE: `references/module-design.md`

**Rationale:**
The skill introduces this reference conditionally: "For module decomposition heuristics during plan design, see @references/module-design.md". The reference provides architectural guidance applicable when:
1. Writing implementation plans (not correction or adherence documents)
2. Decomposing work into modules/components
3. Making design decisions about interfaces and testability

The skill can produce correction plans and adherence assessments without module design heuristics. Even for implementation plans, simple single-file changes or procedural fixes may not require module decomposition.

**Loading Gate:**
```
IF (document_type == "Implementation Plan") AND
   (work involves creating new modules OR refactoring module boundaries OR 
    designing multi-component systems OR user requests architecture guidance),
THEN read /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/defensive-planning/references/module-design.md
```

**Gate Location in Workflow:**
Insert in "Writing Implementation Plans" section, immediately before "Structure" subsection, at the point where architectural decisions are being made. Specifically, trigger this gate when transitioning from preamble/problem definition to phase design.

---

## Summary

All three references are DEFERRABLE:

1. **tdd-mode.md** — Load only for TDD-specific implementation plans
2. **execution.md** — Load only when transitioning from planning to implementation
3. **module-design.md** — Load only when designing multi-module architectures

Each gate is specified with:
- A concrete boolean condition
- Clear insertion point in the workflow
- Condition that makes ignoring the reference IMPOSSIBLE when true

The skill's core defensive planning principles, document structures, and anti-patterns remain functional without any references. All three references extend the base methodology for specific contexts.
