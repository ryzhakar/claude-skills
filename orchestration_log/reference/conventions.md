# Conventions
Last updated: 2026-04-14

Established patterns and principles governing plugin development in this marketplace. All conventions trace to observed model behavior, documented platform constraints, or empirical optimization results.

## Source Documents

Primary sources:
- /Users/ryzhakar/pp/claude-skills/ETHOS.md - Plugin design principles
- /Users/ryzhakar/pp/claude-skills/CLAUDE.md - Repository management rules

This document consolidates operational patterns from both sources plus conventions established through practice.

---

## Self-Containment Principle

**Core rule:** Skills and agents work without reference file reads.

**Rationale:** Models ignore @references in practice. Content not in the body does not get followed. (ETHOS.md line 7)

**Implementation:**
- Inline all essential content directly in SKILL.md or agent .md files
- Compress through prose tightening, not through deferral to files
- No @reference patterns in production skills

**Survival test for references (all three must hold):**
1. Genuinely rare trigger condition
2. Large after compression (>1000t)
3. Unavoidable loading gate that makes skipping impossible

**Cross-skill content sharing:** When skills share reference content, each inlines its own domain deeply and the other domain lightly. Cross-skill duplication for self-containment is acceptable. (ETHOS.md line 11)

**Historical note:** Reference pattern used before 2026-04-13. Compression wave eliminated all references from active skills. Analysis artifacts in orchestration_log/recon/2026-04-13/ document the transition.

---

## Strong Directive Language

**Core rule:** Write commands, not suggestions. Models need a strong hand.

**Patterns:**
- "Do X" not "Consider doing X"
- "NEVER Y" not "Try to avoid Y"
- Emphatic markers (MUST, NEVER, CRITICAL) are intentional design

**Claude 4.6 refinement:** One emphatic marker per directive. Calm force beats shouted repetition. Avoid stacking multiple aggressive markers on one instruction. (ETHOS.md line 17)

**Examples:**
- Good: "NEVER commit without tests."
- Avoid: "You MUST NEVER EVER commit without tests under ANY circumstances."

**Preservation rule:** When editing skills, preserve emphatic markers. Their presence is deliberate, not accidental verbosity.

---

## Token Economy

**Measurement:** Use `just tokens FILE` for all token counts.

**Compression strategies (Strunk & White principles):**
1. Active voice over passive
2. Positive form over negative ("Do X" not "Don't skip X")
3. Concrete language over abstract
4. Omit needless words
5. Parallel construction in lists/tables
6. Emphatic position - important words at sentence start/end

**Specific patterns:**
- Tables replace prose for mappings
- Decision trees replace explanatory paragraphs
- Bulleted checklists replace procedural narratives when structure is parallel

**Target guidelines (soft limits):**
- Skills: aim for <5000t (exceptions justified by scope)
- Agents: aim for <2000t
- Individual sections: compress when >500t

**Source:** ETHOS.md line 21 + bridge-research/prompt-compression-strategies.md from 2026-04-13 analysis.

---

## No Platform Coupling

**Core rule:** Skills produce file artifacts, not platform API calls.

**Prohibited:**
- Direct GitHub API calls (gh issue create, gh pr create, etc.)
- Platform-specific workflows baked into skill logic
- External service dependencies without MCP abstraction

**Permitted:**
- Writing files to disk (issues/, prs/, reports/)
- Using local git operations (read-only preferred)
- Reading from platform (gh issue view) if needed for context

**Rationale:** Output is documents on disk. The user decides where to publish. (ETHOS.md line 25)

**Exception:** plugin-dev:mcp-integration skill teaches MCP server configuration for external integrations when needed. The abstraction layer (MCP) is the platform boundary.

---

## Verb Interpretation for Orchestrators

**Scope:** Applies to orchestration skills: agentic-delegation, dev-orchestration, research-tree, qa-orchestration.

**Core rule:** User action verbs ("do", "make", "research", "implement", "fix", "write", "check") are delegation directives. The orchestrator decomposes, delegates, and assembles - it never executes.

