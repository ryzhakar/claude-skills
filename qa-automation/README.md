# qa-automation

Full QA lifecycle automation with Playwright and TypeScript. Four skills cover the complete loop: plan tests from live browser exploration, generate accessible .spec.ts files with cross-browser-safe locators, execute suites with failure classification, and self-heal broken locators using deterministic ten-tier recovery with confidence-based PR routing.

`playwright` `testing` `e2e` `qa` `automation` `self-healing` `accessibility` `cross-browser` `ci-cd` 
## Skills

### [test-executor](skills/test-executor/SKILL.md)
Execute Playwright test suites, classify failures by type, and produce structured reports. Use when "run tests", "execute Playwright tests", "run E2E tests", "check test results", "run cross-browser tests", "why did tests fail", "classify test failures", "detect flaky tests", or after test-generator produces .spec.ts files. CLI-exclusive (not MCP). Outputs JSON reports with failure classification (locator, timing, data, visual, interaction, other) for test-healer.


**References:** [`failure-classification.md`](skills/test-executor/references/failure-classification.md) · [`playwright-config.md`](skills/test-executor/references/playwright-config.md)
---

### [test-generator](skills/test-generator/SKILL.md)
Transform structured test plans into executable Playwright .spec.ts files with accessibility-first locators. Use when user asks to "generate tests from plan", "create Playwright tests", "write  .spec.ts files", "implement test scenarios", "convert plan to tests", or after test-planner  produces a plan. REQUIRES a seed file -- refuses without one. Generates one test at a time:  write, run, verify, then next. Output is pure Playwright + TypeScript with zero AI runtime  dependency.


---

### [test-healer](skills/test-healer/SKILL.md)
Diagnose test failures, distinguish real bugs from test brittleness, and auto-fix broken locators. Use when "heal tests", "fix broken tests", "auto-fix test failures", "repair locators", "self-heal tests", "why are my tests failing", "fix flaky tests", "update broken selectors", or after test-executor classifies failures in .ai-failures.json. Applies deterministic ten-tier self-healing first (zero LLM cost, 2-5% false positive rate), falls back to LLM reasoning only when deterministic healing fails, computes confidence scores, and creates fix PRs with confidence-based routing. NEVER heals assertion failures or runtime errors.


**References:** [`cicd-workflow.md`](skills/test-healer/references/cicd-workflow.md) · [`confidence-scoring.md`](skills/test-healer/references/confidence-scoring.md) · [`failure-heuristics.md`](skills/test-healer/references/failure-heuristics.md) · [`ten-tier-algorithm.md`](skills/test-healer/references/ten-tier-algorithm.md)
---

### [test-planner](skills/test-planner/SKILL.md)
This skill should be used when the user asks to "create test plan", "what tests should I write", "plan E2E tests", "explore this app for testing", "audit testability", "map user flows", "check page accessibility for testing", or when implementing features requiring Playwright test coverage. Explores the live application via MCP or CLI before writing any plan. Outputs structured markdown consumed by test-generator. NEVER plans from description alone.


**References:** [`artifact-templates.md`](skills/test-planner/references/artifact-templates.md)
---

