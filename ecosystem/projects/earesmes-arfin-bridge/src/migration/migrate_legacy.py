"""
Earesmes-Arfin Clarification Bridge - Legacy Migration Helper
Canonical Implementation for Gate EAB_G2_0 / Milestone M7

Converts legacy unversioned/unstructured pending items into canonical
PendingRecord format with dry-run verification support.
"""

from typing import Dict, Any, List, Tuple, Optional
try:
    from ecosystem.projects.earesmes_arfin_bridge.src.pending.pending_model import PendingRecord, PendingState
except ImportError:
    from src.pending.pending_model import PendingRecord, PendingState

def migrate_legacy_pending_item(legacy_data: Dict[str, Any], dry_run: bool = True) -> Tuple[Optional[PendingRecord], List[str]]:
    """
    Migrates a single legacy pending item dict to a canonical PendingRecord.
    Returns (PendingRecord, list_of_warnings).
    """
    warnings: List[str] = []
    
    owner_actor = legacy_data.get("user_id") or legacy_data.get("owner_actor_id") or ""
    owner_chat = legacy_data.get("chat_id") or legacy_data.get("owner_chat_id") or ""
    raw_prompt = legacy_data.get("prompt") or legacy_data.get("raw_prompt") or ""
    
    if not owner_actor:
        warnings.append("Missing owner_actor_id in legacy data")
    if not owner_chat:
        warnings.append("Missing owner_chat_id in legacy data")
        
    legacy_status = str(legacy_data.get("status", "DRAFT")).upper()
    state_map = {
        "DRAFT": PendingState.DRAFT,
        "PENDING": PendingState.PENDING_REVIEW,
        "STAGED": PendingState.STAGED,
        "APPROVED": PendingState.APPROVED,
        "POSTED": PendingState.POSTED,
        "REJECTED": PendingState.REJECTED,
        "EXPIRED": PendingState.EXPIRED,
        "CANCELLED": PendingState.CANCELLED
    }
    canonical_state = state_map.get(legacy_status, PendingState.DRAFT)
    if legacy_status not in state_map:
        warnings.append(f"Unmapped legacy status '{legacy_status}', defaulted to DRAFT")
        
    payload = legacy_data.get("payload") or legacy_data.get("parsed_payload") or {}
    legacy_id = legacy_data.get("id") or legacy_data.get("pending_id")
    
    record = PendingRecord(
        pending_id=f"pnd_{legacy_id}" if legacy_id and not str(legacy_id).startswith("pnd_") else legacy_id,
        owner_actor_id=str(owner_actor),
        owner_chat_id=str(owner_chat),
        raw_prompt=raw_prompt,
        parsed_payload=payload,
        state=canonical_state,
        pending_version=1,
        created_at=legacy_data.get("created_at"),
        updated_at=legacy_data.get("updated_at")
    )
    
    return record, warnings

def batch_migrate_legacy_items(legacy_items: List[Dict[str, Any]], dry_run: bool = True) -> Tuple[List[PendingRecord], List[Dict[str, Any]]]:
    """
    Migrates a batch of legacy items.
    Returns (list_of_migrated_records, list_of_migration_reports).
    """
    records: List[PendingRecord] = []
    reports: List[Dict[str, Any]] = []
    
    for idx, item in enumerate(legacy_items):
        rec, wrn = migrate_legacy_pending_item(item, dry_run=dry_run)
        if rec:
            records.append(rec)
        reports.append({
            "index": idx,
            "legacy_id": item.get("id"),
            "canonical_pending_id": rec.pending_id if rec else None,
            "short_ref": rec.short_ref if rec else None,
            "dry_run": dry_run,
            "warnings": wrn,
            "success": rec is not None
        })
        
    return records, reports
