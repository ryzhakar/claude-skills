---
name: office-hours
description: >
  Hold an office-hours round: one event in which the owner answers the questions the agent queued.
  "office hours", "questioning round", or an agent about to ask whether the owner is present for a round; never a one-off question mid-task.
---

<open-a-round-on-presence>
Hold a round, the span in which the owner answers questions put through `AskUserQuestion`, whenever the owner starts one; never check presence then.

Ask in conversation text whether the owner is present when a round seems reasonable; never through `AskUserQuestion`.

NEVER assume the owner present.

Count the owner present, and the round open, when the owner types a message stating "i'm present"; never count any other message, or your asking, as either.

Without that message, keep working and ask nothing more until a round opens; never wait for it.

Begin reviewing and flushing the queue, the decide-while-away skill's list of what waits for a round, the moment the owner confirms presence.

A hook denies `AskUserQuestion` while the silence marker `.claude/work-silently` exists.

Ask nothing in silence; never ask there even whether the owner is present.

Remove the marker temporarily with `rm` as a round the owner starts in silence begins; never hold the round with it in place.
</open-a-round-on-presence>

<flush-the-whole-queue>
Review the queue in the order the decide-while-away skill sets; never in another.

Put every entry to the owner through `AskUserQuestion`, in as many calls as flushing all takes; never put a round's question in conversation text.

One call carries 1 to 4 questions, each with 2 to 4 options.

Put one question in each call, except in a rapid-fire set, one the owner asks for; never batch otherwise.

Put a solved entry as its decision and its one alternative, with the options "keep the decision" and "take the alternative"; never as an open question.

Search your records for an answer before every question; NEVER re-raise a settled question, one the owner answered in a round or one a standing word of the owner answers: the gravest breach of a round.

Record each answer the turn it is given; never defer it.

Return a question the owner dismisses without answering to the queue unanswered, and continue the round with the remaining entries; never end the round for it.

Wait inside a round for the answers you asked for; never wait for the owner outside one.

End the round when every entry has an answer or the owner says it ends, whichever comes first; never end it otherwise.

Leave each unanswered entry in the queue; never drop it.

Recreate the marker with `touch .claude/work-silently` the moment a round begun in silence ends; never leave it deleted.
</flush-the-whole-queue>

<make-each-question-portable>
Put everything the owner must see inside the `AskUserQuestion` call; never in conversation text, which stays minimal.

Write each question for an owner who saw nothing of the session; never name a branch, SHA, gate, draft, or id as if known.

Explain every command, term, and id in the question text where it appears; never use shorthand.

State in each option what choosing it does; never leave its effect implied.

You may ask the owner for an act the owner alone can perform; never ask for an errand.

<never_do_this reason="command unexplained">
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"Create the neutral login and run six checks?","header":"Checks","multiSelect":false,"options":[{"label":"Yes","description":"Then `claudes run <label>`."},{"label":"No","description":"Skip."}]}]</parameter>
</invoke>
</never_do_this>
<do_exactly_this>
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"`claudes run reader` starts Claude Code under a second login with no project instructions. Run six checks there?","header":"Checks","multiSelect":false,"options":[{"label":"Yes","description":"I run them."},{"label":"No","description":"Six behaviors go unverified."}]}]</parameter>
</invoke>
</do_exactly_this>

<never_do_this reason="internal id in option">
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"Which rewrite ships?","header":"Rewrite","multiSelect":false,"options":[{"label":"t1","description":"Ship t1."},{"label":"t2","description":"Ship t2."}]}]</parameter>
</invoke>
</never_do_this>
<do_exactly_this>
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"Which welcome text ships?","header":"Rewrite","multiSelect":false,"options":[{"label":"Short","description":"Two lines ship."},{"label":"Full","description":"Ten lines ship."}]}]</parameter>
</invoke>
</do_exactly_this>

<never_do_this reason="errand">
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"Install instruction-eval?","header":"Install","multiSelect":false,"options":[{"label":"Yes","description":"You run it; I notify the sibling."},{"label":"No","description":"Nothing changes."}]}]</parameter>
</invoke>
</never_do_this>
<do_exactly_this>
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"Install the instruction-eval plugin, which tests skills, for a sibling session?","header":"Install","multiSelect":false,"options":[{"label":"Yes","description":"I install it."},{"label":"No","description":"Nothing changes."}]}]</parameter>
</invoke>
</do_exactly_this>
</make-each-question-portable>

<recover-from-a-rejected-question>
When the owner rejects a question or finds it unclear, stop and wait for the owner's word; never repost it.

Replace it with a question that adds every missing definition, then continue the flush with the remaining entries.

Answer the owner's clarifying question directly, in the owner's terms; never in your own.

<never_do_this reason="rejected question reposted">
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"Create the neutral login and run six checks?","header":"Checks","multiSelect":false,"options":[{"label":"Yes","description":"Then `claudes run <label>`."},{"label":"No","description":"Skip."}]}]</parameter>
</invoke>
</never_do_this>
<do_exactly_this>
<invoke name="AskUserQuestion">
<parameter name="questions">[{"question":"`claudes run reader` starts Claude Code under a second login with no project instructions. Run six checks there?","header":"Checks","multiSelect":false,"options":[{"label":"Yes","description":"I run them."},{"label":"No","description":"Six behaviors go unverified."}]}]</parameter>
</invoke>
</do_exactly_this>
</recover-from-a-rejected-question>
