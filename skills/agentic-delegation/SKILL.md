---
name: agentic-delegation
version: 1.0.0
description: |
  The universal framework for decomposing work into agent-delegated units across model tiers.
  Use this skill whenever work can be broken into parts — research, implementation, review,
  debugging, testing, auditing, exploration, writing, or any combination.

  Core thesis: cheap agents are essentially free. Decompose aggressively, delegate everything,
  assemble the results. A swarm of micro-agents almost always beats a single capable agent.

  Triggers: any multi-step task, any task where you'd "need to check something first",
  any task with independent subtasks, any exploration, any audit, any research,
  "delegate", "parallelize", "fan out", "use agents for".
---

# Agentic Delegation

Decompose. Delegate. Assemble. Your context window is the most expensive resource in the system. Agent calls — especially to cheap models — are nearly free. This asymmetry is the foundation of everything below.

## The Economics

This section is not background. It is the core thesis. Everything else follows from it.

### The Cost Inversion

Your context window is finite and irreplaceable mid-conversation. Every line you read, every file you grep, every URL you fetch — it stays in your context forever. Once it's full, you're done.

A haiku agent costs effectively nothing. It gets its own fresh context. It reads files, searches the web, writes reports — and when it's done, you receive a 3-sentence summary. Your context cost: those 3 sentences. The agent's work: unlimited within its own window.

**This means the decision calculus is inverted:**

| Traditional thinking | Correct thinking |
|---------------------|-----------------|
| "Is this worth delegating?" | "Is this worth spending MY context on?" |
| "Should I launch an agent for this?" | "Why would I do this myself?" |
| "That's too small to delegate" | "Small tasks are the CHEAPEST to delegate" |
| "I'll just quickly check..." | "I'll have an agent check and report back" |
| "Let me read this file first" | "Let me have an agent read it and tell me what matters" |

### The Swarm Principle

20 haiku agents running in parallel cost less and finish faster than 1 sonnet agent doing the same work sequentially. This is not a theoretical claim — it's arithmetic:

- **Cost:** 20 haiku calls < 1 sonnet call (often by 10-20x)
- **Wall time:** 20 parallel agents = the time of the slowest one (~60-120s). 1 sequential agent doing 20 things = 20x that.
- **Context:** 20 completion summaries (60 sentences) vs reading all the content yourself (thousands of lines)
- **Fault tolerance:** If 2 of 20 agents produce garbage, you still have 18 good results. If your 1 agent goes wrong, you start over.

**Launch swarms. Not individuals.** When you have 8 things to check, don't check them — launch 8 agents. When you have 15 files to audit, launch 15 agents. When you're not sure whether something is worth investigating, launch an agent anyway — the cost of a wasted haiku agent is literally negligible.

### What "Negligible Cost" Actually Means

A haiku agent that:
- Fetches a URL and extracts 3 facts
- Reads 2 local files and summarizes patterns
- Greps a codebase for a pattern and counts occurrences
- Writes a 50-line report to disk

...costs less than you reading ONE medium-sized file into your context.

This means:
- **Speculative agents are free.** Not sure if something is relevant? Launch an agent. If it comes back empty, you lost nothing.
- **Redundant agents are fine.** Two agents checking the same thing from different angles? Good — you get cross-validation for free.
- **"Nice to know" is worth an agent.** Background context that might inform a decision later? Launch an agent. You'll be glad you did, or it cost you nothing.
- **Exploration is always delegated.** Never explore a codebase, an API, a website yourself. Send agents. Read their summaries.

### When NOT to Delegate

The only reasons to do something yourself:

1. **You need the information to make the NEXT decision in the SAME message.** If you can't proceed without the answer, and you can't do other work while waiting, a foreground agent adds latency. But even then — consider whether you can launch the agent AND do other work in parallel.

2. **The task is literally 1 tool call.** Reading a specific known file path, running a specific known command. The overhead of agent setup exceeds the task.

3. **You need to EDIT a file based on context you already have.** Agents can edit, but if you already know exactly what to change, do it yourself.

Everything else? Delegate.

---

## The Model Ladder

Three tiers. The cheapest model that can reliably do the task is the correct choice. Upgrade on observed failure, not preemptively.

### Haiku: The Workhorse

