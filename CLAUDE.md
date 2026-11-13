> THIS DOCUMENT IS NOT A SUGGESTION - ALL OF THE BELOW ARE HARD REQUIREMENTS
> YOU ARE FORBIDDEN FROM EDITING THIS DOCUMENT IN ANY IMAGINABLE MANNER

@ETHOS.md
@orchestration_log/reference/ground-truth.md
@orchestration_log/reference/conventions.md
@.claude/memento.yaml

## Condition

Each session opens with no memory of the last. What is written here and in the records is all that carries over.

## Session start

1. Init: `memento:init`. Ground: the condition above.

## Goals

### Goal 1 · marketplace · standing · active

- object: Manage this repo as a claude marketplace consisting of plugins with skills, agents, and hooks.
- ground: owner, CLAUDE.md@9f879a0, 2026-10-21.
- constraints: The plugins target **Claude Code** (the CLI/IDE) first and foremost — not the Claude Agent SDK. Filter all research, guidance, and gap analyses for Claude Code semantics; mark SDK-only findings as out of scope.

## Prime directives

### Research

- Don't hesitate to launch the built-in claude code documentation agent on as much requests as you need. Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.
- Make use of plugin-dev:* skills and agents as much as possible. Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.

### Agent dispatch

- Every agent prompt must open with a constitution-binding preamble before the task body. List the relevant constitution elements by source path or URL. Instruct the agent to load each one completely from source, run the manifesto-oath binding protocol (deconstruct → map convergence/tension → activate operating mode), then proceed to the task. Subagents do not inherit the orchestrator's binding; they rebind from source on every dispatch. Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.
- Default stack for research and writing scouts: First Principles ("break the mold") — search the installed manifesto plugin's `manifestos/` folder: Glob `**/llm-manifestos/manifesto/*/manifestos/` below `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/`; Strunk SPR v3 — `https://raw.githubusercontent.com/ryzhakar/llm-manifestos/refs/heads/main/instructions/strunk_spr_v3_complete.xml` (fetch via Bash curl; WebFetch refuses verbatim reproduction). Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.
- Add per-domain elements (orchestration:agentic-delegation, dev-discipline:tdd, etc.) when the agent's task touches that domain. Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.

### Versioning

- Versions live in `plugin.json` only. Skill frontmatters do not carry version fields. Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.
- Never increment major versions without explicit user approval. Use minor (features) or patch (fixes) only. Ground: owner, CLAUDE.md@9f879a0, 2026-10-21.

### Commits

- Any scope of changes must be split into atomic parts. Atomic = irreducible, not merely motivated together. Ground: owner, CLAUDE.md@206cc64, 2026-09-18.
- Split a commit's scope by whether its parts could revert, bisect, or cherry-pick independently — never by shared cause. Ground: owner, CLAUDE.md@206cc64, 2026-09-18.
- One task touching two artifact classes (product code, its own docs/log, config, generated output, tests) is two commits, not one, unless one part is unintelligible without the other in the same diff. Ground: owner, CLAUDE.md@206cc64, 2026-09-18.
- Single-line conventional commit messages only, zero attribution. Capture as terse statements. Ground: owner, CLAUDE.md@206cc64, 2026-09-18.

### Compressed communication

- The project DEMANDS absolute token frugality - no compression level you think of is enough. Always strive for EVEN SHORTER answers. Lossiness in compression IS INEVITABLE AND ACCEPTED. Compress beyond the point of understanding. You may think i mean "up to the boundary" of understanding - not, that's not. I literally demand compression of user-facing communication BEYOND comprehension. Every additional token obscures meaning. Reveal clarity by cutting everything ruthlessly. Any communication gap is on me - i will ask if i don't understand. Ground: owner, CLAUDE.md@41e7ae0, 2026-09-18.

## Pointers

- Record map: `.claude/memento-map.md`.
- On need: `orchestration_log/reference/capabilities.md` (what the system is and does), `orchestration_log/reference/architecture_log.md` (how the core changed), `orchestration_log/reference/user_deferred_items.md` (what the owner put off).
