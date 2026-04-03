# Tier Playbook

Decision criteria, agent heuristics, and completion gates for each research tier. Domain-agnostic — adapt the specifics to your research surface.

---

## Tier 0: Ground Truth (runs parallel with Tier 2)

### Purpose
Establish what the stakeholder actually has and needs. Without this, all recommendations float.

### When to Run
Always. Even if the project seems well-understood, audit agents discover things the orchestrator doesn't know: actual versions, hidden pain points, capability inventories, undocumented patterns.

### Agent Design

| Agent Role | Reads | Produces |
|------------|-------|----------|
| Capability Auditor | Source files, UI/component files, content files | Inventory of what exists, patterns used, repeated code |
| Dependency Auditor | Manifest files, lockfiles, config files | Dependency tree, version constraints, conflict risks |
| Architecture Auditor | Source files, config, routing, API definitions | Structure map, error handling patterns, integration points, DX gaps |

Use the cheapest model. These are fact-finding missions — read files, count things, catalog patterns.

### Agent Count
Typically 2-4 agents based on project complexity. Launch all in parallel at Tier 2 start.

### Completion Gate
All reports exist. Each contains:
- A quantified inventory (counts, not prose)
- Concrete findings with file:line references
- Ranked pain points section

### Common Failure
Shallow keyword search that misses patterns. Mitigate: instruct agents to READ files, not just grep keywords. "Read the file at {path}" not "search for {term}."

---

## Tier 1: Index

### Purpose
Parse the primary research source into a structured, cross-referenceable map.

### When to Run
Always. This is the entry point.

### Agent Design

| Agent Role | Reads | Produces |
|------------|-------|----------|
| Index Parser | Primary source (URL, document, corpus) | `index.md` with categories, entries, counts |

### Agent Count
1 agent. Must complete before Tier 2 starts.

### Completion Gate
`index.md` contains:
- Every category from the source
- Every entry with: name, URL/identifier, one-line description
- Statistics section with totals
- Category list (for orchestrator fan-out)

### Orchestrator Decision
Read ONLY the statistics/category list (last ~20 lines). Never read the full index into context. Fan-out needs the category list, not entry details.

---

## Tier 2: Survey

### Purpose
Broad assessment across the landscape, organized by stakeholder need.

### When to Run
After Tier 1 index is complete. Launches simultaneously with Tier 0 audits.

### Agent Design

| Agent Role | Reads | Produces |
|------------|-------|----------|
| Need-Category Surveyor | Index (relevant section), project context files | `categories/{need-slug}.md` |
| Breadth Expander | Index (for deduplication), external search results | `deep-dives/unlisted-{source}.md` |

### How to Define Need-Categories

Do NOT mirror the source's categories. Instead:
1. Read the stakeholder's research question
2. Decompose into the 3-7 decisions they need to make
3. Each decision becomes a need-category

Example: "Should I adopt a component library?" decomposes into: headless UI primitives, styling tools, form enhancement, data display, DX utilities — not the awesome-list's "Components, Libraries, Tools."

### Agent Count
- 1 surveyor per need-category (3-7 agents)
- 1-2 breadth expanders (registry search, web search)
- All launched in parallel

### Completion Gate
- One report per need-category
- Each report: per-entry analysis with activity, compatibility, relevance rating, assessment
- Breadth expansion reports list finds NOT in the original index

### Model Selection
Cheapest model for mechanical surveying. If a need-category requires nuanced judgment (e.g., assessing architectural compatibility), upgrade that specific agent.

---

## Tier 3: Verify

### Purpose
Deep verification of promising candidates against primary sources. Documentation claims become confirmed or refuted.

### When to Run
After Tier 2 surveys complete. Orchestrator scans completion summaries to identify candidates.

### Agent Design

| Agent Role | Reads | Produces |
|------------|-------|----------|
| Candidate Verifier | Primary sources (manifests, registries, source code) | `deep-dives/{candidate}.md` |
| New Find Verifier | Breadth expansion report, primary sources | `deep-dives/{new-find}.md` |

### What Triggers a Verification Agent

- Any candidate assessed as promising in a Tier 2 survey
- Any new find from breadth expansion above the relevance threshold
- Any extraordinary claim (high component count, massive adoption, production-ready status) — even if rated SKIP
- Anything the orchestrator notices in completion summaries that seems significant

### Verification vs. Summarization

