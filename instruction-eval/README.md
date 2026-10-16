# instruction-eval

Measure whether an LLM instruction changes model behavior.

`instruction` `evaluation` `prompt` 
## Skills

### [calibrate-judge](skills/calibrate-judge/SKILL.md)

Measure a candidate judge against reference raters on a blind sample of the retest's open replies, with acceptance set before any rating, and accept or reject the attempt. Use when the user says "calibrate the judge", "write the judge brief", "judge calibrate", "rate the sample", or "calibration rejected". Use when `r1` replies are collected and the series holds no `6-judge/calibration.yaml`.


---

### [check-coverage](skills/check-coverage/SKILL.md)

Map each demand to the instruction's sentences or to dropped, and each sentence to its demands, into a revision's coverage record, and refuse any imported sentence. "check coverage", "check against the source", "map demands to sentences", "write 3-coverage.yaml", "coverage check failed", "sentence carries no demand". A series holds a checked `2-demands.yaml` and a revision whose `3-coverage.yaml` is absent or refused by `instruction-eval coverage check`.


---

### [diagnose](skills/diagnose/SKILL.md)

Read the open failures of a failed revision for one failing demand and write the hypothesis predicting a movement the noise can show, or stop the series as unresolvable. Use when the user says "diagnose", "why did it fail", "write the hypothesis", "what should change next", or "stop the series". Use when the latest revision's `9-outcome.yaml` holds `outcome: fail` and the series has no `9-stop.yaml`.


---

### [freeze-series](skills/freeze-series/SKILL.md)

Retest `r1` to measure the noise, set each gate check's gap from it with the keep rule and budget, and freeze every part the gate reads by hash. Use when the user says "retest r1", "ask the readers", "collect the replies", "measure the noise", "set the gate", or "freeze the series". Use when a series holds checked tasks and no `8-frozen.yaml`.


---

### [judge-replies](skills/judge-replies/SKILL.md)

Prepare one judge agent per packet of a blinded revision, launch them, and collect the verdicts whose anchors meet the calibrated acceptance. Use when the user says "judge the replies", "judge r1", "launch the judges", "collect the verdicts", or "re-judge". Use when a revision holds `6-packets/` and `6-origins.yaml` and no `7-collected.yaml`.


---

### [keep-revision](skills/keep-revision/SKILL.md)

Apply the frozen keep rule at a series' stop and write the kept revision back over the instruction's live path. Use when the user says "keep the revision", "which revision won", "apply the keep rule", "write back the instruction", or "series keep". Use when the series holds `9-stop.yaml`.


---

### [list-demands](skills/list-demands/SKILL.md)

List every demand the source, or with no source the instruction, makes, one entry each with its boundary, into the series' demand record and check it. "list the demands", "save the demand list", "what does this instruction demand", "write 2-demands.yaml", "demands check failed". A series folder exists and its `2-demands.yaml` is absent, incomplete, or refused by `instruction-eval demands check`.


---

### [measure-revision](skills/measure-revision/SKILL.md)

Ask the reader, judge, detect, score, and gate one revision of a frozen series, then hand it to diagnosis or to the keep rule at a stop. Use when the user says "measure the revision", "gate r1", "score r2", "run r3", "did it pass", or "where does the series stand". Use when a series holds `8-frozen.yaml` and a revision without `9-outcome.yaml`.


---

### [revise](skills/revise/SKILL.md)

Make the hypothesis' one change to the live instruction through the writer and record it as the next revision, refusing any second change. Use when the user says "revise the instruction", "apply the hypothesis", "make the change", "record the revision", "save the cut", or "revision new failed". Use when the latest revision failed, the series has no stop, and `r<n+1>/1-hypothesis.yaml` exists without `r<n+1>/2-instruction.md`.


---

### [start-series](skills/start-series/SKILL.md)

Create a series folder for one instruction and its sources, and set up the neutral login whose session drives the series. Use when the user says "start a series", "evaluate this instruction", "measure this prompt", "test this digest", "set up instruction-eval", or "new series". Use when a user holds an instruction, with or without the source it distills, and no series folder for it yet.


---

### [write-tasks](skills/write-tasks/SKILL.md)

Write the tasks tempting each demand and `overreach`, their answer keys, conversations, and open and sealed split, with the conditions, reader, and first gate keys they need, and check them. Use when the user says "write the tasks", "write 3-tasks.yaml", "pick the controls", "set up the reader", or "tasks check failed". Use when a series holds checked demands and `r1` coverage and no checked `3-tasks.yaml`.


---

