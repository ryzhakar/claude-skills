# Synthesis: session-close

## Baseline

| Component | Tokens |
|-----------|--------|
| SKILL.md | 1,676 |
| references/data-schema.md | 989 |
| references/session-record-format.md | 876 |
| **Total system** | **3,541** |

D1 classified both references as DEFERRABLE with unambiguous loading gates tied to specific LEAVE protocol steps. The previous synthesis kept them as separate files.

**CRITICAL DIRECTIVE OVERRIDE:** Models ignore references in practice. Content not in the body does not get followed. Both references must be inlined. The three-filter survival test (genuinely rare + large after compression >1000t + unavoidable gate) determines whether either reference survives as a separate file.

**data-schema.md (989t):** Fails the survival test on "large after compression >1000t" -- it is under 1000t even before compression. Also fails "genuinely rare" -- the metric extraction agent (Step 1) runs on every session close, and the cost formulas (Step 7) run on every session close. This is the common path. Inline.

**session-record-format.md (876t):** Fails the survival test on "large after compression >1000t" -- it is under 1000t before compression. Also fails "genuinely rare" -- session record drafting (Step 3) runs on every session close. Inline.

---

## Core Points (D2 -- untouchable)

1. **Orchestrator irreplaceable context** -- agents cannot reconstruct decisions, failures, and reasoning from disk artifacts; orchestrator review is mandatory.
2. **Institutional memory production** -- combining objective metrics from disk with orchestrator context into VCS-tracked documentation.
3. **Cache-read cost dominance** -- long orchestrator contexts drive costs via cache-reading, not direct token consumption; this shapes session design.
4. **Session ID backlinking** -- traceability from frozen documentation to raw JSONL data for future correction or re-extraction.
5. **Recon vs. durable separation** -- disposable extraction artifacts (gitignored) vs. version-controlled institutional memory.

---

## Inline from References

### data-schema.md (989t) -> inline at "Session Data on Disk" section

**Before (SKILL.md lines 33-41):** Inline JSONL summary with "See references/data-schema.md for full field reference and parsing patterns" pointer, plus a second mention at Step 1 (line 57).

**After:** Replace the current inline summary AND the reference file with a single compressed schema section. The current body already has a partial duplicate (lines 33-41 describe the same fields the reference describes). Merge and compress:

