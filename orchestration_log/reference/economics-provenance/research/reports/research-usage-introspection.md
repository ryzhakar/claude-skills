# Usage introspection in Claude Code 2.1.322

## Binding

[binding] research-usage-introspection, sent to `main` before any other read.
- first-principles (114 lines, whole): I must reason from verified atoms, not analogy or remembered form, and I will treat the lead's status-line belief as a hypothesis until a fetched page or local file shows the field.
- cargo-cult-science (89 lines, whole): I must not fool myself and must report everything that could invalidate a result, and I will list each unverified step and each contrary fact under Not determined.
- stop-yapping (131 lines, whole): I must give the answer with no preamble, hedging or filler, and I will keep paths, versions, quotes and numbers exact.
- oath skill: 126 lines, whole. Line counts from `wc -l`.

## Sources

Machine: owner's Mac, Darwin 24.3.0; `claude --version` = `2.1.322 (Claude Code)`. Fetched 2026-11-12 with `curl -w '%{http_code} %{size_download}'` (WebFetch gives a model-made summary, so every quote below comes from the curl bytes or from WebFetch's saved raw copy of statusline.md).

| source | HTTP | bytes |
|---|---|---|
| code.claude.com/docs/en/statusline.md | 200 | 66464 |
| code.claude.com/docs/en/hooks.md | 200 | 293031 |
| code.claude.com/docs/en/monitoring-usage.md | 200 | 175703 |
| code.claude.com/docs/en/costs.md | 200 | 46805 |
| code.claude.com/docs/en/settings.md | 200 | 45990 |
| raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | 200 | 1193584 |

Local version 2.1.322 equals the changelog's top entry (`## 2.1.322`), so the pages are not behind the binary.

Local config (`jq` of one key only):
- `/Users/ryzhakar/.claudes/anarchy/settings.json` `.statusLine` = `{"type":"command","command":"bash /Users/ryzhakar/.claude-shared/statusline-command.sh"}`. A status line command is already configured. No `refreshInterval`, no `padding` key in it.
- same file `.subagentStatusLine` = `null`.
- `/Users/ryzhakar/pp/estafette/.claude/settings.json` and `settings.local.json`: absent.
- settings.md (45990 bytes): `grep -i 'statusLine|refreshInterval'` matches nothing; the key lives on statusline.md and `settings-reference` (not fetched, not in the brief).

## Status line input

Fields the command receives on stdin (statusline.md, "Available data"): `model.id`, `model.display_name`, `cwd`, `workspace.current_dir`, `workspace.project_dir`, `workspace.added_dirs`, `workspace.git_worktree`, `workspace.repo.{host,owner,name}`, `cost.total_cost_usd`, `cost.total_duration_ms`, `cost.total_api_duration_ms`, `cost.total_lines_added`, `cost.total_lines_removed`, `context_window.total_input_tokens`, `context_window.total_output_tokens`, `context_window.context_window_size`, `context_window.used_percentage`, `context_window.remaining_percentage`, `context_window.current_usage`, `exceeds_200k_tokens`, `fast_mode`, `effort.level`, `thinking.enabled`, `rate_limits.five_hour.{used_percentage,resets_at}`, `rate_limits.seven_day.{used_percentage,resets_at}`, `rate_limits.spend_limit.{used_percentage,resets_at,used_usd,limit_usd,period}`, `prompt_cache` (sub-fields incl. `warm`, `hit_ratio`, `expires_at`, `last_miss_cause`, `miss_causes`), `session_id`, `session_name`, `prompt_id`, `transcript_path`, `version`, `output_style.name`, `vim.mode`, `agent.name`, `pr.{number,url,review_state,kind}`, `worktree.{name,path,branch,original_cwd,original_branch}`. The `current_usage` and `prompt_cache` sub-field lists sit in sections I did not quote whole (see Not determined).

Rate-limit lines, quoted:
- "`rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage` | Percentage of the 5-hour or 7-day rate limit consumed, from 0 to 100"
- "`rate_limits.five_hour.resets_at`, `rate_limits.seven_day.resets_at` | Unix epoch seconds when the 5-hour or 7-day rate limit window resets"
- "`rate_limits`: appears only for claude.ai Pro, Max, and Ultra subscribers, or behind a Claude apps gateway that sets a spend limit for you. Even then, it appears only after the first API response in the session. Each window (`five_hour`, `seven_day`, `spend_limit`) may be independently absent, and Claude Code drops a window once its `resets_at` time passes."
- Introduced: CHANGELOG 2.1.80 "Added `rate_limits` field to statusline scripts for displaying Claude.ai rate limit usage (5-hour and 7-day windows with `used_percentage` and `resets_at`)". `spend_limit`: 2.1.251; `used_usd/limit_usd/period`: 2.1.284. 2.1.243: "Fixed the status line `rate_limits` fields and `/usage` still showing a rate-limit window's pre-reset usage percentage after the window reset while the session was idle". 2.1.322 >= all of them.

