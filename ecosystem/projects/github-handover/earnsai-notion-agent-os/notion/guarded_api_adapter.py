from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NotionGuardConfig:
    mode: str = "DRY_RUN_ONLY"
    allowed_workspace_name: str = "EarnsAI"
    allow_delete: bool = False
    allow_bulk_update: bool = False
    require_root_page_allowlist: bool = True

    def assert_write_allowed(self, operation: str) -> None:
        op = operation.lower()
        if self.mode != "GUARDED_WRITE":
            raise PermissionError("Notion real write blocked: adapter is not in GUARDED_WRITE mode.")
        if "delete" in op and not self.allow_delete:
            raise PermissionError("Notion delete blocked by guard config.")
        if "bulk" in op and not self.allow_bulk_update:
            raise PermissionError("Notion bulk update blocked by guard config.")


class GuardedNotionAdapter:
    """
    Official Notion API adapter scaffold.

    This file intentionally does not import notion-client yet and does not perform real API calls.
    It only validates the future guard boundary and environment variable presence without printing secrets.
    """

    required_env_keys = ("NOTION_TOKEN", "NOTION_ROOT_PAGE_ID")

    def __init__(self, config: NotionGuardConfig | None = None) -> None:
        self.config = config or NotionGuardConfig()

    def env_status(self) -> dict[str, Any]:
        present = []
        missing = []
        for key in self.required_env_keys:
            if os.getenv(key):
                present.append(key)
            else:
                missing.append(key)
        return {
            "present_keys": present,
            "missing_keys": missing,
            "values_printed": False,
        }

    def build_research_log_plan(self, title: str, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "dry_run": self.config.mode != "GUARDED_WRITE",
            "operation": "append_research_log",
            "target_boundary": "Dedicated EarnsAI Notion workspace only",
            "title": title,
            "payload": payload,
            "blocked_destructive_actions": True,
        }

    def write_research_log(self, title: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.config.assert_write_allowed("append_research_log")
        raise NotImplementedError(
            "Real Notion API write is intentionally not implemented yet. "
            "Add notion-client only after schema and guard checks are approved."
        )
