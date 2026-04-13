# Strunk Analysis: Manifesto Hooks System Prose

Analysis of prose quality in manifesto hooks system against Strunk's Elements of Style (Rules 10, 11, 12, 13, 15, 18).

Files analyzed:
- `/Users/ryzhakar/pp/claude-skills/manifesto/hooks/hooks.json`
- `/Users/ryzhakar/pp/claude-skills/manifesto/hooks/session-start.sh`
- `/Users/ryzhakar/pp/claude-skills/manifesto/hooks/subagent-start.sh`
- `/Users/ryzhakar/pp/claude-skills/manifesto/hooks/ensure-repo.sh`
- `/Users/ryzhakar/pp/claude-skills/manifesto/hooks/post-compact.sh`

---

## Critical & Severe

### R10 (Active Voice) - Severity: Severe

**session-start.sh line 24:**
> "Load each manifesto's full text. Apply the manifesto-oath skill (operational identity assumption, not theatrical oath). **For multiple manifestos, map their interdependence graph.**"

**Issue:** Passive construction with implied agent. "Be mapped" is understood but suppressed. While imperative mood typically uses active voice, this phrasing feels indirect.

**Fix:** "For multiple manifestos, map their interdependence graph." → Already imperative/active. Actually acceptable. **RETRACTED - NOT A VIOLATION.**

**session-start.sh line 17:**
> "MANIFESTO INITIALIZATION REQUIRED."

**Analysis:** Passive construction ("is required" suppressed). However, this follows the pattern of status announcements where agent is irrelevant (system state, not actor). Per R10's "agent_unknown_or_irrelevant" exception, **ACCEPTABLE**.

**subagent-start.sh line 22:**
> "You are not required to perform the full oath ceremony."

**Issue:** Passive voice "are required." The agent (system/protocol) is suppressed.

**Fix:** "The system does not require you to perform the full oath ceremony." OR more direct: "Skip the full oath ceremony."

**Severity verdict:** Moderate, not severe - the meaning is clear and the passive maintains appropriate impersonal register.

### R12 (Concrete/Specific/Definite) - Severity: Severe

**session-start.sh line 20:**
> "Declared manifestos:"

**Issue:** "Declared" is vague - declared by whom? When? How? The reader must infer "declared in your project configuration."

**Fix:** "Manifestos configured in your project:"

**session-start.sh line 32:**
> "Delegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, (3) recommend which manifestos are relevant."

**Issue:** "briefly explore" is vague. What constitutes "brief"? What depth?

**Fix:** "Delegate a subagent to: (1) scan the project's primary language, domain, and coding conventions (5-10 files maximum)..."

**Mitigation:** The parenthetical "(language, domain, conventions)" provides partial specificity. **Moderate severity.**

**post-compact.sh line 24:**
> "Previous bindings did not survive compaction. **This is non-negotiable.**"

**Issue:** "This" is abstract - what exactly is non-negotiable? The re-loading? The application? The fact that bindings didn't survive?

**Fix:** "Previous bindings did not survive compaction. Re-binding is non-negotiable." OR "You must re-bind. This is non-negotiable."

**subagent-start.sh line 16:**
> "MANIFESTO CONTEXT: This project operates under these manifesto bindings:"

**Issue:** "operates under" is abstract. What does it mean for a project to "operate under" a manifesto?

**Fix:** "MANIFESTO CONTEXT: This project enforces these manifesto principles:" OR "...follows these manifestos:"

---

## Moderate

### R11 (Positive Form) - Severity: Moderate

**session-start.sh line 24:**
> "Apply the manifesto-oath skill (operational identity assumption, **not theatrical oath**)."

**Issue:** States what it is NOT rather than what it IS. Reader must negate "not theatrical" to understand "serious/operational."

**Fix:** "Apply the manifesto-oath skill (operational identity assumption via behavioral binding)."