When the command runs (statusline.md, "How status lines work"): once at session start (also on resume), then on: new assistant message; `/compact` finishes; permission mode change; vim mode toggle; `command` edited; "A `refreshInterval` timer elapses, if you set one"; "A rate-limit window in the data your script last received reaches its `resets_at` time"; a warm prompt cache reaches `expires_at`. Debounce 300 ms; a script still running is cancelled by a new trigger.

Idle sessions, quoted: "The event-driven triggers can go quiet when the main session is idle, for example while a coordinator waits on background subagents. To keep time-based or externally-sourced segments current during idle periods, set `refreshInterval` to also re-run the command on a fixed timer." `refreshInterval`: "re-runs your command every N seconds in addition to the event-driven updates. The minimum is `1`." So: without `refreshInterval` the script does not reliably run while the session only waits on agents; with it, it does. (The `refreshInterval` entry appears in CHANGELOG at line 7429, version heading not captured by my awk; the page documents it, 2.1.322 is current.)

Per-agent rows: separate setting `subagentStatusLine` (same page, "Subagent status lines"). Runs "once per refresh tick", stdin carries `tasks[]` with `id`, `name` (optional), `type` (`local_agent`), `agentType` (2.1.293), `status` (`running|completed|failed|killed`), `description`, `label`, `startTime` (ms), `model` (optional, "ID of the resolved model"), `effort`, `contextWindowSize`, `tokenCount` ("Running token count of the subagent, the figure the default row shows"), `tokenSamples` (last 16 readings), `cwd`. It is the panel under the prompt, so it renders for the visible rows of an interactive TUI.

## Hooks

hooks.md event list (from the lifecycle table): SessionStart, SessionEnd, Setup, UserPromptSubmit, UserPromptExpansion, Stop, StopFailure, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, WorktreeCreate, WorktreeRemove, Notification, MessageDisplay (from the WebFetch summary of the first 100000 characters; the rest of the 293031 bytes I grepped, not read whole).

Events whose input carries token, cost or limit figures (grep of the full page for `token|cost|usage|rate_limit|total_cost`):
- Common input fields: none (`session_id`, `prompt_id`, `transcript_path`, `cwd`, `scratchpad_dir`, `permission_mode`, `effort`, `hook_event_name`). No limit figure in any common field.
- SessionStart on `resume`/`fork`: `context_tokens`, `estimated_cache_write_usd` (cost of re-caching the resumed context).
- PreModelSwitch: `context_tokens`, `estimated_cache_write_usd`, plus four more re-send cost fields.
- PostToolUse for a foreground Agent call: `tool_response.totalTokens`, `.usage`{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}, `.resolvedModel`, `.modelsUsed`. Quote: "`totalTokens` ... Token count from the subagent's final API request ... This isn't a total across the whole run". Background agents: "`tool_response` carries no usage fields ... `status: "async_launched"`, `agentId`, `description`, `prompt`, `outputFile`, and `resolvedModel`."
- SubagentStop: `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message`, `background_tasks`, `session_crons`. No usage field, but `agent_transcript_path` points at the file Transcripts below reads.
- StopFailure: `error` value `rate_limit` (event only, no figures).
- Notification: quota events `quota_auto_resume_fired|stale|disabled` (events, no figures).
No hook event carries the 5-hour or weekly utilization.

## Telemetry

monitoring-usage.md metrics: `claude_code.token.usage` (types `input`, `output`, `cacheRead`, `cacheCreation`; attribute `model`), `claude_code.cost.usage` (USD), `session.count`, `lines_of_code.count`, `pull_request.count`, `commit.count`, `code_edit_tool.decision`, `active_time.total`. Attributes on API events: `model`, `query_source` (`main|subagent|auxiliary`), `agent_id`, `parent_agent_id` (2.1.310), `agent.name`; `claude_code.api_request` events carry tokens per request.

