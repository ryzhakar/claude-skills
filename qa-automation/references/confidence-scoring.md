# Confidence Scoring Algorithm

Scoring formula for determining whether a test failure is safe to auto-heal. Uses weighted multi-signal analysis to compute a confidence score between 0.0 and 1.0. Target false positive rate: <5%.

Source: T4-04 false positive detection pipeline. Based on Similo research (98.8% accuracy at 0.85 threshold).

## Hard Rejection Rules (Score = 0.0)

These failures are NEVER healed. Return 0.0 immediately, no scoring computed.

1. **Assertion failures:** Element was found but its content or state is wrong. Real bug.
2. **Runtime errors / crashes:** Application threw an unhandled exception. Real bug.
3. **Console fatal errors:** `console.error` or unhandled promise rejections detected. Application broken.
4. **No candidate element found:** Ten-tier algorithm returned null. Cannot heal.
5. **Mass failure cluster (>10 tests):** More than 10 tests failing simultaneously. Infrastructure issue or real regression.

## Scoring Algorithm

```
calculate_healing_confidence(failure_context):
    score = 0.0

    === PRIMARY SIGNALS (70% weight) ===

    1. Error Type Analysis (max +0.30):
       ELEMENT_NOT_FOUND:  +0.30
       ELEMENT_NOT_VISIBLE: +0.25
       ASSERTION_FAILED:   return 0.0 (hard reject)
       RUNTIME_ERROR:      return 0.0 (hard reject)

    2. DOM Change Detection (max +0.20):
       Attribute changes only (class, id, data-*): +0.20
       Element relocated (same element, new position): +0.15
       Element removed entirely:  +0.05 (low confidence, might be real bug)
       DOM unchanged but element not found: -0.15 (suspicious)

    3. Console/Runtime Errors (max +0.20):
       No console errors:         +0.20
       Console WARNING severity:  +0.10
       Console ERROR or FATAL:    return 0.0 (hard reject)

    === SECONDARY SIGNALS (30% weight) ===

    4. Network/API Health (max +0.10):
       All API responses OK:      +0.10
       API errors detected:       -0.10

    5. Element Match Quality (max +0.10):
       Candidate found with similarity score S: +(S * 0.10)
       No candidate found: return 0.0 (hard reject)

    6. Historical Pattern (max +0.05):
       Test failure rate <2% (stable): +0.05
       Test failure rate >10% (flaky): -0.10

    7. Cluster Analysis (max +0.05):
       Isolated failure (0 concurrent): +0.05
       Small cluster (1-2 concurrent):  +0.03
       Large cluster (>10 concurrent):  -0.15

    === TIER ADJUSTMENT ===

    8. Tier-based confidence adjustment:
       Ten-tier resolved at tier 1-3: +0.05 bonus
       Ten-tier resolved at tier 7-10: -0.05 penalty

    return clamp(score, 0.0, 1.0)
```

## Decision Thresholds

| Score Range | Category | Action | False Positive Rate |
|-------------|----------|--------|---------------------|
| 0.85 - 1.0 | HIGH | Auto-apply fix. In CI: enable auto-merge on PR. | 2-5% |
| 0.60 - 0.84 | MEDIUM | Create PR requiring human review within 24h. | 5-10% |
| 0.40 - 0.59 | LOW | Fail the test. Require manual investigation. | 10-15% |
| 0.0 - 0.39 | REJECT | Never heal. Almost certainly a real bug. | N/A |

**Threshold rationale:**
- 0.85 for auto-apply: Similo research shows 98.8% accuracy at this threshold (VON method)
- 0.60 for review: balances automation coverage (40% of healable failures) with safety
- 0.40 for rejection: below this, failure is more likely a real bug than a locator issue

## Typical Score Scenarios

### HIGH (0.85-1.0): Auto-apply

- Element not found (+0.30) AND DOM attribute changed (+0.20) AND no console errors (+0.20) AND APIs OK (+0.10) AND similarity >0.90 (+0.09) AND stable history (+0.05) AND isolated (+0.05) = **0.99**
- Scenario: CSS class or ID renamed during UI refactor. Element is functionally identical.

