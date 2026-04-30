# orchestration

Agent delegation framework, multi-agent research orchestration, and session lifecycle. Decompose work across model tiers, manage parallel swarms, govern quality, and persist session state.

`orchestration` `delegation` `agents` `research` `parallel` `swarm` `session` `lifecycle` 
## Skills

### [agentic-delegation](skills/agentic-delegation/SKILL.md)

Decompose work into agent-delegated units across model tiers. Cheap agents are free —
decompose aggressively, delegate everything, assemble results.

Triggers: "delegate", "parallelize", "fan out", "dispatch", "orchestrate",
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

Captures context-dependent session state before compaction destroys it. Writes directly to session.md, deferred_items.md, codebase_state.md, and conventions.md — the same artifact paths session-close uses (A4, A6, A7, A8). Each invocation appends a timestamped section. session-close invokes checkpoint as Step 0 before adding computed data and close ceremony.
Triggers: "checkpoint", "save session state", "capture progress", "session-checkpoint", "snapshot the session", "save context".


---

### [session-close](skills/session-close/SKILL.md)

Governs the ARRIVE/WORK/LEAVE session lifecycle for orchestration sessions. Covers session start (reference doc ingestion), session work (convention adherence), and session close (checkpoint invocation, metric extraction, session record, reference updates, cost capture to gitignored cost.md, VCS commit).
Triggers: "close the session", "do session paperwork", "write the session record", "execute the LEAVE protocol", "wrap up the session", "start a session", "ARRIVE", "session lifecycle". Invoked ONLY when the user explicitly requests session close.


**Scripts:** [`extract_metrics.py`](skills/session-close/scripts/extract_metrics.py)
---