Limit utilization: `grep -i 'utiliz|five_hour|seven_day'` on the page matches nothing; `rate.limit` matches only the classifier "unavailable" text and the like. No metric or event carries the 5-hour or weekly share. (The page's remaining 75667 characters were summarized, not read; the grep covered the whole 175703 bytes.)

Receiving locally: `CLAUDE_CODE_ENABLE_TELEMETRY=1`, `OTEL_METRICS_EXPORTER=otlp|prometheus|console`, `OTEL_LOGS_EXPORTER=otlp|console`, `OTEL_EXPORTER_OTLP_PROTOCOL` (no default; must be set), `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`, plus a collector or Prometheus scrape; metric export interval default 60000 ms. Env must be set before `claude` starts, so a running session cannot adopt it. Moot for the stated need: it gives tokens per model and per agent but not the limit.

## Transcripts

Directory `/Users/ryzhakar/.claudes/anarchy/projects/-Users-ryzhakar-pp-estafette/73b37e7c-4410-437c-b9d0-0650d0663d2c/subagents/`: `ls | wc -l` = 940 files = 470 `agent-<id>.jsonl` + 470 `agent-<id>.meta.json` (`ls *.jsonl | wc -l`). Main session transcript: `.../-Users-ryzhakar-pp-estafette/73b37e7c-4410-437c-b9d0-0650d0663d2c.jsonl`, 138683112 bytes (not opened).

Sampled `agent-a02d3b6b1fc032eb6` (3899 lines), structure only via `jq`:
- Meta keys: `agentType`, `description`, `finished`, `isBuiltIn`, `model`, `name`, `pickedEffortModel`, `requestNonInteractive`, `requestShape`, `spawnDepth`, `spawnedWithWorktree`, `toolUseId`, `worktreeBranch`, `worktreePath`. Values seen: `model:"opus"` (alias), `name:"impl-acceptance-local"`, `finished:true`. Across all 470 meta files: `finished` = `true` 109, `null` 291 (count of the first 400 meta files only is 291+109=400; `jq '.finished|tostring'` printed `null` for a missing or null key). Treat `null` as not-marked-finished, not as proof of running.
- Message line (`type:"assistant"`): `.message.model` = full id (`claude-opus-5-5` x1271, `<synthetic>` x3), `.message.id` (`msg_...`), `.message.usage` keys: `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `cache_creation`, `inference_geo`, `iterations`, `output_tokens_details`, `server_tool_use`, `service_tier`, `speed`, `fallback_credit`. Line keys: `agentId`, `sessionId`, `timestamp`, `uuid`, `parentUuid`, `slug`, `gitBranch`, `cwd`, `version`.
- No total field exists; sum per message. Lines repeat: 1273 assistant lines but 700 unique `.message.id` (470 ids repeated); the repeats carry identical usage. Sum must be over `unique_by(.message.id)` and must drop `<synthetic>` (697 left).
- Measured sum for the sample (`jq -s`, unique ids, synthetic excluded, 697 messages): input 1436, output 594555, cache_read 228968943, cache_creation 5868428.
- Subtle: `output_tokens` on an id's first-seen line may be a streaming partial; the sample's repeats were identical, but I did not test that the first line holds the final count across files.

## Answers

(a) 5-hour limit used share and reset time: yes, by the status line command's stdin. "`rate_limits.five_hour.used_percentage` ... Percentage of the 5-hour ... rate limit consumed, from 0 to 100" and "`rate_limits.five_hour.resets_at` | Unix epoch seconds when the 5-hour ... window resets" (statusline.md; added 2.1.80, local 2.1.322). Caveat quoted above: only for claude.ai Pro/Max/Ultra, only after the session's first API response, window dropped once `resets_at` passes. Whether this account is such a subscriber is not read here; the owner's login is said to hit a 5-hour limit, which fits.

(b) Weekly limit: yes, same mechanism: `rate_limits.seven_day.used_percentage` and `rate_limits.seven_day.resets_at`. Same caveats. Per-model weekly rows ("model-specific weekly limit row" appears in `/usage`, CHANGELOG line 3918) have no field on the status line page; not found.

(c) Per-agent tokens and model for agents in flight: yes, two mechanisms. (1) Files: each agent's `agent-<id>.jsonl` (model from `.message.model`, tokens summed over unique `.message.id`) and `.meta.json` (`name`, `model` alias, `agentType`, `finished`); `agent_transcript_path` in the SubagentStop input names the same file. (2) `subagentStatusLine` stdin `tasks[].{name,model,status,tokenCount}`; but "tokenCount" is a "running token count ... the figure the default row shows", its composition (cache reads in or out) is not stated, and it needs the agent panel rows to be visible. Hooks give no running count for background agents (quoted above). OpenTelemetry could, with `agent_id` and `model` attributes, but only if set at launch.

## Smallest mechanism

Use the status line command that is already configured, plus a timer.
1. Where it sits: the existing script `/Users/ryzhakar/.claude-shared/statusline-command.sh` (shared by all logins, so an edit affects every session using it; a copy under the repo is the safer unit, per `scripts-and-paths`: tracked copy, scratch root as env var). Add, near the top, a tee of stdin: `input=$(cat)`; write the three fields `rate_limits.five_hour.{used_percentage,resets_at}` and `rate_limits.seven_day.{used_percentage,resets_at}`, with `// empty`, plus `session_id` and the current epoch time, as one JSON object to a tmp file in a fixed directory, then `mv` it over the final name (`file-paths-and-writes`: temp then rename). Suggested final name `<scratch root>/usage-limits.json`.
2. What it reads: stdin only. It must not print the whole stdin or the environment anywhere (`credentials-unread`).
3. Settings change (named, not made): key `statusLine` in `/Users/ryzhakar/.claudes/anarchy/settings.json`, value shape `{"type":"command","command":"<path of the script>","refreshInterval":60}` (integer seconds, minimum 1). Today the object has `type` and `command` only. `refreshInterval` is what keeps the file fresh while the lead only waits on agents. Only the main session's own `rate_limits` are written; if several sessions share the login they all write the same account-wide figures, so last writer wins and the `session_id` plus epoch fields tell the lead which is newest.
4. Per-agent table: a second script (no setting needed) run by the lead at a wake: for each `subagents/agent-*.jsonl` whose `.meta.json` `finished` is not `true`, `jq -s` over `[.[]|select(.type=="assistant" and .message.model!="<synthetic>")]|unique_by(.message.id)` summing the four usage fields, with `name`, `model` (full id from the message), and the file's mtime as the liveness check (`agent-outcomes`). No settings change. Optional second source: `subagentStatusLine` key (same object shape, `{"type":"command","command":"..."}`) writing `tasks[]` `name, model, status, tokenCount` to a file.
5. Lead at each wake: `jq` the limits file (age = now - written epoch) and run the per-agent script.

Could not verify without running: (i) that this account's `rate_limits` is non-absent in this login (plan type and "first API response" rule); (ii) that `refreshInterval` re-runs the command while the lead is idle in this TUI and the 5 h figure stays fresh; (iii) what the existing script already does with stdin, since I did not open it (outside the brief's paths); (iv) that a hook-less, non-TUI or background-launched `claude` session also feeds this script; (v) `tokenCount` composition; (vi) the dedupe rule's final-count behaviour across files (see Transcripts); (vii) whether `finished:null` ever means running.

