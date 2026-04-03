---
name: systematic-debugging
description: >
  This skill should be used when the user reports a "bug", "test failure", "unexpected behavior",
  "error", "crash", "flaky test", asks to "debug this", "find root cause", "why is this failing",
  "fix this error", or when multiple fix attempts have failed. Provides a mandatory 4-phase
  root cause protocol that prevents random fixes and symptom patching. Apply BEFORE proposing
  any fix, especially under time pressure.
---

# Systematic Debugging

Mandatory root cause protocol for any bug, test failure, or unexpected behavior. Random fixes waste time and create new bugs. Quick patches mask underlying issues.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If Phase 1 has not been completed, no fix may be proposed. Symptom fixes are debugging failures.

## When to Apply

Apply for ANY technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues.

**Apply especially when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- Multiple fixes have already been attempted
- The previous fix did not work
- The issue is not fully understood

**Do not skip when:**
- The issue seems simple (simple bugs have root causes too)
- Time is short (systematic debugging is faster than thrashing)

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

Do not skip past errors or warnings. Read stack traces completely. Note line numbers, file paths, error codes. Error messages often contain the exact solution.

### 2. Reproduce Consistently

Determine: can the issue be triggered reliably? What are the exact steps? Does it happen every time? If not reproducible, gather more data -- do not guess.

### 3. Check Recent Changes

What changed that could cause this? Check git diff, recent commits, new dependencies, config changes, environmental differences.

### 4. Gather Evidence in Multi-Component Systems

When a system has multiple components (CI pipeline, API chain, layered architecture), add diagnostic instrumentation BEFORE proposing fixes:

```
For EACH component boundary:
  - Log what data enters the component
  - Log what data exits the component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify the failing component
THEN investigate that specific component
```

This reveals which layer fails (e.g., secrets pass from workflow to build script but not from build script to signing script).

### 5. Trace Data Flow

When the error is deep in a call stack, trace backward through the call chain until the original trigger is found. Fix at source, not at symptom.

For the complete backward tracing technique with examples, see @references/root-cause-tracing.md — it covers stack trace instrumentation, test pollution bisection, and the principle of fixing at the origination point.

## Phase 2: Pattern Analysis

Find the pattern before fixing.

### 1. Find Working Examples

Locate similar working code in the same codebase. What works that is similar to what is broken?

### 2. Compare Against References

If implementing a known pattern, read the reference implementation COMPLETELY. Do not skim. Partial understanding guarantees bugs.

### 3. Identify Differences

List every difference between working and broken, however small. Do not assume "that cannot matter."

### 4. Understand Dependencies

What other components, settings, config, or environment does the broken code need? What assumptions does it make?

## Phase 3: Hypothesis and Testing

Apply the scientific method.

### 1. Form a Single Hypothesis

State clearly: "I think X is the root cause because Y." Write it down. Be specific, not vague.

### 2. Test Minimally

Make the SMALLEST possible change to test the hypothesis. One variable at a time. Do not fix multiple things at once.

### 3. Verify Before Continuing

Did it work? If yes, proceed to Phase 4. If no, form a NEW hypothesis. Do not add more fixes on top.

If the agentic-delegation skill is available, apply its Speculative Parallel pattern for multi-hypothesis testing: launch parallel agents each investigating one hypothesis independently, then compare their evidence. Otherwise, launch 3 background agents with the cheapest available model, each investigating a different hypothesis independently. Read their summaries to determine which hypothesis has evidence.

### 4. When Understanding Is Incomplete

Say "I do not understand X." Do not pretend to know. Ask for help. Research more.

## Phase 4: Implementation

Fix the root cause, not the symptom.

### 1. Create a Failing Test Case

Write the simplest possible reproduction as an automated test. This MUST exist before fixing. If no test framework is available, a one-off script suffices.

### 2. Implement a Single Fix

Address the root cause identified in Phase 3. ONE change at a time. No "while I'm here" improvements. No bundled refactoring.

### 3. Verify the Fix

Does the test pass? Are other tests unbroken? Is the issue actually resolved?

### 4. If the Fix Does Not Work

STOP. Count fix attempts:

- **Fewer than 3:** Return to Phase 1, re-analyze with new information.
- **3 or more:** STOP and question the architecture (see below).

### 5. Architectural Questioning Threshold (3+ Failed Fixes)

Pattern indicating an architectural problem:
- Each fix reveals new shared state, coupling, or problems in different places
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

STOP and question fundamentals:
- Is this pattern fundamentally sound?
- Is the current approach persisting through inertia?
- Should the architecture be refactored instead of continuing to fix symptoms?

Discuss with the user before attempting more fixes. This is not a failed hypothesis -- this is a wrong architecture.

### 6. Defense in Depth

After fixing the root cause, add validation at every layer the bad data passed through. Make the bug structurally impossible, not just fixed.

For the 4-layer validation pattern (entry point, business logic, environment guards, debug instrumentation), see @references/defense-in-depth.md — it covers entry validation, business logic checks, environment guards, and debug instrumentation.

## Red Flags -- Return to Phase 1

If any of these thoughts occur, STOP and return to Phase 1:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems:" (listing fixes without investigation)
- Proposing solutions before tracing data flow
- "One more fix attempt" (when 2+ already tried)
- Each fix reveals a new problem in a different place

## User Signals of Process Violation

Watch for these redirections from the user:
- "Is that not happening?" -- assumed without verifying
- "Will it show us...?" -- should have added evidence gathering
- "Stop guessing" -- proposing fixes without understanding
- "Ultrathink this" -- need to question fundamentals, not just symptoms

When these signals appear: STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes do not stick. Test first proves it. |
| "Multiple fixes at once saves time" | Cannot isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, do not fix again. |

## Condition-Based Waiting

When debugging flaky tests caused by timing issues, replace arbitrary timeouts with condition polling — see @references/condition-based-waiting.md for the implementation pattern and common mistakes.

## Test Pollution Bisection

When a test creates unwanted files or state but the polluting test is unknown, use the bisection script at scripts/find-polluter.sh. It runs tests one-by-one and stops at the first polluter.

```bash
./scripts/find-polluter.sh '.git' 'src/**/*.test.ts'
```

## Quick Reference

| Phase | Key Activities | Success Criteria |
|---|---|---|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |

## Reference Files

- @references/root-cause-tracing.md — Backward tracing through call stack, stack trace instrumentation, test pollution bisection
- @references/defense-in-depth.md — 4-layer validation pattern: entry, business logic, environment guards, debug instrumentation
- @references/condition-based-waiting.md — Replace arbitrary timeouts with condition polling for flaky tests

---

*Originally based on systematic-debugging from https://github.com/obra/superpowers, MIT licensed. Adapted and enhanced for this plugin.*
