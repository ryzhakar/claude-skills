---
name: revise
description: >
  Make the hypothesis' one change to the live instruction through the writer and record it as the next revision, refusing any second change.
  Use when the user says "revise the instruction", "apply the hypothesis", "make the change", "record the revision", "save the cut", or "revision new failed".
  Use when the latest revision failed, the series has no stop, and `r<n+1>/1-hypothesis.yaml` exists without `r<n+1>/2-instruction.md`.
---

<cover-the-revision-stage>
Follow this skill after `diagnose` writes `r<n+1>/1-hypothesis.yaml`; never revise without a hypothesis.

Let the writer, in any session, make the change; run every command with the series folder as the working directory.
</cover-the-revision-stage>

<make-the-one-change>
Read `change` in `r<n+1>/1-hypothesis.yaml`: `action` `rewrite`, `add`, `delete`, or `move`; `sentence`; and `to` for `move`.

Number the sentences of the parent, `r<n>/2-instruction.md`, from 1 in reading order; never count by eye.

Count as one sentence each leading `---` frontmatter block, fenced code block, heading line, table row line (separator included), blockquote line, and horizontal rule.

Split paragraphs and list items after `.`, `!`, or `?` plus any closing `"`, `'`, `)`, `]`, before whitespace or the unit's end; never split after `e.g`, `i.e`, `etc`, `vs`, `cf`, `Mr`, `Mrs`, `Dr`, `St`, `No`, or a single letter.

Edit the live instruction at `series.yaml` `instruction` so it equals the parent except for that one change; never touch a second sentence.

For `rewrite s`, replace sentence s; for `delete s`, remove it; for `add s`, insert a sentence at position s of the new text; for `move s` with `to t`, place sentence s unchanged at position t.

Keep every three-word sequence of the `3-tasks.yaml` task `message`s and conversation `turns`, the `4-conditions.yaml` `aim`, and `r1/4-conditions/placebo.md` out of the new text; never borrow their wording.
</make-the-one-change>

<record-the-revision>
Run `instruction-eval revision new`; it reads the live instruction once and writes `r<n+1>/2-instruction.md` and `r<n+1>/2-revision.yaml`, hashing the parent's record into the chain, and prints nothing.

Leave both files as written; never edit either, and never edit the live instruction toward a different change afterwards.

On `the instruction does not make the named change: <action> <s>`, restore every other sentence to the parent's text and rerun.

On `revision <r> echoes <label>: <phrase>`, reword the changed sentence to drop the phrase and rerun.

On `unclosed frontmatter: <path>`, close the live instruction's frontmatter with a line exactly `---` and rerun.

On `predicted size <x> does not exceed twice the change noise`, `replies_read shows no failure`, or `replies_read holds no open reply`, return to `diagnose` for a new hypothesis; never edit the numbers to pass.

On `latest revision <r> is not gated` or `did not fail`, report the line to the user and stop.
</record-the-revision>

<hand-off>
Hand off to `check-coverage` for `r<n+1>/3-coverage.yaml` and `coverage check r<n+1>`, then to `measure-revision`; never ask the revision first.
</hand-off>
