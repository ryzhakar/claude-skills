---
name: check-coverage
description: >
  Map each demand to the instruction's sentences or to dropped, and each sentence to its demands, into a revision's coverage record, and refuse any imported sentence.
  "check coverage", "check against the source", "map demands to sentences", "write 3-coverage.yaml", "coverage check failed", "sentence carries no demand".
  A series holds a checked `2-demands.yaml` and a revision whose `3-coverage.yaml` is absent or refused by `instruction-eval coverage check`.
---

<cover-the-coverage-stage>
Follow this skill for `r1` after `list-demands`, and for each later revision after `revise` records it.

Coverage records that every demand is present in the revision or deliberately dropped, and that no sentence imports content no demand holds.

Run every command with the series folder as the working directory.
</cover-the-coverage-stage>

<number-the-sentences>
Number the sentences of `<r>/2-instruction.md` from 1 in reading order; never number the live instruction.

Count each of these as one sentence spanning its whole lines: a leading `---` frontmatter block, a fenced code block, a heading line, a table row line, a blockquote line, a horizontal rule.

Split each paragraph and each list item into sentences; a list item is its text after the marker with continuation lines, and a nested item is an item of its own.

End a sentence after `.`, `!`, or `?` plus any run of `"`, `'`, `)`, `]`, followed by whitespace or the unit's end; never end one after `e.g`, `i.e`, `etc`, `vs`, `cf`, `Mr`, `Mrs`, `Dr`, `St`, `No`, or a single letter.

Close the last sentence of a paragraph or list item at its end.
</number-the-sentences>

<write-the-coverage-record>
Write `<r>/3-coverage.yaml` by hand with two maps: `demands`, from every demand id to a non-empty list of sentence numbers or to `{dropped: <reason>}`; `sentences`, from every sentence number to a non-empty list of demand ids.

Keep the maps inverse: demand d lists sentence n exactly when sentence n lists d.

Drop a demand only where the instruction leaves it out on purpose; never store the word `imported`.

The demands `r1` leaves undropped are the gate demands, fixed for the series; dropped demands are measured and reported apart.

In a later revision, drop exactly the demands `r1` drops.

Edit the record freely until a CLI record hashes it; never edit it after.
</write-the-coverage-record>

<check-the-record>
Run `instruction-eval coverage check <r>`; it writes nothing and prints nothing on success.

`revision ask <r>` reruns the same check and refuses on failure; never ask a revision with a refusal standing.

On `unmapped demand: <id>`, map that demand to its sentences or to `{dropped: <reason>}`.

On `sentence number outside the text: <n>`, renumber by the rules above.

On `coverage maps disagree: demand <d> and sentence <n>`, add the missing pair to the other map.

On `dropped demands differ from r1`, drop exactly `r1`'s set.

On `sentence <n> carries no demand (imported)`, map sentence n to the demand it carries; never map it to a demand it does not carry.

When an imported `r1` sentence carries a demand the source makes, or the series has no source, add that demand through `list-demands`; otherwise the writer cuts the sentence from the live instruction and the series restarts through `start-series`.

Never edit `r1/2-instruction.md`.

When an imported sentence stands in a later revision, report the refusal to the user and stop.
</check-the-record>

<hand-off>
Hand off to `write-tasks` after `r1`, and to `measure-revision` after a later revision.
</hand-off>
