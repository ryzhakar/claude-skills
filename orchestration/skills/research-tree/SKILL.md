---
name: research-tree
description: |
  Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes,
  academic fields, regulatory environments, curated indices, or any domain requiring breadth-first
  exploration followed by depth-first verification.

  Triggers: "research an ecosystem", "survey the landscape", "evaluate options for", "deep-dive",
  "compare alternatives", "map out what exists", "find the best X for Y", "audit the market",
  "what should I use for", "what's available in", "how does X compare to Y across the field".
---

# Research Tree

Govern multi-agent research across any knowledge surface. The orchestrator decides where to look, how deep to go, and when to change course. Agents execute.

## Verb Interpretation

Every research verb from the user implies agent-delegated execution. The orchestrator decomposes, delegates, and assembles. It never does the research itself.

- "research/explore/survey X" — dispatch research agents across the knowledge surface for X.
- "evaluate/compare/assess X" — dispatch evaluation agents with primary-source verification for X.
- "find/discover/map X" — dispatch discovery agents with breadth expansion for X.
- "verify/check/audit X" — dispatch verification agents against primary sources for X.
- "summarize/synthesize X" — dispatch synthesis agents that read all prior reports for X.

The orchestrator's context window is for decisions, detection, and dispatch — not content.

## Philosophy

Research is deciding where to look, how deep to go, and when to change course. The tiers below are default gravity — not a script.

### Five Truths

1. **Organize by need, not by source.** A curated list has categories. A market has segments. These are the SOURCE's structure. Organize research by what the STAKEHOLDER needs to decide. "Which component library?" is a need. "Components" is a source category. They produce different research trees.

2. **Verification depth must match claim consequence.** An option that saves 10 lines of code needs a surface skim. An option that becomes a load-bearing dependency needs source-level verification. Match agent capability and effort to the stakes.

3. **Fresh eyes beat inherited conclusions.** When re-researching at higher fidelity, give new agents raw context (project facts, source URLs) and let them form independent opinions. Prior conclusions are hypotheses to test, not evidence to build on.

4. **The orchestrator detects; agents act.** Detect contradictions between reports. Detect unreliable outputs. Detect insufficient coverage. Detect when the research question has been answered. Then dispatch agents to address what you detected.

5. **Reports are the product.** Every agent writes to disk. Later agents read from disk. The orchestrator points agents to files — never relays content through its own context. If you are summarizing one agent's findings to another, you have broken the model.

### Model Selection

| Task Nature | Model Tier | Examples |
|-------------|------------|---------|
| Fetch, parse, count, categorize | Cheapest available | Index parsing, dep listing, file auditing, URL scraping |
| Assess, compare, reason about compatibility | Mid-tier | Surveys with context, source-code verification, gap analysis |
| Cross-domain synthesis, strategic judgment | Strongest available | Final synthesis, multi-constraint trade-off analysis |

The cheapest model that can reliably do the task is the right model. Upgrade when you observe unreliable outputs — not preemptively. Ten cheap agents in parallel beat two expensive agents in sequence: quality emerges in synthesis.

### When to Re-Research

A second round at higher fidelity is warranted when:
- Verification overturned multiple survey judgments (the first round was unreliable)
- The surviving candidate set is small enough for deeper attention
- Specific technical questions require source-level reading the first model could not do

Second-round rules:
- **Separate directory** — agents do not see first-round reports
- **Higher-capability models** for verification
- **Need-driven organization** (not source-driven)
- **Inherit ONLY facts** — project context, source URLs, raw metadata. Never ratings, opinions, or recommendations from the first round.

### Session Persistence

For multi-session research, the parent's ARRIVE/WORK/LEAVE lifecycle applies. The `reference/` layer holds research-specific conventions and findings inventory; `recon/` holds raw scouting data (gitignored).

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

Not every research needs all tiers. Quick scans skip Tier 3-4. Deep assessments use all six.

### Tier 0 — Ground Truth

