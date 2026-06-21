from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class NotionDryRunAdapter:
    """
    Dry-run only adapter.

    This does not call Notion API, does not read tokens, and does not touch a real workspace.
    It only writes the intended Notion payload to reports/ for review.
    """

    def __init__(self, reports_dir: str | Path = "reports") -> None:
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def write_research_log(self, payload: dict[str, Any]) -> dict[str, str]:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        json_path = self.reports_dir / f"notion_dry_run_{stamp}.json"
        md_path = self.reports_dir / f"notion_dry_run_{stamp}.md"

        envelope = {
            "dry_run": True,
            "target": "EarnsAI dedicated Notion workspace only",
            "operation": "create_or_update_research_log",
            "payload": payload,
        }

        json_path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False), encoding="utf-8")

        lines = [
            f"# Notion Dry Run {stamp}",
            "",
            "Status: **DRY RUN ONLY**",
            "",
            "## Target",
            "- EarnsAI dedicated Notion workspace only",
            "- No real Notion API call",
            "- No token read",
            "- No destructive action",
            "",
            "## Payload Summary",
        ]
        for key, value in payload.items():
            lines.append(f"- **{key}**: {value}")

        md_path.write_text("\n".join(lines), encoding="utf-8")

        return {
            "json": str(json_path),
            "markdown": str(md_path),
        }
