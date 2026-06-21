#!/usr/bin/env python3
"""
AIRO Credit Card Billing Cycle v0.8.

Tokopedia Card / Tokped Card billing cycle:
- start day: 16
- end day: 15
- statement_month is the month containing billing_end.

Examples:
- 2026-04-15 -> statement_month 2026-04, cycle 2026-03-16..2026-04-15
- 2026-04-16 -> statement_month 2026-05, cycle 2026-04-16..2026-05-15
- 2026-05-15 -> statement_month 2026-05, cycle 2026-04-16..2026-05-15
- 2026-05-16 -> statement_month 2026-06, cycle 2026-05-16..2026-06-15
"""

from __future__ import annotations

import argparse
import calendar
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class BillingCycle:
    billing_cycle_id: str
    billing_start: str
    billing_end: str
    statement_month: str
    card_name: str = "TOKPED_CC"


def add_month(year: int, month: int, delta: int = 1) -> tuple[int, int]:
    month_index = (year * 12 + (month - 1)) + delta
    return month_index // 12, month_index % 12 + 1


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def compute_tokped_card_billing_cycle(transaction_date: str | date) -> BillingCycle:
    if isinstance(transaction_date, str):
        tx_date = parse_date(transaction_date)
    else:
        tx_date = transaction_date

    if tx_date.day >= 16:
        start = date(tx_date.year, tx_date.month, 16)
        end_year, end_month = add_month(tx_date.year, tx_date.month, 1)
        end = date(end_year, end_month, 15)
    else:
        end = date(tx_date.year, tx_date.month, 15)
        start_year, start_month = add_month(tx_date.year, tx_date.month, -1)
        start = date(start_year, start_month, 16)

    statement_month = f"{end.year:04d}-{end.month:02d}"
    billing_cycle_id = f"TOKPED_CC_{statement_month}"

    return BillingCycle(
        billing_cycle_id=billing_cycle_id,
        billing_start=start.isoformat(),
        billing_end=end.isoformat(),
        statement_month=statement_month,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Tokopedia Card billing cycle.")
    parser.add_argument("date", help="Transaction date in YYYY-MM-DD format.")
    args = parser.parse_args()

    result = compute_tokped_card_billing_cycle(args.date)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
