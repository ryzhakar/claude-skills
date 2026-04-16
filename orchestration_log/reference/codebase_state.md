# Codebase State
Last updated: 2026-04-16

## Plugin Inventory

| Plugin | Version | Skills | Agents | Hooks |
|--------|---------|--------|--------|-------|
| dev-discipline | 1.4.0 | 7 | 3 | 2 |
| manifesto | 2.1.0 | 2 | 0 | 3 |
| orchestration | 3.1.0 | 3 | 0 | 2 |
| product-craft | 1.1.0 | 2 | 0 | 0 |
| prompt-engineering | 1.1.0 | 2 | 0 | 0 |
| python-tools | 1.1.0 | 2 | 0 | 0 |
| qa-automation | 3.1.0 | 1 | 4 | 0 |
| userland-utilities | 1.0.0 | 1 | 0 | 0 |
| **TOTAL** | - | **20** | **7** | **7** |

## Skill Inventory

| Skill | Plugin | Tokens | Has Refs | Status |
|-------|--------|--------|----------|--------|
| defensive-planning | dev-discipline | 2741 | No | Compressed |
| systematic-debugging | dev-discipline | 2589 | No | Compressed |
| triage-issue | dev-discipline | 1226 | No | Compressed |
| improve-architecture | dev-discipline | 1441 | No | Compressed |
| receiving-code-review | dev-discipline | 1385 | No | Compressed |
| tdd | dev-discipline | 1559 | No | Compressed |
| manifesto-writing | manifesto | 1243 | No | Compressed |
| manifesto-oath | manifesto | 2192 | No | Compressed |
| agentic-delegation | orchestration | 6054 | No | Compressed |
| research-tree | orchestration | 7565 | No | Compressed |
| session-close | orchestration | 3273 | No | Compressed |
| dev-orchestration | dev-discipline | 3684 | No | Compressed, moved from orchestration |
| spec-chef | product-craft | 1730 | No | Compressed |
| user-story-chef | product-craft | 1498 | No | Compressed |
| prompt-eval | prompt-engineering | 3138 | Yes* | Compressed |
| prompt-optimize | prompt-engineering | 2693 | Yes* | Compressed |
| uv-pyright-debug | python-tools | 1092 | No | Compressed |
| python-ast-mass-edit | python-tools | 1270 | No | Compressed |
| qa-orchestration | qa-automation | 4353 | No | Compressed |
| fix-macos-app | userland-utilities | 263 | No | Excluded from optimization |

*References mentioned in instructional content but not used as separate loadable files.

## Agent Inventory

| Agent | Plugin | Tokens | Isolation | Status |
|-------|--------|--------|-----------|--------|
| implementer | dev-discipline | 1004 | worktree | Compressed |
| spec-reviewer | dev-discipline | 782 | none | Compressed |
| code-quality-reviewer | dev-discipline | 1104 | none | Compressed |
| executor-agent | qa-automation | 1891 | none | Compressed |
| generator-agent | qa-automation | 2695 | none | Compressed |
| healer-agent | qa-automation | 3190 | none | Compressed |
| planner-agent | qa-automation | 1922 | none | Compressed |

**Local (not shipped):**
| Agent | Location | Tokens | Purpose |
|-------|----------|--------|---------|
| instruction-writer | .claude/agents/ | 802 | Edits skill/agent instruction files. Not a plugin component — project-local tooling. |

## Hooks Inventory

| Hook Type | Plugin | Matcher | Purpose |
|-----------|--------|---------|---------|
| SessionStart | manifesto | startup\|resume | Initialize manifesto binding |
| PostCompact | manifesto | * | Re-bind manifesto after compaction |
| SubagentStart | manifesto | * | Inject manifesto into subagent context |
| SubagentStop | dev-discipline | implementer | Inject spec-review mandate after implementer stops |
| SubagentStop | dev-discipline | spec-reviewer | Inject quality-review mandate after spec review stops |
| SessionStart | orchestration | startup\|resume | ARRIVE context injection — inject reference doc paths |
| PostCompact | orchestration | * | ARRIVE re-injection after compaction wipes context |

All hooks implemented as `type: "command"` calling bash scripts with template-based output. Prompt hooks (`type: "prompt"`) investigated and rejected — pervasive bugs, zero real-world adoption. See docs/hooks-reference.md for the full authoritative reference.

