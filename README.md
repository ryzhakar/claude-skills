# my-claude-skills

19 skills · 7 agents across 8 plugins

## Plugins

| Plugin | Description | Version | Components |
|--------|-------------|---------|------------|
| [dev-discipline](dev-discipline/) | Software engineering discipline: defensive planning, test-driven... | `1.0.0` | 4S 3A |
| [manifesto](manifesto/) | Create concentrated manifesto declarations and bind Claude behavior to... | `1.2.0` | 2S |
| [orchestration](orchestration/) | Agent delegation framework, multi-agent research orchestration, and... | `2.1.0` | 3S |
| [product-craft](product-craft/) | Product definition and architecture skills: extract specs from stakeholders,... | `1.0.0` | 4S |
| [prompt-engineering](prompt-engineering/) | Evaluate and optimize Claude system prompts using Anthropic-grounded patterns. | `1.0.0` | 2S |
| [python-tools](python-tools/) | Python development tooling: debug type errors in uv-managed projects with... | `1.0.0` | 2S |
| [qa-automation](qa-automation/) | Playwright test lifecycle orchestrator. One skill drives the full loop: plan... | `2.1.0` | 1S 4A |
| [userland-utilities](userland-utilities/) | Practical utilities for common desktop and system tasks. Includes macOS app... | `1.0.0` | 1S |

---

## [dev-discipline](dev-discipline/) `1.0.0`

Software engineering discipline: defensive planning, test-driven development, systematic debugging, and code review reception.

### Skills

- **[defensive-planning](dev-discipline/skills/defensive-planning/SKILL.md)** — Write implementation plans, assessments, and corrections for implementers who may cut corners. Use when: (1) creating implementation...
  References: [`execution.md`](dev-discipline/skills/defensive-planning/references/execution.md), [`module-design.md`](dev-discipline/skills/defensive-planning/references/module-design.md), [`tdd-mode.md`](dev-discipline/skills/defensive-planning/references/tdd-mode.md)
- **[receiving-code-review](dev-discipline/skills/receiving-code-review/SKILL.md)** — This skill should be used to apply anti-performative code review protocol: verify-before-implement discipline, YAGNI enforcement, and...
- **[systematic-debugging](dev-discipline/skills/systematic-debugging/SKILL.md)** — This skill should be used when the user reports a "bug", "test failure", "unexpected behavior", "error", "crash", "flaky test", asks to...
  References: [`condition-based-waiting.md`](dev-discipline/skills/systematic-debugging/references/condition-based-waiting.md), [`defense-in-depth.md`](dev-discipline/skills/systematic-debugging/references/defense-in-depth.md), [`root-cause-tracing.md`](dev-discipline/skills/systematic-debugging/references/root-cause-tracing.md)
  Scripts: [`find-polluter.sh`](dev-discipline/skills/systematic-debugging/scripts/find-polluter.sh)
- **[tdd](dev-discipline/skills/tdd/SKILL.md)** — This skill should be used when the user asks to "implement using TDD", "write tests first", "use test-driven development",...
  References: [`deep-modules.md`](dev-discipline/skills/tdd/references/deep-modules.md), [`interface-design.md`](dev-discipline/skills/tdd/references/interface-design.md), [`mocking.md`](dev-discipline/skills/tdd/references/mocking.md), [`refactoring.md`](dev-discipline/skills/tdd/references/refactoring.md), [`tests.md`](dev-discipline/skills/tdd/references/tests.md)
### Agents

- **[code-quality-reviewer](dev-discipline/agents/code-quality-reviewer.md)** (`inherit`) — Use this agent when reviewing code quality after spec compliance has been verified, when completing a feature and...
- **[implementer](dev-discipline/agents/implementer.md)** (`inherit`) — Use this agent when dispatching a subagent to implement a single task from an implementation plan, execute a...
- **[spec-reviewer](dev-discipline/agents/spec-reviewer.md)** (`inherit`) — Use this agent when verifying that an implementation matches its specification, after an implementer reports task...

