---
name: git-etiquette
description: >
  Commit, push, and integrate with git under the owner's version-control orders: revertible commits, ten-word subjects, zero attribution, a linear main, one worktree per sibling session.
  "commit this", "push it", "integrate to main", "rebase on main", "squash the records", "make a worktree", "open a PR", or any turn about to run a git command that writes history, moves a branch, or creates a worktree.
---

<commit-what-reverts-together>
Commit together exactly the changes you would revert together; never join changes that revert apart.

Commit source code and records, such as journals and status files, apart; never in one commit.

Squash records commits on your own branch to the fewest commits; never commit records one entry at a time.

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
<parameter name="command">git commit -m "doc(journal): add 14:05 entry" records/journal.md && git commit -m "doc(journal): add 14:20 entry" records/status.md</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git commit -m "doc(journal): log build wakes" records/journal.md records/status.md</parameter>
</invoke>
</do_exactly_this>
</commit-what-reverts-together>

<write-a-ten-word-subject>
Write each message as one line `type(scope): subject` of at most ten words; never a body, a second line, or an eleventh word.

Add zero attribution; NEVER write a trailer, a co-author line, or pull-request text naming the tool.

Leave the configured author in place; the author email noreply@anthropic.com is not attribution.

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

Move main by rebasing your branch on `origin/main`, then fast-forwarding main to it; never by a merge commit.

<never_do_this reason="main rewritten">
<invoke name="Bash">
<parameter name="command">git fetch origin && git rebase origin/main && git switch main && git merge integration/parser && git push --force origin main</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git fetch origin && git rebase origin/main && git switch main && git merge --ff-only integration/parser && git push origin main</parameter>
</invoke>
</do_exactly_this>
</keep-main-linear>

<push-the-session-branch>
Commit on your session's own branch; never on main.

Push your session branch after each commit; never leave a commit unpushed.

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

A sibling session is a concurrent session in the same project that you did not launch as a teammate.

Check on waking whether another session works in the project; never assume you are alone.

Claim the project folder when no other session works there; create your own worktree with git when one does.

<never_do_this reason="tool-made worktree">
<invoke name="EnterWorktree">
<parameter name="name">parser</parameter>
</invoke>
</never_do_this>

<do_exactly_this>
<invoke name="Bash">
<parameter name="command">git worktree add -b integration/parser /Users/dev/project.worktrees/parser</parameter>
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
