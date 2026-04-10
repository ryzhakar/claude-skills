# Session JSONL Data Schema

Raw session data for parsing by metric extraction agents.

## File Locations

```
~/.claude-shared/projects/{project-slug}/
  {session-id}.jsonl                    # Main session (orchestrator)
  {session-id}/subagents/
    agent-{id}.jsonl                    # Per-agent conversations
    agent-{id}.meta.json                # Agent metadata
```

Project slug: replace `/` with `-`, strip leading `-`.
Example: `/Users/ryzhakar/competera/my-project` → `-Users-ryzhakar-competera-my-project`

## JSONL Record Fields

Each line is a complete JSON object:

```json
{
  "parentUuid": "uuid-or-null",
  "isSidechain": true,
  "promptId": "uuid",
  "agentId": "agent-{hex-string}",
  "type": "user" | "assistant",
  "message": {
    "role": "user" | "assistant",
    "model": "claude-opus-4-6" | "claude-sonnet-4-5-20250929" | "claude-haiku-4-5-20251001",
    "content": [...],
    "usage": {
      "input_tokens": 945,
      "output_tokens": 22048,
      "cache_read_input_tokens": 32000000,
      "cache_creation_input_tokens": 5200000
    }
  },
  "timestamp": "2026-04-09T19:27:12.161000+00:00",
  "sessionId": "uuid",
  "gitBranch": "main"
}
```

## Content Block Types

```json
// Tool use (agent calling a tool)
{"type": "tool_use", "id": "toolu_vrtx_...", "name": "Read", "input": {...}}

// Tool result (tool response)
{"type": "tool_result", "tool_use_id": "toolu_vrtx_...", "content": "..."}

// Agent dispatch (orchestrator calling Agent tool)
{"type": "tool_use", "name": "Agent", "input": {"description": "...", "model": "sonnet"}}

// Text
{"type": "text", "text": "..."}
```

## Model Tier Detection

```python
def model_tier(model_str: str) -> str:
    if "haiku" in model_str.lower():
        return "haiku"
    elif "sonnet" in model_str.lower():
        return "sonnet"
    elif "opus" in model_str.lower():
        return "opus"
    return "unknown"
```

## Agent Dispatch Counting

Count unique `agentId` values across all JSONL files. Each unique agentId (excluding the main session's orchestrator ID) represents one dispatched subagent.

Alternatively, count `Agent` tool_use blocks in the orchestrator JSONL — each is one agent dispatch.

## Cost Formulas (as of 2026-04)

```python
COST_PER_1M = {
    "opus":   {"input": 15.00, "output": 75.00, "cache_read": 1.50,  "cache_write": 3.75},
    "sonnet": {"input":  3.00, "output": 15.00, "cache_read": 0.30,  "cache_write": 0.75},
    "haiku":  {"input":  0.80, "output":  4.00, "cache_read": 0.08,  "cache_write": 0.20},
}

def compute_cost(tier, usage):
    rates = COST_PER_1M[tier]
    return (
        usage["input_tokens"]              / 1e6 * rates["input"]       +
        usage["output_tokens"]             / 1e6 * rates["output"]      +
        usage["cache_read_input_tokens"]   / 1e6 * rates["cache_read"]  +
        usage["cache_creation_input_tokens"] / 1e6 * rates["cache_write"]
    )
```

Note: The `/cost` command in Claude Code gives the authoritative cost for the current session. Use these formulas only to estimate distribution across model tiers.

## Key Insight: Cache Dominates Cost

In long sessions, cache_read_input_tokens can be 100-800x larger than direct input_tokens. The orchestrator's context window accumulates and is re-sent as cache every turn. This is why Opus dominates cost even when agents do most of the work — the orchestrator's long context is expensive to cache-read repeatedly.
