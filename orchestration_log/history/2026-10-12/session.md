# Session digest — instruction-eval plugin (interim, written 2026-10-15T13:07+0300 before compaction)
Lossy by construction; events in events.md, failures in failures.md, frozen design and spec beside this file.

## What this span is
Building the `instruction-eval` plugin (evaluate and iterate any LLM instruction) from the LLM_MANIFESTOS digest-eval skills and CLI. Frozen design: instruction-eval-design-language.md; spec: instruction-eval-spec.md (129 requirements). Plan: recon/2026-10-14/plans/instruction-eval.md (88 units, 9 waves, ignored by git, on disk).

## State (2026-10-15T13:07+0300)
Branches in /Users/ryzhakar/pp/claude-skills.worktrees/instruction-eval: `claude/instruction-eval` (journal) and `integration/instruction-eval` (code; 629 tests green after wave 2). Unit branches `worktree-agent-<id>` live in /Users/ryzhakar/pp/claude-skills/.claude/worktrees/agent-<id>. Done: wave 1, wave 2 (17 units). Running: batch A (record-loader, series-guard, expected-replies; opus implementer aaf8bda097c84a8a5). Next: batches B (brief-render, verdict-validate, packet-build), C (reply-rows, gate-checks, keep-rank), D (condition-texts, transcript-screen), then waves 4-9, the 11 skills (instruction-writer on opus, never implementers), release. Live status: recon/2026-10-14/dev-status.md; queue and carry-forward in recon/2026-10-14/{recovery-queue,carry-forward}.md.

## Rules in force
One agent at a time (the account's usage limit is shared; two limit deaths happened). Never block on the owner: decide reversible choices from the owner's standing words ("figure this out amongst yourselves", "use tokens sparingly!", protocol 9.3), record them. Owner questions only through AskUserQuestion, in terms the owner recognizes. Skills authored by instruction-writer. Orchestrator reads and writes memento records itself (owner ruling); everything else goes to agents.

## Mechanics learned
- Review loop per batch: implementer → fresh dev-cycle:spec-reviewer → dev-cycle:code-quality-reviewer → implementer fixes → merge by a general-purpose integrator briefed with recon/2026-10-14/prompts/integrator.md. Reviewers and implementers resume by SendMessage across logins.
- Check `git branch --show-current` in each unit worktree before reviews and merges; resumed implementers once committed on a detached HEAD (fixed with `git checkout -B <branch>` after an ancestor check).
- The dev-cycle review-chain Stop hook repeats for units whose loop the orchestrator already owns; clear it with `jq '.pending = []'` on $CLAUDE_CONFIG_DIR/plugins/data/dev-cycle-my-claude-skills/review-chain/$CLAUDE_CODE_SESSION_ID.json.
- Login now /Users/ryzhakar/.claudes/meta; ref 1f3ba5; member card ~/.local/share/agents-of-anarchy/members/claude-skills/instruction-eval.md (loaded peers skill 9.2, pointer 9.3, `machine` set); a reload applies 9.3.

## Open
Six platform checks (PR3 4 5 9 13 14) need the owner's one /login in the neutral login; nothing waits on them. Carry-forward: unify the three refusal types in records.py; GateCheck rename; the R106 check lands in cli-dispatch; ScoredReply contract for reply-rows; token cost keys; locate_transcripts takes working_dir.
