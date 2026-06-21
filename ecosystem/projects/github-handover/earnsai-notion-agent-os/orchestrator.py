from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agent_os.guards.policy import AgentPolicy
from agent_os.memory.jsonl_store import JsonlMemoryStore
from agent_os.notion.dry_run_adapter import NotionDryRunAdapter


@dataclass
class AgentResult:
    agent: str
    status: str
    output: dict[str, Any]


class EarnsAIOrchestrator:
    """
    Sequential orchestrator scaffold.

    Phase 4 rule:
    - research only
    - sequential agents
    - no live trading
    - no private exchange API
    - Notion dry-run only
    """

    def __init__(self) -> None:
        self.policy = AgentPolicy()
        self.memory = JsonlMemoryStore()
        self.notion = NotionDryRunAdapter()

    def run_demo(self) -> list[AgentResult]:
        self.policy.assert_safe_action("research_strategy_review")

        results = [
            AgentResult(
                agent="ResearchAgent",
                status="PASS",
                output={
                    "task": "Inspect latest research artifacts",
                    "mode": "dry_run",
                },
            ),
            AgentResult(
                agent="RiskGuardianAgent",
                status="PASS",
                output={
                    "live_trading": "DISABLED",
                    "private_exchange_api": "DISABLED",
                    "policy": self.policy.summary(),
                },
            ),
            AgentResult(
                agent="ReportAgent",
                status="PASS",
                output={
                    "report_type": "agent_os_smoke",
                    "next_step": "Prepare Notion adapter with guarded official API mode",
                },
            ),
        ]

        notion_payload = {
            "title": "EarnsAI Agent OS Smoke Test",
            "phase": "Phase 4 — Trading Research Lab",
            "status": "dry_run_success",
            "agents": ", ".join(r.agent for r in results),
        }

        notion_result = self.notion.write_research_log(notion_payload)

        results.append(
            AgentResult(
                agent="NotionLibrarianAgent",
                status="PASS",
                output={
                    "dry_run_files": notion_result,
                    "real_notion_api_called": False,
                },
            )
        )

        self.memory.append(
            "agent_os_smoke",
            {
                "status": "PASS",
                "agents": [r.agent for r in results],
                "notion_dry_run": notion_result,
            },
        )

        return results
