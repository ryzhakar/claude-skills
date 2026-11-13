# Orchestration economics: ingredients (everything besides the requirements)

Scope: all the lead knows at 2026-11-12T16:41 on 2026-11-12 that bears on the mental model of orchestration economics: the draft as last shown, facts with their kind and source, derivations, corrections, unknowns, artifacts and what is in flight. Requirements are in `spec/orchestration-economics-requirements.md`. Kinds: owner-stated; published (source, date read); measured (what, by which tool, where); checked (confirmed by the opus check `docs/orchestration_log/recon/2026-10-24/reports/verify-spend-model-figures.md` or by the lead's own script); derived (arithmetic shown); unchecked (a sonnet agent's figure). Machine for every measurement: the owner's Mac, Darwin 24.3.0, Claude Code 2.1.322, this session's transcripts under `/Users/ryzhakar/.claudes/anarchy/projects/-Users-ryzhakar-pp-estafette/73b37e7c-4410-437c-b9d0-0650d0663d2c` (lead `.jsonl`, agents under `subagents/`). Written by the lead (self) on the owner's order.

## 1. The draft as last shown to the owner (not accepted; he then asked for requirements only)

Atoms.
- Per model: three prices (generate a token, re-read a cached token, re-write a token into cache), in dollars and in limit weight; speed in output tokens per second.
- Per model x effort (low, high, max): reach = share of tasks it gets right (capability); appetite = tokens generated per attempt. Yield = reach / appetite = work units per tokens generated ("work effectiveness"; the owner's "work unit delivery for 100k tokens generated").
- Per piece of work: context carried, rounds (each tool round re-reads the whole context), waits past the cache life (each re-writes the whole context), tool time, what a miss costs.
- Two resources: the usage limit, wall time.

Mechanics.
1. Limit per attempt = appetite x generate price + context x rounds x re-read price + context x cold restarts x re-write price. First term = generation bill (effort moves it). Other two = carriage bill (model, context size, round count, wait length move it; effort does not, as far as known).
2. Time per attempt = appetite / speed + tool time.
3. Cost per delivered unit = (attempt + check + (1 - reach) x miss) / reach, in whichever resource binds.
One prescription offered: at every launch and continuation choose model, effort and shape of the work (context, rounds, lifetime) that make relation 3 smallest; read parameters fresh.

Chains shown (change -> what it moves -> size).
- Effort low -> max: appetite up to x10 (Opus 5.5, Artificial Analysis: output tokens 21.1M at low to 218.1M at max over their suite; checked) -> generation bill x10, generation time x10; carriage untouched. Implementer (generation about 1/7 of cost, about 1/5 of wall): cost about x2.3, wall about x2.8 (derived: 6/7+10/7; 0.8+0.2x10). Reviewer (generation 0.9 of wall): wall about x9.
- Model one step up: generate and re-write x2, re-read x2 (x1 Opus -> Fable by list), speed x0.8; reach curve shifts up. Crossing point checked on SWE-bench Pro: Sonnet 5.5 high 87.6 percent, Opus 5.5 low 87.4 percent, 0.11 and 0.12 dollars per SOLVED task.
- Context x rounds: one generated token costs as much as 100 re-read tokens (sonnet, opus list), 200 (fable list; opus by limit weight). A round at 300k context = 1.5k to 3k generated tokens. Context grows with rounds, so carriage grows with the square of an agent's length. Evidence: the opus implementer of fix-restart-path-reselect: 39.67 dollars cache write, 54.63 read, 15.78 output of 110 (carriage 86 percent).
- One wait past the cache life: one cold re-write = 25 re-reads (sonnet, opus, 5-minute tier), 50 (fable). `just check` runs 6.5 minutes: at 380k on opus 1.90 dollars per gate; in 4-minute slices 0.15.
- One agent more: burn rate up, wall time down where independent, one more lead round at the lead's context per message or end.
- One miss: a checker, a continuation (cold re-write plus rounds), the gates again. Median unit cost 5.41 dollars at no review cycle, 13.05 at three or more (unchecked, confounded).
- A limit stop or login change: every cache cold at once.

## 2. Prices (published; platform pricing page read 2026-11-12; `docs/orchestration_log/recon/2026-10-24/scratch/token-prices/prices.json`, `docs/orchestration_log/recon/2026-10-24/reports/research-token-prices.md`; tracked copy `just/usage-prices.json`)

Dollars per million tokens: input, output, cache write 1-hour, cache read.
- fable 5.2: 8, 40, 16, 0.2. opus 5.5: 4, 20, 8, 0.2. sonnet 5.5: 2, 10, 4, 0.1. haiku 5.5: 0.1, 0.5, 0.2, 0.01.
- Cache write 5-minute = 1.25 x input (2.5 sonnet, 5 opus, 10 fable, 0.125 haiku); 1-hour = 2 x input (docs `api-caching.md:295-296`, unchecked quote). Cache read = 0.05 x input for sonnet and opus, 0.025 for fable, 0.1 for haiku. Output = 5 x input for all four.
- Per 100k generated: haiku 0.05 dollars, sonnet 1, opus 2, fable 4. Re-read of 300k: haiku 0.003, sonnet 0.03, opus 0.06, fable 0.06. Cold 5-minute re-write of 300k: haiku 0.04, sonnet 0.75, opus 1.50, fable 3.00.
- By list price a fable re-read costs what an opus one does; only its writes and output are double.

## 3. Limit weights (how the usage limit weighs a token)

- Not published by the vendor (`research-token-prices`, `research-usage-introspection`).
- One source: SemiAnalysis, "Anthropic Subscriptions Offer 5x+ More Value Than OpenAI", 22 captured pages of a paid article, by Andrew Megalaa, Max Kan, Dylan Patel, 2026-10-05; the owner's file `/Users/ryzhakar/Downloads/SemiAnalysis - Anthropic Subscriptions Offer 5x+ More Value Than OpenAI.pdf`; extraction `docs/orchestration_log/recon/2026-10-24/reports/research-limit-mapping-semianalysis.md` (page text and images under `docs/orchestration_log/recon/2026-10-24/scratch/research-limit-mapping-semianalysis/pages/`). Checked: page 10, Claude Max 20x (200 dollars a month), Opus 5.5, share of the MONTHLY limit per million tokens: input 0.045 percent, cache write 0.056, cache read 0.0011, output 0.223. Ratio generate : write : read = 200 : 50 : 1. Input, write, output are proportional to list price at the 5-MINUTE write price; cache read weighs 0.49 of its price; at the 1-hour write price the proportion fails (1-hour write weight unknown). Fable 5.1 input = 4.50 x Opus 5.5 input against a price ratio of 2.5 (checked). Pages 4 and 9 hold five-hour figures not yet in any ledger (302 dollars per five-hour window for Fable 5.1 on Max 20x reconciles with them: 2485 / 247M x 30M). The document says nothing on subagents, cache lifetime, effort, thinking, time of day; Fable 5.2 and Haiku 5.5 absent. The owner's plan tier per login is unknown to the lead.
- Own readings (measured by `just usage::limits` and `just usage::checkpoint`; the second login, arthur2, after the first login hit its five-hour limit at 15:02; resets: five-hour 1794506400, seven-day 1794852000 = 2026-11-16): about 15:08: 3 / 67 percent (five-hour / seven-day); 15:24: 17 / 69; 15:35: 30 / 71; 15:38: 33 / 72; 15:58: 47 / 74; 16:15: 53 / 75; 16:23: 56 / 75.
- Checkpoint deltas (tokens between two checkpoints): 15:35 -> 15:38 (168 s, +3 and +1 points): fable 5.2 cache read 3.04M, output 26k, write 26k; sonnet read 4.56M, output 16k, write 30k; opus none. 15:38 -> 15:58 (+14 and +2 points): fable read 20.4M, write 90k, output 61k; sonnet read 24.5M, write 709k, output 72k; opus read 1.19M, write 165k, output 3k.
- Derived, rough (integer points): one full five-hour window is about one seventh of the seven-day window; weighing by the PDF's Opus shares scaled by price, solving the two intervals for one fable factor gives about 3.3 x Opus, but that applied one factor to every fable token kind, which list price does not support for re-reads; fable's share of the 15:38-15:58 burn is between a half and seven tenths; the lead's own rounds about a quarter. Generation is about a third of the fable burn and a fifth of the sonnet burn; the rest is carriage.
- The checkpoint file changed format at fdf4d32 (keys now model plus effort); older lines are keyed by model alone.

## 4. Speed and wall time (measured, unchecked; `docs/orchestration_log/recon/2026-10-24/reports/research-generation-speed.md`, script `docs/orchestration_log/recon/2026-10-24/scratch/research-generation-speed/gen_speed.py`; 23,982 messages of at least 200 output tokens, gap at most 15 minutes)

- Median output tokens per second: sonnet 5.5 109.4 (n 11,485); opus 5.5 89.9 (8,788); fable 5.2 76.0 (2,269); fable 5.1 73.3 (1,433); haiku too few (7 messages). 100k generated: sonnet 15.2 minutes, opus 18.5, fable 21.9.
- The owner: effort does not change speed; it changes tokens generated. The estimator (gap to previous entry) reads low on short messages; agreed with the harness's thinking-duration field on five long opus messages.
- Generation's share of an agent's wall time, median over agents: opus implementers 0.27, sonnet implementers 0.17, the lead 0.27, sonnet reviewers 0.91, research agents 0.89. So tools and waits dominate implementers; generation dominates reviewers and researchers.
- Haiku's speed: the owner says published Claude Code speeds exist online; the Artificial Analysis haiku page is among the fetched files (`docs/orchestration_log/recon/2026-10-24/scratch/research-model-capability-and-effort/aa-claude-haiku-5-5`), unread.

## 5. Capability and effort

- `docs/orchestration_log/recon/2026-10-24/reports/research-model-capability-and-effort.md` (sonnet, 114 lines): score and dollar series by effort for five models from the publisher's launch charts, a capability table, effort levels with billing. Its cells are unchecked except those below; three of its headline statements were wrong (section 9).
- Checked: SWE-bench Pro: Sonnet 5.5 at high 87.6 percent, Opus 5.5 at low 87.4 percent; 0.11 and 0.12 dollars are per SOLVED task; Opus low per task 0.11; Sonnet high per task not published. Terminal-Bench 4.0: between 38.5 and 43.0 percent Sonnet at high costs 1.94 dollars where Opus needs medium at 2.94, so "Opus at lower effort is cheaper at every shared score" is false on the published points. Artificial Analysis page data publishes token counts per effort level (Opus 5.5 output 21.1M low to 218.1M max); the capability report's claim that only max effort is shown there is wrong.
- Raw sources on disk: `docs/orchestration_log/recon/2026-10-24/scratch/research-model-capability-and-effort/` (announcement texts `*-announce.txt`, chart tables `*.tsv`, `aa-*` model pages, docs `build-with-claude-effort.md`, `about-claude-models-*.md`, `cc-*.md`).
- Missing: reach and appetite for 4 models x 3 efforts (24 numbers); in those sources, not extracted. The lead told the owner it would pull them, with published speeds, in one cheap extraction "when you say the thinking is far enough along"; not launched.
- Effort in Claude Code (`docs/orchestration_log/recon/2026-10-24/reports/research-effort-in-claude-code.md`; docs `sub-agents.md:421`, checked as W6): a subagent with no effort of its own runs at the session's level only on the session's model; on another model that level does not apply. Measured: session at high; 14,239 sonnet subagent messages recorded medium; opus agents recorded high; fable agents high. Changelog 2.1.316 adds `CLAUDE_CODE_SUBAGENT_EFFORT` (the owner: "i won't deal with this"). The Agent tool takes `effort` per launch (low, medium, high, xhigh, max); it cannot change on a continued agent. Observed: a sonnet agent launched with effort low showed medium in its transcript (not determined why); agents launched with high show high.
- The lead now sets effort on every launch itself (owner ruling 10) and journals the pair.

## 6. Cache (measured by the lead's own script and by `just usage::coldturns`; checked)

- Tier tags: the lead's cache writes all 1-hour (14.8M tokens); all 493 subagent transcripts 5-minute (245M tokens).
- Share of context read from cache after a gap (gap between consecutive assistant messages; turns under 20k cached-plus-written dropped): under 4 minutes: lead 0.99 (4,833 turns), agents 0.99 (24,245); 6 to 55 minutes: lead 0.94 (139), agents 0.20 (491 turns, 62 of them mostly read, not traced); over 65 minutes: lead 0.00 (2), agents 0.01 (121).
- Cold turns this session (`just usage::coldturns` at fdf4d32): opus agents (effort high) 286 cold turns wrote 69.4M tokens = 72.5 percent of their cache writes (95.7M); sonnet agents at medium 457 cold turns, 83.7M = 56.8 percent of 147.5M; together 153M of 245M, about 556 dollars at 5-minute list rates; the lead 13 cold turns, 4.2M tokens.
- Docs (`docs/orchestration_log/recon/2026-10-24/reports/research-subagent-cache-lifetime.md`, sonnet at low, unchecked quotes: `prompt-caching.md:341`): main conversation 1 hour on a subscription inside plan usage; everything else (subagents, teammates, forks, compaction) 5 minutes by default. Levers: setting `subagentPromptCacheTtl: "1h"`; `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL=1h`; `ENABLE_PROMPT_CACHING_1H=1` (both buckets); `experimental: {cacheTtl: 1h}` in a subagent file; `FORCE_PROMPT_CACHING_5M=1` overrides. A login change or limit stop empties every cache (owner-stated; seen: 14 five-hour points in a quarter-hour after the 15:03 login change; 3.5M tokens re-written across thirteen agents in the morning).
- Done by the lead at about 16:22: `subagentPromptCacheTtl` set to `1h` in `.claude/settings.local.json` (project-local; the file also holds the `statusLine` entry `python3 -I /Users/ryzhakar/pp/estafette/just/usage.py capture`, refreshInterval 60). At 16:23 one running agent's row read tier 1h, five others 5m: live effect seen once, not fully verified. Break-even (derived): a 1-hour write costs 1.6 x a 5-minute one, so it pays where more than 3/8 of an agent's cache-write tokens are whole contexts re-written after a wait under an hour.
- Done at 15:36: both openers (`docs/orchestration_log/recon/2026-10-24/prompts/_opener.md`, `_implementer-opener.md`) order agents to run long commands detached and wait in slices of at most 240 seconds.
- Consequences for standing texts, not yet corrected: `docs/conventions.md` directives `cache-aware-resumption` and `resource-aware-orchestration` state a 1-hour cache for every conversation (true for the lead only, unless the setting holds); agentic-delegation's "a continued agent costs only the delta" holds for five minutes on the default. The owner: reconciling the dev cycle is not this work's concern.

## 7. Cost of units here (unchecked, confounded; `docs/orchestration_log/recon/2026-10-24/reports/research-cost-per-unit.md`, scripts under `docs/orchestration_log/recon/2026-10-24/scratch/research-cost-per-unit/`)

62 units; median dollars per unit 45.81 where opus implemented (20 units), 6.18 where sonnet did (37); opus took the high-risk units; median review cycles 2 in each group; 5.41 at no cycle, 13.05 at three or more; the lead's own 846.47 dollars belong to no unit; 64.4 percent of all priced dollars attributed. A research agent priced this session at 2,793 dollars list (unverified).

## 8. Derivations dropped from the model as implied by the mechanics (kept here)

1. Effort buys reach at falling yield (reach is capped, appetite is not): the lowest effort that reaches the task is the efficient one.
2. Raise effort when reach gained x cost of a miss exceeds extra tokens x output weight.
3. Effort steps are bigger than model steps: a model step is x2 in token cost and about x1.2 in time, an effort sweep up to x10 in tokens; at equal reach the stronger model at lower effort wins once the cheaper needs more tokens than the weight ratio between them. This is where the owner's sentence 9 holds; his sentence 6 holds inside that ratio.
4. The model multiplies the carriage bill (carriage tokens are billed at the model's input-side rates); effort leaves it alone. Long, many-round, large-context work: cheapest model that reaches, effort first. Strong models: short lives, small context, few rounds, files in, judgement out.
5. Keep carriage small: small context, batched rounds, no wait past the cache life, end rather than idle, fresh from files rather than cold and large. After the cache life a continued agent's only advantage is what it knows that no file holds.
6. The cost of a miss sets the target: cheap and caught at once -> yield; costs a cycle -> reach.
7. The binding resource sets the objective: limit -> weight; wall -> tokens / speed plus tool time.
8. Parameters are re-read, never remembered (checkpoints before and after).
9. Every agent end or message costs the lead one round at the lead's context; the lead's rounds were about a quarter of one measured interval's burn.

## 9. Corrections made on the way (do not repeat)

- Relayed from a sonnet summary before the check, wrong: SWE-bench dollars "per task" (they are per solved task); "Opus at lower effort cheaper at every shared Terminal-Bench score" (false); "no source publishes tokens per effort level" (Artificial Analysis does).
- "One usable five-hour figure in the PDF" was wrong (pages 4 and 9 hold more).
- The lead ordered the resume column priced at the 1-hour rate; the transcripts showed 5-minute for agents; the tool now prices each row at its own tier.
- The burn attribution "fable seven tenths" used one factor for all fable token kinds; range is a half to seven tenths.
- The lead's working effort rule (defaults until measured) and two role tables were withdrawn on the owner's word.
- The owner's "1 h TTL" statement of the morning holds for the lead's conversation; subagents default to 5 minutes.

## 10. Unknown, with the cheapest thing that settles each

- Reach and appetite for the 12 pairs (4 models x low, high, max): one cheap extraction from the fetched sources, then an opus check of the cells used.
- Whether higher effort adds rounds (then effort moves carriage too, and derivations 2 and 4 weaken): compare rounds per task across efforts in our transcripts once agents run at different efforts, or one fixed task at two efforts.
- Limit weight of fable 5.2, of 1-hour writes, of sonnet and haiku: checkpoints around work of one model; `just usage::calibrate` when the calculator lands.
- How far benchmark reach stands for reach on our units: our review-cycle counts by pair once efforts vary.
- Haiku speed: published figures; the fetched Artificial Analysis page.
- Whether the subagent cache setting holds for every launch kind; why a launch at effort low recorded medium: read tier and effort columns of `just usage::inflight` on the next launches.
- The plan tier of each of the owner's logins; the first login's seven-day figure.

## 11. Tools and artifacts

- `just usage::limits`, `usage::checkpoint <label>`, `usage::checkpoints`, `usage::inflight <minutes>` (per agent: idle, context, dollars by kind, resume cost at its tier, tier, model, effort), `usage::coldturns`; script `just/usage.py`, recipes `just/usage.just`, prices `just/usage-prices.json`; integrated on `integration/build-estafette` at fdf4d32. Limit figures file and checkpoints under `docs/orchestration_log/recon/` (`usage-limits.json`, `usage-checkpoints.jsonl`).
- In flight at 2026-11-12T16:41: the calculator (unit usage-calculator, sonnet at high, brief `docs/orchestration_log/recon/2026-10-24/prompts/implementer-usage-calculator.md`): `just usage::attempt`, `unit`, `compare`, `calibrate`, parameters in `just/usage-params.json` (speeds, cache lives, the Opus limit shares, reach and appetite null), refusing on a null atom.
- Reports under `docs/orchestration_log/recon/2026-10-24/reports/`: research-token-prices, research-usage-introspection, research-effort-in-claude-code, research-model-capability-and-effort, research-cost-per-unit, research-limit-mapping-semianalysis (and -r1, the failed first read), verify-spend-model-figures, research-generation-speed, research-subagent-cache-lifetime. Briefs under `docs/orchestration_log/recon/2026-10-24/prompts/` by the same names; `author-model-effort-policy.md` is a brief whose agent the owner had stopped: unused, not to be relaunched.
- `spec/resource-aware-orchestration.md`: the earlier ledger (52 lines) with the owner's first eight statements verbatim and the first ingredients. `docs/conventions.md`: working directives `resource-aware-orchestration`, `cache-aware-resumption`, `spare-the-strong-context`, `search-roots`, `wakes-and-resumes` (the first two carry the 1-hour claim and today's prices in their why lines: to correct; figures do not belong in the portable text).
- The Read tool's PDF backend is broken on this Mac (Homebrew poppler -> freetype 2.15.0 -> `/usr/lib/libhvf.dylib`); PDFs are read through `uv run --with pymupdf`. `du` is aliased to `dust`: use `/usr/bin/du`.

## 12. Where the discussion stands

The owner asked for requirements only and then for this dump. Next, on his word: settle the requirements (his confirmation of the lead's proposed exclusions and the open point on figures), then the lead writes the model itself, fresh, in the three layers, from sections 1 to 8 here, with nothing from sections 9 to 12 in it.

- written by the lead (self), 2026-11-12, from the journal, the reports named above and its own measurements.

## Names settled by the owner, 2026-11-12 (office-hours round; they replace every other name in this file and in the requirements file)

- orchestration economics: the thing itself; never "the model".
- model: the vendor's (haiku, sonnet, opus, fable); prices and generation speed belong to it. effort: the vendor's setting; three in use: low, high, max.
- variant: a model at an effort. lineup: the set of variants.
- capability: the share of attempts a variant gets right. appetite: the tokens a variant generates per attempt. yield: capability divided by appetite, work units per 100k tokens generated.
- attempt: one agent's launch-to-report on one task. failed attempt: an attempt that comes back wrong. check: the work that tells a right result from a failed attempt. work unit: one task delivered right (the owner's own word).
- step: one pass of an agent's loop, the whole context sent once and the tools (several in parallel are one step) run after.
- context: the text an agent holds, sent whole at every step.
- An agent's cost has three parts. output: the tokens generated. intake: every token entering the cache (new material, the agent's own earlier output, the whole context at a cold start). carry: the whole context read back at every step; it grows as context times steps, a triangular sum, quadratic in the agent's life.
- cold start: a step after the TTL has passed, a full-length intake of the context.
- TTL: the span after which an idle cache is dropped, explained where first used as the cache's life (5 minutes by default for a subagent, 1 hour for the main session or with the setting on).
- Prices are dollars and are named after the parts: output price, intake price (one value per TTL), carry price.
- limit weight: the share of the usage limit a token of a given part takes. Price means dollars alone.
- Two resources: usage limit and wall time. An attempt's wall time is generation time (output divided by generation speed) plus tool time (the time between steps while tools run or the agent waits).
- Three layers: atoms, mechanics, demonstrations.
- Dropped, never to be written: reach, generation bill, carriage bill, re-read, re-write, round, call or tool call as the unit, miss, cache life as the term, limit price, wait time, chains, vectors.
- Reading the older text above: reach is capability; generation bill is output; carriage bill is carry plus intake; re-read is carry; re-write is intake, at full length a cold start; rounds are steps.

— owner rulings, 2026-11-12, each journaled the turn it was given (docs/orchestration_log/history/2026-11-09/events.md, lines "round, settled").

## Capability and appetite by variant, extracted 2026-11-12

The pairs the draft above calls unextracted are extracted: `docs/orchestration_log/recon/2026-10-24/reports/extract-pairs-reach-appetite.md` (181 lines) and `scratch/extract-pairs-reach-appetite/pairs.json` beside it hold, for four models at low, high and max, score and output tokens per task from one run each (Artificial Analysis, Terminal-Bench 4.0, pass@1, 66 tasks by 3 repeats), the suite's output tokens relative to low, and published generation speeds, haiku included. Reported by an opus agent whose anchor cells match the earlier figure check; not rechecked by the lead. Figures are read from those files, never from this line.
