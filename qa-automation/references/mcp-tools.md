# Playwright MCP Tool Reference

CLI-first architecture. Use CLI commands by default. MCP is reserved for sandboxed exploratory work requiring fewer than 10 interactions.

Evidence: T3-10 verified CLI consumes 27K tokens vs MCP 114K tokens on comparable workflows (4x reduction). T2-E02 verified MCP cannot execute Playwright test files; only CLI can.

## When to Use CLI vs MCP

| Scenario | Use | Rationale |
|----------|-----|-----------|
| Running tests | CLI | `npx playwright test` -- MCP has no test execution capability |
| Generating tests from recording | CLI | `npx playwright codegen <url>` -- interactive recording |
| TypeScript compilation check | CLI | `npx tsc --noEmit` |
| Viewing traces | CLI | `npx playwright show-trace trace.zip` |
| Viewing HTML report | CLI | `npx playwright show-report` |
| Exploring unknown UI (<10 interactions) | MCP | Accessibility tree + element refs more efficient than screenshots |
| Verifying selectors exist in DOM | MCP | `browser_snapshot` + `browser_click` to test locators |
| Debugging a specific failure interactively | MCP | Navigate to failure point, inspect page state |
| Batch test execution or CI/CD | CLI | Always CLI for execution, artifact collection, reporting |

**Rule of thumb:** If the task involves running tests, generating files, or CI/CD, use CLI. If the task involves exploring a live page to understand its structure, use MCP for up to 10 interactions, then switch to CLI.

## CLI Command Reference

### Test Execution

```bash
# Run all tests with multiple reporters
npx playwright test --reporter=json,html,line

# Run specific test file
npx playwright test tests/auth.spec.ts

# Run tests serially (debugging)
npx playwright test --workers=1

# Run tests in parallel
npx playwright test --workers=4

# Run with specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Test Generation

```bash
# Interactive test recording (user-driven)
npx playwright codegen http://localhost:3000

# Generate test targeting specific browser
npx playwright codegen --browser=firefox http://localhost:3000
```

### Debugging and Reporting

```bash
# Open trace viewer
npx playwright show-trace test-results/auth-user-can-log-in/trace.zip

# Open HTML report
npx playwright show-report

# TypeScript compilation check
npx tsc --noEmit
```

### Installation

```bash
# Install Playwright with browsers
npm init playwright@latest

# Install specific browsers
npx playwright install chromium firefox webkit
```

## MCP Tools (via @playwright/mcp)

Source: microsoft/playwright-mcp repository. Verified tool count: 61 tools total (T3-02).

All tools use the `browser_` prefix. Element interaction uses a two-tier parameter design:
1. `ref` (primary) -- exact element reference from the most recent `browser_snapshot`
2. `selector` (fallback) -- CSS or role selector when ref is unavailable
3. `element` (optional) -- human-readable description for logging

**Workflow:** Always call `browser_snapshot` first, then use `ref` values from the output in subsequent tool calls.

### Core Interaction Tools (always available)

**browser_navigate** -- Navigate to a URL.
```
Parameters: url (string, required)
Example:   browser_navigate({ url: 'http://localhost:3000/login' })
Returns:   Page snapshot after navigation
```

**browser_snapshot** -- Capture accessibility tree. Prefer over screenshots for LLM efficiency.
```
Parameters: filename (string, optional), selector (string, optional), depth (number, optional)
Example:   browser_snapshot()
           browser_snapshot({ selector: 'form', depth: 3 })
Returns:   Accessibility tree in text format with ref values
```

**browser_click** -- Click an element.
```
Parameters: ref (string, required), element (string, optional), selector (string, optional),
            doubleClick (boolean, optional), button (string, optional), modifiers (array, optional)
Example:   browser_click({ element: 'Sign In button', ref: 'e42' })
```

**browser_type** -- Type text into an editable element. Use for single-field input.
```
Parameters: ref (string, required), text (string, required), element (string, optional),
            selector (string, optional), submit (boolean, optional), slowly (boolean, optional)
Example:   browser_type({ element: 'Email input', ref: 'e10', text: 'user@example.com' })
```

**browser_fill_form** -- Fill multiple form fields at once. More efficient than individual browser_type calls.
```
Parameters: fields (array, required) -- each field has element, ref/selector, value
Example:   browser_fill_form({
             fields: [
               { element: 'Email', ref: 'e10', value: 'user@example.com' },
               { element: 'Password', ref: 'e12', value: 'SecurePass123' }
             ]
           })
```

**browser_hover** -- Hover over an element.
```
Parameters: ref (string, required), element (string, optional), selector (string, optional)
```

**browser_select_option** -- Select an option in a dropdown.
```
Parameters: ref (string, required), values (array, required), element (string, optional), selector (string, optional)
Example:   browser_select_option({ element: 'Country', ref: 'e20', values: ['US'] })
```

**browser_press_key** -- Press a keyboard key.
```
Parameters: key (string, required) -- e.g., Enter, Escape, Tab, ArrowDown
Example:   browser_press_key({ key: 'Enter' })
```

**browser_take_screenshot** -- Take a screenshot. Use for visual evidence, not page understanding.
```
Parameters: type (string, required, default: png), filename (string, optional),
            element (string, optional), ref (string, optional), fullPage (boolean, optional)
