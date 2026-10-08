#!/usr/bin/env bash
# Builds dist/sales-call-review.zip for Customize → Plugins → Upload plugin (and GitHub Releases).
# Leaves out evals so users get only what the plugin needs.
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/sync-rubric.sh
mkdir -p dist
rm -f dist/sales-call-review.zip
(cd plugins && zip -qr ../dist/sales-call-review.zip sales-call-review -x "sales-call-review/evals/*" "*/.DS_Store" "*/__pycache__/*")
echo "built dist/sales-call-review.zip"
