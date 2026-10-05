---
name: systematic-debugging
description: >
  Find the root cause of a bug, a test failure, an error, or an unexpected behavior before changing any code, then fix the cause once.
  "debug this", "why does this fail", "the test is failing", "find the root cause", "this keeps breaking", "the fix didn't work",
  a build or integration failure, or any fix attempt that follows a failed one.
---

<investigate-before-fixing>
Finish the investigation — the steps through `compare-with-working-code` below — before changing any code; never change code to see what happens.

Apply the whole procedure to every failure, including one that looks simple and one found under time pressure; never skip it for size or urgency.
</investigate-before-fixing>

<reproduce-and-read>
Read the whole error — the message, the stack trace, the line numbers, the file paths, the exit code; never read past a warning.

Reproduce the failure with exact steps and confirm it recurs; never investigate a failure that has not been reproduced, and gather logs, timestamps, and environment state until it does.

List every change since the last known good state — commits, dependencies, configuration, environment; never assume the failing code is where the change was.
</reproduce-and-read>

<trace-to-the-source>
Trace backward from the line that raised the error through each caller, checking the value each passed, until the first point where the data went wrong; never fix where the error appears.

Instrument each component boundary in a multi-component system — log what enters and what leaves each component — and run once to see which boundary the data crosses wrong; never guess the failing component.

Bisect test pollution — state one test leaves behind that fails another — with `scripts/find-polluter.sh <pollution-path> <test-command> <test-files...>`, which runs the tests one at a time and stops at the first that creates the path; never read every test by eye to find it.
</trace-to-the-source>

<compare-with-working-code>
Find code that works and resembles the broken code, and list every difference between the two, however small; never dismiss a difference as irrelevant before testing it.

Read a reference implementation the broken code follows in full; never adapt a pattern from a partial reading.

Write down what the broken code assumes about its inputs, state, environment, and dependencies; never leave an assumption unwritten.
</compare-with-working-code>

<test-one-hypothesis>
State one hypothesis in writing, in the form `X is the root cause because Y`; never hold two at once.

Test the hypothesis with the smallest change that can confirm or refute it, changing one variable; never stack a second change on an untested first.

Form a new hypothesis when the test refutes the first; never add a fix on top of a refuted one.

Investigate several hypotheses in parallel, one agent per hypothesis, through `agentic-delegation`; never let one agent carry two.

Write `I do not understand why X` and keep investigating when the mechanism is unclear; never propose a fix for a mechanism not yet understood.
</test-one-hypothesis>

<fix-the-root-cause>
Write a failing test that reproduces the bug through the unit's outermost interface, as `tdd` prescribes, before the fix; never fix without one.

Make one change addressing the cause; never bundle a refactor or a second fix with it.

Run the new test and the whole suite; never call the bug fixed on the new test alone.

Add a check at each layer the bad data crossed — rejection at the entry point, a precondition in the business logic, a guard against the dangerous operation in its environment, a log of the arguments before the dangerous operation; never add the check at one layer alone.
</fix-the-root-cause>

<wait-for-conditions>
Replace every fixed sleep in a timing-dependent test with a wait on the condition the test needs, bounded by a timeout that fails with the condition's name; never wait a guessed duration.

Wait a fixed interval after the triggering condition alone, with the interval's origin stated in the code's names, such as `TWO_TICKS_AT_100MS`; never wait a fixed interval in place of a condition.
</wait-for-conditions>

<stop-at-three-failed-fixes>
Count the fix attempts, and return to `reproduce-and-read` with the new evidence after a failed one; never retry a fix unchanged.

Stop after the third failed fix and report that the architecture is the cause — each fix reveals new coupling, needs a large refactor, or creates a symptom elsewhere; never attempt a fourth fix on the same design.
</stop-at-three-failed-fixes>

<report-the-cause>
Report the root cause in two sentences, the evidence that led to it, the fix, and the test results; never report a fix without its cause.
</report-the-cause>
