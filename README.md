# my-claude-skills

33 skills · 14 agents across 12 plugins

## Plugins

| Plugin | Description | Version | Components |
|--------|-------------|---------|------------|
| [agent-conduct](agent-conduct/) | Domain-free skills governing how an agent conducts itself while working,... | `1.2.1` | 2S |
| [dev-cycle](dev-cycle/) | Development cycle orchestration: specify, plan, implement, review,... | `1.0.0` | 1S 4A |
| [dev-cycle-lite](dev-cycle-lite/) | Cost-tiered development cycle over dev-cycle: an opus prescriber writes... | `1.0.0` | 2S 3A |
| [dev-discipline](dev-discipline/) | Software engineering discipline skills, agent-agnostic: outermost-test-first... | `3.0.0` | 5S |
| [manifesto](manifesto/) | Create concentrated manifesto declarations and bind Claude behavior to... | `3.2.0` | 2S 1A |
| [memento](memento/) | A memory and record-keeping system for agents without continuity across sessions. | `0.5.1` | 13S |
| [orchestration](orchestration/) | Agent delegation framework and multi-agent research orchestration. Decompose... | `5.0.0` | 2S |
| [product-craft](product-craft/) | Product definition skills: extract specs from stakeholders, write user... | `1.1.0` | 2S |
| [prompt-engineering](prompt-engineering/) | Evaluate and optimize Claude system prompts using Anthropic-grounded patterns. | `2.0.0` | 0S 2A |
| [python-tools](python-tools/) | Python development tooling: debug type errors in uv-managed projects with... | `1.1.0` | 2S |
| [qa-automation](qa-automation/) | Playwright test lifecycle orchestrator. One skill drives the full loop: plan... | `3.2.0` | 1S 4A |
| [userland-utilities](userland-utilities/) | Practical utilities for common desktop and system tasks. Includes macOS app... | `1.0.0` | 1S |

---

## [agent-conduct](agent-conduct/) `1.2.1`

Domain-free skills governing how an agent conducts itself while working, independent of orchestration, memory, or any specific engineering domain.

### Skills

- **[check-back](agent-conduct/skills/check-back/SKILL.md)** — Before ending a turn that leaves a run pending, set the agent's own next wake, and on waking look at what was pending. "check back",...
- **[work-silently](agent-conduct/skills/work-silently/SKILL.md)** — Keep working while writing nothing to the conversation, except answers to the user's own messages, until the user says to stop....
## [dev-cycle](dev-cycle/) `1.0.0`

Development cycle orchestration: specify, plan, implement, review, integrate. A spec-capturer that interviews the owner, worktree-isolated implementers, spec and code-quality reviewers, and a review chain enforced by hooks.

### Skills

- **[dev-cycle](dev-cycle/skills/dev-cycle/SKILL.md)** — Drive the specify, plan, implement, review, and integrate loop over software work through the spec-capturer, implementer, spec-reviewer,...
### Agents

- **[code-quality-reviewer](dev-cycle/agents/code-quality-reviewer.md)** (`inherit`) — Review the quality of a unit's changed code against the tdd skill's rules and the design checks below, and write a...
- **[implementer](dev-cycle/agents/implementer.md)** (`inherit`) — Use this agent to implement one unit from an implementation plan, carry out a well-specified coding task, or run a...
- **[spec-capturer](dev-cycle/agents/spec-capturer.md)** (`inherit`) — Interview the owner through the AskUserQuestion tool, by the spec-chef skill's protocol, and turn a request into one...
- **[spec-reviewer](dev-cycle/agents/spec-reviewer.md)** (`inherit`) — Verify that an implementation in a worktree matches its specification and write a verdict file reading PASS or FAIL....

## [dev-cycle-lite](dev-cycle-lite/) `1.0.0`

Cost-tiered development cycle over dev-cycle: an opus prescriber writes prescriptions that leave no decision, a sonnet suborchestrator runs the loop and both reviews, disposable haiku executors follow the prescription literally. No hooks.

### Skills

- **[lite-cycle](dev-cycle-lite/skills/lite-cycle/SKILL.md)** — Run the dev-cycle loop over one spec at the lowest cost tier — an opus prescriber writes a prescription per unit, disposable haiku...
- **[prescriptive-planning](dev-cycle-lite/skills/prescriptive-planning/SKILL.md)** — Write a prescription — an implementation plan, or a correction plan after a failed review, that leaves the executor — the agent that...
### Agents

