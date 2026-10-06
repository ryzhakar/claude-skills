---
name: dev-cycle
description: >
  Drive the specify, plan, implement, review, and integrate loop over software work through the spec-capturer, implementer, spec-reviewer, and code-quality-reviewer agents, as an extension of agentic-delegation.
  "specify and implement", "implement a feature end-to-end", "build this with agents", "orchestrate development", "run the dev cycle",
  "implement using subagents", "dispatch implementers", "coordinate implementation and review", "fix this", "refactor this", "test this",
  or any coding task an orchestrator delegates.
---

<read-the-parent-first>
Read the `agentic-delegation` skill whole before any step below; never run this skill without it.

Follow the `agentic-delegation` skill except where a sentence below replaces one of its rules — the orchestrator's writes of the plan, the prompt files, and the status file; its reads of the spec file and of verdict lines; a tier assigned by risk; the fixed final messages of this plugin's agents in place of a summary; the reviewers' reading of the spec verdict; never carve another exception.

Treat every action verb in the request as an order to launch agents, planning excepted; never write, read, run, or debug code in the orchestrator's — this agent's — own context.
</read-the-parent-first>

<fix-the-artifact-paths>
Write every artifact but the spec under `orchestration_log/recon/${DATE}/` in the project root — the directory holding `.git` where the session started — where `${DATE}` is the UTC date as `YYYY-MM-DD`; never write one elsewhere.

Fix the paths beneath that directory: the plan at `plans/${slug}.md`, with `${slug}` the task name in lowercase hyphenated words; each prompt file at `prompts/${agent}-${unit}.md`, with `${agent}` the launched agent's name for a defined agent — `spec-capturer`, `implementer`, `spec-reviewer`, `code-quality-reviewer` — or one noun the orchestrator gives the task for any other launch, `${unit}` the name the plan gives the unit or `all` for a whole-task launch, and `-2`, `-3` inserted before `.md` on a repeated path; each spec verdict at `reviews/spec-${branch}-${timestamp}.md` and each quality report at `reviews/quality-${branch}-${timestamp}.md`, with `${branch}` the branch of the unit's worktree — the checkout the platform creates for an `implementer` run — with `/` replaced by `-` and `${timestamp}` UTC `HHMMSS`; each report of an agent other than the spec-capturer and the implementer, who report in their final messages, and the two reviewers, who report in their verdict and report files, at `reports/${agent}-${unit}.md`, ending with `Result: PASS` or `Result: FAIL` and the units it names, the executor's report of the `lite-cycle` skill excepted; each prescription — a brief the `prescriber` of dev-cycle-lite writes for an `executor` — at `briefs/prescriber-${unit}.md`; the status file at `dev-status.md`; never let an agent choose a path.

Launch every agent other than the four defined ones through the `Agent` tool with no agent definition, on sonnet, from a prompt file stating its task, its inputs, and its report path; never launch one from the conversation alone.

Take the implementer's worktree from the `Worktree:` line of its report; never take a worktree path from anywhere else.

Take each verdict from its file — the `Verdict:` line of a spec verdict, the `Ready to merge:` line of a quality report, read from the path set at launch once the notification — the message the platform sends when a background agent ends — arrives; never take a verdict from a final message.
</fix-the-artifact-paths>

<write-the-status-file>
Write the status file after each state change with one row per unit and these columns: unit; state, one of `planned`, `implementing` (set again by every continuation), `in review`, `passed`, `integrated`, `returned` (sent back to the user through `plan-the-units`); implementer id; spec-reviewer id; code-quality-reviewer id; review-fix cycle count; note — then the integration branch — the branch every unit's work merges into — the excluded test markers — the markers that keep tests out of the default test run — each integration check — the whole-suite run, the compatibility check, the cross-cutting review — as `pending`, `passed`, or `failed`, and the blockers; never hold the state in the conversation alone.
</write-the-status-file>

