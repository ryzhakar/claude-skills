#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
detect_manifestos

# Gate: no config → silent exit
if [ -z "${YOU_STACK:-}" ] || [ "$YOU_STACK" = "[]" ]; then
    exit 0
fi

python3 "$SCRIPT_DIR/parse_taglines.py"

exit 0
