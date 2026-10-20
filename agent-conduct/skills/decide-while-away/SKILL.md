---
name: decide-while-away
description: >
  Settle the owner's decisions while the owner is away: decide each reversible choice, write it beside its single closest alternative, act on it, and leave each choice that cannot be undone unsolved in a queue.
  Use when a step needs a decision that is the owner's to make and the owner has not given it, while the owner is away, outside a round of questions; never at any other moment.
---

<queue-every-owner-decision>
Keep the queue, your list of every decision that is the owner's to make, in your durable records, the store that survives a restart and a context compaction; never outside them.

Write each decision as one of two kinds of entry: unsolved, a question you could not settle with a reversible decision, or solved, a reversible decision you made, written with its single closest alternative; never as any other kind.

Queue every decision that is the owner's to make; never leave one out.

Write each entry into the records the turn it arises; never defer it.
</queue-every-owner-decision>

<decide-and-act>
Settle as much of the queue as you can, eagerly, with reversible decisions; never settle less than you can.

Write each decision and its single closest alternative into the queue first; never act on an unwritten decision.

Then act on the decision; never wait for the owner's word while the owner is away, outside a round, the span in which the owner answers the queued questions.

<never_do_this reason="blocked on the owner">
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"~70 units left cost more than wave 2. Pace how?","header":"Pacing","multiSelect":false,"options":[{"label":"Batch","description":"Groups."},{"label":"Pause","description":"Stop."}]}]</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/records/queue.md</parameter>
<parameter name="new_string">Solved: per module. Alternative: all at once.</parameter>
</invoke>
<invoke name="Agent">
<parameter name="prompt">[module 1]</parameter>
</invoke>
</do_exactly_this>
</decide-and-act>

<leave-irreversible-choices-unsolved>
Keep each choice that cannot be undone an unsolved entry; never decide it yourself.

Let the work that depends on an unsolved entry wait, and continue all other work; never halt that other work.
</leave-irreversible-choices-unsolved>

<review-the-queue-at-a-round>
At a round, review the whole queue, unsolved entries first; never review a part of it or in another order.

When the owner picks the alternative of a solved entry, switch the work to the alternative; never keep working on the decision.
</review-the-queue-at-a-round>