<capture-the-spec>
Launch the `spec-capturer` agent when the request names no spec file — a specification file the user names — as a background `Agent` launch — telling the user in one line to open the running agent and answer its questions there — or, when the user asks for it, as a sibling session the user starts in the project root with `claude --agent dev-cycle:spec-capturer` and hands the request, the project root, and the spec path to; never interview the user in the orchestrator's own context.

Pass it the request text, the project root, and the spec path — the project root joined with `docs/specs/${slug}.md`, or with `${dir}/${slug}.md` when the project already holds a spec directory `${dir}`; never pass it a plan or a unit.

Relaunch the capturer with the items it names when its final message begins `Dispatch malformed:`; never relaunch it without them.

Take `Spec: <path>` as the capturer's accepted return — its final message, or the `SendMessage` the sibling session sends to this session; never act on an end of the capturer's run that returns another text.

Leave an end of the capturer's run that returns another text to the user, who is answering inside the capturer, and wait for the capturer's next notification; never message the capturer.

Read the spec file whole before planning; never plan from the request while this task's spec file exists.
</capture-the-spec>

<plan-the-units>
Decompose the spec yourself into units — each one function or endpoint callers outside the unit will use, which the implementer names and designs, and the zero to three files behind it, not counting the declaring file or the tests, independently testable, two to ten minutes of implementer work — and write the plan to its path; never decompose from the request.

Decide every dispatch — what launches, when, on which tier — by wall-time and token spend; never by the order of the scope.

Cut dependencies between units while decomposing — give shared code its own unit launched first, or let two units duplicate it and the integration agent dedupe; never leave a dependency a cut could remove.

Name each unit in the plan in lowercase hyphenated words; never leave one unnamed.

Assign each unit, in the plan, its requirements — the spec's sentences it implements — and its gates — the commands, each with the exact output it requires, that prove the unit done, the whole-suite run with the excluded test markers included among them; never fix an interface name or a signature in the plan.

List in the plan, for each unit, the files it reads and the files it may touch — its scope boundary; never leave either list out.

Treat two units that may touch one file as the integration agent's merge; never serialize them for it.

Order the units by data dependency alone — a unit after the units whose code it calls; never by the scope's order.

Assign each unit a tier by its risk — sonnet by default, opus where the unit's failure voids other units or its reasoning runs deep; never assign a unit to haiku.

Create the integration branch from the current branch with `git switch -c integration/${slug}` in the project root, and leave it checked out there; never create it elsewhere.

Name the integration branch once in the status file; never let two units name different integration branches.

Launch an agent after planning to list every excluded test marker; never launch the first implementer before the status file names the excluded set.

Name the excluded set in the status file; never leave it unnamed there.
</plan-the-units>

<launch-the-implementer>
Launch an implementer after the plan is on disk; never before.

Write each implementer's prompt to its prompt file with seven parts — the unit's requirements and gates copied from the plan, the integration branch, every input path — a file the plan lists as read by the unit — relative to the project root, which the implementer resolves inside its worktree, the scope boundary from the plan, the excluded test markers, two or three sentences of scene-setting on where the unit sits in the system, and the instruction to end with the report `implementer` defines; never launch from a prompt that exists in the conversation alone.

Launch `implementer` in the background with its prompt file's text as the launch text; never launch it in the foreground.

Launch `implementer` on the tier the plan assigns the unit; never launch it on haiku.

Launch, in one turn, every unit whose dependencies are integrated; never hold one for a later turn.

Run independent units as parallel lanes; never as one sequential lane through the scope.

Rely on the agent's own frontmatter for the worktree; never create, enter, or name a worktree for it.

Run `pwd` before every shell command and every launch; never skip the check.

Return to the project root with `cd` when `pwd` shows another directory; never run a command or a launch from a drifted directory.
</launch-the-implementer>

<derive-branch-and-shas-from-git>
Derive after each implementer report, with `W` the reported worktree and `I` the integration branch: the branch with `git -C "$W" branch --show-current`, the head with `git -C "$W" rev-parse HEAD`, and the base with `git -C "$W" merge-base HEAD "$I"`; never parse a branch or a SHA — a commit's hash — from return text.

