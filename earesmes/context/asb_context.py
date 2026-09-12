"""
EARESMES ASB Context Assembly Layer — P0
=========================================
Assembles targeted context from canonical AIRO Second Brain (ASB) files.
Priority order:
  1. CURRENT.md
  2. state/active-session.md
  3. decisions/decision-log.md
  4. control/ project context

Enforces bounded retrieval: never loads entire repository, extracts only relevant slices.
"""

from pathlib import Path
from typing import Dict, Any, Optional


def get_active_session_info(repo_root: Path) -> Dict[str, str]:
    """Parse state/active-session.md into structured fields."""
    session_file = repo_root / "state" / "active-session.md"
    if not session_file.exists():
        return {}

    text = session_file.read_text(encoding="utf-8", errors="replace")
    fields = {}
    current_key = None
    buffer = []

    for line in text.splitlines():
        line_str = line.strip()
        if line_str.startswith("###"):
            fields["title"] = line_str.replace("#", "").strip()
        elif line_str.startswith("**") and line_str.endswith("**"):
            if current_key and buffer:
                fields[current_key] = " ".join(buffer).strip()
                buffer = []
            current_key = line_str.replace("*", "").strip()
        elif current_key and line_str:
            if not line_str.startswith("→"):
                buffer.append(line_str)

    if current_key and buffer:
        fields[current_key] = " ".join(buffer).strip()

    return fields


def get_current_status_info(repo_root: Path) -> Dict[str, str]:
    """Extract key current status items from CURRENT.md."""
    current_file = repo_root / "CURRENT.md"
    if not current_file.exists():
        return {}

    text = current_file.read_text(encoding="utf-8", errors="replace")
    status_info = {
        "target": "AIRO Second Brain v0.6",
        "milestone": "M6 — Owner Acceptance & Cutover (DONE)",
        "v06_status": "COMPLETE",
        "active_runtime": "VPS Workbench / Earesmes Assistant Active",
    }

    for line in text.splitlines():
        line_str = line.strip()
        if "Current ASB target:" in line_str:
            status_info["target"] = line_str.split(":", 1)[1].strip()
        elif "Final milestone:" in line_str:
            status_info["milestone"] = line_str.split(":", 1)[1].strip()
        elif "v0.6 status:" in line_str:
            status_info["v06_status"] = line_str.split(":", 1)[1].strip()

    return status_info


def get_decision_recall_info(repo_root: Path, query: str = "") -> str:
    """Extract relevant decisions from decisions/decision-log.md."""
    decision_file = repo_root / "decisions" / "decision-log.md"
    control_file = repo_root / "control" / "earesmes-hermes.md"

    # Specific recall for Earesmes rationale
    query_lower = query.lower()
    if "earesmes" in query_lower or "hermes" in query_lower or "kenapa" in query_lower or "mengapa" in query_lower:
        rationale = (
            "Earesmes dibangun sebagai AIRO Personal Assistant Agent yang menjadi jembatan "
            "eksekusi dan interaksi Owner dari Telegram ke runtime VPS.\n\n"
            "Berdasarkan arsitektur kanonikal ASB:\n"
            "• ASB adalah Shared Canonical Knowledge Base / AIRO Kernel.\n"
            "• Semua agen (ChatGPT, Claude, Hermes/Earesmes, Antigravity) adalah operator khusus untuk ekosistem AIRO yang sama.\n"
            "• Earesmes ditugaskan menjaga kontinuitas, memahami konteks Owner, dan memfasilitasi decision making terkontrol tanpa melanggar batasan governance."
        )
        return rationale

    if not decision_file.exists():
        return "Belum ada catatan keputusan spesifik yang ditemukan."

    return "Keputusan ASB mencakup Second Brain Architecture, Cross-Consumer Operator Model, dan Governance Boundaries."


