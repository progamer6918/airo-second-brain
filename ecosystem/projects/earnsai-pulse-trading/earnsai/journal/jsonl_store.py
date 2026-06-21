from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from earnsai.common.config import get_config


def write_json(path: str | Path, data: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {}
    return json.loads(target.read_text(encoding="utf-8"))


def append_jsonl(path: str | Path, record: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    enriched = {"journaled_at": datetime.now(timezone.utc).isoformat(), **record}
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(enriched, sort_keys=True) + "\n")


def append_decision(record: dict[str, Any], path: str | Path | None = None) -> None:
    cfg = get_config()
    append_jsonl(path or cfg.journal_path, record)


def read_jsonl(path: str | Path, limit: int = 20) -> list[dict[str, Any]]:
    target = Path(path)
    if not target.exists():
        return []

    rows: list[dict[str, Any]] = []
    with target.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    if limit <= 0:
        return rows
    return rows[-limit:]
