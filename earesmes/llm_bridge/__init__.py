"""
EARESMES Controlled LLM Bridge Layer — V1
==========================================
Controlled bridge layer for passing validated execution packages to LLM providers.

Governance limits enforced:
  - No autonomous loop
  - No background daemon
  - No runner modification
  - Policy & approval checks must be validated BEFORE calling bridge
"""

from earesmes.llm_bridge.bridge import LLMBridge
from earesmes.llm_bridge.providers.hermes import HermesProviderAdapter
from earesmes.llm_bridge.receipts import BridgeReceiptBuilder

__all__ = ["LLMBridge", "HermesProviderAdapter", "BridgeReceiptBuilder"]
