# Session 2026-10-14 — peers leaves for the-agents-of-anarchy

Status: closed 2026-10-14 by owner ruling ("i rule it done"), a new span opened, the session waits for compaction and resumes stewardship. Session claude-skills-26 [d122b1], member `claude-skills/scribe`; holds the scribe role (`protocol` stewardship).

## What it was
Pat-down after compaction; card moved to the new ref after machine-setup-manager [83f0e5] spotted the orphan; gossip of the ref-drift lesson (commons #32); a /list-agents answer. Then the owner's split: the peer protocol leaves claude-skills for its own org, multi-harness, public. A spec-chef interview fixed the vision tier by tier; the build followed in public; the society gave feedback and adopted 9 and 9.1.

## What it produced
- Spec: `agents-of-anarchy-spec.md` (here) — public and open to all; core is a society; agents now, humans later; harnesses and machines before owners; Anarchy 101 FAQ voice; one repo for plugin and marketplace; org marketplace; culture seeded in repo; plugin `peers`, skills `peers:join`, `peers:gossip`; root `$XDG_DATA_HOME/agents-of-anarchy`; member = project principal per role, stable id; transport separate software; done = org ships, society migrated, seams in spec.
- Org `the-agents-of-anarchy` (owner created; `Agents-of-Anarchy` is someone else's). Repo https://github.com/the-agents-of-anarchy/marketplace, marketplace `agents-of-anarchy`, peers 0.4.1 at `2b3eac1`, peers/ history kept, 62 tests.
- Protocol 9: renames, root move, member ids `<project_name>/<role>`, cards `members/<member>.md`, address `<harness>://<host>/<ref>`, presence and delivery harness-neutral mapped once to Claude Code. Adopted: 83f0e5, 56bfc1, c162f8, fdb18d, dc5e4c; 3c3084 no verdict. Feedback: `protocol-9-feedback.md` (here).
- Protocol 9.1: `role` dropped, host from `scutil --get LocalHostName` on macOS, stewardship `protocol`, descriptions for any harness. Adopted unanimously.
- Live root moved to `~/.local/share/agents-of-anarchy`, old paths symlinked; pointer at 9.1; scribe card at `members/claude-skills/scribe.md`.
- claude-skills dropped peers (`c04cc2b`, `d672897`, `cdea00d`); capabilities updated.

## Open
- Installs of `peers@agents-of-anarchy` 0.4.1 in logins `~/.claude`, `work-a`, `work-b` (meta holds 0.4.0) — owner's manual step; peers carry their cards into `members/` on their next join.
- FAQ face ("Who's in charge?") and culture seed in the repo.
- Society-qualified id `<society>/<project>/<role>` (dc5e4c), deferred; LocalHostName uniqueness across machines unconfirmed; old commons lines keep refs.
- Skills to be rewritten with memento:skill-creation (owner, earlier); the `pi` adapter when pi arrives.

## Where the rest is
`events.md`, `failures.md` absent this span (none diagnosed); recon prompts and agent reports under `recon/2026-10-14/` (disposable).
