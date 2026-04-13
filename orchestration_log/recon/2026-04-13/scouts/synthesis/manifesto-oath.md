# Synthesis: manifesto-oath

**Baseline:** 1058 tokens (SKILL.md) + 1111 tokens (theory.md) + 740 tokens (configuration.md) = 2909 tokens total addressable

---

## Core Points (D2 -- untouchable)

1. Identity-mode transformation: reframe from promise about future behavior to present-tense constitutional constraint defining operating identity
2. Technical vs theatrical language: "operating mode" / "constitutional constraint" engage compliance circuits; "swear" / "promise" engage performance circuits
3. Verification loop as functional conscience: check alignment before each response, flag tensions explicitly, refuse/modify/acknowledge
4. Why theatrical oaths fail: models lack memory persistence, identity continuity, social cost, illocutionary force
5. Constraint hierarchy: safety constraints > user explicit instructions > active manifesto > default behavior

---

## Inline from References

### PREVIOUS DECISION (OVERRIDDEN): Previous synthesis kept both refs as lazy `[label](path)` links. This is now overridden. Models ignore references in practice. Both refs total 1851 tokens. Both under 1200 tokens each. INLINE BOTH.

### theory.md (1111t) -> Inline compressed

**Load-bearing content to extract:**

1. **The thermostat analogy** (why identity-assumption beats promise-making): A thermostat does not "promise" to maintain 70 degrees. It operates under a constraint that defines its behavior. The manifesto should relate to the model the same way.

2. **Circuit activation distinction** (the technical mechanism): "Operating mode" and "constitutional constraint" engage compliance and verification circuits. "Swear" and "promise" engage performance circuits. The linguistic framing determines which circuits activate.

3. **Constitutional AI pattern adaptation** (Bai et al., 2022): Models can critique their own outputs against stated principles. The verification loop adapts this: before generating, check alignment; if tension exists, flag explicitly. This loop must be explicitly invoked because models do not naturally self-verify against arbitrary user-provided constraints.

4. **Visibility as accountability substitute**: Models lack reputation. Transparency substitutes: require explicit flagging of any deviation, never permit quiet drift, force articulation of which principle is violated and why. This creates informational accountability the user can act on.

5. **Philosophical honesty**: This approach creates behavioral equivalence without phenomenological commitment. The model's outputs look like those of a committed agent without the model experiencing commitment. For practical purposes, reliable aligned behavior matters more than felt obligation.

**What to discard from theory.md:**
- Austin/Searle academic citations (models do not need the bibliography)
- Extended re-explanation of the four mechanisms (already in SKILL.md body "Why Theatrical Oaths Fail")
- Repeated identity-assumption vs promise-making table (already in SKILL.md "Critical Distinctions")
- Repeated constraint hierarchy (already in SKILL.md body)

**Compressed inline (target ~250 tokens):**

```markdown
## Why This Works

A thermostat does not promise to maintain 70 degrees -- it operates under a constraint that defines its behavior. Identity assumption creates the same relationship between model and manifesto.

The mechanism is linguistic: "operating mode" and "constitutional constraint" activate compliance circuits. "Swear" and "promise" activate performance circuits. Framing determines which circuits fire.

The verification loop adapts Constitutional AI (Bai et al., 2022): models can critique their own outputs against stated principles. This must be explicitly invoked -- models do not self-verify against arbitrary user constraints by default.

Models lack reputation, so visibility substitutes for social accountability. Require explicit flagging of every deviation. Never permit quiet drift. Force articulation of which principle is violated and why. The user can then act on this information.

This creates behavioral equivalence without phenomenological commitment. Reliable aligned behavior matters more than felt obligation.
```

**Citation:** theory.md full content; D1 manifesto-oath.md (original DEFERRABLE classification, now overridden by inlining directive).

**Delta:** +250 tokens added to SKILL.md body. theory.md reference file deleted. Net vs body+ref total: was 1058+1111=2169 for these tokens; now 1058+250=1308. **Net saving: -861 tokens (-39.7%) for theory content.**

### configuration.md (740t) -> Inline compressed

**Load-bearing content to extract:**

1. **Two config sources** (priority order): `.manifestos.yaml` at project root (preferred), then `## Active Manifestos` section in CLAUDE.md (fallback).

