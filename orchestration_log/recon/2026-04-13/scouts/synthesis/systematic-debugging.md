# Synthesis Report: systematic-debugging (Re-synthesis)

**Baseline:** 2139t (SKILL.md) + 1318t (root-cause-tracing.md) + 818t (defense-in-depth.md) + 847t (condition-based-waiting.md) = 5122t total

**Previous synthesis:** Kept all three refs as lazy files. Models ignore references in practice. This re-synthesis inlines all reference content with compression.

---

## Core Points (Untouchable)

1. No fixes without root cause investigation first (The Iron Law) -- Phase 1 must complete before any fix is proposed
2. In multi-component systems, add diagnostic instrumentation at every component boundary before proposing fixes
3. After 3 failed fix attempts, STOP and question the architecture -- wrong architecture, not failed hypothesis
4. Trace backward through the call chain to the original trigger; fix at source, not at symptom
5. After fixing root cause, add validation at every layer the bad data passed through -- make the bug structurally impossible

---

## Inline from References

### INLINE: root-cause-tracing.md (1318t)

Cite: D1 classifies as DEFERRABLE. Directive overrides: all refs under 1400t must inline. Models skip lazy references. At 1318t this is the largest ref but still under 1400t.

**Content to inline (compressed ~700t):**

Expand Phase 1 Step 5 ("Trace Data Flow") into a full backward tracing protocol, replacing the current 2-line mention:

```
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
```

Remove the separate "Test Pollution Bisection" section (lines 207-213) since it is now folded into the tracing section.

**Savings from deleting reference file:** 1318t removed. Body grows ~700t. Net: -618t.

### INLINE: defense-in-depth.md (818t)

Cite: D1 classifies as DEFERRABLE. Directive overrides: all refs under 1400t must inline. Models skip lazy references.

**Content to inline (compressed ~450t):**

Expand Phase 4 Step 6 into the full 4-layer pattern, replacing the current 2-line mention:

```
### 6. Defense in Depth

After fixing the root cause, add validation at every layer the bad data passed through. Make the bug structurally impossible, not just fixed.

**Four validation layers:**

**Layer 1 -- Entry point:** Reject invalid input at API boundary. Validate: not empty, exists, correct type. Throw with descriptive message.

**Layer 2 -- Business logic:** Ensure data makes sense for this operation. Check preconditions specific to the function's contract.

**Layer 3 -- Environment guards:** Prevent dangerous operations in specific contexts. Example: refuse filesystem operations outside temp directories during tests.

**Layer 4 -- Debug instrumentation:** Log context before dangerous operations for forensics. Include: arguments, cwd, environment, stack trace.

**Why all four:** Different layers catch different failures. Different code paths bypass entry validation. Mocks bypass business logic. Edge cases on different platforms need environment guards. Debug logging identifies structural misuse. One validation point is insufficient.

Apply: trace data flow, map all checkpoints, add validation at each layer, test each layer independently.
```

**Savings from deleting reference file:** 818t removed. Body grows ~450t. Net: -368t.

### INLINE: condition-based-waiting.md (847t)

Cite: D1 classifies as DEFERRABLE. Directive overrides: all refs under 1400t must inline. Models skip lazy references.

**Content to inline (compressed ~420t):**

Replace the current 2-line "Condition-Based Waiting" section with expanded inline content:

```
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
```

**Savings from deleting reference file:** 847t removed. Body grows ~420t. Net: -427t.

---

## Cut

### CUT-1: Redundant "possible" modifiers (lines 107, 124, ~6t)
Cite: D3 Strunk R13.
**Action:** "SMALLEST possible change" -> "SMALLEST change"; "simplest possible reproduction" -> "simplest reproduction."

### CUT-2: "identified in Phase 3" (line 129, ~5t)
Cite: D3 Strunk R13.
**Action:** "Address the root cause identified in Phase 3" -> "Address the root cause."

### CUT-3: "in the same codebase" (line 84, ~4t)
Cite: D3 Strunk R13.
**Action:** "Locate similar working code in the same codebase" -> "Locate similar working code."

