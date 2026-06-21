#!/usr/bin/env python3
import argparse, datetime, json, subprocess, sys, tempfile
from pathlib import Path

RECEIPT_REVIEW = Path("scripts/personal-workflow/airo_receipt_review.py")
ACTION_GATE = Path("scripts/personal-workflow/airo_action_gate.py")

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def run_json(cmd):
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)

def main():
    p = argparse.ArgumentParser(description="Airo transaction proposal builder from receipt review")
    p.add_argument("receipt_file")
    p.add_argument("--mode", choices=["dry-run", "queue"], default="dry-run")
    p.add_argument("--source", default="airo-transaction-proposal")
    p.add_argument("--merchant", default="")
    p.add_argument("--description", required=True)
    p.add_argument("--amount", required=True)
    p.add_argument("--payment-method", default="")
    p.add_argument("--category", default="")
    p.add_argument("--transaction-date", default="")
    p.add_argument("--note", default="")
    p.add_argument("--risk-level", choices=["low", "medium", "high"], default="medium")
    args = p.parse_args()

    if not RECEIPT_REVIEW.exists():
        emit({"ok": False, "error": "receipt review script missing"}, 2)
    if not ACTION_GATE.exists():
        emit({"ok": False, "error": "action gate script missing"}, 2)

    review = run_json([
        sys.executable,
        str(RECEIPT_REVIEW),
        args.receipt_file,
        "--mode", "dry-run",
        "--source", args.source,
        "--merchant", args.merchant,
        "--description", args.description,
        "--amount", args.amount,
        "--payment-method", args.payment_method,
        "--category", args.category,
        "--transaction-date", args.transaction_date,
        "--note", args.note
    ])

    review_payload = review.get("review_payload", {})
    receipt = review_payload.get("receipt", {})
    proposed = review_payload.get("proposed_transaction", {})

    proposal = {
        "operation": "approved_transaction_proposal",
        "created_at": now(),
        "source": args.source,
        "receipt": receipt,
        "transaction_proposal": {
            "type": "personal_expense",
            "merchant": proposed.get("merchant") or args.merchant,
            "description": proposed.get("description") or args.description,
            "amount": proposed.get("amount") or args.amount,
            "payment_method": proposed.get("payment_method") or args.payment_method,
            "category": proposed.get("category") or args.category,
            "transaction_date": proposed.get("transaction_date") or args.transaction_date,
            "note": proposed.get("note") or args.note,
            "receipt_sha256": receipt.get("sha256"),
            "status": "proposal_only_not_written"
        },
        "execution_policy": "approval_required_before_sqlite_write",
        "approval_required": True,
        "transaction_written": False,
        "sqlite_mutated": False
    }

    if args.mode == "dry-run":
        emit({
            "ok": True,
            "mode": "dry-run",
            "decision": "transaction_proposal_preview",
            "proposal": proposal,
            "transaction_written": False,
            "sqlite_mutated": False
        })

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(proposal, f, indent=2, ensure_ascii=False)
        payload_path = f.name

    try:
        gate = run_json([
            sys.executable,
            str(ACTION_GATE),
            "--action-type", "sqlite_mutation",
            "--title", "Approve transaction proposal from receipt review",
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
        "decision": "transaction_proposal_queued_for_approval",
        "proposal": proposal,
        "action_gate": gate,
        "transaction_written": False,
        "sqlite_mutated": False
    })

if __name__ == "__main__":
    main()
