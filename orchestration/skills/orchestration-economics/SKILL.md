---
name: orchestration-economics
description: Count the cost of every launch, continuation, and stop of an agent in usage limit and wall time, and choose the model, the effort, and the shape of the work by that cost. "orchestration economics", "which model", "which effort", "continue or start fresh", "how many agents at once", "what will this launch cost", "why did the limit move", or any turn about to launch, continue, or stop an agent.
---

<count-the-cost-of-every-act>
Before every launch, continuation, and stop of an agent — each one an act, an agent being a vendor's language model run in a loop with tools — count what the act will cost; never make an act whose cost you have not counted.

Count that cost in two resources — the usage limit, what your plan lets you spend in each window of hours or days, and wall time, the time that passes on the clock; never in one of the two alone.

Build the cost from three layers, each named for what it holds — atoms for the quantities you count, mechanics for the relations that turn atoms into a cost, and demonstrations for worked examples in which one parameter moves that cost; never take the cost from a table that assigns models to roles.

Count to the accuracy that separates the choices in hand; never spend more on the count than the choice can save.
</count-the-cost-of-every-act>

<count-the-atoms>
Count an agent's work in steps, a step being one pass of its loop, in which its whole context — the text it holds — goes to the model once and the tools the model calls then run, several in parallel making one step; never count that work in messages or tool calls.

Split the tokens an agent spends, tokens being the units of text a vendor counts, into three parts — the output its model generates, the intake its context takes on, and the carry of that context from step to step; never add the three into one total.

Count as output every token the model generates, its reasoning and its tool calls included; never count the visible reply alone.

Count as intake every token that enters the cache, the store that keeps a context between steps — new material, the agent's own earlier output, and the whole context again once the cache has lapsed; never count new material alone.

Count as carry the whole context read back from the cache at every step; never treat a step that generates little as free.

Call the span an idle cache survives the TTL, the cache's life; never count a cache as alive past it.

Count a cold start at each step taken after the cache has lapsed, the whole context entering as intake again; never count a wait past the TTL as free.

Count yourself as an agent whose every step carries your whole context, each report or message you handle being a step; never treat your own context as free.

Give each model its prices in dollars by part — an output price, an intake price for each TTL on offer, and a carry price; never give a token a price without its part and its model.

Give each part of each model a limit weight, the share of the usage limit that one token of that part takes; never call a limit weight a price.

Call one agent's work on one task, from launch to report, an attempt; never stretch one attempt over two tasks.

Give each model a generation speed, the tokens it generates a second, and each attempt a generation time, its output divided by that speed; never time one model by another's speed.

Count as tool time the time between an agent's steps, in which its tools run or the agent waits; never count that time as generation time.

Treat each model at each of three efforts — low, high, and max, effort being the vendor's setting for how much a model generates on a task — as a variant of its own, and the variants on offer as one lineup; never choose a model and leave its effort to a default.

Give each variant, for each kind of task, a capability — the share of its attempts that come back right — and an appetite — the tokens it generates in one attempt; never give a variant one of the two alone.

Count a work unit — one task delivered right — once a check has passed the attempt, a check being the work that tells a right result from a failed attempt, one that came back wrong; never count an attempt as a work unit before its check.

Compare the efforts of one model by yield — capability divided by appetite, the work units delivered for each 100k tokens generated; never compare the variants of two models by yield alone.

Read each price from the vendor's price list on the day, its tiers by context size included; never from memory.

Take each limit weight from two readings of the usage limit, one before and one after a stretch of work whose tokens you count by part and by model; never from a price where a reading exists.

Where no reading exists, or where the vendor bills by the token, weigh the parts and the models in the proportion of their prices; never report that proportion as a reading.

Read from the usage records the harness keeps of your own agents — the harness being the program that runs them, the records its log of what each step spent — the TTL each kind of agent runs under and the effort an agent runs at when you set none; never assume either from documentation.

