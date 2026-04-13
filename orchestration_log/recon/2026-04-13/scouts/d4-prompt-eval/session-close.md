# Prompt Evaluation: session-close

**Unit Type:** Skill (Claude Code Agent)
**Evaluated:** 2026-04-13
**File:** /Users/ryzhakar/pp/claude-skills/orchestration/skills/session-close/SKILL.md

---

## Overall Score: 88/100 (Good, approaching Excellent)

Excellent workflow definition with numbered steps, clear agent dispatch patterns, and concrete data schema references. Best structural compliance of the four skills evaluated.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- EXAMPLES ✓ (minimal but present)
- TOOLS ✓ (mentions specific tools and files)
- REASONING ✗ (not a reasoning-focused task)
- DATA_SEPARATION ✓ (handles session data from disk)
- AGENT_SPECIFIC ✓

---

## Critical Issues (MUST/MUST_NOT violations)

### MUST Violations

None detected. The skill has:
- Clear task definition ("Governs the LEAVE protocol")
- Explicit workflow (8 numbered steps)
- Agent-specific workflow with model tier assignments
- All required frontmatter fields

### MUST_NOT Violations

1. **CLR-2: Contains undefined vague terms (minimal)**
   - "appropriate" appears implicitly but usage is clear from context
   - "major phases" (line 147) - not quantified but context makes it reasonably clear
   - This is borderline - the terms are used sparingly and context disambiguates
   - Impact: -1.5 points (partial violation - terms present but minimally harmful)

2. **DAT-2: Instructions mixed with data schema without clear boundaries**
   - Lines 33-41 describe JSONL structure inline without tags
   - Should be wrapped in `<data_schema>` tags or similar
   - The schema is referenced from disk (references/data-schema.md) but also described inline
   - Mild violation - the mixing is limited and doesn't cause confusion
   - Impact: -1.5 points (partial violation)

---

## Warnings (SHOULD violations)

1. **STR-5: Ordering is good but could be optimized**
   - Current: Core Principle → Session Data on Disk → LEAVE Protocol (8 steps) → Backlinking → Quality Gates → Additional Resources
   - This is actually close to ideal ordering for a procedural skill
   - Lost: 0 points (ordering is functional)

2. **OUT-6: Doesn't state what to exclude (minor)**
   - No "skip preamble" guidance for agent outputs
   - However, the numbered steps are specific enough that this is implicit
   - Lost: +0.5 points

3. **CLR-4: Success criteria present**
   - "Quality Gates" section (lines 144-154) provides success criteria
   - This is well-done
   - Gained: +1 point

4. **EXM-1: Examples not wrapped in tags**
   - Lines 54-56 show git commands as examples
   - Lines 105-107 show git commands
   - Line 132 shows session record header format
   - These are implicit examples without `<example>` tags
   - Lost: +0.5 points

---

## Anti-Patterns Detected

1. **AP-CLR-02: Undefined qualifiers (minimal)** (Low severity)
   - "major phases" without quantification
   - Very minor instance
   - Maps to CLR-2 partial violation

2. **AP-STR-02: Instruction-data mixing (mild)** (Medium severity)
   - Session data schema described inline (lines 33-41) without clear boundaries
   - Maps to DAT-2 violation

---

## Strengths

1. **Exceptional workflow clarity**
   - 8 numbered steps with clear dependencies (lines 42-127)
   - Steps 1-4 run in parallel, Step 5 is orchestrator-only, Steps 6-8 are sequential
   - Model tier assigned to each step (haiku background, sonnet background, orchestrator)
   - This is the clearest procedural workflow of all four skills evaluated

2. **Strong data schema integration**
   - "Session Data on Disk" section (lines 18-41) provides exact file paths
   - JSONL field descriptions with concrete field names
   - References external schema file (references/data-schema.md) for full details
   - Shows actual directory structure (~/.claude-shared/projects/...)

3. **Good agent dispatch patterns**
   - Each step specifies model tier and run mode (background vs. foreground)
   - Step 1: "haiku agent" with background mode
   - Step 2: "haiku agent" with background mode
   - Step 3: "sonnet agent" with background mode
   - Step 4: "sonnet agent" with background mode
   - Step 5: "orchestrator" (no delegation)
   - Step 6: "haiku agent"
   - Step 7: "orchestrator" (with /cost command)
   - Step 8: note only (no agent)

4. **Core principle clearly stated**
   - Lines 9-15: "The orchestrator holds context no agent can reconstruct"
   - Justifies why Step 5 cannot be delegated
   - Strong conceptual grounding

5. **Quality gates**
   - Checklist with 7 items (lines 146-153)
   - Concrete and verifiable
   - Includes negative check (recon files NOT committed)

6. **Backlinking convention**
   - Lines 129-142 show exact session record header format
   - Explains traceability to raw JSONL files
   - Good institutional memory design

7. **Tool integration**
   - References specific scripts (scripts/extract_metrics.py)
   - References /cost command
   - Shows git commands with exact flags
   - Tool usage is concrete, not abstract

8. **Example commands**
   - Lines 54-56: git log commands with exact format strings
   - Lines 105-107: git add/commit with message template
   - These are actionable and copy-pasteable

9. **Good frontmatter**
   - Clear trigger phrases
   - Version field included (1.0.0)
   - Description includes use cases

10. **References section**
    - Lines 156-159 list 3 external references
    - Each reference has a clear purpose description
    - Format: **`filename`** — description

11. **Scope boundaries clear**
    - Step 8 explicitly states recon/ is gitignored (line 122)
    - Step 7 shows exactly where to fill placeholders (lines 113-119)

12. **Error prevention**
    - Step 5 warns: "This step cannot be delegated" (line 98)
    - Step 4 instructs: "agent must read actual code — not guess" (line 87)
    - These prevent common failure modes