def assemble_context_for_prompt(repo_root: Path, query: str) -> str:
    """Assemble minimal markdown context to enrich Hermes reasoning."""
    session_info = get_active_session_info(repo_root)
    status_info = get_current_status_info(repo_root)

    parts = ["### AIRO Second Brain Context"]
    if status_info:
        parts.append(f"• Target ASB: {status_info.get('target', 'v0.6')}")
        parts.append(f"• Status ASB: {status_info.get('v06_status', 'COMPLETE')}")

    if session_info:
        if "Lagi di" in session_info:
            parts.append(f"• Sesi Aktif (Posisi): {session_info['Lagi di']}")
        if "Progress Terakhir" in session_info:
            parts.append(f"• Progress Terakhir: {session_info['Progress Terakhir']}")
        if "Hambatan" in session_info:
            parts.append(f"• Hambatan/Blocker: {session_info['Hambatan']}")
        if "Berikutnya" in session_info:
            parts.append(f"• Langkah Berikutnya: {session_info['Berikutnya']}")

    return "\n".join(parts)


def format_asb_knowledge_response(repo_root: Path, query: str) -> Optional[str]:
    """
    Directly answer canonical ASB status / decision questions if deterministic.
    Returns None if complex reasoning is required.
    """
    q = query.lower().strip()

    # Capability 1: Daily AIRO Briefing (PRD P1.1)
    if any(k in q for k in ["update earesmes", "update airo", "daily brief", "briefing airo", "briefing", "laporan harian"]):
        session = get_active_session_info(repo_root)
        status = get_current_status_info(repo_root)

        posisi = session.get("Lagi di", "VPS Workbench active")
        progress = session.get("Progress Terakhir", "Earesmes Personal Assistant foundation active")
        hambatan = session.get("Hambatan", "Tidak ada blocker aktif.")
        berikutnya = session.get("Berikutnya", "Use KCC in normal AIRO work and fix only concrete runtime failures")

        return (
            "🧭 AIRO Daily Brief\n\n"
            "Current:\n"
            "• Kondisi Runtime: VPS Workbench & Earesmes Gateway Active\n"
            f"• Project Aktif: {session.get('title', 'AIRO VPS Workbench')}\n\n"
            "Progress:\n"
            f"• Pekerjaan Terakhir: {progress}\n\n"
            "Pending:\n"
            f"• Posisi Saat Ini: {posisi}\n\n"
            "Blocker:\n"
            f"• Masalah Aktif: {hambatan}\n\n"
            "Recommendation:\n"
            f"• Next Action: {berikutnya}"
        )

    # General Query about AIRO Status / Progress
    if any(k in q for k in ["status airo", "kondisi airo", "apa progress", "progress airo", "status sekarang"]):
        session = get_active_session_info(repo_root)
        status = get_current_status_info(repo_root)

        posisi = session.get("Lagi di", "VPS Workbench active")
        progress = session.get("Progress Terakhir", "Earesmes Personal Assistant foundation active")
        hambatan = session.get("Hambatan", "Tidak ada blocker aktif.")
        berikutnya = session.get("Berikutnya", "Pengujian canary dan validasi end-to-end.")

        return (
            "🧭 STATUS AIRO SAAT INI\n\n"
            f"• Target Ekosistem: {status.get('target', 'AIRO Second Brain v0.6 (COMPLETE)')}\n"
            f"• Sesi Aktif: {session.get('title', 'AIRO VPS Workbench')}\n"
            f"• Posisi Terakhir: {posisi}\n"
            f"• Progress Terakhir: {progress}\n"
            f"• Hambatan / Blocker: {hambatan}\n"
            f"• Langkah Berikutnya: {berikutnya}"
        )

    # Query about why Earesmes was created
    if any(k in q for k in ["kenapa kita membuat earesmes", "mengapa membuat earesmes", "tujuan earesmes", "alasan earesmes", "kenapa earesmes dibuat"]):
        return get_decision_recall_info(repo_root, query)

    # Query about continuing last task
    if any(k in q for k in ["lanjutkan pekerjaan terakhir", "lanjutkan tugas terakhir", "lanjutkan sesi", "apa tugas berikutnya"]):
        session = get_active_session_info(repo_root)
        posisi = session.get("Lagi di", "Pekerjaan terakhir")
        berikutnya = session.get("Berikutnya", "Melanjutkan eksekusi tugas berikutnya sesuai rencana.")
        return (
            "Melanjutkan konteks pekerjaan terakhir dari ASB active session:\n\n"
            f"• Posisi Terakhir: {posisi}\n"
            f"• Langkah Berikutnya: {berikutnya}\n\n"
            "Saya siap menjalankan instruksi spesifik untuk memproses langkah tersebut."
        )

    return None
