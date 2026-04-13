# Reference Optionality Analysis: systematic-debugging

## Executive Summary

All three references are DEFERRABLE with concrete loading gates embedded in the main skill workflow. The main SKILL.md provides sufficient entry-level guidance to execute all four phases; references offer depth for specific sub-patterns.

## Reference Classifications

### 1. root-cause-tracing.md — DEFERRABLE

**Classification:** DEFERRABLE

**Rationale:**
- Main skill Phase 1 Step 5 already covers backward tracing principle: "Trace backward through the call chain until the original trigger is found. Fix at source, not at symptom."
- Reference adds implementation techniques (stack trace instrumentation, console.error usage, find-polluter.sh script)
- Skill functions without it for simple debugging; reference needed when tracing becomes non-trivial
- Main skill contains deferral signal: "For the complete backward tracing technique with examples, see @references/root-cause-tracing.md"

**Loading Gate:**
```
IF (Phase 1 Step 5 AND user needs stack trace instrumentation OR polluting test unknown)
THEN read /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/systematic-debugging/references/root-cause-tracing.md
```

**Gate Location:** Within Phase 1, Step 5 (Trace Data Flow) execution — specifically when manual tracing fails or when dealing with test pollution.

**Gate Implementation:** Main SKILL.md line 77 already signals this: "For the complete backward tracing technique with examples, see @references/root-cause-tracing.md — it covers stack trace instrumentation, test pollution bisection, and the principle of fixing at the origination point."

This makes ignoring impossible: if the user needs stack traces or bisection (mentioned in the signal), the reference path is right there.

---

### 2. defense-in-depth.md — DEFERRABLE

**Classification:** DEFERRABLE

**Rationale:**
- Main skill Phase 4 Step 6 already states the principle: "Add validation at every layer the bad data passed through. Make the bug structurally impossible, not just fixed."
- Reference provides the 4-layer pattern (entry, business logic, environment guards, debug)
- Core debugging works without it; reference needed when implementing comprehensive validation
- Main skill contains deferral signal: "For the 4-layer validation pattern (entry point, business logic, environment guards, debug instrumentation), see @references/defense-in-depth.md"

**Loading Gate:**
```
IF (Phase 4 Step 6 execution AND implementing post-fix validation)
THEN read /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/systematic-debugging/references/defense-in-depth.md
```

**Gate Location:** Phase 4, Step 6 (Defense in Depth) — after root cause fix is implemented and verified.

**Gate Implementation:** Main SKILL.md line 162 already signals this: "For the 4-layer validation pattern (entry point, business logic, environment guards, debug instrumentation), see @references/defense-in-depth.md — it covers entry validation, business logic checks, environment guards, and debug instrumentation."

This makes ignoring impossible: the principle is stated, the reference describes the implementation pattern, and the path is provided exactly when needed.

---

### 3. condition-based-waiting.md — DEFERRABLE

**Classification:** DEFERRABLE

**Rationale:**
- Main skill mentions this as a specific sub-pattern under "Condition-Based Waiting" section (line 203)
- Only relevant for flaky tests with timing issues
- Most debugging scenarios never encounter this
- Main skill contains deferral signal: "see @references/condition-based-waiting.md for the implementation pattern and common mistakes"

**Loading Gate:**
```
IF (debugging flaky tests AND timing/race condition identified)
THEN read /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/systematic-debugging/references/condition-based-waiting.md
```

**Gate Location:** Condition-Based Waiting section (line 203-204) — invoked when diagnosis reveals timing-related flakiness.

**Gate Implementation:** Main SKILL.md line 204 already provides the narrow trigger: "When debugging flaky tests caused by timing issues, replace arbitrary timeouts with condition polling — see @references/condition-based-waiting.md for the implementation pattern and common mistakes."

This makes ignoring impossible: the condition is specific (flaky tests + timing issues), and the reference is the only place with the waitFor implementation pattern.

---

## Summary Table

| Reference | Classification | Trigger Condition | Location in Workflow |
|-----------|----------------|-------------------|---------------------|
| root-cause-tracing.md | DEFERRABLE | Stack trace instrumentation needed OR polluting test unknown | Phase 1, Step 5 |
| defense-in-depth.md | DEFERRABLE | Implementing multi-layer validation after fix | Phase 4, Step 6 |
| condition-based-waiting.md | DEFERRABLE | Debugging flaky tests with timing issues | Specialized section (line 203) |

## Validation

All three references are already correctly deferred in the main SKILL.md:
1. Each has a clear inline mention with context
2. Each has an @references/filename.md link at point of need
3. Each describes WHAT the reference contains (techniques, patterns, examples)
4. The main skill is fully functional without them for general debugging
5. Ignoring them when their condition is met is structurally impossible due to explicit inline gates

No changes required to SKILL.md structure.

---

**Analysis Date:** 2026-04-13  
**Unit:** systematic-debugging  
**Skill Path:** /Users/ryzhakar/pp/claude-skills/dev-discipline/skills/systematic-debugging/SKILL.md  
**References Analyzed:** 3/3  
**Essential:** 0  
**Deferrable:** 3
