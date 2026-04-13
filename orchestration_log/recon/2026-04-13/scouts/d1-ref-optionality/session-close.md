# Reference Optionality Analysis: session-close

**Unit:** session-close
**Analyst:** Claude Sonnet 4.5
**Date:** 2026-04-13

## Summary

2 reference files analyzed. Both classified as **DEFERRABLE** with clear loading gates tied to specific workflow steps.

## Classifications

### DEFERRABLE: data-schema.md

**Gate:** IF Step 1 (extract session metrics) is being executed, THEN read `references/data-schema.md`

**Placement in workflow:** At the start of Step 1, when dispatching the haiku agent for metric extraction.

**Rationale:**
- Used exclusively for Step 1 (metric extraction) and Step 7 (cost capture)
- Not needed for core workflow orchestration decisions
- The SKILL.md already provides sufficient summary: "See `references/data-schema.md` for full field reference and parsing patterns" (line 40)
- Agent briefing for Step 1 references it explicitly: "See `references/data-schema.md` for field names and cost formulas" (line 57)
- Only contains technical parsing details (JSONL schema, field types, cost formulas, model tier detection)
- Loading condition is unambiguous: Step 1 execution requires this data

**Gate enforcement:** The workflow explicitly calls out this reference at Step 1. An orchestrator executing Step 1 cannot proceed without briefing the agent on parsing details, making the gate impossible to skip.

---

### DEFERRABLE: session-record-format.md

**Gate:** IF Step 3 (draft session record) is being executed, THEN read `references/session-record-format.md`

**Placement in workflow:** At the start of Step 3, when dispatching the sonnet agent to draft the session record.

**Rationale:**
- Used exclusively for Steps 3 and 5 (drafting and correcting the session record)
- Not needed for Steps 1, 2, 4, 6, 7, or 8
- The SKILL.md already provides sufficient summary: "See `references/session-record-format.md` for required sections and format" (line 78)
- Only contains formatting specifications (header structure, section templates, common agent mistakes)
- The orchestrator needs this when reviewing Step 5, but the reference cite at line 78 is sufficient to trigger a read at that point
- Loading condition is unambiguous: Step 3 execution requires this format spec

**Gate enforcement:** Step 3 explicitly instructs "See `references/session-record-format.md` for required sections and format." An orchestrator dispatching a session-record-drafting agent without reading the format spec would produce an incorrectly-structured record, making the gate impossible to skip in practice.

---

## No ESSENTIAL references

The SKILL.md is complete and self-sufficient for executing the LEAVE protocol. Both references contain implementation details needed only at specific steps, not core vocabulary or workflow logic required at activation time.

## Gate Summary Table

| Reference | Gate Condition | Workflow Location | Enforcement Mechanism |
|-----------|---------------|-------------------|----------------------|
| data-schema.md | Step 1 execution begins | Before dispatching metric extraction agent | Agent briefing impossible without parsing schema |
| session-record-format.md | Step 3 execution begins | Before dispatching session record drafting agent | Agent briefing impossible without format spec |

## Notes

- Both references are already cited in the SKILL.md at the exact points where they become necessary
- Current structure supports lazy loading naturally
- No ambiguity in when to load each reference
- The 8-step LEAVE protocol is fully comprehensible without either reference
- References contain "how" details; SKILL.md contains "what" and "when" logic
