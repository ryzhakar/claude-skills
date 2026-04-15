# Deferred Items
Last updated: 2026-04-15

## Synthesis Recommendations Not Yet Implemented

### 1. research-tree Reference Inlining (High Priority)

**Source:** orchestration_log/recon/2026-04-13/scouts/synthesis/research-tree.md

**Current state:** research-tree SKILL.md (7565t) references four separate files that are not currently used as references but were analyzed for potential inlining:
- agent-templates.md (2474t) - agent prompt skeletons
- report-formats.md (1783t) - output format templates
- tier-playbook.md (2064t) - tier transition heuristics
- anti-patterns.md (2222t) - failure mode catalog

**Synthesis recommendation:** Inline all four files with compression:
- agent-templates.md → 2300t inlined (save 174t)
- report-formats.md → 1700t inlined (save 83t)
- tier-playbook.md → 1200t inlined (save 864t)
- anti-patterns.md → 1400t inlined (save 822t)

**Net effect:** Body grows from 7565t to ~9287t, but 8543t in references eliminated. System total: 11,415t → 9,287t (-2,128t, -18.6%).

**Rationale:** "Models ignore references in practice. Content not in the body does not get followed." (ETHOS.md line 7)

**Status:** Deferred pending user approval for major restructure of largest skill.

### 2. prompt-optimize Reference Pattern Removal (Low Priority)

**Source:** orchestration_log/recon/2026-04-13/scouts/synthesis/prompt-optimize.md

**Current state:** Line 113 of prompt-optimize/SKILL.md mentions references/ pattern in instructional content: "After: SKILL.md (200 lines, core workflow) + references/ (patterns.md, examples.md, edge-cases.md)."

**Issue:** This is not a functional @reference but appears in example/explanation text showing a before/after optimization scenario. Could confuse readers about whether references are still used.

**Synthesis recommendation:** Rewrite example to avoid references/ pattern in "After" state, or explicitly label it as anti-pattern.

**Status:** Deferred - cosmetic issue, no functional impact.

### 3. D4 Prompt-Eval Findings Remediation (Medium Priority)