Take capability, appetite, and generation speed from a published run of each variant on tasks like yours until your own count of attempts replaces them; never carry a published figure past your own count.

Draw from the project's plans, check verdicts, and usage records one row per task and one per attempt — the traits the task showed before its first launch, the variant the harness recorded, the number of attempts, the verdict of the first check, the wall time, and the tokens by part; never take a variant from what its launch asked for.

Sort tasks into kinds by the traits that separate first-check verdicts in those rows; never sort by a trait the rows show separates nothing.

Test each kind on tasks its rows did not hold; never trust a kind tested on the rows that made it.
</count-the-atoms>

<apply-the-mechanics>
Count an attempt's cost on the usage limit as `output × output weight + intake × intake weight + carry × carry weight`; never as its tokens at one rate.

Take `output = appetite`, `intake = material read + output + the context at each cold start`, and `carry = the context summed over the steps`, the context holding everything read and generated so far; never take intake or carry from the material alone.

Count an attempt's wall time as `appetite ÷ generation speed + tool time`; never as its generation time alone.

Count a work unit's cost, once in each resource, as `(attempt + check + (1 − capability) × rework) ÷ capability`, rework being what a failed attempt costs beyond itself — its findings read, the checks run again, and, where the check passes it, everything built on the wrong result; never count a work unit as one attempt.

Count each further attempt at one task with the capability its failed attempts leave; never with the capability of a first attempt.

Count attempts run at once at the sum of their costs on the limit and, where none waits on another, at the longest of their wall times, adding a step of your own for each report and the tool time they cost one another on a shared machine; never count a parallel attempt as free time.

Call the usage limit the binding resource when the work you mean to do before a window's reset weighs more than the share that window has left, and wall time the binding resource otherwise; never take the binding resource from habit.

Weigh the work against every window of the usage limit, the longest included; never against the shortest window alone.

Start an attempt when the share left in every window carries it to its report; never start one that a window's limit will cut.

Choose at every act the variant and the shape of the work — its context, its steps, its waits, its check, its life, and what runs beside it — that make a work unit cost least in the binding resource; never choose by habit, by role, or from a table.

Take, of two choices that cost close in the binding resource, the one that finishes sooner; never save the usage limit at the cost of wall time on a close call.

Count progress in capabilities merged — a capability, in this sentence alone, being what a group of tasks delivers together for a user to use, not a variant's share of right attempts; never in tasks launched or closed.

After each stretch of work, split what the limit and the clock moved among the parts and the agents, yourself included; never explain a movement by a token total.

Correct each figure that the split contradicts; never keep a figure a reading contradicts.
</apply-the-mechanics>

<study-the-demonstrations>
Read every figure in the examples below as a reading of its date; never count an act's cost from one.

Attribute the prices, capabilities, appetites, dollars an attempt, and speeds of these examples to Anthropic's price list and to Artificial Analysis's run of each variant on Terminal-Bench 4.0, both fetched on 2026-11-12; never quote one of them without that source and date.

Attribute the limit weights to SemiAnalysis's reading, published on 2026-10-05, and the agents' figures to one project under Claude Code on 2026-11-12; never quote one of them without that source and date.

Take from each example how one parameter moves the cost; never take an example for a rule.

Expect a step up in effort to multiply appetite and generation time, to raise intake and carry through the context that the added output grows, and to buy a gain in capability that differs from model to model; never expect capability to rise in proportion.

<never_do_this reason="effort bought as though capability rose with it">
The task is hard; opus runs at max.
</never_do_this>

<do_exactly_this>
At low, high, and max, opus has a capability of 0.313, 0.566, and 0.596, an appetite of 37,782, 100,178, and 252,948 tokens, a cost of 2.08, 5.12, and 13.11 dollars an attempt, and a generation time of 5.9, 15.8, and 36.5 minutes. As max adds 0.030 to high for 2.6 times the dollars and 2.3 times the minutes, opus runs at high. From high to max fable gains nothing for 2.3 times the dollars, and sonnet gains 0.197 for 5.8 times.
</do_exactly_this>

