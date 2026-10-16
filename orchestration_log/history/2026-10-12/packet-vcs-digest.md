# Packet digest: version-control rules

## Binding

Loaded whole from source: first-principles.md, self-documenting-code.md, simple-made-easy.md (`/Users/ryzhakar/pp/claude-skills/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/`); Strunk SPR v3 (curl, XML, composition rules read); oath protocol (`manifesto/3.2.0/skills/manifesto-oath/SKILL.md`, injected and read).
Axioms. First principles: keep only the verified; a name is not a source. Self-documenting code: the artifact must teach why; a gloss that drifts is a lie. Simple made easy: simple means not interleaved; accept more parts. Strunk: omit needless words, active voice, concrete terms.
Convergence: one verified fact per row. Tension: re-derivation against brevity, more parts against the 160-line cap. Rule: the cap wins; one claim and one pointer per row; claim and proposal stay in separate sections; a conflict with the repo's CLAUDE.md is a finding, never resolved here.
I must treat every peer rule as a claim, and I will re-count figures from the packet files and the repo and copy quotes by substring with `file:line`. I must read the repo's own rules and practice myself, and I will cite lines or counts for each. I must not decide or edit outside the two outputs, and I will not. I must not cite a Russian-authored source, and I will not.

## Today

1. `/Users/ryzhakar/pp/claude-skills/CLAUDE.md:27-30`: split into atomic parts ("irreducible, not merely motivated together"); split by whether parts "could revert, bisect, or cherry-pick independently"; two artifact classes are two commits unless one part is unintelligible without the other; "Single-line conventional commit messages only, zero attribution."
2. No file states a rule on branches, rebase, merge, force push, push authority, worktrees, or PRs: CLAUDE.md and ETHOS.md contain none (grep). The only adjacent text is `ETHOS.md:25`: "No `gh issue create`, no GitHub-specific workflows", about skill output. "No PRs unless asked" appears in no repo file; the session's tool guidance says commit or push only when asked.
3. Practice, re-counted from `git log -200` on main: 196 subjects are `type(scope): subject`, 2 are unscoped, 2 are PR merge commits (2026-10-06); 17 exceed ten words; 1 body carries a `Co-Authored-By` trailer (3c5ebba, 2026-10-14); 136 of 200 commits carry the author email `noreply@anthropic.com`; 7 merge commits exist in all history. Remote is ssh (`git@github.com:ryzhakar/claude-skills.git`).
4. Layout: main checked out in the repo folder; 46 worktrees listed, 44 under `.claude/worktrees` (agent worktrees), one for this session's `integration/instruction-eval`; 51 local branches.
5. Commons #2 (`extracts/commons-lines.txt:1`) adds a repo-specific rule: run `just readme` before committing any skill change and stop the chain on the first non-zero commit.

## Reports

| file | claim | evidence |
|---|---|---|
| own/vcs-rules-ask.md | scribe asks for owner VCS rules; sibling-witnessed rules take precedence | :3-8 |
| own/vcs-rules-answers.md | 7 peer entries (re-counted); no rule has a living sibling witness | entries :3, :9, :15, :17, :18, :20, :21 |
| own/vcs-rules-synthesis.md | 10 topic tables, 10 conflicts, missing list; "about 70 rules" | re-count: 78 rows, 50 distinct ids; summary :194 |
| own/vcs-rules-synthesis-brief.md | brief to the synthesizer; no recommendations | :4, :17 |
| own/branch-model.md | 8 branch rules, this repo only, relayed by resident-anarchist | :1-12 |
| peers/product-catalog-storage-api-vcs-rules-answer.md | charter Commits text; owner words on squash, rebase, PR branch; #50 overruled, #53 stands | :7, :17-19, :24 |
| peers/memento-vcs-rules-answer.md | "remote is always ssh"; no rm/stash; ten-word subjects; never push without owner | :6, :10-13 |
| peers/embedding_finetuning_for_ecommerce-vcs-rules-answer.md | `type: subject` at most ten words; rebase then fast-forward; never EnterWorktree; squash 65 to 9 | :5-12 |
| extracts/journal-lines.txt | owner's 17:25 ask; main force-pushed at 15:55; branch model "adopted by own ground" | :4, :10, :12 |
| extracts/commons-lines.txt | commons #2 (`just readme`), #26 (EnterWorktree branches from origin/main), #78 (fold with rebase) | :1, :12, :27 |

