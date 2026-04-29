# Conventions
Last updated: 2026-04-29

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

## Bilateral Specification

**Core rule:** Every positive directive in skill or agent bodies pairs with an explicit negative prohibition.

**Rationale:** A skill that says "use X" without saying "do not use Y" leaves a gap. Loosely-prompted agents fill that gap with Y. Mandate language without prohibition language is a permission slip for invented alternatives.

**Format flexibility:** Hard Rules, "You do / You do NOT" scope, Iron Law + Hard Rejection list — formats vary by author. Bilateral coverage is mandatory; format is per-author discretion.

**Existing bilateral patterns in the marketplace:**
- generator-agent — Hard Rules section
- executor-agent — "You do / You do NOT" scope
- healer-agent — Iron Law + Hard Rejection list
- planner-agent — Iron Law only (gap closed session 2026-04-17 per F1)

**Application:** Coverage check during instruction-writer review. A positive directive without a paired prohibition fails review.

**Source:** Session 2026-04-17, codification of pattern observed across qa-automation agents.

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

## Hook Mandates: Unconditional Pattern

**Core rule:** SubagentStop hooks that inject orchestrator mandates MUST inject single unconditional commands, not conditional logic that requires the orchestrator to parse and branch.

**Rationale:** Orchestrators avoid work. A conditional mandate ("if PASS dispatch X; if FAIL dispatch Y") becomes an escape hatch — the orchestrator can drop the dispatch by claiming neither branch matched, by missing the parse, or by being distracted by user pressure. Observed in dev-discipline review chain: spec-reviewer hook had a conditional template, code-quality-reviewer dispatch silently failed in real usage.

**Pattern:**
- Hook injects ONE command: "Dispatch agent X with payload Y."
- Branching logic moves into the receiving agent — agent X reads its inputs and decides whether to short-circuit, not the orchestrator.
- Hook scripts stay simple `envsubst`. Don't move parsing into shell.

**Anti-pattern (rejected after spec-chef review 2026-04-29):**
- Shell script reads upstream artifact, parses verdict, selects template based on parse result. Overengineering — the simpler answer is to remove the conditional entirely and let the receiving agent handle the case.

**Example (dev-discipline 1.4.2):**
- `quality-review-mandate.txt` was conditional ("if PASS... if FAIL..."). Rewritten as single unconditional dispatch instruction. Code-quality-reviewer reads spec verdict at A3 itself and short-circuits if needed.
- New `code-quality-reviewer-stop.sh` follows the same shape: single unconditional merge-decision mandate.

**Source:** Session 2026-04-29 spec-chef session, dev-discipline 1.4.2 commit 6515da5.

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

## Artifact Contract Pattern

**Core rule:** Every multi-skill plugin with hierarchy (orchestrator skill + executor agents) carries an `## Artifact Contract` table near the top of its orchestrator skill.

**Format:**
```markdown
## Artifact Contract

| ID | Path | Producer | Consumer | Format | Required |
|----|------|----------|----------|--------|----------|
| A1 | <path with placeholders> | <agent or skill> | <agent or skill> | <markdown/json/yaml/...> | yes / conditional |
```

**Rules:**
- Path uses `${DATE}`, `${branch}`, `${stem}`, `${timestamp}` placeholders. No curly-brace alternative form.
- Producer and Consumer name roles that map clearly to dispatched agents, the orchestrator skill itself, downstream phases, or "human" / "next-session ARRIVE."
- Required: `yes` or `conditional` (with one-line note when conditional).
- The table is canonical. Body prose may reference rows by ID but MUST NOT contradict the table.

**Rationale:** Without a single greppable artifact contract, paths drift across agent bodies and orchestrator text. Drift is invisible until a phase-chain breakage exposes it. Inline markdown table beats an external `.claude-plugin/artifacts.yaml` manifest because models ignore @references at runtime — the inline table is in the skill the orchestrator already loads.

**Adopted plugins (as of 2026-04-29):**
- `orchestration/skills/session-close/SKILL.md` (8 rows; commit cafdcb0)
- `dev-discipline/skills/dev-orchestration/SKILL.md` (6 rows; commit dffae16, extended in 6515da5)
- `qa-automation/skills/qa-orchestration/SKILL.md` (23 rows; commit e404157)

**Future hardening:** DI-5 proposes an audit-time linter that parses the table and verifies every declared path appears in the producer/consumer files. ~50 lines of shell or Python; pre-commit integration.

