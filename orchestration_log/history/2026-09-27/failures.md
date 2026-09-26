## Orchestrator wiped uncommitted work with an unsplit shell variable (2026-09-27)

A staging script ran `for p in $paths` under zsh, which does not word-split unquoted variables. The loop copied nothing to the backup directory, `set -e` did not stop it, and the next lines ran `git checkout -- .` and `git clean -fd` on the real tree. Every uncommitted file from two agents was destroyed. Recovery: resume each agent by message, since each still held its edits in context.

Derived rule: never run a destructive git command in the same script as the backup it depends on. Verify the backup exists and is non-empty, then destroy, as separate steps. Use arrays, never a space-joined string, for path lists in zsh.