Verification agents must be explicitly told:
> "This is NOT a documentation review. Fetch the actual manifest. Call the registry API. Read the source code. Documentation claims are hypotheses — your job is to confirm or refute them."

### Agent Count
1 per candidate. All launched in parallel.

### Model Selection
This is where model choice matters most. If the verification requires reasoning about type signatures, API compatibility, or cross-referencing multiple technical sources, use a mid-tier model. If it's just checking a version number in a manifest, cheapest model is fine.

### Completion Gate
Each report contains:
- Metadata from authoritative source (registry API, not README)
- Compatibility: VERIFIED / UNVERIFIED / INCOMPATIBLE — with primary-source evidence
- Project-specific integration assessment
- Risks with evidence
- Verdict with confidence level

---

## Tier 4: Resolve

### Purpose
Detect and resolve contradictions between reports.

### When to Run
After Tier 3. Orchestrator scans completion summaries for conflicts.

### Detection Strategy
Scan for:
- Same entity with different verdicts across reports
- Same entity described as "dead" by one agent and "active" by another
- Compatibility claims that disagree
- Feature/capability claims that contradict

### Agent Count
1 per contradiction. Often 0. Sometimes 1-3.

### Completion Gate
Each resolution report states:
- What the contradiction was
- What each original report claimed
- What PRIMARY SOURCE evidence shows
- Which claim is correct (or if both are partially correct)

### When to Skip
If no contradictions are detected in completion summaries, proceed directly to Tier 5.

---

## Tier 5: Synthesize

### Purpose
One capable agent reads ALL reports and produces the final research deliverable.

### When to Run
After all prior tiers complete and no unresolved contradictions remain.

### Agent Design

| Agent Role | Reads | Produces |
|------------|-------|----------|
| Synthesizer | Every report file, listed explicitly | `synthesis/recommendations.md` |

### Agent Count
1 agent. This is the capstone.

### Model Selection
Use the strongest available model for synthesis. This agent must reason across 10-25 reports, weigh conflicting evidence, and produce strategic recommendations. It earns the cost.

### Prompt Structure
The synthesis prompt MUST:
1. List every report file path (all of them)
2. Specify read order: ground-truth audits first, then index, surveys, verifications, resolutions
3. Include the report format template inline
4. Instruct: "Cite evidence from reports. If a claim is not in any report, do not include it."
5. State the stakeholder's original question and require a direct, definitive answer

### Completion Gate
Report contains:
- Executive summary answering the original question
- Tiered recommendations with evidence citations
- Dedicated section for the stakeholder's specific interest
- Integration notes for top-tier items
- Coverage gaps
- Research confidence assessment

### Common Failure
Synthesis agent skims and writes generic recommendations. Mitigate: require the agent to cite specific report files for each claim, and include a confidence section that forces acknowledgment of what wasn't verified.

---

## Tier Transition Decisions

### How Many Tiers?

| Research Need | Tiers Used | Rationale |
|--------------|-----------|-----------|
| Quick landscape scan | 1 → 2 → 5 | No candidates worth deep-diving |
| Standard evaluation | 0 + 1 → 2 → 3 → 5 | Index, survey, verify, synthesize |
| Deep assessment | 0 + 1 → 2 → 3 → 4 → 5 | Full pipeline with contradiction resolution |
| Multi-round deep assessment | Full first round → extract facts → full second round with better models | When first round is unreliable |

### When to Add Agents Within a Tier

- **New finds**: Breadth expansion surfaces significant unlisted candidates → launch Tier 3 verifiers
- **Extraordinary claims**: Agent claims something remarkable → launch verification even if rated SKIP
- **Missing context**: Survey agents need project details Tier 0 didn't cover → launch additional auditor

### When to Stop Early

- **Question answered**: Tier 2 unanimously shows no viable candidates → skip to synthesis with "nothing to adopt"
- **All candidates eliminated**: Tier 3 downgrades everything → skip Tier 4
- **Context budget**: Research consuming too much time/cost → synthesize with what exists, note gaps

### When to Launch a Second Round

- Multiple Tier 3 verdicts overturned Tier 2 assessments (first-round models unreliable)
- 2-4 candidates survived and each needs source-level scrutiny the first-round model can't provide
- A specific technical question (API compatibility, type system interaction) requires reading actual source code

Second-round setup: separate directory, higher-fidelity models, need-driven organization, inherit only facts from round one.
