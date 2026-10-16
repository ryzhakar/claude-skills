---
name: measure-revision
description: >
  Ask the reader, judge, detect, score, and gate one revision of a frozen series, then hand it to diagnosis or to the keep rule at a stop.
  Use when the user says "measure the revision", "gate r1", "score r2", "run r3", "did it pass", or "where does the series stand".
  Use when a series holds `8-frozen.yaml` and a revision without `9-outcome.yaml`.
---

<cover-the-measure-stage>
Follow this skill for `r1` after `freeze-series`, and for each later revision after `check-coverage` passes on it, in the neutral session from the series folder; never run a command elsewhere.

Run `instruction-eval series status` at any step to read the parts present, each revision's outcome, `changed_from_parent`, keep ranks, cost against the budget, packets awaiting judging, and the stop; it writes nothing.
</cover-the-measure-stage>

<ask-a-later-revision>
Skip this section for `r1`; its replies, packets, verdicts, and detectors exist from the retest.

Run `instruction-eval reader prepare <r>`; it writes `<r>/4-conditions/<condition>.md` for `instruction` and the revision's `omit-<n>`, and for an agent reader `.claude/agents/ie-reader-<r>-<condition>.md`.

For an agent reader, wait up to three 20-second waits for the new `ie-reader-<r>-*` types to list among the Agent tool's available agent types; when one stays unlisted, report it to the user and stop; never restart the session for them.

Run `instruction-eval revision ask <r>`, adding `--conditions <name>` once per condition to limit one ask; a command reader's replies land in `<r>/5-replies/`, and an agent reader's launch list prints.

On `reader failed: <path> (<cause>)`, fix the reader command and rerun; on a budget refusal, report it to the user and stop; never raise a frozen budget.

Launch each launch-list entry from the main thread with the Agent tool, its `agent_type` as the agent and its `message` byte for byte as the prompt; never add a word.

Launch at most twenty agents at once; the twenty-first is refused.

Take every reply as its transcript's last assistant message, collected only by `revision collect` or `judge collect`; never paste a reply by hand.

Run `instruction-eval revision collect <r>` after each wave; it writes the missing `<r>/5-replies/<condition>/<task>/repeat-<p>.yaml` files it can match; on `missing replies: <count>, first <path>`, launch the entries still missing and rerun; never relaunch a collected one.

Run `instruction-eval revision blind <r>`; it writes `<r>/6-packets/<packet>.md` and `<r>/6-origins.yaml`, borrowing every control reply from `r1`.

Hand off to `judge-replies` for `<r>`; return when `<r>/7-collected.yaml` exists.

Run `instruction-eval revision detect <r>`; it writes `<r>/7-detectors.yaml`.
</ask-a-later-revision>

<score-and-gate>
Run `instruction-eval revision score <r>`; it writes `<r>/8-scores.yaml`, open rows only.

Run `instruction-eval revision gate <r>`; it writes `<r>/9-outcome.yaml` with `outcome` `pass` or `fail`, each check, the keep ranks, and the cost, and writes `9-stop.yaml` when a stop applies.

Read the outcome to the user from `series status`; never read or quote sealed rows.

On a refusal naming a missing record or a stale input, report the line to the user and stop; never edit a CLI record.
</score-and-gate>

<hand-off>
When `9-stop.yaml` exists, `passed`, `no-effect`, or `capped`, hand off to `keep-revision`; never ask another revision.

When the outcome is `fail` and no stop exists, hand off to `diagnose`; never edit the instruction first.
</hand-off>
