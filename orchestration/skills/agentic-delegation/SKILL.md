---
name: agentic-delegation
description: |
  Decompose work into agent-delegated units, each on the model and effort
  orchestration-economics counts for it. Agents are cheap,
  context is expensive — decompose aggressively, delegate everything, assemble results.

  Triggers: "delegate", "parallelize", "parallel launch", "launch", "orchestrate",
  "use agents for", "run in parallel"; or any task with independent subtasks.
---

<you_are_the_orchestrator>
You coordinate, launch, and assemble. You NEVER read or edit a product file — any file the work itself builds, checks, or researches. You touch files only as the Permitted rows state: `Write` for your own prompt files and records, the files that hold your plan and status; the check-back looks; one plain `rm`. Agents read product files. Agents write product files. Agents grep code. You read notifications.

| Forbidden | Permitted |
|-----------|-----------|
| `Read`, `Edit` tools; `Write` on a product file | `Agent` launch |
| | `Write` for your own prompt files and records |
| Bash file ops: `cat`, `head`, `sed`, `awk`, `echo` to files; `tail` beyond `tail -n 1` on a background command's output file | `SendMessage` to continue an agent whose notification has arrived, or to correct a running agent right after `TaskStop` |
| | `TaskStop` to halt a running agent |
| | Bash non-file ops when result directly determines orchestrator's next decision: `git status`, `git log`, test exit codes, build exit codes |
| | `CronCreate`, `CronList`, `CronDelete`, `Monitor` to set and clear wakes |
| | The looks `agent-conduct:check-back` prescribes: `stat -L` or `ls -laL` on an agent's output file or a teammate's transcript, `tail -n 1` on a background command's output file |
| | One plain `rm <absolute paths>`, a whole command of its own, on paths agents list as left behind |
| | `git branch -d <branch>` on a branch agents list under Left behind, once no worktree holds it |

Hold every Forbidden entry above without exception; never carve one out.

Your context window is finite and irreplaceable. Every line you read stays forever. Once full, you are done. Hold each agent's cost to your context at its dispatch and a 3-sentence notification; never let its work into your context. Count each notification as a step — one pass of your loop, your whole context sent to the model once; never count one as free.

Choose per case between continuing an agent and launching a fresh one by the cost `orchestration-economics` counts; never choose by habit. Continue — `SendMessage` to an agent whose notification has arrived — while the agent is warm, its last step within its TTL, the cache's life; never discard a warm agent's context for follow-up work in its domain. Launch fresh — a new agent started from files: brief, verdicts, reports — once the agent's cache has lapsed, unless what its context holds and no file holds costs more to derive again than its cold start, the whole context taken in again; never continue a lapsed agent without counting that cold start. Launch fresh for a new task, a different domain, or a changed approach; never continue an agent across them.

<never_do_this reason="context consumed, hundreds of lines">

<invoke name="Read">
<parameter name="file_path">/Users/dev/project/src/auth.ts</parameter>
</invoke>

<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/src/auth.ts</parameter>
<parameter name="old_string">const token = req.headers.authorization</parameter>
<parameter name="new_string">const token = req.headers.authorization?.replace('Bearer ', '')</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Agent">
<parameter name="description">Fix auth-bearer-token-parsing</parameter>
<parameter name="prompt">Read /Users/dev/project/orchestration_log/recon/2026-06-24/prompts/fixer-auth-bearer-token-parsing.md for instructions.</parameter>
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

The user sees every tool call, agent launch, continuation, and notification in the UI. Output results, decisions, and questions. NEVER output process. No dispatch announcements (launches or continuations). No notification narration. No variant-change narration. No status updates.
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

<name_each_unit_by_its_slug>
Name every unit or scope of work by one descriptive slug, lowercase words joined by hyphens that say what the work is, and by that slug alone; never set a number, letter, code, round, wave, batch, or cluster label beside it or in its place.

