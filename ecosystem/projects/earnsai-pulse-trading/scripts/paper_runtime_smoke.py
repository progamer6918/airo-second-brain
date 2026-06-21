#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

base_config_path = Path("runtime/paper_runtime/config.json")
smoke_config_path = Path("runtime/paper_runtime/config.smoke.json")

config = json.loads(base_config_path.read_text(encoding="utf-8"))

config["tick_interval_seconds"] = 0
config["report_interval_seconds"] = 999999
config["trade_notifications"] = False
config["periodic_reports"] = False

config["storage"] = {
    "state_json": "runtime/paper_runtime/smoke_state.json",
    "signals_jsonl": "runtime/paper_runtime/smoke_signals.jsonl",
    "trades_csv": "runtime/paper_runtime/smoke_trades.csv",
    "performance_jsonl": "runtime/paper_runtime/smoke_performance.jsonl",
    "runtime_log": "runtime/paper_runtime/smoke_runtime.log"
}

for file in config["storage"].values():
    path = Path(file)
    if path.exists():
        path.unlink()

smoke_config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

cmd = [
    sys.executable,
    "-m",
    "earnsai.paper_runtime.runtime",
    "--config",
    str(smoke_config_path),
    "--max-cycles",
    "35",
]

result = subprocess.run(cmd, text=True, capture_output=True, timeout=120)

print(result.stdout)

if result.returncode != 0:
    print(result.stderr)
    raise SystemExit(result.returncode)

required = [
    Path("runtime/paper_runtime/smoke_state.json"),
    Path("runtime/paper_runtime/smoke_signals.jsonl"),
    Path("runtime/paper_runtime/smoke_performance.jsonl"),
    Path("runtime/paper_runtime/smoke_runtime.log"),
]

for path in required:
    if not path.exists() or path.stat().st_size == 0:
        print(f"PAPER_RUNTIME_SMOKE FAIL missing_or_empty={path}")
        raise SystemExit(1)

state = json.loads(Path("runtime/paper_runtime/smoke_state.json").read_text(encoding="utf-8"))

if state.get("mode") != "PAPER_ONLY":
    print("PAPER_RUNTIME_SMOKE FAIL unsafe_mode")
    raise SystemExit(1)

if state.get("live_trading_locked") is not True:
    print("PAPER_RUNTIME_SMOKE FAIL live_lock_not_true")
    raise SystemExit(1)

perf_lines = Path("runtime/paper_runtime/smoke_performance.jsonl").read_text(encoding="utf-8").splitlines()
signal_lines = Path("runtime/paper_runtime/smoke_signals.jsonl").read_text(encoding="utf-8").splitlines()

if len(perf_lines) < 20:
    print("PAPER_RUNTIME_SMOKE FAIL too_few_perf_rows")
    raise SystemExit(1)

if len(signal_lines) < 20:
    print("PAPER_RUNTIME_SMOKE FAIL too_few_signal_rows")
    raise SystemExit(1)

print("PAPER_RUNTIME_SMOKE PASS")
