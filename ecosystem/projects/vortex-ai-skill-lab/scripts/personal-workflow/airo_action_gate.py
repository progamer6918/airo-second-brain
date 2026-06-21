#!/usr/bin/env python3
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

QUEUE = Path("scripts/personal-workflow/airo_approval_queue.py")
DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

SENSITIVE_ACTIONS = {
    "google_sheets_write",
    "sqlite_mutation",
    "receipt_to_transaction",
    "openclaw_instruction_patch",
    "service_restart",
    "finance_delete"
}

BLOCKED_ACTIONS = {
    "earnsai_runtime_access",
    "live_trading",
    "browser_profile_access",
    "secret_read",
    "cookie_read",
    "session_read"
}

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def load_payload(path):
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    p = argparse.ArgumentParser(description="Airo sensitive action approval gate")
    p.add_argument("--action-type", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--payload", default="")
    p.add_argument("--source", default="airo")
    p.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    action = args.action_type.strip()
    payload = load_payload(args.payload)

    if action in BLOCKED_ACTIONS:
        emit({
            "ok": False,
            "decision": "blocked",
            "action_type": action,
            "reason": "action is outside Airo Personal Workflow safety boundary"
        }, 2)

    if action not in SENSITIVE_ACTIONS:
        emit({
            "ok": True,
            "decision": "allowed_no_queue_required",
            "action_type": action,
            "payload_preview": payload
        })

    queue_payload = {
        "action_type": action,
        "title": args.title,
        "source": args.source,
        "risk_level": args.risk_level,
        "payload": payload,
        "execution_policy": "queue_only_no_execute"
    }

    if args.dry_run:
        emit({
            "ok": True,
            "decision": "queue_required_dry_run",
            "action_type": action,
            "queue_payload": queue_payload
        })

    if not QUEUE.exists():
        emit({"ok": False, "error": "approval queue script not found"}, 2)

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(queue_payload, f, indent=2, ensure_ascii=False)
        tmp_payload = f.name

    try:
        cmd = [
            sys.executable,
            str(QUEUE),
            "--root", str(Path(args.root).expanduser()),
            "add",
            "--source", args.source,
            "--action-type", action,
            "--title", args.title,
            "--payload", tmp_payload,
            "--risk-level", args.risk_level,
        ]
        out = subprocess.check_output(cmd, text=True)
        queued = json.loads(out)
    finally:
        try:
            os.unlink(tmp_payload)
        except Exception:
            pass

    emit({
        "ok": True,
        "decision": "queued_for_approval",
        "action_type": action,
        "queue_item": queued,
        "execution_performed": False
    })

if __name__ == "__main__":
    main()
