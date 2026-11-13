# What decides a subagent's cache lifetime

Answer: Claude Code puts every request in one of two buckets by its query source. Main conversation gets 1h by default (subscription, inside plan usage). Subagents are in "everything else": 5m by default. Four user-settable levers move the subagent bucket to 1h. Nothing here was changed or run; all reads of docs fetched 2026-11-12 into scratch.

## Binding

Commitments (repeat of the `[binding]` message). Lines read whole from Stack paths, `wc -l`: oath SKILL.md 126, first-principles 114, cargo-cult-science 89, stop-yapping 131.
- first-principles: I must verify each claim in source and treat docs, names and variable names as hypotheses, and I will mark every guess from a name as a guess.
- cargo-cult-science: I must report everything that could invalidate a reading, and I will list it under Not determined and not present minified-code readings as documented behaviour.
- stop-yapping: I must cut every word past the answer, and I will write fragments with exact quotes, paths and numbers.

## Docs and changelog

Files in scratch dir `/Users/ryzhakar/pp/estafette/docs/orchestration_log/recon/2026-10-24/scratch/research-subagent-cache-lifetime/` (`doc-<page>.md` from `code.claude.com/docs/en/<page>.md`, `changelog.md` from raw GitHub main, `api-caching.md`). Line numbers are of those files.
- prompt-caching.md:269-272: "Claude Code decides the TTL per request, and every request falls in one of two fixed buckets: **Main conversation**: your interactive turns, non-interactive `-p` runs, and Agent SDK turns, plus the helpers Claude Code runs inline with them / **Everything else**: the requests Claude Code makes outside that conversation, such as subagents, workflows, in-process teammates, forks, compaction, and session titles"
- prompt-caching.md:274: "Unless you choose a TTL yourself, Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage."
- prompt-caching.md:278-279 (table): Main conversation: One hour (subscription within plan usage) / Five minutes (usage credits, API key, cloud provider). Everything else: "Five minutes, except the server-controlled helper requests, which get one hour" / Five minutes.
- prompt-caching.md:341 (section "Subagents and the cache"): "Subagents fall outside the main-conversation TTL bucket, so they get five minutes even on a subscription until you choose a longer one."
- prompt-caching.md:281: overage "drops the main conversation to the five-minute TTL, which charges a lower rate for cache writes."
- prompt-caching.md:265: 1h "keeps the cache warm through longer breaks but charges a higher rate for cache writes ... It costs more on short bursts of work that never idle past five minutes, where the higher write rate applies and the longer cache lifetime goes unused."
- workflows.md:342: "A workflow agent's requests fall outside the main conversation's cache TTL bucket, so its cache holds for five minutes by default, including on a Claude subscription. To keep it for an hour, set `subagentPromptCacheTtl` to `1h`."
- changelog 2.1.243 (changelog.md:4432): "Added `promptCacheTtl` and `subagentPromptCacheTtl` settings so API-key and cloud-provider users can keep a 1-hour prompt cache on the main conversation while subagents stay at 5 minutes". Docs say v2.1.242 (prompt-caching.md:290); changelog files the entry under 2.1.243. Mismatch unresolved; both below 2.1.322.
- changelog 2.1.248 (changelog.md:4275): "Added `experimental.cacheTtl` (`"5m"` or `"1h"`) to agent frontmatter: a per-agent prompt cache TTL used when no subagent TTL setting is configured"
- changelog 2.1.232 (changelog.md:4745): subagent forking on by default, "a `subagent_type: "fork"` subagent inherits the full conversation and prompt cache". prompt-caching.md:345: a fork "inherits the parent's system prompt, tools, and conversation history exactly, so its first request reads the parent's cache."
- Docs name no per-agent-type, per-teammate or per-launch-flag lever beyond those in Levers. `claude` CLI flags for TTL: none named in the fetched pages.

## Levers

