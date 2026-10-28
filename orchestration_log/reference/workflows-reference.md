# Claude Code Dynamic Workflows Reference

Sources: the official docs at code.claude.com (fetched 2026-10-28; the changelog runs through v2.1.309) and the extracted Claude Code system prompts in Piebald-AI/claude-code-system-prompts at commit `53c252d` (2026-10-27; prompts stamped up to v2.1.304). The docs state the user-facing contract; the prompts state what the model is told. Where the two differ, this file says so and names both.

Scope: Claude Code CLI/IDE. Agent SDK facts appear only where they define the `Workflow` tool's input and output.

Companion: `ultracode-evidence.md` holds the verbatim prompt sections that mention ultracode.

---

## Table of contents

- [§1. What a workflow is](#1-what-a-workflow-is)
- [§2. Availability and enablement](#2-availability-and-enablement)
- [§3. Opt-in rule](#3-opt-in-rule)
- [§4. Ultracode](#4-ultracode)
- [§5. The Workflow tool](#5-the-workflow-tool)
- [§6. Approval and permissions](#6-approval-and-permissions)
- [§7. Script contract](#7-script-contract)
- [§8. Runtime limits](#8-runtime-limits)
- [§9. Workflow subagents](#9-workflow-subagents)
- [§10. Model-facing orchestration guidance](#10-model-facing-orchestration-guidance)
- [§11. Persistence, saving, and distribution](#11-persistence-saving-and-distribution)
- [§12. Run management](#12-run-management)
- [§13. Cost controls](#13-cost-controls)
- [§14. Hooks, telemetry, and observability](#14-hooks-telemetry-and-observability)
- [§15. Version timeline](#15-version-timeline)
- [Appendix A — Footguns](#appendix-a--footguns)
- [Appendix B — Docs and prompts disagree](#appendix-b--docs-and-prompts-disagree)
- [Appendix C — Sources](#appendix-c--sources)

---

## §1. What a workflow is

A dynamic workflow is a JavaScript script that orchestrates many subagents. Claude writes the script; a runtime executes it in the background while the session stays responsive. The `Workflow` tool returns a task ID at once, and a `<task-notification>` arrives when the run completes.

The script, not Claude, holds the plan. Loops, branches, and intermediate results live in script variables; Claude's context receives only the final return value.

| | Subagents | Skills | Agent teams | Workflows |
|---|---|---|---|---|
| What it is | A worker Claude spawns | Instructions Claude follows | A lead agent supervising peer sessions | A script the runtime executes |
| Who decides what runs next | Claude, turn by turn | Claude, following the prompt | The lead agent, turn by turn | The script |
| Where intermediate results live | Claude's context window | Claude's context window | A shared task list | Script variables |
| What's repeatable | The worker definition | The instructions | The team definition | The orchestration itself |
| Scale | A few delegated tasks per turn | Same as subagents | A handful of long-running peers | Dozens to hundreds of agents per run |
| Interruption | Restarts the turn | Restarts the turn | Teammates keep running | Resumable in the same session |

Source: docs `workflows#when-to-use-a-workflow`, verbatim.

The authoring reference gives the model three reasons to reach for a workflow: comprehensiveness (decompose and cover in parallel), confidence (independent perspectives and adversarial checks), and scale beyond one context (migrations, audits, broad sweeps).

Claude Code ships one bundled workflow, `/deep-research <question>`. It fans web searches out across several angles, fetches and cross-checks sources, votes on each claim, and returns a cited report. Claims the verifiers could not check appear as unverified, not refuted. It requires the WebSearch tool and runs only on invocation.

---

## §2. Availability and enablement

Workflows run on all paid plans, on the Anthropic API, and on Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. Pro users turn them on from the **Dynamic workflows** row in `/config`. They work in the CLI, the Desktop app, IDE extensions, `claude -p`, and the Agent SDK (v0.3.149+).

| Control | Scope | Effect |
|---|---|---|
| `enableWorkflows: true\|false` | Any settings file; `/config` **Dynamic workflows** writes it to user settings | Turns workflows on or off for you against your plan's default |
| `disableWorkflows: true` | Any settings file, including managed settings | Turns workflows and bundled workflow commands off for everyone the file reaches |
| `CLAUDE_CODE_DISABLE_WORKFLOWS=1` | Environment, read at startup | Turns workflows off for one session |
| Admin toggle at claude.ai/admin-settings/claude-code | Organization | Same as managed `disableWorkflows` |
| `disableBundledSkills` / `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` | Any settings file / environment | Hides bundled skills, bundled workflows, and built-in slash commands from the model |

Any source that turns workflows off wins; `enableWorkflows: true` cannot override it.

Disabling workflows removes `/workflows`, all workflow commands, and the `/workflow-authoring` skill. The `ultracode` keyword stops triggering, and the **Ultracode** toggle leaves `/effort`. A run already in progress keeps going.

Since v2.1.285, Code Review and `/ultrareview` run even with `disableWorkflows` on, unless the reviewing machine's own administrator set it through MDM or the managed-settings file.

---

## §3. Opt-in rule

The model calls `Workflow` only on explicit opt-in. The tool description lists five qualifying signals, verbatim:

> - The user included the keyword "ultracode" in their prompt (you'll see a system-reminder confirming it).
> - Ultracode is on for the session (a system-reminder confirms it) — see **Ultracode** in the workflow authoring reference.
> - The user directly asked you to run a workflow or use multi-agent orchestration in their own words ("use a workflow", "run a workflow", "fan out agents", "orchestrate this with subagents"). The ask must be in the user's words — a task that would merely benefit from a workflow does not count.
> - The user invoked a skill or slash command whose instructions tell you to call Workflow.
> - The user asked you to run a specific named or saved workflow.

Without one of these, the model must not call the tool, "even one that would clearly benefit from parallelism". It uses the Agent tool instead, or describes what a workflow would do and roughly cost, asks whether to run it, and mentions that "use a workflow" skips the ask next time.

The fourth signal matters to plugin authors: a skill or command whose body tells the model to call `Workflow` counts as opt-in when the user invokes that skill or command.

### The keyword

Typing `ultracode` in a prompt opts that one task in. Claude Code highlights the keyword in the input. To dismiss the highlight, press `Option+W` (macOS) or `Alt+W` (Windows, Linux), or press backspace right after the keyword. `workflowKeywordTriggerEnabled: false` (**Ultracode keyword trigger** in `/config`) disables the trigger outright; the `ultracode` effort setting, `/workflows`, and saved commands keep working.

The keyword counts only in human-typed input: the interactive prompt, an IDE panel, a Remote Control client, or SDK input stamped `origin: { kind: "human" }`. It never triggers from:

- a `-p` prompt
- unstamped SDK input
- a scheduled task prompt
- a webhook payload or relayed pull request comment

The keyword chooses only how Claude structures the work. Every agent tool call still passes the session's permission checks and sandbox.

History: the keyword was `ultrawork`, then `workflow` (prompt v2.1.153), then `ultracode` (changelog v2.1.160). The word "workflow" no longer triggers a run.

---

## §4. Ultracode

Ultracode is a session setting, not an effort level. With it on, Claude plans a workflow for every substantive task without being asked, at whatever effort level the session runs.

### Turning it on

| Route | Persistence | Effort side effect |
|---|---|---|
| `/effort ultracode` or `/effort ultracode on` | Session | None |
| `/effort` slider, `Tab` on **Ultracode**, then `Enter` | Session | None |
| `claude --effort ultracode` | Session | Sets `xhigh` |
| `"ultracode": true` in settings, `--settings`, or an SDK control request | Every session | None |
| SDK `effortLevel: "ultracode"` / `applyFlagSettings()` | Session | Sets `xhigh` |

`/effort ultracode off` turns it off for one session, even when the setting is `true`. The persisted `effortLevel` key and `CLAUDE_CODE_EFFORT_LEVEL` reject `ultracode`. Claude Code reads the `ultracode` key but never writes it.

Ultracode is unavailable when workflows are off or when the model lacks `xhigh` support. In that case `--effort ultracode` starts with ultracode off, at the highest effort the model and any cap allow. An effort cap lowers the level but leaves ultracode on. No managed setting turns ultracode off alone; only disabling workflows does.

Before v2.1.284, ultracode forced `xhigh`, picking another level turned it off, a cap below `xhigh` made it unavailable, and `/effort ultracode off` failed with `Invalid argument`.

### What the model is told

When ultracode is on, a system-reminder says, verbatim:

> Ultracode is on: optimize for the most exhaustive, correct answer — not the fastest or cheapest. Use the Workflow tool on every substantive task; token cost is not a constraint. See the **Ultracode** section and quality patterns in the workflow authoring reference.

The authoring reference's **Ultracode** section, verbatim:

> When a system-reminder confirms ultracode is on, that opt-in is standing: author and run a workflow for every substantive task by default. The goal is the most exhaustive, correct answer you can produce — token cost is not a constraint. For multi-phase work (understand → design → implement → review), that often means several workflows in sequence — one per phase — so you stay in the loop between them. The quality patterns below (adversarial verify, multi-modal sweep, completeness critic, loop-until-dry) are the tools; pick what fits the task. Lean toward orchestrating with workflows and adversarially verifying your findings — unless the work is trivial or already verified. Solo only on conversational turns or trivial mechanical edits. When a reminder says ultracode is off, revert to the opt-in rule in the Workflow tool description.

Since v2.1.299, the reminder also reaches scheduled tasks and other delivered headless turns when the setting is on.

### Checks ultracode suspends

- The `Large workflow` warning (§13).
- The session's concurrent subagent limit for Agent-tool spawns (default 20, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- In auto mode, the first-launch approval prompt.

Every request costs more tokens and time under ultracode; on subscriptions it reaches session and weekly limits sooner.

---

## §5. The Workflow tool

`Workflow` is a built-in tool that requires permission. Subagents never receive it: Claude Code strips `Workflow` from every subagent's tool pool, even when the `tools` field lists it. Only the main conversation launches workflows; a script nests at most one level through `workflow()` (§7).

### Input

| Field | Type | Meaning |
|---|---|---|
| `script` | string | Inline script; must open with a literal `export const meta` |
| `name` | string | A bundled or saved workflow; resolved to a script |
| `scriptPath` | string | Script file on disk; wins over `script` and `name`. Rejected when the session lacks `Read` |
| `args` | any JSON | Exposed to the script as the global `args`. Pass real arrays and objects, never a JSON-encoded string |
| `resumeFromRunId` | string | Prior run to resume, same session only |
| `title`, `description` | string | Ignored; `meta` sets both |

At least one of `script`, `name`, or `scriptPath` is required. The tool description forbids writing a fresh script to a file first and forbids setting `name` alongside `script`, because `name` selects a saved workflow.

### Output

| Field | Meaning |
|---|---|
| `status` | `"async_launched"` (in-process) or `"remote_launched"` (dispatched to a cloud session) |
| `taskId` | Background task ID |
| `taskType` | `"local_workflow"` or `"remote_agent"` |
| `workflowName` | `meta.name` |
| `runId` | Resume handle; absent for remote runs, where `sessionUrl` serves instead |
| `summary` | One-line description |
| `transcriptDir` | Where subagent transcripts and `journal.jsonl` land |
| `scriptPath` | The persisted script for this run |
| `sessionUrl` | Cloud session URL for remote runs |
| `warning` | Non-blocking notice, such as local git state diverging from the pushed branch |
| `error` | Syntax-check failure; the run never started despite the launched status |

Check `error` before treating a run as started.

---

## §6. Approval and permissions

The CLI approval prompt shows the planned phases and offers **Yes, run it**, **Yes, and don't ask again for `<name>` in `<path>`** (named bundled, saved, or plugin workflows only, never an ad hoc script), **View raw script**, and **No**. `Ctrl+G` opens the script in an editor; `Tab` adds a comment to the answer.

| Permission mode | Prompt |
|---|---|
| Auto | First launch only; any **Yes** records consent in user settings. Skipped entirely under ultracode |
| Manual, accept edits | Every run, unless **don't ask again** applies |
| Bypass permissions | Never |
| `claude -p`, Agent SDK | Never; the call goes through normal permission evaluation |

Headless runs need one of: an allow rule (`Workflow` for all, `Workflow(<name>)` for one saved workflow), auto mode, bypass mode, a `PreToolUse` hook returning `"allow"`, or a host approver (`--permission-prompt-tool`, SDK `canUseTool`). In plan mode a hook's approval alone does not start the run.

The Desktop app shows an approval card with the name, phases, and a token caution, offering **Once**, **Always**, and **Deny**.

Workflow agents use the session's permission rules; their permission mode follows the subagent rules. Allow the tools the agents need before a long run, or the run pauses on each prompt.

Claude can launch only from a script file the session may read. Add outside directories with `/add-dir` or a Read allow rule first.

---

## §7. Script contract

### `meta`

```javascript
export const meta = {
  name: 'find-flaky-tests',
  description: 'Find flaky tests and propose fixes',   // one line; shown in the permission dialog
  whenToUse: '...',                                    // optional; shown in the workflow list
  phases: [                                            // optional; one per phase() call
    { title: 'Scan', detail: 'grep test logs for retries' },
    { title: 'Fix', detail: 'one agent per flaky test' },
  ],
}
```

`meta` must be the first statement and a pure literal: no variables, calls, spreads, or template interpolation. A non-literal `meta` drops `/<name>` from autocomplete. Phase titles must match `phase()` calls exactly; an unmatched `phase()` gets its own progress group. A phase entry may carry `model` when the host does not force the subagent model.

### Body globals

| Global | Signature and behavior |
|---|---|
| `agent` | `agent(prompt, {label?, phase?, schema?, model?, effort?, isolation?, agentType?, stallMs?})` → `Promise<any>`. Spawns one subagent. Without `schema`, resolves to its final text; with `schema`, to the validated object. Resolves to `null` when the user skips it or it dies on a terminal API error after retries |
| `pipeline` | `pipeline(items, stage1, stage2, ...)` → `Promise<any[]>`. Runs each item through all stages with no barrier between stages. Each stage receives `(prevResult, originalItem, index)`. A throwing stage drops that item to `null` and skips its later stages |
| `parallel` | `parallel(thunks)` → `Promise<any[]>`. Barrier: awaits every thunk. A throwing thunk resolves to `null`; the call never rejects |
| `phase` | `phase(title)`. Groups subsequent agents under a title in the progress view |
| `log` | `log(message)`. Prints a narrator line above the progress tree |
| `args` | The tool's `args` input, verbatim; `undefined` when omitted |
| `budget` | `{total, spent(), remaining()}`. `total` is the turn's `+500k`-style token target or `null`. `spent()` counts output tokens across the main loop and all workflows. Once `spent()` reaches `total`, further `agent()` calls throw |
| `workflow` | `workflow(nameOrRef, args?)`. Runs a saved workflow or `{scriptPath}` inline as a sub-step and returns its result. The child shares the parent's concurrency cap, agent counter, abort signal, and budget. A `workflow()` call inside a child throws |

### `agent()` options

| Option | Meaning |
|---|---|
| `label` | Display label |
| `phase` | Explicit progress group; use it inside `pipeline()`/`parallel()` stages to avoid races on the global `phase()` state |
| `schema` | JSON Schema; forces a StructuredOutput call. Root must be `{type: 'object', properties: {...}}` with `required ⊆ properties`. Claude Code rejects a provably contradictory schema before the agent starts. Validation retries cap at 5 (`MAX_STRUCTURED_OUTPUT_RETRIES`) |
| `model` | Per-agent model override. The prompt tells the model to omit it unless highly confident; hidden when `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is set |
| `effort` | `'low'`…`'max'`; omit to inherit. The prompt advises `'low'` for mechanical stages and high tiers only for the hardest verify or judge stages |
| `isolation` | `'worktree'` runs the agent in a fresh git worktree, removed if unchanged. The prompt calls it expensive (~200–500 ms setup plus disk per agent) and reserves it for agents that mutate files in parallel |
| `agentType` | A registered subagent type, such as `'general-purpose'`, resolved from the Agent tool's registry. Composes with `schema` |
| `stallMs` | Per-agent stall window in milliseconds (docs only; absent from the prompt) |

### Forbidden in scripts

- TypeScript syntax: annotations, interfaces, generics fail to parse.
- `Date.now()`, `Math.random()`, and argless `new Date()` throw, because they would break resume. Pass timestamps through `args`; vary prompts by index for diversity. Mentions inside strings or comments are allowed (v2.1.172).
- `import()` fails before the run starts (sandbox escape fixed in v2.1.223).
- Filesystem, shell, and Node.js APIs. Agents do that work; the script coordinates.
- Return values nested deeper than 28,000 levels (v2.1.299; 100,000 before).

The body runs in an async context with top-level `await` and standard JS built-ins.

---

## §8. Runtime limits

| Limit | Value |
|---|---|
| Concurrent agents per run | 16 by default, fewer with fewer CPUs (container limits respected); `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` sets 1–256 (v2.1.269+). Excess calls queue |
| Items per `parallel()` or `pipeline()` call | 4,096; a longer list errors |
| Agents per run | 1,000 |
| Same-prefix stagger | Up to 5,000 ms (`CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`; `0` disables) |
| Structured-output attempts | 5 (`MAX_STRUCTURED_OUTPUT_RETRIES`) |
| Restarts after stalls | 5 per agent (6 attempts) |
| Usage-limit waits | 2 per run |
| Mid-run user input | None; a run pauses only for agent permission prompts and usage-limit waits |

---

## §9. Workflow subagents

### Definition

The default workflow agent type is `workflow-subagent`: tools `*`, with `SendUserMessage`, `Agent`, and `Workflow` disallowed. A script can substitute any registered type through `agentType`.

### Return contract

Plain-text agents receive, verbatim:

> CRITICAL: Your final text response is returned **verbatim** as a string to the calling script — it is your return value, not a message to a human.
> - Output the literal result (data, JSON, text). Do NOT output confirmations like "Done." or "Sent."
> - If asked for JSON, return ONLY the raw JSON — no code fences, no prose, no markdown.
> - Do NOT use SendUserMessage to deliver your answer. Put your answer in your final text response.
> - Be concise. The script will parse your output.

Schema agents receive, verbatim:

> CRITICAL: You MUST call the ${STRUCTURED_OUTPUT_TOOL_NAME} tool exactly once to return your final answer. The tool's input schema defines the required shape.
> - Do your work (Read files, run commands, etc.), then call ${STRUCTURED_OUTPUT_TOOL_NAME} with your answer.
> - Do NOT put your answer in a text response. The script reads ONLY the ${STRUCTURED_OUTPUT_TOOL_NAME} tool call.
> - If the schema validation fails, read the error and call ${STRUCTURED_OUTPUT_TOOL_NAME} again with a corrected shape.
> - After calling ${STRUCTURED_OUTPUT_TOOL_NAME} successfully, end your turn. No acknowledgment needed.

A custom `agentType` keeps its own system prompt and gets a shorter "return note" appended with the same contract.

### Task authority

Every variant ends with `${WORKFLOW_TASK_AUTHORITY_NOTE}`. Claude Code marks script-computed prompts as text the script computed, not user words, so the auto-mode classifier never reads them as user requests. On Bedrock, Vertex, and Foundry the framing reaches the subagent itself. The security monitor treats workflow scripts like delegation payloads. Since v2.1.301 the note adds that script text still assigns the step: the agent performs that step instead of skipping it.

### Inherited context

- CLAUDE.md files load into every workflow agent, except built-in types that omit them, such as Explore and Plan. The prompt tells the model not to paste CLAUDE.md rules into agent prompts and to name only the rule a stage needs.
- Session MCP tools reach agents through ToolSearch. Interactively authenticated servers may be absent in headless or cron runs.
- A forked skill invoked by a workflow agent returns its result to that agent (v2.1.295+).

### Isolation

An agent spawned with `isolation: 'worktree'` receives a reminder that it runs in a separate working copy at a named path, that its changes do not touch the main directory or other agents, and that the worktree is removed if unchanged or kept for review if changed. A `WorktreeCreate` hook's worktree survives the agent; Claude Code skips `WorktreeRemove` for it.

### Model selection

Workflow agents follow the subagent model order. A model the script passes counts as the per-invocation model. Otherwise the agent inherits the session model.

| Control | Effect |
|---|---|
| `CLAUDE_CODE_SUBAGENT_MODEL` | Default model for subagents, teammates, and workflow agents without another assignment |
| `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` | Forces that model onto all of them; also hides `model` guidance from the authoring prompt |
| `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` | One model for every workflow agent, leaving other subagents alone (changelog v2.1.296; absent from the env-vars page) |
| `availableModels` allowlist | Substitutes a blocked model, with a warning |

---

## §10. Model-facing orchestration guidance

This section condenses the bundled `/workflow-authoring` skill, which Claude loads before writing a script.

### Shape of the work

- **Hybrid:** scout inline first (list files, scope the diff) to find the work list, then call `Workflow` to pipeline over it.
- **Chain single-phase workflows across turns** and read each result before choosing the next: Understand (parallel readers → map), Design (judge panel → scored synthesis), Review (dimensions → find → adversarially verify), Research (multi-modal sweep → deep read → synthesize), Migrate (discover → transform in worktrees → verify).
- **No mid-run sign-off exists**; a stage that needs approval becomes its own workflow.

### Pipeline by default

`pipeline()` is the default for multi-stage work: wall-clock equals the slowest single-item chain. A barrier (`parallel()` between stages) is correct only when stage N needs cross-item context from all of stage N-1:

- dedup or merge across the full result set before expensive work
- early exit on a zero total
- a prompt that compares against "the other findings"

Flatten, map, or filter steps do not justify a barrier; they belong inside a pipeline stage.

### Quality patterns

| Pattern | Mechanism |
|---|---|
| Adversarial verify | N independent skeptics per finding, each prompted to refute and to default to refuted when uncertain; kill on a refuting majority |
| Perspective-diverse verify | One verifier per lens (correctness, security, perf, reproduces) instead of N identical refuters |
| Judge panel | N attempts from different angles, scored by parallel judges; synthesize from the winner and graft the runners-up's best ideas |
| Loop-until-dry | Spawn finders until K consecutive rounds return nothing new; dedup against everything seen, not only the confirmed set, or the loop never converges |
| Multi-modal sweep | Parallel searches by container, content, entity, and time |
| Completeness critic | A final agent asks what is missing; its answer becomes the next round |
| No silent caps | `log()` whatever a bound (top-N, sampling, no-retry) dropped |
| Loop-until-count / loop-until-budget | Accumulate to a target, or spend to `budget.remaining()`; guard on `budget.total`, because `remaining()` is `Infinity` without a target |

Scale follows the request: "find any bugs" gets a few finders and single-vote verify; "thoroughly audit" gets a larger pool, a 3–5 vote adversarial pass, and a synthesis stage. The skill invites novel harnesses such as tournament brackets, self-repair loops, and staged escalation.

### Size guideline

Claude Code sends a size guideline to the model as advice, not a cap; a prompt that asks for another scale overrides it.

| `workflowSizeGuideline` | Target |
|---|---|
| `unrestricted` | Sized to the task |
| `small` | Fewer than 5 agents |
| `medium` | Fewer than 10 agents (default) |
| `large` | Fewer than 50 agents |

Pro plans default to `small` on v2.1.271+. Set it with `/config workflowSizeGuideline=small` or in any settings file, which hides the `/config` row.

---

## §11. Persistence, saving, and distribution

### Per-run script

Unless launched from `scriptPath`, each run's script lands under the session directory in `~/.claude/projects/`, and the tool result returns the path. To iterate, edit that file and relaunch with `{scriptPath}` instead of resending the script.

### Saved workflows

`s` in `/workflows` saves a run's script as a command:

| Location | Reach |
|---|---|
| `.claude/workflows/` | The project, shared through the repo |
| `~/.claude/workflows/` (or `$CLAUDE_CONFIG_DIR/workflows/`) | Every project, personal |

A saved workflow runs as `/<name>` and appears in `/` autocomplete. A project workflow beats a personal one of the same name. In a monorepo, saving targets the nearest existing `.claude/workflows/` between the working directory and the repo root, loading reads every one along that path, and the nearest wins on a name collision. Claude Code refuses to write through symlinks: in the project location any of `.claude`, `.claude/workflows`, or the target; in the personal location only the target. After a hand edit, run `/reload-skills`, then `/<name>`. Run `/workflow-authoring` before editing a saved script by hand.

Names in the `anthropic-skills` and `claude-ai` namespaces do not load; a reserved name produces a startup notice.

### Plugin workflows

A plugin ships workflows in a root `workflows/` directory, or points the manifest's `workflows` field (path or array) at other `.js` files or directories, which replaces the default scan. Plugin workflows are namespaced: `meta.name: 'release-audit'` in plugin `acme-tools` runs as `/acme-tools:release-audit`. Users can approve one with `Workflow(<name>)` or **don't ask again**.

### Parameters

A saved workflow reads input from the `args` global. Claude passes structured data, so `Run /triage-issues on issues 1024, 1025, and 1030` reaches the script as an array.

---

## §12. Run management

### `/workflows`

`/workflows` lists running and completed runs and opens directly when only one exists. The task panel below the input also shows a one-line progress row.

| Key | Action |
|---|---|
| `↑` / `↓` | Select a phase or agent |
| `Enter` / `→` | Drill in; in agent detail, expand or collapse |
| `Esc` / `←` | Back out one level |
| `j` / `k` | Scroll agent detail |
| `f` | Cycle the agent status filter |
| `p` | Pause or resume the run |
| `x` | Stop the selected agent, or the whole run when focus is on it |
| `r` | Restart the selected running agent |
| `s` | Save the script as a command |

Agent detail shows the prompt, recent tool calls with state, the result, and the agent's own task list.

### Resume

`p` resumes a paused run. A stopped run resumes only when Claude relaunches it with `Workflow({scriptPath, resumeFromRunId})`. Claude Code refuses the relaunch until the stopped run's agents exit.

Replay walks agents in start order:

- **Completed** returns its cached result, until the first agent whose prompt differs from the previous run. That agent and every later one run live.
- **Running when stopped** starts over. Stopping the whole run marks no agent failed.
- **Failed**, including one stopped alone with `x`, runs again, and so does every agent started after it.

If A, B, C, D start in order and B fails, the relaunch caches A and reruns B, C, and D. Reordering also counts: a script edited to start A, C, B, D caches A and reruns the rest. Before v2.1.305, completed `pipeline()` and `parallel()` agents could rerun even on an unedited script.

The prompt tells the model to read `<transcriptDir>/journal.jsonl` before diagnosing an empty or unexpected result; it records each agent's actual return value.

### Leaving the session

A run does not continue on its own after the session backgrounds or exits; it continues only on a relaunching `Workflow` call. After `Exit and stop tasks`, resume with `claude --resume` and ask Claude to relaunch. A fresh session has no run to relaunch. A missing journal fails with `nothing to resume`; start over as a new run. Cloud sessions save run results with conversation history, which survives VM reclamation.

### Usage limits

On v2.1.271+, an agent that hits a claude.ai usage limit waits for the reset, and no new agents start; the run then continues on its own. The pause happens only when the session is interactive and signed in with a subscription, `autoContinueAtUsageLimit` is on, the reset falls within 24 hours, and the run has waited fewer than twice. Headless, SDK, background, Remote Control, and teammate sessions fail the agent instead.

### Stalls

An agent silent past the stall window restarts from its prompt, with a `(retry 1)` suffix. The new attempt starts without the old transcript; files the old attempt changed stay changed. After the sixth failed attempt, `agent()` fails with `agent stalled on all 6 attempts`, `agent lost its reply on all 6 attempts`, or `agent abandoned after 6 attempts`. Lengthen the window per agent with `stallMs` or for all with `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` (default 600,000). Inside `parallel()` or `pipeline()` the failure becomes `null`; a directly awaited failure ends the run.

---

## §13. Cost controls

- A run counts toward plan usage and rate limits. `/workflows` shows per-agent tokens live.
- A run that schedules more than 25 agents, or projects past 1.5 million tokens, shows an advisory `Large workflow` warning in the task panel. A user-chosen size guideline replaces the 25-agent threshold; ultracode suppresses the warning.
- The runtime caps (§8) bound a runaway script.
- Prompt caching: agents with the same model, effort, type, tools, schema, and working directory share a cache prefix, and the stagger lets later siblings read it. Workflow agents sit outside the main conversation's TTL bucket: 5 minutes by default, 1 hour with `subagentPromptCacheTtl: "1h"`.
- `/usage` warns about workflow spend (v2.1.299).

---

## §14. Hooks, telemetry, and observability

| Surface | Workflow behavior |
|---|---|
| `PreToolUse` | Matches `Workflow` like any built-in tool; `"allow"` approves headless launches, except in plan mode |
| `Stop` | `background_tasks[]` carries entries with `type: "workflow"` and `name` set to the workflow name, which separates "done" from "waiting on a run" |
| `WorktreeCreate` / `WorktreeRemove` | A worktree made for a workflow agent survives; `WorktreeRemove` does not fire |
| OpenTelemetry | Workflow agents emit `workflow.run_id` and `workflow.name` |
| `agent.spawn` mod hook | Receives workflow agents with run and index; can refuse them (v2.1.292+) or rewrite `prompt` and `model` (v2.1.300+) |
| `CLAUDE_CODE_BG_TASKS_REPORT_RUNNING` | A live run keeps a non-interactive session reporting "running" past turn end |
| Terminal progress indicator | Stays on while a run is live |

---

## §15. Version timeline

| Version | Change |
|---|---|
| 2.1.146 (prompts) | Workflow tool description and both subagent return prompts appear in the extracted prompts |
| 2.1.153 (prompts) | Opt-in keyword renamed `ultrawork` → `workflow` |
| 2.1.154 | Dynamic workflows announced; `/workflows`; prompts add ultracode as standing opt-in and require inline scripts |
| 2.1.157 | Keyword trigger setting in `/config` |
| 2.1.160 | Trigger keyword renamed `workflow` → `ultracode` |
| 2.1.163 (prompts) | 4,096-item cap per call |
| 2.1.178 (prompts) | `effort` option on `agent()` |
| 2.1.202 | **Dynamic workflow size** in `/config` |
| 2.1.203 | `--effort ultracode` accepted |
| 2.1.210 | Keyword stops firing on non-human input |
| 2.1.219 | `workflowSizeGuideline` key; default `medium` (then fewer than 15 agents) |
| 2.1.223 | Dynamic `import()` sandbox escape closed |
| 2.1.229 | Container CPU limits honored; same-prefix stagger |
| 2.1.248 | Tool description cut from ~5.7k to ~1k tokens; the reference moves into the bundled `/workflow-authoring` skill |
| 2.1.257 | `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` hides model guidance |
| 2.1.260 | Unsatisfiable schemas rejected up front |
| 2.1.269 | `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` |
| 2.1.271 | Usage-limit pause; Pro defaults to `small`; `medium` lowered from 15 to 10 agents |
| 2.1.284 | Ultracode becomes its own toggle, independent of effort level |
| 2.1.285 | Code Review and `/ultrareview` survive `disableWorkflows` |
| 2.1.292 | `agent.spawn` mod hook sees workflow agents |
| 2.1.295 | Forked skills return results to the invoking workflow agent |
| 2.1.296 | `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` |
| 2.1.299 | Ultracode reminder reaches headless turns; nesting cap 28,000 |
| 2.1.300 | `agent.spawn` can rewrite workflow agents' prompt and model |
| 2.1.301 | Task-authority note: computed task text still assigns the step; a "lean rewrite" variant of the tool description appears |
| 2.1.305 | Resume serves completed `pipeline()`/`parallel()` agents from the journal |

---

## Appendix A — Footguns

1. **The tool refuses inferred opt-in.** A skill that merely benefits from parallelism never gets a workflow; the skill body must tell the model to call `Workflow`, or the user must ask.
2. **Subagents cannot launch workflows.** A plugin agent that plans to call `Workflow` fails; only the main conversation can.
3. **`agent()` resolves to `null`** on skip, terminal API error, or exhausted stall restarts inside `parallel()`/`pipeline()`. Filter with `.filter(Boolean)` before use.
4. **A failed agent reruns everything after it** on resume, including completed work.
5. **`Date.now()` and `Math.random()` throw.** Pass timestamps through `args`.
6. **Stringified `args`** reach the script as one string; `args.map` then throws.
7. **A non-literal `meta`** silently drops the saved command from autocomplete.
8. **Unguarded `budget.remaining()`** returns `Infinity` without a target, and a budget loop runs to the 1,000-agent cap.
9. **Loop-until-dry deduped against confirmed findings** never converges; dedup against everything seen.
10. **Headless launches need an explicit allow** (rule, mode, hook, or host); otherwise permission evaluation blocks them.
11. **A `-p` or scheduled prompt containing `ultracode`** does not opt in.
12. **The `error` field** can accompany `status: "async_launched"`; the run never started.
13. **Workflow-agent worktrees from a `WorktreeCreate` hook leak**; remove them yourself.
14. **Interactively authenticated MCP servers** may be missing from agents in headless or cron runs.

---

## Appendix B — Docs and prompts disagree

| Topic | Docs | Prompt |
|---|---|---|
| Concurrency | 16 by default, fewer with fewer CPUs; env var sets 1–256 | `min(16, available CPUs - 2)`; "only ~10 run at any moment" |
| `stallMs` option | Documented on `agent()` | Absent from the signature |
| Keyword phrasing | Highlight in input; `workflowKeywordTriggerEnabled` | "you'll see a system-reminder confirming it" (v2.1.248) vs "a message from the system confirms it" (lean rewrite, v2.1.301) |
| `whenToUse` in `meta` | Not mentioned | Optional field, shown in the workflow list |
| Nested `workflow()` | Not mentioned | Documented, one level deep |
| `budget` global | Not mentioned | Documented, a hard ceiling |

The extracted prompts carry two tool descriptions: `Tool Description: Workflow` (v2.1.248) and `Tool Description: Workflow (lean rewrite)` (v2.1.301). They differ in one clause. The repository does not say which one ships when.

---

## Appendix C — Sources

Official docs, fetched 2026-10-28:

- https://code.claude.com/docs/en/workflows.md
- https://code.claude.com/docs/en/agents.md
- https://code.claude.com/docs/en/settings-reference.md (`ultracode`, `enableWorkflows`, `disableWorkflows`, `workflowKeywordTriggerEnabled`, `workflowSizeGuideline`, `subagentPromptCacheTtl`)
- https://code.claude.com/docs/en/env-vars.md
- https://code.claude.com/docs/en/model-config.md (ultracode routes and availability)
- https://code.claude.com/docs/en/agent-sdk/typescript.md (`WorkflowInput`, `WorkflowOutput`)
- https://code.claude.com/docs/en/sub-agents.md (tool filter, concurrency exemption, model order)
- https://code.claude.com/docs/en/hooks.md (`PreToolUse`, `Stop.background_tasks`, worktree hooks)
- https://code.claude.com/docs/en/plugins/manifest-reference.md (`workflows` field)
- https://code.claude.com/docs/en/commands.md, https://code.claude.com/docs/en/skills.md, https://code.claude.com/docs/en/tools-reference.md
- https://code.claude.com/docs/en/changelog.md

Extracted prompts, Piebald-AI/claude-code-system-prompts @ `53c252d`, under `system-prompts/`:

- `tool-description-workflow.md` (v2.1.248)
- `tool-description-workflow-lean-rewrite.md` (v2.1.301)
- `skill-workflow-authoring-reference.md` (v2.1.265)
- `system-reminder-ultracode-enabled.md`
- `system-reminder-workflow-isolated-worktree.md` (v2.1.242)
- `agent-prompt-workflow-subagent-plain-text-output.md`, `agent-prompt-workflow-subagent-structured-output.md` (v2.1.301)
- `agent-prompt-workflow-script-plain-text-return-note.md`, `agent-prompt-workflow-script-structured-return-note.md` (v2.1.301)
- `CHANGELOG.md` (prompt version history)
