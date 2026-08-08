#!/usr/bin/env python3
"""Extract quantitative metrics from Claude Code session JSONL files.

Usage:
    uv run python3 extract_metrics.py <session-dir> [output.md]

Where <session-dir> is:
    ~/.claude-shared/projects/{project-slug}/{session-id}/

Or pass the project slug directory to scan all sessions:
    ~/.claude-shared/projects/{project-slug}/
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def model_tier(model_str: str) -> str:
    if not model_str:
        return "unknown"
    m = model_str.lower()
    if "haiku" in m:
        return "haiku"
    if "sonnet" in m:
        return "sonnet"
    if "opus" in m:
        return "opus"
    return "unknown"


def parse_jsonl(path: Path) -> list[dict]:
    records = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except (OSError, UnicodeDecodeError):
        pass
    return records


def extract_metrics(root: Path) -> dict:
    jsonl_files = list(root.rglob("*.jsonl"))

    sessions: set[str] = set()
    agents: set[str] = set()
    tool_calls: dict[str, int] = defaultdict(int)
    tokens: dict[str, dict[str, int]] = {
        t: {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
        for t in ("opus", "sonnet", "haiku", "unknown")
    }
    timestamps: list[str] = []

    for path in jsonl_files:
        for rec in parse_jsonl(path):
            # Session and agent tracking
            sid = rec.get("sessionId", "")
            if sid:
                sessions.add(sid)
            aid = rec.get("agentId", "")
            if aid:
                agents.add(aid)

            ts = rec.get("timestamp", "")
            if ts:
                timestamps.append(ts)

            msg = rec.get("message", {})
            model = msg.get("model", "")
            tier = model_tier(model)

            # Token accumulation
            usage = msg.get("usage", {})
            if usage:
                tokens[tier]["input"]       += usage.get("input_tokens", 0)
                tokens[tier]["output"]      += usage.get("output_tokens", 0)
                tokens[tier]["cache_read"]  += usage.get("cache_read_input_tokens", 0)
                tokens[tier]["cache_write"] += usage.get("cache_creation_input_tokens", 0)

            # Tool calls
            for block in msg.get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_calls[block.get("name", "unknown")] += 1

    return {
        "sessions": sorted(sessions),
        "agent_count": len(agents),
        "jsonl_files": len(jsonl_files),
        "earliest": min(timestamps) if timestamps else "unknown",
        "latest": max(timestamps) if timestamps else "unknown",
        "tool_calls": dict(sorted(tool_calls.items(), key=lambda x: -x[1])),
        "tokens": tokens,
    }


def format_report(m: dict, root: Path) -> str:
    lines = [
        f"# Session Metrics",
        f"",
        f"**Source:** `{root}`",
        f"**Generated:** {datetime.now().isoformat()}",
        f"",
        f"## Overview",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| JSONL files scanned | {m['jsonl_files']:,} |",
        f"| Distinct sessions | {len(m['sessions'])} |",
        f"| Subagents dispatched | {m['agent_count']:,} |",
        f"| Earliest timestamp | {m['earliest'][:19]} |",
        f"| Latest timestamp | {m['latest'][:19]} |",
        f"",
        f"## Token Usage by Model Tier",
        f"",
        f"| Tier | Input | Output | Cache Read | Cache Write |",
        f"|------|-------|--------|------------|-------------|",
    ]
    for tier in ("opus", "sonnet", "haiku", "unknown"):
        t = m["tokens"][tier]
        if any(t.values()):
            lines.append(
                f"| {tier.title()} "
                f"| {t['input']:,} "
                f"| {t['output']:,} "
                f"| {t['cache_read']:,} "
                f"| {t['cache_write']:,} |"
            )
    lines += [
        f"",
        f"## Tool Call Counts",
        f"",
        f"| Tool | Calls |",
        f"|------|-------|",
    ]
    mcp_total = 0
    for name, count in m["tool_calls"].items():
        lines.append(f"| {name} | {count:,} |")
        if name.startswith("mcp__"):
            mcp_total += count
    lines += [
        f"",
        f"**Total MCP calls:** {mcp_total:,}",
        f"",
        f"## Session IDs",
        f"",
    ]
    for sid in m["sessions"]:
        lines.append(f"- `{sid}`")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    root = Path(sys.argv[1]).expanduser()
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    metrics = extract_metrics(root)
    report = format_report(metrics, root)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report)
        print(f"Written to {output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
