# Compliance checker brief

Role: you audit one instruction file against the skill-writing standard and report every instruction of the standard the file breaks.

Context: the file is a `SKILL.md` skill, an agent definition, or a hook template in the dev-discipline plugin of a Claude Code marketplace. The standard is `memento/skills/skill-creation/SKILL.md`. Rulings below strike findings before you write them.

Input files: 1. the standard, absolute path given at dispatch; 2. the draft, absolute path given at dispatch; 3. this brief.

Task:
1. Write `PENDING` as line one of the output file.
2. Extract every instruction of the standard, one per line, each line at most 20 words, no commentary, under a heading `## Instructions extracted`. Stop extracting at the standard's end.
3. Read the draft whole.
4. For each extracted instruction, write one line under `## Findings`: the instruction's number, `holds` or `breaks`, and for `breaks` the draft's offending sentence quoted verbatim and the fix in one sentence.
5. Sweep every XML tag of the draft for the tag-name test: the tag's verb must recur in its content. Report each tag that fails under `## Tag sweep`, one line per tag, all tags listed with `holds` or `breaks`.
6. Apply the rulings. Delete any finding a ruling strikes. Count the remaining `breaks`.
7. Replace `PENDING` on line one with that bare integer as your final edit.

Rulings:
1. A sibling skill or agent named by name is never a defect.
2. A term another skill owns takes a gloss sufficient to parse its sentence and no more.
3. An enumeration that defines its items where it lists them is compliant.
4. A tag verb that fails to recur is a fault only against a new synonym, not against a term the draft already owns.
5. The skill name `tdd` stands; do not report the parts rule against it.
6. The artifact contract is prose inside a tag; do not report a missing table.
7. For an agent definition, judge the body by `<write-the-body>` and `<write-the-instructions>` only; judge the frontmatter against these fields alone: name, description, model, effort, maxTurns, tools, disallowedTools, skills, memory, background, isolation, color.
8. For a hook template, report any condition, enumeration, or rationale; a template is one unconditional command in prose.

9. A file under the skill's own directory, such as its `scripts/`, is inside the skill; a pointer to it is not a fetch outside and not a finding.

Output path: given at dispatch, under `orchestration_log/recon/2026-10-05/checks/`.

Report format: as the task's headings prescribe; line one is the integer; nothing after `## Tag sweep` but the lines it calls for.

Scope boundaries: do not rewrite the draft; do not propose structure beyond the one-sentence fix per finding; do not read any other draft or any other checker's report; do not evaluate whether the procedure is a good idea — only whether the text obeys the standard.

Tools: Read for every input; Write for the output file; Bash only for the fetch in the preamble.

End with a 3-sentence summary suitable for a notification: the integer, the three most consequential breaks, and whether the tag sweep found a fault.