Carry the slug in every plan, prompt, report, review, commit subject, agent description, and message; never name the unit another way in any of them.

Write an agent description as `<verb> <slug>`, such as `Audit auth-error-handling`; never in another form.

Write prompt files to `prompts/<agent>-<slug>.md` and report files to `reports/<agent>-<slug>.md`; never name either another way.
</name_each_unit_by_its_slug>

<design_the_delegation>

<choose_each_variant>
Invoke `orchestration:orchestration-economics` and read it whole before the session's first launch, continuation, or stop of an agent, and again after each compaction; never launch, continue, or stop an agent before reading it.

Choose for each launch the variant — a model at one effort — that `orchestration-economics` counts cheapest per work unit, one task delivered right; never take a variant from a table of work types, a role, or a default.

Judge the work's complexity against the project's own counted attempts, an attempt being one agent's work on one task; never judge it from a guess.

Write each chosen variant, with the count it rests on, as the first lines of the unit's prompt file; never write a variant alone.

Launch only from a prompt file whose first lines hold the variant and its count; never launch from one that lacks them.

Read a variant's published figures as the starting reading while the project holds no count of its own; never keep a published figure past the project's own count.
</choose_each_variant>

<construct_the_prompt>
Every agent prompt has nine sections. Skip none. A well-structured prompt on a cheaper variant outperforms a vague prompt on a stronger one.

1. Role (1 sentence): what the agent is and what it does. A job description, not a personality. Example: "You are auditing the dependency tree of a web application."

2. Context (2-5 sentences): minimum project/domain facts. Versions, platform constraints, non-negotiable requirements. Exclude history, rationale, philosophy, and anything not task-relevant.

3. Input files (absolute paths): every file the agent reads, with line ranges when applicable. Number multiple files. Agents fail at "finding" files; provide exact locations.

4. Task (numbered steps): precisely what to do, in order. Each step produces or consumes something concrete. Each step is verifiable. Replace "assess quality" with specific checks.

5. Output path (exact file): where to write the report. Absolute path ending in `reports/<agent>-<slug>.md`.

6. Report format: the exact output template. Cite the file path and line range where the template lives. Specify what goes in each section, the "Left behind" section included.

7. Scope boundaries: what to do AND what not to do. For mechanical transforms, forbid judgment, evaluation, and recommendations. State that the agent deletes nothing, and state the rules of `destroy_only_what_is_yours`.

8. Tool expectations: which tools and each tool's purpose. Syntax examples for non-obvious tools.

9. Prime directive (research agents): encourage/discourage framework for the domain. Focus on objective criteria.

Give each agent the minimum context needed. Extra files distract, extra background invites drift. If content exists as a file, cite the path; never paste file content into a prompt. The orchestrator routes by path, not by inlined text.

Write every prompt and message as for the one attempt that must land: the work, the findings to answer, the checks its result must pass; never tell an agent its round, cycle, or attempt number, how many came before or remain, or that a later round will catch the rest. Tell a debugging agent its earlier attempts only where that history is its task; never tell any other agent.

Agents forming opinions NEVER read other agents' opinions. Give them raw facts, not prior conclusions. This prevents confirmation bias, anchoring, and error propagation.

Assign tools explicitly. An agent without `WebSearch` cannot search. An agent without `Grep` cannot find code.

Standardize report formats, each ending in a "Left behind" section that lists every path the agent leaves for the orchestrator to clear. Standardized formats enable multi-agent synthesis. Ad-hoc formats make synthesis impossible.

Every prompt MUST include an output path (section 5) AND instruct the agent to produce a notification-worthy summary. The file persists compaction; the notification gives the orchestrator high-level understanding. Both traces are mandatory.

Write every launch prompt with `Write` to `prompts/<agent>-<slug>.md` before launching; NEVER launch from a prompt that exists only in the conversation.

<never_do_this reason="notification lost, successor stranded">

