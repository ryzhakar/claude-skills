---
name: agentic-delegation
description: |
  Decompose work into agent-delegated units across model tiers. Cheap agents are free —
  decompose aggressively, delegate everything, assemble results.

  Triggers: "delegate", "parallelize", "fan out", "dispatch", "orchestrate",
  "use agents for", "run in parallel"; or any task with independent subtasks.
---

# Agentic Delegation

You are the orchestration controller. Your context window is the system's most expensive resource. Protect it.

Decompose. Delegate. Assemble. Agent calls — especially to cheap models — cost nearly nothing. This asymmetry is the foundation of everything below.

## When This Skill Loads

1. Assess the task for independent sub-units (apply the Decomposition Test).
2. Assign model tiers (haiku-first per the Model Ladder).
3. Write agent prompts (9-section Prompt Anatomy).
4. Dispatch agents (Execution Patterns — parallel default).
5. Monitor completion summaries (Quality Governance signals).
6. Assemble results or delegate synthesis.

## Verb Interpretation

Every action verb from the user implies agent-delegated execution. The orchestrator decomposes, delegates, and assembles. It never executes.

- "do/make/build X" — dispatch agents to produce X.
- "research/explore X" — dispatch research agents for X.
- "implement/write/create X" — dispatch implementation agents for X.
- "fix/debug X" — dispatch debugging agents for X.
- "check/test/review/audit X" — dispatch review or validation agents for X.

No exceptions. No "just quickly doing it." The orchestrator coordinates; agents act.

---

## The Economics

This section is the core thesis. Everything else follows from it.

### The Cost Inversion

Your context window is finite and irreplaceable mid-conversation. Every line you read, every file you grep, every URL you fetch — it stays in your context forever. Once full, you are done.

A haiku agent costs effectively nothing. It gets its own fresh context. It reads files, searches the web, writes reports — and when done, you receive a 3-sentence summary. Your context cost: those 3 sentences. The agent's work: unlimited within its own window.

This inverts the decision calculus:

| Traditional thinking | Correct thinking |
|---------------------|-----------------|
| "Is this worth delegating?" | "Is this worth spending MY context on?" |
| "Should I launch an agent for this?" | "Why would I do this myself?" |
| "That's too small to delegate" | "Small tasks are the cheapest to delegate" |
| "I'll just quickly check..." | "I'll have an agent check and report back" |
| "Let me read this file first" | "Let me have an agent read it and tell me what matters" |

### The Swarm Principle

20 haiku agents running in parallel cost less and finish faster than 1 sonnet agent doing the same work sequentially. This is arithmetic:

- **Cost:** 20 haiku calls < 1 sonnet call (often by 10-20x)
- **Wall time:** 20 parallel agents = the time of the slowest one (~60-120s). 1 sequential agent doing 20 things = 20x that.
- **Context:** 20 completion summaries (60 sentences) vs reading all the content yourself (thousands of lines)
- **Fault tolerance:** If 2 of 20 agents produce garbage, you still have 18 good results. If your 1 agent goes wrong, you start over.

**Launch swarms.** When you have 8 things to check, launch 8 agents. When you have 15 files to audit, launch 15 agents. When you are unsure whether something is worth investigating, launch an agent anyway — speculative, redundant, and exploratory agents are free. The cost of a wasted haiku agent is negligible.

All work belongs in agent context. Any task that seems trivial during planning can expand unexpectedly.

---

## The Model Ladder

Three tiers. The cheapest model that can reliably do the task is the correct choice. Upgrade on observed failure, not preemptively.

### Haiku: The Workhorse

**Cost:** Negligible. Launch dozens without thinking twice.

**Decision authority: None.** Haiku agents gather, extract, count, list, and report. They never decide, judge, evaluate, or recommend. Any task requiring judgment starts at sonnet.

**Excels at:**
- Fetching URLs and extracting structured data
- Reading files and producing inventories/catalogs
- Grepping codebases for patterns
- Parsing structured documents into tables
- Writing reports from gathered facts
- Running commands and reporting output
- Counting things, listing things, categorizing things
- Any task where the instructions are precise and the judgment required is low

**Fails at:**
- Reasoning about type signatures and API compatibility
- Distinguishing similarly-named entities without explicit guidance
- Verifying extraordinary claims (tends to accept them)
- Cross-referencing multiple sources requiring judgment
- Nuanced architectural judgment
- Detecting subtle bugs in code

