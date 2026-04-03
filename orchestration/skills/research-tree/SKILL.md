---
name: research-tree
version: 2.0.0
description: |
  Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes,
  academic fields, regulatory environments, curated indices, or any domain requiring breadth-first
  exploration followed by depth-first verification.

  Triggers: "research an ecosystem", "survey the landscape", "evaluate options for", "deep-dive",
  "compare alternatives", "map out what exists", "find the best X for Y", "audit the market",
  "what should I use for", "what's available in", "how does X compare to Y across the field".

  The orchestrator governs agents that write durable reports to disk. It never does the research
  itself. Its context window is for decisions, detection, and dispatch — not content.
---

# Research Tree

Govern multi-agent research across any knowledge surface. The orchestrator decides where to look, how deep to go, and when to change course. Agents do the looking.

## Philosophy

Research is not a procedure. It is a series of decisions about scope, depth, and course correction. The tiers below are default gravity — not a script.

### Five Truths

1. **Organize by need, not by source.** A curated list has categories. A market has segments. A standards body has working groups. These are the SOURCE's structure. Your research should be organized by what the STAKEHOLDER needs to decide. "Which component library?" is a need. "Components" is a source category. They produce different research trees.

2. **Verification depth must match claim consequence.** An option that saves 10 lines of code needs a surface skim. An option that becomes a load-bearing dependency needs source-level verification. Match agent capability and effort to the stakes of the claim.

3. **Fresh eyes beat inherited conclusions.** When re-researching at higher fidelity, do NOT feed prior conclusions to new agents. Give them raw context (project facts, source URLs) and let them form independent opinions. Prior conclusions are hypotheses to be tested, not evidence to build on.

4. **The orchestrator detects; agents act.** Detect contradictions between reports. Detect unreliable outputs. Detect when coverage is insufficient. Detect when the research question has been answered. Then dispatch agents to address what you detected.

5. **Reports are the product.** Every agent writes to disk. Later agents read from disk. The orchestrator points agents to files — never relays content through its own context. If you're summarizing one agent's findings to another, you've broken the model.

### Model Selection

Match model capability to task nature, not to tier number:

| Task Nature | Model Tier | Examples |
|-------------|------------|---------|
| Fetch, parse, count, categorize | Cheapest available | Index parsing, dep listing, file auditing, URL scraping |
| Assess, compare, reason about compatibility | Mid-tier | Surveys with context, source-code verification, gap analysis |
| Cross-domain synthesis, strategic judgment | Strongest available | Final synthesis, multi-constraint trade-off analysis |

The cheapest model that can reliably do the task is the right model. Upgrade when you observe unreliable outputs — not preemptively. Ten cheap agents in parallel beat two expensive agents in sequence: the synthesis step handles quality.

### When to Re-Research

A second round at higher fidelity is warranted when:
- Verification overturned multiple survey judgments (the first round was unreliable)
- The surviving candidate set is small enough for deeper attention
- Specific technical questions require source-level reading the first model couldn't do

Second-round rules:
- **Separate directory** — agents don't see first-round reports
- **Higher-capability models** for verification
- **Need-driven organization** (not source-driven)
- **Inherit ONLY facts** — project context, source URLs, raw metadata. Never ratings, opinions, or recommendations from the first round.

## The Tier System

```
Tier 0: GROUND TRUTH — what does the stakeholder actually have and need?
   ↓  (runs parallel with Tier 2)
Tier 1: INDEX — parse the primary source into a structured map
   ↓
Tier 2: SURVEY — fan out by need-category, assess candidates
   ↓
Tier 3: VERIFY — deep-dive promising candidates against primary sources
   ↓
Tier 4: RESOLVE — detect and resolve contradictions across reports
   ↓
Tier 5: SYNTHESIZE — one capable agent reads ALL reports, writes final verdict
```

Not every research needs all tiers. Quick scans skip Tier 3-4. Deep assessments use all six. For skip conditions and heuristics, see @references/tier-playbook.md — it covers tier definitions, completion gates, and agent count heuristics.

**Tier 0 — Ground Truth.** Before evaluating any external option, establish what the stakeholder actually has and needs. Agents audit the project/org itself: inventory existing capabilities, map dependencies, identify pain points. Fact-finding only — no external research.

**Tier 1 — Index.** Parse the primary research surface into a structured map. The orchestrator reads ONLY the summary statistics to plan the Tier 2 fan-out. One agent, one output.

**Tier 2 — Survey.** Fan out by NEED (not source category). Each agent gets: the project context brief, a need to investigate, and instructions to search broadly beyond the provided index. Also launch breadth-expansion agents that search registries, forums, and web beyond the primary source.

**Tier 3 — Verify.** Deep-dive every candidate flagged as promising. Verification means fetching the actual manifest/config, reading source code for compatibility, checking registry metadata, testing against project-specific constraints. Verification agents check primary sources — not documentation.

**Tier 4 — Resolve.** Scan Tier 2-3 outputs for contradictions. Launch targeted resolution agents that check primary sources. Often 0 agents; sometimes 1-3.

**Tier 5 — Synthesize.** One capable agent reads EVERY report, in dependency order (ground truth first). Produces the final deliverable answering the stakeholder's original question.

## Agent Design

### The Prime Directive

Include in every research agent prompt, adapted to the domain:

**Encourage:**
1. **Verify from primary sources.** Fetch the actual manifest, registry API, source code, financial filing, standards document. Documentation and marketing copy are hypotheses, not evidence.
2. **Search broadly.** Use web search, registry search, community forums, academic databases. Don't stop at the provided list. Find things the prompt didn't anticipate.
3. **Report evidence, not conclusions.** Quote the manifest line, link the source file, cite the registry response. Strategic conclusions belong to the synthesis agent — you bring back verified facts.

