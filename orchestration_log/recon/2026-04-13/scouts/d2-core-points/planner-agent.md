# Core Points: planner-agent

## Iteration 1

**Point:** Every test plan must be grounded in actual live browser exploration—no page can appear in the plan without being visited, and every scenario must trace to a concrete browser observation.

**Evidence:**
1. Lines 33-39: "The Iron Law" section states "NO PLAN WITHOUT LIVE EXPLORATION FIRST. If you have not visited a page, that page cannot appear in the plan. Every scenario must trace to a browser observation."
2. Line 116: Under "Explore Application (MANDATORY)" the exploration phase is marked as required.
3. Lines 143-144: "Each scenario MUST trace to exploration observations (CLI snapshots or MCP VERIFICATION.md)."

## Iteration 2

**Point:** The agent defaults to @playwright/cli for browser exploration (not MCP) because it writes snapshots to disk at ~50 tokens/command versus MCP's ~4,000 tokens/interaction, enabling unlimited session length.

**Evidence:**
1. Lines 41-43: "Browser Exploration (Default: @playwright/cli)" header and explanation "It writes snapshots to disk (not context), giving unlimited session length at ~50 tokens/command vs MCP's ~4,000 tokens/interaction."
2. Lines 45-53: Detailed @playwright/cli workflow is presented first as the primary method.
3. Lines 63-65: "Use MCP ONLY when the agent cannot access the Bash tool or in sandboxed environments. Cap at 10 interactions."

## Iteration 3

**Point:** DOM quality must be quantitatively scored (0-100) using a specific rubric that rewards semantic HTML, ARIA labels, and proper form elements while penalizing clickable divs and unlabeled inputs, with scores written to .playwright/pages.md.

**Evidence:**
1. Lines 118-136: Detailed DOM quality scoring section with exact formula: "+20 proper form elements", "+15 ARIA labels work", "-20 clickable divs", "-15 inputs without labels", etc.
2. Line 135: "Write scores to `.playwright/pages.md`. Pages scoring below 80: flag specific elements needing `data-testid` attributes."
3. Lines 138-139: "Define Selector Strategy" follows quality analysis, showing quality scoring informs strategy.

## Iteration 4

**Point:** The agent must write a phase completion status file (.playwright/orchestrator-status.json) indicating DONE/NEEDS_CONTEXT/BLOCKED with blockers and artifact paths to enable orchestrator-driven pipeline control.

**Evidence:**
1. Lines 153-169: Entire "Write Status File" section with three JSON schemas for different completion states.
2. Line 154: "After all artifacts are written, create `.playwright/orchestrator-status.json`" shows this is the final coordination step.
3. Lines 18-22 (example): "The orchestrator dispatches planner-agent as the first phase of the QA pipeline" establishes this agent operates within a multi-phase orchestration context.

## Iteration 5

**Point:** MCP usage requires mandatory CVE-2025-9611 security verification by checking @playwright/mcp version >= 0.0.40 before any MCP tool use, with hard stop if vulnerable.

**Evidence:**
1. Lines 67-75: Dedicated "Security Requirement: MCP Version Check" section stating "Before using ANY MCP tools, verify @playwright/mcp version" and "If version < 0.0.40: Report CVE-2025-9611 (DNS rebinding vulnerability) and STOP... This is non-negotiable."
2. Line 65: MCP version requirement is mentioned in the fallback section header: "Requires @playwright/mcp >= v0.0.40."
3. Lines 70-75: Explicit bash command provided and upgrade instruction given, showing this is a blocking security gate.

## Rank Summary

1. **Live exploration mandate (The Iron Law)** — The most emphatic point, presented as "The Iron Law" in its own section with absolute language. Every other workflow step depends on this foundation.

2. **CLI-over-MCP default** — The architectural decision that enables the Iron Law at scale. Token efficiency (50 vs 4,000) directly enables unlimited exploration depth.

3. **Orchestrator status protocol** — The coordination mechanism that makes this agent composable. Without status files, multi-phase pipelines cannot function.

4. **DOM quality scoring** — The only quantitative assessment requirement with a specific 0-100 rubric. Transforms subjective quality into actionable flags for selector strategy.

5. **MCP security gate** — A non-negotiable safety requirement when using the fallback path. Hard stop with CVE citation shows severity, but applies only to non-default workflow.
