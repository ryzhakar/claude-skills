# Synthesis: hooks-system

**Baseline:** 217 tokens (hooks.json) + prompt strings in 4 shell scripts (~480 tokens of injected text across session-start.sh, subagent-start.sh, post-compact.sh, ensure-repo.sh)
**Total addressable prompt surface:** ~697 tokens

---

## Core Points (D2 -- untouchable)

1. Compaction requires re-binding: previous bindings do not survive compaction, re-application is non-negotiable
2. Two-tiered injection: full oath ceremony for main sessions (SessionStart), lightweight awareness for subagents (SubagentStart)
3. Three-mode resolution: plain name (keyword match against repo), URL (fetch), local path (read from project dir)
4. Lazy clone with failure tolerance: repo cloned on first access, `|| true` prevents hook failure
5. Subagent-delegated recommendation: when no config exists, delegate exploration, then ask user

---

## Inline from References

No external reference files. The hooks system is self-contained: hooks.json + 4 shell scripts. Nothing to inline.

---

## Cut

### C1. RESOLVE_INSTRUCTIONS block -- tighten in both locations

Identical text in session-start.sh and post-compact.sh (lines 9-12 each).

**Before:**
```
To resolve each entry:
- Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword
- URL (starts with http): fetch the full text
- Local path (starts with ./ or /): read relative to ${PROJECT_DIR}
```

**After (D3 R13, R15 applied):**
```
Resolve each entry:
- Plain name (e.g. 'decomplect'): find by keyword in ${MANIFESTO_DIR}/manifestos/
- URL (http/https): fetch full text
- Local path (./ or /): read from ${PROJECT_DIR}
```

**Citation:** D3 lines 104-119 (R13: "starts with http" -> "http/https"; "find the matching file in" -> "find by keyword in"); D3 lines 148-169 (R15: parallel grammar).

**Delta:** -12 tokens (x2 locations = -24 tokens total).

### C2. "Declared manifestos:" vagueness

D3 (R12 severe): "Declared" is vague -- declared by whom?

**Action:** Change to "Configured manifestos:" in both session-start.sh and post-compact.sh.

**Citation:** D3 lines 40-44 (R12).

**Delta:** 0 tokens (word swap).

### C3. session-start.sh no-config branch wordiness + vague terms

D3 (R13 moderate) + D4 (WARN-1, CLR-2): "briefly explore" has no bound; "relevant" has no criteria; "the available manifesto files in" is wordy.

**Before:**
```
Delegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, (3) recommend which manifestos are relevant. Then ask the user whether to bind them.
```

**After:**
```
Delegate a subagent to: (1) scan the project (primary language, domain, 2-3 conventions -- max 5 files), (2) read manifestos from ${MANIFESTO_DIR}/manifestos/, (3) recommend manifestos matching project domain. Then ask the user whether to bind them.
```

**Citation:** D3 lines 132-137 (R13); D4 WARN-1 (CLR-2: quantify "briefly", specify "relevant").

**Delta:** -3 tokens.

### C4. post-compact.sh else-branch ambiguity

D3 (R13 moderate): "If manifestos were previously bound, re-apply the manifesto-oath skill." -- this conditional is unresolvable after compaction destroyed the evidence.

**Before:**
```
MANIFESTO PLUGIN ACTIVE -- context was just compacted. If manifestos were previously bound, re-apply the manifesto-oath skill. Repo manifestos available in: ${MANIFESTO_DIR}/manifestos/.
```

**After:**
```
MANIFESTO PLUGIN ACTIVE -- context compacted. No manifesto configuration found. Available manifestos: ${MANIFESTO_DIR}/manifestos/.
```

**Citation:** D3 lines 139-146 (R13: unresolvable conditional).

**Delta:** -8 tokens.

### C5. subagent-start.sh negative construction and weak ending

D3 (R11 moderate): "You are not required to perform the full oath ceremony." -- negative form.
D3 (R18 moderate): Ends with procedural "If you need the full text, read from the paths above or fetch URLs." -- weak closing.

