# Agent Prompt Templates

Domain-adaptable prompt skeletons for every agent type in the research-tree workflow. Replace `{PLACEHOLDERS}` with concrete values for your research surface.

Each template encodes defensive-planning principles: one task per agent, explicit file paths, mandatory report format, named inputs.

---

## The Prime Directive Block

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

---

## Template: Index Parser (Tier 1)

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

**Model:** cheapest available
**Tools needed:** WebFetch, Write

---

## Template: Need-Category Surveyor (Tier 2)

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
[paste from references/report-formats.md — Category Survey Report template]

Assess ONLY candidates relevant to "{NEED_DESCRIPTION}". Do not drift into other needs.
```

**Model:** cheapest available (upgrade for nuanced compatibility assessment)
**Tools needed:** Read, WebFetch, WebSearch, Write

---

## Template: Project Auditor (Tier 0)

Three variants — launch all in parallel. Adapt to the project type.

### Capability/UI Auditor

```
You are auditing the capabilities and components of {PROJECT_PATH}.

TASK — use file reading and search tools extensively:

1. Find all {COMPONENT_TYPE} (e.g., components, modules, endpoints, pages).
   For each: file path, name, key features, patterns used.
2. Find all {INTERACTION_PATTERN} (e.g., forms, API calls, data flows).
   List: handler, fields/params, validation, error handling.
3. Identify repeated code patterns across {COMPONENT_TYPE}.
4. Read the main styling/config file. Catalog patterns and tokens.
5. Check for internationalization/localization state.
6. Identify pain points where external tools could reduce boilerplate.

Write to {REPORT_PATH}/deep-dives/project-capability-audit.md

Format: inventory table, pattern catalog, ranked pain points with file:line references.
```

### Dependency Auditor

```
You are auditing the dependency tree and build configuration of {PROJECT_PATH}.

TASK:
1. Read {MANIFEST_PATH} completely. Document every dependency with version.
2. Check {LOCKFILE_PATH} for resolved versions.
3. Map version constraints that would affect adding new dependencies.
4. Document the build system and dev workflow.
5. Identify any existing tooling for {RESEARCH_DOMAIN} (e.g., existing i18n, existing
   component libraries, existing testing tools).

Write to {REPORT_PATH}/deep-dives/project-deps-audit.md
```

### Architecture Auditor

```
You are auditing the architecture and developer experience of {PROJECT_PATH}.

TASK:
1. Find all {HANDLER_TYPE} (endpoints, server functions, controllers). Map: name, location, purpose.
2. Map routing/navigation structure with guards/middleware.
3. Catalog error handling patterns — is there consistency?
4. Map state management primitives.
5. Find code quality signals: TODOs, FIXMEs, lint suppressions, unsafe patterns.
6. Catalog test infrastructure: count, coverage patterns, gaps.
7. Rank DX gaps by impact.

Write to {REPORT_PATH}/deep-dives/project-arch-audit.md
```

**Model:** cheapest available (fact-finding from local files)
**Tools needed:** Read, Grep, Glob, Bash, Write

---

## Template: Candidate Verifier (Tier 3)

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
[paste from references/report-formats.md — Deep Verification Report template]
```

**Model:** cheapest for version checking; mid-tier for source-code reasoning
**Tools needed:** Read, Grep, WebFetch, WebSearch, Write

---

## Template: Breadth Expander (Tier 2)

```
You are searching for {DOMAIN} options NOT on the primary index.

{PRIME_DIRECTIVE_BLOCK}

TASKS:
1. Search registries and web:
   {SEARCH_URLS_AND_QUERIES}
2. Read the index at {REPORT_PATH}/index.md to know what's already listed.
3. For every find NOT in the index AND above {RELEVANCE_THRESHOLD}:
   — note name, version, adoption metrics, description, category
4. For high-signal finds, fetch their primary page for more details.

Write to {REPORT_PATH}/deep-dives/unlisted-{SOURCE}.md

Include: search methodology, high-signal finds (detailed), medium-signal finds (table),
landscape size stats, notable patterns.
```

**Model:** cheapest available
**Tools needed:** Read, WebFetch, WebSearch, Write

---

## Template: Contradiction Resolver (Tier 4)

```
CRITICAL VERIFICATION TASK: Two research reports make contradictory claims.

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

**Model:** cheapest available (primary source checking is mechanical)
**Tools needed:** WebFetch, WebSearch, Read, Write

---

## Template: Production/Real-World Inspector (Tier 2/3)

```
You are investigating what real-world {DOMAIN} practitioners actually use.

TASKS:
1. Fetch configuration/manifest files from these sources:
   {SOURCE_URLS}
2. For each successful fetch:
   — list all {DOMAIN}-relevant dependencies/tools/choices
   — note version pins and configuration patterns
3. Cross-reference: which choices appear in 2+ sources?

Write to {REPORT_PATH}/deep-dives/production-usage.md

Include: per-source breakdowns, cross-reference table, patterns, implications.
```

**Model:** cheapest available
**Tools needed:** WebFetch, Read, Write

---

## Template: Synthesizer (Tier 5)

```
You are writing the FINAL synthesis for the {TOPIC} research project.

CRITICAL: Synthesize FROM REPORTS, not from your own knowledge. Read every file listed below.
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
[paste from references/report-formats.md — Synthesis Report template]

Be OPINIONATED. Clear yes/no decisions, not diplomatic hedging. Cite report file paths
for every factual claim.
```

**Model:** strongest available
**Tools needed:** Read, Write

---

## Template Adaptation Checklist

When adapting these templates to a new domain:

- [ ] Replace all `{PLACEHOLDERS}` with concrete values
- [ ] Adapt registry/API URLs for the ecosystem (crates.io, npm, PyPI, Maven, NuGet, etc.)
- [ ] Adapt framework version checks for the target stack
- [ ] Add domain-specific constraint checks to verifier templates
- [ ] Name report files to match actual categories/candidates
- [ ] Use absolute file paths in all agent prompts
- [ ] Paste report format templates inline (agents can't read skill files)
- [ ] Include the prime directive block in every agent prompt
- [ ] Verify the synthesizer's file list covers EVERY report from EVERY tier
