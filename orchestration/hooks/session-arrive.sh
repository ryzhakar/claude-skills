#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
REF_DIR="$PROJECT_DIR/orchestration_log/reference"

# Gate: no reference directory = no orchestration session active
[ -d "$REF_DIR" ] || exit 0

export REF_DIR PROJECT_DIR
envsubst '${REF_DIR} ${PROJECT_DIR}' < "$SCRIPT_DIR/templates/arrive-context.txt"
