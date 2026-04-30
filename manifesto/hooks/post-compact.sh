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

# Render orchestrator elements as natural language prose
ELEMENT_DESCRIPTION=$(python3 << 'PYEOF'
import json, os

stack = json.loads(os.environ["YOU_STACK"])
n = len(stack)
count_word = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight"}.get(n, str(n))
sentences = [f"Your constitution has {count_word} element{'s' if n != 1 else ''}."]

for el in stack:
    name = el["name"]
    purpose = el.get("purpose")
    source = el.get("source")
    if purpose and source:
        sentences.append(f'"{name}" governs your {purpose} — fetch it from {source}.' if source.startswith("http") else f'"{name}" governs your {purpose} — read it from {source}.')
    elif purpose:
        sentences.append(f'"{name}" governs your {purpose}.')
    elif source:
        sentences.append(f'"{name}" is part of your constitution — fetch it from {source}.' if source.startswith("http") else f'"{name}" is part of your constitution — read it from {source}.')
    else:
        sentences.append(f'"{name}" is part of your constitution.')

print(" ".join(sentences))
PYEOF
)

export ELEMENT_DESCRIPTION MANIFESTO_DIR PROJECT_DIR
envsubst '${ELEMENT_DESCRIPTION} ${MANIFESTO_DIR} ${PROJECT_DIR}' < "$SCRIPT_DIR/templates/post-compact.txt"
