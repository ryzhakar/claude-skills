#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# Gate: no charter, no project for memento to orient in.
[ -f "$PROJECT_DIR/CLAUDE.md" ] || exit 0

cat "$SCRIPT_DIR/templates/orientation-reminder.txt"
exit 0
