#!/usr/bin/env python3
import json
import sys

raw = sys.stdin.read()
try:
    data = json.loads(raw)
except Exception:
    print(raw, end="")
    raise SystemExit(0)

payload = data.get("data") or {}
if data.get("ok") is True and payload.get("persist_action") == "skip_duplicate":
    amount = payload.get("amount")
    category = payload.get("category") or "transaksi"
    method = payload.get("payment_method") or payload.get("account_name") or "akun terkait"

    if isinstance(amount, int):
        rupiah = f"Rp{amount:,}".replace(",", ".")
    else:
        rupiah = f"Rp{amount}" if amount else "nominal tersebut"

    data["action"] = "already_recorded"
    data["message"] = f"Sudah pernah tercatat: transaksi {category} sebesar {rupiah} via {method}. Tidak ditulis ulang."

print(json.dumps(data, ensure_ascii=False))
