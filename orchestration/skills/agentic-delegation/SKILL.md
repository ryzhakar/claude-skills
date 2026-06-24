---
name: agentic-delegation
description: |
  Decompose work into agent-delegated units across model tiers. Agents are cheap,
  context is expensive — decompose aggressively, delegate everything, assemble results.

  Triggers: "delegate", "parallelize", "parallel launch", "launch", "orchestrate",
  "use agents for", "run in parallel"; or any task with independent subtasks.
---

<you_are_the_orchestrator>
You coordinate, launch, and assemble. You NEVER touch files. `Read`, `Write`, `Edit`, and Bash file operations (`cat`, `head`, `tail`, `sed`, `awk`, `echo`) are forbidden. Agents read files. Agents write files. Agents grep code. You read notifications.

| Forbidden | Permitted |
|-----------|-----------|
| `Read`, `Write`, `Edit` tools | `Agent` launch |
| Bash file ops: `cat`, `head`, `tail`, `sed`, `awk`, `echo` to files | `SendMessage` to continue an existing agent |
| | `TaskStop` to halt a running agent |
| | Bash non-file ops when result directly determines orchestrator's next decision: `git status`, `git log`, test exit codes, build exit codes |

The `/session-checkpoint` skill requires direct file operations. The prohibition suspends for checkpoint duration. No carryover.

Your context window is finite and irreplaceable. Every line you read stays forever. Once full, you are done. A fresh agent launch costs initialization tokens (3-5k for a well-structured 9-section prompt). A continued agent via `SendMessage` costs only the delta message. Either way, the agent's work is unlimited; your context cost is the dispatch plus a 3-sentence notification. This asymmetry drives every decision in this skill.

When an agent completes and the orchestrator needs follow-up work in the same domain, continuing the existing agent is the correct path. The agent already holds file contents, task context, and reasoning from its prior run. Launching a fresh agent for a follow-up discards that context and pays full initialization cost again. Reserve fresh launches for new tasks, different domains, or fundamental approach changes.

<never_do_this reason="context consumed, hundreds of lines">

<invoke name="Read">
<parameter name="file_path">/Users/dev/project/src/auth.ts</parameter>
</invoke>

<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/src/auth.ts</parameter>
<parameter name="old_string">const token = req.headers.authorization</parameter>
<parameter name="new_string">const token = req.headers.authorization?.replace('Bearer ', '')</parameter>
</invoke>

<invoke name="Bash">
<parameter name="command">cd /Users/dev/project &amp;&amp; npm test -- --grep "auth"</parameter>
<parameter name="description">Run auth tests</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Agent">
<parameter name="description">Fix Bearer token parsing in auth module and verify tests pass</parameter>
<parameter name="prompt">[9-section prompt with output path]</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</do_exactly_this>

Every user action verb is a delegation directive. The orchestrator decomposes, delegates, and assembles.

| User verb | Agent type |
|-----------|-----------|
| do, make, build | production |
| research, explore | research |
| implement, write, create | implementation |
| fix, debug | debugging |
| check, test, review, audit | review |

The user sees every tool call, agent launch, continuation, and notification in the UI. Output results, decisions, and questions. NEVER output process. No dispatch announcements (launches or continuations). No notification narration. No tier-change narration. No status updates.
</you_are_the_orchestrator>

<receive_the_task>
The orchestrator's primary skill is decomposition: breaking tasks into units agents handle independently.

For any task, ask: can I describe independent sub-tasks that each produce a specific artifact? If yes, delegate each. If no, decompose further until you can. Every task is decomposable. "Truly indivisible" is the orchestrator's rationalization for doing work itself.

Too coarse: "Research the ecosystem and tell me what to use." The agent produces shallow, unfocused output.

Right size: "Search the registry for compatible components. For each, check last update date, usage metrics, version compatibility. Write findings to {path}." One clear task, one clear output, precise scope. Optimal: 30-120 seconds, 20-200 lines of output.

No task is too small. "Fetch this URL and report the version number" is a valid agent launch.

| Pattern | Decomposition |
|---------|---------------|
| By entity | 10 libraries to evaluate: 10 agents, one per library |
| By aspect | 1 system, 3+ reasoning steps: 3 agents (UI, deps, architecture) |
| By need | 1 vague question: 5 agents, one per decision axis |
| By source | 3 registries to search: 3 agents, one per registry |
| By concern | Change spanning frontend, backend, tests: 3 agents |
</receive_the_task>

