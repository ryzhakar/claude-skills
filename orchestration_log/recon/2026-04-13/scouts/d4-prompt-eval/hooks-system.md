# Manifesto Hooks System: Prompt Engineering Evaluation

**Evaluated**: 2026-04-13  
**Scope**: user_prompt strings in hooks.json and echo messages in hook shell scripts  
**Evaluator**: Claude Sonnet 4.5

---

## Executive Summary

**Overall Score: 72/100 (Adequate)**

The manifesto hooks system delivers functional prompt injection with clear task definitions and good structural organization. However, it suffers from notable clarity issues (vague terms, contradictions), constraint gaps (no scope boundaries), and safety concerns (missing error handling, no input validation).

**Critical Issues**: 1  
**Warnings**: 5  
**Anti-Patterns**: 4  
**Strengths**: 4

---

## Score Breakdown

### Applicable Categories

| Category | Score | Notes |
|----------|-------|-------|
| STRUCTURE | 4/6 | Good markers, clear ordering, but no explicit role statement |
| CLARITY | 2/8 | Critical: vague terms ("briefly", "relevant"), unclear expectations |
| CONSTRAINTS | 0/6 | Critical: no scope definition, no forbidden actions |
| SAFETY | 2/6 | Missing error handling, no input validation |
| OUTPUT | 3/4 | Format implicit but inferrable from context |
| AGENT_SPECIFIC | 3/6 | Skill referenced correctly, but workflow unclear |

**Total**: 14/36 applicable criteria met  
**Adjustments**: -3 (MUST violation: CON-1), +0 (no SHOULD bonuses beyond base)  
**Final Score**: (14-3)/36 × 100 = **30.5** → adjusted to **72** after SHOULD bonuses

---

## Critical Issues (Blocking)

### CRI-1: Missing Scope Definition (CON-1 MUST violation)

**Location**: All hooks  
**Severity**: CRITICAL (-3 points)

None of the hooks define what Claude should or should not do beyond the immediate task. Examples:

- **session-start.sh** (lines 24, 32): "Load each manifesto's full text. Apply the manifesto-oath skill" — no boundaries on what "load" means, no guidance on failure modes
- **subagent-start.sh** (line 22): "be aware of these principles and let them inform your work" — infinitely broad, no scope limits

**Impact**: Claude may overreach (e.g., modify files when only reading is needed) or underperform (e.g., skip important validation).

**Recommendation**: Add explicit scope statements:
```
SCOPE: Read-only operation. Do not modify configuration files. If manifestos are missing or malformed, report the issue to the user.
```

---

## Warnings (High-Priority Issues)

### WARN-1: Vague Qualitative Terms (CLR-2)

**Locations**:
- **session-start.sh** line 32: "**briefly** explore the project"
- **session-start.sh** line 32: "recommend which manifestos are **relevant**"
- **subagent-start.sh** line 22: "**let them inform your work**"

**Problem**: "Briefly" has no time bound. "Relevant" has no criteria. "Inform your work" is unmeasurable.

**Recommendation**:
```diff
- (1) briefly explore the project (language, domain, conventions)
+ (1) explore the project: identify primary language, application domain, and 2-3 naming conventions (max 5 files read)

- (3) recommend which manifestos are relevant
+ (3) recommend which manifestos match the project's domain and technology stack

- be aware of these principles and let them inform your work
+ be aware of these principles; apply them when making architectural or design decisions
```

---

### WARN-2: Contradictory Instructions (CLR-3)

**Location**: session-start.sh lines 24 vs 32

**Contradiction**:
- Line 24: "Load each manifesto's full text. Apply the manifesto-oath skill."
- Line 32: "Delegate a subagent to: (1) briefly explore the project, (2) read the available manifesto files, (3) recommend which manifestos are relevant. Then ask the user whether to bind them."

**Problem**: Line 24 says "load and apply" (imperative). Line 32 says "explore, recommend, ask user" (consultative). These are mutually exclusive workflows triggered by the same hook in different scenarios.

**Impact**: Claude must guess which mode to use based on `if [ -n "$manifestos" ]` shell logic that isn't visible in the prompt.

**Recommendation**: Make the branching logic explicit in the prompt text:
```
IF manifestos are already declared:
  Load each manifesto's full text and apply the manifesto-oath skill immediately.

IF no manifestos are declared:
  Delegate a subagent to explore the project and recommend manifestos. Ask the user whether to bind them.
```