**Source:** Session 2026-04-29 marketplace artifact-ownership audit (recon/2026-04-24/artifact-ownership-audit/).

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
- `feat(manifestos): clear instructions on reading and interplay modeling`

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
isolation: worktree    # Optional — use when agent needs filesystem isolation
---
```

**Version fields:** NEVER in skill/agent frontmatter. Only in plugin.json.

---

## Agent Isolation

**Field:** `isolation: worktree` in agent frontmatter.

**Purpose:** Each dispatch of the agent operates in a separate git worktree — clean filesystem state, no cross-agent interference.

**When to use:** Agents that make code changes (write/edit files, run tests, commit). Prevents race conditions when multiple implementers run in parallel.

**Current adoption:** implementer agent in dev-discipline. Other agents (spec-reviewer, code-quality-reviewer, qa-automation agents) do not require isolation — they read or produce non-code artifacts.

**Platform fact:** Worktree isolation is a platform capability exposed via the `isolation` frontmatter field. Claude Code provisions the worktree; the agent does not need to manage it.

**Source:** dev-discipline 1.3.0, session 2026-04-15.

---

## Worktree Dispatches: Relative Paths Only

**Core rule:** When dispatching an agent with `isolation: "worktree"`, the dispatch prompt MUST use only relative paths for files the agent edits. Absolute paths into the main repo defeat isolation silently.

**Failure mode:** `isolation: "worktree"` provisions the agent an isolated git checkout, but `Edit`/`Write` tools resolve absolute filesystem paths normally. A path like `/Users/ryzhakar/pp/claude-skills/dev-discipline/...` resolves to MAIN's filesystem regardless of the agent's worktree. The agent's edits land in main; the worktree stays empty and may be auto-cleaned for "no changes."

**Pattern:**
- Cite files as `dev-discipline/skills/foo/SKILL.md` (relative to worktree root).
- Never cite as `/Users/.../dev-discipline/skills/foo/SKILL.md`.
- Exception: paths to gitignored directories not present in the worktree (e.g., `orchestration_log/recon/`) — absolute is correct because the directory does not exist in the worktree.
- Exception: external read-only context (e.g., a memo from another project) — absolute is correct because it is not in the marketplace at all.

**Defense in depth (dev-discipline 1.4.2):** Even if an orchestrator prompt leaks absolute paths, dev-discipline's implementer / spec-reviewer / code-quality-reviewer agents now defensively re-root marketplace-prefixed paths into their own worktree and surface re-rooted paths in their status report. Other agents (instruction-writer, general-purpose) do not yet have this defense — orchestrator-side prompt discipline remains the primary control.

**Observed failures:** Session 2026-04-29 dispatches A, C, and E each leaked at least one absolute path despite the discipline. DI-4 tracks the residual orchestrator-side gap.

**Related:** Platform-induced orchestrator CWD drift (DI-7) is a separate failure class — distinct from prompt-writing discipline. The orchestrator's CWD can shift into a worktree without explicit `cd`. Defense: keep `pwd`-check awareness; restore CWD when drift detected.

**Source:** Session 2026-04-29, DI-4 + DI-7. Defense landed in dev-discipline 1.4.2 commit 6515da5.

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

**Two-level synthesis (map-reduce) for large corpora:** When primary-source corpus exceeds ~500KB, decompose synthesis into per-section scouts (sonnet, parallel) followed by one opus assembler. Single-context synthesis on 600K+ tokens degrades quality. Use this strategy whenever section boundaries are cleanly defined (topic clusters, numbered sections, etc.).

**When it applies:** Research waves where the corpus is expected to span dozens of source pages and produce a multi-section reference document. The 2026-04-17 agents wave used 9 parallel section scouts + 1 opus assembler across 78 source files.

**Evidence:** `orchestration_log/recon/2026-04-17/agents-v2/synthesis/sections/` (11 section files) + `synthesis/REFERENCE.md` (assembled output). Session metrics at `orchestration_log/recon/2026-04-17/session_metrics.md` confirm opus used for assembly (strategic, high-output role).

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

## Cost Source Authority

**Rule:** `/cost` is the ONLY trusted cost source. No JSONL-derived cost numbers.

**Rationale:** JSONL double-counts subagent internals. Cost derived from JSONL message logs is structurally inflated and cannot be trusted.

**Verification before use:** Cross-verify `/cost` scope before trusting the number:
1. Wall time range matches the intended session.
2. No branching split the session (branched `/cost` covers only that branch).
3. No multi-session contribution inflates the number.

The verification confirms `/cost` reports for the right scope. It does not compute an alternative number.

**Capture location:** Verbatim `/cost` output lives in gitignored `orchestration_log/history/${DATE}/cost.md` (Artifact Contract row A9 in session-close). Cost numbers MUST NOT be embedded inline in `session.md` — the session record carries a pointer line only. The cost.md file matches `**/cost.md` in `.gitignore`; it is per-session, local-only, and NEVER committed. Cost data is operational (Status Snapshot per session-close Documentation Categories), not historical artifact.

**Source:** session-close SKILL.md, sessions 2026-04-15 and 2026-04-29. Formalized from observed JSONL double-counting behavior; gitignored capture pattern adopted 2026-04-29.

---

## Agent Count Reporting (Two Groupings)

**Convention:** Report agent counts in two separate tables, not one combined count.

**Table 1 — By model tier:** How many agents ran on haiku, sonnet, opus. Extract from `message.model` field in JSONL.

**Table 2 — By agent type:** How many of each `subagent_type` were dispatched (e.g., 5 implementers, 3 spec-reviewers, 15 research agents). Extract from agent metadata or `subagent_type` field.

**Rationale:** Model tier reveals cost distribution; agent type reveals work decomposition. Conflating them loses both signals.

**Source:** session-close SKILL.md Step 1, session 2026-04-15.

---

## Conditional LEAVE Steps

**Convention:** LEAVE Steps 3-4 (draft session record, draft reference doc updates) are conditional — skip if docs are already current.

**Gate condition:** If reference docs were updated within the current session — by agents running earlier LEAVE steps, or by the orchestrator editing reference docs directly — skip Steps 3-4. The orchestrator reviews existing docs in Step 5 instead.

**Purpose:** Prevents redundant agent dispatches when docs are already current. LEAVE protocol adapts to session state.

**Source:** session-close SKILL.md Step 3-4 gate, session 2026-04-15.

---

## instruction-writer Agent

**Location:** .claude/agents/instruction-writer.md (project-local, not in any plugin)

**Purpose:** Edits skill definitions, agent definitions, and hook templates. Specializes in applying ETHOS principles, Strunk compression, and core-point preservation to instruction files.

**When to invoke:** Rewriting, compressing, restructuring, or applying feedback to SKILL.md or agent .md files. The description includes trigger examples.

**Constitutional binding:** Before any edit, the agent reads the first-principles manifesto, ETHOS.md, and the Strunk SPR document. These govern its writing.

**Process:** (1) Read target file. (2) Identify 5 core points. (3) Apply changes. (4) Run `just tokens` before/after. (5) Report delta.

**Source:** Session 2026-04-14/15. Agent created to formalize instruction editing practice.

---

## Constitution Stack via .manifestos.yaml

**Convention:** Project-level manifesto bindings live in `.manifestos.yaml` at the project root, not embedded in CLAUDE.md.

**Format:** YAML list where each entry is auto-detected by shape:
- Plain name (`decomplect`): resolved via tiered protocol — Tier 1: manifesto repo, Tier 2: session skills, Tier 3: project files
- URL (`https://...`): fetched at initialization
- Local path (`./docs/principles.md`): read relative to project root