## Proposed rules

W = witness: none exists for any rule, so grade and date rank them (synthesis:22). "Conflict" is against `CLAUDE.md:27-30`, ETHOS, or measured practice.

**R1. Branch model: main fast-forward only and never rewritten; one integration branch per session; work and records go to it, never to main; `draft/*` for drafts** (own/branch-model.md:5-7, :11). Peers: product-catalog agrees that deferrals belong on the PR branch (PC:20); embedding runs an integration branch (MT:12); machine-setup commits straight to main, no branches (own/vcs-rules-answers.md:9, row for MS); gym holds none. Drafted status: this repo only, `:3` leaves reach to the owner; adopted "by own ground" (E1 :10). Conflict: practice, since this repo commits to main today (HEAD d82db60 on main); and BM1's named host feature, a GitHub ruleset (`branch-model.md:5`), conflicts with ETHOS:25 if the text enters a skill.

**R2. Integration at close or on trigger: fetch, rebase on origin/main, gate, fast-forward main, push; the second integrator rebases** (branch-model.md:9). Agrees: embedding units rebase then `merge --ff-only` (MT:12); product-catalog rebases the feature onto pushed main (PC:19). Differs: push authority (R7). No conflict with CLAUDE.md; the gate command is project-specific.

**R3. Rebase, never merge; no cherry-pick; no merge into a PR branch** (MT:6; PC:19). Commons #50 (merge main in) is retired by the owner's word (own/vcs-rules-answers.md:15); #53 stands. Conflict: practice shows 2 PR merge commits in the last 200 (2026-10-06); PR-branch rules presuppose PRs, which no repo file mentions and ETHOS:25 steers skills away from.

