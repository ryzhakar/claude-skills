# dev-cycle-lite

Cost-tiered development cycle over dev-cycle: an opus prescriber writes prescriptions that leave no decision, a sonnet suborchestrator runs the loop and both reviews, disposable haiku executors follow the prescription literally. No hooks.

`orchestration` `lifecycle` `prescriptive-planning` `haiku` `cost` 
## Skills

### [lite-cycle](skills/lite-cycle/SKILL.md)

Run the dev-cycle loop over one spec at the lowest cost tier — an opus prescriber writes a prescription per unit, disposable haiku executors follow it literally, and the suborchestrator running this skill reviews each unit itself and integrates. "run the lite cycle", "implement this cheaply", "implement with haiku executors", "prescribe and execute", or any dev-cycle run the user marks lite in the dispatch.


---

### [prescriptive-planning](skills/prescriptive-planning/SKILL.md)

Write a prescription — an implementation prescription, or a correction prescription after a failed review — that leaves the executor — the agent that will execute it — no decision, no option, no signature to invent, and no unverifiable step. "write a prescription", "prescribe the implementation", "write the plan for the executor", "correction prescription", "the executor cut corners", or any request for a plan the executor will execute literally.


---

## Agents

### [executor](agents/executor.md)

Execute one prescription — a plan fixing every file, signature, test, and command — literally, inside its own git worktree, and report. Use it in the lite cycle for every unit; discard it after its report. Examples:

<example>
Context: The lite cycle has a prescription on disk for a unit.
user: "Execute briefs/prescriber-invoice-export.md"
assistant: "I'll launch the executor agent with the prescription path and the integration branch."
</example>

<example>
Context: A correction prescription was written after a failed review.
user: "Run the correction prescription"
assistant: "I'll launch a fresh executor agent with the correction prescription."
</example>


**Model:** `haiku` · **Tools:** Read, Write, Edit, Bash, Grep, Glob

---

### [prescriber](agents/prescriber.md)

Write a prescription — an implementation plan leaving the executor no decision, no option, and no signature — for one unit from a spec and its contract, by the prescriptive-planning skill. Use it before each executor launch in the lite cycle, and again to rewrite a prescription around review findings. Examples:

<example>
Context: The lite cycle has planned a unit and needs its prescription before launching an executor.
user: "Prescribe the invoice-export unit"
assistant: "I'll launch the prescriber agent with the spec, the unit's contract, and the prescription path."
</example>

<example>
Context: A spec review failed on an executor's work.
user: "Rewrite the prescription around the verdict's findings"
assistant: "I'll launch the prescriber agent with the findings file for a correction prescription."
</example>


**Model:** `opus` · **Tools:** Read, Write, Grep, Glob, Bash, Skill

---

### [suborchestrator](agents/suborchestrator.md)

Run the lite cycle — plan, prescribe, execute, review, integrate — over one spec as a sonnet agent beneath the main orchestrator, launching prescribers and executors and reviewing each unit itself. Use it when the owner marks a development run lite. Examples:

<example>
Context: A spec file exists and the owner wants the cheapest implementation path.
user: "Implement docs/specs/invoice-export.md with the lite cycle"
assistant: "I'll launch the suborchestrator agent with the spec path and the project root."
</example>

<example>
Context: The main orchestrator has captured a spec and the owner said lite.
user: "Go lite on this one"
assistant: "I'll launch the suborchestrator agent to run the lite cycle over the spec."
</example>


**Model:** `sonnet` · **Tools:** Agent, SendMessage, TaskStop, Read, Write, Bash, Grep, Glob, Skill

---