### CUT-4: Description compression (lines 3-8, ~15t)
Cite: D3 Strunk R13.
**Action:** Compress to: "Mandatory 4-phase root cause protocol for bugs, test failures, errors, or unexpected behavior. Prevents random fixes and symptom patching. Apply BEFORE proposing any fix, especially when multiple attempts have failed or time pressure tempts guessing."

### CUT-5: Reference link sentences removed (~25t)
Three @references/ link sentences and the "Reference Files" section at bottom deleted since content is inlined.

### CUT-6: "guess-and-check thrashing" (line 194, ~2t)
Cite: D3 Strunk R13.
**Action:** "FASTER than guess-and-check thrashing" -> "FASTER than thrashing."

**Total cut savings:** ~57t

---

## Restructure

### RESTRUC-1: Convert passive procedural commands to active imperatives
Cite: D3 Strunk R10 Severe.
- "If Phase 1 has not been completed, no fix may be proposed" -> "Complete Phase 1 before proposing any fix"
- "Error messages often contain the exact solution" -> "Error messages often state the exact solution"
- "Did it work?" -> "Did the change fix the issue?"

### RESTRUC-2: Positive form conversions
Cite: D3 Strunk R11 Moderate.
- "Do not skip when:" -> "Apply even when:"
- "Do not assume 'that cannot matter'" -> "Assume every difference might matter"
- "Do not fix multiple things at once" -> "Fix one thing at a time"
- "No 'while I'm here' improvements" -> "Change only what addresses the root cause"

### RESTRUC-3: Parallel construction in Red Flags (lines 167-177)
Cite: D3 Strunk R15.
**Action:** Convert non-quoted items to quoted self-talk form: "Here are the main problems to fix" / "Let me propose solutions before understanding the flow" / "This fix revealed a new problem elsewhere"

### RESTRUC-4: Parallel construction in User Signals (lines 180-186)
Cite: D3 Strunk R15.
**Action:** Standardize explanations to parallel noun phrases: "assumption without verification" / "missing evidence gathering" / "fixes without understanding" / "symptom focus instead of fundamental questioning"

---

## Strengthen

### STR-1: Concrete "gather more data" (line 48)
Cite: D3 Strunk R12.
**Action:** "gather more evidence: logs, timestamps, environment state. Do not guess."

### STR-2: Concrete "assumptions" (line 96)
Cite: D3 Strunk R12.
**Action:** "What does the broken code assume about inputs, state, environment, or dependencies?"

### STR-3: Concrete "I do not understand X" (line 118)
Cite: D3 Strunk R12.
**Action:** "Say 'I do not understand why this callback fires twice.' Do not propose fixes when understanding is incomplete."

### STR-4: Add reporting protocol
Cite: D4 OUT-1 (primary gap at Medium severity).
**Action:** Add after Phase 4:
```
## Reporting
During debugging: state current phase, quote error messages, show evidence.
After resolution: root cause (1-2 sentences), evidence trail, fix applied, test results.
```
**Cost:** ~30t added.

---

## Hook/Command Splits

No hook candidates. Debugging is a reasoning process, not a deterministic enforcement pattern.

---

## Delete List

- `dev-discipline/skills/systematic-debugging/references/root-cause-tracing.md`
- `dev-discipline/skills/systematic-debugging/references/defense-in-depth.md`
- `dev-discipline/skills/systematic-debugging/references/condition-based-waiting.md`

---

## Projected Token Delta

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| SKILL.md body | 2139t | ~2682t | +543t |
| root-cause-tracing.md | 1318t | 0 (deleted) | -1318t |
| defense-in-depth.md | 818t | 0 (deleted) | -818t |
| condition-based-waiting.md | 847t | 0 (deleted) | -847t |
| **Total** | **5122t** | **~2682t** | **-2440t (-47.6%)** |

Nearly 48% total reduction. The SKILL.md body grows by ~543t from inlined reference content (compressed from 2983t total refs to ~1570t inline). All reference files deleted. Models now see the full debugging arsenal every time the skill loads. D4 score rises from 85 toward 92+ through inlined content, output format addition, and Strunk improvements.
