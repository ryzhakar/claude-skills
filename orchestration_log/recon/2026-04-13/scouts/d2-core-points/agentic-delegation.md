# Core Points: agentic-delegation

## Iteration 1

**Point:** Orchestrator context is the most expensive resource in the system while agent calls (especially to cheap models) are nearly free, creating a cost inversion where the default question should be "why would I do this myself" rather than "is this worth delegating."

**Evidence:**
- SKILL.md lines 18-38: "Your context window is finite and irreplaceable mid-conversation. Every line you read, every file you grep, every URL you fetch — it stays in your context forever... A haiku agent costs effectively nothing. It gets its own fresh context... Your context cost: those 3 sentences."
- SKILL.md lines 31-38: The decision calculus table contrasting "Traditional thinking" vs "Correct thinking" — explicitly inverting delegation logic from "Is this worth delegating?" to "Is this worth spending MY context on?"
- SKILL.md lines 68-80: "There is exactly ZERO reasons to do something in orchestrator context" with detailed rationalization table showing every impulse to work directly is a mistake.

## Iteration 2

**Point:** Swarms of cheap parallel agents almost always beat single capable agents, both in cost (20 haiku < 1 sonnet) and wall time (parallel = time of slowest, sequential = sum of all), making aggressive decomposition and mass parallel dispatch the default pattern.

**Evidence:**
- SKILL.md lines 40-49: "20 haiku agents running in parallel cost less and finish faster than 1 sonnet agent doing the same work sequentially... 20 parallel agents = the time of the slowest one (~60-120s). 1 sequential agent doing 20 things = 20x that."
- SKILL.md lines 48-49: "Launch swarms. Not individuals. When you have 8 things to check, don't check them — launch 8 agents. When you have 15 files to audit, launch 15 agents."
- SKILL.md lines 290-300: Parallel Fan-Out described as "default for most work" with sequential explicitly marked as "the exception."

## Iteration 3

**Point:** Every task must start at the cheapest capable tier (haiku for gathering/extraction, sonnet for reasoning/judgment, opus for strategic synthesis), upgrading only on observed failure rather than preemptively, because a well-structured haiku prompt outperforms a vague sonnet prompt.

**Evidence:**
- SKILL.md lines 84-86: "Three tiers. The cheapest model that can reliably do the task is the correct choice. Upgrade on observed failure, not preemptively."
- SKILL.md lines 152-164: The upgrade path flowchart: "Start every task at haiku level... Agent output seems unreliable?... Re-launch with sonnet. Do NOT debug the haiku output... Never pre-assign sonnet 'just in case.'"
- prompt-anatomy.md lines 144-146: "A well-structured prompt for haiku outperforms a vague prompt for sonnet. If you're tempted to upgrade the model, first try improving the prompt."

## Iteration 4

**Point:** Agents communicate exclusively through files on disk with the orchestrator routing file paths (never relaying content), and failed agents are re-launched with better prompts or higher tiers rather than debugged in orchestrator context, preserving orchestrator context window for decision-making only.

**Evidence:**
- SKILL.md lines 261-276: "Agents communicate through files on disk. The orchestrator points agents to files — never relays content... The relay anti-pattern: Agent A writes report → Orchestrator reads report → Orchestrator summarizes in Agent B's prompt... The correct pattern: Agent A writes report to {path} → Orchestrator tells Agent B: 'Read {path}'"
- quality-governance.md lines 18-27: "Never debug a failed agent in orchestrator context. Don't read its full output, don't trace its reasoning... Re-launch the task with either: A more specific prompt, A better model, Decomposed sub-tasks."
- quality-governance.md lines 29-36: Table contrasting debugging (consumes orchestrator context, takes time to trace) vs re-launching (zero context cost, addresses root cause directly).

## Iteration 5

**Point:** Every agent prompt must contain exactly nine components (role, minimal context, explicit input paths, numbered task steps, absolute output path, pasted format, scope boundaries with DO/DO NOT lists, tool expectations, and prime directive for research), because precise structure compensates for model limitations and prevents drift.

**Evidence:**
- SKILL.md lines 281-283: "Every agent prompt requires: (1) Role statement, (2) Minimal context, (3) Explicit input file paths, (4) Numbered task steps, (5) Absolute output path, (6) Pasted report format, (7) Scope boundaries (DO and DO NOT lists), (8) Tool expectations, (9) Prime directive for research agents."
- prompt-anatomy.md lines 1-3: "Every agent prompt has these sections. Skip none."
- prompt-anatomy.md lines 112-113: "Haiku follows instructions literally. Give it exact file paths, exact commands, exact report formats. The more precise the prompt, the better haiku performs. A great haiku prompt compensates for most of haiku's reasoning limitations."

## Rank Summary

1. **Context cost inversion** — The foundational economic thesis that drives all other decisions: orchestrator context is finite/expensive, agent calls are nearly free, therefore delegation is always the default.

2. **Swarm superiority** — The tactical implication: parallel mass dispatch of cheap agents beats sequential work by capable agents in both cost and time, making aggressive decomposition mandatory.

3. **Tier discipline** — The model selection protocol: always start cheap, upgrade only on observed failure, because prompt quality matters more than model capability for most tasks.

4. **File-based communication + re-launch principle** — The operational patterns that preserve orchestrator context: agents read/write files directly, orchestrator routes paths, failed agents are replaced not debugged.

5. **Nine-component prompt structure** — The technical foundation that makes cheap models reliable: precise structure compensates for reasoning limitations and prevents drift across agent swarms.