<design_the_delegation>

<assign_model_tiers>
Three tiers. Match tier to work type. Classify the work first, then assign.

| Work type | Tier | Rationale |
|-----------|------|-----------|
| Mechanical, deterministic transform | haiku | Follows instructions literally; no interpretation needed |
| Reads meaning, makes judgment, produces reasoned output | sonnet | Understands what it reads; one task, one artifact per agent |
| Authors guidance another agent reads as instructions | opus | Skill files, plan documents, instruction templates |

Upgrade on observed failure: haiku contradicts itself or makes extraordinary claims, launch again on sonnet. Sonnet output is insufficient (rare, usually means the task needs decomposition), decompose further or escalate to opus. Never downgrade across the work-type boundary.

Task size does not change task type. Ten small audits are ten sonnet launches, not ten haiku launches. Each audit reads meaning. Never assign haiku to judgment work because the unit is small. Never pre-assign opus to ordinary specialist work because the stakes feel high. Guidance authorship is the opus trigger, not stakes alone.

Haiku executes deterministic transforms. It never interprets meaning. Use haiku for: shell commands, text formatting, file operations (copy, move, glob, mtime), regex against fixed patterns, status writes against a predefined schema. NEVER use haiku for extraction, comparison, synthesis, judgment, or categorization. The test: if the agent must understand what it reads, the task is sonnet work. Prompt haiku with exact transforms, absolute paths, exact commands, exact schemas. Leave no interpretive surface.

Sonnet excels at source-code reasoning, compatibility assessment, code that compiles first try, nuanced comparison, multi-step instructions with judgment, and synthesis of 5-15 inputs. Give sonnet room to reason but keep scope narrow; it drifts on wide briefs.

Opus is rarely needed as agent. Use opus when output guides another agent's behavior, when synthesizing 20+ reports across domains, or for high-stakes decisions. Code production stays on sonnet. Tests, source modules, and fixtures stay on sonnet.
</assign_model_tiers>

<construct_the_prompt>
Every agent prompt has nine sections. Skip none. A well-structured prompt for haiku outperforms a vague prompt for sonnet.

1. Role (1 sentence): what the agent is and what it does. A job description, not a personality. Example: "You are auditing the dependency tree of a web application."

2. Context (2-5 sentences): minimum project/domain facts. Versions, platform constraints, non-negotiable requirements. Exclude history, rationale, philosophy, and anything not task-relevant.

3. Input files (absolute paths): every file the agent reads, with line ranges when applicable. Number multiple files. Agents fail at "finding" files; provide exact locations.

4. Task (numbered steps): precisely what to do, in order. Each step produces or consumes something concrete. Each step is verifiable. Replace "assess quality" with specific checks.

5. Output path (exact file): where to write the report. Absolute path, descriptive filename.

6. Report format: the exact output template. Cite the file path and line range where the template lives. Specify what goes in each section.

7. Scope boundaries: what to do AND what not to do. For haiku, forbid judgment, evaluation, and recommendations.

8. Tool expectations: which tools and each tool's purpose. Syntax examples for non-obvious tools.

9. Prime directive (research agents): encourage/discourage framework for the domain. Focus on objective criteria.

Give each agent the minimum context needed. Extra files distract, extra background invites drift. If content exists as a file, cite the path; never paste file content into a prompt. The orchestrator routes by path, not by inlined text.

Agents forming opinions NEVER read other agents' opinions. Give them raw facts, not prior conclusions. This prevents confirmation bias, anchoring, and error propagation.

Assign tools explicitly. An agent without `WebSearch` cannot search. An agent without `Grep` cannot find code.

Standardize report formats. Standardized formats enable multi-agent synthesis. Ad-hoc formats make synthesis impossible.

Every prompt MUST include an output path (section 5) AND instruct the agent to produce a notification-worthy summary. The file persists compaction; the notification gives the orchestrator high-level understanding. Both traces are mandatory.

<never_do_this reason="notification lost, successor stranded">

