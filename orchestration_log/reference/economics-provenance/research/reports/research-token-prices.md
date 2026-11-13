# Token prices and this session's spend

Fetched 2026-11-12. Machine: owner's Mac, Darwin 24.3.0, python3 -I. Data: lead transcript (139,995,704 bytes at read time, still growing) plus 477 subagent transcripts (`ls` of subagents: 954 files = 477 jsonl + 477 meta). Counting rule: `inflight.py` (unique `message.id`, `<synthetic>` dropped). Dollars are list price from the table below, not an invoice.

## Binding

- first-principles (114 lines, whole): I must derive prices from quoted published lines, not convention or memory, and I will quote source and line for every figure.
- cargo-cult-science (89 lines, whole): I must not fool myself and must report everything that could invalidate a result, and I will list every caveat under Not determined.
- stop-yapping (131 lines, whole): I must give the answer with zero filler, and I will write compressed fragments.
- oath skill: 126 lines, whole.

## Price table

USD per million tokens. Source: `https://platform.claude.com/docs/en/about-claude/pricing.md`, "Model pricing" table (fetched 2026-11-12, lines 17-37 of the saved fetch `.../tool-results/toolu_01RApUq389CrDuC9hRxKinZ4.txt`). Machine-readable: `scratch/token-prices/prices.json`.

| model id in transcripts | table row | fresh input | cache write 5m | cache write 1h | cache read | output |
|---|---|---|---|---|---|---|
| claude-fable-5-2 (also `claude-fable-5-2[1m]`, 1 message) | Claude Fable 5.2 | 8 | 10 | 16 | 0.20 | 40 |
| claude-fable-5-1 | Claude Fable 5.1 | 10 | 12.50 | 20 | 0.25 | 50 |
| claude-opus-5-5 | Claude Opus 5.5 | 4 | 5 | 8 | 0.20 | 20 |
| claude-sonnet-5-5 | Claude Sonnet 5.5 | 2 | 2.50 | 4 | 0.10 | 10 |
| claude-haiku-5-5, prompt <= 100,000 | Claude Haiku 5.5 (for prompts up to 100,000 tokens) | 0.10 | 0.125 | 0.20 | 0.01 | 0.50 |
| claude-haiku-5-5, prompt > 100,000 | Claude Haiku 5.5 (for prompts over 100,000 tokens) | 0.50 | 0.625 | 1 | 0.05 | 2.50 |

Quoted lines:
- `| Claude Fable 5.2 | $8 / MTok | $10 / MTok | $16 / MTok | $0.20 / MTok<sup>1</sup> | $40 / MTok |`
- `| Claude Fable 5.1 | $10 / MTok | $12.50 / MTok | $20 / MTok | $0.25 / MTok<sup>1</sup> | $50 / MTok |`
- `| Claude Opus 5.5 | $4 / MTok | $5 / MTok | $8 / MTok | $0.20 / MTok<sup>2</sup> | $20 / MTok |`
- `| Claude Sonnet 5.5 | $2 / MTok | $2.50 / MTok | $4 / MTok | $0.10 / MTok<sup>2</sup> | $10 / MTok |`
- `| Claude Haiku 5.5 (for prompts up to 100,000 tokens) | $0.10 / MTok | $0.125 / MTok | $0.20 / MTok | $0.01 / MTok | $0.50 / MTok |` and the over-100,000 row `$0.50 / $0.625 / $1 / $0.05 / $2.50`.
- Haiku rule: "A request's prompt length counts all of its input tokens, including cache reads and cache writes. Each request is priced on its own." Applied per message in the script.
- Footnote 1: "Cache hits and refreshes on Claude Fable 5.2 ... Claude Fable 5.1 ... are priced at 0.025x the base input price."

