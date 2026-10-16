## Binding
Loaded from source: first-principles.md (function over form), self-documenting-code.md (names reveal intent), Strunk SPR v3 (omit needless words). Convergence: a name carries its object and domain; tension: brevity against standing alone, and standing alone wins.
I must test every name alone, with no description, and I will strike any that makes a reader ask "what?"; I must score all nine rules, and I will strike a name that carries one.
I must not cite a Russian-authored source, and I will not; I must not decide or edit beyond this output, and I will not.

## Name
`git-etiquette`

Nine rules: (1) one revert-unit commit per change; (2) records squashed; (3) `type(scope): subject`, at most ten words; (4) zero attribution; (5) never rewrite main; (6) session branch pushed, main on the owner's trigger; (7) rebase then fast-forward; (8) never EnterWorktree; (9) sibling worktrees on wake.
Standalone reading: "how an agent behaves toward the others while using git." Object and domain are in the name; the manners of sharing one repo cover branches, main, worktrees and the shape of a commit. Wink: manners, not law.

## Namespace
`agent-conduct:git-etiquette`. Plugin `agent-conduct`; folder `agent-conduct/skills/git-etiquette/`. Tension named: the plugin line says "independent of ... any specific engineering domain" (`agent-conduct/.claude-plugin/plugin.json:4`); the name puts `git` in the plugin. The owner fixed the namespace; flagged, not resolved.

## Lens lines
All from `grep -n`.
1. `self-documenting-code.md:50`: `Names are your most powerful tool. They should reveal intent, not implementation.`
2. `roots.md:27`: `  > as for me, the "owner", you should consider me as a sort of deity, not a peer who rules you. ...` Main moves on the owner's word; peers keep manners among themselves.
3. `peers/skills/tell/SKILL.md:27`: `Send a peer what affects or helps it in the turn you learn it; never hold it past that turn unless the skill `post` keeps it back.` Conduct toward peers is the grain.
4. `agent-conduct/.claude-plugin/plugin.json:4`: `"description": "Domain-free skills governing how an agent conducts itself while working, ...`
(Paths: manifest dirs `/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/`, `/Users/ryzhakar/.local/share/agents-of-anarchy/culture/`, `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/`, `/Users/ryzhakar/pp/claude-skills/`.)

## Candidates (standalone reading; P pass, S struck)
| # | name | read alone | verdict |
|---|---|---|---|
| 1 | version-control | the tool itself, not conduct | S: names the thing, not the act (owner: not good enough) |
| 2 | keep-version-history | keep the history of versions; of what? | S: object vague, rules 1-2, 5 only |
| 3 | keep-history-clean | clean what history? chat, browser? | S: domain missing |
| 4 | commit-in-revertible-units | commit in units that revert alone | S: rules 1-2 only |
| 5 | work-in-version-history | work inside the history of versions | S: no act a reader can name |
| 6 | git-conduct | conduct in git | P, but repeats the namespace; "conduct" adds nothing |
| 7 | history-etiquette | manners of history? | S: domain missing |
| 8 | branch-and-commit-discipline | discipline of branches and commits | S: "discipline" reads as rank; misses worktrees, main trigger |
| 9 | commit-clean | commit cleanly | S: rules 1-4 only |
| 10 | work-apart | work separately; from whom? | S: rules 6, 8, 9 only |
| 11 | keep-main-clean | keep main clean | S: rules 5-7 only |
| 12 | share-one-history | share one history | S: where? with whom? |
| 13 | version-history-conduct | conduct in version history | P, but long, "history" vague |
| 14 | change-history-keeping | keep the record of changes | S: reads as a records skill (memento) |
| 15 | git-manners | manners in git | P, same as 16 but flip |
| 16 | commit-and-branch-etiquette | manners for commits and branches | S: misses worktrees, main |
| 17 | keep-work-in-history | store work in a history | S: object vague |
| 18 | leave-clean-history | leave a clean history | S: domain missing, rules 1-4 |
| 19 | work-in-worktrees | work in git worktrees | S: rules 8-9 only |
| 20 | record-changes-cleanly | record changes cleanly | S: rules 1-4, "record" clashes with memento's word |
| 21 | git-etiquette | manners toward others while using git | P, covers all nine by domain |
| 22 | keep-git-history-clean | keep the git history clean | P, rules 1-5, 7; 6, 8, 9 absent |
| 23 | share-a-git-repo | share one git repo with others | P, rules 5-9; 1-4 absent |
Twenty-three rows: twenty fresh plus 1 (working title), 21-23 added after the pass.

## Clash check
`ls <dir> | grep -cx -- NAME` over agent-conduct/skills, claude-skills/*/skills, peers/skills, meta plugin cache `*/*/*/skills`. All 23 names return 0, 0, 0, 0. Earlier checks: `settle` 0, 0, 1, 1; `ship` 0, 1, 1 (struck from the earlier files).

## Why not bring-in
Owner: "'bring in' what? bogus." A bare transitive verb with no object fails the standalone test: a model seeing `agent-conduct:bring-in` in a list must ask "what?". Also covers rules 1-7 only through the description, never through the name.

## Struck
`land`, `bring-in`: owner's rejections. Rows 1-5, 7-12, 14, 16-20: see table.

## Runners-up
1. `agent-conduct:keep-git-history-clean`: standalone and clear; leaves rules 6, 8, 9 weak.
2. `agent-conduct:share-a-git-repo`: standalone and clear on the society side; leaves rules 1-4 weak.

Weak spots of the pick: `git-etiquette` carries all nine only by domain. Nothing in the name says "revert unit", "squash", "ten words" or "never EnterWorktree"; "etiquette" reads softer than the orders, and it puts `git` in a plugin that calls itself domain-free.

Summary: I pick `agent-conduct:git-etiquette`, a domain-and-conduct name that passes the standalone test and covers all nine rules by domain. It leaves every rule's strictness to the description and sits against the plugin's "domain-free" line. Runners-up are `keep-git-history-clean` and `share-a-git-repo`; all lens lines are printed from `grep -n` and every name clears the clash check.