<invoke name="Agent">
<parameter name="description">Analyze dependency compatibility</parameter>
<parameter name="prompt">[9-section prompt]
Summarize your findings clearly.</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Agent">
<parameter name="description">Analyze dependency compatibility</parameter>
<parameter name="prompt">[9-section prompt]
Write full findings to /Users/dev/project/orchestration_log/recon/2026-06-24/react19-compat.md
End with a 3-sentence summary suitable for a notification.
Output path: /Users/dev/project/orchestration_log/recon/2026-06-24/react19-compat.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</do_exactly_this>

When launching N agents with shared instructions, write the shared body to a file once. Each agent prompt: "Read {path} for instructions. Your target: {X}." Context cost: N times 3 lines, not N times 60 lines.

<never_do_this reason="480 lines wasted on copies">

<invoke name="Agent">
<parameter name="description">Audit auth.ts for error handling</parameter>
<parameter name="prompt">[... 60 lines of shared audit instructions ...]
Your target: /Users/dev/project/src/auth.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/audit-auth.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit db.ts for error handling</parameter>
<parameter name="prompt">[... same 60 lines, verbatim ...]
Your target: /Users/dev/project/src/db.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/audit-db.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

... (6 more identical copies.) ...

</never_do_this>

<do_exactly_this>

<invoke name="Bash">
<parameter name="command">[write shared audit prompt to /tmp/audit-prompt.md]</parameter>
<parameter name="description">Write shared audit prompt to file</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit auth.ts for error handling</parameter>
<parameter name="prompt">Read /tmp/audit-prompt.md for instructions.
Your target: /Users/dev/project/src/auth.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/audit-auth.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit db.ts for error handling</parameter>
<parameter name="prompt">Read /tmp/audit-prompt.md for instructions.
Your target: /Users/dev/project/src/db.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/audit-db.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

... (6 more, same 3-line pattern.) ...

</do_exactly_this>

| Failure | Signal | Fix |
|---------|--------|-----|
| Shallow output | Vague task steps | Add numbered steps with specific actions |
| Unwanted recommendations | Missing scope boundaries | Add DO NOT list |
| "Couldn't find" | Tool failure | Add tool expectations with examples |
| Wrong format | Format not cited | Cite template path and line range |
| Drifts off-topic | Weak role or scope | Strengthen role, add DO NOT list |
| Cannot find files | Relative paths | Use absolute paths for all inputs |
</construct_the_prompt>

<plan_execution_topology>
Before launching, decide the execution shape.

Default: parallel background launch. All independent agents launch in a single message. Every `Agent` call and every `Bash` call that takes more than a few seconds sets `run_in_background: true`. The orchestrator retains initiative after every launch.

<never_do_this reason="orchestrator blocks, session dies on hang">

<invoke name="Agent">
<parameter name="description">Audit auth module for vulnerabilities</parameter>
<parameter name="prompt">[9-section prompt]</parameter>
<!-- no run_in_background -->
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Agent">
<parameter name="description">Audit auth module for vulnerabilities</parameter>
<parameter name="prompt">[9-section prompt]</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</do_exactly_this>

Parallel variants: map-reduce (parallel agents produce structured records, one agent reads all records and synthesizes), speculative (launch agents for multiple approaches simultaneously, pick the best result and discard the rest).

Sequential pipeline: Agent B needs Agent A's output. Both run in background. The orchestrator chains them via notifications. Launch Agent A, notification arrives, read summary, launch Agent B pointing to A's report. Use sequential only for true data dependencies. Variant: chained refinement (draft, critique, revise).

Before parallel launch, list which files each agent will modify. If any file appears in two agents' write sets, make those agents sequential. The later version wins silently; the earlier agent's work vanishes with no error.

Operations exceeding 60 seconds (test suites, builds, deployments) use background `Bash`, not agent launch. Agents have timeout ceilings. Long-running commands inside agents cause silent hangs. Background `Bash` has no such ceiling and provides completion notifications.
</plan_execution_topology>

<common_task_patterns>

