#!/usr/bin/env bash
# The rubric lives in review-calls; skills can't reliably read each other's files in chat,
# so grade-pasted-call ships its own copy. Run this after editing the rubric.
set -euo pipefail
cd "$(dirname "$0")/../plugins/sales-call-review/skills"
cp review-calls/references/rubric.md grade-pasted-call/references/rubric.md
echo "rubric synced"
