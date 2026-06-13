#!/usr/bin/env bash
set -e
cd /home/egitaristorandas/AI_WORKSPACES/airo-second-brain

OUT="/tmp/airo_git_commit_$(date +%Y%m%d_%H%M%S).txt"
{
  git add .
  git commit -m "fix(airo-brain): finalize Earesmes Telegram gateway routing"
  git push
} 2>&1 | tee "$OUT"
cat "$OUT" | clip.exe
echo "COPIED_TO_CLIPBOARD=$OUT"