**R4. Force push: lease-guarded after rebase of a feature or PR branch (#53); never on main; reshuffle own branch freely** (branch-model.md:5, :8; PC:24). Peers: product-catalog "never rewrite pushed history of a worker branch" is practice (PC:28); embedding and others hold no ruling (own/vcs-rules-answers.md:21). Conflict inside the packet: main was rewritten and force-pushed on the owner's word at 15:55, then declared never-rewritten at 16:08 (E1 :4; branch-model.md:1). CLAUDE.md is silent.

**R5. Commit form: one line; zero attribution; name every path.** Peers differ: `type: subject`, at most ten words (MT:5; ten words also ME:11); `type(scope): subject` (own/vcs-rules-answers.md:17, gym); "single-line conventional" (PC:7, the same text as `CLAUDE.md:30`, matched by substring). Conflicts with practice: the unscoped form (196 of 200 are scoped) and the ten-word cap (17 of 200 exceed it); "zero attribution" already fails once (3c5ebba), and author identity is `noreply@anthropic.com` on 136 of 200. Explicit-path rule (MT:7, PC-C) fits; no conflict.

**R6. Atomicity and records commits.** Proposed units: one per scope (MT:6), per batch (gym), per kind (PC-P), per kind per day (own/vcs-rules-answers.md:20), fold into HEAD (ME-P), squash by meaning (PC:17), objection to per-line journal commits (MT:11). Conflicts: "squashed to their minimum possible linear commits" (own/vcs-rules-answers.md:20) pulls opposite to "irreducible" (`CLAUDE.md:27`); one commit per kind per day and 80-to-2 merge parts that could revert independently (`CLAUDE.md:28`); banning per-record-edit commits (MT:6) can contradict `CLAUDE.md:28` when each edit reverts alone; joining a scope's records with its work contradicts `CLAUDE.md:29`. Agrees: records separate from work (PC:28, `CLAUDE.md:29`).

**R7. Push authority and remotes.** Never push without the owner (own/vcs-rules-answers.md:17, gym; ME:13) against "push it continuously" for the own branch (branch-model.md:8) against "i push as i see fit" (own/vcs-rules-answers.md:5); one push, one yes (ME:7). "The remote is always ssh, everywhere" (ME:6) matches this repo's remote. Conflict: continuous push against the session's tool guidance to push only when asked; CLAUDE.md is silent.

**R8. Worktrees and deletions.** One worktree per guest, prune after moving untracked files by hand (branch-model.md:6, :12); collapse to one feature worktree (PC:18); never call EnterWorktree (MT:8); no `rm`, `rmdir`, `git clean`, `git stash` (ME:10). Conflicts: MT:8 against this marketplace's own implementer and executor agents, which run "inside its own git worktree" and left 44 agent worktrees here; ME:10 against pruning (branch-model.md:12), which the synthesis marks owner's call (synthesis:168).

## Conflicts

1. Rule count: "about 70" (synthesis:194) against 78 rows and 50 distinct ids; the brief says eight member sessions answered (synthesis-brief:4) while the answers file holds 7 entries.
2. #50 retirement: owner word 2026-10-15T01:14 (own/vcs-rules-answers.md:15) against a commons edit 2026-10-16T12:56 (PC:24); same fact, two stamps.
3. Reach of the charter text: synthesis marks PC-A ONE project (synthesis:85); the text is verbatim in this repo's `CLAUDE.md:27-30`, so at least two.
4. Grading: branch-model rules get G3 (synthesis:30) while RA-squash, from the same journal, gets G1 (synthesis:99).
5. Witness: the owner ordered sibling-witnessed rules first (E1 :12); product-catalog has no sibling by construction (PC:3), embedding's d7 weakly shared a file (MT:3); the order ranks nothing.
6. Subject form: `type:` (MT:5), `type(scope):` (gym), ten words (MT:5, ME:11), none (PC:7); the synthesis marks it owner's call (synthesis:160).
7. Main rewrite: PC1 and RA-squash against BM1 (synthesis:162); E1 :4 shows the rewrite happened.
8. Synthesis finds "No conflict found on rebase over merge" (synthesis:171); repo history holds 2 PR merges in the last 200.
9. PC4 graded G1 on a date-only stamp (synthesis:35; PC:20).

## Unmeasured

- Whether the owner's typed words match the journals' paraphrases: only 3 of the answers carry transcript or journal verbatim (own/vcs-rules-answers.md:3, :9, :15).
- Whether the GitHub ruleset in BM1 exists; the packet only claims it.
- Whether any rule reached any project beyond the one that heard it.
- Compliance rates per project; only this repo's practice was counted here.
- Tags, branch naming and deletion, PR merge method, signing, conflict policy, who may integrate (synthesis:173-190).
- Whether author identity counts as attribution.
- How many of the 44 agent worktrees are live.

## Particulars for the owner

1. How far does a rule reach? (a) Every project gets the whole branch model. (b) Only the rules recurring in three or more projects (rebase then fast-forward, no attribution, atomic one-line commits) go everywhere; the rest stay per project. (c) Nothing spreads. Pick (b): spreading ME:10 or MT:8 would break this repo's agents.
2. May main ever be rewritten? (a) Never. (b) Only before its first push, with a backup ref. (c) Whenever you order it. Pick (b): it fits the squashes you ordered before a push and keeps the ruleset sound.
3. Which governs commit count, "minimum possible linear commits" or "irreducible" atomic? (a) CLAUDE.md. (b) The squash order, for records. (c) Atomic for work, one per kind per day for records. Pick (c): records are an artifact class, so a kind-day group reverts together.
4. Commit subject form? (a) Keep "single-line conventional". (b) Add a ten-word cap. (c) Cap and unscoped `type:`. Pick (a): 196 of 200 commits are scoped; 17 would break a cap.
5. Who pushes? (a) Never without your word, per push. (b) The session branch continuously, main only on trigger. (c) Per project. Pick (b): it matches the branch model and your word on main.
6. Does an author email of `noreply@anthropic.com` break "zero attribution"? (a) No, only trailers and PR text. (b) Yes, set your own identity. Pick (a): the setting you approved, `"attribution": false`, governs trailers (own/vcs-rules-answers.md:11).
