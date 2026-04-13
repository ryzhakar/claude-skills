# Reference Optionality: prompt-optimize

## Essential References (must inline into SKILL.md)
None. All references can be deferred with appropriate loading gates.

## Deferrable References (need loading gates)

### improvement-patterns.md
- **Why deferrable**: Not needed on every invocation. Only required when actually applying fixes to identified issues. The main SKILL.md already contains the pattern index table (lines 46-61) mapping issue types to patterns, which is sufficient for workflow navigation. Full pattern details (before/after examples, rationale) are only needed during actual remediation.
- **Loading gate**: IF (Step 3: Map Issues to Patterns OR Step 4: Apply Improvements) AND user is actively fixing a specific issue type, THEN read `references/improvement-patterns.md`
- **Gate placement**: Step 4 "Apply Improvements" - after determining which patterns to use, before writing the fixes. The gate should check which specific patterns (IP-01 through IP-12) are needed and read only those sections.

### ordering-guide.md
- **Why deferrable**: Not needed on every invocation. Only required when restructuring a prompt after individual issues are fixed (Step 5 in workflow). The main SKILL.md already provides the canonical ordering summary in lines 96-107, which covers the basic sequence. The full guide with detailed rationale, examples, and variation patterns is only needed when the user is actively reordering elements.
- **Loading gate**: IF Step 5: Reorder Elements is reached AND the prompt requires structural reorganization, THEN read `references/ordering-guide.md`
- **Gate placement**: Step 5 "Reorder Elements" - after all individual issues are addressed, when determining optimal element sequence.

### term-blacklists.md
- **Why deferrable**: Not needed on every invocation. Only required during Step 6: Eliminate Vague Language, which is a specific cleanup pass after fixes are applied. The skill can perform optimization without this reference if vague language isn't a primary issue. The reference contains extensive lists, regex patterns, and replacement mappings that are only valuable during active vague-term elimination.
- **Loading gate**: IF Step 6: Eliminate Vague Language is reached OR vague terms detected during earlier steps (AP-CLR-02 flagged), THEN read `references/term-blacklists.md`
- **Gate placement**: Step 6 "Eliminate Vague Language" - after reordering, when scanning for and replacing vague terminology.

### evaluation-criteria.md
- **Why deferrable**: Not needed on every invocation. The skill can perform optimization based on known anti-patterns without formal evaluation. This reference is only essential in two scenarios: (1) When no evaluation exists and the skill chooses to run a quick evaluation (Step 1), or (2) When validating the optimized result (Step 7). The main SKILL.md contains enough inline guidance (Quick Fixes section, improvement priorities) to optimize without full criteria.
- **Loading gate**: IF (Step 1: no evaluation available AND user wants formal evaluation before optimizing) OR (Step 7: Validate Result is reached AND formal scoring requested), THEN read `references/evaluation-criteria.md`
- **Gate placement**: 
  - Step 1 "Understand Current State" - when running quick evaluation without existing report
  - Step 7 "Validate Result" - when scoring the optimized prompt

### anti-patterns.md
- **Why deferrable**: Not needed on every invocation. When an evaluation report already exists (common case, per line 27 "Works best after prompt-eval"), the anti-patterns are already identified and documented. This reference is only needed when: (1) no evaluation exists and the skill must scan for obvious issues (Step 1, line 34), or (2) when mapping known issues to improvement patterns requires anti-pattern codes for cross-referencing. The main SKILL.md contains enough inline issue recognition (Quick Fixes examples, priority ordering) to function without the full catalog.
- **Loading gate**: IF (Step 1: no evaluation available AND scanning for issues) OR (Step 3: mapping issues requires anti-pattern code lookup), THEN read `references/anti-patterns.md`
- **Gate placement**: 
  - Step 1 "Understand Current State" - when no evaluation exists and scanning for obvious issues
  - Step 3 "Map Issues to Patterns" - if anti-pattern codes need detailed definitions for accurate mapping

## Summary
- Essential: 0 of 5 references
- Deferrable: 5 of 5 references

## Implementation Notes

All five references support conditional loading because:

1. **The skill has two distinct usage modes**:
   - Post-evaluation mode (primary): evaluation already identifies issues, optimization proceeds directly to fixes
   - Standalone mode (secondary): skill must evaluate first, then optimize

2. **The workflow is sequential with clear decision points**: Each step (1-7) provides natural gates where references become necessary only if specific conditions are met.

3. **SKILL.md contains sufficient inline guidance** for core execution:
   - Pattern index table (lines 46-61) for issue-to-pattern mapping
   - Basic ordering summary (lines 96-107) for restructuring
   - Quick Fixes section (lines 169-214) with inline before/after examples
   - Priority ordering (lines 64-91) for triage

4. **Loading gates are unambiguous**: Each reference has concrete activation conditions tied to workflow steps, user choices, or detected issues. The gates make ignoring references impossible when conditions are met:
   - "IF Step N is reached" - tied to explicit workflow progression
   - "IF AP-CLR-02 flagged" - tied to detected issue types
   - "IF no evaluation available" - tied to input state

5. **Deferred loading prevents context bloat**: The five references total ~48k tokens of detailed patterns, examples, checklists, and edge cases. Most optimization invocations need only 1-2 references, not all five.
