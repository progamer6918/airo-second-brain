#!/usr/bin/env python3
"""Prepare a resumable temporal recovery preview. No ledger posting or approval."""

import sys, json, argparse, collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from airo_finance_core import (
    DatabaseManager,
    FinanceCoreEngine,
    GmailIntelligenceService,
)
from airo_finance_core.temporal_recovery import collect


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", required=True)
    p.add_argument("--gmail", action="store_true")
    p.add_argument("--expected-gmail")
    p.add_argument("--telegram-export")
    p.add_argument("--expected-telegram-owner")
    p.add_argument("--owner-quality-overrides")
    p.add_argument("--report")
    args = p.parse_args()
    db = DatabaseManager(args.db)
    db.init_schema()
    client = None
    try:
        if args.gmail:
            if not args.expected_gmail:
                p.error("--gmail requires --expected-gmail")
            client = GmailIntelligenceService(FinanceCoreEngine(db)).get_service()
            actual = (
                client.users().getProfile(userId="me").execute().get("emailAddress", "")
            )
            if actual.lower() != args.expected_gmail.lower():
                raise ValueError("GMAIL_IDENTITY_MISMATCH")
        exported = (
            json.loads(Path(args.telegram_export).read_text())
            if args.telegram_export
            else None
        )
        overrides = (
            json.loads(Path(args.owner_quality_overrides).read_text())
            if args.owner_quality_overrides
            else None
        )
        result = collect(
            db,
            gmail=client,
            telegram_export=exported,
            owner_overrides=overrides,
            expected_telegram_owner=args.expected_telegram_owner,
        )
        report = {
            "proposal_id": result.get("id"),
            "status": result["status"],
            "groups": dict(
                collections.Counter(i["group_name"] for i in result["items"])
            ),
            "domain_counts": dict(
                collections.Counter(i["entity"] for i in result["items"])
            ),
            "errors": [e["code"] for e in result.get("recovery_errors", [])],
            "ledger_posted": False,
            "historical_times_applied": False,
        }
        if args.report:
            Path(args.report).write_text(json.dumps(report, indent=2))
        print(json.dumps(report))
    finally:
        db.close()


if __name__ == "__main__":
    main()
