# Software Engineering Delegation Patterns

This document provides software-specific examples of the delegation archetypes described in the main skill. Use these as concrete references when applying delegation patterns to code implementation, code review, and debugging tasks.

## Implementation Archetype

```
Orchestrator: read the spec, decompose into implementation units
   ↓
Per-unit: sonnet agent implements (needs reasoning about types, APIs)
   ↓
Per-unit: haiku agent runs tests, reports results
   ↓
Orchestrator: review agent summaries, fix integration issues
```

Sonnet for implementation because code must compile. Haiku for test running because it's mechanical.

**Key delegation points:**
- Spec reading and decomposition: orchestrator
- Unit implementation: sonnet (requires type reasoning, API compatibility assessment)
- Test execution: haiku (mechanical command execution and output reporting)
- Integration review: orchestrator (synthesizes agent summaries)

## Code Review / Audit Archetype

```
Orchestrator: identify files to review
   ↓
Per-file or per-concern: haiku agents audit (security, style, correctness, performance)
   ↓
Sonnet agent synthesizes findings into prioritized review
```

Fan out by CONCERN, not by file. A security audit agent reads all files for security. A style audit agent reads all files for style. This catches cross-file issues that per-file agents miss.

**Key delegation points:**
- File identification: orchestrator
- Concern-specific audits: haiku (parallel fan-out by concern: security, style, correctness, performance)
- Synthesis: sonnet (prioritizes findings, identifies patterns)

**Why concern-based vs file-based:**
- Cross-file security issues (e.g., data flow vulnerabilities)
- Consistency of style across the codebase
- Architectural correctness patterns
- Performance hotspots that span modules

## Debugging Archetype

```
Orchestrator: receive failure report
   ↓
Speculative parallel: 3 haiku agents, each investigating a different hypothesis
   ↓
Whichever finds evidence → sonnet agent implements fix
   ↓
Haiku agent verifies fix (runs tests, checks output)
```

Speculative parallel is key for debugging — you don't know which hypothesis is right, so test all simultaneously.

**Key delegation points:**
- Hypothesis generation: orchestrator (based on failure report)
- Parallel investigation: haiku (each agent tests one hypothesis)
- Fix implementation: sonnet (requires reasoning about code structure)
- Verification: haiku (mechanical test execution)

**Example hypotheses for a failed test:**
- Agent A: check dependency version conflicts
- Agent B: verify environment configuration
- Agent C: examine recent code changes in related modules

## Testing Archetype

```
Orchestrator: identify what needs testing
   ↓
Haiku agents: run test suites, report results to files
   ↓
If failures: delegate debugging (see above)
```

Never run long test suites in orchestrator context. Always delegate to background agents that write results to files.

**Key delegation points:**
- Test suite identification: orchestrator
- Test execution: haiku background agents (parallel per test suite)
- Result aggregation: orchestrator (reads completion summaries)
- Failure triage: triggers debugging archetype

## Domain-Specific Context Examples

### Cargo.toml Example

When delegating dependency audits in Rust projects:

**Minimal context for haiku agent:**
> "The project uses Leptos 0.8, Tailwind CSS v4 (standalone binary, no Node.js), and Postgres via sqlx. Read `/path/to/Cargo.toml`. For each dependency, note version and purpose. Check for version conflicts with the specified Leptos and sqlx versions."

**NOT:**
> "Here's the full project architecture [3000 words], the design system [2000 words], the coding conventions [1500 words]. Now check Cargo.toml."

### Tailwind Compatibility Example

When checking library compatibility with Tailwind v4:

**Minimal context for haiku agent:**
> "Check if library X supports Tailwind v4. The project uses Tailwind v4 standalone (no Node.js, no tailwind.config.js). Fetch the library's documentation and check for Tailwind-related configuration."

**Key constraint:** Tailwind v4 standalone eliminates Node.js dependency — this is the critical compatibility criterion.

### Type Signature Example

When verifying API compatibility (sonnet-level work):

**Minimal context for sonnet agent:**
> "Verify that library X's auth API is compatible with the project's user model. Read `/path/to/models/user.rs` and fetch library X's auth documentation. Check: does the library accept our User struct fields? Are return types compatible?"

**Why sonnet:** Reasoning about type signatures and API compatibility requires more than haiku's pattern-matching capabilities.

## Documentation / Writing Archetype

```
Orchestrator: define structure and requirements
   ↓
Haiku agents: gather facts, read source code, extract examples
   ↓
Sonnet agent: assemble into coherent document
   ↓
(Optional) Haiku agent: verify all claims against source code
```

Fact-gathering is cheap work. Assembly requires judgment. Verification is cheap again.

**Key delegation points:**
- Structure definition: orchestrator
- Fact gathering: haiku (parallel per source file or module)
- Document assembly: sonnet (requires synthesis and coherence)
- Verification: haiku (mechanical claim-checking against source)

**Example for API documentation:**
- Haiku agents: extract function signatures, parameter types, return types from source
- Sonnet agent: write explanatory text, usage examples, integration guidance
- Haiku agent: verify every code snippet compiles