**Purpose:** Establish what the stakeholder has and needs. Without this, all recommendations float.

**Always run.** Even if the project seems well-understood, audit agents discover things the orchestrator does not know: actual versions, hidden pain points, capability inventories, undocumented patterns.

**Agent count:** 2-4 agents (capability auditor, dependency auditor, architecture auditor). Cheapest model. All parallel at Tier 2 start.

**Completion gate:**
- All reports exist
- Each contains quantified inventory (counts, not prose)
- Concrete findings with file:line references
- Ranked pain points section

**Common failure:** Shallow keyword search that misses patterns. Instruct agents to READ files, not just grep keywords.

### Tier 1 — Index

**Purpose:** Parse the primary research surface into a structured, cross-referenceable map. One agent, one output.

**Always run.** This is the entry point. Must complete before Tier 2 starts.

**Completion gate:** `index.md` contains every category and every entry with name, URL/identifier, one-line description, plus statistics section with totals and category list.

**Orchestrator decision:** Read ONLY the statistics/category list (~20 lines). Never read the full index into context. Fan-out needs the category list, not entry details.

### Tier 2 — Survey

**Purpose:** Broad assessment across the landscape, organized by stakeholder need.

**How to define need-categories:** Do NOT mirror the source's categories. Decompose the stakeholder's research question into the 3-7 decisions they need to make. Each decision becomes a need-category. Example: "Should I adopt a component library?" decomposes into headless UI primitives, styling tools, form enhancement, data display, DX utilities — not the source's own category structure.

**Agent count:** 1 surveyor per need-category (3-7 agents) + 1-2 breadth expanders (registry search, web search). All parallel.

**Completion gate:**
- One report per need-category with per-entry analysis (activity, compatibility, relevance rating, assessment)
- Breadth expansion reports listing finds NOT in the original index

**Model selection:** Cheapest for mechanical surveying. Upgrade specific agents that require nuanced judgment (e.g., assessing architectural compatibility).

### Tier 3 — Verify

**Purpose:** Deep verification of promising candidates against primary sources. Documentation claims become confirmed or refuted.

**What triggers a verification agent:**
- Any candidate rated PROMISING in a survey (compatibility confirmed, recent activity)
- Any new find from breadth expansion mentioned in 2+ survey reports OR directly addressing a stakeholder need
- Any claim contradicting 2+ other reports OR asserting capability without primary source evidence — even if rated SKIP
- Anything significant the orchestrator notices in completion summaries

**Verification means:** fetching the actual manifest/config, reading source code, checking registry metadata, testing against project-specific constraints. Verification agents check primary sources — not documentation.

**Agent count:** 1 per candidate. All parallel.

**Model selection:** Cheapest for version/metadata checking; mid-tier for source-code reasoning and cross-referencing.

**Completion gate:** Each report contains:
- Metadata from authoritative source (registry API, not README)
- Compatibility: VERIFIED / UNVERIFIED / INCOMPATIBLE — with primary-source evidence
- Project-specific integration assessment
- Risks with evidence
- Verdict with confidence level

### Tier 4 — Resolve

**Purpose:** Detect and resolve contradictions between reports.

Scan for: same entity with different verdicts, same entity described as "dead" by one agent and "active" by another, compatibility or capability claims that disagree.

**Agent count:** 1 per contradiction. Often 0. Sometimes 1-3. If no contradictions detected, proceed directly to Tier 5.

**Completion gate:** Each resolution report states the contradiction, what each report claimed, what primary source evidence shows, and which claim is correct.

### Tier 5 — Synthesize

**Purpose:** One capable agent reads ALL reports and produces the final research deliverable.

**Model:** Strongest available. This agent must reason across 10-25 reports, weigh conflicting evidence, and produce strategic recommendations. It earns the cost.

**Agent count:** 1. This is the capstone.

**Completion gate:**
- Executive summary answering the original question
- Tiered recommendations with evidence citations
- Dedicated section for the stakeholder's specific interest
- Integration notes for top-tier items
- Coverage gaps
- Research confidence assessment

