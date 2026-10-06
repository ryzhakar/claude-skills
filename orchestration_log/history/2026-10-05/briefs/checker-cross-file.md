# Cross-file contradiction checker brief

Role: you hold every shipped instruction file of the dev-discipline plugin at once and report each place where two files disagree.

Context: eleven instruction files — seven skills, three agents, three hook templates — plus `hooks.json` and `hooks/review-chain.py`. Each was checked alone and passed; what no single-file check can reach is a disagreement between two of them.

Input files: every path under `dev-discipline/skills/*/SKILL.md`, `dev-discipline/agents/*.md`, `dev-discipline/hooks/templates/*.txt`, `dev-discipline/hooks/hooks.json`, `dev-discipline/hooks/review-chain.py`, given as absolute paths at dispatch.

Task:
1. Write `PENDING` as line one of the output file.
2. Read every input whole.
3. Under `## Vocabulary`, list every term two or more files define, with each file's definition quoted; mark `DIFFERS` where the definitions disagree.
4. Under `## Paths`, list every artifact path any file names, with the files that name it; mark `DIFFERS` where two files give the same artifact different paths or the same path different producers or consumers.
5. Under `## Handoffs`, for each pair producer → consumer (plan → implementer, implementer → spec-reviewer, spec-reviewer → code-quality-reviewer, code-quality-reviewer → orchestrator, hook → orchestrator), list what the producer says it hands over and what the consumer says it receives; mark `DIFFERS` on any mismatch of field, format, or path.
6. Under `## Statuses and verdicts`, list every status word and verdict line any file emits or reads; mark `DIFFERS` where a reader expects a value no writer emits or a writer emits a value no reader handles.
7. Under `## Matchers`, compare each `hooks.json` matcher with the agent names in `agents/*.md` and the agent types `review-chain.py` tests; mark `DIFFERS` on any that cannot match.
8. Under `## Findings`, one line per `DIFFERS`: the two files, the two quotes, the one change that reconciles them.
9. Replace `PENDING` with the count of findings as your final edit.

Output path: given at dispatch.

Scope boundaries: report disagreements only; a rule stated in one file and absent from another is not a finding; do not rewrite any file.

Tools: Read, Grep, Glob for inputs; Write for the output; Bash only for the fetch in the preamble.

End with a 3-sentence summary suitable for a notification.
