# Reference Optionality Analysis: improve-architecture

## Summary

Analyzed 2 reference files for the improve-architecture skill. Both references are **DEFERRABLE** with concrete loading gates embedded in the workflow.

---

## Reference 1: dependency-categories.md

**Classification**: DEFERRABLE

**Rationale**: 
The dependency categorization framework is only needed during Phase 2 (candidate presentation) and Phase 4 (multi-design exploration). The skill can activate and begin Phase 1 exploration without this reference. The framework becomes load-bearing when presenting candidates (line 56 references it) and when briefing design agents (line 99 references it).

**Loading Gate**:
```
IF presenting candidate list in Phase 2, THEN read references/dependency-categories.md
```

**Gate Location**: Between Phase 1 (exploration complete) and Phase 2 (presenting candidates).

**Enforcement**: Phase 2 explicitly requires filling the "Dependency category" field in the candidate table (line 56: "Classify using the 4-category framework in @references/dependency-categories.md"). The skill cannot produce Phase 2 output without this reference. Phase 4 agent briefs also require dependency strategy details (line 99: "see @references/dependency-categories.md"), making the reference load-bearing before launching design agents.

**Workflow Integration**:
- Phase 1: Explore codebase (no dependency framework needed)
- **[GATE]** Before Phase 2: Load dependency-categories.md
- Phase 2-6: Use framework for classification, testing strategy, and agent briefs

---

## Reference 2: rfc-template.md

**Classification**: DEFERRABLE

**Rationale**:
The RFC template is only needed in Phase 6 when creating the GitHub issue. The skill executes Phases 1-5 (exploration, candidate presentation, problem framing, multi-design exploration, comparison/recommendation) without requiring the template structure. The template becomes load-bearing when the user selects a design and the skill must create the GitHub issue.

**Loading Gate**:
```
IF user selects a design in Phase 5, THEN read references/rfc-template.md before executing Phase 6
```

**Gate Location**: Between Phase 5 (recommendation/selection) and Phase 6 (creating GitHub issue).

**Enforcement**: Phase 6 explicitly instructs: "create a GitHub issue using `gh issue create` with the template in @references/rfc-template.md" (line 116). The skill cannot execute Phase 6 without this reference. The instruction to "publish directly" (line 118) means the gate must block before any `gh issue create` command is executed.

**Workflow Integration**:
- Phases 1-4: Exploration and design work (no template needed)
- Phase 5: Present recommendation, user selects design
- **[GATE]** Before Phase 6: Load rfc-template.md
- Phase 6: Create GitHub issue using template

---

## Conclusion

Both references are **DEFERRABLE** with unambiguous loading gates:

1. **dependency-categories.md**: Load before Phase 2 (when classification is required)
2. **rfc-template.md**: Load before Phase 6 (when GitHub issue creation is required)

The gates are enforcement-guaranteed because:
- Phase 2 cannot complete its candidate table without dependency classification
- Phase 4 agent briefs explicitly reference the dependency framework
- Phase 6 cannot execute `gh issue create` without the template structure

No references are ESSENTIAL. The skill's early phases (exploration, problem framing) function independently, and the references load just-in-time when their content becomes load-bearing.