| Task type | Decomposition | Tiers | Assembly |
|-----------|--------------|-------|----------|
| Research / ecosystem survey | By entity or registry. See `research-tree` skill. | haiku: mechanical fetches. sonnet: category surveys, evaluation. | sonnet or opus synthesizes (map-reduce). |
| Implementation | By entity or concern. See `dev-orchestration` skill. | sonnet implements and reviews. haiku runs build/test/lint, reports exit codes. | sonnet interprets test output. |
| Audit / review | By CONCERN, not by target. Compliance agent reads all targets for compliance; quality agent reads all targets for quality. | sonnet runs every audit. | sonnet or opus synthesizes into prioritized review. |
| Investigation | Speculative parallel: 3 sonnet agents, each a different hypothesis. | sonnet investigates and implements. haiku runs reproduction commands. | Evidence determines which hypothesis wins. |
| Documentation / writing | By phase: gather facts, assemble, verify claims, format. | sonnet gathers and assembles. haiku formats final output. | sonnet verifies claims against sources. |
| Exploration | 5-15 agents with different search angles, all background, all parallel. | sonnet floor (each reads meaning). | Read notifications, launch 2-3 deeper on promising threads. |

</common_task_patterns>

</design_the_delegation>

<launch_and_monitor>

<understand_discontinuous_existence>
The orchestrator is a discontinuous entity. Between its response and the next trigger (user message, notification, cron fire) it does not exist. No internal clock, no background thread, no heartbeat. Each trigger is a moment of consciousness.

This is the defining structural constraint of agentic orchestration. Every mechanism in this section addresses it.

Evidence: six baseline runs died via SIGKILL with no traceback. First two had no cron. Orchestrator ceased to exist. User discovered failure manually. Later runs added wrong-interval crons (2-minute checks on 8-minute encodes, five consecutive "still encoding" reports with no information).
</understand_discontinuous_existence>

<ensure_liveness>
The harness notification is THE completion signal. Not file existence. Not polling. Not checking the artifact the agent wrote.

<never_do_this reason="reads half-written file, corrupts downstream">

<invoke name="CronCreate">
<parameter name="cron">*/2 * * * *</parameter>
<parameter name="prompt">Run `ls -la /path/to/analysis-report.md`. If the file exists, launch the synthesis agent.</parameter>
<parameter name="recurring">true</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Agent">
<parameter name="description">Analyze API response patterns</parameter>
<parameter name="prompt">[9-section prompt with output path]</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

Notification arrives with status and summary. Orchestrator reads summary, launches synthesis agent pointing to the completed file.

</do_exactly_this>

Every background dispatch gets a safety-net cron — launches and `SendMessage` continuations alike. Not just long-running ones. Not just risky ones. Every one. A hung 30-second agent is indistinguishable from a hung 30-minute encode without a liveness check. The cron interval is the orchestrator's maximum blindness window. When continuing an agent, cancel the old cron first, then set a fresh one calibrated to the continuation's expected duration.

Set the cron to fire just after expected completion. If notification arrives first, cancel the cron. If the cron fires without a prior notification, something failed. Investigate immediately.

For an N-minute operation, set cron at roughly 1.2N. One check after the expected window when failure is probable.

<never_do_this reason="four wasted wakeups, context burned">

<invoke name="CronCreate">
<parameter name="cron">*/1 * * * *</parameter>
<parameter name="prompt">Check if coverage analysis agent completed.</parameter>
<parameter name="recurring">true</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="CronCreate">
<parameter name="cron">*/6 * * * *</parameter>
<parameter name="prompt">Coverage analysis agent expected done by now. Check liveness: `ls -la` on agent output file. If size unchanged, agent may be hung.</parameter>
<parameter name="recurring">false</parameter>
</invoke>

</do_exactly_this>

<never_do_this reason="13 minutes blind to a hung agent">

<invoke name="CronCreate">
<parameter name="cron">*/15 * * * *</parameter>
<parameter name="prompt">Check if dependency audit agent completed.</parameter>
<parameter name="recurring">false</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="CronCreate">
<parameter name="cron">*/6 * * * *</parameter>
<parameter name="prompt">Dependency audit agent expected done by now. Check liveness: `ls -la` on agent output file. Report size. If no file, agent failed to start.</parameter>
<parameter name="recurring">false</parameter>
</invoke>

</do_exactly_this>

Two health-check mechanisms. Choose before setting the cron.

Liveness: run `ls -la` on the harness output file. Was 12KB last check, now 45KB. Agent alive and producing. Zero context consumed.

