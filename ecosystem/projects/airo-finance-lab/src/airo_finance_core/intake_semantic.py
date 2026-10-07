"""Bounded, tool-free Hermes interpretation. Invalid output leaves drafts intact."""

import json, os, subprocess, sys
from pathlib import Path
from .intake_store import dump
from . import intake_parser as parser

FIELDS = {
    "note",
    "category_name",
    "subcategory_name",
    "account_id",
    "date",
    "direction",
}


def validate(service, patch, original):
    if not isinstance(patch, dict) or set(patch) - FIELDS:
        return None
    result = dict(original)
    if patch.get("account_id") and not service.engine.get_account(patch["account_id"]):
        return None
    if patch.get("direction") and patch["direction"] not in (
        "EXPENSE",
        "INCOME",
        "TRANSFER",
        "CC_PAYMENT",
    ):
        return None
    if patch.get("date") and not parser.date_in(patch["date"]):
        return None
    for k, v in patch.items():
        if not isinstance(v, str) or len(v) > 240:
            return None
        # The interpreter may propose meanings, never overwrite explicit monetary facts.
        if (
            k in ("account_id", "date", "direction")
            and result.get(k)
            and result[k] != v
        ):
            continue
        result[k] = v
    if patch.get("category_name"):
        cat = next(
            (
                c
                for c in service.engine.list_categories(active_only=True)
                if c.name.casefold() == patch["category_name"].casefold()
            ),
            None,
        )
        result["category_id"] = cat.id if cat else None
        result["proposed_category"] = None if cat else patch["category_name"]
        sub = (
            next(
                (
                    s
                    for s in service.engine.list_subcategories(cat.id, active_only=True)
                    if s.name.casefold() == patch.get("subcategory_name", "").casefold()
                ),
                None,
            )
            if cat
            else None
        )
        result["subcategory_id"] = sub.id if sub else None
        result["proposed_subcategory"] = (
            patch.get("subcategory_name") if not sub else None
        )
    result["semantic_suggestion"] = True
    result["user_labels_verified"] = False
    return result


def enrich(service, batch, text, resolver=None):
    if resolver is None and os.environ.get("AIRO_FINANCE_OFFLINE_TEST") == "1":
        return False
    rows = [r for r in service.rows(batch) if r["status"] == "DRAFT"]
    if not rows:
        return False
    from .gmail_reliability import state

    context = {
        "owner_context": state(service.db, "intake_owner_context", {}),
        "text": text,
        "drafts": [{"number": r["number"], "data": r["data"]} for r in rows],
        "accounts": [
            {"id": a.id, "name": a.name}
            for a in service.engine.list_accounts(active_only=True)
        ],
        "categories": [
            {
                "name": c.name,
                "subcategories": [
                    s.name
                    for s in service.engine.list_subcategories(c.id, active_only=True)
                ],
            }
            for c in service.engine.list_categories(active_only=True)
        ],
    }
    try:
        if resolver:
            out = resolver(context)
        else:
            executable = Path.home() / ".hermes/hermes-agent/venv/bin/python"
            if not executable.exists():
                return False
            env = dict(
                os.environ,
                HERMES_HOME=str(Path.home() / ".hermes/profiles/airo-hermes"),
                HERMES_QUIET="1",
            )
            res = subprocess.run(
                [
                    str(executable),
                    str(Path(__file__).with_name("intake_semantic_worker.py")),
                ],
                input=dump(context),
                text=True,
                capture_output=True,
                timeout=30,
                env=env,
            )
            if res.returncode:
                return False
            out = json.loads(res.stdout.split("INTAKE_JSON=")[-1].strip())
        if (
            not isinstance(out, dict)
            or set(out) != {"patches"}
            or not isinstance(out["patches"], list)
        ):
            return False
        changes = []
        for entry in out["patches"]:
            if not isinstance(entry, dict) or set(entry) != {"number", "fields"}:
                return False
            row = next((r for r in rows if r["number"] == entry["number"]), None)
            if not row:
                return False
            data = validate(service, entry["fields"], row["data"])
            if data is None:
                return False
            # Unsupported or guessed dates/accounts remain a question, not a silent default.
            data["semantic_review_required"] = True
            data["facts_confirmed"] = False
            changes.append((row, data))
        with service.db.atomic():
            for row, data in changes:
                service._update(row, data)
        return bool(changes)
    except (ValueError, TypeError, subprocess.TimeoutExpired, OSError):
        return False