Example:   browser_take_screenshot({ type: 'png', filename: 'login-page.png' })
```

### Synchronization Tools

**browser_wait_for** -- Wait for text to appear, disappear, or a duration to pass.
```
Parameters: time (number, optional), text (string, optional), textGone (string, optional)
Example:   browser_wait_for({ text: 'Welcome back' })
           browser_wait_for({ textGone: 'Loading...' })
```

### Observation Tools

**browser_console_messages** -- Returns console messages.
```
Parameters: level (string, required: info/warn/error), all (boolean, optional), filename (string, optional)
```

**browser_network_requests** -- Returns network requests since page load.
```
Parameters: static (boolean, required), requestBody (boolean, required),
            requestHeaders (boolean, required), filter (string, optional)
```

### Navigation Tools

**browser_navigate_back** -- Go back in browser history. No parameters.

**browser_tabs** -- Manage browser tabs.
```
Parameters: action (string, required: list/create/close/select), index (number, optional)
Example:   browser_tabs({ action: 'list' })
           browser_tabs({ action: 'create' })
           browser_tabs({ action: 'select', index: 0 })
```

**browser_close** -- Close the current page. No parameters.

### Advanced Tools (require capability flags)

**browser_evaluate** (core) -- Execute JavaScript in page context.
```
Parameters: function (string, required), element (string, optional), ref (string, optional)
```

**browser_run_code** (core) -- Run a Playwright code snippet.
```
Parameters: code (string, optional), filename (string, optional)
Example:   browser_run_code({ code: 'await page.getByRole("button").count()' })
```

**browser_drag** (core) -- Drag and drop between two elements.
```
Parameters: startElement, startRef, endElement, endRef (all strings, required)
```

**browser_file_upload** (core) -- Upload files.
```
Parameters: paths (array, optional) -- absolute paths to files
```

**browser_handle_dialog** (core) -- Handle browser dialogs.
```
Parameters: accept (boolean, required), promptText (string, optional)
```

**browser_resize** (core) -- Resize browser window.
```
Parameters: width (number, required), height (number, required)
```

### Optional Capability Sets

Enable with `--caps=<category>` flag when starting the MCP server.

**Testing tools** (`--caps=testing`, 4 tools):
- `browser_generate_locator` -- Generate optimal locator for an element
- `browser_verify_element_visible` -- Verify element is visible by role and name
- `browser_verify_text_visible` -- Verify text is visible on page
- `browser_verify_list_visible` -- Verify list with specific items is visible

**Storage tools** (`--caps=storage`, 16 tools):
- Cookie management: `browser_cookie_get`, `browser_cookie_set`, `browser_cookie_list`, `browser_cookie_delete`, `browser_cookie_clear`
- LocalStorage: `browser_localstorage_get`, `browser_localstorage_set`, `browser_localstorage_list`, `browser_localstorage_delete`, `browser_localstorage_clear`
- SessionStorage: `browser_sessionstorage_get`, `browser_sessionstorage_set`, `browser_sessionstorage_list`, `browser_sessionstorage_delete`, `browser_sessionstorage_clear`
- State files: `browser_storage_state`, `browser_set_storage_state`

**Network tools** (`--caps=network`, 4 tools):
- `browser_route` -- Mock network requests
- `browser_unroute` -- Remove mocks
- `browser_route_list` -- List active routes
- `browser_network_state_set` -- Toggle offline mode

**DevTools tools** (`--caps=devtools`, 6 tools):
- Tracing: `browser_start_tracing`, `browser_stop_tracing`
- Video: `browser_start_video`, `browser_stop_video`, `browser_video_chapter`
- Debugging: `browser_resume`

**Vision tools** (`--caps=vision`, 6 tools):
- Coordinate-based: `browser_mouse_click_xy`, `browser_mouse_move_xy`, `browser_mouse_drag_xy`
- Button state: `browser_mouse_down`, `browser_mouse_up`, `browser_mouse_wheel`

**PDF tools** (`--caps=pdf`, 1 tool):
- `browser_pdf_save` -- Save page as PDF

**Config tools** (`--caps=config`, 1 tool):
- `browser_get_config` -- Get resolved config

## Common Incorrect Tool Names

These names DO NOT EXIST. Use the correct alternatives.

| Wrong Name | Correct Name |
|------------|-------------|
| `browser_fill` | `browser_type` (single field) or `browser_fill_form` (multiple fields) |
| `browser_screenshot` | `browser_take_screenshot` |
| `browser_tab_new` | `browser_tabs({ action: 'create' })` |
| `browser_tab_close` | `browser_tabs({ action: 'close' })` |
