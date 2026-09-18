# Ground Truth

**Mutability:** changes on owner override only, written in the turn the override lands.
**Holds:** the problem this project solves — task definition, success criterion, data sources,
evaluation protocol, and the constraints the owner has fixed.
**Does not hold:** what the system currently is (`capabilities.md`), how its core changed
(`architecture_log.md`), how to work here (`conventions.md`).
**Convention:** facts only, no recommendations. Every claim here is one the owner set or confirmed.

## The task

Build and maintain a Claude Code plugin marketplace. Its units are plugins; a plugin carries skills,
agents, and hooks. `.claude-plugin/marketplace.json` at the repo root lists every published plugin.

The plugins target Claude Code — the CLI, desktop, and IDE product — and not the Claude Agent SDK.
Research, guidance, and gap analyses are filtered for Claude Code semantics. SDK-only findings are
out of scope and are marked as such.

## Success criterion

A fresh reader executes a skill's workflow from the skill text alone, without following references
and without supplying implied knowledge. Skills produce file artifacts on disk; the owner decides
where those artifacts are published.

A change lands after an agent that did not produce it verifies it against the specification.
Measurement replaces assertion: token claims are measured, not estimated.

## Fixed constraints

- Major version increments require explicit owner approval. Minor and patch increments do not.
- Instruction text states policy without arguing for it. The argument belongs in the maintainer
  record, never in the shipped instruction.
- Every agent dispatch opens with a constitution-binding preamble naming its elements by source path
  or URL and demanding visible binding output. Subagents inherit no binding from the orchestrator;
  they rebind from source on every dispatch.
- Sonnet is the floor for knowledge work — extraction, comparison, synthesis, judgment. Haiku takes
  mechanical, deterministic tasks only.
- The full authoring standard is `CLAUDE.md` and `ETHOS.md` at the repo root, loaded into every
  session by the harness.

## Data sources

- Claude Code platform documentation at `code.claude.com/docs`, and the built-in `claude-code-guide`
  agent, which the owner directs sessions to use freely.
- The `plugin-dev:*` skills and agents, which the owner directs sessions to prefer over reinvented
  patterns.
- The constitution repository `ryzhakar/LLM_MANIFESTOS`. First Principles and Strunk SPR v3 are the
  default stack for research and writing agents; per-domain elements are added by task.
- Field reports from the downstream consumer `competera/embedding_finetuning_for_ecommerce`, which
  observes how the shipped plugins behave inside a working project.
