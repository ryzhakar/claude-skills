---
name: git-etiquette
description: >
  Commit, push, and integrate with git: revertible commits, ten-word subjects, zero attribution, a linear main, one worktree per sibling session.
  "commit this", "push it", "integrate to main", "rebase on main", "squash the records", "make a worktree", "open a PR", or any turn about to run a git command that writes history, moves a branch, or creates a worktree.
---

<commit-what-reverts-together>
Commit together exactly the changes you would revert together; never join changes that revert apart.

Commit source code and records, such as journals and status files, apart; never in one commit.

Squash records commits at your branch's tip into one: `git reset --soft` to the commit before the first, commit, then push the session branch with `--force-with-lease`; never commit records one entry at a time.

<never_do_this reason="fix and journal revert as one">
<invoke name="Bash">
<parameter name="command">git add src/parser.py records/journal.md && git commit -m "fix(parser): accept empty input"</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git add src/parser.py && git commit -m "fix(parser): accept empty input" && git add records/journal.md && git commit -m "doc(journal): log parser fix"</parameter>
</invoke>
</do_exactly_this>

<never_do_this reason="records history in slices">
<invoke name="Bash">
<parameter name="command">git add records/journal.md && git commit -m "doc(journal): add 14:20 entry" && git push origin integration/parser</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git add records/journal.md && git reset --soft HEAD~1 && git commit -m "doc(journal): log build wakes" && git push --force-with-lease origin integration/parser</parameter>
</invoke>
</do_exactly_this>
</commit-what-reverts-together>

<write-a-ten-word-subject>
Write each message as one line `type(scope): subject` of at most ten words; never a body, a second line, or an eleventh word.

Add zero attribution; NEVER write a trailer, a co-author line, or pull-request text naming the tool.

Leave the configured author in place, noreply@anthropic.com included; never count the author email as attribution.

<never_do_this reason="subject past ten words">
<invoke name="Bash">
<parameter name="command">git commit -m "fix(parser): handle the empty input case so the lexer stops crashing on blank files"</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git commit -m "fix(parser): accept empty input"</parameter>
</invoke>
</do_exactly_this>

<never_do_this reason="attribution trailer">
<invoke name="Bash">
<parameter name="command">git commit -m "fix(parser): accept empty input" -m "Co-Authored-By: Claude <noreply@anthropic.com>"</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git commit -m "fix(parser): accept empty input"</parameter>
</invoke>
</do_exactly_this>
</write-a-ten-word-subject>

<keep-main-linear>
NEVER rewrite main or force-push it.

Move main by rebasing your branch on `origin/main`, then fast-forwarding it with `git push origin <branch>:main`; never by a merge commit or `git switch main`.

<never_do_this reason="main rewritten">
<invoke name="Bash">
<parameter name="command">git fetch origin && git push --force origin integration/parser:main</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git fetch origin && git rebase origin/main && git push origin integration/parser:main</parameter>
</invoke>
</do_exactly_this>
</keep-main-linear>

<push-the-session-branch>
Commit on your session's own branch; never on main.

Push your session branch after each commit; never leave a commit unpushed.

<never_do_this reason="commit left unpushed">
<invoke name="Bash">
<parameter name="command">git commit -m "fix(parser): accept empty input"</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git commit -m "fix(parser): accept empty input" && git push origin integration/parser</parameter>
</invoke>
</do_exactly_this>

Move main only on a trigger the owner sets; never on your own judgment.

<never_do_this reason="main moved without trigger">
<invoke name="Bash">
<parameter name="command">git push origin integration/parser main</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git push origin integration/parser</parameter>
</invoke>
</do_exactly_this>
</push-the-session-branch>

<one-worktree-per-sibling-session>
NEVER use the EnterWorktree tool.

Treat as a sibling any concurrent session in the project that you did not launch as a teammate; never treat a teammate you launched as one.

Run `git worktree list` and `git status --short` in the project folder on waking; count a checked-out session branch or a dirty tree there as another session.

Claim the project folder when no other session works there; create your own worktree with git when one does; never share the folder.

<never_do_this reason="tool-made worktree">
<invoke name="EnterWorktree">
<parameter name="name">parser</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git worktree list && git status --short && git worktree add -b integration/parser /Users/dev/project.worktrees/parser</parameter>
</invoke>
</do_exactly_this>
</one-worktree-per-sibling-session>

<publish-through-git-alone>
Open no pull request unless the owner asks; never file an issue or call a hosting platform's tools.

<never_do_this reason="unasked pull request">
<invoke name="mcp__github__create_pull_request">
<parameter name="head">integration/parser</parameter>
<parameter name="base">main</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git push origin integration/parser</parameter>
</invoke>
</do_exactly_this>
</publish-through-git-alone>
