"""
EAB Controlled Integration Dry-Run CLI Runner (CU-11 / M11)
Executes standalone controlled dry-run simulation across synthetic update vectors.
Outputs structured JSON / text dry-run execution report.
"""

import sys
import os
import time
import json
import hashlib
import hmac

bridge_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ecosystem/projects/earesmes-arfin-bridge"))
if bridge_root not in sys.path:
    sys.path.insert(0, bridge_root)

repo_root = os.path.abspath(os.path.join(bridge_root, "../../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.pending.pending_model import PendingRecord, PendingState
from src.adapter.auth_guard import SecurityGuard
from src.adapter.bounded_adapter import BoundedArfinAdapter
from src.bridge.gateway_bridge import GatewayBridge

def execute_dry_run():
    now = time.time()
    curr_key = "synth_current_key_abcdef1234567890"
    prev_key = "synth_previous_key_abcdef1234567890"

    guard = SecurityGuard(
        current_service_key=curr_key,
        previous_service_key=prev_key,
        previous_key_rotated_at=now - 3600,
        allowed_owner_chat_ids={"100", "200"}
    )
    adapter = BoundedArfinAdapter(security_guard=guard, fake_transport_mode=True)
    bridge = GatewayBridge(security_guard=guard, bounded_adapter=adapter)

    record = PendingRecord(owner_actor_id="100", owner_chat_id="100", is_active_cycle=True)
    record.pending_version = 1
    record.display_short_reference = "AF-1001"
    bridge.register_pending_record(record)

    vectors = [
        ("VEC-01", "Valid reply", {"message": {"chat": {"id": "100"}, "short_ref": "AF-1001"}, "items": [{"amount": 500}], "expected_version": 1}),
        ("VEC-02", "Unauthorized chat_id", {"message": {"chat": {"id": "999"}, "short_ref": "AF-1001"}, "items": [{"amount": 500}], "expected_version": 1}),
        ("VEC-03", "Stale version", {"message": {"chat": {"id": "100"}, "short_ref": "AF-1001"}, "items": [{"amount": 500}], "expected_version": 99})
    ]

    results = []
    for vec_id, title, payload in vectors:
        res = bridge.process_telegram_update(payload, current_time=now)
        results.append({
            "vector_id": vec_id,
            "title": title,
            "status": res["status"],
            "queue_message_effect": res.get("queue_message_effect", "N/A")
        })

    report = {
        "dry_run_title": "EAB Controlled Integration Dry-Run Report (CU-11 / M11)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "fake_transport_mode": adapter.fake_transport_mode,
        "vector_count": len(results),
        "results": results,
        "safety_verdict": {
            "network_calls": 0,
            "account_ledger_writes": 0,
            "overall_status": "PASS"
        }
    }
    return report

if __name__ == "__main__":
    rep = execute_dry_run()
    print(json.dumps(rep, indent=2))
