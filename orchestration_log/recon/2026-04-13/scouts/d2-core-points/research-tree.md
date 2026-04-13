# Core Points Extraction: research-tree

## Iteration 1

**Point:** The orchestrator governs decisions and agent dispatch but never does content work itself; agents write all reports to disk and later agents read from disk, never through orchestrator context relay.

**Evidence:**
- SKILL.md line 12-13: "The orchestrator governs agents that write durable reports to disk. It never does the research itself. Its context window is for decisions, detection, and dispatch — not content."
- SKILL.md line 34: "The orchestrator points agents to files — never relays content through its own context. If you're summarizing one agent's findings to another, you've broken the model."
- anti-patterns.md line 7-20 (AP-1 Context Relay): Defines reading reports into orchestrator context and relaying to next agent as a primary anti-pattern that "burns orchestrator context on content that exists on disk" and creates information decay.

## Iteration 2

**Point:** Research must be organized by what the stakeholder needs to decide (need-driven), not by how the source categorizes content (source-driven).

**Evidence:**
- SKILL.md line 26: "Organize by need, not by source. A curated list has categories. A market has segments. A standards body has working groups. These are the SOURCE's structure. Your research should be organized by what the STAKEHOLDER needs to decide."
- SKILL.md line 89: "Fan out by NEED (not source category). Each agent gets: the project context brief, a need to investigate, and instructions to search broadly beyond the provided index."
- tier-playbook.md line 86-91: "Do NOT mirror the source's categories. Instead: 1. Read the stakeholder's research question 2. Decompose into the 3-7 decisions they need to make 3. Each decision becomes a need-category"

## Iteration 3

**Point:** Verification means checking primary sources (manifests, source code, registry APIs, financial filings) not documentation, because documentation and marketing are hypotheses that must be confirmed against ground truth.

**Evidence:**
- SKILL.md line 104: "Verify from primary sources. Fetch the actual manifest, registry API, source code, financial filing, standards document. Documentation and marketing copy are hypotheses, not evidence."
- SKILL.md line 92: "Verification agents check primary sources — not documentation."
- anti-patterns.md line 37-50 (AP-3 README Trust): Documents that READMEs are marketing and lists common lies ("Supports Framework X" when manifest pins X-1, "57+ components" when 20 are stubs), requiring Tier 3 agents to "fetch the actual manifest" and treat "documentation claims as HYPOTHESES, not evidence."

## Iteration 4

**Point:** When re-researching at higher fidelity, agents must receive only raw facts (project context, source URLs, metadata) from the first round, never conclusions or ratings, to ensure fresh independent verification.

**Evidence:**
- SKILL.md line 30: "Fresh eyes beat inherited conclusions. When re-researching at higher fidelity, do NOT feed prior conclusions to new agents. Give them raw context (project facts, source URLs) and let them form independent opinions. Prior conclusions are hypotheses to be tested, not evidence to build on."
- SKILL.md line 59: "Inherit ONLY facts — project context, source URLs, raw metadata. Never ratings, opinions, or recommendations from the first round."
- tier-playbook.md line 251: "Second-round setup: separate directory, higher-fidelity models, need-driven organization, inherit only facts from round one."

## Iteration 5

**Point:** Agents must be launched in parallel within each tier (not sequentially) because they have no information dependencies within the same tier, and parallelism dramatically reduces wall-clock time.

**Evidence:**
- SKILL.md line 137: "Launch ALL tier agents in parallel — one message, multiple Agent calls."
- anti-patterns.md line 74-85 (AP-5 Sequential Addiction): "10 agents × 90 seconds = 15 minutes sequential, 90 seconds parallel" and "No information dependency exists between agents within the same tier — they're independent by design." Fix: "Within each tier, launch ALL agents in a single response with multiple Agent tool calls."
- tier-playbook.md line 95: "All launched in parallel" (in the agent count section for Tier 2)

## Rank Summary

1. **Disk-based communication (no context relay)** — Most pervasive architectural constraint; appears in skill philosophy, orchestration protocol, and as top anti-pattern. Violations break the entire model.

2. **Primary source verification (not documentation)** — Core epistemic principle embedded in prime directive, tier definitions, and dedicated anti-pattern. Determines research reliability.

3. **Need-driven organization (not source-driven)** — Fundamental structuring principle affecting Tier 2 design and multi-round research. Directly impacts research usefulness.

4. **Parallel execution within tiers** — Critical performance and architectural requirement. Enables scalability and appears in protocol and anti-patterns.

5. **Fresh eyes for re-research (no inherited conclusions)** — Important for multi-round research quality but more specialized in application than the above four.
