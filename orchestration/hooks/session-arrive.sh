#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
REF_DIR="$PROJECT_DIR/orchestration_log/reference"

# Gate: no reference directory = no orchestration session active
[ -d "$REF_DIR" ] || exit 0

export REF_DIR PROJECT_DIR
# Dependency-free stand-in for envsubst, which is not guaranteed installed.
python3 -c '
import os, re, sys
allowed = {"REF_DIR", "PROJECT_DIR"}
text = open(sys.argv[1]).read()
def repl(m):
    return os.environ.get(m.group(1), "") if m.group(1) in allowed else m.group(0)
sys.stdout.write(re.sub(r"\$\{(\w+)\}", repl, text))
' "$SCRIPT_DIR/templates/arrive-context.txt"
exit 0