**Before:**
```
MANIFESTO CONTEXT: This project operates under these manifesto bindings:
${escaped}

Repo manifestos: ${MANIFESTO_DIR}/manifestos/
Local paths resolve from: ${PROJECT_DIR}

You are not required to perform the full oath ceremony. But be aware of these principles and let them inform your work. If you need the full text, read from the paths above or fetch URLs.
```

**After:**
```
MANIFESTO CONTEXT: This project follows these manifesto principles:
${escaped}

Manifesto source: ${MANIFESTO_DIR}/manifestos/
Local paths resolve from: ${PROJECT_DIR}

Skip the full oath ceremony. Apply these principles when making design or architectural decisions. For full text, read from paths above or fetch URLs.
```

**Citation:** D3 lines 75-91 (R11: negative -> positive); D3 lines 198-205 (R18: reorder); D3 lines 64-69 (R12: "operates under" -> "follows").

**Delta:** -5 tokens.

---

## Restructure

### R1. Dismiss D4 WARN-2 (contradictory workflows) as false positive

D4 flagged session-start.sh lines 24 vs 32 as contradictory instructions. This is a false positive: the shell `if [ -n "$manifestos" ]` correctly gates which prompt Claude receives. Claude never sees both branches simultaneously.

**Citation:** D4 WARN-2; hooks-full-spec.md section 5 (exit code 0: stdout parsed as context -- only one branch renders per invocation).

**No action.**

### R2. hooks.json -- SessionStart matcher: add "resume"

Current matcher: `"startup"`. This means the hook fires only on fresh startup, not on session resume. Resumed sessions should re-bind manifestos because resume restores context but not behavioral state.

**Action:** Change matcher from `"startup"` to `"startup|resume"`.

**Citation:** hooks-full-spec.md section 2 (SessionStart matcher filters on: startup, resume, clear, compact).

**Delta:** +1 token in hooks.json. High behavioral impact.

---

## Strengthen

### S1. Add scope statement to injected prompts

D4 (CRI-1, CON-1 MUST violation): No hook defines scope boundaries.

**Action:** Add after RESOLVE_INSTRUCTIONS in session-start.sh main branch:
```
SCOPE: Read manifesto text and apply oath protocol. Do not modify project files. Report loading errors to the user.
```

Add in post-compact.sh main branch:
```
SCOPE: Re-read and re-bind manifestos. Do not modify project files.
```

**Citation:** D4 CRI-1 (lines 43-58); D4 recommendation Priority 1 (lines 267-276).

**Delta:** +20 tokens total across both scripts.

### S2. Add error handling guidance

D4 (WARN-4, SAF-6): No hook specifies what to do when manifesto loading fails.

**Action:** Add to session-start.sh and post-compact.sh main branches:
```
If a manifesto cannot be loaded (network error, missing file, malformed content), report the error and continue with remaining manifestos.
```

**Citation:** D4 WARN-4 (lines 125-141); D4 recommendation Priority 3 (lines 291-298).

**Delta:** +18 tokens total across both scripts.

---

## Projected Token Delta

| Category | Tokens |
|---|---|
| Baseline (prompt surface) | ~697 |
| Cut: RESOLVE_INSTRUCTIONS tightening (C1) | -24 |
| Cut: no-config branch (C3) | -3 |
| Cut: post-compact else-branch (C4) | -8 |
| Cut: subagent injection rewrite (C5) | -5 |
| Restructure: SessionStart matcher (R2) | +1 |
| Strengthen: scope statements (S1) | +20 |
| Strengthen: error handling (S2) | +18 |
| **Projected total** | **~696** |
| **Net delta** | **-1 (~0%)** |

Net prompt surface is roughly flat. The cuts fund the strengthening additions. D4 scored this unit at 72% (lowest in plugin), and the primary deficiency was missing scope/error-handling -- not verbosity. The strengthening additions close the gap without expanding the footprint.

### hooks.json structural delta

hooks.json changes only the SessionStart matcher (`"startup"` -> `"startup|resume"`). No other structural changes to the JSON.
