---
name: systematic-debugging
description: >
  Find the root cause of a bug, a test failure, an error, or an unexpected behavior before changing any code, then fix the cause once.
  "debug this", "why does this fail", "the test is failing", "find the root cause", "this keeps breaking", "the fix didn't work",
  a build or integration failure, or any fix attempt that follows a failed one.
---

<investigate-before-fixing>
Finish the investigation — the steps through `test-one-hypothesis` below — before changing any product code, apart from a log line that instruments a boundary and the smallest change that tests a hypothesis or a difference, each reverted before the fix; never change code to see what happens.

Apply the whole procedure to every failure, including one that looks simple and one found under time pressure; never skip it for size or urgency.
</investigate-before-fixing>

<reproduce-and-read>
Read the whole error — the message, the stack trace, the line numbers, the file paths, the exit code; never read past a warning.

Reproduce the failure with exact steps and confirm it recurs; never investigate a failure that has not been reproduced.

Gather logs, timestamps, and environment state while the failure resists reproduction; never guess at a failure that will not recur.

List every change since the last known good state — commits, dependencies, configuration, environment; never assume the failing code is where the change was.
</reproduce-and-read>

<trace-to-the-source>
Trace backward from the line that raised the error through each caller or writer of the value it failed on, checking the value each passed or wrote, until the first point where the data went wrong; never fix where the error appears.

Instrument each component boundary in a multi-component system — log what enters and what leaves each component — and run once to see which boundary the data crosses wrong; never guess the failing component.

Bisect test pollution — state one test leaves behind that fails another — with `scripts/find-polluter.sh <pollution-path> <test-command> <test-files...>` from this skill's directory, which runs the tests one at a time and stops at the first that creates the path, wrapping the test command so it creates a file when the leftover state is not a file; never read every test by eye to find it.
</trace-to-the-source>

<compare-with-working-code>
Compare the broken code with working code that resembles it, listing every difference between the two, however small; never dismiss a difference as irrelevant before testing it.

Read in full the library, document, or sibling module the broken code was modelled on, when one exists; never adapt a pattern from a partial reading.

Write down what the broken code assumes about its inputs, state, environment, and dependencies; never leave an assumption unwritten.
</compare-with-working-code>

<test-one-hypothesis>
State one hypothesis in writing, in the form `X is the root cause because Y`; never test two in one change.

Test the hypothesis with the smallest change that can confirm or refute it, changing one variable, and revert the change; never stack a second change on an untested first.

Form a new hypothesis when the test refutes the first; never add a fix on top of a refuted one.

Investigate several hypotheses in parallel, one agent per hypothesis, through `agentic-delegation`; never let one agent hold two.

Write `I do not understand why X` and keep investigating when the mechanism is unclear; never propose a fix for a mechanism not yet understood.
</test-one-hypothesis>

<fix-the-root-cause>
Write a failing test that reproduces the bug through the unit's outermost interface, as `tdd` prescribes, before the fix; never fix without one.

Make one change addressing the cause, with the layer checks below as part of it; never bundle a refactor or a second fix with it.

Run the new test and the whole suite; never call the bug fixed on the new test alone.

Fix a timing failure by waiting on the condition the test needs, bounded by a timeout that fails with the condition's name; never fix one with a guessed duration.

Add a check at each layer the bad data crossed — rejection at the entry point, a precondition in the business logic, a guard on the operation the bad data would damage that is active where the damage is possible, such as a write outside a temporary directory during tests, and a log of the arguments before that operation; never add the check at one layer alone.
</fix-the-root-cause>

<stop-at-three-failed-fixes>
Count the fix attempts on this failure, including those made before this investigation began, and return to `reproduce-and-read` with the new evidence after a failed one; never retry a fix unchanged.

Stop after the third failed fix and report the architecture as the cause, citing each fix that revealed new coupling, needed a large refactor, or created a symptom elsewhere; never attempt a fourth fix on the same architecture.
</stop-at-three-failed-fixes>

<report-the-cause>
Report the root cause in two sentences, the evidence that led to it, the fix, and the test results; never report a fix without its cause.
</report-the-cause>