**Source:** orchestration_log/recon/2026-04-13/scouts/d4-prompt-eval/*.md

Analysis identified specific quality gaps across skills. Sample findings:

**agentic-delegation (line 244):**
- Finding: TODO mentioned in instructions
- Context: "If external references don't exist yet, mark them as TODO or create them"
- Fix: Remove TODO pattern reference
- Status: Checked 2026-04-15 — no TODO reference found in current file. Resolved in verification feedback wave.

**dev-orchestration (line 59):**
- Finding: Completion criteria includes "no TBD/TODO/placeholder language"
- Context: This is correct (anti-pattern detection) but appears in table
- Fix: No change needed - this is intentional detection language
- Status: Confirmed correct

**Status:** Most D4 findings addressed in compression wave + verification feedback wave (2026-04-14/15). Remaining items tracked here.

### 4. instruction-writer Plugin Placement (Low Priority)

**Current state:** instruction-writer agent lives at .claude/agents/ (project-local). Not packaged in any plugin. Auto-discovery works within this project.

**Issue:** Not portable to other Claude Code sessions or installations. Users of individual plugins cannot get the agent without cloning the full repo.

**Options:**
1. Add to dev-discipline plugin (it is a development discipline tool)
2. Create a new plugin-dev component
3. Leave as project-local tooling (current state)

**Status:** Deferred pending user decision on packaging strategy.

## Excluded from Optimization

### userland-utilities Plugin

**Rationale:** Per CLAUDE.md and project conventions, userland-utilities contains practical system utilities that prioritize pragmatic function over theoretical purity.

**Current state:**
- fix-macos-app: 263t (micro skill)
- No agents, no hooks
- Addresses macOS Gatekeeper/code signing issues

**Decision:** Excluded from compression analysis and token optimization. Maintained as-is for utility value.

**Review cadence:** Only if user reports quality issues or requests updates.

## TODO Comments in Production Code

**Legitimate uses (anti-pattern detection):**

1. **defensive-planning SKILL.md (lines 21, 153, 185):**
   - Context: Examples of what implementers do wrong: "Write `pass` or `TODO` and move on"
   - Purpose: Teaching what NOT to do
   - Action: None - these are intentional negative examples

2. **dev-orchestration SKILL.md (line 59):**
   - Context: Completion gate checklist includes "no TBD/TODO/placeholder language"
   - Purpose: Quality enforcement
   - Action: None - this is correct

3. **research-tree SKILL.md (line 367):**
   - Context: Architecture Auditor task includes "Find code quality signals (TODOs, FIXMEs, lint suppressions)"
   - Purpose: Detection instruction for audit agent
   - Action: None - this is correct

4. **qa-orchestration SKILL.md (line 310):**
   - Context: "Generator must not log implementation gaps... verify each has non-placeholder values (not 'TODO', 'needs implementation', empty strings)"
   - Purpose: Validation instruction
   - Action: None - this is correct

**No action items.** All TODO mentions are in instructional/anti-pattern contexts, not actual deferred work.

## Analysis Artifacts Not Yet Processed

**Location:** orchestration_log/recon/2026-04-13/scouts/

**Structure:**
- d1-ref-optionality/ - Reference optionality analysis (18 files)
- d2-core-points/ - Core points identification (11 files)
- d3-strunk/ - Strunk & White prose analysis (9 files)
- d4-prompt-eval/ - Prompt evaluation scoring (12 files)
- bridge-research/ - Compression strategies research (1 file)
- synthesis/ - Final synthesis recommendations (20 files)

**Status:** Synthesis phase complete. Most recommendations implemented in compression wave (commits 038045b through fea6202) and verification feedback wave (2026-04-14/15). Remaining items documented above.

**Retention:** Keep all analysis artifacts for:
1. Audit trail for versioning decisions
2. Pattern library for future optimization work
3. Evidence base for ETHOS.md principles

**Next review:** When next optimization cycle begins or when quality regression detected.

## Quality Gaps Identified But Not Addressed

### 1. Large Skill Size Guideline Violations

**Issue:** research-tree (7565t) and agentic-delegation (6054t) exceed informal 5000t guideline.

**Analysis verdict (from synthesis):** "This is not bloat -- it is the irreducible operational surface."

**Mitigation:** Both skills govern multi-tier orchestration workflows with templates. Alternative (reference files) demonstrably fails per ETHOS.md. Size justified.

**Status:** Accepted as necessary exception. Documented in codebase_state.md.

### 2. Hook Coverage

**Issue:** Only 1/8 plugins use hooks (manifesto).

**Analysis:** Most plugins contain skills (judgment-heavy workflows) rather than deterministic enforcement patterns. Hooks require:
- Clear trigger condition
- Deterministic action
- Per-invocation justifiable overhead (or one-time SessionStart/PostCompact/SubagentStart)

**Status:** No action. Hook adoption is need-driven, not coverage-driven.

### 3. MCP Integration Absence

**Issue:** plugin-dev:mcp-integration skill exists but no plugins use .mcp.json.

**Analysis:** No current plugin requires external service integration. MCP infrastructure is available when needed.

**Status:** No action. Plugin creation is need-driven.

## Versioning Debt

**Issue:** All version increments since 2026-04-13 were minor/patch per CLAUDE.md line 10: "Never increment major versions without explicit user approval."

**Analysis:** Compression wave touched:
- qa-automation: 2.0.0 → 3.0.0 (major: skill/agent API surface changed)
- manifesto: 1.1.0 → 2.0.0 (major: new behavioral binding skill)
- All others: minor (feature) or patch (compression/fix)

**Question:** Were qa-automation 3.0.0 and manifesto 2.0.0 explicitly approved by user or auto-incremented by automation?

**Status:** Documented for review. If auto-incremented, consider policy clarification in CLAUDE.md.

## Session Persistence Adoption

**Issue:** session-close skill substantially updated 2026-04-15. Adds /cost discipline, conditional LEAVE gates, two-grouping agent counts. Unclear if workflows are adopting these patterns.

**Next action:** Monitor usage. If adopted, document patterns. If not adopted, investigate barriers.

**Status:** Observation period - no action yet.
