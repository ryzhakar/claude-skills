# Reference Optionality Analysis: qa-orchestration

## Unit: qa-orchestration

## Analysis Date: 2026-04-13

## References Analyzed: 9

---

## ESSENTIAL References (3)

These references define core workflow vocabulary, decision thresholds, or structural requirements that the skill cannot execute correctly without at activation time.

### 1. file-protocol.md

**Rationale:** The skill's entire execution model depends on file-based agent communication. The orchestrator MUST know:
- Which files to check for agent completion (`.playwright/orchestrator-status.json`)
- Where to write phase markers (`.claude/qa-phase.txt`)
- What artifacts to verify in the planner completeness check (5 required files)
- Directory structure for parallel healing dispatch (`.playwright/healed/{test-name}.json`)

Without this reference, the orchestrator cannot:
- Read agent status correctly (wrong file paths)
- Implement session resumption (wrong phase marker location)
- Verify planner completeness (missing artifact list)
- Route healer outputs (wrong parallel mode file structure)

**Evidence from SKILL.md:**
- Line 95: "verify all 5 required artifacts exist" — artifact list comes from file-protocol.md
- Line 120: "read `.playwright/orchestrator-status.json` and branch" — file path defined in file-protocol.md
- Line 144: "Write single-item input files to `.playwright/healed/{test-name}-input.json`" — parallel mode structure from file-protocol.md

**Inline Location:** Immediately after "## Dependencies" section, before "## Quality Gates"

---

### 2. confidence-scoring.md

**Rationale:** The skill's healing routing logic (Phase 4, lines 150-152) depends on specific confidence thresholds:
- HIGH (>=0.85) → auto-merge PR
- MEDIUM (0.60-0.84) → review PR
- LOW (<0.60) → defer

The orchestrator cannot route healing results without these thresholds. The skill text says "Route by confidence" but does not define what "HIGH", "MEDIUM", or "LOW" mean numerically.

Additionally, the hard rejection rules (line 152 references them) are essential for preventing false positives:
- Assertion failures → score 0.0
- Runtime errors → score 0.0
- Console fatal errors → score 0.0
- No candidate element → score 0.0
- Mass failure cluster (>10 tests) → score 0.0

**Evidence from SKILL.md:**
- Line 152: "Route by confidence: HIGH (>=0.85) → consolidated auto-merge PR. MEDIUM (0.60-0.84) → review PR. LOW (<0.60) → no PR, record as deferred."
- This exact threshold definition appears only in confidence-scoring.md

**Inline Location:** Within "## Phase 4: HEAL", subsection "### Aggregate and Route", before the routing table

---

### 3. failure-heuristics.md

**Rationale:** The skill's failure routing (Phase 3, lines 126-132) requires the six-category taxonomy to make branching decisions:
- Locator failures → proceed to Phase 4 (Heal)
- Timing failures with test structure issues → re-dispatch generator in fix mode
- Data/assertion failures → NEVER heal

The orchestrator must distinguish between these categories to route correctly. The skill references this taxonomy but does not define it.

**Critical decision point (line 130):** "timing failures where locators are correct but test structure is wrong (serial execution of independent tests, missing waits, fixture teardown races) → re-dispatch generator-agent in fix mode"

This decision cannot be made without the failure classification regex patterns from failure-heuristics.md.

**Evidence from SKILL.md:**
- Line 128: "DONE with locator failures → proceed to Phase 4 (Heal)"
- Line 130: "DONE with timing failures where locators are correct but test structure is wrong → re-dispatch generator-agent in fix mode"
- The distinction between "healable locator failure" and "timing failure requiring generator fix" comes entirely from failure-heuristics.md

**Inline Location:** Within "## Phase 3: EXECUTE", subsection "### Failure Routing", before the routing bullets

---

## DEFERRABLE References (6)

These references provide implementation details, optional patterns, or context that can be loaded conditionally when specific workflow conditions are met.

### 4. cicd-workflow.md

**Classification:** DEFERRABLE

**Loading Gate:** IF healing results exist (`.healing-results.json` written) AND confidence routing requires PR creation, THEN read `/Users/ryzhakar/pp/claude-skills/qa-automation/references/cicd-workflow.md`

**Gate Location:** Phase 4 (HEAL), subsection "### Aggregate and Route", step 2

**Rationale:** This reference contains PR creation implementation details (GitHub Actions workflow YAML, circuit breaker schema, PR body templates). The orchestrator does not create PRs itself — it delegates this to healer-agent or CI/CD automation. The reference is only needed when the orchestrator must provide PR creation instructions to the healer.

The skill already summarizes the circuit breaker rules inline (line 155: "Max 2 healing attempts per test, max 3 PRs per session"). The full YAML is reference material, not execution-critical.

**Deferred Context:** When HIGH or MEDIUM confidence healing results exist and the orchestrator needs to instruct the healer on PR creation format.

---

### 5. mcp-tools.md

**Classification:** DEFERRABLE

**Loading Gate:** IF planner-agent or generator-agent reports NEEDS_CONTEXT for browser exploration, THEN read `/Users/ryzhakar/pp/claude-skills/qa-automation/references/mcp-tools.md`

**Gate Location:** Phase 1 (PLAN), line 93: "NEEDS_CONTEXT → surface the blocker field to the user, re-dispatch once after input"

**Rationale:** MCP tools are conditional tooling. The skill says "pass to agents as dispatch context" (line 48), but the orchestrator does not need to know MCP tool details unless an agent explicitly requests them.

The reference contains tool selection logic (CLI vs MCP decision tree, tool parameters, workflow examples) that agents need, not the orchestrator. The orchestrator only needs to know that this reference exists and when to surface it.

