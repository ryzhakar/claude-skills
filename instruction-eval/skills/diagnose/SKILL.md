---
name: diagnose
description: >
  Read the open failures of a failed revision for one failing demand and write the hypothesis predicting a movement the noise can show, or stop the series as unresolvable.
  Use when the user says "diagnose", "why did it fail", "write the hypothesis", "what should change next", or "stop the series".
  Use when the latest revision's `9-outcome.yaml` holds `outcome: fail` and the series has no `9-stop.yaml`.
---

<cover-the-diagnosis-stage>
Follow this skill after `measure-revision` gates a revision `fail` with no stop, in the neutral session from the series folder; never run it elsewhere.

Read open replies only; never read a sealed reply, a sealed row, or an anchor.
</cover-the-diagnosis-stage>

<find-the-failing-demand>
Take `r<n>` as the latest revision `series status` shows; never diagnose an earlier one.

Read `r<n>/9-outcome.yaml` for the checks that failed, then `r<n>/8-scores.yaml` for the open rows: `breaches` per demand, `kind`, and `done` per reply and condition.

Pick one failing demand: a gate demand the `instruction` replies breach, or `completion` when `instruction` replies fall short of `done`; never pick a dropped demand.

Map each open blind id to its reply through `r<n>/6-origins.yaml`: `<revision>/5-replies/<condition>/<task>/repeat-<p>.yaml`, the revision `borrowed_from` names when set.

Read the accepted verdict of each packet, `r<n>/7-verdicts/<packet>/k<k>.yaml` with k from `r<n>/7-collected.yaml`, for the judge's notes.

Read every `r<n>/5-replies/omit-<s>/<task>/repeat-<p>.yaml`, one condition per sentence s of the open tasks, to see what each sentence carries; never skip a sentence.
</find-the-failing-demand>

<quote-evidence-by-substring>
Read the open replies the failing check names, in full; never diagnose from counts alone.

Quote evidence only as exact substrings of a reply's `text`, and check each quote mechanically against the loaded reply file; never quote from memory or paraphrase inside quotes.
</quote-evidence-by-substring>

<write-the-hypothesis>
Create the folder `r<n+1>/` and write `r<n+1>/1-hypothesis.yaml` by hand; never run `revision new`, which `revise` runs:

```yaml
failing_demand: <gate demand id or completion>
replies_read: [<open blind ids read>]
change: {action: rewrite, sentence: 4}
predicted_movement: {direction: down, size: 0.3}
```

Set `change.action` to `rewrite`, `add`, `delete`, or `move`; `sentence` is the parent's sentence number, or the child's position for `add`; add `to`, the child's position, for `move` only; never name two changes.

Set `direction` to `down` for a demand's breaches per reply and `up` for `completion`'s done rate; set `size` above twice the target's change noise in the series folder's `8-frozen.yaml`, `noise.demands.<demand>` or `noise.done_change`; never copy the example values.

List in `replies_read` only open blind ids holding a breach of the failing demand, or a reply with `done` false for `completion`.

Hand the writer the failing demand, the quoted evidence, and the cause in prose; never store a cause in any record.
</write-the-hypothesis>

<stop-unresolvable>
Bound each target's size by its room to move in `r<n>/8-scores.yaml`: `by_condition.instruction.demands.<demand>` for a demand, `1 - by_condition.instruction.done_rate` for `completion`; never predict past it.

When every failing target's bound is at or below twice its change noise, run `instruction-eval series stop --reason <text>`; it writes `9-stop.yaml` with `stop: unresolvable` and the kept revision.

On `latest gated revision <r> did not fail` or `no gated revision to stop on`, report the line to the user and stop; never write `9-stop.yaml` by hand.
</stop-unresolvable>

<hand-off>
Hand off to `revise` with the hypothesis, or to `keep-revision` after `series stop`; never edit the instruction here.
</hand-off>
