#!/usr/bin/env python3
import argparse, datetime, json, os, sqlite3, subprocess
from pathlib import Path

import importlib.util as _airo_alias_importlib_util
from pathlib import Path as _AiroAliasPath

_AIRO_ACCOUNT_ALIASES_PATH = _AiroAliasPath(__file__).resolve()
for _parent in [_AIRO_ACCOUNT_ALIASES_PATH] + list(_AIRO_ACCOUNT_ALIASES_PATH.parents):
    _candidate = _parent / "scripts" / "personal-workflow" / "airo_account_aliases.py"
    if _candidate.exists():
        _spec = _airo_alias_importlib_util.spec_from_file_location("airo_account_aliases", _candidate)
        _airo_alias_mod = _airo_alias_importlib_util.module_from_spec(_spec)
        assert _spec is not None and _spec.loader is not None
        _spec.loader.exec_module(_airo_alias_mod)
        extract_account_from_text = _airo_alias_mod.extract_account_from_text
        normalize_account_alias = _airo_alias_mod.normalize_account_alias
        break
else:
    extract_account_from_text = None
    normalize_account_alias = None

DEFAULT_ROOT = Path.home() / ".local/share/airo-personal-workflow"

def now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def emit(obj, code=0):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    raise SystemExit(code)

def db_path(root):
    return Path(root).expanduser().resolve() / "approval_queue.sqlite"

def audit_path(root):
    p = Path(root).expanduser().resolve() / "audits" / "transaction_executor_audit.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def audit(root, record):
    p = audit_path(root)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(p)

def load_item(root, item_id):
    db = db_path(root)
    if not db.exists():
        emit({"ok": False, "error": "approval queue db not found", "db": str(db)}, 2)
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    row = con.execute("select * from approval_queue where id=?", (item_id,)).fetchone()
    con.close()
    if not row:
        emit({"ok": False, "error": "queue item not found", "id": item_id}, 2)
    d = dict(row)
    try:
        d["payload"] = json.loads(d.pop("payload_json") or "{}")
    except Exception:
        d["payload"] = {}
    return d

def update_executed(root, item_id, note):
    con = sqlite3.connect(str(db_path(root)))
    con.execute("update approval_queue set status=?, approval_note=?, updated_at=? where id=?", ("executed", note, now(), item_id))
    con.commit()
    con.close()

def unwrap_payload(payload):
    if isinstance(payload, dict) and isinstance(payload.get("payload"), dict):
        return payload["payload"]
    return payload if isinstance(payload, dict) else {}

def extract_proposal(item):
    payload = unwrap_payload(item.get("payload", {}))
    if isinstance(payload.get("transaction_proposal"), dict):
        return payload["transaction_proposal"], payload
    if isinstance(payload.get("proposal"), dict):
        proposal = payload["proposal"]
        if isinstance(proposal.get("transaction_proposal"), dict):
            return proposal["transaction_proposal"], proposal
    if isinstance(payload.get("payload"), dict):
        nested = payload["payload"]
        if isinstance(nested.get("transaction_proposal"), dict):
            return nested["transaction_proposal"], nested
    return {}, payload

def build_airo_message(proposal):
    description = str(proposal.get("description") or proposal.get("merchant") or "").strip()
    amount = str(proposal.get("amount") or "").strip()
    payment = str(proposal.get("payment_method") or "").strip()
    merchant = str(proposal.get("merchant") or "").strip()
    category = str(proposal.get("category") or "").strip()

    if not description:
        emit({"ok": False, "error": "transaction proposal missing description"}, 2)
    if not amount:
        emit({"ok": False, "error": "transaction proposal missing amount"}, 2)

    msg = f"catat {description} {amount}"
    if merchant and merchant.lower() not in description.lower():
        msg += f" di {merchant}"
    if payment:
        msg += f" pakai {payment}"
    if category:
        msg += f" kategori {category}"
    return msg

def run_airo(message, real):
    env = os.environ.copy()
    if not real:
        env["AIRO_WORKFLOW_MODE"] = "dry-run"
    out = subprocess.check_output(["airo-workflow", message], text=True, env=env)
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out}

def main():
    p = argparse.ArgumentParser(description="Airo approved transaction write executor")
    p.add_argument("--root", default=str(DEFAULT_ROOT))
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--mode", choices=["dry-run", "execute"], default="dry-run")
    p.add_argument("--approve-execute", default="NO")
    args = p.parse_args()

    item = load_item(args.root, args.id)
    status = item.get("status", "")
    action_type = item.get("action_type", "")

    base = {
        "ok": True,
        "operation": "transaction_executor",
        "id": args.id,
        "mode": args.mode,
        "status": status,
        "action_type": action_type,
        "transaction_written": False,
        "sqlite_mutated_by_executor": False
    }

    if action_type != "sqlite_mutation":
        record = {**base, "ok": False, "decision": "unsupported_action_type"}
        record["audit_file"] = audit(args.root, record)
        emit(record, 2)

    if status != "approved":
        record = {**base, "ok": False, "decision": "not_executable_until_approved"}
        record["audit_file"] = audit(args.root, record)
        emit(record, 2)

    proposal, raw_payload = extract_proposal(item)
    if not proposal:
        record = {**base, "ok": False, "decision": "missing_transaction_proposal"}
        record["audit_file"] = audit(args.root, record)
        emit(record, 2)

    message = build_airo_message(proposal)

    if args.mode == "dry-run":
        airo_result = run_airo(message, real=False)
        record = {
            **base,
            "decision": "dry_run_ready_no_execution",
            "airo_message": message,
            "proposal": proposal,
            "airo_result": airo_result
        }
        record["audit_file"] = audit(args.root, record)
        emit(record)

    if args.approve_execute != "YES":
        record = {**base, "ok": False, "decision": "execute_blocked_missing_approval_flag", "airo_message": message, "proposal": proposal}
        record["audit_file"] = audit(args.root, record)
        emit(record, 2)

    airo_result = run_airo(message, real=True)
    update_executed(args.root, args.id, "Executed transaction write by airo_transaction_executor.py at " + now())

    record = {
        **base,
        "decision": "executed",
        "transaction_written": True,
        "sqlite_mutated_by_executor": True,
        "airo_message": message,
        "proposal": proposal,
        "airo_result": airo_result
    }
    record["audit_file"] = audit(args.root, record)
    emit(record)

if __name__ == "__main__":
    main()

def _airo_resolve_account_alias_v01(raw_text=None, current_account=None, current_payment_method=None):
    """Resolve user account aliases such as blu/blubca into canonical account names."""
    for value in (current_account, current_payment_method):
        if value and normalize_account_alias is not None:
            resolved = normalize_account_alias(value)
            if resolved:
                return resolved

    if raw_text and extract_account_from_text is not None:
        resolved = extract_account_from_text(raw_text)
        if resolved:
            return resolved

    return current_account or current_payment_method