### MEDIUM (0.60-0.84): Human review

- Element not found (+0.30) AND element relocated (+0.15) AND no console errors (+0.20) AND similarity 0.75 (+0.075) = **0.725**
- Scenario: Button moved from header to sidebar. May be intentional redesign.

### LOW (0.40-0.59): Fail

- Element not found (+0.30) AND element removed (+0.05) AND console warnings (+0.10) AND similarity 0.50 (+0.05) = **0.50**
- Scenario: Element significantly changed or replaced. Could be real feature change.

### REJECT (0.0-0.39): Real bug

- Element not found (+0.30) AND DOM unchanged (-0.15) AND API errors (-0.10) = **0.05**
- Scenario: Element not found, nothing changed in DOM, APIs returning errors. Application broken.

## Element Similarity Scoring

When a candidate element is found, compute similarity to the original using weighted DOM properties. Based on Similo research (14 properties, optimized weights).

```
calculate_element_similarity(original, candidate):
    weights:
        tag:          1.5   (must match, stable)
        id:           1.5   (strong signal)
        name:         1.5   (strong signal)
        type:         1.5   (stable for inputs)
        aria_label:   1.5   (accessibility attribute, stable)
        data_testid:  2.0   (strongest: explicit test identifier)
        class:        0.5   (changes often with CSS)
        href:         0.5   (URLs change)
        visible_text: 1.2   (moderately stable)
        neighbor_text:1.0   (context signal)
        xpath:        0.8   (structure signal)
        position_x:   0.6   (weak: layout shifts)
        position_y:   0.6   (weak: layout shifts)
        role:         1.3   (moderately stable)

    total_weight = 15.6

    Comparison methods:
        Exact match (tag, type, role): 1.0 if equal, 0.0 if not
        Position (x, y): max(0, 1.0 - (distance / 500px))
        String (class, href, xpath): Levenshtein similarity
        Text (visible_text, neighbor_text): word set overlap

    weighted_score = sum(similarity[prop] * weight[prop])
    return weighted_score / total_weight
```

**Note for initial deployment:** Start with primary signals only (error type + DOM changes + console errors). Add secondary signals as false positive monitoring data accumulates.

## Flaky Test Detection

A test with failure rate between 2% and 98% across recent runs is flaky. Flaky tests are NOT candidates for locator healing -- they need wait strategy fixes.

```
detect_flaky_test(test_history):
    recent_runs = last 50 executions
    flaky_rate = failures / total

    if flaky_rate == 0: stable (not flaky)
    if flaky_rate == 1.0: consistently failing (deterministic)
    if 0.02 <= flaky_rate <= 0.98: FLAKY
```

Flaky categories and correct response:

| Category | Prevalence | Fix | Heal Locator? |
|----------|-----------|-----|---------------|
| Async Wait | 45% | Replace `waitForTimeout()` with web-first assertions | NO |
| Race Conditions | 24% | Fix shared state or test ordering | NO |
| Resource-Affected | 46.5% | Increase timeouts, optimize test | NO |
| Network Issues | 9% | Mock APIs or add retries | NO |
| Environment Differences | 12% | Platform-specific locators | CONDITIONAL |

## Cluster Analysis

When multiple tests fail concurrently, probability of a shared root cause increases.

| Cluster Size | Interpretation | Healing Decision |
|-------------|----------------|------------------|
| 1-2 tests | Isolated locator issue | Safe to heal |
| 3-9 tests | Possible shared cause | Reduce confidence by 0.1-0.2 |
| 10+ tests | Infrastructure issue or regression | DO NOT HEAL |

Research shows 75% of flaky tests belong to failure clusters with mean size 13.5 tests sharing the same root cause.

## Application in the Healer Workflow

1. Check hard rejection rules first. If any match, skip with score 0.0.
2. Compute primary signals (70% of score): error type, DOM changes, console errors.
3. Compute secondary signals (30% of score): API health, element similarity, history, cluster.
4. Apply tier-based adjustment: +0.05 for tiers 1-3, -0.05 for tiers 7-10.
5. Route: HIGH -> auto-apply, MEDIUM -> review PR, LOW -> fail, REJECT -> skip.