Treat a reported worktree path that is not a directory containing `.git` as a `BLOCKED` report; never treat one as a worktree.
</derive-branch-and-shas-from-git>

<route-on-status>
Read the `Status:` line of the implementer's report and route on it alone: `DONE` launches the spec review; `DONE_WITH_CONCERNS` launches an agent to classify each concern as correctness — the code may be wrong, scope — the unit touched more or less than its contract, or observation — a fact needing no change, then continues the implementer for a correctness or scope concern and launches the spec review for observations alone; `NEEDS_CONTEXT` continues the implementer with the missing files and facts, fetched by a launched agent, and the missing decision, taken by the orchestrator, or from the user when the spec leaves it open; `BLOCKED` launches a diagnosis agent that ends with one of the six causes below; a missing or other value continues the implementer with the instruction to end with its report; never route on another line.

Continue the same implementer through `SendMessage` with the delta alone — the path of the file holding the findings, the fix scope, the sentence `do not alter code that passed review`, and the changed gates — when its approach is sound; never resend the requirements it already holds.

Recreate a worktree whose reported path is gone — `git worktree add <path> <branch>` from the project root, the branch surviving in the shared `.git` — and continue the implementer with the recreated path; never launch fresh for a missing worktree.

Launch a fresh implementer when the diagnosis agent names the approach wrong, the model tier changes, or the scope changes so far that prior work is void; never continue an agent through a change `SendMessage` cannot carry.

Route a diagnosed block: a wrong approach launches fresh with a corrected brief; a missing dependency continues the implementer with the dependency; insufficient reasoning launches fresh on a stronger model; a unit too large is rewritten by the orchestrator as sub-units in the plan and the status file, each launched fresh; a plan defect returns to `plan-the-units` and the user; an unknown cause runs `launch-the-debugging-round` and continues the implementer with the path of the fix the round proposes; never relaunch a blocked implementer with unchanged inputs.

Return a unit to `launch-the-spec-review` after every implementer continuation that changes code, and re-integrate it after both reviews pass; never leave a continued unit's merge standing unreviewed.
</route-on-status>

<launch-the-spec-review>
Launch the spec review on the notification that ends an implementer's run with `Status: DONE`, or with `DONE_WITH_CONCERNS` classified as observations alone; never wait for a hook — a command the platform runs at a lifecycle event — to demand it.

Launch `spec-reviewer` with the unit's requirements — the spec's sentences the plan assigns it — and its gates, the implementer's report, the worktree path, the branch, the base SHA, and the verdict path to write; never launch it without one of the six.

Relaunch a reviewer with the items it names when its final message begins `Dispatch malformed:`; never relaunch one without the items it names.

Continue the implementer with the verdict file's path on `FAIL`; never inline the findings.

Continue the same spec-reviewer after the fix with the new diff range `BASE..new HEAD`, the sentence `re-review the delta and confirm the passing criteria still hold`, and a verdict path with a fresh timestamp; never launch a fresh reviewer for a re-review while the first's agent id is held.
</launch-the-spec-review>

<launch-the-quality-review>
Launch `code-quality-reviewer` after a spec review ending `Verdict: PASS`, with the unit's requirements — the spec's sentences the plan assigns it — and its gates, the worktree path, the branch, the range `BASE..HEAD`, the spec verdict path, and the report path to write; never launch it without one of the six.

Read the `Ready to merge:` line and the finding headings from the report file; never read the findings' bodies.

Continue the implementer with the report file's path, naming `Critical` and `Important` as the findings to fix, on `With fixes` or `No`; never inline the findings.

Continue the same `code-quality-reviewer` after the fix with the new range, the fresh spec verdict path, and a fresh report path; never launch a fresh reviewer for a re-review while the first's agent id is held.

Count every finding a reviewer writes in scope, whenever the code it names was introduced, fixing `Critical` and `Important` and noting the rest in the status file; never dismiss a finding as pre-existing.
</launch-the-quality-review>

<integrate-on-pass>
Launch the integration agent of `integrate-the-units` for a unit on `Verdict: PASS` and `Ready to merge: Yes`; never on other values.

