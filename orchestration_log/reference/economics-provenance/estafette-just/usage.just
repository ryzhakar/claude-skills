# Account limit figures caught from Claude Code's status line input, and the agents in flight with their token spend and cost.

set shell := ["bash", "-euo", "pipefail", "-c"]

script := source_directory() + '/usage.py'

[doc("Print the last limit figures the status line command wrote and their age; exit 1 when the file is missing or older than max_age_minutes; the file lives under the root checkout's scratch home whichever checkout runs this")]
[group('usage')]
[no-exit-message]
limits max_age_minutes="10":
    python3 -I {{ quote(script) }} limits {{ quote(max_age_minutes) }}

[doc("Print one row per agent whose transcript changed within window_minutes: tokens, context size, dollars by kind at the prices of just/usage-prices.json, the dollars of one cold start at the intake price of the TTL each transcript writes at (5m or 1h, shown in the ttl column; the lead transcript's TTL is printed last), idle minutes, model, effort, name; the session this shell runs in, named by CLAUDE_CODE_SESSION_ID and refused when that is unset or names no transcript, unless a subagents directory is given")]
[group('usage')]
inflight window_minutes="30" subagents_directory="":
    python3 -I {{ quote(script) }} inflight {{ quote(window_minutes) }} {{ quote(subagents_directory) }}

[doc("Append one line to usage-checkpoints.jsonl beside the limits file: the time, the label, the limit figures last written, and the tokens so far of the session this shell runs in (named by CLAUDE_CODE_SESSION_ID, refused when that is unset or names no transcript) by model with effort and kind (fresh input, cache write, cache read, output) over the lead and every agent")]
[group('usage')]
checkpoint label:
    python3 -I {{ quote(script) }} checkpoint {{ quote(label) }}

[doc("Print the checkpoint lines as a table; each line after the first adds the change in limit percentage points and in tokens by model with effort and kind since the line before; exit 1 when no file exists")]
[group('usage')]
[no-exit-message]
checkpoints:
    python3 -I {{ quote(script) }} checkpoints

[doc("Print per source (the lead apart from the agents), model with effort and TTL: the assistant turns whose gap to the model message before them exceeds the TTL (5 minutes or 1 hour), their cache-write tokens and share of all that group's cache-write tokens, and the same for turns within the TTL; the first message of a transcript has no gap and counts in neither; the session this shell runs in, named by CLAUDE_CODE_SESSION_ID and refused when that is unset or names no transcript")]
[group('usage')]
coldturns:
    python3 -I {{ quote(script) }} coldturns

[doc("Compute one attempt, arguments: model effort context_k steps cold_starts tool_time_min agent|lead [--appetite-k N]; model is a key of usage-prices.json or haiku, sonnet, opus or fable for the newest version of each, effort is low, high or max, context_k the thousands of tokens carried on average, tool_time_min the minutes of tool time; prints dollars for output, carry, cold starts and the first intake (the context held at launch, entering once) at the prices of usage-prices.json (the cold start and the first intake at the 5m intake price for an agent, the 1h price for the lead) and their sum, the published dollars of the variant (? where usage-params.json holds none), the limit weight of the same four where usage-params.json knows the model's weights and ? where not, minutes of generation time at the variant's generation speed (the model's where the variant has none), of tool time and their sum, and the TTL of the role; reads usage-prices.json and usage-params.json; refuses an unknown model or effort naming the accepted set, appetite null in usage-params.json and not passed with --appetite-k, and a generation speed null for both the variant and the model")]
[group('usage')]
[no-exit-message]
attempt *arguments:
    python3 -I {{ quote(script) }} attempt {{ arguments }}

[doc("Compute the cost of one work unit, arguments: the arguments of attempt, then check_usd check_min rework_usd rework_min [--capability C] [--appetite-k N]; prints the attempt table and then dollars and minutes per work unit = (attempt + check + (1 - capability) x rework) / capability, where the attempt's minutes are its total and capability is the share of attempts that come back right; reads usage-prices.json and usage-params.json; refuses everything attempt refuses, capability null in usage-params.json and not passed with --capability, and a capability outside 0 to 1 with 0 excluded")]
[group('usage')]
[no-exit-message]
unit *arguments:
    python3 -I {{ quote(script) }} unit {{ arguments }}

[doc("Compare two attempts, arguments: two quoted strings, each the arguments of attempt (for example \"claude-sonnet-5-5 high 200 30 1 10 agent --appetite-k 50\"); prints the attempt table of each side by side and the ratio second over first of every line, ? where either figure is unknown or the first is zero; reads usage-prices.json and usage-params.json; refuses what attempt refuses for either side, before any output")]
[group('usage')]
[no-exit-message]
compare first second:
    python3 -I {{ quote(script) }} compare {{ quote(first) }} {{ quote(second) }}

[doc("Price one work unit across the lineup, arguments: context_k steps cold_starts tool_time_min check_usd rework_usd [--capability-scale X], context_k the thousands of tokens an agent carries on average, tool_time_min the minutes of tool time; prints one row per model (haiku, sonnet, opus, fable, each at its newest version) and effort: capability, appetite in thousands of tokens, dollars of one agent attempt at that appetite by the arithmetic of attempt, minutes of generation time plus tool time, and dollars per work unit = (attempt + check + (1 - capability) x rework) / capability, sorted by dollars per work unit ascending, a variant lacking a figure last with the missing field named, then the note of usage-params.json on the effort the harness records; --capability-scale (default 1) multiplies every capability in usage-params.json by one factor taken from your own count of attempts; reads usage-prices.json and usage-params.json; refuses a scale that puts any capability outside 0 to 1 with 0 excluded, naming the variant, before any output")]
[group('usage')]
[no-exit-message]
lineup *arguments:
    python3 -I {{ quote(script) }} lineup {{ arguments }}

[doc("Calibrate the limit against list price: over consecutive lines of usage-checkpoints.jsonl keyed by model and effort, print the dollars spent in between at the list prices of usage-prices.json by kind (fresh, cache write at the 5m price, cache read, output), the five-hour and seven-day points moved and the dollars per point of each window, then the median dollars per point of each window over the intervals where the window rose; lines of the older format (tokens keyed by model alone) are skipped and counted; ? where a figure is unknown; refuses with fewer than two usable lines, naming how many it found")]
[group('usage')]
[no-exit-message]
calibrate:
    python3 -I {{ quote(script) }} calibrate