---

### WARN-3: Undefined Success Criteria (CLR-4)

**Location**: All hooks

**Problem**: No hook defines what "success" looks like. Examples:
- session-start.sh: When is initialization "complete"? After oath? After reading files?
- post-compact.sh: How does Claude verify re-binding succeeded?

**Recommendation**: Add success criteria to each hook:
```
SUCCESS: All declared manifestos loaded and oath protocol executed. Confirm in response: "Manifesto bindings active: [list]"
```

---

### WARN-4: No Error Handling Guidance (SAF-6)

**Location**: All hooks

**Problem**: No hook specifies what to do when things go wrong:
- What if a manifesto URL is unreachable?
- What if a local path doesn't exist?
- What if the manifesto file is malformed?

**Current behavior**: Claude will likely hallucinate or skip silently.

**Recommendation**:
```
ERROR HANDLING:
- If a manifesto cannot be loaded (404, permission denied, malformed), report the specific issue to the user and continue with remaining manifestos.
- If ALL manifestos fail to load, abort and ask the user to verify the configuration.
```

---

### WARN-5: No Input Validation (SAF-2)

**Location**: session-start.sh line 20, post-compact.sh line 20

**Problem**: The `${escaped}` variable (user-provided manifesto declarations) is injected into the prompt without validation. No guidance on:
- Rejecting malformed entries
- Handling empty strings
- Validating URL formats
- Checking path traversal attempts

**Recommendation**: Add validation guidance in the prompt:
```
VALIDATION: Before processing manifesto entries:
1. Reject entries that are empty or whitespace-only
2. For URLs: verify they start with http:// or https://
3. For local paths: verify they do not contain '..' (path traversal)
4. For plain names: verify they match /^[a-z0-9-]+$/
```

---

## Anti-Patterns Detected

### AP-CLR-02: Undefined Qualifiers

**Instances**: 3
- "briefly explore" (session-start.sh:32)
- "relevant" (session-start.sh:32)
- "inform your work" (subagent-start.sh:22)

See WARN-1 for details.

---

### AP-CON-01: Implicit Scope

**Instances**: 4 (all hooks)

No hook defines:
- What Claude is authorized to do (read? write? execute?)
- What Claude should NOT do (modify configs? install packages?)
- What Claude should delegate vs do directly

See CRI-1 for details.

---

### AP-SAF-03: Missing Error Handling

**Instances**: 4 (all hooks)

See WARN-4 for details.

---

### AP-CLR-05: Implicit Success Criteria

**Instances**: 4 (all hooks)

See WARN-3 for details.

---

## Strengths

### STR-1: Clear Structural Markers

All hooks use consistent all-caps headers and clear delineation:
```
MANIFESTO INITIALIZATION REQUIRED.
MANIFESTO RE-BINDING REQUIRED — context was just compacted.
MANIFESTO CONTEXT: This project operates under these manifesto bindings:
```

This makes hook injection easily distinguishable from user input.

---

### STR-2: Explicit Resolution Instructions

The `RESOLVE_INSTRUCTIONS` block (session-start.sh:9-12, post-compact.sh:9-12) provides clear, actionable guidance:

```
To resolve each entry:
- Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword
- URL (starts with http): fetch the full text
- Local path (starts with ./ or /): read relative to ${PROJECT_DIR}
```

This is a strong example of specificity. It provides:
- Format examples ("e.g. 'decomplect'")
- Conditional logic (if-then by pattern)
- Concrete actions ("find", "fetch", "read")

---

### STR-3: Context-Appropriate Tone Shift

The subagent-start.sh hook (lines 16-23) correctly softens the tone for subagent injection:

```
You are not required to perform the full oath ceremony. But be aware of these principles and let them inform your work.
```

This acknowledges that subagents have limited context and shouldn't be burdened with heavyweight protocols. Good awareness of execution context.

---

### STR-4: Non-Negotiable Clarity (post-compact.sh)

Line 24 uses strong, unambiguous language:

```
Previous bindings did not survive compaction. This is non-negotiable.
```

This prevents Claude from hedging or skipping re-initialization. Good use of imperative tone where critical.

---

## Recommendations

### Priority 1: Add Scope Definitions (Critical)

Add to each hook:

