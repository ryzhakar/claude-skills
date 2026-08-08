# Conventions

**Mutability:** living — a kernel enters when a rule is established and leaves when it is retired.
**Holds:** how to work in THIS project — commit discipline, forbidden patterns, code and data
anti-patterns, methodology, tooling rules — each as a kernel: the rule, a one-line why, the scope
it governs.
**Does not hold:** agent-harness and orchestration mechanics — dispatch, model tiers, worktrees,
return channels — which live in the orchestration skills; decisions (`decisions.md`); system
description (`capabilities.md`).
**Convention:** one bullet per rule. Name the files, commands, or directories the rule governs.

- **Versions live in `plugin.json` only.** One file per plugin is the source of truth, so skill and
  agent frontmatter carry no version field. Governs every `*/.claude-plugin/plugin.json` and every
  `SKILL.md` and agent `.md`.

- **Commits follow conventional format** — `type(scope): description`, type drawn from feat, fix,
  refactor, doc, test, chore, scope naming the plugin. The version bump ships in the same commit as
  the change it describes, so a version always points at its content. Governs every commit.

- **Every positive directive pairs with an explicit prohibition.** A skill that says "use X" without
  saying "never use Y" leaves a gap a loosely-prompted agent fills with its own invention. Governs
  skill and agent authorship; format (Hard Rules, "You do / You do NOT", Iron Law) is the author's
  choice.

- **Skill files use XML tags for structure.** Claude treats them as hard scope delimiters where
  markdown headers are soft hints. Tag names are imperative — `<launch_and_monitor>`, not `<role>`;
  inside a tag, prose, tables, and inline backticks only. Governs `*/skills/*/SKILL.md`.

- **Prefer Claude Code's native vocabulary.** Native terms are recognized faster than invented ones:
  launch over dispatch, agent over subagent, notification over completion summary, run in the
  background over blocking wait. Retain terms with no native equivalent — model ladder, tier,
  ARRIVE/WORK/LEAVE. Governs skill and agent text.

- **Guidance is authored by `instruction-writer`.** Skill definitions, agent definitions, and hook
  templates shape downstream agent behavior rather than producing code, so they go to
  `.claude/agents/instruction-writer.md` and never to an implementer. Governs every instruction file.

- **Hook output is prose.** Hooks inject into a model's context, and structured data — JSON, YAML
  fragments, labeled field lists — activates parsing circuits instead of comprehension. Shell scripts
  render parsed config into sentences. Governs `*/hooks/*.sh` and `*/hooks/templates/`.

- **A hook mandate is one unconditional command.** Conditional logic in the injection becomes an
  escape hatch the orchestrator can decline to parse; branching belongs in the receiving agent.
  Governs `*/hooks/templates/*.txt`.

- **Each orchestrator skill carries one inline `## Artifact Contract` table.** Paths drift silently
  when they scatter across agent bodies, and a single greppable table is the canonical map. Governs
  multi-skill plugins: `orchestration`, `dev-discipline`, `qa-automation`.

- **`just` is the measurement and generation surface.** `just tokens FILE` counts tokens,
  `just readme` regenerates every README after any frontmatter or plugin-metadata change, and
  `just check-readmes` fails on a stale one. Governs the repo root `justfile` and `generate.py`.

- **Fetch Claude Code docs as markdown.** Appending `.md` to a `code.claude.com/docs` URL returns the
  source instead of the JavaScript-rendered shell, so no browser or HTML parsing is needed. Governs
  every doc-extraction wave.

- **Anchor citations from a pre-computed heading index.** Build the index once with an awk pass over
  the fetched `.md` files and run the rewriter against the index, never against the sources, so the
  pass scales past a hundred citations without loading the corpus. Governs every citation-rewrite
  wave.

- **Binding preambles name a fallback source.** The `/tmp` manifesto clone is often absent when an
  agent starts, so every preamble pairs the local path with the raw GitHub URL as a required step.
  Governs every agent dispatch preamble.

- **This repo's constitution stack lives in `.manifestos.yaml`, grouped form.** `you:` binds the
  orchestrator and `subagents:` binds by agent type; a flat list at root binds the orchestrator only.
  Full schema: `manifesto/SCHEMA.md`. Governs the repo root config.
