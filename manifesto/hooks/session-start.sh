#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
manifestos=$(detect_manifestos)

RESOLVE_INSTRUCTIONS="To resolve each entry:\\n- Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword\\n- URL (starts with http): fetch the full text\\n- Local path (starts with ./ or /): read relative to ${PROJECT_DIR}"

if [ -n "$manifestos" ]; then
    escaped=$(escape_json "$manifestos")
    cat <<EOF
{
  "systemMessage": "MANIFESTO INITIALIZATION REQUIRED.\\n\\nDeclared manifestos:\\n${escaped}\\n\\n${RESOLVE_INSTRUCTIONS}\\n\\nLoad each manifesto's full text. Apply the manifesto-oath skill (operational identity assumption, not theatrical oath). For multiple manifestos, map their interdependence graph."
}
EOF
else
    cat <<EOF
{
  "systemMessage": "MANIFESTO PLUGIN ACTIVE — no manifesto configuration found (.manifestos.yaml or Active Manifestos section in CLAUDE.md).\\n\\nRepo manifestos available in: ${MANIFESTO_DIR}/manifestos/\\n\\nDelegate a subagent to: (1) briefly explore the project (language, domain, conventions), (2) read the available manifesto files in ${MANIFESTO_DIR}/manifestos/, (3) recommend which manifestos are relevant. Then ask the user whether to bind them."
}
EOF
fi