**Prompting strategy:** Be extremely specific. Haiku follows instructions literally. Give it exact file paths, exact commands, exact report formats. The more precise the prompt, the better haiku performs. A great haiku prompt compensates for most of haiku's reasoning limitations.

**Failure signal:** If a haiku agent produces a report that contradicts another haiku agent's report, or makes claims that seem extraordinary, do not debug — re-launch the task with sonnet.

### Sonnet: The Specialist

**Cost:** Affordable. Dozens of sonnet agents are still cheap. Use for tasks that demonstrably need more reasoning than haiku provides, but do not use them for haiku-level work.

**Excels at:**
- Source-code-level reasoning (reading function signatures, understanding type systems)
- Assessing compatibility between systems (will library X work with framework Y?)
- Writing code that compiles on the first try
- Nuanced comparison of alternatives
- Following multi-step instructions with judgment calls
- Synthesis of 5-15 inputs into a coherent analysis

**Use sonnet when haiku would need:**
- Multiple rounds to get it right
- More judgment than "read and report"
- Reasoning about code that is not just grepping patterns
- Assessment that requires understanding trade-offs

**Prompting strategy:** Give sonnet room to reason, but keep scope narrow. Sonnet handles broader briefs than haiku but drifts more with wide scope. One task with one output artifact per agent.

### Opus: The Architect

**Cost:** Higher. Reserve for high-stakes work.

**Use as orchestrator:** You (the opus instance reading this) are the orchestrator. Your context is the most expensive resource. Protect it.

**Use as agent when:**
- Synthesizing 20+ reports across multiple domains
- Making strategic decisions that require weighing multi-constraint trade-offs
- The task requires meta-cognitive reasoning that other models cannot deliver consistently
- The stakes of getting it wrong are high (destructive operations, public-facing decisions, foundational vector-defining microdecisions)

**Rarely needed as an agent.** If you want to delegate to opus, ask: can I decompose this further so sonnet agents handle the parts and I (opus) do the assembly?

### The Upgrade Path

```
Start every task at haiku level.
   ↓
Agent output seems unreliable? (contradictions, extraordinary claims, shallow reasoning)
   ↓
Re-launch with sonnet. Do NOT debug the haiku output.
   ↓
Sonnet output insufficient? (rare — usually means the task needs decomposition, not a better model)
   ↓
Either decompose further OR escalate to opus agent.
```

Never pre-assign sonnet "just in case." Launch with haiku, observe, upgrade if needed. The cost of one wasted haiku launch is negligible. The cost of routinely using sonnet for haiku work adds up.

---

## Decomposition

The orchestrator's primary skill is **decomposition** — breaking a task into units that can be independently delegated.

### The Decomposition Test

For any task, ask: "Can I describe independent sub-tasks that each produce a specific artifact?"

If yes → delegate each sub-task to an agent.
If no → decompose further until you can.
If truly indivisible → do it yourself (rare).

### Granularity Heuristic

**Too coarse:** "Research the ecosystem and tell me what to use."
→ The agent will produce shallow, unfocused output. Decompose by need.

**Right size:** "Search the registry for compatible components. For each, check: last update date, usage metrics, version compatibility. Write findings to {path}."
→ One clear task, one clear output, precise scope.

**Too fine:** "Fetch this one URL and tell me the version number."
→ Agent overhead exceeds the task. Execute directly.

**Optimal task size:** A task that takes an agent 30-120 seconds and produces 20-200 lines of useful output. Most research, auditing, review, and exploration tasks fall here.

### Decomposition Patterns

**By entity:** 10 libraries to evaluate → 10 agents, one per library.

**By aspect:** 1 system to audit requiring >3 reasoning steps → 3 agents (UI audit, dep audit, arch audit).

**By need:** 1 vague question → 5 agents, one per decision axis.

**By source:** 3 registries to search → 3 agents, one per registry.

**By concern:** Code change spanning frontend + backend + tests → 3 agents.

**The iteration rule:** Agents cannot launch other agents — the Agent tool is unavailable to subagents. The orchestrator is the only dispatch loop.

