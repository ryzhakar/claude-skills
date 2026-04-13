# Reference Optionality Analysis: dev-orchestration

## Unit: dev-orchestration

## Analysis Date: 2026-04-13

## Reference Files Analyzed

1. `/Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/references/lifecycle-loops.md`
2. `/Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/references/agent-dispatch.md`
3. `/Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/references/domain-context-examples.md`

---

## Classification

### lifecycle-loops.md — DEFERRABLE

**Loading Gate:**
IF the orchestrator encounters a loop limit or state transition failure (review-fix cycle exceeds 3 iterations, integration verification fails, BLOCKED status requires escalation, debugging cycle hits hypothesis limit), THEN read `/Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/references/lifecycle-loops.md`.

**Gate Location in Workflow:**
- After 3rd review-fix cycle without PASS (Phase 3: Review)
- When BLOCKED status is reported and diagnosis is needed (Phase 4: Status-Driven Branching)
- When integration verification fails after all units pass individual review (Multi-Unit Integration section)
- When debugging enters hypothesis limit (Debugging Escalation section)

**Justification:**
The main SKILL.md describes the Plan→Implement→Review→Fix loop at a conceptual level sufficient to begin execution. It explicitly directs readers to lifecycle-loops.md "for the complete state machine with entry/exit criteria and loop limits" (line 53). The workflow can start without the detailed state machine—agents dispatch, reviews happen, fixes apply. The reference becomes critical only when the orchestrator needs to decide whether to continue looping or escalate, which is a minority case. The reference defines escalation thresholds (3 review cycles, 3 debugging hypotheses) and multi-unit dependency tracking that are not needed until those specific conditions occur.

---

### agent-dispatch.md — DEFERRABLE

**Loading Gate:**
IF constructing an agent dispatch brief for implementer/spec-reviewer/code-quality-reviewer AND (dev-discipline plugin is not installed OR the orchestrator needs to handle a non-standard status like DONE_WITH_CONCERNS classification or BLOCKED diagnosis), THEN read `/Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/references/agent-dispatch.md`.

**Gate Location in Workflow:**
- When dispatching implementer agents without dev-discipline plugin (Phase 2: Implement, line 87-90)
- When interpreting DONE_WITH_CONCERNS status and classifying concerns (Phase 4: Status-Driven Branching, line 158-159)
- When BLOCKED status requires root cause diagnosis (Phase 4: Status-Driven Branching, line 165-173)
- When constructing re-dispatch briefs after review failures (Phase 3: Review, line 141-148)

**Justification:**
The main SKILL.md provides enough context to begin dispatching agents: "construct a brief containing: 1. task specification, 2. file paths, 3. TDD requirements, 4. scope boundaries" (lines 82-86). It describes the hard preference for dev-discipline agents, which handle their own context requirements. The reference becomes necessary only when: (a) dev-discipline is not installed and equivalent prompts must be constructed, or (b) the orchestrator encounters a non-trivial status interpretation scenario (DONE_WITH_CONCERNS classification, BLOCKED diagnosis). Most dispatch operations use the dev-discipline agents directly and don't require the detailed context assembly rules.

---

### domain-context-examples.md — ESSENTIAL

**Justification:**
This reference is NOT ESSENTIAL. It provides illustrative examples of how to apply the "minimal context principle" from the parent skill (agentic-delegation) to concrete dev scenarios. The main SKILL.md already instructs to "construct a brief" with specific components (lines 82-86) and references the parent's minimal context governance. The examples (Cargo.toml audit, Tailwind compatibility, type signature verification) are pedagogical aids, not operational requirements. An orchestrator can execute dev-orchestration workflows without reading these examples—they serve as quality improvement guides, not functional prerequisites.

**Reclassification: DEFERRABLE**

**Loading Gate:**
IF the orchestrator is constructing a context brief for a domain-specific task (dependency audits, framework compatibility checks, type signature verification) AND uncertainty exists about what constitutes "minimal context" for that domain, THEN read `/Users/ryzhakar/pp/claude-skills/orchestration/skills/dev-orchestration/references/domain-context-examples.md`.

**Gate Location in Workflow:**
- When constructing implementer briefs for dependency-related tasks (Phase 2: Implement, lines 81-90)
- When providing context for NEEDS_CONTEXT re-dispatch (Phase 4: Status-Driven Branching, lines 162-163)

---

## Summary

- **ESSENTIAL references:** 0
- **DEFERRABLE references:** 3

All references are deferrable. The main SKILL.md provides sufficient instruction to initiate the development loop (Plan→Implement→Review→Fix), dispatch agents with basic briefs, and interpret common status codes (DONE, NEEDS_CONTEXT). References become load-bearing when the workflow encounters edge cases: loop limits, escalation thresholds, non-standard status interpretation, or the need to construct agent prompts without dev-discipline. Each reference has concrete loading gates tied to specific workflow conditions that make ignoring it impossible when those conditions occur.
