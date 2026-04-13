---
name: systematic-debugging
description: >
  Mandatory 4-phase root cause protocol for bugs, test failures, errors, or unexpected behavior.
  Prevents random fixes and symptom patching. Apply BEFORE proposing any fix, especially when
  multiple attempts have failed or time pressure tempts guessing.
---

# Systematic Debugging

Mandatory root cause protocol for any bug, test failure, or unexpected behavior. Random fixes waste time and create new bugs. Quick patches mask underlying issues.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Complete Phase 1 before proposing any fix. Symptom fixes are debugging failures.

## When to Apply

Apply for ANY technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues.

**Apply especially when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- Multiple fixes have already been attempted
- The previous fix did not work
- The issue is not fully understood

**Apply even when:**
- The issue seems simple (simple bugs have root causes too)
- Time is short (systematic debugging is FASTER than thrashing)

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

Do not skip past errors or warnings. Read stack traces completely. Note line numbers, file paths, error codes. Error messages often state the exact solution.

### 2. Reproduce Consistently

Determine: can the issue be triggered reliably? What are the exact steps? Does it happen every time? If not reproducible, gather more evidence: logs, timestamps, environment state. Do not guess.

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

### 5. Trace Backward to Source

When the error is deep in the call stack, trace backward through the call chain to find the original trigger. Fix at source, not at symptom.

**The tracing process:**
1. Observe the symptom (the error message, wrong output)
2. Find immediate cause (which code directly triggers the error)
3. Ask: what called this? Trace one level up
4. What value was passed? Check for invalid data (empty strings, nulls, wrong types)
5. Keep tracing up until you find where the invalid data originated
6. Fix at the origination point

**Adding stack traces when manual tracing fails:**

```typescript
// Before the problematic operation
const stack = new Error().stack;
console.error('DEBUG operation:', {
  directory, cwd: process.cwd(), nodeEnv: process.env.NODE_ENV, stack,
});
```

Use `console.error()` in tests (loggers may be suppressed). Log before the dangerous operation, not after it fails. Include: directory, cwd, environment variables, timestamps. Run and grep: `npm test 2>&1 | grep 'DEBUG operation'`.

**Finding which test causes pollution:**

Use bisection: run tests one-by-one, stop at first polluter.

```bash
./scripts/find-polluter.sh '.git' 'src/**/*.test.ts'
```

**Principle:** NEVER fix where the error appears. Trace back to the original trigger.

## Phase 2: Pattern Analysis

Find the pattern before fixing.

### 1. Find Working Examples

Locate similar working code. What works that is similar to what is broken?

### 2. Compare Against References

If implementing a known pattern, read the reference implementation COMPLETELY. Do not skim. Partial understanding guarantees bugs.

### 3. Identify Differences

List every difference between working and broken, however small. Assume every difference might matter.

### 4. Understand Dependencies

What does the broken code assume about inputs, state, environment, or dependencies?

## Phase 3: Hypothesis and Testing

Apply the scientific method.

### 1. Form a Single Hypothesis

State clearly: "I think X is the root cause because Y." Write it down. Be specific, not vague.

### 2. Test Minimally

Make the SMALLEST change to test the hypothesis. One variable at a time. Fix one thing at a time.

### 3. Verify Before Continuing

Did the change fix the issue? If yes, proceed to Phase 4. If no, form a NEW hypothesis. Do not add more fixes on top.

If the agentic-delegation skill is available, apply its Speculative Parallel pattern for multi-hypothesis testing: launch parallel agents each investigating one hypothesis independently, then compare their evidence. Otherwise, launch 3 background agents with the cheapest available model, each investigating a different hypothesis independently. Read their summaries to determine which hypothesis has evidence.

### 4. When Understanding Is Incomplete

Say "I do not understand why this callback fires twice." Do not propose fixes when understanding is incomplete. Ask for help. Research more.

## Phase 4: Implementation

Fix the root cause, not the symptom.

### 1. Create a Failing Test Case

Write the simplest reproduction as an automated test. This MUST exist before fixing. If no test framework is available, a one-off script suffices.

### 2. Implement a Single Fix

Address the root cause. ONE change at a time. Change only what addresses the root cause. No bundled refactoring.

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

**Four validation layers:**

**Layer 1 -- Entry point:** Reject invalid input at API boundary. Validate: not empty, exists, correct type. Throw with descriptive message.

**Layer 2 -- Business logic:** Ensure data makes sense for this operation. Check preconditions specific to the function's contract.

**Layer 3 -- Environment guards:** Prevent dangerous operations in specific contexts. Example: refuse filesystem operations outside temp directories during tests.

**Layer 4 -- Debug instrumentation:** Log context before dangerous operations for forensics. Include: arguments, cwd, environment, stack trace.

**Why all four:** Different layers catch different failures. Different code paths bypass entry validation. Mocks bypass business logic. Edge cases on different platforms need environment guards. Debug logging identifies structural misuse. One validation point is insufficient.

Apply: trace data flow, map all checkpoints, add validation at each layer, test each layer independently.

## Red Flags -- Return to Phase 1

If any of these thoughts occur, STOP and return to Phase 1:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems to fix" (listing fixes without investigation)
- "Let me propose solutions before understanding the flow"
- "One more fix attempt" (when 2+ already tried)
- "This fix revealed a new problem elsewhere"

## User Signals of Process Violation

Watch for these redirections from the user:
- "Is that not happening?" -- assumption without verification
- "Will it show us...?" -- missing evidence gathering
- "Stop guessing" -- fixes without understanding
- "Ultrathink this" -- symptom focus instead of fundamental questioning

When these signals appear: STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes do not stick. Test first proves it. |
| "Multiple fixes at once saves time" | Cannot isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, do not fix again. |

## Condition-Based Waiting

When debugging flaky tests caused by timing issues, replace arbitrary timeouts with condition polling.

**Core pattern:**
```typescript
// BAD: guessing at timing
await new Promise(r => setTimeout(r, 50));

// GOOD: waiting for condition
await waitFor(() => getResult() !== undefined);
```

**Quick patterns:**
| Scenario | Pattern |
|---|---|
| Wait for event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Wait for state | `waitFor(() => machine.state === 'ready')` |
| Wait for file | `waitFor(() => fs.existsSync(path))` |

**Generic polling function:**
```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string, timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();
  while (true) {
    const result = condition();
    if (result) return result;
    if (Date.now() - startTime > timeoutMs)
      throw new Error(`Timeout: ${description} after ${timeoutMs}ms`);
    await new Promise(r => setTimeout(r, 10));
  }
}
```

**Mistakes:** Polling too fast (use 10ms). No timeout (always include with clear error). Stale data (call getter inside loop, not before).

**When arbitrary timeout IS correct:** First wait for the triggering condition, then wait a known interval. Document WHY: "200ms = 2 ticks at 100ms intervals."

## Reporting

During debugging: state current phase, quote error messages, show evidence.
After resolution: root cause (1-2 sentences), evidence trail, fix applied, test results.

## Quick Reference

| Phase | Key Activities | Success Criteria |
|---|---|---|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |

---

*Originally based on systematic-debugging, adapted and enhanced for this plugin.*
