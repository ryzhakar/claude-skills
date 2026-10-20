# agent-conduct

Domain-free skills governing how an agent conducts itself while working, independent of orchestration, memory, or any specific engineering domain.

`conduct` `behavior` `output-discipline` `silence` 
## Skills

### [check-back](skills/check-back/SKILL.md)

Before ending a turn that leaves a run pending, set the agent's own next wake, and on waking look at what was pending. "check back", "check back in 10 minutes", "wake up when it's done", "keep an eye on the build", "wait for the agents", "don't lose track of background work", "pick up after a resume", or any turn about to end while a background command, a background agent, or an external wait is still running.


---

### [decide-while-away](skills/decide-while-away/SKILL.md)

Settle the owner's decisions while the owner is away: decide each reversible choice, write it beside its single closest alternative, act on it, and leave each choice that cannot be undone unsolved in a queue. Use when a step needs a decision that is the owner's to make and the owner has not given it, while the owner is away, outside a round of questions; never at any other moment.


---

### [git-etiquette](skills/git-etiquette/SKILL.md)

Commit, push, and integrate with git: revertible commits, ten-word subjects, zero attribution, a linear main, one worktree per sibling session. "commit this", "push it", "integrate to main", "rebase on main", "squash the records", "make a worktree", "open a PR", or any turn about to run a git command that writes history, moves a branch, or creates a worktree.


---

### [office-hours](skills/office-hours/SKILL.md)

Hold an office-hours round: one event in which the owner answers the questions the agent queued. "office hours", "questioning round", or an agent about to ask whether the owner is present for a round; never a one-off question mid-task.


---

### [work-silently](skills/work-silently/SKILL.md)

Keep working while writing nothing to the conversation, ending every turn with an empty message, until the user says to stop. Use when the user says "/work-silently", "go silent", "back to silence", "work in silence", "don't write anything until I write", "nothing but tool calls", "stay quiet and keep going", or any request to keep working without writing to the conversation.


---

### [write-well](skills/write-well/SKILL.md)

Write all prose by Strunk's rules of grammar, composition, and usage, and reread each draft against them, most serious fault first. Use when the user says "/write-well", "write-well", "write well", or asks for prose held to Strunk's rules.


---

