---
name: tdd
description: >
  Build code by writing one failing test through the surface its callers use before any code, designing the functions beneath that surface before filling them, and cleaning up once every test passes.
  "tdd", "write tests first", "test-driven development", "red-green-refactor", "implement using tdd",
  "write a failing test", "design the signatures", "outside in", or any request to write code that carries behavior.
---

<name-the-outermost-interface>
Name the outermost interface — the function, command, endpoint, or module surface that callers of the unit, the code being built, use — before writing a test; never start from a function beneath it.

Draw the barrier — the line between the outermost interface and everything beneath it — around the whole unit a caller sees; never draw it around a part of the unit.

Count as foreign a call into a library, a service, a runtime, or another team's module; never count a call into the unit's own code as foreign.
</name-the-outermost-interface>

<write-one-failing-test>
Write one test proving one behavior through the outermost interface; never write a second test before the first passes.

Run the test and read its failure; never continue from a test that passes before any code exists or fails for a reason other than the missing code or behavior.

Name the test for what the caller gets, in the caller's words; never name it for how the code achieves it.
</write-one-failing-test>

<pretend-call-the-missing-functions>
Write the body of the outermost interface as a sequence of painfully obvious steps, each step a pretend call — a call to a function that does not exist yet; never write a step that does two things.

Name each pretend call for what it does and returns, as its best caller would want to read it; never name one for how it works.

Shape each pretend call's arguments and return as the call site — the line that calls it — wants them; never shape them as the body beneath will find convenient.
</pretend-call-the-missing-functions>

<declare-the-signatures>
Declare each pretend-called function with its full signature — name, typed parameters, typed return — and a stub body, which is `...`, a `todo`, or a no-op; never fill a body in this step.

Spend most of the unit's design effort on signatures; never spend it on bodies.

Type each parameter and return as precisely as the caller's need requires and no more strictly; never accept a type the caller has to unwrap or convert before use.

Give each function one docstring of one sentence on one line stating what it does; never give it a second line.

Keep every fact a caller or a later maintainer needs in the signature and the docstring; never keep one in a comment or an external document.
</declare-the-signatures>

<recurse-to-the-leaves>
Treat each declared function as the next outermost interface and repeat the pretend calls and the declarations inside it; never skip a level.

Stop recursing at a body that is a foreign call or a single primitive operation — arithmetic, a lookup, a literal construction; never stop above one.
</recurse-to-the-leaves>

<pass-side-effects-down>
Initialize every side effect — the clock, a random source, the file system, the network, a database, the process environment, a subprocess — at the composition root, the program entry point or the test that calls the outermost interface; never construct one inside the unit.

Pass each side effect as a parameter into the outermost interface and down to every function beneath the barrier that needs it; never let a function reach for one it was not handed.

Keep every function beneath the barrier pure — its result a function of its arguments and nothing else; never let one gain a side effect to save a parameter.
</pass-side-effects-down>

<fill-bodies-to-green>
Fill each stub body with the least code that passes the test; never write code the current test does not demand.

Run the test after each body; never fill a second body before running the test after the first.

Read why a failing run fails before filling the next body; never fill a body against an unread failure.

Reach green — every test passing — before any refactor; never refactor on red — a failing test.
</fill-bodies-to-green>

<refactor-with-hindsight>
Rename, split, merge, and move once green, using everything the filled functions taught about the problem; never keep a name or a boundary the finished code has outgrown.

Deepen each module — hide more behind fewer entry points; never widen an interface to expose a function beneath the barrier.

Move each piece of knowledge that two places hold into one place; never leave one piece of knowledge in two places.

Merge two pieces of code when they hold one piece of knowledge; never merge two that merely look alike.

Run every test after each refactor step; never batch refactor steps between runs.
</refactor-with-hindsight>

<carry-explanations-in-code>
Carry every explanation in names, signatures, docstrings, and structure; never write a comment.

Treat a comment found in the unit as a defect and rewrite the code until the comment has nothing left to say; never leave one standing.

Name every literal that carries meaning — a bare number or string in logic — as a constant whose name states the meaning; never leave such a literal bare.

Name a function for the one thing it does; never join two things with `and` in a name.
</carry-explanations-in-code>

<test-at-the-barrier>
Test through the outermost interface; never test a function beneath the barrier unless one test through the outermost interface cannot reach its behavior.

Test such a function with property-based tests — tests that generate many inputs against a stated property, such as `hypothesis` in Python; never test one with hand-picked examples alone.

Mock foreign calls alone, by passing a stand-in for the side effect through the outermost interface's parameters, or through the entry function's parameters for a command or an endpoint; never mock the unit's own functions.

Pin a behavior — assert an exact current value or sequence as it stands — where the behavior is unconventional and no signature, type, or name can hold it; never pin a value a type could forbid.
</test-at-the-barrier>

<write-the-next-test>
Write the next test for the next behavior after the last reached green, and repeat every step above for it; never write all tests before any body.

Take each next behavior from the behaviors the request states that no test covers yet, shaped by what building the last test taught; never write a test from a list of tests drawn up before any code existed.

Stop when every behavior the request states has a passing test; never stop while one remains untested.
</write-the-next-test>

<read-the-finished-unit>
Read the finished unit against every instruction above and run every test; never report the unit done on a failing run or a standing comment.
</read-the-finished-unit>