- **[executor](dev-cycle-lite/agents/executor.md)** (`haiku`) — Execute one prescription — a plan fixing every file, signature, test, and command — literally, inside its own git...
- **[prescriber](dev-cycle-lite/agents/prescriber.md)** (`opus`) — Write a prescription — an implementation plan leaving the executor no decision, no option, and no signature — for...
- **[suborchestrator](dev-cycle-lite/agents/suborchestrator.md)** (`sonnet`) — Run the lite cycle — plan, prescribe, execute, review, integrate — over one spec as a sonnet agent beneath the main...

## [dev-discipline](dev-discipline/) `3.0.0`

Software engineering discipline skills, agent-agnostic: outermost-test-first signature-first TDD, systematic debugging, bug triage, architecture improvement, and receiving code review. Used ad hoc or by dev-cycle.

### Skills

- **[improve-architecture](dev-discipline/skills/improve-architecture/SKILL.md)** — Find architectural friction — places where understanding a codebase breaks down — explore in parallel several designs for a deepened...
- **[receiving-code-review](dev-discipline/skills/receiving-code-review/SKILL.md)** — Act on code review feedback — each item being one change a reviewer asks for, so a comment asking for two changes holds two items — by...
- **[systematic-debugging](dev-discipline/skills/systematic-debugging/SKILL.md)** — Find the root cause of a bug, a test failure, an error, or an unexpected behavior before changing any code, then fix the cause once....
  Scripts: [`find-polluter.sh`](dev-discipline/skills/systematic-debugging/scripts/find-polluter.sh)
- **[tdd](dev-discipline/skills/tdd/SKILL.md)** — Build code by writing one failing test through the surface its callers use before any code, designing the functions beneath that surface...
- **[triage-issue](dev-discipline/skills/triage-issue/SKILL.md)** — Diagnose a reported bug to its root cause and write an issue document carrying a test-first fix plan, without fixing the code. "triage...
## [manifesto](manifesto/) `3.2.0`

Create concentrated manifesto declarations and bind Claude behavior to user-provided manifestos through identity-assumption protocols.

### Skills

- **[manifesto-oath](manifesto/skills/manifesto-oath/SKILL.md)** — Binds Claude's operating identity to constitutions, manifestos, and principle sets through identity construction — not theatrical oaths....
- **[manifesto-writing](manifesto/skills/manifesto-writing/SKILL.md)** — Trigger when users request manifestos or manifesto tone. Name the enemy, strip hedging, compress to sharp distinctions, end with stark choice.
### Agents

- **[maximalist-reviewer](manifesto/agents/maximalist-reviewer.md)** (`inherit`) — Review a set of files against one manifesto at the manifesto's strongest literal reading, with no allowance for...

## [memento](memento/) `0.5.1`

A memory and record-keeping system for agents without continuity across sessions.

### Skills

- **[authority-check](memento/skills/authority-check/SKILL.md)** — Classify content by who authored it and by the channel that supplied it, apply the rank, and refuse what the rank refuses. "who wrote...
- **[corpus-reconciliation](memento/skills/corpus-reconciliation/SKILL.md)** — Audit every record one project holds against the index over them, then repair each mismatch found. "audit the records", "reconcile the...
- **[event-capture](memento/skills/event-capture/SKILL.md)** — Write a trace — a dated note of one event, an event being a happening of a kind schema-resolution names, fixed once written — into the...
- **[init](memento/skills/init/SKILL.md)** — Read the two skills this system is entered by, follow every skill either one names to the end of the chain, and run the waking check....
- **[owner-ruling](memento/skills/owner-ruling/SKILL.md)** — Carry out a ruling — what the owner, the human whose project this is, rules about content in quarantine, the status that holds a record...
- **[pat-down](memento/skills/pat-down/SKILL.md)** — Re-derive what is true about a project from its written records, inheriting nothing. Session start, resumed or interrupted work, a...
- **[record-promotion](memento/skills/record-promotion/SKILL.md)** — Move a record — a written statement kept past its making — up one tier, a storage class in a fixed order, through that tier's gate, the...
- **[record-writing](memento/skills/record-writing/SKILL.md)** — Write one record — a written statement kept on a durable location, made to outlast the work that wrote it. "write this down", "record...
- **[schema-resolution](memento/skills/schema-resolution/SKILL.md)** — Establish the one schema in force: the shape a project declares for its records — the written statements it keeps. Before a record is...
- **[setup](memento/skills/setup/SKILL.md)** — Explain this memory system to the person whose project it is, place what that project already wrote into it, and write the configuration...
- **[skill-creation](memento/skills/skill-creation/SKILL.md)** — Create a skill — text to be read and followed. "create a skill", "write a skill", "new skill", "add a skill", "make this repeatable", or...
- **[span-closure](memento/skills/span-closure/SKILL.md)** — Close out a stretch of work — one continuous thread of narrative — flushing, summarizing, and auditing what it leaves behind. The end of...
- **[staging-relay](memento/skills/staging-relay/SKILL.md)** — Pair every part of a task that outlives the work at hand with a record and a waking cause — what begins the later work — and bound every...
## [orchestration](orchestration/) `5.0.0`

