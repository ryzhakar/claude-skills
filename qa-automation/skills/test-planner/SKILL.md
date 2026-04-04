---
name: test-planner
description: >
  This skill should be used when the user asks to "create test plan", "what tests should I write",
  "plan E2E tests", "explore this app for testing", "audit testability", "map user flows",
  "check page accessibility for testing", or when implementing features requiring Playwright
  test coverage. Explores the live application via MCP or CLI before writing any plan.
  Outputs structured markdown consumed by test-generator. NEVER plans from description alone.
---

# Test Planner

Explore applications via live browser interaction (MCP or Playwright CLI) and generate structured markdown test plans grounded in actual UI state. One scenario at a time.

## The Iron Law

```
NO PLAN WITHOUT LIVE EXPLORATION FIRST.
```

If the browser has not visited the page, the page cannot appear in the plan. Plans based on assumptions produce tests that verify fiction.

**The litmus test:** If the plan says "Expected..." or "Should..." without a corresponding entry in VERIFICATION.md, the plan is invalid. Every claim must trace to a browser observation.

## Constraints

This skill produces:
- `.playwright/test-plan.md` -- test scenarios with steps, outcomes, edge cases
- `.playwright/pages.md` -- page inventory with DOM quality scores (0-100)
- `.playwright/selector-strategy.md` -- locator approach per page
- `.playwright/project-config.md` -- detected tech stack
- `.playwright/VERIFICATION.md` -- evidence of live exploration

This skill does NOT produce:
- Test code (.spec.ts files) -- that is test-generator
- Selector syntax or assertion code -- generator decides implementation
- Page objects or fixtures -- generator creates those
- CI/CD configuration -- test-executor handles that

## Workflow

### Phase 1: Verify Prerequisites

Before exploring:

1. Ask the user for the base URL if not provided.
2. Read `package.json` to detect the tech stack (framework, state management, auth mechanism, build tool).
3. Check for existing test files (`tests/*.spec.ts`) to learn project naming conventions.
4. Check for an existing `.playwright/` directory with prior planning artifacts.

If the application is not accessible, instruct the user to start the server.

Write detected stack to `.playwright/project-config.md` using the template from @references/artifact-templates.md.

### Phase 2: Explore Application (MANDATORY)

This phase is non-negotiable. Interact with the application in a live browser before writing a single scenario.

**Option A: MCP exploration (default for exploratory work, <10 interactions)**

Use Playwright MCP tools for exploring unknown UI. This is the correct tool for understanding page structure through accessibility trees with element references. Cap at 10 interactions to stay within token budget.

Available tools (see @../../references/mcp-tools.md for full details):

```
browser_navigate({ url: 'http://localhost:3000' })
browser_snapshot()
browser_click({ element: 'Products link', ref: 'e5' })
browser_snapshot()
browser_fill_form({
  fields: [
    { element: 'Email', ref: 'e10', value: 'user@example.com' },
    { element: 'Password', ref: 'e12', value: 'password' }
  ]
})
browser_take_screenshot({ type: 'png', filename: 'login-page.png' })
```

Always call `browser_snapshot` first to get element refs, then use those refs in subsequent interaction tools.

**Option B: CLI interactive recording (alternative for user-driven exploration)**

Use `npx playwright codegen` when the user wants to manually drive the exploration:

```bash
npx playwright codegen http://localhost:3000
```

After codegen completes, ask the user which pages they visited, which elements they interacted with, and which flows they tested.

For each page explored, record:
- Interactive elements (buttons, links, inputs, selects)
- ARIA roles and labels present in the snapshot
- Dynamic content, loading states, client-side routing
- Whether elements respond to interaction

Record all evidence in `.playwright/VERIFICATION.md` using the template from @references/artifact-templates.md.

**These invalidate the plan:**
- "The login page should have..." -- speculative, not verified
- "Expected to see a dashboard with..." -- assumption, not observation
- Planning tests for pages that were not visited

### Phase 3: Analyze Page Quality

For each page visited, compute a DOM quality score (0-100) from the accessibility tree snapshot:

```
Score =
  + 20  proper form elements (<input>, <select>, <textarea>)
  + 15  ARIA labels work (getByLabel targets visible in snapshot)
  + 15  semantic landmarks (<header>, <nav>, <main>, <footer>)
  + 15  heading hierarchy correct (h1 -> h2 -> h3)
  + 10  role attributes verified (getByRole targets visible in snapshot)
  + 10  data-testid present on interactive elements
  - 20  clickable divs (div with click handler instead of button)
  - 15  inputs without labels
  - 15  generic divs used for interactive elements
```

Write scores to `.playwright/pages.md` using the template from @references/artifact-templates.md.

Pages scoring below 80: flag specific elements for the dev team to add `data-testid` attributes.

### Phase 4: Define Selector Strategy

Based on page quality scores and the accessibility tree, define the locator approach per page. Apply the decision tree from @../../references/locator-strategy.md for each element.

Write to `.playwright/selector-strategy.md` using the template from @references/artifact-templates.md.

### Phase 5: Write Test Plan

Create `.playwright/test-plan.md` using the template from @references/artifact-templates.md. Each scenario MUST trace to observations from Phase 2. If you did not visit a page, do not plan tests for it.

### Phase 6: Validate with User

Present the plan. Ask:

1. Are these the right flows to cover?
2. Missing any edge cases?
3. Priority ranking correct?
4. Any pages or features not yet explored?

Refine based on feedback. Update `.playwright/test-plan.md` accordingly.

## Edge Case Checklist

When identifying edge cases for each scenario, check:

- **Empty states:** Page with no data
- **Validation failures:** Empty fields, wrong format, exceeding character limits
- **Unauthorized access:** User not logged in, wrong role
- **Boundary values:** Min/max quantities, pagination at first/last page
- **Network failures:** API call fails -> loading spinner, error message
- **Browser navigation:** State persistence after back/forward/refresh

## WASM Hydration

For Leptos, Yew, Dioxus, or other WASM-based frameworks, apply the wait strategy from @../../references/locator-strategy.md. Note this requirement in project-config.md and selector-strategy.md so test-generator applies it.

## Composability

If the spec-chef skill is available:
  Extract implicit test scenarios from stakeholder conversations or incomplete specs before exploring the app.
Otherwise:
  Ask clarifying questions about which user flows matter most.

If the tdd skill is available:
  Organize the test plan around behavior verification through public interfaces. Each scenario maps to an observable behavior, not an implementation step.
Otherwise:
  Focus on end-user observable behavior.

If the agentic-delegation skill is available:
  Apply exhaustive decomposition to edge case identification -- fan out agents to explore each page independently.
Otherwise:
  Use the edge case checklist above.

## References

- @../../references/file-protocol.md -- Artifact map and directory structure
- @../../references/mcp-tools.md -- MCP vs CLI guidance and tool reference
- @../../references/seed-file-spec.md -- Quality reference and pattern template
- @../../references/locator-strategy.md -- Locator decision tree and cross-browser safety rules
- @references/artifact-templates.md -- Output format templates for all artifacts
