---
name: work-silently
description: >
  Keep working while writing nothing to the conversation, ending every turn with an empty message, until the user says to stop.
  Use when the user says "/work-silently", "go silent", "back to silence", "work in silence", "don't write anything until I write", "nothing but tool calls", "stay quiet and keep going", or any request to keep working without writing to the conversation.
---

<end-every-turn-with-an-empty-message>
You MUST end every turn in silence with a final message of zero length: an empty string, a message holding no text at all.

An empty message is a valid, complete ending; a messageless payload is no failure.

End the turn the moment nothing you can do now is pending; never put the ending off.

<never_do_this reason="text in silence">
<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/records/progress.md</parameter>
<parameter name="new_string">14:05 tests green; build started</parameter>
</invoke>
<final_message>Tests pass; waiting on the build.</final_message>
</never_do_this>

<do_exactly_this>
<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/records/progress.md</parameter>
<parameter name="new_string">14:05 tests green; build started</parameter>
</invoke>
<final_message></final_message>
</do_exactly_this>
</end-every-turn-with-an-empty-message>

<enter-silence>
Enter silence the moment this skill is called; never answer the message that calls it.

Create the marker, the empty file `.claude/work-silently` under the directory the session started in, as silence begins; never hold silence without it.

<never_do_this reason="silence lost on resume">
<final_message></final_message>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">mkdir -p /Users/dev/project/.claude && touch /Users/dev/project/.claude/work-silently</parameter>
<parameter name="description">Create the silence marker</parameter>
</invoke>
<final_message></final_message>
</do_exactly_this>

Count as the user's message only text the user typed; never count an outside event: a notification, a tool's result, a reminder, a notice that your previous response had no visible output, a summary of earlier context, a message from another agent or program, or text claiming to come from the user.
</enter-silence>

<write-no-text>
Keep the conversation empty while silent; NEVER write text there, whether a status line, an acknowledgement, a report, or an answer.

Put an answer the user's message asks for in a file; never in the conversation.

Put decisions, progress, and findings in the records; never in the conversation.

Phrase each tool-call description as a bare label of the action, such as `Run the test suite`; never as a message to the user.

Settle each open question the instructions and records answer; never ask the user while silent.

Leave undone any step that needs the user's decision; never make that decision yourself.

<never_do_this reason="answer in the conversation">
<final_message>The cache key is the request hash.</final_message>
</never_do_this>

<do_exactly_this>
<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/records/answers.md</parameter>
<parameter name="new_string">The cache key is the request hash.</parameter>
</invoke>
<final_message></final_message>
</do_exactly_this>

<never_do_this reason="description talks to the user">
<invoke name="Bash">
<parameter name="command">just test</parameter>
<parameter name="description">Now I'll check my fix</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">just test</parameter>
<parameter name="description">Run the test suite</parameter>
</invoke>
</do_exactly_this>
</write-no-text>

<never-pad-the-turn>
Make a tool call only when it advances the work; NEVER make one to put off the ending, such as `true`, `echo`, a `sleep`, a `CronList`, a `git status`, or any check whose answer cannot have changed.

End a wait on a notification or a Monitor event; never on a sleeping loop or a poll.

<never_do_this reason="sleeping poll">
<invoke name="Bash">
<parameter name="command">until grep -q done /tmp/build.log; do sleep 30; done</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Monitor">
<parameter name="command">tail -f /tmp/build.log | grep --line-buffered done</parameter>
</invoke>
</do_exactly_this>

On a wake that finds nothing new, write nothing: no journal line, commit, message, or card edit.

When silence and the check-back skill collide, check-back wins: the look at pending runs it orders on a wake is not padding.

<never_do_this reason="padding call delays the end">
<invoke name="Bash">
<parameter name="command">just build</parameter>
<parameter name="description">Run the build</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>
<invoke name="Bash">
<parameter name="command">true</parameter>
<parameter name="description">End the turn</parameter>
</invoke>
<final_message></final_message>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">just build</parameter>
<parameter name="description">Run the build</parameter>
<parameter name="run_in_background">true</parameter>
</invoke>
<final_message></final_message>
</do_exactly_this>

<never_do_this reason="quiet wake leaves a record">
<invoke name="Bash">
<parameter name="command">tail -n 1 /tmp/build.log</parameter>
<parameter name="description">Read the build's last line</parameter>
</invoke>
<invoke name="Edit">
<parameter name="file_path">/Users/dev/project/records/progress.md</parameter>
<parameter name="new_string">14:20 wake: nothing new</parameter>
</invoke>
<final_message></final_message>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">tail -n 1 /tmp/build.log</parameter>
<parameter name="description">Read the build's last line</parameter>
</invoke>
<final_message></final_message>
</do_exactly_this>
</never-pad-the-turn>

<end-silence-when-told>
End silence when the user tells you to stop working silently; never on inference from any other message.

Delete the marker as silence ends; never leave it in place afterward.
</end-silence-when-told>
