#!/usr/bin/env python3
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path("scripts/personal-workflow")

TOOLS = {
    "preflight": ROOT / "airo_google_credential_preflight.py",
    "sheets": ROOT / "airo_google_sheets_writer.py",
    "queue": ROOT / "airo_approval_queue.py",
    "gate": ROOT / "airo_action_gate.py",
    "receipt_intake": ROOT / "airo_receipt_intake.py",
    "receipt_review": ROOT / "airo_receipt_review.py",
    "dashboard": ROOT / "airo_local_dashboard.py",
}

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def run_json(cmd):
    out = subprocess.check_output(cmd, text=True)
    try:
        return json.loads(out)
    except Exception:
        emit({"ok": False, "error": "wrapped command did not return JSON", "command": cmd, "raw": out}, 2)

def tool(name):
    p = TOOLS[name]
    if not p.exists():
        emit({"ok": False, "error": f"tool missing: {p}"}, 2)
    return str(p)

def main():
    parser = argparse.ArgumentParser(description="Unified local command wrapper for Airo Personal Workflow")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("preflight")

    sh = sub.add_parser("sheets-dry-run")
    sh.add_argument("--spreadsheet-id", default="")
    sh.add_argument("--range", default="Airo!A:D")
    sh.add_argument("--payload", default="")

    q = sub.add_parser("queue")
    q.add_argument("--status", choices=["pending", "approved", "rejected", "executed", "all"], default="pending")
    q.add_argument("--limit", default="20")

    g = sub.add_parser("gate")
    g.add_argument("--action-type", required=True)
    g.add_argument("--title", required=True)
    g.add_argument("--payload", default="")
    g.add_argument("--source", default="airoctl")
    g.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    g.add_argument("--dry-run", action="store_true")

    ri = sub.add_parser("receipt-intake")
    ri.add_argument("file")
    ri.add_argument("--mode", choices=["dry-run", "store"], default="dry-run")
    ri.add_argument("--source", default="airoctl")
    ri.add_argument("--note", default="")

    rr = sub.add_parser("receipt-review")
    rr.add_argument("file")
    rr.add_argument("--mode", choices=["dry-run", "queue"], default="dry-run")
    rr.add_argument("--description", required=True)
    rr.add_argument("--amount", required=True)
    rr.add_argument("--merchant", default="")
    rr.add_argument("--payment-method", default="")
    rr.add_argument("--category", default="")
    rr.add_argument("--transaction-date", default="")
    rr.add_argument("--note", default="")
    rr.add_argument("--source", default="airoctl")

    d = sub.add_parser("dashboard")
    d.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.cmd == "preflight":
        emit({"ok": True, "wrapper": "airoctl", "command": "preflight", "result": run_json([sys.executable, tool("preflight")])})

    if args.cmd == "sheets-dry-run":
        cmd = [sys.executable, tool("sheets"), "--mode", "dry-run", "--auth-method", "oauth", "--range", args.range]
        if args.spreadsheet_id:
            cmd += ["--spreadsheet-id", args.spreadsheet_id]
        if args.payload:
            cmd += ["--payload", args.payload]
        emit({"ok": True, "wrapper": "airoctl", "command": "sheets-dry-run", "result": run_json(cmd)})

    if args.cmd == "queue":
        emit({"ok": True, "wrapper": "airoctl", "command": "queue", "result": run_json([sys.executable, tool("queue"), "list", "--status", args.status, "--limit", str(args.limit)])})

    if args.cmd == "gate":
        cmd = [sys.executable, tool("gate"), "--action-type", args.action_type, "--title", args.title, "--source", args.source, "--risk-level", args.risk_level]
        if args.payload:
            cmd += ["--payload", args.payload]
        if args.dry_run:
            cmd += ["--dry-run"]
        emit({"ok": True, "wrapper": "airoctl", "command": "gate", "result": run_json(cmd)})

    if args.cmd == "receipt-intake":
        cmd = [sys.executable, tool("receipt_intake"), "--mode", args.mode, "--source", args.source, "--note", args.note, args.file]
        emit({"ok": True, "wrapper": "airoctl", "command": "receipt-intake", "result": run_json(cmd)})

    if args.cmd == "receipt-review":
        cmd = [
            sys.executable, tool("receipt_review"), args.file,
            "--mode", args.mode,
            "--description", args.description,
            "--amount", args.amount,
            "--merchant", args.merchant,
            "--payment-method", args.payment_method,
            "--category", args.category,
            "--transaction-date", args.transaction_date,
            "--note", args.note,
            "--source", args.source,
        ]
        emit({"ok": True, "wrapper": "airoctl", "command": "receipt-review", "result": run_json(cmd)})

    if args.cmd == "dashboard":
        cmd = [sys.executable, tool("dashboard")]
        if args.json:
            cmd += ["--json"]
        emit({"ok": True, "wrapper": "airoctl", "command": "dashboard", "result": run_json(cmd)})

if __name__ == "__main__":
    main()