**Auto-activation:** manifesto plugin hooks read `.manifestos.yaml` at SessionStart (initialize), PostCompact (re-bind), and SubagentStart (full binding ceremony). Bindings activate automatically without user action each session.

**Fallback:** `## Active Manifestos` heading in CLAUDE.md. Names resolved against the manifesto repo.

**Source:** manifesto-oath SKILL.md Project Configuration section, session 2026-04-14/15.

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

**Adoption:** Framework established 2026-04-13. Substantially refined 2026-04-15 (cost source authority, conditional gates, two-grouping agent counts).

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
- No relay through orchestrator (agents write to disk directly)
- Verify agent disk output before declaring phase done
- Collapse references into body (models skip @references)

**Convention updates:** This file (conventions.md) is a living reference. Update when new patterns emerge or old patterns prove ineffective.

**Feedback loop:** Analysis artifacts → synthesis → implementation → observation → memory → updated conventions.

---

## Doc-Extraction Techniques

Conventions for fetching and processing Claude Code documentation pages at scale.

**Mintlify `.md` URL trick:** Appending `.md` to any `code.claude.com` docs URL returns the page as native markdown, bypassing the JS-rendered HTML shell. Use for any doc-extraction wave where scraping rendered HTML would be necessary otherwise. Example: `https://code.claude.com/docs/en/sub-agents.md` returns raw markdown.

**When it applies:** Any wave that reads Claude Code platform docs. Eliminates need for headless browser or HTML parsing.

**Evidence:** `orchestration_log/recon/2026-04-17/agents-v2/primary-sources/` — all 78 source files fetched via `.md` URL variant.

---

**Pre-computed citation index for deep linking:** When rewriting citations to deep-link URLs, pre-compute the heading anchor index via shell pipeline (awk over fetched `.md` files) and run the rewriter against that index. Never load primary-source files into context during the rewrite pass.

**When it applies:** Any wave where the assembled reference document cites specific passages in source docs. Scales to 100+ citations without blowing the context window.

**Evidence:** `orchestration_log/recon/2026-04-17/agents-v2/synthesis/citation-rewrite/heading-index.tsv` (1470 entries), `citations.tsv` (298 rows), `substitution-map.tsv` (298 rewrites). REPORT.md documents the outcome distribution.

---

## Constitution Reliability

**First Principles manifesto path is unreliable:** `/tmp/claude-manifesto-repo/LLM_MANIFESTOS/manifestos/Manifesto, first-principles - "break the mold".md` may be absent when agents start. Do not write binding preambles that treat local presence as the default. Every binding preamble must include the upstream fallback as a required step — Try local read; if absent, `curl -fsSL` from the raw GitHub URL.

**Fallback URL:** `https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/manifestos/Manifesto%2C%20first-principles%20-%20%22break%20the%20mold%22.md`

**When it applies:** Every agent dispatch preamble that binds to the First Principles manifesto. The pattern is already used in the 2026-04-17 task instructions and should be the canonical form going forward.

**Evidence:** 4+ scout agents in the 2026-04-17 wave encountered absent local file and fell back to upstream fetch. See `deferred_items.md` DI-1 for remediation tracking.