**Pattern in skill text:**
- "You are the orchestrator. Agents execute. You decide what, how much, and when."
- "Launch Agent X to do Y. Do not do Y yourself."
- Workflow sections specify agent dispatch, not direct tool use

**Rationale:** Orchestrators that try to execute tasks directly collapse into monolithic procedures. Delegation discipline maintains separation of concerns. (ETHOS.md line 29)

---

## Platform Facts, Not Policy Rules

**Core rule:** State what the platform does, not what the agent should do.

**Pattern:**
- Good: "Agents cannot launch other agents - the Agent tool is unavailable to subagents" (platform fact)
- Avoid: "Agents must not launch other agents" (policy rule implying choice)

**Rationale:** Facts eliminate ambiguity. Policy rules suggest optional compliance. When describing system constraints, state the constraint mechanism, not the desired behavior. (ETHOS.md line 33)

**Application areas:**
- Tool availability in subagent contexts
- File system permissions
- API rate limits
- Model tier capabilities

---

## Hooks: Modularity and Gating

**One-time hooks can be thorough:** SessionStart, PostCompact, SubagentStart are context injections, not per-call overhead. They can be verbose if needed. (ETHOS.md line 37)

**Per-call hooks must be lean:** PreToolUse, PostToolUse run on every tool invocation. Minimize token cost.