## Token Distribution

**Total skill tokens:** 50,989t across 20 skills (avg: 2,549t)
**Total agent tokens:** 12,588t across 7 agents (avg: 1,798t)
**System total:** 63,577t (excludes local instruction-writer agent)

**Size categories:**
- Micro (<500t): 1 skill (fix-macos-app)
- Small (500-1500t): 7 skills
- Medium (1500-3000t): 6 skills, 3 agents
- Large (3000-6000t): 4 skills, 3 agents
- XL (6000t+): 2 skills (agentic-delegation, research-tree)

## Recent Changes (Since 2026-04-15)

**Session 2026-04-16 — Major restructure:**

1. **dev-orchestration moved** from orchestration to dev-discipline plugin. Co-located with its agents (implementer, spec-reviewer, code-quality-reviewer). orchestration bumped to 3.0.0 (breaking).

2. **Review chain hooks added** to dev-discipline:
   - SubagentStop (implementer) → injects spec-review mandate
   - SubagentStop (spec-reviewer) → injects quality-review mandate
   Review is now structurally inevitable via hook enforcement, not just skill documentation.

3. **Worktree discipline enforced end-to-end:**
   - implementer: verifies branch on start, reports branch+SHA in status
   - spec-reviewer + code-quality-reviewer: worktree-aware (read from implementer's branch)
   - dev-orchestration: dispatch protocol includes worktree context

4. **Hook research completed:**
   - Prompt hooks (`type: "prompt"`) investigated: broken on Stop, PreToolUse; zero adoption. Rejected.
   - Command hooks (`type: "command"`) investigated: reliable except subagent bypass and CLAUDE_PLUGIN_ROOT injection.
   - Consolidated authoritative reference: docs/hooks-reference.md (893 lines)

5. **Orchestration ARRIVE hooks added:**
   - SessionStart (startup|resume) + PostCompact (*) inject reference doc paths
   - Gated on orchestration_log/reference/ existence — invisible when unconfigured
   - orchestration bumped to 3.1.0

5. **Hook opportunity audit** across all 8 plugins completed. Priorities identified for orchestration (ARRIVE/SubagentStop), qa-automation (phase gate chain), python-tools (bare pyright block).

**Versioning:**
- dev-discipline: 1.3.0 → 1.4.0 (dev-orchestration moved in, hooks added, worktree discipline)
- orchestration: 2.6.0 → 3.0.0 (breaking: dev-orchestration removed)

## Known Limitations

1. **Reference file pattern not eliminated:** prompt-optimize mentions references/ pattern in instructional content (line 113). Not a functional reference but suggests historical pattern.

2. **Token measurement coverage:** All current skills/agents measured with `just tokens`. Template files not measured separately.

3. **Userland-utilities exclusion:** fix-macos-app (263t) excluded from optimization by design — practical utility over theoretical purity.

4. **Large skill persistence:** research-tree (7565t) remains large after compression. This is the irreducible operational surface for 6-tier multi-agent orchestration. agentic-delegation (6054t) similarly justified by scope.

5. **Hook coverage:** manifesto (3 hooks) and dev-discipline (2 hooks) use hooks. Hook opportunities identified for orchestration, qa-automation, python-tools, prompt-engineering — pending implementation.

6. **MCP integration:** No plugins currently use .mcp.json despite plugin-dev:mcp-integration skill existing.

7. **instruction-writer not in plugin:** Agent lives at .claude/agents/ (project-local). Auto-discovery works, but it is not packaged in any plugin. May need plugin placement for portability.

## Next Actions

1. **Monitor research-tree implementation:** Synthesis recommendations from 2026-04-13 analysis call for inlining 4 reference files (agent-templates, report-formats, tier-playbook, anti-patterns). Not yet implemented. Expected net reduction: -2,128t system total.

2. **Validate compression quality:** Synthesis documents exist for 18/20 skills + all agents. Implementation PRs merged. No quality regression reports yet.

3. **Session-close adoption:** Skill updated and clarified (2026-04-15). Monitor for adoption in multi-session workflows.

4. **instruction-writer placement decision:** Decide whether to package as a dev-discipline agent or create a plugin-dev component.

5. **Deferred items tracking:** See deferred_items.md for synthesis recommendations not yet implemented.

6. **Convention documentation:** See conventions.md for established patterns.