2. **Three entry types** in `.manifestos.yaml`: plain name (keyword-matched against repo `manifestos/` dir), URL (fetched via WebFetch), local path (read relative to project root). Entry shape determines type automatically.

3. **No-config behavior**: When neither source exists, delegate a subagent to explore project, read available manifesto files, recommend relevant ones, ask user before binding.

4. **Hook lifecycle**: Config read at three points -- SessionStart (clone repo, detect config, initialize), PostCompact (re-detect, re-bind since bindings do not survive compaction), SubagentStart (inject lightweight manifesto awareness).

**What to discard from configuration.md:**
- Extended YAML examples for different project types (Rust, Python, external URL) -- these are obvious once the three entry types are stated
- Detailed sed regex for CLAUDE.md extraction -- implementation detail in hook scripts, not needed in skill body
- Verbose resolution rules table -- already compressed into the three entry types above

**Compressed inline (target ~180 tokens):**

```markdown
## Project Configuration

Configure manifesto bindings at the project level. Two sources, checked in order:

1. **`.manifestos.yaml`** (preferred): YAML list at project root. Each entry auto-detected by shape:
   - Plain name (e.g. `decomplect`): keyword-matched against `manifestos/` dir in the LLM_MANIFESTOS repo
   - URL (`https://...`): fetched at initialization
   - Local path (`./docs/principles.md`): read relative to project root

2. **`## Active Manifestos` in CLAUDE.md** (fallback): freeform markdown between that heading and the next `##`. Names resolved against the repo.

When neither exists, the plugin delegates a subagent to explore the project, read available manifesto files, and recommend bindings -- then asks the user before activating.

The plugin hooks read this configuration at SessionStart (initialize bindings), PostCompact (re-bind -- bindings do not survive compaction), and SubagentStart (inject lightweight awareness).
```

**Citation:** configuration.md full content; D1 manifesto-oath.md (original DEFERRABLE classification, now overridden).

**Delta:** +180 tokens added to SKILL.md body. configuration.md reference file deleted. Net vs body+ref total: was 1058+740=1798 for these tokens; now 1058+180=1238. **Net saving: -560 tokens (-31.1%) for configuration content.**

### Reference files after inlining

Both `references/theory.md` and `references/configuration.md` become dead files. Delete them and the `references/` directory. The `@references/theory.md` and `@references/configuration.md` pointers (which were causing eager loading) are eliminated entirely since the content is now in the body.

---

## Cut

### C1. Description verbosity

D3 (R13 moderate): "through identity-assumption protocols rather than theatrical oath-taking" -> tighter. Trigger list "swear an oath, commit to, bind to, adopt, or operate under" is redundant.

**After:**
```yaml
description: >
  Enables behavioral binding to user-provided manifestos through identity assumption
  rather than theatrical oaths. Triggers when user asks Claude to swear an oath, bind
  to, or operate under a manifesto, principles, or ethical framework. Use when user
  provides a manifesto and requests behavioral commitment.
```

**Citation:** D3 lines 52-60 (R13).

**Delta:** -15 tokens.

### C2. Redundant opening line

Line 15: "Enable behavioral binding to user-provided manifestos through operational identity assumption rather than performative oath-taking."

Repeats the description. D3 (R13 minor) flags this.

**Action:** Delete. Start body with "## Why Theatrical Oaths Fail" directly.

**Citation:** D3 line 65; prompt-compression-strategies.md section 1.3 ("Only add context Claude doesn't already have").

**Delta:** -20 tokens.

### C3. Template wordiness

D3 (R13 minor): "Effective immediately, operating under these constitutional constraints:" -> "Now operating under these constitutional constraints:"

**Citation:** D3 lines 72-75.

**Delta:** -2 tokens.

### C4. Implementation bullets passive voice -> active imperative

D3 (R15 moderate): Lines 46-49 mix passive and active.

**After:**
- "Filter all responses through this constitution before output"
- "Flag tensions between requests and constitution explicitly"
- "Persist mode until explicitly revoked or conversation ends"
- "Acknowledge and explain any deviations"

**Citation:** D3 lines 126-132 (R15 parallel construction).

**Delta:** +3 tokens (clarity gain justified).

### C5. Degradation warning vagueness -> concrete

D3 (R10/R12 severe, priority 1): Lines 92-97 use abstract language and weak constructions.

**After:**
- "Long conversations push the manifesto farther back in context, weakening its influence"
- "Each new conversation starts fresh without the binding"
- "Baseline safety constraints always supersede the manifesto"
- "This creates persistent behavioral constraint, not guaranteed compliance"

**Citation:** D3 lines 218-223 (priority 1 revision).

**Delta:** +5 tokens.

### C6. Remove reference pointer sections

Previous SKILL.md had `## Project Configuration` and `## Theoretical Foundation` sections each pointing to a ref file via `@` syntax. Both sections are now replaced by the inlined compressed content (see Inline section above). The `@` pointers and their wrapper sections are eliminated.

