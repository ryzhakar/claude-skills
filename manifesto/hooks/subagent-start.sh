#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
manifestos=$(detect_manifestos)

# Only inject if manifestos are declared
if [ -z "$manifestos" ]; then
    exit 0
fi

escaped=$(escape_json "$manifestos")
cat <<EOF
MANIFESTO CONTEXT: This project operates under these manifesto bindings:
${escaped}

Repo manifestos: ${MANIFESTO_DIR}/manifestos/
Local paths resolve from: ${PROJECT_DIR}

You are not required to perform the full oath ceremony. But be aware of these principles and let them inform your work. If you need the full text, read from the paths above or fetch URLs.
EOF
