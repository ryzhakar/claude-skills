---
name: dev-orchestration
description: >
  Drive the plan, implement, review, fix, and integrate loop over software work through the implementer, spec-reviewer, and code-quality-reviewer agents, as an extension of agentic-delegation.
  "implement a feature end-to-end", "execute an implementation plan", "build this with agents", "orchestrate development", "run the dev loop",
  "implement using subagents", "dispatch implementers", "coordinate implementation and review", or any coding task an orchestrator delegates.
---

<read-the-parent-first>
Read the `agentic-delegation` skill whole before any step below; never run this skill without it, since the decomposition, the prompt anatomy, the model tiers, the background launch, the continuation of an agent, and the verification of results all live there and nothing below restates them.

Treat every action verb in the request — implement, build, fix, refactor, test, review, plan — as an order to launch agents; never write, read, run, or debug code in the orchestrator's own context.
</read-the-parent-first>

<fix-the-artifact-paths>
Write every artifact under `orchestration_log/recon/${DATE}/`, where `${DATE}` is the UTC date as `YYYY-MM-DD`: the plan at `plans/${slug}.md` with `${slug}` the task name in lowercase hyphenated words; each launch prompt at `prompts/${agent}-${unit}.md`; each spec verdict at `reviews/spec-${branch}-${timestamp}.md` and each quality report at `reviews/quality-${branch}-${timestamp}.md`, where `${branch}` is the unit's worktree branch with `/` replaced by `-` and `${timestamp}` is UTC `HHMMSS`; the status file at `dev-status.md`; never write one elsewhere and never let an agent choose a path.

Take the implementer's worktree — the checkout the platform creates for an `implementer` run, on its own branch — from the `Worktree:` line of its report, and confirm the directory exists; never take a worktree path from anywhere else.

Take each verdict from its file, from the `Verdict:` line of a spec verdict and the `Ready to merge:` line of a quality report; never take a verdict from an agent's return text, which names the file and nothing more.
</fix-the-artifact-paths>

<plan-the-units>
Decompose the task into units — one outermost interface each, one to three files, independently testable, two to ten minutes of implementer work — and write the plan through `defensive-planning`; never launch an implementer without a plan on disk.

Fix in the plan each unit's outermost contract and gates, and leave every signature beneath the contract to the implementer, who designs it through `tdd`; never fix inner signatures in the plan.

Order the units so each unit's contract exists before a unit that calls it, and launch units with no dependency between them in parallel; never launch a caller before its callee has passed review.

Name the integration branch — the branch every unit's work merges into — once in the status file; never let two units name different integration branches.
</plan-the-units>

<launch-the-implementer>
Write each implementer's prompt to its prompt file with six parts — the unit's contract and gates copied from the plan, the integration branch, every input path relative to the repository root, the scope boundary, two or three sentences of scene-setting on where the unit sits in the system, and the instruction to end with the report `implementer` defines; never launch from a prompt that exists in the conversation alone.

Launch `implementer` in the background on sonnet; never launch it in the foreground and never launch it on haiku.

Rely on the agent's own frontmatter for the worktree; never create, enter, or name a worktree for it.

Run `pwd` before every shell command and every launch, and `cd` back to the project root when it shows another directory; never run a command or launch from a drifted directory.
</launch-the-implementer>

<derive-branch-and-shas-from-git>
Derive after each implementer report, with `W` the reported worktree and `I` the integration branch: the branch with `git -C "$W" branch --show-current`, the head with `git -C "$W" rev-parse HEAD`, and the base with `git -C "$W" merge-base HEAD "$I"`; never parse a branch or a SHA from agent text.

Stop on a worktree path that is not a directory containing `.git` and treat the report as `BLOCKED`; never query git in a path the implementer did not report.
</derive-branch-and-shas-from-git>

<route-on-status>
Read the `Status:` line of the implementer's report and route: `DONE` launches the spec review; `DONE_WITH_CONCERNS` launches an agent to classify each concern as correctness, scope, or observation, continues the implementer for a correctness or scope concern, and launches the spec review for observations alone; `NEEDS_CONTEXT` continues the implementer with the missing files, facts, or decision inlined; `BLOCKED` launches a diagnosis agent; never route on any other line of the report.

Continue the same implementer through `SendMessage` with the delta alone — the findings with `file:line`, the fix scope, the sentence `do not alter code that passed review`, and a changed verification command — when its approach is sound and its worktree stands; never resend the contract it already holds.

Launch a fresh implementer when the approach is wrong, the model tier changes, or the scope changes so far that prior work is void; never continue an agent through a change `SendMessage` cannot carry, such as a tier.

