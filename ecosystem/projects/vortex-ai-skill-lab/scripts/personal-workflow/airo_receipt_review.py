#!/usr/bin/env python3
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

RECEIPT_INTAKE = Path("scripts/personal-workflow/airo_receipt_intake.py")
ACTION_GATE = Path("scripts/personal-workflow/airo_action_gate.py")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def run_json(cmd):
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)

def main():
    p = argparse.ArgumentParser(description="Airo receipt-to-transaction review bridge")
    p.add_argument("receipt_file")
    p.add_argument("--mode", choices=["dry-run", "queue"], default="dry-run")
    p.add_argument("--source", default="airo-receipt-review")
    p.add_argument("--merchant", default="")
    p.add_argument("--description", required=True)
    p.add_argument("--amount", required=True)
    p.add_argument("--payment-method", default="")
    p.add_argument("--category", default="")
    p.add_argument("--transaction-date", default="")
    p.add_argument("--note", default="")
    p.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    args = p.parse_args()

    if not RECEIPT_INTAKE.exists():
        emit({"ok": False, "error": "receipt intake script missing"}, 2)
    if not ACTION_GATE.exists():
        emit({"ok": False, "error": "action gate script missing"}, 2)

    receipt_mode = "store" if args.mode == "queue" else "dry-run"
    intake = run_json([
        sys.executable,
        str(RECEIPT_INTAKE),
        "--mode", receipt_mode,
        "--source", args.source,
        "--note", args.note,
        args.receipt_file
    ])

    review_payload = {
        "operation": "receipt_to_transaction_review",
        "receipt": {
            "sha256": intake.get("sha256"),
            "kind": intake.get("kind"),
            "mime": intake.get("mime"),
            "size_bytes": intake.get("size_bytes"),
            "stored": intake.get("stored", False),
            "stored_path": intake.get("stored_path", ""),
            "manifest": intake.get("manifest", "")
        },
        "proposed_transaction": {
            "merchant": args.merchant,
            "description": args.description,
            "amount": args.amount,
            "payment_method": args.payment_method,
            "category": args.category,
            "transaction_date": args.transaction_date,
            "source": args.source,
            "note": args.note
        },
        "execution_policy": "review_only_no_transaction_write",
        "approval_required": True
    }

    if args.mode == "dry-run":
        emit({
            "ok": True,
            "mode": "dry-run",
            "decision": "review_payload_preview",
            "receipt_intake": intake,
            "review_payload": review_payload,
            "transaction_written": False
        })

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(review_payload, f, indent=2, ensure_ascii=False)
        payload_path = f.name

    try:
        gate = run_json([
            sys.executable,
            str(ACTION_GATE),
            "--action-type", "receipt_to_transaction",
            "--title", "Review receipt transaction proposal",
            "--payload", payload_path,
            "--source", args.source,
            "--risk-level", args.risk_level
        ])
    finally:
        try:
            Path(payload_path).unlink()
        except Exception:
            pass

    emit({
        "ok": True,
        "mode": "queue",
        "decision": "queued_for_review",
        "receipt_intake": intake,
        "action_gate": gate,
        "transaction_written": False
    })

if __name__ == "__main__":
    main()