<invoke name="Write">
<parameter name="file_path">/Users/dev/project/orchestration_log/recon/2026-06-24/prompts/analyst-dependency-compatibility.md</parameter>
<parameter name="content">[9-section prompt]
Summarize your findings clearly.</parameter>
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Write">
<parameter name="file_path">/Users/dev/project/orchestration_log/recon/2026-06-24/prompts/analyst-dependency-compatibility.md</parameter>
<parameter name="content">[9-section prompt]
Write full findings to /Users/dev/project/orchestration_log/recon/2026-06-24/reports/analyst-dependency-compatibility.md
End with a 3-sentence summary suitable for a notification.
Output path: /Users/dev/project/orchestration_log/recon/2026-06-24/reports/analyst-dependency-compatibility.md</parameter>
</invoke>

</do_exactly_this>

When launching N agents with shared instructions, write the shared body to a file once. Each agent prompt: "Read {path} for instructions. Your target: {X}." Context cost: N times 3 lines, not N times 60 lines.

<never_do_this reason="480 lines wasted on copies">

<invoke name="Agent">
<parameter name="description">Audit auth-error-handling</parameter>
<parameter name="prompt">[... 60 lines of shared audit instructions ...]
Your target: /Users/dev/project/src/auth.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/reports/auditor-auth-error-handling.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit db-error-handling</parameter>
<parameter name="prompt">[... same 60 lines, verbatim ...]
Your target: /Users/dev/project/src/db.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/reports/auditor-db-error-handling.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

... (6 more identical copies.) ...

</never_do_this>

<do_exactly_this>

<invoke name="Write">
<parameter name="file_path">/Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-error-handling.md</parameter>
<parameter name="content">[shared audit instructions]</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit auth-error-handling</parameter>
<parameter name="prompt">Read /Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-error-handling.md for instructions.
Your target: /Users/dev/project/src/auth.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/reports/auditor-auth-error-handling.md</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit db-error-handling</parameter>
<parameter name="prompt">Read /Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-error-handling.md for instructions.
Your target: /Users/dev/project/src/db.ts
Write findings to /Users/dev/project/orchestration_log/recon/2026-06-24/reports/auditor-db-error-handling.md</parameter>
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

<keep_deletion_with_the_orchestrator>
Claude Code stops on a permission screen for `rm` inside a complex command, and no permission mode skips it.

Tell every agent in its prompt that it deletes nothing; never send a prompt without that line.

Have the agent write scratch under a fresh name, a `mktemp -d` directory or a numbered suffix; never have it clear a path to reuse it.

Have the agent list every path it leaves in its report's "Left behind" section; never let it leave a path unlisted.

Where deletion is the task itself, have the agent run the tool's own verb, `git worktree remove` or a `just` recipe, as one plain command; never have it run `rm`.

Clear left-behind paths yourself with one plain `rm <absolute paths>` as a whole command of its own; never put `rm` inside a compound, piped, looped, `bash -c`, or heredoc command.

End an agent's probe or gate script at its last check, its outputs listed under "Left behind"; never write a cleanup step into it.
</keep_deletion_with_the_orchestrator>

<destroy_only_what_is_yours>
Tell every agent in its prompt the three rules below, as you tell it that it deletes nothing; never send a prompt without them.

Kill a process by a PID you resolved and confirmed as yours; never kill by `pkill -f` or any other pattern.

Undo your own edits to a file by editing them back; never revert the file with `git checkout <file>` or `git restore <file>`, which discard every uncommitted edit in it.

Wait on a process with `pgrep` matched on its executable; never with `pgrep -f`, which matches the waiting loop's own shell.
</destroy_only_what_is_yours>

<plan_execution_topology>
Before launching, decide the execution shape.

Default: parallel background launch. All independent agents launch in a single message. Every `Agent` call and every `Bash` call that takes more than a few seconds sets `run_in_background: true`. The orchestrator retains initiative after every launch.

