# Reference Optionality Analysis: agentic-delegation

**Skill:** agentic-delegation
**Analyst:** Sonnet 4.5
**Date:** 2026-04-13

---

## Summary

All three reference files are ESSENTIAL and must be inlined into the main SKILL.md body. None can be deferred because each defines workflow steps that are needed on every invocation of this skill.

---

## Reference Analysis

### 1. prompt-anatomy.md

**Classification:** ESSENTIAL

**Reasoning:**

The skill's core operation is decomposing work and delegating it to agents. Section 3 ("Prompt Anatomy") of SKILL.md reads:

> "Every agent prompt requires: (1) Role statement, (2) Minimal context, (3) Explicit input file paths, (4) Numbered task steps, (5) Absolute output path, (6) Pasted report format, (7) Scope boundaries (DO and DO NOT lists), (8) Tool expectations, (9) Prime directive for research agents. A well-structured prompt for haiku outperforms a vague prompt for sonnet.
>
> For complete prompt structure with examples and quality checklists, see @references/prompt-anatomy.md"

The skill cannot function correctly without prompt anatomy because:
- The orchestrator must write agent prompts on EVERY invocation
- The 9-section structure is not just a recommendation — it's the mandatory format
- The quality checklist determines whether prompts will produce correct results
- The failure signal table (section "Common Prompt Failures") is diagnostic infrastructure needed during every agent dispatch

Without this reference, users cannot write valid agent prompts, which means they cannot delegate work, which means the skill is non-functional.

**Evidence from SKILL.md:**

Line 283: "Every agent prompt requires: (1) Role statement... (9) Prime directive for research agents."

This is a specification of required prompt structure. The reference contains the implementation details of that specification. Deferring it would be like publishing an API specification without the parameter schemas.

---

### 2. quality-governance.md

**Classification:** ESSENTIAL

**Reasoning:**

The skill's execution model relies on detecting and correcting bad agent output. Section 6 ("Quality Governance") of SKILL.md reads:

> "Detect bad output through completion summaries (extraordinary claims, contradictions, suspiciously short reports). Never debug failed agents in orchestrator context — re-launch with better prompts or higher tiers. Resolve contradictions by launching verification agents that check primary sources. For batches of 10+ agents, spot-check 1-2 reports to validate batch quality.
>
> For complete quality governance patterns including detecting bad output, the re-launch principle, contradiction resolution, and spot-checking strategies, see @references/quality-governance.md"

The skill cannot function correctly without quality governance because:
- Agents fail regularly (model limitations, vague prompts, task complexity)
- The orchestrator must detect failures through completion summaries (table at quality-governance.md lines 9-15)
- The re-launch principle (lines 19-46) is a core workflow step, not optional advice
- Contradiction resolution (lines 49-78) defines the mandatory procedure when agents disagree
- Spot-checking (lines 81-121) is required for batches of 10+ agents

Without this reference, users will debug failed agents in orchestrator context (burning expensive context on waste), make wrong decisions when agents contradict each other, and trust unreliable agent self-reports.

**Evidence from SKILL.md:**

Line 361: "Detect bad output through completion summaries (extraordinary claims, contradictions, suspiciously short reports)."

This requires the signal detection table from quality-governance.md (lines 9-15). Without it, the orchestrator cannot distinguish signal from noise.

Line 361: "Never debug failed agents in orchestrator context — re-launch with better prompts or higher tiers."

This is not advice — it's a prohibition. The re-launch principle (quality-governance.md lines 19-46) defines what to do instead. Without it, users will violate the prohibition by default.

---

### 3. session-persistence.md

**Classification:** ESSENTIAL

**Reasoning:**

The skill explicitly designates session persistence as part of its core workflow. Section 10 ("Session Persistence") of SKILL.md reads:

> "Multi-session orchestration work accumulates knowledge: which model tiers work, which patterns fail, what the codebase looks like, what debt exists. Without persistence, every session starts from zero and repeats prior mistakes.
>
> The ARRIVE/WORK/LEAVE lifecycle protocol maintains living reference documents (what's true now), frozen session history (what happened then), and disposable recon data (raw scouting). The orchestrator reads reference docs on arrival and updates them before leaving. Every rule in the conventions traces to a documented failure.
>
> For the full protocol including directory structure, mutability rules, session record format, and reference document templates, see @references/session-persistence.md"

The skill cannot function correctly without session persistence because:
- The ARRIVE/WORK/LEAVE protocol (lines 44-69) is the lifecycle wrapper around all delegation work
- Without ARRIVE, the orchestrator starts from zero (burns money repeating solved problems)
- Without LEAVE, knowledge is lost at session end (the next session repeats failures)
- The directory structure (lines 15-39) defines where all reports and findings go — without it, agent outputs are ad-hoc and ungovernable

**Evidence from SKILL.md:**

Line 465: "The ARRIVE/WORK/LEAVE lifecycle protocol maintains living reference documents (what's true now), frozen session history (what happened then), and disposable recon data (raw scouting)."

This is not a feature — it's the execution model. ARRIVE/WORK/LEAVE wraps all delegation work. Without the reference, users don't know:
- What to read on ARRIVE (which reference docs exist)
- What to update on LEAVE (which docs are living vs frozen)
- Where to write agent reports during WORK (directory structure)

Line 467: "The orchestrator reads reference docs on arrival and updates them before leaving."

This is a mandatory workflow step. Without session-persistence.md defining which reference docs exist and what format they use, this step is non-executable.

---

## Deferral Attempt

Could any of these references be loaded conditionally?

### Prompt Anatomy

**Gate attempt:** "IF the user asks to delegate work, THEN read prompt-anatomy.md"

**Failure:** The skill description reads: "Use this skill whenever work can be broken into parts." The entire skill IS delegation. There is no invocation that doesn't require prompt anatomy.

### Quality Governance

**Gate attempt:** "IF an agent returns bad output, THEN read quality-governance.md"

**Failure:** The orchestrator must detect bad output BEFORE it knows the output is bad. Detection requires the signal table from quality-governance.md. You can't defer the detection guide until after detection happens.

### Session Persistence

**Gate attempt:** "IF starting a new session, THEN read session-persistence.md"

**Failure:** ARRIVE is the first step of every session. The orchestrator cannot know what to read on ARRIVE without session-persistence.md defining the ARRIVE protocol. The protocol defines itself — circular dependency makes deferral impossible.

---

## Conclusion

All three references are ESSENTIAL. Each defines core workflow steps needed on every invocation:

1. **prompt-anatomy.md** — How to write agent prompts (required for every agent dispatch)
2. **quality-governance.md** — How to detect and correct failures (required for every agent batch)
3. **session-persistence.md** — ARRIVE/WORK/LEAVE lifecycle (required for every session)

None can be deferred without making the skill non-functional.

**Recommendation:** Inline all three references into SKILL.md. The skill's length is justified — it defines a complete orchestration discipline with mandatory procedures at every step.
