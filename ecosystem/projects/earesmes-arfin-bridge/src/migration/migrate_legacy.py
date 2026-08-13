# -*- coding: utf-8 -*-
"""
ecosystem/projects/earesmes-arfin-bridge/src/migration/migrate_legacy.py
Migration & Backfill Helper for Legacy Arfin Single-Pending Pointer to Multi-Pending Registry.
Dry-run idempotent tooling.
"""

from typing import Dict, Any, List

def migrate_legacy_pending(legacy_data: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
    if not legacy_data:
        return {"migrated": 0, "items": []}
    
    return {
        "migrated": 1 if legacy_data.get("amount") else 0,
        "dry_run": dry_run,
        "items": [legacy_data] if legacy_data.get("amount") else []
    }
