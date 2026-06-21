#!/usr/bin/env bash
set -euo pipefail

cat > /tmp/airo_exact_header_patch.py <<'PY'
from pathlib import Path

path = Path("/home/egitaristorandas/vortex-ai-skill-lab/scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")
text = path.read_text(encoding="utf-8")

old = """    const findColumn_ = function(info, aliases, fallbackIndex) {
      for (var i = 0; i < info.normalized.length; i++) {
        for (var j = 0; j < aliases.length; j++) {
          if (info.normalized[i] === aliases[j] || info.normalized[i].indexOf(aliases[j]) >= 0) {
            return i + 1;
          }
        }
      }
      return fallbackIndex;
    };
"""

new = """    const findColumn_ = function(info, aliases, fallbackIndex) {
      for (var i = 0; i < info.normalized.length; i++) {
        for (var j = 0; j < aliases.length; j++) {
          if (info.normalized[i] === aliases[j]) {
            return i + 1;
          }
        }
      }
      for (var i2 = 0; i2 < info.normalized.length; i2++) {
        for (var j2 = 0; j2 < aliases.length; j2++) {
          if (String(aliases[j2] || "").length >= 5 && info.normalized[i2].indexOf(aliases[j2]) >= 0) {
            return i2 + 1;
          }
        }
      }
      return fallbackIndex;
    };
"""

marker = "String(aliases[j2] || \"\").length >= 5"
if marker in text:
    print("PATCH_ALREADY_PRESENT")
else:
    count = text.count(old)
    print("FINDCOLUMN_BLOCK_COUNT", count)
    if count < 2:
        raise SystemExit("ABORT: expected at least 2 findColumn_ helpers")
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print("PATCH_DONE")
PY

cd /home/egitaristorandas/vortex-ai-skill-lab

echo "## branch"
git branch --show-current

echo "## status before"
git status --short

echo "## latest commit"
git log -1 --oneline

echo "## safety: require expected base commit"
if ! git log -1 --oneline | grep -q "^e6dcc50 "; then
  echo "ABORT: latest commit is not e6dcc50"
  exit 1
fi

echo "## patch"
python3 /tmp/airo_exact_header_patch.py
rm -f /tmp/airo_exact_header_patch.py

echo "## status after patch"
git status --short

echo "## safety: require only approved file modified"
status="$(git status --short)"
printf "%s\n" "$status"
if printf "%s\n" "$status" | grep -v "^ M scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs$" | grep -q .; then
  echo "ABORT: unexpected git status entry detected"
  exit 1
fi

echo "## diff stat"
git diff --stat

echo "## diff check"
git diff --check

echo "## stage approved file only"
git add scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs

echo "## staged files"
git diff --cached --name-only

echo "## staged stat"
git diff --cached --stat

echo "## forbidden staged path check"
if git diff --cached --name-only | grep -Ei "(^|/)(\.env|.*secret.*|.*token.*|.*credential.*|.*cookie.*|.*session.*|.*api.?key.*|runtime|EarnsAI|trading|receipts|oauth|local\.db|\.sqlite|\.sqlite3)($|/)"; then
  echo "ABORT: forbidden staged path detected"
  git reset -- scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs
  exit 1
fi

echo "## commit"
git commit -m "fix(airo-finance): prefer exact headers in cash parity audits"

echo "## latest commit after commit"
git log -1 --oneline

echo "## push"
git -c credential.helper="!gh auth git-credential" push origin main

echo "## sync source to apps-script-live"
cp scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs apps-script-live/AIRO_Finance_Multitab_Final_v1.js

echo "## verify source/live identical"
diff -q scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs apps-script-live/AIRO_Finance_Multitab_Final_v1.js

echo "## deploy via official script"
export PATH=$PATH:~/.npm-global/bin
bash scripts/personal-workflow/airo_apps_script_deploy.sh

echo "## final status"
git status --short

echo "## final commit"
git log -1 --oneline
