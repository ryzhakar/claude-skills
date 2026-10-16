---
name: judge-replies
description: >
  Prepare one judge agent per packet of a blinded revision, launch them, and collect the verdicts whose anchors meet the calibrated acceptance.
  Use when the user says "judge the replies", "judge r1", "launch the judges", "collect the verdicts", or "re-judge".
  Use when a revision holds `6-packets/` and `6-origins.yaml` and no `7-collected.yaml`.
---

<cover-the-judging-stage>
Follow this skill after `revision blind <r>`, from `freeze-series` for `r1` or `measure-revision` for a later revision, in the neutral session from the series folder; never run it elsewhere.

Judge with the accepted calibration only; never write a brief, a judge definition, or a verdict by hand.
</cover-the-judging-stage>

<prepare-and-launch>
Run `instruction-eval judge prepare <r>`; for each packet with no accepted judging it writes `.claude/agents/ie-judge-<r>-<packet>-k<k>.md`, prints `judging k<k> pending: <packet>` for a packet whose judge still runs, then prints the launch list of `agent_type` entries.

Wait up to three 20-second waits for the new `ie-judge-<r>-*` types to list among the Agent tool's available agent types; when one stays unlisted, report it to the user and stop; never restart the session for them.

Launch each listed agent type once from the main thread with the Agent tool and the prompt `Begin.`; never launch from a subagent.

Launch the first twenty listed types, then one more as each judge ends; never launch a twenty-first while twenty run.

Each judge writes its own verdict to `<r>/7-verdicts/<packet>/k<k>.yaml`; never write, paste, or edit a verdict.

Take every reply as its transcript's last assistant message, collected only by `revision collect` or `judge collect`; never paste a reply by hand.
</prepare-and-launch>

<collect>
Run `instruction-eval judge collect <r>` once every launched judge has ended; with every packet accepted it writes `<r>/7-collected.yaml` and prints nothing.

On `re-judge: <packet>` lines, run `judge prepare <r>` again, launch the next judgings it lists, and collect again; never relaunch a judging that already returned.

On `judging pending: <packet>`, wait for that judge to end and rerun collect; never launch a second judging of that packet meanwhile.

On `recalibrate in a new series`, report it to the user and start a new series through `start-series`; never prepare another judging here.

On `edited packet`, `missing packet`, or a refusal naming a definition or transcript, report the line to the user and stop; never edit a packet or definition.
</collect>

<hand-off>
Return to `freeze-series` for `r1` or to `measure-revision` for a later revision once `<r>/7-collected.yaml` exists; never detect or score before it.
</hand-off>