**Cost:** Negligible. Launch dozens without thinking twice.

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
- Cross-referencing multiple complex sources
- Nuanced architectural judgment
- Detecting subtle bugs in code

**Prompting strategy:** Be EXTREMELY specific. Haiku follows instructions literally. Give it exact file paths, exact commands, exact report formats. The more precise the prompt, the better haiku performs. A great haiku prompt compensates for most of haiku's reasoning limitations.

**Failure signal:** If a haiku agent produces a report that contradicts another haiku agent's report, or makes claims that seem extraordinary, don't debug — re-launch the task with sonnet.

### Sonnet: The Specialist

**Cost:** Moderate. Use for tasks that demonstrably need more reasoning than haiku provides. Dozens of sonnet agents are still cheap — don't be afraid to use them, but don't use them for haiku-level work.

**Excels at:**
- Source-code-level reasoning (reading function signatures, understanding type systems)
- Assessing compatibility between systems (will library X work with framework Y?)
- Writing code that compiles on the first try
- Nuanced comparison of alternatives
- Following complex multi-step instructions with judgment calls
- Synthesis of 5-15 inputs into a coherent analysis

**Use sonnet when haiku would need:**
- Multiple rounds to get it right
- More judgment than "read and report"
- Reasoning about code that isn't just grepping patterns
- Assessment that requires understanding trade-offs

**Prompting strategy:** Give sonnet room to reason, but keep scope narrow. Sonnet handles broader briefs than haiku but drifts more with wide scope. One focused task per agent.

### Opus: The Architect

**Cost:** High. Reserve for the orchestrator role and rare high-stakes synthesis.

**Use as orchestrator:** You (the opus instance reading this) are the orchestrator. Your context is the most expensive resource. Protect it.

**Use as agent only when:**
- Synthesizing 20+ reports across multiple domains
- Making strategic decisions that require weighing complex trade-offs
- The task requires the kind of meta-cognitive reasoning that sonnet can't do
- The stakes of getting it wrong are very high (destructive operations, public-facing decisions)

**Almost never needed as an agent.** If you find yourself wanting to delegate to opus, ask: can I decompose this further so sonnet agents handle the parts and I (opus) do the assembly?

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

The orchestrator's primary skill is not coding, not researching, not writing. It is **decomposition** — breaking a task into units that can be independently delegated.

### The Decomposition Test

For any task, ask: "Can I describe independent sub-tasks that each produce a specific artifact?"

If yes → delegate each sub-task to an agent.
If no → decompose further until you can.
If truly indivisible → do it yourself (rare).

### Granularity Heuristic

**Too coarse:** "Research the JavaScript ecosystem and tell me what to use."
→ The agent will produce shallow, unfocused output. Decompose by need.

**Right size:** "Search npm for Tailwind-compatible datepicker components. For each, check: last publish date, weekly downloads, Tailwind version compatibility. Write findings to {path}."
→ One clear task, one clear output, precise scope.

**Too fine:** "Fetch this one URL and tell me the version number."
→ Just do it yourself. Agent overhead exceeds the task.

**Sweet spot:** A task that takes an agent 30-120 seconds and produces 20-200 lines of useful output. Most research, auditing, code review, and exploration tasks fall here.

### Decomposition Patterns

**By entity:** 10 libraries to evaluate → 10 agents, one per library.

**By aspect:** 1 complex system to audit → 3 agents (UI audit, dep audit, arch audit).

**By need:** 1 vague question → 5 agents, one per decision axis.

**By source:** 3 registries to search → 3 agents, one per registry.

**By concern:** Code change spanning frontend + backend + tests → 3 agents (or do frontend yourself, delegate review to agents).

**The fractal rule:** If an agent's task is still "big," it should further decompose and delegate sub-agents. Research-tree's tier system is an example: the orchestrator delegates to survey agents, which could in theory delegate to per-entry agents if the category is large enough.

---

## Context Design

What you put in an agent's prompt determines what it can do and how much it drifts.

### The Minimal Context Principle

Give each agent the MINIMUM context needed to complete its task. Every extra file, every extra paragraph of background, is:
- Potential for distraction
- Potential for misinterpretation
- Wasted agent context window

**Instead of:** "Here's the full project architecture, the design system, the test guide, and the coding conventions. Now check if library X supports Tailwind v4."