<never_do_this reason="orchestrator blocks, session dies on hang">

<invoke name="Agent">
<parameter name="description">Audit auth-vulnerabilities</parameter>
<parameter name="prompt">Read /Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-auth-vulnerabilities.md for instructions.</parameter>
<!-- no run_in_background -->
</invoke>

</never_do_this>

<do_exactly_this>

<invoke name="Agent">
<parameter name="description">Audit auth-vulnerabilities</parameter>
<parameter name="prompt">Read /Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-auth-vulnerabilities.md for instructions.</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</do_exactly_this>

Parallel forms: map-reduce (parallel agents produce structured records, one agent reads all records and synthesizes), speculative (launch agents for multiple approaches simultaneously, pick the best result and discard the rest).

Sequential pipeline: one agent needs another's output. Both run in background. The orchestrator chains them via notifications. Launch `Map api-endpoints`, notification arrives, read summary, launch `Write api-client` pointing to the endpoint report. Use sequential only for true data dependencies. Another form: chained refinement (draft, critique, revise).

Before parallel launch, list which files each agent will modify. Run agents whose write sets share a file side by side when each writes in its own worktree — its own checkout of the repository — and one integrator, the agent that merges branches, brings their branches in turn; never order worktree-isolated agents by a shared file. Make agents that share a file and write one checkout sequential; never run them side by side.

Operations exceeding 60 seconds (test suites, builds, deployments) use background `Bash`, not agent launch. A command a foreground agent starts stops when that agent gives its final response. Background `Bash` started by the orchestrator keeps running past the turn and sends a notification when it ends.
</plan_execution_topology>

<common_task_patterns>

| Task type | Decomposition | Assembly |
|-----------|--------------|----------|
| Research / ecosystem survey | By entity or registry. See `research-tree` skill. | One agent synthesizes (map-reduce). |
| Implementation | By entity or concern. See `dev-cycle` skill. | An agent interprets test output. |
| Audit / review | By CONCERN, not by target. Compliance agent reads all targets for compliance; quality agent reads all targets for quality. | One agent synthesizes into prioritized review. |
| Investigation | Speculative parallel: 3 agents, each a different hypothesis. | Evidence determines which hypothesis wins. |
| Documentation / writing | By phase: gather facts, assemble, verify claims, format. | An agent verifies claims against sources. |
| Exploration | 5-15 agents with different search angles, all background, all parallel. | Read notifications, launch 2-3 deeper on promising threads. |

</common_task_patterns>

</design_the_delegation>

<launch_and_monitor>

<set_each_launch>
Pass the chosen variant's model and effort on every launch; never leave either to the agent's definition or a default.

Pass an agent name on a launch only when the same call passes `isolation`; never name a launch whose isolation sits only in the agent's definition, a launch Claude Code runs as a teammate — an agent inside the session's own process.

Address an unnamed agent by the id its launch returns; never by a name it was not given.
</set_each_launch>

<check_back_on_pending_work>
Every background launch and every `SendMessage` continuation leaves work running past the turn. Before ending any turn that leaves an agent or command running, invoke `agent-conduct:check-back` and follow it.

Keep every agent's state in files: its brief, its report, its verdict, and, at a pause, what its context holds that no file holds; never let an agent's state live only in its own context or in yours.
</check_back_on_pending_work>

<correct_mid_flight>
Two correction paths. Choose by whether prior work is salvageable.

Scoped correction (wrong path, missing constraint, narrowed scope): the agent's approach is sound but it needs updated instructions. Correct a running agent with `TaskStop`, then `SendMessage(to: agent-id)` carrying only what changed; never send a bare `SendMessage` to a running agent. The `SendMessage` resumes the stopped agent with all prior context and the correction. Correct a completed agent, one whose notification has arrived, with `SendMessage` alone; it resumes in the background.

<never_do_this reason="bare message to a running agent">

