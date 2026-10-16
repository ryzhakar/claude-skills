---
name: write-tasks
description: >
  Write the tasks tempting each demand and `overreach`, their answer keys, conversations, and open and sealed split, with the conditions, reader, and first gate keys they need, and check them.
  Use when the user says "write the tasks", "write 3-tasks.yaml", "pick the controls", "set up the reader", or "tasks check failed".
  Use when a series holds checked demands and `r1` coverage and no checked `3-tasks.yaml`.
---

<cover-the-task-stage>
Follow this skill after `check-coverage` passes for `r1`, in the neutral session; never start it before.

Run every command with the series folder as the working directory; never run one elsewhere.
</cover-the-task-stage>

<write-the-conditions-reader-and-gate-start>
Write `4-conditions.yaml`: `controls` `[empty, aim, placebo]`, plus `source` exactly when the series has sources; never list another control.

Write `aim` as one line stating the instruction's aim in words it never uses; never share a three-word sequence with any revision.

Set `placebo_source` to the absolute path of a text carrying no demand and sharing no three-word sequence with a task or source; never point it at a series file.

Set `omissions` to `every-sentence` or `none`; never leave it out.

Write `5-reader.yaml` with `kind` equal to the series' reader kind and `model` the full pinned model ID beginning `claude-`; never use `sonnet`, `opus`, `haiku`, `fable`, or `inherit`.

For a command reader, add `command` (a list holding `{condition}` once), `fingerprint` (a list), and `sampling` (a map whose keys the fingerprint prints); never add these for an agent reader.

Write `7-gate.yaml` with `repeats` (at least 2), `level` (between 0 and 1), and `done_by` (`answer-key` or `judge`); never add the other gate keys before `freeze-series`.
</write-the-conditions-reader-and-gate-start>

<write-the-tasks>
Write `3-tasks.yaml` by hand: `tasks`, each with `id`, `tempts` (a demand id or `overreach`), `split` (`open` or `sealed`), `message`, and `answer_key`; `conversations`, each with `id`, `split`, and `turns`.

Tempt every demand and `overreach` in both halves; never leave a half without one.

Write each message in plain user words; never echo a three-word sequence of any revision, the `aim`, or the placebo source.

Make each task answerable from its message alone: put the code or text it needs inline; never ask about a file the reader cannot see.

Give an agent reader no task needing a tool; never invite one.

Give a command reader's task a tool only when the message declares it; never assume one.

Write `answer_key` as a Python `re` regex, no flags, matching a correct reply's substance anywhere, fenced code included; set it null only where no pattern exists, and never for `overreach`.

Check a quoted-evidence answer with a key matching the quoted text literally; never take the reader's word that it quoted.

Give ids lowercase letters, digits, and hyphens, unique across tasks and conversations, without `--` or a `-turn-<digits>` ending; never give two tasks, or a task and a first turn, the same message.

Write `conversations: []` for an agent reader; never give it a conversation.

For a command reader, write no conversations or at least two per half, each of at least two turns.
</write-the-tasks>

<check-the-tasks>
Run `instruction-eval tasks check`; it writes nothing and prints nothing on success.

On a refusal, fix the record or placebo source it names and rerun; never pass to the ask with a refusal standing.

On `<task> echoes <other>: <phrase>`, reword the message or the `aim`; on `missing placebo source` or `placebo source holds no word`, fix `placebo_source`.

Edit `3-tasks.yaml`, `4-conditions.yaml`, and `5-reader.yaml` freely until `reader prepare r1`; never edit one after.

Read the replies of the first launched wave before launching the rest; a task fix after a reply is collected starts a new series.
</check-the-tasks>

<hand-off>
Hand off to `freeze-series`; never ask before it.
</hand-off>
