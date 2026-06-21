from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


BLOCKED_ACTION_KEYWORDS = {
    "create_order",
    "market_order",
    "limit_order",
    "withdraw",
    "leverage",
    "private_api",
    "private exchange",
    "live_trade",
    "live trading",
}


@dataclass(frozen=True)
class AgentPolicy:
    mode: str = "PHASE4_RESEARCH_ONLY"
    live_trading_enabled: bool = False
    private_exchange_api_enabled: bool = False
    notion_write_mode: str = "DRY_RUN_ONLY"
    destructive_actions_enabled: bool = False
    max_parallel_agents: int = 1

    def assert_safe_action(self, action: str) -> None:
        normalized = action.lower().replace("-", "_")
        if not self.live_trading_enabled and any(k in normalized for k in BLOCKED_ACTION_KEYWORDS):
            raise PermissionError(f"Blocked by EarnsAI policy: {action}")
        if "delete" in normalized and not self.destructive_actions_enabled:
            raise PermissionError(f"Destructive action blocked: {action}")

    def summary(self) -> dict:
        return {
            "mode": self.mode,
            "live_trading_enabled": self.live_trading_enabled,
            "private_exchange_api_enabled": self.private_exchange_api_enabled,
            "notion_write_mode": self.notion_write_mode,
            "destructive_actions_enabled": self.destructive_actions_enabled,
            "max_parallel_agents": self.max_parallel_agents,
        }


def validate_actions(actions: Iterable[str], policy: AgentPolicy | None = None) -> list[str]:
    policy = policy or AgentPolicy()
    checked = []
    for action in actions:
        policy.assert_safe_action(action)
        checked.append(action)
    return checked
