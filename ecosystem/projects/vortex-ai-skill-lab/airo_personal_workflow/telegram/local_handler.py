import os
from airo_personal_workflow.db.repository import (
    check_installment,
    monthly_summary,
    record_from_text,
)
from airo_personal_workflow.intents.parser import parse_user_message
from airo_personal_workflow.reports.monthly import generate_monthly_markdown
from airo_personal_workflow.adapters.google.workspace_dry_run import generate_google_workspace_plan
# AIRO_LOCAL_HANDLER_PERSISTENCE_V06
import importlib.util as _airo_persist_importlib_util
from pathlib import Path as _AiroPersistPath

_AIRO_PERSIST_PATH = _AiroPersistPath(__file__).resolve()
for _parent in [_AIRO_PERSIST_PATH] + list(_AIRO_PERSIST_PATH.parents):
    _candidate = _parent / "scripts" / "personal-workflow" / "airo_transaction_persistence.py"
    if _candidate.exists():
        _persist_spec = _airo_persist_importlib_util.spec_from_file_location("airo_transaction_persistence", _candidate)
        _persist_mod = _airo_persist_importlib_util.module_from_spec(_persist_spec)
        assert _persist_spec is not None and _persist_spec.loader is not None
        _persist_spec.loader.exec_module(_persist_mod)
        persist_transaction = _persist_mod.persist_transaction
        break
else:
    persist_transaction = None



def handle_telegram_text(text: str) -> dict:
    parsed = parse_user_message(text)
    intent = parsed.get("intent")

    if intent in {"record_transaction", "record_installment_payment"}:
        saved = record_from_text(text)
        _primary_persist_action = saved.get("persist_action")
        if intent == "record_transaction":
            _persist_payload = dict(saved) if isinstance(saved, dict) else {}
            _persist_payload.setdefault("raw_text", text)
            _persist_payload.setdefault("source", "telegram")
            _skip_legacy_persist = (
                os.environ.get("AIRO_WORKFLOW_MODE", "").strip().lower() in {"dry-run", "dry_run", "test"}
                or bool(os.environ.get("AIRO_DB_PATH", "").strip())
                or saved.get("persist_action") == "skip_duplicate"
                or saved.get("already_recorded") is True
            )

            if _skip_legacy_persist:
                _persist_result = {
                    "ok": True,
                    "action": "skipped_best_effort",
                    "reason": "dry_run_temp_db_or_duplicate",
                }
                saved["persistence_warning"] = _persist_result
            if _primary_persist_action:
                saved["persist_action"] = _primary_persist_action
            else:
                try:
                    _persist_result = _airo_persist_record_transaction_v06(_persist_payload)
                except Exception as _persist_exc:
                    # Reply path safety: the primary record_from_text write has already
                    # succeeded. The legacy/canonical persistence hook is best-effort and
                    # must not turn a successful write into a Telegram tool error.
                    _persist_result = {
                        "ok": False,
                        "action": "best_effort_failed",
                        "error": type(_persist_exc).__name__,
                        "message": str(_persist_exc),
                    }
                    saved["persistence_warning"] = _persist_result
            if _primary_persist_action:
                saved["persist_action"] = _primary_persist_action
            if isinstance(saved, dict) and isinstance(_persist_result, dict) and _persist_result.get("ok"):
                saved = dict(saved)
                saved["account_name"] = _persist_result.get("account_name") or _persist_result.get("payment_method") or saved.get("account_name")
                saved["payment_method"] = _persist_result.get("payment_method") or saved.get("payment_method")
                saved["account_id"] = _persist_result.get("account_id") or saved.get("account_id")
                saved["transaction_id"] = _persist_result.get("transaction_id") or saved.get("transaction_id")
                saved["legacy_persist_action"] = _persist_result.get("action") or saved.get("persist_action")
        # LEGACY_PERSIST_ACTION_PRESERVE_GUARD
        if saved.get("already_recorded") is True or saved.get("action") == "skip_duplicate":
            saved["persist_action"] = "skip_duplicate"

        return {
            "ok": True,
            "intent": intent,
            "action": "recorded",
            "data": saved,
            "message": _record_message(saved),
        }

    if intent == "check_installment":
        name = parsed["installment_name"]
        result = check_installment(name)
        return {
            "ok": True,
            "intent": intent,
            "action": "checked",
            "data": result,
            "message": _installment_message(name, result),
        }

    if intent == "monthly_report":
        period = parsed["period"]
        summary = monthly_summary(period)
        report_path = generate_monthly_markdown(period)
        google_plan = generate_google_workspace_plan(period)
        return {
            "ok": True,
            "intent": intent,
            "action": "reported",
            "data": {
                "summary": summary,
                "report_path": report_path,
                "google_dry_run": google_plan,
            },
            "message": _summary_message(summary, report_path),
        }

    return {
        "ok": False,
        "intent": intent,
        "action": "needs_review",
        "data": parsed,
        "message": "Saya belum yakin maksudnya. Tolong tulis lebih jelas, misalnya: catat beli makan Rp50.000 pakai Tokopedia Credit Card.",
    }


def _rupiah(value) -> str:
    value = int(value or 0)
    return "Rp" + f"{value:,}".replace(",", ".")


def _record_message(saved: dict) -> str:
    if saved["intent"] == "record_installment_payment":
        return (
            f"Tercatat pembayaran {saved['installment_name']} "
            f"ke-{saved.get('installment_number')} sebesar {_rupiah(saved['amount'])}."
        )

    return (
        f"Tercatat transaksi {saved.get('category')} sebesar "
        f"{_rupiah(saved['amount'])} via {saved.get('account_name') or 'akun belum ditentukan'}."
    )


def _installment_message(name: str, result: dict) -> str:
    if not result.get("found"):
        return f"{name} belum ada di database."

    inst = result["installment"]
    paid = inst.get("paid_installments") or 0
    total = inst.get("total_installments") or "?"
    return f"{name} tercatat sudah bayar ke-{paid} dari {total}."


def _summary_message(summary: dict, report_path: str) -> str:
    trx = summary["transactions"]
    inst = summary["installment_payments"]
    return (
        f"Ringkasan {summary['period']}: transaksi {_rupiah(trx.get('total'))} "
        f"({trx.get('count')} item), cicilan {_rupiah(inst.get('total'))} "
        f"({inst.get('count')} pembayaran). Report lokal: {report_path}"
    )

def _airo_persist_record_transaction_v06(payload):
    """Persist Telegram record_transaction payload into canonical SQLite if helper is available."""
    if persist_transaction is None:
        return {
            "ok": False,
            "reason": "persist_helper_unavailable",
        }

    if not isinstance(payload, dict):
        payload = {
            "raw_text": str(payload),
        }

    return persist_transaction(payload)
