# Core Points: qa-orchestration

## Iteration 1

**Point:** The orchestrator drives a linear five-phase loop (Prerequisites, Plan, Generate, Execute, Heal, Report) with an inner Generate-Execute-Heal cycle that repeats until all tests pass, only non-healable failures remain, circuit breaker trips, or no progress occurs.

**Evidence:**
1. SKILL.md lines 62-76: "The QA Loop" section describes the prerequisite check, outer linear sequence (Plan then inner loop then Report), and inner loop (Generate→Execute→Heal) with four explicit exit conditions.
2. SKILL.md lines 88-106: Phase 1 (PLAN) dispatch and branching rules, followed by planner completeness check before proceeding to GENERATE.
3. SKILL.md lines 165-173: Phase 5 (Report) validates findings, writes session report, and clears phase marker, completing the outer loop.

## Iteration 2

**Point:** All agents communicate exclusively through durable file artifacts written to disk, never relaying content through conversation context, with the orchestrator routing agents to file paths rather than summarizing or transforming agent outputs.

**Evidence:**
1. file-protocol.md lines 6-19: "Core Rule" section explicitly forbids orchestrator summarization, showing correct (agent writes file, next agent reads directly) versus wrong (orchestrator reads and summarizes) patterns.
2. file-protocol.md lines 22-46: Artifact map defines 22 distinct file artifacts with producer, consumer, format, and location for each, establishing the complete communication protocol.
3. SKILL.md line 20: "agents communicate through files on disk (the orchestrator routes, never relays)" states the principle directly in the skill introduction.

## Iteration 3

**Point:** Confidence scoring uses a seven-signal weighted algorithm (error type, DOM changes, console errors, API health, element similarity, historical pattern, cluster size) with hard rejection at 0.0 for assertion failures, runtime errors, console fatal errors, mass clusters, and zero-candidate results, routing fixes to auto-merge (≥0.85), human review (0.60-0.84), or rejection (<0.60).

**Evidence:**
1. confidence-scoring.md lines 7-16: Hard rejection rules list five scenarios that immediately return 0.0 confidence without scoring, including assertion failures and runtime errors.
2. confidence-scoring.md lines 18-68: Complete scoring algorithm breaks down into primary signals (70% weight: error type, DOM changes, console errors) and secondary signals (30% weight: network health, element similarity, history, cluster) with tier adjustment.
3. confidence-scoring.md lines 70-84: Decision thresholds table maps score ranges to HIGH (0.85-1.0 auto-apply), MEDIUM (0.60-0.84 review), LOW (0.40-0.59 fail), REJECT (0.0-0.39 never heal) with explicit false positive rates.

## Iteration 4

**Point:** Test failures are classified into six categories (locator 28%, timing 30%, data/assertion 14%, visual 10%, interaction 10%, other 8%) using regex-based pattern matching on error messages, with only locator failures eligible for automated healing and assertion failures strictly forbidden from healing to prevent masking real bugs.

**Evidence:**
1. failure-heuristics.md lines 5-33: Six-category taxonomy section defines each category with prevalence percentages, regex patterns, and healability status, explicitly marking locator as "YES - candidate for automated healing" and data/assertion as "NO - NEVER heal these automatically."
2. failure-heuristics.md lines 75-87: "Why these MUST NOT be healed" section explains that assertion failures mean the locator found the element correctly but application returned wrong data, making healing a false positive risk that masks bugs.
3. failure-heuristics.md lines 135-167: Classification algorithm function shows the ordered regex matching that routes errors into the six categories.

## Iteration 5

**Point:** The ten-tier deterministic locator discovery algorithm tries progressively weaker selector strategies (role+name, role-only, test-id, HTML id, ARIA label exact/contains, href fragment, CSS class exact/partial, visible text) with 1500ms timeout per tier, achieving self-healing in under 1 second for tiers 1-3 and zero operational cost by eliminating LLM calls.

**Evidence:**
1. ten-tier-algorithm.md lines 16-30: Tier priority table lists all ten strategies with examples and confidence ratings, showing the progression from HIGH confidence (tiers 1-3) through MEDIUM (4-6) to LOW (7-10).
2. ten-tier-algorithm.md lines 142-220: DOMExtractor implementation shows the complete cascade through all ten tiers, with each tier's tryRole/tryCss/tryText method using a 1500ms timeout (line 225, 1500 timeout parameter).
3. ten-tier-algorithm.md line 13: "Verified: 100% pass rate (31/31 tests), <1s healing time per broken selector, zero operational cost" quantifies the performance and cost characteristics.

## Rank Summary

1. The orchestrator's five-phase loop structure with inner Generate-Execute-Heal cycle and explicit exit conditions governs the entire test lifecycle architecture.
2. File-based communication with no content relaying through orchestrator context ensures agents work from authoritative artifacts rather than lossy summaries.
3. Confidence scoring's seven-signal algorithm with hard rejection rules and three-tier routing (auto-merge/review/reject) balances automation coverage against false positive risk.
4. Six-category failure taxonomy with regex classification and strict prohibition on healing assertion failures prevents the healer from masking real application bugs.
5. Ten-tier deterministic locator discovery with per-tier timeouts and zero LLM cost achieves sub-second healing for high-confidence tiers while maintaining exhaustive fallback coverage.