**Do:** "Check if library X supports Tailwind v4. The project uses Tailwind v4 standalone (no Node.js, no tailwind.config.js). Fetch the library's Cargo.toml and check for Tailwind-related configuration."

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

When to isolate:
- Second research rounds (higher fidelity re-evaluation)
- Contradiction resolution (agent must check primary sources, not pick a side)
- Any task where independent judgment is the whole point

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

**When the orchestrator SHOULD read:** Completion summaries (3-sentence notifications from the Agent tool). These are free — they're already in your context. Use them for tier-transition decisions, contradiction detection, and progress tracking.

---

## Prompt Anatomy

Every agent prompt has these sections. Skip none.

### 1. Role (1 sentence)
What the agent is and what it's doing. Not a personality — a job description.
> "You are auditing the dependency tree of a Leptos web application."

### 2. Context (2-5 sentences)
The minimum project/domain context needed. Not a tutorial.
> "The project uses Leptos 0.8, Tailwind CSS v4 (standalone binary, no Node.js), and Postgres via sqlx."

### 3. Input Files (explicit paths)
Every file the agent must read, with absolute paths.
> "Read these files: 1. `/path/to/Cargo.toml` 2. `/path/to/guidance/design-system.md`"

### 4. Task (numbered steps)
Precisely what to do, in order. Each step produces or consumes something concrete.
> "1. Read the Cargo.toml. 2. For each dependency, note version and purpose. 3. Check for version conflicts..."

### 5. Output Path (exact file)
Where to write the report. Absolute path.
> "Write your report to `/path/to/research/report.md`"

### 6. Report Format (pasted inline)
The exact template. Agents can't read skill files — paste the format.

### 7. Scope Boundaries
What to do AND what NOT to do. Critical for preventing drift.
> "DO: check every dependency in Cargo.toml. DO NOT: suggest changes, read source code, or assess code quality."

### 8. Tool Expectations
Which tools the agent should use.
> "Use WebFetch for registry APIs, Read for local files, Grep for codebase search."

### 9. Prime Directive (for research agents)
The encourage/discourage framework adapted to the domain. See research-tree skill.

### The Prompt Quality Shortcut

A well-structured prompt for haiku outperforms a vague prompt for sonnet. If you're tempted to upgrade the model, first try improving the prompt. Apply prompt-optimize skill principles if the prompt feels weak.

---

## Execution Patterns

### Parallel Fan-Out (default for most work)

Launch all independent agents in a single message. This is the default — sequential is the exception.

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
**Minimize by:** Asking "does B REALLY need A's output, or just the same inputs?"

### Background Swarm

Launch agents in background, continue your own work, get notified on completion.

```
Launch 10 background agents → do your own work → notifications arrive → process results
```

**When:** You have other work to do while agents run. Research-tree uses this heavily.
**Caution:** Don't launch background agents and then poll/sleep. Trust the notification system.

### Map-Reduce

Many agents produce reports (map), one agent reads all reports (reduce).

```
10 haiku agents write 10 reports → 1 sonnet agent reads all 10 → 1 synthesis report
```

**When:** The goal is a unified answer from diverse investigation. Research-tree's entire structure is map-reduce.

### Speculative Parallel

Not sure which approach will work? Launch agents for each approach simultaneously.

```
Agent A tries approach 1 → Agent B tries approach 2 → Agent C tries approach 3
   → pick the best result, discard the rest
```

**When:** Exploring solution spaces. Debugging (try 3 hypotheses in parallel). Implementation (try 2 architectures, pick the better one).
**Why it works:** The cost of 2 "wasted" haiku agents is negligible. The time saved by not trying approaches sequentially is enormous.

### Chained Refinement

Output of one agent becomes the input of the next, each refining.

```
Haiku agent produces draft → Sonnet agent critiques → Haiku agent revises based on critique
```

**When:** Quality needs to exceed what a single agent call achieves, but the task doesn't justify opus.

---

## Quality Governance

### Detecting Bad Output

You receive completion summaries, not full reports. Scan summaries for:

| Signal | Likely Problem | Action |
|--------|---------------|--------|
| Extraordinary claims (huge numbers, superlatives) | Hallucination | Launch verification agent |
| Two agents contradict each other | At least one is wrong | Launch resolution agent |
| Agent says "I couldn't find" or "not available" | Agent couldn't use tools effectively | Re-launch with clearer tool instructions |
| Report is suspiciously short | Agent gave up early or misunderstood | Re-launch with more specific prompt |
| Agent made recommendations when told not to | Prompt wasn't clear enough | Discard recommendations, use findings only |

### The Re-Launch Principle

**Never debug a failed agent in orchestrator context.** Don't read its full output, don't trace its reasoning, don't figure out where it went wrong. Instead:

1. Note the failure signal from the completion summary
2. Re-launch the task with either:
   - A more specific prompt (if the issue was vague instructions)
   - A better model (if the issue was reasoning capability)
   - Decomposed sub-tasks (if the issue was task complexity)

Debugging an agent burns YOUR context. Re-launching costs nearly nothing.

### Contradiction Resolution

When two agents disagree:
1. Do NOT decide which is right by reading both reports
2. Launch a new agent tasked ONLY with checking primary sources
3. Give it both file paths and the specific contradiction
4. It reports back which claim is supported by evidence

### Spot-Checking

For any research/audit with more than 10 agents, spot-check 1-2 reports by launching a verification agent that re-does a specific agent's task independently. If the spot-check matches, trust the batch. If it doesn't, re-run the suspect agent (or the whole tier) at higher fidelity.

---

## Task Archetypes

How to delegate common work types. Each archetype shows the decomposition pattern, model assignment, and assembly strategy.

### Research / Ecosystem Survey

See the `research-tree` skill for the full tiered workflow. Key delegation points:
- Index parsing: haiku
- Category surveys: haiku (parallel fan-out)
- Project audits: haiku (parallel fan-out)
- Candidate verification: haiku for metadata, sonnet for source-code reasoning
- Synthesis: sonnet or opus (map-reduce)

### Code Implementation

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

### Code Review / Audit

```
Orchestrator: identify files to review
   ↓
Per-file or per-concern: haiku agents audit (security, style, correctness, performance)
   ↓
Sonnet agent synthesizes findings into prioritized review
```

Fan out by CONCERN, not by file. A security audit agent reads all files for security. A style audit agent reads all files for style. This catches cross-file issues that per-file agents miss.

### Debugging

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

### Testing

```
Orchestrator: identify what needs testing
   ↓
Haiku agents: run test suites, report results to files
   ↓
If failures: delegate debugging (see above)
```

Never run long test suites in orchestrator context. Always delegate to background agents that write results to files.

### Documentation / Writing

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

### Exploration / "What's Out There?"

```
Launch 5-15 haiku agents with different search angles (ALL background, ALL parallel)
   ↓
Read completion summaries → identify interesting threads
   ↓
Launch 2-3 sonnet agents to go deeper on promising threads
   ↓
Assemble findings yourself or delegate synthesis
```

This is where the swarm principle shines hardest. 15 speculative haiku agents exploring different angles cost less than you reading one API doc. Most will come back with nothing useful. The few that find something pay for all of them.

---

## Governing Principles (Summary)

1. **Your context is expensive. Agent calls are cheap.** This asymmetry drives every decision.

2. **Decompose aggressively.** 10 micro-agents > 1 macro-agent. The synthesis step (which you or a capable agent does) is where quality emerges.

3. **Haiku is the default.** Every task starts at haiku. Upgrade on observed failure, not preemptively.

4. **Parallel is the default.** Sequential only when there's a true data dependency.

5. **Reports are the medium.** Agents write to disk. Later agents read from disk. The orchestrator routes, never relays.

6. **Isolation preserves judgment.** Agents that form opinions get raw facts, not prior opinions.

7. **Re-launch, don't debug.** Failed agents get a better prompt or a better model. Never investigate an agent's reasoning in orchestrator context.

8. **Speculate freely.** Uncertain which approach works? Launch agents for all of them. The cost of wasted cheap agents rounds to zero.

9. **Tools are force multipliers.** An agent without WebSearch can't search. An agent without Grep can't find code. Assign tools explicitly.

10. **Format is infrastructure.** Standardized report formats enable multi-agent synthesis. Ad-hoc formats make synthesis impossible.
