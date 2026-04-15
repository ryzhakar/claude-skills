# Codebase State
Last updated: 2026-04-15

## Plugin Inventory

| Plugin | Version | Skills | Agents | Hooks |
|--------|---------|--------|--------|-------|
| dev-discipline | 1.3.0 | 6 | 3 | 0 |
| manifesto | 2.1.0 | 2 | 0 | 3 |
| orchestration | 2.6.0 | 4 | 0 | 0 |
| product-craft | 1.1.0 | 2 | 0 | 0 |
| prompt-engineering | 1.1.0 | 2 | 0 | 0 |
| python-tools | 1.1.0 | 2 | 0 | 0 |
| qa-automation | 3.1.0 | 1 | 4 | 0 |
| userland-utilities | 1.0.0 | 1 | 0 | 0 |
| **TOTAL** | - | **20** | **7** | **3** |

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
| dev-orchestration | orchestration | 3684 | No | Compressed |
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

| Hook Type | Plugin | Trigger | Purpose |
|-----------|--------|---------|---------|
| SessionStart | manifesto | startup/resume | Initialize manifesto binding |
| PostCompact | manifesto | * | Re-bind manifesto after compaction |
| SubagentStart | manifesto | * | Inject manifesto into subagent context |

All hooks implemented as command hooks calling bash scripts in manifesto/hooks/.

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

## Recent Changes (Since 2026-04-14)

**Verification feedback applied (session 2026-04-14/15):**
- agentic-delegation: feedback-driven update (6054t, up from 5991t)
- session-close: feedback-driven update (3273t, up from 2286t) — cost source clarity, conditional LEAVE gates, agent count groupings, worktree isolation note
- qa-orchestration: feedback-driven update (4353t, up from 4118t) — QA-context-specific derivation

**New components:**
- instruction-writer agent added at .claude/agents/ (project-local, not shipped in any plugin)
- implementer agent gained `isolation: worktree` field (dev-discipline 1.3.0)

**Versioning:**
- dev-discipline: 1.2.0 → 1.3.0 (implementer worktree isolation)
- manifesto: 2.0.0 → 2.1.0 (minor update)
- orchestration: 2.4.0 → 2.6.0 (session-close + feedback updates)
- qa-automation: 3.0.0 → 3.1.0 (qa-orchestration feedback update)

## Known Limitations

1. **Reference file pattern not eliminated:** prompt-optimize mentions references/ pattern in instructional content (line 113). Not a functional reference but suggests historical pattern.

2. **Token measurement coverage:** All current skills/agents measured with `just tokens`. Template files not measured separately.

3. **Userland-utilities exclusion:** fix-macos-app (263t) excluded from optimization by design — practical utility over theoretical purity.

4. **Large skill persistence:** research-tree (7565t) remains large after compression. This is the irreducible operational surface for 6-tier multi-agent orchestration. agentic-delegation (6054t) similarly justified by scope.

5. **Hook coverage:** Only manifesto plugin uses hooks. Other plugins have not identified hook-worthy patterns yet.

6. **MCP integration:** No plugins currently use .mcp.json despite plugin-dev:mcp-integration skill existing.

7. **instruction-writer not in plugin:** Agent lives at .claude/agents/ (project-local). Auto-discovery works, but it is not packaged in any plugin. May need plugin placement for portability.

## Next Actions

1. **Monitor research-tree implementation:** Synthesis recommendations from 2026-04-13 analysis call for inlining 4 reference files (agent-templates, report-formats, tier-playbook, anti-patterns). Not yet implemented. Expected net reduction: -2,128t system total.

2. **Validate compression quality:** Synthesis documents exist for 18/20 skills + all agents. Implementation PRs merged. No quality regression reports yet.

3. **Session-close adoption:** Skill updated and clarified (2026-04-15). Monitor for adoption in multi-session workflows.

4. **instruction-writer placement decision:** Decide whether to package as a dev-discipline agent or create a plugin-dev component.

5. **Deferred items tracking:** See deferred_items.md for synthesis recommendations not yet implemented.

6. **Convention documentation:** See conventions.md for established patterns.
