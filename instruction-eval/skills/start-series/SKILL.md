---
name: start-series
description: >
  Create a series folder for one instruction and its sources, and set up the neutral login whose session drives the series.
  Use when the user says "start a series", "evaluate this instruction", "measure this prompt", "test this digest", "set up instruction-eval", or "new series".
  Use when a user holds an instruction, with or without the source it distills, and no series folder for it yet.
---

<gather-the-inputs>
Ask the user for the instruction path, each source path, a series name, and whether the reader is a Claude model; never guess one.
</gather-the-inputs>

<set-up-the-neutral-login-once>
Skip this section when `test -d ~/.claudes-bare/readers` succeeds; never make the login twice.

Install the plugin in the default login with `/plugin install instruction-eval@my-claude-skills` before `claudes new`; never run `claudes new` first.

Make the neutral login with `claudes new --bare readers instruction-eval@my-claude-skills manifesto@my-claude-skills`.

Edit `$(claudes path readers)/settings.json`: add `Write(~/instruction-series/**/7-verdicts/**)` and `Write(~/instruction-series/**/6-judge/calibration/**)` to `permissions.allow`, creating the key when absent; never drop an existing entry.

Keep `enabledPlugins` exactly `instruction-eval@my-claude-skills` and `manifesto@my-claude-skills`, both true; never add a `CLAUDE.md`, a skill, or an agent to the bare login.

Read `settings.json` back and confirm both allow rules and both plugins; fix any gap before the next step.

Hand the user `claudes run readers` to start once in their own terminal and run `/login` with the same account; wait for their word that login succeeded.
</set-up-the-neutral-login-once>

<make-the-series-folder>
Run `instruction-eval series new <name> --instruction <path> [--source <path>]… --reader-kind agent|command` from the Bash tool, where the enabled plugin puts `instruction-eval` on PATH; never start a session in the folder before it.

Give a bare name, which creates `~/instruction-series/<name>/`; never give a path outside `~/instruction-series/`.

Repeat `--source` once per source file; omit it for an instruction with no source.

Pick `--reader-kind agent` for a Claude reader and `command` for any other model; never change the kind within a series.

Expect `series.yaml`, an empty `.claude/agents/`, `1-source/<basename>` per source, `r1/2-instruction.md`, `r1/2-revision.yaml`, and the folder path printed; never edit a file `series new` wrote.
</make-the-series-folder>

<answer-each-refusal>
On a refusal, fix the named fault and rerun the same command; never edit a file the command wrote.

On `series folder not empty`, choose a new name; never empty a folder to reuse it.

On `series folder under a memory file` or `series folder inside a git work tree`, choose a folder outside every `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `.manifestos.yaml`, and git work tree.

On `duplicate source basename`, give one of the two sources another file name.

On `unclosed frontmatter: <path>`, close the frontmatter in that file with a line exactly `---`.

On `missing file`, correct the path.
</answer-each-refusal>

<launch-the-neutral-session>
End the turn at the printed folder path and hand the user `cd <series folder> && claudes run readers` to run in their own terminal; never launch it yourself.

Run every later step in that session, whose `CLAUDE_CONFIG_DIR` lies under `~/.claudes-bare/`; never run `reader prepare`, `judge prepare`, or `judge calibrate` stage one elsewhere.

Launch every generated agent from that session's main thread; never from a subagent.

After each `reader prepare`, `judge prepare`, and `judge calibrate` stage one, wait up to 60 seconds for the new agent types to appear in the Agent tool's list of available agents, then launch; never restart the session for them.

When a type stays absent after 60 seconds, stop and report the missing type to the user.
</launch-the-neutral-session>

<hand-off>
Load `list-demands` in the neutral session once it runs.
</hand-off>