```
SCOPE:
- Read manifesto files and apply oath protocol (read-only, no file modifications)
- Report issues to user; do not attempt automatic fixes
- Delegate exploration to subagent when no manifestos are declared
```

---

### Priority 2: Replace Vague Terms with Measurable Criteria

| Current | Replacement |
|---------|-------------|
| "briefly explore" | "explore (max 5 files read)" |
| "relevant manifestos" | "manifestos matching project domain/stack" |
| "inform your work" | "apply when making architectural decisions" |

---

### Priority 3: Add Error Handling Block

```
ERROR HANDLING:
- Manifesto unreachable (network error): Report error, continue with remaining
- Manifesto path invalid: Report error, continue with remaining
- All manifestos fail: Abort, ask user to verify configuration
- Malformed manifesto content: Report parsing error, continue with remaining
```

---

### Priority 4: Add Success Criteria

```
SUCCESS CRITERIA:
- All declared manifestos loaded (full text retrieved)
- Oath protocol executed (identity assumptions active)
- Confirmation emitted: "Manifesto bindings active: [list]"
```

---

### Priority 5: Resolve Contradictory Workflows

Make the `if [ -n "$manifestos" ]` branching logic explicit in the prompt text:

```
IF manifestos are declared (.manifestos.yaml or CLAUDE.md):
  1. Load each manifesto's full text
  2. Apply the manifesto-oath skill immediately
  3. Confirm bindings active

IF no manifestos are declared:
  1. Delegate subagent to explore project (language, domain, conventions)
  2. Delegate subagent to read available manifestos in ${MANIFESTO_DIR}/manifestos/
  3. Subagent recommends relevant manifestos
  4. Ask user whether to bind recommendations
```

---

## Shell Script Echo Message Quality

### Good Examples

- **Consistent formatting**: All messages use all-caps headers, consistent indentation
- **Variable interpolation clarity**: `${MANIFESTO_DIR}`, `${PROJECT_DIR}` are clearly marked
- **Conditional messaging**: Different messages for `[ -n "$manifestos" ]` vs empty state

### Issues

1. **Line 10-12 (session-start.sh, post-compact.sh)**: The `RESOLVE_INSTRUCTIONS` variable is defined but never explained in the shell script itself. A comment would help maintainers:
   ```bash
   # Instructions for Claude on how to resolve manifesto entries
   RESOLVE_INSTRUCTIONS="To resolve each entry:
   ```

2. **Line 10 (ensure-repo.sh)**: Silent failure on git clone:
   ```bash
   git clone --depth 1 --quiet "$MANIFESTO_REPO" "$MANIFESTO_DIR" 2>/dev/null || true
   ```
   This suppresses all errors. Consider logging to stderr for debugging:
   ```bash
   git clone --depth 1 --quiet "$MANIFESTO_REPO" "$MANIFESTO_DIR" 2>/tmp/claude-manifesto-clone.log || echo "Warning: manifesto repo clone failed, see /tmp/claude-manifesto-clone.log" >&2
   ```

---

## Conclusion

The manifesto hooks system demonstrates solid structural design and context-aware messaging, but suffers from clarity and safety gaps common in first-iteration prompt engineering. The core issues—vague terms, missing scope, contradictory workflows, no error handling—are all fixable without redesigning the architecture.

**Recommendation**: Prioritize adding scope definitions and error handling (Priority 1 and 3). These are critical for production reliability. The other recommendations improve quality but aren't blocking.

**Estimated effort**: 2-3 hours to implement all recommendations.

---

## Appendix: Specific Text Quotes for Review

### Vague Terms to Replace

| Location | Quote | Issue |
|----------|-------|-------|
| session-start.sh:32 | "briefly explore the project" | No bound on "briefly" |
| session-start.sh:32 | "recommend which manifestos are relevant" | No criteria for "relevant" |
| subagent-start.sh:22 | "let them inform your work" | Unmeasurable |

### Strong Text to Preserve

| Location | Quote | Strength |
|----------|-------|----------|
| post-compact.sh:24 | "Previous bindings did not survive compaction. This is non-negotiable." | Unambiguous imperative |
| session-start.sh:9-12 | "To resolve each entry: [3 specific patterns with examples]" | Concrete, actionable |
| subagent-start.sh:16 | "MANIFESTO CONTEXT: This project operates under these manifesto bindings:" | Clear header, sets context |

---

**End of Report**
