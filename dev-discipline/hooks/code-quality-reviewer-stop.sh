#!/bin/bash
set -euo pipefail

# SubagentStop hook for code-quality-reviewer agents.
# Fires when a code-quality-reviewer finishes. Injects merge-decision mandate into orchestrator context.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Read stdin for agent metadata
INPUT=$(cat)

# Guard against re-entry
STOP_HOOK_ACTIVE=$(echo "$INPUT" | python3 -c 'import sys,json; print(json.loads(sys.stdin.read()).get("stop_hook_active", False))' 2>/dev/null || echo "False")
if [ "$STOP_HOOK_ACTIVE" = "True" ]; then
    exit 0
fi

# Extract agent info for the template
AGENT_TYPE=$(echo "$INPUT" | python3 -c 'import sys,json; print(json.loads(sys.stdin.read()).get("agent_type", "unknown"))' 2>/dev/null || echo "unknown")
LAST_MESSAGE=$(echo "$INPUT" | python3 -c 'import sys,json; msg=json.loads(sys.stdin.read()).get("last_assistant_message", ""); print(msg[:500])' 2>/dev/null || echo "")

export AGENT_TYPE LAST_MESSAGE
# Dependency-free stand-in for envsubst, which is not guaranteed installed.
python3 -c '
import os, re, sys
allowed = {"AGENT_TYPE", "LAST_MESSAGE"}
text = open(sys.argv[1]).read()
def repl(m):
    return os.environ.get(m.group(1), "") if m.group(1) in allowed else m.group(0)
sys.stdout.write(re.sub(r"\$\{(\w+)\}", repl, text))
' "$SCRIPT_DIR/templates/merge-mandate.txt"