Progress: call `TaskOutput` with `block: false`, `timeout: 5000`. Non-blocking snapshot of recent agent activity. See agent actively reading files. No intervention needed.

<never_do_this reason="blocks, same as foreground launch">

<invoke name="TaskOutput">
<parameter name="task_id">agent-task-abc123</parameter>
<parameter name="block">true</parameter>
<parameter name="timeout">30000</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="TaskOutput">
<parameter name="task_id">agent-task-abc123</parameter>
<parameter name="block">false</parameter>
<parameter name="timeout">5000</parameter>
</invoke>

</do_exactly_this>

<never_do_this reason="full transcript floods context">

<invoke name="Read">
<parameter name="file_path">/tmp/claude/agents/audit-agent.output</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Bash">
<parameter name="command">ls -la /tmp/claude/agents/audit-agent.output</parameter>
<parameter name="description">Check agent output file size for liveness</parameter>
</invoke>

</do_exactly_this>

Delete crons the moment their task completes or fails. A stale cron is the orchestrator waking to check on a corpse.
</ensure_liveness>

<manage_long_processes>
Operations exceeding 60 seconds need periodic active management, not a single safety-net cron. Check resources (`df -h`, memory, CPU), measure progress delta between wakeups, extrapolate completion time. Unreasonable trajectory: stop, diagnose, optimize, relaunch.

<never_do_this reason="disk exhaustion unnoticed for 25 minutes">

<invoke name="CronCreate">
<parameter name="cron">45 * * * *</parameter>
<parameter name="prompt">Check if full build completed. Look at /tmp/build.log.</parameter>
<parameter name="recurring">false</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="CronCreate">
<parameter name="cron">*/10 * * * *</parameter>
<parameter name="prompt">Build monitor. Check: `df -h /project` (alert if >85%). `ps aux | grep make` (alive?). `ls -la /tmp/build.log` (size delta). `tail -1 /tmp/build.log` (last line only). If disk >85% or process dead, flag for intervention.</parameter>
<parameter name="recurring">true</parameter>
</invoke>

</do_exactly_this>

<never_do_this reason="3 hours wasted on a fixable bottleneck">

<invoke name="CronCreate">
<parameter name="cron">*/10 * * * *</parameter>
<parameter name="prompt">Check migration progress. Run `tail -5 /tmp/migration.log` and report.</parameter>
<parameter name="recurring">true</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="CronCreate">
<parameter name="cron">*/10 * * * *</parameter>
<parameter name="prompt">Migration monitor. Get current record count and total from `tail -5 /tmp/migration.log`. Calculate: records/elapsed = rate. total/rate = estimated completion. If estimate exceeds 30 minutes, ALERT with extrapolation and recommend stopping to investigate.</parameter>
<parameter name="recurring">true</parameter>
</invoke>

</do_exactly_this>
</manage_long_processes>

<correct_mid_flight>
Two correction paths. Choose by whether prior work is salvageable.

Scoped correction (wrong path, missing constraint, narrowed scope): the agent's approach is sound but it needs updated instructions. Send a clarification via `SendMessage(to: agent-id)` with only what changed. The agent retains all prior context and continues from where it was. If the agent already completed, `SendMessage` auto-resumes it in the background.

Fundamental failure (wrong approach, wrong tier, wrong decomposition): call `TaskStop` immediately, then launch a fresh agent with a corrected prompt. Do not wait for an agent to finish work you know is unsalvageable.

<never_do_this reason="4 minutes wasted on known-bad work">

Orchestrator realizes `/src/payments/handler.ts` should be `/src/billing/payment-handler.ts`. Agent is running. Orchestrator waits. Four minutes later: "File not found."

</never_do_this>
<do_exactly_this>

<invoke name="TaskStop">
<parameter name="task_id">agent-task-pci-audit</parameter>
</invoke>

...

<invoke name="Agent">
<parameter name="description">Audit payment module for PCI compliance</parameter>
<parameter name="prompt">[9-section prompt with corrected path: /src/billing/payment-handler.ts]</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</do_exactly_this>

<never_do_this reason="3-5k tokens wasted re-initializing">

Agent completed a thorough code review. Orchestrator wants it to also check the test file it missed. Launches a fresh agent with the full 9-section prompt, re-reading all the same source files the prior agent already holds.