Route a diagnosed block: a missing dependency continues the implementer with the dependency; insufficient reasoning launches fresh on a stronger model; a task too large launches fresh on decomposed sub-units; a plan defect returns to `plan-the-units` and the user; an unknown cause launches investigation agents, one hypothesis each, and continues the one that finds the cause with `propose a minimal fix`; never relaunch a blocked implementer with unchanged inputs.
</route-on-status>

<launch-the-spec-review>
Launch `spec-reviewer` with the unit's contract, the worktree path, the branch, the base SHA, and the verdict path to write; never launch it with the implementer's report as evidence.

Read the `Verdict:` line from the verdict file once the notification arrives; never read the rest of the file into the orchestrator's context.

Continue the implementer with the verdict file's findings on `FAIL`, then continue the same spec-reviewer with the new diff range, the sentence `re-review the delta and confirm the passing criteria still hold`, and a verdict path with a fresh timestamp; never launch a fresh reviewer for a re-review while the first stands.
</launch-the-spec-review>

<launch-the-quality-review>
Launch `code-quality-reviewer` after every spec review, with the worktree path, the branch, the range `BASE..HEAD`, the spec verdict path, and the report path to write; never skip it on a `FAIL`, since the reviewer reads the verdict and returns at once on `FAIL`.

Read the `Ready to merge:` line from the report file once the notification arrives; never read the findings into the orchestrator's context.

Continue the implementer with the report file's `Critical` and `Important` findings on `With fixes` or `No`, then continue the same quality reviewer with the new range and a fresh report path; never merge on `With fixes` with a finding open.

Own every finding a reviewer writes, whenever the code it names was introduced; never dismiss a finding as pre-existing.
</launch-the-quality-review>

<decide-the-merge>
Decide on `Ready to merge: Yes` with a `PASS` spec verdict: integrate the unit; on open findings: continue the implementer with the findings as `route-on-status` prescribes; on a finding the plan cannot resolve: write the finding to the status file and surface it to the user; never leave a quality report without one of the three.

Write the decision to the status file in the same turn; never carry it in the conversation alone.
</decide-the-merge>

<cap-the-fix-loop>
Count the review-fix cycles — a `FAIL` or an open finding followed by an implementer continuation — per unit, and stop at three; never enter a fourth cycle with the same model, the same contract, and the same decomposition.

Change one structural thing before the next cycle: launch fresh on a stronger model, return the unit's contract to `plan-the-units` for the user to clarify, or split the unit; never retry on hope.
</cap-the-fix-loop>

<escalate-to-debugging>
Launch agents under `systematic-debugging` when a failure has no clear cause — tests fail for an unclear reason, behavior contradicts the contract while the code looks right, a fix breaks something elsewhere, or a third fix attempt failed; never let an implementer guess at a fix.

Launch one agent per hypothesis, three at most, in parallel, and compare their evidence; never let one agent carry two hypotheses.

Surface to the user, with the evidence gathered, when three hypotheses fail; never launch a fourth round without new evidence.
</escalate-to-debugging>

<integrate-the-units>
Launch an integration agent for each unit that passed both reviews, to merge its worktree branch into the integration branch, run the whole test suite, and report the result; never merge in the orchestrator's own context.

Remove the unit's worktree with `git worktree remove <path>` after the integration agent reports success and no continuation of that implementer remains; never remove it while a fix cycle may continue the implementer.

Launch, after every unit is integrated, one agent to run the whole suite and one to check interface compatibility between units — types, signatures, data contracts — and end-to-end behavior against the original request; never call the task done on unit tests alone.

Launch a cross-cutting review of the whole change with one agent per concern — spec fidelity, data flow integrity, simplicity, duplicated knowledge and unused features; never review module by module.

Return a failing unit to `route-on-status`; never fix an integration failure in the orchestrator's context.
</integrate-the-units>

<audit-the-tests>
Launch an agent before the first verification to list every test marker that excludes tests from the default run, and name the excluded set in the status file; never report `all tests pass` while a marker hides tests from the run.

Launch an agent after the suite stabilizes to classify each test as `valuable` — asserts a behavior that could regress, `smoke` — proves the code runs, `tautological` — asserts a default equals its own copy or a library's guarantee, or `missing` — a behavior with no test; never keep a tautological test and never leave a `missing` row unaddressed.
</audit-the-tests>

<record-the-status>
Write the status file after each state change with one row per unit — unit, state, implementer id, spec-reviewer id, quality-reviewer id, note — the integration branch, the integration checks pending, and the blockers; never hold the state in the conversation alone.

Rely on this plugin's hooks, which record each `implementer`, `spec-reviewer`, and `code-quality-reviewer` stop and continue the orchestrator's turn with the next stage's mandate while that stage has not launched; never treat a mandate from a hook as the driver, since the orchestrator launches each stage on the notification itself.
</record-the-status>