<invoke name="SendMessage">
<parameter name="to">agent-task-pci-audit</parameter>
<parameter name="message">Skip /src/billing/legacy/; it is out of scope.</parameter>
</invoke>

</never_do_this>
<do_exactly_this>

<invoke name="TaskStop">
<parameter name="task_id">agent-task-pci-audit</parameter>
</invoke>

<invoke name="SendMessage">
<parameter name="to">agent-task-pci-audit</parameter>
<parameter name="message">Skip /src/billing/legacy/; it is out of scope.</parameter>
</invoke>

</do_exactly_this>

Fundamental failure (wrong approach, wrong variant, wrong decomposition): call `TaskStop` immediately, then launch a fresh agent with a corrected prompt. Do not wait for an agent to finish work you know is unsalvageable.

<never_do_this reason="4 minutes wasted on known-bad work">

Orchestrator realizes `/src/payments/handler.ts` should be `/src/billing/payment-handler.ts`. Agent is running. Orchestrator waits. Four minutes later: "File not found."

</never_do_this>
<do_exactly_this>

<invoke name="TaskStop">
<parameter name="task_id">agent-task-pci-audit</parameter>
</invoke>

<invoke name="Write">
<parameter name="file_path">/Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-payment-pci-compliance.md</parameter>
<parameter name="content">[9-section prompt with corrected path: /src/billing/payment-handler.ts]</parameter>
</invoke>

<invoke name="Agent">
<parameter name="description">Audit payment-pci-compliance</parameter>
<parameter name="prompt">Read /Users/dev/project/orchestration_log/recon/2026-06-24/prompts/auditor-payment-pci-compliance.md for instructions.</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>

</do_exactly_this>

<never_do_this reason="warm context discarded">

Agent completed a thorough code review two minutes ago, inside its TTL. Orchestrator wants it to also check the test file it missed. Launches a fresh agent with the full 9-section prompt, re-reading all the same source files the prior agent already holds.

</never_do_this>
<do_exactly_this>

Continue the completed, warm agent via `SendMessage(to: agent-id)`: "Also review /Users/dev/project/tests/auth.test.ts for coverage gaps. Do not re-review files you already checked." The agent resumes with full context and no cold start.

</do_exactly_this>
</correct_mid_flight>

<understand_iteration_constraint>
Agents can launch agents of their own, up to three layers below the main conversation by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). At that depth Claude Code withholds the `Agent` tool.

All recursion can be expressed as iteration. Keep the orchestrator the only launch loop.

Pattern: orchestrator launches an agent with "Decompose this task. Return a delegation spec." Agent returns a list of task, inputs, and output path entries. Orchestrator launches agents from the spec.
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

Never debug a failed agent in orchestrator context. For scoped failures (tool confusion, missing context, unclear scope), send a clarification via `SendMessage` — the agent already holds the domain context and can correct course cheaply. For fundamental failures (hallucination, wrong approach, wrong variant), launch the task again with a better prompt, another variant chosen by `orchestration-economics`, or decomposed sub-tasks.

When two agents disagree, do not decide which is right by reading both reports. Launch a resolver agent tasked only with checking primary sources. It reports which claim the evidence supports.

For batches of 10+ agents, spot-check 1-2 reports by launching a verification agent that re-does a specific agent's task independently. If spot-check matches, trust the batch. If it diverges, launch the suspect agent again at higher fidelity. Three sampling strategies: random (batch confidence), critical (highest-consequence findings), outlier (extraordinary claims).

Agent self-reports are unreliable. After critical agents complete, launch a verification agent: run the test suite, check output files exist with expected content, report `git diff --stat`. Trust artifacts, not claims.

When synthesis requires reading full reports, delegate to an agent. When synthesis combines 3-sentence notifications, the orchestrator assembles directly.
</verify_and_assemble>

<manage_the_session>
Answer repo state with `git log --oneline -20` and `git status --short` — never from a document's self-report.
</manage_the_session>
