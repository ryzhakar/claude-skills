# My Claude Skills

A collection of specialized skills for software development with Claude Code.

## Skills Included

### 1. Defensive Planning
Write implementation plans, assessments, and corrections for implementers who may cut corners. Produces prescriptive documents with verification gates, forbidden patterns, and zero escape hatches.

**Use when:**
- Creating implementation plans for peers/subordinates/contractors
- Reviewing implementations for adherence
- Writing correction plans after failures
- Situations requiring zero-tolerance for shortcuts

### 2. UV-Pyright Debug
Debug type errors in uv-managed Python projects by accessing true pyright diagnostics. Critical for projects using pydantic models where Field() defaults may not be properly inferred.

**Use when:**
- IDE shows type errors but standalone pyright reports 0 errors
- Systematic analysis of type errors is needed before mass edits
- Working with uv-managed Python projects

### 3. Python AST Mass Edit
Systematic workflow for AST-based mass edits in Python codebases. Includes pre-surveying with grep/pyright, idempotent transformations, and validation protocol.

**Use when:**
- Editing 3+ files with structural changes (decorators, function signatures, imports, class definitions)
- NOT for simple string replacements or <5 instances

### 4. Manifesto Oath
Enable behavioral binding to user-provided manifestos through identity-assumption protocols rather than theatrical oath-taking.

**Use when:**
- User provides a manifesto and requests oath-like commitment
- User asks Claude to swear to or bind itself to specific principles
- User wants persistent behavioral constraint within a conversation

### 5. Manifesto Writing
Transform talks, essays, or documentation into manifestos: concentrated declarations of principle that command rather than explain.

**Use when:**
- Turning talks, essays, or docs into manifestos
- Requesting manifesto tone or command-style guidance
- Need for enemy-and-stakes framing

### 6. Spec Chef
Extract implicit product decisions from stakeholders into durable artifacts through systematic gap detection and constrained questioning.

**Use when:**
- Analyzing incomplete specs or finding documentation gaps
- Stakeholder interviews and extracting product requirements
- Defining MVP scope
- Existing documentation has implicit assumptions or undefined behaviors

### 7. User Story Chef
Write user stories as value negotiation units, not template-filling exercises. Teaches function (value decomposition, falsifiable AC, feedback optimization) over form (templates).

**Use when:**
- Writing user stories or acceptance criteria
- Story splitting and backlog refinement
- Evaluating story quality with INVEST criteria
- Creating Agile artifacts that capture work units

## Installation

Install this plugin using Claude Code:

```bash
claude code plugins install /path/to/claude-skills
```

Or add to your marketplace configuration.

## Structure

```
claude-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   └── marketplace.json     # Marketplace definition
├── skills/
│   ├── defensive-planning/
│   ├── uv-pyright-debug/
│   ├── python-ast-mass-edit/
│   ├── manifesto-oath/
│   ├── manifesto-writing/
│   ├── spec-chef/
│   └── user-story-chef/
└── README.md
```

## License

MIT

## Author

ryzhakar
