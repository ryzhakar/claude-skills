# orchestration

Agent delegation framework, multi-agent research orchestration, and development lifecycle coordination. Decompose work across model tiers, manage parallel swarms, govern quality, and orchestrate the plan-implement-review-fix loop.

`orchestration` `delegation` `agents` `research` `parallel` `swarm` `development` `lifecycle` 
## Skills

### [agentic-delegation](skills/agentic-delegation/SKILL.md)

The universal framework for decomposing work into agent-delegated units across model tiers.
Use this skill whenever work can be broken into parts — research, implementation, review,
debugging, testing, auditing, exploration, writing, or any combination.

Core thesis: cheap agents are essentially free. Decompose aggressively, delegate everything,
assemble the results. A swarm of micro-agents almost always beats a single capable agent.

Triggers: "delegate", "parallelize", "fan out", "use agents for", "use subagents",
"run in parallel", "dispatch", "orchestrate this"; or any task with clearly
independent subtasks where delegating preserves the orchestrator's context window.


**References:** [`prompt-anatomy.md`](skills/agentic-delegation/references/prompt-anatomy.md) · [`quality-governance.md`](skills/agentic-delegation/references/quality-governance.md) · [`session-persistence.md`](skills/agentic-delegation/references/session-persistence.md)
---

### [dev-orchestration](skills/dev-orchestration/SKILL.md)

Extension of agentic-delegation for the software development lifecycle.
Adds the Plan→Implement→Review→Fix loop, dev-discipline agent orchestration,
TDD gates, status-driven branching, and debugging escalation.

Prerequisite: agentic-delegation (same plugin — must be read first).
Hard preference: dev-discipline plugin (implementer, spec-reviewer, code-quality-reviewer agents).

Triggers: "implement a feature end-to-end", "execute an implementation plan",
"build this with agents", "orchestrate development", "run the dev loop",
"implement using subagents", "dispatch implementers", "coordinate implementation and review".


**References:** [`agent-dispatch.md`](skills/dev-orchestration/references/agent-dispatch.md) · [`domain-context-examples.md`](skills/dev-orchestration/references/domain-context-examples.md) · [`lifecycle-loops.md`](skills/dev-orchestration/references/lifecycle-loops.md)
---

### [research-tree](skills/research-tree/SKILL.md)

Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes,
academic fields, regulatory environments, curated indices, or any domain requiring breadth-first
exploration followed by depth-first verification.

Triggers: "research an ecosystem", "survey the landscape", "evaluate options for", "deep-dive",
"compare alternatives", "map out what exists", "find the best X for Y", "audit the market",
"what should I use for", "what's available in", "how does X compare to Y across the field".

The orchestrator governs agents that write durable reports to disk. It never does the research
itself. Its context window is for decisions, detection, and dispatch — not content.


**References:** [`agent-templates.md`](skills/research-tree/references/agent-templates.md) · [`anti-patterns.md`](skills/research-tree/references/anti-patterns.md) · [`report-formats.md`](skills/research-tree/references/report-formats.md) · [`tier-playbook.md`](skills/research-tree/references/tier-playbook.md)
**Examples:** [`awesome-leptos-session.md`](skills/research-tree/examples/awesome-leptos-session.md)
---

### [session-close](skills/session-close/SKILL.md)

This skill should be used when the user asks to "close the session", "do session paperwork", "write the session record", "execute the LEAVE protocol", "wrap up the session", or at the natural end of a development orchestration session. Governs the full session close-out workflow including agent-based metric extraction from raw session data on disk, session record authoring, reference document updates, cost capture, and VCS commit.

**References:** [`data-schema.md`](skills/session-close/references/data-schema.md) · [`session-record-format.md`](skills/session-close/references/session-record-format.md)
**Scripts:** [`extract_metrics.py`](skills/session-close/scripts/extract_metrics.py)
---

