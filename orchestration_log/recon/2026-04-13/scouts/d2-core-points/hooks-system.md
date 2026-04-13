# Manifesto Hooks System - Core Points

## Iteration 1

**Point**: The hooks system treats context compaction as a destructive event that requires full manifesto re-binding because behavioral context does not survive compaction.

**Evidence**:
- `post-compact.sh:24` — "Re-load each manifesto's full text and re-apply the manifesto-oath skill. Previous bindings did not survive compaction. This is non-negotiable."
- `post-compact.sh:17` — "MANIFESTO RE-BINDING REQUIRED — context was just compacted."
- `hooks.json:16-25` — PostCompact hook has universal matcher "*", ensuring re-binding runs after every compaction event

## Iteration 2

**Point**: The system enforces two-tiered manifesto injection: full ceremony for main sessions (SessionStart), lightweight awareness for subagents (SubagentStart).

**Evidence**:
- `session-start.sh:24` — "Apply the manifesto-oath skill (operational identity assumption, not theatrical oath)" - full binding for main session
- `subagent-start.sh:22` — "You are not required to perform the full oath ceremony. But be aware of these principles and let them inform your work." - lightweight for subagents
- `hooks.json:4-14, 28-38` — SessionStart and SubagentStart hooks configured separately with different scripts

## Iteration 3

**Point**: Manifesto discovery supports three resolution modes (plain name keyword match, URL fetch, local path read) to accommodate manifestos from multiple sources.

**Evidence**:
- `session-start.sh:9-12` — "Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword / URL (starts with http): fetch the full text / Local path (starts with ./ or /): read relative to ${PROJECT_DIR}"
- `post-compact.sh:9-12` — Same three-mode resolution instructions repeated verbatim in post-compact hook
- `ensure-repo.sh:17-27` — detect_manifestos() checks both `.manifestos.yaml` and `CLAUDE.md` Active Manifestos section

## Iteration 4

**Point**: The system uses lazy repository cloning to ensure manifesto source availability without blocking hook execution if the clone fails.

**Evidence**:
- `ensure-repo.sh:8-11` — "if [ ! -d "$MANIFESTO_DIR/manifestos" ]; then ... git clone --depth 1 --quiet "$MANIFESTO_REPO" "$MANIFESTO_DIR" 2>/dev/null || true"
- `ensure-repo.sh:10` — `|| true` ensures clone failure does not fail the hook
- `hooks.json:11,23,34` — All hooks have 10-30 second timeouts but lazy clone runs asynchronously without blocking

## Iteration 5

**Point**: The system delegates manifesto recommendation to subagents when no configuration exists, rather than imposing defaults or failing silently.

**Evidence**:
- `session-start.sh:32` — "Delegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, (3) recommend which manifestos are relevant. Then ask the user whether to bind them."
- `session-start.sh:14-26` — Explicit bifurcation: if manifestos declared, load them; if not, delegate recommendation
- `subagent-start.sh:9-12` — "if [ -z "$manifestos" ]; then exit 0" - subagents only inject if manifestos are already declared, avoiding recursive recommendation

## Rank Summary

1. Compaction requires re-binding (most emphatic, repeated as "non-negotiable")
2. Two-tiered injection (main vs subagent) (pervasive across all hook scripts)
3. Three-mode resolution (plain/URL/path) (explicit in multiple locations)
4. Lazy clone with failure tolerance (foundational infrastructure pattern)
5. Subagent-delegated recommendation (workflow design, less emphatic than others)
