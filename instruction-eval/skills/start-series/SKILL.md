---
name: start-series
description: >
  Create a series folder for one instruction and its sources, and set up the neutral login whose session drives the series.
  Use when the user says "start a series", "evaluate this instruction", "measure this prompt", "test this digest", "set up instruction-eval", or "new series".
  Use when a user holds an instruction, with or without the source it distills, and no series folder for it yet.
---

<gather-the-inputs>
Ask the user for the instruction path, each source path, a series name without `/`, and the reader: a Claude model (`agent`) or another model served by a command (`command`); never guess one.

Turn every path into an absolute path; never pass a relative one.
</gather-the-inputs>

<set-up-the-neutral-login-once>
Skip this section when `$(claudes path readers)/settings.json` holds both allow rules and both plugins below; never skip on the folder's existence alone.

When `claudes ls` lists no `readers`, hand the user `/plugin marketplace add ryzhakar/claude-skills` and then `/plugin install instruction-eval@my-claude-skills` to type in the default login, and ask for each command's result; never continue before two reports of success.

On a failure report, stop and report its text; never retry it yourself.

Then make the login with `claudes new --bare readers instruction-eval@my-claude-skills manifesto@my-claude-skills`; never name another plugin.

When `claudes ls` lists `readers`, skip the plugin commands, `claudes new`, and the `/login` hand-off, and only fix `settings.json`; never make the login twice.

Edit `$(claudes path readers)/settings.json`, creating it as `{}` when absent: add `Write(~/instruction-series/**/7-verdicts/**)` and `Write(~/instruction-series/**/6-judge/calibration/**)` to `permissions.allow`, creating `permissions` and `allow` when absent; never drop an existing allow entry.

Set `enabledPlugins` to exactly `instruction-eval@my-claude-skills` and `manifesto@my-claude-skills`, both true; never list another plugin in `enabledPlugins`.

Keep the bare login free of a `CLAUDE.md`, a skill, and an agent; never add one.

Read `settings.json` back and confirm both allow rules and both plugins; never continue with a gap.

Only when `claudes new` ran in this turn, hand the user `claudes run readers` to start once in their own terminal and ask them to run `/login` there with the same account and report success; never continue before that report.
</set-up-the-neutral-login-once>

<make-the-series-folder>
Run `instruction-eval series new <name> --instruction <path> [--source <path>]… --reader-kind agent|command` by bare name from the Bash tool in any working directory; never start a session in the folder before it.

When Bash finds no `instruction-eval`, hand the user `/reload-plugins` and rerun; never call the CLI by its cache path.

Give the bare name, which creates `~/instruction-series/<name>/`; never give a path outside `~/instruction-series/`.

Repeat `--source` once per source file; never pass it for an instruction with no source.

Pick `--reader-kind agent` for a Claude reader and `command` for any other model; never change the kind within a series.

Run `cd ~/instruction-series/<name> && ls -a . .claude .claude/agents 1-source r1` and confirm `series.yaml`, an empty `.claude/agents/`, `1-source/<basename>` per source, `r1/2-instruction.md`, and `r1/2-revision.yaml`; never continue past a missing item.

Leave every file `series new` wrote as written; never edit one.
</make-the-series-folder>

<answer-each-refusal>
Read a refusal as the one line `series new` prints on stderr with a nonzero exit; never treat stdout as one.

On `series folder not empty`, choose a new name; never empty a folder to reuse it.

On `series folder under a memory file` or `series folder inside a git work tree`, choose a folder outside every `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `.manifestos.yaml`, and git work tree; never delete the file named.

On `duplicate source basename`, copy one of the two sources to another file name and pass the copy; never rename the user's file.

On `unclosed frontmatter: <path>`, ask the user to close the frontmatter in that file with a line exactly `---`; never edit their file unasked.

On `missing file`, correct the path; never create the file.

On any other refusal, or the same refusal after a fix, stop and report its text; never run `series new` after three refusals of any kind in a row.
</answer-each-refusal>

<rules-for-the-neutral-session>
These rules apply to later skills; apply them in the neutral session; never act on them in this skill.

Run every other instruction-eval skill in the neutral session; never run `reader prepare`, `judge prepare`, or `judge calibrate` stage one in another.

Launch every generated agent from that session's main thread; never from a subagent.

After each `reader prepare`, `judge prepare`, and `judge calibrate` stage one, check the Agent tool's list of available agent types for the new ones, rechecking after each of up to three 20-second waits; never restart the session for them.

When a type stays absent after the third wait, stop and report it to the user; never launch a missing type.
</rules-for-the-neutral-session>

<hand-off>
End the turn with one message holding the absolute folder path, `cd ~/instruction-series/<name> && claudes run readers` for the user's own terminal, and `/instruction-eval:list-demands` to type first in that session; never launch the session or load `list-demands` yourself.
</hand-off>
