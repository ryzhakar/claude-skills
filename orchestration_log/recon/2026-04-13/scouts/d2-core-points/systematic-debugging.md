# Core Points: systematic-debugging

## Iteration 1

**Point**: No fixes may be proposed without completing root cause investigation first (Phase 1), because symptom fixes and random guessing waste time and create new bugs.

**Evidence**:
- SKILL.md lines 17-21: "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST ... If Phase 1 has not been completed, no fix may be proposed. Symptom fixes are debugging failures."
- SKILL.md lines 163-177: Red flags section lists "Quick fix for now, investigate later", "Just try changing X and see if it works", and "I don't fully understand but this might work" as signals to STOP and return to Phase 1
- root-cause-tracing.md lines 154: "NEVER fix just where the error appears. Trace back to find the original trigger."

## Iteration 2

**Point**: In multi-component systems, add diagnostic instrumentation at every component boundary to gather evidence showing WHERE it breaks before proposing any fixes.

**Evidence**:
- SKILL.md lines 54-70: "For EACH component boundary: - Log what data enters the component - Log what data exits the component - Verify environment/config propagation - Check state at each layer ... Run once to gather evidence showing WHERE it breaks THEN analyze evidence to identify the failing component THEN investigate that specific component"
- SKILL.md lines 42-44: "Read stack traces completely. Note line numbers, file paths, error codes. Error messages often contain the exact solution."
- root-cause-tracing.md lines 67-95: Shows stack trace instrumentation pattern with console.error and explains running "npm test 2>&1 | grep 'DEBUG git init'" to analyze traces

## Iteration 3

**Point**: After reaching 3 failed fix attempts, STOP and question the architecture itself rather than continuing to fix symptoms, because this pattern indicates fundamental design problems not hypothesis failures.

**Evidence**:
- SKILL.md lines 138-156: "STOP. Count fix attempts: ... 3 or more: STOP and question the architecture (see below) ... Pattern indicating an architectural problem: - Each fix reveals new shared state, coupling, or problems in different places ... STOP and question fundamentals: - Is this pattern fundamentally sound? ... This is not a failed hypothesis -- this is a wrong architecture."
- SKILL.md lines 177: Red flags include "One more fix attempt (when 2+ already tried)"
- SKILL.md lines 200-201: Common rationalization "'One more fix attempt' (after 2+ failures)" with reality "3+ failures = architectural problem. Question pattern, do not fix again."

## Iteration 4

**Point**: Fix bugs at their source by tracing backward through the entire call chain to find the original trigger, not at the symptom point where the error appears.

**Evidence**:
- SKILL.md lines 72-76: "When the error is deep in a call stack, trace backward through the call chain until the original trigger is found. Fix at source, not at symptom."
- root-cause-tracing.md lines 4-7: "Bugs often manifest deep in the call stack ... Your instinct is to fix where the error appears, but that's treating a symptom. Core principle: Trace backward through the call chain until you find the original trigger, then fix at the source."
- root-cause-tracing.md lines 110-122: Real example traces through 5 levels from "git init runs in process.cwd()" back to "Test accessed context.tempDir before beforeEach" as root cause

## Iteration 5

**Point**: After fixing the root cause, add validation at every layer the bad data passed through (entry point, business logic, environment guards, debug instrumentation) to make the bug structurally impossible.

**Evidence**:
- SKILL.md lines 158-161: "After fixing the root cause, add validation at every layer the bad data passed through. Make the bug structurally impossible, not just fixed. For the 4-layer validation pattern (entry point, business logic, environment guards, debug instrumentation), see @references/defense-in-depth.md"
- defense-in-depth.md lines 7-8: "Core principle: Validate at EVERY layer data passes through. Make the bug structurally impossible."
- defense-in-depth.md lines 115-121: "All four layers were necessary. During testing, each layer caught bugs the others missed: - Different code paths bypassed entry validation - Mocks bypassed business logic checks - Edge cases on different platforms needed environment guards - Debug logging identified structural misuse ... Don't stop at one validation point. Add checks at every layer."

## Rank Summary

1. **Mandatory root cause investigation before fixes** - The foundational "Iron Law" repeated throughout (lines 17-21, 163-177, root-cause-tracing.md:154)
2. **Multi-component diagnostic instrumentation** - Required for complex systems to identify failing layers (lines 54-70)
3. **3-failure architectural questioning threshold** - Critical escape valve from symptom-fixing loops (lines 138-156, 177, 200-201)
4. **Trace to source, not symptom** - Core debugging direction principle (lines 72-76, root-cause-tracing.md:4-7, 110-122)
5. **Defense-in-depth validation** - Post-fix hardening across all layers (lines 158-161, defense-in-depth.md:7-8, 115-121)