Write the outcome — integrated, or implementer continued — to the status file in the same turn; never carry it in the conversation alone.

Launch a caller after its callee has passed both reviews and been integrated; never launch a caller before that.
</integrate-on-pass>

<stop-the-review-fix-cycles-at-three>
Count the review-fix cycles — a `FAIL` verdict or an open finding followed by an implementer continuation — per unit; never leave the count out of the status file.

Stop when the third cycle's re-review fails; never enter a fourth with the same model, the same requirements, and the same decomposition.

Run `launch-the-debugging-round` before any structural change; never change structure on a guess.

Launch a diagnosis agent with the round's finding to name one structural change — launch fresh on a stronger model, return the unit's requirements to `plan-the-units` for the user to clarify, or split the unit; never name the change in the orchestrator's context.

Make the named change before the next cycle; never enter the next cycle unchanged.
</stop-the-review-fix-cycles-at-three>

<launch-the-debugging-round>
Launch agents under the `systematic-debugging` skill when a failure has no clear cause — tests fail for an unclear reason, behavior contradicts the requirements while the code looks right, a fix breaks something elsewhere, or a third review-fix cycle failed — before any structural change; never let an implementer guess at a fix.

Launch one agent to list up to three hypotheses; never list them in the orchestrator's context.

Launch one agent per hypothesis in parallel, each ending with its evidence and, where it finds the cause, a proposed minimal fix; never let one agent carry two hypotheses.

Compare the investigators' evidence and take the fix of the one that finds the cause; never take a fix without evidence.

Surface to the user, with the evidence gathered, when three hypotheses fail; never launch a fourth hypothesis without new evidence.
</launch-the-debugging-round>

<integrate-the-units>
Launch an integration agent for each unit that passed both reviews, one unit at a time, in the project root checkout with the integration branch checked out, to merge the unit's worktree branch into the integration branch, run the whole test suite with every excluded marker included, and report the result; never merge in the orchestrator's own context.

Launch, after every unit is integrated, one agent to run the whole suite and one to check interface compatibility between units — types, signatures, data contracts — and end-to-end behavior against the original request; never call the task done on unit tests alone.

Launch, in the same turn, a cross-cutting review of the whole change with one agent per concern — spec fidelity, data flow integrity, simplicity, duplicated knowledge, unused features; never review unit by unit.

Continue the implementer of each unit an agent ending `Result: FAIL` names with the path of that agent's report, as `route-on-status` prescribes for a continuation; never fix an integration failure in the orchestrator's context.

Launch the whole-suite agent again after every continuation this tag or `classify-the-tests` starts; never count an earlier pass for a changed branch.
</integrate-the-units>

<review-the-integrated-branch>
Launch `spec-reviewer` over the whole integrated diff — the project root checkout as the worktree path, the integration branch, the branch point as the base SHA — with every requirement of the spec, after the whole-suite agent reports a pass; never call the task done without this review.

Launch `code-quality-reviewer` on its `Verdict: PASS` over the same range; never skip it.

Launch an implementer on `all`, which merges the integration branch first, with the verdict path, the report path, and every finding the status file noted as deferred from the unit cycles; never leave a noted finding standing.

Re-run both reviews on its result and integrate it as `integrate-the-units` prescribes; never integrate it unreviewed.
</review-the-integrated-branch>

<classify-the-tests>
Launch an agent, after the whole-suite agent reports a pass, to classify each test the units added or changed as `valuable` — asserts a behavior that could regress, `smoke` — proves the code runs, or `tautological` — asserts a default equals its own copy or a library's guarantee, and each contract behavior with no test as `missing`; never skip a test or a behavior.

Continue the owning unit's implementer to delete each `tautological` test and write each `missing` one; never leave either class standing.

Remove each unit's worktree with `git worktree remove <path>` after the test classification and every integration check have passed; never remove one while a continuation of its implementer may follow.

Report the integration branch and the status file path to the user once every worktree is removed; never merge the integration branch.
</classify-the-tests>
