#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
detect_manifestos

# Gate: no config → silent exit
if [ -z "${YOU_STACK:-}" ] && [ -z "${SUBAGENT_SECTION:-}" ]; then
    exit 0
fi
if [ "${YOU_STACK:-[]}" = "[]" ] && [ "${SUBAGENT_SECTION:-\{\}}" = "{}" ]; then
    exit 0
fi

cat "$SCRIPT_DIR/templates/subagent-start.txt"