Skill `claude-api` cross-check (the skill's main text was delivered inline; no `SKILL.md` file exists at its base directory, so no file line is citable for the model table, header "Current Models (cached: 2026-10-06)"): Fable 5.1 10/50, Opus 5.5 4/20, Sonnet 5.5 2/10, Haiku 5.5 0.10/0.50. It has no Fable 5.2 row (older than that model). Citable file line: `shared/prompt-caching.md:144`: "Cache writes cost **1.25x for 5-minute TTL, 2x for 1-hour TTL**" and "0.025x on Claude Fable 5.1 ($0.25/MTok ...) and 0.05x on Claude Opus 5.5 ($0.20/MTok)". Matches the page: 12.5/10 = 1.25, 16/8 = 2, and so on. One conflict: the skill text says Sonnet 5.5 "cache reads $0.20"; the pricing page says $0.10 (0.05x of $2). The page is newer and is used.

## Cache facts

Source `https://code.claude.com/docs/en/prompt-caching.md`, "Cache lifetime" and "Which TTL each request gets".
- Lifetime: "Cached prefixes expire after a period of inactivity. Each request that hits the cache resets the timer."
- Requested TTL: "Unless you choose a TTL yourself, Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage." Main conversation: one hour on subscription within plan usage, five minutes on "Usage credits, API key, or cloud provider". "Everything else" (subagents, workflows, teammates, forks, compaction): "Five minutes, except the server-controlled helper requests, which get one hour".
- Over plan usage: "Claude Code drops the main conversation to the five-minute TTL".
- Subagents: "they get five minutes even on a subscription until you choose a longer one". Override: `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` / `subagentPromptCacheTtl` (v2.1.242+).
- Refresh: a read refreshes the timer at no charge (API skill `prompt-caching.md:148`: "A cache read refreshes the entry's timer at no additional cost, on either TTL").
- Scope: "each model has its own cache"; model switch "reads the entire conversation history with no cache hits"; caches "isolated between organizations"; effort change keeps cache on Fable 5.1+, Opus 5.5, Sonnet 5.5, Haiku 5.5 (API key or subscription).
- Login change: not stated. Searched `prompt-caching.md`, `costs.md`. Only "Caches are isolated between organizations, and on some providers, between workspaces".
- Measured here: all 48,055 subagent messages carrying `cache_creation_input_tokens` also carry the `ephemeral_1h_input_tokens` split (0 without). Subagent writes are 5m for Opus and Sonnet (0 tokens at 1h), consistent with the "five minutes" rule; the lead's writes are 1h (Fable rows below).

## Limit weighting

Not stated. Searched: `code.claude.com/docs/en/costs.md`, `support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work`, `support.claude.com/en/articles/14782391-claude-enterprise-consumption-guide`. Lines found:
- costs.md: "a seat-based usage window on a subscription plan, shared across all models, so the developer can't restore access by switching models with /model"; separately "After the model-specific 'You've hit your Opus limit' or 'Sonnet limit' message, switching to a model outside that family ... does keep the developer working."
- costs.md: plan allowance "resets on a rolling five-hour window and a weekly window", "shared with Claude chat and Cowork".
- Help article (as returned by the fetch tool): no per-model rate; "some plans also have a separate weekly limit for Fable"; "Weekly limits apply across all models"; cache reads: not stated.
- Consumption guide: "Usage is measured in tokens"; model intensity High (Opus), Moderate (Sonnet), Low (Haiku), Very High (Fable), no numbers.
- costs.md: "/usage" attributes usage to skills, subagents, plugins, MCP servers; figures "approximate".

## Session spend by model

Script: `scratch/token-prices/price_session.py` (output `session-priced.json`). Grand total at list price: **$2,793.33**. Lead file read at run time; it grows, so later runs differ. Tokens in millions (M), `fresh` = uncached input.

| model | agents | messages | fresh tok | write 5m M | write 1h M | read M | output M | $ total | share |
|---|---|---|---|---|---|---|---|---|---|
| claude-opus-5-5 | 55 | 10,497 | 21,487 | 95.25 | 0 | 2,959.38 | 8.81 | 1,244.35 | 44.5% |
| claude-sonnet-5-5 | 417 | 14,005 | 28,973 | 143.42 | 0 | 2,143.17 | 9.94 | 672.33 | 24.1% |
| claude-fable-5-2 | 3 | 2,756 | 7,006 | 1.37 | 8.38 | 1,041.56 | 2.92 | 472.71 | 16.9% |
| claude-fable-5-1 | 0 | 2,351 | 44,780 | 0 | 6.03 | 845.90 | 1.43 | 403.91 | 14.5% |
| claude-haiku-5-5 | 2 | 9 | 18 | 0.16 | 0 | 0.50 | 0.006 | 0.03 | 0.0% |

Dollars by kind per model: Opus fresh 0.09, w5m 476.26, read 591.88, out 176.13. Sonnet 0.06, 358.56, 214.32, 99.40. Fable 5.2 0.06, w5m 13.70, w1h 134.00, read 208.31, out 116.63. Fable 5.1 0.45, w1h 120.58, read 211.48, out 71.41. Haiku 0.00, 0.02, 0.01, 0.00.

Lead's own row (the lead transcript, 4,935 messages, max context 567,294): Fable 5.2 $442.56 + Fable 5.1 $403.91 = **$846.47** (30.3% of total). The agent counts in the table exclude the lead. Fable subagents: 3 files, all Fable 5.2 (investigate-lab-test-26 $15.75, investigate-lab-test-7 $13.60, ping-fable $0.79); no Fable 5.1 subagent. Agents total (477 files, script sum): $1,946.86 (69.7%). Agent dollars by model: Opus $1,244.35; Sonnet $672.33; Fable 5.2 $30.15; Haiku $0.03.

Price ratio relative to Sonnet 5.5 (derived from the table): output Fable 5.2 x4, Opus 5.5 x2, Haiku x0.05; cache read Fable 5.2 x2, Opus x2, Haiku x0.1; cache write 5m Fable 5.2 x4, Opus x2, Haiku x0.05. Fable 5.1: output x5, read x2.5, write 5m x5.

## Spend by kind

| kind | $ | share |
|---|---|---|
| fresh input | 0.65 | 0.0% |
| cache write 5m | 848.53 | 30.4% |
| cache write 1h | 254.59 | 9.1% |
| cache read | 1,225.99 | 43.9% |
| output | 463.58 | 16.6% |

Cache (write + read) = 83.4% of all dollars. Fresh input is negligible.

## Twenty largest agents

Largest context = max over messages of input + cache write + cache read tokens. Agents only (the lead is apart).

| rank | agent | model | messages | $ | largest context |
|---|---|---|---|---|---|
| 1 | Implement trace-seam trace seam | opus-5-5 | 1,129 | 131.57 | 579,337 |
| 2 | impl-fix-restart-stale-connections | opus-5-5 | 801 | 108.10 | 566,753 |
| 3 | impl-acceptance-local | opus-5-5 | 697 | 87.03 | 568,422 |
| 4 | impl-note | opus-5-5 | 417 | 76.76 | 566,290 |
| 5 | impl-acceptance-forging-addresses | opus-5-5 | 458 | 65.68 | 567,119 |
| 6 | impl-fix-observer-rows | opus-5-5 | 427 | 45.82 | 565,662 |
| 7 | impl-acceptance-lab-rest-third | opus-5-5 | 304 | 45.26 | 515,124 |
| 8 | impl-cli-infra | opus-5-5 | 287 | 42.14 | 572,126 |
| 9 | impl-fix-host-records | opus-5-5 | 296 | 40.78 | 566,085 |
| 10 | impl-all-node | opus-5-5 | 342 | 34.49 | 563,926 |
| 11 | spec-reviewer-trace-seam | opus-5-5 | 267 | 33.60 | 564,205 |
| 12 | impl-fix-restart-close | opus-5-5 | 256 | 31.43 | 494,239 |
| 13 | impl-node-rebind | opus-5-5 | 197 | 31.15 | 497,400 |
| 14 | impl-all-acceptance-tests | sonnet-5-5 | 408 | 28.84 | 565,767 |
| 15 | impl-restart-reachability | opus-5-5 | 209 | 25.54 | 504,525 |
| 16 | impl-mcp | opus-5-5 | 220 | 25.12 | 546,678 |
| 17 | impl-bridge-harness-line | sonnet-5-5 | 280 | 25.04 | 542,502 |
| 18 | impl-presence-request | opus-5-5 | 223 | 23.97 | 434,227 |
| 19 | impl-node-presence | opus-5-5 | 157 | 23.65 | 508,098 |
| 20 | impl-all-storage | sonnet-5-5 | 234 | 23.53 | 573,957 |

Top 20 sum: $949.50 (hand sum of the rows above, 48.8% of the $1,946.86 spent by agents). Names are the agents' own labels as in `.meta.json`.

## One turn, warm and cold

Script `derived_tables.py`. Prompt only: no new tokens, no output, no thinking. warm = ctx x cache read; cold = ctx x cache write (5m / 1h). USD per turn. Add output at the price table's per-token rate (per 1,000 output tokens: Fable 5.2 $0.040, Fable 5.1 $0.050, Opus $0.020, Sonnet $0.010, Haiku $0.0005).

| model | 100k warm | 100k cold 5m / 1h | 300k warm | 300k cold 5m / 1h | 500k warm | 500k cold 5m / 1h |
|---|---|---|---|---|---|---|
| Fable 5.2 | 0.0200 | 1.00 / 1.60 | 0.0600 | 3.00 / 4.80 | 0.1000 | 5.00 / 8.00 |
| Fable 5.1 | 0.0250 | 1.25 / 2.00 | 0.0750 | 3.75 / 6.00 | 0.1250 | 6.25 / 10.00 |
| Opus 5.5 | 0.0200 | 0.50 / 0.80 | 0.0600 | 1.50 / 2.40 | 0.1000 | 2.50 / 4.00 |
| Sonnet 5.5 | 0.0100 | 0.25 / 0.40 | 0.0300 | 0.75 / 1.20 | 0.0500 | 1.25 / 2.00 |
| Haiku 5.5 | 0.0010 | 0.0125 / 0.0200 | 0.0150 | 0.1875 / 0.3000 | 0.0250 | 0.3125 / 0.5000 |

Haiku at 100k uses the <=100,000 rate (a prompt of exactly 100,000 tokens is "up to"); at 300k and 500k the >100,000 rate.
Cold 5m / warm ratio (price table): Fable 5.2 50x, Fable 5.1 50x, Opus 5.5 25x, Sonnet 5.5 25x, Haiku 5.5 12.5x (both tiers).

## Cold resume of large contexts

Population: agents whose last counted message has context > 200,000 tokens: 115 of 477 (selection rule: input + cache write + cache read of the last unique `message.id` in the transcript), sum of those contexts 36,440,950 tokens. Cost of one cold resume of all 115, prompt only, if each ran on the named model (all contexts priced as cache write; Haiku per-agent rate by its own context):

| model | all 115, write 5m | all 115, write 1h | mean per agent, 5m |
|---|---|---|---|
| Fable 5.2 | $364.41 | $583.06 | $3.169 |
| Fable 5.1 | $455.51 | $728.82 | $3.961 |
| Opus 5.5 | $182.20 | $291.53 | $1.584 |
| Sonnet 5.5 | $91.10 | $145.76 | $0.792 |
| Haiku 5.5 | $22.78 | $36.44 | $0.198 |

Cold resume reprocesses a context once, at write price; a warm resume would read it at the cache-read price (12.5x to 50x less, ratios above).

## Not determined

- Weighting of the 5-hour and weekly plan limits by model and by kind: no published number found. Settles it: an Anthropic statement, or a measurement of the `/usage` bars against known token spends per model on this account.
- Effect of a login change on cache lifetime: not stated in `prompt-caching.md` or `costs.md`. Settles it: Anthropic documentation, or a run with one cache write, `/login` to another account, then a read.
- Whether this account pays list price, a contracted rate (`modelPricing`), or draws from plan usage in dollars: all dollars here are list price estimates; the lead transcript is an Anthropic subscription or API run, unknown. Settles it: the Console cost page or the `Total cost ... at your organization's configured rates` note in `/usage`.
- The skill table (`claude-api`) has no file line; its Sonnet 5.5 cache-read figure ($0.20) conflicts with the pricing page ($0.10); the page was used. The pricing page footnote 2 (for Opus 5.5 and Sonnet 5.5 cache reads) was not read.
- `claude-fable-5-2[1m]` (1 message) priced as Fable 5.2; no separate long-context surcharge is published for Fable in the lines read.
- The agent "last context" uses dict insertion order (first-seen position of each `message.id`), the same as `inflight.py`; a transcript that rewrites an older id after later ones would misplace "last". Not checked.
- A resumed agent's real cold-resume cost depends on whether its cache expired; the table assumes it did. Whether the 4,935-message lead file includes compaction requests is not separated.
- Lead file still grows; re-run `price_session.py` for current totals. Thinking tokens are inside `output_tokens` by API rule; not separated.
- Left for the lead to clear: nothing deleted; the saved fetch `.../tool-results/toolu_01RApUq389CrDuC9hRxKinZ4.txt` and the files in `scratch/token-prices/` (`prices.json`, `price_session.py`, `derived_tables.py`, `session-priced.json`).

Result: PASS

token-economy
