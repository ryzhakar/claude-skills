#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
manifestos=$(detect_manifestos)

RESOLVE_INSTRUCTIONS="To resolve each entry:
- Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword
- URL (starts with http): fetch the full text
- Local path (starts with ./ or /): read relative to ${PROJECT_DIR}"

if [ -n "$manifestos" ]; then
    escaped=$(escape_json "$manifestos")
    cat <<EOF
MANIFESTO INITIALIZATION REQUIRED.

Declared manifestos:
${escaped}

${RESOLVE_INSTRUCTIONS}

Load each manifesto's full text. Apply the manifesto-oath skill (operational identity assumption, not theatrical oath). For multiple manifestos, map their interdependence graph.
EOF
else
    cat <<EOF
MANIFESTO PLUGIN ACTIVE — no manifesto configuration found (.manifestos.yaml or Active Manifestos section in CLAUDE.md).

Repo manifestos available in: ${MANIFESTO_DIR}/manifestos/

Delegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, (3) recommend which manifestos are relevant. Then ask the user whether to bind them.
EOF
fi