**Template extraction pattern:** Extract prompt text into template files (hooks/templates/*.txt) for modularity. Load via command hooks calling bash scripts.

**Gating rule:** Gate all hooks on config existence. A hook must be invisible when unconfigured. No default-on behavior that requires user opt-out.

**Example structure (manifesto plugin):**
```
hooks/
  hooks.json          # Hook registration
  session-start.sh    # SessionStart command
  post-compact.sh     # PostCompact command
  subagent-start.sh   # SubagentStart command
  templates/
    manifesto-inject.txt  # Template text loaded by scripts
```

**Current adoption:** 1/8 plugins (manifesto) use hooks. Others have not identified hook-worthy patterns.

---

## Core Points as Untouchable Spine

**Analysis pattern:** When optimizing a skill, identify its 5 core points first - what it most emphatically communicates. (ETHOS.md line 40)

**Implementation rule:** Core points survive and remain the most prominent elements in any rewrite. Compression amplifies core points; it never buries them.

**Process:**
1. D2 analysis identifies core points from current skill
2. Synthesis marks core points as "untouchable"
3. Implementation preserves core point prominence (section headers, emphatic position, verbatim text)

**Example (from defensive-planning synthesis):**
- Core point: "The implementer will optimize for 'appears done' over 'is done.'"
- Preserved verbatim in restructure
- Moved to prominent section position
- Emphatic markers retained

**Validation:** After optimization, check that core points are findable within first 2 pages and retain emphatic language.

---

## Analysis Before Action

**Full optimization workflow:**
1. **D1: Reference Optionality** - Can references be removed? Three-filter survival test.
2. **D2: Core Points** - What are the 5 untouchable points? Identify spine.
3. **D3: Strunk Prose** - Apply Strunk & White principles. Active voice, positive form, concrete language, parallel construction.
4. **D4: Prompt-Eval** - Score against prompt quality rubric. Identify vague terms, missing examples, weak structure.
5. **Bridge Research** - Gather compression strategies, platform criteria, pattern libraries.
6. **Synthesis** - Per-unit synthesis document with specific cut/restructure/strengthen recommendations.
7. **Implementation** - Apply synthesis recommendations. One PR per plugin or logical unit.

**Artifact location:** orchestration_log/recon/YYYY-MM-DD/scouts/

**Retention:** Keep all analysis artifacts for audit trail and pattern library.

**Source:** ETHOS.md line 45 + actual workflow from 2026-04-13 compression wave.

---

## Plugin Structure Patterns

**Standard layout:**
```
plugin-name/
  .claude-plugin/
    plugin.json          # Metadata, version (source of truth)
  skills/
    skill-name/
      SKILL.md           # Skill implementation (no version field)
      examples/          # Optional worked examples
  agents/
    agent-name.md        # Agent implementation
  hooks/
    hooks.json           # Hook registration
    *.sh                 # Command hook scripts
    templates/           # Template files loaded by hooks
  .mcp.json              # Optional MCP server config
```

**Key rules:**
- Versions live in plugin.json ONLY (CLAUDE.md line 9)
- Skill frontmatters do not carry version fields
- Never increment major versions without explicit user approval (CLAUDE.md line 10)

**Naming:**
- Skills: kebab-case (spec-chef, triage-issue)
- Agents: kebab-case (executor-agent, implementer)
- Plugins: kebab-case (dev-discipline, qa-automation)

---

## Git Commit Conventions

**Conventional commits format:**
```
type(scope): description

[optional body]
```

**Types:**
- feat: New feature (minor version bump)
- fix: Bug fix (patch version bump)
- refactor: Code restructure without behavior change (patch)
- doc: Documentation only (no version bump)
- test: Test changes (no version bump)

**Scope:** Plugin name or component (e.g., qa-automation, orchestration, CLAUDE)

**Examples from recent history:**
- `feat: session-close skill for orchestration LEAVE protocol`
- `fix(qa-automation): clean stale hook references after hooks removal`
- `refactor(orchestration): instruction compression`
- `doc(CLAUDE): document maintenance principles`

**Version increment timing:** Bump version in plugin.json in the same commit as the feature/fix.

---

## Versioning Policy

**Source of truth:** plugin.json version field ONLY. Skill/agent files do not carry version metadata.

**Increment rules:**
- Major (X.0.0): NEVER without explicit user approval
- Minor (0.X.0): New skills, new agents, new features, API additions
- Patch (0.0.X): Compression, fixes, refactors, documentation

**Rationale:** Major version bumps signal breaking changes. Only user can determine if ecosystem impact justifies major increment. (CLAUDE.md line 10 + MEMORY.md feedback_semver_majors.md)

**Gray area (observed in practice):**
- qa-automation 2.0.0 → 3.0.0: skill/agent refactor (major)
- manifesto 1.1.0 → 2.0.0: new behavioral binding skill (major)

Both incremented during 2026-04-13 compression wave. Unclear if user explicitly approved or if automation made judgment. Policy may need clarification.

---

## Testing and Validation

**TDD enforcement:** dev-discipline:tdd skill teaches test-first development. No formalized CI/CD for plugins themselves yet.

**Validation methods:**
1. Token count verification: `just tokens FILE` before/after
2. Skill invocation testing: Manual trigger with test scenarios
3. Agent dispatch testing: Invoke via orchestration skills
4. Synthesis artifact review: Check D1-D4 + synthesis documents for completeness

**Quality gates (from defensive-planning):**
- No placeholder language (TODO, TBD, "implement later")
- No references to undefined types/functions
- All examples include actual code, not descriptions of code
- Completion criteria are measurable

**Hook testing:** SessionStart/PostCompact/SubagentStart hooks tested via actual session lifecycle. No unit test framework for hooks.

---

## Documentation Standards

**NEVER create documentation files unless explicitly requested:** No proactive README.md, GUIDE.md, or markdown docs. (Standard Claude Code practice)

**Permitted documentation:**
- SKILL.md (required for skills)
- Agent .md files (required for agents)
- ETHOS.md, CLAUDE.md (repository-level governance)
- orchestration_log/ artifacts (analysis records)
- This file (conventions.md) and siblings (codebase_state.md, deferred_items.md)

**Frontmatter format (skills):**
```yaml
---
description: One-line description matching plugin.json
trigger: When to invoke (natural language)
---
```

**Frontmatter format (agents):**
```yaml
---
description: One-line role description
tools: [tool1, tool2]  # Optional
color: blue            # Optional
---
```

**Version fields:** NEVER in skill/agent frontmatter. Only in plugin.json.

---

## Plugin Development Skills

**Namespace:** plugin-dev:*

**Available skills:**
- plugin-dev:create-plugin - Guided end-to-end creation
- plugin-dev:mcp-integration - .mcp.json configuration
- plugin-dev:skill-development - Skill creation guidance
- plugin-dev:command-development - Command/slash command creation
- plugin-dev:plugin-settings - .local.md / settings management
- plugin-dev:hook-development - Hook creation (PreToolUse, PostToolUse, etc.)
- plugin-dev:plugin-structure - Plugin scaffolding
- plugin-dev:agent-development - Agent creation guidance

**Usage convention:** Invoke plugin-dev skills when creating/modifying plugin structure. Don't reinvent patterns documented in those skills.

**Reference:** CLAUDE.md line 3 - "Make use of plugin-dev:* skills and agents as much as possible."

---

## Orchestration Patterns

**Tier-based decomposition (research-tree):**
1. Ground truth tier - establish baseline
2. Survey tier - broad coverage
3. Deep dive tier - verification
4. Later tiers as needed (synthesis, contradiction resolution)

**Swarm density allocation (research-tree, qa-automation):**
- Allocate agent granularity by expected hit density
- Don't uniformly subdivide search space
- High-density areas get more agents; sparse areas get fewer

**Tier ordering discipline:**
- Never launch later tiers before earlier tiers complete
- Ground truth informs search design
- Parallel execution WITHIN tiers, sequential BETWEEN tiers

**Source:** MEMORY.md feedback_swarm_decomposition.md + feedback_tier_ordering.md

---

## Model Selection

**Tier mapping (from orchestration skills):**
- Haiku: Parsing, routing, deterministic transforms
- Sonnet: Analysis, judgment, synthesis, orchestration
- Opus: Deep reasoning, contradiction resolution, novel pattern detection

**Cost discipline:** Agent costs negligible compared to thoroughness guarantees. Never optimize for fewer dispatches if it compromises result quality. (MEMORY.md feedback_agent_costs.md)

**Orchestrator model:** Always Sonnet or Opus. Orchestration is judgment-intensive.

---

## Session Persistence (ARRIVE/WORK/LEAVE)

**Framework:** session-close skill implements LEAVE protocol for multi-session workflows.

**Layers:**
1. **reference/** - Living reference documents (this file, codebase_state.md, deferred_items.md)
2. **recon/** - Raw scouting data (gitignored, ephemeral)
3. **Session record** - What was done, what's next, blockers

**ARRIVE:** Load reference/ documents to understand current state.
**WORK:** Update reference/ as understanding evolves. Write to recon/ for scratch work.
**LEAVE:** session-close skill writes session record and updates reference/ documents.

**Adoption:** Framework established 2026-04-13. Adoption monitoring in progress.

---

## Quality Principles

**From ETHOS.md:**
1. Self-containment beats modularity
2. Strong directives beat suggestions
3. Token efficiency through prose quality, not through deferral
4. Platform facts beat policy rules
5. Core points are untouchable
6. Analysis before action

**Compression goal:** Reduce tokens while amplifying core points. If compression buries essential content, it failed.

**Validation:** Can a fresh reader execute the skill's workflow from the text alone, without external references or implied knowledge?

---

## Evolution and Feedback

**Memory system:** /Users/ryzhakar/.claude-competera/projects/-Users-ryzhakar-pp-claude-skills/memory/MEMORY.md

**Recorded patterns:**
- Swarm decomposition by density (not uniformly)
- Research tier ordering (sequential between tiers, parallel within)
- No major version bumps without approval
- Agent costs negligible (thoroughness over efficiency)

**Convention updates:** This file (conventions.md) is a living reference. Update when new patterns emerge or old patterns prove ineffective.

**Feedback loop:** Analysis artifacts → synthesis → implementation → observation → memory → updated conventions.
