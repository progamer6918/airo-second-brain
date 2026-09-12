"""
EARESMES Project Continuity Capability — P1.4
=============================================
Enables resuming work from last known position without repeating context.
Priority order:
  1. state/active-session.md (Current working position)
  2. CURRENT.md (Canonical snapshot)
  3. latest receipts (Execution evidence)
  4. decisions/decision-log.md (Historical reasoning)

Upholds Core Principle:
  Continuity ≠ Autonomy.
  Provides structured state recovery and next logical step recommendation.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import json


def get_latest_receipt_details(repo_root: Path) -> Optional[Dict[str, Any]]:
    """Read most recent receipt JSON from earesmes/state/receipts/."""
    receipts_dir = repo_root / "earesmes" / "state" / "receipts"
    if not receipts_dir.is_dir():
        return None

    receipts = sorted(receipts_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not receipts:
        return None

    try:
        data = json.loads(receipts[0].read_text(encoding="utf-8", errors="replace"))
        return {
            "file": receipts[0].name,
            "job_id": data.get("job_id", "unknown"),
            "status": data.get("final_status", data.get("status", "unknown")),
            "detail": data.get("detail", data.get("_runner_exec_detail", "")),
        }
    except Exception:
        return None


def parse_active_session(repo_root: Path) -> Dict[str, str]:
    """Parse state/active-session.md into structured key-value pairs."""
    session_file = repo_root / "state" / "active-session.md"
    if not session_file.exists():
        return {}

    text = session_file.read_text(encoding="utf-8", errors="replace")
    fields: Dict[str, str] = {}
    current_key = None
    buf = []

    for line in text.splitlines():
        line_s = line.strip()
        if line_s.startswith("###"):
            fields["title"] = line_s.replace("#", "").strip()
        elif line_s.startswith("**") and line_s.endswith("**"):
            if current_key and buf:
                fields[current_key] = " ".join(buf).strip()
                buf = []
            current_key = line_s.replace("*", "").strip()
        elif current_key and line_s:
            if not line_s.startswith("→"):
                buf.append(line_s)

    if current_key and buf:
        fields[current_key] = " ".join(buf).strip()

    return fields


def parse_current_md(repo_root: Path) -> Dict[str, str]:
    """Extract baseline snapshot from CURRENT.md."""
    current_file = repo_root / "CURRENT.md"
    if not current_file.exists():
        return {}

    text = current_file.read_text(encoding="utf-8", errors="replace")
    data = {}
    for line in text.splitlines():
        line_s = line.strip()
        if "Current ASB target:" in line_s:
            data["target"] = line_s.split(":", 1)[1].strip()
        elif "Final milestone:" in line_s:
            data["milestone"] = line_s.split(":", 1)[1].strip()
        elif "v0.6 status:" in line_s:
            data["status"] = line_s.split(":", 1)[1].strip()
    return data


def format_new_chat_handoff(repo_root: Path) -> str:
    """
    Format concise bootstrap summary for handing off context to a new session/chat.
    """
    session = parse_active_session(repo_root)
    current = parse_current_md(repo_root)
    latest_rec = get_latest_receipt_details(repo_root)

    objective = session.get("Yang Saya Minta", "Menjaga kontinuitas ekosistem AIRO dan mengoperasikan asisten personal Earesmes.")
    completed = session.get("Progress Terakhir", current.get("milestone", "Milestone v0.6 Selesai"))
    position = session.get("Lagi di", "VPS Workbench active")
    next_step = session.get("Berikutnya", "Melanjutkan eksekusi langkah berikutnya sesuai rencana.")

    recent_exec_note = f" (Receipt terakhir: {latest_rec['job_id']} - {latest_rec['status']})" if latest_rec else ""

    return (
        "AIRO CONTINUITY HANDOFF\n\n"
        f"Current Objective:\n{objective}\n\n"
        f"Completed:\n{completed}\n\n"
        "Important Decisions:\n"
        "• ASB adalah Shared Canonical Knowledge Base / AIRO Kernel.\n"
        "• Earesmes bertindak sebagai AIRO Personal Assistant Agent (Decision Support & Continuity, bukan Decision Maker).\n"
        "• Owner memegang kewenangan final penuh atas setiap mutasi dan persetujuan.\n\n"
        f"Current Position:\n{position}{recent_exec_note}\n\n"
        f"Next Step:\n{next_step}"
    )


def resolve_project_continuity(repo_root: Path, query: str) -> str:
    """
    Build continuity status from ASB canonical sources.
    Handles standard continuity, new chat handoff, and stale state detection.
    """
    q = query.lower().strip()

    # 1. Use Case 3: New Chat Handoff
    if any(k in q for k in ["ringkas supaya chat baru paham", "handoff chat baru", "bootstrap chat baru", "ringkasan chat baru"]):
        return format_new_chat_handoff(repo_root)

    # 2. Check for missing state safety (Test 4)
    session_file = repo_root / "state" / "active-session.md"
    current_file = repo_root / "CURRENT.md"
    if not session_file.exists() and not current_file.exists():
        return (
            "🧭 AIRO CONTINUITY\n\n"
            "Status:\n"
            "Context tidak tersedia. Dokumen kanonikal state/active-session.md dan CURRENT.md belum ditemukan di workspace ini. "
            "Earesmes tidak dapat melakukan recovery posisi tanpa data kanonikal pendukung."
        )

    session = parse_active_session(repo_root)
    current = parse_current_md(repo_root)
    latest_rec = get_latest_receipt_details(repo_root)

    project_name = session.get("title", "AIRO Ecosystem")
    last_known_state = current.get("target", "AIRO Second Brain v0.6 (COMPLETE)")
    completed = session.get("Progress Terakhir", "Belum ada catatan pekerjaan selesai terbaru.")
    active = session.get("Lagi di", "Sesi aktif belum terdefinisi.")
    blocker = session.get("Hambatan", "Tidak ada blocker aktif.")
    next_step = session.get("Berikutnya", "Menunggu arahan Owner untuk melanjutkan pekerjaan.")

    # 3. Check for stale state / conflicting information (Test 5)
    conflict_notes = []
    if latest_rec:
        rec_status = latest_rec.get("status", "").lower()
        if "failed" in rec_status and "tidak ada blocker" in blocker.lower():
            conflict_notes.append(
                f"Catatan Inkonsistensi: active-session mencatat tidak ada blocker, namun receipt terbaru ({latest_rec['job_id']}) "
                f"berstatus [{latest_rec['status'].upper()}]: {latest_rec.get('detail', '')}"
            )

    conflict_section = ("\n\n⚠️ State Conflict:\n" + "\n".join(conflict_notes)) if conflict_notes else ""

    # 4. Standard Continuity Format
    return (
        "🧭 AIRO CONTINUITY\n\n"
        f"Project:\n{project_name}\n\n"
        f"Last Known State:\n{last_known_state}\n\n"
        f"Completed:\n{completed}\n\n"
        f"Active:\n{active}\n\n"
        f"Blocker:\n{blocker}\n\n"
        f"Next Suggested Step:\n{next_step}"
        f"{conflict_section}"
    )
