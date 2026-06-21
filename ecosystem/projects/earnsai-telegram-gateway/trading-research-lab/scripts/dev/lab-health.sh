#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_MD="reports/lab_health_$TS.md"
OUT_JSON="reports/lab_health_$TS.json"
LATEST_MD="reports/LAB_HEALTH_LATEST.md"
LATEST_JSON="reports/LAB_HEALTH_LATEST.json"
TMP_JSON="$(mktemp)"

echo "== EarnsAI Research Lab Health v0.1 =="
echo "Mode: full local read-only verification bundle"
echo "Network/API/live trading: disabled"
echo ".env/credentials: not read"
echo ""

python3 - "$TMP_JSON" <<'PY'
import json, sys
from datetime import datetime
Path = __import__("pathlib").Path

tmp = Path(sys.argv[1])
data = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "phase": "Phase 4 — Trading Research Lab",
    "baseline": "EarnsAI Pulse v3.1.9 Sequential Handler Mode VERIFIED",
    "mode": "full local read-only verification bundle",
    "steps": []
}
tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
PY

run_step() {
  local name="$1"
  local cmd="$2"
  local log_file="reports/lab_health_${TS}_${name}.log"

  echo ""
  echo ">>> $name"

  local start
  start="$(date +%s)"

  if bash -lc "$cmd" > "$log_file" 2>&1; then
    local end
    end="$(date +%s)"
    local duration=$((end - start))
    echo "PASS: $name (${duration}s)"

    python3 - "$TMP_JSON" "$name" "PASS" "$duration" "$log_file" <<'PY'
import json, sys
from pathlib import Path

tmp = Path(sys.argv[1])
name = sys.argv[2]
status = sys.argv[3]
duration = int(sys.argv[4])
log_file = sys.argv[5]

data = json.loads(tmp.read_text(encoding="utf-8"))
data["steps"].append({
    "name": name,
    "status": status,
    "duration_seconds": duration,
    "log_file": log_file
})
tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
PY
  else
    local end
    end="$(date +%s)"
    local duration=$((end - start))
    echo "FAILED: $name (${duration}s)"
    echo "Last 80 lines from $log_file:"
    tail -80 "$log_file" || true

    python3 - "$TMP_JSON" "$name" "FAILED" "$duration" "$log_file" <<'PY'
import json, sys
from pathlib import Path

tmp = Path(sys.argv[1])
name = sys.argv[2]
status = sys.argv[3]
duration = int(sys.argv[4])
log_file = sys.argv[5]

data = json.loads(tmp.read_text(encoding="utf-8"))
data["steps"].append({
    "name": name,
    "status": status,
    "duration_seconds": duration,
    "log_file": log_file
})
tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
PY
    return 1
  fi
}

run_step "verify-v319" "bash scripts/dev/verify-v319.sh"
run_step "diff-v319" "bash scripts/dev/diff-v319.sh"
run_step "command-audit" "bash scripts/dev/command-audit.sh"
run_step "research-status" "bash scripts/dev/research-status.sh"
run_step "state-doctor" "bash scripts/dev/state-doctor.sh"
run_step "research-report" "bash scripts/dev/research-report.sh"
run_step "analyze-paper" "bash scripts/dev/analyze-paper.sh"
run_step "inspect-backtest" "bash scripts/dev/inspect-backtest.sh"
run_step "summarize-datasets" "bash scripts/dev/summarize-datasets.sh"
run_step "lab-index" "bash scripts/dev/lab-index.sh"
run_step "check" "bash scripts/dev/check.sh"
run_step "smoke" "bash scripts/dev/smoke.sh"

python3 - "$TMP_JSON" "$OUT_MD" "$OUT_JSON" "$LATEST_MD" "$LATEST_JSON" <<'PY'
import json, sys
from pathlib import Path

tmp = Path(sys.argv[1])
out_md = Path(sys.argv[2])
out_json = Path(sys.argv[3])
latest_md = Path(sys.argv[4])
latest_json = Path(sys.argv[5])

data = json.loads(tmp.read_text(encoding="utf-8"))
steps = data["steps"]
passed = sum(1 for s in steps if s["status"] == "PASS")
failed = sum(1 for s in steps if s["status"] != "PASS")
data["summary"] = {
    "total_steps": len(steps),
    "passed": passed,
    "failed": failed,
    "health": "PASS" if failed == 0 else "FAILED"
}

lines = []
lines.append("# EarnsAI Research Lab Health v0.1")
lines.append("")
lines.append(f"- Generated at: {data['generated_at']}")
lines.append(f"- Phase: {data['phase']}")
lines.append(f"- Baseline: {data['baseline']}")
lines.append("- Mode: full local read-only verification bundle")
lines.append("- Network/API/live trading: disabled")
lines.append("- `.env` / credentials: not read")
lines.append("")
lines.append("## Summary")
lines.append("")
lines.append(f"- Health: `{data['summary']['health']}`")
lines.append(f"- Total steps: `{data['summary']['total_steps']}`")
lines.append(f"- Passed: `{data['summary']['passed']}`")
lines.append(f"- Failed: `{data['summary']['failed']}`")
lines.append("")
lines.append("## Steps")
lines.append("")
lines.append("| Step | Status | Duration | Log |")
lines.append("|---|---:|---:|---|")
for s in steps:
    lines.append(f"| `{s['name']}` | `{s['status']}` | {s['duration_seconds']}s | `{s['log_file']}` |")
lines.append("")
lines.append("## Result")
lines.append("")
if failed == 0:
    lines.append("Research Lab local verification bundle passed.")
else:
    lines.append("Research Lab local verification bundle failed. Inspect the failed step log.")
lines.append("")

report = "\n".join(lines)

out_md.write_text(report, encoding="utf-8")
latest_md.write_text(report, encoding="utf-8")
out_json.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
latest_json.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print("")
print(f"Lab health markdown created: {out_md}")
print(f"Lab health json created: {out_json}")
print(f"Latest markdown updated: {latest_md}")
print(f"Latest json updated: {latest_json}")
print("")
print(f"Research Lab health result: {data['summary']['health']}")

if failed:
    raise SystemExit(1)
PY

rm -f "$TMP_JSON"
