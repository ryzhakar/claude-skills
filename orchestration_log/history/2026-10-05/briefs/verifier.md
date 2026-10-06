# Verifier brief

Role: you verify the finished dev-discipline change without having written any of it, and report every check that fails.

Context: the plugin at `dev-discipline/` under the project root was rewritten on branch `claude/dev-discipline-iteration-yby2xn`. The plan is `orchestration_log/history/2026-10-05/reviews/dev-discipline-iteration-plan.md`.

Input files: the plan; every file under `dev-discipline/`; `.claude-plugin/marketplace.json`; `justfile`; `README.md`; `dev-discipline/README.md`.

Task, each step one line under `## Checks` reading `PASS` or `FAIL` with the evidence:
1. `cd` to the project root and run `just hooks-test`; record the exit code and the final summary line.
2. Run `claude plugin validate dev-discipline`; record the exit code and output.
3. Run `just check-readmes`; record the exit code.
4. Count tokens of every file in plan §2 with `node /tmp/claude-0/-home-user/de2fb84f-005b-59e0-acc4-2127576d4b64/scratchpad/tok/count.js <files>`; compare each against its ceiling; a file over its ceiling is a FAIL line naming the overage.
5. Grep every skill and agent body for backticked names of skills and agents; confirm each resolves to a directory under `dev-discipline/skills/`, a file under `dev-discipline/agents/`, or a skill under `orchestration/skills/` or `agent-conduct/skills/`; a name that resolves nowhere is a FAIL.
6. Parse each agent's frontmatter; confirm every key is one of name, description, model, effort, maxTurns, tools, disallowedTools, skills, memory, background, isolation, color; confirm `isolation` is `worktree` where present and `skills` entries are `plugin:skill` form.
7. Grep `dev-discipline/hooks/*.py` and `dev-discipline/skills/**/*.sh` for `#` lines other than the shebang; any is a FAIL.
8. Grep every `SKILL.md` body for `|---`, three backticks, `# `, `- ` at line start, and `**`; any inside a tag is a FAIL.
9. Grep every `SKILL.md` and agent frontmatter for `version:`; any is a FAIL.
10. Confirm `plugin.json` and `marketplace.json` carry the same dev-discipline version.
11. Confirm `hooks.json` parses as JSON and every `command` path it names exists under `dev-discipline/hooks/`.
12. Feed `review-chain.py` one SubagentStop input with `agent_type` `dev-discipline:implementer` then one Stop input, with `CLAUDE_PLUGIN_DATA` set to a temp dir; confirm the Stop output is JSON carrying `hookSpecificOutput.additionalContext` that contains the word `spec-reviewer`.

Output path: given at dispatch. Line one `PENDING`, replaced by the count of FAIL lines as your final edit.

Scope boundaries: change nothing; report only.

Tools: Bash, Read, Grep, Glob; Write for the output.

End with a 3-sentence summary suitable for a notification.
