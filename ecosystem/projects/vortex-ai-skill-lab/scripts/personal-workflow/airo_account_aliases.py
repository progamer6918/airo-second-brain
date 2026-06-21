#!/usr/bin/env python3
"""
AIRO account alias normalization v0.1.

Purpose:
- Normalize common user phrases into canonical finance account names.
- Keep parser behavior consistent before Google Sheets sync.

Canonical account names match Google Sheet Finance v1.1.8:
- BCA
- BLU BCA
- Mandiri
- GoPay
- ShopeePay
- Cash
- Tokopedia CC
"""

from __future__ import annotations

import re
import sys
from typing import Optional


ACCOUNT_ALIASES: dict[str, str] = {
    "bca": "BCA",
    "bank bca": "BCA",
    "blu": "BLU BCA",
    "blu bca": "BLU BCA",
    "blubca": "BLU BCA",
    "blu-bca": "BLU BCA",
    "blu_bca": "BLU BCA",
    "bank blu": "BLU BCA",
    "bank blu bca": "BLU BCA",
    "mandiri": "Mandiri",
    "bank mandiri": "Mandiri",
    "gopay": "GoPay",
    "go pay": "GoPay",
    "shopeepay": "ShopeePay",
    "shopee pay": "ShopeePay",
    "cash": "Cash",
    "tunai": "Cash",
    "uang cash": "Cash",
    "tokopedia credit card": "Tokopedia CC",
    "tokopedia cc": "Tokopedia CC",
    "cc tokopedia": "Tokopedia CC",
    "kartu kredit tokopedia": "Tokopedia CC",
}


def normalize_account_alias(value: str | None) -> Optional[str]:
    if value is None:
        return None

    raw = str(value).strip().lower()
    if not raw:
        return None

    compact = re.sub(r"[\s_\-]+", " ", raw).strip()
    no_space = compact.replace(" ", "")

    candidates = [
        raw,
        compact,
        no_space,
    ]

    for candidate in candidates:
        if candidate in ACCOUNT_ALIASES:
            return ACCOUNT_ALIASES[candidate]

    return None


def extract_account_from_text(text: str | None) -> Optional[str]:
    if text is None:
        return None

    raw = str(text).lower()

    patterns = [
        r"\bpakai\s+([a-z0-9 _-]+)",
        r"\bvia\s+([a-z0-9 _-]+)",
        r"\bdari\s+([a-z0-9 _-]+)",
        r"\bke\s+([a-z0-9 _-]+)",
    ]

    stop_words = {
        "untuk", "buat", "sebesar", "rp", "ribu", "rb", "k",
        "makan", "siang", "malam", "beli", "catat", "hari", "ini"
    }

    for pattern in patterns:
        match = re.search(pattern, raw)
        if not match:
            continue

        phrase = match.group(1).strip()
        tokens = []
        for token in re.split(r"\s+", phrase):
            if token in stop_words:
                break
            tokens.append(token)

        candidate = " ".join(tokens).strip()
        normalized = normalize_account_alias(candidate)
        if normalized:
            return normalized

        # Also check first one/two tokens for compact user inputs.
        for n in (1, 2, 3):
            partial = " ".join(tokens[:n]).strip()
            normalized = normalize_account_alias(partial)
            if normalized:
                return normalized

    # Fallback: direct substring alias scan, longest aliases first.
    for alias in sorted(ACCOUNT_ALIASES, key=len, reverse=True):
        if re.search(r"\b" + re.escape(alias) + r"\b", raw):
            return ACCOUNT_ALIASES[alias]

    # Compact fallback catches "blubca" reliably.
    compact_text = re.sub(r"[\s_\-]+", "", raw)
    for alias in sorted(ACCOUNT_ALIASES, key=len, reverse=True):
        compact_alias = re.sub(r"[\s_\-]+", "", alias)
        if compact_alias and compact_alias in compact_text:
            return ACCOUNT_ALIASES[alias]

    return None


def main() -> int:
    text = " ".join(sys.argv[1:]).strip()
    print(extract_account_from_text(text) or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