- Retain the file location diagram verbatim (body already has this).
- Retain the JSONL record fields but compress: the current body gives a prose description of each field; the reference gives the JSON example. Replace both with a single compact JSON example with inline annotations. This eliminates the prose-then-JSON redundancy.
- Inline the content block types (tool_use, tool_result, Agent dispatch, text) -- these are needed for the metric extraction agent to parse correctly. Compress from 4 separate code blocks to a single annotated block.
- Inline the model tier detection function. Compress from a Python function (8 lines) to a 3-line rule: "Model tier: 'haiku' if model contains 'haiku', 'sonnet' if 'sonnet', 'opus' if 'opus'."
- Inline agent dispatch counting rule: "Count unique agentId values across all JSONL files (excluding orchestrator ID), or count Agent tool_use blocks in orchestrator JSONL."
- Inline the cost formulas. Retain the rate table verbatim (Opus/Sonnet/Haiku input/output/cache_read/cache_write per 1M tokens). Compress the compute_cost function to a formula description: "Cost = sum of (tokens / 1M * rate) for each of the four token categories per tier."
- Retain the "Cache Dominates Cost" insight verbatim (D2 core point #3 depends on it).
- Cut the "Note: /cost command gives authoritative cost" disclaimer -- the body already instructs using /cost at Step 7.

**Projected:** ~650t inlined (from 989t reference + ~200t existing body overlap removed). The body's current partial schema (lines 33-41) is replaced, not duplicated.

### session-record-format.md (876t) -> inline at Step 3 and new "Session Record Format" section

**Before (SKILL.md line 78):** "See references/session-record-format.md for required sections and format."

**After:** Inline compressed format directly into the body:

- Retain the header template verbatim (lines 8-16 of ref). Currently the body ALSO has a header template at "Backlinking Convention" (lines 129-142). These overlap -- the body's version has 7 fields, the reference's has 7 fields with slightly different formatting. Merge into one definitive template.
- Inline the required sections list: Timeline (phase-anchored to git commits), Decision Log (table: decision/context/rationale/outcome), Failure Log (table: failure/root cause/correction/prevention), Quantitative Summary (table: metric/value), Next Session Priorities. Compress each from the reference's multi-line description to a 1-2 line specification.
- Inline "What Agents Get Wrong" list (lines 93-105 of ref). Compress from 8 items with explanations to 8 items as a bulleted list without explanations. The item names are self-explanatory: "research phases (no commits)", "failed first attempts (context lost)", "conversation-driven decisions", "tool failures", "user corrections", "skipped protocol steps", "stale numbers", "guessed function signatures." The orchestrator reads these at Step 5 to know what to correct. *Citation: bridge-research/prompt-compression-strategies.md section 5.4 -- "general instructions beat prescriptive steps." The item names are general instructions; the explanations are prescriptive elaboration Claude can infer.*
- Cut "Backlinking to Raw Data" section (lines 109-118 of ref, ~80t). This restates what the body already says in the Backlinking Convention section. After merging the header templates, there is only one place this information lives.
- Cut the "Common phases agents miss" prose (lines 37-43 of ref, ~60t). The "What Agents Get Wrong" list covers the same ground in compressed form.

**Projected:** ~550t inlined (from 876t reference + ~100t existing body overlap removed via header template merge).

---

## Cut

### 1. JSONL schema description redundancy (SKILL.md lines 33-41 vs. data-schema.md)

**Before:** 9-line inline description of JSONL fields (`message.model`, `message.content[]`, `message.usage`, `agentId`, `timestamp`) with format annotations, PLUS the reference file describing the same fields with a JSON example.

**After:** A single compressed schema section replacing both. Net savings counted in the inline section above (~200t of body content removed and replaced by the compressed inline version).

**Citation:** D4-prompt-eval DAT-2 -- "Instructions mixed with data schema without clear boundaries." The merged version uses a clear structural marker.

**Token delta:** accounted in inline projection.

### 2. Step 8 restates Step 6 (SKILL.md lines 122-127)

**Before:** Step 8 "Note on recon data" is a 3-line section: "The `docs/orchestration_log/recon/` directory is gitignored -- session metrics and raw git history are disposable. They exist only to assist the session close-out. Regenerate if needed." This restates Step 6's "Do NOT commit recon/ data -- it is gitignored."

**After:** Cut Step 8 entirely. Rename to a 7-step protocol. Add "Recon data is gitignored and disposable; regenerate if needed." as a parenthetical to Step 6.

**Citation:** D3-strunk R13 finding 13 -- "Needless repetition weakening force."

**Token delta:** ~40t saved.

### 3. Step 2 project-specific commands (SKILL.md lines 63-67)

**Before:** 4 specific git/find/wc commands listed inline.

**After:** Keep the first two commands (`git log`, `git diff --stat`) which define the essential output. Cut the `find | wc -l` and `wc -l` commands -- these are project-specific codebase size measurements that belong in project context, not a generic session-close skill. The agent determines appropriate size metrics from project context.

**Citation:** Bridge-research section 1.3 -- "Only add context Claude doesn't already have."

**Token delta:** ~25t saved.

### 4. Frontmatter: remove `version` field (SKILL.md line 4)

**Before:** `version: 1.0.0` in frontmatter.

**After:** Remove. Per project instructions in CLAUDE.md: "Versions live in `plugin.json` only. Skill frontmatters do not carry version fields."

**Token delta:** ~5t saved.

### 5. Backlinking Convention standalone section (SKILL.md lines 129-142)

**Before:** Standalone section with header template, appearing between LEAVE Protocol and Quality Gates.

**After:** Merge into Step 3 subsection. The backlinking convention is a requirement for the session record header. Moving it to Step 3 places the instruction at the point of use. The header template is now the single merged version from the session-record-format inline.

**Citation:** ordering-guide.md -- "constraints should appear before or at the task they constrain, not after."

**Token delta:** ~-20t (merge eliminates the standalone section header and transition sentence; header template is now the single merged version).

---

## Restructure

### Section ordering

The current ordering is near-optimal per D4-prompt-eval (score: 88/100). Changes:

**Before:** Core Principle -> Session Data on Disk -> LEAVE Protocol (8 steps) -> Backlinking Convention -> Quality Gates -> Additional Resources

**After:**
1. **Core Principle** (unchanged)
2. **Session Data on Disk** (now with inlined data-schema.md content -- JSONL schema, content block types, model tier detection, cost formulas, cache dominance insight)
3. **Session Record Format** (new section, inlined from session-record-format.md -- header template, required sections, "What Agents Get Wrong" list)
4. **LEAVE Protocol** (7 steps, renumbered; Step 3 now includes backlinking requirement inline; Step 6 includes recon note)
5. **Quality Gates** (unchanged)
6. (no Additional Resources or References section -- all inlined)

**Citation:** ordering-guide.md -- "Context/data before workflow, output format before task."

**Token delta:** ~0t (reordering only).

---

## Strengthen

### 1. Eliminate vague terms (D4-prompt-eval CLR-2, partial violation)

| Before | After | Citation |
|--------|-------|----------|
| "major phases" (quality gate, line 147) | "all phases that changed code, updated docs, or made decisions (including failures)" | D4 CLR-2 |

**Token delta:** ~+10t.

### 2. Clarify agency (D3-strunk R10 findings 2, 3)

| Before | After |
|--------|-------|
| "Execute in this order. Steps 1-4 run in parallel." (line 44) | "The orchestrator executes in this order. Run Steps 1-4 in parallel." |
| "Brief the agent to count:" (line 50) | "Dispatch the agent with instructions to count:" |

**Citation:** D3-strunk findings 2, 3 -- "Who executes? Active voice clarifies immediately."

**Token delta:** ~+5t.

### 3. Convert negative to positive (D3-strunk R11 finding 12)

**Before (line 109):** "Do NOT commit recon/ data -- it is gitignored."

**After:** "Commit only `docs/orchestration_log/history/` and `docs/orchestration_log/reference/`. The recon/ directory is gitignored."

**Citation:** D3-strunk R11 -- "Negative instruction when positive would be clearer."

**Token delta:** ~+10t.

### 4. Standardize reference doc list parallelism (D3-strunk R15 finding 10)

**Before (lines 83-85):** First item says "read actual code (commands)," second and third use imperative verbs (add/remove, add).

**After:**
- `codebase_state.md` -- update from actual code (`grep`, `wc -l`, pytest)
- `deferred_items.md` -- add new findings, remove resolved items
- `conventions.md` -- add patterns discovered this session

**Token delta:** ~0t.

### 5. Strengthen Step 5 temporal trigger (D3-strunk R12 finding 5)

**Before (line 89-91):** "Step 5: Orchestrator review and correction (orchestrator). Read the draft session record. Correct: [list]"

**After:** "Step 5: Review and correct drafts (orchestrator, after Steps 1-4 complete). Read the draft session record. Correct: [list]"

**Citation:** D3-strunk R12 -- "Imperative without clear trigger."

**Token delta:** ~+5t.

---

## Hook/Command Splits

### Recommended: SessionEnd hook for LEAVE protocol reminder

The LEAVE protocol is the most-skipped protocol step. A `SessionEnd` hook can remind the orchestrator.

**Proposed hook:**
- Event: `SessionEnd`
- Type: `command`
- Behavior: Check if `docs/orchestration_log/history/{today}/session.md` exists. If not, print reminder: "LEAVE protocol not executed. Run /session-close before ending."

**Benefit:** Deterministic enforcement. *Citation: bridge-research/hooks-full-spec.md -- SessionEnd fires once per session; cannot block but can notify.*

**Implementation note:** This hook belongs in the plugin's `hooks/hooks.json`, not in the skill frontmatter.

**SKILL.md change:** No change to SKILL.md. Plugin-level hook recommendation.

**Token delta:** 0t to SKILL.md.

### Recommended: disable-model-invocation: true

The skill is only invoked at session end, always by the user (or by orchestrator protocol). Claude should never auto-invoke it mid-session. Setting `disable-model-invocation: true` removes the description from the context window entirely, saving ~100 description tokens across all non-session-close interactions.

**Citation:** Bridge-research section 2.4 -- "`disable-model-invocation: true` reduces context cost to absolute zero until you manually invoke the skill."

**Token delta:** ~0t to SKILL.md (frontmatter field), but saves ~100t of description budget across all other skill invocations in the plugin.

---

## Projected Token Delta

| Change | Delta |
|--------|-------|
| Inline data-schema.md (compressed, minus body overlap) | +450t |
| Inline session-record-format.md (compressed, minus body overlap) | +450t |
| Cut: Step 8 redundancy elimination | -40t |
| Cut: Step 2 project-specific commands | -25t |
| Cut: Frontmatter version field | -5t |
| Cut: Backlinking Convention standalone section merge | -20t |
| Add: Vague term definition | +10t |
| Add: Agency clarification | +5t |
| Add: Positive form conversion | +10t |
| Add: Temporal trigger | +5t |
| **Net body change** | **+840t** |
| **Eliminated references** | **-1,865t** |
| **Net system change** | **-1,025t** |

**Before:** 3,541t system total (1,676t body + 1,865t in 2 references).
**After:** ~2,516t system total (~2,516t body + 0t references).
**Net reduction:** ~1,025t (28.9%).

The body grows from 1,676t to ~2,516t, well under both the 5,000t compaction survival threshold and the 500-line guideline. The system total drops significantly because compression during inlining eliminates redundancy between the body and the references (the body had partial schema descriptions that overlapped with data-schema.md, and the backlinking convention overlapped with the session-record-format header template). All content is now in one place, followed on every invocation.

The `disable-model-invocation: true` recommendation saves additional tokens in practice: it removes the 100+ token description from the system prompt context window for every non-session-close interaction across the entire plugin.
