# Strunk Analysis: planner-agent.md

## Critical & Severe

### R10 (Active Voice) - Severe
**Line 4:** "Use this agent when the user needs to explore a live web application to plan Playwright tests."
- Passive: "needs to explore" is active, but "to plan" is infinitive construction weakening agency
- Severity: Moderate (borderline severe)
- Suggested revision: "Use this agent when the user explores a live web application and plans Playwright tests."

**Line 31:** "You are a test planning agent."
- Good: Active construction
- No violation

**Line 43:** "It writes snapshots to disk (not context)"
- Good: Active voice
- No violation

**Line 87:** "Use @playwright/cli (default):"
- Good: Imperative = active
- No violation

### R12 (Concrete Language) - Severe
**Line 5:** "Produces structured test planning artifacts from browser exploration."
- Abstract: "structured test planning artifacts" is vague
- Severity: Severe
- Suggested revision: "Produces test plans, selector strategies, and DOM quality scores from live browser sessions."

**Line 60:** "Dynamic content, loading states, client-side routing"
- Good: Concrete examples
- No violation

**Line 87:** "Launch browser, capture snapshots to disk, read and analyze them. Unlimited interactions, ~50 tokens per command."
- Good: Specific numbers, concrete actions
- No violation

## Moderate

### R13 (Needless Words) - Moderate
**Line 39:** "If you have not visited a page, that page cannot appear in the plan."
- Wordy: "If you have not visited" → "Unvisited pages"
- Severity: Moderate
- Suggested revision: "Unvisited pages cannot appear in the plan."

**Line 69:** "Before using ANY MCP tools, verify @playwright/mcp version:"
- "ANY" is emphatic but adds minimal value
- Severity: Minor
- Suggested revision: "Before using MCP tools, verify @playwright/mcp version:"

**Line 79:** "Ask the user for the base URL if not provided."
- Adequate concision
- No violation

**Line 116:** "Record ALL evidence in `.playwright/VERIFICATION.md`."
- "ALL" emphatic, justified for emphasis
- No violation

### R11 (Positive Form) - Moderate
**Line 36:** "NO PLAN WITHOUT LIVE EXPLORATION FIRST."
- Negative construction for emphasis (Iron Law)
- Justified as emphatic denial, but could be positive
- Severity: Minor
- Suggested revision: "EVERY PLAN REQUIRES LIVE EXPLORATION FIRST." (though negative has rhetorical force here)

**Line 39:** "If you have not visited a page, that page cannot appear in the plan."
- Double negative: "not visited" + "cannot appear"
- Severity: Moderate
- Suggested revision: "Only visited pages appear in the plan."

**Line 136:** "Define Selector Strategy"
- Positive form
- No violation

### R15 (Parallel Construction) - Moderate
**Lines 54-60:** Exploration workflow list
```
1. `playwright-cli open <base-url>` — launch browser
2. `playwright-cli snapshot --filename=.playwright/snap-home.yaml` — capture page state
3. Read the snapshot file to find element refs
4. `playwright-cli click <ref>` — interact with elements
```
- Inconsistent: Steps 1, 2, 4 use backticked commands; step 3 uses bare imperative
- Severity: Moderate
- Suggested revision: Step 3 should match: "`Read .playwright/snap-home.yaml` — find element refs"

**Lines 145-150:** Edge case list
```
- Empty states
- Validation failures  
- Unauthorized access
- Boundary values
- Network failures
- Browser navigation (back/forward/refresh)
```
- Good: All noun phrases, parallel
- No violation

## Minor & Stylistic

### R18 (Emphatic Position) - Minor
**Line 31:** "You are a test planning agent. You explore live web applications via browser interaction and generate structured test plans grounded in actual UI state."
- First sentence ends weakly with "agent" (generic)
- Second sentence ends strongly with "actual UI state" (specific, emphatic)
- Severity: Minor
- Suggested revision: Combine for stronger ending: "You are a test planning agent that explores live web applications via browser interaction and generates test plans grounded in actual UI state."

**Line 43:** "It writes snapshots to disk (not context), giving unlimited session length at ~50 tokens/command vs MCP's ~4,000 tokens/interaction."
- Ends strongly with concrete comparison
- Good use of emphatic position
- No violation

**Line 75:** "This is non-negotiable."
- Strong emphatic ending
- Good
- No violation

### R13 (Needless Words) - Minor
**Line 161:** "After all artifacts are written, create `.playwright/orchestrator-status.json`:"
- "After all artifacts are written" could be "After writing all artifacts"
- Severity: Minor
- Suggested revision: "After writing all artifacts, create `.playwright/orchestrator-status.json`:"

**Line 177:** "Read these files from disk before proceeding:"
- "from disk" somewhat redundant (Read always reads from disk)
- Severity: Minor
- Suggested revision: "Read these files before proceeding:"

## Summary

**Strengths:**
- Generally uses active voice and concrete language effectively
- Good use of specific numbers (~50 tokens, 10 interactions, score 0-100)
- Parallel construction mostly consistent in lists
- Strong emphatic endings in key directive sentences

**Priority fixes:**
1. Line 5 (R12 Severe): Make "structured test planning artifacts" concrete with specific file types
2. Line 39 (R11 + R13 Moderate): Convert double negative to positive form and reduce words
3. Lines 54-60 (R15 Moderate): Standardize workflow step format

**Total findings:**
- Critical/Severe: 2 (1 concrete language, 1 borderline active voice)
- Moderate: 5 (2 needless words, 2 positive form, 1 parallel construction)
- Minor/Stylistic: 3 (2 needless words, 1 emphatic position)