**Delta:** -30 tokens (two section headers + two pointer sentences removed; inlined content replaces them at different locations in the body).

---

## Restructure

### R1. Place inlined sections logically in body

The new "## Why This Works" section (compressed theory.md) goes immediately after "## Why Theatrical Oaths Fail" -- it extends the theoretical grounding before the protocol begins. This follows the ordering-guide.md pattern: Context/Background before Rules/Workflow.

The new "## Project Configuration" section (compressed configuration.md) goes at the end, after the Example section and before any closing matter. Configuration is reference material, not core workflow.

**Citation:** ordering-guide.md "Agent/Skill System Prompt" pattern (Role -> Context -> Constraints -> Workflow -> Output -> Error handling).

**Delta:** 0 tokens (placement only).

---

## Strengthen

### S1. Operationalize verification loop

D4 (high priority, CLR-4): The verification loop is described conceptually ("silently verify alignment") but never operationalized.

**Action:** Add concrete 3-line protocol under step 3:

```
Before each response, check against each principle:
- Alignment confirmed: proceed
- Tension detected: quote the specific principle, state the conflict, offer refuse/modify/acknowledge
```

**Citation:** D4 recommendation 1 (lines 178-193).

**Delta:** +25 tokens. Justified: D2 core point 3 (verification loop) is under-specified for execution.

### S2. Add internal-contradiction edge case

D4 (medium priority, AP-OUT-03): No guidance for manifesto with contradictory principles.

**Action:** Add one line to "Extract and Confirm" step: "If the manifesto contains contradictory principles, request disambiguation priority from the user."

**Citation:** D4 recommendation 2 (line 199).

**Delta:** +12 tokens.

---

## Projected Token Delta

| Category | Tokens |
|---|---|
| Baseline SKILL.md | 1058 |
| Inline: theory.md compressed | +250 |
| Inline: configuration.md compressed | +180 |
| Cut: description compression (C1) | -15 |
| Cut: redundant opening (C2) | -20 |
| Cut: template wordiness (C3) | -2 |
| Cut: passive to active (C4) | +3 |
| Cut: degradation rewrite (C5) | +5 |
| Cut: remove ref pointer sections (C6) | -30 |
| Strengthen: verification loop (S1) | +25 |
| Strengthen: contradiction edge case (S2) | +12 |
| **Projected SKILL.md total** | **~1466** |

### Net token comparison vs body+refs total

| Metric | Before | After |
|---|---|---|
| SKILL.md body | 1058 | ~1466 |
| theory.md (separate file) | 1111 | 0 (deleted) |
| configuration.md (separate file) | 740 | 0 (deleted) |
| **Total tokens** | **2909** | **~1466** |
| **Net reduction** | -- | **-1443 (-49.6%)** |

### Why this is the right trade

The previous synthesis preserved refs as lazy-loaded separate files under the premise that Claude would read them when needed. The directive overrides this: models ignore references in practice. Content that matters must be in the body.

By compressing theory.md from 1111t to ~250t and configuration.md from 740t to ~180t, the load-bearing content survives while the academic apparatus, redundant tables, and verbose examples are discarded. The SKILL.md body grows by ~408 tokens but the total token footprint drops by 1443 tokens.

The `@` syntax problem (eager loading) is also eliminated since there are no more reference files to point to.

Additionally: the previous synthesis's highest-impact fix was changing `@references/file.md` to `[label](references/file.md)` to prevent eager loading. That fix is now moot -- inlining eliminates both the pointer syntax and the files themselves.
