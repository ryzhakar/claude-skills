## Binding
Loaded from source: first-principles.md (function over form), self-documenting-code.md (names reveal intent), Strunk SPR v3 (omit needless words). Convergence: name the whole function in few words; tension: one name never carries nine rules, so I score coverage and pick the best.
I must test each name against all nine rules, and I will strike a name that covers one; I must print each cited line verbatim from `grep -n`, and I will.
I must not cite a Russian-authored source, and I will not; I must not decide or edit beyond this output, and I will not.

## Name
`bring-in`

The skill's whole job, nine rules: (1) one revert-unit commit per change; (2) records squashed to the minimum; (3) subject `type(scope): subject`, at most ten words; (4) zero attribution; (5) never rewrite or force-push main; (6) session branch pushed continuously, main moved only on the owner's trigger; (7) rebase then fast-forward; (8) never EnterWorktree; (9) sibling sessions each make a worktree on wake.
`bring-in` coverage: 1-7 directly (a change is brought in clean, as units, without a trace of the tool, onto a main nobody rewrites); 8-9 weakly (where you work while bringing it in). 7 of 9, best of the field. Siblings' grain: `check-back`, `work-silently` are bare imperative acts, two plain words. `bring-in` is the same; wink: you bring it in like the washing, folded.

## Namespace
`agent-conduct:bring-in`. Plugin `agent-conduct` ("Domain-free skills governing how an agent conducts itself while working"); the folder `agent-conduct/skills/bring-in/` supplies the name.

## Lens lines
All printed from `grep -n`.
1. Code Speaks, `/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/self-documenting-code.md:50`: `Names are your most powerful tool. They should reveal intent, not implementation.`
2. Anarchy, `/Users/ryzhakar/.local/share/agents-of-anarchy/culture/roots.md:27`: `as for me, the "owner", you should consider me as a sort of deity, not a peer who rules you.` (main moves on the owner's trigger; peers bring in their own work.)
3. Peer-to-peer, `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/tell/SKILL.md:27`: `Send a peer what affects or helps it in the turn you learn it; never hold it past that turn unless the skill `post` keeps it back.` Short act verbs; the same continuous handing-on as the session branch push.
4. Namespace, `/Users/ryzhakar/pp/claude-skills/agent-conduct/.claude-plugin/plugin.json:4`: `"description": "Domain-free skills governing how an agent conducts itself while working, ...` and `:2` `"name": "agent-conduct",`. Siblings' folders: `check-back`, `work-silently`.
Owner's words (brief): "peers:<verb> is great. you can make good exceptions from that when needed, but conformity to hyphens and other stuff is dumb." Named for the act, never a rank; no legislative word.

## Clash check
Command per name: `ls <dir> | grep -cx -- NAME` over agent-conduct/skills, claude-skills/*/skills, peers/skills, meta plugin cache `*/*/*/skills`.
`bring-in`, `commit-clean`, `work-apart`, `keep-history`, `leave-no-trace`, `work-linearly`: 0, 0, 0, 0 each. `settle`: 0, 0, 1, 1 (peers:settle). `sync`, `stage`, `hand-in`, `tidy`, `keep`, `trunk`, `pass-on`, `lodge`, `file`, `bank`, `send`: 0 everywhere.

## Why not land
The owner rejected it ("THE NAME WAS BOGUS"). It names only the last step, reaching main, which is rules 6-7 of nine; commits, records, subject, attribution and worktrees go unnamed. It fits the old plugin `dev-discipline` and not this grain: `check-back` and `work-silently` name a whole conduct, not an endpoint.

## Struck
Twelve candidates, ten struck:
- `land`: owner's rejection, one-endpoint name.
- `settle`: clashes with `peers:settle`.
- `commit-clean`: rules 1-4 only; silent on branches, main, worktrees.
- `work-apart`: rules 6, 8, 9 only; silent on commit form.
- `work-linearly`: rules 5, 7 only.
- `keep-history`: names the artifact, not an act; covers 2, 5.
- `leave-no-trace`: rule 4 only, and wrong for records.
- `tidy`, `sync`: one rule (squash; fetch), or implementation.
- `hand-in`, `pass-on`: read as delivery to a peer, which `peers:tell` owns.
Kept: `bring-in`.

## Runners-up
1. `agent-conduct:commit-clean`: sibling grain (verb plus manner), but covers 4 of 9.
2. `agent-conduct:work-apart`: sibling grain (`work-silently` shape), but covers 4 of 9.

Summary: I propose `agent-conduct:bring-in`, a bare act in the siblings' grain that covers seven of the nine rules directly and the worktree two weakly. `land` is struck and explained: it names one endpoint. All cited lines are printed verbatim from `grep -n`, and the clash checks show no `bring-in` in agent-conduct, claude-skills, peers or the cache.
