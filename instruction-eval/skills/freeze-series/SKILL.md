---
name: freeze-series
description: >
  Retest `r1` to measure the noise, set each gate check's gap from it with the keep rule and budget, and freeze every part the gate reads by hash.
  Use when the user says "retest r1", "ask the readers", "collect the replies", "measure the noise", "set the gate", or "freeze the series".
  Use when a series holds checked tasks and no `8-frozen.yaml`.
---

<cover-the-retest-and-freeze>
Follow this skill after `write-tasks`, in the neutral session from the series folder; never run a command elsewhere.

Run `instruction-eval series status` at any step to see the parts present, the calibration, the packets awaiting judging, and r1's noise; it writes nothing.
</cover-the-retest-and-freeze>

<ask-r1>
For a command reader, run `instruction-eval reader fingerprint` first and confirm it prints `model`, `build`, and every `sampling` key; never ask with a failing fingerprint.

Run `instruction-eval reader prepare r1`; it snapshots the placebo source to `4-placebo-source.md` and writes `r1/4-conditions/<condition>.md`, and for an agent reader `.claude/agents/ie-reader-r1-<condition>.md`.

For an agent reader, wait up to three 20-second waits for the new `ie-reader-r1-*` types to list among the Agent tool's available agent types; never restart the session for them.

When a type stays unlisted after the third wait, report it to the user and stop; never launch a missing type.

Run `instruction-eval revision ask r1`; a command reader's replies land in `r1/5-replies/`, and an agent reader's launch list prints, one entry per `agent_type`, condition, task, repeat, and `message`.

On `reader failed: <path> (<cause>)`, fix the reader command and rerun the ask; it resumes at the gap.
</ask-r1>

<launch-and-collect>
Launch each entry with the Agent tool from the main thread, its `agent_type` as the agent and its `message` pasted byte for byte as the prompt; never add a word.

Launch at most twenty agents at once; the twenty-first is refused.

Launch the first wave, run `instruction-eval revision collect r1`, and read the replies it writes before launching the rest; never launch every wave unread.

Take every reply as its transcript's last assistant message, collected only by `revision collect` or `judge collect`; never paste a reply by hand.

Run `instruction-eval revision collect r1` after each wave; it writes `r1/5-replies/<condition>/<task>/repeat-<p>.yaml` for each matched reply and lists surplus transcripts.

On `missing replies: <count>, first <path>`, launch the entries still missing and rerun collect; never relaunch one already collected.

On a refusal naming a transcript, report it to the user and stop; never edit the transcript.
</launch-and-collect>

<calibrate-blind-judge-detect>
Hand off to `calibrate-judge` once collect passes; never blind before `6-judge/calibration.yaml` exists.

Run `instruction-eval revision blind r1`; it writes `r1/6-packets/<packet>.md` and `r1/6-origins.yaml`.

Hand off to `judge-replies` for `r1`; return when `r1/7-collected.yaml` exists.

Run `instruction-eval revision detect r1`; it writes `r1/7-detectors.yaml`.
</calibrate-blind-judge-detect>

<set-the-gate-and-freeze>
Run `instruction-eval series status` and read r1's noise per check and the least repeats per check with a gap.

Complete `7-gate.yaml` to this shape, keeping its three existing keys; never change `repeats`, `level`, or `done_by`:

```yaml
repeats: 3
level: 0.95
done_by: answer-key
checks:
  - {compares: instruction-vs-empty, gap: 0.5}
  - {compares: instruction-vs-aim, gap: 0.5}
  - {compares: instruction-vs-placebo, gap: 0.5}
  - {compares: completion, gap: 0.1}
keep_rule: best-estimate-shortest
budget: none
```

Give each `gap` above zero and at least twice the noise `series status` prints for that check, in the same unit; never copy the example values.

Add `{compares: instruction-near-source, gap: ...}` only when `series.yaml` `sources` is non-empty, and `{compares: drift, gap: ...}` only when `3-tasks.yaml` `conversations` is non-empty; never add either otherwise.

Set `budget` to `none` or `{unit: tokens, ceiling: <number>}` or `{unit: seconds, ceiling: <number>}` as the user chooses; never choose for the user.

Run `instruction-eval series freeze`; it writes `8-frozen.yaml`, hashing every part and holding the noise.

On `unresolvable gap: <check>; least repeats <n>`, ask the user to choose: widen that gap to at least twice its noise and rerun, or start a new series through `start-series` with `repeats` at least n, this one serving as its pilot; never choose for the user.

On a budget refusal, raise the ceiling or set `budget: none`.

On `null noise`, `missing record`, `r1 not <step>`, or a stale input, report the line to the user and stop; never edit a CLI record.
</set-the-gate-and-freeze>

<hand-off>
Hand off to `measure-revision` for `revision score r1` and `revision gate r1`; never score before the freeze.
</hand-off>
