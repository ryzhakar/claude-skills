# Anti-Patterns in Delegated Research

Failure modes observed in real multi-agent research sessions, with detection strategies and fixes.

---

## AP-1: Context Relay

**Pattern:** Orchestrator reads a report, then includes its content in the next agent's prompt.

**Why it fails:**
- Burns orchestrator context on content that exists on disk.
- Information decays through summarization — the relay introduces noise.
- Scales as O(n) context per relay step. By Tier 5, the orchestrator's context is full of stale summaries.

**Detection:** The orchestrator's prompt to an agent contains verbatim quotes or detailed summaries from another agent's report.

**Fix:** Point agents to file paths. Replace `"The components report found that X, Y, Z..."` with `"Read the components report at {path} for context."` The receiving agent reads the file itself.

**Exception:** Completion summaries (~3 sentences returned by the Agent tool) are fine to scan. The orchestrator needs these to make tier-transition decisions. The anti-pattern is reading the FULL report.

---

## AP-2: Premature Synthesis

**Pattern:** Launching the synthesis agent before project audits (Tier 0) are complete.

**Why it fails:** Recommendations float without ground truth. The synthesizer guesses at what the project needs instead of knowing. Typical result: recommends libraries that solve problems the project doesn't have, or misses libraries that solve problems it does have.

**Detection:** Synthesis task has no `blockedBy` dependency on project audit tasks, or audits are still running when synthesis starts.

**Fix:** Always run project audit agents in parallel with Tier 2. Block synthesis on ALL prior tiers including Tier 0. The synthesis prompt must list project audit reports as the FIRST files to read.

---

## AP-3: README Trust

**Pattern:** Treating a library's README as evidence of its capabilities.

**Why it fails:** READMEs are marketing. They describe aspirations, not reality. Common lies:
- "Supports Framework X" → manifest pins Framework X-1.
- "57+ components" → 20 are stubs, 5 have compile errors.
- "Production ready" → 40 downloads, last commit 8 months ago.
- "Market leader" → 3 customers, none in your segment.
- "Headless" → Injects 200 lines of CSS.
- "Peer-reviewed" → no DOI, no journal, conference workshop only.

**Detection:** Verification report contains phrases like "according to the README", "the documentation states", "described as" without corresponding primary-source evidence.

**Fix:** Tier 3 verification agents must be explicitly instructed: "This is NOT a documentation review. Fetch the actual manifest (Cargo.toml, package.json, pyproject.toml, pom.xml). Call the registry API. Read the source code. Documentation claims are HYPOTHESES, not evidence."

---

## AP-4: Model Waste

**Pattern:** Using opus/sonnet for mechanical tasks (fetching URLs, parsing structured text, grepping code).

**Why it fails:** Expensive models are no better than haiku at:
- Fetching a URL and extracting data.
- Grepping a codebase for patterns.
- Parsing a structured document into a table.
- Counting files or lines.

Using them for these tasks wastes budget that should be reserved for judgment-heavy work (synthesis, contradiction resolution, nuanced compatibility assessment).

**Detection:** Sonnet or opus agents performing tasks that are pure fetch-parse-write without judgment.

**Fix:** Use haiku for all Tier 1, Tier 2, and most Tier 3 work. Use sonnet only for Tier 5 synthesis and complex Tier 3 verifications that require cross-referencing multiple sources with judgment. Use opus only for the orchestrator.

**Corollary:** Haiku agents compensate for lower reasoning with higher parallelism. Ten haiku agents running in parallel cost less and finish faster than two sonnet agents running sequentially. Optimize for throughput, not per-agent quality — the synthesis step handles quality.

---

## AP-5: Sequential Addiction

**Pattern:** Launching agents one at a time, waiting for each to complete before launching the next.

**Why it fails:**
- 10 agents × 90 seconds = 15 minutes sequential, 90 seconds parallel.
- The orchestrator's context grows with each wait-launch-wait cycle.
- No information dependency exists between agents within the same tier — they're independent by design.

**Detection:** Only one agent is running at a time, or agents are launched in separate messages when they could be in one message.

**Fix:** Within each tier, launch ALL agents in a single response with multiple Agent tool calls. The only sequential dependency is between tiers (Tier 2 waits for Tier 1, etc.). Within a tier, everything is parallel.

---

## AP-6: Hallucination Propagation

**Pattern:** An agent hallucinates a claim. The claim is not verified. It reaches the synthesis report as fact.

**Why it fails:** LLM agents, especially haiku, will occasionally:
- Invent library names that don't exist.
- Confuse two similarly-named libraries.
- Claim a library has features it doesn't.
- Report version numbers that are wrong.

If these claims propagate unchecked to synthesis, the final recommendations are unreliable.