Expect one capability to be on offer twice, from a cheap model at a high effort and from a strong model at a low one, the first lighter on the limit and the second quicker; never rank the lineup by model alone.

<never_do_this reason="lineup ranked by model">
The task is middling; sonnet, the middle model, runs at low.
</never_do_this>

<do_exactly_this>
Near a capability of 0.32 the lineup offers haiku at max, 0.328 for 0.65 dollars and 22.6 minutes of generation, and opus at low, 0.313 for 2.08 dollars and 5.9 minutes; sonnet at low gives 0.207 for 1.28 dollars. Haiku at max runs when the limit binds, and opus at low when wall time binds. Higher up, sonnet at max gives 0.636 for 12.65 dollars and 43.7 minutes where fable at low gives 0.545 for 4.34 dollars and 9.1 minutes: 2.9 times the dollars and 4.8 times the minutes buy 0.091.
</do_exactly_this>

Expect capability to be worth more as the check and the rework grow dearer; never compare variants by the cost of one attempt.

<never_do_this reason="one attempt compared, check and rework left out">
Sonnet at high costs 2.19 dollars an attempt and opus at high 5.12; sonnet runs.
</never_do_this>

<do_exactly_this>
Sonnet at high has a capability of 0.439 and opus at high 0.566. Where a test suite is the check and spends no tokens, a work unit costs `2.19 ÷ 0.439 = 4.99` dollars on sonnet and `5.12 ÷ 0.566 = 9.05` on opus, and sonnet runs. Where the check is a review at 6 dollars and each failed attempt brings 5 dollars of rework, opus runs: a work unit costs `(2.19 + 6 + 0.561 × 5) ÷ 0.439 = 25.05` on sonnet and `(5.12 + 6 + 0.434 × 5) ÷ 0.566 = 23.48` on opus.
</do_exactly_this>

Expect carry to grow as the square of an agent's steps; never count a long life as a short one repeated.

<never_do_this reason="every step counted alike">
The agent finished the first half of the task in 100 steps; the second half will cost the same.
</never_do_this>

<do_exactly_this>
A context that starts at 40k tokens and gains 2k a step carries 13.9M tokens over 100 steps and 47.8M over 200; the second 100 steps cost 2.4 times the first. A generated token costs what 100 carried tokens cost at sonnet's and opus's prices and what 200 cost at fable's. One step at 300k tokens of context therefore costs what 3,000 generated tokens cost, 1,500 on fable, before it generates one. Of the 110 dollars one opus agent spent on one task, carry took 54.63, intake 39.67, and output 15.78.
</do_exactly_this>

Expect a wait past the TTL to cost the whole context at the intake price, tens of steps of carry at once; never expect a wait to be free.

<never_do_this reason="wait past the TTL counted as free">
The suite takes 6.5 minutes; the agent starts it and waits for the result.
</never_do_this>

<do_exactly_this>
An opus agent holds 380k tokens under a 5-minute TTL. One wait of 6.5 minutes ends in a cold start that costs `380k × 5 ÷ 1M = 1.90` dollars; the same wait taken as 2 steps inside the TTL costs `2 × 380k × 0.20 ÷ 1M = 0.15`. A cold start costs what 25 steps of carry cost at sonnet's and opus's 5-minute intake prices and what 50 cost at fable's; at the 1-hour prices it costs what 40 and 80 cost. Intake under a 1-hour TTL costs 1.6 times intake under a 5-minute one, and the 1-hour TTL pays wherever cold starts would otherwise make more than three eighths of intake. Under the 5-minute TTL cold starts made 72.5 percent of the opus agents' intake and 56.8 percent of the sonnet agents'.
</do_exactly_this>