**Common failure:** Synthesis agent skims and writes generic recommendations. Require it to cite specific report files for each claim and include a confidence section acknowledging what was not verified.

## Tier Transitions

### How Many Tiers?

| Research Need | Tiers Used | Rationale |
|--------------|-----------|-----------|
| Quick landscape scan | 1 → 2 → 5 | No candidates worth deep-diving |
| Standard evaluation | 0 + 1 → 2 → 3 → 5 | Index, survey, verify, synthesize |
| Deep assessment | 0 + 1 → 2 → 3 → 4 → 5 | Full pipeline with contradiction resolution |
| Multi-round deep assessment | Full first round → extract facts → full second round with better models | When first round is unreliable |

### When to Add Agents Within a Tier

- **New finds:** Breadth expansion surfaces significant unlisted candidates → launch Tier 3 verifiers
- **Extraordinary claims:** Agent claims something remarkable → launch verification even if rated SKIP
- **Missing context:** Survey agents need project details Tier 0 did not cover → launch additional auditor

### When to Stop Early

- **Question answered:** Tier 2 unanimously shows no viable candidates → skip to synthesis with "nothing to adopt"
- **All candidates eliminated:** Tier 3 downgrades everything → skip Tier 4
- **Context budget:** Research consuming too much time/cost → synthesize with what exists, note gaps

### When to Launch a Second Round

- Multiple Tier 3 verdicts overturned Tier 2 assessments (first-round models unreliable)
- 2-4 candidates survived and each needs source-level scrutiny the first-round model cannot provide
- A specific technical question requires reading actual source code

Second-round setup: separate directory, higher-fidelity models, need-driven organization, inherit only facts from round one.

## Orchestration Protocol

### Setup

