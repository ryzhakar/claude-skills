---
name: calibrate-judge
description: >
  Measure a candidate judge against reference raters on a blind sample of the retest's open replies, with acceptance set before any rating, and accept or reject the attempt.
  Use when the user says "calibrate the judge", "write the judge brief", "judge calibrate", "rate the sample", or "calibration rejected".
  Use when `r1` replies are collected and the series holds no `6-judge/calibration.yaml`.
---

<cover-the-calibration-stage>
Follow this skill after `revision collect r1` passes and before `revision blind r1`, in the neutral session from the series folder; never run it elsewhere.

Calibrate once per series; never copy a calibration, anchors, or a brief's acceptance from another series.

`6-judge/calibration.yaml` records the accepted brief's hash; never treat a calibration as valid for any other brief.
</cover-the-calibration-stage>

<write-the-brief-and-plan>
Start `6-judge/brief.md` from the template whose absolute path stage one prints when the brief is missing; never write one from memory.

Keep `{SOURCE}`, `{DEMANDS}`, `{PACKET}`, and `{OUT}` once each and the literal `manifesto:manifesto-oath`; never name a condition, the reader, the reader's model ID, the series folder, or the words `empty`, `aim`, `placebo`, `instruction`, `omit`, `control`, `condition`, `revision`, `reader`, or `digest`.

Write `6-judge/calibration/attempt-<n>/plan.yaml` before any rating: `judge_model` and `rater_model` (full IDs beginning `claude-`, different from each other), `raters` (`[user]` or `[agent, agent]`, `rater_model` only for agents), `sample_size`, `anchors_per_packet` (at least 3), and `acceptance` with `breach_difference`, `self_difference`, and `done_agreement` (0 to 1); never change a plan after its stage one.
</write-the-brief-and-plan>

<run-stage-one>
Run `instruction-eval judge calibrate`; with no `origins.yaml` in the latest attempt it snapshots the brief to `attempt-<n>/brief.md`, writes `sample.md`, `origins.yaml`, and rating definitions `ie-calib-<n>-candidate-1`, `-candidate-2`, and for agent raters `-rater-1`, `-rater-2`, and prints their launch list.

Wait up to three 20-second waits for the new agent types to list in the Agent tool; never restart the session for them.

Launch each listed agent type once from the main thread with the Agent tool and a prompt adding nothing to its definition; never launch from a subagent.

Launch at most twenty agents at once; the twenty-first is refused.

Each agent writes its own rating file; never write, paste, or edit a rating by hand.

Take every reply as its transcript's last assistant message, collected only by `revision collect` or `judge collect`; never paste a reply by hand.

For `raters: [user]`, have the user write `attempt-<n>/reference-user.yaml` in the verdict shape: `verdicts`, each with `id`, a `breaches` map per judge demand, `done`, `kind`, `notes`.
</run-stage-one>

<run-stage-two>
Run `instruction-eval judge calibrate` again once every rating file exists; it writes `attempt-<n>/agreement.yaml` and prints `accepted: attempt <n>` or `rejected: attempt <n> (<reason>)`.

On acceptance it writes `6-judge/calibration.yaml` and `6-judge/anchors.yaml`; never edit either.

On `missing rating: <path>`, relaunch the same definition; never write the file yourself.

On `rejected`, edit `6-judge/brief.md`, write `attempt-<n+1>/plan.yaml`, and rerun stage one; never alter the rejected attempt.

On `calibration pool exhausted`, lower `sample_size` in the next plan or start a new series with more repeats.

On `brief fault: <fault>`, fix that fault in `6-judge/brief.md` and rerun.

On `invalid rating`, `no reference done in the sample`, or `<CLAUDE_CONFIG_DIR> is outside`, report the line to the user and stop; never rerun past it.

On `already calibrated`, take the existing calibration; never start another attempt.
</run-stage-two>

<hand-off>
Hand off to `freeze-series` for `revision blind r1`; never blind before acceptance.
</hand-off>
