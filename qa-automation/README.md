# qa-automation

Playwright test lifecycle orchestrator. One skill drives the full loop: plan from live browser exploration, generate accessible .spec.ts files, execute with failure classification, and self-heal broken locators via deterministic ten-tier recovery with confidence-based PR routing.

`playwright` `testing` `e2e` `qa` `automation` `self-healing` `accessibility` `cross-browser` `ci-cd` 
## Skills

### [qa-orchestration](skills/qa-orchestration/SKILL.md)

Extension of agentic-delegation for the Playwright test lifecycle. Adds the Plan→Generate→Execute→Heal→Report loop, four-agent orchestration, confidence-based PR routing, circuit breaker safety, and session persistence.
Hard preference: orchestration plugin (agentic-delegation skill). Same-plugin agents: planner-agent, generator-agent, executor-agent, healer-agent.
Triggers: "run QA", "automate testing", "create and run Playwright tests", "set up E2E testing", "generate and execute tests", "run the full test pipeline", "heal broken tests", or mentions running the full Playwright test lifecycle.


---

## Agents

### [executor-agent](agents/executor-agent.md)

Use this agent to execute Playwright test suites via CLI, classify every failure into six categories, detect flaky tests, and produce .ai-failures.json. CLI-exclusive — never uses MCP for test execution. Use after test generation is complete.

<example>
Context: Tests have been generated, need to run the suite
user: "Run the Playwright tests and classify any failures"
assistant: "I'll dispatch the executor-agent to run the suite via CLI and classify failures."
<commentary>
Test execution and failure classification is the executor-agent's sole function.
</commentary>
</example>

<example>
Context: QA orchestrator running Phase 3
user: "Run QA on my app"
assistant: "Phase 2 complete. Dispatching executor-agent for Phase 3: test execution."
<commentary>
Orchestrator dispatches executor-agent after generator-agent completes.
</commentary>
</example>


**Model:** `haiku` · **Tools:** Read, Write, Bash, Glob

---

### [generator-agent](agents/generator-agent.md)

Use this agent when test planning is complete and executable Playwright .spec.ts files need
to be generated from .playwright/test-plan.md, OR when existing tests need structural fixes
(timing issues, fixture races, test architecture problems). Two modes: create (from plan)
and fix (from failure description). Requires tests/seed.spec.ts.

<example>
Context: Test plan exists, user wants tests generated
user: "Generate the Playwright tests from the test plan"
assistant: "I'll dispatch the generator-agent to transform the test plan into passing .spec.ts files."
<commentary>
Test plan exists at .playwright/test-plan.md — generator-agent transforms it into code (create mode).
</commentary>
</example>

<example>
Context: Executor found timing failures with correct locators — test architecture problem
user: "Run QA on my app"
assistant: "Timing failures are structural, not locator issues. Re-dispatching generator-agent in fix mode."
<commentary>
Timing failures where locators are correct route to generator (fix mode), not healer.
</commentary>
</example>


**Model:** `sonnet` · **Tools:** Read, Write, Edit, Bash, Glob

---

### [healer-agent](agents/healer-agent.md)

Use this agent to repair broken Playwright locators using the deterministic ten-tier algorithm. Computes Similo-based confidence scores. NEVER heals assertion failures — element found + wrong value = application bug. Can process a single failure or a batch from .ai-failures.json.

<example>
Context: Test execution found locator failures
user: "Heal the broken locators in the test suite"
assistant: "I'll dispatch the healer-agent to apply ten-tier deterministic repair to the locator failures."
<commentary>
Locator failures detected — healer-agent applies deterministic repair, not assertion fixes.
</commentary>
</example>

<example>
Context: QA orchestrator running Phase 4 with a single failure
user: "Run QA on my app"
assistant: "Phase 3 found 2 locator failures. Dispatching healer-agent to repair them."
<commentary>
Orchestrator dispatches healer-agent for locator repair. Below N=5 threshold, single agent handles all.
</commentary>
</example>


**Model:** `sonnet` · **Tools:** Read, Write, Edit, Bash, Grep, Glob

---

### [planner-agent](agents/planner-agent.md)

Use this agent when the user needs to explore a live web application to plan Playwright tests. 
Produces structured test planning artifacts from browser exploration.

<example>
Context: User wants to create test plans for their web application
user: "Explore my app at localhost:3000 and plan what tests we need"
assistant: "I'll dispatch the planner-agent to explore the live application and produce a test plan."
<commentary>
User wants test planning from live exploration — this is the planner-agent's core function.
</commentary>
</example>

<example>
Context: QA orchestrator is running Phase 1
user: "Run QA on my app"
assistant: "Starting Phase 1: dispatching planner-agent to explore the application."
<commentary>
The orchestrator dispatches planner-agent as the first phase of the QA pipeline.
</commentary>
</example>


**Model:** `sonnet` · **Tools:** Read, Write, Bash, Glob

---

