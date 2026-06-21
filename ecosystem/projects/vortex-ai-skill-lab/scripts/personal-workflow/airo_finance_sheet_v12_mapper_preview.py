#!/usr/bin/env python3
"""AIRO Finance Sheet v1.2 mapper preview.

Unified read-only mapper for planner-ready Google Sheet Finance routes.

No credential read, no SQLite mutation, no Google write, no OpenClaw restart.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import pathlib
import sys
from typing import Any

REPO = pathlib.Path(__file__).resolve().parents[2]


def load_module(name: str, relative_path: str):
    path = REPO / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load {}".format(relative_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


review_mod = load_module("airo_review_queue_planner", "scripts/personal-workflow/airo_review_queue_planner.py")
cash_mod = load_module("airo_cash_ledger_planner", "scripts/personal-workflow/airo_cash_ledger_planner.py")
cicilan_mod = load_module("airo_cicilan_rumah_planner", "scripts/personal-workflow/airo_cicilan_rumah_planner.py")
hutang_mod = load_module("airo_hutang_planner", "scripts/personal-workflow/airo_hutang_planner.py")


def normalize_text(raw_text: str) -> str:
    return " ".join(raw_text.strip().lower().split())


def select_domain(raw_text: str) -> str:
    text = normalize_text(raw_text)

    # Treat cash/tunai purchase-like phrases as normal core transactions,
    # not as Cash Ledger intent. Example:
    # "cash beli minum 12345 hari ini" => review_or_core/core expense path.
    has_cash_account = bool(re.search(r"\b(cash|tunai)\b", text))
    has_amount = bool(re.search(r"\b\d+[.,]?\d*\s*(rb|ribu|k|jt|juta)?\b", text))
    has_purchase_verb = bool(re.search(
        r"\b(beli|bayar|jajan|makan|minum|kopi|sarapan|lunch|dinner|belanja|checkout)\b",
        text,
    ))

    if has_cash_account and has_purchase_verb and has_amount:
        return "review_or_core"

    if "cash" in text or "tunai" in text:
        return "cash_ledger"
    if "cicilan rumah" in text or "kpr" in text or "angsuran rumah" in text:
        return "cicilan_rumah"
    if "hutang" in text or "utang" in text:
        return "hutang"
    return "review_or_core"


def core_targets_for(target_tab: str) -> list[str]:
    if target_tab == "💳 Credit Card":
        return ["💸 Transactions", "💳 Credit Card"]
    if target_tab == "🥇 Aset":
        return ["💸 Transactions", "🥇 Aset"]
    if target_tab == "💸 Transactions":
        return ["💸 Transactions"]
    if target_tab == "🧾 Review Queue":
        return ["🧾 Review Queue"]
    return [target_tab]


def mapper_preview(raw_text: str, confidence: float = 0.95, source: str = "telegram") -> dict[str, Any]:
    domain = select_domain(raw_text)

    if domain == "cash_ledger":
        plan = cash_mod.plan_cash_ledger(raw_text, source=source)
    elif domain == "cicilan_rumah":
        plan = cicilan_mod.plan_cicilan_rumah(raw_text, source=source)
    elif domain == "hutang":
        plan = hutang_mod.plan_hutang(raw_text, source=source)
    else:
        plan = review_mod.plan_review_queue(raw_text, confidence=confidence, source=source)

    target_tab = plan["target_tab"]
    core_targets = core_targets_for(target_tab)

    if plan["route_to_review"]:
        mapper_operation = "review_queue_preview_candidate"
    elif target_tab in {"💵 Cash Ledger", "🏠 Cicilan Rumah", "🤝 Hutang"}:
        mapper_operation = "planner_tab_preview_candidate"
    else:
        mapper_operation = "existing_core_route_preview"

    return {
        "mapper": "airo_finance_sheet_v12_mapper_preview",
        "google_write_performed": False,
        "sqlite_mutation_performed": False,
        "credential_read_performed": False,
        "openclaw_restart_performed": False,
        "raw_text": raw_text,
        "source": source,
        "selected_domain": domain,
        "mapper_operation": mapper_operation,
        "target_tab": target_tab,
        "target_tabs": core_targets,
        "route_to_review": plan["route_to_review"],
        "planner": plan["planner"],
        "planner_operation": plan["operation"],
        "duplicate_key": plan["duplicate_key"],
        "normalized": plan["normalized"],
        "ambiguity_reasons": plan["ambiguity_reasons"],
        "plan": plan,
        "next_action": "dry_run_write_preview_only",
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "AIRO Finance Sheet v1.2 Mapper Preview",
        "Mapper operation: {}".format(payload["mapper_operation"]),
        "Selected domain: {}".format(payload["selected_domain"]),
        "Target tab: {}".format(payload["target_tab"]),
        "Target tabs: {}".format(", ".join(payload["target_tabs"])),
        "Route to review: {}".format(payload["route_to_review"]),
        "Planner: {}".format(payload["planner"]),
        "Planner operation: {}".format(payload["planner_operation"]),
        "Duplicate key: {}".format(payload["duplicate_key"]),
        "",
        "Ambiguity reasons:",
    ]
    reasons = payload["ambiguity_reasons"]
    if reasons:
        lines.extend("- {}".format(reason) for reason in reasons)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "Next action: {}".format(payload["next_action"]),
        "Safety: no Google write, no SQLite mutation, no credential read, no OpenClaw restart",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview AIRO Finance Sheet v1.2 planner mapping.")
    parser.add_argument("message")
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--source", default="telegram")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = mapper_preview(args.message, confidence=args.confidence, source=args.source)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