## [manifesto](manifesto/) `1.2.0`

Create concentrated manifesto declarations and bind Claude behavior to user-provided manifestos through identity-assumption protocols.

### Skills

- **[manifesto-oath](manifesto/skills/manifesto-oath/SKILL.md)** — Enables behavioral binding to user-provided manifestos, principles, or codes through identity-assumption protocols rather than...
  References: [`configuration.md`](manifesto/skills/manifesto-oath/references/configuration.md), [`theory.md`](manifesto/skills/manifesto-oath/references/theory.md)
- **[manifesto-writing](manifesto/skills/manifesto-writing/SKILL.md)** — Trigger when users ask to turn talks, essays, or docs into a manifesto—or request manifesto tone, command-style guidance, or...
## [orchestration](orchestration/) `2.1.0`

Agent delegation framework, multi-agent research orchestration, and development lifecycle coordination. Decompose work across model tiers, manage parallel swarms, govern quality, and orchestrate the plan-implement-review-fix loop.

### Skills

- **[agentic-delegation](orchestration/skills/agentic-delegation/SKILL.md)** — The universal framework for decomposing work into agent-delegated units across model tiers. Use this skill whenever work can be broken...
  References: [`prompt-anatomy.md`](orchestration/skills/agentic-delegation/references/prompt-anatomy.md), [`quality-governance.md`](orchestration/skills/agentic-delegation/references/quality-governance.md)
- **[dev-orchestration](orchestration/skills/dev-orchestration/SKILL.md)** — Extension of agentic-delegation for the software development lifecycle. Adds the Plan→Implement→Review→Fix loop, dev-discipline agent...
  References: [`agent-dispatch.md`](orchestration/skills/dev-orchestration/references/agent-dispatch.md), [`domain-context-examples.md`](orchestration/skills/dev-orchestration/references/domain-context-examples.md), [`lifecycle-loops.md`](orchestration/skills/dev-orchestration/references/lifecycle-loops.md)
- **[research-tree](orchestration/skills/research-tree/SKILL.md)** — Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes, academic fields, regulatory...
  References: [`agent-templates.md`](orchestration/skills/research-tree/references/agent-templates.md), [`anti-patterns.md`](orchestration/skills/research-tree/references/anti-patterns.md), [`report-formats.md`](orchestration/skills/research-tree/references/report-formats.md), [`tier-playbook.md`](orchestration/skills/research-tree/references/tier-playbook.md)
  Examples: [`awesome-leptos-session.md`](orchestration/skills/research-tree/examples/awesome-leptos-session.md)
## [product-craft](product-craft/) `1.0.0`

Product definition and architecture skills: extract specs from stakeholders, write user stories, triage bugs, improve codebase architecture, and establish ubiquitous language.

### Skills

- **[improve-architecture](product-craft/skills/improve-architecture/SKILL.md)** — This skill should be used when the user asks to "improve the architecture", "find refactoring opportunities", "deepen shallow modules",...
  References: [`dependency-categories.md`](product-craft/skills/improve-architecture/references/dependency-categories.md), [`rfc-template.md`](product-craft/skills/improve-architecture/references/rfc-template.md)
- **[spec-chef](product-craft/skills/spec-chef/SKILL.md)** — Extract implicit product decisions from stakeholders into durable artifacts. Triggers: analyzing incomplete specs, stakeholder...
  References: [`artifact-separation.md`](product-craft/skills/spec-chef/references/artifact-separation.md), [`dependency-tiers.md`](product-craft/skills/spec-chef/references/dependency-tiers.md), [`gap-heuristics.md`](product-craft/skills/spec-chef/references/gap-heuristics.md), [`terminology-extraction.md`](product-craft/skills/spec-chef/references/terminology-extraction.md)