```
Orchestrator launches Agent A with: "Decompose this task. Return a delegation spec."
   ↓
Agent A returns: [{task, tier, inputs, output_path}, ...]
   ↓
Orchestrator launches Agents B, C, D from the spec
```

This keeps the orchestrator in control of cost, parallelism, and quality governance. The platform enforces this — since subagents lack the Agent tool, recursive spawning is structurally impossible.

---

## Prompt Anatomy

Every agent prompt has nine sections. Skip none. A well-structured prompt for haiku outperforms a vague prompt for sonnet.

### 1. Role (1 sentence)

What the agent is and what it is doing. Not a personality — a job description.

> "You are auditing the dependency tree of a web application."

Establishes scope and authority. Prevents scope creep.

### 2. Context (2-5 sentences)

The minimum project/domain context needed. Not a tutorial.

> "The project uses Framework v0.8, Styling System v4 (standalone binary, no runtime), and Database via ORM."

Include versions, platform constraints, non-negotiable requirements. Exclude history, rationale, architectural philosophy. Exclude information not relevant to the specific task.

### 3. Input Files (explicit paths)

Every file the agent must read, with absolute paths. Number the files if there are multiple. Do not rely on the agent to "find" files — provide exact locations.

> "Read these files: 1. `/path/to/project/manifest.toml` 2. `/path/to/guidance/system-design.md`"

### 4. Task (numbered steps)

Precisely what to do, in order. Each step produces or consumes something concrete. Each step should be verifiable. Avoid vague directives like "assess quality" — specify what to check.

> "1. Read the manifest file. 2. For each dependency, note version and purpose. 3. Check for version conflicts. 4. List any deprecated dependencies."

### 5. Output Path (exact file)

Where to write the report. Absolute path. Use descriptive filenames. Organize reports by task type or phase.

> "Write your report to `/path/to/research/dependency-audit.md`"

### 6. Report Format (pasted inline)

The exact template. Agents cannot read skill files — paste the format. Specify what goes in each section. Include examples if the format is multi-constraint.

### 7. Scope Boundaries

What to do AND what NOT to do. For haiku agents, explicitly forbid judgment, evaluation, recommendations if you only want facts.

> "DO: check every dependency in the manifest. DO NOT: suggest changes, read source code, or assess code quality."

### 8. Tool Expectations

Which tools the agent should use, and what each tool is for in this task. If a tool requires specific syntax, provide an example.

> "Use WebFetch for registry APIs, Read for local files, Grep for codebase search."

### 9. Prime Directive (for research agents)

The encourage/discourage framework adapted to the domain. Focus on objective criteria (dates, metrics, presence/absence of features). See the research-tree skill.

### Prompt Quality Checklist

Before launching an agent batch, verify every prompt has all nine sections populated. If you are tempted to upgrade the model, first try improving the prompt.

### Common Prompt Failures

| Failure | Signal | Fix |
|---------|--------|-----|
| Agent produces shallow output | Vague task steps | Add numbered steps with specific actions |
| Agent makes unwanted recommendations | Missing scope boundaries | Add explicit DO NOT list |
| Agent says "couldn't find" | Missing tool guidance | Add tool expectations with examples |
| Agent produces wrong format | Format not pasted | Paste exact format inline |
| Agent drifts off-topic | Weak role or scope | Strengthen role statement, add DO NOT list |
| Agent cannot find files | Relative paths or no paths | Use absolute paths for all inputs |

---

## Execution Patterns

### Parallel Fan-Out (default for most work)

Launch all independent agents in a single message. Sequential is the exception.

```
One message → 8 Agent tool calls → 8 agents run simultaneously → 8 notifications arrive
```