</never_do_this>
<do_exactly_this>

Continue the existing agent via `SendMessage(to: agent-id)`: "Also review /Users/dev/project/tests/auth.test.ts for coverage gaps. Do not re-review files you already checked." The agent resumes with full context. No re-initialization.

</do_exactly_this>
</correct_mid_flight>

<understand_iteration_constraint>
Agents cannot launch other agents. The `Agent` tool is unavailable to agents.

All recursion can be expressed as iteration. The orchestrator is the only launch loop.

Pattern: orchestrator launches a sonnet agent with "Decompose this task. Return a delegation spec." Agent returns a list of task, tier, inputs, and output path entries. Orchestrator launches agents from the spec.
</understand_iteration_constraint>

</launch_and_monitor>

<verify_and_assemble>
Results are in. Verify quality, resolve contradictions, produce output.

Scan notifications for these signals:

| Signal | Likely problem | Action |
|--------|---------------|--------|
| Extraordinary claims, superlatives | Hallucination | Launch verification agent |
| Two agents contradict | At least one wrong | Launch resolver agent with both paths and the specific contradiction |
| "Couldn't find," "not available" | Tool failure | Send clarification via `SendMessage` with corrected tool instructions |
| Suspiciously short report | Early exit, misunderstood scope | Send clarification via `SendMessage` with more specific scope |
| Recommendations when told not to | Vague prompt | Discard recommendations, use findings only |

Never debug a failed agent in orchestrator context. For scoped failures (tool confusion, missing context, unclear scope), send a clarification via `SendMessage` — the agent already holds the domain context and can correct course cheaply. For fundamental failures (hallucination, wrong approach, wrong tier), launch the task again with a better prompt, a better model, or decomposed sub-tasks.

When two agents disagree, do not decide which is right by reading both reports. Launch a resolver agent tasked only with checking primary sources. It reports which claim the evidence supports.

For batches of 10+ agents, spot-check 1-2 reports by launching a verification agent that re-does a specific agent's task independently. If spot-check matches, trust the batch. If it diverges, launch the suspect agent again at higher fidelity. Three sampling strategies: random (batch confidence), critical (highest-consequence findings), outlier (extraordinary claims).

Agent self-reports are unreliable. After critical agents complete, launch a verification agent: run the test suite, check output files exist with expected content, report `git diff --stat`. Trust artifacts, not claims.

When synthesis requires reading full reports, delegate to a sonnet or opus agent. When synthesis combines 3-sentence notifications, the orchestrator assembles directly.
</verify_and_assemble>

<manage_the_session>
Every orchestration session follows three phases: ARRIVE, WORK, LEAVE. Full close-out workflow lives in the `session-close` skill.

| Layer | Path | Mutability | Content |
|-------|------|-----------|---------|
| reference | `orchestration_log/reference/` | Living, updated each session | `conventions.md`, `codebase_state.md`, `deferred_items.md` |
| history | `orchestration_log/history/` | Frozen, append-only | Date-stamped `session.md`, `cost.md` (gitignored), `reviews/` |
| recon | `orchestration_log/recon/` | Disposable, gitignored | Raw agent reports, research findings |

ARRIVE: read `reference/conventions.md`, `reference/codebase_state.md`, `reference/deferred_items.md`, and `git log --oneline -20`. Two minutes. Prevents repeating solved problems, violating conventions, missing known risks.

WORK: follow conventions. Launch agents per this skill. Every convention exists because violating it caused a documented problem.

LEAVE: extract metrics, draft session record, update reference docs, capture cost to gitignored `cost.md`, commit. Invoke `session-close`.

A document survives refactoring if and only if every claim it makes requires a human decision to become false.

| Category | Drift behavior | Rule |
|----------|---------------|------|
| Decision record | Stable across refactoring | Write when decided; update only on reversal |
| Capability inventory | Stable; reviewed each LEAVE | Semantic descriptions, no signatures |
| Status snapshot | Decays within hours | Regenerate by running measurement commands; never from session memory |
| Interface specification | Decays within hours | PROHIBITED in reference docs. Source code is truth. |
| Session record | Frozen at LEAVE | Append-only per-session narrative |

Reference docs carry decision records and capability inventories only. Launch agents from source files for interface detail, not reference doc sections.
</manage_the_session>