- **[triage-issue](product-craft/skills/triage-issue/SKILL.md)** — This skill should be used when the user reports a bug, says "this is broken", asks to "triage an issue", "investigate a bug", "find the...
- **[user-story-chef](product-craft/skills/user-story-chef/SKILL.md)** — Write user stories as value negotiation units, not template-filling exercises. Triggers: writing user stories, acceptance criteria,...
  References: [`anti-patterns.md`](product-craft/skills/user-story-chef/references/anti-patterns.md), [`slicing.md`](product-craft/skills/user-story-chef/references/slicing.md)
## [prompt-engineering](prompt-engineering/) `1.0.0`

Evaluate and optimize Claude system prompts using Anthropic-grounded patterns.

### Skills

- **[prompt-eval](prompt-engineering/skills/prompt-eval/SKILL.md)** — This skill should be used when the user asks to "evaluate a prompt", "review a system prompt", "assess prompt quality", "check if this...
  Examples: [`sample-evaluation.md`](prompt-engineering/skills/prompt-eval/examples/sample-evaluation.md)
- **[prompt-optimize](prompt-engineering/skills/prompt-optimize/SKILL.md)** — This skill should be used when the user asks to "improve this prompt", "optimize a prompt", "fix this system prompt", "make this prompt...
  Examples: [`sample-optimization.md`](prompt-engineering/skills/prompt-optimize/examples/sample-optimization.md)
## [python-tools](python-tools/) `1.0.0`

Python development tooling: debug type errors in uv-managed projects with pyright, and perform AST-based mass structural edits across codebases.

### Skills

- **[python-ast-mass-edit](python-tools/skills/python-ast-mass-edit/SKILL.md)** — Systematic workflow for AST-based mass edits in Python codebases. Use when editing 3+ files with structural changes (decorators,...
  Scripts: [`template_transformer.py`](python-tools/skills/python-ast-mass-edit/scripts/template_transformer.py)
- **[uv-pyright-debug](python-tools/skills/uv-pyright-debug/SKILL.md)** — Debug type errors in uv-managed Python projects by accessing true pyright diagnostics. Use when IDE shows type errors but standalone...
  Scripts: [`analyze_errors.py`](python-tools/skills/uv-pyright-debug/scripts/analyze_errors.py), [`line_index_errors.py`](python-tools/skills/uv-pyright-debug/scripts/line_index_errors.py)
## [qa-automation](qa-automation/) `2.1.0`

Playwright test lifecycle orchestrator. One skill drives the full loop: plan from live browser exploration, generate accessible .spec.ts files, execute with failure classification, and self-heal broken locators via deterministic ten-tier recovery with confidence-based PR routing.

### Skills

- **[qa-orchestration](qa-automation/skills/qa-orchestration/SKILL.md)** — Extension of agentic-delegation for the Playwright test lifecycle. Adds the Plan→Generate→Execute→Heal→Report loop, four-agent...
### Agents

- **[executor-agent](qa-automation/agents/executor-agent.md)** (`haiku`) — Use this agent to execute Playwright test suites via CLI, classify every failure into six categories, detect flaky...
- **[generator-agent](qa-automation/agents/generator-agent.md)** (`sonnet`) — Use this agent when test planning is complete and executable Playwright .spec.ts files need to be generated from...
- **[healer-agent](qa-automation/agents/healer-agent.md)** (`sonnet`) — Use this agent to repair broken Playwright locators using the deterministic ten-tier algorithm. Computes...
- **[planner-agent](qa-automation/agents/planner-agent.md)** (`sonnet`) — Use this agent when the user needs to explore a live web application to plan Playwright tests. Produces structured...

## [userland-utilities](userland-utilities/) `1.0.0`

Practical utilities for common desktop and system tasks. Includes macOS app bundle repair (Gatekeeper, code signing, quarantine flags).

### Skills

- **[fix-macos-app](userland-utilities/skills/fix-macos-app/SKILL.md)** — This skill should be used when the user asks to "fix a broken app", "app won't open", "Gatekeeper blocks app", "can't launch app", "app...

---

*Generated README — run `just readme` to regenerate.*
