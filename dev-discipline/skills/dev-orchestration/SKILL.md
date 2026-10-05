---
name: dev-orchestration
description: >
  Drive the plan, implement, review, fix, and integrate loop over software work through the implementer, spec-reviewer, and code-quality-reviewer agents, as an extension of agentic-delegation.
  "implement a feature end-to-end", "execute an implementation plan", "build this with agents", "orchestrate development", "run the dev loop",
  "implement using subagents", "dispatch implementers", "coordinate implementation and review", or any coding task an orchestrator delegates.
---

<read-the-parent-first>
Read the `agentic-delegation` skill whole before any step below; never run this skill without it.

Treat every action verb in the request — implement, build, fix, refactor, test, review, plan — as an order to launch agents; never write, read, run, or debug code in the orchestrator's own context.
</read-the-parent-first>

<fix-the-artifact-paths>
Write every artifact under `orchestration_log/recon/${DATE}/`, where `${DATE}` is the UTC date as `YYYY-MM-DD`; never write one elsewhere.

Fix the paths beneath that directory: the plan at `plans/${slug}.md`, with `${slug}` the task name in lowercase hyphenated words; each launch prompt at `prompts/${agent}-${unit}.md`, with `${agent}` the launched agent's role name, `${unit}` the name the plan gives the unit — one outermost interface and the one to three files behind it — or `all` for a whole-task launch, and `-2`, `-3` appended to a repeated path; each spec verdict at `reviews/spec-${branch}-${timestamp}.md` and each quality report at `reviews/quality-${branch}-${timestamp}.md`, with `${branch}` the unit's worktree branch with `/` replaced by `-` and `${timestamp}` UTC `HHMMSS`; the status file at `dev-status.md`; never let an agent choose a path.

Take the implementer's worktree — the checkout the platform creates for an `implementer` run, on its own branch — from the `Worktree:` line of its report; never take a worktree path from anywhere else.

Take each verdict from its file — the `Verdict:` line of a spec verdict, the `Ready to merge:` line of a quality report; never take a verdict from an agent's return text.
</fix-the-artifact-paths>

<plan-the-units>
Launch an agent under `defensive-planning` to decompose the task into units — each independently testable, two to ten minutes of implementer work — and write the plan to its path; never launch an implementer without a plan on disk.

Require the plan to fix each unit's outermost contract and gates and to leave every signature beneath the contract to the implementer, who designs it through `tdd`; never accept a plan that fixes an inner signature.

Create the integration branch — the branch every unit's work merges into — from the current branch with `git branch`, and name it once in the status file; never let two units name different integration branches.

Launch units with no dependency between them in parallel; never launch a caller before its callee has passed both reviews and been integrated.

Launch an agent after planning and before the first implementer launch to list every test marker that excludes tests from the default run, and name the excluded set in the status file; never report `all tests pass` while a marker hides tests from the run.
</plan-the-units>

<launch-the-implementer>
Write each implementer's prompt to its prompt file with six parts — the unit's contract and gates copied from the plan, the integration branch, every input path relative to the repository root, the scope boundary, two or three sentences of scene-setting on where the unit sits in the system, and the instruction to end with the report `implementer` defines; never launch from a prompt that exists in the conversation alone.

Launch `implementer` in the background on sonnet; never launch it in the foreground or on haiku.

Rely on the agent's own frontmatter for the worktree; never create, enter, or name a worktree for it.

Run `pwd` before every shell command and every launch, and `cd` back to the project root when it shows another directory; never run a command or a launch from a drifted directory.
</launch-the-implementer>

<derive-branch-and-shas-from-git>
Derive after each implementer report, with `W` the reported worktree and `I` the integration branch: the branch with `git -C "$W" branch --show-current`, the head with `git -C "$W" rev-parse HEAD`, and the base with `git -C "$W" merge-base HEAD "$I"`; never parse a branch or a SHA from agent text.

Treat a reported worktree path that is not a directory containing `.git` as a `BLOCKED` report; never query git in a path the implementer did not report.
</derive-branch-and-shas-from-git>

<route-on-status>
Read the `Status:` line of the implementer's report and route on it alone: `DONE` launches the spec review; `DONE_WITH_CONCERNS` launches an agent to classify each concern as correctness, scope, or observation, then continues the implementer for a correctness or scope concern and launches the spec review for observations alone; `NEEDS_CONTEXT` continues the implementer with the missing files and facts, fetched by a launched agent, and the missing decision, taken by the orchestrator or from the user when the decision is the user's; `BLOCKED` launches a diagnosis agent; never route on another line.

Continue the same implementer through `SendMessage` with the delta alone — the path of the file holding the findings, the fix scope, the sentence `do not alter code that passed review`, and a changed verification command — when its approach is sound and its worktree stands; never resend the contract it already holds.

Launch a fresh implementer when the approach is wrong, the model tier changes, or the scope changes so far that prior work is void; never continue an agent through a change `SendMessage` cannot carry.

