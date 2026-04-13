# Core Points: session-close

## Iteration 1

**Point:** The orchestrator holds irreplaceable context that agents cannot reconstruct from disk artifacts, making orchestrator review and correction of agent-drafted outputs mandatory before committing session records.

**Evidence:**
1. SKILL.md:11-15: "**The orchestrator holds context no agent can reconstruct.** Agents extract objective data (metrics, git history, file changes) from disk. The orchestrator synthesizes that with the actual decisions made, failures encountered, and reasoning behind choices — then corrects the agents' reconstructions before committing. Never delegate the final synthesis and correction to an agent."
2. SKILL.md:89-98: "Read the draft session record. Correct: Missing phases (agents reconstruct from git, they miss non-code work), Wrong numbers (agents may use stale data from earlier in session), Missing failures (agents omit failures that aren't in git history), Wrong attribution (which decisions were made vs. which were imposed), Guessed function signatures (agent must read actual code, not infer). This step cannot be delegated."
3. session-record-format.md:94-106: Lists 8 systematic categories agents miss when reconstructing from artifacts: "research/investigation phases — no commits, no artifacts", "Failed first attempts — commits exist but context (why it failed) is lost", "Conversation-driven decisions — never captured in any file", etc.

## Iteration 2

**Point:** The LEAVE protocol produces durable institutional memory by combining objective metrics extracted from raw session JSONL files on disk with orchestrator context into version-controlled documentation.

**Evidence:**
1. SKILL.md:7-9: "Governs the LEAVE protocol for orchestration sessions. Produces durable institutional memory by combining objective data extracted from raw session files on disk with orchestrator context that only the active session possesses."
2. SKILL.md:17-31: Documents the structured session data storage location at `~/.claude-shared/projects/{project-slug}/{session-id}.jsonl` with full JSONL schema including model, usage, agentId, and timestamp fields.
3. SKILL.md:42-87: Defines the 8-step LEAVE protocol workflow where Steps 1-4 extract metrics/history/drafts from disk in parallel, Step 5 requires orchestrator correction, and Steps 6-8 commit the corrected documentation to VCS.

## Iteration 3

**Point:** Cache-read token costs dominate long session expenses because the orchestrator's accumulating context window is re-sent and cache-read every turn, making Opus the dominant cost driver even when most work is delegated to cheaper agent tiers.

**Evidence:**
1. data-schema.md:102-105: "In long sessions, cache_read_input_tokens can be 100-800x larger than direct input_tokens. The orchestrator's context window accumulates and is re-sent as cache every turn. This is why Opus dominates cost even when agents do most of the work — the orchestrator's long context is expensive to cache-read repeatedly."
2. data-schema.md:81-98: Provides complete cost formulas showing cache_read rates (e.g., Opus: $1.50/1M vs $15.00/1M input) and the compute_cost function that aggregates all four token categories including cache_read_input_tokens.
3. SKILL.md:33-38: Documents that JSONL usage objects contain four token count fields: input_tokens, output_tokens, cache_read_input_tokens, cache_creation_input_tokens, establishing cache tokens as first-class billing components.

## Iteration 4

**Point:** Session records must include backlinking via session ID to enable traceability from frozen documentation back to raw JSONL data for future re-extraction or correction.

**Evidence:**
1. SKILL.md:127-141: "Every session record header must include the session ID for traceability" with template showing "**Session ID:** {session-id from JSONL filenames}" and explanation "The session ID links directly to the raw JSONL files in `~/.claude-shared/projects/{slug}/{session-id}.jsonl`."
2. session-record-format.md:109-118: "The session ID in the header links the frozen session record to the live raw data" at the file paths, with explicit statement that "Future orchestrators can re-run metric extraction on the same raw data if the session record needs correction or the recon files were discarded."
3. session-record-format.md:10-11: Header template requires "**Session ID:** {session-id} ← links to raw JSONL files" as a mandatory field with inline annotation emphasizing the linking purpose.

## Iteration 5

**Point:** The LEAVE protocol enforces a separation between gitignored disposable recon data used during session close-out and version-controlled durable session records and reference documentation.

**Evidence:**
1. SKILL.md:123-127: "The `docs/orchestration_log/recon/` directory is gitignored — session metrics and raw git history are disposable. They exist only to assist the session close-out. Regenerate if needed."
2. SKILL.md:100-109: Step 6 commit instructions explicitly state "Do NOT commit recon/ data — it is gitignored" while committing only "docs/orchestration_log/" with session records and reference updates.
3. SKILL.md:80-86: Step 4 targets three "living reference documents" in `docs/orchestration_log/reference/` (codebase_state, deferred_items, conventions) that are durable and version-controlled, contrasting with the disposable recon data from Steps 1-2.

## Rank Summary

1. **Orchestrator irreplaceable context** — The foundational principle that agents cannot reconstruct decisions, failures, and reasoning from artifacts, making orchestrator review mandatory.
2. **Institutional memory production** — The core purpose of combining objective metrics from disk with orchestrator context into VCS-tracked documentation.
3. **Cache-read cost dominance** — The economic reality that shapes session design: long orchestrator contexts drive costs via cache-reading, not direct token consumption.
4. **Session ID backlinking** — The traceability mechanism connecting frozen documentation to raw data for future correction or re-extraction.
5. **Recon vs. durable separation** — The architectural distinction between disposable extraction artifacts and version-controlled institutional memory.
