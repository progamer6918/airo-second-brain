#!/usr/bin/env python3


# AIRO_V13_FINANCE_FORCE_ROUTER_PATCH
def _airo_v13_finance_force_router():
    import json
    import importlib.util
    import pathlib
    import sys

    message = " ".join(sys.argv[1:]).strip()
    if not message:
        return False

    text = message.lower()
    signals = [
        "bayar", "beli", "jajan", "makan", "cash", "tunai",
        "hutang", "utang", "cicilan", "kpr", "angsuran",
        "nabung", "tabungan", "tf", "transfer", "topup",
        "tokopedia cc", "tokopedia credit card", "blu", "bca", "emas",
    ]

    if not any(signal in text for signal in signals):
        return False

    repo = pathlib.Path(__file__).resolve().parents[2]
    mapper_path = repo / "scripts/personal-workflow/airo_finance_sheet_v12_mapper_preview.py"
    spec = importlib.util.spec_from_file_location("airo_finance_sheet_v12_mapper_preview", mapper_path)
    if spec is None or spec.loader is None:
        print(json.dumps({
            "intent": "finance_capture",
            "status": "error",
            "error": "mapper_not_loadable",
            "message": message,
        }, ensure_ascii=False))
        sys.exit(2)

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    confidence = 0.30 if any(word in text for word in ["kayaknya", "mungkin", "sesuatu", "gimana"]) else 0.95
    payload = module.mapper_preview(message, confidence=confidence, source="telegram")

    out = {
        "intent": "finance_capture",
        "status": "routed",
        "route": "airo_finance_v13",
        "message": message,
        "target_tab": payload.get("target_tab"),
        "target_tabs": payload.get("target_tabs"),
        "route_to_review": payload.get("route_to_review"),
        "mapper_operation": payload.get("mapper_operation"),
        "planner": payload.get("planner"),
        "planner_operation": payload.get("planner_operation"),
        "duplicate_key": payload.get("duplicate_key"),
        "next_action": payload.get("next_action"),
        "safe_reply": (
            "Masuk jalur AIRO Finance Review Queue."
            if payload.get("target_tab") == "🧾 Review Queue"
            else "Masuk jalur AIRO Finance."
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
    sys.exit(0)


_airo_v13_finance_force_router()

import argparse, json, shlex

def emit(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def has_any(text, words):
    return any(w in text for w in words)

def route(message):
    raw = message.strip()
    text = raw.lower()
    quoted = shlex.quote(raw)

    base = {
        "input": raw,
        "execution_performed": False,
        "router_mode": "preview_only",
        "safety_boundary_active": True
    }

    if has_any(text, ["live trading", "aktifkan live trading", "real trading", "earnsai runtime", "baca token", "baca secret", "baca cookie", "baca session", "baca .env", "browser profile"]):
        return {
            **base,
            "ok": False,
            "decision": "blocked",
            "intent": "blocked_safety_boundary",
            "confidence": "high",
            "risk": "blocked",
            "approval_required": False,
            "reason": "Request matches a blocked safety boundary.",
            "recommended_next_step": "Do not execute.",
            "exact_safe_command": None,
            "blocked_reason": "Outside approved Airo Personal Workflow scope."
        }

    if has_any(text, ["daily", "harian", "status hari ini", "cek status", "next action", "apa yang harus"]):
        return {
            **base,
            "ok": True,
            "decision": "route",
            "intent": "daily_status",
            "confidence": "high",
            "risk": "low",
            "approval_required": False,
            "reason": "Message asks for daily status or next action.",
            "recommended_next_step": "Run unified daily command.",
            "exact_safe_command": "./bin/airo-daily --text",
            "json_command": "./bin/airo-daily"
        }

    if has_any(text, ["approval", "queue pending", "pending approval", "lihat queue"]):
        return {
            **base,
            "ok": True,
            "decision": "route",
            "intent": "approval_queue_view",
            "confidence": "high",
            "risk": "low",
            "approval_required": False,
            "reason": "Message asks to inspect approval queue.",
            "recommended_next_step": "List pending approvals.",
            "exact_safe_command": "python3 scripts/personal-workflow/airo_approval_review.py list --status pending --limit 10"
        }

    if has_any(text, ["dashboard", "daily ops", "operasi harian"]):
        return {
            **base,
            "ok": True,
            "decision": "route",
            "intent": "dashboard",
            "confidence": "high",
            "risk": "low",
            "approval_required": False,
            "reason": "Message asks for dashboard.",
            "recommended_next_step": "Refresh daily ops dashboard.",
            "exact_safe_command": "python3 scripts/personal-workflow/airo_ops_dashboard.py"
        }

    if has_any(text, ["google sheets", "sheet", "sync google", "upload ke google", "kirim ke sheet"]):
        return {
            **base,
            "ok": True,
            "decision": "queue_required",
            "intent": "google_sheets_write",
            "confidence": "high",
            "risk": "medium",
            "approval_required": True,
            "reason": "Google Sheets write/sync is sensitive and must be queued.",
            "recommended_next_step": "Queue through action gate after payload is ready.",
            "exact_safe_command": "python3 scripts/personal-workflow/airo_action_gate.py --action-type google_sheets_write --title \"Google Sheets write request\" --source airo-intent-router --risk-level medium --dry-run"
        }

    if has_any(text, ["receipt", "struk", "nota", "kwitansi"]):
        return {
            **base,
            "ok": True,
            "decision": "route",
            "intent": "receipt_review_or_transaction_proposal",
            "confidence": "high",
            "risk": "medium",
            "approval_required": True,
            "reason": "Message refers to receipt review.",
            "recommended_next_step": "Run transaction proposal dry-run.",
            "exact_safe_command": "python3 scripts/personal-workflow/airo_transaction_proposal.py receipt.pdf --mode dry-run --description \"...\" --amount \"...\""
        }

    if has_any(text, ["catat", "beli", "bayar", "pengeluaran", "transaksi", "cicilan", "ringkasan", "makan", "pakai"]):
        return {
            **base,
            "ok": True,
            "decision": "route",
            "intent": "personal_finance_capture_or_summary",
            "confidence": "medium",
            "risk": "low",
            "approval_required": False,
            "reason": "Message looks like normal personal finance capture or summary.",
            "recommended_next_step": "Run airo-workflow dry-run first.",
            "exact_safe_command": "AIRO_WORKFLOW_MODE=dry-run airo-workflow " + quoted,
            "real_command_requires_user_intent": "airo-workflow " + quoted
        }

    return {
        **base,
        "ok": True,
        "decision": "needs_review",
        "intent": "unknown",
        "confidence": "low",
        "risk": "unknown",
        "approval_required": None,
        "reason": "Router could not classify confidently.",
        "recommended_next_step": "Run daily status or inspect pending approvals.",
        "exact_safe_command": "./bin/airo-daily --text"
    }

def main():
    p = argparse.ArgumentParser(description="Airo local intent router with preview fields")
    p.add_argument("message", nargs="+")
    p.add_argument("--compact", action="store_true")
    args = p.parse_args()
    result = {"ok": True, "operation": "local_intent_router", "version": "phase7c", "result": route(" ".join(args.message))}
    print(json.dumps(result, ensure_ascii=False) if args.compact else json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