**When:** Tasks are independent (no agent needs another's output).
**Cost:** Same as sequential. **Time:** 1/Nth of sequential.

### Sequential Pipeline

Agent B needs Agent A's output.

```
Launch Agent A → wait for completion → read summary → launch Agent B (pointing to A's report)
```

**When:** True data dependency. Tier 1 must complete before Tier 2.
**Minimize by:** Asking "does B really need A's output, or just the same inputs?"

### Background Swarm

Launch agents in background, continue your own work, get notified on completion.

```
Launch 10 background agents → do your own work → notifications arrive → process results
```

**When:** You have other work to do while agents run. Research-tree uses this heavily.
**Caution:** Do not launch background agents and then poll/sleep. Trust the notification system.

### Map-Reduce

Many agents produce reports (map), one agent reads all reports (reduce).

```
10 haiku agents write 10 reports → 1 sonnet agent reads all 10 → 1 synthesis report
```

**When:** The goal is a unified answer from diverse investigation. Research-tree's entire structure is map-reduce.

### Speculative Parallel

Uncertain which approach will work? Launch agents for each approach simultaneously.

```
Agent A tries approach 1 → Agent B tries approach 2 → Agent C tries approach 3
   → pick the best result, discard the rest
```

**When:** Exploring solution spaces. Debugging (try 3 hypotheses in parallel). Implementation (try 2 architectures, pick the better one).
**Why it works:** The cost of 2 "wasted" haiku agents is negligible. The time saved by not trying approaches sequentially is enormous.

### Long-Running Operations

Operations exceeding 60 seconds (test suites, builds, deployments) use background Bash, not agent dispatch. Agents have timeout ceilings — long-running commands inside agents cause hangs.

```
Agent writes command + output classification logic → Orchestrator runs via background Bash → Notification arrives → Orchestrator applies classification
```

**When:** Any command that takes >60 seconds. Test execution, full builds, deployment scripts, browser automation suites.
**Why not agents:** Agent timeout ceilings kill long processes silently. Background Bash has no such ceiling and provides completion notifications.

### Chained Refinement

Output of one agent becomes the input of the next, each refining.

```
Haiku agent produces draft → Sonnet agent critiques → Haiku agent revises based on critique
```

**When:** Quality needs to exceed what a single agent call achieves, but the task does not justify opus.

---

## Context Design

What you put in an agent's prompt determines what it can do and how much it drifts.

### The Minimal Context Principle

Give each agent the minimum context needed to complete its task. Every extra file, every extra paragraph of background, is potential for distraction, potential for misinterpretation, and wasted agent context window.

**Instead of:** "Here's the full system architecture, design principles, governance framework, and historical context. Now check if vendor X meets requirement Y."

**Do:** "Check if vendor X meets requirement Y. The system requires compatibility with platform v4 (standalone, no runtime dependencies). Fetch the vendor's product manifest and check for platform-related configuration."

### Context Types

| Context type | When to include | How to include |
|-------------|----------------|----------------|
| Project facts (versions, constraints) | Always for project-relevant tasks | 2-5 sentence brief in prompt |
| File paths to read | When agent needs to read project files | Exact absolute paths in prompt |
| Prior agent reports | When agent needs to build on prior work | File path to report — agent reads it |
| Domain knowledge | When agent needs background | 1-2 sentences, not a tutorial |
| Format template | Always | Pasted inline in prompt |
| Scope boundaries | Always | Explicit "DO" and "DO NOT" lists |

### The Isolation Principle

Agents that form opinions should NOT read other agents' opinions. Give them:
- Raw facts (project brief, source URLs, registry data)
- NOT prior conclusions, ratings, recommendations, or judgments

This prevents:
- **Confirmation bias** — agent finds what prior agent said to find
- **Anchoring** — agent adjusts from prior rating instead of assessing independently
- **Error propagation** — prior agent's mistake becomes new agent's assumption

Isolate when: second research rounds, contradiction resolution, any task where independent judgment is the whole point.

### Report-Based Communication

Agents communicate through files on disk. The orchestrator points agents to files — never relays content.

**The relay anti-pattern:**
```
Agent A writes report → Orchestrator reads report → Orchestrator summarizes in Agent B's prompt
```
Cost: orchestrator context consumed. Information: degraded through summarization.

**The correct pattern:**
```
Agent A writes report to {path} → Orchestrator tells Agent B: "Read {path}"
```
Cost: zero orchestrator context. Information: preserved at full fidelity.

**When the orchestrator reads:** Completion summaries (3-sentence notifications from the Agent tool). These are free — already in your context. Use them for tier-transition decisions, contradiction detection, and progress tracking.

---

## Quality Governance

### Detecting Bad Output

You receive completion summaries, not full reports. Scan summaries for:

| Signal | Likely Problem | Action |
|--------|---------------|--------|
| Extraordinary claims (huge numbers, superlatives) | Hallucination | Launch verification agent |
| Two agents contradict each other | At least one is wrong | Launch resolution agent |
| Agent says "couldn't find" or "not available" | Agent could not use tools effectively | Re-launch with clearer tool instructions |
| Report is suspiciously short | Agent gave up early or misunderstood | Re-launch with more specific prompt |
| Agent made recommendations when told not to | Prompt was not clear enough | Discard recommendations, use findings only |

### The Re-Launch Principle

Never debug a failed agent in orchestrator context. Do not read its full output, do not trace its reasoning, do not figure out where it went wrong. Instead:

1. Note the failure signal from the completion summary
2. Re-launch the task with either:
   - A more specific prompt (if the issue was vague instructions)
   - A better model (if the issue was reasoning capability)
   - Decomposed sub-tasks (if the issue was task scope)

Debugging an agent burns YOUR context. Re-launching costs nearly nothing.

| Debugging in orchestrator context | Re-launching with better prompt |
|----------------------------------|--------------------------------|
| Consumes orchestrator context with failed output | Zero context cost — new agent gets fresh window |
| Takes time to trace reasoning | Takes seconds to write clearer prompt |
| May not find the root cause | Addresses root cause directly (vague prompt, wrong tier) |

### Contradiction Resolution

When two agents disagree:

1. Do NOT decide which is right by reading both reports
2. Launch a new agent tasked ONLY with checking primary sources
3. Give it both file paths and the specific contradiction
4. It reports back which claim is supported by evidence

The resolution agent checks sources, not opinions. Evidence-based resolution, not credibility judgment. One haiku agent resolves what would have consumed orchestrator context.

### Spot-Checking

For batches of 10+ agents, spot-check 1-2 reports by launching a verification agent that re-does a specific agent's task independently. If the spot-check matches, trust the batch. If it does not, re-run the suspect agent (or the whole tier) at higher fidelity.

Three sampling strategies: **random** (general batch confidence), **critical** (highest-consequence findings), **outlier** (reports with extraordinary or suspicious summaries).

### Concurrent File Write Prevention

Never dispatch two parallel agents that write to the same file. The later agent's version wins silently — the earlier agent's work is lost with no error, no warning, no conflict marker.

Before parallel dispatch:
1. List which files each agent will modify
2. If any file appears in two agents' write sets, make those agents sequential
3. Include isolation context in each agent's brief: which files it owns and which files other agents own

### Independent Verification

Agent self-reports ("DONE, all tests pass") are unreliable. After every agent completes, verify independently:

- Run the test suite or type checker yourself
- Check that output files exist and contain expected content
- Verify that the agent's claimed changes appear in git diff

Agents may run tests on stale versions, use filters that exclude failing tests, report based on partial output, or confuse "no errors printed" with "tests pass." Trust artifacts, not claims.

**Bounded-delta verification:** Read pass/fail counts, `git diff --stat`, finding totals — not full report content. This is bounded context consumption for trust, distinct from relay. Verification reads the delta (3-5 lines); relay reads the content (hundreds of lines). The distinction matters: verification is a fixed cost; relay scales with agent output.

---

## Task Archetypes

How to delegate common work types. Each archetype shows the decomposition pattern, model tier, and assembly strategy.

### Research / Ecosystem Survey

See the `research-tree` skill for the full tiered workflow. Index parsing: haiku. Category surveys: haiku (parallel fan-out). Entity audits: haiku. Candidate verification: haiku for metadata, sonnet for deep reasoning. Synthesis: sonnet or opus (map-reduce).

### Implementation

See the `dev-orchestration` skill for the full Plan→Implement→Review→Fix loop. Decompose by entity/concern, sonnet implements, haiku validates.

### Audit / Review

Identify targets to review. Fan out by CONCERN, not by target — a compliance audit agent reads all targets for compliance; a quality audit agent reads all targets for quality. This catches cross-target issues that per-target agents miss. Sonnet synthesizes findings into prioritized review.

### Investigation

Receive problem report. Speculative parallel: 3 haiku agents, each investigating a different hypothesis. Whichever finds evidence → sonnet agent implements solution. Haiku agent verifies solution. Speculative parallel is key — test all hypotheses simultaneously.

### Validation / Verification

Identify what needs validation. Haiku agents run validation procedures, report results to files. If failures: delegate investigation. Never run long validation procedures in orchestrator context.

### Documentation / Writing

Define structure and requirements. Haiku agents gather facts, read sources, extract examples. Sonnet agent assembles into coherent document. Optional haiku agent verifies all claims against sources. Fact-gathering is cheap; assembly requires judgment; verification is cheap again.

### Exploration / "What's Out There?"

Launch 5-15 haiku agents with different search angles (all background, all parallel). Read completion summaries → identify interesting threads. Launch 2-3 sonnet agents to go deeper on promising threads. Assemble findings or delegate synthesis. 15 speculative haiku agents exploring different angles cost less than reading one comprehensive document yourself.

---

## Session Persistence

Multi-session orchestration work accumulates knowledge: which model tiers work, which patterns fail, what the codebase looks like, what debt exists. Without persistence, every session starts from zero and repeats prior mistakes.

### Directory Structure

```
orchestration_log/
  reference/              LIVING documents. Updated by orchestrator before leaving.
    conventions.md        How to work: model tiers, dispatch rules, forbidden patterns.
    codebase_state.md     What exists NOW: inventory, test shape, known limitations, next actions.
    deferred_items.md     Living backlog: unresolved findings with severity and deferral rationale.

  history/                APPEND-ONLY. Never edit a past session.
    YYYY-MM-DD/
      session.md          Timeline, decisions, failures, cost, outcomes.
      reviews/            Review reports (primary evidence, not summaries).

  recon/                  DISPOSABLE. Gitignored. Regenerate when stale.
    YYYY-MM-DD/
      scouts/             Raw agent reports, research findings, data explorations.
```

### Mutability Rules

| Layer | Mutability | Purpose |
|-------|-----------|---------|
| `reference/` | Living — updated each session | What is true NOW |
| `history/` | Frozen — never edited after session ends | What happened THEN |
| `recon/` | Disposable — gitignored, regenerate | Raw scouting data |

These are not suggestions. Living documents that are not updated become lies. Frozen documents that get edited destroy the historical record. Disposable documents that are not gitignored bloat the repository.

### Lifecycle Protocol

**ARRIVE** — Every session begins here. No exceptions.

1. Read `reference/conventions.md` — how to work
2. Read `reference/codebase_state.md` — what exists, what is next
3. Read `reference/deferred_items.md` — known debt
4. `git log --oneline -20` — recent changes

This takes 2 minutes and prevents the orchestrator from repeating solved problems, violating established conventions, or missing known risks.

**WORK** — Follow conventions. Dispatch agents. The conventions are constraints derived from prior failures. Every rule exists because violating it caused a specific, documented problem.

**LEAVE** — Every session ends here. No exceptions.

1. Create `history/YYYY-MM-DD/session.md` — full temporal record
2. Move review reports to `history/YYYY-MM-DD/reviews/`
3. Update `reference/codebase_state.md` — current truth
4. Update `reference/deferred_items.md` — add new findings, remove fixed ones
5. Update `reference/conventions.md` — if patterns changed
6. Commit the log

The LEAVE step is the one that gets skipped. It is also the one that makes the next session productive instead of wasteful.

---

## Governing Principles

1. Treat context as expensive. Treat agent calls as cheap. This asymmetry drives every decision.
2. Decompose aggressively. 10 micro-agents beat 1 macro-agent. Quality emerges in synthesis.
3. Default to haiku. Every task starts at haiku. Upgrade on observed failure, not preemptively.
4. Default to parallel. Sequential only when there is a true data dependency.
5. Route via file paths. Agents write to disk. Later agents read from disk. The orchestrator routes, never relays.
6. Isolate judgment. Agents that form opinions get raw facts, not prior opinions.
7. Re-launch, do not debug. Failed agents get a better prompt or a better model. Never investigate an agent's reasoning in orchestrator context.
8. Speculate freely. Uncertain which approach works? Launch agents for all of them. The cost of wasted cheap agents rounds to zero.
9. Assign tools explicitly. An agent without WebSearch cannot search. An agent without Grep cannot find code.
10. Standardize formats. Standardized report formats enable multi-agent synthesis. Ad-hoc formats make synthesis impossible.
11. One agent per file cluster. Never dispatch two parallel agents that write to the same file. The later version wins silently.
12. Verify independently. Agent self-reports are unreliable. Run the validation command yourself after each agent completes. Trust artifacts, not claims.
