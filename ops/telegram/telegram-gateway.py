#!/usr/bin/env python3
"""
Earesmes Telegram Gateway Integration Script (CU-03)
Provides interface functions to route Telegram updates through GatewayBridge.
Zero background autostart, zero import-time network calls.
"""

import sys
import os
import json
import time
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ecosystem/projects/earesmes-arfin-bridge")))

from src.adapter.auth_guard import SecurityGuard
from src.adapter.bounded_adapter import BoundedArfinAdapter
from src.bridge.gateway_bridge import GatewayBridge

class TelegramGatewayRunner:
    """
    Runner for Telegram gateway updates in offline or fake-gateway mode.
    """
    def __init__(
        self,
        security_guard: SecurityGuard,
        bounded_adapter: BoundedArfinAdapter,
        bridge: Optional[GatewayBridge] = None
    ):
        self.security_guard = security_guard
        self.bounded_adapter = bounded_adapter
        self.bridge = bridge if bridge is not None else GatewayBridge(security_guard, bounded_adapter)

    def handle_raw_update(self, update_json: str, current_time: Optional[float] = None) -> str:
        """
        Parse raw JSON update and route through GatewayBridge.
        Returns JSON string result with redacted audit evidence.
        """
        try:
            update_dict = json.loads(update_json)
        except Exception as e:
            return json.dumps({
                "status": "REJECTED",
                "error_code": "INVALID_JSON",
                "message": f"Malformed update JSON: {str(e)}",
                "queue_message_effect": "REJECTED"
            })

        res = self.bridge.process_telegram_update(update_dict, current_time=current_time)
        return json.dumps(res)

if __name__ == "__main__":
    print("Telegram Gateway integration runner loaded (offline/fake mode).")
