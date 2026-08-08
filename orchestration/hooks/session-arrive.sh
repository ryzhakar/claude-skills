#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
REF_DIR="$PROJECT_DIR/orchestration_log/reference"

# Gate: no reference directory = no orchestration session active
[ -d "$REF_DIR" ] || exit 0

STATE_FILE="$PROJECT_DIR/orchestration_log/recon/$(date +%F)/session-state.md"
export REF_DIR PROJECT_DIR
envsubst '${REF_DIR} ${PROJECT_DIR}' < "$SCRIPT_DIR/templates/arrive-context.txt"
[ -f "$STATE_FILE" ] && printf '\n6. %s — in-flight state from this session\n' "$STATE_FILE"
exit 0
