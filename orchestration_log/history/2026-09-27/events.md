# Events 2026-09-27

- decision (owner): work-silently reviewed; fixed to persist via `.claude/work-silently` marker and a SessionStart hook; merged to main as agent-conduct 1.1.0. PR #1 closed unmerged by ruling.
- decision (owner): `check-back` extracted from agentic-delegation into agent-conduct; its subject is the agent itself, never other agents. Stop hook tried by ruling. agent-conduct 1.2.0.
- decision (owner): plugins declare dependencies. orchestration → agent-conduct; dev-discipline, qa-automation → orchestration.
- decision (owner): orchestration untied from memento — every mention removed, `session-close` and `session-checkpoint` stubs deleted. Version 5.0.0 by ruling.
- decision (owner): a silent turn ends with the empty string. agent-conduct 1.2.1.
- failure: unsplit zsh variable in a staging script wiped uncommitted work; recovered by resuming agents. See failures.md.
- discovery: plugin dependencies are live on Claude Code 2.1.283 (feature since 2.1.143); isolated install of dev-discipline pulled both dependencies. The owner's real install holds orchestration 4.3.1 and dev-discipline 2.0.2, predating the field — declarations inert there until updated.
- discovery: this repo has no `.claude/memento.yaml`; the shipped default homes records under `docs/`, which this repo does not use, so its `orchestration_log/` records sit at homes the schema does not declare.
- discovery: `decisions.md` was retired for `architecture_log.md` before this stretch; a ruling appended to the retired path recreated it and was moved.
