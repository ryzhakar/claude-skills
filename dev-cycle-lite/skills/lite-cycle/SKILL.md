---
name: lite-cycle
description: >
  Run the dev-cycle loop over one spec at the lowest cost tier — an opus prescriber writes a prescription per unit, disposable haiku executors follow it literally, and the suborchestrator running this skill reviews each unit itself and integrates.
  "run the lite cycle", "implement this cheaply", "implement with haiku executors", "prescribe and execute", or any dev-cycle run the user marks lite in the dispatch.
---

<read-the-parents-first>
Read the `dev-cycle` skill and the `agentic-delegation` skill whole before any step below; never run this skill without both.

Follow every rule of the `dev-cycle` skill from its `plan-the-units` stage on, and of the `agentic-delegation` skill, except where a sentence below replaces it — tiers, discarded executors, reviews done by this agent, this agent as a second launch loop; never re-decide a rule they already fix.
</read-the-parents-first>

<dispatch-the-suborchestrator>
Launch, when this skill runs in the main session rather than in `suborchestrator`, the `suborchestrator` agent in the background with the absolute spec path, the project root, the artifact directory — `orchestration_log/recon/${DATE}/` under the project root — and the integration branch or `none`; never run the stages below in the main session.

Read its report's `Status:`, `Integration branch:`, `Units integrated:`, `Units returned:`, and `Status file:` lines; never read another line.

Return each unit on `Units returned:` to the user with its prescription and verdict paths; never re-run it in the main session.
</dispatch-the-suborchestrator>

<take-the-spec>
Take from the dispatch — the message that launched this run — the absolute spec path, the project root, the artifact directory, and the integration branch or `none`; never take one from elsewhere.

Leave spec capture to the orchestrator above; never run the spec-capturer from this skill.

Plan the units as the `dev-cycle` skill prescribes; never skip a step of its planning.

Assign every unit to haiku — the lowest model tier; never assign a unit to another tier.

Write the status file at the path the `dev-cycle` skill fixes after planning and after each launch, review, integration, and return; never hold the state in the conversation alone.
</take-the-spec>

<prescribe-each-unit>
Launch `prescriber` once per unit, in the background, on opus — the strongest model tier — with the spec path, the unit's contract and gates copied from the plan, the unit's input paths, and the prescription path — `briefs/prescriber-${unit}.md` under the artifact directory the `dev-cycle` skill fixes, `${unit}` the unit's name in the plan; never launch it with another item.

Hold the executor launch until the prescription is on disk; never launch an executor without one.
</prescribe-each-unit>

<launch-the-executor>
Launch `executor` in the background, on haiku, with the prescription path and the integration branch as its whole brief; never add a third item.

Discard an executor after its report; never continue one through `SendMessage`.

Write an executor report carrying `Status: BLOCKED` to `reports/executor-${unit}.md` under the artifact directory; never leave one in the conversation alone.

Relaunch a prescriber or an executor with the items it names when its final message begins `Dispatch malformed:`; never relaunch one without them.
</launch-the-executor>

<review-each-unit-yourself>
Invoke the `dev-discipline:tdd` skill with the `Skill` tool before the first review; never review without its text in this context.

Review each unit whose executor report carries `Status: DONE` yourself — one review being the spec review by the `dev-cycle` plugin's `spec-reviewer` procedure and the quality review by its `code-quality-reviewer` procedure together; never launch a reviewer.

Write one verdict file and one quality report file per review at the paths the `dev-cycle` skill fixes; never leave either unwritten.

Read in full each file changed against the integration branch in the executor's worktree — the path on the `Worktree:` line of its report — before recording a requirement as met or unmet in the verdict file; never record from the executor's report.
</review-each-unit-yourself>

<integrate-each-passed-unit>
Integrate a unit on `Verdict: PASS` in the verdict file and `Ready to merge: Yes` in the quality report file, as the `dev-cycle` skill's `integrate-the-units` prescribes; never integrate on other values.
</integrate-each-passed-unit>

<re-prescribe-after-a-failed-review>
Launch `prescriber` again after a `BLOCKED` executor report or after any review other than `Verdict: PASS` with `Ready to merge: Yes`, with the spec path, the unit's contract, gates, and input paths from its first launch, the failed prescription's path, and the findings path — the `BLOCKED` report's file, the verdict file after `Verdict: FAIL`, or the quality report file after a `Ready to merge:` other than `Yes`; never launch it without the findings path.

Pass it `briefs/prescriber-${unit}-2.md`, then `-3.md`, then `-4.md`, as the prescription path; never pass an earlier path again.

Re-prescribe and launch a fresh executor wherever the `dev-cycle` skill continues an implementer — an integration failure, a test classification; never continue an executor.

Launch a fresh executor with the correction prescription's path and the integration branch, from which it starts and redoes the whole unit; never hand a findings file to an executor.
</re-prescribe-after-a-failed-review>

<escalate-on-the-third-failure>
Escalate a unit at its third failed review-fix cycle, as the `dev-cycle` skill counts them, by stopping work on it and listing it on the `Units returned:` line of the final report with its last prescription path and last verdict path; never run a fourth cycle.

Continue the other units after an escalation; never stop the run for one returned unit.
</escalate-on-the-third-failure>

<report-to-the-orchestrator>
End with a report of these lines: `Status:` — `DONE` when `Units returned:` reads `none`, `BLOCKED` otherwise; `Integration branch:` — its name; `Units integrated:` — their names, or `none`; `Units returned:` — each name with its last prescription path and last verdict path, or `none`; `Status file:` — its path; never omit a line.
</report-to-the-orchestrator>
