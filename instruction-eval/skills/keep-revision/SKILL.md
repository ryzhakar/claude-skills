---
name: keep-revision
description: >
  Apply the frozen keep rule at a series' stop and write the kept revision back over the instruction's live path.
  Use when the user says "keep the revision", "which revision won", "apply the keep rule", "write back the instruction", or "series keep".
  Use when the series holds `9-stop.yaml`.
---

<cover-the-keep-stage>
Follow this skill at the stop, after `measure-revision` or `diagnose` leaves `9-stop.yaml`, from the series folder; never run it before a stop.

Run `instruction-eval series status` first and read the stop, each gated revision's outcome, and the keep ranks to the user; it writes nothing.
</cover-the-keep-stage>

<read-the-stop>
Read `9-stop.yaml`: `stop` is `passed`, `no-effect`, `capped`, or `unresolvable`; `kept` is the revision the keep rule picked, or null; `reason` holds the user's text for `unresolvable` and `budget` for a budget cap.

The keep rule `best-estimate-shortest` takes the gated revisions that passed `completion`; the passing revision when one exists; else the lowest `instruction_breaches`, ties to fewer `words`, then the lower number; never pick a revision by another rule.
</read-the-stop>

<write-back>
Confirm with the user before replacing the live instruction at `series.yaml` `instruction`; never write back unasked.

Run `instruction-eval series keep`; it writes `r<kept>/2-instruction.md` over the live instruction and prints nothing.

On `series not stopped`, hand off to `measure-revision` or `diagnose`; never write `9-stop.yaml` by hand.

On `no revision passed completion`, report that no revision qualifies and leave the live instruction as it is; never copy a revision by hand.

Edit nothing in the series folder after the stop; never run a command there but `series status` and `series keep`.
</write-back>

<hand-off>
Hand the kept instruction back to the writer; start any further change as a new series through `start-series`, never in this one.
</hand-off>
