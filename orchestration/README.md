# orchestration

Agent delegation framework, multi-agent research orchestration, and development lifecycle coordination. Decompose work across model tiers, manage parallel swarms, govern quality, and orchestrate the plan-implement-review-fix loop.

`orchestration` `delegation` `agents` `research` `parallel` `swarm` `development` `lifecycle` 
## Skills

### [agentic-delegation](skills/agentic-delegation/SKILL.md) `1.0.0`
The universal framework for decomposing work into agent-delegated units across model tiers.
Use this skill whenever work can be broken into parts — research, implementation, review,
debugging, testing, auditing, exploration, writing, or any combination.

Core thesis: cheap agents are essentially free. Decompose aggressively, delegate everything,
assemble the results. A swarm of micro-agents almost always beats a single capable agent.

Triggers: "delegate", "parallelize", "fan out", "use agents for", "use subagents",
"run in parallel", "dispatch", "orchestrate this"; or any task with clearly
independent subtasks where delegating preserves the orchestrator's context window.


**References:** [`prompt-anatomy.md`](skills/agentic-delegation/references/prompt-anatomy.md) · [`quality-governance.md`](skills/agentic-delegation/references/quality-governance.md)
---

### [dev-orchestration](skills/dev-orchestration/SKILL.md) `1.0.0`
This skill should be used when the user asks to "implement a feature end-to-end",
"execute an implementation plan", "build this with agents", "orchestrate development",
"run the dev loop", "implement using subagents", "dispatch implementers",
"coordinate implementation and review", or when a multi-step development task
requires planning, implementation, review, and iteration as a coordinated workflow.

Governs the full plan-implement-review-fix development lifecycle by orchestrating
dev-discipline agents (implementer, spec-reviewer, code-quality-reviewer) and skills
(defensive-planning, tdd, systematic-debugging, receiving-code-review) into a
coherent execution workflow with quality gates and status-driven branching.


**References:** [`agent-dispatch.md`](skills/dev-orchestration/references/agent-dispatch.md) · [`lifecycle-loops.md`](skills/dev-orchestration/references/lifecycle-loops.md) · [`software-engineering-examples.md`](skills/dev-orchestration/references/software-engineering-examples.md)
---

### [research-tree](skills/research-tree/SKILL.md) `2.0.0`
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

