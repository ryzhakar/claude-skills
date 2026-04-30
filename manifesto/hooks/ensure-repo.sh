#!/bin/bash
# Shared helper: ensure manifesto repo is cloned + parse .manifestos.yaml
# Sources this file from other hook scripts.

MANIFESTO_REPO="https://github.com/ryzhakar/LLM_MANIFESTOS.git"
MANIFESTO_DIR="/tmp/claude-manifesto-repo/LLM_MANIFESTOS"

if [ ! -d "$MANIFESTO_DIR/manifestos" ]; then
    mkdir -p /tmp/claude-manifesto-repo
    git clone --depth 1 --quiet "$MANIFESTO_REPO" "$MANIFESTO_DIR" 2>/dev/null || true
fi

escape_json() {
    printf '%s' "$1" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read())[1:-1], end="")'
}

detect_manifestos() {
    local project_dir="${CLAUDE_PROJECT_DIR:-.}"
    local config_file="$project_dir/.manifestos.yaml"
    local claude_md="$project_dir/CLAUDE.md"

    local raw=""
    if [ -f "$config_file" ]; then
        raw=$(cat "$config_file")
    elif [ -f "$claude_md" ]; then
        raw=$(sed -n '/^## Active Manifestos/,/^## /{ /^## Active Manifestos/d; /^## /d; p; }' "$claude_md")
    fi

    if [ -z "$raw" ]; then
        return
    fi

    # Parse YAML into JSON env vars: YOU_STACK, SUBAGENT_SECTION
    eval "$(python3 -c '
import sys, json, yaml

raw = sys.stdin.read().strip()
if not raw:
    sys.exit(0)

data = yaml.safe_load(raw)

def normalize_item(item):
    """String -> {name: str}; dict passes through."""
    if isinstance(item, str):
        return {"name": item}
    return item

def normalize_list(lst):
    return [normalize_item(i) for i in lst]

# Flat list at root = orchestrator only
if isinstance(data, list):
    you_stack = normalize_list(data)
    subagent_section = {}
elif isinstance(data, dict):
    you_raw = data.get("you", [])
    you_stack = normalize_list(you_raw) if isinstance(you_raw, list) else []
    sub_raw = data.get("subagents", {})
    subagent_section = {}
    if isinstance(sub_raw, dict):
        for role, items in sub_raw.items():
            if isinstance(items, list):
                subagent_section[role] = normalize_list(items)
else:
    you_stack = []
    subagent_section = {}

# Shell-safe export
you_json = json.dumps(you_stack)
sub_json = json.dumps(subagent_section)
print(f"YOU_STACK={repr(you_json)}")
print(f"SUBAGENT_SECTION={repr(sub_json)}")
' <<< "$raw")"

    export YOU_STACK SUBAGENT_SECTION
}
