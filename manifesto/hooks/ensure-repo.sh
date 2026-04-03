#!/bin/bash
# Shared helper: ensure manifesto repo is cloned. Lazy — only clones if missing.
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

    if [ -f "$config_file" ]; then
        cat "$config_file"
    elif [ -f "$claude_md" ]; then
        sed -n '/^## Active Manifestos/,/^## /{ /^## Active Manifestos/d; /^## /d; p; }' "$claude_md"
    fi
}
