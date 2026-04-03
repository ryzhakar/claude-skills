# Report Formats

Standardized markdown templates for every report type. Consistent formats allow the Tier 5 synthesizer to cross-reference findings reliably.

---

## Index Report (`index.md`)

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

**Required fields:** Every entry must have name, URL, and description. No partial entries.

---

## Category Survey Report (`categories/{slug}.md`)

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

**Required fields per entry:** URL, activity indicator, version compatibility, relevance, recommendation. Entries with missing fields indicate the agent failed to fetch.

**Rating scale:**
- **ADOPT** — clear value, verified compatibility, worth integrating
- **EVALUATE** — promising but needs a proof-of-concept or has a specific uncertainty
- **SKIP** — assessed and rejected (state why: incompatible, dead, out of scope, etc.)

---

## Deep Verification Report (`deep-dives/{candidate}.md`)

```markdown
# {Candidate Name} — Deep Technical Verification

## Metadata
- **Registry:** {url to crates.io / npm / etc.}
- **Latest version:** {version}
- **Framework dependency:** {exact version or range from manifest}
- **Downloads:** {total} total / {recent} recent
- **Last publish:** {date}
- **License:** {license}

## {Framework} {Version} Compatibility
**{VERIFIED / UNVERIFIED / INCOMPATIBLE}**

Evidence: {exact line from manifest file showing the dependency version}

## {Constraint 1, e.g., "SSR + Hydration Support"}
**{VERIFIED / UNVERIFIED / INCOMPATIBLE}**

Evidence: {what was found}

## {Constraint 2, e.g., "Tailwind v4 Compatibility"}
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
2. {Risk 2 with evidence}

## Verdict
**{ADOPT / DEFER / SKIP}** — Confidence: {high / medium / low}

{2-3 sentences justifying the verdict}
```

**Verification levels:**
- **VERIFIED** — primary source (manifest, source code, registry API) confirms the claim
- **UNVERIFIED** — only README/docs support the claim; no primary source checked
- **INCOMPATIBLE** — primary source contradicts compatibility

---

## Project Audit Report (`deep-dives/project-{aspect}-audit.md`)

```markdown
# Project {Aspect} Audit

## {Inventory Section}
[Table or list of everything found. Quantified.]

| Item | Location | Properties |
|------|----------|------------|
| ... | file:line | ... |

## {Pattern Section}
[Recurring patterns found, with frequency counts]

## {Gap/Pain Point Section}
[Ranked by impact. Each entry: description, severity, affected files, potential fix]

| # | Pain Point | Severity | Files Affected | Fix Category |
|---|-----------|----------|----------------|--------------|
| 1 | ... | HIGH/MEDIUM/LOW | N files | library / refactor / new code |
```

**Required:** At least one inventory table, at least one quantified finding, ranked pain points.

---

## Contradiction Resolution Report (`deep-dives/{topic}-resolution.md`)

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

### Check 2: {what was checked}
[repeat]

## Verdict
**{Report A is correct / Report B is correct / Both partially correct / Both wrong}**

Evidence summary: {2-3 sentences}

## Impact on Recommendations
[How this resolution changes the adoption recommendation, if at all]
```

---

## Synthesis Report (`synthesis/recommendations.md`)

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
| Architectural mismatch | lib6, lib7 |
| Out of scope | lib8, lib9, lib10, ... |

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

---

## Format Enforcement

When writing agent prompts, paste the relevant format template directly into the prompt. The agent must produce output matching the template. Deviations indicate the agent misunderstood the task — in that case, the report should be flagged for re-execution, not accepted.

Cross-referencing between reports works because:
1. Every entry uses the same name across reports (from the index).
2. Every verdict uses the same scale (ADOPT/EVALUATE/SKIP with VERIFIED/UNVERIFIED/INCOMPATIBLE).
3. Every report references source files by absolute path.
4. Every quantified finding uses the same units (stars, downloads, file counts).
