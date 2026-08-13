# -*- coding: utf-8 -*-
"""
ecosystem/projects/earesmes-arfin-bridge/src/adapter/bounded_adapter.py
Bounded EAB Adapter Interface - 4 Operations: EAB_GET_PENDING, EAB_LIST_PENDING, EAB_SUBMIT_BATCH_CLARIFICATION, EAB_CREATE_MANUAL_TRANSACTION.
"""

from typing import Dict, Any, List, Optional

class EABBoundedAdapter:
    def __init__(self, client):
        self.client = client

    def get_pending(self, pending_id: str, owner_chat_id: str) -> Dict[str, Any]:
        return self.client.get_pending(pending_id, owner_chat_id)

    def list_pending(self, owner_chat_id: str) -> Dict[str, Any]:
        return self.client.list_pending(owner_chat_id)

    def submit_batch_clarification(self, items: List[Dict[str, Any]], owner_chat_id: str) -> Dict[str, Any]:
        return self.client.submit_batch_clarification(items, owner_chat_id)

    def create_manual_transaction(self, amount: float, category: str, description: str, owner_chat_id: str) -> Dict[str, Any]:
        return self.client.create_manual_transaction(amount, category, description, owner_chat_id)