**Deferred Context:** When planner or generator needs browser exploration guidance and requests it via NEEDS_CONTEXT status.

---

### 6. multi-app-patterns.md

**Classification:** DEFERRABLE

**Loading Gate:** IF multiple base URLs detected in user input OR project-config.md lists multiple apps, THEN read `/Users/ryzhakar/pp/claude-skills/qa-automation/references/multi-app-patterns.md`

**Gate Location:** Prerequisites Check, immediately after "Base URL known" (line 83)

**Rationale:** The skill explicitly gates this reference: "load when multiple base URLs detected" (line 49). Multi-app mode is a specialized pattern, not the default workflow.

The reference contains:
- Dual-context fixture patterns
- Comparison-as-findings pattern
- Finding taxonomy (MATCH/MISMATCH/MISSING/EXTRA)

These patterns are only needed when the orchestrator detects multi-app mode. Single-app sessions (the default) do not require this reference.

**Deferred Context:** When prerequisites check detects multiple base URLs or when the test plan indicates comparison testing.

---

### 7. seed-file-spec.md

**Classification:** DEFERRABLE

**Loading Gate:** IF seed file check fails (line 81: "If missing, STOP"), THEN read `/Users/ryzhakar/pp/claude-skills/qa-automation/references/seed-file-spec.md` to construct user-facing error message with template

**Gate Location:** Prerequisites Check, step 1

**Rationale:** The orchestrator only needs to know:
1. Check `tests/seed.spec.ts` exists
2. If missing, tell the user it's required

The full seed file specification (template code, quality attributes, multi-seed strategy) is educational material for the user, not operational knowledge for the orchestrator.

The skill already says: "If missing, STOP. Tell the user a seed file is required (see @references/seed-file-spec.md for the template)."

This is a deferred read — the orchestrator surfaces the reference to the user when needed, rather than inlining the template.

**Deferred Context:** When seed file check fails and orchestrator needs to provide the user with a template for creating one.

---

### 8. locator-strategy.md

**Classification:** DEFERRABLE

**Loading Gate:** IF planner-agent produces `.playwright/selector-strategy.md` with browser-specific flags OR executor detects browser-specific failures, THEN read `/Users/ryzhakar/pp/claude-skills/qa-automation/references/locator-strategy.md`

**Gate Location:** Phase 3 (EXECUTE), within "### Failure Routing", after locator failure detection

**Rationale:** The orchestrator does not select locators — agents do. The orchestrator only needs to know:
- Locator failures exist (from executor classification)
- Route them to healer

The detailed locator decision tree (safe roles, shadow DOM handling, cross-browser matrix) is agent context, not orchestrator context.

The skill references this indirectly via agent instructions but does not require it for orchestration decisions.

**Deferred Context:** When executor reports browser-specific locator failures or when healer needs cross-browser safety guidance.

---

### 9. ten-tier-algorithm.md

**Classification:** DEFERRABLE

**Loading Gate:** IF healer-agent is dispatched (Phase 4, line 143), THEN read `/Users/ryzhakar/pp/claude-skills/qa-automation/references/ten-tier-algorithm.md`

**Gate Location:** Phase 4 (HEAL), subsection "### Dispatch", before healer launch

**Rationale:** The orchestrator does not execute the ten-tier algorithm — healer-agent does. The orchestrator only needs to know:
- When to dispatch healer (locator failures exist)
- How to dispatch healer (single vs parallel fan-out)

The full ten-tier implementation (TypeScript code, LocatorCache, DOMExtractor, SmartFind) is healer execution context, not orchestrator routing logic.

The skill references the algorithm abstractly ("applies ten-tier locator algorithm" line 36) but does not require the implementation details for orchestration.

**Deferred Context:** When healer-agent is dispatched and needs the algorithm implementation to execute healing.

---

## Summary

| Reference | Classification | Inline? | Gate Condition |
|-----------|---------------|---------|----------------|
| file-protocol.md | ESSENTIAL | Yes | N/A — always required |
| confidence-scoring.md | ESSENTIAL | Yes | N/A — routing thresholds needed at Phase 4 |
| failure-heuristics.md | ESSENTIAL | Yes | N/A — category taxonomy needed at Phase 3 |
| cicd-workflow.md | DEFERRABLE | No | Healing results exist AND PR creation required |
| mcp-tools.md | DEFERRABLE | No | Agent reports NEEDS_CONTEXT for browser exploration |
| multi-app-patterns.md | DEFERRABLE | No | Multiple base URLs detected |
| seed-file-spec.md | DEFERRABLE | No | Seed file check fails |
| locator-strategy.md | DEFERRABLE | No | Browser-specific locator failures detected |
| ten-tier-algorithm.md | DEFERRABLE | No | Healer-agent dispatched |

---

## Deferred Read Implementation Pattern

For all DEFERRABLE references, the skill should include an explicit conditional read instruction at the gate location:

```markdown
IF [condition]:
  READ /Users/ryzhakar/pp/claude-skills/qa-automation/references/[filename].md
  THEN [use information for specific decision]
```

Example for multi-app-patterns.md at Prerequisites Check:

```markdown
2. **Base URL known:** Extract from the user's argument, or check `.playwright/project-config.md`. If neither exists, ask the user.

   IF multiple base URLs detected:
     READ /Users/ryzhakar/pp/claude-skills/qa-automation/references/multi-app-patterns.md
     THEN include dual-context fixture instructions in planner-agent dispatch
```

This pattern makes ignoring the reference IMPOSSIBLE when the condition is met, satisfying the analysis requirement.
