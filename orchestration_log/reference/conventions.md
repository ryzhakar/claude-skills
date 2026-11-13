# Conventions

**Mutability:** living — a kernel enters when a rule is established and leaves when it is retired.
**Holds:** how to work in THIS project — commit discipline, forbidden patterns, code and data
anti-patterns, methodology, tooling rules — each as a kernel: the rule, a one-line why, the scope
it governs.
**Does not hold:** agent-harness and orchestration mechanics — dispatch, model tiers, worktrees,
return channels — which live in the orchestration skills; core-shape changes
(`architecture_log.md`); system description (`capabilities.md`).
**Convention:** one block per rule under the schema's headings. Name the files, commands, or directories the rule governs in `when`.

## commit & merge

### versions-live-in-plugin-json
when    touching a plugin version, or the frontmatter of any skill or agent: every `*/.claude-plugin/plugin.json`, every `SKILL.md` and agent `.md`
do      keep the version in `plugin.json` only; skill and agent frontmatter carry no version field
why     one file per plugin is the source of truth
ground  541a9d3, the commit of 2026-04-14 that recorded this rule

### commits-follow-conventional-format
when    writing any commit
do      use `type(scope): description`, type drawn from feat, fix, refactor, doc, test, chore, scope naming the plugin; ship the version bump in the same commit as the change it describes
why     a version always points at its content
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### atomic-commit-one-irreducible-scope
when    a commit touches more than one plugin, or crosses plugin and `orchestration_log` boundaries
do      commit one irreducible scope per commit; split a plugin's own files (skills, agents, hooks, `plugin.json`) from `orchestration_log/reference/*` into separate commits even when one task changed both
never   bundle scopes into one commit
ground  5bab4e2, the commit of 2026-09-18 that recorded the atomic-commit scope-splitting rule

## code

### hook-output-is-prose
when    writing `*/hooks/*.sh` and `*/hooks/templates/`
do      emit prose; shell scripts render parsed config into sentences
never   inject structured data: JSON, YAML fragments, labeled field lists
why     hooks inject into a model's context, and structured data activates parsing circuits instead of comprehension
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### hook-mandate-is-one-unconditional-command
when    writing `*/hooks/templates/*.txt`
do      make a hook mandate one unconditional command; leave branching to the receiving agent
never   put conditional logic in the injection
why     conditional logic becomes an escape hatch the orchestrator can decline to parse
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### one-artifact-path-tag-per-orchestrator-skill
when    writing a multi-skill plugin: `orchestration`, `dev-cycle`, `dev-cycle-lite`, `qa-automation`; `qa-orchestration` still carries the older table form
do      carry one artifact-path tag per orchestrator skill, as the canonical map: `<fix-the-artifact-paths>` in `dev-cycle`, prose and inline backticks inside, as `memento:skill-creation` admits nothing else in a tag
why     paths drift silently when they scatter across agent bodies, and a single greppable tag is the canonical map
ground  a7c57c7, the commit of 2026-10-05 that recorded the artifact-path tag convention

### constitution-stack-in-manifestos-yaml-grouped-form
when    configuring the repo root config `.manifestos.yaml`, this repo's constitution stack; full schema in `manifesto/SCHEMA.md`
do      use the grouped form: `you:` binds the orchestrator and `subagents:` binds by agent type; a flat list at root binds the orchestrator only
ground  fe26145, the commit of 2026-08-08 that recorded this rule

## measuring & quoting

### just-is-the-measurement-and-generation-surface
when    measuring tokens or regenerating READMEs; governs the repo root `justfile` and `generate.py`
do      count tokens with `just tokens FILE`; regenerate every README with `just readme` after any frontmatter or plugin-metadata change; `just check-readmes` fails on a stale one
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### fetch-claude-code-docs-as-markdown
when    running any doc-extraction wave over `code.claude.com/docs`
do      append `.md` to the docs URL
why     it returns the source instead of the JavaScript-rendered shell, so no browser or HTML parsing is needed
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### anchor-citations-from-a-heading-index
when    running any citation-rewrite wave
do      build the index once with an awk pass over the fetched `.md` files, then run the rewriter against the index
never   run the rewriter against the sources
why     the pass scales past a hundred citations without loading the corpus
ground  fe26145, the commit of 2026-08-08 that recorded this rule

