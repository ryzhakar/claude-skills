# Orchestration Plugin — Maintainer Guide

Implicit decisions and structural invariants for anyone modifying skills in this plugin.

## Skill Hierarchy

```
agentic-delegation          <-- root (the universal framework)
  |
  +-- research-tree         <-- domain extension: research workflows
  |
  +-- dev-orchestration     <-- domain extension: development lifecycle
```

agentic-delegation is the parent. Everything else is a domain extension. This is not a flat collection of independent skills.

## The Hard Prerequisite Rule

Domain extensions MUST gate on the parent.

When dev-orchestration or research-tree is loaded, the model MUST read agentic-delegation's SKILL.md first. Not optional. Not "if available." A hard gate. The parent establishes the economics, the model ladder, the decomposition patterns, the prompt anatomy, the execution patterns, and the quality governance. Domain skills assume all of this is already internalized.

Both are in the same plugin. There is no scenario where a domain skill is present without its parent. All "if the agentic-delegation skill is available" language is wrong and must never appear.

## Composition Principles

### Cached Derivations, Not Overrides

When the parent's reasoning already reaches a conclusion for a specific domain, the domain skill caches that conclusion as shorthand. It does not override the parent.

Example: agentic-delegation's Implementation archetype prescribes sonnet for implementation ("requires reasoning about system constraints"). dev-orchestration's "default sonnet for implementers" is a cached derivation of this — the same conclusion, pre-derived so the model doesn't re-derive it in context every time.

If a domain skill appears to contradict the parent, one of two things is true:
1. The domain skill is wrong (most likely).
2. The domain has a justified deviation that must be explicitly acknowledged, traced to the parent rule it deviates from, and explained.

Silent divergence is a bug.

### Delta-Only Content

Domain skills contain ONLY what the parent does not cover:
- dev-orchestration adds: the Plan-Implement-Review-Fix loop, status-driven branching, TDD gates, debugging escalation, multi-unit integration.
- research-tree adds: tiered research structure, need-driven organization, re-research protocols.

If the parent already defines a pattern (speculative-parallel, fan-out-by-concern, map-reduce, prompt anatomy), the domain skill references it. It does not restate it. Not even as a summary.

**Why:** One source of truth. When the parent changes, domain skills automatically benefit. Restated copies silently diverge. Derivations break loudly.

### Reference Files Follow the Same Rule

Reference docs in domain skills (e.g., `agent-dispatch.md`, `lifecycle-loops.md`) contain domain-specific content only. If a reference file mostly restates the parent's content with minor domain adjustments, it should be reduced to the delta or removed.

## Cross-Plugin References

### Same Plugin (orchestration internals)

Always direct references. No "if available" guards. No fallback branches.

### External Plugins (e.g., dev-discipline)

dev-orchestration has a **hard preference** for the dev-discipline plugin (implementer, spec-reviewer, code-quality-reviewer agents). The pattern:

1. Reference the preferred agent by name.
2. If absent, recommend installing the dev-discipline plugin.
3. If installation isn't happening immediately, a single sentence fallback ("otherwise, construct an equivalent agent prompt") suffices.
4. No full fallback prompt templates. Those duplicate dev-discipline's agent definitions and diverge silently.

## The Orchestrator Contract

These invariants apply to ALL orchestration skills in this plugin.

### What the Orchestrator Does

- Reads status codes from completion summaries
- Pattern-matches on metadata shape (contradictions between summaries, anomalies, extraordinary claims, suspiciously short reports)
- Routes: maps status to next dispatch action via deterministic state machine
- Dispatches agents with precise, minimal prompts

### What the Orchestrator Does NOT Do

- Read implementation files, source code, or full agent reports
- Perform content-level analysis (classifying concerns, diagnosing root causes, evaluating trade-offs)
- Write code
- Debug failed agents by tracing their reasoning

Any analysis beyond reading a status code is itself work that must be re-delegated to agents, preferably in parallel.

### Communication Model

Agents communicate through artifacts on disk. The orchestrator routes via completion summaries.

What "artifact on disk" means varies by domain:
- **Research:** structured report files in a research directory
- **Dev:** changed source files, inspectable via git diff
- **Both:** the completion summary is the routing signal; the artifact is the substance

The orchestrator never relays content between agents. It provides file paths. Agents read files.

## Quality Governance

### The Parent's Governance

agentic-delegation defines general quality patterns: re-launch (don't debug), contradiction resolution (dispatch verification agents), spot-checking (sample-verify large batches). These are the default for any orchestration workflow.

### Domain Subsumption

Domain skills may define more structured quality gates that subsume the parent's general patterns for that domain:
- dev-orchestration's two-stage review (spec compliance then code quality) with 3-cycle loop limits subsumes the parent's general patterns for dev work.
- research-tree's tiered re-research with fresh-eyes isolation subsumes the parent's contradiction resolution for research work.

The parent's patterns remain authoritative for any orchestration context not covered by a domain skill's specific gates.

## Isolation Principle — When It Applies

agentic-delegation's isolation principle ("agents forming opinions must not see other agents' opinions") applies to **parallel agents independently evaluating the same question**.

It does NOT apply to:
- **Sequential pipeline stages** where one agent verifies another's work (implementer -> reviewer -> fixer). These are adversarial verification chains.
- **Tiered research** where higher-fidelity agents re-evaluate lower-fidelity findings. These get raw sources, not prior opinions — isolation is achieved by input design, not by hiding the prior agent's existence.

## Decomposition Units

Each domain has natural decomposition units. Do not force cross-domain mappings.

| Domain | Natural unit | Granularity heuristic |
|--------|-------------|----------------------|
| General (parent) | Time and output size | 30-120s, 20-200 lines of output |
| Research | Knowledge surface segment | One index category, one entity, one source |
| Dev | Files and testable behaviors | 1-3 files, independently testable, 2-10 minutes |

## Adding a New Domain Skill

When creating a new domain extension:

1. It MUST gate on reading agentic-delegation first.
2. Content is delta-only. Reference the parent for shared patterns.
3. Define domain-specific decomposition units if the parent's don't fit.
4. Define domain-specific quality gates if the parent's general governance is insufficient. Domain gates subsume, not layer.
5. Cached derivations of the parent's reasoning are encouraged as shorthand. Trace each to the parent rule it derives from.
6. Cross-plugin references use the hard-preference pattern (prefer, recommend install, succinct fallback).