**Detection signals:**
- Extraordinary claims (">1000 components", "10M downloads") without URL evidence.
- Two reports disagree about the same library (one says archived, another says active).
- A library name appears in one report but not in the original index or any verification report.
- Download counts or star counts that seem implausible for the ecosystem size.

**Fix:**
1. **Tier 4 contradiction resolution** — scan completion summaries for disagreements.
2. **Spot-check extraordinary claims** — if something sounds too good, launch a verification agent even if the entry was rated SKIP.
3. **Synthesis agent instruction** — include: "If a claim appears in only one report and is not corroborated by a verification report, flag it as UNVERIFIED in the confidence section."

---

## AP-7: Scope Drift

**Pattern:** Agents wander beyond their assigned category/topic, producing reports with tangential findings.

**Why it fails:**
- Report format breaks when the agent mixes in-scope and out-of-scope entries.
- The synthesizer can't tell which findings are authoritative (in-scope) vs incidental.
- Agent context budget is wasted on tangential exploration.

**Detection:** A category report includes entries not in that category's section of the index, or discusses features beyond its assessment criteria.

**Fix:** Each agent prompt names the exact section of the index to read and the exact entries to assess. Include: "Assess ONLY the entries listed in the '{Category}' section of the index. Do not research entries from other categories."

---

## AP-8: Format Anarchy

**Pattern:** Each agent uses a different report format, making cross-referencing impossible.

**Why it fails:** The Tier 5 synthesizer must read 15-25 reports. If every report has a different structure, the synthesizer spends its context budget parsing formats instead of synthesizing insights. Inconsistent rating scales (one agent uses "RECOMMENDED/NOT RECOMMENDED", another uses "ADOPT/SKIP") create false disagreements.

**Detection:** Reports in `categories/` don't follow the same template, or use different rating terminology.

**Fix:** Paste the exact report template from @references/report-formats.md into every agent prompt. Use the same rating scale everywhere: ADOPT/EVALUATE/SKIP for recommendations, VERIFIED/UNVERIFIED/INCOMPATIBLE for compatibility checks.

---

## AP-9: Orphaned Findings

**Pattern:** A breadth-expansion agent finds a significant library, but no Tier 3 verification agent is launched for it.

**Why it fails:** The finding exists only in a breadth report with surface-level assessment. It may be the best candidate in the entire ecosystem, but because it wasn't in the original index, it slips through the tier pipeline.

**Detection:** Breadth expansion report contains entries rated EVALUATE or ADOPT, but no corresponding deep-dive report exists in `deep-dives/`.

**Fix:** After breadth-expansion agents complete, scan their summaries for high-signal finds. For any entry with:
- >5000 downloads (or ecosystem-appropriate threshold)
- Direct relevance to the research goal
- ADOPT or EVALUATE rating

Launch a Tier 3 verification agent. Block synthesis on these additional verifiers.

---

## AP-10: No Project Context in Survey Agents

**Pattern:** Tier 2 survey agents assess libraries in a vacuum, without reading project context files.

**Why it fails:** "Relevance to this project" becomes guesswork. The agent rates a library HIGH relevance because it sounds useful in general, not because it solves a specific project problem.

**Detection:** Survey agent prompt doesn't include paths to project guidance files, or the report's relevance assessments don't reference specific project features/constraints.

**Fix:** Every Tier 2 agent prompt must include:
1. A project description sentence.
2. Paths to 1-3 project context files (design system, architecture doc, dependency manifest).
3. The instruction: "Assess relevance based on the project's ACTUAL needs as described in the context files, not general usefulness."

---

## Detection Checklist

Before launching each tier, verify:

- [ ] No agent prompt relays content from another agent's report (AP-1)
- [ ] All prior tiers are complete, including project audits (AP-2)
- [ ] Verification agents are instructed to check primary sources, not READMEs (AP-3)
- [ ] Agent model matches task complexity: haiku for mechanical, sonnet for synthesis (AP-4)
- [ ] All independent agents launch in parallel within a single message (AP-5)
- [ ] Extraordinary claims from prior tiers have verification agents assigned (AP-6)
- [ ] Each agent's scope matches exactly one category/candidate (AP-7)
- [ ] Report format template is pasted into every agent prompt (AP-8)
- [ ] Breadth-expansion high-signal finds have verification agents (AP-9)
- [ ] Survey agents receive project context file paths (AP-10)

Before launching synthesis, verify:

- [ ] No contradictions remain unresolved between reports
- [ ] Every ADOPT recommendation has a corresponding deep-dive report
- [ ] Synthesis agent's file list includes EVERY report from EVERY tier
- [ ] Synthesis prompt includes the user's original question