Expect a continued agent to carry its whole context at every further step and, once its cache has lapsed, to take that context in again; never count a continuation by the message that starts it.

<never_do_this reason="continuation counted by its message">
The agent knows the code already; two lines continue it for almost nothing.
</never_do_this>

<do_exactly_this>
An opus agent holds 440k tokens, its cache has lapsed under a 1-hour TTL, and 20 steps of work remain. Continued, it costs `440k × 8 ÷ 1M = 3.52` dollars for the cold start and `20 × 440k × 0.20 ÷ 1M = 1.76` for carry, 5.28 before it generates a token. A fresh agent that starts from 60k tokens of instructions and files, and averages 80k over the 20 steps, costs 0.48 for intake and `20 × 80k × 0.20 ÷ 1M = 0.32` for carry, 0.80. The old agent continues if what its context holds and no file holds would cost more to derive again than the 4.48 dollars that separate the two, the cost of 224k generated tokens; otherwise the fresh agent starts. While a cache is warm, one step that writes what the agent knows into a file costs 0.09 dollars of carry and the output of the file.
</do_exactly_this>

Expect a token to cost what the model that holds it charges, its intake price once and its carry price at every later step of that context; never expect a token to cost the same in every context.

<never_do_this reason="bulk read into the dearest context">
The logs run to 300k tokens; I read them and decide.
</never_do_this>

<do_exactly_this>
Read into my own context on fable under a 1-hour TTL, 300k tokens of logs cost `300k × 16 ÷ 1M = 4.80` dollars of intake and `300k × 0.20 ÷ 1M = 0.06` of carry at each later step, 6 dollars more over 100 steps. Read by a sonnet agent that reports in 3k tokens, the logs cost `300k × 4 ÷ 1M = 1.20` dollars of intake there and `3k × 16 ÷ 1M = 0.05` in my context.
</do_exactly_this>

Expect each agent that runs beside the others to add its cost to the limit at once, to cut wall time where its attempt waits on no other, and to cost you a step for each report; never expect parallel work to weigh less on the limit.

<never_do_this reason="own steps counted as free">
The 20 agents send 5 messages each; they do the work, and I route.
</never_do_this>

<do_exactly_this>
Their 100 messages are 100 steps of mine. At 400k tokens of context on fable each step carries `400k × 0.20 ÷ 1M = 0.08` dollars, the cost of 2,000 generated tokens, before I answer; the 100 steps cost 8 dollars and grow my context. One step taken after my own 1-hour TTL costs `400k × 16 ÷ 1M = 6.40` dollars, as much as 80 of those steps.
</do_exactly_this>

Expect a stop at the limit, or a change of login, to lapse every cache at once and to deliver nothing from the attempts it cuts; never expect cut work to resume for the cost of a message.

<never_do_this reason="launch counted without the share left">
Of the window 12 percent is left; 4 more attempts start, and the reset will sort out the rest.
</never_do_this>

<do_exactly_this>
One stop at the limit caught 13 agents mid-attempt; at their next steps they took in 3.5M tokens of context again, and I took in 0.4M. With 12 percent of the window left, the limit binds. The attempts that 12 percent carries to a report start now, and the others wait for the reset.
</do_exactly_this>

Expect the limit to weigh the three parts in other proportions than the price list gives them; never read a dollar total as the movement of the limit.

<never_do_this reason="dollars read as limit">
The agent cost 110 dollars at list prices; it took 110 dollars' worth of the limit.
</never_do_this>

<do_exactly_this>
The one published reading covers opus on one plan: a million tokens take 0.223 percent of the monthly limit as output, 0.056 as 5-minute intake, and 0.0011 as carry. As those weights stand at `200 : 50 : 1` where the prices stand at `100 : 25 : 1`, carry weighs half of what its price suggests. No reading exists for the other models or for 1-hour intake; two readings of the limit around one model's work supply one.
</do_exactly_this>
</study-the-demonstrations>
