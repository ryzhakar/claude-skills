#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
manifestos=$(detect_manifestos)

# Gate: no config → silent exit
if [ -z "$manifestos" ]; then
    exit 0
fi

MANIFESTO_LIST=$(escape_json "$manifestos")
RESOLVE_INSTRUCTIONS="Resolve each entry by its shape:
- Plain name (e.g. 'decomplect'): find by keyword in ${MANIFESTO_DIR}/manifestos/
- URL (http/https): fetch the full text from that URL
- Local path (./ or /): read the file from ${PROJECT_DIR}"

export MANIFESTO_LIST RESOLVE_INSTRUCTIONS
envsubst '${MANIFESTO_LIST} ${RESOLVE_INSTRUCTIONS}' < "$SCRIPT_DIR/templates/subagent-start.txt"
