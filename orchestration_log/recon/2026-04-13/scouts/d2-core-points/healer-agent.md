# Core Points Analysis: healer-agent

## Iteration 1

**Point:** The healer-agent only repairs locator failures and explicitly refuses to touch assertion failures or runtime errors, treating "element found + wrong value" as an application bug requiring no test modification.

**Evidence:**
- Lines 32-38: "THE IRON LAW" section states in all-caps "NEVER HEAL ASSERTION FAILURES. NEVER HEAL RUNTIME ERRORS. ELEMENT FOUND + WRONG VALUE = APPLICATION BUG. DO NOT TOUCH THE TEST."
- Lines 39-40: Explicit instruction to write `confidence: 0.0` and skip assertion failures
- Lines 61-62: Hard rejection rule #1 states "Assertion on element value — REAL BUG"

## Iteration 2

**Point:** The agent implements a deterministic ten-tier healing algorithm with mandatory Similo-based confidence scoring and applies fixes only when confidence reaches >= 0.60.

**Evidence:**
- Lines 69-78: "Ten-Tier Algorithm" section references the deterministic algorithm from `@references/ten-tier-algorithm.md` with defined confidence bands (HIGH: 2-5% FP, MEDIUM: 5-10% FP, LOW: 10-15% FP)
- Lines 82-88: "Confidence Scoring" section defines explicit thresholds where >= 0.85 is HIGH, 0.60-0.84 is MEDIUM, and < 0.40 is REJECT
- Line 120: "Apply Fixes (confidence >= 0.60 only)" header enforces the minimum threshold

## Iteration 3

**Point:** DOM verification using @playwright/cli is mandatory for tier 7+ fixes and for DOM re-discovery when all tiers return null, ensuring proposed locators actually exist in the live application.

**Evidence:**
- Lines 96-100: "DOM Verification (Mandatory for Tiers 7+)" section states "Before applying any fix at tier 7 or below, verify the proposed locator exists in the live DOM using @playwright/cli"
- Lines 102-118: "DOM Re-Discovery (Mandatory when all tiers return null)" section provides step-by-step instructions including playwright-cli snapshot commands
- Line 115: "This step is MANDATORY when all tiers return null" reinforces the requirement

## Iteration 4

**Point:** The agent maintains a cross-cycle feedback loop through `.playwright/lessons.md` to prevent repeating failed selectors and accumulate healing discoveries across multiple attempts.

**Evidence:**
- Lines 91-94: "Lessons" section instructs to read `.playwright/lessons.md` before starting, stating "It contains discoveries from prior cycles — selectors that failed and why, patterns that worked, structural issues. Do not repeat a selector that a prior cycle already tried and failed."
- Lines 93-94: Agent must "Append your own discoveries after healing: which selectors you replaced, which tiers succeeded, which approaches didn't work. This is the feedback loop between cycles."
- Line 50: Mentions circuit breaker with "Max 2 attempts per test" which the lessons file supports

## Iteration 5

**Point:** The agent enforces a strict circuit breaker pattern that limits healing attempts to a maximum of 2 per test and honors a blocklist, treating the healing-state.json as read-only to prevent concurrent modification.

**Evidence:**
- Lines 50-58: "Circuit Breaker (READ-ONLY)" section states "Max 2 attempts per test (key: `"file:line:title"`) — skip and mark deferred if exceeded" and "Tests on blocklist — skip"
- Line 58: Explicitly states "DO NOT write to this file. The orchestrator updates it after aggregation."
- Line 133: In the Apply Fixes section, "If still fails after fix: mark as deferred" shows the circuit breaker's exit path

## Rank Summary

1. **Iron Law (no assertion healing)** — The single most emphatic point, presented in all-caps as "THE IRON LAW" and repeated across multiple sections. This is the agent's primary constraint and the most frequently emphasized rule.

2. **Deterministic ten-tier + confidence thresholds** — The core algorithm that defines the agent's repair methodology. Mentioned in the description, referenced throughout, and central to every healing decision.

3. **Mandatory DOM verification** — A critical safety mechanism that prevents theoretical fixes from being applied without live verification, especially emphasized for lower-confidence tiers.

4. **Cross-cycle lessons feedback loop** — A unique architectural feature that enables learning across healing attempts and prevents repeated failures, making the agent progressively smarter.

5. **Circuit breaker (read-only, 2 attempts max)** — Important for preventing infinite loops and respecting orchestrator-managed state, but less pervasive than the above points.