1. Create the report directory structure (see below).
2. Define three things: the **research surface** (URL, topic, corpus), the **research question** (what the stakeholder needs to decide), and the **project context** (what local files describe the stakeholder's situation).
3. Use task tracking: one task per agent, mark in_progress/completed, set `blockedBy` for synthesis.

### Per-Tier Execution

1. Design agent prompts from templates, adapted to domain.
2. Launch ALL tier agents in parallel — one message, multiple Agent calls.
3. Mark completions as notifications arrive. Read full reports only when arbitration is needed.
4. Gate check: all tasks complete? Any reports missing?
5. Scan completion summaries for: candidates to verify, contradictions to resolve, surprising claims to spot-check.
6. Launch next tier — agents read prior tier reports via file paths.

### Between-Tier Decisions

After Tier 2, decide what enters Tier 3:
- Every candidate rated PROMISING in a survey → verification agent
- Every new find from breadth expansion mentioned in 2+ survey reports OR directly addressing a stakeholder need → verification agent
- Every claim contradicting 2+ other reports OR asserting capability without primary source evidence → spot-check agent
- Every contradiction between reports → resolution agent

### Completion Criteria

- Synthesis complete.
- All recommendations backed by verification reports.
- All contradictions resolved.
- Stakeholder's question answered definitively with grounded evidence.

## Agent Design

### The Prime Directive

Include in every research agent prompt, adapted to the domain:

**Encourage:**
1. **Verify from primary sources.** Fetch the actual manifest, registry API, source code, financial filing, standards document. Documentation and marketing copy are hypotheses, not evidence.
2. **Search broadly.** Use web search, registry search, community forums, academic databases. Search beyond the provided list. Find things the prompt did not anticipate.
3. **Report evidence, not conclusions.** Quote the manifest line, link the source file, cite the registry response. Strategic conclusions belong to the synthesis agent — you bring back verified facts.

**Discourage:**
1. Verify all claims against primary sources. "Supports X" in a README, "market leader" in a press release, "peer-reviewed" without a DOI — all unverified until confirmed.
2. Distinguish similarly-named entities by exact names, URLs, identifiers. Two things with similar names are two things until proven otherwise.
3. Report findings with evidence. Leave strategic recommendations to the synthesis agent.

### Prompt Structure

Every agent prompt specifies:
1. **One task** with one output file path
2. **Named input files** the agent must read — not "check the project" but "read `{path}`"
3. **Report format template** pasted inline — agents cannot read skill reference files
4. **Scope boundaries** — what to research and explicitly what NOT to research
5. **Tool expectations** — which tools to use (WebSearch, WebFetch, Read, Grep, Bash, etc.)
6. **The prime directive** adapted to the domain

## Agent Prompt Templates

Domain-adaptable prompt skeletons for every agent type. Replace `{PLACEHOLDERS}` with concrete values for your research surface.

### The Prime Directive Block

Include this (adapted to domain) in EVERY research agent prompt:

```
RESEARCH PRINCIPLES — follow these throughout:
1. Verify from primary sources — fetch the actual manifest, registry entry, source code,
   filing, or standards document. Documentation and marketing copy are hypotheses, not evidence.
2. Search broadly — use web search, registries, forums. Don't stop at the provided list.
   Find things this prompt didn't anticipate.
3. Report evidence, not conclusions — quote the source, link the file, cite the response.
   Strategic recommendations belong to the synthesis agent. You bring back verified facts.

DO NOT:
- Trust documentation claims without primary-source confirmation
- Conflate similarly-named entities — verify exact names, URLs, identifiers
- Make strategic adoption/rejection recommendations — report findings with evidence
```

### Index Parser (cheapest; WebFetch, Write)

```
You are indexing {SOURCE_DESCRIPTION} for a research project.

TASK:
1. Fetch {PRIMARY_URL}
2. Parse the full document and extract EVERY category and EVERY entry listed.
3. Write a structured index to {REPORT_PATH}/index.md

The index format MUST be:

# {TOPIC} Full Index

Fetched: {DATE}
Source: {PRIMARY_URL}

## Categories

### [Category Name]

| # | Name | URL/Identifier | One-line description |
|---|------|----------------|----------------------|
| 1 | ... | ... | ... |

[repeat per category]

## Statistics

- Total categories: N
- Total entries: N
- Categories list: cat1, cat2, cat3, ...

Be EXHAUSTIVE. Every single entry must appear. Do not skip or summarize.
```

### Need-Category Surveyor (cheapest, upgrade for nuanced assessment; Read, WebFetch, WebSearch, Write)

```
You are investigating {NEED_DESCRIPTION} in the {DOMAIN} landscape.

CONTEXT: {PROJECT_DESCRIPTION}

{PRIME_DIRECTIVE_BLOCK}

INPUT FILES:
1. {REPORT_PATH}/index.md — the structured index (your starting point, not your boundary)
2. {PROJECT_CONTEXT_FILE} — the stakeholder's current situation and constraints

TASK:
1. Read the index for relevant entries
2. Read the project context to understand actual needs
3. Search BEYOND the index — use WebSearch and registry searches to find candidates
   the index doesn't list
4. For EACH candidate found:
   a. Fetch its primary page (README, homepage, registry entry)
   b. Check: last activity, adoption signals, version compatibility with {FRAMEWORK_VERSION}
   c. Assess: does it address the specific need "{NEED_DESCRIPTION}" for this project?
5. Write your report to {REPORT_PATH}/categories/{NEED_SLUG}.md

REPORT FORMAT:
Paste the relevant format from the Report Format Templates section below.

Assess ONLY candidates relevant to "{NEED_DESCRIPTION}". Do not drift into other needs.
```

### Project Auditor (cheapest; Read, Grep, Glob, Bash, Write)

Three variants — launch all in parallel. Adapt to the project type.

**Capability/UI Auditor:** Find all components/modules/endpoints. For each: file path, name, key features, patterns used. Find interaction patterns. Identify repeated code patterns. Catalog styling/config tokens. Identify pain points where external tools could reduce boilerplate. Write to `{REPORT_PATH}/deep-dives/project-capability-audit.md`.

**Dependency Auditor:** Read manifest completely. Document every dependency with version. Check lockfile for resolved versions. Map version constraints. Document build system and dev workflow. Identify existing tooling for the research domain. Write to `{REPORT_PATH}/deep-dives/project-deps-audit.md`.

**Architecture Auditor:** Find all handlers/endpoints/controllers. Map routing with guards/middleware. Catalog error handling patterns. Map state management. Find code quality signals (TODOs, FIXMEs, lint suppressions). Catalog test infrastructure. Rank DX gaps by impact. Write to `{REPORT_PATH}/deep-dives/project-arch-audit.md`.

### Candidate Verifier (cheapest for metadata, mid-tier for source-code reasoning; Read, Grep, WebFetch, WebSearch, Write)

```
You are doing a DEEP technical verification of {CANDIDATE_NAME} for a {PROJECT_DESCRIPTION}.

This is NOT a documentation review. VERIFY claims by reading actual source code and metadata.

{PRIME_DIRECTIVE_BLOCK}

TASKS:
1. Fetch registry metadata: {REGISTRY_API_URL}
   — exact version, adoption metrics, last publish date
2. Fetch the manifest from the repo: {REPO_MANIFEST_URL}
   — check what version of {FRAMEWORK} it actually depends on
3. Check compatibility: does it target {FRAMEWORK_VERSION}? Direct pin or feature flags?
4. Fetch changelog or releases for breaking changes
5. Check project-specific constraints: {CONSTRAINT_CHECKLIST}
6. Read the project's current approach: {PROJECT_FILES_TO_COMPARE}
7. Assess: would adopting this improve the project, or does the current approach suffice?

Write to {REPORT_PATH}/deep-dives/{CANDIDATE_SLUG}.md

REPORT FORMAT:
Paste the relevant format from the Report Format Templates section below.
```

### Breadth Expander (cheapest; Read, WebFetch, WebSearch, Write)

```
You are searching for {DOMAIN} options NOT on the primary index.

{PRIME_DIRECTIVE_BLOCK}

TASKS:
1. Search registries and web: {SEARCH_URLS_AND_QUERIES}
2. Read the index at {REPORT_PATH}/index.md to know what's already listed.
3. For every find NOT in the index AND above relevance threshold
   (mentioned in 2+ sources OR directly addresses a stakeholder need):
   — note name, version, adoption metrics, description, category
4. For high-signal finds, fetch their primary page for more details.

Write to {REPORT_PATH}/deep-dives/unlisted-{SOURCE}.md

Include: search methodology, high-signal finds (detailed), medium-signal finds (table),
landscape size stats, notable patterns.
```

### Contradiction Resolver (cheapest; WebFetch, WebSearch, Read, Write)

```
VERIFICATION TASK: Two research reports make contradictory claims.

Report A ({REPORT_A_PATH}) claims: {CLAIM_A}
Report B ({REPORT_B_PATH}) claims: {CLAIM_B}

These claims CONTRADICT each other. One may be wrong or hallucinated.

{PRIME_DIRECTIVE_BLOCK}

TASK: Verify against PRIMARY SOURCES. Do NOT trust either report.

1. {VERIFICATION_STEPS}
2. For anything that exists: check version, status, last activity.

Write to {REPORT_PATH}/deep-dives/{TOPIC}-resolution.md

Format:
# {TOPIC} — Contradiction Resolution

## The Contradiction
- Report A claims: ...
- Report B claims: ...

## Primary Source Checks
### Check 1: {what was checked}
- URL: ...
- Result: ...
- Supports: Report A / Report B / Neither

## Verdict
{Which claim is correct, with evidence}

DO NOT HALLUCINATE. If a URL 404s, say so. If something doesn't exist, say so.
```

### Production/Real-World Inspector (cheapest; WebFetch, Read, Write)

```
You are investigating what real-world {DOMAIN} practitioners actually use.

TASKS:
1. Fetch configuration/manifest files from these sources: {SOURCE_URLS}
2. For each successful fetch:
   — list all {DOMAIN}-relevant dependencies/tools/choices
   — note version pins and configuration patterns
3. Cross-reference: which choices appear in 2+ sources?

Write to {REPORT_PATH}/deep-dives/production-usage.md

Include: per-source breakdowns, cross-reference table, patterns, implications.
```

### Synthesizer (strongest available; Read, Write)

```
You are writing the FINAL synthesis for the {TOPIC} research project.

Synthesize FROM REPORTS, not from your own knowledge. Read every file listed below.
Do not include claims that aren't in any report.

## Reports to Read (ALL of them, in this order)

### Ground Truth (Tier 0)
{TIER_0_FILE_PATHS}

### Index (Tier 1)
{TIER_1_FILE_PATHS}

### Surveys (Tier 2)
{TIER_2_FILE_PATHS}

### Verifications (Tier 3)
{TIER_3_FILE_PATHS}

### Resolutions (Tier 4, if any)
{TIER_4_FILE_PATHS}

## The Question to Answer
{STAKEHOLDER_RESEARCH_QUESTION}

## Output
Write to {REPORT_PATH}/synthesis/recommendations.md

## Format
Paste the relevant format from the Report Format Templates section below.

Be OPINIONATED. Clear yes/no decisions, not diplomatic hedging. Cite report file paths
for every factual claim.
```

## Report Format Templates

Consistent formats allow the Tier 5 synthesizer to cross-reference findings reliably. Paste the relevant template into every agent prompt.

**Rating scales (use consistently across all reports):**
- **ADOPT** — clear value, verified compatibility, worth integrating
- **EVALUATE** — promising but needs a proof-of-concept or has a specific uncertainty
- **SKIP** — assessed and rejected (state why: incompatible, dead, out of scope, etc.)
- **VERIFIED** — primary source (manifest, source code, registry API) confirms the claim
- **UNVERIFIED** — only README/docs support the claim; no primary source checked
- **INCOMPATIBLE** — primary source contradicts compatibility

### Index Report (`index.md`)

```markdown
# {Topic} Full Index

Fetched: YYYY-MM-DD
Source: {URL}

## Categories

### {Category Name}

| # | Name | URL | Description |
|---|------|-----|-------------|
| 1 | ... | ... | ... |

[repeat per category]

## Statistics

- **Total categories:** N
- **Total entries:** N
- **Categories list:** cat1, cat2, cat3
```

Every entry must have name, URL, and description. No partial entries.

### Category Survey Report (`categories/{slug}.md`)

```markdown
# {Category Name} — Deep Dive

## Summary
[2-3 sentences: what this category covers, overall ecosystem maturity]

## Per-Entry Analysis

### {Entry Name}
- **URL:** {url}
- **Stars/Activity:** {stars} stars, last commit {date} / {downloads} downloads
- **Version compatibility:** {framework} {version} / unknown / incompatible
- **What it does:** [1-2 sentences]
- **Relevance to this project:** HIGH / MEDIUM / LOW / NONE — [1 sentence why]
- **Adoption recommendation:** ADOPT / EVALUATE / SKIP — [1 sentence why]

[repeat per entry]

## Category Verdict
[2-4 sentences: which entries matter, overall recommendation for this category]
```

Required per entry: URL, activity indicator, version compatibility, relevance, recommendation. Missing fields indicate agent failed to fetch.

### Deep Verification Report (`deep-dives/{candidate}.md`)

```markdown
# {Candidate Name} — Deep Technical Verification

## Metadata
- **Registry:** {url}
- **Latest version:** {version}
- **Framework dependency:** {exact version or range from manifest}
- **Downloads:** {total} total / {recent} recent
- **Last publish:** {date}
- **License:** {license}

## {Framework} {Version} Compatibility
**{VERIFIED / UNVERIFIED / INCOMPATIBLE}**

Evidence: {exact line from manifest file showing the dependency version}

## {Constraint 1}
**{VERIFIED / UNVERIFIED / INCOMPATIBLE}**

Evidence: {what was found}

## Current Project Approach
[What the project does now for the same problem. From reading project files, not guessing.]

## Integration Effort
**{Trivial / Moderate / Significant}**

- Files changed: ~N
- Lines changed: ~N
- Risk: {low / medium / high} — {why}

## Risks
1. {Risk 1 with evidence}

## Verdict
**{ADOPT / DEFER / SKIP}** — Confidence: {high / medium / low}

{2-3 sentences justifying the verdict}
```

### Project Audit Report (`deep-dives/project-{aspect}-audit.md`)

```markdown
# Project {Aspect} Audit

## {Inventory Section}
| Item | Location | Properties |
|------|----------|------------|
| ... | file:line | ... |

## {Pattern Section}
[Recurring patterns found, with frequency counts]

## {Gap/Pain Point Section}
| # | Pain Point | Severity | Files Affected | Fix Category |
|---|-----------|----------|----------------|--------------|
| 1 | ... | HIGH/MEDIUM/LOW | N files | library / refactor / new code |
```

Required: at least one inventory table, at least one quantified finding, ranked pain points.

### Contradiction Resolution Report (`deep-dives/{topic}-resolution.md`)

```markdown
# {Topic} — Contradiction Resolution

## The Contradiction
- **Report A** ({file path}): claims {claim A}
- **Report B** ({file path}): claims {claim B}

## Primary Source Checks

### Check 1: {what was checked}
- **URL:** {url}
- **Result:** {what the primary source shows}
- **Supports:** Report A / Report B / Neither

## Verdict
**{Report A is correct / Report B is correct / Both partially correct / Both wrong}**

Evidence summary: {2-3 sentences}

## Impact on Recommendations
[How this resolution changes the adoption recommendation]
```

### Synthesis Report (`synthesis/recommendations.md`)

```markdown
# {Topic}: Final Adoption Recommendations

> Research basis: {N} reports, {N} entries surveyed, {N} deep verifications, {N} project audits.

## Executive Summary
[5-7 sentences. Answer the user's original question definitively.]

## Project Context (from audits)
[Brief: framework version, component count, dep count, top 3 pain points]

## Adoption Tiers

### Tier 1: ADOPT NOW
[Only items with VERIFIED compatibility from Tier 3 reports.]

#### {Library Name}
- **What it solves:** [specific project problem, citing project audit]
- **Verification:** [cite deep-dive report file]
- **Integration effort:** {Trivial / Moderate / Significant}
- **Risk:** {1 sentence}

### Tier 2: EVALUATE (needs POC)
#### {Library Name}
- **What it might solve:** ...
- **POC must test:** [specific technical question]
- **Decision criteria:** [adopt if X, skip if Y]

### Tier 3: WATCH (trigger conditions)
#### {Library Name}
- **Becomes relevant when:** [specific project change]

### Tier 4: SKIP
| Reason | Libraries |
|--------|-----------|
| Incompatible version | lib1, lib2, lib3 |
| Archived/dead | lib4, lib5 |
| Out of scope | lib6, lib7, ... |

## {Special Interest Section}
[Dedicated answer to the user's specific sub-question. Ground in evidence.]

## Integration Notes
[For each ADOPT item: exact steps, files that change, version to pin]

## Coverage Gaps
[What the project needs that the ecosystem does not provide]

## Research Confidence
| Tier | Confidence | Basis |
|------|-----------|-------|
| ADOPT | High | All verified against primary sources |
| EVALUATE | Medium | README-level assessment, POC needed |
| WATCH | Low | Surface scan only |
| SKIP | High | Verified incompatible or clearly irrelevant |

[Note any claims that were not independently verified]
```

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

```
{project}/research/{topic}-v2/
├── context/                    # Facts extracted from v1 (NO opinions)
│   ├── project-brief.md       # Distilled from Tier 0 audits
│   ├── source-index.md        # The structured index (factual)
│   └── metadata-factsheet.md  # Raw metadata: versions, URLs, dates
├── tier1-landscape/            # Need-driven surveys
├── tier2-verification/         # Source-level deep-dives
└── synthesis/
    └── final-verdict.md
```

## Adapting to Different Domains

The tier system is domain-agnostic. The instantiation is domain-specific:

| Domain | Primary Source | Registry/DB | Verification Method |
|--------|---------------|-------------|---------------------|
| Software ecosystem | Awesome-list, ecosystem page | Package registry (crates.io, npm, PyPI) | Manifest inspection, source code, CI status, integration tests, latency measurements |
| Market landscape | Industry reports, review sites | Company databases (Crunchbase, etc.) | Pricing pages, SEC filings, user reviews |
| Academic field | Survey papers, conference procs | Citation databases (Semantic Scholar, etc.) | Paper retrieval, citation verification, replication data |
| Regulatory environment | Statute indices, agency sites | Legal databases (case law, regulations) | Primary statute text, enforcement actions, advisory opinions |

## Anti-Patterns

Ten failure modes observed in real multi-agent research sessions. The orchestrator checks for these before launching each tier and after scanning completion summaries.

**AP-1: Context Relay.** Reading reports into orchestrator context and relaying to next agent. Fix: point agents to file paths.

**AP-2: Premature Synthesis.** Launching synthesis before project audits (Tier 0) complete. Fix: block synthesis on ALL prior tiers including Tier 0.

**AP-3: README Trust.** Treating a library's README as evidence. Fix: Tier 3 agents fetch actual manifests, registry APIs, source code.

**AP-4: Model Waste.** Using sonnet for mechanical fetch-parse-write tasks. Fix: haiku for all mechanical work; sonnet only for synthesis and source-code reasoning.

**AP-5: Sequential Addiction.** Launching agents one at a time when they could run in parallel. Fix: all independent agents launch in a single message.

**AP-6: Hallucination Propagation.** Unchecked hallucinated claims reaching synthesis. Fix: spot-check extraordinary claims, Tier 4 contradiction resolution, synthesizer flags single-source unverified claims.

**AP-7: Scope Drift.** Agents wandering beyond their assigned category. Fix: name the exact index section and entries to assess.

**AP-8: Format Anarchy.** Each agent uses a different report format. Fix: paste the exact template into every prompt.

**AP-9: Orphaned Findings.** Breadth expansion finds significant candidates but no verifier is launched. Fix: scan summaries, launch verifiers for high-signal finds.

**AP-10: No Project Context in Survey Agents.** Agents assess relevance in a vacuum. Fix: include paths to project context files and instruct "assess based on ACTUAL needs."

### Pre-Launch Checklist

Before launching each tier:

- [ ] No agent prompt relays content from another agent's report (AP-1)
- [ ] All prior tiers complete, including project audits (AP-2)
- [ ] Verification agents instructed to check primary sources, not READMEs (AP-3)
- [ ] Agent model matches task: cheapest for mechanical, mid-tier for reasoning (AP-4)
- [ ] All independent agents launch in parallel within a single message (AP-5)
- [ ] Extraordinary claims from prior tiers have verification agents assigned (AP-6)
- [ ] Each agent's scope matches exactly one category/candidate (AP-7)
- [ ] Report format template pasted into every agent prompt (AP-8)
- [ ] Breadth-expansion high-signal finds have verification agents (AP-9)
- [ ] Survey agents receive project context file paths (AP-10)

Before launching synthesis:

- [ ] All contradictions resolved between reports
- [ ] Every ADOPT recommendation has a corresponding deep-dive report
- [ ] Synthesis agent's file list includes EVERY report from EVERY tier
- [ ] Synthesis prompt includes the user's original question
