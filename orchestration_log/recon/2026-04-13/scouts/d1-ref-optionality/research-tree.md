# Reference Optionality Analysis: research-tree

## Overview

The research-tree skill governs multi-agent research workflows across knowledge surfaces. It references four files that provide tier definitions, failure mode catalogs, prompt templates, and report formats. This analysis determines which references must be inlined and which can remain conditionally loaded.

## Reference Classification

### 1. tier-playbook.md — DEFERRABLE

**Rationale:**
The skill's main body already provides the tier system structure (lines 67-96), tier philosophy (lines 20-66), and general orchestration flow (lines 127-157). The tier-playbook.md provides detailed per-tier specifications: agent counts, completion gates, model selection heuristics, and transition decisions. These details are not needed at activation—they are needed when designing and launching agents for specific tiers.

**Loading gate:**
```
WHEN preparing to launch agents for Tier {N}
THEN read /Users/ryzhakar/pp/claude-skills/orchestration/skills/research-tree/references/tier-playbook.md section "Tier {N}: {NAME}"
```

**Placement in workflow:**
Between tier completion and next tier launch. Specifically:
- After Tier 1 completes → read Tier 2 section before designing survey agents
- After Tier 2 completes → read Tier 3 section before determining what to verify
- After Tier 3 completes → read Tier 4 section before scanning for contradictions
- Before Tier 5 → read Tier 5 section before designing synthesis prompt

**Gate enforcement:**
The orchestration protocol (lines 127-157) explicitly requires per-tier decisions about agent design, agent count, and completion gates. The reference is named in line 83 with @references/tier-playbook.md, creating a clear lookup point. The impossibility constraint: designing tier-specific agents without the playbook means guessing at agent counts and completion criteria—the orchestrator must consult it.

### 2. anti-patterns.md — DEFERRABLE

**Rationale:**
The main body already summarizes the three most damaging anti-patterns (lines 206-212). The full catalog of 10 failure modes with detection strategies exists for quality control and debugging, not for basic skill activation. Anti-pattern awareness is needed when reviewing agent prompts, scanning tier outputs for issues, or diagnosing why a research session produced poor results.

**Loading gate:**
```
IF any of:
  - Designing agent prompts for a tier
  - Reviewing completed tier outputs for quality issues
  - Debugging why research results seem unreliable
  - User requests research quality audit
THEN read /Users/ryzhakar/pp/claude-skills/orchestration/skills/research-tree/references/anti-patterns.md
```

**Placement in workflow:**
- Before launching each tier → read sections AP-1, AP-2, AP-5, AP-10 to verify prompt design
- After tier completion → read sections AP-6, AP-9 to scan for hallucinations and orphaned findings
- When synthesis produces generic output → read AP-4 and section "Before launching synthesis"

**Gate enforcement:**
Lines 139 and 183 in the main body explicitly call out detection responsibilities ("Detect contradictions", "Scan completion summaries"). The anti-patterns reference provides the detection checklist. The detection checklist (anti-patterns.md lines 174-194) is a mandatory pre-launch verification step that the orchestrator cannot skip without violating the orchestration protocol.

### 3. agent-templates.md — ESSENTIAL

**Rationale:**
Agent design is not optional—it happens on every research invocation. The main body states "Every agent prompt specifies: [6 requirements]" (lines 113-121) but does not provide the actual prompt skeletons. Lines 125 states "For domain-adaptable skeletons, see @references/agent-templates.md." Without these templates, the orchestrator must construct agent prompts from scratch on every tier, leading to format inconsistency (anti-pattern AP-8) and missing the prime directive (lines 99-112).

The templates encode:
- The prime directive block (used in every research agent)
- Structural requirements (one task, explicit file paths, report format pasted inline)
- Domain placeholders that ensure the orchestrator doesn't miss critical adaptations

**Inline integration strategy:**
Move agent-templates.md content into the main SKILL.md body under a new "## Agent Prompt Construction" section after "## Agent Design" (after line 125). This makes the templates immediately available without requiring a reference lookup on every tier launch.

### 4. report-formats.md — ESSENTIAL

**Rationale:**
Report format templates are required infrastructure, not conditional knowledge. The main body explicitly requires format consistency:
- Line 122: "Report format template pasted inline — agents can't read skill reference files"
- Lines 113-121: "Every agent prompt specifies... Report format template pasted inline"
- Anti-pattern AP-8 (lines in anti-patterns.md): "Format Anarchy" is a primary failure mode when templates aren't used

Every agent in every tier must receive a report format template in its prompt. The orchestrator cannot defer this—it must have the templates available at tier launch time. Line 125 references @references/report-formats.md, but the reference is consulted on every agent prompt construction, not conditionally.

**Inline integration strategy:**
Move report-formats.md content into the main SKILL.md body under a new "## Report Format Templates" section after "## Agent Design" or as an appendix. This eliminates the lookup friction on every agent prompt construction.

## Summary

| Reference | Classification | Trigger Condition |
|-----------|---------------|-------------------|
| tier-playbook.md | DEFERRABLE | When preparing agents for Tier N, read Tier N section |
| anti-patterns.md | DEFERRABLE | When designing prompts, reviewing outputs, or debugging quality issues |
| agent-templates.md | ESSENTIAL | Inline into main SKILL.md—required for every agent prompt |
| report-formats.md | ESSENTIAL | Inline into main SKILL.md—required for every agent prompt |

## Implementation Notes

**For ESSENTIAL references:**
- Integrate agent-templates.md and report-formats.md into the main SKILL.md body as dedicated sections
- Preserve all content—do not summarize or excerpt
- Update internal cross-references to point to the new section headers

**For DEFERRABLE references:**
- Keep as separate reference files
- Strengthen the loading gates in the main body by converting @references/foo.md mentions into explicit conditional read instructions
- Example: Replace "see @references/tier-playbook.md" with "When launching Tier 2, read tier-playbook.md Tier 2 section for agent count heuristics and completion gates"

The skill's correctness depends on agent prompt construction quality. Making templates immediately available (ESSENTIAL) while keeping tier-specific heuristics and anti-pattern checklists accessible on-demand (DEFERRABLE) balances activation speed with execution reliability.
