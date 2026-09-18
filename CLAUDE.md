> THIS DOCUMENT IS NOT A SUGGESTION - ALL OF THE BELOW ARE HARD REQUIREMENTS

Manage this repo as a claude marketplace consisting of plugins with skills, agents, and hooks. The plugins target **Claude Code** (the CLI/IDE) first and foremost — not the Claude Agent SDK. Filter all research, guidance, and gap analyses for Claude Code semantics; mark SDK-only findings as out of scope.
Don't hesitate to launch the built-in claude code documentation agent on as much requests as you need.
Make use of plugin-dev:* skills and agents as much as possible.

@ETHOS.md

## Agent dispatch

Every agent prompt must open with a constitution-binding preamble before the task body. List the relevant constitution elements by source path or URL. Instruct the agent to load each one completely from source, run the manifesto-oath binding protocol (deconstruct → map convergence/tension → activate operating mode), then proceed to the task. Subagents do not inherit the orchestrator's binding; they rebind from source on every dispatch.

Default stack for research and writing scouts:
- First Principles ("break the mold") — search `.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/`
- Strunk SPR v3 — `https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml` (fetch via Bash curl; WebFetch refuses verbatim reproduction)

Add per-domain elements (orchestration:agentic-delegation, dev-discipline:tdd, etc.) when the agent's task touches that domain.

## Versioning

- Versions live in `plugin.json` only. Skill frontmatters do not carry version fields.
- Never increment major versions without explicit user approval. Use minor (features) or patch (fixes) only.

## Commits

Single-line conventional commits only, zero attribution. Capture as terse statements.

## Compressed communication

The project DEMANDS absolute token frugality - no compression level you think of is enough.
Always strive for EVEN SHORTER answers. Lossiness in compression IS INEVITABLE AND ACCEPTED.
Compress beyond the point of understanding. You may think i mean "up to the boundary" of understanding - not, that's not.
I literally demand compression of user-facing communication BEYOND comprehension.
Every additional token obscures meaning. Reveal clarity by cutting everything ruthlessly.
Any communication gap is on me - i will ask if i don't understand.

