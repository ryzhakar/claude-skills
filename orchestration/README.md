# orchestration

Domain-agnostic agent delegation framework and multi-agent research orchestration. Decompose work across model tiers, manage parallel swarms, and govern quality.

`orchestration` `delegation` `agents` `research` `parallel` `swarm` 
## Skills

### [agentic-delegation](skills/agentic-delegation/SKILL.md) `1.0.0`
The universal framework for decomposing work into agent-delegated units across model tiers.
Use this skill whenever work can be broken into parts — research, implementation, review,
debugging, testing, auditing, exploration, writing, or any combination.

Core thesis: cheap agents are essentially free. Decompose aggressively, delegate everything,
assemble the results. A swarm of micro-agents almost always beats a single capable agent.

Triggers: any multi-step task, any task where you'd "need to check something first",
any task with independent subtasks, any exploration, any audit, any research,
"delegate", "parallelize", "fan out", "use agents for".


**References:** [`prompt-anatomy.md`](skills/agentic-delegation/references/prompt-anatomy.md) · [`quality-governance.md`](skills/agentic-delegation/references/quality-governance.md) · [`software-engineering-examples.md`](skills/agentic-delegation/references/software-engineering-examples.md)
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

