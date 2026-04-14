# Codebase State
Last updated: 2026-04-14

## Plugin Inventory

| Plugin | Version | Skills | Agents | Hooks |
|--------|---------|--------|--------|-------|
| dev-discipline | 1.2.0 | 6 | 3 | 0 |
| manifesto | 2.0.0 | 2 | 0 | 3 |
| orchestration | 2.4.0 | 4 | 0 | 0 |
| product-craft | 1.1.0 | 2 | 0 | 0 |
| prompt-engineering | 1.1.0 | 2 | 0 | 0 |
| python-tools | 1.1.0 | 2 | 0 | 0 |
| qa-automation | 3.0.0 | 1 | 4 | 0 |
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
| manifesto-oath | manifesto | 1204 | No | Compressed |
| agentic-delegation | orchestration | 5991 | No | Compressed |
| research-tree | orchestration | 7565 | No | Compressed |
| session-close | orchestration | 2286 | No | New (2026-04-13) |
| dev-orchestration | orchestration | 3684 | No | Compressed |
| spec-chef | product-craft | 1730 | No | Compressed |
| user-story-chef | product-craft | 1498 | No | Compressed |
| prompt-eval | prompt-engineering | 3138 | Yes* | Compressed |
| prompt-optimize | prompt-engineering | 2693 | Yes* | Compressed |
| uv-pyright-debug | python-tools | 1092 | No | Compressed |
| python-ast-mass-edit | python-tools | 1270 | No | Compressed |
| qa-orchestration | qa-automation | 4118 | No | Compressed |
| fix-macos-app | userland-utilities | 263 | No | Excluded from optimization |

*References mentioned in instructional content but not used as separate loadable files.

## Agent Inventory

| Agent | Plugin | Tokens | Status |
|-------|--------|--------|--------|
| implementer | dev-discipline | 998 | Compressed |
| spec-reviewer | dev-discipline | 782 | Compressed |
| code-quality-reviewer | dev-discipline | 1104 | Compressed |
| executor-agent | qa-automation | 1891 | Compressed |
| generator-agent | qa-automation | 2695 | Compressed |
| healer-agent | qa-automation | 3190 | Compressed |
| planner-agent | qa-automation | 1922 | Compressed |

## Hooks Inventory

| Hook Type | Plugin | Trigger | Purpose |
|-----------|--------|---------|---------|
| SessionStart | manifesto | startup/resume | Initialize manifesto binding |
| PostCompact | manifesto | * | Re-bind manifesto after compaction |
| SubagentStart | manifesto | * | Inject manifesto into subagent context |

All hooks implemented as command hooks calling bash scripts in manifesto/hooks/.

## Token Distribution

**Total skill tokens:** 48,716t across 20 skills (avg: 2,436t)
**Total agent tokens:** 12,582t across 7 agents (avg: 1,797t)
**System total:** 61,298t

**Size categories:**
- Micro (<500t): 1 skill (fix-macos-app)
- Small (500-1500t): 8 skills, 0 agents
- Medium (1500-3000t): 7 skills, 5 agents
- Large (3000-6000t): 3 skills, 2 agents
- XL (6000t+): 1 skill (research-tree)

## Recent Changes (Since 2026-04-13)

**Compression wave completed:**
- dev-discipline: all 6 skills compressed
- product-craft: 2 skills compressed (triage-issue relocated to dev-discipline)
- orchestration: all 4 skills compressed
- qa-automation: 1 skill + 4 agents compressed
- prompt-engineering: 2 skills compressed
- python-tools: 2 skills compressed

**Versioning:**
- qa-automation: 2.0.0 → 3.0.0 (skill/agent refactor)
- manifesto: 1.1.0 → 2.0.0 (oath skill added)
- orchestration: 2.3.0 → 2.4.0 (session-close added)
- All others: patch or minor increments

## Known Limitations

1. **Reference file pattern not eliminated:** prompt-optimize mentions references/ pattern in instructional content (line 113). Not a functional reference but suggests historical pattern.

2. **Token measurement coverage:** All current skills/agents measured with `just tokens`. Template files not measured separately.

3. **Userland-utilities exclusion:** fix-macos-app (263t) excluded from optimization by design - practical utility over theoretical purity.

4. **Large skill persistence:** research-tree (7565t) remains large after compression. This is the irreducible operational surface for 6-tier multi-agent orchestration. Exceeds 500-line and 5000t guidelines but justified by scope.

5. **Hook coverage:** Only manifesto plugin uses hooks. Other plugins have not identified hook-worthy patterns yet.

6. **MCP integration:** No plugins currently use .mcp.json despite plugin-dev:mcp-integration skill existing.

## Next Actions

1. **Monitor research-tree implementation:** Synthesis recommendations from 2026-04-13 analysis call for inlining 4 reference files (agent-templates, report-formats, tier-playbook, anti-patterns). Not yet implemented. Expected net reduction: -2,128t system total.

2. **Validate compression quality:** Synthesis documents exist for 18/20 skills + all agents. Implementation PRs merged. No quality regression reports yet.

3. **Session-close integration:** New skill (2286t) added 2026-04-13. Monitor adoption for multi-session workflows.

4. **Deferred items tracking:** See deferred_items.md for synthesis recommendations not yet implemented.

5. **Convention documentation:** See conventions.md for established patterns.