## Not determined

- Whether `rate_limits` is present for this account's login: run the script once and read the file (needs a settings edit and one API response).
- Whether `refreshInterval` fires while the session only waits: observe the file's `written` epoch advance with the lead idle.
- Sub-fields of `context_window.current_usage` and `prompt_cache`: statusline.md sections "Context window fields" and "Prompt cache fields" not quoted here; read them if needed.
- Content of `/Users/ryzhakar/.claude-shared/statusline-command.sh`: outside the brief's paths; read it before editing.
- Composition of `tasks[].tokenCount`: compare it with the transcript sum for one running agent.
- Meaning of `meta.finished = null` (291 of the first 400 files): compare with live `ListAgents` or file mtimes.
- Whether the first-seen line of a repeated `message.id` holds final `output_tokens` in every file: compare first-seen vs last-seen totals over all 470 files.
- Per-model weekly limit field: none found on the status line page; `/usage` shows it (CHANGELOG line 3918), no script-readable source found.
- The hooks page's text beyond what I grepped (293031 bytes, never read whole): a hook event carrying limit figures under words other than `token|cost|usage|rate_limit|total_cost` would have been missed.
- The monitoring page's last 75667 characters were not read in prose; the grep for `utiliz|five_hour|seven_day` covered all bytes and found nothing.

Scratch left: none. No file written but this report. No setting changed, nothing installed, no `claude` session started.

Result: PASS

usage-figures
