## Binding
Loaded from source: first-principles.md ("atoms, not analogies": function over form), self-documenting-code.md (names reveal intent, not implementation), Strunk SPR v3 (omit needless words, active voice). Convergence: name the function, in few words; no tension found.
I must name the function a member performs, not the form or tool, and I will pick a bare act verb; I must not cite a Russian-authored source, and I will not.
I must quote by substring with `file:line`, and I will; I must not decide or edit beyond this output, and I will not.

## Name
`land`

The member's act: land the change. Each commit lands as one revert unit, the session branch lands continuously, main is landed only on the owner's trigger. Plain verb, one syllable, a wink at planes: nothing touches main until it has landed clean.

## Namespace
`dev-discipline:land`. Plugin: `dev-discipline` (engineering discipline, home of `tdd`, `triage-issue`). The folder `dev-discipline/skills/land/` supplies the skill name, the plugin `name` supplies the namespace, as `tdd` resolves to `dev-discipline:tdd`.

## Lens lines
1. self-documenting-code (`/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/self-documenting-code.md:50`): "They should reveal intent, not implementation." `land` shows the intent (change arrives); `version-control`, `rebase-ff` show the tool.
2. Anarchy (`/Users/ryzhakar/.local/share/agents-of-anarchy/culture/roots.md:27`): "i cannot be the part of the society on the same level you guys are." Owner outside, deity: main moves on the owner's word, sessions land their own branches. The name carries no rank and no vote.
3. Peer-to-peer (`/Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/tell/SKILL.md:27`): "Send a peer what affects or helps it in the turn you learn it". Members' skills are short acts (`tell`, `post`, `join`); `land` matches that grain.
4. Namespace (`/Users/ryzhakar/pp/claude-skills/dev-discipline/.claude-plugin/plugin.json:2`): `"name": "dev-discipline",` and (`/Users/ryzhakar/pp/claude-skills/dev-discipline/skills/tdd/SKILL.md:2`) `name: tdd`. Owner's rule (`/Users/ryzhakar/.local/share/agents-of-anarchy/culture/roots.md:6`): "the skill `peers:join` (plugin `peers@agents-of-anarchy`)", so the plugin carries the context and the verb stays bare.

## Clash check
`ls claude-skills/*/skills/ | grep -cx land` = 0; `ls agents-of-anarchy-marketplace/peers/skills | grep -cx land` = 0; `ls ~/.claudes/meta/plugins/cache/*/*/*/skills/ | grep -cx land` = 0.
Same three counts for `commit` = 0, 0, 0; `tidy` = 0, 0, 0; `ship` = 0, 1, 1 (peers:ship exists: protocol-change release skill).

## Struck
Twelve candidates, nine struck:
- `version-control`: owner's "not good enough"; names the tool, not the act.
- `ship`: clashes with `peers:ship`.
- `govern-main`, `main-law`, `merge-assembly`: legislative words.
- `commit-steward`, `main-keeper`: rank.
- `rebase-ff`: implementation, not intent.
- `git-order`: tool plus a decree.
- `session-branch-flow`: hyphen soup, three parts; owner called conformity to hyphens dumb.
Kept: `land`, `commit`, `tidy`.

## Runners-up
1. `dev-discipline:commit`: plain, common, but covers only one third of the orders (branch, main, worktrees go unnamed).
2. `dev-discipline:tidy`: reveals the squash-and-single-line intent with a wink, but hides the main-trigger and worktree rules.

Summary: I propose `dev-discipline:land`, the act a member does when a change arrives on a branch and then on main. It clears the clash check (no `land` anywhere) and avoids `peers:ship`, legislative words, and ranks. Runners-up are `commit` and `tidy`.

## Orchestrator's check of the cites, 2026-10-16T19:31+0300 (appended)
Read verbatim: self-documenting-code.md:50, peers/skills/tell/SKILL.md:27, dev-discipline plugin.json:2 and tdd SKILL.md:2 MATCH. Clash for `land`: 0 in claude-skills, the meta cache and peers/skills. The roots.md cites hold the quoted sentences only at other lines than the agent gave (checked by grep, see the numbers in the journal); the pick rests on the naming lenses, not on those two quotes. dev-discipline holds improve-architecture, receiving-code-review, systematic-debugging, tdd, triage-issue — `land` fits beside them as the act of landing a change.