Agent delegation framework and multi-agent research orchestration. Decompose work across model tiers, manage parallel swarms, and govern quality.

### Skills

- **[agentic-delegation](orchestration/skills/agentic-delegation/SKILL.md)** — Decompose work into agent-delegated units across model tiers. Agents are cheap, context is expensive — decompose aggressively, delegate...
- **[research-tree](orchestration/skills/research-tree/SKILL.md)** — Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes, academic fields, regulatory...
  Examples: [`awesome-leptos-session.md`](orchestration/skills/research-tree/examples/awesome-leptos-session.md)
## [product-craft](product-craft/) `1.1.0`

Product definition skills: extract specs from stakeholders, write user stories, and establish ubiquitous language.

### Skills

- **[spec-chef](product-craft/skills/spec-chef/SKILL.md)** — Extracts implicit product decisions from stakeholders into durable artifacts through systematic gap detection and constrained...
- **[user-story-chef](product-craft/skills/user-story-chef/SKILL.md)** — Writes user stories as value negotiation units, not template-filling exercises. Triggers: writing user stories, acceptance criteria,...
## [prompt-engineering](prompt-engineering/) `2.0.0`

Evaluate and optimize Claude system prompts using Anthropic-grounded patterns.

### Agents

- **[prompt-eval](prompt-engineering/agents/prompt-eval.md)** (`sonnet`) — Evaluate a Claude system prompt against a structured rubric. Use when asked to "evaluate a prompt", "review a system...
- **[prompt-optimize](prompt-engineering/agents/prompt-optimize.md)** (`sonnet`) — Optimize a Claude system prompt by applying improvement patterns. Use when asked to "improve this prompt", "optimize...

## [python-tools](python-tools/) `1.1.0`

Python development tooling: debug type errors in uv-managed projects with pyright, and perform AST-based mass structural edits across codebases.

### Skills

- **[python-ast-mass-edit](python-tools/skills/python-ast-mass-edit/SKILL.md)** — Systematic workflow for AST-based mass edits in Python codebases. Use when editing 3+ files with structural changes (decorators,...
  Scripts: [`template_transformer.py`](python-tools/skills/python-ast-mass-edit/scripts/template_transformer.py)
- **[uv-pyright-debug](python-tools/skills/uv-pyright-debug/SKILL.md)** — Debug type errors in uv-managed Python projects by accessing true pyright diagnostics. Use when IDE shows type errors but standalone...
  Scripts: [`analyze_errors.py`](python-tools/skills/uv-pyright-debug/scripts/analyze_errors.py), [`line_index_errors.py`](python-tools/skills/uv-pyright-debug/scripts/line_index_errors.py)
## [qa-automation](qa-automation/) `3.2.0`

Playwright test lifecycle orchestrator. One skill drives the full loop: plan from live browser exploration, generate accessible .spec.ts files, execute with failure classification, and self-heal broken locators via deterministic ten-tier recovery with confidence-based PR routing.

### Skills

- **[qa-orchestration](qa-automation/skills/qa-orchestration/SKILL.md)** — Extension of agentic-delegation for the Playwright test lifecycle. Adds the Plan->Generate->Execute->Heal->Report loop, four-agent...
### Agents

- **[executor-agent](qa-automation/agents/executor-agent.md)** (`haiku`) — Use this agent to execute Playwright test suites via CLI, classify every failure into six categories, detect flaky...
- **[generator-agent](qa-automation/agents/generator-agent.md)** (`sonnet`) — Use this agent when test planning is complete and executable Playwright .spec.ts files need to be generated from...
- **[healer-agent](qa-automation/agents/healer-agent.md)** (`sonnet`) — Use this agent to repair broken Playwright locators using the deterministic ten-tier algorithm. Computes...
- **[planner-agent](qa-automation/agents/planner-agent.md)** (`opus`) — Use this agent when the user needs to explore a live web application to plan Playwright tests. Produces test plans,...

## [userland-utilities](userland-utilities/) `1.0.0`

Practical utilities for common desktop and system tasks. Includes macOS app bundle repair (Gatekeeper, code signing, quarantine flags).

### Skills

- **[fix-macos-app](userland-utilities/skills/fix-macos-app/SKILL.md)** — This skill should be used when the user asks to "fix a broken app", "app won't open", "Gatekeeper blocks app", "can't launch app", "app...

---

*Generated README — run `just readme` to regenerate.*