Precedence, prompt-caching.md:292-299 (list items at 294-299): 1 `FORCE_PROMPT_CACHING_5M=1`; 2 bucket env var; 3 bucket setting; 4 subagent frontmatter `experimental.cacheTtl`; 5 `ENABLE_PROMPT_CACHING_1H=1`; 6 bucket default. Values accepted: `5m` or `1h` only (prompt-caching.md:285).
- `subagentPromptCacheTtl` (settings.json, any scope file; settings-reference.md:237, 751-760): "Choose how long the prompt cache holds the requests Claude Code makes outside the main conversation. This key applies to subagents, workflows, and Claude Code's own background and helper requests, such as compaction and session titles." Reaches subagents: yes.
- `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` (env-vars.md:404): "for requests outside the main conversation, such as subagents, workflows, and background work. Takes precedence over the `subagentPromptCacheTtl` setting and over `ENABLE_PROMPT_CACHING_1H`, and `FORCE_PROMPT_CACHING_5M` overrides it. The API bills 1-hour cache writes at a higher rate." Reaches subagents: yes.
- `experimental.cacheTtl` in subagent file frontmatter (sub-agents.md:316-325): "choose the prompt cache lifetime for this subagent's requests ... ignores `1h` while your Claude subscription is using usage credits, and reads the field only from subagent files." Reaches subagents: yes, per agent file; not for built-in or fork (not stated).
- `ENABLE_PROMPT_CACHING_1H=1` (env-vars.md:472): "request a 1-hour prompt cache TTL instead of the default 5 minutes ... For subscription users within included usage, Claude Code requests the 1-hour TTL automatically on the main conversation." prompt-caching.md:298 and agent-sdk cost-tracking.md:384: "asks for the 1-hour TTL on every request in both buckets". Reaches subagents: yes.
- `FORCE_PROMPT_CACHING_5M=1` (env-vars.md:477): forces 5m; overrides all above. Reaches subagents: yes (forces them to 5m).
- `promptCacheTtl` (settings-reference.md:165, 713) and `CLAUDE_CODE_PROMPT_CACHE_TTL` (env-vars.md:366): main conversation only: "for the main conversation: your interactive, `-p`, and SDK turns, plus the helpers that run inline with them". Reaches subagents: no.
- `ENABLE_PROMPT_CACHING_1H_BEDROCK` (env-vars.md:473): "Deprecated. Use `ENABLE_PROMPT_CACHING_1H` instead."
- `DISABLE_PROMPT_CACHING`, `_HAIKU`, `_SONNET`, `_OPUS`, `_FABLE` (env-vars.md:461-465): disable caching, not TTL. Reaches subagents by model (prompt-caching.md:366: Haiku "wherever that model runs").
- Plan feature: not a lever. The subscription-within-usage condition decides the main-bucket default (prompt-caching.md:274); plan tier is not named.
- Cost, prompt-caching.md:290 and settings-reference.md:713: set via these levers, writes cost more. Pricing quote, api-caching.md:295-296: "Cache write tokens with a 5-minute TTL are 1.25 times the base input tokens price. Cache write tokens with a 1-hour TTL are 2 times the base input tokens price." Cache reads: one column "Cache hits and refreshes" for both TTLs (api-caching.md:261); example row Fable 5.2: base $8, 5m write $10, 1h write $16, hit $0.20 per MTok.
- Gateway: `ANTHROPIC_BASE_URL` gateways must forward the `anthropic-beta` header for 1h (prompt-caching.md:307).

## Installed program

Binary `/Users/ryzhakar/.local/share/claude/versions/2.1.322` (Mach-O arm64, 323,702,464 bytes; `~/.local/bin/claude` symlinks to it; `command -v claude` is empty because `claude` is a shell function). Search by `strings -n 8` into scratch `strings.txt`, then `grep -a`. All below is a reading of minified code, not documented behaviour.
- TTL chooser, strings.txt:375284: `function cwn(e,n,r=!1){if(i.FORCE_PROMPT_CACHING_5M)return{ttl:"5m",reason:"force_5m_env"};let s=dOr(e),h=s?i.CLAUDE_CODE_PROMPT_CACHE_TTL:i.CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL;if(h!==void 0)return{ttl:h,reason:"env"};let y=St(),w=s?y.promptCacheTtl:y.subagentPromptCacheTtl;if(w!==void 0)return{ttl:w,reason:"setting"};if(n!==void 0&&!(n==="1h"&&r))return{ttl:n,reason:"agent_frontmatter"};if(i.ENABLE_PROMPT_CACHING_1H||...)return{ttl:"1h",reason:"enable_1h_env"};return}` Matches the documented order.
- Bucket test, same line: `var Hst=["repl_main_thread*","sdk","auto_mode","memdir_relevance"];function dOr(e){return Bst(e,Hst)}` (e = request query source). Reading: a query source outside this list is the subagent bucket.
- Default, strings.txt:392747: `function bMe(e,{agentCacheTtlOverride:n,ignoreOverage:r=!1,mainThreadModel:s}={}){...w=y&&!r&&bi().isUsingOverage===!0,b=cwn(h,n,w);if(b!==void 0)return b;if(!y||w)return{ttl:"5m",reason:"default"};let H=d8s();if(H===null)H=k("tengu_prompt_cache_1h_config",{allowlist:[...Hst]}).allowlist??[],c8s(H);if(!Bst(h,H))return{ttl:"5m",reason:"default"};...return{ttl:"1h",reason:"subscriber"}}` Reading: 1h default needs subscriber (y), not overage, and a query source in an allowlist from remote flag `tengu_prompt_cache_1h_config`, local fallback = the four sources above. Fits the docs' "server-controlled helper requests". Reading: the server can add sources; nothing local does.
- `S1(e)`: `function S1(e){return i.CLAUDE_CODE_MESSAGES_PROMPT_CACHE_TTL==="5m"?"5m":e}`. Variable `CLAUDE_CODE_MESSAGES_PROMPT_CACHE_TTL` is in no fetched doc page or changelog (`grep -c` 0 in all). Guess from name and `S1`: forces 5m on a messages path only; scope unread.
- Schema texts, strings.txt:214736 and 247925-247926: agent frontmatter "Prompt cache TTL for this agent's requests ("5m" or "1h") when no `subagentPromptCacheTtl` setting or env var is set. "1h" is ignored while a Claude subscription is in overage." Setting: "Prompt cache TTL for everything outside the main conversation — subagents, workflows, background and helper requests: ... Unset = automatic (5 minutes unless ENABLE_PROMPT_CACHING_1H=1)."
- Counts (`grep -a -c` on binary): `ephemeral` 73 lines, `cache_control` 39, `PROMPT_CACH` 12 (65 `_PROMPT_CACH` tokens by `-o`).