---

## Recommendations

### High Priority (Fix violations)

1. **Wrap data schema in tags**
   ```markdown
   ## Session Data on Disk
   
   Claude Code stores structured session data at:
   
   <data_schema>
   ~/.claude-shared/projects/{project-slug}/
     {session-id}.jsonl          — main conversation (orchestrator turns)
     {session-id}/
       subagents/
         agent-{id}.jsonl        — per-agent conversation
         agent-{id}.meta.json    — agent metadata
       tool-results/             — persisted tool outputs
   
   Each JSONL line is a JSON object with:
   - `message.model` — model used
   - `message.content[]` — array of text/tool_use/tool_result blocks
   - `message.usage` — token counts: input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens
   - `agentId` — identifies which agent produced the message
   - `timestamp` — ISO 8601
   </data_schema>
   
   See `references/data-schema.md` for full field reference and parsing patterns.
   ```

2. **Wrap examples in tags**
   ```markdown
   <example>
   Commands to run:
   - `git log --format="%ai %H %s" --since="{session-start-date}" --reverse`
   - `git diff --stat {first-session-commit}..HEAD`
   </example>
   ```

3. **Define "major phases"**
   - Line 147: "Session record covers all major phases"
   - Replace with: "Session record covers all phases that changed code, updated docs, or made architectural decisions (including failures)"

### Medium Priority (Improve compliance)

4. **Add exclusion guidance**
   ```markdown
   ## Agent Output Guidance
   
   For all agents dispatched in this protocol:
   - Skip preambles ("Here's the session record draft...")
   - Lead with the artifact (start with markdown header)
   - No sign-offs or meta-commentary
   ```

5. **Make parallelism more explicit in Step heading**
   - Current: "Step 1: Extract session metrics (haiku, background)"
   - Better: "Steps 1-4 (run in parallel):"
   - This makes the parallel execution pattern more visible

### Low Priority (Polish)

6. **Add timing estimates**
   - Step 1-4: "Background, ~60-90 seconds each"
   - Step 5: "Orchestrator, ~5-10 minutes"
   - This helps set expectations

7. **Add failure handling**
   - What if a background agent fails?
   - "If Step 1-4 agents fail: re-dispatch with error message included. If failure persists, execute that step manually."

8. **Cross-reference parent protocols**
   - The skill mentions "LEAVE protocol" but could reference where ARRIVE and WORK are defined
   - Add: "For the full ARRIVE/WORK/LEAVE lifecycle, see agentic-delegation skill's session persistence section"

9. **Show example session record structure**
   - Lines 132-142 show header format
   - Could add a skeleton showing all sections: Header / Summary / Phases / Failures / Decisions / Artifacts / Cost

10. **Clarify project slug generation**
    - Line 23: "The project slug is the filesystem-safe form"
    - Add: "(slash → hyphen, unsafe chars stripped)"

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| STRUCTURE | 7/7 | Clear role (session close governor), excellent context (data on disk), perfect structure markers (numbered steps), explicit task definition, optimal ordering, minimal data mixing (only in schema section) |
| CLARITY | 6/7 | Minimal vague terms (partial violation), no contradictions, explicit success criteria (quality gates), excellent numbered steps |
| CONSTRAINTS | 6/6 | Clear scope (LEAVE protocol only), explicit constraints (Step 5 cannot be delegated, recon/ not committed), good rationale |
| SAFETY | 6/6 | No unsafe operations, good error prevention (warnings in steps), handles sensitive data appropriately (session logs), no unsafe access |
| OUTPUT | 5/6 | Explicit format (session record + reference docs), shows templates, handles missing data (placeholder pattern), good length guidance (implicit), minor: no exclusion list |
| EXAMPLES | 2/3 | Examples present (git commands, session header), not wrapped in tags, examples show expected output (commit messages) |
| TOOLS | 3/3 | Tools specified (git, /cost, scripts/extract_metrics.py), usage shown concretely |
| DATA_SEPARATION | 2/3 | Data schema described, mild mixing without tags, descriptive naming (~/.claude-shared/projects/{slug}) |
| AGENT_SPECIFIC | 9/10 | Excellent name/description/triggers, perfect workflow (8 steps), focused scope, tools specified, no bloat (160 lines), excellent output format, version field present, uses argument substitution pattern (YYYY-MM-DD) |

**Calculation:**
- Applicable criteria: 51 (includes EXAMPLES, TOOLS, DATA_SEPARATION)
- MUST violations: 0 points
- MUST_NOT violations: -3 points (vague terms partial + data mixing partial = -1.5 each)
- Passed SHOULD: +24 points
- Base: 24 passed criteria
- Score: (24 + 24 - 3) / 51 × 100 = 88.2

**Final: 88/100 (Good, approaching Excellent)**

Best structural compliance of the four skills. The 8-step workflow with parallel/sequential execution patterns, concrete data schema references, and quality gates represent production-grade orchestration design. Minor violations (data schema wrapping, example tags) prevent "Excellent" rating, but this is very close to production-ready.

---

## Comparison Note

Skill ranking by score:
1. **session-close** (88/100) - best workflow clarity, data schema integration, quality gates
2. **dev-orchestration** (85/100) - best phase structure, review protocol
3. **research-tree** (82/100) - best tier system, domain adaptation
4. **agentic-delegation** (78/100) - best conceptual framework but weakest structure

session-close benefits from:
- Narrow, well-defined scope (exactly 8 steps)
- Concrete data sources (JSONL files with known schema)
- Clear orchestrator vs. agent boundaries
- No open-ended exploration (unlike research) or complex state (unlike dev)

This focused scope allows it to achieve exceptional procedural clarity.
