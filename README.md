# my-claude-skills

19 skills · 9 agents across 8 plugins

## Plugins

| Plugin | Description | Version | Components |
|--------|-------------|---------|------------|
| [dev-discipline](dev-discipline/) | Software engineering discipline with development lifecycle orchestration.... | `1.4.2` | 7S 3A |
| [manifesto](manifesto/) | Create concentrated manifesto declarations and bind Claude behavior to... | `2.2.1` | 2S |
| [orchestration](orchestration/) | Agent delegation framework, multi-agent research orchestration, and session... | `3.3.0` | 4S |
| [product-craft](product-craft/) | Product definition skills: extract specs from stakeholders, write user... | `1.1.0` | 2S |
| [prompt-engineering](prompt-engineering/) | Evaluate and optimize Claude system prompts using Anthropic-grounded patterns. | `2.0.0` | 0S 2A |
| [python-tools](python-tools/) | Python development tooling: debug type errors in uv-managed projects with... | `1.1.0` | 2S |
| [qa-automation](qa-automation/) | Playwright test lifecycle orchestrator. One skill drives the full loop: plan... | `3.1.2` | 1S 4A |
| [userland-utilities](userland-utilities/) | Practical utilities for common desktop and system tasks. Includes macOS app... | `1.0.0` | 1S |

---

## [dev-discipline](dev-discipline/) `1.4.2`

Software engineering discipline with development lifecycle orchestration. Plan-implement-review-fix loop, TDD, defensive planning, systematic debugging, code review, bug triage, architecture improvement, and worktree-isolated implementation agents.

### Skills

- **[defensive-planning](dev-discipline/skills/defensive-planning/SKILL.md)** — Write implementation plans, assessments, and corrections for implementers who may cut corners. Use when: creating implementation plans,...
- **[dev-orchestration](dev-discipline/skills/dev-orchestration/SKILL.md)** — Extension of agentic-delegation for software development. Adds the Plan→Implement→Review→Fix loop, TDD gates, status-driven branching,...
- **[improve-architecture](dev-discipline/skills/improve-architecture/SKILL.md)** — Explores codebases for architectural friction, discovers module-deepening opportunities, and proposes refactors through multi-design...
- **[receiving-code-review](dev-discipline/skills/receiving-code-review/SKILL.md)** — This skill should be used to apply anti-performative code review protocol: verify-before-implement discipline, YAGNI enforcement, and...
- **[systematic-debugging](dev-discipline/skills/systematic-debugging/SKILL.md)** — Mandatory 4-phase root cause protocol for bugs, test failures, errors, or unexpected behavior. Prevents random fixes and symptom...
  Scripts: [`find-polluter.sh`](dev-discipline/skills/systematic-debugging/scripts/find-polluter.sh)
- **[tdd](dev-discipline/skills/tdd/SKILL.md)** — This skill should be used when the user asks to "implement using TDD", "write tests first", "use test-driven development",...
- **[triage-issue](dev-discipline/skills/triage-issue/SKILL.md)** — Autonomously diagnoses bugs, traces root causes, designs TDD fix plans, and writes issue documents. Triggers: bug reports, "this is...
### Agents

- **[code-quality-reviewer](dev-discipline/agents/code-quality-reviewer.md)** (`inherit`) — Use this agent when reviewing code quality after spec compliance has been verified, when completing a feature and...
- **[implementer](dev-discipline/agents/implementer.md)** (`inherit`) — Use this agent when dispatching a subagent to implement a single task from an implementation plan, execute a...
- **[spec-reviewer](dev-discipline/agents/spec-reviewer.md)** (`inherit`) — Use this agent when verifying that an implementation matches its specification, after an implementer reports task...

## [manifesto](manifesto/) `2.2.1`

Create concentrated manifesto declarations and bind Claude behavior to user-provided manifestos through identity-assumption protocols.

### Skills

- **[manifesto-oath](manifesto/skills/manifesto-oath/SKILL.md)** — Enables behavioral binding to user-provided manifestos, constitutions, and principle sets through identity assumption — not theatrical...
- **[manifesto-writing](manifesto/skills/manifesto-writing/SKILL.md)** — Trigger when users request manifestos or manifesto tone. Name the enemy, strip hedging, compress to sharp distinctions, end with stark choice.
## [orchestration](orchestration/) `3.3.0`

Agent delegation framework, multi-agent research orchestration, and session lifecycle. Decompose work across model tiers, manage parallel swarms, govern quality, and persist session state.

### Skills

- **[agentic-delegation](orchestration/skills/agentic-delegation/SKILL.md)** — Decompose work into agent-delegated units across model tiers. Cheap agents are free — decompose aggressively, delegate everything,...
- **[research-tree](orchestration/skills/research-tree/SKILL.md)** — Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes, academic fields, regulatory...
  Examples: [`awesome-leptos-session.md`](orchestration/skills/research-tree/examples/awesome-leptos-session.md)
- **[session-checkpoint](orchestration/skills/session-checkpoint/SKILL.md)** — Captures context-dependent session state before compaction destroys it. Writes directly to session.md, deferred_items.md,...
- **[session-close](orchestration/skills/session-close/SKILL.md)** — Governs the ARRIVE/WORK/LEAVE session lifecycle for orchestration sessions. Covers session start (reference doc ingestion), session work...
  Scripts: [`extract_metrics.py`](orchestration/skills/session-close/scripts/extract_metrics.py)
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
## [qa-automation](qa-automation/) `3.1.2`

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