**Severity:** Moderate. The positive term "operational identity assumption" is present, so "not theatrical oath" serves as antithesis (legitimate use per R11's "strong_negatives"). However, could be strengthened.

**subagent-start.sh line 22:**
> "You are **not required** to perform the full oath ceremony."

**Issue:** Negative construction. Tells what agent should NOT do, not what they SHOULD do.

**Fix:** "You may skip the full oath ceremony." OR "Awareness of these principles suffices; omit the full oath ceremony."

**session-start.sh line 28:**
> "MANIFESTO PLUGIN ACTIVE — **no manifesto configuration found** (.manifestos.yaml or Active Manifestos section in CLAUDE.md)."

**Issue:** "no manifesto configuration found" is negative - tells what ISN'T there.

**Fix:** "MANIFESTO PLUGIN ACTIVE — awaiting manifesto configuration (.manifestos.yaml or Active Manifestos section in CLAUDE.md missing)." 

**Better:** "MANIFESTO PLUGIN ACTIVE — configure manifestos via .manifestos.yaml or CLAUDE.md 'Active Manifestos' section."

### R13 (Omit Needless Words) - Severity: Moderate

**session-start.sh lines 9-12:**
> "To resolve each entry:
> - Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword
> - URL (starts with http): fetch the full text
> - Local path (starts with ./ or /): read relative to ${PROJECT_DIR}"

**Issue:** "starts with http" is wordy. Could be "http URLs."

**Fix:**
> "To resolve each entry:
> - Plain name (e.g. 'decomplect'): find in ${MANIFESTO_DIR}/manifestos/ by keyword
> - URL (http/https): fetch full text
> - Local path (./ or /): read from ${PROJECT_DIR}"

**Reduction:** Removes redundant "the" and "matching file", condenses URL description.

**session-start.sh line 17:**
> "MANIFESTO INITIALIZATION REQUIRED."

vs. line 17 in post-compact.sh:
> "MANIFESTO RE-BINDING REQUIRED — context was just compacted."

**Issue:** "REQUIRED" is emphatic but could be more directive. Headers are commands, not status reports.

**Alternative:** "INITIALIZE MANIFESTOS" / "RE-BIND MANIFESTOS AFTER COMPACTION"

**Mitigation:** Caps-lock headers serve as visual anchors; brevity acceptable. Not a clear violation.

**session-start.sh line 32:**
> "Delegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, (3) recommend which manifestos are relevant."

**Issue:** "the available manifesto files in" is wordy. "Available" is implied; "files in" is redundant with path.

**Fix:** "...(2) read manifestos from ${MANIFESTO_DIR}/manifestos/, (3)..."

**post-compact.sh line 28:**
> "MANIFESTO PLUGIN ACTIVE — context was just compacted. If manifestos were previously bound, re-apply the manifesto-oath skill."

**Issue:** "If manifestos were previously bound" - reader must infer conditional from history.

**Fix:** "MANIFESTO PLUGIN ACTIVE — context compacted. Re-apply manifesto-oath skill if needed."

**Better:** Ambiguous whether this matters - unclear if user needs this guidance. Possibly delete entire else-clause.

### R15 (Parallel Construction) - Severity: Moderate

**session-start.sh lines 9-12:**
> "To resolve each entry:
> - Plain name (e.g. 'decomplect'): **find** the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword
> - URL (starts with http): **fetch** the full text
> - Local path (starts with ./ or /): **read** relative to ${PROJECT_DIR}"

**Issue:** Verbs are all different (find/fetch/read), but all describe the same ACTION (retrieval). Lack of parallel form obscures functional similarity.

**Fix:**
> "To resolve each entry:
> - Plain name (e.g. 'decomplect'): **load** by keyword from ${MANIFESTO_DIR}/manifestos/
> - URL (starts with http): **load** from web
> - Local path (starts with ./ or /): **load** from ${PROJECT_DIR}"

**Alternative:** Keep verb variety if methods truly differ, but ensure grammatical parallelism:
> "- Plain name: **finding** file in ${MANIFESTO_DIR}/manifestos/ by keyword
> - URL: **fetching** full text from web
> - Local path: **reading** from ${PROJECT_DIR}"

**Severity:** Moderate - the instructions are comprehensible, but parallel structure would enhance scannability.

---

## Minor & Stylistic

### R18 (Emphatic Position) - Severity: Moderate

**session-start.sh line 24:**
> "Load each manifesto's full text. Apply the manifesto-oath skill (operational identity assumption, not theatrical oath). **For multiple manifestos, map their interdependence graph.**"

**Issue:** Final sentence ends with "interdependence graph" - technical term but not the emphatic point. The POINT is "map the relationships between them."

**Analysis:** "Interdependence graph" is precise and emphatic enough. The technical term carries weight. **ACCEPTABLE**.

**session-start.sh line 32:**
> "Delegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, **(3) recommend which manifestos are relevant. Then ask the user whether to bind them.**"

**Issue:** Final clause "Then ask the user whether to bind them" is emphatic by position but ends weakly with pronoun "them."

**Fix:** "...(3) recommend relevant manifestos, then ask the user whether to bind those recommendations."

**Better:** "...(3) recommend relevant manifestos and request user approval for binding."

**post-compact.sh line 24:**
> "Re-load each manifesto's full text and re-apply the manifesto-oath skill. Previous bindings did not survive compaction. **This is non-negotiable.**"

**Analysis:** "This is non-negotiable" receives emphatic final position. Strong closure. **GOOD**.

**subagent-start.sh line 22:**
> "You are not required to perform the full oath ceremony. But be aware of these principles and let them inform your work. **If you need the full text, read from the paths above or fetch URLs.**"

**Issue:** Ends with "fetch URLs" - weak, procedural. The emphatic point should be "these principles inform your work."

**Fix:** Reorder: "If you need full text, read from the paths above or fetch URLs. But be aware of these principles and let them inform your work." (Ends with "work" - the goal.)

**Better:** "You are not required to perform the full oath ceremony, but let these principles inform your work. If you need full text, read from the paths above or fetch URLs."

### R10 (Active Voice) - Additional observations

**hooks.json line 2:**
> "Manifesto lifecycle: initialization, re-binding after compaction, subagent injection"

**Analysis:** Noun string, no verb. Acceptable for metadata description field. Not prose. **NOT APPLICABLE**.

**session-start.sh line 28:**
> "no manifesto configuration found"

**Issue:** Passive "found" with suppressed agent. However, this is standard system-message idiom ("file not found"). **ACCEPTABLE per convention**.

### R12 (Concrete/Specific/Definite) - Additional observations

**session-start.sh line 30:**
> "Repo manifestos available in: ${MANIFESTO_DIR}/manifestos/"

**Analysis:** "Repo manifestos" - vague category. What are "repo manifestos" vs. project manifestos?

**Fix:** "Available manifestos in repository:" OR "Manifesto library:"

**Severity:** Minor - context makes meaning clear enough.

---

## Summary

### High-priority issues (Severe)

1. **R12 violations (vague language):**
   - "Declared manifestos" → "Manifestos configured in your project"
   - "This is non-negotiable" → "Re-binding is non-negotiable" (specify referent)
   - "operates under these manifesto bindings" → "enforces/follows these manifestos"

### Medium-priority issues (Moderate)

2. **R11 violations (negative constructions):**
   - "not theatrical oath" → strengthen positive alternative or justify as antithesis
   - "You are not required" → "You may skip" or "Awareness suffices; omit..."
   - "no manifesto configuration found" → "configure manifestos via..."

3. **R13 violations (needless words):**
   - "the available manifesto files in" → "manifestos from"
   - "starts with http" → "http/https URLs"
   - "find the matching file in...by keyword" → "find in...by keyword"

4. **R15 violations (parallel construction):**
   - Resolution instructions use different verbs (find/fetch/read) for parallel actions → unify to "load" or ensure grammatical parallelism

### Low-priority issues (Minor/Stylistic)

5. **R18 violations (emphatic position):**
   - "Then ask the user whether to bind them" → ends with weak pronoun
   - subagent-start.sh ending sequence could reorder for stronger close

### Strengths

- **Active voice:** Most instructions use imperative mood correctly (R10)
- **Economy:** Headers are appropriately terse (R13)
- **Emphatic closings:** "This is non-negotiable" is strong final positioning (R18)
- **Clarity:** Despite moderate violations, instructions are comprehensible

### Recommended fixes priority

1. **Critical:** Resolve R12 vague referents ("This", "Declared", "operates under")
2. **Important:** Convert negative constructions to positive (R11)
3. **Polish:** Parallel construction in resolution instructions (R15), remove needless words (R13)
4. **Optional:** Reorder sentences for emphatic endings (R18)

The prose is functional but could achieve greater clarity and vigor through systematic application of Strunk's principles, particularly R12 (concrete language) and R11 (positive form).
