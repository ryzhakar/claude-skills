---
name: check-back
description: >
  Before ending a turn that leaves a run pending, set the agent's own next wake, and on waking look at what was pending.
  "check back", "check back in 10 minutes", "wake up when it's done", "keep an eye on the build", "wait for the agents", "don't lose track of background work", "pick up after a resume", or any turn about to end while a background command, a background agent, or an external wait is still running.
---

<follow-before-the-turn-ends>
Follow this skill before ending any turn — one reply, from the input that starts it to the moment it stops — that leaves a pending run; never end such a turn without it.

Count as a pending run each background command, background agent, or external wait — a CI run, a deploy, a remote job — whose end or result the task in hand still waits on; never count a run left going with no end awaited, such as a dev server.

Nothing of the agent executes between turns, and a turn starts on a trigger alone: a user message, a notification — the message Claude Code sends when a background agent or command finishes or fails, carrying its result or its error — or a wake — a trigger the agent schedules for itself.

A hung agent or command sends no notification, and an external wait sends none at all.
</follow-before-the-turn-ends>

<set-one-wake-before-ending-the-turn>
Set a wake before ending a turn that leaves a pending run; never end that turn with no wake set.

Set the wake while a notification is still due; never count a coming notification as a wake.

Aim the wake at the earliest moment any pending run should have ended; never set a second wake for the same stretch.
</set-one-wake-before-ending-the-turn>

<choose-the-wake-mechanism>
Set a one-shot cron by default: `CronCreate` with `recurring: false` and a schedule pinning minute, hour, day of month, and month, such as `47 14 27 9 *`; never give a one-shot a step schedule such as `*/6 * * * *`.

Pin the minute off `:00` and `:30`; never pin it on either, where one-shots fire up to 90 seconds early.

Write each cron's prompt to stand alone, opening with `[check-back]` and naming each pending run's task ID, what it does, where it writes, and when it started; never write a prompt that leans on memory of the conversation.

A cron fires while the session sits idle between turns, waits out a busy turn, and skips missed fires without catching up.

Call `ScheduleWakeup` in place of a cron inside a self-paced `/loop` — a `/loop` started with a prompt and no interval — with a delay of 1 to 60 minutes; never call it outside such a loop.

Start a Monitor watch — the `Monitor` tool running a command whose each output line reaches the agent as an event — when one output line marks the change awaited and the wait fits the watch's deadline, 5 minutes by default and 30 at most; never start one for a longer wait.

A Monitor watch sends one notice at its deadline, and the tool is missing on Bedrock, Vertex, and Foundry and with telemetry turned off.
</choose-the-wake-mechanism>

<take-the-end-from-the-notification>
Take the end of a background agent or command from its notification; never infer the end from a file's existence or size.
</take-the-end-from-the-notification>

<look-at-pending-runs-on-waking>
On each wake, look at every pending run; never skip one.

A background agent's output file is a symlink to its transcript — the file recording each of its messages — and the transcript grows once per completed message, staying flat while the agent writes one long message.

Look at a background agent through the transcript's metadata with `stat -L` or `ls -laL`; never through plain `ls -la`, which reports the symlink's own size.

Look at a background agent without its transcript's contents; never `Read` the output file or call the deprecated `TaskOutput`.

Look at a background command through the last line of its output file with `tail -n 1`; never through the whole file.

Look at an external wait through its own status query, such as the CI tool's run status; never assume its state.

Set the next wake before ending the waking turn while any pending run remains; never let a wake pass without setting the next.
</look-at-pending-runs-on-waking>

<clear-wakes-that-guard-nothing>
Delete with `CronDelete` each `[check-back]` cron that `CronList` shows guarding no pending run; never leave one behind.

End a self-paced `/loop` with `ScheduleWakeup` and `stop: true` once no pending run remains; never leave it rescheduling.
</clear-wakes-that-guard-nothing>

<treat-a-resumed-session-as-emptied>
Compaction leaves pending runs and wakes in place and shrinks the conversation to a summary, while cron prompts survive it whole.

Closing a session kills every background command, background agent, and Monitor watch, and resuming it restores unexpired `CronCreate` crons but no one-shot whose time passed, no background command or agent, no Monitor watch, and no self-paced `/loop` wake.

After a resume, treat each run pending at the old session's end as ended without a notification; never wait for that notification.

Look at what each such run left on disk before acting on it; never assume its output complete or absent.
</treat-a-resumed-session-as-emptied>
