# orchestration

Agent delegation framework, multi-agent research orchestration, and session lifecycle. Decompose work across model tiers, manage parallel swarms, govern quality, and persist session state.

`orchestration` `delegation` `agents` `research` `parallel` `swarm` `session` `lifecycle` 
## Skills

### [agentic-delegation](skills/agentic-delegation/SKILL.md)

Decompose work into agent-delegated units across model tiers. Agents are cheap,
context is expensive — decompose aggressively, delegate everything, assemble results.

Triggers: "delegate", "parallelize", "parallel launch", "launch", "orchestrate",
"use agents for", "run in parallel"; or any task with independent subtasks.


---

### [research-tree](skills/research-tree/SKILL.md)

Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes,
academic fields, regulatory environments, curated indices, or any domain requiring breadth-first
exploration followed by depth-first verification.

Triggers: "research an ecosystem", "survey the landscape", "evaluate options for", "deep-dive",
"compare alternatives", "map out what exists", "find the best X for Y", "audit the market",
"what should I use for", "what's available in", "how does X compare to Y across the field".


**Examples:** [`awesome-leptos-session.md`](skills/research-tree/examples/awesome-leptos-session.md)
---

### [session-checkpoint](skills/session-checkpoint/SKILL.md)

Flushes decisions not yet written and brings the session record current. Two functions, nothing else: append any decision made this session that is missing from orchestration_log/reference/decisions.md, and append to orchestration_log/history/${DATE}/session.md what has happened since its last write — phases completed, work in flight, and current direction.
Triggers: "checkpoint", "save session state", "capture progress", "session-checkpoint", "snapshot the session", "save context".


---

### [session-close](skills/session-close/SKILL.md)

Runs the LEAVE protocol: verify memory completeness, then commit. Six ordered steps — verify the .gitignore patterns, finalize orchestration_log/history/${DATE}/failures.md, dispatch a verification sweep across the five living files, dispose every finding by direct write, finalize orchestration_log/history/${DATE}/session.md, commit orchestration_log/. Optional telemetry follows: session metrics, verbatim /cost into gitignored cost.md, orphan-script sweep.
Triggers: "close the session", "do session paperwork", "write the session record", "execute the LEAVE protocol", "wrap up the session", "session-close". Invoked ONLY when the user explicitly requests session close.


**Scripts:** [`extract_metrics.py`](skills/session-close/scripts/extract_metrics.py)
---

