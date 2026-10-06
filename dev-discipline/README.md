# dev-discipline

Software engineering discipline skills, agent-agnostic: outermost-test-first signature-first TDD, systematic debugging, bug triage, architecture improvement, and receiving code review. Used ad hoc or by dev-cycle.

`tdd` `debugging` `code-review` `testing` `triage` `architecture` `refactoring` 
## Skills

### [improve-architecture](skills/improve-architecture/SKILL.md)

Find architectural friction — places where understanding a codebase breaks down — explore in parallel several designs for a deepened module — one hiding more implementation behind a smaller interface — and write an RFC — a proposal document — recommending one. "improve the architecture", "find refactoring opportunities", "deepen shallow modules", "reduce coupling", "simplify the module structure", "this module is hard to navigate", or any mention of architectural friction or module boundaries.


---

### [receiving-code-review](skills/receiving-code-review/SKILL.md)

Act on code review feedback — each item being one change a reviewer asks for, so a comment asking for two changes holds two items — by verifying each against the code, clarifying every unclear item before implementing any, pushing back with evidence, and implementing one item at a time. "address the review", "review comments to handle", "PR feedback", "should I implement this suggestion", "the reviewer says", or any reply to review findings.


---

### [systematic-debugging](skills/systematic-debugging/SKILL.md)

Find the root cause of a bug, a test failure, an error, or an unexpected behavior before changing any code, then fix the cause once. "debug this", "why does this fail", "the test is failing", "find the root cause", "this keeps breaking", "the fix didn't work", a build or integration failure, or any fix attempt that follows a failed one.


**Scripts:** [`find-polluter.sh`](skills/systematic-debugging/scripts/find-polluter.sh)
---

### [tdd](skills/tdd/SKILL.md)

Build code by writing one failing test through the surface its callers use before any code, designing the functions beneath that surface before filling them, and refactoring once every test passes. "tdd", "write tests first", "test-driven development", "red-green-refactor", "implement using tdd", "write a failing test", "design the signatures", "outside in", or any request to write code that carries behavior.


---

### [triage-issue](skills/triage-issue/SKILL.md)

Diagnose a reported bug to its root cause and write an issue document carrying a test-first fix plan, without fixing the code. "triage this", "this is broken", "investigate a bug", "find the root cause and file it", "write up this bug", "file an issue", or any bug report that asks for a diagnosis rather than a fix.


---

