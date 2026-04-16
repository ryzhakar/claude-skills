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

### [session-close](skills/session-close/SKILL.md)

Governs the ARRIVE/WORK/LEAVE session lifecycle for orchestration sessions. Covers session start (reference doc ingestion), session work (convention adherence), and session close (metric extraction, session record, reference updates, cost capture, VCS commit).
Triggers: "close the session", "do session paperwork", "write the session record", "execute the LEAVE protocol", "wrap up the session", "start a session", "ARRIVE", "session lifecycle"; or at the natural end of a development orchestration session. Also invoked by model when session persistence context is needed.


**Scripts:** [`extract_metrics.py`](skills/session-close/scripts/extract_metrics.py)
---

## Hooks

### ARRIVE Context Injection

Two hooks enforce the ARRIVE protocol — reading reference docs before any work begins.

| Event | Matcher | Script | Purpose |
|---|---|---|---|
| SessionStart | `startup\|resume` | `hooks/session-arrive.sh` | Inject reference doc paths at session start |
| PostCompact | `*` | `hooks/session-arrive.sh` | Re-inject after compaction wipes context |

Both gate on `orchestration_log/reference/` directory existence. Invisible when no orchestration session is active.

---