**Discourage:**
1. **Don't trust claims without primary-source verification.** "Supports X" in a README, "market leader" in a press release, "peer-reviewed" without a DOI — all unverified until confirmed.
2. **Don't conflate similarly-named entities.** Verify exact names, URLs, maintainer identity, publication dates. Two things with similar names are two things until proven otherwise.
3. **Don't make strategic recommendations.** Report what you found with evidence. The synthesis agent decides what it means for the stakeholder.

### Prompt Structure

Every agent prompt specifies:
1. **One task** with one output file path
2. **Named input files** the agent must read — not "check the project" but "read `{path}`"
3. **Report format template** pasted inline — agents can't read skill reference files
4. **Scope boundaries** — what to research and explicitly what NOT to research
5. **Tool expectations** — which tools to use (WebSearch, WebFetch, Read, Grep, Bash, etc.)
6. **The prime directive** adapted to the domain

For prompt quality, apply general prompt engineering principles (clear role, specific instructions, constrained output). The `prompt-optimize` skill codifies these if refinement is needed.

For domain-adaptable skeletons, see @references/agent-templates.md — it provides prompt templates for every agent type.

## Orchestration Protocol

### Setup

1. Create the report directory structure (see below).
2. Define three things: the **research surface** (URL, topic, corpus), the **research question** (what the stakeholder needs to decide), and the **project context** (what local files describe the stakeholder's situation).
3. Use task tracking: one task per agent, mark in_progress/completed, set `blockedBy` for synthesis.

### Per-Tier Execution

1. Design agent prompts from templates, adapted to domain.
2. Launch ALL tier agents in parallel — one message, multiple Agent calls.
3. Mark completions as notifications arrive. Do not read full reports unless arbitration is needed.
4. Gate check: all tasks complete? Any reports missing?
5. Scan completion summaries for: candidates to verify, contradictions to resolve, surprising claims to spot-check.
6. Launch next tier — agents read prior tier reports via file paths.

### Between-Tier Decisions

After Tier 2, decide what enters Tier 3:
- Every candidate rated **promising** in a survey → verification agent
- Every **new find** from breadth expansion above relevance threshold → verification agent
- Every **extraordinary claim** → spot-check agent (even if rated SKIP)
- Every **contradiction** between reports → resolution agent

### Completion Criteria

- Synthesis report exists
- Every high-confidence recommendation is backed by a verification report
- No unresolved contradictions
- The stakeholder's specific question has a definitive, grounded answer

## Directory Structure

### Single-Round Research

```
{project}/research/{topic}/
├── index.md                    # Tier 1: structured map of the surface
├── categories/                 # Tier 2: per-need-category surveys
│   ├── {need-a}.md
│   └── {need-b}.md
├── deep-dives/                 # Tier 0 + 3 + 4: audits, verifications, resolutions
│   ├── project-{aspect}-audit.md
│   ├── {candidate}.md
│   └── {topic}-resolution.md
└── synthesis/
    └── recommendations.md      # Tier 5: final deliverable
```

### Multi-Round Research

When re-researching at higher fidelity, use a parallel directory:

```
{project}/research/{topic}-v2/
├── context/                    # Facts extracted from v1 (NO opinions)
│   ├── project-brief.md       # Distilled from Tier 0 audits
│   ├── source-index.md        # The structured index (factual)
│   └── metadata-factsheet.md  # Raw metadata: versions, URLs, dates
├── tier1-landscape/            # Need-driven surveys (not source-category-driven)
├── tier2-verification/         # Source-level deep-dives
└── synthesis/
    └── final-verdict.md
```

## Adapting to Different Domains

The tier system is domain-agnostic. The instantiation is domain-specific:

| Domain | Primary Source | Registry/DB | Verification Method |
|--------|---------------|-------------|---------------------|
| Software ecosystem | Awesome-list, ecosystem page | Package registry (crates.io, npm, PyPI) | Manifest inspection, source code, CI status |
| Market landscape | Industry reports, review sites | Company databases (Crunchbase, etc.) | Pricing pages, SEC filings, user reviews |
| Academic field | Survey papers, conference procs | Citation databases (Semantic Scholar, etc.) | Paper retrieval, citation verification, replication data |
| Regulatory environment | Statute indices, agency sites | Legal databases (case law, regulations) | Primary statute text, enforcement actions, advisory opinions |
| API ecosystem | API directories, developer docs | Usage metrics, status pages | Integration tests, latency measurements, rate limit checks |

## Anti-Patterns

The three most damaging (for the full catalog of 10 failure modes with detection strategies, see @references/anti-patterns.md):

1. **Context Relay** — reading reports into orchestrator context and relaying to next agent. Burns context on content that lives on disk. Fix: point agents to file paths.
2. **Documentation Trust** — treating marketing prose as evidence. Fix: verification agents must fetch primary sources.
3. **Premature Synthesis** — synthesizing before ground truth exists. Fix: block synthesis on ALL prior tiers including project audits.

## References

- For tier definitions, skip conditions, agent count heuristics, and completion gates, see @references/tier-playbook.md
- For 10 failure modes with detection strategies and fixes, see @references/anti-patterns.md
- For domain-adaptable prompt skeletons for every agent type, see @references/agent-templates.md
- For standardized templates for every report type, see @references/report-formats.md
- For a worked example of software ecosystem research (Rust/Leptos, 98 entries, 22 agents, 5 tiers), see @examples/awesome-leptos-session.md
