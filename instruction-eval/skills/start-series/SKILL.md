---
name: start-series
description: >
  Create a series folder for one instruction and its sources, and set up the neutral login whose session drives the series.
  "start a series", "evaluate this instruction", "measure this prompt", "test this digest", "set up instruction-eval", "new series".
  A user holds an instruction, with or without the source it distills, and no series folder for it yet.
---

<cover-the-first-stage>
Follow this skill at the start of a series: the neutral login once per machine, the series folder once per instruction, then the launch of the neutral session in that folder.

A series is every revision of one instruction measured under one frozen set of demands, tasks, conditions, reader, judge, gate, and keep rule.
</cover-the-first-stage>

<set-up-the-neutral-login-once>
Install `instruction-eval@my-claude-skills` in the default login first; `claudes new` refuses a plugin missing from the shared registry.

Make the neutral login with `claudes new --bare readers instruction-eval@my-claude-skills manifesto@my-claude-skills`, which writes `~/.claudes-bare/readers`.

Start it once with `claudes run readers` and run `/login` with the same account.

Add `Write(~/instruction-series/**/7-verdicts/**)` and `Write(~/instruction-series/**/6-judge/calibration/**)` to `permissions.allow` in the bare login's `settings.json`; `claudes path readers` prints its folder.

Keep `enabledPlugins` exactly `instruction-eval@my-claude-skills` and `manifesto@my-claude-skills`, both true; never add a `CLAUDE.md`, a skill, or an agent to the bare login.

`reader prepare`, `judge prepare`, and `judge calibrate` stage one refuse a session whose `CLAUDE_CONFIG_DIR` lies outside `~/.claudes-bare/` or breaks either rule.
</set-up-the-neutral-login-once>

<make-the-series-folder>
Run `instruction-eval series new <name|path> --instruction <path> [--source <path>]… --reader-kind agent|command` in any shell, the working session included; never start a session in the folder before it.

Give a bare name, which puts the series at `~/instruction-series/<name>/` where the allow rules reach; never give a path outside `~/instruction-series/`.

Repeat `--source` once per source file; omit it for an instruction with no source.

Pick `--reader-kind agent` for a Claude reader and `command` for any other model; never change the kind within a series.

`series new` writes `series.yaml`, an empty `.claude/agents/`, `1-source/<basename>` per source, `r1/2-instruction.md`, and `r1/2-revision.yaml`, then prints the folder; never edit a file it wrote.
</make-the-series-folder>

<answer-each-refusal>
A refusal prints one line, writes nothing, and names the one fault; fix that fault and rerun the same command.

On `series folder not empty`, choose a new name; never empty a folder to reuse it.

On `series folder under a memory file` or `series folder inside a git work tree`, choose a folder outside every `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `.manifestos.yaml`, and git work tree.

On `duplicate source basename`, give one of the two sources another file name.

On `unclosed frontmatter: <path>`, close the frontmatter in that file with a line exactly `---`.

On `missing file`, correct the path.
</answer-each-refusal>

<launch-the-neutral-session>
Launch it with `cd <series folder> && claudes run readers`; run every later step in that session.

Launch every generated agent from that session's main thread; never from a subagent.

After each `reader prepare`, `judge prepare`, and `judge calibrate` stage one, wait until the new agent types list in the Agent tool, then launch; never restart the session for them.

PR7 measured four definitions written into the series folder's `.claude/agents/` registering in the main thread's Agent tool within about 40 seconds without restart, and never in a subagent's Agent tool.
</launch-the-neutral-session>

<hand-off>
Hand off to `list-demands`.
</hand-off>
