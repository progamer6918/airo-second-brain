#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${AIRO_REPO_DIR:-$HOME/vortex-ai-skill-lab}"
SRC="$REPO_DIR/scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs"
LIVE_DIR="$REPO_DIR/apps-script-live"
LIVE="$LIVE_DIR/AIRO_Finance_Multitab_Final_v1.js"
test -f "$SRC"
test -d "$LIVE_DIR"
cp "$SRC" "$LIVE"
cd "$LIVE_DIR"

# Current Web App deployment ID from the working /exec URL.
# Override if needed:
# export AIRO_DEPLOYMENT_ID="AKfycb...."
DEPLOYMENT_ID="${AIRO_DEPLOYMENT_ID:-AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA}"

STAMP="$(date +%Y%m%d_%H%M%S)"
DESC="AIRO Finance deploy $STAMP"

echo "===== CLASP VERSION ====="
npx clasp --version

echo
echo "===== PUSH SOURCE ====="
npx clasp push -f

echo
echo "===== CREATE VERSION ====="
VERSION_OUTPUT="$(npx clasp create-version "$DESC" 2>&1 || npx clasp version "$DESC" 2>&1)"
echo "$VERSION_OUTPUT"

VERSION_NUMBER="$(echo "$VERSION_OUTPUT" | grep -oE '[0-9]+' | tail -n 1)"

if [ -z "$VERSION_NUMBER" ]; then
  echo "ERROR: Cannot parse version number."
  exit 1
fi

echo
echo "Created version: $VERSION_NUMBER"

echo
echo "===== UPDATE EXISTING WEB APP DEPLOYMENT ====="
npx clasp create-deployment \
  --deploymentId "$DEPLOYMENT_ID" \
  --versionNumber "$VERSION_NUMBER" \
  --description "$DESC"


echo
echo "DONE_AIRO_APPS_SCRIPT_DEPLOY"
echo "Deployment ID: $DEPLOYMENT_ID"
echo "Version: $VERSION_NUMBER"
