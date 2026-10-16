---
name: list-demands
description: >
  List every demand the source, or with no source the instruction, makes, one entry each with its boundary, into the series' demand record and check it.
  "list the demands", "save the demand list", "what does this instruction demand", "write 2-demands.yaml", "demands check failed".
  A series folder exists and its `2-demands.yaml` is absent, incomplete, or refused by `instruction-eval demands check`.
---

<cover-the-demand-stage>
Follow this skill at the second step of a series, after `start-series` and before any revision's coverage.

A demand is one thing the instruction tells its reader to do or refuse, with its boundary folded in; a breach is one failure of a reply to obey one demand.

Run every command with the series folder as the working directory; every command but `series new` refuses elsewhere.
</cover-the-demand-stage>

<list-every-demand>
List from the files in `1-source/` when the series has a source, else from `r1/2-instruction.md`; never list from the live instruction.

Write one entry per distinct demand; collapse every restatement into one entry.

Fold each demand's boundary, where it stops applying, into the entry; never leave a boundary blank.

Attest completeness to the user when the list is done; the check verifies structure only.
</list-every-demand>

<write-the-demand-record>
Write `2-demands.yaml` by hand as `demands:`, a non-empty list of entries with `id`, `text`, `boundary`, and `counted_by`.

Give each `id` lowercase letters, digits, and hyphens, starting with a letter or digit, unique in the list; never use `overreach` or `completion`.

Set `counted_by: judge` for a demand a judge must read, with neither `pattern` nor `limit`.

Set `counted_by: pattern` with `pattern`, a Python `re` regex compiled with no flags, for a demand one match breaches; a detector counts its non-overlapping matches in the reply with fenced code blocks removed.

Set `counted_by: long-sentences` with `limit`, an integer above zero, for a sentence-length demand; a detector counts the reply's sentences holding more words than `limit`.

Edit `2-demands.yaml` freely until a CLI record hashes it; never edit it after.

A record whose hashed input changed refuses as stale, and the series restarts in a new folder.
</write-the-demand-record>

<check-the-record>
Run `instruction-eval demands check`; it writes nothing and prints nothing on success.

A refusal prints one line naming the entry at fault, such as `duplicate demand id: <id> (2-demands.yaml)`; fix that entry and rerun the check; never pass to coverage with a refusal standing.
</check-the-record>

<hand-off>
Hand off to `check-coverage` for `r1`.
</hand-off>
