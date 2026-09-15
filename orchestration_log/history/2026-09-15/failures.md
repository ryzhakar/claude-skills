# Failures 2026-09-15

## 00:07 — Safety-net liveness check returned a false hang
Root cause: `agentic-delegation` `<ensure_liveness>` prescribes `ls -la` on the agent output file, but the harness exposes that path as a symlink into `~/.claude/projects/${PROJECT}/${SESSION}/subagents/agent-${ID}.jsonl`. `ls -la` reports the 142-byte link and never the transcript behind it, so the check reads constant regardless of agent state — a false hang on every dispatch.
Correction: re-sampled with `ls -laL` before acting; both scouts were live and growing (+87KB and +143KB across the window). No agent was stopped; roughly 830KB of accumulated work preserved. Skill fix pending: `<ensure_liveness>` must prescribe `ls -laL`.

## 00:20–00:31 — Stance-report writer hung after initialization
Root cause: undiagnosed. Transcript reached 562381 bytes at dispatch and took zero further bytes across 10.5 minutes; the output directory was never created. Distinguishing shape versus a live agent: steady growth between samples means alive, a large initialization burst followed by a flat line does not. Suspects not ruled out — three blocking constitution fetches without `--max-time`, and four full input reads before the first write.
Correction: killed after two samples showed zero delta, never on a single reading. Relaunched hardened — `mkdir -p` as step 1, fetches capped at 20s with a fail-and-proceed rule, input set cut from four files to the two recon reports, and the write ordered before polishing. No evidence lost; both scout reports were already on disk.
Superseded 00:41 — the diagnosis below shows this agent was probably not hung and the kill was wrong.

## 00:41 — Transcript-size liveness cannot see an agent that is generating
Root cause: the subagent JSONL grows per completed message, not per token. An agent whose final act is composing a long document writes nothing to its transcript for the whole generation — the flat line appears exactly during the most productive phase. Both "hangs" this session shared that shape: initialization burst, then flat immediately after the last input read. `TaskOutput` on the relaunched agent returned `status: running` with its last transcript event at 00:32, the moment it finished reading input 2, with the write step still ahead of it.
Correction: the first writer was killed at 10.5 minutes flat and was probably mid-generation; its output was destroyed and the work redone. The second was left alone. Size deltas answer "is the process alive" and never "is the agent working" — an agent past its last read needs a progress check, not another size sample. Both mechanisms are named in `agentic-delegation` `<ensure_liveness>`; nothing there says which one a generating agent requires.

## 00:41 — TaskOutput on a local_agent flooded orchestrator context
Root cause: called `TaskOutput` to get a progress snapshot on a `local_agent` task. The tool is deprecated for that type and its own description forbids it — the `.output` path is a symlink to the full subagent transcript. It returned the complete 204-line history report plus JSONL envelope.
Correction: none available; the tokens are spent and permanent. The deprecation notice was in the loaded schema and was read past. No non-flooding progress check for a `local_agent` was identified this session.
