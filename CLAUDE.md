Manage this repo as a claude marketplace consisting of plugins with skills, agents, and hooks. The plugins target **Claude Code** (the CLI/IDE) first and foremost — not the Claude Agent SDK. Filter all research, guidance, and gap analyses for Claude Code semantics; mark SDK-only findings as out of scope.
Don't hesitate to launch the built-in claude code documentation agent on as much requests as you need.
Make use of plugin-dev:* skills and agents as much as possible.

@ETHOS.md

## Agent dispatch

Every agent prompt must open with a constitution-binding preamble before the task body. List the relevant constitution elements by source path or URL. Instruct the agent to load each one completely from source, run the manifesto-oath binding protocol (deconstruct → map convergence/tension → activate operating mode), then proceed to the task. Subagents do not inherit the orchestrator's binding; they rebind from source on every dispatch.

Default stack for research and writing scouts:
- First Principles ("break the mold") — search `/tmp/claude-manifesto-repo/LLM_MANIFESTOS/manifestos/`
- Strunk SPR v3 — `https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml` (fetch via Bash curl; WebFetch refuses verbatim reproduction)

Add per-domain elements (orchestration:agentic-delegation, dev-discipline:tdd, etc.) when the agent's task touches that domain.

Default model tier: sonnet for any knowledge work (extraction, comparison, synthesis, judgment). Reserve haiku for mechanical/deterministic tasks only.

## Versioning

- Versions live in `plugin.json` only. Skill frontmatters do not carry version fields.
- Never increment major versions without explicit user approval. Use minor (features) or patch (fixes) only.
