#!/bin/bash
# Shared helper: ensure manifesto repo is cloned + parse .manifestos.yaml
# Source this file from hook scripts. No side effects on source.

MANIFESTO_REPO="https://github.com/ryzhakar/LLM_MANIFESTOS.git"
MANIFESTO_DIR="/tmp/claude-manifesto-repo/LLM_MANIFESTOS"

ensure_repo() {
    if [ ! -d "$MANIFESTO_DIR/manifestos" ]; then
        mkdir -p /tmp/claude-manifesto-repo
        git clone --depth 1 --quiet "$MANIFESTO_REPO" "$MANIFESTO_DIR" 2>/dev/null || true
    else
        git -C "$MANIFESTO_DIR" pull --quiet 2>/dev/null || true
    fi
}

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

    local _tmpdir
    _tmpdir=$(mktemp -d)
    python3 -c '
import os, sys, json, yaml

raw = sys.stdin.read().strip()
if not raw:
    sys.exit(0)

try:
    data = yaml.safe_load(raw)
except Exception:
    sys.exit(0)

def normalize_item(item):
    if item is None:
        return None
    if isinstance(item, dict):
        return item
    return {"name": str(item)}

def normalize_list(lst):
    return [x for x in (normalize_item(i) for i in lst) if x is not None]

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
    manifesto_dir = data.get("manifesto_dir")
else:
    you_stack = []
    subagent_section = {}

outdir = sys.argv[1]
with open(os.path.join(outdir, "you"), "w") as f:
    json.dump(you_stack, f)
with open(os.path.join(outdir, "sub"), "w") as f:
    json.dump(subagent_section, f)
mdir = locals().get("manifesto_dir") or ""
if mdir:
    with open(os.path.join(outdir, "mdir"), "w") as f:
        f.write(str(mdir))
' "$_tmpdir" <<< "$raw" 2>/dev/null

    if [ -f "$_tmpdir/you" ]; then
        YOU_STACK=$(cat "$_tmpdir/you")
        SUBAGENT_SECTION=$(cat "$_tmpdir/sub")
        if [ -f "$_tmpdir/mdir" ]; then
            MANIFESTO_DIR=$(cat "$_tmpdir/mdir")
        fi
    fi
    rm -rf "$_tmpdir"

    export YOU_STACK SUBAGENT_SECTION MANIFESTO_DIR
}
