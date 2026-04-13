# Reference Optionality Analysis: manifesto-oath

## Skill Overview

The skill enables behavioral binding to user-provided manifestos through identity-assumption protocols. Core workflow: user provides manifesto + requests binding -> skill activates operational mode with verification loop -> ongoing constraint checking.

## Reference Files Analysis

### 1. configuration.md (3147 bytes)

**Classification: DEFERRABLE**

**Content Summary:**
- `.manifestos.yaml` file format specification (3 entry types: name, URL, local path)
- CLAUDE.md fallback format (`## Active Manifestos` section)
- Resolution rules for each entry type
- Hook lifecycle documentation (SessionStart, PostCompact, SubagentStart)
- Configuration examples for different project types

**Loading Gate:**
```
IF user asks about:
  - "how do I configure manifestos for a project"
  - "what is .manifestos.yaml"
  - "how do hooks work"
  - "how to set up automatic manifesto binding"
  - "project-level manifesto configuration"
  - mentions hooks, SessionStart, PostCompact, SubagentStart
THEN read references/configuration.md
```

**Reasoning:**
This is project infrastructure documentation, not core oath protocol. The skill's primary use case is immediate interactive binding (user provides manifesto in conversation -> activate mode). Configuration is relevant only when user asks about persistent/automated binding across sessions or for understanding the plugin's hook system. The gate condition makes it impossible to help with configuration questions without loading the reference.

**Essential Elements in SKILL.md:**
The main skill body correctly omits configuration details and includes only a pointer: "See @references/configuration.md" in the Project Configuration section. This is appropriate delegation.

---

### 2. theory.md (5521 bytes)

**Classification: DEFERRABLE**

**Content Summary:**
- Why human oaths work (4 mechanisms: memory, identity, cost, illocutionary force)
- Why naive model oaths fail (lacks all 4 mechanisms)
- Constitutional shift theory (identity assumption vs promise-making)
- Verification loop mechanism (active alignment checking)
- Implementation principles (technical framing, present-tense, explicit protocol)
- Constraint hierarchy explanation
- Philosophical status discussion
- Academic references (Austin, Bai et al., Searle)

**Loading Gate:**
```
IF user asks about:
  - "why does this approach work"
  - "what's wrong with just saying 'I promise'"
  - "theoretical foundation"
  - "why not just swear an oath"
  - "is this actually binding"
  - "philosophy behind this"
  - challenges the methodology
  - questions whether identity-assumption is better than promises
THEN read references/theory.md
```

**Reasoning:**
The theory provides justification and deeper understanding but is NOT required for basic invocation. The SKILL.md body already contains the practical distinctions (theatrical vs operational table, implementation template, verification loop mechanics). Theory.md answers "why" questions that arise when users probe the rationale or challenge the approach. The skill works without this knowledge; it's loaded only when user exhibits curiosity about foundations. Gate captures all "why/justification" inquiry patterns.

**Essential Elements Already in SKILL.md:**
- "Why Theatrical Oaths Fail" section (condensed practical version)
- "Critical Distinctions" table (operational guidance extracted from theory)
- Verification loop mechanics (implementation, not theory)
- Constraint hierarchy (practical list, not philosophical explanation)

The main body preserves actionability while theory.md preserves intellectual rigor.

---

## Summary

Both references are DEFERRABLE:

1. **configuration.md**: Project-level automation infrastructure. Load when user asks about persistent binding, hooks, or `.manifestos.yaml` setup.

2. **theory.md**: Intellectual foundation and methodology justification. Load when user questions the approach, asks "why," or challenges the identity-assumption vs promise-making distinction.

Neither is needed for the core invocation path (user provides manifesto -> activate mode -> ongoing constraint checking). The SKILL.md body contains all workflow-critical content. References serve advanced/meta concerns.

## Gate Robustness

Both gates are designed to be impossible to ignore when triggered:
- Configuration gate: Cannot explain automation/hooks/file formats without the reference
- Theory gate: Cannot justify approach or explain "why this works" without the reference

Standard invocations (immediate interactive binding) bypass both references entirely, achieving maximum token efficiency.