Route a diagnosed block: a missing dependency continues the implementer with the dependency; insufficient reasoning launches fresh on a stronger model; a unit too large launches fresh on decomposed sub-units; a plan defect returns to `plan-the-units` and the user; an unknown cause launches investigation agents, one hypothesis each, and continues the one that finds the cause with `propose a minimal fix`; never relaunch a blocked implementer with unchanged inputs.
</route-on-status>

<launch-the-spec-review>
Launch `spec-reviewer` with the unit's contract, the implementer's report, the worktree path, the branch, the base SHA, and the verdict path to write; never launch it without one of the six.

Read the `Verdict:` line from the verdict file once the notification arrives; never read the rest of the file.

Continue the implementer with the verdict file's path on `FAIL`; never inline the findings.

Continue the same spec-reviewer after the fix with the new diff range, the sentence `re-review the delta and confirm the passing criteria still hold`, and a verdict path with a fresh timestamp; never launch a fresh reviewer for a re-review while the first stands.
</launch-the-spec-review>

<launch-the-quality-review>
Launch `code-quality-reviewer` after every spec review, on `PASS` and on `FAIL` alike, with the unit's contract, the worktree path, the branch, the range `BASE..HEAD`, the spec verdict path, and the report path to write; never launch it without one of the six.

Read the `Ready to merge:` line from the report file once the notification arrives; never read the findings.

Treat the report that follows a `FAIL` spec verdict as closed by the implementer continuation the spec review already started; never start a second continuation from it.

Continue the implementer with the report file's path, naming `Critical` and `Important` as the findings to fix, on `With fixes` or `No` after a `PASS` spec verdict; never inline the findings.

Continue the same `code-quality-reviewer` after the fix with the new range and a fresh report path; never launch a fresh reviewer for a re-review while the first stands.

Own every finding a reviewer writes, whenever the code it names was introduced; never dismiss a finding as pre-existing.
</launch-the-quality-review>

<decide-the-merge>
Integrate the unit on `Ready to merge: Yes`; never integrate on another value.

Write the decision — integrate, or continue the implementer — to the status file in the same turn; never carry it in the conversation alone.
</decide-the-merge>

<stop-the-review-fix-cycles-at-three>
Count the review-fix cycles — a `FAIL` verdict or an open finding followed by an implementer continuation — per unit; never leave the count out of the status file.

Stop at the third failed cycle; never enter a fourth with the same model, the same contract, and the same decomposition.

Change one structural thing before the next cycle — launch fresh on a stronger model, return the unit's contract to `plan-the-units` for the user to clarify, or split the unit; never retry on hope.
</stop-the-review-fix-cycles-at-three>

<launch-the-debugging-round>
Launch agents under `systematic-debugging` when a failure has no clear cause — tests fail for an unclear reason, behavior contradicts the contract while the code looks right, a fix breaks something elsewhere, or a third review-fix cycle failed — before any structural change; never let an implementer guess at a fix.

Launch one agent per hypothesis, three at most, in parallel, and compare their evidence; never let one agent carry two hypotheses.

Surface to the user, with the evidence gathered, when three hypotheses fail; never launch a fourth hypothesis without new evidence.
</launch-the-debugging-round>

<integrate-the-units>
Launch an integration agent for each unit that passed both reviews, one unit at a time, in the project root checkout with the integration branch checked out, to merge the unit's worktree branch into the integration branch, run the whole test suite, and report the result; never merge in the orchestrator's own context.

Launch, after every unit is integrated, one agent to run the whole suite and one to check interface compatibility between units — types, signatures, data contracts — and end-to-end behavior against the original request; never call the task done on unit tests alone.

Launch a cross-cutting review of the whole change with one agent per concern — spec fidelity, data flow integrity, simplicity, duplicated knowledge and unused features; never review module by module.

Continue the implementer of each unit a failing agent names with the path of that agent's report, as `route-on-status` prescribes for a continuation; never fix an integration failure in the orchestrator's context.

Remove each unit's worktree with `git worktree remove <path>` after every check in this tag has passed; never remove one while a continuation of its implementer may follow.
</integrate-the-units>

<classify-the-tests>
Launch an agent, after the whole-suite agent in `integrate-the-units` reports a pass, to classify each test as `valuable` — asserts a behavior that could regress, `smoke` — proves the code runs, `tautological` — asserts a default equals its own copy or a library's guarantee, or `missing` — a behavior with no test; never skip a test.

Continue the owning unit's implementer to delete each `tautological` test and write each `missing` one; never leave either class standing.
</classify-the-tests>

<record-the-status>
Write the status file after each state change with one row per unit — unit, state, implementer id, spec-reviewer id, code-quality-reviewer id, review-fix cycle count, note — the integration branch, the excluded test markers, the integration checks pending, and the blockers; never hold the state in the conversation alone.

Launch each review stage on the notification that ends the stage before it; never wait for a hook to demand it.

This plugin's hooks record each `implementer`, `spec-reviewer`, and `code-quality-reviewer` stop under the plugin's data directory and continue the orchestrator's turn with the next stage's mandate while that stage has not launched; the status file stays the orchestrator's own.
</record-the-status>