## reviewing & tests

### instruction-text-built-against-two-blind-checkers
when    building any `*/skills/*/SKILL.md`, agent definition, or hook template
do      have one agent write; one checker audit the draft against its governing standard; one checker read the draft alone and follow it literally on a case it invents, counting every point that forces a guess; open each report with `PENDING` on line one, replaced by a bare integer as the final edit; cap rounds at four, then ship the draft and record its open findings as residue
never   let either checker see the other's report or the author's reasoning
why     a checker that knows the intent stops reading what the text says, and the PENDING line distinguishes a file that exists from a check that finished
ground  37d7a08, the commit of 2026-09-17 that recorded the adversarial authoring protocol

### settled-ruling-goes-in-the-checkers-prompt
when    dispatching any checker
do      put a settled ruling in the checker's prompt
never   filter the checker's output for it
why     filtering after the fact spends a checker to produce findings already known to be struck; checkers carrying the rulings inline returned counts up to eight times cleaner on the same file
ground  37d7a08, the commit of 2026-09-17 that recorded the adversarial authoring protocol

### change-lands-after-independent-verification
when    editing shipped instruction text, including one-word edits and edits made under an owner ruling
do      land the change only after an agent that did not produce it verifies it
why     on 2026-09-17 three agents each edited their own file correctly and the contradiction existed only between them, which no single-file check could reach
ground  37d7a08, the commit of 2026-09-17 that recorded the adversarial authoring protocol

## writing craft

### every-positive-directive-pairs-with-a-prohibition
when    authoring any skill or agent instruction; format (Hard Rules, "You do / You do NOT", Iron Law) is the author's choice
do      pair every positive directive with an explicit prohibition
never   say "use X" without saying "never use Y"
why     a skill that says "use X" without "never use Y" leaves a gap a loosely-prompted agent fills with its own invention
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### skill-files-use-xml-tags-for-structure
when    writing `*/skills/*/SKILL.md`
do      structure the file with XML tags named imperatively, `<launch_and_monitor>` not `<role>`; inside a tag use prose, tables, and inline backticks only
why     Claude treats XML tags as hard scope delimiters where markdown headers are soft hints
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### prefer-claude-codes-native-vocabulary
when    writing skill and agent text
do      prefer native terms: launch over dispatch, agent over subagent, notification over completion summary, run in the background over blocking wait; retain terms with no native equivalent: model ladder, tier, ARRIVE/WORK/LEAVE
why     native terms are recognized faster than invented ones
ground  fe26145, the commit of 2026-08-08 that recorded this rule

## delegating agents

### guidance-is-authored-by-instruction-writer
when    producing any instruction file: skill definitions, agent definitions, hook templates
do      route it to `.claude/agents/instruction-writer.md`
never   route it to an implementer
why     instruction files shape downstream agent behavior rather than producing code
ground  fe26145, the commit of 2026-08-08 that recorded this rule

### binding-preambles-name-a-fallback-source
when    writing any agent dispatch preamble
do      pair the project-local manifesto clone (the `manifesto-repo` directory under `.claude`) with the raw GitHub URL as a required step
why     the clone can still be absent: a fresh dispatch outside any hooked session, a clone that failed offline
ground  fe26145, the commit of 2026-08-08 that recorded this rule

## owner

### owner-question-names-what-the-owner-recognizes
when    asking the owner any question; binds `memento:setup`, where the reader is a stranger to the system
do      name something the owner already recognizes: point at a file, a rule, or a sentence they made, and ask what should happen to it
never   carry internal vocabulary in a question
why     questions carrying internal vocabulary came back unparsed twice; the same questions rewritten to name a file the owner wrote were answered immediately
ground  37d7a08, the commit of 2026-09-17 that recorded the adversarial authoring protocol
