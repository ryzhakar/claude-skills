# Prompt Anatomy

Every agent prompt has these sections. Skip none.

## 1. Role (1 sentence)

What the agent is and what it's doing. Not a personality — a job description.

**Example:**
> "You are auditing the dependency tree of a web application."

**Purpose:** Establishes the agent's scope and authority. Prevents scope creep.

## 2. Context (2-5 sentences)

The minimum project/domain context needed. Not a tutorial.

**Example:**
> "The project uses Framework v0.8, Styling System v4 (standalone binary, no runtime), and Database via ORM."

**Purpose:** Provides essential constraints without overwhelming the agent with background.

**Guidelines:**
- Include versions, platform constraints, non-negotiable requirements
- Exclude history, rationale, architectural philosophy
- Exclude information not relevant to the specific task

## 3. Input Files (explicit paths)

Every file the agent must read, with absolute paths.

**Example:**
> "Read these files: 1. `/path/to/project/manifest.toml` 2. `/path/to/guidance/system-design.md`"

**Purpose:** Eliminates ambiguity. Agent knows exactly what to read.

**Guidelines:**
- Always use absolute paths
- Number the files if there are multiple
- Do not rely on the agent to "find" files — provide exact locations

## 4. Task (numbered steps)

Precisely what to do, in order. Each step produces or consumes something concrete.

**Example:**
> "1. Read the manifest file. 2. For each dependency, note version and purpose. 3. Check for version conflicts with the specified framework version. 4. List any deprecated dependencies."

**Purpose:** Gives the agent a clear procedure to follow. Prevents drift and misinterpretation.

**Guidelines:**
- Use numbered steps
- Each step should be verifiable
- Each step should produce data or a decision
- Avoid vague directives like "assess quality" — specify what to check

## 5. Output Path (exact file)

Where to write the report. Absolute path.

**Example:**
> "Write your report to `/path/to/research/dependency-audit.md`"

**Purpose:** Ensures report-based communication. The orchestrator can point future agents to this file.

**Guidelines:**
- Always absolute paths
- Use descriptive filenames that indicate the agent's task
- Organize reports by task type or phase (e.g., `/research/`, `/audits/`, `/synthesis/`)

## 6. Report Format (pasted inline)

The exact template. Agents can't read skill files — paste the format.

**Example:**
```markdown
Use this format:

# Dependency Audit

## Dependencies Analyzed
- [Dependency name]: version, purpose

## Version Conflicts
- [Conflict description]

## Deprecated Dependencies
- [Dependency name]: deprecated since [version], recommended alternative: [alternative]

## Summary
[2-3 sentence summary]
```

**Purpose:** Ensures consistency across agents. Enables automated synthesis.

**Guidelines:**
- Paste the exact format inline — do not reference external files
- Use markdown headings for structure
- Specify what goes in each section
- Include examples if the format is complex

## 7. Scope Boundaries

What to do AND what NOT to do. Critical for preventing drift.

**Example:**
> "DO: check every dependency in the manifest. DO NOT: suggest changes, read source code, or assess code quality."

**Purpose:** Prevents agents from making recommendations when you only want facts, or analyzing aspects outside their scope.

**Guidelines:**
- Always include both DO and DO NOT lists
- Be explicit about what the agent should NOT do
- For haiku agents, explicitly forbid judgment, evaluation, recommendations if you only want facts

## 8. Tool Expectations

Which tools the agent should use.

**Example:**
> "Use WebFetch for registry APIs, Read for local files, Grep for codebase search."

**Purpose:** Guides tool selection. Prevents agents from trying to "find" things manually or giving up when a tool would work.

**Guidelines:**
- List specific tools by name
- Indicate what each tool is for in this task
- If a tool requires specific syntax, provide an example

## 9. Prime Directive (for research agents)

The encourage/discourage framework adapted to the domain. See research-tree skill.

**Example:**
> "ENCOURAGE investigation of: active projects (updated within 6 months), projects with clear documentation, projects with stable APIs. DISCOURAGE investigation of: archived projects, projects with no activity in 12+ months, projects marked experimental."

**Purpose:** Guides the agent's prioritization without micromanaging every decision.

**Guidelines:**
- Only needed for research/exploration agents
- Focus on objective criteria (dates, metrics, presence/absence of features)
- Avoid subjective judgments unless absolutely necessary

## The Prompt Quality Shortcut

A well-structured prompt for haiku outperforms a vague prompt for sonnet. If you're tempted to upgrade the model, first try improving the prompt. Apply prompt-optimize skill principles if the prompt feels weak.

### Prompt Quality Checklist

Before launching an agent batch, verify every prompt has:
- [ ] Clear role statement
- [ ] Minimal but sufficient context
- [ ] Absolute file paths for all inputs
- [ ] Numbered task steps
- [ ] Absolute output path
- [ ] Pasted report format
- [ ] DO and DO NOT lists
- [ ] Tool usage guidance
- [ ] (If research) Prime directive with encourage/discourage criteria

### Common Prompt Failures

| Failure | Signal | Fix |
|---------|--------|-----|
| Agent produces shallow output | Vague task steps | Add numbered steps with specific actions |
| Agent makes unwanted recommendations | Missing scope boundaries | Add explicit DO NOT list |
| Agent says "couldn't find" | Missing tool guidance | Add tool expectations with examples |
| Agent produces wrong format | Format not pasted | Paste exact format inline, with examples |
| Agent drifts off-topic | Weak role or scope | Strengthen role statement, add DO NOT list |
| Agent can't find files | Relative paths or no paths | Use absolute paths for all inputs |

## Example: Complete Agent Prompt

Here's a complete prompt following all 9 sections:

```
You are cataloging the dependency tree of a web application for compatibility verification.

The project uses Leptos 0.8, Tailwind CSS v4 (standalone binary, no Node.js), and Postgres via sqlx. All dependencies must be compatible with these versions.

Read these files:
1. `/home/project/Cargo.toml`
2. `/home/project/guidance/tech-stack.md`

Task:
1. Read Cargo.toml and extract all dependencies
2. For each dependency, note: name, version, and stated purpose (from comments or context)
3. Check if any dependency has version constraints that conflict with Leptos 0.8 or sqlx
4. Identify any dependencies marked as deprecated in their crates.io metadata
5. Write findings to the specified output path

Write your report to `/home/project/research/dependency-catalog.md`

Use this format:

# Dependency Catalog

## All Dependencies
- [name]: v[version] — [purpose]

## Version Conflicts
- [dependency name]: requires [constraint], conflicts with [Leptos 0.8 | sqlx]

## Deprecated Dependencies
- [name]: deprecated since [version], alternative: [alternative]

## Summary
[2-3 sentences summarizing total dependencies, any conflicts, any deprecated packages]

DO: catalog every dependency, check version constraints, check deprecation status
DO NOT: recommend changes, assess code quality, read source code beyond Cargo.toml

Use Read for Cargo.toml, WebFetch for crates.io metadata.

ENCOURAGE investigation of: dependencies with clear version constraints, dependencies with recent crates.io activity
DISCOURAGE investigation of: transitive dependencies (only direct dependencies needed), dev-dependencies
```

This prompt gives the agent everything it needs and nothing it doesn't need.