## Table

| lever | source | documented or inferred | reaches subagents | cost side stated |
| - | - | - | - | - |
| `subagentPromptCacheTtl` setting | settings-reference.md:751; prompt-caching.md:288 | documented; code confirmed | yes | yes, settings-reference.md:753 "bills each cache write at a higher rate"; 2x base input, api-caching.md:296 |
| `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` | env-vars.md:404 | documented; code confirmed | yes | yes, env-vars.md:404 |
| `experimental.cacheTtl` frontmatter | sub-agents.md:316; changelog 2.1.248 | documented; code confirmed | yes, per subagent file | not stated on that page; `1h` ignored in overage |
| `ENABLE_PROMPT_CACHING_1H=1` | env-vars.md:472; prompt-caching.md:298 | documented; code confirmed | yes (both buckets) | yes, env-vars.md:472 |
| `FORCE_PROMPT_CACHING_5M=1` | env-vars.md:477 | documented; code confirmed | yes (forces 5m) | lower rate, prompt-caching.md:281 |
| `promptCacheTtl`, `CLAUDE_CODE_PROMPT_CACHE_TTL` | settings-reference.md:713; env-vars.md:366 | documented | no, main bucket only | yes |
| `CLAUDE_CODE_MESSAGES_PROMPT_CACHE_TTL` | strings.txt:375284 only | inferred (minified code) | not stated | not stated |
| remote flag `tengu_prompt_cache_1h_config` allowlist | strings.txt:392747; prompt-caching.md:274 "server-controlled helper requests" | inferred; user cannot set | not stated | n/a |
| plan tier / subscription | prompt-caching.md:274 | documented as main-bucket default only | no | n/a |

## Not determined

- Whether `subagentPromptCacheTtl: "1h"` in the session's real settings gives these 493-transcript-class subagents 1h writes. Experiment: set it in a scratch settings file, launch one subagent from an interactive session on 2.1.322, read `ephemeral_1h_input_tokens` in its transcript. (Docs and code agree; not run.)
- Whether the session already has a TTL variable or setting set that explains the 5m tags. Experiment: read the user, project and managed settings files and test the two variable names for presence with a yes/no construct. Not read; outside the sources named.
- Whether Agent-tool launches, teammates and worktree agents all take the non-main bucket. Docs list subagents, teammates, forks in "Everything else" (prompt-caching.md:272) but say a fork reads the parent's cache (:345). Experiment: one launch of each kind, compare tags. The 493 transcripts all being 5m is consistent, but the sample's fork share is unknown.
- Whether `experimental.cacheTtl: 1h` reaches a launch whose `subagent_type` is a plugin agent or the `claude`/`general-purpose` built-ins (docs: "reads the field only from subagent files"). Experiment: one launch per type with the field.
- Meaning and scope of `CLAUDE_CODE_MESSAGES_PROMPT_CACHE_TTL`. Experiment: set it to `5m` in a scratch run and read tags on main and subagent requests.
- Docs version mismatch 2.1.242 vs 2.1.243. Experiment: none needed on 2.1.322; both are older.
- Whether the remote allowlist `tengu_prompt_cache_1h_config` currently contains a subagent query source on this account. Experiment: none user-side; the 5m tags suggest not.
- Whether 1h pays off: write 2x vs 1.25x base against a reread of about four fifths of context per 6-55 minute gap. Break-even not computed here; no price for the models in use was read.

Scratch left for the lead to clear (nothing deleted): `/Users/ryzhakar/pp/estafette/docs/orchestration_log/recon/2026-10-24/scratch/research-subagent-cache-lifetime/` holding doc-*.md, changelog.md, api-caching.md, strings.txt (71 MB), strings.err, strings.done.

Result: PASS
