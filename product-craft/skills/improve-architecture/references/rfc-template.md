# Refactor RFC Issue Template

Use this template when creating the GitHub issue via `gh issue create`.

```
## Problem

Describe the architectural friction:

- Which modules are shallow and tightly coupled
- What integration risk exists in the seams between them
- Why this makes the codebase harder to navigate, test, and maintain

Do NOT reference specific file paths or line numbers. Describe modules
by responsibility and behavior so the issue survives reorganization.

## Proposed Interface

The selected interface design:

- Interface signature (types, methods, parameters)
- Usage example showing how callers consume the new interface
- What complexity the module hides internally

## Dependency Strategy

Which category applies (in-process, local-substitutable, ports & adapters,
true external) and how dependencies are handled:

- For in-process: merged directly, tested with unit tests
- For local-substitutable: tested with [specific stand-in]
- For ports & adapters: port definition, production adapter, test adapter
- For true external: mock boundary, contract test for real client

## Testing Strategy

- **New boundary tests to write**: behaviors to verify at the interface
- **Old tests to delete**: shallow module tests that become redundant
- **Test environment needs**: local stand-ins or adapters required

## Implementation Recommendations

Durable guidance NOT coupled to current file layout:

- What the module should own (responsibilities)
- What it should hide (implementation details)
- What it should expose (the interface contract)
- How callers should migrate to the new interface
- Suggested implementation order (which boundaries to draw first)
```
