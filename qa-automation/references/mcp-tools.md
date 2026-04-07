# Playwright MCP Tool Reference

## Version Requirement

### Hard Pin: @playwright/mcp >= v0.0.40

**CVE-2025-9611** (DNS rebinding vulnerability) affects all versions below v0.0.40. This allows attackers to hijack the MCP server's browser session via DNS rebinding attacks.

**Before using any MCP tools, verify the installed version:**
```bash
npx @playwright/mcp --version
```

If the version is below 0.0.40:
1. STOP. Do not use MCP tools.
2. Report: "Installed @playwright/mcp version is vulnerable to CVE-2025-9611 (DNS rebinding). Upgrade to >=0.0.40 before proceeding."
3. Suggest: `npm install @playwright/mcp@latest`

This is a non-negotiable security requirement. No exceptions.

### @playwright/cli (Agent-Optimized Browser CLI)

**Install:** `npm install -g @playwright/cli@latest`  
**Current version:** 0.1.5 (April 2026)  
**Package:** https://www.npmjs.com/package/@playwright/cli

Separate npm package from standard `npx playwright` CLI. Provides 67 token-efficient commands optimized for coding agents. Each command outputs ~50 tokens vs MCP's 3,800-8,000 tokens/tool call.

**Primary use:** Live browser exploration, DOM inspection, element interaction via snapshots saved to YAML files.

---

## Architecture Priority

1. **@playwright/cli** — DEFAULT for agent browser exploration (~50 tokens/command)
2. **Standard npx playwright** — test execution, code generation, trace viewing
3. **@playwright/mcp** — ONLY when agent cannot use Bash tool (sandboxed environments)

Evidence: T3-10 verified CLI consumes 27K tokens vs MCP 114K tokens on comparable workflows (4x reduction). T2-E02 verified MCP cannot execute Playwright test files; only CLI can.

## When to Use Which Tool

| Scenario | @playwright/cli | npx playwright | @playwright/mcp |
|----------|-----------------|----------------|-----------------|
| Live browser exploration | ✅ DEFAULT | ❌ | Fallback (no Bash access) |
| DOM inspection via snapshots | ✅ ~50 tokens/cmd | ❌ | ~3,800 tokens/call |
| Element interaction | ✅ Via YAML refs | ❌ | Via accessibility tree refs |
| Running tests | ❌ | ✅ `npx playwright test` | ❌ No capability |
| Generating tests from recording | ❌ | ✅ `npx playwright codegen` | ❌ |
| TypeScript compilation check | ❌ | ✅ `npx tsc --noEmit` | ❌ |
| Viewing traces | ❌ | ✅ `npx playwright show-trace` | ❌ |
| Viewing HTML report | ❌ | ✅ `npx playwright show-report` | ❌ |
| Batch test execution or CI/CD | ❌ | ✅ Always standard CLI | ❌ |
| Sandboxed environment (no Bash) | ❌ | ❌ | ✅ MCP as fallback |

**Decision tree:**
1. Can you use Bash tool? → Use `@playwright/cli` for exploration, `npx playwright` for tests
2. Cannot use Bash? → Use `@playwright/mcp` (up to 10 interactions max due to token cost)
3. Need to run tests? → Always `npx playwright test` (MCP cannot execute tests)

## @playwright/cli Key Commands

### Session Management

```bash
# Launch browser (creates new session)
playwright-cli open <url>

# Navigate to URL in active session
playwright-cli goto <url>

# List active sessions
playwright-cli list

# Close all sessions
playwright-cli close-all
```

### Page Inspection

```bash
# Capture page snapshot to YAML (default: snapshot.yaml)
playwright-cli snapshot

# Capture to specific file
playwright-cli snapshot --filename=snap.yaml

# Take screenshot (default: screenshot.png)
playwright-cli screenshot

# Take screenshot to specific file
playwright-cli screenshot --filename=page.png
```

### Element Interaction

Snapshots generate element references (e.g., `ref: e42`). Use these refs in interaction commands:

```bash
# Click element by ref from snapshot
playwright-cli click <ref>
# Example: playwright-cli click e42

# Fill input by ref
playwright-cli fill <ref> <text>
# Example: playwright-cli fill e10 "user@example.com"

# Press keyboard key
playwright-cli press <key>
# Example: playwright-cli press Enter
```

### Debugging and Observation

```bash
# Read console messages
playwright-cli console

# List network requests
playwright-cli network
```

### Workflow Example

```bash
# 1. Open browser
playwright-cli open http://localhost:3000/login

# 2. Capture snapshot
playwright-cli snapshot --filename=login.yaml
# Read login.yaml to find element refs

# 3. Interact with elements
playwright-cli fill e10 "user@example.com"  # email input ref from snapshot
playwright-cli fill e12 "password123"       # password input ref
playwright-cli click e15                    # submit button ref

# 4. Verify result
playwright-cli snapshot --filename=result.yaml
# Read result.yaml to verify login success

# 5. Cleanup
playwright-cli close-all
```

## Standard npx playwright Commands

These commands use the standard Playwright test runner, NOT @playwright/cli.

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
