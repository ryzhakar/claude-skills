# QA Automation Plugin — Maintainer Guide

Implicit decisions, structural invariants, and known pitfalls for anyone modifying this plugin.

## Relationship to Orchestration

qa-orchestration is a domain extension of agentic-delegation (orchestration plugin). The same rules from `orchestration/MAINTAINERS.md` apply:

- **Hard prerequisite:** qa-orchestration MUST gate on reading agentic-delegation first.
- **Delta-only content:** the SKILL.md contains only what the parent does not cover.
- **Cached derivations, not overrides:** if it appears to contradict agentic-delegation, the qa skill is wrong unless the deviation is explicitly justified.
- **Cross-plugin hard preference:** reference agentic-delegation by name, recommend installing the orchestration plugin if absent, one-sentence fallback. No duplicated prompt templates.

## Plugin Structure

```
qa-automation/
  .claude-plugin/plugin.json   <-- per-plugin manifest (version here)
  skills/qa-orchestration/     <-- sole skill (the orchestrator)
  agents/                      <-- planner, generator, executor, healer
  hooks/hooks.json             <-- session recovery + failure detection
  references/                  <-- operational docs loaded by the orchestrator
```

One skill, four agents. The skill is the orchestrator; agents are dispatched by it.

## Version Bump Checklist

The version is the single source of truth in `plugin.json`. The root marketplace index is synced programmatically:

| File | Field | How it's set |
|------|-------|-------------|
| `.claude-plugin/plugin.json` | `"version"` | Manual bump (the source of truth) |
| `../../.claude-plugin/marketplace.json` | `"version"` under the `qa-automation` entry | Auto-synced by `generate.py` from `plugin.json` |

SKILL.md frontmatter no longer carries a `version:` field (removed in `ebbc699`). Do not add it back.

**After bumping `plugin.json`, run `generate.py`** to propagate the version to the root marketplace manifest. A mismatch between these two causes the plugin to fail to load from the marketplace — Claude Code resolves plugins through the root manifest first, so a stale version there makes the correct per-plugin files invisible.

## Skill Rename Protocol

Renaming a skill (e.g., `qa-run` to `qa-orchestration`) requires more than updating the directory and frontmatter:

1. Rename the skill directory under `skills/`.
2. Update the `name:` field in the skill's `SKILL.md` frontmatter.
3. Update any references in `hooks/hooks.json` (slash-command mentions in prompts).
4. Bump the version in `plugin.json` and run `generate.py` (see checklist above).
5. **After pushing:** consumers must delete old version cache directories manually. Claude Code caches each version independently under `~/.claude-shared/plugins/cache/<marketplace>/<plugin>/<version>/` and `~/.claude-competera/plugins/cache/<marketplace>/<plugin>/<version>/`. The old version's cache retains the old skill name and will shadow the new one until removed.

**Known behavior (2026-04-08):** after renaming `qa-run` to `qa-orchestration` in v2.1.0, the skill continued to appear as `qa-run` in Claude Code sessions. Root cause: stale v2.0.0 cache directories containing `skills/qa-run/` were still present alongside the correct v2.1.0 cache. Deleting the old cache directories resolved the issue. Claude Code does not automatically purge old version caches when a new version is installed.

## Agent Definitions

All four agents are same-plugin. Reference them directly, never with "if available" guards.

| Agent | Role |
|-------|------|
| `planner-agent` | Explores live app via browser, produces test plan |
| `generator-agent` | Generates `.spec.ts` files from test plan, one at a time until green |
| `executor-agent` | Runs suite via CLI, classifies failures, produces `.ai-failures.json` |
| `healer-agent` | Repairs broken locators via ten-tier algorithm, computes confidence scores |

## Hooks

- **SessionStart:** checks `.claude/qa-phase.txt` for pipeline resumption after session restart or context compaction.
- **PostToolUse (Bash):** detects Playwright test failures in Bash output and suggests invoking `/qa-orchestration` for locator healing. Does not trigger on assertion failures (real bugs).
